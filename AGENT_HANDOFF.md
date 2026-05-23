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
- Dataset copied: no
- Augmentation code implemented: no
- Training runner implemented: no
- Remote packaging implemented: no
- Experiments run: none

## Completed Steps

| Date | Step | Notes |
|---|---|---|
| 2026-05-22 | Created project scaffold | Directory structure and initial docs added. |
| 2026-05-22 | Added experiment config placeholders | E01-E08 are represented under `configs/experiments/`. |
| 2026-05-22 | Initialized nested Git repository | First `git init` hit a stale lock; `.git/config.lock` was removed and init succeeded. |
| 2026-05-23 | Completed initial data discovery | See `DATA_DISCOVERY.md`; prepared YOLO segmentation data exists at `../datasets/indraeye_seg`. |

## Next Recommended Actions

1. Resolve/confirm the correct class mapping for EO and IR segmentation labels.
2. Add dataset validation and copy scripts.
3. Copy only matched `.jpg`/`.txt` pairs into the new repository.
4. Generate manifests for copied/skipped files and class counts.
5. Commit the dataset tooling and discovery notes.

## Latest Data Discovery Summary

- Best candidate source: `../datasets/indraeye_seg`
- Labels are already YOLO segmentation polygon files.
- Image folders include both `.jpg` and `.json`; copy `.jpg` and `.txt` pairs.
- A small number of images have no matching labels.
- Important caveat: existing EO/IR YAML class mappings disagree; resolve before
  training.

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
