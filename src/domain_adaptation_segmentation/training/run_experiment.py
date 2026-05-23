"""Run one YOLO segmentation experiment with durable logs and status files."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def resolve_path(path: str, repo_root: Path) -> Path:
    expanded = os.path.expandvars(path)
    candidate = Path(expanded)
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    return candidate.resolve()


def build_yolo_command(
    config: dict[str, Any],
    dataset_path: Path,
    run_dir: Path,
    device: str,
    epochs_override: int | None,
    batch_override: str | None,
    workers: int,
    patience: int,
) -> list[str]:
    epochs = epochs_override if epochs_override is not None else int(config.get("epochs", 100))
    batch = batch_override if batch_override is not None else str(config.get("batch", "auto"))
    image_size = int(config.get("imgsz", 640))
    seed = int(config.get("seed", 42))
    model = str(config["model"])

    return [
        "yolo",
        "segment",
        "train",
        f"model={model}",
        f"data={dataset_path.as_posix()}",
        f"epochs={epochs}",
        f"imgsz={image_size}",
        f"batch={batch}",
        f"device={device}",
        f"workers={workers}",
        f"seed={seed}",
        f"patience={patience}",
        f"project={(run_dir / 'ultralytics').as_posix()}",
        "name=train",
        "exist_ok=True",
        "plots=True",
        "save=True",
        "verbose=True",
    ]


def copy_if_exists(source: Path, dest: Path) -> None:
    if source.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)


def collect_basic_outputs(run_dir: Path) -> dict[str, str]:
    train_dir = run_dir / "ultralytics" / "train"
    outputs: dict[str, str] = {}
    for name in ["results.csv", "args.yaml"]:
        source = train_dir / name
        if source.exists():
            dest = run_dir / name
            copy_if_exists(source, dest)
            outputs[name] = str(dest)

    weights_dir = train_dir / "weights"
    for name in ["best.pt", "last.pt"]:
        source = weights_dir / name
        if source.exists():
            outputs[name] = str(source)

    return outputs


def run_experiment(
    config_path: Path,
    repo_root: Path,
    output_root: Path,
    device: str,
    epochs_override: int | None,
    batch_override: str | None,
    workers: int,
    patience: int,
    dry_run: bool,
) -> int:
    config = read_yaml(config_path)
    exp_id = str(config["id"])
    exp_name = str(config["name"])
    run_dir = output_root / "experiments" / f"{exp_id}_{exp_name}"
    run_dir.mkdir(parents=True, exist_ok=True)

    dataset_path = resolve_path(str(config["dataset"]), repo_root)
    command = build_yolo_command(
        config=config,
        dataset_path=dataset_path,
        run_dir=run_dir,
        device=device,
        epochs_override=epochs_override,
        batch_override=batch_override,
        workers=workers,
        patience=patience,
    )

    shutil.copy2(config_path, run_dir / "config.yaml")
    (run_dir / "command.txt").write_text(" ".join(command) + "\n", encoding="utf-8")

    status = {
        "experiment_id": exp_id,
        "name": exp_name,
        "status": "dry_run" if dry_run else "running",
        "started_at_utc": utc_now(),
        "last_heartbeat_utc": utc_now(),
        "config_path": str(config_path),
        "dataset_path": str(dataset_path),
        "run_dir": str(run_dir),
        "device": device,
        "command": command,
    }
    write_json(run_dir / "status.json", status)

    timestamps = {
        "started_at_utc": status["started_at_utc"],
        "finished_at_utc": None,
        "elapsed_seconds": None,
    }
    write_json(run_dir / "timestamps.json", timestamps)

    if dry_run:
        print(" ".join(command))
        return 0

    start = time.time()
    stdout_path = run_dir / "stdout.log"
    stderr_path = run_dir / "stderr.log"

    with stdout_path.open("w", encoding="utf-8") as stdout_log, stderr_path.open(
        "w", encoding="utf-8"
    ) as stderr_log:
        process = subprocess.Popen(
            command,
            cwd=repo_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        assert process.stdout is not None
        for line in process.stdout:
            print(line, end="")
            stdout_log.write(line)
            stdout_log.flush()
            status["last_heartbeat_utc"] = utc_now()
            write_json(run_dir / "status.json", status)

        return_code = process.wait()
        if return_code != 0:
            stderr_log.write(f"Command failed with return code {return_code}\n")

    elapsed = time.time() - start
    outputs = collect_basic_outputs(run_dir)
    status.update(
        {
            "status": "completed" if return_code == 0 else "failed",
            "finished_at_utc": utc_now(),
            "return_code": return_code,
            "elapsed_seconds": round(elapsed, 2),
            "outputs": outputs,
        }
    )
    timestamps.update(
        {
            "finished_at_utc": status["finished_at_utc"],
            "elapsed_seconds": round(elapsed, 2),
        }
    )
    write_json(run_dir / "status.json", status)
    write_json(run_dir / "timestamps.json", timestamps)

    return return_code


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path(os.environ.get("OUTPUT_ROOT", "runs")),
    )
    parser.add_argument("--device", default=os.environ.get("YOLO_DEVICE", "0"))
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch", default=None)
    parser.add_argument("--workers", type=int, default=int(os.environ.get("YOLO_WORKERS", "2")))
    parser.add_argument("--patience", type=int, default=int(os.environ.get("YOLO_PATIENCE", "25")))
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    raise SystemExit(
        run_experiment(
            config_path=args.config,
            repo_root=repo_root,
            output_root=args.output_root,
            device=args.device,
            epochs_override=args.epochs,
            batch_override=args.batch,
            workers=args.workers,
            patience=args.patience,
            dry_run=args.dry_run,
        )
    )


if __name__ == "__main__":
    main()

