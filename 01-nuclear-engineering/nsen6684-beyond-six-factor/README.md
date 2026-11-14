# Beyond the Six-Factor Formula: Neutron Leakage, Spectral Effects, and Reactivity Feedback in Compact Space Fission Reactors

**Irais Strong** · Ph.D. Program in Nuclear Engineering · Idaho State University · NSEN 6684 (Reactor Physics), Fall 2026

> **Thesis.** Classical neutron life-cycle theory provides the conceptual foundation for criticality, but compact fast-spectrum space reactors require more detailed consideration of neutron transport, leakage, reflector interactions, and temperature-dependent reactivity.

▶ **Video:** _coming soon_ · 📄 **[Slides (PDF)](presentation/NSEN6684_Beyond_Six_Factor.pdf)** · 📘 **[Technical report (PDF)](report/NSEN6684_Beyond_Six_Factor_Report.pdf)** · 🌐 **[Portfolio page](https://istrong8.github.io/professional-portfolio/#work)**

This repository holds an ~18-minute graduate presentation and everything behind it:

- the slide deck;
- the narration script;
- a LaTeX technical report;
- a verified Monte Carlo and diffusion analysis that produces every calculated number;
- OpenMC inputs for the next, higher-fidelity step.

> **Scope.** Academic coursework using only public sources. The calculations use the idealized LA-13511 analytic-benchmark cross sections, so they are mathematical illustrations, **not** predictions for KRUSTY or any other reactor. KRUSTY values come from the cited papers. Views are my own and do not represent any employer.

## Contents

| Folder | What's inside |
|---|---|
| [`presentation/`](presentation/) | `NSEN6684_Beyond_Six_Factor.pdf` (view in the browser) and `NSEN6684_Beyond_Six_Factor.pptx`: 13 content slides + references, dark 16:9, full speaker notes, clickable section navigation, fade transitions. `build_deck.js` regenerates it. |
| [`narration/`](narration/) | `NSEN6684_Narration_Script.md`: ~2,300-word script with slide numbers, titles and target times (18:00). |
| [`report/`](report/) | `NSEN6684_Beyond_Six_Factor_Report.tex`, `references.bib`, compiled PDF. See [`report/README.md`](report/README.md) for Windows / VS Code build steps. |
| [`code/`](code/) | `benchmarks.py` (published constants), `mc_transport.py` (multigroup Monte Carlo k-eigenvalue solver), `diffusion.py`, `run_analysis.py` (all studies), `make_figures.py`, `make_diagrams.py`. |
| [`results/`](results/) | `analysis_output.txt` (every printed value) and `analysis_results.json`. |
| [`figures/`](figures/) | Report figures (PNG + PDF); `figures/dark/` holds slide versions. |
| [`openmc/`](openmc/) | OpenMC multigroup inputs reproducing the benchmarks, plus the continuous-energy plan. **Not yet run.** |
| [`youtube/`](youtube/) | Title, description and chapter timestamps for the upload. |

## Key results

**Verification.** The Monte Carlo solver reproduces five exact LA-13511 transport solutions (bare, three reflected, and two-group spheres) within ≈1σ (σ ≈ 0.0003).

| Finding | Value | Type |
|---|---|---|
| One-group diffusion error in k_eff at exactly critical compact configurations | −6 % bare, −10 to −12 % reflected | calculated |
| Diffusion critical radius, bare sphere | 7.97 cm vs exact 7.43 cm (+7.3 %) | calculated |
| Diffusion k error vs size | 9.8 % at 1.3 λ_tr → 1.9 % at 4.6 λ_tr | calculated |
| Leakage fraction, 4–14 cm spheres | 75 % → 32 % | calculated |
| Reflector savings (1–3 mfp), transport | 1.0–1.4 cm; slab formula ×2.7–3.8 too high | calculated |
| Fissions by reflector-returned neutrons | 15–19 % | calculated |
| Fast share: infinite-medium flux / leakage | 32 % / 45 % | calculated |
| One-group spectral-collapse error in R_c | −1.1 % (−0.6 % leakage-weighted) | calculated |
| Expansion feedback, idealized sphere | −0.36 to −0.41 ¢/K (KRUSTY expansion share ≈ −0.17 ¢/K) | calculated vs published |
| KRUSTY platen (reflector) worth | 10.7–12.0 ¢/mm vs B₄C rod ≈ 4 ¢/mm | observed |
| KRUSTY fuel feedback | ≈ −0.2 ¢/°C near 800 °C; passive load following | observed |

## Reproduce everything

```bash
# Python 3.9+
pip install -r code/requirements.txt
cd code
python benchmarks.py                 # checks published constants
python run_analysis.py               # ~4-5 min (use --quick for ~20 s, larger error bars)
python make_figures.py && python make_figures.py --dark
python make_diagrams.py && python make_diagrams.py --dark
cd ..

# Slides (Node.js 18+)
cd presentation && npm install && npm run build && cd ..

# Report: see report/README.md
```

Speaker notes are read from `narration/NSEN6684_Narration_Script.md` at build time, so editing the script and rebuilding keeps them in sync.

## Key references

- A. Sood, R. A. Forster, D. K. Parsons, *Analytical Benchmark Test Set for Criticality Code Verification*, LA-13511 (1999); *Prog. Nucl. Energy* 42, 55–106 (2003).
- D. I. Poston et al., "KRUSTY Reactor Design," *Nucl. Technol.* 206 (sup1), S13–S30 (2020).
- D. I. Poston et al., "Results of the KRUSTY Nuclear System Test," *Nucl. Technol.* 206 (sup1), S89–S117 (2020).
- K. N. Stolte et al., "Benchmark of the KRUSTY Component Critical Configurations," *Nucl. Technol.* 208(4), 625–643 (2022).
- J. J. Duderstadt, L. J. Hamilton, *Nuclear Reactor Analysis* (1976); G. I. Bell, S. Glasstone, *Nuclear Reactor Theory* (1970).

Full bibliography: [`report/references.bib`](report/references.bib).

## License

Code: MIT ([`LICENSE`](LICENSE)). Text, slides and figures: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). All figures are original. The KRUSTY component data in `fig_krusty_feedback` are re-plotted from Poston et al. (2020), Table II, with citation.
