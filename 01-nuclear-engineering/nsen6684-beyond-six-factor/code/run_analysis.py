#!/usr/bin/env python3
"""
NSEN 6684 -- Beyond the Six-Factor Formula: Neutron Leakage, Spectral Effects,
and Reactivity Feedback in Compact Space Fission Reactors.

Reproducible analysis (Irais Strong, Idaho State University).

Every cross section comes from the LA-13511 analytic benchmark set (see benchmarks.py).
These are IDEALIZED verification problems with exact transport solutions -- they are
not KRUSTY, not any space reactor, and nothing here is a design calculation. The
point is to measure, against known answers, how leakage, reflection and energy
dependence change k_eff, and how much the one-group diffusion approximation misses.

Studies
  0. classical  : six-factor ledger with assumed LWR-like factors (review slide only)
  1. verify     : Monte Carlo vs exact LA-13511 critical dimensions (1 and 2 groups)
  2. sensitivity: k_eff and leakage vs radius, bare sphere (diffusion vs transport)
  3. reflector  : critical radius vs reflector thickness; reflector savings
  4. spectral   : two-group leakage, spectral index, one-group collapse error
  5. feedback   : reactivity response to uniform thermal expansion (dln k / d eps)

Usage:  python run_analysis.py [--quick]
Writes results/analysis_results.json and results/analysis_output.txt.
Runtime: roughly 10-20 minutes on a laptop (--quick: ~2 minutes, larger error bars).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

import benchmarks as bm
import diffusion as df
import mc_transport as mc

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
RES.mkdir(exist_ok=True)
QUICK = "--quick" in sys.argv
NP, NI, NA = (10000, 30, 80) if QUICK else (40000, 50, 250)       # particles, inactive, active
NP_FB, NA_FB = (10000, 80) if QUICK else (80000, 400)              # feedback study needs tighter sigma

lines: list[str] = []
R: dict = {"settings": {"particles": NP, "inactive": NI, "active": NA, "quick": QUICK}}


def log(s=""):
    print(s, flush=True)
    lines.append(s)


def run(regions, seed, n=NP, na=NA, **kw):
    t0 = time.time()
    out = mc.solve(regions, n_particles=n, n_inactive=NI, n_active=na, seed=seed, **kw)
    out["seconds"] = round(time.time() - t0, 1)
    return out


def scaled(m, s):
    """Material with all macroscopic cross sections multiplied by s (density change)."""
    return bm.material(nu=m["nu"], sig_f=s * m["sig_f"], sig_c=s * m["sig_c"],
                       sig_s=s * m["sig_s"], sig_t=s * m["sig_t"], chi=m["chi"])


def mc_critical_radius(make_regions, R_guess, seed0, n_iter=4):
    """Secant search for k(R) = 1 with Monte Carlo; returns R_c, its 1-sigma, and the points."""
    pts = []
    Ra, Rb = R_guess, R_guess * 0.97
    ka = run(make_regions(Ra), seed0)["k"]
    rb = run(make_regions(Rb), seed0 + 1)
    kb = rb["k"]
    pts += [(Ra, ka), (Rb, kb)]
    for it in range(n_iter):
        Rn = Rb + (1.0 - kb) * (Rb - Ra) / (kb - ka)
        rn = run(make_regions(Rn), seed0 + 2 + it)
        Ra, ka, Rb, kb = Rb, kb, Rn, rn["k"]
        pts.append((Rn, kb))
        if abs(kb - 1.0) < 2 * rn["k_std"]:
            break
    # local linear fit through the points closest to k = 1
    P = np.array(sorted(pts, key=lambda p: abs(p[1] - 1))[:3])
    slope, icpt = np.polyfit(P[:, 0], P[:, 1], 1)
    Rc = (1.0 - icpt) / slope
    sig = rn["k_std"] / abs(slope)
    return float(Rc), float(sig), [(float(a), float(b)) for a, b in pts], float(slope)


T0 = time.time()
log("=" * 78)
log("NSEN 6684 analysis -- LA-13511 benchmark constants, Monte Carlo vs diffusion")
log(f"MC settings: {NP} particles/generation, {NI} inactive, {NA} active generations")
log("=" * 78)

# ------------------------------------------------------------------ 0. classical review
f = {"eta": 1.84, "epsilon": 1.03, "p": 0.78, "f": 0.90}
P_FNL, P_TNL = 0.80, 0.95
ledger = [1000.0]
for fac in (f["eta"], f["epsilon"], P_FNL, f["p"], P_TNL, f["f"]):
    ledger.append(ledger[-1] * fac)
R["classical"] = {"factors": f, "P_FNL": P_FNL, "P_TNL": P_TNL, "ledger": ledger,
                  "k_inf": f["eta"] * f["epsilon"] * f["p"] * f["f"], "k_eff": ledger[-1] / 1000}
log(f"\n[0] Classical six-factor ledger (assumed LWR-like factors, review only): k_eff = {ledger[-1]/1000:.4f}")

# ------------------------------------------------------------------ 1. verification
log("\n[1] VERIFICATION against exact LA-13511 transport solutions (k = 1 by construction)")
U = bm.U235
ver = {}
r = run([(bm.BARE_U235A_SPHERE_RC, U["a"], False)], seed=101, keep_history=True)
ver["Ua-1-0-SP"] = {"k_mc": r["k"], "k_std": r["k_std"], "k_diff": df.bare_sphere_k(U["a"], bm.BARE_U235A_SPHERE_RC)[0],
                    "leak_mc": r["leak_frac"], "k_history": r["k_history"], "flux": r["flux"][0],
                    "r_edges": r["r_edges"], "collisions": r["collisions_per_history"]}
log(f"  Ua-1-0-SP  bare sphere R = {bm.BARE_U235A_SPHERE_RC} cm: k_MC = {r['k']:.5f} +/- {r['k_std']:.5f}"
    f"   k_diffusion = {ver['Ua-1-0-SP']['k_diff']:.5f}")
for i, (pid, (uset, T)) in enumerate(bm.REFLECTED.items()):
    regs = [(bm.REFLECTED_CORE_R, U[uset], False), (bm.REFLECTED_CORE_R + T, bm.H2O_1G, True)]
    r = run(regs, seed=110 + i)
    kd = df.reflected_sphere_k(U[uset], bm.H2O_1G, bm.REFLECTED_CORE_R, T)
    ver[pid] = {"k_mc": r["k"], "k_std": r["k_std"], "k_diff": kd, "leak_mc": r["leak_frac"],
                "frac_fis_after_refl": r["frac_fissions_after_reflector"], "T_cm": T}
    log(f"  {pid:18s} core 6.12745 cm, H2O {T:8.5f} cm: k_MC = {r['k']:.5f} +/- {r['k_std']:.5f}"
        f"   k_diffusion = {kd:.5f}   fissions by reflector-returned neutrons = {100*r['frac_fissions_after_reflector']:.1f}%")
r = run([(bm.TWO_GROUP_SPHERE_RC, bm.U235_2G, False)], seed=120)
kd2 = df.multigroup_bare_sphere_k(bm.U235_2G, bm.TWO_GROUP_SPHERE_RC)
ver["U-2-0-SP"] = {"k_mc": r["k"], "k_std": r["k_std"], "k_diff": kd2, "leak_mc": r["leak_frac"]}
log(f"  U-2-0-SP   two-group bare R = {bm.TWO_GROUP_SPHERE_RC} cm: k_MC = {r['k']:.5f} +/- {r['k_std']:.5f}"
    f"   k_diffusion(2-group) = {kd2:.5f}")
# flux shape check (normalized at r/rc = 0.25)
edges = np.array(ver["Ua-1-0-SP"]["r_edges"]); ctr = 0.5 * (edges[1:] + edges[:-1])
phi = np.array(ver["Ua-1-0-SP"]["flux"])
rc = bm.BARE_U235A_SPHERE_RC
cmp_ = {}
c1 = df.one_group_constants(U["a"]); Re = rc + c1["d"]
phi_d = lambda x: np.sin(np.pi * x / Re) / x
def phi_at(x):
    """Interpolate the binned MC flux; at the outer surface extrapolate linearly from the last two bins."""
    if x <= ctr[-1]:
        return np.interp(x, ctr, phi)
    return phi[-1] + (phi[-1] - phi[-2]) / (ctr[-1] - ctr[-2]) * (x - ctr[-1])


for q, exact in bm.BARE_U235A_FLUX_RATIOS.items():
    mc_val = phi_at(q * rc) / phi_at(0.25 * rc)
    cmp_[q] = {"exact": exact / bm.BARE_U235A_FLUX_RATIOS[0.25], "mc": float(mc_val),
               "diffusion": float(phi_d(q * rc) / phi_d(0.25 * rc))}
ver["flux_shape_norm_at_0.25"] = cmp_
log("  Flux shape, normalized at r/rc = 0.25 (exact | MC | diffusion):")
for q, d in cmp_.items():
    log(f"     r/rc = {q:4.2f}: {d['exact']:.4f} | {d['mc']:.4f} | {d['diffusion']:.4f}")
R["verification"] = ver

# ------------------------------------------------------------------ 2. sensitivity vs size
log("\n[2] SENSITIVITY: k_eff and leakage vs radius, bare U-235(a) sphere")
lam = 1 / U["a"]["sig_t"][0]
sens = []
for i, Rr in enumerate([4.0, 5.0, 6.0, 7.0, bm.BARE_U235A_SPHERE_RC, 8.0, 9.0, 10.0, 12.0, 14.0]):
    r = run([(Rr, U["a"], False)], seed=200 + i)
    kd, B2, pnl = df.bare_sphere_k(U["a"], Rr)
    pnl_tr = r["k"] / bm.kinf(U["a"])[0]        # exact in one group: k = k_inf * P_NL
    row = {"R": Rr, "R_over_lam": Rr / lam, "k_mc": r["k"], "k_std": r["k_std"], "k_diff": kd,
           "leak_mc": r["leak_frac"], "pnl_tr": pnl_tr, "leak_diff": 1 - pnl, "B2": B2,
           "err_pct": 100 * (kd - r["k"]) / r["k"]}
    sens.append(row)
    log(f"  R = {Rr:7.4f} cm ({Rr/lam:4.2f} mfp): k_MC = {r['k']:.4f} +/- {r['k_std']:.4f}  k_diff = {kd:.4f}"
        f"  leakage MC = {100*r['leak_frac']:5.1f}%  diff = {100*(1-pnl):5.1f}%  diffusion error = {row['err_pct']:+5.2f}%")
R["sensitivity"] = {"rows": sens, "rc_exact": bm.BARE_U235A_SPHERE_RC, "rc_diff": df.bare_sphere_rc(U["a"]),
                    "lam_tr": lam, "kinf": bm.kinf(U["a"])[0]}
log(f"  Critical radius: exact transport {bm.BARE_U235A_SPHERE_RC} cm; diffusion {df.bare_sphere_rc(U['a']):.4f} cm "
    f"({100*(df.bare_sphere_rc(U['a'])/bm.BARE_U235A_SPHERE_RC-1):+.1f}%)")

# ------------------------------------------------------------------ 3. reflector savings
log("\n[3] REFLECTOR: critical core radius vs H2O(c=0.9) reflector thickness, fuel U-235(a)")
refl = []
rc0 = bm.BARE_U235A_SPHERE_RC
for i, T in enumerate([3.063725, 6.12745, 9.191176]):
    mk = lambda Rr, T=T: [(Rr, U["a"], False), (Rr + T, bm.H2O_1G, True)]
    rc_d = df.reflected_sphere_rc(U["a"], bm.H2O_1G, T)
    rc_m, sig, pts, slope = mc_critical_radius(mk, rc_d * 0.92, seed0=300 + 10 * i)
    slab = df.slab_reflector_savings(U["a"], bm.H2O_1G, T)
    row = {"T": T, "T_mfp": T * 0.32640, "rc_mc": rc_m, "rc_mc_sigma": sig, "rc_diff": rc_d,
           "savings_mc": rc0 - rc_m, "savings_diff": df.bare_sphere_rc(U["a"]) - rc_d, "savings_slab": slab,
           "mc_points": pts}
    refl.append(row)
    log(f"  T = {T:8.5f} cm ({T*0.3264:.0f} mfp): R_c MC = {rc_m:.4f} +/- {sig:.4f} cm   R_c diffusion = {rc_d:.4f} cm"
        f"   savings MC = {rc0-rc_m:.3f}  diffusion = {row['savings_diff']:.3f}  slab formula = {slab:.3f} cm")
R["reflector"] = {"rows": refl, "rc_bare_exact": rc0, "rc_bare_diff": df.bare_sphere_rc(U["a"]),
                  "L_r": float(np.sqrt(df.one_group_constants(bm.H2O_1G)["L2"]))}

# ------------------------------------------------------------------ 4. spectral effects
log("\n[4] SPECTRAL: two-group U-235 (LA-13511 Tables 33-35)")
m2 = bm.U235_2G
k2inf, spec_inf = bm.kinf(m2)
rc2 = bm.TWO_GROUP_SPHERE_RC
r = run([(rc2, m2, False)], seed=400)
spec = {"kinf": k2inf, "spec_inf": spec_inf.tolist(), "rc_exact": rc2,
        "k_mc_at_rc": r["k"], "k_std": r["k_std"], "leak_by_group": r["leak_by_group"],
        "fission_by_group": r["fission_by_group"], "flux_fast": r["flux"][0], "flux_slow": r["flux"][1],
        "r_edges": r["r_edges"], "rc_diff_2g": df.multigroup_bare_sphere_rc(m2),
        "k_diff_2g_at_rc": df.multigroup_bare_sphere_k(m2, rc2)}
lk = np.array(r["leak_by_group"])
log(f"  k_inf = {k2inf:.6f}; infinite-medium flux fractions fast/slow = {spec_inf[0]:.4f}/{spec_inf[1]:.4f}")
log(f"  MC at exact R_c: k = {r['k']:.5f} +/- {r['k_std']:.5f}; leakage fast {100*lk[0]:.1f}% + slow {100*lk[1]:.1f}% of source")
log(f"  share of leaked neutrons that are fast = {100*lk[0]/lk.sum():.1f}%  (fast share of infinite-medium flux = {100*spec_inf[0]:.1f}%)")
log(f"  two-group diffusion: R_c = {spec['rc_diff_2g']:.4f} cm; k at exact R_c = {spec['k_diff_2g_at_rc']:.5f}")
# one-group collapses
for label, w in (("infinite-medium spectrum", spec_inf),
                 ("leakage-weighted spectrum", df.leakage_weighted_spectrum(m2, rc2))):
    m1 = df.collapse_to_one_group(m2, w)
    rc_d1 = df.bare_sphere_rc(m1)
    rc_m1, sig1, pts1, _ = mc_critical_radius(lambda Rr, m1=m1: [(Rr, m1, False)], rc_d1 * 0.93,
                                               seed0=410 if "infinite" in label else 430)
    key = "collapse_inf" if "infinite" in label else "collapse_leak"
    spec[key] = {"weights": np.asarray(w).tolist(), "rc_mc": rc_m1, "rc_mc_sigma": sig1, "rc_diff": rc_d1,
                 "err_mc_pct": 100 * (rc_m1 / rc2 - 1), "kinf_1g": bm.kinf(m1)[0]}
    log(f"  one-group collapse with {label} (w_fast = {w[0]:.4f}): transport R_c = {rc_m1:.4f} +/- {sig1:.4f} cm "
        f"({spec[key]['err_mc_pct']:+.2f}% vs exact two-group); diffusion R_c = {rc_d1:.4f} cm")
R["spectral"] = spec

# ------------------------------------------------------------------ 5. expansion feedback
log("\n[5] FEEDBACK: reactivity response to uniform thermal expansion (strain eps)")
log("    density scales as (1+eps)^-3, dimensions as (1+eps)")
eps = 0.01
fb = {}


def expansion_runs(name, make, seed):
    ks = {}
    for j, e in enumerate((-eps, +eps)):
        r = run(make(e), seed=seed + j, n=NP_FB, na=NA_FB)
        ks[e] = (r["k"], r["k_std"])
    dlnk = (np.log(ks[eps][0]) - np.log(ks[-eps][0])) / (2 * eps)
    sig = np.sqrt((ks[eps][1] / ks[eps][0]) ** 2 + (ks[-eps][1] / ks[-eps][0]) ** 2) / (2 * eps)
    fb[name] = {"dlnk_deps": float(dlnk), "sigma": float(sig),
                "k_minus": ks[-eps][0], "k_plus": ks[eps][0], "k_std": ks[eps][1]}
    log(f"  {name:48s} dln k/d eps = {dlnk:+.3f} +/- {sig:.3f}")


rcb = bm.BARE_U235A_SPHERE_RC
expansion_runs("bare sphere, whole core expands",
               lambda e: [(rcb * (1 + e), scaled(U["a"], (1 + e) ** -3), False)], 500)
Rc_, T_ = bm.REFLECTED_CORE_R, bm.REFLECTED["Ub-H2O(1)-1-0-SP"][1]
expansion_runs("reflected (Ub-H2O(1)), core only expands",
               lambda e: [(Rc_ * (1 + e), scaled(U["b"], (1 + e) ** -3), False),
                          (Rc_ * (1 + e) + T_, bm.H2O_1G, True)], 510)
expansion_runs("reflected (Ub-H2O(1)), reflector only expands",
               lambda e: [(Rc_, U["b"], False),
                          (Rc_ + T_ * (1 + e), scaled(bm.H2O_1G, (1 + e) ** -3), True)], 520)
# diffusion counterpart for the bare case: k depends only on N*R
kd = lambda e: df.bare_sphere_k(scaled(U["a"], (1 + e) ** -3), rcb * (1 + e))[0]
fb["bare_diffusion_dlnk_deps"] = float((np.log(kd(eps)) - np.log(kd(-eps))) / (2 * eps))
log(f"  bare sphere, diffusion                           dln k/d eps = {fb['bare_diffusion_dlnk_deps']:+.3f}")

ALPHA = 17.2e-6      # 1/K, U-10Mo mean CTE RT-800 C (Burkes et al., INL/EXT-10-19373), proxy for U-7.65Mo
BETA = 0.00688       # KRUSTY beta_eff from MCNP (Poston et al. 2020, KRUSTY Reactor Design)
for key in ("bare sphere, whole core expands", "reflected (Ub-H2O(1)), core only expands"):
    c = fb[key]["dlnk_deps"] * ALPHA / BETA * 100.0
    cs = fb[key]["sigma"] * ALPHA / BETA * 100.0
    fb[key]["cents_per_K"] = float(c); fb[key]["cents_per_K_sigma"] = float(cs)
    log(f"  -> {key}: alpha*dln k/d eps / beta = {c:+.3f} +/- {cs:.3f} cents/K")
fb["alpha_per_K"] = ALPHA; fb["beta_eff"] = BETA; fb["eps"] = eps
fb["krusty_fuel_coeff_cents_per_K"] = -0.1844        # KRUSTY Reactor Design, Table II (published model result)
fb["krusty_fuel_expansion_share"] = 0.90               # ~90% of fuel feedback from expansion (same source)
fb["krusty_measured_cents_per_C"] = 0.2              # magnitude, ~800 C (Results of the KRUSTY Nuclear System Test)
log(f"  KRUSTY (published): fuel coefficient -0.1844 c/K (design model, Table II); ~90% from expansion -> "
    f"{-0.1844*0.9:.3f} c/K; measured magnitude ~0.2 c/C near 800 C")
R["feedback"] = fb

R["runtime_minutes"] = round((time.time() - T0) / 60, 1)
log(f"\nTotal runtime: {R['runtime_minutes']} min")


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return round(float(o), 7)
    if isinstance(o, np.integer):
        return int(o)
    return o


(RES / "analysis_results.json").write_text(json.dumps(_clean(R), indent=1))
(RES / "analysis_output.txt").write_text("\n".join(lines) + "\n")
print("wrote", RES / "analysis_results.json")
