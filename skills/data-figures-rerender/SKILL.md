---
name: data-figures-rerender
description: Faithfully replicate or vectorize data figures (scatter/bar/slope charts) — re-render from the same frozen tables with encodings kept item-by-item; outputs SVG + 600 dpi PNG; full pitfall list.
---

# Data-figure re-rendering from frozen tables

## Iron rule

Every point on a data figure is real experimental data — **the encoding is the semantics**. Faithful replication = re-render from the *same frozen tables* (CSVs), keeping palette, marker shapes, axes, log ticks, legends and count annotations item-by-item. Never hand-draw, restyle, or move points — that is fabrication, not replication. Legitimate upgrades are exactly three: an SVG vector version, a higher-dpi PNG, and fixing objective defects in the original (text overflow, label colliding with a marker, edge clipping).

## Workflow

1. **Locate the real data.** A paper's figure script often carries a stale relative path — `find <project-root> -name "<key>.csv"` for the live outputs/tables directory; verify every CSV exists with plausible row counts before writing code.
2. **Port the data pipeline verbatim.** Copy the original script's `load()` / aggregation / pairing functions line-for-line; never change a statistic.
3. **Upgrade rendering.** `save(fig, name)` emits both SVG (`svg.fonttype="path"` — text as paths, renders identically everywhere) and PNG (600 dpi). One script drives all figures: `python make_figures_svg.py` regenerates everything.
4. **Acceptance.** Vision-judge against the original PNG: panel structure, axes, legends, annotations identical + point clouds coincide (same source data ⇒ points coincide naturally, which also cross-validates the ported pipeline).

## Template

`make_figures_svg.py` in this folder is a complete runnable template (six figure types from one script): global rcParams, dual-format `save()`, and ready-made patterns for overview block diagram / dot-strip panel / paired log-log scatter / slope chart / grouped bars / histogram. Adapt `load()` to your own frozen tables.

## Read before drawing

`PITFALLS.md` — ten field-tested pitfalls, including: no linear text offsets on log axes (raster overflow at 600 dpi — use multiplicative), FancyBboxPatch clips to the axes bbox (anchored-at-edge boxes silently lose their bottom border), multi-line text anchor semantics, box-title width overflow, stale relative data paths.
