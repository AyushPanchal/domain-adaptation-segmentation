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

## Class Mapping Decision

The existing YAML files in the parent workspace disagree:

- `indraeye_eo_seg.yaml` maps class `0` to `Bicycle` and includes `Ignore`.
- `indraeye_ir_seg.yaml` maps class `0` to `Backhoe loader` and drops `Ignore`.
- `indraeye_mixed_seg.yaml` uses 13 names and adds `Backhoe loader` as class `12`.

The prepared YOLO segmentation labels in `../datasets/indraeye_seg` contain
class IDs `0-11`, not `12`. This matches the corrected Phase 3 mapping:

```text
0: Bicycle
1: Bus
2: Car
3: Cargo trike
4: Ignore
5: Motorcycle
6: Person
7: Rickshaw
8: Small truck
9: Tractor
10: Truck
11: Van
```

Verification checks:

- `../phase3_ensemble/AI_HANDOFF.md` warns that the corrected mapping is
  `0: Bicycle ... 11: Van, 12: Backhoe loader`.
- The local prepared labels currently contain only `0-11`.
- A sample file with YOLO class IDs `[2, 4, 5, 6, 7, 10]` has JSON labels
  including `car`, `ignore`, `motorcycle`, `person`, `rickshaw`, and `truck`.
- A sample file containing YOLO class ID `0` has JSON labels including
  `bicycle`.

Decision for this repository: use a 12-class active mapping for the prepared
dataset, stored in `configs/classes/indraeye_seg_active12.yaml`.

## Recommended Next Step

Completed on 2026-05-23:

1. Added a copy script for matched `.jpg`/`.txt` pairs.
2. Copied the prepared dataset into `data/raw/indraeye_seg`.
3. Wrote copied/skipped/checksum/class-count manifests into `data/manifests`.
4. Validated polygon coordinates, class IDs, and image/label pairing.
5. Confirmed zero validation issues after copying.

Copied dataset totals:

- Copied pairs: 5108
- Skipped unlabeled images: 13
- Instances: 125055
- Validation issues: 0

Next step: implement augmentation generation for Full Gray, Box-Guided Gray,
MGA, and BA-MGA.
