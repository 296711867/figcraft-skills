"""Re-render all six manuscript figures as SVG + 2x PNG, faithfully to make_figures.py.

Data source: the same frozen analysis CSVs (<project>/outputs). Encodings identical
(palette, markers, axes, log scales); only typography/layout fixes on top:
  - fig1: "Frozen deployment" title no longer overflows its box (title fontsize 7.4,
    body top offset adjusted); everything else unchanged.

Read-only w.r.t. analysis outputs. Run:  python make_figures_svg.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / "outputs"                 # <project>/outputs (frozen CSVs)
FIG = HERE
FIG.mkdir(exist_ok=True)

# dataviz reference palette (identical to make_figures.py)
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRAY, GRID = "#0b0b0b", "#52514e", "#8c8b86", "#e4e3df"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.5,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "grid.color": GRID,
    "grid.linewidth": 0.6,
    "legend.frameon": False,
    "savefig.dpi": 600,          # 2x-quality PNG (reference was 300)
    "pdf.fonttype": 42,
    "svg.fonttype": "path",      # text as paths: portable SVG
})


# ---------------------------------------------------------------- data (identical)
def load() -> dict[str, pd.DataFrame]:
    frames = []
    b = pd.read_csv(OUT / "final_conf_analysis" / "internal_room_errors.csv")
    for col, name in [("PatchTSTCI", "PatchTST-CI (MSE)"), ("Persistence", "Persistence"),
                      ("RidgeDelta", "RidgeDelta"), ("DLinear", "DLinear")]:
        frames.append(pd.DataFrame({"cohort": "bear39", "unit": b["room"].astype(str),
                                    "horizon": b["horizon_hours"], "method": name, "mae": b[col]}))
    g = pd.read_csv(OUT / "volatility_gate_analysis" / "stage1_per_unit.csv")
    g = g[(g.cohort == "bear39") & (g.arm == "mae")]
    frames.append(pd.DataFrame({"cohort": "bear39", "unit": g["unit"].astype(str),
                                "horizon": g["horizon"], "method": "PatchTST-CI (MAE)",
                                "mae": g["always_model_mae"]}))
    r = pd.read_csv(OUT / "final_conf_analysis" / "rescast_building_mae.csv")
    for h in (1, 6, 24):
        for col, name in [(f"PatchTSTCI_h{h}", "PatchTST-CI (MSE)"), (f"Persistence_h{h}", "Persistence")]:
            frames.append(pd.DataFrame({"cohort": "rescast24", "unit": r["building_id"].astype(str),
                                        "horizon": h, "method": name, "mae": r[col]}))
    d = pd.read_csv(OUT / "duration_confound_analysis" / "per_building.csv")
    for h in (1, 6, 24):
        for col, name in [(f"mse_h{h}", "PatchTST-CI (MSE)"), (f"mae_h{h}", "PatchTST-CI (MAE)"),
                          (f"mse32_h{h}", "PatchTST-CI (MSE, 32 ep.)"),
                          (f"persistence_h{h}", "Persistence")]:
            frames.append(pd.DataFrame({"cohort": "rescast48", "unit": d["building_id"].astype(str),
                                        "horizon": h, "method": name, "mae": d[col]}))
    f = pd.read_csv(OUT / "fm_baseline_analysis" / "per_unit_mae.csv")
    fm_name = {"chronos2": "Chronos-2", "timesfm": "TimesFM 2.5", "moirai2": "Moirai-2"}
    f["method"] = f["model"].map(fm_name) + np.where(f["arm"] == "long", " (168 h)", "")
    frames.append(pd.DataFrame({"cohort": f["cohort"], "unit": f["unit"].astype(str),
                                "horizon": f["horizon"], "method": f["method"], "mae": f["mae"]}))
    return pd.concat(frames, ignore_index=True)


def mean_table(long: pd.DataFrame) -> pd.DataFrame:
    return long.groupby(["cohort", "method", "horizon"])["mae"].mean().unstack("horizon")


def paired(long, cohort, h, a, b):
    sub = long[(long.cohort == cohort) & (long.horizon == h)]
    p = sub.pivot(index="unit", columns="method", values="mae")[[a, b]].dropna()
    return p[a].to_numpy(), p[b].to_numpy()


def rel(m, ref):
    return 100.0 * (m - ref) / ref


def save(fig, name):
    fig.savefig(FIG / f"{name}.svg", bbox_inches="tight")
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight")
    plt.close(fig)
    print("saved", name)


# ---------------------------------------------------------------- fig 1
def fig_overview():
    fig, ax = plt.subplots(figsize=(6.9, 2.75))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 40)
    ax.axis("off")

    def box(x, y, w, h, title, body):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                    linewidth=0.8, edgecolor=INK2, facecolor="#f6f5f2"))
        ax.text(x + w / 2, y + h - 2.2, title, ha="center", va="top", fontsize=7.4,
                fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 6.6, body, ha="center", va="top", fontsize=6.3, color=INK2,
                linespacing=1.35)

    def arrow(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.8, mutation_scale=8))

    box(0.5, 8, 22, 29, "Source rooms",
        "64 BEAR rooms (°F)\nchronological\ntrain / val split\n\nonly the room's own\ntemperature channel\nis given to the model")
    box(26, 8, 22, 29, "Training (once)",
        "PatchTST-CI\n9,667 parameters\nwindow norm. (RevIN)\npatch 6, stride 3\n\nloss and early stopping\n= deployment metric\n(MAE)")
    box(51.5, 8, 22, 29, "Frozen deployment",
        "unseen room/building\nlast 24 h of its\ntemperature only\n\nno identity, weather,\nsetpoints or scaler;\nno fine-tuning")
    box(77, 8, 22, 29, "Horizon routing",
        "1 h, 6 h: frozen model\n24 h: Persistence\n(same hour yesterday)\n\n>24 h of history:\npretrained foundation\nforecaster")
    arrow(23.3, 22.5, 25.3, 22.5)
    arrow(48.8, 22.5, 50.8, 22.5)
    arrow(74.3, 22.5, 76.3, 22.5)
    ax.text(50, 2.2, "Evaluation: fresh BEAR rooms (measured) and simulated RESCAST buildings never used for "
            "any modelling decision; unit-weighted MAE, paired tests.", ha="center", fontsize=6.8,
            color=INK2, style="italic")
    save(fig, "fig1_overview")


# ---------------------------------------------------------------- fig 2
COH = {"bear39": ("BEAR, 39 fresh rooms", BLUE, "o"),
       "rescast24": ("RESCAST, 24 buildings", ORANGE, "s"),
       "rescast48": ("RESCAST, 48 buildings", AQUA, "^")}


def fig_landscape(long):
    mt = mean_table(long)
    rows = ["RidgeDelta", "DLinear", "PatchTST-CI (MSE)", "PatchTST-CI (MAE)",
            "Chronos-2", "TimesFM 2.5", "Moirai-2",
            "Chronos-2 (168 h)", "TimesFM 2.5 (168 h)", "Moirai-2 (168 h)"]
    labels = ["Ridge (Δ-target)", "DLinear", "PatchTST-CI, MSE", "PatchTST-CI, MAE",
              "Chronos-2", "TimesFM 2.5", "Moirai-2",
              "Chronos-2", "TimesFM 2.5", "Moirai-2"]
    ypos = {r: (len(rows) - 1 - i + (0.6 if i < 7 else 0)) for i, r in enumerate(rows)}
    lo, hi = -82, 100
    fig, axes = plt.subplots(1, 3, figsize=(6.9, 3.6), sharey=True)
    offs = {"bear39": 0.18, "rescast24": 0.0, "rescast48": -0.18}
    for ax, h in zip(axes, (1, 6, 24)):
        ax.axvline(0, color=INK2, lw=0.8)
        ax.grid(axis="x")
        ax.set_axisbelow(True)
        for c, (lab, col, mk) in COH.items():
            ref = mt.loc[(c, "Persistence"), h]
            for r in rows:
                if (c, r) not in mt.index:
                    continue
                v = rel(mt.loc[(c, r), h], ref)
                y = ypos[r] + offs[c]
                if v > hi:
                    ax.plot(hi, y, marker=">", color=col, ms=5, lw=0)
                    ax.text(hi - 6, y + 1.8 * offs[c], f"+{v:.0f}", ha="right", va="center",
                            fontsize=6, color=INK2)
                else:
                    ax.plot(v, y, marker=mk, color=col, ms=4.6, lw=0, mec="white", mew=0.5)
        ax.set_xlim(lo, hi + 4)
        ax.set_title(f"{h} h ahead", color=INK)
        ax.set_xlabel("MAE change vs Persistence (%)" if h == 6 else "")
        ax.set_xticks([-50, 0, 50, 100])
        ax.axhline(ypos["Moirai-2"] - 0.8, color=GRID, lw=0.8)
    axes[0].set_yticks([ypos[r] for r in rows])
    axes[0].set_yticklabels(labels)
    axes[0].text(-0.80, (ypos["Chronos-2 (168 h)"] + ypos["Moirai-2 (168 h)"]) / 2,
                 "168 h\ncontext", transform=axes[0].get_yaxis_transform(), ha="center",
                 va="center", fontsize=6.8, color=INK2, rotation=90)
    axes[0].text(-0.80, (ypos["RidgeDelta"] + ypos["Moirai-2"]) / 2,
                 "24 h context (task contract)", transform=axes[0].get_yaxis_transform(),
                 ha="center", va="center", fontsize=6.8, color=INK2, rotation=90)
    handles = [plt.Line2D([], [], marker=mk, color=col, lw=0, ms=5, label=lab)
               for lab, col, mk in COH.values()]
    fig.legend(handles=handles, loc="upper center", ncol=3, bbox_to_anchor=(0.55, 1.03))
    fig.tight_layout(rect=(0.02, 0, 1, 0.95))
    save(fig, "fig2_landscape")


# ---------------------------------------------------------------- fig 3
def fig_paired(long):
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 2.9))
    spec = [("bear39", "PatchTST-CI (MSE)", "(a) BEAR, 39 fresh rooms"),
            ("rescast24", "PatchTST-CI (MSE)", "(b) RESCAST, 24 buildings")]
    for ax, (c, m, title) in zip(axes, spec):
        mod, per = paired(long, c, 6, m, "Persistence")
        chr_, per2 = paired(long, c, 6, "Chronos-2", "Persistence")
        lo = min(mod.min(), per.min(), chr_.min()) * 0.8
        hi = max(mod.max(), per.max(), chr_.max()) * 1.2
        ax.plot([lo, hi], [lo, hi], color=INK2, lw=0.8)
        ax.scatter(per2, chr_, s=16, marker="s", facecolor="none", edgecolor=ORANGE, lw=0.8,
                   label="Chronos-2 (zero-shot)", zorder=2)
        ax.scatter(per, mod, s=16, color=BLUE, edgecolor="white", lw=0.4,
                   label="PatchTST-CI (9,667 param.)", zorder=3)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_xlabel("Persistence 6 h MAE (°F)")
        ax.set_ylabel("Model 6 h MAE (°F)")
        ax.set_title(title, loc="left")
        ax.grid(which="major")
        wins = int((mod < per).sum())
        ax.text(0.97, 0.05, f"PatchTST-CI below diagonal: {wins}/{len(mod)}",
                transform=ax.transAxes, ha="right", fontsize=6.8, color=INK2)
    axes[0].legend(loc="upper left")
    fig.tight_layout()
    save(fig, "fig3_paired6h")


# ---------------------------------------------------------------- fig 4
def fig_objective(long):
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.85), gridspec_kw={"width_ratios": [1, 1.15]})
    ax = axes[0]
    mse, mae = paired(long, "rescast48", 6, "PatchTST-CI (MSE)", "PatchTST-CI (MAE)")
    lo, hi = min(mse.min(), mae.min()) * 0.85, max(mse.max(), mae.max()) * 1.15
    ax.plot([lo, hi], [lo, hi], color=INK2, lw=0.8)
    ax.scatter(mse, mae, s=16, color=AQUA, edgecolor="white", lw=0.4)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.grid()
    ax.set_xlabel("MSE-trained 6 h MAE (°F)")
    ax.set_ylabel("MAE-trained 6 h MAE (°F)")
    ax.set_title("(a) 48 RESCAST buildings, 6 h", loc="left")
    ax.text(0.97, 0.05, f"below diagonal: {(mae < mse).sum()}/{len(mae)}", transform=ax.transAxes,
            ha="right", fontsize=6.8, color=INK2)

    ax = axes[1]
    mt = mean_table(long).loc["rescast48"]
    arms = [("Persistence", "Persistence", GRAY, "D"),
            ("PatchTST-CI (MSE)", "MSE, early-stopped", BLUE, "o"),
            ("PatchTST-CI (MSE, 32 ep.)", "MSE, fixed 32 epochs", ORANGE, "s"),
            ("PatchTST-CI (MAE)", "MAE (aligned)", AQUA, "^")]
    xs = np.arange(3)
    for k, (m, lab, col, mk) in enumerate(arms):
        vals = [mt.loc[m, h] for h in (1, 6, 24)]
        ax.plot(xs + (k - 1.5) * 0.13, vals, marker=mk, lw=0, color=col, ms=5.2, label=lab,
                mec="white", mew=0.5)
    ax.set_xticks(xs)
    ax.set_xticklabels(["1 h", "6 h", "24 h"])
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(0, 1.45)
    ax.grid(axis="y")
    ax.set_ylabel("mean building MAE (°F)")
    ax.set_title("(b) objective and training-duration arms", loc="left")
    ax.legend(loc="upper left", ncol=1)
    fig.tight_layout()
    save(fig, "fig4_objective")


# ---------------------------------------------------------------- fig 5
def fig_context(long):
    mt = mean_table(long)
    fig, axes = plt.subplots(1, 3, figsize=(6.9, 2.6))
    fms = [("Chronos-2", BLUE, "o"), ("TimesFM 2.5", ORANGE, "s"), ("Moirai-2", AQUA, "^")]
    titles = {"bear39": "(a) BEAR, 39 rooms", "rescast24": "(b) RESCAST, 24 bldgs",
              "rescast48": "(c) RESCAST, 48 bldgs"}
    for ax, c in zip(axes, ("bear39", "rescast24", "rescast48")):
        per = mt.loc[(c, "Persistence"), 6]
        ax.axhline(per, color=GRAY, lw=0.9, ls=(0, (4, 2)))
        ax.text(1.35, per, "Persistence", fontsize=6.3, color=INK2, va="bottom", ha="right")
        for m, col, mk in fms:
            v = [mt.loc[(c, m), 6], mt.loc[(c, m + " (168 h)"), 6]]
            ax.plot([0, 1], v, color=col, lw=1.2, marker=mk, ms=4.8, mec="white", mew=0.5,
                    label=m)
        ours = "PatchTST-CI (MAE)" if (c, "PatchTST-CI (MAE)") in mt.index else "PatchTST-CI (MSE)"
        ax.plot([0], [mt.loc[(c, ours), 6]], marker="*", color=INK, ms=9, lw=0,
                label="PatchTST-CI (24 h only)")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["24 h", "168 h"])
        ax.set_xlim(-0.35, 1.4)
        ax.set_xlabel("history available")
        ax.set_title(titles[c], loc="left")
        ax.grid(axis="y")
        ax.set_ylim(0, max(1.35, per * 1.08))
    axes[0].set_ylabel("mean 6 h MAE (°F)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 1.07))
    fig.tight_layout()
    save(fig, "fig5_context")


# ---------------------------------------------------------------- fig 6
def fig_persistence_shape(long):
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    allv = []
    for c, (lab, col, mk) in COH.items():
        sub = long[(long.cohort == c) & (long.method == "Persistence")]
        p = sub.pivot(index="unit", columns="horizon", values="mae")
        n_easier = int((p[24] < p[6]).sum())
        ax.scatter(p[6], p[24], s=14, marker=mk, color=col, edgecolor="white", lw=0.4,
                   label=f"{lab}: {n_easier}/{len(p)}")
        allv += [p[6].min(), p[24].min(), p[6].max(), p[24].max()]
    lo, hi = min(allv) * 0.8, max(allv) * 1.2
    ax.plot([lo, hi], [lo, hi], color=INK2, lw=0.8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.grid()
    ax.set_xlabel("Persistence 6 h MAE (°F)")
    ax.set_ylabel("Persistence 24 h MAE (°F)")
    ax.legend(title="units where 24 h < 6 h", loc="lower right", title_fontsize=6.5, fontsize=6.3)
    fig.tight_layout()
    save(fig, "fig6_persistence")


def main():
    long = load()
    fig_overview()
    fig_landscape(long)
    fig_paired(long)
    fig_objective(long)
    fig_context(long)
    fig_persistence_shape(long)


if __name__ == "__main__":
    main()
