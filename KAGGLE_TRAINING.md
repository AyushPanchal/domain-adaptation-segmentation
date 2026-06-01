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

It is a single-notebook workflow for one experiment. It:

- runs a smoke test first with `RUN_STAGE="smoke"`
- switches to the full 100-epoch run later with `RUN_STAGE="full"`
- streams logs live in each notebook cell
- prints `status.json`, the latest `results.csv` rows, and key mask/box metrics
- packages run outputs and report tables at the end

For Kaggle, the final zip is exposed as a notebook file/link. For Colab, the
same final cell calls `google.colab.files.download(...)` to start a browser
download automatically.

The Kaggle smoke result zip is:

```text
/kaggle/working/smoke_e01_results.zip
```

The Kaggle full-run result zip is:

```text
/kaggle/working/full_e01_results.zip
```

Default settings use both Kaggle T4 GPUs:

```text
EXPERIMENT_CONFIG=configs/experiments/e01_source_rgb_yolo11s.yaml
OUTPUT_ROOT=/kaggle/working/runs/kaggle_single_e01_smoke  # smoke
OUTPUT_ROOT=/kaggle/working/runs/kaggle_single_e01_full   # full
YOLO_DEVICE=0,1
YOLO_BATCH=16
YOLO_WORKERS=2
YOLO_EPOCHS=1    # smoke
YOLO_EPOCHS=100  # full
YOLO_RESUME=auto
```

The same run can also be launched from a notebook cell or Kaggle terminal:

```bash
cd /kaggle/working/domain-adaptation-segmentation
export OUTPUT_ROOT=/kaggle/working/runs/kaggle_single_e01
export EXPERIMENT_CONFIG=configs/experiments/e01_source_rgb_yolo11s.yaml
export YOLO_DEVICE=0,1
export YOLO_BATCH=16
export YOLO_WORKERS=2
export YOLO_EPOCHS=100
export YOLO_PATIENCE=25
export YOLO_RESUME=auto
bash scripts/remote/kaggle_run_one_experiment.sh
```

If dual-GPU training is unstable in Kaggle, fall back to `YOLO_DEVICE=0` and
`YOLO_BATCH=8` for debugging.

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
