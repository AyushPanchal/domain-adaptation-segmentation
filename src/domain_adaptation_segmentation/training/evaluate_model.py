"""Evaluate a YOLO segmentation checkpoint and persist metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ultralytics import YOLO


def scalar(value: Any) -> Any:
    if hasattr(value, "item"):
        return value.item()
    if isinstance(value, (list, tuple)):
        return [scalar(item) for item in value]
    return value


def evaluate_model(
    model_path: Path,
    data_path: Path,
    output_root: Path,
    name: str,
    device: str,
    image_size: int,
    batch: int,
    workers: int,
) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    model = YOLO(str(model_path))
    results = model.val(
        data=str(data_path),
        imgsz=image_size,
        batch=batch,
        device=device,
        workers=workers,
        project=str(output_root),
        name=name,
        exist_ok=True,
        plots=True,
        verbose=True,
    )

    metrics = {key: scalar(value) for key, value in results.results_dict.items()}
    payload: dict[str, Any] = {
        "name": name,
        "model_path": str(model_path),
        "data_path": str(data_path),
        "device": device,
        "imgsz": image_size,
        "batch": batch,
        "workers": workers,
        "save_dir": str(results.save_dir),
        "metrics": metrics,
    }

    eval_dir = output_root / name
    eval_dir.mkdir(parents=True, exist_ok=True)
    (eval_dir / "metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--device", default="0")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--workers", type=int, default=2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = evaluate_model(
        model_path=args.model,
        data_path=args.data,
        output_root=args.output_root,
        name=args.name,
        device=args.device,
        image_size=args.imgsz,
        batch=args.batch,
        workers=args.workers,
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
