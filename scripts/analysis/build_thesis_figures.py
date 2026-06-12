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
    fig, ax = plt.subplots(figsize=(8.2, 10.4))
    ax.set_xlim(0, 8.2)
    ax.set_ylim(0, 10.4)
    ax.axis("off")

    fig.patch.set_facecolor("#f8fafc")
    ax.set_facecolor("#f8fafc")

    ax.text(
        4.1,
        10.05,
        "Proposed Workflow for EO/IR Aerial Image Segmentation",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="#0f172a",
    )
    ax.text(
        4.1,
        9.72,
        "Controlled YOLO-Seg experiments across modality, scale, resolution, and ensemble axes",
        ha="center",
        va="center",
        fontsize=8.5,
        color="#475569",
    )

    # Input and preparation path.
    add_box(ax, 0.35, 8.65, 2.05, 0.78, "IndraEye\nEO + IR Dataset", "#dbeafe", fontsize=8.8)
    add_box(ax, 3.08, 8.65, 2.05, 0.78, "Data Validation\nClass Mapping\nYOLO Labels", "#e0f2fe", fontsize=8.0)
    add_box(ax, 5.8, 8.65, 2.05, 0.78, "Dataset YAMLs\nTrain/Val Splits\nRun Configs", "#ccfbf1", fontsize=8.0)

    add_arrow(ax, (2.4, 9.04), (3.08, 9.04))
    add_arrow(ax, (5.13, 9.04), (5.8, 9.04))
    add_arrow(ax, (6.82, 8.65), (4.1, 8.18), rad=-0.08)

    # Experiment matrix.
    add_box(ax, 1.1, 7.55, 6.0, 0.58, "Controlled Experiment Matrix", "#ffffff", fontsize=9.0)
    add_arrow(ax, (4.1, 7.55), (4.1, 7.28))

    add_box(ax, 0.8, 6.67, 6.6, 0.58, "EO-only transfer baseline: E01", "#fef3c7", fontsize=8.8)
    add_box(ax, 0.8, 5.86, 6.6, 0.58, "Grayscale-domain transformations: E02-E04", "#fde68a", fontsize=8.5)
    add_box(ax, 0.8, 5.05, 6.6, 0.58, "IR and mixed-domain supervision: E05-E07", "#dcfce7", fontsize=8.5)
    add_box(ax, 0.8, 4.24, 6.6, 0.58, "Model scale, resolution, and ensemble study: E08-E12", "#ede9fe", fontsize=8.2)

    add_arrow(ax, (4.1, 6.67), (4.1, 6.44))
    add_arrow(ax, (4.1, 5.86), (4.1, 5.63))
    add_arrow(ax, (4.1, 5.05), (4.1, 4.82))
    add_arrow(ax, (4.1, 4.24), (4.1, 3.9))

    # Training and evaluation.
    add_box(
        ax,
        1.35,
        3.18,
        5.5,
        0.72,
        "YOLO11 Segmentation Training\npretrained weights, consistent labels, tracked runs",
        "#ffffff",
        fontsize=8.6,
    )
    add_arrow(ax, (4.1, 3.18), (4.1, 2.82))

    add_box(ax, 0.25, 2.0, 2.35, 0.72, "Primary Evaluation\nIR validation\nmask mAP50-95", "#fee2e2", fontsize=7.5)
    add_box(ax, 2.93, 2.0, 2.35, 0.72, "Secondary Evaluation\nEO+IR validation\nrobustness", "#ffedd5", fontsize=7.5)
    add_box(ax, 5.6, 2.0, 2.35, 0.72, "Consolidated Analysis\nCSV/JSON tables\nmodel comparison", "#e2e8f0", fontsize=7.5)

    add_arrow(ax, (4.1, 2.82), (1.42, 2.72), rad=0.10)
    add_arrow(ax, (4.1, 2.82), (4.1, 2.72), rad=0.0)
    add_arrow(ax, (4.1, 2.82), (6.78, 2.72), rad=-0.10)

    # Final outcome band.
    add_box(
        ax,
        0.75,
        0.95,
        6.7,
        0.68,
        "Outcome: select strongest IR and combined EO+IR models using controlled evidence",
        "#f0fdf4",
        fontsize=8.0,
    )
    add_arrow(ax, (1.42, 2.0), (2.45, 1.63), rad=-0.05)
    add_arrow(ax, (4.1, 2.0), (4.1, 1.63), rad=0.0)
    add_arrow(ax, (6.78, 2.0), (5.75, 1.63), rad=0.05)

    fig.tight_layout(pad=0.15)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / "proposed_workflow.png", dpi=260, bbox_inches="tight", pad_inches=0.08)
    fig.savefig(OUT_DIR / "proposed_workflow.pdf", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def main() -> None:
    save_proposed_workflow()
    print(f"Wrote thesis figures to {OUT_DIR}")


if __name__ == "__main__":
    main()
