# LaTeX Bibliography Fix

This folder contains a replacement bibliography file for the online LaTeX thesis package:

`SVNITPhDbibtex.bib`

Use it to replace the stale bibliography file inside the online LaTeX project:

`SVNITPhDbibtex.bib`

## What Was Fixed

- Removed the old legal/text-clustering bibliography content.
- Added 40 real references covering:
  - core object detection,
  - semantic and instance segmentation,
  - YOLO-family models,
  - aerial/UAV perception datasets,
  - EO/IR and RGB-thermal perception,
  - domain adaptation and image translation.
- Added all citation keys currently used in Chapter 2:
  - `fasterrcnn2015`
  - `yolo2016`
  - `ultralytics2023`
  - `saga2025`
  - `unifiedeoir2024`
  - `indraeye2024`
  - `maskrcnn2017`
  - `detr2020`
  - `cyclegan2017`
  - `pixelda2017`

## Verification

Static citation check after replacing the extracted online package bibliography:

```text
bib_entries: 40
citation_instances: 13
missing_cites: 0
```

## Rebuild Sequence

In Overleaf or the online LaTeX editor, rebuild using:

```text
XeLaTeX
BibTeX
XeLaTeX
XeLaTeX
```

Then search the generated PDF for:

```text
[?]
```

There should be no unresolved citation markers in Chapter 2.

## Note

The current Chapter 2 key `unifiedeoir2024` is mapped to a real RGB-infrared aerial vehicle detection paper to avoid unresolved citations. For the cleanest final thesis, the surrounding Chapter 2 sentence can later be rewritten to avoid calling it an SVNIT-specific study unless that exact study is added as a formal publication or internal report.
