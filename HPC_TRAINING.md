# HPC Training

Assumed cluster location:

```text
~/P24DS013/indraeye-obb/domain-adaptation-segmentation
```

## 1. Pull Latest Code

```bash
cd ~/P24DS013/indraeye-obb/domain-adaptation-segmentation
git pull origin main
```

## 2. Activate Environment

Use the Python/conda environment available on the cluster. Then install missing
dependencies if needed:

```bash
pip install -r requirements.txt
```

If the cluster has a module system, load CUDA/Python modules first according to
local HPC rules.

## 3. Check Setup

```bash
bash scripts/remote/hpc_check.sh
```

This verifies:

- Python
- Git commit
- `data/processed`
- dataset YAMLs
- GPU visibility
- Ultralytics import

If `git` is not available inside a compute job, the check script will skip the
commit check. That is okay.

If PyTorch fails with an error involving `libcusparse.so.12` and
`__nvJitLinkAddData`, the Slurm scripts try to prefer conda's bundled
`nvjitlink` library automatically. If it still fails, create/use a clean conda
environment with a PyTorch build matching the cluster CUDA module, then submit
with:

```bash
CONDA_ENV=<your_env_name> sbatch scripts/remote/slurm_smoke.sbatch
```

## 4. Smoke Test

The SVNIT manual says GPU jobs should run through Slurm. Prefer `sbatch`:

```bash
sbatch scripts/remote/slurm_smoke.sbatch
squeue
```

Watch logs:

```bash
tail -f logs/mga_smoke_<jobid>.out
tail -f logs/mga_smoke_<jobid>.err
```

If you are inside an allocated GPU job and need to run manually, use:

```bash
export YOLO_DEVICE=0
export YOLO_BATCH=8
bash scripts/remote/hpc_smoke_test.sh
```

The run folder will be:

```text
runs/experiments/E01_source_rgb_yolo11s
```

Useful live/partial files:

```text
runs/experiments/E01_source_rgb_yolo11s/status.json
runs/experiments/E01_source_rgb_yolo11s/stdout.log
runs/experiments/E01_source_rgb_yolo11s/results.csv
```

## 5. Main Runs

After the smoke test passes:

```bash
sbatch scripts/remote/slurm_e01_to_e06.sbatch
squeue
```

To watch:

```bash
tail -f logs/mga_e01_e06_<jobid>.out
```

The underlying direct command is:

```bash
export YOLO_DEVICE=0
export YOLO_BATCH=16
export YOLO_WORKERS=4
bash scripts/remote/hpc_run_e01_to_e06.sh
```

If memory fails, reduce batch:

```bash
export YOLO_BATCH=8
```

After E01-E06 complete, run the large model comparison:

```bash
sbatch scripts/remote/slurm_e07_e08.sbatch
```

Underlying direct command:

```bash
export YOLO_DEVICE=0
export YOLO_BATCH=8
bash scripts/remote/hpc_run_e07_e08.sh
```

## Slurm Notes

The batch scripts use:

```text
#SBATCH --partition=gpu
#SBATCH --gres=shard:1
#SBATCH --cpus-per-task=12
```

The user manual FAQ says not to explicitly specify a node number, so the scripts
do not use `--nodelist`.

The default conda environment name is:

```text
base
```

Override it at submit time if your environment has another name:

```bash
CONDA_ENV=my_env sbatch scripts/remote/slurm_smoke.sbatch
```

## 6. Bring Results Back

Use WinSCP for large folders:

```text
runs/
reports/
```

Git should only be used for small summaries such as:

```text
reports/tables/summary_results.csv
reports/tables/summary_results.json
```
