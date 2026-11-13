# Ku Saga: Planet X — Orbital Dynamics & Scientific Worldbuilding

**Research author and creative originator:** Irais Strong  
**Project affiliation:** Atom-Collab  
**Research release:** v0.3.1 (publication review package)

## Purpose

This research investigates the physical assumptions behind the fictional **Ku Saga: Planet X** setting. The objective is to use numerical modeling, scientific reasoning, and documented limitations to evaluate which fictional planetary-system configurations are physically plausible and which elements of the saga may need revision.

**This is not a claim that Planet X, the depicted binary, or the companion moon has been observed.** The project is scientific worldbuilding and exploratory computational research, not peer-reviewed validation of habitability or long-term stability.

## Modeled System

The archive models a hypothetical Sun-like star and stellar-mass black hole in a binary configuration, five planets including **Planet X**, and its companion moon. The scenario explores gravitational dynamics, orbital configuration, selected parameter cases, and simplified climate-related screening.

## Computational Work

- Newtonian eight-body numerical demonstration, including a velocity-Verlet implementation.
- REBOUND-based orbital scenarios using IAS15.
- Short-duration integrator cross-checks using velocity-Verlet, SciPy DOP853, and REBOUND IAS15.
- Orbital diagnostics and selected 200-year and 1,000-year author-reported scenario outputs.
- Parameter screening, figures, and exploratory climate calculations.
- An offline interactive orbital visualization with precomputed positions.

## How the Science Informs the Story

Numerical studies can help identify orbital configurations, environmental constraints, and scientific inconsistencies relevant to the Ku Saga. A setting's fictional status is preserved; any resulting story revisions will be creative decisions informed by these technical studies.

## Source Package & Reproducibility

The author has supplied the research archive **Ku_Saga_Planet_X_V031_Final_Research** together with previous research versions and an HTML viewer. The full reviewed distribution contains Python sources, tests, dependencies, figures, JSON/CSV diagnostics, LaTeX/PDF technical documentation, and an offline orbital viewer.

**Publication status:** This repository page documents the project. The full file set is being transferred separately; until the files appear below, they should not be described as hosted here.

Once uploaded, the intended paths are:

- `src/` — numerical solvers, REBOUND scenarios, validation, and screening scripts
- `tests/` — original test scripts
- `reports/` — LaTeX research paper, PDF, validation notes, sources, and future studies
- `figures/` — generated plots and diagrams
- `results/`, `scenario_results/`, and `user_reported_runs/` — example diagnostics and numerical outputs
- `web/index.html` — offline interactive orbital viewer
- `requirements*.txt` — Python dependency declarations

## Numerical Caveats

The v0.3.1 package reports short (0.25-year) three-integrator comparisons and user-recorded longer scenario runs. Some numerical outcomes are transcribed summaries rather than independently regenerated original trajectory files. Short-term agreement across numerical methods does not demonstrate long-term physical stability, habitability, or real-world astrophysical plausibility.

The original scripts were reorganized into a publication folder structure; import paths and execution from that structure require testing before it can be represented as a validated turnkey release.

## Authorship and Rights

Irais Strong confirmed that she authored the research and authorized publication of its scientific code, viewer, technical figures, and reports. Atom-Collab is the stated project affiliation. No open-source reuse license has yet been selected; public access alone does not grant a license to redistribute, adapt, or commercialize the project.

Unpublished literary manuscripts and confidential business materials are not included.

## Status

**Exploratory technical research; publication in progress; not peer reviewed.** The full archive, executable layout, and independent numerical reproduction require follow-up verification.
