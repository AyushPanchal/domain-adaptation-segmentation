"""Validate a copied YOLO segmentation dataset and write a validation report."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from domain_adaptation_segmentation.data.copy_dataset import DOMAINS, SPLITS, parse_nc, validate_label


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def validate_dataset(dataset_root: Path, manifest_root: Path, class_config: Path) -> int:
    nc = parse_nc(class_config)
    issue_rows: list[dict[str, object]] = []
    class_counts: dict[tuple[str, str], Counter[int]] = defaultdict(Counter)
    split_summary: dict[str, dict[str, dict[str, int]]] = defaultdict(dict)

    for domain in DOMAINS:
        for split in SPLITS:
            img_dir = dataset_root / domain / "images" / split
            lab_dir = dataset_root / domain / "labels" / split
            image_paths = sorted(img_dir.glob("*.jpg"))
            label_paths = sorted(lab_dir.glob("*.txt"))
            image_stems = {path.stem for path in image_paths}
            label_stems = {path.stem for path in label_paths}

            instances = 0
            invalid_labels = 0
            missing_labels = sorted(image_stems - label_stems)
            orphan_labels = sorted(label_stems - image_stems)

            for stem in missing_labels:
                issue_rows.append(
                    {
                        "domain": domain,
                        "split": split,
                        "stem": stem,
                        "label": "",
                        "issue": "missing_label",
                    }
                )
            for stem in orphan_labels:
                issue_rows.append(
                    {
                        "domain": domain,
                        "split": split,
                        "stem": stem,
                        "label": str(lab_dir / f"{stem}.txt"),
                        "issue": "orphan_label",
                    }
                )

            for label_path in label_paths:
                validation = validate_label(label_path, nc)
                if not validation.valid:
                    invalid_labels += 1
                    for issue in validation.issues:
                        issue_rows.append(
                            {
                                "domain": domain,
                                "split": split,
                                "stem": label_path.stem,
                                "label": str(label_path),
                                "issue": issue,
                            }
                        )
                    continue

                instances += validation.instances
                class_counts[(domain, split)].update(validation.class_counts)

            split_summary[domain][split] = {
                "jpg_images": len(image_paths),
                "label_files": len(label_paths),
                "missing_labels": len(missing_labels),
                "orphan_labels": len(orphan_labels),
                "invalid_labels": invalid_labels,
                "instances": instances,
            }

    class_count_rows: list[dict[str, object]] = []
    for (domain, split), counts in sorted(class_counts.items()):
        for class_id in range(nc):
            class_count_rows.append(
                {
                    "domain": domain,
                    "split": split,
                    "class_id": class_id,
                    "instances": counts.get(class_id, 0),
                }
            )

    report = {
        "validated_at_utc": utc_now(),
        "dataset_root": str(dataset_root),
        "class_config": str(class_config),
        "nc": nc,
        "domains": split_summary,
        "totals": {
            "issues": len(issue_rows),
            "instances": sum(
                split_info["instances"]
                for domain_info in split_summary.values()
                for split_info in domain_info.values()
            ),
        },
    }

    write_csv(
        manifest_root / "validation_issues.csv",
        issue_rows,
        ["domain", "split", "stem", "label", "issue"],
    )
    write_csv(
        manifest_root / "validation_class_counts.csv",
        class_count_rows,
        ["domain", "split", "class_id", "instances"],
    )
    (manifest_root / "validation_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    print(json.dumps(report["totals"], indent=2))
    return 0 if not issue_rows else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", type=Path, default=Path("data/raw/indraeye_seg"))
    parser.add_argument("--manifest-root", type=Path, default=Path("data/manifests"))
    parser.add_argument(
        "--class-config",
        type=Path,
        default=Path("configs/classes/indraeye_seg_active12.yaml"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raise SystemExit(validate_dataset(args.dataset_root, args.manifest_root, args.class_config))


if __name__ == "__main__":
    main()

