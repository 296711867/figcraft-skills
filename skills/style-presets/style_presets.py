# -*- coding: utf-8 -*-
"""
论文配图技能库 · 样式预设（06-style-presets）

三种风格，科研风（academic）为默认：
  academic —— 科研风（默认）：白底、克制用色、无阴影无渐变、细线、Times+黑体/宋体（METHOD.md 原生风格）
  web      —— web 风：深色页头带、白色圆角卡片、柔和投影、胶囊标签、YaHei
  tech     —— 科技风：深空底色、青色霓虹强调、辉光、点阵底纹、等宽字标签

合同（图 = 声明 · 四层分离）：几何与内容由图脚本声明，本模块只供"样式令牌"。
换风格 = 换一个令牌字典，图脚本零改动；新增风格 = 加一个 dict。
用法：
    from style_presets import get_style
    S = get_style("tech")          # 缺省返回科研风
"""
from copy import deepcopy

DEFAULT = "academic"

REQUIRED_KEYS = [
    # 画布与页头
    "page_bg", "deco", "head", "head_bg", "head_h", "head_title", "head_sub",
    "head_rule", "head_bar", "date_style", "date_edge",
    # 基础文字与线条
    "ink", "muted", "faint", "line", "text_mid",
    # 卡片体系
    "card", "card_edge", "card_r", "fx",
    "badge_bg", "badge_fg",
    # 强调语义（本图的 GPU；通用图里即"主强调"）
    "gpu_fill", "gpu_edge", "gpu_deep", "gpu_sub", "gpu_perf", "gpu_soft",
    "gpu_chip_bg", "gpu_chip_fg",
    # 中性语义（CPU / 次要）
    "cpu_fill", "cpu_edge", "cpu_chip_bg", "cpu_chip_fg",
    # 虚线离线带 / 环境小签 / 表格 / 备注
    "off_fill", "off_dash", "env_fill", "env_fg", "table_head",
    "arrow", "note_bg", "note_line",
    # 字体与圆角
    "font_title", "font_body", "font_mono", "chip_r",
]

PRESETS = {
    # ---------------- 科研风（默认，METHOD.md 原生） ----------------
    "academic": {
        "page_bg": "#ffffff", "deco": "none",
        "head": "plain", "head_bg": None, "head_h": 96,
        "head_title": "#111111", "head_sub": "#52514e",
        "head_rule": True, "head_bar": None,
        "date_style": "text", "date_edge": "#8a8984",
        "ink": "#111111", "muted": "#52514e", "faint": "#8a8984",
        "line": "#e4e3df", "text_mid": "#3d3c39",
        "card": "#ffffff", "card_edge": "#d8d6d0", "card_r": 5, "fx": "none",
        "badge_bg": "#111111", "badge_fg": "#ffffff",
        "gpu_fill": "#fdf1ec", "gpu_edge": "#eb6834", "gpu_deep": "#8c3d1f",
        "gpu_sub": "#8c3d1f", "gpu_perf": "#a05a2d", "gpu_soft": "#fae3d9",
        "gpu_chip_bg": "#eb6834", "gpu_chip_fg": "#ffffff",
        "cpu_fill": "#f4f3ef", "cpu_edge": "#b8b6b0",
        "cpu_chip_bg": "#52514e", "cpu_chip_fg": "#ffffff",
        "off_fill": "#fdf6f2", "off_dash": "4 3",
        "env_fill": "#fae3d9", "env_fg": "#8c3d1f",
        "table_head": "#f4f3ef",
        "arrow": "#8a8984", "note_bg": "#f9f8f5", "note_line": "#e4e3df",
        "font_title": "Times New Roman, SimHei",
        "font_body": "Times New Roman, SimSun",
        "font_mono": "Consolas, monospace",
        "chip_r": 3,
    },
    # ---------------- web 风 ----------------
    "web": {
        "page_bg": "#f4f6fa", "deco": "none",
        "head": "band", "head_bg": "#0f172a", "head_h": 96,
        "head_title": "#ffffff", "head_sub": "#c7d2e2",
        "head_rule": False, "head_bar": None,
        "date_style": "pill", "date_edge": "#475569",
        "ink": "#0f172a", "muted": "#64748b", "faint": "#94a3b8",
        "line": "#e2e8f0", "text_mid": "#334155",
        "card": "#ffffff", "card_edge": "#e2e8f0", "card_r": 14, "fx": "soft",
        "badge_bg": "#0f172a", "badge_fg": "#ffffff",
        "gpu_fill": "#fff7ed", "gpu_edge": "#f97316", "gpu_deep": "#9a3412",
        "gpu_sub": "#9a3412", "gpu_perf": "#b45309", "gpu_soft": "#ffedd5",
        "gpu_chip_bg": "#f97316", "gpu_chip_fg": "#ffffff",
        "cpu_fill": "#f8fafc", "cpu_edge": "#cbd5e1",
        "cpu_chip_bg": "#64748b", "cpu_chip_fg": "#ffffff",
        "off_fill": "#fffbeb", "off_dash": "5 3",
        "env_fill": "#ffedd5", "env_fg": "#9a3412",
        "table_head": "#eef2f7",
        "arrow": "#94a3b8", "note_bg": "#f8fafc", "note_line": "#e2e8f0",
        "font_title": "Microsoft YaHei, PingFang SC, Segoe UI, sans-serif",
        "font_body": "Microsoft YaHei, PingFang SC, Segoe UI, sans-serif",
        "font_mono": "Consolas, monospace",
        "chip_r": 7.5,
    },
    # ---------------- 科技风 ----------------
    "tech": {
        "page_bg": "#0b1220", "deco": "dots",
        "head": "plain", "head_bg": None, "head_h": 96,
        "head_title": "#f2f7ff", "head_sub": "#8fa5c5",
        "head_rule": False, "head_bar": "#22d3ee",
        "date_style": "pill", "date_edge": "#2b4258",
        "ink": "#e8f0fb", "muted": "#9fb2cc", "faint": "#5d7395",
        "line": "#6288b8", "text_mid": "#b9c9e2",
        "card": "#111a2e", "card_edge": "#233250", "card_r": 12, "fx": "glow",
        "badge_bg": "#16283f", "badge_fg": "#7dd3fc",
        "gpu_fill": "#0e2a3a", "gpu_edge": "#22d3ee", "gpu_deep": "#a5f3fc",
        "gpu_sub": "#7dd3fc", "gpu_perf": "#67e8f9", "gpu_soft": "#0c3242",
        "gpu_chip_bg": "#22d3ee", "gpu_chip_fg": "#06202b",
        "cpu_fill": "#182338", "cpu_edge": "#334766",
        "cpu_chip_bg": "#3b4c68", "cpu_chip_fg": "#dbe7f7",
        "off_fill": "#0d2434", "off_dash": "5 3",
        "env_fill": "#0c3242", "env_fg": "#7dd3fc",
        "table_head": "#16223a",
        "arrow": "#4a607f", "note_bg": "#0f1930", "note_line": "#6288b8",
        "font_title": "Segoe UI, Microsoft YaHei, sans-serif",
        "font_body": "Segoe UI, Microsoft YaHei, sans-serif",
        "font_mono": "Consolas, monospace",
        "chip_r": 7.5,
    },
}


def names():
    """全部风格名（默认风格排第一）"""
    return [DEFAULT] + [k for k in PRESETS if k != DEFAULT]


def get_style(name: str | None = None) -> dict:
    """取风格令牌字典；缺省科研风。返回副本，调用方可安心改写个别令牌。"""
    key = name or DEFAULT
    if key not in PRESETS:
        raise KeyError(f"未知风格 {key!r}，可选：{names()}")
    s = deepcopy(PRESETS[key])
    missing = [k for k in REQUIRED_KEYS if k not in s]
    assert not missing, f"风格 {key} 缺少令牌：{missing}"
    return s


if __name__ == "__main__":
    for n in names():
        s = get_style(n)
        print(f"{n:9s} head={s['head']:5s} fx={s['fx']:4s} accent={s['gpu_edge']}  font={s['font_title'][:28]}")
