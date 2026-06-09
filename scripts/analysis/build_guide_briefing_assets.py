"""Generate guide-briefing visuals from final experiment metrics."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
METRICS_CSV = ROOT / "reports" / "final" / "tables" / "final_metrics_long.csv"
OUT_DIR = ROOT / "reports" / "guide_briefing" / "assets"


def load_rows() -> list[dict[str, str]]:
    with METRICS_CSV.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def get_metric(rows: list[dict[str, str]], exp_id: str, eval_name: str, metric: str) -> float:
    for row in rows:
        if row["id"] == exp_id and row["eval"] == eval_name:
            return float(row[metric])
    raise KeyError((exp_id, eval_name, metric))


def save_progression(rows: list[dict[str, str]]) -> None:
    ids = ["E01", "E09", "N3", "N7", "N8"]
    labels = [
        "EO only\nYOLO11s",
        "EO+IR\nYOLO11s",
        "EO+IR\nYOLO11l 640",
        "EO+IR\nYOLO11l 960",
        "EO+IR\nYOLO11x 960",
    ]
    ir_values = [get_metric(rows, exp_id, "eval_ir", "mask_mAP50_95") for exp_id in ids]
    combo_values = [get_metric(rows, exp_id, "eval_eo_ir", "mask_mAP50_95") for exp_id in ids]
    x = np.arange(len(ids))

    fig, ax = plt.subplots(figsize=(11, 5.6))
    ax.plot(x, ir_values, marker="o", linewidth=3, color="#2563eb", label="IR validation")
    ax.plot(x, combo_values, marker="o", linewidth=3, color="#dc2626", label="EO+IR validation")
    ax.fill_between(x, ir_values, alpha=0.08, color="#2563eb")
    ax.fill_between(x, combo_values, alpha=0.08, color="#dc2626")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Mask mAP50-95")
    ax.set_title("Performance Progression Across the Experiment Plan")
    ax.set_ylim(0, 0.6)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, loc="upper left")
    for idx, value in enumerate(ir_values):
        ax.text(idx, value + 0.018, f"{value:.3f}", ha="center", fontsize=9, color="#1d4ed8")
    for idx, value in enumerate(combo_values):
        ax.text(idx, value - 0.04, f"{value:.3f}", ha="center", fontsize=9, color="#b91c1c")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "performance_progression.png", dpi=180)
    plt.close(fig)


def save_heatmap(rows: list[dict[str, str]]) -> None:
    ids = ["N3", "N6", "N7", "N8"]
    cols = [
        ("IR\nMask 50", "eval_ir", "mask_mAP50"),
        ("IR\nMask 50-95", "eval_ir", "mask_mAP50_95"),
        ("IR\nBox 50-95", "eval_ir", "box_mAP50_95"),
        ("EO+IR\nMask 50", "eval_eo_ir", "mask_mAP50"),
        ("EO+IR\nMask 50-95", "eval_eo_ir", "mask_mAP50_95"),
        ("EO+IR\nBox 50-95", "eval_eo_ir", "box_mAP50_95"),
    ]
    data = np.array([[get_metric(rows, exp_id, eval_name, metric) for _, eval_name, metric in cols] for exp_id in ids])

    fig, ax = plt.subplots(figsize=(10.8, 4.7))
    im = ax.imshow(data, cmap="YlGnBu", vmin=0.30, vmax=0.75)
    ax.set_xticks(np.arange(len(cols)))
    ax.set_xticklabels([col[0] for col in cols])
    ax.set_yticks(np.arange(len(ids)))
    ax.set_yticklabels(ids)
    ax.set_title("Main Model Comparison Heatmap")
    for row_idx in range(data.shape[0]):
        for col_idx in range(data.shape[1]):
            val = data[row_idx, col_idx]
            ax.text(col_idx, row_idx, f"{val:.3f}", ha="center", va="center", fontsize=9)
    fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02, label="Metric value")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "main_comparison_heatmap.png", dpi=180)
    plt.close(fig)


def save_experiment_map() -> None:
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)

    boxes = [
        (0.6, 5.7, 2.2, 1.0, "Problem\nEO to IR masks", "#e0f2fe"),
        (3.4, 6.2, 2.2, 0.9, "EO-only\nE01-E04", "#fef3c7"),
        (3.4, 4.8, 2.2, 0.9, "IR supervision\nE09, N1, N2", "#dcfce7"),
        (6.2, 5.7, 2.2, 1.0, "Model scale\nN3, N4", "#ede9fe"),
        (8.9, 6.2, 2.2, 0.9, "Ensemble\nN6", "#fee2e2"),
        (8.9, 4.8, 2.2, 0.9, "High resolution\nN7, N8", "#dbeafe"),
        (4.8, 2.0, 2.6, 1.05, "Final story\nN7 primary IR\nN8 combined EO+IR", "#f0fdf4"),
    ]
    for x, y, w, h, text, color in boxes:
        patch = plt.Rectangle((x, y), w, h, facecolor=color, edgecolor="#334155", linewidth=1.6)
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=11, weight="bold")

    arrows = [
        ((2.8, 6.2), (3.4, 6.65)),
        ((2.8, 6.2), (3.4, 5.25)),
        ((5.6, 5.25), (6.2, 6.2)),
        ((8.4, 6.2), (8.9, 6.65)),
        ((8.4, 6.2), (8.9, 5.25)),
        ((10.0, 4.8), (6.1, 3.05)),
        ((10.0, 6.2), (6.1, 3.05)),
    ]
    for start, end in arrows:
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops={"arrowstyle": "->", "lw": 1.8, "color": "#475569"},
        )

    ax.text(
        0.6,
        0.7,
        "Design principle: isolate one axis at a time: domain supervision, model scale, resolution, and ensembling.",
        fontsize=11,
        color="#334155",
    )
    ax.set_title("Structured Experiment Design", fontsize=16, weight="bold", pad=12)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "experiment_design_map.png", dpi=180)
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    save_progression(rows)
    save_heatmap(rows)
    save_experiment_map()
    print(f"Wrote guide briefing assets to {OUT_DIR}")


if __name__ == "__main__":
    main()
