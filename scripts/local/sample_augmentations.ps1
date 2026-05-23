$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"

python -m domain_adaptation_segmentation.visualization.sample_augmentations `
  --processed-root data\processed `
  --raw-root data\raw\indraeye_seg `
  --output-dir reports\qualitative\augmentation_samples `
  --limit 4

