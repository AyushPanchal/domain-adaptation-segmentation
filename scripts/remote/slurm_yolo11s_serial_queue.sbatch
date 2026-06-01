#!/bin/bash
#SBATCH --job-name=mga_y11s_queue
#SBATCH --output=logs/mga_y11s_queue_%j.out
#SBATCH --error=logs/mga_y11s_queue_%j.err
#SBATCH --partition=gpu
#SBATCH --gres=shard:10
#SBATCH --cpus-per-task=12
#SBATCH --mem=64G
#SBATCH --time=24:00:00

set -euo pipefail

echo "========================================="
echo "MGA / BA-MGA YOLO11s Serial Queue"
echo "Job ID   : ${SLURM_JOB_ID:-unknown}"
echo "Node     : ${SLURM_NODELIST:-unknown}"
echo "Start    : $(date)"
echo "Submit   : ${SLURM_SUBMIT_DIR:-$PWD}"
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
export YOLO_DEVICE="${YOLO_DEVICE:-0}"
export YOLO_EPOCHS="${YOLO_EPOCHS:-100}"
export YOLO_BATCH="${YOLO_BATCH:-16}"
export YOLO_WORKERS="${YOLO_WORKERS:-0}"
export YOLO_PATIENCE="${YOLO_PATIENCE:-25}"

python scripts/remote/train_e01_to_e06.py \
  --repo-root "$REPO_ROOT" \
  --output-root "$OUTPUT_ROOT" \
  --device "$YOLO_DEVICE" \
  --epochs "$YOLO_EPOCHS" \
  --batch "$YOLO_BATCH" \
  --workers "$YOLO_WORKERS" \
  --patience "$YOLO_PATIENCE" \
  --reports-dir "${REPORT_DIR:-reports/tables/yolo11s_100ep_serial}"

echo "========================================="
echo "Serial queue completed at: $(date)"
echo "========================================="
