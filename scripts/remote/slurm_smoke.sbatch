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

# Some cluster images expose an older system nvJitLink before the conda/PyTorch
# copy. Prefer conda's bundled CUDA helper libraries when present.
NVJITLINK_DIR="$(python - <<'PY'
from pathlib import Path
import sys
root = Path(sys.prefix)
candidates = list(root.glob("lib/python*/site-packages/nvidia/nvjitlink/lib"))
print(candidates[0] if candidates else "")
PY
)"
if [ -n "$NVJITLINK_DIR" ]; then
  export LD_LIBRARY_PATH="$NVJITLINK_DIR:${LD_LIBRARY_PATH:-}"
  echo "nvJitLink: $NVJITLINK_DIR"
fi

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

bash scripts/remote/hpc_check.sh
bash scripts/remote/hpc_smoke_test.sh

echo "========================================="
echo "Smoke test completed at: $(date)"
echo "========================================="
