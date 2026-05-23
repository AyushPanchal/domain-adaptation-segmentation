#!/usr/bin/env bash
set -euo pipefail

cd /kaggle/working/domain-adaptation-segmentation
export PYTHONPATH=/kaggle/working/domain-adaptation-segmentation/src
export OUTPUT_ROOT=/kaggle/working/runs

CONFIGS=(
  configs/experiments/e01_source_rgb_yolo11s.yaml
  configs/experiments/e02_full_gray_yolo11s.yaml
  configs/experiments/e03_box_guided_gray_yolo11s.yaml
  configs/experiments/e04_mga_yolo11s.yaml
  configs/experiments/e05_ba_mga_yolo11s.yaml
  configs/experiments/e06_ir_oracle_yolo11s.yaml
)

for config in "${CONFIGS[@]}"; do
  python -m domain_adaptation_segmentation.training.run_experiment \
    --config "$config" \
    --output-root "$OUTPUT_ROOT" \
    --device "${YOLO_DEVICE:-0,1}" \
    --batch "${YOLO_BATCH:-16}" \
    --workers "${YOLO_WORKERS:-2}" \
    --patience "${YOLO_PATIENCE:-25}"

  python -m domain_adaptation_segmentation.training.collect_results \
    --runs-root "$OUTPUT_ROOT" \
    --output-dir reports/tables
done

