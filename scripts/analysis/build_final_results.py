"""Build final paper/dissertation result tables from downloaded experiment artifacts."""

from __future__ import annotations

import csv
import json
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DOWNLOADS = ROOT / "downloads"
REPORT_DIR = ROOT / "reports" / "final"
TABLE_DIR = REPORT_DIR / "tables"
FIGURE_DIR = REPORT_DIR / "figures"


EXPERIMENTS = [
    {
        "id": "E01",
        "method": "EO-only baseline",
        "model": "YOLO11s-seg",
        "train": "EO",
        "zip": "e01_bestpt_evaluations.zip",
        "eval_aliases": {"eval_ir": "eval_ir_debug"},
    },
    {
        "id": "E02",
        "method": "Full grayscale EO",
        "model": "YOLO11s-seg",
        "train": "EO-gray",
        "zip": "full_e02_results.zip",
    },
    {
        "id": "E03",
        "method": "Box-guided grayscale EO",
        "model": "YOLO11s-seg",
        "train": "EO box-gray",
        "zip": "full_e03_results.zip",
    },
    {
        "id": "E04",
        "method": "Mask-guided grayscale EO",
        "model": "YOLO11s-seg",
        "train": "EO mask-gray",
        "zip": "full_e04_results.zip",
    },
    {
        "id": "E09",
        "method": "Joint EO+IR",
        "model": "YOLO11s-seg",
        "train": "EO+IR",
        "zip": "full_e09_results.zip",
    },
    {
        "id": "N1",
        "method": "IR-only supervised",
        "model": "YOLO11s-seg",
        "train": "IR",
        "zip": "full_n1_results.zip",
    },
    {
        "id": "N2",
        "method": "Balanced EO+IR",
        "model": "YOLO11s-seg",
        "train": "EO+IR balanced",
        "zip": "full_n2_results.zip",
    },
    {
        "id": "N3",
        "method": "Joint EO+IR large",
        "model": "YOLO11l-seg",
        "train": "EO+IR",
        "zip": "full_n3_results.zip",
    },
    {
        "id": "N4",
        "method": "IR-only large",
        "model": "YOLO11l-seg",
        "train": "IR",
        "zip": "full_n4_results.zip",
    },
    {
        "id": "N6",
        "method": "N3+N4 mask-aware ensemble",
        "model": "2x YOLO11l-seg",
        "train": "EO+IR + IR",
        "zip": "n6_n3_n4_ensemble_results.zip",
    },
    {
        "id": "N7",
        "method": "Joint EO+IR high-res",
        "model": "YOLO11l-seg",
        "train": "EO+IR",
        "zip": "full_n7_results.zip",
    },
    {
        "id": "N8",
        "method": "Joint EO+IR high-res XL",
        "model": "YOLO11x-seg",
        "train": "EO+IR",
        "zip": "full_n8_results.zip",
        "manual_metrics": {
            "eval_ir": {
                "metrics/mAP50(B)": 0.7204501325873608,
                "metrics/mAP50-95(B)": 0.6091304423510924,
                "metrics/mAP50(M)": 0.7040857021798551,
                "metrics/mAP50-95(M)": 0.5145016775507094,
            },
            "eval_eo_ir": {
                "metrics/mAP50(B)": 0.6632091284242422,
                "metrics/mAP50-95(B)": 0.5455120796059331,
                "metrics/mAP50(M)": 0.6462590517563528,
                "metrics/mAP50-95(M)": 0.4421922340208558,
            },
        },
        "manual_note": "full_n8_results.zip was readable via Windows tar but not Python zipfile; metrics were extracted from packaged metrics.json.",
    },
]


METRIC_KEYS = [
    "metrics/mAP50(B)",
    "metrics/mAP50-95(B)",
    "metrics/mAP50(M)",
    "metrics/mAP50-95(M)",
]


def metric_short_name(key: str) -> str:
    return {
        "metrics/mAP50(B)": "box_mAP50",
        "metrics/mAP50-95(B)": "box_mAP50_95",
        "metrics/mAP50(M)": "mask_mAP50",
        "metrics/mAP50-95(M)": "mask_mAP50_95",
    }[key]


def read_metrics_from_zip(zip_path: Path, eval_name: str) -> dict[str, float] | None:
    if not zip_path.exists():
        return None
    try:
        with zipfile.ZipFile(zip_path) as archive:
            candidates = [
                name
                for name in archive.namelist()
                if name.endswith(f"evaluations/{eval_name}/metrics.json")
                or name.endswith(f"{eval_name}/metrics.json")
            ]
            if not candidates:
                return None
            payload = json.loads(archive.read(candidates[0]).decode("utf-8"))
            return payload.get("metrics", {})
    except zipfile.BadZipFile:
        return None


def build_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for exp in EXPERIMENTS:
        zip_path = DOWNLOADS / str(exp["zip"])
        manual = exp.get("manual_metrics", {})
        for eval_name in ["eval_ir", "eval_eo_ir"]:
            artifact_eval_name = exp.get("eval_aliases", {}).get(eval_name, eval_name)
            metrics = read_metrics_from_zip(zip_path, artifact_eval_name)
            source = "zip"
            if metrics is None:
                metrics = manual.get(eval_name)
                source = "manual"
            if metrics is None:
                continue
            row: dict[str, Any] = {
                "id": exp["id"],
                "method": exp["method"],
                "model": exp["model"],
                "train": exp["train"],
                "eval": eval_name,
                "source": source,
            }
            for key in METRIC_KEYS:
                row[metric_short_name(key)] = float(metrics[key])
            rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def select_main_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    main_ids = {"N3", "N6", "N7", "N8"}
    return [row for row in rows if row["id"] in main_ids]


def write_markdown(rows: list[dict[str, Any]], main_rows: list[dict[str, Any]]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / "final_results_summary.md"

    def table(selected: list[dict[str, Any]]) -> str:
        headers = [
            "ID",
            "Method",
            "Model",
            "Eval",
            "Mask mAP50",
            "Mask mAP50-95",
            "Box mAP50",
            "Box mAP50-95",
        ]
        lines = ["| " + " | ".join(headers) + " |"]
        lines.append("|" + "|".join(["---"] * len(headers)) + "|")
        for row in selected:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row["id"]),
                        str(row["method"]),
                        str(row["model"]),
                        str(row["eval"]),
                        f"{row['mask_mAP50']:.4f}",
                        f"{row['mask_mAP50_95']:.4f}",
                        f"{row['box_mAP50']:.4f}",
                        f"{row['box_mAP50_95']:.4f}",
                    ]
                )
                + " |"
            )
        return "\n".join(lines)

    n7_ir = next(row for row in rows if row["id"] == "N7" and row["eval"] == "eval_ir")
    n8_ir = next(row for row in rows if row["id"] == "N8" and row["eval"] == "eval_ir")
    n7_combo = next(row for row in rows if row["id"] == "N7" and row["eval"] == "eval_eo_ir")
    n8_combo = next(row for row in rows if row["id"] == "N8" and row["eval"] == "eval_eo_ir")

    text = f"""# Final Results Summary

Generated from downloaded experiment artifacts under `downloads/`.

## Main Comparison

{table(main_rows)}

## Interpretation

- **Primary IR evaluation:** N7 remains the best strict-mask model with IR mask mAP50-95 `{n7_ir['mask_mAP50_95']:.4f}` versus N8 `{n8_ir['mask_mAP50_95']:.4f}`.
- **Combined EO+IR evaluation:** N8 is strongest with mask mAP50-95 `{n8_combo['mask_mAP50_95']:.4f}` versus N7 `{n7_combo['mask_mAP50_95']:.4f}`.
- **Scaling result:** moving from YOLO11l 640 (N3) to YOLO11l 960 (N7) gives the cleanest primary IR gain. Moving from YOLO11l 960 (N7) to YOLO11x 960 (N8) helps combined EO+IR but does not replace N7 on the primary IR metric.
- **Ensemble result:** the N3+N4 ensemble (N6) is useful as an ablation, but does not beat high-resolution joint training.

## Full Table

{table(rows)}

## Files

- `reports/final/tables/final_metrics_long.csv`
- `reports/final/tables/main_comparison.csv`
- `reports/final/figures/mask_map50_95_eval_ir.png`
- `reports/final/figures/mask_map50_95_eval_eo_ir.png`
"""
    path.write_text(text, encoding="utf-8")


def write_plots(rows: list[dict[str, Any]]) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover - environment dependent
        print(f"Skipping plots because matplotlib is unavailable: {exc}")
        return

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    for eval_name in ["eval_ir", "eval_eo_ir"]:
        selected = [row for row in rows if row["eval"] == eval_name]
        labels = [str(row["id"]) for row in selected]
        values = [float(row["mask_mAP50_95"]) for row in selected]
        colors = ["#6b7280"] * len(values)
        for idx, row in enumerate(selected):
            if row["id"] == "N7":
                colors[idx] = "#2563eb"
            elif row["id"] == "N8":
                colors[idx] = "#dc2626"

        fig, ax = plt.subplots(figsize=(10, 4.8))
        ax.bar(labels, values, color=colors)
        ax.set_title(f"Mask mAP50-95 on {eval_name}")
        ax.set_xlabel("Experiment")
        ax.set_ylabel("Mask mAP50-95")
        ax.set_ylim(0, max(values) * 1.18)
        ax.grid(axis="y", alpha=0.25)
        for i, value in enumerate(values):
            ax.text(i, value + 0.01, f"{value:.3f}", ha="center", va="bottom", fontsize=8)
        fig.tight_layout()
        fig.savefig(FIGURE_DIR / f"mask_map50_95_{eval_name}.png", dpi=180)
        plt.close(fig)


def main() -> None:
    rows = build_rows()
    rows.sort(key=lambda row: (row["eval"], row["id"]))
    main_rows = select_main_rows(rows)
    write_csv(TABLE_DIR / "final_metrics_long.csv", rows)
    write_csv(TABLE_DIR / "main_comparison.csv", main_rows)
    write_markdown(rows, main_rows)
    write_plots(rows)
    print(f"Wrote {len(rows)} metric rows to {TABLE_DIR}")


if __name__ == "__main__":
    main()
