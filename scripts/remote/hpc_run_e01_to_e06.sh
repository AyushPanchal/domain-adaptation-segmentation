#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$PWD}"
cd "$REPO_ROOT"

export PYTHONPATH="$REPO_ROOT/src"
export OUTPUT_ROOT="${OUTPUT_ROOT:-$REPO_ROOT/runs}"
export YOLO_DEVICE="${YOLO_DEVICE:-0}"
export YOLO_BATCH="${YOLO_BATCH:-16}"
export YOLO_WORKERS="${YOLO_WORKERS:-4}"
export YOLO_PATIENCE="${YOLO_PATIENCE:-25}"

python scripts/remote/train_e01_to_e06.py

echo "[HPC RUN] E01-E06 queue complete"
