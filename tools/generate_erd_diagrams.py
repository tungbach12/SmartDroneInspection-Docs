#!/usr/bin/env python3
"""Generate the Full 31-Table Mermaid ERD (PK, FK, and all fields without SQL data types) for Report 3 and Report 4."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
BACKEND_MIGRATIONS = ROOT.parent / "SmartDroneInspection-backend" / "src" / "main" / "resources" / "db" / "migration"
ERD_OUT_DIR = ROOT / "diagrams" / "erd"


def parse_migrations(mig_dir: Path = BACKEND_MIGRATIONS):
    sql = "\n".join(p.read_text(encoding="utf-8") for p in sorted(mig_dir.glob("V*.sql")))
    tables: dict[str, list[str]] = {}
    pk_map: dict[str, set[str]] = {}
    fk_map: dict[str, dict[str, str]] = {}

    for m in re.finditer(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)\s*\((.*?)\);", sql, re.S | re.I):
        tname = m.group(1).lower()
        body = m.group(2)
        cols = []
        pks = {"id"}
        fks = {}
        for raw_line in body.splitlines():
            line = raw_line.strip().rstrip(",")
            if not line or line.startswith("--"):
                continue
            up = line.upper()
            if up.startswith(("CONSTRAINT ", "PRIMARY KEY", "FOREIGN KEY", "UNIQUE ", "CHECK ")):
                fk_m = re.search(r"FOREIGN\s+KEY\s*\(([^)]+)\)\s*REFERENCES\s+(\w+)\s*\(([^)]+)\)", line, re.I)
                if fk_m:
                    src_cols = [c.strip().lower() for c in fk_m.group(1).split(",")]
                    ref_tbl = fk_m.group(2).lower()
                    for sc in src_cols:
                        if sc != "organization_id" or ref_tbl == "organizations":
                            fks[sc] = ref_tbl
                continue
            col_m = re.match(r"^(\w+)\s+(.+)$", line)
            if col_m:
                cname = col_m.group(1).lower()
                rest = col_m.group(2)
                cols.append(cname)
                ref_m = re.search(r"REFERENCES\s+(\w+)", rest, re.I)
                if ref_m:
                    fks[cname] = ref_m.group(1).lower()
        tables[tname] = cols
        pk_map[tname] = pks
        fk_map[tname] = fks

    for m in re.finditer(r"ALTER\s+TABLE\s+(?:ONLY\s+)?(\w+)\s+(.*?);", sql, re.S | re.I):
        tname = m.group(1).lower()
        if tname not in tables:
            continue
        ops = m.group(2)
        for drop_m in re.finditer(r"DROP\s+COLUMN\s+(?:IF\s+EXISTS\s+)?(\w+)", ops, re.I):
            dc = drop_m.group(1).lower()
            if dc in tables[tname]:
                tables[tname].remove(dc)
            fk_map[tname].pop(dc, None)
        for add_m in re.finditer(r"ADD\s+COLUMN\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)\s+([^,\n]+)", ops, re.I):
            ac = add_m.group(1).lower()
            rest = add_m.group(2)
            if ac not in tables[tname]:
                tables[tname].append(ac)
            ref_m = re.search(r"REFERENCES\s+(\w+)", rest, re.I)
            if ref_m:
                fk_map[tname][ac] = ref_m.group(1).lower()
        for fk_m in re.finditer(r"FOREIGN\s+KEY\s*\(([^)]+)\)\s*REFERENCES\s+(\w+)", ops, re.I):
            src_cols = [c.strip().lower() for c in fk_m.group(1).split(",")]
            ref_tbl = fk_m.group(2).lower()
            for sc in src_cols:
                if sc != "organization_id" or ref_tbl == "organizations":
                    fk_map[tname][sc] = ref_tbl

    ordered_cols: dict[str, list[tuple[str, str]]] = {}
    for tname, cols in tables.items():
        pks = [c for c in cols if c in pk_map[tname]]
        fks = [c for c in cols if c in fk_map[tname] and c not in pk_map[tname]]
        regs = [c for c in cols if c not in pk_map[tname] and c not in fk_map[tname]]
        ordered_cols[tname] = [(c, "PK") for c in pks] + [(c, "FK") for c in fks] + [(c, "") for c in regs]
    return ordered_cols, fk_map


def build_mermaid_er_code(ordered_cols: dict[str, list[tuple[str, str]]]) -> str:
    mermaid_lines = [
        "%% title: Database Entity Relationship Diagram (ERD)",
        "erDiagram",
        "  organizations ||--o{ users : employs",
        "  organizations ||--o{ subscriptions : holds",
        "  subscriptions ||--o{ payment_transactions : settles",
        "  organizations ||--o{ drones : owns",
        "  organizations ||--o{ drone_leases : contracts",
        "  platform_drones ||--o{ drone_leases : leased_via",
        "  drone_leases ||--o| drones : provisions",
        "  users ||--o{ drone_leases : requests",
        "  organizations ||--o{ assets : owns",
        "  asset_categories ||--o{ assets : categorizes",
        "  assets ||--o{ asset_documents : attaches",
        "  organizations ||--o{ audit_events : records",
        "  organizations ||--o{ notifications : scopes",
        "  users ||--o{ notifications : receives",
        "  users ||--o{ auth_sessions : opens",
        "  organizations ||--o{ inspections : owns",
        "  assets ||--o{ inspections : undergoes",
        "  users ||--o{ inspections : assigned_inspector",
        "  drones ||--o{ inspections : assigned_drone",
        "  organizations ||--o{ recurring_inspection_schedules : schedules",
        "  assets ||--o{ recurring_inspection_schedules : recurs_for",
        "  users ||--o{ recurring_inspection_schedules : default_inspector",
        "  drones ||--o{ recurring_inspection_schedules : default_drone",
        "  recurring_inspection_schedules ||--o{ schedule_occurrences : generates",
        "  organizations ||--o{ schedule_occurrences : scopes",
        "  inspections |o--o{ schedule_occurrences : fulfills",
        "  recurring_inspection_schedules ||--o{ inspections : dispatches",
        "  inspections ||--o{ field_sessions : executes",
        "  inspections ||--o{ evidence : contains",
        "  field_sessions ||--o{ evidence : captures",
        "  inspections ||--o{ findings : records",
        "  evidence ||--o{ findings : locates",
        "  inspections ||--o{ inspection_reports : delivers",
        "  organizations ||--o{ maintenance_work_orders : owns",
        "  assets ||--o{ maintenance_work_orders : remediates",
        "  users ||--o{ maintenance_work_orders : governs",
        "  findings ||--o{ maintenance_work_orders : initiates",
        "  inspection_reports ||--o{ maintenance_work_orders : references",
        "  maintenance_work_orders ||--o{ maintenance_team_members : deploys",
        "  maintenance_work_orders ||--o{ maintenance_tasks : deconstructs",
        "  maintenance_work_orders ||--o{ maintenance_estimate_versions : projects",
        "  maintenance_estimate_versions ||--o{ maintenance_cost_lines : itemizes",
        "  maintenance_tasks ||--o{ maintenance_cost_lines : accrues",
        "  maintenance_work_orders ||--o{ maintenance_change_orders : requests",
        "  maintenance_tasks ||--o{ maintenance_work_logs : tracks",
        "  maintenance_work_orders ||--o{ maintenance_reports : delivers",
        "  maintenance_reports ||--o{ maintenance_acceptance_decisions : accepts",
    ]
    all_31_order = [
        "organizations", "users", "auth_sessions", "subscriptions", "payment_transactions",
        "platform_drones", "drone_leases", "drones", "asset_categories", "assets", "asset_documents",
        "recurring_inspection_schedules", "schedule_occurrences", "inspections", "field_sessions", "evidence",
        "findings", "inspection_reports", "repair_knowledge_chunks", "notifications", "audit_events", "event_publication",
        "maintenance_work_orders", "maintenance_team_members", "maintenance_tasks", "maintenance_estimate_versions", "maintenance_cost_lines",
        "maintenance_change_orders", "maintenance_work_logs", "maintenance_reports", "maintenance_acceptance_decisions",
    ]
    for tname in all_31_order:
        mermaid_lines.append(f"  {tname} {{")
        for cname, key_kind in ordered_cols[tname]:
            suffix = f" {key_kind}" if key_kind else ""
            mermaid_lines.append(f"    _ {cname}{suffix}")
        mermaid_lines.append("  }")
    return "\n".join(mermaid_lines)


def build_renderer_html(code: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>body {{ margin: 0; padding: 16px; background: #fff; display: inline-block; }}</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
</head>
<body>
<div id="c"></div>
<script>
const code = {json.dumps(code)};
mermaid.initialize({{
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
  maxTextSize: 500000,
  er: {{ useMaxWidth: false }}
}});
mermaid.render('erd_svg', code).then(({{ svg }}) => {{
  document.getElementById('c').innerHTML = svg;
  const svgEl = document.querySelector('#c svg');
  svgEl.querySelectorAll('g.label.attribute-type').forEach(g => g.remove());
  svgEl.querySelectorAll('g.node').forEach(node => {{
    const divs = node.querySelectorAll('g.divider');
    if (divs.length >= 2) divs[1].remove();
    node.querySelectorAll('g.label.attribute-name').forEach(g => {{
      const tf = g.getAttribute('transform') || '';
      const m = tf.match(/translate\\(([-\\d.]+),\\s*([-\\d.]+)\\)/);
      if (m) {{
        const outer = node.querySelector('g.outer-path path');
        const d = outer ? outer.getAttribute('d') : '';
        const xm = d.match(/^M([-\\d.]+)/);
        const leftX = xm ? parseFloat(xm[1]) + 12 : parseFloat(m[1]);
        g.setAttribute('transform', 'translate(' + leftX + ', ' + m[2] + ')');
      }}
    }});
  }});

  const cols = [
    ['organizations', 'users', 'auth_sessions', 'subscriptions', 'payment_transactions'],
    ['platform_drones', 'drone_leases', 'drones', 'asset_categories', 'asset_documents'],
    ['assets', 'recurring_inspection_schedules', 'schedule_occurrences', 'notifications', 'audit_events'],
    ['inspections', 'field_sessions', 'evidence', 'findings', 'event_publication'],
    ['inspection_reports', 'maintenance_work_orders', 'maintenance_team_members', 'maintenance_tasks', 'maintenance_estimate_versions'],
    ['maintenance_cost_lines', 'maintenance_change_orders', 'maintenance_work_logs', 'maintenance_reports', 'maintenance_acceptance_decisions', 'repair_knowledge_chunks'],
  ];
  const nodeMap = {{}};
  svgEl.querySelectorAll('g.node').forEach(n => {{
    const id = n.id || '';
    const m = id.match(/entity-([a-z0-9_]+)-\\d+$/);
    if (m) {{
      const outer = n.querySelector('g.outer-path path');
      const d = outer ? outer.getAttribute('d') : '';
      const dm = d.match(/^M([-\\d.]+)\\s+([-\\d.]+)\\s+L([-\\d.]+)\\s+([-\\d.]+)\\s+L([-\\d.]+)\\s+([-\\d.]+)/);
      const w = dm ? Math.abs(parseFloat(dm[3]) - parseFloat(dm[1])) : 280;
      const h = dm ? Math.abs(parseFloat(dm[6]) - parseFloat(dm[2])) : 200;
      nodeMap[m[1]] = {{ el: n, w, h }};
    }}
  }});
  let curX = 32, colGap = 56, rowGap = 32, maxH = 0;
  cols.forEach((colTables, cIdx) => {{
    const colW = Math.max(...colTables.map(t => nodeMap[t] ? nodeMap[t].w : 260));
    let curY = 32;
    colTables.forEach((t, rIdx) => {{
      const info = nodeMap[t];
      if (!info) return;
      const cx = curX + colW / 2, cy = curY + info.h / 2;
      Object.assign(info, {{ cx, cy, col: cIdx, row: rIdx, left: cx - info.w / 2, right: cx + info.w / 2, top: cy - info.h / 2, bottom: cy + info.h / 2 }});
      info.el.setAttribute('transform', 'translate(' + cx + ', ' + cy + ')');
      curY += info.h + rowGap;
    }});
    if (curY > maxH) maxH = curY;
    curX += colW + colGap;
  }});
  const totalW = Math.ceil(curX - colGap + 32), totalH = Math.ceil(maxH + 16);
  const edgeLabels = svgEl.querySelectorAll('g.edgeLabels g.edgeLabel');
  svgEl.querySelectorAll('g.edgePaths path.relationshipLine').forEach((p, idx) => {{
    const did = p.getAttribute('data-id') || p.id || '';
    const m = did.match(/entity-([a-z0-9_]+)-\\d+_entity-([a-z0-9_]+)-\\d+/);
    if (m && nodeMap[m[1]] && nodeMap[m[2]]) {{
      const a = nodeMap[m[1]], b = nodeMap[m[2]], offset = ((idx % 7) - 3) * 5;
      if (a.col === b.col) {{
        const x1 = a.cx + offset, x2 = b.cx + offset;
        const y1 = a.cy < b.cy ? a.bottom : a.top, y2 = a.cy < b.cy ? b.top : b.bottom;
        p.setAttribute('d', 'M' + x1 + ',' + y1 + ' L' + x2 + ',' + y2);
        if (edgeLabels[idx]) {{
          if (Math.abs(a.row - b.row) === 1) edgeLabels[idx].setAttribute('transform', 'translate(' + ((x1+x2)/2) + ', ' + ((y1+y2)/2) + ')');
          else edgeLabels[idx].style.display = 'none';
        }}
      }} else {{
        const dir = a.cx < b.cx ? 1 : -1;
        const x1 = dir > 0 ? a.right : a.left, y1 = a.cy + offset;
        const x2 = dir > 0 ? b.left : b.right, y2 = b.cy + offset;
        const mx = x1 + dir * (colGap / 2) + offset;
        p.setAttribute('d', 'M' + x1 + ',' + y1 + ' L' + mx + ',' + y1 + ' L' + mx + ',' + y2 + ' L' + x2 + ',' + y2);
        if (edgeLabels[idx]) edgeLabels[idx].style.display = 'none';
      }}
    }}
  }});
  svgEl.setAttribute('width', String(totalW));
  svgEl.setAttribute('height', String(totalH));
  svgEl.setAttribute('viewBox', '0 0 ' + totalW + ' ' + totalH);
  document.body.setAttribute('data-ready', '1');
}});
</script>
</body>
</html>"""


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not BACKEND_MIGRATIONS.is_dir():
        raise SystemExit(f"Backend migrations directory not found: {BACKEND_MIGRATIONS}")
    ordered_cols, _ = parse_migrations(BACKEND_MIGRATIONS)
    code = build_mermaid_er_code(ordered_cols)
    digest = hashlib.sha256(code.encode("utf-8")).hexdigest()[:12]
    ERD_OUT_DIR.mkdir(parents=True, exist_ok=True)
    mmd_out = ERD_OUT_DIR / f"full_erd_31_{digest}.mmd"
    mmd_out.write_text(code + "\n", encoding="utf-8")

    for md_path in [
        ROOT / "reports" / "report-4-software-design-document" / "02-database-design.md",
        ROOT / "reports" / "report-3-software-requirement-specification" / "03-functional-requirements.md",
    ]:
        txt = md_path.read_text(encoding="utf-8")
        marker = "%% title: Database Entity Relationship Diagram (ERD)"
        idx = txt.find(marker)
        if idx == -1:
            marker = "%% title: Entity Relationship Diagram (ERD)"
            idx = txt.find(marker)
        assert idx != -1, f"ERD marker not found in {md_path}"
        start_fence = txt.rfind("```mermaid", 0, idx)
        end_fence = txt.find("```", idx)
        assert start_fence != -1 and end_fence != -1
        txt_new = txt[:start_fence] + "```mermaid\n" + code + "\n```" + txt[end_fence + 3:]
        md_path.write_text(txt_new, encoding="utf-8")

    html_out = ERD_OUT_DIR / "render_mermaid_erd.html"
    html_out.write_text(build_renderer_html(code), encoding="utf-8")
    print(f"Updated Report 3 & Report 4 with 31-table Mermaid ERD ({digest}) and wrote {html_out}")


if __name__ == "__main__":
    main()
