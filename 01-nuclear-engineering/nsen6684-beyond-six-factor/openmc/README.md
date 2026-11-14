# OpenMC: the higher-fidelity next step

**Status: these inputs have not been run yet. No OpenMC results appear anywhere in this repository.**

## Why OpenMC

The study in `code/` uses idealized one- and two-group benchmark constants. It shows how large the diffusion error is in compact, leakage-dominated systems. It cannot represent the things that matter in a real space reactor:

- the continuous energy spectrum;
- resonances and Doppler broadening;
- anisotropic scattering;
- heterogeneous geometry (an annular core, heat pipes, a B₄C rod, a moving BeO reflector).

Continuous-energy Monte Carlo transport with evaluated nuclear data (OpenMC; Romano et al., *Ann. Nucl. Energy* 82, 2015) represents all of these directly. Its results only become evidence after validation against integral experiments, such as the KRUSTY component-critical benchmark (Stolte et al., *Nucl. Technol.* 208, 2022).

## Planned sequence

| Step | File | Needs nuclear data? | Purpose |
|---|---|---|---|
| 1 | `mg_benchmarks.py` | No (writes its own `mgxs_*.h5`) | Re-run the five LA-13511 problems in OpenMC multigroup mode as an independent cross-check of `code/mc_transport.py`. Expected: k = 1 within statistics. |
| 2 | Continuous-energy bare HEU sphere (Godiva, ICSBEP HEU-MET-FAST-001) | Yes (ENDF/B-VIII.0 HDF5) | First continuous-energy check against a measured critical. Take the benchmark-model composition from the ICSBEP Handbook. It is deliberately not typed in here, to avoid unverified numbers. |
| 3 | KRUSTY component-critical model | Yes | Build from the geometry and material specifications in Stolte et al. (2022) and compare with the published benchmark k_eff. Then compute reflector worth versus platen height and the expansion coefficients from Section 11 of the report. |

## Running step 1 (WSL / Linux)

```bash
conda activate openmc          # or your OpenMC environment
cd openmc
python mg_benchmarks.py
```
