$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"

python -m domain_adaptation_segmentation.data.generate_augmented_datasets `
  --raw-root data\raw\indraeye_seg `
  --processed-root data\processed `
  --manifest-root data\manifests `
  --yaml-root data\manifests\dataset_yamls `
  --class-config configs\classes\indraeye_seg_active12.yaml `
  --skip-class 4 `
  --feather-radius 3.0
