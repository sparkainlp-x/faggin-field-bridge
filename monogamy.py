# monogamy.py
#
# CKW monogamy in triads: pairwise concurrence misses
# genuine tripartite entanglement, and D tracks the
# one-to-rest tangle, not the pairwise one.
#
# The mechanism, defined inside the model (not discovered):
#   - A thought is a TWO-QUBIT state, so a triad of three
#     thoughts is a six-qubit system where pairwise Wootters
#     concurrence is not directly defined. The triads here
#     are therefore THREE-QUBIT pure states (8-dim), where
#     each member is a BINARY thought -- one qubit whose
#     basis maps into the thought space as |0> -> |00>
#     (attention) and |1> -> |10> (self). The mapping is a
#     DEFINITION (an embedding), not a discovery: it says
#     which two of the four concepts a binary thought can
#     be, nothing more.
#   - GHZ-like triad = (|000> + |111>) / sqrt(2);
#     W-like triad = (|001> + |010> + |100>) / sqrt(3).
#     Two interpolation families connect them and probe
#     the D-vs-tangle relation:
#       (a) generalized GHZ: a|000> + sqrt(1-a^2)|111>,
#           a in [1/sqrt(2), 1] -- pairwise tangle is
#           EXACTLY zero throughout, while the one-to-rest
#           tangle sweeps 1 -> 0;
#       (b) GHZ/W interpolation: cos(t)|GHZ> + sin(t)|W>.
#   - Pairwise tangle tau_ij = C^2, C the Wootters
#     concurrence (thought_entanglement.py) of the reduced
#     two-qubit state (third qubit traced out).
#   - One-to-rest tangle tau_A(BC) = 4 det(rho_A), exact
#     for pure states (rho_A the member's reduced 2x2
#     state). Residual genuine-tripartite tangle =
#     tau_A(BC) - tau_AB - tau_AC (Coffman-Kundu-Wootters).
#   - D_A for a member = Tr(P rho_A_embedded), the EXISTING
#     self-knowing projector (self_knowing.py) on the
#     member's embedded 4-dim reduced state.
#   - Noise: unity.gaussian_copies on the 8-dim triad
#     vector (the same model as everywhere else, seeded);
#     the copies stay PURE, so the 4 det(rho_A) formula
#     stays valid.
#
# Pilot verification of the embedding (exact values, before
# any claim was written):
#   GHZ: tau_A(BC) = 1, pairwise tau = 0, residual = 1,
#     D_A = 2/3. W: tau_A(BC) = 8/9, pairwise tau = 4/9
#     each, residual = 0, D_A = 7/9. All exact to 1e-9.
#   Noise keeps the copies pure (purity 1.0 at every
#   sigma); the smallest CKW margin seen in the pilot is
#   0.0485 (noisy W, sigma = 1.0).
#
# Honesty, stated up front:
#   - Monogamy is an ESTABLISHED THEOREM of quantum
#     information (Coffman-Kundu-Wootters, Phys. Rev. A 61,
#     052306, 2000; Osborne & Verstraete, Phys. Rev. Lett.
#     96, 220503, 2006) applied to the model's states. The
#     triads are defined in code, not physical systems; the
#     binary-thought embedding is a definition, not a
#     discovery. Classical emulation throughout. Faggin's
#     metaphysics is interpretive and is NOT tested here.
#   - Claim (xvii) is a CODE CHECK, not a discovery: if
#     the CKW inequality is ever violated, the code's
#     concurrence is wrong, not the theorem. It is
#     reported as a defect, not a result.
#   - The headline numbers sit near saturation (REPORT.md
#     section 5, v0.3.1 review): the curves -- residual vs
#     pairwise sum, D_A vs tau_A(BC) -- are the science,
#     not the points.
#
# Pre-registered verdict rules for claims (xvii)-(xix),
# written before the final measurement run (see the
# claim_*_verdict functions and REPORT.md section 13).
# Thresholds are round numbers set from the pilot sweep:
#   (xvii) CKW holds: tau_AB + tau_AC <= tau_A(BC) for
#       EVERY triad and EVERY sigma in the sweep (GHZ, W,
#       both interpolation families, noisy copies at
#       sigma = 0.00, 0.25, 0.50, 1.00), for every member.
#       The minimum margin must be >= -CKW_TOL (1e-9,
#       numerical zero). A violation is a defect.
#   (xviii) GHZ vs W: at sigma = 0 the GHZ-like triad has
#       pairwise tangle <= 1e-9 and residual >= 1 - 1e-9,
#       while the W-like triad has pairwise tangle 4/9
#       each (within 1e-9) and residual <= 1e-9. The
#       pairwise-only miss fraction (residual /
#       tau_A(BC)) is >= 0.9 for GHZ and <= 0.1 for W.
#       Pairwise concurrence therefore MISSES the GHZ
#       entanglement entirely.
#   (xix) D_A falls as tau_A(BC) rises even when tau_AB
#       is flat: on the generalized-GHZ branch
#       a in [1/sqrt(2), 1], Pearson(D_A, tau_A(BC))
#       <= -0.95 (pilot: -0.9608), max tau_AB <= 1e-9
#       (pilot: exactly 0), and the D_A range >= 0.25
#       (pilot: 1/3). The GHZ/W interpolation and the GHZ
#       noise sweep are reported descriptively, not gated:
#       the interpolation confounds tau_AB (it rises to
#       4/9) and the noise sweep moves D_A and tau_A(BC)
#       together (both decay with noise), so neither
#       separates "entanglement with the pair" from
#       "entanglement with B" -- the generalized-GHZ
#       branch is the clean test.
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""CKW monogamy of entanglement in triads of binary thoughts."""

import math

import numpy as np

import bridge
import self_knowing as sk
import thought_entanglement as te
import unity

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TRIAD_DIM = 8
MEMBERS = (0, 1, 2)
SIGMA_GRID = [0.0, 0.25, 0.5, 1.0]
DEFAULT_N_COPIES = 5
DEFAULT_SEED = 42

# Generalized-GHZ branch for claim (xix): a in [1/sqrt(2), 1].
# tau_AB is exactly 0 throughout; tau_A(BC) sweeps 1 -> 0.
GHZ_BRANCH_GRID = [1.0 / math.sqrt(2.0), 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]

# GHZ/W interpolation angles (degrees) for the CKW sweep and
# the descriptive (xix) comparison.
INTERPOLATION_DEGREES = [0, 15, 30, 45, 60, 75, 90]

# Full generalized-GHZ grid for the CKW sweep (both branches).
GENERALIZED_GHZ_GRID = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

# ---------------------------------------------------------------------------
# Pre-registered thresholds (set from the pilot sweep, REPORT.md
# section 13, and never moved after the final measurement run).
# ---------------------------------------------------------------------------

# CKW margin tolerance: numerical zero. Any margin below
# -CKW_TOL is a defect in the code's concurrence, not a
# result about the theorem.
CKW_TOL = 1e-9

# Exact-value tolerance for the GHZ/W endpoints at sigma = 0.
EXACT_TOL = 1e-9

# Miss-fraction gates for claim (xviii): the GHZ regime's
# entanglement is (nearly) all residual, the W regime's is
# (nearly) all pairwise.
MISS_GHZ_MIN = 0.9
MISS_W_MAX = 0.1

# Claim (xix) gates on the generalized-GHZ branch: the pilot
# gives Pearson -0.9608, Spearman -1.0, max tau_AB exactly 0,
# D_A range 1/3. -0.95 and 0.25 are the round numbers below
# the pilot values.
D_TAU_PEARSON_MAX = -0.95
TAU_AB_FLAT_MAX = 1e-9
D_RANGE_MIN = 0.25


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("CKW_TOL", CKW_TOL),
        ("EXACT_TOL", EXACT_TOL),
        ("MISS_GHZ_MIN", MISS_GHZ_MIN),
        ("MISS_W_MAX", MISS_W_MAX),
        ("D_TAU_PEARSON_MAX", D_TAU_PEARSON_MAX),
        ("TAU_AB_FLAT_MAX", TAU_AB_FLAT_MAX),
        ("D_RANGE_MIN", D_RANGE_MIN),
    ) if value is None]
    if missing:
        raise ValueError(
            "monogamy thresholds are unset: run the pilot sweep "
            "and set " + ", ".join(missing) + " first "
            "(REPORT.md section 13)")
    return {
        "ckw_tol": float(CKW_TOL),
        "exact_tol": float(EXACT_TOL),
        "miss_ghz_min": float(MISS_GHZ_MIN),
        "miss_w_max": float(MISS_W_MAX),
        "d_tau_pearson_max": float(D_TAU_PEARSON_MAX),
        "tau_ab_flat_max": float(TAU_AB_FLAT_MAX),
        "d_range_min": float(D_RANGE_MIN),
    }


# ---------------------------------------------------------------------------
# Triad states (8-dim three-qubit pure states)
# ---------------------------------------------------------------------------

def ghz_triad():
    """GHZ-like triad: (|000> + |111>) / sqrt(2)."""
    psi = np.zeros(TRIAD_DIM, dtype=complex)
    psi[0] = 1.0 / math.sqrt(2.0)
    psi[7] = 1.0 / math.sqrt(2.0)
    return psi


def w_triad():
    """W-like triad: (|001> + |010> + |100>) / sqrt(3)."""
    psi = np.zeros(TRIAD_DIM, dtype=complex)
    for i in (1, 2, 4):
        psi[i] = 1.0 / math.sqrt(3.0)
    return psi


def generalized_ghz(a):
    """Generalized GHZ: a|000> + sqrt(1-a^2)|111>, a in [0, 1].

    Pairwise tangle is exactly 0 for every a; the one-to-rest
    tangle is 4 a^2 (1-a^2), maximal at a = 1/sqrt(2).
    """
    a = float(a)
    if not 0.0 <= a <= 1.0:
        raise ValueError("generalized-GHZ weight a must be in [0, 1]")
    psi = np.zeros(TRIAD_DIM, dtype=complex)
    psi[0] = a
    psi[7] = math.sqrt(1.0 - a * a)
    return psi


def ghz_w_interpolation(theta):
    """cos(theta)|GHZ> + sin(theta)|W>, theta in radians.

    theta = 0 is GHZ-like, theta = pi/2 is W-like. The two
    endpoint states have disjoint support, so they are
    orthogonal and the interpolation needs no renormalization.
    """
    return (math.cos(float(theta)) * ghz_triad()
            + math.sin(float(theta)) * w_triad())


def density_matrix(psi):
    """rho = |psi><psi| for an 8-dim triad state vector."""
    psi = np.asarray(psi, dtype=complex)
    if psi.shape != (TRIAD_DIM,):
        raise ValueError("a triad state is an 8-dim vector")
    return np.outer(psi, psi.conj())


# ---------------------------------------------------------------------------
# Partial trace (three qubits, einsum)
# ---------------------------------------------------------------------------

def partial_trace(rho, keep):
    """Reduced density matrix keeping the qubits in `keep`.

    rho is 8x8; keep is a tuple of qubit indices (0, 1, 2).
    The (2,2,2,2,2,2) tensor has row axes a,b,c and column
    axes A,B,C; a traced qubit sums the matching row and
    column letter, a kept qubit stays an output axis.
    """
    rho = np.asarray(rho, dtype=complex)
    if rho.shape != (TRIAD_DIM, TRIAD_DIM):
        raise ValueError("partial_trace needs an 8x8 triad density matrix")
    keep = tuple(int(q) for q in keep)
    if not keep or not set(keep) <= {0, 1, 2} or len(set(keep)) != len(keep):
        raise ValueError("keep must be a non-empty tuple of distinct "
                         "qubit indices in {0, 1, 2}")
    t = rho.reshape(2, 2, 2, 2, 2, 2)
    row = "abc"
    col = "ABC"
    expr_in = row + "".join(col[q] if q in keep else row[q]
                            for q in range(3))
    expr_out = "".join(row[q] for q in keep) + "".join(col[q] for q in keep)
    out = np.einsum(expr_in + "->" + expr_out, t)
    n = len(keep)
    return out.reshape(2 ** n, 2 ** n)


def reduced_single(rho, member):
    """A member's reduced 2x2 state (the other two traced out)."""
    return partial_trace(rho, (int(member),))


def reduced_pair(rho, i, j):
    """A pair's reduced 4x4 state (the third qubit traced out)."""
    return partial_trace(rho, (int(i), int(j)))


# ---------------------------------------------------------------------------
# Binary-thought embedding: member qubit -> thought space
# ---------------------------------------------------------------------------

# |0> -> |00> (attention, index 0), |1> -> |10> (self, index 2).
_EMBEDDING = np.zeros((4, 2), dtype=complex)
_EMBEDDING[0, 0] = 1.0
_EMBEDDING[2, 1] = 1.0


def embed_member_state(rho_member):
    """Embed a member's 2x2 reduced state in the 4-dim thought
    space: rho_embedded = M rho M-dagger."""
    rho_member = np.asarray(rho_member, dtype=complex)
    if rho_member.shape != (2, 2):
        raise ValueError("a member state is a 2x2 density matrix")
    return _EMBEDDING @ rho_member @ _EMBEDDING.conj().T


def member_self_knowing(rho, member):
    """D_A = Tr(P rho_A_embedded) for one member, using the
    EXISTING self-knowing projector (self_knowing.py)."""
    return sk.self_knowing_of_state(
        embed_member_state(reduced_single(rho, member)))


# ---------------------------------------------------------------------------
# Tangles
# ---------------------------------------------------------------------------

def pairwise_tangle(rho, i, j):
    """tau_ij = C^2, C the Wootters concurrence of the reduced
    two-qubit state (third qubit traced out)."""
    return float(te.concurrence(reduced_pair(rho, i, j)) ** 2)


def one_to_rest_tangle(rho, member):
    """tau_A(BC) = 4 det(rho_A), exact for pure states."""
    rho_a = reduced_single(rho, member)
    return float(4.0 * np.real(np.linalg.det(rho_a)))


def residual_tangle(rho, member):
    """Genuine-tripartite tangle for one member:
    tau_A(BC) - tau_AB - tau_AC."""
    others = [q for q in MEMBERS if q != int(member)]
    return float(one_to_rest_tangle(rho, member)
                 - pairwise_tangle(rho, member, others[0])
                 - pairwise_tangle(rho, member, others[1]))


def ckw_margin(rho, member):
    """tau_A(BC) - tau_AB - tau_AC: the CKW inequality's
    slack. >= 0 iff the theorem holds for this member.
    (Identical to residual_tangle; named for the claim.)"""
    return residual_tangle(rho, member)


def triad_analysis(psi):
    """Every tangle, residual, and D for one triad state.

    Per member: tau to the pair, tau to each other member,
    residual, D. Symmetric triads give the same numbers for
    all three members; they are still computed separately,
    so an asymmetry would show.
    """
    rho = density_matrix(psi)
    members = {}
    for m in MEMBERS:
        others = [q for q in MEMBERS if q != m]
        members[m] = {
            "tau_one_to_rest": one_to_rest_tangle(rho, m),
            "tau_pair": {
                (m, o): pairwise_tangle(rho, m, o) for o in others},
            "residual": residual_tangle(rho, m),
            "ckw_margin": ckw_margin(rho, m),
            "d_member": member_self_knowing(rho, m),
        }
    return {"members": members, "rho": rho}


def pairwise_miss_fraction(analysis, member=0):
    """Residual / tau_A(BC): the fraction of A's entanglement
    that pairwise concurrence misses. 1.0 for GHZ (all of it
    is tripartite), 0.0 for W (all of it is pairwise). None
    when tau_A(BC) is 0 (no entanglement to miss)."""
    m = analysis["members"][int(member)]
    tau = m["tau_one_to_rest"]
    if tau <= 0.0:
        return None
    return float(m["residual"] / tau)


# ---------------------------------------------------------------------------
# Noise: the unity.py model on the 8-dim triad vector
# ---------------------------------------------------------------------------

def noisy_triad_copies(psi, sigma, n_copies=DEFAULT_N_COPIES,
                       seed=DEFAULT_SEED):
    """Noisy copies of a triad: the unity.gaussian_copies model.

    The real 8-dim vector plus real Gaussian noise (std sigma),
    renormalized. The copies stay PURE (purity 1.0), so the
    4 det(rho_A) formula stays valid. Returned as complex
    vectors.
    """
    psi = np.asarray(psi, dtype=complex)
    if np.any(np.imag(psi) != 0.0):
        raise ValueError("noisy_triad_copies needs a real triad vector")
    copies = unity.gaussian_copies(np.real(psi), sigma, n_copies, seed)
    return [np.asarray(c, dtype=complex) for c in copies]


def triad_purity(psi):
    """Tr(rho^2) for a triad state vector: 1.0 iff pure."""
    rho = density_matrix(psi)
    return float(np.real(np.trace(rho @ rho)))


# ---------------------------------------------------------------------------
# Sweeps
# ---------------------------------------------------------------------------

def _sweep_states():
    """Every triad in the CKW sweep: exact GHZ, W, the two
    interpolation families."""
    states = [("ghz", ghz_triad()), ("w", w_triad())]
    for deg in INTERPOLATION_DEGREES[1:-1]:
        states.append((f"ghz_w_{deg}deg",
                       ghz_w_interpolation(math.radians(deg))))
    for a in GENERALIZED_GHZ_GRID:
        states.append((f"gen_ghz_a={a}", generalized_ghz(a)))
    return states


def ckw_sweep(sigmas=None, n_copies=DEFAULT_N_COPIES,
              seed=DEFAULT_SEED):
    """CKW margins for every triad, every sigma, every member.

    At sigma = 0 the exact states are measured (one copy each);
    at sigma > 0 the seeded noisy copies are measured. One row
    per (state, sigma) with the minimum margin across copies
    and members, plus the mean residual and mean pairwise sum
    for the GHZ/W miss comparison.
    """
    rows = []
    for name, psi in _sweep_states():
        for sigma in (SIGMA_GRID if sigmas is None else sigmas):
            copies = ([psi] if float(sigma) == 0.0
                      else noisy_triad_copies(psi, sigma, n_copies, seed))
            margins, residuals, pair_sums, purities = [], [], [], []
            for c in copies:
                analysis = triad_analysis(c)
                purities.append(triad_purity(c))
                for m in MEMBERS:
                    margins.append(analysis["members"][m]["ckw_margin"])
                    residuals.append(analysis["members"][m]["residual"])
                    pair_sums.append(sum(
                        analysis["members"][m]["tau_pair"].values()))
            rows.append({
                "state": name,
                "sigma": float(sigma),
                "n_copies": len(copies),
                "min_margin": float(np.min(margins)),
                "mean_margin": float(np.mean(margins)),
                "mean_residual": float(np.mean(residuals)),
                "mean_pairwise_sum": float(np.mean(pair_sums)),
                "min_purity": float(np.min(purities)),
            })
    return rows


def ghz_vs_w_noise(sigmas=None, n_copies=DEFAULT_N_COPIES,
                   seed=DEFAULT_SEED):
    """GHZ vs W under noise: mean tangles, residual, miss, D_A.

    One row per (state, sigma), member A. The miss fraction is
    residual / tau_A(BC): what pairwise concurrence misses.
    """
    rows = []
    for name, psi in (("ghz", ghz_triad()), ("w", w_triad())):
        for sigma in (SIGMA_GRID if sigmas is None else sigmas):
            copies = ([psi] if float(sigma) == 0.0
                      else noisy_triad_copies(psi, sigma, n_copies, seed))
            taus, pair_sums, residuals, ds = [], [], [], []
            for c in copies:
                analysis = triad_analysis(c)
                m = analysis["members"][0]
                taus.append(m["tau_one_to_rest"])
                pair_sums.append(sum(m["tau_pair"].values()))
                residuals.append(m["residual"])
                ds.append(m["d_member"])
            mean_tau = float(np.mean(taus))
            rows.append({
                "state": name,
                "sigma": float(sigma),
                "mean_tau_one_to_rest": mean_tau,
                "mean_pairwise_sum": float(np.mean(pair_sums)),
                "mean_residual": float(np.mean(residuals)),
                "mean_miss_fraction": (float(np.mean(residuals) / mean_tau)
                                      if mean_tau > 0.0 else None),
                "mean_d_member": float(np.mean(ds)),
            })
    return rows


def d_vs_tau_generalized_ghz(a_grid=None):
    """D_A vs tau_A(BC) on the generalized-GHZ branch.

    tau_AB is exactly 0 throughout (the branch's point), so
    any D_A movement with tau_A(BC) is entanglement with
    the PAIR, not with B. Returns the rows plus Pearson and
    Spearman correlations (self_knowing.py's exact ranks).
    """
    rows = []
    for a in (GHZ_BRANCH_GRID if a_grid is None else a_grid):
        psi = generalized_ghz(a)
        analysis = triad_analysis(psi)
        m = analysis["members"][0]
        rows.append({
            "a": float(a),
            "tau_one_to_rest": m["tau_one_to_rest"],
            "tau_ab": m["tau_pair"][(0, 1)],
            "tau_ac": m["tau_pair"][(0, 2)],
            "d_member": m["d_member"],
        })
    taus = [r["tau_one_to_rest"] for r in rows]
    ds = [r["d_member"] for r in rows]
    return {
        "rows": rows,
        "pearson_d_tau": sk.pearson(ds, taus),
        "spearman_d_tau": sk.spearman(ds, taus),
        "max_tau_ab": float(max(r["tau_ab"] for r in rows)),
        "d_range": float(max(ds) - min(ds)),
    }


def d_vs_tau_interpolation():
    """D_A vs tau_A(BC) across the GHZ/W interpolation.

    Descriptive, not gated: tau_AB rises to 4/9 along this
    family, so it confounds "entanglement with the pair"
    with "entanglement with B".
    """
    rows = []
    for deg in INTERPOLATION_DEGREES:
        psi = ghz_w_interpolation(math.radians(deg))
        analysis = triad_analysis(psi)
        m = analysis["members"][0]
        rows.append({
            "theta_deg": deg,
            "tau_one_to_rest": m["tau_one_to_rest"],
            "tau_ab": m["tau_pair"][(0, 1)],
            "d_member": m["d_member"],
        })
    taus = [r["tau_one_to_rest"] for r in rows]
    ds = [r["d_member"] for r in rows]
    return {
        "rows": rows,
        "pearson_d_tau": sk.pearson(ds, taus),
        "spearman_d_tau": sk.spearman(ds, taus),
    }


# ---------------------------------------------------------------------------
# Claims (xvii)-(xix): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_ckw_verdict(sigmas=None, n_copies=DEFAULT_N_COPIES,
                      seed=DEFAULT_SEED):
    """(xvii) CKW holds: tau_AB + tau_AC <= tau_A(BC) for
    EVERY triad and EVERY sigma.

    PASS iff the minimum CKW margin over the whole sweep
    (every state, every sigma, every member) is >= -CKW_TOL.
    A violation is a defect in the code's concurrence, not
    a result -- the theorem is established, the code is
    what is being tested.
    """
    t = _thresholds()
    rows = ckw_sweep(sigmas, n_copies, seed)
    min_margin = min(r["min_margin"] for r in rows)
    check = min_margin >= -t["ckw_tol"]
    worst = min(rows, key=lambda r: r["min_margin"])
    return {
        "claim": "(xvii) CKW monogamy holds in triads",
        "passed": bool(check),
        "checks": {
            "min_margin_at_least_minus_tol": bool(check),
        },
        "ckw_tol": t["ckw_tol"],
        "min_margin": float(min_margin),
        "worst_row": worst,
        "n_rows": len(rows),
        "rows": rows,
    }


def claim_ghz_vs_w_verdict():
    """(xviii) GHZ vs W: pairwise concurrence misses the
    GHZ entanglement and carries the W entanglement.

    PASS iff at sigma = 0 the GHZ-like triad has pairwise
    tangle <= EXACT_TOL and residual >= 1 - EXACT_TOL
    (miss fraction >= MISS_GHZ_MIN), while the W-like
    triad has pairwise tangle 4/9 each (within EXACT_TOL)
    and residual <= EXACT_TOL (miss fraction <=
    MISS_W_MAX). The noise rows are reported, not gated.
    """
    t = _thresholds()
    ghz = triad_analysis(ghz_triad())["members"][0]
    w = triad_analysis(w_triad())["members"][0]
    ghz_miss = pairwise_miss_fraction(triad_analysis(ghz_triad()), 0)
    w_miss = pairwise_miss_fraction(triad_analysis(w_triad()), 0)

    checks = {
        "ghz_pairwise_tangle_zero": all(
            v <= t["exact_tol"] for v in ghz["tau_pair"].values()),
        "ghz_residual_one": abs(ghz["residual"] - 1.0) <= t["exact_tol"],
        "ghz_tau_one_to_rest_one": abs(ghz["tau_one_to_rest"] - 1.0)
        <= t["exact_tol"],
        "ghz_d_two_thirds": abs(ghz["d_member"] - 2.0 / 3.0)
        <= t["exact_tol"],
        "ghz_miss_at_least_min": (ghz_miss is not None
                                  and ghz_miss >= t["miss_ghz_min"]),
        "w_pairwise_tangle_four_ninths": all(
            abs(v - 4.0 / 9.0) <= t["exact_tol"]
            for v in w["tau_pair"].values()),
        "w_residual_zero": abs(w["residual"]) <= t["exact_tol"],
        "w_tau_one_to_rest_eight_ninths": abs(
            w["tau_one_to_rest"] - 8.0 / 9.0) <= t["exact_tol"],
        "w_d_seven_ninths": abs(w["d_member"] - 7.0 / 9.0)
        <= t["exact_tol"],
        "w_miss_at_most_max": (w_miss is not None
                               and w_miss <= t["miss_w_max"]),
    }
    noise_rows = ghz_vs_w_noise()
    passed = bool(all(checks.values()))
    return {
        "claim": "(xviii) GHZ vs W: pairwise concurrence misses "
                 "tripartite entanglement",
        "passed": passed,
        "checks": checks,
        "ghz": {
            "tau_one_to_rest": ghz["tau_one_to_rest"],
            "tau_ab": ghz["tau_pair"][(0, 1)],
            "tau_ac": ghz["tau_pair"][(0, 2)],
            "residual": ghz["residual"],
            "d_member": ghz["d_member"],
            "miss_fraction": ghz_miss,
        },
        "w": {
            "tau_one_to_rest": w["tau_one_to_rest"],
            "tau_ab": w["tau_pair"][(0, 1)],
            "tau_ac": w["tau_pair"][(0, 2)],
            "residual": w["residual"],
            "d_member": w["d_member"],
            "miss_fraction": w_miss,
        },
        "noise_rows": noise_rows,
    }


def claim_d_vs_tau_verdict(a_grid=None):
    """(xix) D_A falls as tau_A(BC) rises even when tau_AB
    is flat.

    PASS iff, on the generalized-GHZ branch a in
    [1/sqrt(2), 1], Pearson(D_A, tau_A(BC)) <=
    D_TAU_PEARSON_MAX (-0.95; pilot -0.9608), max tau_AB
    <= TAU_AB_FLAT_MAX (1e-9; pilot exactly 0), and the
    D_A range >= D_RANGE_MIN (0.25; pilot 1/3). The GHZ/W
    interpolation and the GHZ noise sweep are reported
    alongside, not gated.
    """
    t = _thresholds()
    branch = d_vs_tau_generalized_ghz(a_grid)
    checks = {
        "pearson_at_most_max": (
            branch["pearson_d_tau"] <= t["d_tau_pearson_max"]),
        "tau_ab_flat": branch["max_tau_ab"] <= t["tau_ab_flat_max"],
        "d_range_at_least_min": (
            branch["d_range"] >= t["d_range_min"]),
    }
    interp = d_vs_tau_interpolation()
    ghz_noise = [r for r in ghz_vs_w_noise() if r["state"] == "ghz"]
    passed = bool(all(checks.values()))
    return {
        "claim": "(xix) D_A falls as tau_A(BC) rises with "
                 "tau_AB flat",
        "passed": passed,
        "checks": checks,
        "pearson_d_tau": branch["pearson_d_tau"],
        "spearman_d_tau": branch["spearman_d_tau"],
        "max_tau_ab": branch["max_tau_ab"],
        "d_range": branch["d_range"],
        "branch_rows": branch["rows"],
        "interpolation": interp,
        "ghz_noise_rows": ghz_noise,
    }


def monogamy_claims():
    """The three monogamy claims (xvii)-(xix), measured fresh."""
    claim_xvii = claim_ckw_verdict()
    claim_xviii = claim_ghz_vs_w_verdict()
    claim_xix = claim_d_vs_tau_verdict()
    verdicts = [claim_xvii, claim_xviii, claim_xix]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_xvii_ckw": claim_xvii,
        "claim_xviii_ghz_vs_w": claim_xviii,
        "claim_xix_d_vs_tau": claim_xix,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the CKW sweep, the GHZ/W comparison, the D-vs-tau
    branch, and the claims (xvii)-(xix) verdicts."""
    print("CKW monogamy in triads -- claims (xvii)-(xix)")
    print()
    verdicts = monogamy_claims()
    xvii = verdicts["claim_xvii_ckw"]
    print(f"CKW sweep: {xvii['n_rows']} (state, sigma) rows, "
          f"min margin = {xvii['min_margin']:.4f} "
          f"(worst: {xvii['worst_row']['state']} at "
          f"sigma = {xvii['worst_row']['sigma']})")
    print(f"claim (xvii) verdict: {'PASS' if xvii['passed'] else 'FAIL'}")
    print()
    xviii = verdicts["claim_xviii_ghz_vs_w"]
    g, w = xviii["ghz"], xviii["w"]
    print("sigma = 0 endpoints (member A):")
    print(f"  GHZ: tau_A(BC) = {g['tau_one_to_rest']:.4f}, "
          f"tau_AB = {g['tau_ab']:.4f}, tau_AC = {g['tau_ac']:.4f}, "
          f"residual = {g['residual']:.4f}, D_A = {g['d_member']:.4f}, "
          f"miss = {g['miss_fraction']:.4f}")
    print(f"  W:   tau_A(BC) = {w['tau_one_to_rest']:.4f}, "
          f"tau_AB = {w['tau_ab']:.4f}, tau_AC = {w['tau_ac']:.4f}, "
          f"residual = {w['residual']:.4f}, D_A = {w['d_member']:.4f}, "
          f"miss = {w['miss_fraction']:.4f}")
    print("noise (mean residual vs mean pairwise sum):")
    for r in xviii["noise_rows"]:
        miss = ("None" if r["mean_miss_fraction"] is None
                else f"{r['mean_miss_fraction']:.4f}")
        print(f"  {r['state']} sigma = {r['sigma']:>4}: "
              f"tau_A(BC) = {r['mean_tau_one_to_rest']:.4f}, "
              f"pairwise sum = {r['mean_pairwise_sum']:.4f}, "
              f"residual = {r['mean_residual']:.4f}, miss = {miss}, "
              f"D_A = {r['mean_d_member']:.4f}")
    print(f"claim (xviii) verdict: {'PASS' if xviii['passed'] else 'FAIL'}")
    print()
    xix = verdicts["claim_xix_d_vs_tau"]
    print("Generalized-GHZ branch (tau_AB = 0 throughout):")
    for r in xix["branch_rows"]:
        print(f"  a = {r['a']:.4f}: tau_A(BC) = "
              f"{r['tau_one_to_rest']:.4f}, D_A = {r['d_member']:.4f}")
    print(f"  Pearson(D_A, tau_A(BC)) = {xix['pearson_d_tau']:.4f}, "
          f"Spearman = {xix['spearman_d_tau']:.4f}, "
          f"max tau_AB = {xix['max_tau_ab']:.2e}, "
          f"D_A range = {xix['d_range']:.4f}")
    print(f"  interpolation Pearson = "
          f"{xix['interpolation']['pearson_d_tau']:.4f} (descriptive)")
    print("  GHZ noise sweep (descriptive): D_A and tau_A(BC) "
          "decay together; tau_AB stays small")
    for r in xix["ghz_noise_rows"]:
        print(f"    sigma = {r['sigma']:>4}: tau_A(BC) = "
              f"{r['mean_tau_one_to_rest']:.4f}, pairwise sum = "
              f"{r['mean_pairwise_sum']:.4f}, D_A = "
              f"{r['mean_d_member']:.4f}")
    print(f"claim (xix) verdict: {'PASS' if xix['passed'] else 'FAIL'}")
    print()
    print(f"claims (xvii)-(xix): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
