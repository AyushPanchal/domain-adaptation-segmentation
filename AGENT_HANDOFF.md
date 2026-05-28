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
- Experiments run: none

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
| 2026-05-28 | Added HPC training workflow | Use `HPC_TRAINING.md` and `scripts/remote/hpc_*.sh` after pulling on the cluster. |
| 2026-05-28 | Added Slurm batch wrappers | Use `scripts/remote/slurm_*.sbatch`; they follow the SVNIT manual GPU pattern with `--partition=gpu` and `--gres=shard:1`. |

## Next Recommended Actions

1. On HPC, pull latest code and run `bash scripts/remote/hpc_check.sh`.
2. Submit smoke test with `sbatch scripts/remote/slurm_smoke.sbatch`.
3. If smoke test passes, submit `sbatch scripts/remote/slurm_e01_to_e06.sbatch`.
4. After E01-E06 completes, submit `sbatch scripts/remote/slurm_e07_e08.sbatch`.
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
