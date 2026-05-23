# Augmentation Methods

Generated on 2026-05-23 from `data/raw/indraeye_seg`.

## Methods

| Method | Train Source | Validation Source | Transform |
|---|---|---|---|
| `source_rgb` | EO train | IR val | Copy EO images unchanged |
| `full_gray` | EO train | IR val | Convert full EO image to 3-channel grayscale |
| `box_guided_gray` | EO train | IR val | Convert bounding rectangle around each object polygon to grayscale |
| `mga` | EO train | IR val | Convert only object polygon pixels to grayscale |
| `ba_mga` | EO train | IR val | Convert object polygon pixels with a soft boundary mask |
| `ir_oracle` | IR train | IR val | Copy IR images unchanged |

## Ignore Class Policy

Class `4: Ignore` is not transformed by object-region methods:

- `box_guided_gray`
- `mga`
- `ba_mga`

The label remains present for training, but ignored regions are not treated as
semantic foreground objects for gray augmentation.

## Boundary Settings

`ba_mga` uses a Gaussian feather radius of `3.0` pixels when creating the soft
object mask.

## Generated Outputs

Processed datasets are written under:

```text
data/processed/
```

Generated YOLO dataset YAML files are written under:

```text
data/manifests/dataset_yamls/
```

The main summary files are:

```text
data/manifests/augmentation_summary.json
data/manifests/augmentation_manifest.csv
data/manifests/augmentation_class_counts.csv
data/manifests/processed_validation_report.json
```

Latest validation result:

```text
issues: 0
instances across generated datasets: 402437
```

