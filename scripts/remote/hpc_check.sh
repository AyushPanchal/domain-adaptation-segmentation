#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$PWD}"
cd "$REPO_ROOT"

echo "[HPC CHECK] repo: $REPO_ROOT"
echo "[HPC CHECK] python: $(command -v python)"
python --version

echo "[HPC CHECK] git commit:"
if command -v git >/dev/null 2>&1; then
  git rev-parse --short HEAD
else
  echo "git not found on this compute node; skipping commit check"
fi

echo "[HPC CHECK] checking required paths..."
test -d data/processed
test -d data/manifests/dataset_yamls
test -f configs/experiments/e01_source_rgb_yolo11s.yaml

echo "[HPC CHECK] dataset yaml files:"
ls -lh data/manifests/dataset_yamls

echo "[HPC CHECK] processed dataset folders:"
find data/processed -maxdepth 1 -mindepth 1 -type d -printf "%f\n" | sort

echo "[HPC CHECK] GPU status:"
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi
else
  echo "nvidia-smi not found"
fi

echo "[HPC CHECK] ultralytics import:"
python - <<'PY'
try:
    import torch
    print("torch", torch.__version__)
    print("cuda available", torch.cuda.is_available())
    print("cuda devices", torch.cuda.device_count())
    import ultralytics
    print("ultralytics", ultralytics.__version__)
except Exception as exc:
    print("python dependency import failed:", exc)
    raise
PY

echo "[HPC CHECK] OK"
