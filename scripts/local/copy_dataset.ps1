$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"

python -m domain_adaptation_segmentation.data.copy_dataset `
  --source-root ..\datasets\indraeye_seg `
  --dest-root data\raw\indraeye_seg `
  --manifest-root data\manifests `
  --class-config configs\classes\indraeye_seg_active12.yaml
