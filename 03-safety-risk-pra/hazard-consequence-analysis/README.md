# Hazard & Consequence Analysis — Engineering Safety Assessment

## Overview

This directory documents independent research and computational engineering projects involving hazard identification, accident analysis, source-term characterization, consequence modeling, and safety assessment.

The objective is to investigate how engineering hazards can be identified, characterized, analyzed, and evaluated using systematic methodologies, physics-based models, and defensible assumptions.

Projects will include educational and independently developed examples relevant to nuclear engineering, industrial systems, and conceptual space nuclear power applications.

## Research Interests

- Hazard identification and characterization
- Preliminary hazard analysis (PHA)
- Hazard and operability studies (HAZOP)
- Failure Modes and Effects Analysis (FMEA)
- Failure Modes, Effects and Criticality Analysis (FMECA)
- Accident scenario identification
- Nuclear accident consequence analysis
- Material-at-risk (MAR) characterization
- Airborne release fraction (ARF)
- Respirable fraction (RF)
- Damage ratio and leak-path factors
- Radioactive material transport and dispersion
- Radiation exposure pathways
- Radiation dose assessment
- Natural phenomena hazards
- Hazard screening and prioritization
- Safety margins and uncertainty analysis
- Terrestrial and extraterrestrial engineering hazards

## Computational Methods and Tools

Projects may use:

- **Python:** Engineering calculations, parameter studies, and data analysis
- **NumPy and SciPy:** Numerical computation
- **pandas:** Tabular engineering data
- **Matplotlib:** Scientific visualization
- **OpenMC:** Selected radiation transport and nuclear analysis applications
- **Geant4:** Particle transport and detector-related studies
- **HYSPLIT:** Terrestrial atmospheric dispersion analysis
- **HotSpot:** Screening-level terrestrial radiological consequence analysis
- **RAVEN and SALib:** Uncertainty and sensitivity analysis
- **SCRAM:** Reliability and probabilistic accident sequence modeling
- **QGIS and GeoPandas:** Geospatial analysis

Applicable regulatory guidance, technical standards, and scientific references will be identified in individual reports.

## Planned Computational Exercises

### Project 01 — Preliminary Hazard Analysis

**Status: Planned.**

Develop a preliminary hazard analysis for a hypothetical engineering system.

Identify hazards, initiating conditions, potential consequences, preventive controls, and proposed mitigation strategies.

### Project 02 — Failure Modes and Effects Analysis

**Status: Planned.**

Conduct an educational FMEA of a simplified engineering subsystem.

Document component functions, failure modes, effects, detection methods, and qualitative or quantitative prioritization criteria.

### Project 03 — Hypothetical Radiological Source-Term Calculation

**Status: Planned.**

Develop an illustrative radionuclide release calculation using a clearly defined material inventory and appropriately justified release assumptions.

Distinguish physical inventory, material-at-risk, released material, and airborne source terms.

### Project 04 — Terrestrial Atmospheric Consequence Assessment

**Status: Planned.**

Investigate a hypothetical atmospheric release and examine the influence of selected meteorological and source-term parameters on modeled transport and consequence estimates.

### Project 05 — Radiation Exposure Pathway Analysis

**Status: Planned.**

Develop an educational study examining relevant radiation exposure pathways and the assumptions required to estimate dose.

### Project 06 — Natural Phenomena Hazard Screening

**Status: Planned.**

Develop a systematic hazard screening matrix for a hypothetical engineering installation.

Consider applicable natural phenomena, exposure conditions, safety functions, and evidence needs.

### Project 07 — Lunar Surface Hazard Identification

**Status: Planned.**

Develop an independently authored preliminary hazard assessment for a hypothetical lunar surface power installation.

Potential environmental considerations include vacuum, reduced gravity, regolith dust, micrometeoroids, thermal extremes, surface charging, and radiation exposure.

### Project 08 — Martian Surface Hazard Identification

**Status: Planned.**

Investigate hazards associated with a conceptual Martian surface engineering system, including low atmospheric pressure, dust transport, thermal conditions, and environmental uncertainties.

### Project 09 — Hazard-to-Evidence Traceability

**Status: Planned.**

Develop a traceability framework connecting hazard identification, safety claims, computational evidence, assumptions, verification activities, and unresolved technical uncertainties.

## Project Documentation Standards

Each completed project will include:

- Engineering objective and scope
- System description and boundaries
- Hazard definitions and initiating conditions
- Applicable scientific and technical references
- Modeling assumptions and input data
- Governing equations and computational methods
- Original source code and model files
- Results, figures, and tables
- Sensitivity and uncertainty discussion
- Verification and validation considerations
- Safety significance and limitations
- LaTeX technical reports and compiled PDFs
- Reproducibility instructions

## Source-Term and Consequence Modeling Considerations

Where relevant, radiological source-term analyses will distinguish material inventories, physical release mechanisms, airborne transport, and subsequent exposure pathways.

Release assumptions will be justified for the modeled environment rather than transferred between terrestrial and extraterrestrial conditions without supporting evidence.

Terrestrial atmospheric dispersion models are not directly applicable to a lunar vacuum or necessarily suitable for the low-pressure Martian atmosphere.

Computed source terms, environmental concentrations, and radiation dose will be treated as distinct quantities requiring appropriate physical models and units.

## Verification, Validation and Uncertainty

Computational results will be assessed using analytical checks, independent calculations, publicly available reference problems, or experimental evidence where applicable.

Uncertainty sources and model limitations will be documented.

A successful computational run does not independently establish physical validation or regulatory acceptability.

## Reproducibility

Each project will document software versions, input parameters, calculation procedures, dependencies, and relevant assumptions.

Publicly redistributable input data and independently developed models will be included where appropriate.

## Publication Policy

Only independently authored research, original computational models, and publicly distributable information will be published.

Employer-owned, proprietary, export-controlled, restricted-licensed, confidential, or otherwise non-public materials will be excluded.

Examples involving nuclear systems will use publicly available information or clearly identified hypothetical assumptions.

## Status

**Research area established. Computational projects planned.**

Completed models, hazard assessment tables, visualizations, and technical reports will be added as the research develops.
