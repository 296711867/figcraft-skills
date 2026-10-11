# -*- coding: utf-8 -*-
"""check_tiling.py — 浏览器截屏导出的 PNG 平铺自检。

背景：对超一屏页面用 fullPage 截屏、或对超大视口截屏，浏览器会把画面裁成
视口大小的碎片重复铺满整张 PNG——尺寸完全正确但内容是坏的，且只查尺寸发现不了。

原理：真被 2×2 平铺的图，上半与下半、左半与右半几乎逐像素相同。
用法：python check_tiling.py a.png b.png ...
      vdiff/hdiff 均 < 6 判为疑似平铺（对称图会误报，结合肉眼）。
"""
from __future__ import annotations

import sys

import numpy as np
from PIL import Image


def score(path: str) -> tuple[float, float]:
    a = np.asarray(Image.open(path).convert("L"), dtype=np.int16)
    h, w = a.shape
    v = np.abs(a[: h // 2, :] - a[h // 2: h // 2 * 2, :]).mean()
    hz = np.abs(a[:, : w // 2] - a[:, w // 2: w // 2 * 2]).mean()
    return float(v), float(hz)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        v, hz = score(p)
        flag = "TILED?" if (v < 6 and hz < 6) else "ok"
        print(f"{p:40s} vdiff={v:6.1f} hdiff={hz:6.1f} {flag}")
