---
name: style-presets
description: Style presets for structure figures — three token dictionaries (academic default / web / tech). Same geometry and content declaration, swap skins with zero figure-code changes. Includes a worked GPU-pipeline example that regenerates all three finishes.
---

# Style presets (academic / web / tech)

One figure, multiple finishes: a paper-grade default, a screen-friendly web look, and a dark "tech" skin — all from the same declared geometry and content. Style lives in token dictionaries; the figure script never hardcodes a color.

## When to use

- The same structural figure must ship in several looks (paper, slide deck, promo screen) and you do not want to re-draw it per style.
- Works with any route that declares style separately: [`parametric-diagram`](../parametric-diagram/SKILL.md), [`declarative-engine`](../declarative-engine/SKILL.md), hand-written SVG with a shared style block.

## The three presets

| Preset | key | Visual language | Use for |
|---|---|---|---|
| **Academic (default)** | `academic` | White ground, restrained three-color accents, no shadows or gradients, thin strokes, small radii, Times + CJK serif/hei pairing | Papers, theses, formal documents |
| Web | `web` | Dark header band, white rounded cards, soft shadows, pill chips, YaHei/Segoe | Work reports, projected decks |
| Tech | `tech` | Deep-space ground with dot grid, cyan neon accents, glow on accent elements, mono labels | Demos, large screens, product pages |

## Usage

```python
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # folder containing style_presets.py
from style_presets import get_style, names

S = get_style("academic")   # default when called with no argument; returns a copy you may tweak
# every color / font / radius / effect in the figure script reads S["..."] — no hex literals
```

CLI: `--style academic|web|tech|all` (default `academic`; `all` emits every finish in one run). See `examples/make_gpu_flow_fig.py`, which regenerates the three GPU-pipeline figures in `examples/fig-gpu-flow-*.svg` from one declaration.

## Token contract

`get_style()` asserts a fixed key set (see `REQUIRED_KEYS` in `style_presets.py`): canvas/header (`page_bg`, `head`, `head_bg`, `head_rule`, `head_bar`, `date_style`, …), text/line (`ink`, `muted`, `faint`, `line`, `text_mid`), cards (`card`, `card_edge`, `card_r`, `fx` = none|soft|glow, `badge_bg`/`badge_fg`), accent semantics (`gpu_*` — your figure's primary accent), neutral semantics (`cpu_*`), fittings (`off_fill`/`off_dash`, `env_fill`/`env_fg`, `table_head`, `arrow`, `note_*`), and typography/radius (`font_title`, `font_body`, `font_mono`, `chip_r`). Adding a preset = adding one dict; the figure script never changes.

Fonts use fallback lists for Latin/CJK splitting: academic pairs `Times New Roman, SimHei` (titles) with `Times New Roman, SimSun` (small notes).

## Discipline

1. **Style and geometry/content are separate declarations.** Changing a skin must not touch coordinates or text; hex literals are banned from the figure script.
2. **≤3 accents + neutrals still holds inside every preset** — orange only marks the accent semantics in `academic`, cyan only in `tech`.
3. **Effects are tiered**: `academic` = `fx: none`; `web` = `soft` (low-opacity dark shadow); `tech` = `glow` (accent-colored, accent elements only).
4. **Dark skins: verify contrast on the render, not the hex math.** 1.2 px hairlines lose ~60 % of theoretical contrast to antialiasing — pick `line`/`note_line`/text tokens so the exported PNG shows ≥40 gray levels against the real background (see [`visual-acceptance`](../visual-acceptance/SKILL.md), dark-theme contrast check).
