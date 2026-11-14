"""
Minimal multigroup Monte Carlo k-eigenvalue solver for concentric spheres.

Purpose: an independent *transport* reference for the idealized LA-13511 problems,
so that the diffusion approximation can be judged against something better than
itself. It is verified against the exact LA-13511 critical dimensions
(see run_analysis.py, "verification"). It is NOT a reactor-design code: isotropic
scattering, homogeneous spherical shells, multigroup constants, analog physics.

Physics per history (analog):
  free flight ~ Exp(Sigma_t) -> boundary crossing or collision;
  collision: scatter (group transfer from the scattering matrix, isotropic direction)
             or absorption (fission with probability Sigma_f/Sigma_a, which banks
             int(nu + xi) fission sites with groups sampled from chi);
  leaving the outermost sphere = leakage.
Power iteration: the fission bank of generation n is resampled to N sites and
becomes the source of generation n+1. k is estimated per generation with the
collision estimator  k = (1/N) * sum over collisions of nu*Sigma_f / Sigma_t.

Life-cycle tallies (active generations, per source neutron):
  leakage by group, capture and fission by region and group, collisions,
  fissions caused by neutrons that had entered a reflector region,
  radial collision-estimated scalar flux by group, radial fission density.
"""
from __future__ import annotations

import math

import numpy as np
from numba import njit


@njit(cache=True)
def _seed(s):
    np.random.seed(s)


@njit(cache=True)
def _iso_dir():
    mu = 2.0 * np.random.random() - 1.0
    phi = 2.0 * math.pi * np.random.random()
    st = math.sqrt(max(0.0, 1.0 - mu * mu))
    return st * math.cos(phi), st * math.sin(phi), mu


@njit(cache=True)
def _dist_to_shell(x, y, z, u, v, w, r_in, r_out):
    """Distance along (u,v,w) to the inner (if hit) or outer sphere; flag +1 outward, -1 inward."""
    b = x * u + y * v + z * w
    r2 = x * x + y * y + z * z
    d_out = -b + math.sqrt(max(0.0, b * b - (r2 - r_out * r_out)))
    if r_in > 0.0 and b < 0.0:
        disc = b * b - (r2 - r_in * r_in)
        if disc > 0.0:
            d_in = -b - math.sqrt(disc)
            if d_in < d_out:
                return d_in, -1
    return d_out, 1


@njit(cache=True)
def _generation(src, src_g, radii, mat_id, sig_t, sig_a, sig_f, nusig_f, sig_s_cum, chi_cum,
                is_refl, nbins, rbin_max, bank, bank_g, tally_on,
                t_leak, t_cap, t_fis, t_fis_refl, t_flux, t_fdens, t_coll):
    N = src.shape[0]
    nreg = radii.shape[0]
    G = sig_t.shape[1]
    nb = 0
    kcol = 0.0
    cap_bank = bank.shape[0]
    for i in range(N):
        x, y, z = src[i, 0], src[i, 1], src[i, 2]
        g = src_g[i]
        u, v, w = _iso_dir()
        r = math.sqrt(x * x + y * y + z * z)
        reg = 0
        while reg < nreg - 1 and r > radii[reg]:
            reg += 1
        visited = False
        while True:
            m = mat_id[reg]
            r_in = radii[reg - 1] if reg > 0 else 0.0
            r_out = radii[reg]
            if m < 0:                              # void region: stream to boundary
                d_b, flag = _dist_to_shell(x, y, z, u, v, w, r_in, r_out)
                x += (d_b + 1e-10) * u; y += (d_b + 1e-10) * v; z += (d_b + 1e-10) * w
                reg += flag
                if reg >= nreg:
                    if tally_on:
                        t_leak[g] += 1.0
                    break
                if is_refl[reg]:
                    visited = True
                continue
            st = sig_t[m, g]
            d = -math.log(1.0 - np.random.random()) / st
            d_b, flag = _dist_to_shell(x, y, z, u, v, w, r_in, r_out)
            if d < d_b:
                x += d * u; y += d * v; z += d * w
                r = math.sqrt(x * x + y * y + z * z)
                kcol += nusig_f[m, g] / st
                if tally_on:
                    t_coll[0] += 1.0
                    ib = int(r / rbin_max * nbins)
                    if ib < nbins:
                        t_flux[g, ib] += 1.0 / st
                xi = np.random.random() * st
                if xi < st - sig_a[m, g]:          # scattering: pick outgoing group
                    xs = xi / (st - sig_a[m, g])
                    gp = 0
                    while gp < G - 1 and xs > sig_s_cum[m, g, gp]:
                        gp += 1
                    g = gp
                    u, v, w = _iso_dir()
                    continue
                # absorption
                if np.random.random() * sig_a[m, g] < sig_f[m, g]:
                    if tally_on:
                        t_fis[reg, g] += 1.0
                        if visited:
                            t_fis_refl[0] += 1.0
                        ib = int(r / rbin_max * nbins)
                        if ib < nbins:
                            t_fdens[ib] += 1.0
                    nu = nusig_f[m, g] / sig_f[m, g]
                    n_new = int(nu + np.random.random())
                    for _ in range(n_new):
                        if nb < cap_bank:
                            bank[nb, 0] = x; bank[nb, 1] = y; bank[nb, 2] = z
                            xc = np.random.random()
                            gc = 0
                            while gc < G - 1 and xc > chi_cum[m, gc]:
                                gc += 1
                            bank_g[nb] = gc
                            nb += 1
                else:
                    if tally_on:
                        t_cap[reg, g] += 1.0
                break
            else:
                x += (d_b + 1e-10) * u; y += (d_b + 1e-10) * v; z += (d_b + 1e-10) * w
                reg += flag
                if reg >= nreg:
                    if tally_on:
                        t_leak[g] += 1.0
                    break
                if is_refl[reg]:
                    visited = True
    return nb, kcol / N


def solve(regions, n_particles=20000, n_inactive=50, n_active=200, seed=12345, nbins=60,
          keep_history=False):
    """
    regions: list of (outer_radius_cm, material_dict_or_None, is_reflector_bool), inner to outer.
    The first region is the (fissile) core used for the initial source.
    Returns a dict with k (mean, std error), life-cycle tallies and radial shapes.
    """
    mats = [m for (_, m, _) in regions if m is not None]
    G = mats[0]["sig_t"].size
    uniq = []
    mat_id = []
    for (_, m, _) in regions:
        if m is None:
            mat_id.append(-1)
            continue
        for j, u in enumerate(uniq):
            if u is m:
                mat_id.append(j)
                break
        else:
            uniq.append(m)
            mat_id.append(len(uniq) - 1)
    M = len(uniq)
    sig_t = np.array([m["sig_t"] for m in uniq])
    sig_a = np.array([m["sig_a"] for m in uniq])
    sig_f = np.array([m["sig_f"] for m in uniq])
    nusig_f = np.array([m["nusig_f"] for m in uniq])
    sig_s_cum = np.zeros((M, G, G))
    chi_cum = np.zeros((M, G))
    for j, m in enumerate(uniq):
        for g in range(G):
            row = m["sig_s"][g]
            tot = row.sum()
            sig_s_cum[j, g] = np.cumsum(row) / tot if tot > 0 else np.ones(G)
        chi_cum[j] = np.cumsum(m["chi"])
    radii = np.array([r for (r, _, _) in regions], float)
    mat_id = np.array(mat_id, np.int64)
    is_refl = np.array([bool(f) for (_, _, f) in regions])
    R0, R_out = radii[0], radii[-1]

    _seed(seed)
    rng = np.random.default_rng(seed)
    # initial source: uniform in the core, groups from chi
    pts = rng.normal(size=(n_particles, 3))
    pts /= np.linalg.norm(pts, axis=1)[:, None]
    pts *= (R0 * rng.random(n_particles) ** (1 / 3))[:, None]
    src_g = rng.choice(G, size=n_particles, p=uniq[mat_id[0]]["chi"]).astype(np.int64)

    nreg = len(regions)
    t_leak = np.zeros(G); t_cap = np.zeros((nreg, G)); t_fis = np.zeros((nreg, G))
    t_fis_refl = np.zeros(1); t_flux = np.zeros((G, nbins)); t_fdens = np.zeros(nbins); t_coll = np.zeros(1)
    bank = np.zeros((4 * n_particles, 3)); bank_g = np.zeros(4 * n_particles, np.int64)
    ks = []
    for gen in range(n_inactive + n_active):
        on = gen >= n_inactive
        nb, kc = _generation(pts, src_g, radii, mat_id, sig_t, sig_a, sig_f, nusig_f, sig_s_cum, chi_cum,
                             is_refl, nbins, R_out, bank, bank_g, on,
                             t_leak, t_cap, t_fis, t_fis_refl, t_flux, t_fdens, t_coll)
        ks.append(kc)
        idx = rng.integers(0, nb, size=n_particles)
        pts = bank[idx].copy()
        src_g = bank_g[idx].copy()
    ks = np.array(ks)
    ka = ks[n_inactive:]
    n_hist = n_particles * n_active
    edges = np.linspace(0, R_out, nbins + 1)
    vol = 4 / 3 * np.pi * (edges[1:] ** 3 - edges[:-1] ** 3)
    out = {
        "k": float(ka.mean()), "k_std": float(ka.std(ddof=1) / np.sqrt(len(ka))),
        "n_histories_active": int(n_hist),
        "leak_frac": float(t_leak.sum() / n_hist), "leak_by_group": (t_leak / n_hist).tolist(),
        "capture_by_region": (t_cap.sum(axis=1) / n_hist).tolist(),
        "fission_by_region": (t_fis.sum(axis=1) / n_hist).tolist(),
        "fission_by_group": (t_fis.sum(axis=0) / n_hist).tolist(),
        "frac_fissions_after_reflector": float(t_fis_refl[0] / max(t_fis.sum(), 1)),
        "collisions_per_history": float(t_coll[0] / n_hist),
        "r_edges": edges.tolist(),
        "flux": (t_flux / vol / n_hist).tolist(),
        "fission_density": (t_fdens / vol / n_hist).tolist(),
    }
    if keep_history:
        out["k_history"] = ks.tolist()
        out["n_inactive"] = n_inactive
    return out
