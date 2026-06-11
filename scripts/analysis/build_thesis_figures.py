"""Generate thesis-ready figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "thesis" / "Figures" / "Chapter3"


def add_box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    face: str,
    edge: str = "#334155",
    fontsize: int = 10,
    weight: str = "bold",
    rounding: float = 0.12,
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.03,rounding_size={rounding}",
        linewidth=1.6,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=weight,
        color="#0f172a",
    )


def add_arrow(ax, start: tuple[float, float], end: tuple[float, float], rad: float = 0.0) -> None:
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 1.8,
            "color": "#475569",
            "mutation_scale": 14,
            "connectionstyle": f"arc3,rad={rad}",
        },
    )


def save_proposed_workflow() -> None:
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    fig.patch.set_facecolor("#f8fafc")
    ax.set_facecolor("#f8fafc")

    ax.text(
        7,
        7.62,
        "Proposed Workflow for EO/IR Aerial Image Segmentation",
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="#0f172a",
    )
    ax.text(
        7,
        7.25,
        "Controlled YOLO-Seg experiments across modality, scale, resolution, and ensemble axes",
        ha="center",
        va="center",
        fontsize=11,
        color="#475569",
    )

    # Input and preparation path.
    add_box(ax, 0.55, 5.75, 2.25, 1.05, "IndraEye\nEO + IR Dataset", "#dbeafe", fontsize=10)
    add_box(ax, 3.35, 5.75, 2.25, 1.05, "Data Validation\nClass Mapping\nYOLO Labels", "#e0f2fe", fontsize=9)
    add_box(ax, 6.15, 5.75, 2.25, 1.05, "Dataset YAMLs\nTrain/Val Splits\nRun Configs", "#ccfbf1", fontsize=9)

    add_arrow(ax, (2.8, 6.28), (3.35, 6.28))
    add_arrow(ax, (5.6, 6.28), (6.15, 6.28))

    # Experiment groups.
    add_box(ax, 0.65, 3.95, 2.55, 1.15, "EO-only Transfer\nE01", "#fef3c7", fontsize=10)
    add_box(ax, 3.65, 3.95, 2.55, 1.15, "Grayscale Domain\nTransforms\nE02-E04", "#fde68a", fontsize=9)
    add_box(ax, 6.65, 3.95, 2.55, 1.15, "IR Supervision\nEO+IR / IR / Balanced\nE05-E07", "#dcfce7", fontsize=9)
    add_box(ax, 9.65, 3.95, 2.55, 1.15, "Scale + Resolution\nEnsemble Study\nE08-E12", "#ede9fe", fontsize=9)

    add_arrow(ax, (7.28, 5.75), (1.92, 5.1), rad=0.08)
    add_arrow(ax, (7.28, 5.75), (4.92, 5.1), rad=0.04)
    add_arrow(ax, (7.28, 5.75), (7.92, 5.1), rad=-0.04)
    add_arrow(ax, (7.28, 5.75), (10.92, 5.1), rad=-0.08)

    # Training and evaluation.
    add_box(ax, 4.45, 2.45, 5.1, 0.95, "YOLO11 Segmentation Training\npretrained weights, consistent labels, tracked runs", "#ffffff", fontsize=10)
    add_arrow(ax, (1.92, 3.95), (4.75, 3.4), rad=-0.05)
    add_arrow(ax, (4.92, 3.95), (5.75, 3.4), rad=-0.03)
    add_arrow(ax, (7.92, 3.95), (7.6, 3.4), rad=0.02)
    add_arrow(ax, (10.92, 3.95), (9.25, 3.4), rad=0.05)

    add_box(ax, 2.05, 1.25, 3.05, 0.95, "Primary Evaluation\nIR validation\nmask mAP50-95", "#fee2e2", fontsize=9)
    add_box(ax, 5.5, 1.25, 3.05, 0.95, "Secondary Evaluation\nEO+IR validation\nrobustness", "#ffedd5", fontsize=9)
    add_box(ax, 8.95, 1.25, 3.05, 0.95, "Consolidated Analysis\nCSV/JSON tables\nmodel comparison", "#e2e8f0", fontsize=9)

    add_arrow(ax, (5.7, 2.45), (3.58, 2.2), rad=0.05)
    add_arrow(ax, (7.0, 2.45), (7.02, 2.2), rad=0.0)
    add_arrow(ax, (8.3, 2.45), (10.48, 2.2), rad=-0.05)

    # Final outcome band.
    add_box(
        ax,
        3.1,
        0.25,
        7.8,
        0.68,
        "Outcome: select strongest IR and combined EO+IR models using controlled evidence",
        "#f0fdf4",
        fontsize=9,
    )
    add_arrow(ax, (3.58, 1.25), (5.25, 0.93), rad=-0.05)
    add_arrow(ax, (7.02, 1.25), (7.0, 0.93), rad=0.0)
    add_arrow(ax, (10.48, 1.25), (8.78, 0.93), rad=0.05)

    fig.tight_layout(pad=0.4)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / "proposed_workflow.png", dpi=220)
    fig.savefig(OUT_DIR / "proposed_workflow.pdf")
    plt.close(fig)


def main() -> None:
    save_proposed_workflow()
    print(f"Wrote thesis figures to {OUT_DIR}")


if __name__ == "__main__":
    main()
