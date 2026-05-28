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

CONFIGS=(
  configs/experiments/e01_source_rgb_yolo11s.yaml
  configs/experiments/e02_full_gray_yolo11s.yaml
  configs/experiments/e03_box_guided_gray_yolo11s.yaml
  configs/experiments/e04_mga_yolo11s.yaml
  configs/experiments/e05_ba_mga_yolo11s.yaml
  configs/experiments/e06_ir_oracle_yolo11s.yaml
)

for config in "${CONFIGS[@]}"; do
  echo "[HPC RUN] starting $config"
  python -m domain_adaptation_segmentation.training.run_experiment \
    --config "$config" \
    --output-root "$OUTPUT_ROOT" \
    --device "$YOLO_DEVICE" \
    --batch "$YOLO_BATCH" \
    --workers "$YOLO_WORKERS" \
    --patience "$YOLO_PATIENCE"

  python -m domain_adaptation_segmentation.training.collect_results \
    --runs-root "$OUTPUT_ROOT" \
    --output-dir reports/tables
done

echo "[HPC RUN] E01-E06 queue complete"

