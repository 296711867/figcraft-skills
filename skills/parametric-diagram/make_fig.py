# -*- coding: utf-8 -*-
"""图：三层全连接网络示意（输入层 x_d --W1--> 隐层 h_N --W2--> 输出层 f_C）。

图=声明：几何/拓扑/样式三层分离。
  几何 COLS/ROWS 常量  → 拓扑 mesh() 全连接循环  → 样式 STYLE 常量。
产物：fig-mlp.svg（1× = 参考图坐标系 755×709；PNG 由内联页 2× 截屏得到）。
改尺寸/加节点：只动 COLS/ROWS/STYLE，重新运行本脚本即可。
"""
import math
from pathlib import Path

# ---------- 声明层：几何（探测自 reference.png） ----------
W, H = 755, 709
COLS = {
    "x": dict(cx=105.5, r=52, ys=[199, 319, 484]),          # 输入 x1 x2 xd
    "h": dict(cx=414.0, r=50, ys=[105.5, 223.5, 355.5, 559.5]),  # 隐层 h1 h2 h3 hN
    "f": dict(cx=650.0, r=50, ys=[165, 300, 532]),          # 输出 f1 f2 fC
}
BAND = dict(x=332, y=44, w=154, h=589)                       # 隐层蓝带
DOTS = {  # 竖排省略点（3 个小方块）：列 → (x, 首块中心y, 间距)
    "x": (102, 382.5, 18), "h": (419.5, 431, 18), "f": (657.5, 396, 18),
}
LABELS = {  # 文字标注：(x, y, 文本, 类别)
    "W1": (250, 96, "W1", "ui"), "W2": (556, 92, "W2", "ui"),
    "输入层": (107, 586, "输入层", "cn"), "隐层": (421, 678, "隐层", "cn"),
    "输出层": (663, 662, "输出层", "cn"),
}
NODE_TEXT = {  # 节点内标签：(列, 行序) → (主字母, 下标, 下标是否斜体)
    ("x", 0): ("x", "1", False), ("x", 1): ("x", "2", False), ("x", 2): ("x", "d", True),
    ("h", 0): ("h", "1", False), ("h", 1): ("h", "2", False), ("h", 2): ("h", "3", False),
    ("h", 3): ("h", "N", True),
    ("f", 0): ("f", "1", False), ("f", 1): ("f", "2", False), ("f", 2): ("f", "C", True),
}

# ---------- 声明层：样式 ----------
STYLE = dict(
    ink="#111111", line_w=1.5, ring_w=2.4,
    band_fill="#BDCCE5", band_stroke="#3D4C6F", band_w=2.2,
    math_font="Times New Roman, SimSun, serif", cn_font="SimHei, 'Microsoft YaHei', sans-serif",
    node_main=36, node_sub=23, w_label=27, cn_label=31,
    dot=8, marker=9.5,
)

# ---------- 生成层 ----------

def edge_point(src, dst, r_src, gap=0.0):
    """源圆缘出发、距目标圆缘 gap 处的截断点。"""
    dx, dy = dst[0] - src[0], dst[1] - src[1]
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    return (src[0] + ux * r_src, src[1] + uy * r_src,
            dst[0] - ux * (r_src and COLS_DEST_R[dst_col] + gap), dst[1] - uy * (COLS_DEST_R[dst_col] + gap))

COLS_DEST_R = {c: v["r"] for c, v in COLS.items()}

def line(p, q, extra=""):
    return f'    <line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" marker-end="url(#ah)" {extra}/>'

def mesh():
    """拓扑：全连接 x→h（W1）、h→f（W2），箭头落在目标圆缘。"""
    out = ['  <g stroke="%s" stroke-width="%s" fill="none">' % (STYLE["ink"], STYLE["line_w"])]
    def edges(col_a, col_b):
        ra, rb = COLS[col_a]["r"], COLS[col_b]["r"]
        for ya in COLS[col_a]["ys"]:
            for yb in COLS[col_b]["ys"]:
                ax_, ay = COLS[col_a]["cx"], ya
                bx_, by = COLS[col_b]["cx"], yb
                dx, dy = bx_ - ax_, by - ay
                d = math.hypot(dx, dy)
                ux, uy = dx / d, dy / d
                p = (ax_ + ux * ra, ay + uy * ra)
                q = (bx_ - (rb + 2.0), by)   # 参考图画法：入线全部汇聚到目标圆左极点，箭头堆叠成簇
                out.append(line(p, q))
    edges("x", "h")
    edges("h", "f")
    out.append("  </g>")
    return "\n".join(out)

def band():
    b = BAND
    return (f'  <rect x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" '
            f'fill="{STYLE["band_fill"]}" stroke="{STYLE["band_stroke"]}" stroke-width="{STYLE["band_w"]}"/>')

def circle(col, i):
    c = COLS[col]
    return (f'    <circle cx="{c["cx"]}" cy="{c["ys"][i]}" r="{c["r"]}" '
            f'fill="#ffffff" stroke="{STYLE["ink"]}" stroke-width="{STYLE["ring_w"]}"/>')

def node_text(col, i):
    c = COLS[col]
    main, sub, sub_it = NODE_TEXT[(col, i)]
    sub_style = "" if sub_it else ' font-style="normal"'   # 数字下标直立，字母下标斜体
    return (f'    <text x="{c["cx"]}" y="{c["ys"][i]}" text-anchor="middle" dominant-baseline="central" '
            f'font-family="{STYLE["math_font"]}" font-style="italic" font-size="{STYLE["node_main"]}" '
            f'fill="{STYLE["ink"]}">{main}<tspan dy="{STYLE["node_sub"]*0.35:.1f}" '
            f'font-size="{STYLE["node_sub"]}"{sub_style}>{sub}</tspan></text>')

def dots(col):
    x, y0, gap = DOTS[col]
    s = STYLE["dot"]
    return "\n".join(
        f'  <rect x="{x - s/2:.1f}" y="{y0 + k*gap - s/2:.1f}" width="{s}" height="{s}" fill="{STYLE["ink"]}"/>'
        for k in range(3))

def labels():
    out = []
    for text, (x, y, val, kind) in LABELS.items():
        if kind == "math":
            out.append(f'  <text x="{x}" y="{y}" text-anchor="middle" font-family="{STYLE["math_font"]}" '
                       f'font-style="italic" font-size="{STYLE["w_label"]}" fill="{STYLE["ink"]}">{val}</text>')
        elif kind == "ui":   # W1/W2：直立黑体
            out.append(f'  <text x="{x}" y="{y}" text-anchor="middle" font-family="{STYLE["cn_font"]}" '
                       f'font-size="{STYLE["w_label"]}" fill="{STYLE["ink"]}">{val}</text>')
        else:
            out.append(f'  <text x="{x}" y="{y}" text-anchor="middle" font-family="{STYLE["cn_font"]}" '
                       f'font-size="{STYLE["cn_label"]}" fill="{STYLE["ink"]}">{val}</text>')
    return "\n".join(out)

def build():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '  <defs>',
        f'    <marker id="ah" markerUnits="userSpaceOnUse" markerWidth="{STYLE["marker"]+3}" '
        f'markerHeight="{STYLE["marker"]}" refX="{STYLE["marker"]+1.5}" refY="{STYLE["marker"]/2}" orient="auto">',
        f'      <path d="M0,0 L{STYLE["marker"]},{STYLE["marker"]/2} L0,{STYLE["marker"]} z" fill="{STYLE["ink"]}"/>',
        '    </marker>',
        '  </defs>',
        f'  <rect width="{W}" height="{H}" fill="#ffffff"/>',
        band(),
        mesh(),
    ]
    for col in ("x", "h", "f"):
        n = len(COLS[col]["ys"])
        parts += [circle(col, i) for i in range(n)]
        parts += [node_text(col, i) for i in range(n)]
        parts.append(dots(col))
    parts.append(labels())
    parts.append("</svg>")
    return "\n".join(parts) + "\n"

if __name__ == "__main__":
    svg = build()
    Path(__file__).with_name("fig-mlp.svg").write_text(svg, encoding="utf-8")
    print("fig-mlp.svg written,", len(svg), "bytes")
