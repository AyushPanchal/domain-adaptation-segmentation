#!/usr/bin/env bash
set -euo pipefail

cd /kaggle/working/domain-adaptation-segmentation
pip install -q -r requirements.txt

export PYTHONPATH=/kaggle/working/domain-adaptation-segmentation/src
export OUTPUT_ROOT=/kaggle/working/runs
export YOLO_DEVICE=${YOLO_DEVICE:-0,1}
export YOLO_WORKERS=${YOLO_WORKERS:-2}
export YOLO_PATIENCE=${YOLO_PATIENCE:-25}

echo "PYTHONPATH=$PYTHONPATH"
echo "OUTPUT_ROOT=$OUTPUT_ROOT"
echo "YOLO_DEVICE=$YOLO_DEVICE"

