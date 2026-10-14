# 用 Codex 完成一套 figcraft 制图

这份指南把“读项目 → 理清结构 → 参数化绘图 → 浏览器导出 → 视觉验收 → 交付”串成完整流程。附带小马宝莉主题塔罗网站的真实案例、图源和结果图。案例在 Codex 桌面环境完成，不依赖特定模型名称。

## 65 类选型与科研图

复杂结构图或科研数据图先使用 [paper-figure](skills/paper-figure/SKILL.md)。它能独立安装，提供 45 类布局规范与 20 类可运行科研模板；本指南的源码事实梳理与实际视觉验收仍适用。合成演示不可用作实验结果。

## 直接使用

把下面这段发给 Codex，替换技能库和项目路径即可：

```text
请读取 <figcraft-skills路径>/skills/codex-figure-workflow/SKILL.md，
基于 <项目路径> 的实际源码制作一张架构图。
先核对页面、模块、数据与部署关系，再生成参数化 SVG 和高清 PNG。
完成活页面检查、导出检查及独立视觉验收；保留图源和验收记录。
未实现的模块不要画成已实现，最后展示结果图并提供文件链接。
```

该入口是组合技能，依赖本库中的其他技能和工具。若安装到个人 Codex 技能目录，应保留整个库的相对结构；最简单的方式是把本库作为项目资源，通过上述绝对路径调用。仅复制入口文件夹会使其相对链接失效。

## 1. 从事实整理内容

先读项目说明和约束，再读入口、模块、配置及存储实现。优先用 `rg --files` 和 `rg` 定位，不需要通读依赖、构建缓存或第三方仓库的全部代码。

整理一份小清单：

| 要素 | 需要回答的问题 |
|---|---|
| 运行边界 | 浏览器、服务器、外部服务分别处理什么？ |
| 模块 | 哪些是页面、面板、共享组件或逻辑函数？ |
| 数据 | 来自静态文件、运行状态、本地存储还是远程接口？ |
| 关系 | 箭头表示调用、读写、数据流还是部署？ |
| 状态 | 哪些已实现，哪些仍是计划或占位？ |

先写准内容再摆框。单页弹窗不要画成多个路由；本地模板解读不要画成 AI 服务；静态站点不要凭空加后端和数据库。

## 2. 选择路线

| 任务 | 使用技能 |
|---|---|
| 基于源码从零画架构图/流程图 | [parametric-diagram](skills/parametric-diagram/SKILL.md) |
| 复刻已有位图结构图 | [hand-svg-structure](skills/hand-svg-structure/SKILL.md) |
| 用声明式引擎组织网格大图 | [declarative-engine](skills/declarative-engine/SKILL.md) |
| 按真实结果表重绘统计图 | [data-figures-rerender](skills/data-figures-rerender/SKILL.md) |
| 任一路线的交付验收 | [visual-acceptance](skills/visual-acceptance/SKILL.md) |

本案例选择参数化 SVG。文生图适合场景插画，不适合本次要求准确中文、模块名和箭头关系的架构图。

## 3. 编写可改的图源

将声明分成四组：`CONTENT`（文字）、`LINKS`（关系）、`NODES/COLS/ROWS`（位置尺寸）、`STYLE`（视觉）。完整例子见 [make_architecture.py](examples/pony-tarot/make_architecture.py)。

箭头端点从节点几何推导；颜色表达语义；按列宽、行距和边距统一对齐。文字超出宽度时优先精简内容、合理换行或增加框宽，避免不断缩字号。字体要在实际渲染环境可用。

SVG 和预览 HTML 都由脚本生成。后续改动回到脚本，再重新生成和验收。

## 4. 在 Codex 中预览与导出

浏览器控制优先用当前会话提供的工具。使用 `mcp__cua_repl` 时，先按工具要求只执行一次入口调用，阅读返回文档，再使用其中描述的 API。不要复制其他环境的 Playwright 调用，也不要假定 tab ID 永远不变。

本次使用了以下路线：

1. 从新 SVG 生成内联 HTML；用临时本地 HTTP 服务访问。
2. 普通窗口打开 `preview.html`，截图并查看整体显示。
3. 以精确 viewport 截取 1× 页。
4. 因 2× 页面高为 2440，使用上下半页，每页 3200 × 1220。
5. 普通截图保存为 `export-top.png` 和 `export-bottom.png`，用 Pillow 合成。

这条浏览器导出路线避免 `fullPage` 和独立 SVG 截图的已知平铺风险。其他经过验证的矢量渲染器也可用，但不能省略实际预览和输出验收。

PowerShell 示例（在库根目录执行；Python 路径请按实际环境替换）：

```powershell
$figurePython = 'C:\Asoftware\anaconda3\python.exe'
& $figurePython '.\examples\pony-tarot\make_architecture.py'
& $figurePython '.\skills\hand-svg-structure\prepare_export_pages.py' '.\examples\pony-tarot\pony-tarot-architecture.svg' --halves
& $figurePython -m http.server 3001 --bind 127.0.0.1 --directory '.\examples\pony-tarot'
```

服务器命令会持续运行，应放在单独终端或可保留的执行会话中；端口已占用时换空闲端口。不要停止项目自己的预览服务。

生成页与 viewport 的对应关系：

| 页面后缀 | 本案例 viewport | 用途 |
|---|---|---|
| `@1x.html` | 1600 × 1220 | 原尺寸检查 |
| `@2x.html` | 3200 × 2440 | 完整高分辨率页 |
| `@2x_top.html` | 3200 × 1220 | 上半部截图 |
| `@2x_bot.html` | 3200 × 1220 | 下半部截图 |

截取两半后执行：

```powershell
& $figurePython '.\examples\pony-tarot\export_png.py'
& $figurePython '.\skills\visual-acceptance\check_tiling.py' '.\examples\pony-tarot\pony-tarot-architecture.png'
```

案例导出脚本需要 Pillow、案例两张分片截图及 Windows 微软雅黑字体；这是实战脚本，不是跨平台通用导出器。换平台时同时调整 SVG 字体声明和字体测宽路径。

600 dpi 元数据不会增加像素。本次最终为 3200 × 2440 px，按 600 dpi 对应约 13.55 × 10.33 cm；更大印刷尺寸优先使用 SVG，或提高真实导出分辨率。

## 5. 验收闭环

验收包含三类证据：

- **语义与几何**：节点与实际实现一致；文字完整；箭头方向准确；无截断、重叠或越界。
- **渲染与导出**：普通窗口预览正常；最终尺寸正确；运行平铺检测。半图差异接近零可提示重复，但自然对称图也可能接近零，需要结合目视判断。
- **独立视觉检查**：给裁判成品、图源、事实依据和验收标准；让其检查文字、结构、箭头和画质，返回 JSON。原创图没有位图参考时，使用内容清单和源码作为语义依据，不虚构参考图。

独立裁判提示词：

```text
请独立验收这张项目架构图，只读文件，不修改源码。
成品：<PNG绝对路径>
图源：<绘图脚本绝对路径>
事实依据：<项目入口/配置/关键模块路径>
检查：文字完整可读，节点关系符合实现，箭头不穿框，边界不裁切，
布局无重叠，导出无重复平铺。没有位图参考，以源码和内容声明核对。
返回 {"page":"...","verdict":"PASS或FAIL","issues":[...]}，
每个问题包含位置与可观察证据。
```

若环境不能委派独立裁判，记录“未执行独立验收”，不要把自检写成独立 PASS。收到问题后改图源，再生成 SVG、导出页和 PNG，只复核相关问题及回归点。

## 6. 交付和保留

至少保留图源、SVG、PNG和验收记录。导出脚本依赖的中间截图也要保留，或明确写出重新捕获的方法。交付时显示 PNG，链接 SVG；说明图对应的源码快照，不把它说成永久有效。

临时服务只清理自己启动的实例，浏览器窗口恢复普通尺寸。不要修改业务代码来配合画图。

## 本次实战与结果

案例：小马宝莉主题塔罗网站，2026-10-12。主图展示静态构建与部署，以及浏览器内的交互、抽牌、内容和本地存储。独立视觉裁判返回 PASS；完整步骤、限制和记录见 [CASE.md](examples/pony-tarot/CASE.md)。

![Codex 塔罗网站架构图实战结果](examples/pony-tarot/pony-tarot-architecture.png)

[可编辑 SVG](examples/pony-tarot/pony-tarot-architecture.svg) · [高清 PNG](examples/pony-tarot/pony-tarot-architecture.png) · [图源](examples/pony-tarot/make_architecture.py) · [验收记录](examples/pony-tarot/acceptance.json)
