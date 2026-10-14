---
name: codex-figure-workflow
description: 使用 Codex 从项目源码或参考图完成架构图、流程图与结构图，串联 figcraft 的参数化 SVG、浏览器导出和视觉验收，并保留可重生成的源文件与案例证据。
---

# Codex 制图工作流

用户要求基于真实项目画架构图，或用 Codex 完成 figcraft 整套结构图工作时使用。科研图型选型或新绘制统计图可用 [paper-figure](../paper-figure/SKILL.md) 的 65 类入口；已有数据图忠实重绘仍走 `data-figures-rerender`，不套用本案例的三列布局。

先读 [Codex 完整指南](../../CODEX.md)。需要核对成品结构、尺寸和实战时，再读 [塔罗网站案例](../../examples/pony-tarot/CASE.md)。

## 执行顺序

1. **确认图的事实来源。** 项目图读入口、模块、存储和部署配置；复刻图读参考图。写清节点、边和未实现功能，避免把设想画成已有能力。
2. **选路线。** 原创结构图读 [parametric-diagram](../parametric-diagram/SKILL.md)；位图复刻读 [hand-svg-structure](../hand-svg-structure/SKILL.md)；网格型大图可读 [declarative-engine](../declarative-engine/SKILL.md)。共同原则见 [METHOD.md](../../METHOD.md)。
3. **以脚本为图源。** 内容、拓扑、几何、样式分开声明。修改声明后重生成 SVG，避免手改导出文件。把图输出放进独立目录，不混入业务代码。
4. **预览和导出。** SVG 内联进 HTML，先检查普通窗口下的活页面。然后用精确尺寸 viewport 普通截屏；需要分片时生成上下半页，逐页截取后拼接。浏览器具体 API 以当前工具文档为准。
5. **验收。** 使用 [visual-acceptance](../visual-acceptance/SKILL.md)：文字/箭头/边界检查、平铺检测、独立视觉裁判。此步骤需要独立评审时，委派一名具备读图能力的子代理，只读图源、成品和事实依据。无委派能力则如实记录未完成独立验收。
6. **交付。** 保存 SVG、PNG、源脚本、必要导出资源和验收记录；展示结果图并链接可编辑版本。只停止自己为此次导出启动的临时服务。

## Codex 适配要点

- 首次浏览器调用遵守该工具的初始化要求；持久会话不要照搬“每次调用都是新内核”的旧工具假设。
- 不固定浏览器 tab ID、工具名、端口或 Python 路径。先发现运行环境和 API；中文字体需要明确且可用。
- 导出页必须在最新 SVG 生成之后重建。截图宽高、分片范围与合成尺寸必须一致。
- PNG 的 600 dpi 是打印元数据，清晰度由实际像素决定；同时报告像素尺寸。
- `check_tiling.py` 是重复平铺的启发式检查，不代替人工/独立读图。
- 不把案例中的静态部署、localStorage、三列布局或 Windows 字体当成所有项目的要求。
