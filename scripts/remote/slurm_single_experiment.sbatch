#!/bin/bash
#SBATCH --job-name=mga_single
#SBATCH --output=logs/mga_single_%j.out
#SBATCH --error=logs/mga_single_%j.err
#SBATCH --partition=gpu
#SBATCH --gres=shard:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=06:00:00

set -euo pipefail

echo "========================================="
echo "MGA / BA-MGA Single YOLO Experiment"
echo "Job ID   : ${SLURM_JOB_ID:-unknown}"
echo "Node     : ${SLURM_NODELIST:-unknown}"
echo "Start    : $(date)"
echo "Submit   : ${SLURM_SUBMIT_DIR:-$PWD}"
echo "Config   : ${EXPERIMENT_CONFIG:-unset}"
echo "Epochs   : ${YOLO_EPOCHS:-config default}"
echo "========================================="

cd "${SLURM_SUBMIT_DIR:-$PWD}"

if [ -z "${EXPERIMENT_CONFIG:-}" ]; then
  echo "ERROR: set EXPERIMENT_CONFIG to a config YAML path."
  exit 2
fi

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
export YOLO_BATCH="${YOLO_BATCH:-2}"
export YOLO_WORKERS="${YOLO_WORKERS:-2}"
export YOLO_PATIENCE="${YOLO_PATIENCE:-25}"

EPOCH_ARGS=()
if [ -n "${YOLO_EPOCHS:-}" ]; then
  EPOCH_ARGS=(--epochs "$YOLO_EPOCHS")
fi

python -m domain_adaptation_segmentation.training.run_experiment \
  --config "$EXPERIMENT_CONFIG" \
  --output-root "$OUTPUT_ROOT" \
  --device "$YOLO_DEVICE" \
  "${EPOCH_ARGS[@]}" \
  --batch "$YOLO_BATCH" \
  --workers "$YOLO_WORKERS" \
  --patience "$YOLO_PATIENCE"

python -m domain_adaptation_segmentation.training.collect_results \
  --runs-root "$OUTPUT_ROOT" \
  --output-dir reports/tables

echo "========================================="
echo "Single experiment completed at: $(date)"
echo "========================================="
