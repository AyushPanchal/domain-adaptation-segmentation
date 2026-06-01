#!/usr/bin/env bash
set -euo pipefail

mkdir -p logs

export OUTPUT_ROOT="${OUTPUT_ROOT:-$PWD/runs/yolo11s_100ep_serial}"
export REPORT_DIR="${REPORT_DIR:-reports/tables/yolo11s_100ep_serial}"
export CONDA_ENV="${CONDA_ENV:-domainseg}"
export YOLO_EPOCHS="${YOLO_EPOCHS:-100}"
export YOLO_BATCH="${YOLO_BATCH:-16}"
export YOLO_WORKERS="${YOLO_WORKERS:-0}"
export YOLO_PATIENCE="${YOLO_PATIENCE:-25}"

echo "[SUBMIT] single Slurm job: E01-E06 sequential queue"
echo "[SUBMIT] output root: $OUTPUT_ROOT"
echo "[SUBMIT] reports    : $REPORT_DIR"
echo "[SUBMIT] batch/workers/epochs: $YOLO_BATCH/$YOLO_WORKERS/$YOLO_EPOCHS"

sbatch "$@" scripts/remote/slurm_yolo11s_serial_queue.sbatch
