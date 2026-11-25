---
name: drawio-diagram-skill
description: Read, edit, validate, and open local draw.io diagrams (.drawio mxGraphModel XML) directly in app.diagrams.net in Chrome without HTML wrappers. Use for changing shapes, labels, edges, ER tables, sequence/UML/state/package/activity diagrams, splitting diagram types into type-specific multi-tab .drawio files, and checking overlaps/crossings.
---

# draw.io Diagram Edits (Local-First)

**Work directly on local `.drawio` files.** Keep edits minimal, preserve existing IDs/routing/styles when updating an existing tab, and keep every untouched page byte-identical.

The `.drawio` file is XML: either `<mxfile>` with inline `<mxGraphModel>` (preferred, directly text-editable) or `<diagram>` carrying compressed base64 (decode first via `extract`). Never hand-edit compressed base64.

The helper script lives beside this file (`.agents/skills/drawio-diagram-skill/scripts/drawio.mjs`, relative to the repository root):

```powershell
node ".agents/skills/drawio-diagram-skill/scripts/drawio.mjs" <command> [args]
```

| Command | Purpose |
| --- | --- |
| `info <file>` | List pages, IDs, cell counts, bounds, and structural notes |
| `check <file> [--verbose]` | Validation gate (`--verbose` also checks sibling overlaps & straight-edge crossings through unrelated vertices) |
| `extract <file> --page <name\|id\|index>` | Print plain `<mxGraphModel>` XML for one tab |
| `open <file> [--port <port>] [--no-launch]` | Start a 1-shot localhost 302 redirect and open the full multi-tab `.drawio` file directly in native `app.diagrams.net` (no HTML wrapper, no 32 KB CLI/copy-paste limit) |
| `url <file>` | Build the direct `https://app.diagrams.net/?splash=0&ui=kennedy&title=<file>#R...` URL packing all tabs |
| `pack <xml-file>` | Re-encode XML for a compressed `<diagram>` |

All commands accept `--json`. Flags (`--verbose`, `--json`, `--page`, `--port`, `--no-launch`) can appear before or after `<file>`.

## 1. File Organization & Ground Truth

1. **One Diagram Type = One `.drawio` File:** Group sub-diagrams of the same diagram type as multiple `<diagram>` tabs inside one `.drawio` file (e.g., `smartdrone-use-case-diagrams.drawio` containing `UC-1`..`UC-5`, `smartdrone-package-diagrams.drawio` containing `Backend`, `Web Portal`, `Mobile App`), and keep `<mxfile pages="N">` accurate when adding or removing tabs.
2. **Inspect Live Code Before Editing:** When syncing diagrams to the current codebase, verify modules, controllers, roles, entities, enums, integrations, and config directly in source code (`src/`), never from stale prose or retired features. Drop out-of-scope diagrams/tabs cleanly when confirmed.
3. **Check `git status --short` first** and match pages by **name or id** (never by fragile 1-based index alone).
4. **Update Diagrams First, Reports Last:** Keep diagram `.drawio` iterations focused and reviewed; export images and update report markdown/Word outputs once after diagrams are approved.

## 2. Structural & Layout Rules

### XML Integrity
- Preserve `id="0"`, `id="1"`, existing IDs, and the `parent` chain.
- New IDs must be unique within each page; follow the local ID style and verify with `check`.
- Vertices require `<mxGeometry x=".." y=".." width=".." height=".." as="geometry" />`. Edges require `<mxGeometry relative="1" as="geometry" />` plus valid `source` and `target` in the same page.
- Escape XML strictly inside attributes (`&amp; &lt; &gt; &quot;`). With `html=1`, HTML tags inside `value="..."` must be escaped (`&lt;br&gt;`, `&lt;b&gt;`). Python `xml.etree.ElementTree` or controlled string templates with strict `check` prevent parser errors.

### Diagram Style & Readability
- **No standalone canvas title boxes:** Do not embed top-of-canvas `text` title/subtitle boxes (`SmartDroneInspection - ... Diagram`) inside `.drawio` canvases unless explicitly asked; report captions handle figure numbering.
- **Default monochrome UML unless asked otherwise:** Use `#FFFFFF` fill and `#000000` stroke (`strokeWidth=1`, `fontColor=#000000`, `Helvetica`) by default for UML ovals/actors/classes/states/actions/diamonds; avoid unrequested colored fills.
- **Activity Diagram Swimlanes:** Use real vertical `swimlane` containers (`startSize=34;fillColor=#EEEEEE;swimlaneFillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1;fontStyle=1;`) placed side-by-side (`1px` solid black borders, no dashed dividers), `#000000` Start circle and `endState` bullseye, concise action text (no noisy `(FE-xx)` codes or diagram subtitles inside lanes), and plain guard labels without square brackets (`Yes`, `No`, `Publish`, `Return`). Split multi-flow pages (e.g., two unrelated workflows in one stage) into separate diagram tabs.
- **Atomic Use Cases:** Never combine distinct user goals into one oval (e.g., keep `Manage Building Assets`, `Manage Building Checkpoints`, `Manage Building Documents` separate; keep `Sign in with Password`, `Sign in with Google`, `Reset Password`, `Change Password` separate). Split dense domains into multiple tabs (`~10–14` ovals per tab) rather than cramping one canvas.
- **Keep actor links clean (no inheritance spaghetti):** Avoid fanning 4+ concrete role stick figures sideways into a shared `Authenticated User` actor when a clean pair of `Guest` + `Authenticated User` (in auth view) or direct role-specific views keeps edges clean.
- **Single-arrowhead UML Generalization Bus (Tree Style):** When 3+ specialized use cases or classes inherit from one parent, do **not** point multiple hollow triangles to the same `entryX=1;entryY=0.5` point (arrowheads clump together). Instead, route horizontal orthogonal branches onto a vertical spine (`2x2` black junction vertex) and draw **one** `endArrow=block;endFill=0;` trunk arrow into the parent oval.
- **Explicit ports & open corridors:** Specify `exitX`, `exitY`, `entryX`, `entryY` on `edgeStyle=none` links and verify cross-column lines pass through open vertical gaps without grazing adjacent ovals (`check --verbose` flags straight edges crossing unrelated vertices). For UML `shape=folder` (`tabHeight=18`), land top-edge arrows on the flat right shoulder (`entryX >= 0.36;entryY=0.22;entryPerimeter=0;exitPerimeter=0;`) so arrows neither hit the sticky folder tab nor float above it.

## 3. Local Validation & Direct `app.diagrams.net` Opening (No Wrapper)

1. Run structural & geometry validation after every edit:
   ```powershell
   node ".agents/skills/drawio-diagram-skill/scripts/drawio.mjs" check <file.drawio> --verbose
   ```
   Fix all `ERROR` lines and inspect any unexpected `warn` overlap or `crosses vertex` lines.
2. **Open the local `.drawio` directly in native `app.diagrams.net` (zero HTML wrapper, zero base64 copy-paste):**
   - **NEVER** generate or open wrapped `preview.html` (`viewer-static.min.js`) files, and **NEVER** hand-copy long `#R...` base64 URLs into tool calls (truncation or a single bad base64 token triggers `invalid distance too far back`).
   - Run `open` with `--no-launch` in background (`WaitMsBeforeAsync: 1000`), which starts a 1-shot localhost `302` redirect and prints `http://127.0.0.1:<port>/open`:
     ```powershell
     node ".agents/skills/drawio-diagram-skill/scripts/drawio.mjs" open <file.drawio> --no-launch
     ```
     Then navigate Chrome (`chrome-devtools` `navigate_page` / `new_page`, or drop `--no-launch` to open the OS browser directly) to `http://127.0.0.1:<port>/open`. The browser follows the `302` straight into `https://app.diagrams.net/?splash=0&ui=kennedy&title=<file>#R...` with bit-exact XML across all tabs, and the 1-shot HTTP server exits automatically right after serving the redirect.
   - To visually inspect every tab inside `app.diagrams.net` via `chrome-devtools`:
     - Click each bottom tab cleanly using `.geTab` mouse events (`pointerdown`, `mousedown`, `pointerup`, `mouseup`, `click`), then call `take_screenshot` with `fullPage: false` (diagrams.net auto-fits the canvas cleanly in the viewport without timing out like `fullPage: true`).
     - Keep only the native `app.diagrams.net` tab open for the user. Local `.drawio` remains the source of truth — never push to Google Drive unless explicitly requested.

## 4. Do Not

- Do not generate wrapped HTML preview pages (`viewer-static.min.js`), keep local preview tabs open, or push changes to Google Drive unless explicitly asked.
- Do not hand-copy giant `#R...` base64 strings into browser navigation tools (always route via `drawio.mjs open`).
- Do not hand-edit compressed base64 `<diagram>` payloads or `.drawio.svg`/`.drawio.png` binaries.
- Do not commit temporary scratch files into the repository; store temporary helpers inside the scratch directory.
