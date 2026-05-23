"""Generate processed YOLO segmentation datasets for gray-augmentation experiments."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from domain_adaptation_segmentation.data.copy_dataset import parse_nc, validate_label


RGB_METHODS = {
    "source_rgb": "none",
    "full_gray": "full_gray",
    "box_guided_gray": "box_guided_gray",
    "mga": "mask_guided_gray",
    "ba_mga": "boundary_aware_mask_guided_gray",
}
ORACLE_METHOD = "ir_oracle"
ALL_METHODS = (*RGB_METHODS.keys(), ORACLE_METHOD)


@dataclass(frozen=True)
class PolygonInstance:
    class_id: int
    points: list[tuple[float, float]]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_instances(label_path: Path) -> list[PolygonInstance]:
    instances: list[PolygonInstance] = []
    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        class_id = int(float(parts[0]))
        coords = [float(value) for value in parts[1:]]
        points = list(zip(coords[0::2], coords[1::2]))
        instances.append(PolygonInstance(class_id=class_id, points=points))
    return instances


def normalized_to_pixels(
    points: list[tuple[float, float]], width: int, height: int
) -> list[tuple[int, int]]:
    pixel_points: list[tuple[int, int]] = []
    for x_norm, y_norm in points:
        x = min(max(int(round(x_norm * (width - 1))), 0), width - 1)
        y = min(max(int(round(y_norm * (height - 1))), 0), height - 1)
        pixel_points.append((x, y))
    return pixel_points


def grayscale_rgb(image: Image.Image) -> Image.Image:
    return image.convert("L").convert("RGB")


def full_gray(image: Image.Image, _instances: list[PolygonInstance]) -> Image.Image:
    return grayscale_rgb(image)


def box_guided_gray(
    image: Image.Image, instances: list[PolygonInstance], skip_classes: set[int]
) -> Image.Image:
    output = image.copy()
    gray = grayscale_rgb(image)
    width, height = image.size
    for instance in instances:
        if instance.class_id in skip_classes:
            continue
        points = normalized_to_pixels(instance.points, width, height)
        if len(points) < 3:
            continue
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        box = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
        output.paste(gray.crop(box), box)
    return output


def polygon_mask(
    image_size: tuple[int, int],
    instances: list[PolygonInstance],
    skip_classes: set[int],
    feather_radius: float = 0.0,
) -> Image.Image:
    width, height = image_size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    for instance in instances:
        if instance.class_id in skip_classes:
            continue
        points = normalized_to_pixels(instance.points, width, height)
        if len(points) >= 3:
            draw.polygon(points, fill=255)
    if feather_radius > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(radius=feather_radius))
    return mask


def mask_guided_gray(
    image: Image.Image, instances: list[PolygonInstance], skip_classes: set[int]
) -> Image.Image:
    gray = grayscale_rgb(image)
    mask = polygon_mask(image.size, instances, skip_classes)
    return Image.composite(gray, image, mask)


def boundary_aware_mask_guided_gray(
    image: Image.Image,
    instances: list[PolygonInstance],
    skip_classes: set[int],
    feather_radius: float,
) -> Image.Image:
    gray = grayscale_rgb(image)
    mask = polygon_mask(image.size, instances, skip_classes, feather_radius=feather_radius)
    return Image.composite(gray, image, mask)


def copy_pair(image_path: Path, label_path: Path, dest_image: Path, dest_label: Path) -> None:
    dest_image.parent.mkdir(parents=True, exist_ok=True)
    dest_label.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(image_path, dest_image)
    shutil.copy2(label_path, dest_label)


def save_augmented_pair(
    method: str,
    image_path: Path,
    label_path: Path,
    dest_image: Path,
    dest_label: Path,
    skip_classes: set[int],
    feather_radius: float,
) -> None:
    dest_image.parent.mkdir(parents=True, exist_ok=True)
    dest_label.parent.mkdir(parents=True, exist_ok=True)

    image = Image.open(image_path).convert("RGB")
    instances = read_instances(label_path)

    if method == "full_gray":
        augmented = full_gray(image, instances)
    elif method == "box_guided_gray":
        augmented = box_guided_gray(image, instances, skip_classes)
    elif method == "mga":
        augmented = mask_guided_gray(image, instances, skip_classes)
    elif method == "ba_mga":
        augmented = boundary_aware_mask_guided_gray(
            image, instances, skip_classes, feather_radius=feather_radius
        )
    else:
        raise ValueError(f"Unsupported augmentation method: {method}")

    augmented.save(dest_image, quality=95)
    shutil.copy2(label_path, dest_label)


def iter_pairs(root: Path, domain: str, split: str) -> list[tuple[Path, Path]]:
    image_dir = root / domain / "images" / split
    label_dir = root / domain / "labels" / split
    pairs: list[tuple[Path, Path]] = []
    for image_path in sorted(image_dir.glob("*.jpg")):
        label_path = label_dir / f"{image_path.stem}.txt"
        if label_path.exists():
            pairs.append((image_path, label_path))
    return pairs


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_dataset_yaml(method: str, processed_root: Path, yaml_root: Path, names: dict[int, str]) -> Path:
    yaml_root.mkdir(parents=True, exist_ok=True)
    method_root = processed_root / method
    yaml_path = yaml_root / f"{method}.yaml"
    lines = [
        f"path: {method_root.as_posix()}",
        "train: images/train",
        "val: images/val",
        "",
        f"nc: {len(names)}",
        "names:",
    ]
    for class_id, class_name in names.items():
        lines.append(f"  {class_id}: {class_name}")
    yaml_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return yaml_path


def parse_class_names(class_config: Path) -> dict[int, str]:
    names: dict[int, str] = {}
    in_names = False
    for line in class_config.read_text(encoding="utf-8").splitlines():
        if line.strip() == "names:":
            in_names = True
            continue
        if in_names and ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            if key.isdigit():
                names[int(key)] = value.strip()
    if not names:
        raise ValueError(f"No class names found in {class_config}")
    return dict(sorted(names.items()))


def generate_augmented_datasets(
    raw_root: Path,
    processed_root: Path,
    manifest_root: Path,
    yaml_root: Path,
    class_config: Path,
    skip_classes: set[int],
    feather_radius: float,
) -> None:
    nc = parse_nc(class_config)
    names = parse_class_names(class_config)
    manifest_rows: list[dict[str, object]] = []
    class_counts: dict[tuple[str, str], Counter[int]] = defaultdict(Counter)
    summary: dict[str, object] = {
        "created_at_utc": utc_now(),
        "raw_root": str(raw_root),
        "processed_root": str(processed_root),
        "class_config": str(class_config),
        "nc": nc,
        "skip_classes": sorted(skip_classes),
        "feather_radius": feather_radius,
        "methods": {},
    }

    ir_val_pairs = iter_pairs(raw_root, "ir", "val")

    for method in ALL_METHODS:
        method_root = processed_root / method
        if method == ORACLE_METHOD:
            train_pairs = iter_pairs(raw_root, "ir", "train")
            train_source = "ir"
        else:
            train_pairs = iter_pairs(raw_root, "eo", "train")
            train_source = "eo"

        split_pairs = {"train": train_pairs, "val": ir_val_pairs}
        method_counts = {"train": 0, "val": 0}
        method_instances = {"train": 0, "val": 0}

        for split, pairs in split_pairs.items():
            for image_path, label_path in pairs:
                dest_image = method_root / "images" / split / image_path.name
                dest_label = method_root / "labels" / split / label_path.name
                validation = validate_label(label_path, nc)
                if not validation.valid:
                    raise ValueError(f"Invalid source label during augmentation: {label_path}")

                if split == "train" and method in RGB_METHODS and method != "source_rgb":
                    save_augmented_pair(
                        method=method,
                        image_path=image_path,
                        label_path=label_path,
                        dest_image=dest_image,
                        dest_label=dest_label,
                        skip_classes=skip_classes,
                        feather_radius=feather_radius,
                    )
                    transform = RGB_METHODS[method]
                else:
                    copy_pair(image_path, label_path, dest_image, dest_label)
                    transform = "copy"

                method_counts[split] += 1
                method_instances[split] += validation.instances
                class_counts[(method, split)].update(validation.class_counts)
                manifest_rows.append(
                    {
                        "method": method,
                        "split": split,
                        "source_domain": train_source if split == "train" else "ir",
                        "transform": transform,
                        "source_image": str(image_path),
                        "source_label": str(label_path),
                        "dest_image": str(dest_image),
                        "dest_label": str(dest_label),
                        "instances": validation.instances,
                    }
                )

        yaml_path = generate_dataset_yaml(method, processed_root, yaml_root, names)
        summary["methods"][method] = {
            "dataset_yaml": str(yaml_path),
            "train_pairs": method_counts["train"],
            "val_pairs": method_counts["val"],
            "train_instances": method_instances["train"],
            "val_instances": method_instances["val"],
        }

    class_count_rows: list[dict[str, object]] = []
    for (method, split), counts in sorted(class_counts.items()):
        for class_id in range(nc):
            class_count_rows.append(
                {
                    "method": method,
                    "split": split,
                    "class_id": class_id,
                    "instances": counts.get(class_id, 0),
                }
            )

    write_csv(
        manifest_root / "augmentation_manifest.csv",
        manifest_rows,
        [
            "method",
            "split",
            "source_domain",
            "transform",
            "source_image",
            "source_label",
            "dest_image",
            "dest_label",
            "instances",
        ],
    )
    write_csv(
        manifest_root / "augmentation_class_counts.csv",
        class_count_rows,
        ["method", "split", "class_id", "instances"],
    )
    (manifest_root / "augmentation_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print(json.dumps(summary["methods"], indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw/indraeye_seg"))
    parser.add_argument("--processed-root", type=Path, default=Path("data/processed"))
    parser.add_argument("--manifest-root", type=Path, default=Path("data/manifests"))
    parser.add_argument("--yaml-root", type=Path, default=Path("data/manifests/dataset_yamls"))
    parser.add_argument(
        "--class-config",
        type=Path,
        default=Path("configs/classes/indraeye_seg_active12.yaml"),
    )
    parser.add_argument(
        "--skip-class",
        dest="skip_classes",
        action="append",
        type=int,
        default=[],
        help="Class ID to leave unchanged during object-region gray augmentation.",
    )
    parser.add_argument("--feather-radius", type=float, default=3.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate_augmented_datasets(
        raw_root=args.raw_root,
        processed_root=args.processed_root,
        manifest_root=args.manifest_root,
        yaml_root=args.yaml_root,
        class_config=args.class_config,
        skip_classes=set(args.skip_classes),
        feather_radius=args.feather_radius,
    )


if __name__ == "__main__":
    main()

