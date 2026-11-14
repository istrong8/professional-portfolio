"""
Published cross sections and exact solutions used in this study.

Source: A. Sood, R. A. Forster, D. K. Parsons, "Analytical Benchmark Test Set for
Criticality Code Verification," LA-13511, Los Alamos National Laboratory (1999);
also Progress in Nuclear Energy 42(1), 55-106 (2003).

These are *verification* data: idealized one- and two-group constants with exact
transport solutions. LA-13511 states they are not general-purpose cross sections
and are not meant to predict experiments. They are used here because every value is
published and every critical dimension is known exactly, so both the Monte Carlo
solver and the diffusion approximation can be tested against a known answer.

Units: macroscopic cross sections in 1/cm, lengths in cm. All scattering isotropic.
Group convention in this code: g = 0 fast, g = 1 slow (LA-13511 numbers the fast
group "2"; the mapping is done below).
"""
import numpy as np


def material(nu, sig_f, sig_c, sig_s, sig_t, chi=None):
    """Build a material dict. sig_s is the group-to-group matrix [from, to]."""
    nu = np.atleast_1d(np.asarray(nu, float))
    sig_f = np.atleast_1d(np.asarray(sig_f, float))
    sig_c = np.atleast_1d(np.asarray(sig_c, float))
    sig_s = np.atleast_2d(np.asarray(sig_s, float))
    sig_t = np.atleast_1d(np.asarray(sig_t, float))
    G = sig_t.size
    chi = np.ones(G) / G if chi is None else np.asarray(chi, float)
    sig_a = sig_f + sig_c
    # consistency check: total = absorption + all scattering out of the group
    assert np.allclose(sig_t, sig_a + sig_s.sum(axis=1), rtol=1e-6), "inconsistent cross sections"
    return {"nu": nu, "sig_f": sig_f, "sig_c": sig_c, "sig_a": sig_a, "sig_s": sig_s,
            "sig_t": sig_t, "nusig_f": nu * sig_f, "chi": chi}


# --- One-group U-235 sets (LA-13511 Table 12); only nu differs between a, b, c, d
_U = dict(sig_f=0.065280, sig_c=0.013056, sig_s=[[0.248064]], sig_t=0.32640)
U235 = {
    "a": material(nu=2.70, **_U),       # c = 1.30
    "b": material(nu=2.797101, **_U),   # c = 1.3194202
    "c": material(nu=2.707308, **_U),   # c = 1.3014616
    "d": material(nu=2.679198, **_U),   # c = 1.2958396
}
# One-group H2O reflector, c = 0.90 (LA-13511 Table 15 problems)
H2O_1G = material(nu=0.0, sig_f=0.0, sig_c=0.032640, sig_s=[[0.293760]], sig_t=0.32640)
VOID = None

# --- Exact one-group results (LA-13511 Tables 13-15)
BARE_U235A_SPHERE_RC = 7.428998            # Ua-1-0-SP, cm (2.4248249802 mfp)
BARE_U235A_FLUX_RATIOS = {0.25: 0.93244907, 0.50: 0.74553332, 0.75: 0.48095413, 1.00: 0.17177706}
REFLECTED_CORE_R = 6.12745                 # 2 mfp, all three reflected problems
REFLECTED = {                              # (U-235 set, H2O thickness cm) -> k_eff = 1 exactly
    "Ub-H2O(1)-1-0-SP": ("b", 3.063725),
    "Uc-H2O(2)-1-0-SP": ("c", 6.12745),
    "Ud-H2O(3)-1-0-SP": ("d", 9.191176),
}

# --- Two-group U-235 (LA-13511 Tables 33-35). LA-13511 fast group = "2".
# chi_slow is illegible in the scanned report; chi_fast = 0.575 is printed, so
# chi_slow = 1 - 0.575 = 0.425. This is checked against the published
# k_inf = 2.216349 in verify_two_group_kinf() below.
U235_2G = material(
    nu=[2.70, 2.50],
    sig_f=[0.06192, 0.06912],
    sig_c=[0.00384, 0.01344],
    sig_s=[[0.078240, 0.0720],   # fast -> fast, fast -> slow
           [0.0,      0.26304]], # slow -> fast, slow -> slow
    sig_t=[0.2160, 0.3456],
    chi=[0.575, 0.425],
)
TWO_GROUP_KINF = 2.216349
TWO_GROUP_FLUX_RATIO_2_TO_1 = 0.474967     # LA-13511, infinite medium (group 2 = fast)
TWO_GROUP_SPHERE_RC = 7.909444             # U-2-0-SP, cm


def kinf(mat):
    """Infinite-medium multiplication and fundamental spectrum (multigroup)."""
    G = mat["sig_t"].size
    M = np.diag(mat["sig_t"]) - mat["sig_s"].T
    F = np.outer(mat["chi"], mat["nusig_f"])
    w, v = np.linalg.eig(np.linalg.solve(M, F))
    i = np.argmax(w.real)
    phi = np.abs(v[:, i].real)
    return w[i].real, phi / phi.sum()


def verify_two_group_kinf():
    k, phi = kinf(U235_2G)
    return k, phi[0] / phi[1]


if __name__ == "__main__":
    for key, m in U235.items():
        print(f"U-235({key}) k_inf = {kinf(m)[0]:.6f}  c = {(m['nusig_f'][0] + m['sig_s'][0, 0]) / m['sig_t'][0]:.7f}")
    k2, ratio = verify_two_group_kinf()
    print(f"Two-group k_inf = {k2:.6f} (LA-13511: {TWO_GROUP_KINF});  fast/slow flux = {ratio:.6f} "
          f"(LA-13511 group-2-to-1: {TWO_GROUP_FLUX_RATIO_2_TO_1})")
