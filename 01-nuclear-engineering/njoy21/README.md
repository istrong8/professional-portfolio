# NJOY21 — Nuclear Data Processing and Cross-Section Preparation

## Overview

This directory documents planned independent computational projects using **NJOY21**, a nuclear data processing system developed at Los Alamos National Laboratory.

NJOY21 provides tools for processing evaluated nuclear data into application-ready forms used in radiation transport, reactor physics, and nuclear engineering calculations.

Projects in this directory will focus on nuclear data processing methods, cross-section preparation, reaction data analysis, and reproducible computational workflows.

## Research Interests

- Evaluated nuclear reaction data
- Nuclear cross-section processing
- Neutron resonance reconstruction
- Doppler broadening and temperature effects
- Nuclear data formats and conversion
- Continuous-energy transport data preparation
- Thermal scattering data
- Nuclear data verification and comparison
- Sensitivity to processing assumptions
- Applications to reactor physics and shielding

## Software

- **Primary software:** NJOY21
- **Programming and build environment:** C++ and supported build tools
- **Supporting analysis:** Python, NumPy, SciPy, Matplotlib
- **Related software:** FUDGE, OpenMC
- **Input data:** Publicly distributable evaluated nuclear data libraries

## Planned Computational Exercises

### Project 01 — Nuclear Data Processing Workflow

**Status: Planned.**

Establish a reproducible workflow for processing selected evaluated nuclear reaction data.

Document input evaluations, processing settings, output formats, and software version.

### Project 02 — Resonance Reconstruction Study

**Status: Planned.**

Investigate resonance-region cross-section behavior and compare suitable processed results against reference data.

### Project 03 — Temperature-Dependent Cross Sections

**Status: Planned.**

Explore the effects of Doppler broadening on selected neutron reaction cross sections at representative temperatures.

### Project 04 — Thermal Scattering Data Investigation

**Status: Planned.**

Investigate thermal scattering treatments and their relevance to neutron transport calculations.

### Project 05 — Nuclear Data Comparison for Transport Applications

**Status: Planned.**

Compare selected processed nuclear data outputs and document differences arising from evaluations or processing assumptions.

## Project Documentation Standards

Each completed project will include:

- Engineering objective and theoretical background
- Nuclear data library and evaluation version
- Isotope and reaction identification
- Processing modules and parameter settings
- Input and output data formats
- Original processing scripts and analysis code
- Numerical figures and results
- Verification and appropriate reference comparisons
- Sensitivity and uncertainty discussion
- LaTeX technical reports and compiled PDFs
- Reproducibility instructions and references

## Reproducibility

Each project will document the NJOY21 version, applicable build configuration, data sources, processing parameters, and numerical analysis methods.

Large or redistribution-restricted nuclear data libraries will not be committed to GitHub.

## Publication Policy

Only independently developed scripts, original documentation, and publicly distributable nuclear data information will be published.

Employer-owned, proprietary, export-controlled, restricted-licensed, and non-public materials will be excluded.

## Status

**Software installation not yet verified. Computational exercises planned.**

This directory is an organizational starting point. Completed numerical studies will be added after software installation and verification.
