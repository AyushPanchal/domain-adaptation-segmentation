# Online LaTeX Thesis Package Audit

Source package audited:

`docs/cross-domain-semantic-segmentation.zip`

Temporary extraction path used for inspection:

`C:\Users\Ayush\AppData\Local\Temp\codex_thesis_audit_cross_domain`

Audit date: 2026-06-15

## Executive Summary

The online LaTeX package is structurally usable and contains the main thesis source files, generated PDF, chapters, figures, class file, and bibliography file. The current PDF appears to build into an 85-page report and includes the current EO/IR segmentation chapters. However, the package is not submission-ready yet.

The most important problems are:

1. The bibliography file is still from the senior/reference legal-text clustering report.
2. All citation keys used in Chapter 2 are missing from the `.bib` file, causing citation markers to appear as `[?]` in the PDF.
3. The List of Acronyms is still from the legal-text clustering project.
4. The appendix still contains `Industrial Internship Report at Siemens`.
5. Some front-matter details are placeholders or hardcoded in the class file.
6. The package includes many stale auxiliary files and unrelated old images from the reference report.

The thesis content itself is mostly in place, but the surrounding LaTeX package needs cleanup before final guide/examiner review.

## Package Inventory

Extracted package contents:

| Item | Count / Status |
|---|---:|
| Total files | 95 |
| `.tex` files | 13 |
| `.png` files | 52 |
| `.pdf` files | 10 |
| `.jpg` files | 6 |
| `.eps` files | 2 |
| `.aux` files | 7 |
| Main file | `MainReport.tex` |
| Class file | `SVNITPhDReport.cls` |
| Bibliography file | `SVNITPhDbibtex.bib` |
| Included PDF | `MainReport.pdf`, 85 pages |

Included chapters:

| Chapter | File | Status |
|---|---|---|
| Chapter 1 | `Chapter1/ch1.tex` | Present |
| Chapter 2 | `Chapter2/ch2.tex` | Present |
| Chapter 3 | `Chapter3/ch3.tex` | Present |
| Chapter 4 | `Chapter4/chp4.tex` | Present |
| Chapter 5 | `chapter5/ch5.tex` | Present |
| Chapter 6 | `Chapter6/ch6.tex` | Present |
| Appendix | `Appendix/appndx.tex` | Present, but stale/wrong |

## Checks Performed

Static checks performed:

- Main file structure inspection.
- Chapter include path inspection.
- Figure reference inspection.
- Label and reference consistency check.
- Citation key check against `SVNITPhDbibtex.bib`.
- PDF text extraction using `pypdf`.
- Search for stale reference-report terms.
- Package and front-matter inspection.

Compile check:

- A fresh LaTeX compile could not be run locally because `xelatex`, `pdflatex`, `lualatex`, `latexmk`, and `bibtex` were not available in this environment.
- The existing `MainReport.pdf` was inspected instead.

## What Is Working

### Main Source Structure

`MainReport.tex` includes all major chapters:

```tex
\include{Chapter1/ch1}
\include{Chapter2/ch2}
\include{Chapter3/ch3}
\include{Chapter4/chp4}
\include{chapter5/ch5}
\include{Chapter6/ch6}
```

This is structurally correct for the current package.

### Figures

No missing `\includegraphics` files were found. All graphics referenced from TeX files exist in the extracted package.

Chapter 3 workflow figure exists:

`Figures/Chapter3/proposed_workflow.png`

Chapter 5 generated figures exist:

- `Figures/Chapter5/performance_progression_story.png`
- `Figures/Chapter5/eo_only_augmentation_comparison.png`
- `Figures/Chapter5/supervision_strategy_comparison.png`
- `Figures/Chapter5/scale_resolution_ablation.png`
- `Figures/Chapter5/ensemble_ablation.png`
- `Figures/Chapter5/ir_results_ranking.png`
- `Figures/Chapter5/combined_results_ranking.png`
- `Figures/Chapter5/final_model_recommendation.png`

### Labels and References

No duplicate labels were detected.

No unresolved `\ref`, `\eqref`, or `\pageref` references were detected in the source.

## Critical Issues

### 1. Bibliography Is Wrong

Severity: Critical

The current `SVNITPhDbibtex.bib` file contains references from the senior/reference legal document clustering project, such as:

- TF-IDF references
- K-means clustering references
- DBSCAN references
- legal document clustering references
- document index graph clustering references

It does not contain the citation keys used in Chapter 2.

Missing citation keys found:

```text
fasterrcnn2015
yolo2016
ultralytics2023
saga2025
unifiedeoir2024
indraeye2024
maskrcnn2017
detr2020
cyclegan2017
pixelda2017
```

Impact:

- The PDF renders these references as `[?]`.
- Chapter 2 cannot be accepted as a literature survey until the bibliography is corrected.
- The bibliography pages currently show unrelated legal/text clustering papers.

Evidence from PDF:

- Chapter 2 contains unresolved citations such as `Faster R-CNN ... [?]`.
- Bibliography page contains old entries such as K-means, DBSCAN, legal document clustering, and TF-IDF papers.

Recommended fix:

Replace or rebuild `SVNITPhDbibtex.bib` with EO/IR, segmentation, YOLO, domain adaptation, and dataset references. At minimum, add valid entries for all missing citation keys listed above.

Fix artifact created:

`docs/latex_fixes/SVNITPhDbibtex.bib`

This replacement file contains 39 research-paper references covering EO/IR, YOLO, aerial perception, segmentation, and domain adaptation. Software/GitHub-only citations were removed. Static citation checking after replacing the extracted package bibliography reports zero missing citation keys.

### 2. Acronym List Is From the Wrong Project

Severity: Critical

Current file:

`Sections/Acr.tex`

The acronym list currently contains legal/text clustering acronyms:

```text
TF-IDF
DIGBC
BERT
RCC
LDA
DBSCAN
HAC
KNN
WCSS
PCA
DBI
```

Impact:

- This is visibly inconsistent with the EO/IR segmentation thesis.
- It appears on the PDF front matter as `List of Acronyms`.

Recommended replacement acronyms:

```text
EO: Electro-Optical
IR: Infrared
UAV: Unmanned Aerial Vehicle
YOLO: You Only Look Once
CNN: Convolutional Neural Network
RGB: Red Green Blue
IoU: Intersection over Union
mAP: mean Average Precision
AP: Average Precision
NMS: Non-Maximum Suppression
GPU: Graphics Processing Unit
HPC: High Performance Computing
```

Optional:

```text
TTA: Test-Time Augmentation
MGA: Mask-Guided Gray Augmentation
BA-MGA: Boundary-Aware Mask-Guided Gray Augmentation
```

Fix artifact created:

`docs/latex_fixes/Acr.tex`

This file is a drop-in replacement for `Sections/Acr.tex` in the online LaTeX project.

### 3. Appendix Is Wrong

Severity: Critical

Current file:

`Appendix/appndx.tex`

Current content:

```tex
\chapter{Industrial Internship Report at Siemens}
```

Impact:

- The table of contents includes `Appendix A Industrial Internship Report at Siemens`.
- This is unrelated to the EO/IR segmentation thesis.

Recommended fix:

Either remove the appendix include from `MainReport.tex`:

```tex
% \include{Appendix/appndx}
```

or replace the appendix with relevant material, such as:

- Experiment configuration summary
- Dataset class mapping
- Additional result tables
- Kaggle notebook execution notes
- Generated figure list
- Reproducibility checklist

Fix artifact created:

`docs/latex_fixes/MainReport.tex`

This drop-in replacement comments out the appendix include and the following blank page so the stale Siemens appendix is removed from the compiled report.

### 4. Broken Citations Are Visible in the PDF

Severity: Critical

The included `MainReport.pdf` contains unresolved citation markers `[?]` in Chapter 2.

Examples found in extracted PDF text:

- Faster R-CNN citation appears as `[?]`
- YOLO citation appears as `[? ?]`
- Unified EO/IR object detection citation appears as `[?]`
- IndraEye dataset citation appears as `[?]`
- CycleGAN and PixelDA citations appear as `[? ?]`

Recommended fix:

After fixing `SVNITPhDbibtex.bib`, rebuild using the proper sequence:

```text
XeLaTeX
BibTeX
XeLaTeX
XeLaTeX
```

Then verify that no `[?]` remains in the PDF.

## Major Issues

### 5. HOD Name Is a Placeholder

Severity: Major

Current setting in `MainReport.tex`:

```tex
\hodname{HODNAME}
```

Impact:

- The template may render placeholder text in some front-matter pages.

Recommended fix:

Replace with the current official HOD name, or confirm whether the class file uses its own hardcoded HOD text instead.

### 6. Class File Contains Hardcoded Personal/Administrative Details

Severity: Major

The class file `SVNITPhDReport.cls` contains hardcoded certificate and acknowledgement text, including:

- report title
- student name
- registration number
- supervisor names
- external supervisor details
- PG in-charge / department text

Examples found:

```text
Cross-Domain Semantic Segmentation in Aerial Traffic Surveillance
Mr. Ayush Panchal
P24DS013
Sameer Chivukula
Elsevier
```

Impact:

- Some front-matter pages may not fully respond to fields set in `MainReport.tex`.
- Future edits in `MainReport.tex` may not propagate everywhere.

Recommended fix:

Review `SVNITPhDReport.cls` front-matter macros and either:

1. replace hardcoded values with macros from `MainReport.tex`, or
2. keep hardcoded values but verify every displayed field manually in the PDF.

### 7. Acknowledgement Has Formatting and Name Issues

Severity: Major

Evidence from PDF:

- `guideDr. Dipti P. Rana` appears without a space.
- `thankDr. Sankita J. Patel` appears without a space.
- `Dr. Sankita J. Patel` appears in the generated acknowledgement, while `Sections/ack.tex` contains a different HOD name text.

Impact:

- Front matter looks unpolished.
- The active acknowledgement may come from the class file, not `Sections/ack.tex`.

Recommended fix:

Find the active acknowledgement macro in `SVNITPhDReport.cls`, likely `\putsvnitack`, and correct the text there. If using `Sections/ack.tex`, modify `MainReport.tex` to input that file instead of the class macro.

### 8. Abstract Source in Zip Differs From Repo Style

Severity: Major

In the zip, `Sections/abstract.tex` is wrapped inside:

```tex
\textit{ ... }
```

The online template uses:

```tex
\putsvnitabstract{
\input{./Sections/abstract}
}
```

This is acceptable if the class macro supplies the abstract heading. However, it differs from the repo-local `thesis/Sections/abstract.tex`, which uses:

```tex
\chapter*{Abstract}
\addcontentsline{toc}{chapter}{Abstract}
```

Impact:

- Copying the repo abstract directly into the online zip may duplicate the abstract heading.
- The online zip currently uses a different keyword list from the repo-local abstract.

Recommended fix:

Keep the online version without `\chapter*{Abstract}` if using `\putsvnitabstract`, but sync the text and keyword line intentionally.

### 9. List of Tables Is Disabled

Severity: Major

`MainReport.tex` has:

```tex
\borderlof
\addcontentsline{toc}{section}{List of Figures}
%\borderlot
```

The thesis contains many tables, especially in Chapter 3 and Chapter 5, but the List of Tables is commented out.

Impact:

- The report may miss a required front-matter list.

Recommended fix:

Enable the List of Tables if required by the department:

```tex
\borderlot
```

Also check whether manual `\addcontentsline` entries are duplicating or misclassifying front-matter entries.

### 10. Chapter 5 Tables Are Too Wide in PDF Text Extraction

Severity: Major

The extracted PDF text shows some Chapter 5 rows running together:

```text
E11 ... 0.70250.5250
E12 ... EO+IR0.70410.5145
```

This suggests that table spacing is tight and may visually touch or overflow in the PDF.

Impact:

- Result tables may be hard to read.
- Examiner may notice cramped numeric columns.

Recommended fix:

Use smaller font, `tabularx`, `adjustbox`, or shorten columns. Example:

```tex
\begin{table}[h]
\centering
\small
\setlength{\tabcolsep}{3pt}
...
\end{table}
```

or use:

```tex
\resizebox{\textwidth}{!}{...}
```

## Moderate Issues

### 11. Duplicate Packages in `MainReport.tex`

Severity: Moderate

Duplicate packages detected:

| Package | Count |
|---|---:|
| `natbib` | 2 |
| `subfigure` | 2 |
| `algorithm` | 2 |
| `listings` | 2 |
| `fancybox` | 2 |
| `graphicx` | 3 |
| `amsmath` | 2 |
| `booktabs` | 2 |
| `rotating` | 2 |
| `fontenc` | 2 |
| `titlesec` | 2 |

Impact:

- May not break compilation, but increases warning risk and makes the preamble messy.
- `subfigure` is obsolete and may conflict with `subcaption`.
- Both `algorithmic` and `algpseudocode` are loaded, which can conflict depending on usage.

Recommended fix:

Clean the preamble after the thesis content stabilizes. Keep only packages actually used.

### 12. Stale Auxiliary Files Are Included

Severity: Moderate

The zip includes `.aux` files:

```text
Appendix/appndx.aux
Chapter1/ch1.aux
Chapter2/ch2.aux
Chapter3/ch3.aux
Chapter4/chp4.aux
chapter5/ch5.aux
Chapter6/ch6.aux
```

Impact:

- Online LaTeX systems usually regenerate these.
- Stale auxiliary files can hide or confuse reference/bibliography issues.

Recommended fix:

Before final export, remove generated files:

```text
*.aux
*.log
*.out
*.toc
*.lof
*.lot
*.bbl
*.blg
```

Keep source files and figures only.

### 13. Many Unused Images From Reference Project

Severity: Moderate

The package contains many old images under:

- `Chapter4/`
- `chapter5/`
- `Figures/`

Examples include clustering-related or old reference names:

```text
kmeans1p.png
DBIcomp.png
digbckmeanswc.png
kmeansWordCloudc.png
```

Impact:

- Increases package clutter.
- Makes final project harder to audit.
- Risk of accidentally inserting irrelevant assets later.

Recommended fix:

Keep only images used by current TeX files. Based on static checks, current thesis figures mainly need:

- institute logo and border images
- `Figures/Chapter3/proposed_workflow.png`
- `Figures/Chapter5/*.png`

### 14. Inconsistent Folder Naming

Severity: Moderate

The package uses:

```text
Chapter1
Chapter2
Chapter3
Chapter4
chapter5
Chapter6
```

Impact:

- Works on Windows and Overleaf if the path matches exactly.
- Can cause confusion and errors when renaming or syncing on case-sensitive systems.

Recommended fix:

Rename `chapter5` to `Chapter5` and update:

```tex
\include{Chapter5/ch5}
```

Only do this if you are comfortable updating paths consistently in the online editor.

### 15. Comments in `MainReport.tex` Are Outdated

Severity: Minor to Moderate

Example:

```tex
\include{chapter5/ch5}  %future work
\include{Chapter6/ch6}  %conclusion
```

Chapter 5 is now results and discussion, not future work.

Recommended fix:

Update comments:

```tex
\include{Chapter5/ch5}  %Results and Discussion
\include{Chapter6/ch6}  %Conclusion and Future Work
```

## Content-Level Observations

### Chapter 1

Status: Strong draft.

Notes:

- Good problem framing.
- Research questions align with Chapter 6.
- Contributions still mention final model names and results. This is acceptable in Chapter 1, but make sure it does not sound like results are known before the study unless your guide is okay with this style.

### Chapter 2

Status: Good structure, but bibliography is broken.

Main issue:

- All citation keys used in this chapter are missing from the `.bib` file.

This chapter should not be considered final until the bibliography is replaced.

### Chapter 3

Status: Good design chapter.

Notes:

- Figure 3.1 exists and is included.
- Experiment notation is clean as E01-E12.
- Tables are comprehensive.

Potential improvement:

- If the workflow figure appears small or isolated, adjust figure placement/size in final PDF.

### Chapter 4

Status: Good implementation chapter.

Notes:

- Explains repository, Kaggle, evaluation, result packaging, and reproducibility.
- No figures are currently included. This is acceptable, but a methodology flow figure could make Chapter 4 more visually balanced.

### Chapter 5

Status: Strong results chapter.

Notes:

- Eight figures are included.
- Tables are complete.
- Some tables appear cramped in PDF extraction and should be visually checked in the rendered PDF.

### Chapter 6

Status: Strong conclusion chapter.

Notes:

- Research questions are answered clearly.
- Limitations and future work are appropriate.

## Recommended Fix Order

### Must Fix Before Showing Final PDF

1. Replace `SVNITPhDbibtex.bib` with correct EO/IR segmentation references.
2. Recompile and verify no `[?]` citation markers remain.
3. Replace `Sections/Acr.tex` with EO/IR and computer vision acronyms.
4. Remove or replace `Appendix/appndx.tex`.
5. Fix front-matter names and placeholders, especially `HODNAME`.
6. Check acknowledgement spacing and active acknowledgement source.

### Should Fix Before Submission

1. Enable List of Tables if required.
2. Clean duplicate packages in `MainReport.tex`.
3. Remove stale `.aux` files from the zip.
4. Remove unused old reference-report images.
5. Normalize `chapter5` to `Chapter5`.
6. Visually inspect Chapter 5 tables for spacing.

### Nice To Have

1. Add a Chapter 4 methodology figure.
2. Add an appendix containing experiment configurations and reproducibility notes.
3. Add a short note in README describing the exact compile sequence.

## Suggested Correct Acronym File

Replacement draft for `Sections/Acr.tex`:

```tex
\label{page:Acronyms}
\begin{center}
    \textbf{\Large List of Acronyms}
\end{center}

\begin{acronym}
    \acro{EO}{Electro-Optical}\vspace*{0.5mm}
    \acro{IR}{Infrared}\vspace*{0.5mm}
    \acro{UAV}{Unmanned Aerial Vehicle}\vspace*{0.5mm}
    \acro{RGB}{Red Green Blue}\vspace*{0.5mm}
    \acro{YOLO}{You Only Look Once}\vspace*{0.5mm}
    \acro{CNN}{Convolutional Neural Network}\vspace*{0.5mm}
    \acro{IoU}{Intersection over Union}\vspace*{0.5mm}
    \acro{mAP}{mean Average Precision}\vspace*{0.5mm}
    \acro{AP}{Average Precision}\vspace*{0.5mm}
    \acro{NMS}{Non-Maximum Suppression}\vspace*{0.5mm}
    \acro{GPU}{Graphics Processing Unit}\vspace*{0.5mm}
    \acro{HPC}{High Performance Computing}\vspace*{0.5mm}
    \acro{MGA}{Mask-Guided Gray Augmentation}\vspace*{0.5mm}
    \acro{BA-MGA}{Boundary-Aware Mask-Guided Gray Augmentation}\vspace*{0.5mm}
\end{acronym}
\newpage
```

## Suggested Bibliography Keys To Add

At minimum, add BibTeX entries with these exact keys:

```text
fasterrcnn2015
yolo2016
ultralytics2023
saga2025
unifiedeoir2024
indraeye2024
maskrcnn2017
detr2020
cyclegan2017
pixelda2017
```

After adding these, re-run:

```text
XeLaTeX
BibTeX
XeLaTeX
XeLaTeX
```

Then search the PDF for:

```text
[?]
```

## Final Verdict

The online LaTeX project is a good working draft, but it is not final-review ready. The body chapters are mostly aligned with the EO/IR segmentation thesis, and the figures are present. The main blockers are the stale bibliography, stale acronyms, stale appendix, and front-matter/template details.

Priority should be:

1. fix bibliography and citations,
2. replace acronyms,
3. remove stale appendix,
4. verify front matter,
5. rebuild and visually inspect the final PDF.
