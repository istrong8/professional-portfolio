"""
Analytic diffusion-theory solutions for spheres (one and two groups).

Conventions: D = 1/(3 Sigma_tr) with Sigma_tr = Sigma_t (isotropic scattering, as in
LA-13511). Vacuum boundaries use the Milne extrapolation distance d = 0.7104 lambda_tr.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

EXTRAP = 0.7104


def one_group_constants(m):
    st = float(m["sig_t"][0]); sa = float(m["sig_a"][0]); nsf = float(m["nusig_f"][0])
    D = 1.0 / (3.0 * st)
    return {"D": D, "sig_a": sa, "nusig_f": nsf, "L2": D / sa, "kinf": nsf / sa,
            "lam_tr": 1.0 / st, "d": EXTRAP / st}


def bare_sphere_k(m, R):
    c = one_group_constants(m)
    B2 = (np.pi / (R + c["d"])) ** 2
    pnl = 1.0 / (1.0 + c["L2"] * B2)
    return c["kinf"] * pnl, B2, pnl


def bare_sphere_rc(m):
    c = one_group_constants(m)
    return np.pi / np.sqrt((c["kinf"] - 1.0) / c["L2"]) - c["d"]


def reflected_sphere_k(core, refl, R, T):
    """One-group two-region diffusion: core radius R, reflector thickness T (vacuum outside).

    Flux continuity and current continuity (D_c phi_c' = D_r phi_r') at r = R with
    phi_c = A sin(Br)/r and phi_r = C sinh(kappa (R + T + d_r - r))/r give
        D_c [B R cot(B R) - 1] + D_r [kappa R coth(kappa T_e) + 1] = 0,  T_e = T + d_r,
    solved for the material buckling B, then k = nu Sigma_f / (Sigma_a + D_c B^2).
    """
    if T <= 0:
        return bare_sphere_k(core, R)[0]
    c = one_group_constants(core)
    r = one_group_constants(refl)
    kap = np.sqrt(r["sig_a"] / r["D"])
    Te = T + r["d"]
    rhs = r["D"] * (kap * R / np.tanh(kap * Te) + 1.0)
    g = lambda B: c["D"] * (B * R / np.tan(B * R) - 1.0) + rhs
    B = brentq(g, 1e-9, np.pi / R - 1e-9)
    return c["nusig_f"] / (c["sig_a"] + c["D"] * B * B)


def reflected_sphere_rc(core, refl, T):
    rc_bare = bare_sphere_rc(core)
    return brentq(lambda R: reflected_sphere_k(core, refl, R, T) - 1.0, 0.2, 1.3 * rc_bare)


def slab_reflector_savings(core, refl, T):
    """Large-core (flat flux) one-group estimate delta = (D_c/D_r) L_r tanh(T/L_r)."""
    c = one_group_constants(core); r = one_group_constants(refl)
    Lr = np.sqrt(r["L2"])
    return c["D"] / r["D"] * Lr * np.tanh(T / Lr)


# ---------------------------------------------------------------- two groups
def multigroup_bare_sphere_k(m, R):
    """Multigroup diffusion, bare sphere, single geometric buckling for all groups.

    Each group has its own extrapolation distance in principle; here the buckling is
    set with the extrapolation distance of the group with the longest lambda_tr
    (documented approximation; the result is reported with that caveat).
    """
    D = 1.0 / (3.0 * m["sig_t"])
    d = EXTRAP / m["sig_t"]
    B2 = (np.pi / (R + d)) ** 2                     # group-dependent buckling
    Mx = np.diag(D * B2 + m["sig_t"]) - m["sig_s"].T
    F = np.outer(m["chi"], m["nusig_f"])
    w = np.linalg.eigvals(np.linalg.solve(Mx, F))
    return float(np.max(w.real))


def multigroup_bare_sphere_rc(m):
    return brentq(lambda R: multigroup_bare_sphere_k(m, R) - 1.0, 0.5, 100.0)


def collapse_to_one_group(m, spectrum):
    """Flux-weighted one-group collapse with a given group spectrum (normalized)."""
    w = np.asarray(spectrum, float) / np.sum(spectrum)
    st = float(w @ m["sig_t"]); sa = float(w @ m["sig_a"]); sf = float(w @ m["sig_f"])
    nsf = float(w @ m["nusig_f"])
    from benchmarks import material
    return material(nu=nsf / sf, sig_f=sf, sig_c=sa - sf, sig_s=[[st - sa]], sig_t=st)


def leakage_weighted_spectrum(m, R):
    """Fundamental-mode multigroup diffusion spectrum at the buckling of radius R."""
    D = 1.0 / (3.0 * m["sig_t"])
    d = EXTRAP / m["sig_t"]
    B2 = (np.pi / (R + d)) ** 2
    Mx = np.diag(D * B2 + m["sig_t"]) - m["sig_s"].T
    F = np.outer(m["chi"], m["nusig_f"])
    w, v = np.linalg.eig(np.linalg.solve(Mx, F))
    phi = np.abs(v[:, np.argmax(w.real)].real)
    return phi / phi.sum()
