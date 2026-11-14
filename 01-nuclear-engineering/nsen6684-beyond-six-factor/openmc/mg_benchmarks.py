#!/usr/bin/env python3
"""
OpenMC multigroup reproduction of the LA-13511 benchmarks used in this study.

STATUS: provided as the next step of the analysis. NOT YET RUN by the author;
no OpenMC results are reported anywhere in this repository.

Why: the in-house Monte Carlo code (code/mc_transport.py) was verified against the
exact LA-13511 solutions. Running the same problems in OpenMC's multigroup mode is an
independent cross-check of that code before moving on to continuous-energy models.
No nuclear data library is needed: the cross sections are written to mgxs.h5 below.

Usage (Linux / WSL with OpenMC installed):
    python mg_benchmarks.py            # builds and runs all cases
    python mg_benchmarks.py Ua-1-0-SP  # one case
Expected: k_eff = 1.0000 within statistics for every case (exact LA-13511 solutions).

Reference: A. Sood, R. A. Forster, D. K. Parsons, LA-13511 (1999), Tables 12-15, 33-35.
"""
import sys
from pathlib import Path

import numpy as np
import openmc

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- cross sections
one = openmc.mgxs.EnergyGroups([0.0, 20.0e6])
two = openmc.mgxs.EnergyGroups([0.0, 1.0, 20.0e6])   # boundaries arbitrary; only the group structure matters


def one_group(name, nu, sf, sc, ss, st):
    x = openmc.XSdata(name, one)
    x.order = 0
    x.set_total([st])
    x.set_absorption([sf + sc])
    x.set_scatter_matrix(np.array([[[ss]]]))
    if sf > 0:
        x.set_fission([sf])
        x.set_nu_fission([nu * sf])
        x.set_chi([1.0])
    return x


xs = [
    one_group("U235a", 2.70, 0.065280, 0.013056, 0.248064, 0.32640),
    one_group("U235b", 2.797101, 0.065280, 0.013056, 0.248064, 0.32640),
    one_group("U235c", 2.707308, 0.065280, 0.013056, 0.248064, 0.32640),
    one_group("U235d", 2.679198, 0.065280, 0.013056, 0.248064, 0.32640),
    one_group("H2O", 0.0, 0.0, 0.032640, 0.293760, 0.32640),
]
# two-group U-235 (OpenMC group 0 = fast). chi_slow = 1 - 0.575 (see code/benchmarks.py)
u2 = openmc.XSdata("U235_2G", two)
u2.order = 0
u2.set_total([0.2160, 0.3456])
u2.set_absorption([0.06192 + 0.00384, 0.06912 + 0.01344])
u2.set_fission([0.06192, 0.06912])
u2.set_nu_fission([2.70 * 0.06192, 2.50 * 0.06912])
u2.set_chi([0.575, 0.425])
u2.set_scatter_matrix(np.array([[[0.078240], [0.0720]],      # [g_in, g_out, legendre]
                                [[0.0],      [0.26304]]]))
lib1 = openmc.MGXSLibrary(one); lib1.add_xsdatas(xs); lib1.export_to_hdf5(str(HERE / "mgxs_1g.h5"))
lib2 = openmc.MGXSLibrary(two); lib2.add_xsdatas([u2]); lib2.export_to_hdf5(str(HERE / "mgxs_2g.h5"))

# ---------------------------------------------------------------- cases
CASES = {   # name: (library, [(outer radius cm, macroscopic name)])
    "Ua-1-0-SP": ("mgxs_1g.h5", [(7.428998, "U235a")]),
    "Ub-H2O(1)-1-0-SP": ("mgxs_1g.h5", [(6.12745, "U235b"), (6.12745 + 3.063725, "H2O")]),
    "Uc-H2O(2)-1-0-SP": ("mgxs_1g.h5", [(6.12745, "U235c"), (6.12745 + 6.12745, "H2O")]),
    "Ud-H2O(3)-1-0-SP": ("mgxs_1g.h5", [(6.12745, "U235d"), (6.12745 + 9.191176, "H2O")]),
    "U-2-0-SP": ("mgxs_2g.h5", [(7.909444, "U235_2G")]),
}


def build_and_run(name, particles=100000, batches=300, inactive=50):
    lib, shells = CASES[name]
    work = HERE / name.replace("(", "_").replace(")", "")
    work.mkdir(exist_ok=True)
    mats, cells, prev = [], [], None
    for i, (r, macro) in enumerate(shells):
        m = openmc.Material(name=f"{macro}_{i}")
        m.set_density("macro", 1.0)
        m.add_macroscopic(macro)
        mats.append(m)
        last = i == len(shells) - 1
        surf = openmc.Sphere(r=r, boundary_type="vacuum" if last else "transmission")
        region = -surf if prev is None else (+prev & -surf)
        cells.append(openmc.Cell(fill=m, region=region))
        prev = surf
    materials = openmc.Materials(mats)
    materials.cross_sections = str(HERE / lib)
    geometry = openmc.Geometry(openmc.Universe(cells=cells))
    settings = openmc.Settings()
    settings.energy_mode = "multi-group"
    settings.particles, settings.batches, settings.inactive = particles, batches, inactive
    settings.source = openmc.IndependentSource(space=openmc.stats.Point())
    model = openmc.Model(geometry, materials, settings)
    sp = model.run(cwd=str(work))
    with openmc.StatePoint(sp) as s:
        k = s.keff
    print(f"{name:20s} k_eff = {k.nominal_value:.5f} +/- {k.std_dev:.5f}   (exact: 1)")
    return k


if __name__ == "__main__":
    names = sys.argv[1:] or list(CASES)
    for nm in names:
        build_and_run(nm)
