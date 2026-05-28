#!/bin/bash
#SBATCH --job-name=mga_e07_e08
#SBATCH --output=logs/mga_e07_e08_%j.out
#SBATCH --error=logs/mga_e07_e08_%j.err
#SBATCH --partition=gpu
#SBATCH --gres=shard:1
#SBATCH --cpus-per-task=12
#SBATCH --mem=64G
#SBATCH --time=24:00:00

set -euo pipefail

echo "========================================="
echo "MGA / BA-MGA YOLO11x Experiment Queue"
echo "Job ID   : ${SLURM_JOB_ID:-unknown}"
echo "Node     : ${SLURM_NODELIST:-unknown}"
echo "Start    : $(date)"
echo "Submit   : ${SLURM_SUBMIT_DIR:-$PWD}"
echo "========================================="

cd "${SLURM_SUBMIT_DIR:-$PWD}"

source /apps/compilers/anaconda3-24.2/etc/profile.d/conda.sh
conda activate "${CONDA_ENV:-base}"

echo "Python   : $(which python)"
python --version
python - <<'PY'
try:
    import torch
    print("Torch    :", torch.__version__)
    print("CUDA     :", torch.cuda.is_available(), torch.cuda.device_count())
except Exception as exc:
    print("Torch import failed:", exc)
PY

export REPO_ROOT="$PWD"
export PYTHONPATH="$PWD/src"
export OUTPUT_ROOT="${OUTPUT_ROOT:-$PWD/runs}"
export YOLO_DEVICE="${YOLO_DEVICE:-0}"
export YOLO_BATCH="${YOLO_BATCH:-8}"
export YOLO_WORKERS="${YOLO_WORKERS:-12}"
export YOLO_PATIENCE="${YOLO_PATIENCE:-25}"

bash scripts/remote/hpc_run_e07_e08.sh

echo "========================================="
echo "E07-E08 queue completed at: $(date)"
echo "========================================="
