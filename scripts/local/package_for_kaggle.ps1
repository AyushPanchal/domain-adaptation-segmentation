$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"

python -m domain_adaptation_segmentation.data.package_for_kaggle `
  --repo-root . `
  --output-zip artifacts\kaggle\domain-adaptation-segmentation-kaggle.zip `
  --compression-level 1

