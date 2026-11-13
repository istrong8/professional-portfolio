# OpenMC — Monte Carlo Reactor Physics and Radiation Transport

## Overview

This directory documents independent computational nuclear engineering projects using **OpenMC**, an open-source Monte Carlo particle transport code.

OpenMC supports neutron and photon transport calculations, reactor criticality analysis, reaction-rate tallies, depletion studies, and scientific investigations of nuclear systems.

Projects in this directory focus on reactor physics, numerical methods, radiation transport, model verification, and reproducible computational research.

## Research Interests

- Monte Carlo neutron transport
- Reactor criticality and effective multiplication factor
- Neutron energy spectra and multigroup flux analysis
- Fuel composition and isotope effects
- Neutron reaction rates
- Reactor fuel pin and assembly modeling
- Radiation transport and shielding
- Nuclear data sensitivity
- Depletion and fuel burnup
- Applications to space fission power systems

## Software

- **Primary software:** OpenMC
- **Programming language:** Python
- **Supporting libraries:** NumPy, SciPy, pandas, Matplotlib
- **Nuclear data:** Compatible evaluated nuclear data libraries, subject to applicable distribution conditions

## Computational Projects

### Project 01 — Uranium Fuel Pin-Cell Study

**Status: Computational exercises performed; technical documentation in development.**

This project examines the neutron behavior of a uranium-fueled pin-cell configuration.

Previously explored quantities include:

- Effective multiplication factor
- Neutron flux distributions
- Multigroup neutron energy spectra
- Fission reaction rates
- Fuel isotope contributions
- Monte Carlo convergence
- Numerical results and scientific visualization

The final portfolio project will include reproducible models, numerical results, verification checks, and a LaTeX technical report.

Further OpenMC studies (criticality benchmark, shielding, nuclear data sensitivity, conceptual space reactor neutronics) are listed in [`ROADMAP.md`](../../ROADMAP.md).

## Project Documentation Standards

Each completed project will contain, where applicable:

- Engineering problem and objectives
- Governing physics and modeling assumptions
- Geometry and material definitions
- Nuclear data specifications
- Python source code and simulation inputs
- Computational settings and numerical methodology
- Convergence and verification studies
- Scientific figures and quantitative results
- Uncertainty and limitations
- LaTeX technical report and compiled PDF
- References and reproducibility instructions

## Reproducibility

Software versions, dependencies, nuclear data sources, simulation settings, and computational assumptions will be documented for each completed study.

Large simulation outputs and restricted nuclear data files will not be committed directly to the repository.

## Publication Policy

All published work will be independently developed or explicitly authorized for public release.

Employer-owned, proprietary, export-controlled, restricted-licensed, or non-public research information will not be included.

## Status

**OpenMC installed and previously tested. Initial pin-cell computational exercises completed. Portfolio documentation in preparation.**
