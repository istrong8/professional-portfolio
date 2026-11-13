# MOOSE — Multiphysics and Finite Element Simulation

## Overview

This directory documents planned independent computational engineering projects using the **Multiphysics Object-Oriented Simulation Environment (MOOSE)**, an open-source finite-element simulation framework developed at Idaho National Laboratory.

MOOSE provides an extensible computational framework for solving systems of coupled partial differential equations and performing multiphysics simulations.

Projects in this directory will focus on heat transfer, finite-element methods, coupled physics, numerical solution methods, and applications to nuclear and space systems engineering.

## Research Interests

- Finite element analysis (FEA)
- Steady-state and transient heat transfer
- Coupled multiphysics simulation
- Nuclear reactor thermal analysis
- Temperature-dependent material properties
- Structural and thermal effects
- Mesh generation and mesh convergence
- Numerical solution methods
- Verification, validation, and uncertainty quantification
- Applications to space fission power systems

## Software

- **Primary framework:** MOOSE
- **Programming and configuration:** C++, Python, MOOSE input files
- **Supporting tools:** ParaView, Gmsh, NumPy, Matplotlib
- **Numerical approach:** Finite-element solution of coupled partial differential equations

## Planned Computational Exercises

### Project 01 — Two-Dimensional Steady-State Heat Conduction

**Status: Planned.**

Develop a simplified finite-element heat conduction model and evaluate temperature distributions under specified material properties and boundary conditions.

Compare numerical results against analytical solutions where applicable.

### Project 02 — Transient Thermal Analysis

**Status: Planned.**

Simulate the time-dependent temperature response of a solid material subjected to changing thermal boundary conditions.

Investigate time-step sensitivity and numerical convergence.

### Project 03 — Reactor Fuel Temperature Model

**Status: Planned.**

Develop an educational thermal model representing a simplified nuclear fuel geometry with prescribed volumetric heat generation.

Evaluate temperature gradients, material properties, and boundary-condition sensitivity.

### Project 04 — Thermal-Structural Coupling

**Status: Planned.**

Investigate the interaction between temperature distributions and thermal expansion or stress in a simplified engineering component.

### Project 05 — Conceptual Space Reactor Thermal Study

**Status: Planned.**

Develop an introductory thermal modeling study relevant to a hypothetical space fission system, including representative operating assumptions and applicable environmental constraints.

## Project Documentation Standards

Each completed project will include:

- Engineering objective and physical assumptions
- Governing equations and boundary conditions
- Material properties and source terms
- Finite-element formulation and mesh description
- MOOSE input files and original supporting code
- Numerical solver settings
- Mesh refinement and convergence studies
- Time-step sensitivity where applicable
- Temperature and field visualizations
- Verification and applicable validation comparisons
- Uncertainty, limitations, and interpretation
- LaTeX technical reports and compiled PDFs
- Software versions and reproducibility instructions

## Verification and Validation

Projects will distinguish code execution, numerical verification, solution convergence, and physical validation.

Analytical solutions and published benchmark problems will be used when appropriate and available.

## Reproducibility

Each project will document the MOOSE framework version, relevant dependencies, mesh specifications, solver settings, material properties, and boundary conditions.

Large binary simulation outputs will be excluded from the public repository.

## Publication Policy

Only independently developed models, original documentation, and publicly distributable information will be published.

Employer-owned, proprietary, export-controlled, restricted, licensed, and non-public research material will not be included without authorization.

## Status

**MOOSE source code previously cloned. Installation and executable verification incomplete. Computational exercises planned.**

The MOOSE framework must be successfully built and tested before simulation results are added or claimed as completed.
