"""Collect YOLO run summaries into CSV/JSON tables."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import pandas as pd


def latest_metrics(results_csv: Path) -> dict[str, float | int | str]:
    df = pd.read_csv(results_csv)
    df.columns = [column.strip() for column in df.columns]
    last = df.iloc[-1].to_dict()
    return {key: (value.item() if hasattr(value, "item") else value) for key, value in last.items()}


def collect_results(runs_root: Path, output_dir: Path) -> None:
    rows: list[dict[str, object]] = []
    for status_path in sorted(runs_root.glob("experiments/*/status.json")):
        status = json.loads(status_path.read_text(encoding="utf-8"))
        run_dir = status_path.parent
        row: dict[str, object] = {
            "experiment_id": status.get("experiment_id"),
            "name": status.get("name"),
            "status": status.get("status"),
            "device": status.get("device"),
            "elapsed_seconds": status.get("elapsed_seconds"),
            "run_dir": str(run_dir),
        }
        results_csv = run_dir / "results.csv"
        if results_csv.exists():
            metrics = latest_metrics(results_csv)
            row.update(metrics)
            (run_dir / "metrics.json").write_text(
                json.dumps(metrics, indent=2), encoding="utf-8"
            )
        rows.append(row)

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "summary_results.json"
    csv_path = output_dir / "summary_results.csv"
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    if rows:
        fieldnames = sorted({key for row in rows for key in row})
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        csv_path.write_text("", encoding="utf-8")

    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-root", type=Path, default=Path("runs"))
    parser.add_argument("--output-dir", type=Path, default=Path("reports/tables"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    collect_results(args.runs_root, args.output_dir)


if __name__ == "__main__":
    main()

