# Kaggle Training

Target hardware: Kaggle T4 x2.

## Recommended: Direct Kaggle Dataset Workflow

Use the existing Kaggle dataset instead of uploading the full project ZIP:

[ayushbpanchal/indraeye-seg](https://www.kaggle.com/datasets/ayushbpanchal/indraeye-seg)

In the Kaggle notebook:

1. Add the dataset `ayushbpanchal/indraeye-seg`.
2. Select accelerator `GPU T4 x2`.
3. Enable Internet so the notebook can clone the GitHub code repo and install
   packages.
4. Open/run one notebook:

```text
notebooks/kaggle_one_experiment_e01.ipynb                 # E01 Source RGB
notebooks/kaggle_one_experiment_e02_full_gray.ipynb       # E02 Full Gray
notebooks/kaggle_one_experiment_e03_box_guided_gray.ipynb # E03 Box-Guided Gray
notebooks/kaggle_one_experiment_e04_mga.ipynb             # E04 MGA
notebooks/kaggle_one_experiment_e09_joint_eo_ir.ipynb     # E09 EO+IR supervised diagnostic
notebooks/kaggle_one_experiment_n1_ir_only.ipynb          # N1 IR-only supervised baseline
notebooks/kaggle_one_experiment_n2_balanced_eo_ir.ipynb   # N2 balanced EO+IR supervised baseline
notebooks/kaggle_one_experiment_n3_joint_eo_ir_yolo11l.ipynb # N3 EO+IR YOLO11l large-model baseline
notebooks/kaggle_one_experiment_n4_ir_only_yolo11l.ipynb  # N4 IR-only YOLO11l specialist
notebooks/kaggle_ensemble_n3_n4_yolo11l.ipynb             # N6 N3+N4 mask-aware ensemble evaluation
```

The notebook uses:

```text
/kaggle/input/datasets/ayushbpanchal/indraeye-seg/eo/images/train
/kaggle/input/datasets/ayushbpanchal/indraeye-seg/eo/labels/train
/kaggle/input/datasets/ayushbpanchal/indraeye-seg/ir/images/val
/kaggle/input/datasets/ayushbpanchal/indraeye-seg/ir/labels/val
```

It auto-detects this path and also falls back to `/kaggle/input/indraeye-seg`
if Kaggle mounts the dataset using the shorter slug. It creates a small YOLO
dataset YAML inside `/kaggle/working`, then runs the selected experiment. No
large ZIP upload is required.

Start with:

```python
RUN_STAGE = "smoke"
```

After smoke passes, change only:

```python
RUN_STAGE = "full"
```

Defaults:

```text
YOLO_DEVICE=0,1
YOLO_BATCH=16
YOLO_WORKERS=2
YOLO_EPOCHS=1    # smoke
YOLO_EPOCHS=100  # full
```

The notebook prints logs live, prints metrics in the notebook, and creates one
of these result zips:

```text
/kaggle/working/smoke_e01_results.zip
/kaggle/working/full_e01_results.zip
/kaggle/working/smoke_e02_results.zip
/kaggle/working/full_e02_results.zip
/kaggle/working/smoke_e03_results.zip
/kaggle/working/full_e03_results.zip
/kaggle/working/smoke_e04_results.zip
/kaggle/working/full_e04_results.zip
/kaggle/working/smoke_e09_results.zip
/kaggle/working/full_e09_results.zip
/kaggle/working/smoke_n1_results.zip
/kaggle/working/full_n1_results.zip
/kaggle/working/smoke_n2_results.zip
/kaggle/working/full_n2_results.zip
/kaggle/working/smoke_n3_results.zip
/kaggle/working/full_n3_results.zip
/kaggle/working/smoke_n4_results.zip
/kaggle/working/full_n4_results.zip
/kaggle/working/n6_n3_n4_ensemble_results.zip
```

After training, the notebook evaluates `best.pt` on two validation settings:

```text
eval_ir     = IR validation only
eval_eo_ir  = EO validation + IR validation combined
```

Use `eval_ir` as the primary RGB-to-IR domain-transfer metric. Use
`eval_eo_ir` as the combined overall-validation metric.

For N6, add `full_n3_results.zip` and `full_n4_results.zip` as Kaggle input
files, or place them in `/kaggle/working`. The notebook extracts each
experiment's `best.pt`, runs a mask-aware N3+N4 ensemble evaluation, prints
deltas against the standalone N3/N4 baselines, and packages
`/kaggle/working/n6_n3_n4_ensemble_results.zip`.

Kaggle cannot silently auto-download local files from the kernel, but the final
cell displays a `FileLink` and the zip also appears in the Output/Files panel.
In Colab, the same cell uses `google.colab.files.download(...)`.

## Optional: Upload / Working Directory Package

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

## Optional Package Setup

```bash
cd /kaggle/working/domain-adaptation-segmentation
bash scripts/remote/kaggle_setup.sh
```

## Optional Package Smoke Test

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

## Direct One-Experiment Notebook

```text
notebooks/kaggle_one_experiment_e01.ipynb
notebooks/kaggle_one_experiment_e02_full_gray.ipynb
notebooks/kaggle_one_experiment_e03_box_guided_gray.ipynb
notebooks/kaggle_one_experiment_e04_mga.ipynb
notebooks/kaggle_one_experiment_e09_joint_eo_ir.ipynb
notebooks/kaggle_one_experiment_n1_ir_only.ipynb
notebooks/kaggle_one_experiment_n2_balanced_eo_ir.ipynb
notebooks/kaggle_one_experiment_n3_joint_eo_ir_yolo11l.ipynb
notebooks/kaggle_one_experiment_n4_ir_only_yolo11l.ipynb
```

Each notebook is a single-experiment workflow. It:

- runs a smoke test first with `RUN_STAGE="smoke"`
- switches to the full 100-epoch run later with `RUN_STAGE="full"`
- streams logs live in each notebook cell
- prints `status.json`, the latest `results.csv` rows, and key mask/box metrics
- evaluates `best.pt` on `eval_ir` and `eval_eo_ir`
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
/kaggle/working/full_e02_results.zip
/kaggle/working/full_e03_results.zip
/kaggle/working/full_e04_results.zip
/kaggle/working/full_e09_results.zip
/kaggle/working/full_n1_results.zip
/kaggle/working/full_n2_results.zip
/kaggle/working/full_n3_results.zip
/kaggle/working/full_n4_results.zip
```

Default settings use both Kaggle T4 GPUs:

```text
DATASET_ROOT=/kaggle/input/datasets/ayushbpanchal/indraeye-seg
EXPERIMENT_CONFIG=configs/experiments/e01_kaggle_direct_source_rgb_yolo11s.yaml
EXPERIMENT_CONFIG=configs/experiments/e02_kaggle_full_gray_yolo11s.yaml
EXPERIMENT_CONFIG=configs/experiments/e03_kaggle_box_guided_gray_yolo11s.yaml
EXPERIMENT_CONFIG=configs/experiments/e04_kaggle_mga_yolo11s.yaml
EXPERIMENT_CONFIG=configs/experiments/e09_kaggle_joint_eo_ir_yolo11s.yaml
EXPERIMENT_CONFIG=configs/experiments/n1_kaggle_ir_only_yolo11s.yaml
EXPERIMENT_CONFIG=configs/experiments/n2_kaggle_balanced_eo_ir_yolo11s.yaml
EXPERIMENT_CONFIG=configs/experiments/n3_kaggle_joint_eo_ir_yolo11l.yaml
EXPERIMENT_CONFIG=configs/experiments/n4_kaggle_ir_only_yolo11l.yaml
OUTPUT_ROOT=/kaggle/working/runs/kaggle_direct_e01_smoke  # smoke
OUTPUT_ROOT=/kaggle/working/runs/kaggle_direct_e01_full   # full
OUTPUT_ROOT=/kaggle/working/runs/kaggle_e02_full_gray_smoke
OUTPUT_ROOT=/kaggle/working/runs/kaggle_e02_full_gray_full
OUTPUT_ROOT=/kaggle/working/runs/kaggle_e03_box_guided_gray_smoke
OUTPUT_ROOT=/kaggle/working/runs/kaggle_e03_box_guided_gray_full
OUTPUT_ROOT=/kaggle/working/runs/kaggle_e04_mga_smoke
OUTPUT_ROOT=/kaggle/working/runs/kaggle_e04_mga_full
OUTPUT_ROOT=/kaggle/working/runs/kaggle_e09_joint_eo_ir_smoke
OUTPUT_ROOT=/kaggle/working/runs/kaggle_e09_joint_eo_ir_full
OUTPUT_ROOT=/kaggle/working/runs/kaggle_n1_ir_only_smoke
OUTPUT_ROOT=/kaggle/working/runs/kaggle_n1_ir_only_full
OUTPUT_ROOT=/kaggle/working/runs/kaggle_n2_balanced_eo_ir_smoke
OUTPUT_ROOT=/kaggle/working/runs/kaggle_n2_balanced_eo_ir_full
OUTPUT_ROOT=/kaggle/working/runs/kaggle_n3_joint_eo_ir_yolo11l_smoke
OUTPUT_ROOT=/kaggle/working/runs/kaggle_n3_joint_eo_ir_yolo11l_full
OUTPUT_ROOT=/kaggle/working/runs/kaggle_n4_ir_only_yolo11l_smoke
OUTPUT_ROOT=/kaggle/working/runs/kaggle_n4_ir_only_yolo11l_full
YOLO_DEVICE=0,1
YOLO_EVAL_DEVICE=0
YOLO_BATCH=16
YOLO_WORKERS=2
YOLO_EPOCHS=1    # smoke
YOLO_EPOCHS=100  # full
YOLO_RESUME=auto
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
