# SALib — Sensitivity Analysis and Uncertainty Quantification

## Overview

This directory documents planned independent computational engineering projects using **SALib (Sensitivity Analysis Library)**, an open-source Python library for conducting sensitivity analysis.

SALib provides numerical methods for investigating how variations in model inputs influence computational outputs.

Projects in this directory will focus on parameter sensitivity, uncertainty analysis, model assessment, and applications to nuclear, safety, and space engineering systems.

## Research Interests

- Global sensitivity analysis
- Variance-based sensitivity methods
- Sobol sensitivity indices
- Morris elementary effects
- Parameter screening
- Monte Carlo and quasi-Monte Carlo sampling
- Model input uncertainty
- Sensitivity of radiation dose calculations
- Reactor thermal model sensitivity
- Reliability and risk model sensitivity
- Numerical convergence of sensitivity estimates
- Risk-informed engineering decision support

## Software

- **Primary software:** SALib
- **Programming language:** Python
- **Supporting libraries:** NumPy, SciPy, pandas, Matplotlib
- **Related software:** RAVEN, OpenMC, MOOSE
- **Computational approach:** Statistical sampling and sensitivity analysis

## Planned Computational Exercises

### Project 01 — Analytical Benchmark Sensitivity Study

**Status: Planned.**

Apply SALib to a mathematical benchmark function with known sensitivity characteristics.

Calculate sensitivity indices and compare results with analytical or published reference values.

### Project 02 — Morris Parameter Screening

**Status: Planned.**

Apply the Morris elementary-effects method to identify influential parameters in a simplified engineering model.

### Project 03 — Reactor Thermal Model Sensitivity

**Status: Planned.**

Investigate how uncertainties in thermal conductivity, heat generation, and boundary conditions influence the predicted temperature of a simplified reactor component.

### Project 04 — Radiation Dose Model Sensitivity

**Status: Planned.**

Evaluate the influence of selected input assumptions on the results of a simplified radiation dose model.

### Project 05 — Reliability Model Sensitivity

**Status: Planned.**

Investigate how component failure probabilities influence an illustrative system failure probability.

### Project 06 — Space Systems Parameter Sensitivity

**Status: Planned.**

Develop a conceptual space engineering model and examine the relative importance of selected uncertain design or environmental inputs.

## Project Documentation Standards

Each completed project will include:

- Scientific or engineering objective
- Mathematical model and governing equations
- Input parameters and uncertainty ranges
- Sampling methodology
- SALib configurations and Python source code
- Numerical convergence assessments
- Sensitivity indices and scientific visualizations
- Independent analytical or reference comparisons
- Interpretation and limitations
- LaTeX technical reports and PDFs
- Reproducibility instructions and references

## Verification and Validation

Sensitivity estimates will be evaluated through appropriate convergence studies, analytical checks, or published reference problems.

Sensitivity measures depend on the selected model, parameter ranges, input distributions, and assumptions.

## Reproducibility

Each project will document the SALib version, random seeds where applicable, parameter definitions, sample sizes, and analysis methods.

## Publication Policy

Only independently developed code, original documentation, and publicly distributable scientific information will be published.

Employer-owned, proprietary, export-controlled, restricted-licensed, and non-public materials will be excluded.

## Status

**Software installation not yet verified. Computational exercises planned.**

Completed analyses and results will be added after the software has been installed and tested.
