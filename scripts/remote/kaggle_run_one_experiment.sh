#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${KAGGLE_REPO_DIR:-/kaggle/working/domain-adaptation-segmentation}"
cd "$REPO_DIR"

export PYTHONPATH="$REPO_DIR/src"
export OUTPUT_ROOT="${OUTPUT_ROOT:-/kaggle/working/runs/kaggle_single_e01}"
export REPORT_DIR="${REPORT_DIR:-reports/tables/kaggle_single_e01}"
export EXPERIMENT_CONFIG="${EXPERIMENT_CONFIG:-configs/experiments/e01_source_rgb_yolo11s.yaml}"
export YOLO_DEVICE="${YOLO_DEVICE:-0}"
export YOLO_EPOCHS="${YOLO_EPOCHS:-100}"
export YOLO_BATCH="${YOLO_BATCH:-8}"
export YOLO_WORKERS="${YOLO_WORKERS:-2}"
export YOLO_PATIENCE="${YOLO_PATIENCE:-25}"
export YOLO_RESUME="${YOLO_RESUME:-auto}"

RESUME_ARGS=()
case "$YOLO_RESUME" in
  auto)
    RESUME_ARGS=(--resume-if-available)
    ;;
  1|true|TRUE|yes|YES)
    RESUME_ARGS=(--resume)
    ;;
  0|false|FALSE|no|NO)
    RESUME_ARGS=()
    ;;
  *)
    echo "ERROR: YOLO_RESUME must be auto, true, or false."
    exit 2
    ;;
esac

echo "[KAGGLE RUN] repo       : $REPO_DIR"
echo "[KAGGLE RUN] config     : $EXPERIMENT_CONFIG"
echo "[KAGGLE RUN] output root: $OUTPUT_ROOT"
echo "[KAGGLE RUN] report dir : $REPORT_DIR"
echo "[KAGGLE RUN] device     : $YOLO_DEVICE"
echo "[KAGGLE RUN] epochs     : $YOLO_EPOCHS"
echo "[KAGGLE RUN] batch      : $YOLO_BATCH"
echo "[KAGGLE RUN] workers    : $YOLO_WORKERS"
echo "[KAGGLE RUN] resume     : $YOLO_RESUME"

python -m domain_adaptation_segmentation.training.run_experiment \
  --config "$EXPERIMENT_CONFIG" \
  --output-root "$OUTPUT_ROOT" \
  --device "$YOLO_DEVICE" \
  --epochs "$YOLO_EPOCHS" \
  --batch "$YOLO_BATCH" \
  --workers "$YOLO_WORKERS" \
  --patience "$YOLO_PATIENCE" \
  "${RESUME_ARGS[@]}"

python -m domain_adaptation_segmentation.training.collect_results \
  --runs-root "$OUTPUT_ROOT" \
  --output-dir "$REPORT_DIR"

echo "[KAGGLE RUN] done"
