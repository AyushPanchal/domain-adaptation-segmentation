#!/usr/bin/env python
"""Run the full E01-E06 YOLO11s experiment queue from Python.

Environment defaults:
  OUTPUT_ROOT, YOLO_DEVICE, YOLO_EPOCHS, YOLO_BATCH, YOLO_WORKERS,
  YOLO_PATIENCE.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


CONFIGS = [
    "configs/experiments/e01_source_rgb_yolo11s.yaml",
    "configs/experiments/e02_full_gray_yolo11s.yaml",
    "configs/experiments/e03_box_guided_gray_yolo11s.yaml",
    "configs/experiments/e04_mga_yolo11s.yaml",
    "configs/experiments/e05_ba_mga_yolo11s.yaml",
    "configs/experiments/e06_ir_oracle_yolo11s.yaml",
]


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


def env_optional_int(name: str) -> int | None:
    value = os.environ.get(name)
    return None if value in (None, "") else int(value)


def env_str(name: str, default: str) -> str:
    return os.environ.get(name) or default


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--configs",
        nargs="+",
        type=Path,
        default=[Path(config) for config in CONFIGS],
        help="Experiment YAMLs to run in order.",
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
    parser.add_argument(
        "--epochs",
        type=int,
        default=env_optional_int("YOLO_EPOCHS"),
        help="Epoch override. Defaults to each experiment YAML.",
    )
    parser.add_argument("--batch", default=env_str("YOLO_BATCH", "2"))
    parser.add_argument("--workers", type=int, default=env_int("YOLO_WORKERS", 2))
    parser.add_argument("--patience", type=int, default=env_int("YOLO_PATIENCE", 0))
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=Path("reports/tables"),
        help="Directory for summary_results.csv/json.",
    )
    parser.add_argument(
        "--keep-going",
        action="store_true",
        help="Continue with later configs if one experiment fails.",
    )
    parser.add_argument("--no-collect", action="store_true", help="Skip summary table refresh.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def resolve_config(repo_root: Path, config: Path) -> Path:
    return config if config.is_absolute() else repo_root / config


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    output_root = args.output_root.resolve()
    failures: list[tuple[Path, int]] = []

    print("[PY TRAIN] experiments:", len(args.configs))
    print("[PY TRAIN] epochs:", args.epochs if args.epochs is not None else "config default")
    print("[PY TRAIN] batch:", args.batch)
    print("[PY TRAIN] workers:", args.workers)
    print("[PY TRAIN] patience:", args.patience)
    print("[PY TRAIN] device:", args.device)

    for index, config in enumerate(args.configs, start=1):
        config_path = resolve_config(repo_root, config)
        print(f"[PY TRAIN] starting {index}/{len(args.configs)}: {config_path}")

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

        if return_code != 0:
            failures.append((config_path, return_code))
            print(f"[PY TRAIN] failed {config_path} with return code {return_code}")
            if not args.keep_going:
                break

        if not args.no_collect and not args.dry_run:
            collect_results(output_root, repo_root / args.reports_dir)

    if failures:
        print("[PY TRAIN] failures:")
        for config_path, return_code in failures:
            print(f"  {config_path}: {return_code}")
        return failures[0][1]

    if not args.no_collect and not args.dry_run:
        collect_results(output_root, repo_root / args.reports_dir)
        print("[PY TRAIN] summary tables refreshed")

    print("[PY TRAIN] E01-E06 queue complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
