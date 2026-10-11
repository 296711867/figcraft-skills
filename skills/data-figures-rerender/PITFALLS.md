# 数据图重渲染坑清单（全部真实踩过，出图前过一遍）

## 路径与数据

1. **论文脚本的数据路径常失效**：改版迁移后 `OUT = HERE.parent.parent / "xxx" / "outputs"` 指向不存在的目录。先 `find <项目根> -name "<关键csv>"` 定位真实位置，逐个核实存在 + 行数，再写新脚本。
2. 读 CSV 前先 `head` 看列名——历史脚本的列名可能与当前表不一致。

## matplotlib 渲染

3. **log 轴上禁止线性偏移文本坐标**：`ax.text(x - 0.15, ...)` 在 log 轴上，负数经 log 变换为非法位置，600 dpi 栅格化时报 `RuntimeError: FT_Render_Glyph ... raster overflow`。要偏移用**乘法**：`ax.text(x * 1.35, ...)`（0.15 个单位 ≈ log 轴上 0.06 个 decade）。
4. **patches 默认裁剪到 axes 包围盒**：`FancyBboxPatch` 在 axes 分数坐标里贴边锚（y=0.0）+ `boxstyle pad>0`，框的底边与圆角被无声裁掉（无报错、只有图难看）。锚点留出 ≥pad 的余量，或 `clip_on=False`。
5. **多行文本锚点语义**：默认 `va="baseline"` 锚第一行基线——两行标注放在标记正下方时首行仍会压住标记；改 `va="top"` 让整块垂下来，或 `ha="left"` 放到标记右侧。
6. **盒子标题溢出**：matplotlib 不自动缩字，标题字号 × 标题宽 > 框宽就顶边框。出图后逐框目检，调字号（8→7.4 级别的小步调）比改框宽安全。
7. `savefig` 的 `dpi` 参数优先于 rcParams 的 `savefig.dpi`；PNG 想提清晰度在 save() 里显式传。
8. `svg.fonttype="path"`（matplotlib 默认）把文字转路径——任何环境打开不跑字体，代价是不可再编辑文字；要可编辑改 `"none"`。

## 流程

9. 改 SVG/脚本后重出 PNG，**重建导出页必须在改完之后**（顺序反了嵌旧图，白跑一轮验收）。
10. 交付前 numpy 半图对比自检平铺（见 05-verification/check_tiling.py）。
