# -*- coding: utf-8 -*-
"""probe_geometry.py — 从参考位图程序化提取结构图的几何与配色（复刻第一步）。

用法：把本文件作为模板，按需调用下面的函数；典型顺序：
    1) show()/采样点取色         → 确认填充/边框/文字/虚线颜色
    2) find_fill_boxes(color)    → 按填充色连通域找盒子边界
    3) ring_scan / hscan         → 圆形节点的圆心与直径
    4) text_rows(x0,y0,x1,y1)    → 文字行的 y 区间（定基线）
    5) darkruns_row/col          → 连线端点、箭头位置、虚线区间
依赖：numpy、Pillow；连通域需要 scipy（可选，无则用 find_fill_boxes_basic）。
"""
from __future__ import annotations

import numpy as np
from PIL import Image


def load(path: str) -> np.ndarray:
    """RGB int 数组，H×W×3。"""
    return np.array(Image.open(path).convert("RGB")).astype(int)


def px(a: np.ndarray, x: int, y: int, label: str = "") -> None:
    print(f"{label or ''}({x},{y}) = {tuple(a[y, x])}")


def color_mask(a: np.ndarray, color: tuple, tol: int = 30):
    return np.abs(a - np.array(color)).sum(axis=2) < tol


def clusters(idx: np.ndarray, gap: int = 8):
    """一维索引聚类 → [(start, end), ...]，找连续区段。"""
    idx = np.unique(idx)
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v - p > gap:
            out.append((int(s), int(p)))
            s = v
        p = v
    out.append((int(s), int(p)))
    return out


def find_fill_boxes(a: np.ndarray, color: tuple, tol: int = 30, min_area: int = 800):
    """按填充色做连通域，返回盒子 [x0,y0,x1,y1,area]（需 scipy）。"""
    from scipy import ndimage
    lab, n = ndimage.label(color_mask(a, color, tol))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(xs) >= min_area:
            out.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(xs)))
    return sorted(out, key=lambda b: (b[1], b[0]))


def darkruns_row(a: np.ndarray, y: int, x0: int, x1: int, thr: int = 380) -> list:
    """某行上暗像素的 x 区间（连线端点/边框位置）。"""
    return clusters(np.where(a[y, x0:x1].sum(axis=1) < thr)[0] + x0, gap=3)


def darkruns_col(a: np.ndarray, x: int, y0: int, y1: int, thr: int = 380) -> list:
    """某列上暗像素的 y 区间（盒子上下边、圆环顶底、文字行）。"""
    return clusters(np.where(a[y0:y1, x].sum(axis=1) < thr)[0] + y0, gap=3)


def text_rows(a: np.ndarray, x0: int, y0: int, x1: int, y1: int, thr: int = 430) -> list:
    """区域内文字行的 y 区间（基线 ≈ 区间底 -3px @14px 字号）。"""
    sub = a[y0:y1, x0:x1].sum(axis=2)
    rows = np.where((sub < thr).sum(axis=1) > 2)[0]
    return clusters(rows + y0, gap=5)


def ring_scan(a: np.ndarray, col: int, y0: int, y1: int, thr: int = 260):
    """圆环竖直扫描：过圆心的列上暗像素区段 → (顶, 底) = 圆环上下缘。"""
    return darkruns_col(a, col, y0, y1, thr)


def darkest(a: np.ndarray, x0: int, y0: int, x1: int, y1: int) -> tuple:
    """区域内最深像素的颜色（文字/边框真色，避开抗锯齿取中值更稳）。"""
    r = a[y0:y1, x0:x1].reshape(-1, 3)
    return tuple(r[r.sum(axis=1).argmin()])


def mean_color(a: np.ndarray, x0: int, y0: int, x1: int, y1: int, mask=None) -> tuple:
    r = a[y0:y1, x0:x1].reshape(-1, 3)
    if mask is not None:
        r = mask[y0:y1, x0:x1].reshape(-1, 3)
    return tuple(r.mean(axis=0).round().astype(int))


def hexc(rgb: tuple) -> str:
    return "#%02X%02X%02X" % rgb


if __name__ == "__main__":
    import sys
    a = load(sys.argv[1] if len(sys.argv) > 1 else "reference.png")
    print("size:", a.shape[1], "x", a.shape[0])
    print("示例：px(a, 100, 200, '采样'), find_fill_boxes(a, (228,238,248)), text_rows(a, 80,25,940,60) ...")
