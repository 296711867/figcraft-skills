#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三项目环节流程 × GPU 使用点 —— 多风格版
路线：论文配图技能库 02-parametric-diagram（参数化脚本即源）+ 06-style-presets（样式令牌）
三段声明：GEOM（几何）/ CONTENT（内容）/ 样式一律来自 style_presets（换风格零改代码）。
运行：python -X utf8 make_gpu_flow_fig.py --style all   # academic|web|tech|all，默认 academic
"""
import argparse
import html
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent   # 06-style-presets 根目录（examples 副本相对定位）
sys.path.insert(0, str(LIB))
from style_presets import get_style, names  # noqa: E402

DEST = Path(__file__).parent
ZH = {"academic": "科研风", "web": "web风", "tech": "科技风"}

# ================= GEOM（几何声明，与样式无关） =================
M      = 40            # 对称边距
W      = 1880
HEAD_H = 96
INNER  = W - 2 * M     # 1800

LANE_X, LANE_W, LPAD = M, INNER, 22
CARD_H   = 130         # 环节卡高
GAP_ARR  = 20          # 环节卡间隙（放箭头）
OFF_H    = 46          # 离线带高
NOTE_H   = 30          # 关键数字带高
LANE_GAP = 18
LANE_H   = 66 + CARD_H + 13 + OFF_H + 8 + NOTE_H + 16   # = 309，由下方布局常量推出

SUM_X, SUM_W, SUM_PAD = M, INNER, 24
COL_W  = (SUM_W - 2 * SUM_PAD - 28) // 2   # 结论两列
PT_SLOT = 62
TBL_COL = [210, 320, 232, 400]             # 表格前四列，末列占余下
TBL_HH, TBL_RH = 32, 48
SUM_H  = SUM_PAD + 34 + 3 * PT_SLOT + 10 + TBL_HH + 3 * TBL_RH + 20

FS_TITLE, FS_SUB = 24, 12.5
FS_LANE_T, FS_LANE_D = 19, 12
FS_CARD_T, FS_CARD_S, FS_CARD_P, FS_CHIP, FS_ENV = 13, 10.8, 10.2, 9.5, 9
FS_NOTE, FS_PT_T, FS_PT_D, FS_TBL = 12, 13, 12, 11.3


# ================= CONTENT（内容声明，与样式无关） =================
TITLE   = "三个项目环节流程 × GPU 使用点总览"
SUBTITLE = ("① 02-3D-detect（RGB-D 6D 位姿识别与抓取）　② 08-Intrusion-Detection-System（机械臂区域入侵检测）"
            "　③ 09-State-Inspection（手机排线膜工艺状态巡检）　·　硬件基线：RTX 5050 Laptop 8GB（sm_120 · CUDA 13 走 conda 环境）")
DATE_CHIP = "2026-10-13"

LEGEND = [
    ("gpu",  "GPU 在线推理（每次运行都要）"),
    ("gpuf", "GPU 离线训练/标注（一次性/偶尔）"),
    ("cpu",  "CPU 环节（标定 · 采集 · 几何/规则 · 上报）"),
]
LEGEND_NOTE = "框内小字＝方法 / 框架与实测数字"

LANES = [
    dict(
        no="1", name="02-3D-detect · RGB-D 6D 位姿识别与抓取",
        desc="系列标定 → RGB-D 采集 → 实例分割 → 6D 位姿精配（FoundationPose）→ 变换到机器人基座系 → 准确度验证",
        badge="在线 GPU ×2 · 离线 GPU ×1",
        stages=[
            dict(t=["系列标定"], s=["TCP 四点法 / 手眼标定", "Tag 偏移 · 离线一次性"], cpu=True, p=["手眼 2.64mm · TCP 1.04mm"]),
            dict(t=["RGB-D 图像采集"], s=["Orbbec 336L / D435i", "1280×720@10fps"], cpu=True, p=["pyorbbecsdk2 / pyrealsense2"]),
            dict(t=["实例检测/分割"], s=["YOLO11-seg 检出+掩码", "备选 SAM2"], cpu=False, env="envs/yoloseg", p=["ultralytics + torch cu130"]),
            dict(t=["对象检索"], s=["实例 → CAD 映射", "tag / 尺寸颜色"], cpu=True, p=["numpy / cv2"]),
            dict(t=["位姿初值"], s=["AprilTag PnP /", "盒·mesh PCA 8 假设"], cpu=True, p=["cv2 solvePnP · open3d"]),
            dict(t=["6D 位姿精配"], s=["FoundationPose 迭代精修", "备选 ICP（CPU）透明壳拉偏"], cpu=False, env="envs/foundationpose", p=["显存 ~255MB · nvdiffrast"]),
            dict(t=["变换到机器人基座"], s=["T_base_obj = base_T_cam ×", "T_cam_obj · 多帧择优"], cpu=True, p=["基座系重复性 ±4mm"]),
            dict(t=["准确度验证"], s=["到位容差 + NCC 外观", "BOP 黄金集回归"], cpu=True, p=["端到端 ≤15mm 验收"]),
        ],
        offline_label="离线 GPU",
        offline=[dict(cpu=False, w=520, t="YOLO 训练 / SAM2 辅助标注", p="900 帧 · 60ep 3.7min · sm_120 须 amp=False · FP 权重已就绪")],
        offline_note="一次性 / 偶发，分钟级",
        note="关键数字：在线单实例 74ms≈13.5Hz（双实例 121ms）· GPU 子进程冷启 ~10s · YOLO+FP 常驻共存 8GB 无 OOM · provider ~29ms / refine ~50ms（shm IPC）",
    ),
    dict(
        no="2", name="08-Intrusion-Detection-System · 机械臂区域入侵检测（安全联锁）",
        desc="RGB-D 采集 → YOLO 整臂检测 → ByteTrack 跟踪 → 排除掩码 → 深度背景差区域判定 → 报警逻辑 → 停机联动",
        badge="在线 GPU ×1 · 离线 GPU ×1",
        stages=[
            dict(t=["RGB-D 采集"], s=["Orbbec 336L 彩色+深度", "1280×800@30fps · D2C"], cpu=True, p=["pyorbbecsdk"]),
            dict(t=["整臂检测"], s=["YOLO11n 单类 robot_arm", "imgsz 1280 · conf 0.65"], cpu=False, env="conda yolo", p=["10FPS 节流 · 权重 5.4MB"]),
            dict(t=["多目标跟踪"], s=["ByteTrack 接回遮挡 ID", "buffer ≈6s"], cpu=True, p=["ultralytics 内置"]),
            dict(t=["排除掩码"], s=["检测框铺矩形 + EMA 平滑", "形态学外扩"], cpu=True, p=["OpenCV / numpy"]),
            dict(t=["区域入侵判定"], s=["深度背景差 >8cm", "帧间运动 >4cm · 排除臂掩码"], cpu=True, p=["OpenCV 规则 · 非神经网络"]),
            dict(t=["报警逻辑"], s=["≥1017px 且连续 4 帧命中", "2s 无命中解除"], cpu=True, p=["纯逻辑"]),
            dict(t=["安全联动"], s=["停机文件 + TCP + HTTP", "→ 机械臂控制器"], cpu=True, p=["失败每秒重试"]),
            dict(t=["监视与记录"], s=["Web :8765 实时画面", "报警截图留存 30 张"], cpu=True, p=["http.server"]),
        ],
        offline_label="离线链路",
        offline=[
            dict(cpu=True, w=330, t="数据采集 / 标注 / 增强", p="565 张 ×3 增强副本 · 纯 CPU"),
            dict(cpu=False, w=330, t="YOLO 训练（device=0, amp）", p="yolo11n 起始 · 100ep · imgsz 640"),
        ],
        offline_note="一次性 / 偶发",
        note="关键数字：mAP50 0.995 / R 1.0（28 张混合验证集）· CUDA 冷启 >8s → worker 预热后常驻 · 主程序 orbbec 环境不装 torch",
    ),
    dict(
        no="3", name="09-State-Inspection · 手机排线膜工艺状态巡检",
        desc="图像采集 → 正反面识别（YOLO）→ 落位检查 → 保护膜撕除 → 黑膜捋平 → 结果汇总上报",
        badge="在线 GPU ×1 · 离线 GPU ×1",
        stages=[
            dict(t=["图像采集"], s=["Orbbec RGB-D + 海康 2D×2", "按需取帧"], cpu=True, p=["pyorbbecsdk2 + 海康 MVS"]),
            dict(t=["正反面识别"], s=["YOLO11s front/back 两类", "conf 0.5 · imgsz 640"], cpu=False, env="conda stateinsp", p=["~8ms/帧 · 权重 ~19MB"]),
            dict(t=["落位检查"], s=["ROI 灰度深色覆盖率", "≥70%（阈值 80）"], cpu=True, p=["OpenCV 规则 · 无模型"]),
            dict(t=["保护膜撕除"], s=["ROI 双白条检测", "列亮度中位数 · 亮差 35"], cpu=True, p=["0 条 OK / 1-2 条 NG"]),
            dict(t=["黑膜捋平"], s=["上缘距离 P80 vs", "合格模板 +3px 容差"], cpu=True, p=["实测 133 < 上限 154.8px"]),
            dict(t=["汇总与上报"], s=["runs/ 落盘 + Dash 工位台", "HTTP API :8060 五项独立接口"], cpu=True, p=["MES / 机械臂按项调用"]),
        ],
        offline_label="离线 GPU",
        offline=[dict(cpu=False, w=560, t="采集 → 标注（SAM2 辅助，可选）→ YOLO 训练（device=0）", p="178 张人工标注 · v2s yolo11s@640 · 第 84 轮最佳")],
        offline_note="一次性 / 偶发",
        note="关键数字：mAP50 0.995 / mAP50-95 0.819 · 现场置信度 0.86 · 推理 ~8ms/帧满足 ≤10Hz 节拍 · 其余四项全规则算法 · 冷启 ~4–10s",
    ),
]

POINTS = [
    ("GPU 只集中在「神经网络」环节",
     ["在线推理 4 处：YOLO 分割 · FoundationPose 精配 · YOLO 整臂 · YOLO 正反面；",
      "标定 / 采集 / 几何算法 / 规则判定 / 联动上报全部 CPU。"]),
    ("显存压力小、单卡可共载",
     ["最大 FoundationPose 实测 ~255MB，其余为 5~19MB 小模型；",
      "02 已实测 YOLO+FP 在 RTX 5050 8GB 共存无 OOM。"]),
    ("GPU 依赖环境隔离、可统一管理",
     ["全部在独立 conda 环境 / 子进程，主程序不装 torch；",
      "CUDA 走 conda（无系统级安装），换卡 / 换驱动只动 envs。"]),
    ("主要代价是冷启动（4~10s）而非吞吐",
     ["GPU 推理进程需常驻或预热，不宜频繁启停；",
      "训练离线偶发（分钟级），可与在线推理错峰。"]),
    ("CPU 退化路径有限，建议配看门狗",
     ["02 透明壳 ICP 拉偏 ~22mm 必须 GPU；09 可退 CPU 但慢；",
      "08 检测退 CPU 帧率无保障 → 降级 / 告警策略需预先设计。"]),
]
SUM_TITLE = "给上层架构师的结论"

TBL_HEAD = ["项目", "在线 GPU 环节", "离线 GPU 环节", "GPU 框架 · 环境", "实测性能 · 显存"]
TBL_ROWS = [
    (["02-3D-detect", "6D 位姿识别与抓取"],
     ["实例分割 YOLO11-seg", "6D 精配 FoundationPose"],
     ["YOLO 训练；SAM2 标注"],
     ["torch cu130 + nvdiffrast + pytorch3d", "envs/yoloseg · envs/foundationpose 子进程"],
     ["FP 显存 ~255MB · 单实例 74ms≈13.5Hz", "8GB 共存无 OOM · 冷启 ~10s"]),
    (["08-Intrusion", "区域入侵检测"],
     ["整臂检测 YOLO11n@1280", "（≈10FPS 节流）"],
     ["YOLO 训练（device=0）"],
     ["ultralytics + torch CUDA", "conda yolo 环境子进程"],
     ["mAP50 0.995 · 权重 5.4MB · 冷启 >8s（已预热）", "深度判定全 CPU"]),
    (["09-State-Inspection", "工艺状态巡检"],
     ["正反面识别 YOLO11s@640", "（~8ms/帧，≤10Hz 节拍达标）"],
     ["YOLO 训练 · SAM2 辅助", "标注（可选）"],
     ["torch cu130 + ultralytics", "conda stateinsp 单环境"],
     ["mAP50 0.995 · 权重 ~19MB", "冷启 ~4–10s · 漏检较 v1 降 22%"]),
]

FOOTER = ("依据：各项目 README / docs / 源码 manifest 与配置（02: docs/12 台账 · 08: configs/settings.json · 09: DATASET.md）"
          "　·　2026-10-13　·　参数化脚本生成（论文配图技能库 02 路线 + 06 样式预设）")


# ================= 组装（样式全部取自令牌 S） =================
def tw(s: str, fs: float) -> float:
    """文字宽度预算（技能库规范）：CJK×fs + latin×0.55×fs"""
    cjk = sum(1 for c in s if ord(c) > 0x2E00)
    lat = len(s) - cjk
    return cjk * fs + lat * 0.55 * fs


def fit(s: str, fs: float, maxw: float, where: str):
    w = tw(s, fs)
    assert w <= maxw, f"[{where}] 越界 +{w - maxw:.0f}px（{w:.0f}/{maxw:.0f}）: {s}"


def build(S: dict, key: str):
    FT, FB, FM = S["font_title"], S["font_body"], S["font_mono"]

    def esc(s):
        return html.escape(s, quote=True)

    def text(x, y, s, fs, fill, w=None, fam=None, anchor="start", ls=None):
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        wt = f' font-weight="{w}"' if w else ""
        lsp = f' letter-spacing="{ls}"' if ls else ""
        return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" fill="{fill}" '
                f'font-family="{fam or FB}"{wt}{a}{lsp}>{esc(s)}</text>')

    def rrect(x, y, w, h, r, fill, stroke=None, sw=1.2, dash=None, fx=None):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        f = f' filter="url(#{fx})"' if fx else ""
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}"{st}{da}{f}/>'

    def chip(x, y, label, kind):
        h = 15
        w = tw(label, FS_CHIP) + 14
        bg, fg = (S["gpu_chip_bg"], S["gpu_chip_fg"]) if kind == "gpu" else (S["cpu_chip_bg"], S["cpu_chip_fg"])
        return rrect(x, y, w, h, S["chip_r"], bg) + text(x + w / 2, y + 11, label, FS_CHIP, fg, 700, anchor="middle"), x + w

    def env_pill(x, y, label):
        h = 15
        w = tw(label, FS_ENV) + 12
        return rrect(x, y, w, h, 4, S["env_fill"]) + text(x + w / 2, y + 10.5, label, FS_ENV, S["env_fg"], fam=FM, anchor="middle"), x + w

    def arrow(x1, x2, y):
        return (f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2 - 2:.1f}" y2="{y:.1f}" stroke="{S["arrow"]}" '
                f'stroke-width="1.6" marker-end="url(#arr)"/>')

    big_fx = "fsoft" if S["fx"] in ("soft", "glow") else None
    gpu_fx = "fglow" if S["fx"] == "glow" else (big_fx if S["fx"] == "soft" else None)

    def stage_card(x, y, w, st, lane_i, st_i):
        pad = 11
        iw = w - 2 * pad
        gpu = not st["cpu"]
        fill, edge = (S["gpu_fill"], S["gpu_edge"]) if gpu else (S["cpu_fill"], S["cpu_edge"])
        body = [rrect(x, y, w, CARD_H, min(S["card_r"], 10), fill, edge, 1.8 if gpu else 1.2, fx=gpu_fx)]
        ty = y + pad + 12
        for line in st["t"]:
            fit(line, FS_CARD_T, iw, f"[{key}]lane{lane_i}-stage{st_i}-title")
            body.append(text(x + pad, ty, line, FS_CARD_T, S["ink"], 700, fam=FT))
            ty += 16
        ty += 2
        sy = ty
        for line in st["s"]:
            fit(line, FS_CARD_S, iw, f"[{key}]lane{lane_i}-stage{st_i}-sub")
            body.append(text(x + pad, sy, line, FS_CARD_S, S["gpu_sub"] if gpu else S["muted"]))
            sy += 13.5
        by = y + CARD_H - 10
        chip_y = by - 15
        tags, tx = "", x + pad
        tg, tx = chip(tx, chip_y, "GPU" if gpu else "CPU", "gpu" if gpu else "cpu")
        tags += tg
        if gpu:
            tg, tx = env_pill(tx + 5, chip_y, st["env"])
            tags += tg
        py = chip_y - 5
        for line in reversed(st["p"]):
            fit(line, FS_CARD_P, iw, f"[{key}]lane{lane_i}-stage{st_i}-perf")
            body.append(text(x + pad, py, line, FS_CARD_P, S["gpu_perf"] if gpu else S["faint"]))
            py -= 12.5
        assert sy - 13.5 + 4 <= py - 2, f"[{key}]lane{lane_i}-stage{st_i} 内容超高"
        return "".join(body)

    def build_lane(lane, lane_i, y0):
        parts = [rrect(LANE_X, y0, LANE_W, LANE_H, S["card_r"], S["card"], S["card_edge"], 1.2, fx=big_fx)]
        bx, by = LANE_X + LPAD, y0 + 20
        parts.append(rrect(bx, by, 34, 34, max(S["card_r"] - 5, 3), S["badge_bg"]))
        parts.append(text(bx + 17, by + 23, lane["no"], 17, S["badge_fg"], 700, fam=FT, anchor="middle"))
        tx0 = bx + 34 + 14
        parts.append(text(tx0, by + 15, lane["name"], FS_LANE_T, S["ink"], 700, fam=FT))
        fit(lane["name"], FS_LANE_T, LANE_W - (tx0 - LANE_X) - 220, f"[{key}]lane{lane_i}-name")
        parts.append(text(tx0, by + 33, lane["desc"], FS_LANE_D, S["muted"]))
        fit(lane["desc"], FS_LANE_D, LANE_W - (tx0 - LANE_X) - 220, f"[{key}]lane{lane_i}-desc")
        bw = tw(lane["badge"], 12.5) + 26
        bxp = LANE_X + LANE_W - LPAD - bw
        parts.append(rrect(bxp, by + 4, bw, 25, 12.5, S["gpu_soft"], S["gpu_edge"], 1.2))
        parts.append(text(bxp + bw / 2, by + 21, lane["badge"], 12.5, S["gpu_deep"], 700, anchor="middle"))
        n = len(lane["stages"])
        inner_w = LANE_W - 2 * LPAD
        cw = (inner_w - (n - 1) * GAP_ARR) / n
        row_y = by + 34 + 12
        cy = row_y + CARD_H / 2
        x = LANE_X + LPAD
        for i, st in enumerate(lane["stages"]):
            parts.append(stage_card(x, row_y, cw, st, lane_i, i))
            if i < n - 1:
                parts.append(arrow(x + cw + 3, x + cw + GAP_ARR - 3, cy))
            x += cw + GAP_ARR
        oy = row_y + CARD_H + 13
        parts.append(text(LANE_X + LPAD + 2, oy + 21, lane["offline_label"], 11.5, S["gpu_deep"], 700, ls=1))
        ox = LANE_X + LPAD + 2 + tw(lane["offline_label"], 11.5) + 16
        for k, ob in enumerate(lane["offline"]):
            gpu = not ob["cpu"]
            wdt = ob["w"]
            if gpu:
                parts.append(rrect(ox, oy + 2, wdt, OFF_H - 10, min(S["card_r"], 9), S["off_fill"],
                                   S["gpu_edge"], 1.5, dash=S["off_dash"]))
            else:
                parts.append(rrect(ox, oy + 2, wdt, OFF_H - 10, min(S["card_r"], 9), S["cpu_fill"],
                                   S["cpu_edge"], 1.2))
            parts.append(text(ox + 11, oy + 18, ob["t"], 11.5, S["ink"], 700))
            fit(ob["t"], 11.5, wdt - 22, f"[{key}]lane{lane_i}-off{k}-t")
            parts.append(text(ox + 11, oy + 32, ob["p"], 10.2, S["gpu_perf"] if gpu else S["muted"]))
            fit(ob["p"], 10.2, wdt - 22, f"[{key}]lane{lane_i}-off{k}-p")
            ox += wdt
            if k < len(lane["offline"]) - 1:
                parts.append(arrow(ox + 5, ox + GAP_ARR - 3, oy + OFF_H / 2 - 3))
                ox += GAP_ARR
        parts.append(text(ox + 14, oy + 21, lane["offline_note"], 11, S["faint"]))
        ny = oy + OFF_H + 8
        parts.append(rrect(LANE_X + LPAD, ny, inner_w, NOTE_H, 7, S["note_bg"], S["note_line"], 1))
        lead, rest = "关键数字：", lane["note"][len("关键数字："):]
        fit(lane["note"], FS_NOTE, inner_w - 24, f"[{key}]lane{lane_i}-note")
        lx = LANE_X + LPAD + 12
        parts.append(f'<text x="{lx}" y="{ny + 20}" font-size="{FS_NOTE}" font-family="{FB}">'
                     f'<tspan font-weight="700" fill="{S["ink"]}">{esc(lead)}</tspan>'
                     f'<tspan fill="{S["muted"]}">{esc(rest)}</tspan></text>')
        return "".join(parts)

    E = [f'<rect x="0" y="0" width="{W}" height="2400" fill="{S["page_bg"]}"/>']
    defs = (f'<marker id="arr" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="8" '
            f'refX="8" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 z" fill="{S["arrow"]}"/></marker>')
    if S["fx"] in ("soft", "glow"):
        dark = "#0f172a" if S["fx"] == "soft" else "#000000"
        op = "0.08" if S["fx"] == "soft" else "0.45"
        defs += (f'<filter id="fsoft" x="-15%" y="-15%" width="130%" height="130%">'
                 f'<feDropShadow dx="0" dy="1.5" stdDeviation="2.6" flood-color="{dark}" flood-opacity="{op}"/></filter>')
    if S["fx"] == "glow":
        defs += (f'<filter id="fglow" x="-40%" y="-40%" width="180%" height="180%">'
                 f'<feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="{S["gpu_edge"]}" flood-opacity="0.4"/></filter>')
    if S["deco"] == "dots":
        defs += (f'<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">'
                 f'<circle cx="1.5" cy="1.5" r="1.3" fill="#1b2942"/></pattern>')
    E.append(f"<defs>{defs}</defs>")
    if S["deco"] == "dots":
        E.append(f'<rect x="0" y="0" width="{W}" height="2400" fill="url(#dots)"/>')

    # --- 页头 ---
    hh = S["head_h"]
    if S["head"] == "band":
        E.append(f'<rect x="0" y="0" width="{W}" height="{hh}" fill="{S["head_bg"]}"/>')
        E.append(text(M, 44, TITLE, FS_TITLE, S["head_title"], 700, fam=FT))
        E.append(text(M, 74, SUBTITLE, FS_SUB, S["head_sub"]))
        dw = tw(DATE_CHIP, 12) + 24
        E.append(rrect(W - M - dw, 32, dw, 24, 12, "none", S["date_edge"], 1.2))
        E.append(text(W - M - dw / 2, 48, DATE_CHIP, 12, S["head_sub"], anchor="middle"))
    else:
        tx = M
        if S["head_bar"]:
            E.append(rrect(M, 26, 5, 30, 2, S["head_bar"]))
            tx = M + 16
        E.append(text(tx, 44, TITLE, FS_TITLE, S["head_title"], 700, fam=FT))
        E.append(text(M, 74, SUBTITLE, FS_SUB, S["head_sub"]))
        if S["date_style"] == "pill":
            dw = tw(DATE_CHIP, 12) + 24
            E.append(rrect(W - M - dw, 32, dw, 24, 12, "none", S["date_edge"], 1.2))
            E.append(text(W - M - dw / 2, 48, DATE_CHIP, 12, S["head_sub"], anchor="middle"))
        else:
            E.append(text(W - M, 44, DATE_CHIP, 12.5, S["faint"], anchor="end"))
        if S["head_rule"]:
            E.append(f'<line x1="{M}" y1="{hh - 12}" x2="{W - M}" y2="{hh - 12}" stroke="{S["line"]}" stroke-width="1.2"/>')
    fit(TITLE, FS_TITLE, INNER - 160, f"[{key}]title")
    fit(SUBTITLE, FS_SUB, INNER - 130, f"[{key}]subtitle")

    # --- 图例行 ---
    ly = hh + 27
    lx = M + 2
    for kind, label in LEGEND:
        if kind == "gpu":
            E.append(rrect(lx, ly - 11, 22, 13, S["chip_r"] / 2 + 1, S["gpu_fill"], S["gpu_edge"], 1.6))
        elif kind == "gpuf":
            E.append(rrect(lx, ly - 11, 22, 13, S["chip_r"] / 2 + 1, S["off_fill"], S["gpu_edge"], 1.5, dash=S["off_dash"]))
        else:
            E.append(rrect(lx, ly - 11, 22, 13, S["chip_r"] / 2 + 1, S["cpu_fill"], S["cpu_edge"], 1.3))
        E.append(text(lx + 30, ly, label, 12.5, S["text_mid"]))
        lx += 30 + tw(label, 12.5) + 26
    E.append(text(lx, ly, LEGEND_NOTE, 11.5, S["faint"]))

    # --- 三条泳道 ---
    y = hh + 46
    for i, lane in enumerate(LANES):
        E.append(build_lane(lane, i + 1, y))
        y += LANE_H + LANE_GAP

    # --- 结论 + 清单卡 ---
    y += 6
    E.append(rrect(SUM_X, y, SUM_W, SUM_H, S["card_r"], S["card"], S["card_edge"], 1.2, fx=big_fx))
    E.append(text(SUM_X + SUM_PAD, y + SUM_PAD + 12, SUM_TITLE, 17, S["ink"], 700, fam=FT))
    py = y + SUM_PAD + 34
    last = SUM_W - SUM_PAD * 2 - sum(TBL_COL)
    cols = TBL_COL + [last]
    for idx, (head, details) in enumerate(POINTS):
        col, row = idx % 2, idx // 2
        px = SUM_X + SUM_PAD + col * (COL_W + 28)
        qy = py + row * PT_SLOT
        E.append(f'<circle cx="{px + 4}" cy="{qy - 4}" r="3.5" fill="{S["gpu_edge"]}"/>')
        E.append(text(px + 15, qy, head, FS_PT_T, S["ink"], 700, fam=FT))
        fit(head, FS_PT_T, COL_W - 15, f"[{key}]point{idx}-head")
        for j, d in enumerate(details):
            fit(d, FS_PT_D, COL_W - 15, f"[{key}]point{idx}-d{j}")
            E.append(text(px + 15, qy + 17 + j * 16.5, d, FS_PT_D, S["muted"]))
    ty0 = py + 3 * PT_SLOT + 10
    E.append(rrect(SUM_X + SUM_PAD, ty0, SUM_W - 2 * SUM_PAD, TBL_HH + 3 * TBL_RH, 8, S["card"], S["line"], 1.2))
    E.append(rrect(SUM_X + SUM_PAD, ty0, SUM_W - 2 * SUM_PAD, TBL_HH, 8, S["table_head"]))
    cx = SUM_X + SUM_PAD
    for c, htxt in zip(cols, TBL_HEAD):
        E.append(text(cx + 10, ty0 + 21, htxt, 11.5, S["text_mid"], 700))
        cx += c
    for r, row in enumerate(TBL_ROWS):
        ry = ty0 + TBL_HH + r * TBL_RH
        if r:
            E.append(f'<line x1="{SUM_X + SUM_PAD}" y1="{ry}" x2="{SUM_X + SUM_W - SUM_PAD}" y2="{ry}" stroke="{S["line"]}"/>')
        cx = SUM_X + SUM_PAD
        for ci, (c, cell) in enumerate(zip(cols, row)):
            for j, line in enumerate(cell):
                if ci == 0:
                    col_fill, wt = (S["ink"], 700) if j == 0 else (S["muted"], None)
                elif ci == 1:
                    col_fill, wt = S["gpu_deep"], 700
                else:
                    col_fill, wt = S["muted"], None
                fit(line, FS_TBL, c - 20, f"[{key}]tbl-r{r}-c{ci}-l{j}")
                E.append(text(cx + 10, ry + 20 + j * 15.5, line, FS_TBL, col_fill, wt))
            cx += c
    for k in range(len(cols) - 1):
        vx = SUM_X + SUM_PAD + sum(cols[:k + 1])
        E.append(f'<line x1="{vx}" y1="{ty0}" x2="{vx}" y2="{ty0 + TBL_HH + 3 * TBL_RH}" stroke="{S["line"]}"/>')

    # --- 页脚 ---
    fy = y + SUM_H + 26
    E.append(text(M + 2, fy, FOOTER, 10.5, S["faint"]))
    fit(FOOTER, 10.5, INNER - 4, f"[{key}]footer")
    H = fy + 30

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" '
           f'viewBox="0 0 {W} {H:.0f}" font-family="{FB}">' + "".join(E) + "</svg>")
    return svg, W, int(H)


def emit(key: str, outdir: Path):
    S = get_style(key)
    svg, w, h = build(S, key)
    outdir.mkdir(parents=True, exist_ok=True)
    svg_path = outdir / f"三项目GPU环节流程图_{ZH[key]}.svg"
    svg_path.write_text(svg, encoding="utf-8")
    mt = int(svg_path.stat().st_mtime)
    exp = (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
           f'*{{margin:0;padding:0}}body{{background:{S["page_bg"]}}}'
           f'img{{display:block;width:{w}px;height:{h}px}}</style></head>'
           f'<body><img src="三项目GPU环节流程图_{ZH[key]}.svg?v={mt}"></body></html>')
    (outdir / f"export_{key}.html").write_text(exp, encoding="utf-8")
    print(f"[{key:8s}] {w}x{h}  -> {svg_path.name}  (export_{key}.html)")


def main():
    ap = argparse.ArgumentParser(description="三项目 GPU 流程图 · 多风格参数化出图")
    ap.add_argument("--style", default="academic", choices=names() + ["all"],
                    help="风格：academic(默认科研风)/web/tech/all")
    ap.add_argument("--outdir", default=None, help="输出目录（默认脚本所在目录）")
    a = ap.parse_args()
    outdir = Path(a.outdir) if a.outdir else DEST
    for key in (names() if a.style == "all" else [a.style]):
        emit(key, outdir)


if __name__ == "__main__":
    main()
