---
name: declarative-engine-figures
description: Grid-based block diagrams, network overview figures and deployment/phase flowcharts via a declarative layout engine — config syntax with real manuscript configs, and a no-download SVG extraction path.
---

# Declarative layout-engine figures

## When to use

Your figure fits a **row×column grid**: network overview figures (backbone/neck/head columns with legends and column heads), deployment or phase flowcharts (stacked dashed phase frames), method framework diagrams. A declarative engine does layout, alignment and orthogonal routing; you only write the configuration — and the same config always renders the same figure.

The configs in this folder were authored for a local companion engine (grid + emphasis colors + lane-based orthogonal routing + dashed groups + captions + true sub/superscripts). The engine itself is not bundled here; the **config syntax and workflow below are the transferable part** — port them to your engine of choice, or keep them as the spec.

## Config syntax (real examples in `configs/`)

- Node: `name: main text | sub text @rRowcCol !blue` — spans `@r1-3c1` (rows), `@r2c3-4` (columns); `nat` = natural-width narrow node; two `nat` nodes in one cell pack side-by-side.
- Column heads `@head 1: Backbone`; bottom legend `@legend blue: P2 branch, orange: ACR`; dashed phase group `@group Training only : dashed … @end`; bottom caption `@caption …`.
- Edges `A -> B`, colored `A -> B !orange`; sub text supports `_{sub}` `^{sup}` (stackable: `z^{T}_{c}`) and `\n` forced line breaks.
- Text arrows like `(32→64)` inside node text are never mistaken for edges (position-based disambiguation).

## Workflow (no-download SVG extraction)

1. Write the config; base64url-encode it into the hash: `engine.html#c=<b64url>`; success = `window.__archState.ok === true`.
2. Evaluate `buildSVG(lastScene)` in the page console — it returns the full SVG string (no browser download handling needed).
3. The exported width/height are **float strings** — later regexes must accept `[\d.]+`.
4. Export PNG via the `hand-svg-structure` inline-page pipeline.

## Real configs (`configs/`)

- `fig4-1.config.txt` — network overview with column heads + legend + packed narrow-node pair.
- `fig5-2.config.txt` — teacher–student distillation training framework.
- `fig6-2_convert.config.md` — TensorRT deployment flow (two stacked dashed phase frames).
