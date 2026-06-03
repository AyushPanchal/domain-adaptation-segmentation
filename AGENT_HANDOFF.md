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
| 2026-06-02 | Completed Kaggle E01 full run | `downloads/full_e01_results.zip`; status completed on T4x2. Early stopped at epoch 35/100 with best epoch 10. Final best.pt validation: mask mAP50 0.221, mask mAP50-95 0.0961, box mAP50 0.236, box mAP50-95 0.163. |
| 2026-06-02 | Added dual eval outputs to Kaggle notebook | After training, `notebooks/kaggle_one_experiment_e01.ipynb` evaluates `best.pt` on `eval_ir` (IR-only, primary domain-transfer metric) and `eval_eo_ir` (EO val + IR val combined). Metrics are saved under `OUTPUT_ROOT/evaluations/*/metrics.json` and printed in the notebook. |
| 2026-06-02 | Completed E01 eval_ir and eval_eo_ir checks | E01 `best.pt` eval_ir: mask mAP50 0.2203, mask mAP50-95 0.0948, box mAP50 0.2362, box mAP50-95 0.1644. eval_eo_ir: mask mAP50 0.3386, mask mAP50-95 0.1669, box mAP50 0.3621, box mAP50-95 0.2603. |
| 2026-06-02 | Added Kaggle E02 full-gray notebook | Use `notebooks/kaggle_one_experiment_e02_full_gray.ipynb`. It generates full grayscale EO training images inside `/kaggle/working/generated/e02_full_gray`, trains YOLO11s-seg on T4x2, evaluates `best.pt` on `eval_ir` and `eval_eo_ir`, and packages `smoke_e02_results.zip` or `full_e02_results.zip`. |
| 2026-06-02 | Completed Kaggle E02 smoke run | `downloads/smoke_e02_results.zip`; status completed on T4x2 in 149.43 seconds. E02 smoke eval_ir: mask mAP50 0.1199, mask mAP50-95 0.0625, box mAP50 0.1232, box mAP50-95 0.0683. eval_eo_ir: mask mAP50 0.1197, mask mAP50-95 0.0605, box mAP50 0.1220, box mAP50-95 0.0692. |
| 2026-06-02 | Completed Kaggle E02 full run | `downloads/full_e02_results.zip`; status completed on T4x2. Early stopped at epoch 76/100 with best epoch 51. E02 `best.pt` eval_ir: mask mAP50 0.2274, mask mAP50-95 0.1040, box mAP50 0.2438, box mAP50-95 0.1548. eval_eo_ir: mask mAP50 0.2917, mask mAP50-95 0.1417, box mAP50 0.3194, box mAP50-95 0.2179. |
| 2026-06-02 | Added Kaggle E03 box-guided gray notebook | Use `notebooks/kaggle_one_experiment_e03_box_guided_gray.ipynb`. It generates box-guided grayscale EO training images inside `/kaggle/working/generated/e03_box_guided_gray`, skips class `4: Ignore`, trains YOLO11s-seg on T4x2, evaluates `best.pt` on `eval_ir` and `eval_eo_ir`, and packages `smoke_e03_results.zip` or `full_e03_results.zip`. |
| 2026-06-02 | Completed Kaggle E03 smoke run | `downloads/smoke_e03_results.zip`; status completed on T4x2 in 149.77 seconds. E03 smoke eval_ir: mask mAP50 0.1605, mask mAP50-95 0.0581, box mAP50 0.1651, box mAP50-95 0.1023. eval_eo_ir: mask mAP50 0.1636, mask mAP50-95 0.0603, box mAP50 0.1850, box mAP50-95 0.1213. |
| 2026-06-02 | Completed Kaggle E03 full run | `downloads/full_e03_results.zip`; status completed on T4x2. Early stopped at epoch 30/100 with best epoch 5. E03 `best.pt` eval_ir: mask mAP50 0.1972, mask mAP50-95 0.0811, box mAP50 0.2051, box mAP50-95 0.1342. eval_eo_ir: mask mAP50 0.1427, mask mAP50-95 0.0605, box mAP50 0.1553, box mAP50-95 0.1027. E03 underperformed E02 Full Gray on primary IR mask metrics. |
| 2026-06-02 | Added Kaggle E04 MGA notebook | Use `notebooks/kaggle_one_experiment_e04_mga.ipynb`. It generates polygon mask-guided grayscale EO training images inside `/kaggle/working/generated/e04_mga`, skips class `4: Ignore`, trains YOLO11s-seg on T4x2, evaluates `best.pt` on `eval_ir` and `eval_eo_ir`, and packages `smoke_e04_results.zip` or `full_e04_results.zip`. |
| 2026-06-02 | Completed Kaggle E04 smoke run | `downloads/smoke_e04_results.zip`; status completed on T4x2 in 149.26 seconds. E04 smoke eval_ir: mask mAP50 0.2006, mask mAP50-95 0.0812, box mAP50 0.2144, box mAP50-95 0.1384. eval_eo_ir: mask mAP50 0.1768, mask mAP50-95 0.0705, box mAP50 0.1987, box mAP50-95 0.1282. |
| 2026-06-02 | Completed Kaggle E04 full run | `downloads/full_e04_results.zip`; status completed on T4x2. Early stopped at epoch 26/100 with best epoch 1, so full-run `best.pt` metrics match smoke. E04 eval_ir: mask mAP50 0.2006, mask mAP50-95 0.0812, box mAP50 0.2144, box mAP50-95 0.1384. eval_eo_ir: mask mAP50 0.1768, mask mAP50-95 0.0705, box mAP50 0.1987, box mAP50-95 0.1282. E04 outperformed E03 but underperformed E02 Full Gray on primary IR mask metrics. |
| 2026-06-02 | Added Kaggle E09 joint EO+IR notebook | Use `notebooks/kaggle_one_experiment_e09_joint_eo_ir.ipynb`. It copies EO train and IR train into `/kaggle/working/generated/e09_joint_eo_ir/images/train` with filename prefixes, trains YOLO11s-seg on T4x2, evaluates `best.pt` on `eval_ir` and `eval_eo_ir`, and packages `smoke_e09_results.zip` or `full_e09_results.zip`. This is a supervised mixed-domain diagnostic, not an EO-only domain-transfer method. |
| 2026-06-02 | Completed Kaggle E09 smoke run | `downloads/smoke_e09_results.zip`; status completed on T4x2 in 223.11 seconds. E09 smoke eval_ir: mask mAP50 0.3854, mask mAP50-95 0.1823, box mAP50 0.4001, box mAP50-95 0.2747. eval_eo_ir: mask mAP50 0.3342, mask mAP50-95 0.1516, box mAP50 0.3602, box mAP50-95 0.2507. This confirms the pipeline/model can learn much better with IR supervision; low EO-only results are mostly domain shift. |
| 2026-06-03 | Completed Kaggle E09 full run | `downloads/full_e09_results.zip`; status completed on T4x2. Run resumed from epoch 42, early stopped at epoch 73/100, and best model was epoch 48. E09 eval_ir: mask mAP50 0.6691, mask mAP50-95 0.4229, box mAP50 0.6899, box mAP50-95 0.5640. eval_eo_ir: mask mAP50 0.5483, mask mAP50-95 0.3069, box mAP50 0.5774, box mAP50-95 0.4469. This is a supervised mixed-domain reference and should not be presented as EO-only adaptation. |
| 2026-06-03 | Added Kaggle N1 IR-only notebook | Use `notebooks/kaggle_one_experiment_n1_ir_only.ipynb`. It copies IR train into `/kaggle/working/generated/n1_ir_only/images/train`, trains YOLO11s-seg on T4x2, evaluates `best.pt` on `eval_ir` and `eval_eo_ir`, and packages `smoke_n1_results.zip` or `full_n1_results.zip`. This is the target-domain supervised baseline needed to interpret E09 EO+IR joint training. |
| 2026-06-03 | Completed Kaggle N1 smoke run | `downloads/smoke_n1_results.zip`; status completed on T4x2 in 165.58 seconds. N1 smoke eval_ir: mask mAP50 0.3703, mask mAP50-95 0.2051, box mAP50 0.3936, box mAP50-95 0.2739. eval_eo_ir: mask mAP50 0.2316, mask mAP50-95 0.1093, box mAP50 0.2485, box mAP50-95 0.1681. IR-only smoke is close to E09 EO+IR smoke on primary IR metrics. |
| 2026-06-03 | Completed Kaggle N1 full run | `downloads/full_n1_results.zip`; status completed on T4x2 in 2869.52 seconds. N1 eval_ir: mask mAP50 0.6530, mask mAP50-95 0.4342, box mAP50 0.7015, box mAP50-95 0.5743. eval_eo_ir: mask mAP50 0.3233, mask mAP50-95 0.1902, box mAP50 0.3660, box mAP50-95 0.2894. N1 completed 100/100 epochs after resume; best training-row mask mAP50-95 was at epoch 81. Compared with E09, IR-only is slightly lower on IR mask mAP50 but slightly higher on IR mask mAP50-95 and box metrics; E09 remains much better for combined EO+IR evaluation. |
| 2026-06-03 | Added Kaggle N2 balanced EO+IR notebook | Use `notebooks/kaggle_one_experiment_n2_balanced_eo_ir.ipynb`. It samples equal EO and IR training image/label pairs with fixed `BALANCE_SEED=42`, copies them into `/kaggle/working/generated/n2_balanced_eo_ir/images/train`, writes `balance_manifest.json`, trains YOLO11s-seg on T4x2, evaluates `best.pt` on `eval_ir` and `eval_eo_ir`, and packages `smoke_n2_results.zip` or `full_n2_results.zip`. |

## Next Recommended Actions

1. Run N2 smoke on Kaggle T4 x2 with `RUN_STAGE="smoke"` in `notebooks/kaggle_one_experiment_n2_balanced_eo_ir.ipynb`.
2. Download `/kaggle/working/smoke_n2_results.zip` and inspect it before the full run.
3. If smoke passes, run N2 full and compare against E09 and N1 using the same `eval_ir` and `eval_eo_ir` metrics.

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
