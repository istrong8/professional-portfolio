# Technical report — compile instructions

Files in this folder:

| File | Purpose |
|---|---|
| `NSEN6684_Beyond_Six_Factor_Report.tex` | report source |
| `references.bib` | BibTeX bibliography (`unsrtnat` style via `natbib`) |
| `NSEN6684_Beyond_Six_Factor_Report.pdf` | compiled report |
| `.vscode/settings.json` | LaTeX Workshop build recipes for VS Code on Windows |

The report reads figures from `../figures/` and code listings from `../code/` (`mc_transport.py`, `diffusion.py`). Keep the repository folder structure intact, and compile from inside this `report/` folder.

## Windows + VS Code (recommended)

1. Install a LaTeX distribution:
   - **MiKTeX** (https://miktex.org). During setup, choose *"Install missing packages on-the-fly: Yes"*.
   - or **TeX Live** (https://tug.org/texlive).
2. Install VS Code and the **LaTeX Workshop** extension (James Yu).
3. Open the **`report` folder** in VS Code (*File → Open Folder…*). That way the bundled `.vscode/settings.json` is picked up.
4. Open the `.tex` file and press **Ctrl+Alt+B** (or click *Build LaTeX project* in the TeX sidebar).
   The default recipe is `pdflatex → bibtex → pdflatex → pdflatex`, which needs nothing beyond MiKTeX.
5. View the PDF with **Ctrl+Alt+V**.

> The `latexmk` recipe is also provided. On MiKTeX, latexmk needs Perl (for example Strawberry Perl). TeX Live includes Perl.

## Command line (any OS)

```bash
cd report
pdflatex NSEN6684_Beyond_Six_Factor_Report.tex
bibtex   NSEN6684_Beyond_Six_Factor_Report
pdflatex NSEN6684_Beyond_Six_Factor_Report.tex
pdflatex NSEN6684_Beyond_Six_Factor_Report.tex
```

or, with Perl available: `latexmk -pdf NSEN6684_Beyond_Six_Factor_Report.tex`

## Packages used

All are in a standard MiKTeX or TeX Live install: `lmodern`, `geometry`, `microtype`, `amsmath`, `amssymb`, `siunitx`, `booktabs`, `tabularx`, `graphicx`, `float`, `caption`, `xcolor`, `listings`, `textcomp`, `enumitem`, `natbib`, `hyperref`.

## Regenerating figures

The figures are produced by the Python scripts. From the repository root:

```bash
pip install -r code/requirements.txt
cd code
python run_analysis.py
python make_figures.py
python make_diagrams.py
```

Then rebuild the report.

## Troubleshooting

- **`File 'fig_life_cycle' not found`**: the `figures/` folder is missing or you compiled from another directory. Run the Python scripts above, or open the `report` folder itself in VS Code.
- **Citations show as `[?]`**: BibTeX did not run. Use the full recipe (pdflatex → bibtex → pdflatex ×2).
- **Undefined references on the first pass** are normal. They resolve on the later passes.
