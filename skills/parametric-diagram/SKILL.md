---
name: parametric-diagram-script
description: Draw editable structure diagrams from scratch as a parametric Python script — geometry/topology/style declared in three blocks; re-run to regenerate the SVG. The script is the single source of truth.
---

# Parametric diagram scripts (script = source of truth)

## When to use

Drawing a structure figure **from scratch** (not replicating a bitmap) that you *expect to revise*: add nodes, recolor, reword, reuse in the next paper. Hand-editing SVG coordinates every revision is painful; with a parametric script you edit the declaration block and re-run. For one-shot figures, `hand-svg-structure` is fine.

## Template

`make_fig.py` in this folder is the complete pattern (a three-layer fully-connected network figure), three declaration blocks:

```python
COLS      = {...}   # geometry: columns / centers / radii / row ys (or box x,y,w,h)
NODE_TEXT = {...}   # content: per-node text (main letter, subscript, subscript-italic?)
STYLE     = {...}   # style: palette / line widths / font sizes / families, one place
def mesh(): ...     # topology: loops generate edges (fully-connected / zip chains / trees)
def build(): ...    # assemble the SVG string and write to disk
```

Adding a node = one entry in `COLS["ys"]` + one line in `NODE_TEXT`. Recoloring = `STYLE`. Then `python make_fig.py` regenerates the SVG; export PNG via the `hand-svg-structure` export pages.

## Craft notes (field lessons)

- Compute connector endpoints from declared constants (centers ± radii) — no scattered magic numbers.
- Arrow markers: `markerUnits="userSpaceOnUse"` + `orient="auto"`, line end pulled back 1.5–2 px so the tip touches the target edge.
- Converging/fully-connected figures: end all incoming edges at the target's **left pole** `(cx-(r+2), cy)` so arrowheads stack into a cluster (radial landing reads as wrong vs. classic references).
- Subscript regime: main letters in italic serif; digit subscripts explicitly upright (tspans inherit italics); letter subscripts italic.
- Chinese layer/section labels in a hei-ti face; in-node math in Times.

## Example

`examples/fig-mlp.svg/.png` — three-layer fully-connected network (x_d —W1→ h_N —W2→ f_C) with hidden-layer band, stacked arrowhead clusters, ellipsis dots; `mlp_reference.png` is the reference it replicates (accepted by the visual judge on first re-check).
