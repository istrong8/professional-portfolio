# Event Tree Analysis — Accident Sequence and Risk Modeling

## Overview

This directory documents independent engineering projects involving **Event Tree Analysis (ETA)**, a systematic method for evaluating the possible outcomes of an initiating event.

Event trees represent sequences of system responses, including the success or failure of safety functions, to identify potential accident sequences and quantify their probabilities or frequencies.

Projects in this directory focus on accident progression, safety system performance, probabilistic risk assessment (PRA), and risk-informed engineering decisions.

## Research Interests

- Event Tree Analysis (ETA)
- Accident sequence development
- Initiating event identification
- Safety system success and failure
- Conditional probability modeling
- Accident sequence quantification
- Initiating event frequencies
- Success criteria and system dependencies
- Common-cause and dependent failures
- Fault tree and event tree integration
- Uncertainty and sensitivity analysis
- Nuclear and space system safety

## Computational Methods and Tools

Projects may use:

- **SCRAM:** Event-tree and fault-tree analysis
- **Python:** Independent probability calculations and sequence modeling
- **NumPy and SciPy:** Numerical and probabilistic analysis
- **NetworkX:** Graph-based sequence representation
- **Matplotlib:** Event-tree diagrams and visualizations
- **RAVEN:** Uncertainty quantification
- **SALib:** Parameter sensitivity analysis

Each project will identify the software and methods actually used.

## Planned Computational Exercises

### Project 01 — Basic Event Tree Construction

**Status: Planned.**

Develop a simplified event tree for a hypothetical initiating event involving two or more engineering safety functions.

Identify success and failure branches, calculate conditional sequence probabilities, and verify that mutually exclusive and collectively exhaustive sequence probabilities sum to one.

### Project 02 — Initiating Event Frequency Analysis

**Status: Planned.**

Calculate representative accident sequence frequencies using an assumed initiating event frequency and conditional system response probabilities.

### Project 03 — Safety Function Success and Failure

**Status: Planned.**

Investigate how success criteria and system response assumptions influence the sequence outcomes of a simplified engineering system.

### Project 04 — Integrated Fault Tree and Event Tree Analysis

**Status: Planned.**

Use a simplified fault tree to estimate a system failure probability and incorporate that result into a related event tree.

Document dependencies and avoid double counting shared basic events.

### Project 05 — Accident Sequence Importance Analysis

**Status: Planned.**

Identify dominant sequences in a hypothetical accident model and investigate how selected probability assumptions affect their relative contributions.

### Project 06 — Nuclear Safety Accident Sequence Study

**Status: Planned.**

Develop an educational accident sequence model for a hypothetical nuclear engineering system using independently defined safety functions and illustrative probabilities.

### Project 07 — Space System Accident Sequence Model

**Status: Planned.**

Investigate alternative outcomes following a hypothetical initiating event affecting a spacecraft or lunar surface engineering subsystem.

## Project Documentation Standards

Each completed project will include:

- Engineering problem and analysis objectives
- System description and analysis boundaries
- Initiating event definition and frequency assumptions
- Safety functions and success criteria
- Event-tree logic diagrams
- Sequence definitions and outcomes
- Conditional probability assumptions
- Model input data and provenance
- Original computational scripts and model files
- Quantitative sequence probabilities or frequencies
- Verification and consistency checks
- Uncertainty and sensitivity analysis
- Model limitations
- LaTeX technical reports and compiled PDFs
- Reproducibility instructions and references

## Technical Considerations

Event-tree branch probabilities will be treated as conditional probabilities when the modeled system response depends on preceding events or states.

The analysis will distinguish sequence probability from sequence frequency.

Sequence frequency calculations will include the initiating event frequency and relevant conditional branch probabilities.

Dependencies between systems, common-cause failures, and shared basic events will be documented explicitly.

Illustrative probabilities and frequencies will not be represented as measured reliability data.

## Verification and Validation

Event-tree results will be checked through independent numerical calculations, probability consistency checks, and appropriate reference examples where available.

The successful execution of an event-tree model does not independently establish physical validation.

## Reproducibility

Each project will document the software version, event-tree structure, initiating event assumptions, branch probabilities, dependencies, and computational settings.

Only independently developed or appropriately authorized modeling inputs and results will be published.

## Publication Policy

Employer-owned, proprietary, export-controlled, restricted-licensed, and non-public information will not be included.

All publicly shared models will be independently developed or approved for public release.

## Status

**Research area established. Computational exercises planned.**

Completed event-tree models, supporting calculations, visualizations, and technical reports will be added as the projects are developed and verified.
