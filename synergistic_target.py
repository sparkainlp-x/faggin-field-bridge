# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Genuinely synergistic target: XOR-target PID of the collaboration gap (v0.20.0).

PID follow-up to v0.14.0 (claims (xl)-(xliii)). That build found
the Williams & Beer I_min decomposition arithmetically exact but
UNABLE to adjudicate "synergy, not redundancy" in its wiring:
with target Y = the joint outcome (X1, X2), Syn = Red - I(X1;X2)
and I(X1;X2) is 0.00-0.06 bits on every sigma/seed, so Syn is
numerically almost Red everywhere and claims (xli)-(xliii) FAIL.
The recorded discovery: a genuinely synergistic target (a
field-level outcome coupled to both agents) would be needed to
separate them. This module builds exactly that.

The target is the bitwise XOR of the two agents' 2-bit Born
outcomes: Y = X1 (+) X2 in {0, 1, 2, 3}. This is the textbook
synergistic target (Williams & Beer 2010; the XOR example in
the PID literature): with X1, X2 independent and uniform, each
source alone carries ZERO information about Y (I(X1;Y) =
I(X2;Y) = 0) while the pair jointly determines Y completely
(I(X1,X2;Y) = H(Y) = 2 bits) -- pure synergy, zero redundancy,
zero unique information. Any redundancy or unique information
in the measured decomposition therefore comes from the agents'
non-uniform marginals and from the pooled mixture, not from
the target's construction.

The construction (fixed in docs/preregistration-v0.20.0.md
before the evaluation run):

  - Sources X1, X2 are the two agents' Born outcomes (4
    concepts each); target Y = X1 (+) X2. The joint
    distribution is the EXACT pooled distribution from
    pid.pair_arm_distributions (design B, N = 2, 10
    generations): the same evolution as v0.14.0, reused,
    not reimplemented.
  - p(y) = sum over x1 (+) x2 = y of p(x1, x2).
    I(X1,X2;Y) = H(Y), because Y is a deterministic
    function of (X1, X2).
  - Redundancy is Williams & Beer I_min, the same measure
    as v0.14.0, so the comparison is apples to apples:
    Red = sum_y p(y) * min(I(X1; Y=y), I(X2; Y=y)),
    where the specific information I(Xi; Y=y) =
    D_KL(p(xi|y) || p(xi)), computed exactly from the
    joint. Uniq_i = I(Xi;Y) - Red, Syn =
    I(X1,X2;Y) - Red - Uniq1 - Uniq2.
  - I(X1;Y) and I(X2;Y) are computed EXACTLY from the
    joint (p(x1,y) = p(x1, x1 (+) y)). They are NOT
    computed as H(Y) - H(X2): that shortcut assumes the
    pooled joint is a product distribution, and it is
    not -- it is a MIXTURE of per-generation products,
    so X1 and X2 are correlated through the generation
    index and H(Y|X1) != H(X2). The first pilot pass
    used the shortcut and produced negative unique
    atoms (worst -0.6955 bits, seed 7); the exact
    computation restores all atoms to >= -0.0000 bits.
    This correction was made BEFORE any threshold was
    frozen and is disclosed in the preregistration.
  - The "gap" for the new target is dI =
    I_collab(X1,X2;Y) - I_isol(X1,X2;Y), with dSyn,
    dRed, dUniq defined the same way; the four arm
    differences sum to dI exactly.

Honesty, stated up front:
  - This is a SYNTHETIC, CLASSICAL emulation. It does
    not measure consciousness, synergy, or redundancy
    in a living system, and it does not test Faggin's
    Quantum Information Panpsychism. It imports IIT's
    DECOMPOSITION (Luppi et al.), not its contested
    Phi identity claim: no scalar Phi is computed here
    and none is presented as a consciousness measure
    (explicit do-not from the deep-think report,
    Cogitate 2025).
  - The XOR target separates synergy from redundancy
    at sigma = 0.25 (claim (lxv)), where the
    joint-outcome target could not. It does NOT make
    synergy track resonance: synergy rises with noise
    toward the 2-bit ceiling as the marginals
    uniformize, and it does not fall at sigma = 0.50
    (claim (lxvi) FAILS on calibration). The isolated
    arm is NOT synergy-free at high sigma: the pooled
    mixture over generations correlates the collapsed
    agents through the generation index, and that
    mixture-correlation is itself synergistic about
    the XOR (Syn_isol reaches 0.9610 / 0.6000 bits at
    sigma = 0.50, seeds 42 / 7).
  - The share dSyn / dI can exceed 1: on seed 42 at
    sigma = 0.25 it is 1.293, because dUniq is
    negative (-0.6420 bits -- the isolated arm carries
    0.7219 bits of UNIQUE information about Y that
    collaboration destroys). The atoms sum to dI
    exactly; a share above 1 is arithmetic, not an
    error.

Pre-registered verdict rules for claims (lxiv)-(lxvii),
written before the evaluation run (see the claim_*_
verdict functions and REPORT.md section 26).
Thresholds are round numbers set from the calibration
pilot on seeds 42 and 7 only and never moved after
the evaluation run.
"""

import math

import numpy as np

import bridge
import cost
import empathy_field as ef
import pid
import self_knowing as sk

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SIGMA_GRID = ef.SIGMA_GRID
DEFAULT_SEED = 42
DEFAULT_GENERATIONS = ef.DEFAULT_GENERATIONS
CALIBRATION_SEEDS = (42, 7)
EVALUATION_SEEDS = (1234, 2026)
ALL_SEEDS = CALIBRATION_SEEDS + EVALUATION_SEEDS
SIGMA_REF = 0.25
SIGMA_HIGH = 0.50
N_CONCEPTS = 4

# ---------------------------------------------------------------------------
# Pre-registered thresholds (set from the calibration pilot,
# docs/preregistration-v0.20.0.md, and never moved after
# the evaluation run).
# ---------------------------------------------------------------------------

# (lxiv) Identity tolerance: the atoms sum to I(X1,X2;Y)
# within this (floating-point scale); every atom is at
# least -ATOM_MIN_BITS. The calibration pilot's worst
# identity error is 2.22e-16 and its worst atom is
# -0.0000 bits.
XOR_PID_IDENTITY_TOL_BITS = 1e-9
XOR_PID_ATOM_MIN_BITS = -1e-9

# (lxiv) Cross-check: the exact H(Y) agrees with the
# sampled run_collaboration (N = 2, design B) H(Y),
# computed from the sampled joint counts via Y = X1 (+)
# X2, within this at sigma = 0.25. The round number
# used in (xl).
EXACT_SAMPLED_HY_TOL_BITS = 0.25

# (lxv) Synergy dominance: delta-synergy must exceed
# delta-redundancy and be at least this fraction of the
# information gap dI at sigma = 0.25. Calibration
# shares are 1.293 (seed 42) and 0.858 (seed 7);
# delta-synergy / delta-redundancy ratios are 4.60 and
# 7.17.
SYNERGY_SHARE_MIN = 0.5

# (lxvi) Synergy must rise with R: Pearson(synergy,
# mean R_post) across the sigma grid at least this.
# Calibration Pearsons are 0.3731 (seed 42) and 0.3424
# (seed 7).
SYNERGY_R_PEARSON_MIN = 0.5

# (lxvii) Redundancy share: the collaborating arm's
# redundancy is at most this fraction of its total
# information about Y, on every (seed, sigma) with
# I_collab > 0. Calibration worst shares are 0.192
# (seed 42, sigma = 0.10) and 0.236 (seed 7,
# sigma = 0.10).
REDUNDANCY_SHARE_MAX = 0.25


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("XOR_PID_IDENTITY_TOL_BITS", XOR_PID_IDENTITY_TOL_BITS),
        ("XOR_PID_ATOM_MIN_BITS", XOR_PID_ATOM_MIN_BITS),
        ("EXACT_SAMPLED_HY_TOL_BITS", EXACT_SAMPLED_HY_TOL_BITS),
        ("SYNERGY_SHARE_MIN", SYNERGY_SHARE_MIN),
        ("SYNERGY_R_PEARSON_MIN", SYNERGY_R_PEARSON_MIN),
        ("REDUNDANCY_SHARE_MAX", REDUNDANCY_SHARE_MAX),
    ) if value is None]
    if missing:
        raise ValueError(
            "synergistic_target thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.20.0.md)")
    return {
        "identity_tol_bits": float(XOR_PID_IDENTITY_TOL_BITS),
        "atom_min_bits": float(XOR_PID_ATOM_MIN_BITS),
        "exact_sampled_hy_tol_bits": float(EXACT_SAMPLED_HY_TOL_BITS),
        "synergy_share_min": float(SYNERGY_SHARE_MIN),
        "synergy_r_pearson_min": float(SYNERGY_R_PEARSON_MIN),
        "redundancy_share_max": float(REDUNDANCY_SHARE_MAX),
    }


# ---------------------------------------------------------------------------
# XOR-target PID of a joint distribution (Williams & Beer I_min)
# ---------------------------------------------------------------------------

def xor_target(y_value, x1, x2):
    """The synergistic target: Y = X1 (+) X2 (bitwise XOR)."""
    return int(x1) ^ int(x2)


def xor_pid_from_joint(joint):
    """Williams & Beer I_min PID of I(X1, X2; Y), Y = X1 (+) X2.

    joint is a 4x4 array p(x1, x2). Returns H(Y),
    I(X1,X2;Y) (= H(Y), since Y is a deterministic
    function of (X1, X2)), I(X1;Y), I(X2;Y), Red,
    Uniq1, Uniq2, Syn. The four atoms sum to
    I(X1,X2;Y) by construction (Syn is defined as the
    remainder), so the identity is a check on the
    arithmetic, not on a theorem.

    I(X1;Y) and I(X2;Y) are computed EXACTLY from the
    joint: p(x1, y) = p(x1, x1 (+) y). The shortcut
    I(X1;Y) = H(Y) - H(X2) is WRONG for a pooled
    mixture distribution (the pooled joint is a
    mixture of per-generation products, not a product),
    and it produced negative unique atoms in the first
    pilot pass.
    """
    joint = np.asarray(joint, dtype=float)
    if joint.shape != (N_CONCEPTS, N_CONCEPTS):
        raise ValueError("joint must be a 4x4 distribution")
    if np.any(joint < 0.0):
        raise ValueError("joint probabilities must be nonnegative")
    total = float(np.sum(joint))
    if total <= 0.0:
        raise ValueError("joint distribution sums to zero")
    joint = joint / total
    p1 = joint.sum(axis=1)
    p2 = joint.sum(axis=0)
    # p(y): y = x1 (+) x2.
    py = np.zeros(N_CONCEPTS)
    for a in range(N_CONCEPTS):
        for b in range(N_CONCEPTS):
            py[a ^ b] += joint[a, b]
    h_y = cost.shannon_entropy(py)
    # I(X1,X2;Y) = H(Y): Y is a deterministic function
    # of (X1, X2), so H(Y|X1,X2) = 0.
    total_info = h_y
    # I(Xi;Y) exactly from the joint.
    i1 = 0.0
    i2 = 0.0
    for a in range(N_CONCEPTS):
        for b in range(N_CONCEPTS):
            y = a ^ b
            pxy = joint[a, b]
            if pxy <= 0.0:
                continue
            if p1[a] > 0.0 and py[y] > 0.0:
                i1 += pxy * math.log2(pxy / (p1[a] * py[y]))
            if p2[b] > 0.0 and py[y] > 0.0:
                i2 += pxy * math.log2(pxy / (p2[b] * py[y]))
    # Specific informations I(Xi; Y=y) = D_KL(p(xi|y) || p(xi)).
    red = 0.0
    for y in range(N_CONCEPTS):
        if py[y] <= 0.0:
            continue
        cond1 = np.array([joint[a, a ^ y] / py[y]
                          for a in range(N_CONCEPTS)])
        cond2 = np.array([joint[b ^ y, b] / py[y]
                          for b in range(N_CONCEPTS)])
        s1 = sum(float(c) * math.log2(float(c) / float(p))
                 for c, p in zip(cond1, p1) if c > 0.0 and p > 0.0)
        s2 = sum(float(c) * math.log2(float(c) / float(p))
                 for c, p in zip(cond2, p2) if c > 0.0 and p > 0.0)
        red += float(py[y]) * min(s1, s2)
    uniq1 = i1 - red
    uniq2 = i2 - red
    syn = total_info - red - uniq1 - uniq2
    return {
        "h_y_bits": float(h_y),
        "total_info_bits": float(total_info),
        "i_x1_y_bits": float(i1),
        "i_x2_y_bits": float(i2),
        "redundant_bits": float(red),
        "unique1_bits": float(uniq1),
        "unique2_bits": float(uniq2),
        "synergistic_bits": float(syn),
        "atom_sum_bits": float(red + uniq1 + uniq2 + syn),
    }


def sampled_h_y(counts):
    """H(Y) (bits) of the XOR target from sampled joint counts.

    counts is a Counter over (x1, x2) concept tuples, as
    returned by empathy_field.run_collaboration. Y = x1 (+) x2.
    """
    total = float(sum(counts.values()))
    if total <= 0.0:
        raise ValueError("sampled counts are empty")
    py = np.zeros(N_CONCEPTS)
    for (a, b), c in counts.items():
        py[int(a) ^ int(b)] += float(c)
    return float(cost.shannon_entropy(py / total))


# ---------------------------------------------------------------------------
# Exact pooled XOR-target PID per (seed, sigma) (design-B evolution)
# ---------------------------------------------------------------------------

def xor_arm_distributions(sigma=SIGMA_REF,
                          generations=DEFAULT_GENERATIONS,
                          seed=DEFAULT_SEED, design="B"):
    """Exact pooled XOR-target PID for a 2-agent pair.

    Reuses pid.pair_arm_distributions for the exact
    pooled joint distributions and mean R_post, then
    decomposes I(X1,X2; Y = X1 (+) X2) in each arm by
    Williams & Beer I_min. Also returns the arm
    differences dI, dSyn, dRed, dUniq, which sum to dI
    exactly.
    """
    row = pid.pair_arm_distributions(
        sigma=sigma, generations=generations, seed=seed, design=design)
    for arm in ("collaborating", "isolated"):
        row[arm]["xor_pid"] = xor_pid_from_joint(row[arm]["joint"])
    collab = row["collaborating"]["xor_pid"]
    isol = row["isolated"]["xor_pid"]
    row["delta_total_info_bits"] = (
        collab["total_info_bits"] - isol["total_info_bits"])
    row["delta_synergistic_bits"] = (
        collab["synergistic_bits"] - isol["synergistic_bits"])
    row["delta_redundant_bits"] = (
        collab["redundant_bits"] - isol["redundant_bits"])
    row["delta_unique_bits"] = (
        (collab["unique1_bits"] + collab["unique2_bits"])
        - (isol["unique1_bits"] + isol["unique2_bits"]))
    return row


def xor_gap_vs_noise(sigmas=None, seeds=ALL_SEEDS,
                     generations=DEFAULT_GENERATIONS, design="B"):
    """The XOR-target PID gap decomposition per (seed, sigma)."""
    rows = []
    for seed in seeds:
        for sigma in (SIGMA_GRID if sigmas is None else sigmas):
            rows.append(xor_arm_distributions(
                sigma=sigma, generations=generations,
                seed=int(seed), design=design))
    return rows


# ---------------------------------------------------------------------------
# Claim verdicts (lxiv)-(lxvii)
# ---------------------------------------------------------------------------

def claim_xor_identity_verdict(seeds=ALL_SEEDS, sigmas=None,
                               generations=DEFAULT_GENERATIONS,
                               design="B", sweep=None):
    """(lxiv) XOR-target PID identity, canonical checks,
    sampled cross-check.

    PASS iff, for every seed, every sigma, and both arms:
    the four atoms sum to I(X1,X2;Y) within
    XOR_PID_IDENTITY_TOL_BITS and every atom is at least
    XOR_PID_ATOM_MIN_BITS; AND the canonical cases hold
    exactly (independent uniform -> Syn = 2, Red = 0,
    Uniq = 0; X1 = X2 uniform -> all atoms 0; X1
    deterministic, X2 uniform -> Uniq2 = 2, Syn = 0,
    Red = 0); AND at sigma = 0.25 the exact H(Y)
    agrees with the sampled run_collaboration (N = 2,
    design B) H(Y) within EXACT_SAMPLED_HY_TOL_BITS.
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else xor_gap_vs_noise(
        sigmas, seeds, generations, design))
    worst_identity = 0.0
    worst_atom = 0.0
    for row in rows:
        for arm in ("collaborating", "isolated"):
            xpid = row[arm]["xor_pid"]
            err = abs(xpid["atom_sum_bits"] - xpid["total_info_bits"])
            worst_identity = max(worst_identity, err)
            worst_atom = min(worst_atom, xpid["redundant_bits"],
                             xpid["unique1_bits"],
                             xpid["unique2_bits"],
                             xpid["synergistic_bits"])
    checks = {}
    checks["atoms_sum_to_total_info"] = (
        worst_identity <= t["identity_tol_bits"])
    checks["all_atoms_nonnegative"] = (
        worst_atom >= t["atom_min_bits"])
    canonical = {}
    # (a) X1, X2 independent uniform: pure synergy.
    p = xor_pid_from_joint(np.full((4, 4), 1.0 / 16.0))
    canonical["independent_uniform"] = {
        "synergistic_bits": p["synergistic_bits"],
        "redundant_bits": p["redundant_bits"],
        "unique1_bits": p["unique1_bits"],
        "unique2_bits": p["unique2_bits"],
        "total_info_bits": p["total_info_bits"],
    }
    checks["canonical_independent_uniform"] = bool(
        abs(p["synergistic_bits"] - 2.0) <= 1e-9
        and abs(p["redundant_bits"]) <= 1e-9
        and abs(p["unique1_bits"]) <= 1e-9
        and abs(p["unique2_bits"]) <= 1e-9)
    # (b) X1 = X2 uniform: Y = 0 always, no information.
    p = xor_pid_from_joint(np.diag(np.full(4, 0.25)))
    canonical["perfectly_correlated"] = {
        "synergistic_bits": p["synergistic_bits"],
        "redundant_bits": p["redundant_bits"],
        "unique1_bits": p["unique1_bits"],
        "unique2_bits": p["unique2_bits"],
        "total_info_bits": p["total_info_bits"],
    }
    checks["canonical_perfectly_correlated"] = bool(
        abs(p["total_info_bits"]) <= 1e-9
        and abs(p["synergistic_bits"]) <= 1e-9
        and abs(p["redundant_bits"]) <= 1e-9
        and abs(p["unique1_bits"]) <= 1e-9
        and abs(p["unique2_bits"]) <= 1e-9)
    # (c) X1 deterministic, X2 uniform: all unique to X2.
    joint = np.zeros((4, 4))
    joint[0, :] = 0.25
    p = xor_pid_from_joint(joint)
    canonical["one_source_deterministic"] = {
        "synergistic_bits": p["synergistic_bits"],
        "redundant_bits": p["redundant_bits"],
        "unique1_bits": p["unique1_bits"],
        "unique2_bits": p["unique2_bits"],
        "total_info_bits": p["total_info_bits"],
    }
    checks["canonical_one_source_deterministic"] = bool(
        abs(p["unique2_bits"] - 2.0) <= 1e-9
        and abs(p["synergistic_bits"]) <= 1e-9
        and abs(p["redundant_bits"]) <= 1e-9
        and abs(p["unique1_bits"]) <= 1e-9)
    cross = []
    worst_cross = 0.0
    for seed in seeds:
        exact = next(r for r in rows
                     if r["seed"] == int(seed)
                     and r["sigma"] == SIGMA_REF)
        sampled = ef.run_collaboration(
            n_agents=2, sigma=SIGMA_REF,
            generations=generations, seed=int(seed), design=design)
        d_collab = abs(
            exact["collaborating"]["xor_pid"]["h_y_bits"]
            - sampled_h_y(sampled["collaborating"]["counts"]))
        d_isol = abs(
            exact["isolated"]["xor_pid"]["h_y_bits"]
            - sampled_h_y(sampled["isolated"]["counts"]))
        worst_cross = max(worst_cross, d_collab, d_isol)
        cross.append({
            "seed": int(seed),
            "exact_h_y_collaborating_bits":
                exact["collaborating"]["xor_pid"]["h_y_bits"],
            "sampled_h_y_collaborating_bits": float(
                sampled_h_y(sampled["collaborating"]["counts"])),
            "exact_h_y_isolated_bits":
                exact["isolated"]["xor_pid"]["h_y_bits"],
            "sampled_h_y_isolated_bits": float(
                sampled_h_y(sampled["isolated"]["counts"])),
            "diff_collaborating_bits": float(d_collab),
            "diff_isolated_bits": float(d_isol),
        })
    checks["exact_matches_sampled_h_y"] = (
        worst_cross <= t["exact_sampled_hy_tol_bits"])
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxiv) XOR-target PID identity, canonical "
                 "checks, sampled cross-check",
        "passed": passed,
        "checks": checks,
        "worst_identity_error_bits": float(worst_identity),
        "worst_atom_bits": float(worst_atom),
        "worst_exact_sampled_h_y_diff_bits": float(worst_cross),
        "identity_tol_bits": t["identity_tol_bits"],
        "atom_min_bits": t["atom_min_bits"],
        "exact_sampled_h_y_tol_bits":
            t["exact_sampled_hy_tol_bits"],
        "canonical_cases": canonical,
        "cross_check_rows": cross,
    }


def claim_synergy_dominant_verdict(seeds=ALL_SEEDS,
                                   generations=DEFAULT_GENERATIONS,
                                   design="B", sweep=None):
    """(lxv) The information gap about the synergistic
    target IS synergy, not redundancy, at sigma = 0.25.

    PASS iff, on EVERY seed: delta-synergy exceeds
    delta-redundancy AND delta-synergy is at least
    SYNERGY_SHARE_MIN of the information gap dI at
    sigma = 0.25.
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else xor_gap_vs_noise(
        (SIGMA_REF,), seeds, generations, design))
    per_seed = []
    checks = {}
    for seed in seeds:
        row = next(r for r in rows
                   if r["seed"] == int(seed)
                   and r["sigma"] == SIGMA_REF)
        d_info = row["delta_total_info_bits"]
        d_syn = row["delta_synergistic_bits"]
        d_red = row["delta_redundant_bits"]
        share = d_syn / d_info if d_info != 0.0 else float("nan")
        per_seed.append({
            "seed": int(seed),
            "delta_total_info_bits": float(d_info),
            "delta_synergistic_bits": float(d_syn),
            "delta_redundant_bits": float(d_red),
            "delta_unique_bits": float(row["delta_unique_bits"]),
            "synergy_share_of_gap": float(share),
        })
        checks[f"seed_{seed}_synergy_exceeds_redundancy"] = bool(
            d_syn > d_red)
        checks[f"seed_{seed}_synergy_majority_of_gap"] = bool(
            share >= t["synergy_share_min"])
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxv) The information gap about the "
                 "synergistic target IS synergy, not "
                 "redundancy, at sigma = 0.25",
        "passed": passed,
        "checks": checks,
        "sigma": SIGMA_REF,
        "synergy_share_min": t["synergy_share_min"],
        "per_seed": per_seed,
    }


def claim_synergy_rises_falls_verdict(seeds=ALL_SEEDS, sigmas=None,
                                      generations=DEFAULT_GENERATIONS,
                                      design="B", sweep=None):
    """(lxvi) Synergy rises with R and falls at sigma = 0.50.

    PASS iff, on EVERY seed: Pearson(synergy_collab,
    mean R_post) across the sigma grid is at least
    SYNERGY_R_PEARSON_MIN AND synergy_collab at sigma =
    0.50 is below synergy_collab at sigma = 0.25.
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else xor_gap_vs_noise(
        sigmas, seeds, generations, design))
    per_seed = []
    checks = {}
    for seed in seeds:
        sub = [r for r in rows if r["seed"] == int(seed)]
        sub.sort(key=lambda r: r["sigma"])
        syns = [r["collaborating"]["xor_pid"]["synergistic_bits"]
                for r in sub]
        rs = [r["collaborating"]["mean_r_post"] for r in sub]
        pearson = sk.pearson(syns, rs)
        by_sigma = {r["sigma"]: r for r in sub}
        syn_025 = by_sigma[SIGMA_REF]["collaborating"]["xor_pid"][
            "synergistic_bits"]
        syn_050 = by_sigma[SIGMA_HIGH]["collaborating"]["xor_pid"][
            "synergistic_bits"]
        per_seed.append({
            "seed": int(seed),
            "pearson_synergy_r_post": float(pearson),
            "synergy_collab_sigma_0.25_bits": float(syn_025),
            "synergy_collab_sigma_0.50_bits": float(syn_050),
            "synergies_collab_bits": [float(s) for s in syns],
            "mean_r_post": [float(v) for v in rs],
        })
        checks[f"seed_{seed}_synergy_rises_with_r"] = bool(
            pearson >= t["synergy_r_pearson_min"])
        checks[f"seed_{seed}_synergy_falls_at_sigma_0.50"] = bool(
            syn_050 < syn_025)
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxvi) Synergy rises with R and falls at "
                 "sigma = 0.50",
        "passed": passed,
        "checks": checks,
        "synergy_r_pearson_min": t["synergy_r_pearson_min"],
        "per_seed": per_seed,
    }


def claim_redundancy_share_verdict(seeds=ALL_SEEDS, sigmas=None,
                                   generations=DEFAULT_GENERATIONS,
                                   design="B", sweep=None):
    """(lxvii) Redundancy stays a small share of the
    target information across the grid.

    PASS iff, on EVERY (seed, sigma) with I_collab > 0:
    Red_collab <= REDUNDANCY_SHARE_MAX *
    I_collab(X1,X2;Y).
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else xor_gap_vs_noise(
        sigmas, seeds, generations, design))
    per_seed = []
    checks = {}
    for seed in seeds:
        sub = [r for r in rows if r["seed"] == int(seed)]
        sub.sort(key=lambda r: r["sigma"])
        worst_share = 0.0
        worst_sigma = None
        shares = []
        for r in sub:
            xpid = r["collaborating"]["xor_pid"]
            total = xpid["total_info_bits"]
            share = (xpid["redundant_bits"] / total
                     if total > 0.0 else 0.0)
            shares.append(float(share))
            if share > worst_share:
                worst_share = share
                worst_sigma = r["sigma"]
        per_seed.append({
            "seed": int(seed),
            "worst_redundancy_share": float(worst_share),
            "worst_redundancy_share_sigma": worst_sigma,
            "redundancy_shares": shares,
        })
        checks[f"seed_{seed}_redundancy_share_small"] = bool(
            worst_share <= t["redundancy_share_max"])
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxvii) Redundancy stays a small share of "
                 "the target information across the grid",
        "passed": passed,
        "checks": checks,
        "redundancy_share_max": t["redundancy_share_max"],
        "per_seed": per_seed,
    }


def synergistic_target_claims():
    """The four XOR-target claims (lxiv)-(lxvii), measured fresh.

    One shared sweep over all seeds and sigmas feeds all
    four verdicts, so the evaluation run touches each
    held-out seed once.
    """
    sweep = xor_gap_vs_noise()
    claim_lxiv = claim_xor_identity_verdict(sweep=sweep)
    claim_lxv = claim_synergy_dominant_verdict(sweep=sweep)
    claim_lxvi = claim_synergy_rises_falls_verdict(sweep=sweep)
    claim_lxvii = claim_redundancy_share_verdict(sweep=sweep)
    verdicts = [claim_lxiv, claim_lxv, claim_lxvi, claim_lxvii]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_lxiv_xor_identity": claim_lxiv,
        "claim_lxv_synergy_dominant": claim_lxv,
        "claim_lxvi_synergy_rises_falls": claim_lxvi,
        "claim_lxvii_redundancy_share": claim_lxvii,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the XOR-target PID decomposition and the claims
    (lxiv)-(lxvii) verdicts."""
    print("Genuinely synergistic target (XOR) -- claims "
          "(lxiv)-(lxvii)")
    print()
    verdicts = synergistic_target_claims()
    lxiv = verdicts["claim_lxiv_xor_identity"]
    print(f"worst identity error: {lxiv['worst_identity_error_bits']:.2e} "
          f"bits (tol {lxiv['identity_tol_bits']:.0e}); worst atom: "
          f"{lxiv['worst_atom_bits']:.4f} bits")
    print(f"worst exact-vs-sampled H(Y) diff at sigma = 0.25: "
          f"{lxiv['worst_exact_sampled_h_y_diff_bits']:.4f} bits "
          f"(tol {lxiv['exact_sampled_h_y_tol_bits']:.2f})")
    print(f"claim (lxiv) verdict: {'PASS' if lxiv['passed'] else 'FAIL'}")
    print()
    lxv = verdicts["claim_lxv_synergy_dominant"]
    for r in lxv["per_seed"]:
        print(f"seed {r['seed']}: dI = {r['delta_total_info_bits']:+.4f}, "
              f"dSyn = {r['delta_synergistic_bits']:+.4f}, "
              f"dRed = {r['delta_redundant_bits']:+.4f}, "
              f"dUniq = {r['delta_unique_bits']:+.4f}, "
              f"synergy share = {r['synergy_share_of_gap']:.3f}")
    print(f"claim (lxv) verdict: {'PASS' if lxv['passed'] else 'FAIL'}")
    print()
    lxvi = verdicts["claim_lxvi_synergy_rises_falls"]
    for r in lxvi["per_seed"]:
        print(f"seed {r['seed']}: Pearson(Syn, R_post) = "
              f"{r['pearson_synergy_r_post']:+.4f}, Syn(0.25) = "
              f"{r['synergy_collab_sigma_0.25_bits']:.4f}, Syn(0.50) = "
              f"{r['synergy_collab_sigma_0.50_bits']:.4f}")
    print(f"claim (lxvi) verdict: "
          f"{'PASS' if lxvi['passed'] else 'FAIL'}")
    print()
    lxvii = verdicts["claim_lxvii_redundancy_share"]
    for r in lxvii["per_seed"]:
        print(f"seed {r['seed']}: worst Red_c/I_c = "
              f"{r['worst_redundancy_share']:.4f} at sigma = "
              f"{r['worst_redundancy_share_sigma']} "
              f"(bar {lxvii['redundancy_share_max']:.2f})")
    print(f"claim (lxvii) verdict: "
          f"{'PASS' if lxvii['passed'] else 'FAIL'}")
    print()
    print(f"claims (lxiv)-(lxvii): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
