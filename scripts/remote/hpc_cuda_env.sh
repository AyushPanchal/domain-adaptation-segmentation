#!/usr/bin/env bash

setup_conda_cuda_paths() {
  # Prefer CUDA helper libraries bundled inside the active Python/conda
  # environment. This avoids accidentally selecting incompatible system copies.
  local nvjitlink_dir
  nvjitlink_dir="$(python - <<'PY'
from pathlib import Path
import sys

root = Path(sys.prefix)
version = f"python{sys.version_info.major}.{sys.version_info.minor}"
path = root / "lib" / version / "site-packages" / "nvidia" / "nvjitlink" / "lib"
print(path if path.exists() else "")
PY
)"

  if [ -n "$nvjitlink_dir" ]; then
    export LD_LIBRARY_PATH="$nvjitlink_dir:${LD_LIBRARY_PATH:-}"
    echo "nvJitLink: $nvjitlink_dir"
  else
    echo "nvJitLink: not found in active Python environment"
  fi
}

print_python_gpu_diagnostics() {
  echo "Python   : $(which python)"
  python --version
  echo "Conda env: ${CONDA_DEFAULT_ENV:-unknown}"
  echo "Conda prefix: ${CONDA_PREFIX:-unknown}"
  echo "PYTHONNOUSERSITE: ${PYTHONNOUSERSITE:-<unset>}"
  echo "LD_LIBRARY_PATH: ${LD_LIBRARY_PATH:-<empty>}"

  echo "nvidia-smi:"
  if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi || true
  else
    echo "nvidia-smi not found"
  fi

  echo "nvidia-smi with empty LD_LIBRARY_PATH:"
  if command -v nvidia-smi >/dev/null 2>&1; then
    env -u LD_LIBRARY_PATH nvidia-smi || true
  fi

  echo "Torch check:"
  python - <<'PY'
try:
    import torch
    print("Torch    :", torch.__version__)
    print("CUDA     :", torch.cuda.is_available(), torch.cuda.device_count())
    if torch.cuda.is_available():
        print("Device 0 :", torch.cuda.get_device_name(0))
except Exception as exc:
    print("Torch import failed:", exc)
PY
}
