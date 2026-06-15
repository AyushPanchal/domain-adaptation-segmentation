# LaTeX Fix Files

This folder contains drop-in replacement files for the online LaTeX thesis package.

## Bibliography

`SVNITPhDbibtex.bib`

Use it to replace the stale bibliography file inside the online LaTeX project:

`SVNITPhDbibtex.bib`

## What Was Fixed

- Removed the old legal/text-clustering bibliography content.
- Added 39 research-paper references covering:
  - core object detection,
  - semantic and instance segmentation,
  - YOLO-family models,
  - aerial/UAV perception datasets,
  - EO/IR and RGB-thermal perception,
  - domain adaptation and image translation.
- Removed software/GitHub-only citations from the bibliography.
- Ordered the bibliography so the most thesis-relevant papers appear first:
  - IndraEye,
  - SAGA,
  - RGB-infrared aerial vehicle detection,
  - thermal/multispectral perception,
  - domain adaptation,
  - YOLO and core segmentation/detection foundations.
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
bib_entries: 39
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

## Acronyms

`Acr.tex`

Use it to replace the stale acronym file inside the online LaTeX project:

`Sections/Acr.tex`

The replacement removes legal/text-clustering acronyms and adds EO/IR, computer vision, segmentation, training, and evaluation acronyms used by this thesis.

## Appendix Removal

`MainReport.tex`

Use it to replace the online LaTeX project `MainReport.tex` if you want the stale appendix removed for now.

The only intended appendix-related change is:

```tex
% Appendix removed for current thesis draft. Re-enable after adding a relevant appendix.
% \include{Appendix/appndx}
% \blankpage
```

This removes `Appendix A Industrial Internship Report at Siemens` from the compiled PDF and table of contents.

## List of Tables

The replacement `MainReport.tex` also enables the List of Tables:

```tex
\addcontentsline{toc}{section}{List of Tables}
\borderlot
```

This is useful because Chapters 3 and 5 contain multiple thesis result/design tables.

## List of Publications

`our_pub.tex`

Use it to replace the stale online LaTeX project file:

`Sections/our_pub.tex`

The replacement `MainReport.tex` enables the List of Publications using:

```tex
\rhead{\textit{List of Publications}}
\addcontentsline{toc}{chapter}{List of Publications}
\input{./Sections/our_pub}
```

The replacement `our_pub.tex` currently states that no publications are included in the report at present. Replace that line later if a paper, preprint, or accepted publication needs to be listed.
