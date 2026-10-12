---
name: game-arch-diagram
description: Software/game architecture diagrams as a parametric script — layered bands, rider-chip band titles, semantic tints with accent bars, update-order badges, white-halo edge labels, and the six real collision defects found by vision-judge rounds.
---

# Game/software architecture diagram (parametric, design-polished)

## When to use

Drawing a **software or game architecture figure** — layered bands (input → state machine → core loop → meta systems → platform), a scene/state machine with chips, cross-band feedback loops, and a side build/CI chain. The figure is original (no bitmap reference), expected to be revised, and must pass an independent vision judge. For generic structure figures see [`parametric-diagram`](../parametric-diagram/SKILL.md); for the end-to-end process see [`codex-figure-workflow`](../codex-figure-workflow/SKILL.md).

## What this skill adds over a plain parametric script

A **design language** that makes the figure look art-directed, not default. All of it is flat color — no shadows, no gradients (METHOD 第 7 条).

1. **Rider-chip band titles（骑缝标题牌）** — each dashed band's title is a white rounded chip sitting ON the band's top border (white fill, semantic-color border + bold colored text). Reads as swimlane labels; frees the band's top row for content.
2. **Semantic tinted fills + left accent bar** — every box gets a 4%-tint fill of its semantic color plus a 4px solid color bar on the left edge. Grouping becomes visible even in grayscale thumbnails.
3. **Update-order badges** — numbered circle badges ①–⑥ in the top-right corner of core-loop boxes, matching the engine's per-frame call order. Readers infer execution flow without arrows.
4. **White-halo edge labels** — every edge label gets `stroke="#fff" stroke-width="4.5" paint-order="stroke"`, so a label sitting on any line or border stays legible.
5. **Band corner tags** — small gray right-aligned text inside each band's top-right: 事件驱动 / updatePlay(1/60)·60Hz / 跨局持久 / 常驻. Free metadata, zero clutter.
6. **Three-tier type rhythm** — figure title 34 / box main 22 bold / box sub 15 + band chip 20 / edge label 14.5, on a 1720px canvas. Scales down without collapsing.
7. **State-machine micro-flows** — glyph arrows (→) between sequential chips, (·) between parallel ones, and a 「← 由 select 进入」 note for sub-scenes.

## Declaration blocks (the template)

`make_arch.py` in this folder is a real, accepted figure. Structure:

```python
GROUPS = {...}   # bands: (x,y,w,h, rider-chip text, corner tag, semantic color)
BOXES  = {...}   # boxes: (x,y,w,h, main, sub, semantic color)  sub may contain \n
BADGES = {...}   # core boxes: id → update-order digit
EDGES  = [...]   # E([waypoints], label, lx, ly, color, dash, anchor) — polyline, arrowhead on last segment
STYLE  = dict(...)  # palette constants + font sizes + line widths, one place
V_RHYTHM = {h: (main_dy, sub_dy, line_h)}  # per-box-height text vertical centering
est_w(text, size)  # text width budget: CJK 1.0×size, latin 0.56×size
```

Text-width budget is enforced everywhere a label meets a container: `est_w(label) + start_x + 20 < W` for legend rows; `est_w(sub_line) < w − 24` for box subs; split into two lines instead of shrinking font.

## Workflow

1. **Inventory the real system** from source: layers, modules (with real class/function names), data flows, persistence, build/CI chain. Never draw aspirations.
2. **Grid the bands** top-down following data flow; keep one semantic color per band; ≤3 accent colors total.
3. **Place boxes on an equal-gap grid**; write subs as two lines max; wire `EDGES` as waypoint polylines (orthogonal jogs through designated channels between rows/columns).
4. **Render → export → judge** exactly as [`visual-acceptance`](../visual-acceptance/SKILL.md): inline-HTML pages, exact-size viewport screenshots (HTTP only — IAB/webview agents cannot `goto file:`), halves stitched with PIL, `check_tiling.py`, then an independent vision judge.
5. **Fix root causes** from judge pixel evidence (see the defect catalogue below), re-render, targeted re-check.

## Defect catalogue (all six found by vision judges on a real figure — pre-check these)

1. **Long reroute arrows cross unrelated boxes** — a left-edge detour routed at a box row's mid-height flew straight through the 键盘 box. *Fix: route detours ABOVE the top band (outside its border), not between rows.*
2. **Vertical segment strikes through band-title glyphs** — a drop line at the same x as the band title read as a strikethrough. *Fix: shorten the title; move the origin x past the title's `est_w` end; or drop the horizontal jog below the glyph row.*
3. **Edge label wider than the inter-box gap crosses both box borders** — *fix: move the label to the band's title strip row (y between band title and box tops), where there is full-width room.*
4. **Orthogonal elbow corner lands inside a rider chip** — chips stick OUT of the band border by half their height; any jog near the band's top-left corner can clip the chip. *Fix: drop below `chip_bottom = band_y + 16` before turning toward the target.*
5. **Horizontal segment grazes a band corner-tag's glyph bottoms** — tags occupy the band's y+12..y+30 row on the right. *Fix: run that segment at band_y+40 or lower.*
6. **Legend row wider than the canvas** — *fix: `legend_x + est_w(longest_row) + 20 < W`; shorten wording, don't shrink font.*

Also: an SVG must be exported via inline HTML over **HTTP** — IAB/webview agents cannot navigate `file:`, and `<img src="*.svg">` renders wrong.

## Files

- `make_arch.py` — the real accepted figure's source (字狂潮 v2.3 game architecture, 1720×1400): bands, scene machine with chips, 6 core modules with badges, meta-economy band with feedback loop, platform band, build chain, legend.
- `examples/arch-v2@2x.png` — final render (3440×2800, stitched from viewport halves).
- `examples/arch-v2.svg` / `arch-v2@1x.png` — vector source and full-view preview.

Verdict trail: round 1 FAIL (defects 1/2/3) → round 2 FAIL (defects 4/5/6 introduced by the design polish itself) → round 3 PASS, issues: [].
