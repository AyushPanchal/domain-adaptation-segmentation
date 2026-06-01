#!/bin/bash
#SBATCH --job-name=mga_y11s
#SBATCH --output=logs/mga_y11s_%A_%a.out
#SBATCH --error=logs/mga_y11s_%A_%a.err
#SBATCH --partition=gpu
#SBATCH --gres=shard:10
#SBATCH --cpus-per-task=12
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --array=1-6%1

set -euo pipefail

CONFIGS=(
  "configs/experiments/e01_source_rgb_yolo11s.yaml"
  "configs/experiments/e02_full_gray_yolo11s.yaml"
  "configs/experiments/e03_box_guided_gray_yolo11s.yaml"
  "configs/experiments/e04_mga_yolo11s.yaml"
  "configs/experiments/e05_ba_mga_yolo11s.yaml"
  "configs/experiments/e06_ir_oracle_yolo11s.yaml"
)

TASK_INDEX="${SLURM_ARRAY_TASK_ID:?SLURM_ARRAY_TASK_ID is required}"
CONFIG="${CONFIGS[$((TASK_INDEX - 1))]}"

echo "========================================="
echo "MGA / BA-MGA YOLO11s Serial Array"
echo "Array ID : ${SLURM_ARRAY_JOB_ID:-unknown}"
echo "Task ID  : ${SLURM_ARRAY_TASK_ID:-unknown}"
echo "Job ID   : ${SLURM_JOB_ID:-unknown}"
echo "Node     : ${SLURM_NODELIST:-unknown}"
echo "Start    : $(date)"
echo "Submit   : ${SLURM_SUBMIT_DIR:-$PWD}"
echo "Config   : $CONFIG"
echo "========================================="

cd "${SLURM_SUBMIT_DIR:-$PWD}"
mkdir -p logs

source /apps/compilers/anaconda3-24.2/etc/profile.d/conda.sh
conda activate "${CONDA_ENV:-domainseg}"
export PYTHONNOUSERSITE=1

source scripts/remote/hpc_cuda_env.sh
setup_conda_cuda_paths
print_python_gpu_diagnostics

export REPO_ROOT="$PWD"
export PYTHONPATH="$PWD/src"
export OUTPUT_ROOT="${OUTPUT_ROOT:-$PWD/runs/yolo11s_100ep_serial}"
export REPORT_DIR="${REPORT_DIR:-$PWD/reports/tables/yolo11s_100ep_serial}"
export YOLO_DEVICE="${YOLO_DEVICE:-0}"
export YOLO_EPOCHS="${YOLO_EPOCHS:-100}"
export YOLO_BATCH="${YOLO_BATCH:-16}"
export YOLO_WORKERS="${YOLO_WORKERS:-0}"
export YOLO_PATIENCE="${YOLO_PATIENCE:-25}"

python -m domain_adaptation_segmentation.training.run_experiment \
  --config "$CONFIG" \
  --output-root "$OUTPUT_ROOT" \
  --device "$YOLO_DEVICE" \
  --epochs "$YOLO_EPOCHS" \
  --batch "$YOLO_BATCH" \
  --workers "$YOLO_WORKERS" \
  --patience "$YOLO_PATIENCE"

python -m domain_adaptation_segmentation.training.collect_results \
  --runs-root "$OUTPUT_ROOT" \
  --output-dir "$REPORT_DIR"

echo "========================================="
echo "Task completed at: $(date)"
echo "========================================="
