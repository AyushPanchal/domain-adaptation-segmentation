# Final Results Summary

Generated from downloaded experiment artifacts under `downloads/`.

## Main Comparison

| ID | Method | Model | Eval | Mask mAP50 | Mask mAP50-95 | Box mAP50 | Box mAP50-95 |
|---|---|---|---|---|---|---|---|
| N3 | Joint EO+IR large | YOLO11l-seg | eval_eo_ir | 0.5823 | 0.3308 | 0.6192 | 0.5025 |
| N6 | N3+N4 mask-aware ensemble | 2x YOLO11l-seg | eval_eo_ir | 0.5462 | 0.3139 | 0.5828 | 0.4749 |
| N7 | Joint EO+IR high-res | YOLO11l-seg | eval_eo_ir | 0.6163 | 0.4310 | 0.6383 | 0.5244 |
| N8 | Joint EO+IR high-res XL | YOLO11x-seg | eval_eo_ir | 0.6463 | 0.4422 | 0.6632 | 0.5455 |
| N3 | Joint EO+IR large | YOLO11l-seg | eval_ir | 0.6968 | 0.4555 | 0.7167 | 0.6099 |
| N6 | N3+N4 mask-aware ensemble | 2x YOLO11l-seg | eval_ir | 0.6910 | 0.4553 | 0.7171 | 0.6143 |
| N7 | Joint EO+IR high-res | YOLO11l-seg | eval_ir | 0.7025 | 0.5250 | 0.7192 | 0.6128 |
| N8 | Joint EO+IR high-res XL | YOLO11x-seg | eval_ir | 0.7041 | 0.5145 | 0.7205 | 0.6091 |

## Interpretation

- **Primary IR evaluation:** N7 remains the best strict-mask model with IR mask mAP50-95 `0.5250` versus N8 `0.5145`.
- **Combined EO+IR evaluation:** N8 is strongest with mask mAP50-95 `0.4422` versus N7 `0.4310`.
- **Scaling result:** moving from YOLO11l 640 (N3) to YOLO11l 960 (N7) gives the cleanest primary IR gain. Moving from YOLO11l 960 (N7) to YOLO11x 960 (N8) helps combined EO+IR but does not replace N7 on the primary IR metric.
- **Ensemble result:** the N3+N4 ensemble (N6) is useful as an ablation, but does not beat high-resolution joint training.

## Full Table

| ID | Method | Model | Eval | Mask mAP50 | Mask mAP50-95 | Box mAP50 | Box mAP50-95 |
|---|---|---|---|---|---|---|---|
| E01 | EO-only baseline | YOLO11s-seg | eval_eo_ir | 0.3386 | 0.1669 | 0.3621 | 0.2603 |
| E02 | Full grayscale EO | YOLO11s-seg | eval_eo_ir | 0.2917 | 0.1417 | 0.3194 | 0.2179 |
| E03 | Box-guided grayscale EO | YOLO11s-seg | eval_eo_ir | 0.1427 | 0.0605 | 0.1553 | 0.1027 |
| E04 | Mask-guided grayscale EO | YOLO11s-seg | eval_eo_ir | 0.1768 | 0.0705 | 0.1987 | 0.1282 |
| E09 | Joint EO+IR | YOLO11s-seg | eval_eo_ir | 0.5483 | 0.3069 | 0.5774 | 0.4469 |
| N1 | IR-only supervised | YOLO11s-seg | eval_eo_ir | 0.3233 | 0.1902 | 0.3660 | 0.2894 |
| N2 | Balanced EO+IR | YOLO11s-seg | eval_eo_ir | 0.5251 | 0.2969 | 0.5618 | 0.4321 |
| N3 | Joint EO+IR large | YOLO11l-seg | eval_eo_ir | 0.5823 | 0.3308 | 0.6192 | 0.5025 |
| N4 | IR-only large | YOLO11l-seg | eval_eo_ir | 0.3448 | 0.1984 | 0.3768 | 0.3011 |
| N6 | N3+N4 mask-aware ensemble | 2x YOLO11l-seg | eval_eo_ir | 0.5462 | 0.3139 | 0.5828 | 0.4749 |
| N7 | Joint EO+IR high-res | YOLO11l-seg | eval_eo_ir | 0.6163 | 0.4310 | 0.6383 | 0.5244 |
| N8 | Joint EO+IR high-res XL | YOLO11x-seg | eval_eo_ir | 0.6463 | 0.4422 | 0.6632 | 0.5455 |
| E01 | EO-only baseline | YOLO11s-seg | eval_ir | 0.2203 | 0.0948 | 0.2362 | 0.1644 |
| E02 | Full grayscale EO | YOLO11s-seg | eval_ir | 0.2274 | 0.1040 | 0.2438 | 0.1548 |
| E03 | Box-guided grayscale EO | YOLO11s-seg | eval_ir | 0.1972 | 0.0811 | 0.2051 | 0.1342 |
| E04 | Mask-guided grayscale EO | YOLO11s-seg | eval_ir | 0.2006 | 0.0812 | 0.2144 | 0.1384 |
| E09 | Joint EO+IR | YOLO11s-seg | eval_ir | 0.6691 | 0.4229 | 0.6899 | 0.5640 |
| N1 | IR-only supervised | YOLO11s-seg | eval_ir | 0.6530 | 0.4342 | 0.7015 | 0.5743 |
| N2 | Balanced EO+IR | YOLO11s-seg | eval_ir | 0.6407 | 0.4031 | 0.6680 | 0.5325 |
| N3 | Joint EO+IR large | YOLO11l-seg | eval_ir | 0.6968 | 0.4555 | 0.7167 | 0.6099 |
| N4 | IR-only large | YOLO11l-seg | eval_ir | 0.6555 | 0.4438 | 0.7056 | 0.5943 |
| N6 | N3+N4 mask-aware ensemble | 2x YOLO11l-seg | eval_ir | 0.6910 | 0.4553 | 0.7171 | 0.6143 |
| N7 | Joint EO+IR high-res | YOLO11l-seg | eval_ir | 0.7025 | 0.5250 | 0.7192 | 0.6128 |
| N8 | Joint EO+IR high-res XL | YOLO11x-seg | eval_ir | 0.7041 | 0.5145 | 0.7205 | 0.6091 |

## Files

- `reports/final/tables/final_metrics_long.csv`
- `reports/final/tables/main_comparison.csv`
- `reports/final/figures/mask_map50_95_eval_ir.png`
- `reports/final/figures/mask_map50_95_eval_eo_ir.png`
