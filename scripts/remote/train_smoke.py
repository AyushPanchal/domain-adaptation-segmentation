#!/usr/bin/env python
"""Run one YOLO segmentation smoke experiment from Python.

Environment defaults mirror the old shell wrapper:
  EXPERIMENT_CONFIG, OUTPUT_ROOT, YOLO_DEVICE, YOLO_EPOCHS, YOLO_BATCH,
  YOLO_WORKERS, YOLO_PATIENCE.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[2]


REPO_ROOT = repo_root_from_script()
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from domain_adaptation_segmentation.training.collect_results import collect_results
from domain_adaptation_segmentation.training.run_experiment import run_experiment


def env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    return default if value in (None, "") else int(value)


def env_str(name: str, default: str) -> str:
    return os.environ.get(name) or default


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            env_str("EXPERIMENT_CONFIG", "configs/experiments/e01_source_rgb_yolo11s.yaml")
        ),
        help="Experiment YAML to run.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(env_str("REPO_ROOT", str(REPO_ROOT))),
        help="Repository root. Defaults to this script's repository.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path(env_str("OUTPUT_ROOT", str(REPO_ROOT / "runs"))),
        help="Root directory for experiment outputs.",
    )
    parser.add_argument("--device", default=env_str("YOLO_DEVICE", "0"))
    parser.add_argument("--epochs", type=int, default=env_int("YOLO_EPOCHS", 1))
    parser.add_argument("--batch", default=env_str("YOLO_BATCH", "8"))
    parser.add_argument("--workers", type=int, default=env_int("YOLO_WORKERS", 4))
    parser.add_argument("--patience", type=int, default=env_int("YOLO_PATIENCE", 5))
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=Path("reports/tables"),
        help="Directory for summary_results.csv/json.",
    )
    parser.add_argument("--no-collect", action="store_true", help="Skip summary table refresh.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    output_root = args.output_root.resolve()
    config_path = args.config if args.config.is_absolute() else repo_root / args.config

    print("[PY SMOKE] config:", config_path)
    print("[PY SMOKE] epochs:", args.epochs)
    print("[PY SMOKE] batch:", args.batch)
    print("[PY SMOKE] workers:", args.workers)
    print("[PY SMOKE] patience:", args.patience)
    print("[PY SMOKE] device:", args.device)

    return_code = run_experiment(
        config_path=config_path,
        repo_root=repo_root,
        output_root=output_root,
        device=args.device,
        epochs_override=args.epochs,
        batch_override=args.batch,
        workers=args.workers,
        patience=args.patience,
        dry_run=args.dry_run,
    )

    if return_code == 0 and not args.no_collect and not args.dry_run:
        collect_results(output_root, repo_root / args.reports_dir)
        print("[PY SMOKE] summary tables refreshed")

    print("[PY SMOKE] done")
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
