# RAVEN — Risk Analysis, Uncertainty Quantification and Computational Modeling

## Overview

This directory documents planned independent computational engineering projects using **RAVEN (Risk Analysis Virtual Environment)**, a software framework developed at Idaho National Laboratory.

RAVEN provides computational capabilities for uncertainty quantification, statistical sampling, sensitivity analysis, surrogate modeling, optimization, and risk-informed engineering studies.

Projects in this directory will explore probabilistic modeling, uncertainty propagation, computational risk assessment, and applications to nuclear and space engineering systems.

## Research Interests

- Probabilistic risk assessment (PRA)
- Uncertainty quantification (UQ)
- Monte Carlo sampling
- Latin hypercube sampling
- Sensitivity analysis
- Statistical distributions and parameter uncertainty
- Surrogate and reduced-order modeling
- Reliability engineering
- Risk-informed decision-making
- Model calibration and optimization
- Applications to reactor safety and space systems

## Software

- **Primary software:** RAVEN
- **Supporting languages:** Python and RAVEN input configurations
- **Supporting libraries:** NumPy, SciPy, pandas, Matplotlib
- **Related tools:** OpenMC, MOOSE, SALib, and other compatible analysis tools

## Planned Computational Exercises

### Project 01 — Monte Carlo Uncertainty Propagation

**Status: Planned.**

Develop a simplified engineering model with uncertain input parameters.

Use statistical sampling to investigate output distributions, confidence intervals, and sensitivity to input assumptions.

### Project 02 — Parameter Sensitivity Analysis

**Status: Planned.**

Investigate the influence of selected model parameters on an engineering output using appropriate sensitivity analysis methods.

### Project 03 — Surrogate Model Development

**Status: Planned.**

Construct a simplified surrogate model from computational results and evaluate its predictive performance against reference model outputs.

### Project 04 — Reliability and Failure Probability Analysis

**Status: Planned.**

Develop an illustrative engineering reliability study using clearly documented failure assumptions and probability distributions.

### Project 05 — Reactor Thermal Model Uncertainty

**Status: Planned.**

Evaluate the propagation of selected material-property and boundary-condition uncertainties through a simplified reactor thermal model.

### Project 06 — Space System Risk-Informed Analysis

**Status: Planned.**

Develop a conceptual risk-informed engineering study for a hypothetical space system using independently defined and clearly labeled illustrative assumptions.

## Project Documentation Standards

Each completed project will include:

- Engineering problem and analysis objectives
- Mathematical and statistical methodology
- Input probability distributions
- Model assumptions and uncertainties
- RAVEN configurations and original Python code
- Sampling methods and convergence assessment
- Numerical outputs and probability distributions
- Sensitivity results and scientific visualizations
- Verification and applicable validation comparisons
- Limitations and interpretation
- LaTeX technical reports and compiled PDFs
- Reproducibility instructions and references

## Verification and Validation

Projects will distinguish numerical verification, statistical convergence, and validation against experimental or reference information where applicable.

Illustrative reliability parameters will not be represented as measured component failure probabilities.

## Reproducibility

Each project will document software versions, statistical distributions, sampling settings, random seeds, numerical models, and computational dependencies.

Large simulation outputs and restricted data will not be committed to the public repository.

## Publication Policy

Only independently developed code, original documentation, and publicly distributable information will be published.

Employer-owned, proprietary, export-controlled, restricted-licensed, and non-public materials will be excluded.

## Status

**Software installation not yet verified. Computational exercises planned.**

This directory is an organizational starting point. Results will be added after the software has been installed, tested, and used for documented computational exercises.
