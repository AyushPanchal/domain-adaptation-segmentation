# Remote Training Notes

This project is designed so dataset preparation and result collection can happen
locally, while training can run on Kaggle or college GPU servers.

## Environment Variables

Training scripts should resolve paths from environment variables when present:

```bash
export DATA_ROOT=/path/to/data
export OUTPUT_ROOT=/path/to/runs
```

Kaggle example:

```bash
export DATA_ROOT=/kaggle/input/indraeye-mga
export OUTPUT_ROOT=/kaggle/working/runs
```

College GPU example:

```bash
export DATA_ROOT=/home/$USER/datasets/indraeye-mga
export OUTPUT_ROOT=/home/$USER/runs/domain-adaptation-segmentation
```

## Required Artifacts To Bring Back

For each experiment, copy back:

- `status.json`
- `timestamps.json`
- `command.txt`
- `stdout.log`
- `stderr.log`
- `results.csv`
- `metrics.json`
- `best.pt` or a note if weights are too large
- qualitative predictions, if generated

## Progress Visibility

Every training run should:

- stream output to terminal
- write output to `stdout.log` and `stderr.log`
- update `status.json`
- preserve partial logs on failure

## Live Watch Command

From the repository root on a remote machine:

```bash
export PYTHONPATH=$PWD/src
bash scripts/remote/watch_runs.sh runs/yolo11s_100ep_v1 40
```

This displays experiment statuses, the active/latest run, latest `results.csv`
row if available, and the tail of `stdout.log`.

## One Experiment At A Time On Slurm

Use the serial Slurm array for the main YOLO11s E01-E06 run. The array is
declared as `--array=1-6%1`, so Slurm will keep at most one experiment task
running at any time.

```bash
git pull
conda activate domainseg
export PYTHONPATH=$PWD/src

export OUTPUT_ROOT=$PWD/runs/yolo11s_100ep_serial
export REPORT_DIR=$PWD/reports/tables/yolo11s_100ep_serial
export YOLO_BATCH=16
export YOLO_WORKERS=0
export YOLO_EPOCHS=100
export YOLO_PATIENCE=25

bash scripts/remote/submit_yolo11s_serial_array.sh
```

If a node is unstable, pass normal `sbatch` options through the helper:

```bash
bash scripts/remote/submit_yolo11s_serial_array.sh --exclude=node1
```

Monitor it from the login node:

```bash
squeue -u "$USER"
bash scripts/remote/watch_runs.sh runs/yolo11s_100ep_serial 40
```

When all tasks finish, collect the final table:

```bash
python -m domain_adaptation_segmentation.training.collect_results \
  --runs-root runs/yolo11s_100ep_serial \
  --output-dir reports/tables/yolo11s_100ep_serial
```
