# HYSPLIT — Atmospheric Transport, Dispersion and Consequence Modeling

## Overview

This directory documents planned independent computational projects using **HYSPLIT (Hybrid Single-Particle Lagrangian Integrated Trajectory)**, an atmospheric transport and dispersion modeling system developed by the National Oceanic and Atmospheric Administration (NOAA).

HYSPLIT supports the analysis of atmospheric trajectories, dispersion, and deposition of airborne materials.

Projects in this directory will focus on environmental transport, atmospheric dispersion modeling, accident consequence analysis, and numerical assessment of hypothetical airborne releases.

## Research Interests

- Atmospheric transport and dispersion
- Air-mass trajectory analysis
- Pollutant plume modeling
- Radiological atmospheric release scenarios
- Atmospheric deposition
- Meteorological influences on dispersion
- Source term and release-duration sensitivity
- Environmental consequence modeling
- Uncertainty and sensitivity analysis
- Geographic visualization of model results

## Software

- **Primary software:** NOAA HYSPLIT
- **Supporting tools:** Python, NumPy, pandas, Matplotlib
- **Geographic analysis:** QGIS and GeoPandas
- **Meteorological inputs:** Compatible meteorological datasets with appropriate redistribution permissions

HYSPLIT software access and applicable licensing or distribution conditions will be checked before publishing any associated software or third-party data.

## Planned Computational Exercises

### Project 01 — Atmospheric Trajectory Analysis

**Status: Planned.**

Calculate and visualize representative forward and backward air-mass trajectories using suitable meteorological inputs.

### Project 02 — Hypothetical Atmospheric Release

**Status: Planned.**

Model atmospheric transport and dispersion for a simplified, hypothetical release using independently specified source parameters.

### Project 03 — Meteorological Sensitivity

**Status: Planned.**

Investigate how selected meteorological conditions influence modeled transport pathways and concentration distributions.

### Project 04 — Deposition Analysis

**Status: Planned.**

Investigate simplified atmospheric deposition results under documented modeling assumptions.

### Project 05 — Radiological Consequence Modeling

**Status: Planned.**

Explore a hypothetical radiological atmospheric release and document how transport modeling outputs could inform subsequent consequence calculations.

Any dose assessment will require appropriately justified source terms, radionuclide properties, exposure pathways, and dose conversion factors.

### Project 06 — Geographic Visualization

**Status: Planned.**

Develop maps of simulated atmospheric transport and dispersion outputs using compatible geospatial tools.

## Project Documentation Standards

Each completed exercise will include:

- Engineering objective and scenario definition
- Source parameters and release assumptions
- Meteorological data sources and time periods
- Atmospheric transport settings
- Model configuration and input files
- Original scripts and supporting calculations
- Plume or trajectory visualizations
- Sensitivity studies and uncertainty discussion
- Verification or comparison with reference data
- Modeling limitations
- LaTeX technical reports and compiled PDFs
- Reproducibility instructions and references

## Modeling Limitations

HYSPLIT is an atmospheric transport model. Its terrestrial atmospheric assumptions do not directly describe particle transport in a lunar vacuum or all conditions in the Martian atmosphere.

Any planetary application would require separate physical modeling, environmental data, and appropriate verification and validation.

Predicted atmospheric concentrations and deposition are not equivalent to radiation dose without additional consequence calculations.

## Reproducibility

Each completed project will document the HYSPLIT version, meteorological inputs, simulation domain, source definition, and relevant computational settings.

Large or redistribution-restricted meteorological datasets will not be committed to this repository.

## Publication Policy

Only independently developed models, original documentation, and publicly distributable data will be published.

Employer-owned, proprietary, export-controlled, restricted-licensed, and non-public information will be excluded.

## Status

**Software installation not yet verified. Computational exercises planned.**

This directory is an organizational starting point. Simulation results will be added after the required software and input data have been verified.
