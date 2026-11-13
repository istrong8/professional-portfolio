# SCRAM — Probabilistic Risk Assessment and Reliability Modeling

## Overview

This directory documents planned independent computational engineering projects using **SCRAM**, an open-source probabilistic risk assessment and reliability analysis tool.

SCRAM provides capabilities for constructing and evaluating fault trees, event trees, and probabilistic models of system failures.

Projects in this directory will focus on probabilistic risk assessment (PRA), reliability engineering, accident sequence analysis, and risk-informed decision-making.

## Research Interests

- Probabilistic risk assessment (PRA)
- Fault tree analysis (FTA)
- Event tree analysis (ETA)
- System reliability and availability
- Minimal cut set analysis
- Common-cause failure modeling
- Failure probability estimation
- Basic-event importance measures
- Accident sequence quantification
- Sensitivity and uncertainty analysis
- Applications to nuclear and space engineering systems

## Software

- **Primary software:** SCRAM
- **Supporting tools:** Python, NumPy, SciPy, pandas, Matplotlib
- **Related frameworks:** RAVEN and other reliability analysis tools
- **Modeling methods:** Fault trees, event trees, and Boolean reliability models

## Planned Computational Exercises

### Project 01 — Basic Fault Tree Analysis

**Status: Planned.**

Develop a simplified engineering fault tree using AND and OR logic gates.

Calculate the top-event probability and compare results against independently derived analytical expressions.

### Project 02 — Minimal Cut Set Analysis

**Status: Planned.**

Construct a representative system fault tree and identify minimal combinations of basic events capable of producing the top event.

### Project 03 — Event Tree Analysis

**Status: Planned.**

Develop an event tree representing a hypothetical initiating event and alternative system response sequences.

Calculate illustrative accident sequence probabilities using clearly documented assumptions.

### Project 04 — Component Reliability Importance

**Status: Planned.**

Investigate the contribution of selected component failures to an illustrative system risk model using suitable importance measures.

### Project 05 — Common-Cause Failure Investigation

**Status: Planned.**

Explore how common-cause failures can influence the reliability of a redundant engineering system.

### Project 06 — Space System Reliability Study

**Status: Planned.**

Develop an educational PRA model for a hypothetical space system, using independently defined and clearly identified illustrative failure probabilities.

## Project Documentation Standards

Each completed project will include:

- Engineering problem and system boundaries
- Model objectives and assumptions
- Fault-tree or event-tree diagrams
- Basic-event definitions and probabilities
- Data sources and uncertainty assumptions
- SCRAM model inputs and settings
- Quantitative probability calculations
- Minimal cut sets and importance measures, where applicable
- Analytical checks and sensitivity studies
- Model limitations
- LaTeX technical reports and compiled PDFs
- Reproducibility instructions and references

## Verification and Validation

Model outputs will be checked against analytical calculations, independently developed examples, or appropriate published benchmarks where available.

Illustrative failure rates and probabilities will not be represented as measured reliability data.

## Reproducibility

Each project will document the SCRAM version, modeling assumptions, system structure, probability inputs, and analysis settings.

Only original and publicly distributable model files and data will be included.

## Publication Policy

No employer-owned, proprietary, export-controlled, restricted-licensed, or non-public information will be published.

All risk models will be independently developed for educational or research demonstration purposes unless otherwise indicated.

## Status

**Software installation not yet verified. Computational exercises planned.**

This directory is an organizational starting point. Documented analysis results will be added after software installation and verification.
