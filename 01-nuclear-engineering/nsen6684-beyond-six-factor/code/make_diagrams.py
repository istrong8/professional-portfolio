#!/usr/bin/env python3
"""
Conceptual diagrams for the NSEN 6684 presentation and report (original artwork).

    fig_life_cycle.png/.pdf      thermal-reactor life cycle (six-factor ledger) vs fast-spectrum cycle
    fig_bare_vs_reflected.*      conceptual leakage comparison (not a transport result)
    fig_krusty_schematic.*       simplified, not-to-scale KRUSTY layout from public descriptions

The life-cycle numbers are read from results/analysis_results.json, so run
run_analysis.py first.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DARK = "--dark" in sys.argv            # dark-card versions for the slide deck
FIG = ROOT / "figures" / ("dark" if DARK else "")
FIG.mkdir(parents=True, exist_ok=True)
RES = ROOT / "results"

if DARK:
    AMBER, TEAL, SLATE, GRAY, INK, LOSS = "#E8833A", "#2A9D8F", "#4F6E94", "#7D8AA3", "#E8ECF2", "#C9583F"
    BG, DARKTXT, DIVIDER = "#141D2E", "#1B2430", "#2A3650"
    LINE_SLATE = "#8FB3E0"
else:
    AMBER, TEAL, SLATE, GRAY, INK, LOSS = "#E8833A", "#2A9D8F", "#46607D", "#8A94A6", "#1B2430", "#B5523B"
    BG, DARKTXT, DIVIDER = "#FFFFFF", "#1B2430", "#E3E6EB"
    LINE_SLATE = SLATE
LOSS_TXT = "#F08A70" if DARK else LOSS
TEAL_TXT = "#4FD1C5" if DARK else TEAL
AMBER_TXT = "#F5A15E" if DARK else AMBER
plt.rcParams.update({"font.family": "DejaVu Sans", "savefig.dpi": 220, "savefig.bbox": "tight",
                     "figure.facecolor": BG, "savefig.facecolor": BG, "text.color": INK})


def save(fig, name):
    fig.savefig(FIG / f"{name}.png")
    fig.savefig(FIG / f"{name}.pdf")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, ec=None, tc="white", fs=10.5, bold=False):
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                       fc=fc, ec=ec or fc, lw=1.5)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", color=tc, fontsize=fs,
            fontweight="bold" if bold else "normal", linespacing=1.25)


def arrow(ax, p0, p1, color=INK, lw=1.8, style="-|>", ls="-", rad=0.0):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=14, color=color, lw=lw,
                        linestyle=ls, connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a)


# ---------------------------------------------------------------------------
# 1. Life cycle: thermal (left) vs fast (right), one fixed-scale canvas
# ---------------------------------------------------------------------------
res = json.loads((RES / "analysis_results.json").read_text())["classical"]
L = res["ledger"]
fac = res["factors"]
cc = {"P_FNL": res["P_FNL"], "P_TNL": res["P_TNL"]}

fig = plt.figure(figsize=(15.4, 7.8))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 30.8)
ax.set_ylim(-1.4, 14.2)
ax.axis("off")
FS = 12
W, H = 4.5, 1.85
X = [2.6, 8.4, 14.2]
YT, YM, YB = 11.0, 6.5, 2.0
pos = {0: (X[0], YT), 1: (X[1], YT), 2: (X[2], YT), 3: (X[2], YM), 4: (X[2], YB), 5: (X[1], YB), 6: (X[0], YB)}
labels = [
    f"{L[0]:.0f} thermal neutrons\nabsorbed in fuel",
    f"{L[1]:.0f} fast neutrons\nfrom thermal fission",
    f"{L[2]:.0f} fast neutrons\n(incl. fast fission)",
    f"{L[3]:.0f} fast neutrons\nstay in the core",
    f"{L[4]:.0f} neutrons\nreach thermal energy",
    f"{L[5]:.0f} thermal neutrons\nstay in the core",
    f"{L[6]:.0f} absorbed in fuel\n= next generation",
]
cols = [SLATE, AMBER, AMBER, AMBER, TEAL, TEAL, SLATE]
for i, (x, y) in pos.items():
    box(ax, x, y, W, H, labels[i], cols[i], fs=FS, bold=(i in (0, 6)))
ax.text(0.4, 13.6, "Thermal reactor: six-factor life cycle (hypothetical compact core)",
        fontsize=15, color=INK, fontweight="bold", va="center")
# top row factors (above the gap)
for i, lab in ((0, f"× η = {fac['eta']:.2f}"), (1, f"× ε = {fac['epsilon']:.2f}")):
    x0, x1 = X[i] + W / 2, X[i + 1] - W / 2
    arrow(ax, (x0, YT), (x1, YT))
    ax.text((x0 + x1) / 2, YT + 1.35, lab, ha="center", fontsize=FS + 0.5, color=INK)
# right column: factor on the left of arrow, loss to the right
for (ya, yb, lab, loss) in ((YT, YM, f"× P_FNL = {cc['P_FNL']:.2f}", f"fast leakage\n−{L[2]-L[3]:.0f}"),
                            (YM, YB, f"× p = {fac['p']:.2f}", f"resonance capture\n−{L[3]-L[4]:.0f}")):
    y0, y1 = ya - H / 2, yb + H / 2
    arrow(ax, (X[2], y0), (X[2], y1))
    ym = (y0 + y1) / 2
    ax.text(X[2] - 0.3, ym, lab, ha="right", va="center", fontsize=FS + 0.5, color=INK)
    arrow(ax, (X[2], ym), (X[2] + 2.0, ym), color=LOSS, lw=1.5, ls="--")
    ax.text(X[2] + 2.15, ym, loss, ha="left", va="center", fontsize=FS, color=LOSS_TXT)
# bottom row: factor above arrow (interior), loss below
for (i, j, lab, loss) in ((4, 5, f"× P_TNL = {cc['P_TNL']:.2f}", f"thermal leakage\n−{L[4]-L[5]:.0f}"),
                          (5, 6, f"× f = {fac['f']:.2f}", f"absorbed outside fuel\n−{L[5]-L[6]:.0f}")):
    x0, x1 = pos[i][0] - W / 2, pos[j][0] + W / 2
    arrow(ax, (x0, YB), (x1, YB))
    xm = (x0 + x1) / 2
    ax.text(xm, YB + 1.3, lab, ha="center", fontsize=FS + 0.5, color=INK)
    arrow(ax, (xm, YB), (xm, YB - 1.35), color=LOSS, lw=1.5, ls="--")
    ax.text(xm, YB - 1.55, loss, ha="center", va="top", fontsize=FS - 0.5, color=LOSS_TXT)
# return arrow and k
arrow(ax, (X[0], YB + H / 2), (X[0], YT - H / 2), color=LINE_SLATE, lw=2.2, ls=":")
ax.text(X[0] + 0.5, YM, f"k_eff = {L[6]:.0f} / {L[0]:.0f}\n        = {L[6]/L[0]:.3f}", ha="left", va="center",
        fontsize=12.5, color=LINE_SLATE, fontweight="bold")

# divider
ax.plot([20.0, 20.0], [-0.8, 13.0], color=DIVIDER, lw=1.5)

# fast-spectrum panel
ax.text(20.6, 13.6, "Fast-spectrum core (KRUSTY-type)", fontsize=15, color=INK, fontweight="bold", va="center")
FX = 25.6
box(ax, FX, YT, 5.6, 1.75, "Fission by fast neutrons\nν ≈ 2.5 per fission, ~MeV", AMBER, fs=FS, bold=True)
box(ax, FX, 7.9, 5.6, 1.75, "Little slowing down\n(no moderator: no p, no f)", AMBER, fs=FS)
arrow(ax, (FX, YT - 0.875), (FX, 7.9 + 0.875))
OX = [22.2, 25.6, 29.0]
outs = [("Fission\n→ next generation", SLATE), ("Capture\n(fuel, structure)", LOSS), ("Leakage\n(large fraction)", LOSS)]
for x, (t, c) in zip(OX, outs):
    box(ax, x, 3.6, 3.1, 1.55, t, c, fs=FS - 1)
    arrow(ax, (FX, 7.9 - 0.875), (x, 3.6 + 0.78))
box(ax, OX[2], 0.75, 3.2, 1.1, "reflector\nreturns some", TEAL, fs=FS - 1.5)
arrow(ax, (OX[2], 0.75 + 0.55), (OX[2], 3.6 - 0.78), color=TEAL, lw=1.8)
arrow(ax, (OX[0] - 1.55, 3.6), (20.4, 3.6), color=LINE_SLATE, lw=2.0, ls=":", style="-")
arrow(ax, (20.4, 3.6), (20.4, YT), color=LINE_SLATE, lw=2.0, ls=":", style="-")
arrow(ax, (20.4, YT), (FX - 2.8, YT), color=LINE_SLATE, lw=2.0, ls=":")
ax.text(OX[0] + 1.7, 1.55, "k = production / (absorption + leakage)", ha="center", fontsize=FS + 0.5,
        color=INK, style="italic")
ax.text(0.4, -1.15, "Assumed LWR-like factors for review (code/run_analysis.py, study 0). Not data for any real reactor.",
        fontsize=9, color=GRAY)
save(fig, "fig_life_cycle")


# ---------------------------------------------------------------------------
# 2. Bare vs reflected (conceptual)
# ---------------------------------------------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(11, 5.2))
rng = np.random.default_rng(7)
for a, title, refl in ((axs[0], "Bare multiplying region", False),
                       (axs[1], "Reflected multiplying region", True)):
    a.set_xlim(-5, 5)
    a.set_ylim(-5, 5)
    a.set_aspect("equal")
    a.axis("off")
    a.set_title(title, fontsize=16, color=INK, fontweight="bold")
    if refl:
        a.add_patch(Circle((0, 0), 3.9, fc=("#16343A" if DARK else "#D9EFEC"), ec=TEAL, lw=2))
        a.text(0, -3.45, "reflector", ha="center", color=TEAL_TXT, fontsize=13)
    a.add_patch(Circle((0, 0), 2.0, fc="#F6D2B5", ec=AMBER, lw=2))
    a.text(0, 0, "core", ha="center", va="center", color=DARKTXT, fontsize=15, fontweight="bold")
    angles = np.linspace(0, 2 * np.pi, 9, endpoint=False) + 0.2
    for k, th in enumerate(angles):
        r0 = 0.6 + 0.5 * rng.random()
        p0 = (r0 * np.cos(th), r0 * np.sin(th))
        if not refl or k % 3 == 2:
            p1 = (4.6 * np.cos(th), 4.6 * np.sin(th))
            arrow(a, p0, p1, color=LOSS, lw=1.6)
        else:
            pr = (3.4 * np.cos(th), 3.4 * np.sin(th))
            back = (1.25 * np.cos(th + 0.55), 1.25 * np.sin(th + 0.55))
            arrow(a, p0, pr, color=LINE_SLATE, lw=1.6)
            arrow(a, pr, back, color=TEAL, lw=1.6, rad=0.25)
    a.text(0, -4.85, "most escaping neutrons are lost" if not refl else
           "some escaping neutrons scatter back into the core",
           ha="center", fontsize=13, color=INK)
fig.text(0.5, 0.01, "Conceptual sketch only — not a transport calculation.", ha="center",
         fontsize=9.5, color=GRAY)
save(fig, "fig_bare_vs_reflected")


# ---------------------------------------------------------------------------
# 3. KRUSTY simplified schematic (axial cut, not to scale, operating configuration)
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(9.6, 7.4))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(-52, 50)
ax.set_ylim(-31, 59)
ax.set_aspect("equal")
ax.axis("off")
for x0 in (-23.3, 20.3):                       # stainless radial shield
    ax.add_patch(Rectangle((x0, -4), 3.0, 33, fc="#C9CED6", ec=GRAY, lw=1))
for x0 in (-19.05, 7.25):                      # BeO radial reflector, raised around core
    ax.add_patch(Rectangle((x0, -4), 11.8, 33, fc="#D9EFEC", ec=TEAL, lw=1.6))
for x0 in (-24.0, 7.25):                       # platen (two halves around vessel)
    ax.add_patch(Rectangle((x0, -8), 16.75, 4, fc="#DDE1E7", ec=GRAY, lw=1))
ax.add_patch(Rectangle((-6.8, -12), 13.6, 46, fc="none", ec=LINE_SLATE, lw=1.3, ls="--"))   # vacuum vessel
ax.add_patch(Rectangle((-6.35, -10.2), 12.7, 10.2, fc="#D9EFEC", ec=TEAL, lw=1.2))   # lower axial BeO
ax.add_patch(Rectangle((-6.35, 25), 12.7, 6, fc="#D9EFEC", ec=TEAL, lw=1.2))         # upper axial BeO
for x0 in (-5.5, 2.0):                         # fuel annulus
    ax.add_patch(Rectangle((x0, 0), 3.5, 25, fc="#F6D2B5", ec=AMBER, lw=1.6))
ax.add_patch(Rectangle((-1.6, 0), 3.2, 25, fc="#5C6370", ec=("#AAB4C5" if DARK else INK), lw=1))              # B4C rod
for x in (-5.9, 5.9):                          # heat pipes
    ax.plot([x, x], [-8, 47], color=LOSS, lw=3, solid_capstyle="round")
ax.add_patch(FancyBboxPatch((-13, 47), 26, 6, boxstyle="round,pad=0.3", fc="#EDE3F1", ec="#7A5C8A", lw=1.3))
ax.text(0, 50, "2 Stirling convertors +\n6 thermal simulators", ha="center", va="center", fontsize=11.5, color=DARKTXT)


def call(xy, txy, text, color=INK, ha="left"):
    color = {TEAL: TEAL_TXT, AMBER: AMBER_TXT, LOSS: LOSS_TXT, SLATE: LINE_SLATE}.get(color, color)
    ax.annotate(text, xy=xy, xytext=txy, fontsize=(15 if DARK else 12), color=color, va="center", ha=ha,
                arrowprops=dict(arrowstyle="-", color=color, lw=0.9, shrinkA=2, shrinkB=0))


call((-3.8, 14), (-27, 14), "HEU U-7.65Mo fuel\n(annulus: 11 cm OD,\n4 cm ID, 25 cm tall)", AMBER, "right")
call((0, 22), (-27, 38), "central B4C rod", INK, "right")
call((-4, -6), (-27, -12), "BeO axial\nreflectors", TEAL, "right")
call((5.9, 41), (25, 42), "8 sodium heat pipes", LOSS)
call((6.8, 32), (25, 35), "vacuum vessel", SLATE)
call((14, 18), (25, 24), "BeO radial reflector\n(raised around core)", TEAL)
call((22.5, 8), (25, 8), "stainless steel\nradial shield", GRAY)
call((18, -6), (25, -8), "platen", GRAY)
arrow(ax, (-15, -24), (-15, -9), color=TEAL, lw=2.4)
ax.text(-13.5, -17, "platen lifts the radial reflector\ninto place → adds reactivity", fontsize=(15 if DARK else 12),
        color=TEAL_TXT, va="center")
ax.text(0, 57, "KRUSTY — simplified axial cut (not to scale)", ha="center", fontsize=12.5,
        fontweight="bold", color=INK)
ax.text(0, -29.5, "Original schematic drawn from public descriptions (Poston et al. 2020; Sanchez et al. 2020).",
        ha="center", fontsize=8.6, color=GRAY)
save(fig, "fig_krusty_schematic")
print("Diagrams written to", FIG)
