"""figcraft parametric-diagram: geometry, content, topology and style declarations.
Run with Python to regenerate the editable SVG and browser preview page.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent
W, H = 1600, 1220

# Geometry: fixed column rhythm, common box sizes, symmetric margins.
COLS = (80, 595, 1110)
BOX_W = 410
ROWS = ((395, 160), (610, 235), (900, 160))

# Semantic palette: three accents, neutral connectors; no shadows or gradients.
STYLE = {
    "ink": "#263442", "muted": "#647386", "edge": "#8C99A8",
    "paper": "#FFFFFF", "group": "#D6DDE5",
    "ui": ("#7657A4", "#F4F0FA"),
    "logic": ("#327E82", "#EFF7F6"),
    "data": ("#B28A46", "#FCF6EA"),
    "neutral": ("#667487", "#F5F7F9"),
    "font": "'Microsoft YaHei', 'PingFang SC', Arial, sans-serif",
}

# Content: line breaks are intentional, independently editable from geometry.
CONTENT = {
    "build": ("Next.js · React · TypeScript", "开发源码 / pony-tarot", ["npm run build"]),
    "export": ("静态导出", "next.config.ts · output: export", ["out/：HTML / CSS / JS / 图片 / 字体"]),
    "host": ("静态 HTTP 服务器", "当前：本地预览 / 127.0.0.1:3000", ["可部署至静态托管平台"]),
    "home": ("家园首页与会话编排", "Home · app/page.tsx", ["建筑导航 · 打开 / 关闭功能面板", "React 状态：面板 / 设置 / 历史", "问题与抽牌结果在浏览器内处理"]),
    "theme": ("主题与交互表现", "ThemeSwitch · globals.css", ["明亮 / 暗色 · 用户选择即刻生效", "桌面 / 手机布局 · 标题渐变遮罩", "翻牌 / 光晕 / 星尘 · 可关闭动效"]),
    "assets": ("插画与卡面资源", "public/art · public/cards · fonts", ["日景 / 夜景 × 桌面 / 手机", "卡面 ID → manifest.json", "正式塔罗卡面由用户后续提供"]),
    "panels": ("功能面板", "单页内打开，不是五个独立路由", ["ReadingPanel · 今日一牌 / 三牌占卜", "LibraryPanel · 78 张图鉴与牌义", "JournalPanel · 本地魔法记录", "SettingsPanel · 主题 / 动效 / 逆位", "PanelDialog / TarotCard · 通用交互"]),
    "engine": ("抽牌与本地解读", "lib/engine.ts", ["drawCards · Fisher–Yates 无重复抽牌", "dailyDraw · 按本地日期固定每日牌", "interpret · 拼接牌义与角色话术", "makeReading · 问题 / 牌 / 解读快照"]),
    "content": ("牌库与角色内容", "data/cards.ts · data/personas.ts", ["78 张牌：正逆位关键词与牌义", "M6：六种开场与收尾语气", "角色切换不改变抽到的牌", "当前采用本地模板，不调用 AI"]),
    "actions": ("保存与偏好操作", "Home 回调 · 功能面板触发", ["保存 / 删除 / 清空 / 文本导出", "主题 / 动效 / 逆位偏好", "存储失败提示，不阻止查看结果"]),
    "storage": ("本地存储接口", "lib/storage.ts", ["readHistory / writeHistory", "readSettings / writeSettings", "结果快照与设置分别读写"]),
    "local": ("浏览器 localStorage", "不需要账号、云数据库或后端 API", ["记录：最多 50 条结果快照", "偏好：主题 / 动效 / 逆位", "清理浏览器数据会丢失记录"]),
}

# Node geometry and kinds are declared separately from their contents.
NODES = {
    "build": (COLS[0], 138, BOX_W, 90, "neutral"),
    "export": (COLS[1], 138, BOX_W, 90, "neutral"),
    "host": (COLS[2], 138, BOX_W, 90, "neutral"),
}
for row, ids in zip(ROWS, (("home", "theme", "assets"), ("panels", "engine", "content"), ("actions", "storage", "local"))):
    for col, node, kind in zip(COLS, ids, ("ui", "logic", "data")):
        NODES[node] = (col, row[0], BOX_W, row[1], kind)

# Topology: arrows denote calls / reads / writes, not returned data.
LINKS = [
    ("build", "export", "构建", "horizontal"),
    ("export", "host", "提供文件", "horizontal"),
    ("home", "theme", "切换外观", "horizontal"),
    ("theme", "assets", "加载资源", "horizontal"),
    ("panels", "engine", "发起占卜", "horizontal"),
    ("engine", "content", "读取内容", "horizontal"),
    ("actions", "storage", "调用接口", "horizontal"),
    ("storage", "local", "读写本地", "horizontal"),
    ("home", "panels", "打开面板", "vertical"),
    ("panels", "actions", "保存 / 偏好", "vertical"),
]


def text(x, y, value, size=17, color=None, weight=400, anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color or STYLE["ink"]}">{escape(value)}</text>'


def box(node):
    x, y, w, h, kind = NODES[node]
    title, code, lines = CONTENT[node]
    edge, fill = STYLE[kind]
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{edge}" stroke-width="1.4"/>']
    parts.append(text(x + 23, y + 33, title, 21, edge, 600))
    parts.append(text(x + 23, y + 59, code, 14, STYLE["muted"]))
    start = 80 if kind == "neutral" else 90
    for i, line in enumerate(lines):
        parts.append(text(x + 23, y + start + 26 * i, line, 16 if kind == "neutral" else 17))
    return "\n".join(parts)


def link(source, target, label, direction):
    sx, sy, sw, sh, _ = NODES[source]
    tx, ty, tw, th, _ = NODES[target]
    if direction == "horizontal":
        p, q = (sx + sw + 2, sy + sh / 2), (tx - 2, ty + th / 2)
        lx, ly, anchor = (p[0] + q[0]) / 2, p[1] - 12, "middle"
    else:
        p, q = (sx + sw / 2, sy + sh + 2), (tx + tw / 2, ty - 2)
        lx, ly, anchor = p[0] + 19, (p[1] + q[1]) / 2 + 5, "start"
    arrow = f'<path d="M {p[0]} {p[1]} L {q[0]} {q[1]}" fill="none" stroke="{STYLE["edge"]}" stroke-width="1.6" marker-end="url(#arrow)"/>'
    return arrow + text(lx, ly, label, 13, STYLE["muted"], anchor=anchor)


def build():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="figure-title figure-desc">',
             '<title id="figure-title">小马利亚魔法塔罗当前实现架构</title>',
             '<desc id="figure-desc">静态构建和部署，浏览器中的交互、核心逻辑、静态内容及本地存储，箭头表示调用或读取方向。</desc>',
             f'<defs><marker id="arrow" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" refX="7.5" refY="4.5" orient="auto"><path d="M 0 0 L 7.5 4.5 L 0 9 Z" fill="{STYLE["edge"]}"/></marker></defs>',
             f'<rect width="{W}" height="{H}" fill="{STYLE["paper"]}"/>',
             f'<g font-family="{STYLE["font"]}">',
             text(80, 60, '小马利亚魔法塔罗｜当前实现架构', 34, weight=600),
             text(80, 94, '双主题家园 · 78 张牌义 · 免费使用 · 浏览器本地运行', 17, STYLE["muted"]),
             f'<rect x="40" y="290" width="1520" height="822" rx="14" fill="none" stroke="{STYLE["group"]}" stroke-width="1.5" stroke-dasharray="7 5"/>',
             '<rect x="64" y="277" width="260" height="27" fill="#FFFFFF"/>',
             text(76, 298, '浏览器运行边界', 16, STYLE["muted"], 500)]
    for x, title, subtitle, kind in zip(COLS, ('页面与交互', '逻辑与状态', '内容与存储'), ('PRESENTATION', 'CLIENT LOGIC', 'LOCAL RESOURCES'), ('ui', 'logic', 'data')):
        parts += [text(x + 205, 342, title, 23, STYLE[kind][0], 600, 'middle'), text(x + 205, 367, subtitle, 12, STYLE["muted"], anchor='middle')]
    parts.append(f'<path d="M {COLS[2] + BOX_W / 2} 230 V 287" stroke="{STYLE["edge"]}" stroke-width="1.6" fill="none" marker-end="url(#arrow)"/>')
    parts.append(text(COLS[2] + BOX_W / 2 + 18, 264, '首次加载', 13, STYLE["muted"]))
    parts.extend(link(*entry) for entry in LINKS)
    parts.extend(box(node) for node in NODES)
    parts.append(text(80, 1152, '箭头表示调用、读取或写入方向；界面与逻辑在同一个前端应用中协作。', 16, STYLE["muted"]))
    parts.append(text(80, 1186, '实际状态：无业务后端，问题不发送到 AI；正式卡面通过 ID 映射接入。', 16, STYLE["muted"]))
    parts.append(text(1520, 1186, '源码快照 · 2026-10-12', 13, STYLE["muted"], anchor='end'))
    parts += ['</g>', '</svg>']
    return '\n'.join(parts) + '\n'


if __name__ == '__main__':
    svg = build()
    path = ROOT / 'pony-tarot-architecture.svg'
    path.write_text(svg, encoding='utf-8')
    html = f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>小马利亚魔法塔罗 · 架构图</title><style>html,body{{margin:0;background:#fff}}svg{{display:block;width:100%;height:auto}}</style>{svg}</html>'
    (ROOT / 'preview.html').write_text(html, encoding='utf-8')
    print(f'Generated {path} ({W}x{H}); 12 nodes, 10 declared links.')
