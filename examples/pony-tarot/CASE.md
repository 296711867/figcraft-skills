# 实战：小马宝莉主题塔罗网站架构图

用户希望看看整个项目的架构，并认可了成品。本案例保留 2026-10-12 的实际实现快照，用于说明 Codex 如何完成 figcraft 整套流程。

## 事实与结构

项目使用 Next.js、React、TypeScript，构建后静态导出。首页通过 React 状态打开抽牌、图鉴、记录和设置面板；抽牌与解读在浏览器执行。78 张牌的牌义与角色话术来自本地内容；正式卡面待用户提供。主题有明亮/暗色两套；历史快照和偏好保存在 localStorage。

图按三列组织：页面与交互、逻辑与状态、内容与存储。顶部为构建、静态导出和 HTTP 托管；虚线框内为浏览器运行边界。箭头表示调用或读写，不表示返回流。本图没有后端 API、账号、云数据库或 AI 解读服务，因为当时的源码没有这些能力。

本库未复制整个网站源码，因此这里是案例快照，不能单靠案例文件重新审计业务实现。用于新项目时必须重新读该项目源码，替换内容及拓扑。

## 实际完成的步骤

1. 阅读 figcraft 的方法、参数化绘图、导出页工具与视觉验收说明。
2. 核对网站入口、面板、抽牌函数、静态资源、存储与构建配置。
3. 编写 `make_architecture.py`：分开声明内容、几何、拓扑和样式，生成 SVG 及预览页。
4. 画布 1600 × 1220，三列等宽 410；用紫、青、金三种语义色与中性灰连线。
5. 内联 SVG 导出页；普通窗口检查预览，再分别截取 2× 上下半页。
6. 用 `export_png.py` 合成 3200 × 2440 PNG，写入 600 dpi；用真实微软雅黑字体检测节点内文字宽度。
7. 执行平铺检测；独立视觉裁判对照图源与实际实现检查，返回 PASS、无问题。
8. 保存成品与验收证据；停止临时导出服务，保留原网站预览服务。

## 结果与检查范围

| 检查 | 实际结果 |
|---|---|
| PNG | 3200 × 2440 px，600 dpi 元数据 |
| 节点文字测宽 | 全部在声明宽度预算内；不代表标题、箭头等所有文字均经过程序测宽 |
| 平铺启发式检查 | verticalDifference 18.9，horizontalDifference 18.0，ok |
| 独立视觉裁判 | PASS，issues 为空 |
| 业务代码 | 此次绘图未修改网站代码 |

这些结果只对应当前保留的成品。重新生成或改变字体、文字、结构后，应重新验收。

![最终架构图](pony-tarot-architecture.png)

## 文件与重生成

- [make_architecture.py](make_architecture.py)：可改的内容、布局、箭头和样式声明。
- [pony-tarot-architecture.svg](pony-tarot-architecture.svg)：可编辑矢量成品。
- [pony-tarot-architecture.png](pony-tarot-architecture.png)：高清结果图。
- [export_png.py](export_png.py)：分片合成与节点文字测宽；依赖 Pillow 和 Windows 字体。
- `export-top.png` / `export-bottom.png`：原始浏览器分片，保留供复核及重合成。
- [acceptance.json](acceptance.json)：实战验收记录。

先运行图源，再用库内 `prepare_export_pages.py --halves` 重建导出页、重新截图，最后合成和验收。仅修改图源后直接运行合成脚本，会继续使用旧截图。完整命令与 Codex 工具适配见 [CODEX.md](../../CODEX.md)。
