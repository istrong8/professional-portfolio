# HotSpot — Radiological Consequence and Atmospheric Dispersion Analysis

## Overview

This directory documents planned independent computational exercises using **HotSpot**, a radiological consequence assessment software package developed at Lawrence Livermore National Laboratory (LLNL).

HotSpot provides simplified methods for estimating atmospheric dispersion and potential radiation exposure associated with hypothetical releases of radioactive material.

Projects in this directory will focus on radiological consequence assessment, source-term assumptions, atmospheric dispersion, radiation dose estimation, and sensitivity analysis.

## Research Interests

- Radiological accident consequence analysis
- Atmospheric dispersion of radioactive materials
- Gaussian plume modeling
- Radionuclide source-term characterization
- Radiation dose assessment
- Inhalation and external exposure pathways
- Meteorological sensitivity
- Atmospheric stability and wind conditions
- Emergency planning and consequence screening
- Model uncertainty and limitations
- Comparison of atmospheric dispersion methods

## Software

- **Primary software:** HotSpot Health Physics Codes
- **Developer:** Lawrence Livermore National Laboratory
- **Supporting tools:** Python, NumPy, pandas, Matplotlib
- **Related modeling tools:** HYSPLIT, QGIS

HotSpot is distributed under applicable access and licensing conditions. Its availability does not imply that the software itself may be redistributed.

## Planned Computational Exercises

### Project 01 — Introductory Radiological Release Assessment

**Status: Planned.**

Develop a simplified hypothetical release scenario and investigate the resulting atmospheric concentration and radiological consequence estimates.

Document the radionuclide assumptions, release conditions, meteorological parameters, and modeling limitations.

### Project 02 — Meteorological Sensitivity Analysis

**Status: Planned.**

Investigate how selected wind speeds and atmospheric stability classes influence predicted dispersion and consequence estimates.

### Project 03 — Release Parameter Sensitivity

**Status: Planned.**

Evaluate the influence of selected source-term parameters on calculated consequences within the assumptions of the selected model.

### Project 04 — Dose Versus Distance Analysis

**Status: Planned.**

Investigate how calculated radiation dose varies with downwind distance for a clearly defined hypothetical scenario.

### Project 05 — Comparison of Dispersion Modeling Approaches

**Status: Planned.**

Compare appropriate outputs from HotSpot with simplified analytical calculations or other atmospheric dispersion tools when their assumptions and output quantities are sufficiently compatible.

### Project 06 — Model Assumptions and Limitations Study

**Status: Planned.**

Evaluate the applicability and limitations of simplified atmospheric consequence models under representative terrestrial conditions.

## Project Documentation Standards

Each completed project will include:

- Engineering objective and scenario description
- Radionuclide and source-term assumptions
- Release configuration and duration
- Meteorological conditions
- Atmospheric dispersion settings
- Exposure pathway and dose assumptions
- Original analysis scripts and supporting calculations
- Numerical results and scientific figures
- Sensitivity and uncertainty discussions
- Verification against analytical or published references where applicable
- Model limitations and interpretation
- LaTeX technical reports and compiled PDFs
- Reproducibility instructions and scientific references

## Modeling Limitations

HotSpot provides simplified screening-level radiological consequence estimates.

Its calculations depend on assumptions concerning atmospheric dispersion, source terms, meteorological conditions, exposure pathways, and dose conversion methods.

HotSpot results should not automatically be interpreted as validated site-specific consequences or regulatory safety determinations.

Terrestrial atmospheric dispersion assumptions are not directly applicable to the lunar vacuum or Martian atmospheric conditions.

## Verification and Validation

Computational results will be evaluated using appropriate analytical comparisons, publicly available references, and sensitivity analyses where feasible.

Successful software execution does not independently establish physical validation.

## Reproducibility

Each project will document the HotSpot version, modeling assumptions, input parameters, applicable dose calculation settings, and supporting analysis methods.

Only independently created input data, appropriately shareable results, and original supporting scripts will be published.

## Publication Policy

No employer-owned, proprietary, export-controlled, restricted-licensed, or non-public information will be included.

The HotSpot software itself will not be redistributed through this repository without appropriate authorization.

## Status

**Software installation not yet verified. Computational exercises planned.**

This directory is an organizational starting point. Independent numerical studies will be added following software installation, verification, and documentation.
