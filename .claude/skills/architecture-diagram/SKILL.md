---
name: architecture-diagram
description: Create dark-themed architecture diagrams as SVG files for this MkDocs site. Use when asked for system, infrastructure, cloud, security, homelab, or network topology diagrams, or to edit an existing diagram in diagrams/src/.
---

# Architecture Diagram Skill

Diagrams are authored as SVG source in `diagrams/src/`, then built into
`docs/images/diagrams/` with the font embedded.

> **Version 4.0** · MIT License · Originally authored by [Cocoon AI](mailto:hello@cocoon-ai.com)

## Workflow

```bash
# author or edit
diagrams/src/homelab.svg

# build (verifies, then writes docs/images/diagrams/homelab.svg)
python3 .claude/skills/architecture-diagram/resources/build.py diagrams/src/homelab.svg

# verify without writing
python3 .claude/skills/architecture-diagram/resources/build.py diagrams/src/homelab.svg --check
```

Then reference it from a page:

```markdown
![Homelab architecture](../images/diagrams/homelab.svg){: .dia-dark }
```

**Never hand-edit anything in `docs/images/diagrams/`.** Those files are generated; edit
the source and rebuild. Commit both — `mkdocs gh-deploy` does not run this build.

## How this fits the site

Diagrams are embedded with `<img>`, and `docs/stylesheets/style.css` inverts them per
colour scheme by matching `img.dia-dark`. Three consequences follow, and all of them are
load-bearing:

1. **Author dark on transparent.** Light text, light strokes, no background rect. The site
   inverts the whole image in light mode. The filter is `invert(100%) hue-rotate(180deg)`,
   which flips lightness while preserving hue, so `#FFFFFF` text becomes `#000000` and
   coloured icons keep their hue.
2. **The output must have zero external references.** An SVG loaded through `<img>` renders
   in a restricted mode that blocks every external resource — fonts, images, scripts — and
   the page's CSS cannot reach inside it. This is why `build.py` embeds the font and icons.
3. **Do not inline the SVG into page HTML.** No inline-svg plugin, no `pymdownx.snippets`
   `--8<--` include, no custom hook. Inlining removes the `<img>` element, so the
   `img.dia-dark` selector matches nothing and light/dark mapping silently breaks.

Do not modify `docs/stylesheets/style.css`.

## Output Contract

- Root: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="..." role="img" font-family="...">`.
  The `xmlns` is mandatory — a standalone `.svg` will not render without it.
- **`viewBox` only, no `width`/`height`**, so the diagram scales to its container.
- First child is `<title>`, describing the diagram. Screen readers use it.
- **No background rect, no grid.** Transparent background.
- **No legend, header, title bar, toolbar, export buttons, summary cards, or footer.** The
  diagram is the whole deliverable.
- Size the viewBox to the content plus margin. Never pad out to a default canvas size.

## Design System

### Colour Palette

| Component type | Fill | Stroke |
|---|---|---|
| Frontend / client | `rgba(8, 51, 68, 0.4)` | `#22d3ee` |
| Backend | `rgba(6, 78, 59, 0.4)` | `#34d399` |
| Database | `rgba(76, 29, 149, 0.4)` | `#a78bfa` |
| Cloud / network edge | `rgba(120, 53, 15, 0.3)` | `#fbbf24` |
| Security | `rgba(136, 19, 55, 0.4)` | `#fb7185` |
| Message bus | `rgba(251, 146, 60, 0.3)` | `#fb923c` |
| External / generic | `rgba(30, 41, 59, 0.5)` | `#94a3b8` |

Text: `white` titles, `#94a3b8` sublabels. Boundary labels take their boundary's stroke
colour. Arrow labels are `#94a3b8`, except a distinctive coloured flow may use its own
stroke colour.

### Typography

| Role | Size | Weight |
|---|---|---|
| Component title | 15px | 600 |
| Component sublabel | 13px | 400 |
| Zone / region label | 14px | 600 |
| Security-group label | 12px | 400 |
| Arrow label | 13px | 400 |
| Inline connector (bus) | 11px | 400 |

Set the family once on the root so it inherits:

```svg
font-family="Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
```

Only weights 400 and 600 are embedded — any other weight is synthesised into a fake bold.
Sizes are deliberately large relative to the shapes, for on-screen legibility. **Never
shrink a size to make a label fit**; shorten the label or widen the box.

### Component Boxes

**Default: 160 × 66**, `rx="6"`, `stroke-width="1.5"`. Use 170 wide for a longer name.

```svg
<rect x="X" y="Y" width="160" height="66" rx="6" fill="FILL" stroke="STROKE" stroke-width="1.5"/>
<text x="CX" y="Y+27" fill="white" font-size="15" font-weight="600" text-anchor="middle">Title</text>
<text x="CX" y="Y+50" fill="#94a3b8" font-size="13" text-anchor="middle">sublabel</text>
```

Baselines `y+27` and `y+50` leave ~16px of padding above and below the text block.
`rx` and `stroke-width` do not scale with the shapes — the linework stays fine.

**Exactly one sublabel line per component.** A box is a title plus at most one sublabel:
never a bullet list, an extra detail line, or a tagline. This is why the height is fixed at
66. If a component needs more explanation, split it into two components or drop the detail.

**Component text is always centred** (`text-anchor="middle"`, `x` = the box's horizontal
centre) — a solid-line box's text aligns with the bubble it sits in, full stop. There is no
left-aligned variant; every component follows this rule uniformly.

No icons. Components are text-only — title plus at most one sublabel, per the rule above.

### Boundaries

- **Region / zone:** `stroke-dasharray="8,4"`, `rx="12"`, `fill="none"`, 14px label at `y+26`.
- **Security group:** `stroke-dasharray="4,4"`, `rx="8"`, `fill="none"`, 12px label at `y+19`,
  inset ~15px around the box it wraps.
- **Nested sub-zone:** region styling, stroke-coloured to match the components it contains
  (e.g. `#34d399` for a zone of backend services). Distinguishes nesting without falsely
  implying a security boundary.

**Boundary text is always top-left aligned** — no `text-anchor`, default left-to-right
start, positioned at roughly `x+18, y+26` from the zone's top-left corner. This is the
opposite rule from components (which centre): dashed/dotted perimeter = top-left label,
solid component = centred label. That distinction is deliberate — it's the fastest visual
cue for "is this a container or a thing."

Always `fill="none"` — a translucent wash over a transparent background compounds
unpredictably against the page.

### Arrows

```svg
<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
  <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
</marker>
```

**Default to a rounded-corner `<path>`, not a raw diagonal `<line>`.** A straight line
between two components that aren't already on the same row or column travels through open
space at an arbitrary angle — that's exactly what makes label placement unpredictable and
prone to landing on a neighbouring box or a boundary edge. An orthogonal path with one
rounded corner gives the label a straight, predictable segment to sit on instead:

```svg
<!-- horizontal, then a rounded turn, then vertical -->
<path d="M 300 200 L 380 200 Q 388 200 388 208 L 388 260" fill="none"
      stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrowhead)"/>
<text x="340" y="190" fill="#94a3b8" font-size="13" text-anchor="middle">label</text>
```

- **Corner radius ~8px.** Pick the turn point roughly 60-70% along the dominant axis, not
  at the midpoint — it reads more intentional than a perfectly centred bend.
- **Put the label on the longer straight segment**, offset ~10px off the path (not on top
  of it), in whichever direction has open space. Never on the curved segment itself.
- **A straight `<line>` is still fine when source and target are already aligned** on the
  same row or column — there's no bend to make, so forcing one adds nothing.
- **Route edge-to-edge**, stopping ~2px short of the target box.
- **Minimum length ~15px.** The marker is 10 units wide; anything shorter is all arrowhead.
- Auth / security flows keep their own distinct treatment: dashed (`5,5`), rose, routed
  *around* components, never through them — same rounded-corner mechanics, just with that
  styling layered on top to signal "security-relevant."
- If an arrow must pass beneath a box, draw arrows before components and give that box an
  opaque backing rect (`fill="#0f172a"`) beneath its translucent fill. This creates a solid
  patch in an otherwise transparent file, so prefer rerouting instead.

### Message Buses

```svg
<rect x="X" y="Y" width="170" height="24" rx="4" fill="rgba(251,146,60,0.3)" stroke="#fb923c" stroke-width="1"/>
<text x="CX" y="Y+16" fill="#fb923c" font-size="11" text-anchor="middle">Kafka / RabbitMQ</text>
```

Sits **in the gap between** components, never overlapping one. A 24px bus needs a 90px gap
to leave room for the arrows entering and leaving it.

### Spacing

- Component: 160 × 66 (170 for longer names, 230 for the icon variant).
- Minimum vertical gap between stacked components: **50px**; **90px** with a bus between.
- Horizontal gap: **40px**, enough for an arrow plus a short label.
- Boundary padding: **20px** between a boundary and the shapes inside it.
- Outer margin: **20–25px** from the outermost element to the viewBox edge.
- Target shape area: **17–25% of viewBox area.** Below that, the diagram reads as small
  boxes floating in empty space.

**Size the viewBox to the content, not the other way around.** Lay out the shapes, then set
the viewBox to the content extent plus the outer margin.

Worked vertical rhythm:

```
Row 1:      y=30,  h=66  -> ends 96
Row 2:      y=180, h=66  -> ends 246
Gap:        246 -> 336   (90px, holds a bus)
  arrow in:   248 -> 277
  bus:        y=279, h=24 -> ends 303
  arrow out:  305 -> 334
Row 3:      y=336, h=66  -> ends 402
Boundary:   y=140, h=282 -> ends 422
viewBox:    0 0 1050 450
Columns:    160 wide + 40 gap -> 240, 440, 640, 840
```

### Draw Order

1. `<title>`
2. `<defs>` — the marker
3. Boundaries — outermost first, then nested
4. Arrows and their labels
5. Components — rect, then title, then sublabel

## Label Fit

**Measured, never estimated.** The font is proportional: advances run from about 0.28em
(`i`) to 0.99em (`W`), a 3.6× spread, so counting characters errs by roughly −52% to +37%.
`build.py` measures every label against real advance widths and fails the build if any
exceeds **88%** of the width available to it.

Stick to ASCII in labels. Inter's latin subset has no `→` (and likely no other
arrows or symbols); `make_metrics.py` reports any missing glyphs at setup time. A missing
glyph is measured at an average width and may not render at all.

Do not hand-estimate — run `--check`. As a rough authoring guide only, a 160px box holds
about 20 title characters or 24 sublabel characters of typical mixed-case text, but
capital-heavy strings run far wider.

## Verification

`build.py` enforces automatically, and refuses to emit output on failure:

- Root has the SVG namespace and `viewBox`, and no `width`/`height`
- A `<title>` element is present
- No label exceeds 88% of its available width (icon-aware)
- No component has more than two text lines
- No two component boxes overlap
- Nothing extends outside the viewBox
- Shape area is 17–25% of canvas (warning only)

Confirm by eye what a script cannot judge:

- [ ] Every box sits inside the boundary meant to contain it
- [ ] Arrows stop short of their targets; no label sits on top of a line
- [ ] Renders correctly in **both** colour schemes under `mkdocs serve`

Zero external references in the built file:

```bash
grep -oE 'url\([^)]*|<script|<image [^>]*href="[^"]*|@import' docs/images/diagrams/NAME.svg \
  | grep -v 'url(#\|url(data:\|href="data:' || echo "clean"
```

## Template

Copy `resources/template.svg` into `diagrams/src/` and edit. It demonstrates every
component type, both boundary types, horizontal/vertical/rounded-corner arrows, and a
message bus — all at single-sublabel discipline.

## Working from a Reference Mockup

If `diagrams/inbox/` contains a reference mockup, build from it instead of a text/YAML
description — this is the preferred path when a mockup is present. **PNG only** — not an
Excalidraw SVG export. An SVG export embeds a full base64 font subset and draws every
shape as many hand-sketched bezier segments, which is expensive to read and expensive to
decode by hand for no benefit, since the mockup is only ever read for structure, never for
exact coordinates. A PNG is pixels: read visually, same information, far fewer tokens.

1. **Read the mockup visually** to identify components, groupings/zones, and connections
   — relative positions, groupings, reading order. Not a source of exact pixel coordinates.
2. **Recreate it using this skill's design system**, not the mockup's own styling: the
   palette, box sizes (default 160x66, or a deliberately larger/square "hero" box for a
   component the mockup visually emphasizes), boundary conventions, and typography table
   all still apply — including the centred-component / top-left-zone text alignment rule
   and the rounded-corner arrow routing rule above. Ignore the mockup's own colors, fonts,
   and exact spacing.
3. **Don't hand-compute every coordinate up front.** Lay out approximate positions that
   preserve the mockup's structure and reading order, then run `build.py --check`
   iteratively and fix whatever it actually flags (overlaps, out-of-bounds, label
   width) — this is cheaper than pre-verifying every box by arithmetic, and it's what
   the tool is for. The only firm requirement is no excessive overlap between
   components in the final output.
4. **After a successful build, ask before deleting the mockup from `diagrams/inbox/`.**
   Never delete it automatically, even on success — confirm with the user first.
