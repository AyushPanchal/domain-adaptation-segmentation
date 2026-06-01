#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$PWD}"
cd "$REPO_ROOT"

export PYTHONPATH="$REPO_ROOT/src"
export OUTPUT_ROOT="${OUTPUT_ROOT:-$REPO_ROOT/runs}"
export YOLO_DEVICE="${YOLO_DEVICE:-0}"
export YOLO_WORKERS="${YOLO_WORKERS:-4}"
export EXPERIMENT_CONFIG="${EXPERIMENT_CONFIG:-configs/experiments/e01_source_rgb_yolo11s.yaml}"
export YOLO_EPOCHS="${YOLO_EPOCHS:-1}"

python scripts/remote/train_smoke.py

echo "[HPC SMOKE] done"
echo "[HPC SMOKE] config: $EXPERIMENT_CONFIG"
