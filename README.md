<div align="center">

🌐 本开源项目已链接并认可 <a href="https://linux.do/"><strong>LINUX DO</strong></a> 社区

</div>

---

<div align="center">

# 🎨 figcraft-skills

**Agent skills for publication-quality paper figures**
**让 AI Agent 稳定产出印刷级论文配图的技能包**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Skills](https://img.shields.io/badge/skills-8-7B61FF)
![Figures validated](https://img.shields.io/badge/figures%20validated-25%2B-2EA44F)
![Tested with](https://img.shields.io/badge/tested%20with-GLM--5.3--Flash-D9630E)

*Probed-geometry SVG replication · Parametric diagram sources · Data-faithful re-renders · Visual-judge acceptance loop*

</div>

---

## Codex 完整流程与实战

新增 [Codex 制图指南](CODEX.md) 与 [codex-figure-workflow](skills/codex-figure-workflow/SKILL.md)：从项目事实梳理到参数化 SVG、浏览器导出和独立视觉验收。附 [小马宝莉塔罗网站实战](examples/pony-tarot/CASE.md)、可重生成图源和结果图。

![Codex 架构图实战](examples/pony-tarot/pony-tarot-architecture.png)

## 新增：65 类论文配图入口

新增 **[paper-figure](skills/paper-figure/SKILL.md)**，可整目录独立安装。包含参考项目的 45 类布局规范与示例，加 20 类可直接运行的科研图模板（分布、区间、模型评价、诊断、场、信号与多面板）。已有五条路线和两个参考项目保留。

- [65 类索引](skills/paper-figure/references/chart-catalog.md)：区分 Agent 按规范绘制与脚本直接渲染。
- [离线图型画廊](skills/paper-figure/gallery.html)：可搜索图型与查看示例；科研示例全部标为合成数据。
- [科研模板与输入](skills/paper-figure/references/scientific-recipes.md)：20 类完整 JSON 与统计约定。
- [论文样式和交付](skills/paper-figure/references/publication.md)：灰度/彩色、真实尺寸、数据来源、字体和视觉检查。

直接请 Agent：「读取上述 paper-figure/SKILL.md，按我的真实数据或参考图生成论文配图，保留图源、SVG/PDF/PNG 与验收记录。」不需要先配置品牌或联网字体。

在技能目录运行 `python scripts/render.py --list` 查看 65 类。用 `--spec 文件.json --out 输出目录` 绘制；`--demo all` 仅生成明确标记的合成样例。需本地 numpy、matplotlib；检查与画廊还需 Pillow。

Codex 安装：将 `skills/paper-figure` 整目录复制到 `~/.codex/skills/paper-figure`，即可使用 `$paper-figure`。这次只修改项目，没有自动改动个人已安装技能。

## Why / 为什么

"Draw Figure 1 like the reference" is where AI agents usually produce something *almost* right — wrong fonts, drifting layouts, hand-moved data points, and no way to verify. This repo packages the workflow that fixes it:

**Four routes cover every figure type, one acceptance loop gates them all.**

"照着参考图画一张 Figure 1"是 AI 出图最容易翻车的任务——字体不对、布局漂移、数据点被手挪、还没法验证。本仓库把解决它的完整工作流打包成技能：

> **四条路线覆盖全部图型，一条验收闭环兜底。**

| | Reference → Replica | Reference → Replica |
|---|---|---|
| 📷 | ![ECG before/after](assets/before_after_ecg.png) | |
| | *Bitmap reference → probed-geometry SVG (every box/text/arrow at probed coordinates)* | |

## The nine skills / 九个技能

| Skill | Use when | What you get |
|---|---|---|
| [`paper-figure`](skills/paper-figure/SKILL.md) | 65 chart families: guided SVG layouts + runnable scientific templates | Print styles, SVG/PDF/PNG, provenance and offline gallery |
| [`codex-figure-workflow`](skills/codex-figure-workflow/SKILL.md) | End-to-end project diagrams in Codex | Source-backed structure → SVG/PNG → acceptance, with a real website case |
| [`game-arch-diagram`](skills/game-arch-diagram/SKILL.md) | **Software/game architecture figures** — layered bands, state machine, feedback loops | Design language (rider-chip band titles, semantic tints + accent bars, update-order badges, white-halo labels) + 6-defect collision catalogue from real judge rounds |
| [`hand-svg-structure`](skills/hand-svg-structure/SKILL.md) | Replicating a **bitmap** structure figure (block diagram / flowchart / network) | `probe_geometry.py` (connected-component boxes, ring-scan circles, text-row baselines, color extraction) + `prepare_export_pages.py` (tile-safe browser export pages) |
| [`parametric-diagram`](skills/parametric-diagram/SKILL.md) | Drawing a structure figure **from scratch** that will be revised | `make_fig.py` — geometry/topology/style declared in three blocks; the script is the single source of truth |
| [`data-figures-rerender`](skills/data-figures-rerender/SKILL.md) | **Data figures** (scatter/bar/slope) — points are real results | Re-render from the same frozen tables, encodings kept item-by-item; SVG + 600 dpi PNG; [`PITFALLS.md`](skills/data-figures-rerender/PITFALLS.md) with 10 field-tested traps |
| [`declarative-engine`](skills/declarative-engine/SKILL.md) | Grid-based block diagrams via a declarative layout engine | Config syntax + three real manuscript configs + no-download SVG extraction |
| [`visual-acceptance`](skills/visual-acceptance/SKILL.md) | **Before delivery, always** | Live-page screenshots, tiling self-check (`check_tiling.py`), vision-judge dispatch templates, evidence-driven fix discipline |
| [`style-presets`](skills/style-presets/SKILL.md) | One figure, several finishes — **academic (default) / web / tech** | Token-dict presets (`get_style()`), swap skins without touching geometry; GPU-pipeline example regenerates all three from one declaration |

| 技能 | 何时用 | 产出 |
|---|---|---|
| `paper-figure` | 65 类论文图型：45 类按规范绘制 + 20 类可运行科研模板 | 打印样式、SVG/PDF/PNG、来源记录与离线画廊 |
| `codex-figure-workflow` | Codex 从源码完成整套架构图 | 完整指南、参数化图源、结果图和验收实战 |
| `game-arch-diagram` | 软件 / 游戏架构图（分层带 + 状态机 + 反馈回路） | 设计语言七件套（骑缝标题牌 / 语义色浅底 / 色条 / 顺序徽标 / 白描边标签）+ 视觉裁判实战缺陷库 |
| `hand-svg-structure` | 复刻位图结构图（框图/流程/网络/示意） | 位图几何配色程序化探测 + 防平铺导出页工具 |
| `parametric-diagram` | 从零画会反复修改的结构图 | 参数化脚本即图源：几何/拓扑/样式三段声明，改声明重跑即再生 |
| `data-figures-rerender` | 数据图（散点/柱状/斜率）——点是真数据 | 同一批冻结表格重渲染，编码逐项保持；绝不手挪数据点 |
| `declarative-engine` | 网格型框图/网络总览/部署流程图 | 声明式引擎配置语法 + 三份真实论文图配置 |
| `visual-acceptance` | 交付前必过 | 活页面截屏、平铺自检、独立视觉裁判逐字对照、按像素证据修根因 |
| `style-presets` | 同一张结构图出科研风（默认）/web 风/科技风多版本 | 样式令牌字典 `get_style()`，换肤不动几何内容；GPU 流程图一图三款示例 |

Codex 新增组合入口：[codex-figure-workflow](skills/codex-figure-workflow/SKILL.md)，适用于基于实际项目制作结构图并完成整套交付。它复用以上路线，不替代它们。

## More before/after / 更多对比

<p>
  <img src="assets/before_after_mlp.png" width="49%" alt="MLP before/after">
  <img src="assets/before_after_roadmap.png" width="49%" alt="Roadmap before/after">
</p>

*Left pair: textbook network figure — bitmap reference vs parametric-script replica (stacked arrowhead clusters, upright digit subscripts). Right pair: research roadmap — matplotlib original vs hand-authored SVG.*

## Results / 战绩

| Batch | Figures | Outcome |
|---|---|---|
| Journal manuscript figures (re-render) | 6 | 6/6 PASS, first round |
| Journal submission figures (7 + graphical abstract) | 8 | 8/8 PASS, first round |
| Thesis architecture figures (redrawn) | 11 | 11/11 PASS after 2 rounds |
| Single-figure replications (ECG pipeline, MLP) | 2 | PASS |
| Game architecture figure (design-polish rounds) | 1 | PASS after 2 judge rounds — 6 collision defects catalogued into [`game-arch-diagram`](skills/game-arch-diagram/SKILL.md) |

All accepted figures shipped as **SVG (vector) + 600 dpi PNG**, judge-verified string-by-string and arrow-by-arrow against their references.

所有通过验收的图均以 **SVG 矢量 + 600 dpi PNG** 交付，由独立视觉裁判逐字符串、逐箭头对照参考图后放行。

## Install / 安装到你的 Agent

Each folder under [`skills/`](skills/) is a self-contained skill in the common `SKILL.md` format (frontmatter + workflow). To use:

```bash
# Claude Code / ZCode — per project
cp -r skills/hand-svg-structure  .claude/skills/
# or globally
cp -r skills/hand-svg-structure  ~/.claude/skills/
```

Then just ask your agent: *"Replicate this reference figure as a print-quality SVG"* — the skill drives the workflow (probe → author → export → judge).

每个技能目录自带 `SKILL.md`（frontmatter + 工作流）与所需工具脚本，复制到 Agent 的技能目录即可被自动发现。数据图路线的 `load()` 需要对接你自己的冻结结果表。

## Tested with / 实测环境

The original paper cases were tested with **GLM-5.3-Flash** (ZCode). The added website architecture case was completed in **Codex desktop**. The workflow is model-agnostic.

原有论文案例由 **GLM-5.3-Flash**（ZCode）完成；新增网站架构图案例在 **Codex 桌面环境**完成。方法不绑定模型——具备文件读写、浏览器渲染与独立视觉检查能力的 Agent 均可使用。

## Repository layout / 目录

```
figcraft-skills/
├── skills/
│   ├── paper-figure/           # 65-type routing, 20 scientific renderers, gallery
│   ├── hand-svg-structure/     # probe tool + export pages + examples
│   ├── parametric-diagram/     # make_fig.py template + example
│   ├── data-figures-rerender/  # re-render template + PITFALLS.md
│   ├── declarative-engine/     # config syntax + manuscript configs
│   ├── visual-acceptance/      # check_tiling.py + judge templates
│   ├── codex-figure-workflow/   # Codex end-to-end entry
│   └── game-arch-diagram/      # architecture design language + defect catalogue
├── examples/pony-tarot/         # Codex case, sources, renders, evidence
├── CODEX.md                    # Codex workflow guide
├── assets/                     # before/after composites
├── METHOD.md                   # the 8 principles behind every route
└── LICENSE                     # MIT
```

Start with [`METHOD.md`](METHOD.md) — the eight principles (declare-don't-draw, semantic palettes, grid rhythm, probe-don't-eyeball, …) that every route assumes.

## License / 许可

[MIT](LICENSE) — use it, fork it, ship it. Example figures included for demonstration; please don't reuse them in your own papers.
