# Irais Strong — Engineering Portfolio

Nuclear facility safety analysis, space fission systems research, and scientific computing.

**Website:** https://istrong8.github.io/professional-portfolio/
**LinkedIn:** https://www.linkedin.com/in/iraisstrong/
**Résumé:** [PDF](docs/resume/Gemma-Irais-Strong-Resume.pdf) (source: `resume/resume.tex`)
**Email:** irastrong3@gmail.com

## Projects

| Project | Status | Where |
|---|---|---|
| **Ku Saga: Planet X** — orbital dynamics of a fictional star–black hole binary system (velocity-Verlet, REBOUND/IAS15, SciPy DOP853 cross-checks) | Live viewer; source release in progress | [Viewer](https://istrong8.github.io/professional-portfolio/planet_x_live.html) · [Methods & limitations](02-space-astronomy/rebound/ku-saga-planet-x/) |
| **Beyond the Six-Factor Formula** (NSEN 6684, ISU) — neutron leakage, spectral effects and reactivity feedback in compact space reactors; in-house Monte Carlo verified against exact LA-13511 benchmarks, diffusion-error study, KRUSTY feedback analysis | Slides, narration, report and code complete; OpenMC step not yet run | [Project](01-nuclear-engineering/nsen6684-beyond-six-factor/) · [Slides PDF](01-nuclear-engineering/nsen6684-beyond-six-factor/presentation/NSEN6684_Beyond_Six_Factor.pdf) · [Report PDF](01-nuclear-engineering/nsen6684-beyond-six-factor/report/NSEN6684_Beyond_Six_Factor_Report.pdf) |
| **OpenMC pin-cell study** — k-eff, flux, multigroup spectra, fission rates, Monte Carlo convergence | Exercises complete; write-up in preparation | [Notes](01-nuclear-engineering/openmc/) |
| **TLECUIL** — first-order fission surface power sizer; benchmarked against four published NASA designs | v0.2.1, open source (BSD-3-Clause) | [Calculator](https://istrong8.github.io/tlecuil/) · [Code](https://github.com/istrong8/tlecuil) |

## Reference pages

| Page | What it covers | Where |
|---|---|---|
| **Advanced reactor tracker** | Stage-by-stage DOE authorization and NRC licensing status of 21 projects, 2026 criticalities, Launch Pad, uranium conversion companies, GAIN and NRIC. Dated; refreshed monthly. | [Tracker](https://istrong8.github.io/professional-portfolio/licensing/tracker.html) |
| **Licensing pathways** | Licensing vs regulation, DOE-STD-1271 authorization, 10 CFR Parts 40, 50, 52, 53, the §50.43(f) bridge rule, review timeframes, fuel-cycle CFR map. | [Pathways](https://istrong8.github.io/professional-portfolio/licensing/pathways.html) |
| **Nuclear software QA** | DOE G 414.1-4 and NRC/NQA-1 software categorization, the Subpart 2.7 life cycle, public SQA program examples, accepted codes, TLECUIL worked example. | [Software QA](https://istrong8.github.io/professional-portfolio/licensing/software-qa.html) |

All three are compiled from public NRC, DOE, Federal Register and trade-press sources and link to them; no documents are hosted.

## Writing

- **Reframing Nuclear Licensing: The FSAR as a Tool, Not a Barrier** — white paper, NE 5599, Idaho State University, May 2025. [PDF](docs/papers/reframing-nuclear-licensing-fsar.pdf) · [LaTeX source](writing/fsar-white-paper/). The Oklo case study covers the NRC's 2022 denial; a footnote notes Oklo's 2025 NRC readiness assessment.

Planned studies and areas of exploration are listed in [`ROADMAP.md`](ROADMAP.md).

## Repository layout

```
docs/                       GitHub Pages site
  index.html                home: work, expertise, experience, standards
  toolkit.html              analysis codes and tools
  moon-mars*.html, space-reactors.html   Moon & Mars research set
  licensing/                licensing & software QA set (hub, tracker, pathways, software-qa)
  assets/css/site.css       home and toolkit styles; page.css for the licensing set
  planet_x_live.html        Planet X viewer
01-nuclear-engineering/     OpenMC work; NSEN 6684 space-reactor physics study
02-space-astronomy/         Planet X orbital dynamics
writing/                    white paper source (LaTeX)
ROADMAP.md                  planned work
```

## Publication policy

Everything here is personal, independently developed work. Employer-owned, proprietary, export-controlled, restricted-license, or non-public information is not included, and nothing here represents any employer.
