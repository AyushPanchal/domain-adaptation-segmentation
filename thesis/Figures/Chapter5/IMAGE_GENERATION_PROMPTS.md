# Chapter 5 Image Generation Prompts

Use these prompts to generate thesis-ready visuals for Chapter 5. Save the generated images with the exact filenames shown below inside:

```text
thesis/Figures/Chapter5/
```

General style for all images:

- Clean academic visual style suitable for an MTech dissertation.
- Light background, high contrast text, professional color palette.
- Use readable sans-serif typography.
- Avoid decorative clutter, cartoon style, excessive gradients, and fake UI chrome.
- Use the exact experiment IDs and metric values provided.
- Do not invent additional metrics, datasets, logos, or claims.
- Prefer 300 dpi or high-resolution PNG/PDF output.

---

## 1. Performance Progression Story

Filename:

```text
performance_progression_story.png
```

Caption target:

```text
Performance progression on IR-only validation using strict mask mAP50-95.
```

Prompt:

```text
Create a clean academic infographic showing the performance progression of YOLO segmentation experiments on IR-only validation. Use a horizontal milestone chart or stepped bar chart. Title: "IR Segmentation Performance Progression". Metric: "Mask mAP50-95". Use these exact values: E01 EO-only baseline = 0.0948, E02 full grayscale EO = 0.1040, E05 joint EO+IR YOLO11s = 0.4229, E08 joint EO+IR YOLO11l = 0.4555, E11 joint EO+IR YOLO11l at 960 = 0.5250, E12 joint EO+IR YOLO11x at 960 = 0.5145. Visually emphasize the large jump from EO-only to IR-supervised training and the later gain from high-resolution training. Use a calm palette: blue for EO-only, amber for grayscale, green for IR supervision, purple for model scaling, teal for high-resolution. Include a small annotation: "IR supervision gives the largest gain; high resolution gives the strongest strict-mask result." Keep the figure thesis-ready, minimal, readable, and not flashy.
```

Negative prompt:

```text
No 3D bars, no cartoon graphics, no fake images of vehicles, no extra values, no watermark, no dark background.
```

Recommended aspect ratio: 16:9.

---

## 2. Full IR Results Ranking

Filename:

```text
ir_results_ranking.png
```

Caption target:

```text
IR-only validation ranking of all full experiments using mask mAP50-95.
```

Prompt:

```text
Create a publication-quality horizontal bar chart ranking all experiments by IR-only validation mask mAP50-95. Title: "IR-only Validation: Mask mAP50-95 Ranking". Use exact labels and values: E01 0.0948, E02 0.1040, E03 0.0811, E04 0.0812, E05 0.4229, E06 0.4342, E07 0.4031, E08 0.4555, E09 0.4438, E10 0.4553, E11 0.5250, E12 0.5145. Sort bars from highest to lowest. Highlight E11 as "Best IR strict-mask model" and E12 as "Close second". Use muted colors grouped by experiment family: EO-only/grayscale, supervised YOLO11s, large YOLO11l, ensemble, high-resolution. Include values at the end of bars with three decimals. Clean academic layout, white background, subtle gridlines.
```

Negative prompt:

```text
No distorted text, no wrong ordering, no additional experiments, no 3D effects, no decorative icons.
```

Recommended aspect ratio: 4:3 or 16:10.

---

## 3. Combined EO+IR Results Ranking

Filename:

```text
combined_results_ranking.png
```

Caption target:

```text
Combined EO+IR validation ranking using mask mAP50-95.
```

Prompt:

```text
Create a clean horizontal bar chart ranking all experiments by combined EO+IR validation mask mAP50-95. Title: "Combined EO+IR Validation: Mask mAP50-95 Ranking". Use exact labels and values: E01 0.1669, E02 0.1417, E03 0.0605, E04 0.0705, E05 0.3069, E06 0.1902, E07 0.2969, E08 0.3308, E09 0.1984, E10 0.3139, E11 0.4310, E12 0.4422. Sort bars from highest to lowest. Highlight E12 as "Best combined EO+IR model" and E11 as "Best YOLO11l high-resolution model". Use the same visual language as the IR ranking chart so both figures look like a matching pair. Include values at the end of bars with three decimals. White background, restrained colors, crisp labels.
```

Negative prompt:

```text
No invented values, no dark theme, no excessive decoration, no blurry text.
```

Recommended aspect ratio: 4:3 or 16:10.

---

## 4. EO-only Augmentation Comparison

Filename:

```text
eo_only_augmentation_comparison.png
```

Caption target:

```text
Comparison of EO-only and grayscale-domain baselines on IR validation.
```

Prompt:

```text
Create an academic comparison figure for EO-only adaptation baselines evaluated on IR-only validation. Title: "EO-only and Grayscale-domain Baselines". Show four methods as cards or bars with mask mAP50-95 values: E01 EO-only = 0.0948, E02 full grayscale = 0.1040, E03 box-guided grayscale = 0.0811, E04 mask-guided grayscale = 0.0812. Add a visual note: "Color removal alone does not close the EO-to-IR segmentation gap." Use a subtle EO-to-IR domain-gap motif: left side visible EO palette, right side thermal gray/IR palette, with a gap indicator. Keep the graphic formal and thesis-friendly, not illustrative or cartoonish. Use simple icons only if needed: image, mask, box, grayscale.
```

Negative prompt:

```text
No real vehicle photos, no excessive thermal flame colors, no futuristic UI, no extra metrics.
```

Recommended aspect ratio: 16:9.

---

## 5. Supervision Strategy Comparison

Filename:

```text
supervision_strategy_comparison.png
```

Caption target:

```text
Effect of adding real IR supervision compared with EO-only training.
```

Prompt:

```text
Create a grouped bar chart comparing supervision strategies on mask mAP50-95 for two evaluation settings: IR-only validation and combined EO+IR validation. Title: "Effect of IR Supervision". Use exact values:
E01 EO-only: IR = 0.0948, EO+IR = 0.1669.
E05 joint EO+IR YOLO11s: IR = 0.4229, EO+IR = 0.3069.
E06 IR-only YOLO11s: IR = 0.4342, EO+IR = 0.1902.
E07 balanced EO+IR YOLO11s: IR = 0.4031, EO+IR = 0.2969.
Use two bars per experiment, one for IR-only and one for combined EO+IR. Add a small annotation: "Real IR labels dominate grayscale-only adaptation." Keep the figure clean, with a legend, readable values, and muted green/orange colors.
```

Negative prompt:

```text
No 3D chart, no invented trend line, no crowded labels, no dark background.
```

Recommended aspect ratio: 16:9.

---

## 6. Scale and Resolution Ablation

Filename:

```text
scale_resolution_ablation.png
```

Caption target:

```text
Effect of model scale and input resolution on strict mask performance.
```

Prompt:

```text
Create a clean ablation figure showing how model scale and input resolution affect mask mAP50-95. Use a two-line chart with x-axis experiment progression: E05 YOLO11s 640, E08 YOLO11l 640, E11 YOLO11l 960, E12 YOLO11x 960. Plot two lines: IR-only validation values = 0.4229, 0.4555, 0.5250, 0.5145; combined EO+IR validation values = 0.3069, 0.3308, 0.4310, 0.4422. Title: "Model Scale and Resolution Ablation". Use markers at each experiment. Annotate E11 as "Best IR strict-mask" and E12 as "Best combined EO+IR". Use a polished academic style with subtle gridlines and strong readability.
```

Negative prompt:

```text
No exaggerated 3D perspective, no extra data points, no wrong labels, no heavy decorative background.
```

Recommended aspect ratio: 16:9.

---

## 7. Ensemble Ablation

Filename:

```text
ensemble_ablation.png
```

Caption target:

```text
Mask-aware ensemble ablation compared with strong single-model baselines.
```

Prompt:

```text
Create a thesis-ready ablation chart comparing E08, E09, E10, and E11 on IR-only validation mask mAP50-95. Use exact values: E08 joint EO+IR YOLO11l = 0.4555, E09 IR-only YOLO11l = 0.4438, E10 E08+E09 mask-aware ensemble = 0.4553, E11 joint EO+IR YOLO11l at 960 = 0.5250. Title: "Ensemble Ablation". Visual message: "The ensemble matches the 640-resolution large model but does not beat high-resolution joint training." Use a focused bar chart or comparison card layout. Highlight E10 in gray/blue and E11 in teal. Include values with three decimals. Clean white background.
```

Negative prompt:

```text
No claim that ensemble is best, no invented improvement arrows, no dark background, no clutter.
```

Recommended aspect ratio: 16:9.

---

## 8. Final Model Recommendation Summary

Filename:

```text
final_model_recommendation.png
```

Caption target:

```text
Summary of the best model choices for IR-only and combined EO+IR evaluation.
```

Prompt:

```text
Create an elegant thesis summary card with two main recommendation panels. Left panel: "Best primary IR model" with E11, YOLO11l-seg, EO+IR training, 960 image size, IR mask mAP50-95 = 0.5250. Right panel: "Best combined EO+IR model" with E12, YOLO11x-seg, EO+IR training, 960 image size, combined EO+IR mask mAP50-95 = 0.4422. Add a small neutral note at the bottom: "E11 is preferred for strict IR segmentation; E12 is preferred for combined-modality robustness." Use clean academic colors, no decorative clutter, high readability.
```

Negative prompt:

```text
No trophy icons, no hype language, no unrealistic vehicle imagery, no watermark.
```

Recommended aspect ratio: 16:9.
