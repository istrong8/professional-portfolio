# Fault Tree Analysis — Probabilistic Risk and System Reliability

## Overview

This directory documents independent engineering projects involving **Fault Tree Analysis (FTA)**, a systematic method for identifying and evaluating combinations of failures that can lead to an undesirable system event.

Fault trees use Boolean logic to represent relationships between component failures, human actions, common-cause events, and system-level failure conditions.

Projects in this directory will focus on reliability modeling, failure logic, system risk quantification, and applications to nuclear engineering, industrial safety, and space systems.

## Research Interests

- Fault Tree Analysis (FTA)
- Boolean failure logic
- AND and OR gate structures
- System reliability and availability
- Minimal cut sets
- Basic-event probability modeling
- Common-cause failure
- Component redundancy and diversity
- Risk importance measures
- Uncertainty and sensitivity analysis
- Risk-informed engineering decisions
- Nuclear and space system reliability

## Computational Methods and Tools

Projects may use:

- **SCRAM:** Fault-tree modeling and quantification
- **Python:** Independent analytical calculations
- **NumPy and SciPy:** Numerical and probabilistic analysis
- **NetworkX:** Graph-based system representations
- **Matplotlib:** Risk diagrams and visualizations
- **SALib:** Sensitivity analysis
- **RAVEN:** Uncertainty quantification

Each project will identify the software actually used.

## Planned Computational Exercises

### Project 01 — Basic AND/OR Gate Probability Analysis

**Status: Planned.**

Develop a simple fault tree using AND and OR gates.

Calculate top-event probability and compare software results with independently derived analytical expressions.

### Project 02 — Redundant System Reliability

**Status: Planned.**

Investigate a hypothetical redundant engineering system and quantify how component redundancy affects system failure probability.

### Project 03 — Minimal Cut Set Analysis

**Status: Planned.**

Construct a representative fault tree and identify minimal combinations of basic events that can cause the top event.

### Project 04 — Component Importance Analysis

**Status: Planned.**

Evaluate the influence of selected basic events using applicable reliability importance measures.

### Project 05 — Common-Cause Failure Modeling

**Status: Planned.**

Explore the impact of illustrative common-cause failure assumptions on a redundant system.

### Project 06 — Nuclear Safety Function Reliability

**Status: Planned.**

Develop an educational fault-tree model representing a simplified, hypothetical nuclear safety function.

### Project 07 — Space System Reliability Model

**Status: Planned.**

Investigate the reliability of a conceptual spacecraft or lunar surface engineering subsystem using independently defined assumptions.

## Project Documentation Standards

Each completed project will include:

- System description and analysis objective
- System boundaries and assumptions
- Top-event definition
- Basic-event descriptions
- Fault-tree structure and logic diagrams
- Probability inputs and data provenance
- Mathematical formulation
- Model files and original source code
- Quantitative results and minimal cut sets
- Importance measures, where applicable
- Verification and sensitivity analysis
- Uncertainty and limitations
- LaTeX technical reports and compiled PDFs
- Reproducibility instructions and references

## Technical Considerations

Probability calculations will distinguish independent events, dependent events, and common-cause failure assumptions.

Simple products of basic-event probabilities are not generally valid when events are dependent.

Results using illustrative failure probabilities will be identified as educational examples and not as measured reliability estimates.

## Verification and Validation

Results will be checked using analytical expressions, independent numerical calculations, or published reference examples where applicable.

Model assumptions and limitations will be documented explicitly.

## Reproducibility

Each project will specify software versions, basic-event probabilities, assumptions about dependence, and model configuration.

Only independently developed or appropriately authorized models and data will be published.

## Publication Policy

Employer-owned, proprietary, export-controlled, restricted-licensed, and non-public information will not be included.

All publicly shared models will be independently developed or approved for release.

## Status

**Research area established. Computational exercises planned.**

Completed fault-tree models and analysis results will be added as the projects are developed and verified.
