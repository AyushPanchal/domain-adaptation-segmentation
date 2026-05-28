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

## 4. Smoke Test

Run one epoch of E01:

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
export YOLO_DEVICE=0
export YOLO_BATCH=8
bash scripts/remote/hpc_run_e07_e08.sh
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

