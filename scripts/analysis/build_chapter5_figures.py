"""Generate thesis-ready Chapter 5 result figures."""

from __future__ import annotations

from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "thesis" / "Figures" / "Chapter5"

BG = "#fbfcfe"
PANEL = "#ffffff"
TEXT = "#172033"
MUTED = "#5b667a"
GRID = "#d9e1ec"
EDGE = "#2f3d52"

COLORS = {
    "eo": "#3778bf",
    "gray": "#dfa62a",
    "supervised": "#2f9362",
    "large": "#7251a3",
    "ensemble": "#7b8794",
    "highres": "#209da8",
    "highres2": "#48b6c2",
    "ir": "#2364aa",
    "combo": "#d9912b",
    "soft_green": "#e8f8ef",
    "soft_blue": "#eaf3ff",
    "soft_teal": "#e6f7f8",
}

IR_VALUES = {
    "E01": 0.0948,
    "E02": 0.1040,
    "E03": 0.0811,
    "E04": 0.0812,
    "E05": 0.4229,
    "E06": 0.4342,
    "E07": 0.4031,
    "E08": 0.4555,
    "E09": 0.4438,
    "E10": 0.4553,
    "E11": 0.5250,
    "E12": 0.5145,
}

COMBO_VALUES = {
    "E01": 0.1669,
    "E02": 0.1417,
    "E03": 0.0605,
    "E04": 0.0705,
    "E05": 0.3069,
    "E06": 0.1902,
    "E07": 0.2969,
    "E08": 0.3308,
    "E09": 0.1984,
    "E10": 0.3139,
    "E11": 0.4310,
    "E12": 0.4422,
}

METHODS = {
    "E01": "EO-only baseline",
    "E02": "Full grayscale EO",
    "E03": "Box-guided grayscale EO",
    "E04": "Mask-guided grayscale EO",
    "E05": "Joint EO+IR YOLO11s",
    "E06": "IR-only YOLO11s",
    "E07": "Balanced EO+IR YOLO11s",
    "E08": "Joint EO+IR YOLO11l",
    "E09": "IR-only YOLO11l",
    "E10": "E08+E09 ensemble",
    "E11": "Joint EO+IR YOLO11l 960",
    "E12": "Joint EO+IR YOLO11x 960",
}


def configure() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titleweight": "bold",
            "axes.titlesize": 16,
            "axes.labelsize": 12,
            "axes.edgecolor": "#c7d0dd",
            "axes.linewidth": 1.0,
            "xtick.color": "#374151",
            "ytick.color": "#374151",
            "text.color": TEXT,
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
        }
    )


def wrapped(label: str, width: int = 16) -> str:
    return "\n".join(wrap(label, width=width))


def style_axis(ax, y_label: str = "Mask mAP50-95", ymax: float = 0.6) -> None:
    ax.set_ylim(0, ymax)
    ax.set_ylabel(y_label, labelpad=10)
    ax.grid(axis="y", color=GRID, linewidth=1.0, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save(fig, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / name, dpi=260, bbox_inches="tight", pad_inches=0.14)
    fig.savefig(OUT_DIR / name.replace(".png", ".pdf"), bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)


def add_footer(ax, text: str) -> None:
    ax.text(
        0.5,
        -0.22,
        text,
        transform=ax.transAxes,
        ha="center",
        va="top",
        color=MUTED,
        fontsize=10,
    )


def performance_progression() -> None:
    ids = ["E01", "E02", "E05", "E08", "E11", "E12"]
    labels = [
        "E01\nEO-only",
        "E02\nFull gray",
        "E05\nEO+IR\nYOLO11s",
        "E08\nEO+IR\nYOLO11l",
        "E11\nYOLO11l\n960",
        "E12\nYOLO11x\n960",
    ]
    values = [IR_VALUES[i] for i in ids]
    colors = [
        COLORS["eo"],
        COLORS["gray"],
        COLORS["supervised"],
        COLORS["large"],
        COLORS["highres"],
        COLORS["highres2"],
    ]
    x = np.arange(len(ids))

    fig, ax = plt.subplots(figsize=(12.8, 6.7))
    bars = ax.bar(x, values, width=0.64, color=colors, edgecolor=EDGE, linewidth=1.2)
    ax.plot(x, values, color="#263241", marker="o", linewidth=2.4, markersize=6, zorder=4)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    style_axis(ax, ymax=0.62)
    ax.set_title("IR Segmentation Performance Progression", pad=18)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.018,
            f"{value:.4f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    ax.annotate(
        "largest gain\nwith IR supervision",
        xy=(2, values[2]),
        xytext=(1.25, 0.31),
        arrowprops={"arrowstyle": "->", "lw": 1.8, "color": COLORS["supervised"]},
        bbox={"boxstyle": "round,pad=0.35", "fc": "#effaf3", "ec": "#97d4b4"},
        color="#1f6846",
        ha="center",
        fontsize=11,
        fontweight="bold",
    )
    ax.annotate(
        "best strict-mask result",
        xy=(4, values[4]),
        xytext=(4.35, 0.59),
        arrowprops={"arrowstyle": "->", "lw": 1.8, "color": COLORS["highres"]},
        bbox={"boxstyle": "round,pad=0.35", "fc": "#eefbfc", "ec": "#8cd5dc"},
        color="#116b73",
        ha="center",
        fontsize=11,
        fontweight="bold",
    )
    add_footer(
        ax,
        "IR supervision gives the largest jump; 960-resolution YOLO11l gives the strongest IR strict-mask score.",
    )
    fig.tight_layout()
    save(fig, "performance_progression_story.png")


def ranking_chart(values: dict[str, float], title: str, highlight_id: str, filename: str) -> None:
    ordered = sorted(values.items(), key=lambda item: item[1])
    ids = [item[0] for item in ordered]
    vals = [item[1] for item in ordered]
    labels = [f"{exp}\n{wrapped(METHODS[exp], 20)}" for exp in ids]
    colors = []
    for exp in ids:
        if exp == highlight_id:
            colors.append(COLORS["highres"])
        elif exp in {"E01", "E02", "E03", "E04"}:
            colors.append("#a8c4e8")
        elif exp in {"E05", "E06", "E07"}:
            colors.append("#a7d8bd")
        elif exp in {"E08", "E09"}:
            colors.append("#c5b7df")
        elif exp == "E10":
            colors.append("#b8c0cb")
        else:
            colors.append("#8dd9df")

    fig, ax = plt.subplots(figsize=(10.8, 8.2))
    y = np.arange(len(ids))
    bars = ax.barh(y, vals, color=colors, edgecolor=EDGE, linewidth=1.0, height=0.68)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlim(0, 0.58)
    ax.set_xlabel("Mask mAP50-95")
    ax.set_title(title, pad=16)
    ax.grid(axis="x", color=GRID, linewidth=1.0, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for bar, value, exp in zip(bars, vals, ids):
        weight = "bold" if exp == highlight_id else "normal"
        ax.text(value + 0.008, bar.get_y() + bar.get_height() / 2, f"{value:.3f}", va="center", fontweight=weight)
    ax.text(
        values[highlight_id] - 0.005,
        ids.index(highlight_id),
        "  best",
        va="center",
        ha="right",
        color="#073f45",
        fontweight="bold",
    )
    fig.tight_layout()
    save(fig, filename)


def eo_only_comparison() -> None:
    ids = ["E01", "E02", "E03", "E04"]
    vals = [IR_VALUES[i] for i in ids]
    labels = ["EO-only\nbaseline", "Full\nGrayscale", "Box-guided\nGrayscale", "Mask-guided\nGrayscale"]
    colors = [COLORS["eo"], COLORS["gray"], "#d8b04c", "#c79638"]

    fig, ax = plt.subplots(figsize=(11.5, 6.3))
    x = np.arange(len(ids))
    bars = ax.bar(x, vals, color=colors, edgecolor=EDGE, linewidth=1.2, width=0.62)
    style_axis(ax, ymax=0.16)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("EO-only and Grayscale-domain Baselines", pad=16)
    for bar, value in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.006, f"{value:.4f}", ha="center", fontweight="bold")
    ax.text(
        0.5,
        0.83,
        "Color removal alone does not close the EO-to-IR segmentation gap",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#7a4f04",
        bbox={"boxstyle": "round,pad=0.45", "fc": "#fff8e6", "ec": "#e3bd61"},
    )
    add_footer(ax, "All four baselines use EO-only training and are evaluated on IR validation.")
    fig.tight_layout()
    save(fig, "eo_only_augmentation_comparison.png")


def supervision_strategy() -> None:
    ids = ["E01", "E05", "E06", "E07"]
    labels = ["E01\nEO-only", "E05\nEO+IR", "E06\nIR-only", "E07\nBalanced\nEO+IR"]
    ir_vals = [IR_VALUES[i] for i in ids]
    combo_vals = [COMBO_VALUES[i] for i in ids]
    x = np.arange(len(ids))
    width = 0.34

    fig, ax = plt.subplots(figsize=(12, 6.4))
    ax.bar(x - width / 2, ir_vals, width, color=COLORS["ir"], edgecolor=EDGE, label="IR validation")
    ax.bar(x + width / 2, combo_vals, width, color=COLORS["combo"], edgecolor=EDGE, label="EO+IR validation")
    style_axis(ax, ymax=0.50)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Effect of IR Supervision", pad=16)
    ax.legend(frameon=False, loc="upper left")
    for xpos, value in zip(x - width / 2, ir_vals):
        ax.text(xpos, value + 0.012, f"{value:.3f}", ha="center", fontsize=9, fontweight="bold")
    for xpos, value in zip(x + width / 2, combo_vals):
        ax.text(xpos, value + 0.012, f"{value:.3f}", ha="center", fontsize=9, fontweight="bold")
    ax.annotate(
        "real IR labels dominate\ngrayscale-only adaptation",
        xy=(1, ir_vals[1]),
        xytext=(1.55, 0.47),
        arrowprops={"arrowstyle": "->", "lw": 1.8, "color": COLORS["supervised"]},
        bbox={"boxstyle": "round,pad=0.35", "fc": "#effaf3", "ec": "#97d4b4"},
        ha="center",
        color="#1f6846",
        fontweight="bold",
    )
    fig.tight_layout()
    save(fig, "supervision_strategy_comparison.png")


def scale_resolution_ablation() -> None:
    ids = ["E05", "E08", "E11", "E12"]
    labels = ["E05\nYOLO11s\n640", "E08\nYOLO11l\n640", "E11\nYOLO11l\n960", "E12\nYOLO11x\n960"]
    ir_vals = [IR_VALUES[i] for i in ids]
    combo_vals = [COMBO_VALUES[i] for i in ids]
    x = np.arange(len(ids))

    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.plot(x, ir_vals, marker="o", markersize=8, linewidth=3, color=COLORS["ir"], label="IR validation")
    ax.plot(x, combo_vals, marker="o", markersize=8, linewidth=3, color=COLORS["combo"], label="EO+IR validation")
    ax.fill_between(x, ir_vals, color=COLORS["ir"], alpha=0.08)
    ax.fill_between(x, combo_vals, color=COLORS["combo"], alpha=0.08)
    style_axis(ax, ymax=0.58)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Model Scale and Resolution Ablation", pad=16)
    ax.legend(frameon=False, loc="upper left")
    for xpos, value in zip(x, ir_vals):
        ax.text(xpos, value + 0.016, f"{value:.3f}", ha="center", color=COLORS["ir"], fontweight="bold")
    for xpos, value in zip(x, combo_vals):
        ax.text(xpos, value - 0.04, f"{value:.3f}", ha="center", color="#9a5d00", fontweight="bold")
    ax.annotate("best IR strict-mask", xy=(2, ir_vals[2]), xytext=(1.55, 0.555), arrowprops={"arrowstyle": "->", "color": COLORS["ir"], "lw": 1.8})
    ax.annotate("best combined EO+IR", xy=(3, combo_vals[3]), xytext=(2.72, 0.30), arrowprops={"arrowstyle": "->", "color": COLORS["combo"], "lw": 1.8})
    fig.tight_layout()
    save(fig, "scale_resolution_ablation.png")


def ensemble_ablation() -> None:
    ids = ["E08", "E09", "E10", "E11"]
    vals = [IR_VALUES[i] for i in ids]
    labels = [
        "E08\nEO+IR\nYOLO11l",
        "E09\nIR-only\nYOLO11l",
        "E10\nMask-aware\nensemble",
        "E11\nEO+IR\nYOLO11l 960",
    ]
    colors = [COLORS["large"], "#987bc1", COLORS["ensemble"], COLORS["highres"]]

    fig, ax = plt.subplots(figsize=(11.6, 6.2))
    x = np.arange(len(ids))
    bars = ax.bar(x, vals, color=colors, edgecolor=EDGE, linewidth=1.2, width=0.62)
    style_axis(ax, ymax=0.58)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Ensemble Ablation", pad=16)
    for bar, value in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.014, f"{value:.4f}", ha="center", fontweight="bold")
    ax.text(
        0.5,
        0.90,
        "E10 matches E08 at 640 resolution, but E11 remains clearly stronger.",
        transform=ax.transAxes,
        ha="center",
        va="center",
        bbox={"boxstyle": "round,pad=0.38", "fc": "#f2f5f9", "ec": "#c7d0dd"},
        fontsize=10.5,
        fontweight="bold",
    )
    fig.tight_layout()
    save(fig, "ensemble_ablation.png")


def final_recommendation() -> None:
    fig, ax = plt.subplots(figsize=(12.5, 6.6))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.text(6.25, 6.15, "Final Model Recommendation", ha="center", fontsize=22, fontweight="bold")
    ax.text(6.25, 5.75, "Model choice depends on the validation objective", ha="center", fontsize=12, color=MUTED)

    def card(x: float, title: str, exp: str, model: str, metric_label: str, value: str, face: str) -> None:
        patch = FancyBboxPatch(
            (x, 1.4),
            5.25,
            3.75,
            boxstyle="round,pad=0.04,rounding_size=0.16",
            linewidth=1.8,
            edgecolor=EDGE,
            facecolor=face,
        )
        ax.add_patch(patch)
        ax.text(x + 2.625, 4.58, title, ha="center", va="center", fontsize=15, fontweight="bold")
        ax.text(x + 2.625, 3.82, exp, ha="center", va="center", fontsize=30, fontweight="bold", color="#0f5961")
        ax.text(x + 2.625, 3.22, model, ha="center", va="center", fontsize=13)
        ax.text(x + 2.625, 2.55, "EO+IR training, image size 960", ha="center", va="center", fontsize=11, color=MUTED)
        ax.text(x + 2.625, 1.96, metric_label, ha="center", va="center", fontsize=11, color=MUTED)
        ax.text(x + 2.625, 1.62, value, ha="center", va="center", fontsize=18, fontweight="bold")

    card(0.7, "Best primary IR model", "E11", "YOLO11l-seg", "IR mask mAP50-95", "0.5250", COLORS["soft_teal"])
    card(6.55, "Best combined EO+IR model", "E12", "YOLO11x-seg", "EO+IR mask mAP50-95", "0.4422", COLORS["soft_blue"])
    ax.text(
        6.25,
        0.65,
        "E11 is preferred for strict IR segmentation; E12 is preferred for combined-modality robustness.",
        ha="center",
        fontsize=12,
        color=TEXT,
        bbox={"boxstyle": "round,pad=0.45", "fc": PANEL, "ec": "#d5dde8"},
    )
    fig.tight_layout()
    save(fig, "final_model_recommendation.png")


def main() -> None:
    configure()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    performance_progression()
    ranking_chart(IR_VALUES, "IR-only Validation: Mask mAP50-95 Ranking", "E11", "ir_results_ranking.png")
    ranking_chart(COMBO_VALUES, "Combined EO+IR Validation: Mask mAP50-95 Ranking", "E12", "combined_results_ranking.png")
    eo_only_comparison()
    supervision_strategy()
    scale_resolution_ablation()
    ensemble_ablation()
    final_recommendation()
    print(f"Wrote Chapter 5 figures to {OUT_DIR}")


if __name__ == "__main__":
    main()
