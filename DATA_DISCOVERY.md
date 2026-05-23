# Data Discovery Notes

Date: 2026-05-23

## Candidate Source

The current workspace contains a prepared YOLO segmentation dataset:

```text
../datasets/indraeye_seg/
  eo/
    images/train
    images/val
    labels/train
    labels/val
  ir/
    images/train
    images/val
    labels/train
    labels/val
```

This is currently the best candidate source for the new experiment repository
because labels are already in YOLO segmentation polygon format:

```text
class_id x1 y1 x2 y2 ... xn yn
```

## Existing YAML Files In Parent Workspace

```text
../configs/indraeye_eo_seg.yaml
../configs/indraeye_ir_seg.yaml
../configs/indraeye_mixed_seg.yaml
```

These are useful references but should not be copied blindly because the class
name mappings differ between EO, IR, and mixed configs.

## File Counts

| Domain | Split | JPG Images | JSON Sidecars | YOLO Label TXT |
|---|---:|---:|---:|---:|
| EO | train | 2026 | 2027 | 2024 |
| EO | val | 60 | 60 | 59 |
| IR | train | 2977 | 2973 | 2967 |
| IR | val | 58 | 58 | 58 |

The image directories contain `.jpg` images and `.json` sidecars. For YOLO
training, copy only `.jpg` images and matching `.txt` labels unless a future
step needs the JSON annotations.

## Image/Label Matching

| Domain | Split | Missing Labels | Orphan Labels |
|---|---:|---:|---:|
| EO | train | 2 | 0 |
| EO | val | 1 | 0 |
| IR | train | 10 | 0 |
| IR | val | 0 | 0 |

Known missing label examples:

- EO train: `day_eo_22_03_day_drone_mount_eo_nvrec1_0000`
- EO train: `day_eo_22_03_day_drone_mount_eo_nvrec1_0070`
- EO val: `day_eo_22_03_day_drone_mount_eo_nvrec1_0105`
- IR train: `day_ir_22_03_day_drone_mount_eo_nvrec1_10115(1)`
- IR train: `day_ir_22_03_day_drone_mount_eo_nvrec1_7210(1)`
- IR train: `day_ir_day_ir_main_opp_tunnel_frame_5495`
- IR train: `day_ir_day_ir_main_opp_tunnel_frame_5530`
- IR train: `day_ir_day_ir_main_opp_tunnel_frame_5565`

Recommended copy policy: copy only images with matching label files, and log
all skipped images into a manifest.

## Label Class Counts

| Domain | Split | Label Files | Instances | Class IDs Present |
|---|---:|---:|---:|---|
| EO | train | 2024 | 68414 | 0-11 |
| EO | val | 59 | 2254 | 0-8, 10-11 |
| IR | train | 2967 | 53191 | 0-11 |
| IR | val | 58 | 1196 | 0-11 |

## Class Mapping Caveat

The existing YAML files disagree:

- `indraeye_eo_seg.yaml` maps class `0` to `Bicycle` and includes `Ignore`.
- `indraeye_ir_seg.yaml` maps class `0` to `Backhoe loader` and drops `Ignore`.
- `indraeye_mixed_seg.yaml` uses 13 names and adds `Backhoe loader` as class `12`.

Before training, we must define one consistent 12-class or 13-class mapping and
verify it against the original conversion scripts or annotation JSON files.

This is the highest-risk data issue discovered so far.

## Recommended Next Step

Implement a validation script that:

1. Copies only matched `.jpg`/`.txt` pairs into the new repo.
2. Records skipped files and checksum metadata.
3. Computes class counts per split.
4. Validates polygon coordinates are normalized in `[0, 1]`.
5. Fails loudly if class IDs exceed the selected class mapping.

