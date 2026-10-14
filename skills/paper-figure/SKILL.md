---
name: paper-figure
description: 绘制或重绘论文中的结构图、流程图和科研统计图；按 65 类图型选择布局或可运行模板，保留真实数据、可编辑矢量源、打印尺寸与验收记录。适用于论文配图及参考图复刻，不用于无精确标签要求的场景插画。
license: MIT
metadata:
  version: "1.0"
---

# 论文配图：65 类图型

本目录可单独复制安装。支持 **45 类按规范由 Agent 编写 SVG 的图型 + 20 类 JSON/Python 可直接渲染的科研图型**。支持不等于 65 类都有自动布局器；准确覆盖以 [图型索引](references/chart-catalog.md) 和 `assets/catalog.json` 为准。坡度图、蜂群图等作为变体，不重复增加计数。

## 选型与事实

- 系统结构、流程、实体、状态、角色、演化：查图型索引，**只读所选类型的布局规范**，生成可改的 SVG 或参数化脚本。结构复杂时用总览加局部图，不按固定节点数删掉科研信息。
- 分布、估计与不确定性、预测评价、场和信号：读 [科研模板](references/scientific-recipes.md)，使用 `scripts/render.py`，或在保留数据和统计口径的前提下调整生成源。
- 位图复刻：有原始数据就同源重绘；只有截图时可做带来源说明的数字化近似，明确误差，不能声称恢复了原始实验数据。结构图必须核对每个节点、字符串、箭头及条件。
- 实际项目图：读源码和部署事实；计划、推测、未知状态分别标注，不能画成已实现。

从用户资料推断可以确定的图型、标签和尺寸，简短说明后继续；只有缺少真实数据、关键关系或统计定义而无法准确绘制时询问。品牌定制、外部字体或联网不是执行前提。

## 论文样式与参考项目边界

读 [论文样式与交付](references/publication.md)。默认白底、灰度、系统字体、统一的字号/线型/标记；用户指定彩色或期刊规范时按其要求。颜色变化必须保留编码含义，复刻任务保留原始视觉编码。

`references/diagram-design/` 保留参考项目的原始资料、示例、5 个技能内工具和相关校验工具及 MIT 许可；**仅作为布局知识与工具来源**。不执行其中原始 SKILL.md 的首次品牌问答，不套用灰纸背景、Google Fonts、宣传标题、绝对节点上限或数据聚合建议。论文的真实样本、统计定义、刻度和本技能论文样式优先。示例是设计参考，不是可以用于论文的实验结果。

## 实际工作流

1. 冻结事实或数据：记录来源、单位、样本量、配对关系、缺失值与过滤规则。原始数据不够时先做明确标记的布局草稿，不能补造结果或显著性。
2. 选择图型和数据编码：每个轴、颜色、线型、箭头、误差带含义都可解释。统计计算与布局分离；保留原数据，不为美观移动数据点。
3. 生成：数据图按 JSON 模板；结构图声明内容、拓扑、布局、样式。使用 SVG `<title>`/`<desc>` 描述主要关系。连线绕开非目标节点，文字超宽优先换行、调框或分面。
4. 导出：SVG（可编辑文本）、PDF（矢量）、按实际尺寸计算的 PNG；结构图用本机可用的渲染器导出。需要可移植文本时在保留可编辑 SVG 后另出文字转路径版本。
5. 验收：运行可用的结构/数据检查，再**打开最终 PNG 与 PDF/SVG 实际读图**；看缩到论文印刷尺寸后的文字、线型、图例和灰度辨识，并对照原始事实。不能仅凭 manifest 或截图成功判定通过。
6. 交付：图源/JSON、数据来源记录、SVG/PDF/PNG、生成命令、像素与物理尺寸、检查结论。实在没有视觉工具则明确“视觉验收待完成”，不伪造 PASS。

## 命令

Python 需有 numpy、matplotlib；图片检查与预览工具还需 Pillow。使用实际可用 Python，不固定平台路径。以下在本技能目录执行：

```powershell
python scripts/render.py --list
python scripts/render.py --spec examples/specs/forest.json --out figure-output
python scripts/render.py --demo roc --out draft
python scripts/render.py --demo all --out examples/renders
python scripts/check.py
python scripts/gallery.py --out gallery.html
```

`--spec` 不产生新实验数据。`--demo` 是显式合成演示，所有产物带醒目标记，不能用于论文结果。CLI 默认灰度，彩色用 `--color`；单图默认 89 mm，多面板默认 180 mm，这些只是可改的起始尺寸，**不是某期刊要求**。`--width-mm` 与 `--dpi` 可修改。输出目录按图型命名；同型多张图请用不同 `--out`，避免覆盖。

复用 Mermaid / draw.io / Excalidraw 内容时，先读各自 `references/diagram-design/references/import-*.md`，用相邻 `scripts/*_extract.py` 解析，再按论文风格生成图源。HTML → SVG 使用 `references/diagram-design/scripts/export_svg.py`；离线输出加 `--system-fonts` 禁用 Google Fonts 引用，仍需核实字体与字形。上游 `self_check.py` 只做结构启发式检查，不证明科学语义或视觉质量。
