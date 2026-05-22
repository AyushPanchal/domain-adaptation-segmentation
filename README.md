# Domain Adaptation Segmentation

This repository contains experiments for visible-to-thermal aerial instance
segmentation using YOLO segmentation models.

The central study compares gray-based source-domain augmentations for RGB to
IR segmentation:

- Source RGB baseline
- Full-image gray augmentation
- Box-guided gray augmentation
- Mask-guided gray augmentation (MGA)
- Boundary-aware mask-guided gray augmentation (BA-MGA)
- IR oracle baseline

The project is designed for portable execution on local machines, college GPU
servers, or Kaggle notebooks.

## Current Status

See [AGENT_HANDOFF.md](AGENT_HANDOFF.md) for the latest implementation status
and [EXPERIMENT_TRACKER.md](EXPERIMENT_TRACKER.md) for the experiment log.

## Planned Workflow

1. Copy the required IndraEye segmentation data into `data/raw/`.
2. Validate image, label, class, and split consistency.
3. Generate YOLO segmentation datasets for each augmentation setting.
4. Package datasets and configs for remote GPU training.
5. Run YOLO segmentation experiments.
6. Collect metrics, logs, model artifacts, and qualitative predictions.

