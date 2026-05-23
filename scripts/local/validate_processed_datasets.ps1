$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"

python -m domain_adaptation_segmentation.data.validate_processed_datasets `
  --processed-root data\processed `
  --manifest-root data\manifests `
  --class-config configs\classes\indraeye_seg_active12.yaml

