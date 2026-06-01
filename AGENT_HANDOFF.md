# Agent Handoff Log

This file is the source of truth for continuing work with another coding agent.
Update it after every meaningful step.

## Project Goal

Build a clean, portable experiment repository for YOLO-based RGB-to-IR aerial
segmentation experiments using mask-guided gray augmentation.

## Naming

Avoid naming the method as a direct "SAGA" variant in code, configs, and paper
tables. Use:

- `MGA`: Mask-Guided Gray Augmentation
- `BA-MGA`: Boundary-Aware Mask-Guided Gray Augmentation
- `Box-Guided Gray`: box-level semantic gray baseline

SAGA can be cited in related work as prior box-level grayscale augmentation for
visible-to-thermal object detection.

## Current Repository State

- Repository directory: `domain-adaptation-segmentation`
- Scaffold status: initialized with docs, config placeholders, source package layout,
  and nested Git repository
- Dataset copied: yes, matched `.jpg`/`.txt` pairs under `data/raw/indraeye_seg`
- Augmentation code implemented: yes
- Training runner implemented: yes, with status/log/result collection helpers
- Remote packaging implemented: yes, Kaggle package script added
- Experiments run: HPC GPU smoke test passed for E01 on node2

## Completed Steps

| Date | Step | Notes |
|---|---|---|
| 2026-05-22 | Created project scaffold | Directory structure and initial docs added. |
| 2026-05-22 | Added experiment config placeholders | E01-E08 are represented under `configs/experiments/`. |
| 2026-05-22 | Initialized nested Git repository | First `git init` hit a stale lock; `.git/config.lock` was removed and init succeeded. |
| 2026-05-23 | Completed initial data discovery | See `DATA_DISCOVERY.md`; prepared YOLO segmentation data exists at `../datasets/indraeye_seg`. |
| 2026-05-23 | Resolved prepared-label class mapping | Use active 12-class mapping: `0 Bicycle ... 11 Van`; see `configs/classes/indraeye_seg_active12.yaml`. |
| 2026-05-23 | Copied and validated raw YOLO segmentation pairs | 5108 matched pairs, 125055 instances, 13 skipped unlabeled images, 0 validation issues. |
| 2026-05-23 | Generated processed augmentation datasets | `source_rgb`, `full_gray`, `box_guided_gray`, `mga`, `ba_mga`, and `ir_oracle`; processed validation has 0 issues. |
| 2026-05-23 | Added Kaggle training runner and packaging workflow | Use `KAGGLE_TRAINING.md`; package ZIP is generated locally under `artifacts/kaggle/`. |
| 2026-05-23 | Built Kaggle upload ZIP locally | `artifacts/kaggle/domain-adaptation-segmentation-kaggle.zip`, 26926 files, about 3.52 GB. |
| 2026-06-01 | Added live run watcher | Use `bash scripts/remote/watch_runs.sh <runs-root> 40` on cluster/Kaggle to monitor status, metrics, and stdout tail. |
| 2026-05-28 | Added HPC training workflow | Use `HPC_TRAINING.md` and `scripts/remote/hpc_*.sh` after pulling on the cluster. |
| 2026-05-28 | Added Slurm batch wrappers | Use `scripts/remote/slurm_*.sbatch`; they follow the SVNIT manual GPU pattern with `--partition=gpu` and `--gres=shard:1`. |
| 2026-05-29 | Patched HPC smoke environment checks | `git` is optional on compute nodes; Slurm scripts prepend conda `nvjitlink` when available to avoid PyTorch CUDA library mismatch. |
| 2026-05-29 | Added HPC GPU environment diagnostic job | Use `sbatch scripts/remote/slurm_env_diagnose.sbatch` if `nvidia-smi` or PyTorch CUDA imports fail. |
| 2026-05-29 | Isolated Slurm Python env from user site packages | Slurm scripts set `PYTHONNOUSERSITE=1` to avoid loading CUDA/PyTorch packages from `~/.local`. |
| 2026-05-29 | Added TorchVision as explicit dependency | HPC smoke reached Ultralytics import but failed without TorchVision package metadata; install matching `torchvision==0.20.1+cu124` for `torch==2.5.1+cu124`. |
| 2026-06-01 | HPC GPU smoke passed | Job `24475` ran YOLO11s-seg E01 for 1 epoch on node2/H100 with CUDA; `GPU_mem` reached about 4.08G and `reports/tables/summary_results.*` were written. |
| 2026-06-01 | Added single-experiment Slurm wrapper | Use `scripts/remote/slurm_single_experiment.sbatch` with `EXPERIMENT_CONFIG=...` when long queue jobs are cancelled by Slurm. |
| 2026-06-01 | Added `YOLO_EPOCHS` override for Slurm runs | Use `YOLO_EPOCHS=1` or small values to debug HPC scheduler kills without editing experiment YAMLs. |
| 2026-06-01 | Made smoke runner configurable | `slurm_smoke.sbatch` can now run any `EXPERIMENT_CONFIG` with `YOLO_EPOCHS`; use this path if other Slurm wrappers are cancelled. |
| 2026-06-01 | Added serial YOLO11s Slurm array | Use `bash scripts/remote/submit_yolo11s_serial_array.sh`; it submits E01-E06 with `--array=1-6%1`, so only one experiment can run at a time. Defaults: 100 epochs, batch 16, workers 0, patience 25. |
| 2026-06-01 | Hardened experiment runner paths and startup failures | Relative `--output-root` is now resolved under the repo root, preventing nested Ultralytics `runs/segment/runs/...` paths. If `yolo` cannot start, `status.json` is marked failed instead of staying in running state. |
| 2026-06-01 | Added single-job serial Slurm queue | Use `bash scripts/remote/submit_yolo11s_serial_queue.sh`; it submits only one Slurm job and runs E01-E06 sequentially inside it. This avoids `AssocMaxSubmitJobLimit` on clusters that count array tasks against the submit quota. |
| 2026-06-01 | Added checkpoint resume support | `run_experiment.py` supports `--resume` and `--resume-if-available`; `slurm_single_experiment.sbatch` defaults to `YOLO_RESUME=auto`. Re-submit the same experiment with the same `OUTPUT_ROOT` after cluster cancellation to continue from `ultralytics/train/weights/last.pt`. |
| 2026-06-02 | Added Kaggle direct one-experiment workflow | Use `notebooks/kaggle_one_experiment_e01.ipynb` with dataset `ayushbpanchal/indraeye-seg`; no large ZIP upload is needed. The notebook clones the small GitHub repo, writes a direct YOLO YAML using `/kaggle/input/datasets/ayushbpanchal/indraeye-seg` with fallback to `/kaggle/input/indraeye-seg`, and runs only E01. Defaults use T4x2: device `0,1`, batch 16, workers 2, resume auto. Use `RUN_STAGE="smoke"` for 1 epoch first and `RUN_STAGE="full"` for 100 epochs later. |

## Next Recommended Actions

1. On HPC, pull latest code.
2. Submit the serial main run with `bash scripts/remote/submit_yolo11s_serial_queue.sh`; this keeps only one E01-E06 experiment running at once while using only one submitted Slurm job.
3. Monitor with `bash scripts/remote/watch_runs.sh runs/yolo11s_100ep_serial 40`.
4. After E01-E06 completes, decide whether to run YOLO11x E07/E08.
5. Bring back `runs/` and `reports/` with WinSCP.

## Latest Data Discovery Summary

- Best candidate source: `../datasets/indraeye_seg`
- Labels are already YOLO segmentation polygon files.
- Image folders include both `.jpg` and `.json`; copy `.jpg` and `.txt` pairs.
- A small number of images have no matching labels.
- Important caveat: existing EO/IR YAML class mappings disagree in the parent
  workspace. This repo now uses the verified prepared-label mapping in
  `configs/classes/indraeye_seg_active12.yaml`.

## Copied Dataset Summary

- Raw copy root: `data/raw/indraeye_seg`
- Manifest root: `data/manifests`
- Copied pairs: 5108
- Skipped records: 13
- Validation issues: 0
- Instances: 125055
- EO train: 2024 images, 68414 instances
- EO val: 59 images, 2254 instances
- IR train: 2967 images, 53191 instances
- IR val: 58 images, 1196 instances

## Processed Dataset Summary

- Processed root: `data/processed`
- Generated dataset YAMLs: `data/manifests/dataset_yamls`
- Methods generated: `source_rgb`, `full_gray`, `box_guided_gray`, `mga`,
  `ba_mga`, `ir_oracle`
- Object-region augmentations skip class `4: Ignore`.
- BA-MGA feather radius: `3.0`
- Processed validation issues: 0
- Total instances across generated train/val datasets: 402437

## Known Constraints

- Training will likely run on college GPU resources or Kaggle, not the local
  computer.
- The system must preserve logs and partial results for failed runs.
- Keep bulky datasets, model weights, and training outputs out of Git.

## Important Paths

- Configs: `configs/`
- Source code: `src/domain_adaptation_segmentation/`
- Local raw data copy: `data/raw/`
- Generated datasets: `data/processed/`
- Experiment runs: `runs/experiments/`
- Result summaries: `reports/tables/`
