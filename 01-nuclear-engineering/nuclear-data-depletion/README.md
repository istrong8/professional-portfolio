# Nuclear Data, Fuel Depletion & Isotopic Analysis

## Overview

This directory documents independent computational nuclear engineering projects involving nuclear data analysis, radioactive decay, isotopic inventories, fuel depletion, and nuclear reaction modeling.

These studies examine how nuclear material compositions evolve through radioactive decay, neutron-induced reactions, and irradiation.

The objective is to demonstrate computational methods relevant to reactor physics, nuclear fuel behavior, radiation source characterization, and scientific analysis of nuclear systems.

## Research Interests

- Radioactive decay and decay chains
- Isotopic inventory calculations
- Nuclear fuel depletion and burnup
- Neutron-induced transmutation
- Fission product generation
- Actinide evolution
- Nuclear reaction rates
- Cross-section data and evaluation
- Decay heat and source characterization
- Numerical methods for coupled inventory equations
- Verification and uncertainty analysis

## Computational Tools

Projects may use:

- **OpenMC:** Monte Carlo transport and depletion calculations
- **FUDGE:** Evaluated nuclear reaction data analysis
- **NJOY21:** Nuclear data processing
- **radioactivedecay:** Python radioactive decay and inventory calculations
- **SciPy:** Numerical solution of decay and transmutation equations
- **NumPy and pandas:** Scientific data processing
- **Matplotlib:** Scientific visualization

Additional software will be documented when used.

## Planned Computational Exercises

### Project 01 — Radioactive Decay Chain Analysis

**Status: Planned.**

Implement and verify a simplified radioactive decay-chain calculation.

Compare the numerical solution with analytical Bateman equations where applicable.

### Project 02 — Isotopic Inventory Evolution

**Status: Planned.**

Investigate how the composition of an initially specified radioactive material changes over time through radioactive decay.

### Project 03 — Fuel Burnup and Depletion

**Status: Planned.**

Develop a simplified depletion study using appropriate neutron transport and inventory modeling capabilities.

Examine the evolution of selected fuel isotopes under documented irradiation assumptions.

### Project 04 — Fission Product Inventory Analysis

**Status: Planned.**

Investigate representative fission product inventories and relevant radioactive decay characteristics.

### Project 05 — Decay Heat Evolution

**Status: Planned.**

Develop an introductory calculation of radioactive decay heat following a clearly defined irradiation or inventory scenario.

### Project 06 — Nuclear Data Sensitivity

**Status: Planned.**

Investigate how selected nuclear data assumptions influence simplified inventory or reaction-rate calculations.

## Project Documentation Standards

Each completed project will include:

- Scientific objective and theoretical background
- Governing equations and numerical methods
- Initial isotopic composition
- Nuclear data and decay data sources
- Modeling assumptions and boundary conditions
- Python source code and computational inputs
- Numerical results and scientific figures
- Analytical verification or applicable benchmark comparisons
- Uncertainty and sensitivity discussion
- Model limitations
- LaTeX technical report and compiled PDF
- Reproducibility instructions and references

## Verification and Validation

Numerical results will be checked against appropriate analytical solutions, independent calculations, or publicly available benchmark data where possible.

Software execution alone will not be considered evidence of physical validation.

## Reproducibility

Each project will document the software versions, nuclear data libraries, simulation parameters, initial compositions, and numerical solver settings used.

Large simulation outputs, restricted nuclear data libraries, and non-public materials will not be included directly in the repository.

## Publication Policy

Only independently developed code, original documentation, and publicly distributable scientific information will be published.

Employer-owned, proprietary, export-controlled, restricted-licensed, and non-public research materials will be excluded.

## Status

**Research area established. Computational projects planned.**

Related OpenMC and FUDGE tools have previously been used or tested. Depletion-specific project results have not yet been documented in this directory.
