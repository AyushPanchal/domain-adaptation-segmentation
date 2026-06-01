#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/remote/watch_runs.sh <runs-root> [tail-lines]"
  echo "Example: bash scripts/remote/watch_runs.sh runs/yolo11s_100ep_v1 40"
  exit 1
fi

export PYTHONPATH="${PYTHONPATH:-$PWD/src}"
RUNS_ROOT="$1"
TAIL_LINES="${2:-40}"

python -m domain_adaptation_segmentation.training.watch_runs \
  --runs-root "$RUNS_ROOT" \
  --tail "$TAIL_LINES" \
  --interval 10

