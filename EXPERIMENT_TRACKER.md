# Experiment Tracker

Update this table whenever an experiment is planned, started, completed, or
fails. Results should also be exported as CSV/JSON under `reports/tables/`.

| ID | Method | Model | Train | Test | Platform | Status | Started | Finished | Key Metrics | Result Path | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SMOKE-E01 | Source RGB | YOLO11s-seg | RGB | IR | SVNIT HPC node2 H100 | completed | 2026-06-01 12:14 IST | 2026-06-01 12:16 IST | mask mAP50 0.224, mask mAP50-95 0.108, box mAP50 0.240, box mAP50-95 0.153 | `runs/experiments/E01_source_rgb_yolo11s`, `reports/tables/summary_results.*` | 1 epoch GPU smoke, batch=2, workers=2, CUDA:0, peak GPU_mem about 4.08G |
| E01 | Source RGB | YOLO11s-seg | RGB | IR | Kaggle T4x2 | completed | 2026-06-02 01:52 IST | 2026-06-02 02:32 IST | eval_ir: mask mAP50 0.2203, mask mAP50-95 0.0948, box mAP50 0.2362, box mAP50-95 0.1644; eval_eo_ir: mask mAP50 0.3386, mask mAP50-95 0.1669, box mAP50 0.3621, box mAP50-95 0.2603 | `downloads/full_e01_results.zip`; `downloads/e01_bestpt_evaluations.zip` | Direct Kaggle dataset run, device=0,1, batch=16, workers=2. Early stopped at epoch 35/100; best epoch 10. Use `eval_ir` as primary domain-transfer metric and `eval_eo_ir` as secondary combined metric. |
| E02 | Full Gray | YOLO11s-seg | RGB-gray | IR | Kaggle T4x2 | notebook ready | - | - | - | `notebooks/kaggle_one_experiment_e02_full_gray.ipynb` | Naive full-image grayscale baseline. Notebook generates gray EO train data under `/kaggle/working/generated/e02_full_gray`; eval uses `eval_ir` as primary and `eval_eo_ir` as secondary. |
| E03 | Box-Guided Gray | YOLO11s-seg | RGB | IR | TBD | planned | - | - | - | - | Box-level semantic gray baseline |
| E04 | MGA | YOLO11s-seg | RGB | IR | TBD | planned | - | - | - | - | Proposed mask-guided method |
| E05 | BA-MGA | YOLO11s-seg | RGB | IR | TBD | planned | - | - | - | - | Main proposed method |
| E06 | IR Oracle | YOLO11s-seg | IR | IR | TBD | planned | - | - | - | - | Upper-bound baseline |
| E07 | Source RGB | YOLO11x-seg | RGB | IR | TBD | planned | - | - | - | - | Large-model domain gap baseline |
| E08 | BA-MGA | YOLO11x-seg | RGB | IR | TBD | planned | - | - | - | - | Best-performance result |
