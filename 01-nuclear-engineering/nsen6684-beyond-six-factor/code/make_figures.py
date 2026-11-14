#!/usr/bin/env python3
"""
Figures for the report (light) and slides (--dark) from results/analysis_results.json.
Run run_analysis.py first. No calculation results are created here except smooth
diffusion curves evaluated with diffusion.py for plotting.

Published KRUSTY values plotted in fig_krusty_feedback come from Poston et al.,
"KRUSTY Reactor Design," Nucl. Technol. 206 (2020), Table II (design-model results).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import benchmarks as bm  # noqa: E402
import diffusion as df  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DARK = "--dark" in sys.argv
FIG = ROOT / "figures" / ("dark" if DARK else "")
FIG.mkdir(parents=True, exist_ok=True)
R = json.loads((ROOT / "results" / "analysis_results.json").read_text())

if DARK:
    AMBER, TEAL, SKY, GRAY, INK, CORAL = "#F28C38", "#2EC4B6", "#8FB3E0", "#7D8AA3", "#E8ECF2", "#E06C55"
    BG, GRID, EDGE, TICK = "#141D2E", "#24304A", "#4A5876", "#B8C2D3"
else:
    AMBER, TEAL, SKY, GRAY, INK, CORAL = "#D9702A", "#1F8A7E", "#3E5F8A", "#8A94A6", "#1B2430", "#B5523B"
    BG, GRID, EDGE, TICK = "#FFFFFF", "#E3E6EB", "#5A6475", "#3A4352"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": INK, "axes.titlecolor": INK, "axes.labelcolor": INK,
    "axes.edgecolor": EDGE, "xtick.color": TICK, "ytick.color": TICK,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "DejaVu Sans", "font.size": 15 if DARK else 11, "axes.titlesize": 15 if DARK else 12,
    "axes.labelsize": 15 if DARK else 11, "legend.fontsize": 13 if DARK else 9,
    "xtick.labelsize": 14 if DARK else 10, "ytick.labelsize": 14 if DARK else 10, "legend.frameon": False,
    "savefig.dpi": 220, "savefig.bbox": "tight",
})
FSm = 13 if DARK else 9          # annotation font size
ILLUS = "Idealized LA-13511 benchmark constants — mathematical illustration, not a reactor calculation"


def save(fig, name, note=True):
    if DARK:                          # slides carry their own titles and labels
        for a in fig.axes:
            for loc in ("left", "center", "right"):
                a.set_title("", loc=loc)
    if note and not DARK:
        fig.text(0.01, -0.02, ILLUS, fontsize=8, color=GRAY, ha="left", va="top")
    fig.savefig(FIG / f"{name}.png")
    fig.savefig(FIG / f"{name}.pdf")
    plt.close(fig)


U = bm.U235
ver, sens, refl, spec, fb = R["verification"], R["sensitivity"], R["reflector"], R["spectral"], R["feedback"]

# ---------------------------------------------------------------- power iteration
kh = np.array(ver["Ua-1-0-SP"]["k_history"]); ni = R["settings"]["inactive"]
fig, ax = plt.subplots(figsize=(6.6, 3.6))
ax.axvspan(0, ni, color=GRAY, alpha=0.15, lw=0)
ax.plot(np.arange(len(kh)), kh, color=SKY, lw=1.1)
ax.axhline(1.0, color=AMBER, ls="--", lw=1.4)
ax.text(ni / 2, kh.min() + 0.25 * (1 - kh.min()), "inactive\n(source\nconverging)", ha="center", va="center", fontsize=FSm, color=GRAY)
ax.text(len(kh) * 0.98, 1.0 - 0.012, "exact eigenvalue k = 1 (LA-13511)", ha="right", va="top", fontsize=FSm, color=AMBER)
ka = ver["Ua-1-0-SP"]
ax.set_title(f"Power iteration, bare sphere at R_c: k = {ka['k_mc']:.4f} ± {ka['k_std']:.4f}", loc="left")
ax.set_xlabel("Generation (power-iteration cycle)")
ax.set_ylabel("k per generation")
save(fig, "fig_power_iteration")

# ---------------------------------------------------------------- sensitivity (2 panels)
rows = sens["rows"]
Rm = np.array([r["R"] for r in rows]); km = np.array([r["k_mc"] for r in rows]); ks = np.array([r["k_std"] for r in rows])
lm = np.array([r["leak_mc"] for r in rows])
Rd = np.linspace(3.5, 14.5, 300)
kd = np.array([df.bare_sphere_k(U["a"], x)[0] for x in Rd])
ld = np.array([1 - df.bare_sphere_k(U["a"], x)[2] for x in Rd])
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.6, 4.0))
a1.plot(Rd, kd, color=SKY, lw=2.2, label="one-group diffusion")
a1.errorbar(Rm, km, yerr=2 * ks, fmt="o", color=AMBER, ms=6, capsize=2, label="Monte Carlo transport (±2σ)")
a1.axhline(1, color=GRAY, ls="--", lw=1)
a1.axvline(sens["rc_exact"], color=AMBER, ls=":", lw=1.2)
a1.axvline(sens["rc_diff"], color=SKY, ls=":", lw=1.2)
a1.text(sens["rc_exact"] - 0.15, 0.55, f"exact R_c\n{sens['rc_exact']:.2f} cm", ha="right", fontsize=FSm, color=AMBER)
a1.text(sens["rc_diff"] + 0.15, 0.55, f"diffusion R_c\n{sens['rc_diff']:.2f} cm", ha="left", fontsize=FSm, color=SKY)
a1.set_xlabel("Sphere radius R [cm]"); a1.set_ylabel("k_eff")
a1.set_title("(a) Multiplication vs size", loc="left"); a1.legend(loc="lower right", fontsize=FSm)
a2.plot(Rd, 100 * ld, color=SKY, lw=2.2, label="diffusion: 1 − 1/(1+L²B²)")
a2.plot(Rm, 100 * lm, "o", color=AMBER, ms=6, label="Monte Carlo leakage tally")
a2b = a2.twinx()
err = np.array([r["err_pct"] for r in rows])
a2b.plot(Rm, err, "s--", color=CORAL, ms=4, lw=1.2, label="diffusion k error [%]")
a2b.set_ylabel("diffusion error in k_eff [%]", color=CORAL); a2b.tick_params(axis="y", colors=CORAL)
a2b.grid(False); a2b.spines["right"].set_visible(True)
a2.set_xlabel("Sphere radius R [cm]"); a2.set_ylabel("Neutrons leaking per source neutron [%]")
a2.set_title("(b) Leakage and diffusion error vs size", loc="left")
h1, l1 = a2.get_legend_handles_labels(); h2, l2 = a2b.get_legend_handles_labels()
a2.legend(h1 + h2, l1 + l2, loc="upper right", fontsize=FSm)
fig.tight_layout()
save(fig, "fig_sensitivity")

# ---------------------------------------------------------------- flux shape
edges = np.array(ver["Ua-1-0-SP"]["r_edges"]); ctr = 0.5 * (edges[1:] + edges[:-1])
phi = np.array(ver["Ua-1-0-SP"]["flux"]); rc = bm.BARE_U235A_SPHERE_RC
c1 = df.one_group_constants(U["a"]); Re = rc + c1["d"]
x = np.linspace(0.01, 1.0, 200) * rc
pd = np.sin(np.pi * x / Re) / x
norm_mc = np.interp(0.25 * rc, ctr, phi); norm_d = np.interp(0.25 * rc, x, pd)
fig, ax = plt.subplots(figsize=(6.2, 3.8))
ax.step(ctr / rc, phi / norm_mc, where="mid", color=AMBER, lw=1.6, label="Monte Carlo (binned)")
ax.plot(x / rc, pd / norm_d, color=SKY, lw=2, label="diffusion  sin(πr/R_e)/r")
ex = bm.BARE_U235A_FLUX_RATIOS
ax.plot(list(ex.keys()), [v / ex[0.25] for v in ex.values()], "D", color=INK, ms=7, label="exact transport (LA-13511)")
ax.set_xlim(0, 1.02); ax.set_ylim(0, 1.25)
ax.set_xlabel("r / R_c"); ax.set_ylabel("Flux (norm. at r/R_c = 0.25)" if DARK else "Scalar flux (normalized at r/R_c = 0.25)")
ax.set_title("Bare critical sphere: diffusion overestimates edge flux", loc="left")
ax.legend(fontsize=FSm, loc="lower left")
save(fig, "fig_flux_shape")

# ---------------------------------------------------------------- reflector savings
T = np.array([0.0] + [r["T"] for r in refl["rows"]])
rcm = np.array([refl["rc_bare_exact"]] + [r["rc_mc"] for r in refl["rows"]])
rcs = np.array([0.0] + [r["rc_mc_sigma"] for r in refl["rows"]])
Td = np.linspace(0.3, 10, 120)      # thin-reflector limit uses a different vacuum BC than the bare formula
rcd = np.array([df.reflected_sphere_rc(U["a"], bm.H2O_1G, t) for t in Td])
Ts_ = np.linspace(0, 10, 120)
rcslab = df.bare_sphere_rc(U["a"]) - np.array([df.slab_reflector_savings(U["a"], bm.H2O_1G, t) for t in Ts_])
fig, ax = plt.subplots(figsize=(6.4, 3.9))
ax.plot(Td, rcd, color=SKY, lw=2.2, label=("two-region diffusion" if DARK else "two-region diffusion (interface conditions)"))
ax.plot(0, df.bare_sphere_rc(U["a"]), "s", color=SKY, ms=7)
ax.plot(Ts_, rcslab, color=GRAY, lw=1.6, ls="--", label=("slab formula" if DARK else "large-core slab formula δ = (D_c/D_r)L_r tanh(T/L_r)"))
ax.errorbar(T, rcm, yerr=2 * rcs, fmt="o", color=AMBER, ms=7, capsize=2, label="Monte Carlo transport")
ax.set_xlabel("Reflector thickness T [cm]" + ("" if DARK else "   (H₂O, c = 0.90; 1 mfp = 3.06 cm)"))
ax.set_ylabel("Critical core radius R_c [cm]")
ax.set_ylim(2, 8.3)
ax.set_title("Reflector savings: transport vs diffusion vs slab formula", loc="left")
ax.legend(fontsize=FSm, loc="lower left")
save(fig, "fig_reflector_savings")

# ---------------------------------------------------------------- spectral
e2 = np.array(spec["r_edges"]); c2 = 0.5 * (e2[1:] + e2[:-1]); rc2 = spec["rc_exact"]
ff = np.array(spec["flux_fast"]); fs = np.array(spec["flux_slow"])
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.2, 3.9), gridspec_kw={"width_ratios": [1.25, 1]})
sl = slice(2, None)          # skip the two innermost bins (few collisions, noisy ratio)
a1.plot(c2[sl] / rc2, (ff / fs)[sl], color=AMBER, lw=2, label="Monte Carlo φ_fast/φ_slow")
a1.axhline(R["spectral"]["spec_inf"][0] / R["spectral"]["spec_inf"][1], color=SKY, ls="--", lw=1.6,
           label=f"infinite medium = {bm.TWO_GROUP_FLUX_RATIO_2_TO_1:.3f} (LA-13511)")
a1.set_xlabel("r / R_c"); a1.set_ylabel("Spectral index φ_fast / φ_slow")
wl = df.leakage_weighted_spectrum(bm.U235_2G, rc2)
a1.axhline(wl[0] / wl[1], color=TEAL, ls=":", lw=1.6, label=f"fundamental mode with leakage (diffusion B²) = {wl[0]/wl[1]:.3f}")
a1.set_ylim(0.4, 0.85)
a1.set_title("(a) A finite core is harder than an infinite medium", loc="left"); a1.legend(fontsize=FSm, loc="lower left")
inf_fast = 100 * spec["spec_inf"][0]
lk = np.array(spec["leak_by_group"]); fis = np.array(spec["fission_by_group"])
cats = ["flux\n(infinite medium)", "neutrons\nthat leak", "fissions"]
vals = [inf_fast, 100 * lk[0] / lk.sum(), 100 * fis[0] / fis.sum()]
bars = a2.bar(cats, vals, color=[SKY, CORAL, AMBER], width=0.55)
for b_, v in zip(bars, vals):
    a2.text(b_.get_x() + b_.get_width() / 2, v + 1, f"{v:.1f}%", ha="center", fontsize=FSm, color=INK)
a2.set_ylabel("Fast-group share [%]"); a2.set_ylim(0, max(vals) * 1.3)
a2.set_title("(b) Leakage removes fast neutrons preferentially", loc="left")
fig.tight_layout()
save(fig, "fig_spectral")

# ---------------------------------------------------------------- KRUSTY Table II (published)
comp = ["Fuel", "Heat pipes", "Ring clamp", "Axial reflector", "Vacuum can", "Radial reflector", "Platen & shielding"]
coef = [-0.1844, -0.0015, -0.0027, -0.0005, 0.0233, 0.0585, -0.0121]
temp = [1093, 1073, 1068, 473, 393, 343, 323]
fig, ax = plt.subplots(figsize=(6.6, 3.8))
cols = [CORAL if c < 0 else TEAL for c in coef]
y = np.arange(len(comp))[::-1]
ax.barh(y, coef, color=cols, height=0.6)
for yi, c, t in zip(y, coef, temp):
    ax.text(c + (0.004 if c >= 0 else -0.004), yi, f"{c:+.4f}  ({t} K)", va="center",
            ha="left" if c >= 0 else "right", fontsize=FSm, color=INK)
ax.set_yticks(y); ax.set_yticklabels(comp)
ax.axvline(0, color=EDGE, lw=1)
ax.set_xlim(-0.36 if DARK else -0.30, 0.16 if DARK else 0.13)
ax.set_xlabel("Temperature coefficient [¢/K]" if DARK else "Average reactivity temperature coefficient [¢/K]")
ax.set_title("KRUSTY component feedback (published design-model values)", loc="left")
if not DARK:
    fig.text(0.01, -0.02, "Data: Poston et al., KRUSTY Reactor Design, Nucl. Technol. 206 (2020), Table II. "
             "Operating temperatures in parentheses.", fontsize=8, color=GRAY, ha="left", va="top")
save(fig, "fig_krusty_feedback", note=False)

# ---------------------------------------------------------------- feedback comparison
b = fb["bare sphere, whole core expands"]; rr = fb["reflected (Ub-H2O(1)), core only expands"]
labels = (["bare\nsphere", "reflected\ncore", "KRUSTY\nexpansion*", "KRUSTY\nfuel total*", "KRUSTY\nmeasured"]
          if DARK else ["Idealized bare\nsphere (this work)", "Idealized reflected\ncore (this work)",
                        "KRUSTY fuel,\nexpansion share*", "KRUSTY fuel\ntotal*", "KRUSTY measured\n(~800 °C)"])
vals = [b["cents_per_K"], rr["cents_per_K"], fb["krusty_fuel_coeff_cents_per_K"] * fb["krusty_fuel_expansion_share"],
        fb["krusty_fuel_coeff_cents_per_K"], -fb["krusty_measured_cents_per_C"]]
errs = [2 * b["cents_per_K_sigma"], 2 * rr["cents_per_K_sigma"], 0, 0, 0]
cols = [AMBER, AMBER, SKY, SKY, TEAL]
fig, ax = plt.subplots(figsize=(6.8, 3.8))
bars = ax.bar(range(5), vals, yerr=errs, color=cols, width=0.6, capsize=3, ecolor=INK)
for i, v in enumerate(vals):
    ax.text(i, v - 0.015, f"{v:.2f}", ha="center", va="top", fontsize=FSm, color=INK)
ax.set_xticks(range(5)); ax.set_xticklabels(labels, fontsize=FSm)
ax.axhline(0, color=EDGE, lw=1)
ax.set_ylim(min(vals) * 1.3, 0.03)
ax.set_ylabel("Coefficient [¢/K]" if DARK else "Fuel expansion reactivity coefficient [¢/K]")
ax.set_title("Expansion feedback: idealized estimate vs KRUSTY", loc="left")
if not DARK:
    fig.text(0.01, -0.02, "This work: (dln k/dε)·α/β with α = 17.2e-6/K (U-10Mo proxy) and β = 0.00688. "
             "*Published design-model values (Table II); measured value from the 2018 test.",
             fontsize=7.6, color=GRAY, ha="left", va="top")
save(fig, "fig_feedback_compare", note=False)
# ---------------------------------------------------------------- single-panel versions (slides)
FS = 13 if DARK else 9
fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.plot(Rd, kd, color=SKY, lw=3, label="one-group diffusion")
ax.plot(Rm, km, "o", color=AMBER, ms=9, label="Monte Carlo transport")
ax.axhline(1, color=GRAY, ls="--", lw=1.2)
ax.annotate(f"exact R_c = {sens['rc_exact']:.2f} cm", (sens["rc_exact"], 1.0), xytext=(9.3, 0.62),
            color=AMBER, fontsize=FS, arrowprops=dict(arrowstyle="->", color=AMBER))
ax.annotate(f"diffusion R_c = {sens['rc_diff']:.2f} cm", (sens["rc_diff"], 1.0), xytext=(9.8, 0.80),
            color=SKY, fontsize=FS, arrowprops=dict(arrowstyle="->", color=SKY))
ax.set_xlabel("Sphere radius R [cm]"); ax.set_ylabel("k_eff")
ax.legend(loc="upper left")
save(fig, "fig_k_vs_R")

fig, ax = plt.subplots(figsize=(6.6, 4.6))
sl = slice(2, None)
ax.plot(c2[sl] / rc2, (ff / fs)[sl], color=AMBER, lw=3, label="Monte Carlo, critical sphere")
ax.axhline(wl[0] / wl[1], color=TEAL, ls=":", lw=2.2, label=f"with leakage (diffusion B²): {wl[0]/wl[1]:.2f}")
ax.axhline(bm.TWO_GROUP_FLUX_RATIO_2_TO_1, color=SKY, ls="--", lw=2.2, label=f"infinite medium: {bm.TWO_GROUP_FLUX_RATIO_2_TO_1:.2f}")
ax.set_ylim(0.4, 1.0)
ax.set_xlabel("r / R_c"); ax.set_ylabel("Fast / slow flux")
ax.legend(loc="upper left")
save(fig, "fig_spectral_index")

fig, ax = plt.subplots(figsize=(6.0, 4.6))
cats = ["flux,\ninfinite\nmedium", "neutrons\nthat leak", "fissions"]
vals = [inf_fast, 100 * lk[0] / lk.sum(), 100 * fis[0] / fis.sum()]
bars = ax.bar(cats, vals, color=[SKY, CORAL, AMBER], width=0.6)
for b_, v in zip(bars, vals):
    ax.text(b_.get_x() + b_.get_width() / 2, v + 1.2, f"{v:.0f}%", ha="center", fontsize=FS + 3, color=INK, fontweight="bold")
ax.set_ylabel("Fast-group share [%]"); ax.set_ylim(0, 58)
save(fig, "fig_fast_share")
print("figures written to", FIG)
