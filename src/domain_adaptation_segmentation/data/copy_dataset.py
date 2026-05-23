"""Copy matched IndraEye YOLO segmentation image/label pairs.

The parent workspace contains image folders with both .jpg images and .json
sidecars. This script copies only usable YOLO segmentation pairs into this
project and writes manifests for copied/skipped files.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DOMAINS = ("eo", "ir")
SPLITS = ("train", "val")


@dataclass(frozen=True)
class LabelValidation:
    valid: bool
    instances: int
    class_counts: Counter[int]
    issues: list[str]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_nc(class_config: Path) -> int:
    for line in class_config.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("nc:"):
            return int(stripped.split(":", 1)[1].strip())
    raise ValueError(f"Could not find nc in class config: {class_config}")


def validate_label(path: Path, nc: int) -> LabelValidation:
    issues: list[str] = []
    class_counts: Counter[int] = Counter()
    instances = 0

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return LabelValidation(False, 0, class_counts, ["empty_label"])

    for line_number, line in enumerate(text.splitlines(), start=1):
        parts = line.strip().split()
        if not parts:
            continue

        try:
            class_id = int(float(parts[0]))
            coords = [float(value) for value in parts[1:]]
        except ValueError:
            issues.append(f"line_{line_number}:non_numeric")
            continue

        if class_id < 0 or class_id >= nc:
            issues.append(f"line_{line_number}:class_out_of_range:{class_id}")

        if len(coords) < 6:
            issues.append(f"line_{line_number}:too_few_coordinates:{len(coords)}")
        if len(coords) % 2 != 0:
            issues.append(f"line_{line_number}:odd_coordinate_count:{len(coords)}")

        bad_coords = [value for value in coords if value < 0.0 or value > 1.0]
        if bad_coords:
            issues.append(f"line_{line_number}:coords_out_of_range:{len(bad_coords)}")

        class_counts[class_id] += 1
        instances += 1

    return LabelValidation(len(issues) == 0 and instances > 0, instances, class_counts, issues)


def ensure_dirs(dest_root: Path) -> None:
    for domain in DOMAINS:
        for split in SPLITS:
            (dest_root / domain / "images" / split).mkdir(parents=True, exist_ok=True)
            (dest_root / domain / "labels" / split).mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_dataset(source_root: Path, dest_root: Path, manifest_root: Path, class_config: Path) -> None:
    nc = parse_nc(class_config)
    ensure_dirs(dest_root)

    copied_rows: list[dict[str, object]] = []
    skipped_rows: list[dict[str, object]] = []
    issue_rows: list[dict[str, object]] = []
    class_counts: dict[tuple[str, str], Counter[int]] = defaultdict(Counter)
    split_summary: dict[str, dict[str, dict[str, int]]] = defaultdict(dict)

    for domain in DOMAINS:
        for split in SPLITS:
            src_img_dir = source_root / domain / "images" / split
            src_lab_dir = source_root / domain / "labels" / split
            dst_img_dir = dest_root / domain / "images" / split
            dst_lab_dir = dest_root / domain / "labels" / split

            if not src_img_dir.exists() or not src_lab_dir.exists():
                raise FileNotFoundError(f"Missing source split: {src_img_dir} or {src_lab_dir}")

            image_paths = sorted(src_img_dir.glob("*.jpg"))
            label_paths = sorted(src_lab_dir.glob("*.txt"))
            image_stems = {path.stem for path in image_paths}
            label_stems = {path.stem for path in label_paths}

            copied = 0
            skipped = 0
            invalid = 0
            instances = 0

            for image_path in image_paths:
                label_path = src_lab_dir / f"{image_path.stem}.txt"
                common = {
                    "domain": domain,
                    "split": split,
                    "stem": image_path.stem,
                    "source_image": str(image_path),
                    "source_label": str(label_path),
                }

                if not label_path.exists():
                    skipped += 1
                    skipped_rows.append({**common, "reason": "missing_label"})
                    continue

                validation = validate_label(label_path, nc)
                if not validation.valid:
                    invalid += 1
                    skipped += 1
                    skipped_rows.append({**common, "reason": "invalid_label"})
                    for issue in validation.issues:
                        issue_rows.append({**common, "issue": issue})
                    continue

                dst_image = dst_img_dir / image_path.name
                dst_label = dst_lab_dir / label_path.name
                shutil.copy2(image_path, dst_image)
                shutil.copy2(label_path, dst_label)

                copied += 1
                instances += validation.instances
                class_counts[(domain, split)].update(validation.class_counts)
                copied_rows.append(
                    {
                        **common,
                        "dest_image": str(dst_image),
                        "dest_label": str(dst_label),
                        "image_sha256": sha256_file(dst_image),
                        "label_sha256": sha256_file(dst_label),
                        "instances": validation.instances,
                    }
                )

            for orphan_stem in sorted(label_stems - image_stems):
                skipped_rows.append(
                    {
                        "domain": domain,
                        "split": split,
                        "stem": orphan_stem,
                        "source_image": "",
                        "source_label": str(src_lab_dir / f"{orphan_stem}.txt"),
                        "reason": "orphan_label",
                    }
                )

            split_summary[domain][split] = {
                "source_jpg_images": len(image_paths),
                "source_label_files": len(label_paths),
                "copied_pairs": copied,
                "skipped_images": skipped,
                "invalid_labels": invalid,
                "orphan_labels": len(label_stems - image_stems),
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

    summary = {
        "created_at_utc": utc_now(),
        "source_root": str(source_root),
        "dest_root": str(dest_root),
        "class_config": str(class_config),
        "nc": nc,
        "domains": split_summary,
        "totals": {
            "copied_pairs": len(copied_rows),
            "skipped_records": len(skipped_rows),
            "label_issues": len(issue_rows),
            "instances": sum(int(row["instances"]) for row in copied_rows),
        },
    }

    write_csv(
        manifest_root / "copied_files.csv",
        copied_rows,
        [
            "domain",
            "split",
            "stem",
            "source_image",
            "source_label",
            "dest_image",
            "dest_label",
            "image_sha256",
            "label_sha256",
            "instances",
        ],
    )
    write_csv(
        manifest_root / "skipped_files.csv",
        skipped_rows,
        ["domain", "split", "stem", "source_image", "source_label", "reason"],
    )
    write_csv(
        manifest_root / "label_issues.csv",
        issue_rows,
        ["domain", "split", "stem", "source_image", "source_label", "issue"],
    )
    write_csv(
        manifest_root / "class_counts.csv",
        class_count_rows,
        ["domain", "split", "class_id", "instances"],
    )
    (manifest_root / "dataset_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print(json.dumps(summary["totals"], indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path("../datasets/indraeye_seg"))
    parser.add_argument("--dest-root", type=Path, default=Path("data/raw/indraeye_seg"))
    parser.add_argument("--manifest-root", type=Path, default=Path("data/manifests"))
    parser.add_argument(
        "--class-config",
        type=Path,
        default=Path("configs/classes/indraeye_seg_active12.yaml"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    copy_dataset(
        source_root=args.source_root,
        dest_root=args.dest_root,
        manifest_root=args.manifest_root,
        class_config=args.class_config,
    )


if __name__ == "__main__":
    main()

