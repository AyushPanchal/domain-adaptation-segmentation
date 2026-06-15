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
| 2026-06-03 | Completed Kaggle N2 smoke run | `downloads/smoke_n2_results.zip`; status completed on T4x2 in 196.69 seconds. Balance manifest: raw EO 2024, raw IR 2967, balanced train pairs 2024 per domain, total train pairs 4048. N2 smoke eval_ir: mask mAP50 0.3529, mask mAP50-95 0.1897, box mAP50 0.3699, box mAP50-95 0.2570. eval_eo_ir: mask mAP50 0.3280, mask mAP50-95 0.1676, box mAP50 0.3528, box mAP50-95 0.2481. Smoke passed; full N2 is ready to run. |
| 2026-06-03 | Completed Kaggle N2 full run | `downloads/full_n2_results.zip`; status completed on T4x2 in 6174.00 seconds. Balance manifest: raw EO 2024, raw IR 2967, balanced train pairs 2024 per domain, total train pairs 4048. N2 eval_ir: mask mAP50 0.6407, mask mAP50-95 0.4031, box mAP50 0.6680, box mAP50-95 0.5325. eval_eo_ir: mask mAP50 0.5251, mask mAP50-95 0.2969, box mAP50 0.5618, box mAP50-95 0.4321. Early stopped at epoch 56/100; best epoch 31. N2 is much stronger than N1 on combined EO+IR, but E09 remains the best mixed-domain model overall. |
| 2026-06-03 | Added Kaggle N3 joint EO+IR YOLO11l notebook | Use `notebooks/kaggle_one_experiment_n3_joint_eo_ir_yolo11l.ipynb`. It follows the E09 full EO+IR training recipe but upgrades the model to `yolo11l-seg.pt` and uses `YOLO_BATCH=8` for safer T4x2 memory. It evaluates `best.pt` on `eval_ir` and `eval_eo_ir`, and packages `smoke_n3_results.zip` or `full_n3_results.zip`. |
| 2026-06-03 | Completed Kaggle N3 smoke run | `downloads/smoke_n3_results.zip`; status completed on T4x2 in 310.04 seconds. N3 smoke eval_ir: mask mAP50 0.3996, mask mAP50-95 0.1986, box mAP50 0.4302, box mAP50-95 0.3200. eval_eo_ir: mask mAP50 0.3429, mask mAP50-95 0.1630, box mAP50 0.3804, box mAP50-95 0.2795. YOLO11l trained with `device=0,1`, `batch=8`, and peak displayed GPU_mem about 4.7G, so the full N3 run is safe to launch. |
| 2026-06-04 | Completed Kaggle N3 full run | `downloads/full_n3_results.zip`; status completed on T4x2 in 5898.00 seconds. N3 eval_ir: mask mAP50 0.6968, mask mAP50-95 0.4555, box mAP50 0.7167, box mAP50-95 0.6099. eval_eo_ir: mask mAP50 0.5823, mask mAP50-95 0.3308, box mAP50 0.6192, box mAP50-95 0.5025. Run resumed from `last.pt`; final status recorded epoch 95/100, and early stopping reported best epoch 70. This is the strongest mixed-domain result so far and beats E09 on both IR-only and combined EO+IR evaluation. |
| 2026-06-04 | Added Kaggle N4 IR-only YOLO11l notebook | Use `notebooks/kaggle_one_experiment_n4_ir_only_yolo11l.ipynb`. It follows the N1 IR-only training recipe but upgrades the model to `yolo11l-seg.pt` and uses `YOLO_BATCH=8` for safer T4x2 memory. It evaluates `best.pt` on `eval_ir` and `eval_eo_ir`, and packages `smoke_n4_results.zip` or `full_n4_results.zip`. This is the IR specialist needed before testing an N3+N4 ensemble. |
| 2026-06-04 | Completed Kaggle N4 smoke run | `downloads/smoke_n4_results.zip`; status completed on T4x2 in 208.76 seconds. N4 smoke eval_ir: mask mAP50 0.3904, mask mAP50-95 0.2039, box mAP50 0.4242, box mAP50-95 0.3103. eval_eo_ir: mask mAP50 0.2359, mask mAP50-95 0.1114, box mAP50 0.2651, box mAP50-95 0.1872. Smoke passed; full N4 is ready to run. |
| 2026-06-04 | Completed Kaggle N4 full run | `downloads/full_n4_results.zip`; status completed on T4x2 in 12853.39 seconds. N4 eval_ir: mask mAP50 0.6555, mask mAP50-95 0.4438, box mAP50 0.7056, box mAP50-95 0.5943. eval_eo_ir: mask mAP50 0.3448, mask mAP50-95 0.1984, box mAP50 0.3768, box mAP50-95 0.3011. Completed 100/100 epochs; best training-row mask mAP50-95 was epoch 79. N4 improves over N1 slightly but remains below N3, so use it as the first ensemble candidate with N3 rather than as the new best standalone model. |
| 2026-06-05 | Added N6 N3+N4 ensemble evaluator and Kaggle notebook | New module: `src/domain_adaptation_segmentation/training/evaluate_segmentation_ensemble.py`. New notebook: `notebooks/kaggle_ensemble_n3_n4_yolo11l.ipynb`. The evaluator performs cross-model NMS over raw predictions and reconstructs masks with each selected candidate's own source-model prototype, avoiding the standard Ultralytics ensemble limitation for segmentation masks. The notebook searches `/kaggle/input` and `/kaggle/working` for `full_n3_results.zip` and `full_n4_results.zip`, extracts `best.pt`, evaluates `eval_ir` and `eval_eo_ir`, prints deltas against N3/N4, and packages `n6_n3_n4_ensemble_results.zip`. A local one-image CPU smoke test passed. |
| 2026-06-05 | Completed Kaggle N6 N3+N4 ensemble evaluation | `downloads/n6_n3_n4_ensemble_results.zip`; eval_ir: mask mAP50 0.6910, mask mAP50-95 0.4553, box mAP50 0.7171, box mAP50-95 0.6143. eval_eo_ir: mask mAP50 0.5462, mask mAP50-95 0.3139, box mAP50 0.5828, box mAP50-95 0.4749. Compared with N3, N6 is slightly better on IR box metrics (+0.0004 box mAP50, +0.0044 box mAP50-95) but slightly lower on IR mask mAP50-95 (-0.0002) and clearly lower on combined EO+IR. Treat N6 as an ensemble ablation, not the best model. |
| 2026-06-05 | Added Kaggle N7 high-resolution N3-style notebook | Use `notebooks/kaggle_one_experiment_n7_joint_eo_ir_yolo11l_img960.ipynb`. It follows the N3 EO+IR YOLO11l recipe but changes only the resolution axis: `imgsz=960`, `batch=4`, `device=0,1`, eval on `eval_ir` and `eval_eo_ir`. Run smoke first and inspect memory/runtime before attempting full. This is the next best chance for a real mask-quality gain because it targets small-object and boundary detail without changing model family. |
| 2026-06-05 | Completed Kaggle N7 high-resolution smoke run | `downloads/smoke_n7_results.zip`; status completed in 543.78 seconds with `imgsz=960`, batch=4, device=0,1. Parsed peak GPU memory from stdout was about 9.01G. N7 smoke eval_ir: mask mAP50 0.3871, mask mAP50-95 0.2413, box mAP50 0.4038, box mAP50-95 0.2933. eval_eo_ir: mask mAP50 0.3589, mask mAP50-95 0.2208, box mAP50 0.3836, box mAP50-95 0.2831. Compared with N3 smoke, N7 is lower on IR mask mAP50 but better on strict mask mAP50-95 for both IR and EO+IR. Full N7 is worth running. |
| 2026-06-06 | Completed Kaggle N7 high-resolution full run | `downloads/full_n7_results.zip`; status completed in 17837.79 seconds after resume with `imgsz=960`, batch=4, device=0,1. N7 eval_ir: mask mAP50 0.7025, mask mAP50-95 0.5250, box mAP50 0.7192, box mAP50-95 0.6128. eval_eo_ir: mask mAP50 0.6163, mask mAP50-95 0.4310, box mAP50 0.6383, box mAP50-95 0.5244. This is the new best result and beats N3 by +0.0695 on IR mask mAP50-95 and +0.1002 on EO+IR mask mAP50-95. Early stopping reported best epoch 51; training CSV best mask row was epoch 68. |
| 2026-06-06 | Added Kaggle N8 high-resolution YOLO11x stretch notebook | Use `notebooks/kaggle_one_experiment_n8_joint_eo_ir_yolo11x_img960.ipynb`. It follows the N7 high-resolution EO+IR recipe but upgrades model capacity to `yolo11x-seg.pt`. Current defaults: `imgsz=960`, `batch=2`, `device=0`, eval on `eval_ir` and `eval_eo_ir`. Run smoke first because YOLO11x at 960 is memory/runtime risky on T4x2. |
| 2026-06-06 | Patched N8 to avoid two-GPU DDP failure | Kaggle smoke failed under `device=0,1` with PyTorch DDP `Expected to have finished reduction... unused parameters` on rank 1, not CUDA OOM. Updated N8 default to `device=0`, `batch=2`; if memory fails, reduce batch to 1. |
| 2026-06-06 | Patched N8 best.pt lookup path | Single-GPU N8 smoke trained but the notebook looked for `experiments/n8_joint.../best.pt`; the runner saves under `experiments/N8_joint...` because run dirs are `<id>_<name>`. Updated `EXPERIMENT_NAME` to `N8_joint_eo_ir_yolo11x_img960`. |
| 2026-06-06 | Completed Kaggle N8 YOLO11x high-resolution smoke run | `downloads/smoke_n8_results.zip`; status completed in 1323.60 seconds with `imgsz=960`, device=0, batch=2. Parsed peak GPU memory from stdout was about 13.9G. N8 smoke eval_ir: mask mAP50 0.4345, mask mAP50-95 0.2849, box mAP50 0.4465, box mAP50-95 0.3312. eval_eo_ir: mask mAP50 0.3699, mask mAP50-95 0.2384, box mAP50 0.3853, box mAP50-95 0.2853. N8 smoke beats N7 smoke on mask metrics, but one epoch took about 22 minutes on single T4, so full N8@960 is a runtime/quota risk. |
| 2026-06-09 | Checked Kaggle N8 YOLO11x high-resolution full run | `downloads/full_n8_results.zip`; status completed. Python `zipfile` reports a bad central directory, but Windows `tar` can read the packaged metrics/status files. Final eval_ir: mask mAP50 0.7041, mask mAP50-95 0.5145, box mAP50 0.7205, box mAP50-95 0.6091. eval_eo_ir: mask mAP50 0.6463, mask mAP50-95 0.4422, box mAP50 0.6632, box mAP50-95 0.5455. Training rows reached epoch 96; early stopping reported best epoch 71. N8 improves combined EO+IR metrics over N7 but is slightly lower than N7 on primary IR mask mAP50-95, so use it as capacity-scaling ablation / combined-eval best rather than replacing N7 outright. |
| 2026-06-09 | Built final result consolidation artifacts | Added `scripts/analysis/build_final_results.py`. Generated `reports/final/final_results_summary.md`, `reports/final/tables/final_metrics_long.csv`, `reports/final/tables/main_comparison.csv`, and mask mAP50-95 bar charts under `reports/final/figures/`. The tables include all full experiments E01/E02/E03/E04/E09/N1/N2/N3/N4/N6/N7/N8 across `eval_ir` and `eval_eo_ir`. |
| 2026-06-09 | Built structured technical briefing | Added `reports/guide_briefing/GUIDE_BRIEFING.md` with dataset summary, experiment inventory, result tables, interpretation, thesis contributions, paper storyline, limitations, and next steps. Added generated visuals under `reports/guide_briefing/assets/` using `scripts/analysis/build_guide_briefing_assets.py`. |
| 2026-06-09 | Neutralized briefing wording | Updated `reports/guide_briefing/GUIDE_BRIEFING.md` with a clickable index, formal section titles, open technical decisions, and no informal meeting-prep wording. |
| 2026-06-10 | Drafted dissertation Chapter 1 | Added `thesis/Chapter1/ch1.tex` with introduction, motivation, problem statement, research questions, objectives, scope, dataset overview, methodology overview, contributions, report organization, and chapter summary. |
| 2026-06-11 | Drafted dissertation Chapter 2 | Added `thesis/Chapter2/ch2.tex` covering aerial perception, EO/IR sensing, domain gap, detection, segmentation, YOLO models, domain adaptation, visible-to-thermal augmentation, mixed-domain training, model scaling, resolution, ensembling, IndraEye, related work, and research gap. Citation placeholders were added for the later BibTeX file. |
| 2026-06-11 | Drafted dissertation Chapter 3 | Added `thesis/Chapter3/ch3.tex` covering experimental design goals, dataset organization, class taxonomy, evaluation protocol, EO-only baselines, grayscale transformations, IR supervision, model scaling, high-resolution experiments, ensemble design, experiment matrix, execution environment, result tracking, and analysis plan. |
| 2026-06-11 | Normalized Chapter 3 experiment notation | Updated thesis-facing Chapter 3 labels to a single E01-E12 sequence. Mapping: internal E09 -> thesis E05, N1 -> E06, N2 -> E07, N3 -> E08, N4 -> E09, N6 -> E10, N7 -> E11, N8 -> E12. Internal result artifacts retain their original filenames/IDs. |
| 2026-06-12 | Added Chapter 3 workflow figure | Added `scripts/analysis/build_thesis_figures.py`, generated `thesis/Figures/Chapter3/proposed_workflow.{png,pdf}`, and inserted the workflow as Figure 3.1 in `thesis/Chapter3/ch3.tex`. |
| 2026-06-12 | Drafted dissertation Chapter 4 | Added `thesis/Chapter4/ch4.tex` covering repository organization, software environment, dataset preparation, YOLO label format, augmentation generation, dataset YAML creation, experiment configuration, training runner, checkpoint resume, Kaggle/HPC execution, evaluation, ensemble implementation, result packaging, and reproducibility. |
| 2026-06-12 | Drafted dissertation Chapter 5 | Added `thesis/Chapter5/ch5.tex` with results tables, discussion, and placeholder-safe figure slots. Added `thesis/Figures/Chapter5/IMAGE_GENERATION_PROMPTS.md` with eight external image-generation prompts for Chapter 5 visuals. |
| 2026-06-12 | Generated Chapter 5 result figures | Added `scripts/analysis/build_chapter5_figures.py` and generated eight thesis-ready Chapter 5 figures in PNG/PDF form under `thesis/Figures/Chapter5/` using exact metric values. |
| 2026-06-15 | Drafted dissertation conclusion and abstract | Added `thesis/Chapter6/ch6.tex` with conclusions, research-question answers, limitations, and future work. Added the front-matter abstract in `thesis/Sections/abstract.tex`. |
| 2026-06-15 | Audited online LaTeX thesis package | Inspected `docs/cross-domain-semantic-segmentation.zip` and created `docs/ONLINE_LATEX_THESIS_AUDIT.md` with package inventory, compile/static checks, critical issues, and cleanup recommendations. |
| 2026-06-15 | Fixed LaTeX bibliography source | Added `docs/latex_fixes/SVNITPhDbibtex.bib` with 39 research-paper references covering EO/IR, YOLO, segmentation, aerial perception, and domain adaptation. Static check against the extracted online package reports zero missing citation keys. |

## Next Recommended Actions

1. Use `reports/guide_briefing/GUIDE_BRIEFING.md` as the formal technical summary for story, claims, and experiment framing.
2. Use `reports/final/final_results_summary.md` as the starting point for paper/dissertation result writing.
3. Generate qualitative examples comparing N7 vs N8 if the full N8 visual archive is available locally; avoid using N8 smoke visuals for final qualitative claims.

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
