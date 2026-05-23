"""Package code, configs, manifests, and processed datasets for Kaggle upload."""

from __future__ import annotations

import argparse
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path


INCLUDE_PATHS = [
    "configs",
    "data/manifests",
    "data/processed",
    "scripts/remote",
    "src",
    "AUGMENTATION_METHODS.md",
    "DATA_DISCOVERY.md",
    "EXPERIMENT_TRACKER.md",
    "KAGGLE_TRAINING.md",
    "README.md",
    "REMOTE_TRAINING.md",
    "pyproject.toml",
    "requirements.txt",
]

EXCLUDED_DIR_NAMES = {"__pycache__", ".pytest_cache", ".ruff_cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def should_include(path: Path) -> bool:
    if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return True


def iter_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for include in INCLUDE_PATHS:
        path = repo_root / include
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(file for file in path.rglob("*") if file.is_file() and should_include(file))
        else:
            raise FileNotFoundError(f"Required package path missing: {path}")
    return sorted(files)


def package_for_kaggle(repo_root: Path, output_zip: Path, compression_level: int) -> None:
    files = iter_files(repo_root)
    output_zip.parent.mkdir(parents=True, exist_ok=True)

    manifest = {
        "created_at_utc": utc_now(),
        "repo_root": str(repo_root),
        "output_zip": str(output_zip),
        "files": len(files),
        "include_paths": INCLUDE_PATHS,
    }

    compression = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(
        output_zip,
        "w",
        compression=compression,
        compresslevel=compression_level,
    ) as archive:
        for index, file_path in enumerate(files, start=1):
            arcname = file_path.relative_to(repo_root).as_posix()
            archive.write(file_path, arcname)
            if index % 1000 == 0:
                print(f"Packaged {index}/{len(files)} files...")

        archive.writestr("PACKAGE_MANIFEST.json", json.dumps(manifest, indent=2))

    size_mb = output_zip.stat().st_size / (1024 * 1024)
    manifest["size_mb"] = round(size_mb, 2)
    manifest_path = output_zip.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"zip": str(output_zip), "files": len(files), "size_mb": round(size_mb, 2)}, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--output-zip",
        type=Path,
        default=Path("artifacts/kaggle/domain-adaptation-segmentation-kaggle.zip"),
    )
    parser.add_argument("--compression-level", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    package_for_kaggle(
        repo_root=args.repo_root.resolve(),
        output_zip=args.output_zip,
        compression_level=args.compression_level,
    )


if __name__ == "__main__":
    main()

