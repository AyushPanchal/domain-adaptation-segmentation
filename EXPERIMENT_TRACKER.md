# Experiment Tracker

Update this table whenever an experiment is planned, started, completed, or
fails. Results should also be exported as CSV/JSON under `reports/tables/`.

| ID | Method | Model | Train | Test | Platform | Status | Started | Finished | Key Metrics | Result Path | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SMOKE-E01 | Source RGB | YOLO11s-seg | RGB | IR | SVNIT HPC node2 H100 | completed | 2026-06-01 12:14 IST | 2026-06-01 12:16 IST | mask mAP50 0.224, mask mAP50-95 0.108, box mAP50 0.240, box mAP50-95 0.153 | `runs/experiments/E01_source_rgb_yolo11s`, `reports/tables/summary_results.*` | 1 epoch GPU smoke, batch=2, workers=2, CUDA:0, peak GPU_mem about 4.08G |
| E01 | Source RGB | YOLO11s-seg | RGB | IR | Kaggle T4x2 | completed | 2026-06-02 01:52 IST | 2026-06-02 02:32 IST | best.pt val: mask mAP50 0.221, mask mAP50-95 0.0961, box mAP50 0.236, box mAP50-95 0.163 | `downloads/full_e01_results.zip` | Direct Kaggle dataset run, device=0,1, batch=16, workers=2. Early stopped at epoch 35/100; best epoch 10. `summary_results.csv` row is last epoch, while paper table should use final best.pt validation metrics from stdout. |
| E02 | Full Gray | YOLO11s-seg | RGB | IR | TBD | planned | - | - | - | - | Naive grayscale baseline |
| E03 | Box-Guided Gray | YOLO11s-seg | RGB | IR | TBD | planned | - | - | - | - | Box-level semantic gray baseline |
| E04 | MGA | YOLO11s-seg | RGB | IR | TBD | planned | - | - | - | - | Proposed mask-guided method |
| E05 | BA-MGA | YOLO11s-seg | RGB | IR | TBD | planned | - | - | - | - | Main proposed method |
| E06 | IR Oracle | YOLO11s-seg | IR | IR | TBD | planned | - | - | - | - | Upper-bound baseline |
| E07 | Source RGB | YOLO11x-seg | RGB | IR | TBD | planned | - | - | - | - | Large-model domain gap baseline |
| E08 | BA-MGA | YOLO11x-seg | RGB | IR | TBD | planned | - | - | - | - | Best-performance result |
