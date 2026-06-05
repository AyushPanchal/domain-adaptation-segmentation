"""Evaluate a YOLO segmentation ensemble with mask-aware cross-model NMS."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import torch
from ultralytics import YOLO
from ultralytics.models.yolo.segment.val import SegmentationValidator
from ultralytics.nn.tasks import load_checkpoint
from ultralytics.utils import ops
from ultralytics.utils import nms


def scalar(value: Any) -> Any:
    if hasattr(value, "item"):
        return value.item()
    if isinstance(value, (list, tuple)):
        return [scalar(item) for item in value]
    return value


class SegmentationNmsEnsemble(torch.nn.Module):
    """Concatenate predictions from multiple YOLO segmentation models.

    The standard Ultralytics `Ensemble` concatenates raw prediction tensors but drops segmentation
    prototypes. This wrapper keeps each model's prototype tensor so the custom validator can build
    masks from the correct source model after cross-model NMS.
    """

    def __init__(self, weights: list[Path]) -> None:
        super().__init__()
        if len(weights) < 2:
            raise ValueError("At least two checkpoints are required for an ensemble.")

        self.models = torch.nn.ModuleList()
        for weight in weights:
            model, _ = load_checkpoint(weight, fuse=True)
            if getattr(model, "task", None) != "segment":
                raise ValueError(f"Expected a segmentation checkpoint, got task={model.task!r}: {weight}")
            self.models.append(model)

        first = self.models[0]
        self.names = first.names
        self.nc = len(first.names)
        self.task = "segment"
        self.stride = first.stride
        self.args = first.args
        self.yaml = getattr(first, "yaml", {"channels": 3})
        self.pt_path = "+".join(str(weight) for weight in weights)

    def fuse(self, verbose: bool = True) -> "SegmentationNmsEnsemble":
        for i, model in enumerate(self.models):
            if hasattr(model, "fuse"):
                self.models[i] = model.fuse(verbose=verbose)
        return self

    def forward(
        self,
        x: torch.Tensor,
        augment: bool = False,
        profile: bool = False,
        visualize: bool = False,
        embed: list[int] | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        raw_predictions: list[torch.Tensor] = []
        prototypes: list[torch.Tensor] = []
        candidate_counts: list[int] = []

        for model in self.models:
            output = model(x, augment=augment, profile=profile, visualize=visualize)
            raw = output[0]
            proto_output = output[1]
            proto = proto_output[-1] if isinstance(proto_output, (list, tuple)) else proto_output

            raw_predictions.append(raw)
            prototypes.append(proto)
            candidate_counts.append(raw.shape[-1])

        return {
            "prediction": torch.cat(raw_predictions, dim=2),
            "prototypes": prototypes,
            "candidate_counts": candidate_counts,
        }


class SegmentationNmsEnsembleValidator(SegmentationValidator):
    """Ultralytics validator that reconstructs masks from each source model's prototypes."""

    def postprocess(self, preds: Any) -> list[dict[str, torch.Tensor]]:
        if not isinstance(preds, dict):
            return super().postprocess(preds)

        prediction = preds["prediction"]
        prototypes: list[torch.Tensor] = preds["prototypes"]
        candidate_counts: list[int] = preds["candidate_counts"]

        outputs, kept_indices = nms.non_max_suppression(
            prediction,
            self.args.conf,
            self.args.iou,
            nc=self.nc,
            multi_label=True,
            agnostic=self.args.single_cls or self.args.agnostic_nms,
            max_det=self.args.max_det,
            end2end=self.end2end,
            return_idxs=True,
        )

        imgsz = [4 * x for x in prototypes[0].shape[2:]]
        results: list[dict[str, torch.Tensor]] = []
        for image_index, detections in enumerate(outputs):
            pred = {
                "bboxes": detections[:, :4],
                "conf": detections[:, 4],
                "cls": detections[:, 5],
                "extra": detections[:, 6:],
            }

            coefficients = pred.pop("extra")
            if coefficients.shape[0] == 0:
                pred["masks"] = torch.zeros(
                    (0, *(imgsz if self.process is ops.process_mask_native else prototypes[0].shape[2:])),
                    dtype=torch.uint8,
                    device=prediction.device,
                )
                results.append(pred)
                continue

            source_ids = self._source_ids(kept_indices[image_index], candidate_counts)
            masks = []
            for row_index, source_id in enumerate(source_ids.tolist()):
                masks.append(
                    self.process(
                        prototypes[source_id][image_index],
                        coefficients[row_index : row_index + 1],
                        pred["bboxes"][row_index : row_index + 1],
                        shape=imgsz,
                    )
                )
            pred["masks"] = torch.cat(masks, dim=0)
            results.append(pred)

        return results

    @staticmethod
    def _source_ids(kept_indices: torch.Tensor, candidate_counts: list[int]) -> torch.Tensor:
        source_ids = torch.zeros_like(kept_indices)
        start = 0
        for source_index, count in enumerate(candidate_counts):
            end = start + count
            source_ids[(kept_indices >= start) & (kept_indices < end)] = source_index
            start = end
        return source_ids


def evaluate_segmentation_ensemble(
    weights: list[Path],
    data_path: Path,
    output_root: Path,
    name: str,
    device: str,
    image_size: int,
    batch: int,
    workers: int,
    conf: float | None,
    iou: float,
) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)

    yolo = YOLO(str(weights[0]))
    yolo.model = SegmentationNmsEnsemble(weights)
    yolo.overrides["task"] = "segment"

    val_kwargs: dict[str, Any] = {
        "data": str(data_path),
        "imgsz": image_size,
        "batch": batch,
        "device": device,
        "workers": workers,
        "project": str(output_root),
        "name": name,
        "exist_ok": True,
        "plots": True,
        "verbose": True,
        "iou": iou,
    }
    if conf is not None:
        val_kwargs["conf"] = conf

    results = yolo.val(validator=SegmentationNmsEnsembleValidator, **val_kwargs)
    metrics = {key: scalar(value) for key, value in results.results_dict.items()}
    payload: dict[str, Any] = {
        "name": name,
        "weights": [str(weight) for weight in weights],
        "data_path": str(data_path),
        "device": device,
        "imgsz": image_size,
        "batch": batch,
        "workers": workers,
        "conf": conf,
        "iou": iou,
        "save_dir": str(results.save_dir),
        "metrics": metrics,
    }

    eval_dir = output_root / name
    eval_dir.mkdir(parents=True, exist_ok=True)
    (eval_dir / "metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", type=Path, nargs="+", required=True)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--device", default="0")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--conf", type=float, default=None)
    parser.add_argument("--iou", type=float, default=0.7)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = evaluate_segmentation_ensemble(
        weights=args.weights,
        data_path=args.data,
        output_root=args.output_root,
        name=args.name,
        device=args.device,
        image_size=args.imgsz,
        batch=args.batch,
        workers=args.workers,
        conf=args.conf,
        iou=args.iou,
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
