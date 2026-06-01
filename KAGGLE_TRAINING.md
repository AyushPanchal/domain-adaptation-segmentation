# Kaggle Training

Target hardware: Kaggle T4 x2.

## Upload / Working Directory

Create the Kaggle package locally:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\local\package_for_kaggle.ps1
```

Upload the generated ZIP as a Kaggle Dataset:

```text
artifacts/kaggle/domain-adaptation-segmentation-kaggle.zip
```

Latest local package size: about `3.52 GB` with all processed dataset variants.

Then unzip it in the notebook:

```python
import zipfile

zip_path = "/kaggle/input/<your-kaggle-dataset-name>/domain-adaptation-segmentation-kaggle.zip"
out_dir = "/kaggle/working/domain-adaptation-segmentation"

with zipfile.ZipFile(zip_path, "r") as zf:
    zf.extractall(out_dir)
```

After extraction, the repository should exist at:

```text
/kaggle/working/domain-adaptation-segmentation
```

The generated datasets should be present under:

```text
/kaggle/working/domain-adaptation-segmentation/data/processed
```

The raw copied data is not required for training once `data/processed` and
`data/manifests/dataset_yamls` are available.

## Setup

```bash
cd /kaggle/working/domain-adaptation-segmentation
bash scripts/remote/kaggle_setup.sh
```

## Smoke Test

Run one epoch on E01 first:

```bash
bash scripts/remote/kaggle_smoke_test.sh
```

This should create:

```text
/kaggle/working/runs/experiments/E01_source_rgb_yolo11s/
```

Watch progress in the notebook output or inspect:

```text
/kaggle/working/runs/experiments/E01_source_rgb_yolo11s/status.json
/kaggle/working/runs/experiments/E01_source_rgb_yolo11s/stdout.log
```

## One Full Experiment First

For the Kaggle trial, use the notebook:

```text
notebooks/kaggle_one_experiment_e01.ipynb
```

It extracts the uploaded project ZIP, installs dependencies, runs only E01, and
packages `/kaggle/working/runs` plus `reports` into:

```text
/kaggle/working/kaggle_single_e01_results.zip
```

Default settings are conservative for Kaggle T4:

```text
EXPERIMENT_CONFIG=configs/experiments/e01_source_rgb_yolo11s.yaml
OUTPUT_ROOT=/kaggle/working/runs/kaggle_single_e01
YOLO_DEVICE=0
YOLO_BATCH=8
YOLO_WORKERS=2
YOLO_EPOCHS=100
YOLO_RESUME=auto
```

The same run can also be launched from a notebook cell or Kaggle terminal:

```bash
cd /kaggle/working/domain-adaptation-segmentation
export OUTPUT_ROOT=/kaggle/working/runs/kaggle_single_e01
export EXPERIMENT_CONFIG=configs/experiments/e01_source_rgb_yolo11s.yaml
export YOLO_DEVICE=0
export YOLO_BATCH=8
export YOLO_WORKERS=2
export YOLO_EPOCHS=100
export YOLO_PATIENCE=25
export YOLO_RESUME=auto
bash scripts/remote/kaggle_run_one_experiment.sh
```

If E01 completes cleanly, try `YOLO_BATCH=16` or `YOLO_DEVICE=0,1` in a fresh
test. Keep `YOLO_DEVICE=0` for the first run because single-GPU training is
usually easier to debug inside notebooks.

## Main YOLO11s Queue

After the smoke test passes:

```bash
export YOLO_DEVICE=0,1
export YOLO_BATCH=16
export YOLO_WORKERS=2
export YOLO_PATIENCE=25
bash scripts/remote/kaggle_run_e01_to_e06.sh
```

If dual-GPU training is unstable in Kaggle, switch to:

```bash
export YOLO_DEVICE=0
export YOLO_BATCH=8
```

## Bring Back Results

After each run, preserve:

```text
/kaggle/working/runs
/kaggle/working/domain-adaptation-segmentation/reports/tables
```

Each experiment folder contains:

- `config.yaml`
- `command.txt`
- `status.json`
- `timestamps.json`
- `stdout.log`
- `stderr.log`
- `results.csv`
- `metrics.json` after result collection
- `ultralytics/train/weights/best.pt`
- `ultralytics/train/weights/last.pt`

## Live Monitoring

For any run queue, open a second terminal/session and run:

```bash
export PYTHONPATH=$PWD/src
bash scripts/remote/watch_runs.sh runs/yolo11s_100ep_v1 40
```

For a one-time snapshot:

```bash
python -m domain_adaptation_segmentation.training.watch_runs \
  --runs-root runs/yolo11s_100ep_v1 \
  --tail 40 \
  --once
```
