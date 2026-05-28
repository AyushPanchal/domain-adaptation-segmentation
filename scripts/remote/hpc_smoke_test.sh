#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$PWD}"
cd "$REPO_ROOT"

export PYTHONPATH="$REPO_ROOT/src"
export OUTPUT_ROOT="${OUTPUT_ROOT:-$REPO_ROOT/runs}"
export YOLO_DEVICE="${YOLO_DEVICE:-0}"
export YOLO_WORKERS="${YOLO_WORKERS:-4}"

python -m domain_adaptation_segmentation.training.run_experiment \
  --config configs/experiments/e01_source_rgb_yolo11s.yaml \
  --output-root "$OUTPUT_ROOT" \
  --device "$YOLO_DEVICE" \
  --epochs 1 \
  --batch "${YOLO_BATCH:-8}" \
  --workers "$YOLO_WORKERS" \
  --patience 5

python -m domain_adaptation_segmentation.training.collect_results \
  --runs-root "$OUTPUT_ROOT" \
  --output-dir reports/tables

echo "[HPC SMOKE] done"
echo "[HPC SMOKE] run folder: $OUTPUT_ROOT/experiments/E01_source_rgb_yolo11s"

