#!/usr/bin/env bash
set -euo pipefail

cd /kaggle/working/domain-adaptation-segmentation
export PYTHONPATH=/kaggle/working/domain-adaptation-segmentation/src
export OUTPUT_ROOT=/kaggle/working/runs

python -m domain_adaptation_segmentation.training.run_experiment \
  --config configs/experiments/e01_source_rgb_yolo11s.yaml \
  --output-root "$OUTPUT_ROOT" \
  --device "${YOLO_DEVICE:-0}" \
  --epochs 1 \
  --batch 8 \
  --workers "${YOLO_WORKERS:-2}" \
  --patience 5

python -m domain_adaptation_segmentation.training.collect_results \
  --runs-root "$OUTPUT_ROOT" \
  --output-dir reports/tables

