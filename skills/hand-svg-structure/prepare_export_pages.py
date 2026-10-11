# -*- coding: utf-8 -*-
"""prepare_export_pages.py — SVG → 浏览器截屏导出的内联 HTML 页生成器。

为什么存在：SVG 导出 PNG 唯一可靠通道 = 把 SVG **内联**进 HTML，浏览器 viewport
设成精确内容尺寸后普通截屏。<img src="*.svg"> 会渲染跑偏；对独立 SVG 文档或
超一屏页面用 fullPage 截屏会触发"平铺 bug"（碎片重复铺满，尺寸对内容坏）。

用法：
    python prepare_export_pages.py fig.svg            # 1× + 2× 两页
    python prepare_export_pages.py fig.svg --halves   # 再加 2× 上下半页（高>2160 时用）

随后（Browser Use / MCP node_repl）：
    tab.setViewportSize({width: W, height: H});
    tab.goto("file 页面 URL");
    png = await tab.screenshot();                      // 普通，不 fullPage
    fs.writeFileSync("out.png", Buffer.from(png));
截屏偶发失败（activity capture failed for guest）→ 等 1 秒重试即可。
高 >2160 的图：分别截 top/bot 两页，再用 PIL 纵向拼接：
    canvas.paste(top, (0,0)); canvas.paste(bot, (0, top.height))
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

TPL = ("<!doctype html><html><head><meta charset='utf-8'>"
       "<style>html,body{{margin:0;padding:0;background:#fff;overflow:hidden}}</style></head>"
       "<body style='width:{w}px;height:{h}px;overflow:hidden'>{body}</body></html>")


def inline(svg_path: Path):
    """返回 (svg主体, 原始w字符串, 原始h字符串, w浮点, h浮点)。宽高可能是浮点。"""
    svg = svg_path.read_text(encoding="utf-8")
    body = svg.split("?>", 1)[1] if svg.startswith("<?xml") else svg
    m = re.search(r'<svg[^>]*?width="([\d.]+)" height="([\d.]+)"', body)
    if not m:
        raise SystemExit("SVG 根元素未找到 width/height")
    return body, m.group(1), m.group(2), float(m.group(1)), float(m.group(2))


def write(page: Path, body: str, w: int, h: int, shift: str = "") -> None:
    inner = f"<div style='{shift}'>{body}</div>" if shift else body
    page.write_text(TPL.format(w=w, h=h, body=inner), encoding="utf-8")
    print("page:", page.name, f"{w}x{h}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("svg", type=Path)
    ap.add_argument("--halves", action="store_true", help="额外生成 2× 上下半页（内容高 >2160 时用）")
    ap.add_argument("--outdir", type=Path, default=None)
    args = ap.parse_args()
    outdir = args.outdir or args.svg.parent
    outdir.mkdir(parents=True, exist_ok=True)
    stem = args.svg.stem

    body, ws, hs, w, h = inline(args.svg)
    write(outdir / f"{stem}@1x.html", body, round(w), round(h))

    w2, h2 = round(w * 2), round(h * 2)
    old = f'width="{ws}" height="{hs}"'          # 用原始字符串替换，浮点不会被 :g 破坏
    new = f'width="{w2}" height="{h2}"'
    if old not in body:
        raise SystemExit(f"尺寸替换失败：{old} 不在 SVG 中")
    body2 = body.replace(old, new, 1)
    write(outdir / f"{stem}@2x.html", body2, w2, h2)

    if args.halves:
        half = h2 // 2
        write(outdir / f"{stem}@2x_top.html", body2, w2, half)
        write(outdir / f"{stem}@2x_bot.html", body2, w2, half, shift=f"transform:translateY(-{half}px)")
        print(f"拼接提示：top+bot 两张 PNG 用 PIL 纵向 paste 即得 {w2}x{h2}")


if __name__ == "__main__":
    main()
