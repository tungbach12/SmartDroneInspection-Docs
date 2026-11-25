#!/usr/bin/env node
// Inspect, validate, extract, pack, and open draw.io diagram XML directly in app.diagrams.net.
// Usage:
//   node drawio.mjs info <file> [--json] [--verbose]
//   node drawio.mjs check <file> [--json] [--verbose]
//   node drawio.mjs extract <file> --page <name|id|index> [--json]
//   node drawio.mjs open <file> [--port <port>] [--no-launch]
//   node drawio.mjs url <file>
//   node drawio.mjs pack <xml-file>

import { spawn } from "node:child_process";
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import zlib from "node:zlib";

const BOOLEAN_FLAGS = new Set(["verbose", "json", "no-launch"]);

function parseArgs(argv) {
  const positionals = [];
  const flags = {};
  for (let i = 0; i < argv.length; i++) {
    if (!argv[i].startsWith("--")) {
      positionals.push(argv[i]);
      continue;
    }
    const key = argv[i].slice(2);
    const next = argv[i + 1];
    if (!BOOLEAN_FLAGS.has(key) && next !== undefined && !next.startsWith("--")) {
      flags[key] = next;
      i++;
    } else {
      flags[key] = true;
    }
  }
  const [command, file] = positionals;
  return { command, file, flags };
}

function decodeEntities(value) {
  return value
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&amp;/g, "&");
}

function parseXml(xml) {
  const errors = [];
  const doc = { name: "#document", attrs: {}, children: [], text: "", start: 0, end: xml.length };
  const stack = [doc];
  const top = () => stack[stack.length - 1] ?? doc;
  const n = xml.length;
  let i = 0;

  while (i < n) {
    const lt = xml.indexOf("<", i);
    if (lt === -1) {
      if (xml.slice(i).trim()) top().text += xml.slice(i);
      break;
    }
    if (lt > i) top().text += xml.slice(i, lt);

    if (xml.startsWith("<!--", lt)) {
      const end = xml.indexOf("-->", lt + 4);
      if (end === -1) {
        errors.push(`unterminated comment at offset ${lt}`);
        break;
      }
      i = end + 3;
      continue;
    }
    if (xml.startsWith("<![CDATA[", lt)) {
      const end = xml.indexOf("]]>", lt + 9);
      if (end === -1) {
        errors.push(`unterminated CDATA at offset ${lt}`);
        break;
      }
      top().text += xml.slice(lt + 9, end);
      i = end + 3;
      continue;
    }
    if (xml.startsWith("<?", lt)) {
      const end = xml.indexOf("?>", lt + 2);
      if (end === -1) {
        errors.push(`unterminated processing instruction at offset ${lt}`);
        break;
      }
      i = end + 2;
      continue;
    }
    if (xml.startsWith("<!", lt)) {
      let j = lt + 2;
      let depth = 0;
      while (j < n) {
        const c = xml[j];
        if (c === "[") depth++;
        else if (c === "]") depth--;
        else if (c === ">" && depth <= 0) break;
        j++;
      }
      i = j + 1;
      continue;
    }

    let j = lt + 1;
    let quote = null;
    while (j < n) {
      const c = xml[j];
      if (quote) {
        if (c === quote) quote = null;
      } else if (c === '"' || c === "'") {
        quote = c;
      } else if (c === ">") {
        break;
      }
      j++;
    }
    if (j >= n) {
      errors.push(`unterminated tag at offset ${lt}`);
      break;
    }

    let body = xml.slice(lt + 1, j);
    const tagStart = lt;
    i = j + 1;

    if (body.startsWith("/")) {
      const name = body.slice(1).trim();
      const node = stack.pop();
      if (!node || node.name !== name) {
        errors.push(`mismatched closing tag </${name}> at offset ${lt}`);
        let current = node;
        while (current && current.name !== name) current = stack.pop();
      } else {
        node.end = i;
      }
      continue;
    }

    let selfClosing = false;
    if (body.endsWith("/")) {
      selfClosing = true;
      body = body.slice(0, -1).trimEnd();
    }
    const nameMatch = /^([^\s/>]+)/.exec(body);
    if (!nameMatch) {
      errors.push(`missing element name at offset ${lt}`);
      continue;
    }
    const attrs = {};
    const attrRe = /([^\s=/>]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/g;
    let match;
    while ((match = attrRe.exec(body)) !== null) {
      const rawVal = match[2] !== undefined ? match[2] : (match[3] ?? "");
      if (rawVal.includes("<")) {
        errors.push(`unescaped "<" in attribute ${match[1]} near offset ${lt}`);
      }
      if (/&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)/.test(rawVal)) {
        errors.push(`unescaped "&" in attribute ${match[1]} near offset ${lt}`);
      }
      attrs[match[1]] = decodeEntities(rawVal);
    }

    const node = { name: nameMatch[1], attrs, children: [], text: "", start: tagStart, end: i };
    top().children.push(node);
    if (!selfClosing) stack.push(node);
  }

  if (stack.length > 1) errors.push(`unclosed element <${top().name}>`);
  return { doc, errors };
}

function decompressDiagram(text) {
  const compact = text.replace(/\s+/g, "");
  const bytes = Buffer.from(compact, "base64");
  let xml;
  try {
    xml = zlib.inflateRawSync(bytes).toString("utf8");
  } catch {
    xml = zlib.inflateSync(bytes).toString("utf8");
  }
  return decodeURIComponent(xml);
}

function compressDiagram(xml) {
  const encoded = Buffer.from(encodeURIComponent(xml), "utf8");
  return zlib.deflateRawSync(encoded).toString("base64");
}

function child(node, name) {
  return node.children.find((c) => c.name === name);
}

function collectCells(rootEl) {
  if (!rootEl) return [];
  return rootEl.children.filter((c) => c.name === "mxCell");
}

function num(value, fallback = 0) {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function analyzeModel(model, where, verbose = false) {
  const errors = [];
  const warnings = [];
  const rootEl = child(model, "root");
  if (!rootEl) {
    errors.push(`${where}: missing <root>`);
    return { errors, warnings, stats: { cells: 0, vertices: 0, edges: 0, bounds: null } };
  }

  const cells = collectCells(rootEl);
  const ids = new Map();
  for (const cell of cells) {
    const id = cell.attrs.id;
    if (!id) {
      errors.push(`${where}: mxCell without id`);
      continue;
    }
    if (ids.has(id)) errors.push(`${where}: duplicate id "${id}"`);
    ids.set(id, cell);
  }

  for (const required of ["0", "1"]) {
    if (!ids.has(required)) warnings.push(`${where}: missing root cell id="${required}"`);
  }

  let vertices = 0;
  let edges = 0;
  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;

  const boxes = [];
  const boxMap = new Map();
  const straightEdges = [];
  for (const cell of cells) {
    const id = cell.attrs.id ?? "?";
    const parent = cell.attrs.parent;
    if (parent && !ids.has(parent)) errors.push(`${where}: cell "${id}" has missing parent "${parent}"`);

    const isVertex = cell.attrs.vertex === "1";
    const isEdge = cell.attrs.edge === "1";
    const geometry = child(cell, "mxGeometry");

    if (isVertex) {
      vertices++;
      if (!geometry) {
        errors.push(`${where}: vertex "${id}" has no <mxGeometry>`);
      } else {
        for (const key of ["x", "y", "width", "height"]) {
          if (geometry.attrs[key] === undefined && verbose) {
            warnings.push(`${where}: vertex "${id}" geometry missing ${key}`);
          }
        }
        const x = num(geometry.attrs.x);
        const y = num(geometry.attrs.y);
        const w = num(geometry.attrs.width);
        const h = num(geometry.attrs.height);
        minX = Math.min(minX, x);
        minY = Math.min(minY, y);
        maxX = Math.max(maxX, x + w);
        maxY = Math.max(maxY, y + h);
        const style = cell.attrs.style || "";
        const isContainer = /\b(swimlane|group)\b/.test(style) || style.startsWith("text;");
        const isBorderlessFrame =
          !isContainer &&
          geometry.attrs.x !== undefined &&
          geometry.attrs.y !== undefined &&
          w >= 12 &&
          h >= 12 &&
          !geometry.attrs.relative;
        if (verbose && isBorderlessFrame) {
          const b = { id, parent: parent || "", x, y, x2: x + w, y2: y + h };
          boxes.push(b);
          boxMap.set(id, b);
        }
      }
    }

    if (isEdge) {
      edges++;
      for (const key of ["source", "target"]) {
        const ref = cell.attrs[key];
        if (!ref && verbose) warnings.push(`${where}: edge "${id}" has no ${key}`);
        else if (ref && !ids.has(ref)) errors.push(`${where}: edge "${id}" ${key} "${ref}" does not exist`);
      }
      if (!geometry && verbose) warnings.push(`${where}: edge "${id}" has no <mxGeometry>`);
      const style = cell.attrs.style || "";
      const hasWaypoints = geometry && child(geometry, "Array");
      if (verbose && !hasWaypoints && style.includes("edgeStyle=none") && cell.attrs.source && cell.attrs.target) {
        straightEdges.push({ id, source: cell.attrs.source, target: cell.attrs.target, style });
      }
    }
  }

  const contains = (outer, inner) =>
    outer.x <= inner.x && outer.y <= inner.y && outer.x2 >= inner.x2 && outer.y2 >= inner.y2;

  for (let i = 0; i < boxes.length; i++) {
    for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i];
      const b = boxes[j];
      if (a.parent !== b.parent) continue;
      if (contains(a, b) || contains(b, a)) continue;
      const ox = Math.min(a.x2, b.x2) - Math.max(a.x, b.x);
      const oy = Math.min(a.y2, b.y2) - Math.max(a.y, b.y);
      if (ox > 10 && oy > 10) {
        warnings.push(`${where}: vertices "${a.id}" and "${b.id}" overlap (${Math.round(ox)}x${Math.round(oy)}px)`);
      }
    }
  }

  const getPort = (box, style, prefix, defX, defY) => {
    const px = new RegExp(`${prefix}X=([0-9.]+)`).exec(style);
    const py = new RegExp(`${prefix}Y=([0-9.]+)`).exec(style);
    const fx = px ? Number.parseFloat(px[1]) : defX;
    const fy = py ? Number.parseFloat(py[1]) : defY;
    return { x: box.x + (box.x2 - box.x) * fx, y: box.y + (box.y2 - box.y) * fy };
  };

  const segHitsRect = (p1, p2, r) => {
    let t0 = 0;
    let t1 = 1;
    const dx = p2.x - p1.x;
    const dy = p2.y - p1.y;
    for (const [p, q] of [
      [-dx, p1.x - (r.x + 2)],
      [dx, r.x2 - 2 - p1.x],
      [-dy, p1.y - (r.y + 2)],
      [dy, r.y2 - 2 - p1.y],
    ]) {
      if (Math.abs(p) < 1e-9) {
        if (q < 0) return false;
      } else {
        const t = q / p;
        if (p < 0) t0 = Math.max(t0, t);
        else t1 = Math.min(t1, t);
        if (t0 > t1) return false;
      }
    }
    return t0 <= t1;
  };

  for (const edge of straightEdges) {
    const sb = boxMap.get(edge.source);
    const tb = boxMap.get(edge.target);
    if (!sb || !tb) continue;
    const p1 = getPort(sb, edge.style, "exit", 0.5, 0.5);
    const p2 = getPort(tb, edge.style, "entry", 0.5, 0.5);
    for (const b of boxes) {
      if (b.id === sb.id || b.id === tb.id || contains(b, sb) || contains(b, tb)) continue;
      if (segHitsRect(p1, p2, b)) {
        warnings.push(`${where}: edge "${edge.id}" crosses vertex "${b.id}"`);
      }
    }
  }

  const bounds =
    vertices > 0 && Number.isFinite(minX)
      ? { x: minX, y: minY, width: maxX - minX, height: maxY - minY }
      : null;

  return { errors, warnings, stats: { cells: cells.length, vertices, edges, bounds } };
}

function collectPages(xml) {
  const { doc, errors } = parseXml(xml);
  const parserErrors = [...errors];
  const root = doc.children[0];
  const pages = [];

  if (!root) {
    return { pages, parserErrors: [...parserErrors, "empty document"] };
  }

  const addPage = (node, index) => {
    const name = node.attrs.name || `Page-${index + 1}`;
    const id = node.attrs.id || "";
    let model = child(node, "mxGraphModel");
    let modelXml = null;
    let pageErrors = [];

    if (model) {
      modelXml = xml.slice(model.start, model.end);
    } else {
      const payload = node.text.trim();
      if (!payload) {
        pageErrors.push(`page "${name}": empty diagram`);
      } else {
        try {
          const decoded = decompressDiagram(payload);
          const parsed = parseXml(decoded);
          pageErrors = parsed.errors;
          model = child(parsed.doc, "mxGraphModel") ?? child(parsed.doc, "diagram");
          if (!model) pageErrors.push(`page "${name}": decoded payload has no <mxGraphModel>`);
          else modelXml = decoded.slice(model.start, model.end);
        } catch (error) {
          pageErrors.push(`page "${name}": cannot decode compressed payload (${error.message})`);
        }
      }
    }

    pages.push({ index, name, id, model, modelXml, errors: pageErrors });
  };

  if (root.name === "mxfile") {
    root.children.filter((c) => c.name === "diagram").forEach(addPage);
  } else if (root.name === "diagram") {
    addPage(root, 0);
  } else if (root.name === "mxGraphModel") {
    const name = "Page-1";
    pages.push({
      index: 0,
      name,
      id: "",
      model: root,
      modelXml: xml.slice(root.start, root.end),
      errors: [],
    });
  } else {
    parserErrors.push(`unexpected root element <${root.name}>`);
  }

  return { pages, parserErrors };
}

function report(file, xml, flags) {
  const { pages, parserErrors } = collectPages(xml);
  const compressed = /<diagram[^>]*>\s*[A-Za-z0-9+/=\s]{40,}/.test(xml);
  const results = [];

  for (const page of pages) {
    const where = `page ${page.index + 1} "${page.name}"${page.id ? ` [${page.id}]` : ""}`;
    const analysis = page.model
      ? analyzeModel(page.model, where, Boolean(flags.verbose))
      : { errors: [], warnings: [], stats: { cells: 0, vertices: 0, edges: 0, bounds: null } };
    results.push({
      index: page.index + 1,
      name: page.name,
      id: page.id,
      ...analysis,
      errors: [...page.errors, ...analysis.errors],
    });
  }

  if (flags.json) {
    console.log(JSON.stringify({ file, compressed, pages: results, errors: parserErrors }, null, 2));
    return results.some((r) => r.errors.length) || parserErrors.length ? 1 : 0;
  }

  console.log(`File: ${file}`);
  console.log(`Pages: ${results.length}${compressed ? " (compressed payload present)" : ""}`);
  for (const page of results) {
    const { cells, vertices, edges, bounds } = page.stats;
    console.log(
      `- ${page.index}. "${page.name}"${page.id ? ` [${page.id}]` : ""}: ${cells} cells (${vertices} vertices, ${edges} edges)` +
        (bounds
          ? `, bounds ${Math.round(bounds.width)}x${Math.round(bounds.height)} @ (${Math.round(bounds.x)}, ${Math.round(bounds.y)})`
          : ""),
    );
    for (const error of page.errors) console.log(`    ERROR ${error.replace(/^page[^:]*:\s*/, "")}`);
    const shownWarnings = page.warnings.slice(0, 15);
    for (const warning of shownWarnings) console.log(`    warn  ${warning.replace(/^page[^:]*:\s*/, "")}`);
    if (page.warnings.length > shownWarnings.length) {
      console.log(`    warn  ... ${page.warnings.length - shownWarnings.length} more warnings (see --json)`);
    }
  }
  for (const error of parserErrors) console.log(`ERROR ${error}`);

  const errorCount =
    parserErrors.length + results.reduce((sum, page) => sum + page.errors.length, 0);
  const warningCount = results.reduce((sum, page) => sum + page.warnings.length, 0);
  console.log(`Result: ${errorCount === 0 ? "ok" : "failed"} (${errorCount} errors, ${warningCount} warnings)`);
  return errorCount === 0 ? 0 : 1;
}

function extractPage(file, xml, selector) {
  const { pages } = collectPages(xml);
  if (!selector) throw new Error("--page is required (name, id, or 1-based index)");
  const index = Number.parseInt(selector, 10);
  const match =
    pages.find((page) => page.id && page.id === selector) ??
    pages.find((page) => page.name === selector) ??
    (Number.isInteger(index) && String(index) === String(selector) ? pages[index - 1] : undefined);

  if (!match) {
    throw new Error(
      `page "${selector}" not found. Available: ${pages
        .map((page) => `${page.index + 1}.${page.name}${page.id ? ` [${page.id}]` : ""}`)
        .join(", ")}`,
    );
  }
  if (!match.modelXml) throw new Error(`page "${selector}" has no readable model XML`);
  return { page: match, xml: match.modelXml };
}

function buildAppUrl(file, xml) {
  const packed = xml.replace(
    /(<diagram\b[^>]*>\s*)(<mxGraphModel[\s\S]*?<\/mxGraphModel>)(\s*<\/diagram>)/g,
    (_, open, model, close) => `${open}${compressDiagram(model)}${close}`,
  );
  const title = encodeURIComponent(path.basename(file));
  return `https://app.diagrams.net/?splash=0&ui=kennedy&title=${title}#R${encodeURIComponent(packed)}`;
}

function launchSystemBrowser(url) {
  if (process.platform === "win32") {
    spawn("cmd", ["/c", "start", "", url], { detached: true, stdio: "ignore" }).unref();
  } else if (process.platform === "darwin") {
    spawn("open", [url], { detached: true, stdio: "ignore" }).unref();
  } else {
    spawn("xdg-open", [url], { detached: true, stdio: "ignore" }).unref();
  }
}

function openInBrowser(file, xml, flags) {
  const targetUrl = buildAppUrl(file, xml);
  const requestedPort = flags.port !== undefined ? Number.parseInt(flags.port, 10) : 41999;
  const noLaunch = Boolean(flags["no-launch"]);
  let settled = false;

  const server = http.createServer((req, res) => {
    if (req.url === "/favicon.ico") {
      res.writeHead(404);
      res.end();
      return;
    }
    res.writeHead(302, {
      Location: targetUrl,
      "Cache-Control": "no-store",
      Connection: "close",
    });
    res.end();
    if (!settled) {
      settled = true;
      setTimeout(() => {
        server.closeAllConnections?.();
        server.close(() => process.exit(0));
      }, 400);
    }
  });

  const timeout = setTimeout(() => {
    if (!settled) {
      server.close(() => process.exit(0));
    }
  }, 45000);
  timeout.unref();

  const startListening = (port) => {
    server.once("error", (err) => {
      if (err.code === "EADDRINUSE" && port !== 0) {
        startListening(0);
        return;
      }
      throw err;
    });
    server.listen(port, "127.0.0.1", () => {
      const addr = server.address();
      const localUrl = `http://127.0.0.1:${addr.port}/open`;
      console.log(localUrl);
      if (!noLaunch) {
        launchSystemBrowser(localUrl);
      }
    });
  };

  startListening(Number.isFinite(requestedPort) ? requestedPort : 41999);
}

function main() {
  const { command, file, flags } = parseArgs(process.argv.slice(2));

  if (!command || !file || !["info", "check", "extract", "open", "url", "pack"].includes(command)) {
    console.error(
      "Usage: drawio.mjs <info|check|extract|open|url|pack> <file> [--page <name|id|index>] [--port <port>] [--no-launch] [--json] [--verbose]",
    );
    process.exit(2);
  }

  const xml = fs.readFileSync(file, "utf8");

  if (command === "pack") {
    process.stdout.write(compressDiagram(xml) + "\n");
    return;
  }

  if (command === "url") {
    process.stdout.write(buildAppUrl(file, xml) + "\n");
    return;
  }

  if (command === "open") {
    openInBrowser(file, xml, flags);
    return;
  }

  if (command === "extract") {
    const { page, xml: modelXml } = extractPage(file, xml, flags.page);
    if (flags.json) {
      console.log(JSON.stringify({ index: page.index + 1, name: page.name, id: page.id, xml: modelXml }, null, 2));
    } else {
      console.error(`# ${page.index + 1}. "${page.name}"${page.id ? ` [${page.id}]` : ""}`);
      process.stdout.write(modelXml.endsWith("\n") ? modelXml : modelXml + "\n");
    }
    return;
  }

  process.exit(report(file, xml, flags));
}

main();
