---
name: hand-svg-structure-figure
description: Replicate a bitmap/screenshot structure diagram (block diagram, flowchart, network, schematic) as a hand-authored static SVG — programmatic geometry/color probing, live-page export, full pitfall list.
---

# Hand-authored SVG structure-figure replication

## When to use

The reference is a **bitmap** (paper screenshot, scan, slide export) showing a *structure* figure — block diagram / flowchart / network / schematic — and you need an editable, print-quality vector replica. Do **not** use this route for data plots (see `data-figures-rerender`).

## Workflow (five steps)

1. **Probe, don't eyeball.** Use `probe_geometry.py` (this folder) to extract exact pixel values from the reference bitmap: box bounds via fill-color connected components, circle centers/diameters via ring scans, text-row baselines, connector endpoints, dash/fill/border colors. Build the first draft **in the reference's coordinate system** — it lands ~80% right with zero guessing.
2. **Copy text verbatim.** Every string checked against the reference. Sub/superscripts via `tspan dy` (math letters in italic serif; **upright digit subscripts need explicit `font-style="normal"`** — tspans inherit italics).
3. **Hand-write the SVG.** Styles centralized in a `<style>` block + semantic color constants (see repo-root `METHOD.md`); structural comments per region; default ink color inherited from a wrapping `<g fill="...">`.
4. **Export PNG.** `prepare_export_pages.py` builds inline-HTML pages → set the browser viewport to the *exact* content size → plain screenshot (**never fullPage** — it triggers the tiling bug); for content taller than ~2160 px, capture top/bottom halves and stitch with PIL.
5. **Acceptance.** Live-page screenshot + an independent vision-model judge comparing replica vs reference (criteria: every string, arrow source→target topology, no overflow/overlap; intentional style upgrades are not defects). On FAIL, fix root causes using the judge's pixel evidence.

## Hard-won pitfalls (all real)

- **SVG `<style>` overrides presentation attributes**: `text{fill:…}` beats `fill=""` on elements → colored titles render near-black. Keep `fill` out of CSS; inherit defaults from a wrapping `<g fill>` and set colors per-element.
- **Never export via `<img src="*.svg">`**: renders wrong (italic leakage, cascade anomalies); standalone SVG documents screenshot as scaled tiles. Inline HTML is the only reliable channel.
- **Signature style of fully-connected network figures**: incoming edges converge on the target circle's **left pole**, arrowheads stacked in a cluster — radial rim distribution reads as "wrong".
- Judge "likeness" at the structural-semantic level: the reference is a semantic target, not a pixel template.

## Examples (`examples/`)

- `fig-prefix-classifier` — two-section pipeline figure (blue/orange dashed groups, feedback loop), replicated from a bitmap in the reference coordinate system (`ecg_reference.png` is the source bitmap).
- `fig1-1_roadmap` — four-stage research roadmap redrawn from a matplotlib source script (coordinates mapped 1:1).
