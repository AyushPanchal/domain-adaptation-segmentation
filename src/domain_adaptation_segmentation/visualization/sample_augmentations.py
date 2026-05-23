"""Create contact sheets for visual inspection of generated augmentations."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


METHODS = ("source_rgb", "full_gray", "box_guided_gray", "mga", "ba_mga")
CLASS_NAMES = {
    0: "Bicycle",
    1: "Bus",
    2: "Car",
    3: "Cargo trike",
    4: "Ignore",
    5: "Motorcycle",
    6: "Person",
    7: "Rickshaw",
    8: "Small truck",
    9: "Tractor",
    10: "Truck",
    11: "Van",
}


@dataclass(frozen=True)
class Candidate:
    stem: str
    classes: set[int]
    instances: int


def read_label_classes(label_path: Path) -> Counter[int]:
    counts: Counter[int] = Counter()
    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if parts:
            counts[int(float(parts[0]))] += 1
    return counts


def read_label_points(label_path: Path) -> list[tuple[int, list[tuple[float, float]]]]:
    instances: list[tuple[int, list[tuple[float, float]]]] = []
    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        class_id = int(float(parts[0]))
        coords = [float(value) for value in parts[1:]]
        points = list(zip(coords[0::2], coords[1::2]))
        instances.append((class_id, points))
    return instances


def choose_samples(label_dir: Path, limit: int) -> list[Candidate]:
    candidates: list[Candidate] = []
    for label_path in sorted(label_dir.glob("*.txt")):
        counts = read_label_classes(label_path)
        candidates.append(
            Candidate(stem=label_path.stem, classes=set(counts), instances=sum(counts.values()))
        )

    selected: list[Candidate] = []
    covered: set[int] = set()
    remaining = candidates[:]

    while remaining and len(selected) < limit:
        remaining.sort(
            key=lambda item: (len(item.classes - covered), len(item.classes), item.instances),
            reverse=True,
        )
        best = remaining.pop(0)
        selected.append(best)
        covered.update(best.classes)
        if len(covered) == len(CLASS_NAMES) and len(selected) >= min(limit, 3):
            break

    return selected


def resize_with_padding(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    image = image.convert("RGB")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, (245, 245, 245))
    x = (size[0] - image.width) // 2
    y = (size[1] - image.height) // 2
    canvas.paste(image, (x, y))
    return canvas


def add_header(image: Image.Image, text: str, height: int = 34) -> Image.Image:
    canvas = Image.new("RGB", (image.width, image.height + height), (30, 30, 30))
    canvas.paste(image, (0, height))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    draw.text((8, 8), text, fill=(255, 255, 255), font=font)
    return canvas


def make_method_sheet(
    processed_root: Path,
    raw_label_dir: Path,
    candidate: Candidate,
    output_dir: Path,
    tile_size: tuple[int, int],
) -> Path:
    tiles: list[Image.Image] = []
    for method in METHODS:
        image_path = processed_root / method / "images" / "train" / f"{candidate.stem}.jpg"
        image = Image.open(image_path)
        tile = resize_with_padding(image, tile_size)
        tiles.append(add_header(tile, method))

    width = tile_size[0] * len(tiles)
    height = tiles[0].height
    sheet = Image.new("RGB", (width, height), (255, 255, 255))
    for index, tile in enumerate(tiles):
        sheet.paste(tile, (index * tile_size[0], 0))

    class_names = ", ".join(CLASS_NAMES[class_id] for class_id in sorted(candidate.classes))
    caption_height = 52
    final = Image.new("RGB", (sheet.width, sheet.height + caption_height), (255, 255, 255))
    final.paste(sheet, (0, 0))
    draw = ImageDraw.Draw(final)
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except OSError:
        font = ImageFont.load_default()
    label_path = raw_label_dir / f"{candidate.stem}.txt"
    counts = read_label_classes(label_path)
    count_text = "; ".join(f"{CLASS_NAMES[k]}={v}" for k, v in sorted(counts.items()))
    draw.text((10, sheet.height + 8), candidate.stem, fill=(0, 0, 0), font=font)
    draw.text((10, sheet.height + 28), count_text or class_names, fill=(40, 40, 40), font=font)

    output_path = output_dir / f"{candidate.stem}_augmentation_comparison.jpg"
    final.save(output_path, quality=95)
    return output_path


def make_overview_sheet(image_paths: list[Path], output_path: Path, max_width: int = 1600) -> None:
    images = [Image.open(path).convert("RGB") for path in image_paths]
    if not images:
        return
    width = min(max_width, max(image.width for image in images))
    resized: list[Image.Image] = []
    for image in images:
        if image.width != width:
            new_height = int(image.height * width / image.width)
            image = image.resize((width, new_height), Image.Resampling.LANCZOS)
        resized.append(image)
    total_height = sum(image.height for image in resized)
    sheet = Image.new("RGB", (width, total_height), (255, 255, 255))
    y = 0
    for image in resized:
        sheet.paste(image, (0, y))
        y += image.height
    sheet.save(output_path, quality=95)


def crop_box_from_label(label_path: Path, image_size: tuple[int, int], padding_ratio: float) -> tuple[int, int, int, int]:
    width, height = image_size
    xs: list[float] = []
    ys: list[float] = []
    for class_id, points in read_label_points(label_path):
        if class_id == 4:
            continue
        for x_norm, y_norm in points:
            xs.append(x_norm * width)
            ys.append(y_norm * height)
    if not xs or not ys:
        return (0, 0, width, height)

    x1, x2 = min(xs), max(xs)
    y1, y2 = min(ys), max(ys)
    pad = padding_ratio * max(x2 - x1, y2 - y1)
    left = max(int(x1 - pad), 0)
    top = max(int(y1 - pad), 0)
    right = min(int(x2 + pad), width)
    bottom = min(int(y2 + pad), height)
    if right <= left or bottom <= top:
        return (0, 0, width, height)
    return (left, top, right, bottom)


def save_individual_method_images(
    processed_root: Path,
    raw_label_dir: Path,
    candidate: Candidate,
    output_dir: Path,
    crop_padding_ratio: float,
) -> list[Path]:
    output_paths: list[Path] = []
    sample_dir = output_dir / candidate.stem
    sample_dir.mkdir(parents=True, exist_ok=True)
    label_path = raw_label_dir / f"{candidate.stem}.txt"

    source_image = Image.open(processed_root / "source_rgb" / "images" / "train" / f"{candidate.stem}.jpg")
    crop_box = crop_box_from_label(label_path, source_image.size, crop_padding_ratio)

    for method in METHODS:
        image_path = processed_root / method / "images" / "train" / f"{candidate.stem}.jpg"
        image = Image.open(image_path).convert("RGB")
        full_out = sample_dir / f"{method}_full.jpg"
        crop_out = sample_dir / f"{method}_crop.jpg"
        image.save(full_out, quality=95)
        image.crop(crop_box).save(crop_out, quality=95)
        output_paths.extend([full_out, crop_out])

    return output_paths


def make_ir_oracle_sheet(
    processed_root: Path,
    label_dir: Path,
    output_dir: Path,
    limit: int,
    tile_size: tuple[int, int],
) -> Path:
    candidates = choose_samples(label_dir, limit)
    tiles: list[Image.Image] = []
    for candidate in candidates:
        image_path = processed_root / "ir_oracle" / "images" / "train" / f"{candidate.stem}.jpg"
        image = resize_with_padding(Image.open(image_path), tile_size)
        classes = ", ".join(CLASS_NAMES[class_id] for class_id in sorted(candidate.classes))
        tiles.append(add_header(image, classes[:80]))

    columns = min(limit, len(tiles))
    width = tile_size[0] * columns
    height = tiles[0].height if tiles else tile_size[1]
    sheet = Image.new("RGB", (width, height), (255, 255, 255))
    for index, tile in enumerate(tiles):
        sheet.paste(tile, (index * tile_size[0], 0))
    output_path = output_dir / "ir_oracle_samples.jpg"
    sheet.save(output_path, quality=95)
    return output_path


def write_manifest(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["kind", "path", "stem", "classes", "instances"])
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--processed-root", type=Path, default=Path("data/processed"))
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw/indraeye_seg"))
    parser.add_argument(
        "--output-dir", type=Path, default=Path("reports/qualitative/augmentation_samples")
    )
    parser.add_argument("--limit", type=int, default=4)
    parser.add_argument("--tile-width", type=int, default=320)
    parser.add_argument("--tile-height", type=int, default=220)
    parser.add_argument("--crop-padding-ratio", type=float, default=0.08)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    tile_size = (args.tile_width, args.tile_height)

    eo_label_dir = args.raw_root / "eo" / "labels" / "train"
    selected = choose_samples(eo_label_dir, args.limit)
    rows: list[dict[str, object]] = []
    comparison_paths: list[Path] = []

    for candidate in selected:
        output_path = make_method_sheet(
            processed_root=args.processed_root,
            raw_label_dir=eo_label_dir,
            candidate=candidate,
            output_dir=args.output_dir,
            tile_size=tile_size,
        )
        comparison_paths.append(output_path)
        rows.append(
            {
                "kind": "augmentation_comparison",
                "path": str(output_path),
                "stem": candidate.stem,
                "classes": "|".join(CLASS_NAMES[class_id] for class_id in sorted(candidate.classes)),
                "instances": candidate.instances,
            }
        )
        for path in save_individual_method_images(
            processed_root=args.processed_root,
            raw_label_dir=eo_label_dir,
            candidate=candidate,
            output_dir=args.output_dir / "individual",
            crop_padding_ratio=args.crop_padding_ratio,
        ):
            rows.append(
                {
                    "kind": "individual_method_image",
                    "path": str(path),
                    "stem": candidate.stem,
                    "classes": "|".join(
                        CLASS_NAMES[class_id] for class_id in sorted(candidate.classes)
                    ),
                    "instances": candidate.instances,
                }
            )

    overview_path = args.output_dir / "augmentation_comparison_overview.jpg"
    make_overview_sheet(comparison_paths, overview_path)
    rows.append(
        {
            "kind": "augmentation_overview",
            "path": str(overview_path),
            "stem": "",
            "classes": "",
            "instances": "",
        }
    )

    ir_path = make_ir_oracle_sheet(
        processed_root=args.processed_root,
        label_dir=args.raw_root / "ir" / "labels" / "train",
        output_dir=args.output_dir,
        limit=args.limit,
        tile_size=tile_size,
    )
    rows.append(
        {
            "kind": "ir_oracle_samples",
            "path": str(ir_path),
            "stem": "",
            "classes": "",
            "instances": "",
        }
    )

    write_manifest(args.output_dir / "sample_manifest.csv", rows)
    for row in rows:
        print(row["path"])


if __name__ == "__main__":
    main()
