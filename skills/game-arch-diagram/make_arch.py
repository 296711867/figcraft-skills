# -*- coding: utf-8 -*-
"""图：字狂潮 v2.3 · 游戏架构图（设计打磨版）。

图=声明：几何 BOXES / 内容（label+sub）/ 拓扑 EDGES / 样式 STYLE 四层分离。
设计语言：语义色浅底 + 左侧色条 + 骑缝式带标题牌 + 标签白描边 + 三级字号节奏 + 更新顺序徽标。
产物：arch-v2.svg（1720×1400；PNG 由内联页 2× 截屏拼接得到）。
"""
from pathlib import Path

# ---------- 声明层：几何 ----------
W, H = 1720, 1400

GROUPS = {  # id → (x, y, w, h, 带标题牌, 右上角标, 语义色)
    "input": (90, 100, 1210, 130, "输入层", "事件驱动", "#8a8984"),
    "core": (90, 520, 1210, 430, "对局核心循环", "updatePlay(1/60) · 场景 play · 60Hz", "#2a78d6"),
    "meta": (90, 1000, 1210, 170, "局外成长 · v2", "跨局持久 · 事件 + 结算", "#eb6834"),
    "plat": (90, 1220, 1210, 120, "平台层", "常驻", "#1baf7a"),
    "build": (1400, 100, 300, 700, "构建与发布", "双端产物", "#8a8984"),
}

BOXES = {  # id → (x, y, w, h, 主标, 子标, 语义色)
    "kb":     (120, 146, 360, 64, "键盘", "WASD · 数字 1~0 · B/C/T/E/R/P/M", "#8a8984"),
    "mouse":  (520, 146, 360, 64, "鼠标 · 触摸", "虚拟摇杆 joyVec · 点击 uiHit", "#8a8984"),
    "wxtap":  (920, 146, 340, 64, "微信触摸路径", "wx.onTouchStart · __wxTap 合成", "#8a8984"),
    "player": (120, 590, 350, 140, "player 火柴人", "心血 5♥→8 · 护盾 · 无敌帧\nWASD/摇杆 · 受击/死亡流程", "#2a78d6"),
    "enemies":(525, 590, 350, 140, "enemies 数字大军", "LV_WAVES 波次表 · 15 种怪\n碰撞 / 弹幕 · 精英加速光环", "#2a78d6"),
    "boss":   (930, 590, 350, 140, "boss BOSS 战", "BOSS_DEF 技能池 ×14\n三形态 · 重生 · 狂暴", "#2a78d6"),
    "weapons":(120, 770, 350, 140, "weapons 武器", "6 武器 × 5 级\n满级 + 专属被动 → 6 进化", "#2a78d6"),
    "items":  (525, 770, 350, 140, "items 掉落", "粉笔屑 = 经验 · 道具 ×6\n磁吸拾取 · 30s 闪烁消失", "#2a78d6"),
    "upgrades":(930, 770, 350, 140, "upgrades 三选一", "新武器 · 被动 ×8 · 回心血\n进化卡必出首位（金色）", "#2a78d6"),
    "chalk":  (125, 1050, 270, 90, "粉笔货币", "calcChalk · 每杀实时 +1\n连杀加成 ≤ +25%", "#eb6834"),
    "shop":   (425, 1050, 270, 90, "强化商店", "META_DEF ×8 · B 键\n属性跨局生效", "#eb6834"),
    "ach":    (725, 1050, 270, 90, "成就", "ACH_DEF ×10 · C 键\n解锁 toast · k/n 进度条", "#eb6834"),
    "codex":  (1025, 1050, 270, 90, "收集图鉴", "CODEX ×36 · T 键\n首杀点亮 · 里程碑", "#eb6834"),
    "p5":     (120, 1262, 390, 62, "p5.js 2.3.2 渲染", "canvas · letterbox 1280×720 · LOWFX", "#1baf7a"),
    "audio":  (540, 1262, 350, 62, "WebAudio 合成", "音效 sfx · 三套 BGM · 分档音量", "#1baf7a"),
    "store":  (920, 1262, 370, 62, "存档 STORE", "svsn_v2 · 10s 自动存档 · 导入/导出", "#1baf7a"),
    "src":    (1430, 146, 240, 72, "主仓库 js/", "字狂潮v2-全局货币", "#8a8984"),
    "base":   (1430, 272, 240, 72, "porting-baseline", "移植基线 · 同步快照", "#8a8984"),
    "bundle": (1430, 398, 240, 72, "build-bundle.py", "单文件 bundle.js", "#8a8984"),
    "wxmg":   (1430, 524, 240, 72, "微信小游戏", "minigame-1 · 开发者工具", "#8a8984"),
    "gh":     (1430, 650, 240, 72, "GitHub 仓库", "main=v1 冻结 · v2=续作", "#8a8984"),
}

SCENE_BOX = (90, 290, 1210, 170)
SCENE_CHIPS = [
    (120, 344, 150, "title"), (300, 344, 150, "select"), (480, 344, 150, "play"),
    (660, 344, 130, "over"), (820, 344, 130, "clear"), (980, 344, 150, "allclear"),
    (120, 398, 150, "shop 强化"), (300, 398, 150, "ach 成就"), (480, 398, 150, "codex 图鉴"),
]

# 核心框更新顺序徽标（updatePlay 调用序）
BADGES = {"player": "1", "weapons": "2", "enemies": "3", "boss": "4", "items": "5", "upgrades": "6"}

LEGEND = (1380, 830)

# ---------- 声明层：样式 ----------
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, NEUTRAL_FILL, NEUTRAL_EDGE = "#111111", "#52514e", "#f4f3ef", "#8a8984"
TINT = {"#2a78d6": "#f4f8fd", "#eb6834": "#fff7f0", "#1baf7a": "#f2faf7", "#8a8984": "#f4f3ef"}
STYLE = dict(
    cn="SimHei, 'Microsoft YaHei', sans-serif",
    edge_w=1.8, band_w=1.8, box_w=2.0, accent_w=4,
    title=34, sub=16.5, box_main=22, box_sub=15, chip_title=20,
    edge="#52514e", marker=10.5,
)

# 框内文字纵向节奏：h → (主标基线偏移, 子标首行偏移, 行距)
V_RHYTHM = {140: (34, 64, 21), 90: (30, 58, 21), 72: (27, 51, 21), 64: (26, 49, 21), 62: (25, 47, 21)}

def est_w(text, size):
    w = 0.0
    for chb in text:
        w += size if ord(chb) > 0x2E7F else size * 0.56
    return w

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------- 生成层 ----------
def poly(e):
    pts = " ".join(f"{x:.0f},{y:.0f}" for x, y in e["pts"])
    dash = ' stroke-dasharray="7,5"' if e["dash"] else ""
    return (f'  <polyline points="{pts}" fill="none" stroke="{e["color"]}" '
            f'stroke-width="{STYLE["edge_w"]}"{dash} marker-end="url(#ah-{e["color"][1:]})"/>')

def edge_label(e):
    if not e["label"]:
        return ""
    return (f'  <text x="{e["lx"]}" y="{e["ly"]}" font-family="{STYLE["cn"]}" font-size="14.5" '
            f'fill="{MUTED}" text-anchor="{e["anchor"]}" stroke="#ffffff" stroke-width="4.5" '
            f'paint-order="stroke" stroke-linejoin="round">{esc(e["label"])}</text>')

def group(gid):
    x, y, w, h, chip, tag, col = GROUPS[gid]
    tw = est_w(chip, STYLE["chip_title"]) + 26
    out = [f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{col}" fill-opacity="0.05" '
           f'stroke="{col}" stroke-width="{STYLE["band_w"]}" stroke-dasharray="9,6"/>']
    # 骑缝标题牌：白底 + 语义色描边 + 色字
    out.append(f'  <rect x="{x+16}" y="{y-16}" width="{tw:.0f}" height="32" rx="8" fill="#ffffff" '
               f'stroke="{col}" stroke-width="1.6"/>')
    out.append(f'  <text x="{x+16+tw/2:.0f}" y="{y+5}" text-anchor="middle" font-family="{STYLE["cn"]}" '
               f'font-size="{STYLE["chip_title"]}" font-weight="bold" fill="{col}">{esc(chip)}</text>')
    if tag:
        out.append(f'  <text x="{x+w-16}" y="{y+26}" text-anchor="end" font-family="{STYLE["cn"]}" '
                   f'font-size="14" fill="{MUTED}">{esc(tag)}</text>')
    return "\n".join(out)

def box(bid):
    x, y, w, h, main, sub, col = BOXES[bid]
    edge_col = NEUTRAL_EDGE if col == "#8a8984" else col
    fill = TINT[col]
    out = [f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" '
           f'stroke="{edge_col}" stroke-width="{STYLE["box_w"]}"/>']
    # 左侧语义色条
    out.append(f'  <rect x="{x+1.4}" y="{y+3}" width="{STYLE["accent_w"]}" height="{h-6}" rx="2" fill="{col}"/>')
    my, sy, lh = V_RHYTHM[h]
    out.append(f'  <text x="{x+w/2}" y="{y+my}" text-anchor="middle" font-family="{STYLE["cn"]}" '
               f'font-size="{STYLE["box_main"]}" font-weight="bold" fill="{INK}">{esc(main)}</text>')
    for k, line_ in enumerate(sub.split("\n")):
        out.append(f'  <text x="{x+w/2}" y="{y+sy+k*lh}" text-anchor="middle" font-family="{STYLE["cn"]}" '
                   f'font-size="{STYLE["box_sub"]}" fill="{MUTED}">{esc(line_)}</text>')
    if bid in BADGES:
        out.append(f'  <circle cx="{x+w-16}" cy="{y+16}" r="11" fill="#ffffff" stroke="{col}" stroke-width="1.4"/>')
        out.append(f'  <text x="{x+w-16}" y="{y+16}" text-anchor="middle" dominant-baseline="central" '
                   f'font-family="{STYLE["cn"]}" font-size="13" font-weight="bold" fill="{col}">{BADGES[bid]}</text>')
    return "\n".join(out)

def scene_machine():
    x, y, w, h = SCENE_BOX
    out = [f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
           f'fill="#ffffff" stroke="{INK}" stroke-width="2.2"/>']
    out.append(f'  <text x="{x+18}" y="{y+34}" font-family="{STYLE["cn"]}" font-size="{STYLE["box_main"]}" '
               f'font-weight="bold" fill="{INK}">场景状态机 SCENE</text>')
    out.append(f'  <text x="{x+w-18}" y="{y+34}" text-anchor="end" font-family="{STYLE["cn"]}" '
               f'font-size="{STYLE["box_sub"]}" fill="{MUTED}">全局 let · 每帧 switch 分发 upd/draw</text>')
    for cx, cy, cwid, txt in SCENE_CHIPS:
        out.append(f'  <rect x="{cx}" y="{cy}" width="{cwid}" height="40" rx="8" '
                   f'fill="#e9eff8" stroke="#3d4c6f" stroke-width="1.4"/>')
        out.append(f'  <text x="{cx+cwid/2}" y="{cy+20}" text-anchor="middle" font-family="{STYLE["cn"]}" '
                   f'font-size="16" font-weight="bold" fill="{INK}">{esc(txt)}</text>')
    # 状态流转小箭头（title→select→play），其余并列
    for gx in (285, 465):
        out.append(f'  <text x="{gx}" y="364" text-anchor="middle" font-family="{STYLE["cn"]}" '
                   f'font-size="16" font-weight="bold" fill="{MUTED}">→</text>')
    for gx in (645, 805, 965):
        out.append(f'  <text x="{gx}" y="364" text-anchor="middle" font-family="{STYLE["cn"]}" '
                   f'font-size="16" fill="{MUTED}">·</text>')
    out.append(f'  <text x="642" y="418" text-anchor="start" font-family="{STYLE["cn"]}" '
               f'font-size="13" fill="{MUTED}">← 由 select 进入</text>')
    return "\n".join(out)

def legend_block():
    x, y = LEGEND
    rows = [
        (BLUE, "对局核心（每帧 update + draw）"),
        (ORANGE, "局外成长（跨局持久，结算入账）"),
        (AQUA, "平台层（渲染 / 音频 / 存档）"),
        (None, "实线 = 调用/数据流 · 虚线框 = 分组"),
    ]
    out = [f'  <text x="{x}" y="{y}" font-family="{STYLE["cn"]}" font-size="17" '
           f'font-weight="bold" fill="{INK}">图例</text>']
    for k, (col, txt) in enumerate(rows):
        yy = y + 32 + k * 27
        if col:
            out.append(f'  <rect x="{x}" y="{yy-12}" width="24" height="15" rx="3" fill="{col}" '
                       f'fill-opacity="0.15" stroke="{col}" stroke-width="1.4" stroke-dasharray="4,3"/>')
        out.append(f'  <text x="{x+34}" y="{yy}" font-family="{STYLE["cn"]}" font-size="15" '
                   f'fill="{MUTED}">{esc(txt)}</text>')
    out.append(f'  <text x="{x}" y="{y+32+4*27+20}" font-family="{STYLE["cn"]}" font-size="13.5" '
               f'fill="{MUTED}">字狂潮 v2.3 · 2026-10</text>')
    return "\n".join(out)

def title_block():
    return (
        f'  <text x="{W-40}" y="52" text-anchor="end" font-family="{STYLE["cn"]}" '
        f'font-size="{STYLE["title"]}" font-weight="bold" fill="{INK}">字狂潮 v2.3 · 游戏架构</text>\n'
        f'  <text x="{W-40}" y="80" text-anchor="end" font-family="{STYLE["cn"]}" '
        f'font-size="{STYLE["sub"]}" fill="{MUTED}">p5.js 割草木鸽 · 浏览器 + 微信小游戏双端</text>'
    )

def markers():
    out = ['  <defs>']
    for name, col in [("ah-" + c[1:], c) for c in (STYLE["edge"], ORANGE)]:
        m = STYLE["marker"]
        out.append(f'    <marker id="{name}" markerUnits="userSpaceOnUse" markerWidth="{m+3}" '
                   f'markerHeight="{m}" refX="{m+1.5}" refY="{m/2}" orient="auto">'
                   f'<path d="M0,0 L{m},{m/2} L0,{m} z" fill="{col}"/></marker>')
    out.append('  </defs>')
    return "\n".join(out)

def build():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        markers(),
        f'  <rect width="{W}" height="{H}" fill="#ffffff"/>',
        title_block(),
    ]
    for gid in ("input", "core", "meta", "plat", "build"):
        parts.append(group(gid))
    parts.append(scene_machine())
    for bid in BOXES:
        parts.append(box(bid))
    parts.append('  <g fill="none">')
    for e in EDGES:
        parts.append(poly(e))
    parts.append('  </g>')
    for e in EDGES:
        parts.append(edge_label(e))
    parts.append(legend_block())
    parts.append("</svg>")
    return "\n".join(parts) + "\n"

# ---------- 声明层：拓扑 ----------
def E(pts, label=None, lx=None, ly=None, color=None, dash=False, anchor="start"):
    return dict(pts=pts, label=label, lx=lx, ly=ly, color=color or "#52514e",
                dash=dash, anchor=anchor)

EDGES = [
    # 输入 → 场景机
    E([(300, 210), (300, 290)], "kp() · 快捷键", 312, 254),
    E([(700, 210), (700, 290)], "uiHit 点击", 712, 254),
    E([(1090, 210), (1090, 290)], "wx 触摸事件", 1102, 254),
    # 鼠标 → player：经输入带上方沿左缘绕行
    E([(700, 146), (700, 60), (50, 60), (50, 660), (120, 660)]),
    # 场景机 → 对局
    E([(695, 460), (695, 520)], "startPlay(lv) · Esc/按钮返回", 707, 494),
    # 对局内部
    E([(295, 770), (295, 752), (610, 752), (610, 730)], "命中 hurtEnemy −1", 298, 744),
    E([(525, 660), (470, 660)], "受击 hurtPlayer −1♥ · 碰撞/弹幕", 497, 578, anchor="middle"),
    E([(875, 660), (930, 660)], "t≥300s spawnBoss", 902, 578, anchor="middle"),
    E([(700, 730), (700, 770)], "击杀掉落", 712, 758),
    E([(875, 840), (930, 840)], "粉笔屑 = 经验 addXp", 902, 758, anchor="middle"),
    # 对局 → 局外
    E([(340, 950), (340, 1030), (300, 1030), (300, 1050)], "击杀实时 +1 · 结算", 352, 992),
    E([(1000, 950), (1000, 1040), (1139, 1040), (1139, 1050)], "击杀收录 · 达成解锁", 1012, 995),
    # 局外 → 对局（反馈）
    E([(560, 1050), (560, 950)], "META 属性加成 · 下一局", 578, 982, ORANGE),
    # 局外 → 存档（持久化）
    E([(1105, 1140), (1105, 1262)], "saveStore · 10s 自动 + 结算", 1117, 1205, dash=True),
    # build 链
    E([(1550, 218), (1550, 272)]),
    E([(1550, 344), (1550, 398)]),
    E([(1550, 470), (1550, 524)], "require bundle", 1562, 502),
    E([(1550, 596), (1550, 650)]),
]

if __name__ == "__main__":
    out = Path(__file__).with_name("arch-v2.svg")
    out.write_text(build(), encoding="utf-8")
    print("arch-v2.svg written,", out)
