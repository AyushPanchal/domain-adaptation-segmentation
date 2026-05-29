#!/bin/bash
#SBATCH --job-name=mga_env_diag
#SBATCH --output=logs/mga_env_diag_%j.out
#SBATCH --error=logs/mga_env_diag_%j.err
#SBATCH --partition=gpu
#SBATCH --gres=shard:1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:10:00

set -euo pipefail

echo "========================================="
echo "MGA / BA-MGA GPU Environment Diagnostic"
echo "Job ID   : ${SLURM_JOB_ID:-unknown}"
echo "Node     : ${SLURM_NODELIST:-unknown}"
echo "Start    : $(date)"
echo "Submit   : ${SLURM_SUBMIT_DIR:-$PWD}"
echo "========================================="

cd "${SLURM_SUBMIT_DIR:-$PWD}"

echo "[Before conda]"
echo "PATH=$PATH"
echo "LD_LIBRARY_PATH=${LD_LIBRARY_PATH:-<empty>}"
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi || true
  echo "[Before conda, empty LD_LIBRARY_PATH]"
  env -u LD_LIBRARY_PATH nvidia-smi || true
else
  echo "nvidia-smi not found before conda"
fi

source /apps/compilers/anaconda3-24.2/etc/profile.d/conda.sh
conda activate "${CONDA_ENV:-base}"
export PYTHONNOUSERSITE=1
source scripts/remote/hpc_cuda_env.sh
setup_conda_cuda_paths
print_python_gpu_diagnostics

echo "========================================="
echo "Diagnostic completed at: $(date)"
echo "========================================="
