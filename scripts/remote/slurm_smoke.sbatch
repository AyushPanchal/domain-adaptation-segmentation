#!/bin/bash
#SBATCH --job-name=mga_smoke
#SBATCH --output=logs/mga_smoke_%j.out
#SBATCH --error=logs/mga_smoke_%j.err
#SBATCH --partition=gpu
#SBATCH --gres=shard:1
#SBATCH --cpus-per-task=12
#SBATCH --mem=32G
#SBATCH --time=00:30:00

set -euo pipefail

echo "========================================="
echo "MGA / BA-MGA YOLO Segmentation Smoke Test"
echo "Job ID   : ${SLURM_JOB_ID:-unknown}"
echo "Node     : ${SLURM_NODELIST:-unknown}"
echo "Start    : $(date)"
echo "Submit   : ${SLURM_SUBMIT_DIR:-$PWD}"
echo "========================================="

cd "${SLURM_SUBMIT_DIR:-$PWD}"

source /apps/compilers/anaconda3-24.2/etc/profile.d/conda.sh
conda activate "${CONDA_ENV:-base}"
export PYTHONNOUSERSITE=1

source scripts/remote/hpc_cuda_env.sh
setup_conda_cuda_paths
print_python_gpu_diagnostics

export REPO_ROOT="$PWD"
export PYTHONPATH="$PWD/src"
export OUTPUT_ROOT="${OUTPUT_ROOT:-$PWD/runs}"
export YOLO_DEVICE="${YOLO_DEVICE:-0}"
export YOLO_BATCH="${YOLO_BATCH:-8}"
export YOLO_WORKERS="${YOLO_WORKERS:-12}"

bash scripts/remote/hpc_check.sh
bash scripts/remote/hpc_smoke_test.sh

echo "========================================="
echo "Smoke test completed at: $(date)"
echo "========================================="
