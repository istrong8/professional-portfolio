# Reliability Engineering — System Reliability, Availability and Failure Analysis

## Overview

This directory documents independent computational engineering projects involving **reliability engineering**, system availability, component failure analysis, and risk-informed maintenance.

Reliability engineering applies probabilistic and statistical methods to evaluate the likelihood that engineering systems will perform required functions under specified operating conditions and time intervals.

Projects in this directory will focus on quantitative reliability modeling, failure distributions, system configurations, maintenance strategies, and applications to nuclear, industrial, and space systems engineering.

## Research Interests

- Component reliability and failure probability
- System reliability and availability
- Failure rate and hazard function modeling
- Mean time to failure (MTTF)
- Mean time between failures (MTBF)
- Mean time to repair (MTTR)
- Reliability block diagrams
- Series and parallel system configurations
- Weibull and exponential failure distributions
- Preventive and corrective maintenance
- Reliability-centered maintenance
- Failure Modes and Effects Analysis (FMEA)
- Failure Modes, Effects and Criticality Analysis (FMECA)
- Common-cause and dependent failures
- Reliability sensitivity and uncertainty
- Nuclear and space system applications

## Computational Methods and Tools

Projects may use:

- **Python:** Reliability modeling and statistical calculations
- **SciPy:** Failure distributions and numerical methods
- **NumPy and pandas:** Data analysis
- **Matplotlib:** Reliability and failure probability visualizations
- **reliability (Python package):** Reliability and lifetime analysis
- **lifelines:** Survival and lifetime modeling
- **SCRAM:** Fault-tree reliability analysis
- **RAVEN:** Uncertainty quantification and probabilistic modeling
- **SALib:** Sensitivity analysis

Each project will identify the software and methods actually used.

## Planned Computational Exercises

### Project 01 — Exponential Reliability Model

**Status: Planned.**

Develop a simplified component reliability model assuming a constant failure rate.

Calculate reliability as a function of mission time and compare numerical results with analytical expressions.

### Project 02 — Weibull Lifetime Analysis

**Status: Planned.**

Investigate the Weibull distribution and evaluate how shape and scale parameters influence reliability and failure behavior.

### Project 03 — Series and Parallel System Reliability

**Status: Planned.**

Model simplified engineering systems with series and parallel reliability structures.

Compare numerical results with analytical calculations under clearly stated independence assumptions.

### Project 04 — System Availability Analysis

**Status: Planned.**

Develop an introductory availability model using illustrative failure and repair parameters.

Investigate steady-state availability and its sensitivity to maintenance assumptions.

### Project 05 — Preventive Maintenance Optimization

**Status: Planned.**

Explore how simplified preventive maintenance intervals influence reliability, downtime, and maintenance-related performance measures.

### Project 06 — Reliability Block Diagram Study

**Status: Planned.**

Develop a representative reliability block diagram and calculate system reliability for selected configurations.

### Project 07 — Space Mission Reliability

**Status: Planned.**

Investigate the reliability of a hypothetical spacecraft or lunar surface subsystem over a defined mission duration.

### Project 08 — Reliability-Centered Maintenance Study

**Status: Planned.**

Develop an educational study connecting failure modes, component importance, maintenance strategies, and risk-informed decision-making.

## Project Documentation Standards

Each completed project will include:

- Engineering objective and system description
- System boundaries and operating assumptions
- Component or system failure models
- Probability distributions and parameters
- Reliability and availability equations
- Data sources and parameter provenance
- Original Python source code
- Numerical calculations and scientific figures
- Analytical comparisons and consistency checks
- Sensitivity and uncertainty analysis
- Interpretation and modeling limitations
- LaTeX technical reports and compiled PDFs
- Reproducibility instructions and references

## Technical Considerations

Reliability estimates depend on the selected failure distributions, operating conditions, mission duration, repair assumptions, and component dependencies.

The distinction between reliability, availability, and maintainability will be maintained throughout the analyses.

Illustrative failure parameters will not be presented as measured component reliability data.

## Verification and Validation

Computational results will be checked using appropriate analytical solutions, independent calculations, or publicly available benchmark examples.

Numerical agreement with an analytical reliability model does not independently establish that the selected model represents actual field failure behavior.

## Reproducibility

Each project will document the software versions, statistical assumptions, random seeds where applicable, failure model parameters, and computational methods.

Only original and publicly distributable models and data will be published.

## Publication Policy

Employer-owned, proprietary, export-controlled, restricted-licensed, and non-public information will not be included.

All published reliability models will be independently developed or explicitly approved for public release.

## Status

**Research area established. Computational exercises planned.**

Completed reliability analyses and technical reports will be added as the projects are developed and verified.
