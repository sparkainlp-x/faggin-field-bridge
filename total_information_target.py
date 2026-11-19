# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""A target for which collaboration reliably raises total information (v0.21.0).

Follow-up to v0.20.0 (claims (lxiv)-(lxvii)). The XOR
target separated synergy from redundancy (delta-synergy
exceeds delta-redundancy on all four seeds at sigma =
0.25) but the "gap is synergy" framing broke: on
held-out seed 1234 collaboration did NOT raise total
information about the XOR target at all (delta-I =
-0.2591, I_isol 1.7610 > I_collab 1.5019), so a
share-of-gap criterion was meaningless there. This
module asks whether ANY target exists for which
collaboration reliably raises total information
(delta-I > 0 on every seed) while keeping the PID
separable.

The method is a candidate search on CALIBRATION seeds
only (42 and 7), over deterministic targets Y =
f(X1, X2) of the two agents' 2-bit Born outcomes,
decomposed by the same Williams & Beer I_min PID on
the same exact pooled distributions
(pid.pair_arm_distributions, design B, N = 2, 10
generations), with I(Xi;Y) computed exactly from the
joint (the v0.20.0 pitfall: never the H(Y) - H(Xj)
product shortcut, which produced negative unique
atoms on the pooled mixture). Fourteen targets were
screened; the selection rule and its two exclusions
are disclosed in docs/preregistration-v0.21.0.md
before the evaluation run: the incumbents xor and
joint are references (already measured on all four
seeds), and the Latin-square / group-difference
targets sum_mod4 and diff_mod4 are near-duplicates
of the incumbent BY CONSTRUCTION (fixing one source
permutes Y; their H(Y) is driven by the same
difference distribution whose mixture-correlation
uniformization is the diagnosed XOR failure
mechanism, and they track XOR to within 0.004 bits
on calibration). Among the remaining new targets,
eligible by the gates (delta-I > 0, delta-Syn >
delta-Red with |delta-Syn - delta-Red| >= 0.10,
Red_c / I_c <= 0.50 on both calibration seeds),
max min-seed delta-I at sigma = 0.25 picks MAX, Y =
max(X1, X2) (+1.8927 / +1.0707). OR, the other
agreement-family target, tracks MAX within 0.03
bits at sigma = 0.25 and is the reported sensitivity
check. AND and MIN fail the gates (delta-I <= 0 on
at least one calibration seed); x1 fails separability
(delta-Syn = 0 exactly); eq / parity / lowbit_xor
pass with small min delta-I (<= +0.2616);
lowbits_pair fails the separation gate on seed 42.

MAX is an agreement-family target: when
collaboration makes the agents similar, Y follows
the shared concept, and H(Y) is driven by the
spread of the shared marginal, not by a difference
distribution. It is NOT a pure-synergy target: with
independent uniform sources a single source alone
carries 0.6712 bits about the max (I = 1.7490, Syn
= 1.0778, Red = 0.6712), and with X1 = X2 uniform
the decomposition is all redundant (Red = 2.0).

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
  - The isolated arm DEGENERATES at low sigma: I_isol
    = 0 exactly at sigma <= 0.25 on seed 42 and sigma
    <= 0.10 on seed 7 -- the design-B lock-in (a
    collapsed agent stays near its collapsed concept
    under small kicks, so max is a point mass). The
    large delta-I at low sigma is driven as much by
    the isolated arm collapsing to a point as by
    collaboration raising information. On seed 7 at
    sigma = 0.25 the isolated arm is NOT degenerate
    (I_isol = 0.8813).
  - The synergy share at sigma = 0.25 is tight on
    seed 42: 0.5431 against the 0.5 bar (seed 7:
    0.9635). Claim (lxx) is calibrated to pass, but
    only just on one seed.
  - Redundancy is a much larger share for MAX than
    for XOR (calibration worst 0.3837 vs 0.2357);
    the (lxxi) bar 0.50 is looser than the XOR bar
    0.25 for exactly that reason -- MAX's
    independent-uniform canonical case already
    carries Red / I = 0.3837.
  - The grid-wide delta-I is positive everywhere on
    calibration but falls steeply past sigma = 0.25
    (seed 42: 1.8927 -> 0.8261 -> 0.4338) and its
    minimum is 0.2337 (seed 7, sigma = 1.00).

Pre-registered verdict rules for claims
(lxviii)-(lxxii), written before the evaluation run
(see the claim_*_verdict functions and REPORT.md
section 27). Thresholds are round numbers set from
the calibration pilot on seeds 42 and 7 only and
never moved after the evaluation run.
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
N_CONCEPTS = 4
CHOSEN_TARGET = "max"

# ---------------------------------------------------------------------------
# Pre-registered thresholds (set from the calibration pilot,
# docs/preregistration-v0.21.0.md, and never moved after
# the evaluation run).
# ---------------------------------------------------------------------------

# (lxviii) Identity tolerance: the atoms sum to
# I(X1,X2;Y) within this (floating-point scale); every
# atom is at least -ATOM_MIN_BITS. Canonical values
# are checked within CANONICAL_TOL_BITS (the
# independent-uniform MAX values are irrational).
MAX_PID_IDENTITY_TOL_BITS = 1e-9
MAX_PID_ATOM_MIN_BITS = -1e-9
MAX_PID_CANONICAL_TOL_BITS = 1e-3

# (lxviii) Cross-check: the exact H(Y) agrees with the
# sampled run_collaboration (N = 2, design B) H(Y),
# computed from the sampled joint counts via Y =
# max(X1, X2), within this at sigma = 0.25. The round
# number used in (xl) and (lxiv). Calibration worst
# diff is 0.0087 bits.
EXACT_SAMPLED_HY_TOL_BITS = 0.25

# (lxx) Synergy dominance: delta-synergy must exceed
# delta-redundancy and be at least this fraction of
# the information gap dI at sigma = 0.25.
# Calibration shares are 0.5431 (seed 42) and 0.9635
# (seed 7) -- tight on seed 42.
SYNERGY_SHARE_MIN = 0.5

# (lxxi) Redundancy share: the collaborating arm's
# redundancy is at most this fraction of its total
# information about Y, on every (seed, sigma) with
# I_collab > 0. Calibration worst share is 0.3837
# (seed 42, sigma = 0.00; seed 7 the same).
REDUNDANCY_SHARE_MAX = 0.50


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("MAX_PID_IDENTITY_TOL_BITS", MAX_PID_IDENTITY_TOL_BITS),
        ("MAX_PID_ATOM_MIN_BITS", MAX_PID_ATOM_MIN_BITS),
        ("MAX_PID_CANONICAL_TOL_BITS", MAX_PID_CANONICAL_TOL_BITS),
        ("EXACT_SAMPLED_HY_TOL_BITS", EXACT_SAMPLED_HY_TOL_BITS),
        ("SYNERGY_SHARE_MIN", SYNERGY_SHARE_MIN),
        ("REDUNDANCY_SHARE_MAX", REDUNDANCY_SHARE_MAX),
    ) if value is None]
    if missing:
        raise ValueError(
            "total_information_target thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.21.0.md)")
    return {
        "identity_tol_bits": float(MAX_PID_IDENTITY_TOL_BITS),
        "atom_min_bits": float(MAX_PID_ATOM_MIN_BITS),
        "canonical_tol_bits": float(MAX_PID_CANONICAL_TOL_BITS),
        "exact_sampled_hy_tol_bits": float(EXACT_SAMPLED_HY_TOL_BITS),
        "synergy_share_min": float(SYNERGY_SHARE_MIN),
        "redundancy_share_max": float(REDUNDANCY_SHARE_MAX),
    }


# ---------------------------------------------------------------------------
# Candidate targets: deterministic functions Y = f(X1, X2)
# ---------------------------------------------------------------------------

def _xor(a, b):
    return int(a) ^ int(b)


def _and(a, b):
    return int(a) & int(b)


def _or(a, b):
    return int(a) | int(b)


def _sum_mod4(a, b):
    return (int(a) + int(b)) % 4


def _diff_mod4(a, b):
    return (int(a) - int(b)) % 4


def _sum_int(a, b):
    return int(a) + int(b)


def _min(a, b):
    return min(int(a), int(b))


def _max(a, b):
    return max(int(a), int(b))


def _eq(a, b):
    return 1 if int(a) == int(b) else 0


def _parity(a, b):
    return (int(a) + int(b)) % 2


def _lowbit_xor(a, b):
    return (int(a) & 1) ^ (int(b) & 1)


def _lowbits_pair(a, b):
    return 2 * (int(a) & 1) + (int(b) & 1)


def _x1(a, b):
    return int(a)


def _joint(a, b):
    return 4 * int(a) + int(b)


# name -> (function, number of distinct Y values). xor and
# joint are REFERENCES (v0.20.0 / v0.14.0, already measured
# on all four seeds), not selection candidates; sum_mod4
# and diff_mod4 are Latin-square / group-difference
# near-duplicates of the incumbent XOR, excluded from
# selection for the reason in the preregistration.
TARGET_FUNCTIONS = {
    "xor": (_xor, 4),
    "and": (_and, 4),
    "or": (_or, 4),
    "sum_mod4": (_sum_mod4, 4),
    "diff_mod4": (_diff_mod4, 4),
    "sum_int": (_sum_int, 7),
    "min": (_min, 4),
    "max": (_max, 4),
    "eq": (_eq, 2),
    "parity": (_parity, 2),
    "lowbit_xor": (_lowbit_xor, 2),
    "lowbits_pair": (_lowbits_pair, 4),
    "x1": (_x1, 4),
    "joint": (_joint, 16),
}

# Targets excluded from selection: the incumbents
# (already measured on all four seeds) and the
# Latin-square difference targets (near-duplicates of
# the incumbent by construction).
REFERENCE_TARGETS = ("xor", "joint")
INCUMBENT_FAMILY_TARGETS = ("sum_mod4", "diff_mod4")

# Eligibility gates for the selection (calibration
# seeds, sigma = 0.25): delta-I > 0, delta-Syn >
# delta-Red with |delta-Syn - delta-Red| >= this,
# Red_c / I_c <= 0.50.
SELECTION_SEPARATION_MIN_BITS = 0.10
SELECTION_REDUNDANCY_SHARE_MAX = 0.50


def target_pid_from_joint(joint, target_fn, n_out):
    """Williams & Beer I_min PID of I(X1, X2; Y), Y = f(X1, X2).

    joint is a 4x4 array p(x1, x2); target_fn maps
    (x1, x2) to a Y value in {0, ..., n_out - 1}.
    Returns H(Y), I(X1,X2;Y) (= H(Y), since Y is a
    deterministic function of (X1, X2)), I(X1;Y),
    I(X2;Y), Red, Uniq1, Uniq2, Syn. The four atoms
    sum to I(X1,X2;Y) by construction (Syn is defined
    as the remainder), so the identity is a check on
    the arithmetic, not on a theorem.

    I(X1;Y) and I(X2;Y) are computed EXACTLY from the
    joint: p(x1, y) = sum over x2 with f(x1, x2) = y
    of p(x1, x2). The shortcut I(X1;Y) = H(Y) -
    H(X2) is WRONG for a pooled mixture distribution
    (the pooled joint is a mixture of per-generation
    products, not a product) -- see v0.20.0, where it
    produced negative unique atoms.
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
    fmap = np.zeros((N_CONCEPTS, N_CONCEPTS), dtype=int)
    for a in range(N_CONCEPTS):
        for b in range(N_CONCEPTS):
            y = int(target_fn(a, b))
            if y < 0 or y >= int(n_out):
                raise ValueError("target function value out of range")
            fmap[a, b] = y
    py = np.zeros(int(n_out))
    for a in range(N_CONCEPTS):
        for b in range(N_CONCEPTS):
            py[fmap[a, b]] += joint[a, b]
    h_y = cost.shannon_entropy(py)
    # I(X1,X2;Y) = H(Y): Y is a deterministic function
    # of (X1, X2), so H(Y|X1,X2) = 0.
    total_info = h_y
    # I(Xi;Y) exactly from the joint.
    pxy1 = np.zeros((N_CONCEPTS, int(n_out)))
    pxy2 = np.zeros((N_CONCEPTS, int(n_out)))
    for a in range(N_CONCEPTS):
        for b in range(N_CONCEPTS):
            y = fmap[a, b]
            pxy1[a, y] += joint[a, b]
            pxy2[b, y] += joint[a, b]
    i1 = 0.0
    i2 = 0.0
    for a in range(N_CONCEPTS):
        for y in range(int(n_out)):
            if pxy1[a, y] > 0.0 and p1[a] > 0.0 and py[y] > 0.0:
                i1 += pxy1[a, y] * math.log2(
                    pxy1[a, y] / (p1[a] * py[y]))
    for b in range(N_CONCEPTS):
        for y in range(int(n_out)):
            if pxy2[b, y] > 0.0 and p2[b] > 0.0 and py[y] > 0.0:
                i2 += pxy2[b, y] * math.log2(
                    pxy2[b, y] / (p2[b] * py[y]))
    # Specific informations I(Xi; Y=y) = D_KL(p(xi|y) || p(xi)).
    red = 0.0
    for y in range(int(n_out)):
        if py[y] <= 0.0:
            continue
        cond1 = np.array([pxy1[a, y] / py[y]
                          for a in range(N_CONCEPTS)])
        cond2 = np.array([pxy2[b, y] / py[y]
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


def max_pid_from_joint(joint):
    """Williams & Beer I_min PID of I(X1, X2; Y), Y = max(X1, X2)."""
    return target_pid_from_joint(joint, _max, 4)


def sampled_h_y_max(counts):
    """H(Y) (bits) of the MAX target from sampled joint counts.

    counts is a Counter over (x1, x2) concept tuples, as
    returned by empathy_field.run_collaboration. Y = max(x1, x2).
    """
    total = float(sum(counts.values()))
    if total <= 0.0:
        raise ValueError("sampled counts are empty")
    py = np.zeros(N_CONCEPTS)
    for (a, b), c in counts.items():
        py[max(int(a), int(b))] += float(c)
    return float(cost.shannon_entropy(py / total))


# ---------------------------------------------------------------------------
# Candidate screen (calibration seeds only, by design)
# ---------------------------------------------------------------------------

def screen_candidates(seeds=CALIBRATION_SEEDS, sigma=SIGMA_REF,
                      generations=DEFAULT_GENERATIONS, design="B"):
    """The v0.21.0 candidate screen, reproducible in code.

    For each target in TARGET_FUNCTIONS: per-seed
    delta-I, delta-Syn, delta-Red, delta-Uniq and the
    collaborating arm's redundancy share at the
    reference sigma, on the given (calibration) seeds
    only. Eligibility is the preregistered gates;
    selection among the eligible non-excluded targets
    is max min-seed delta-I. Reference targets and
    incumbent-family targets are reported but never
    selected.
    """
    rows = []
    for name, (fn, n_out) in TARGET_FUNCTIONS.items():
        per_seed = []
        for seed in seeds:
            row = pid.pair_arm_distributions(
                sigma=sigma, generations=generations,
                seed=int(seed), design=design)
            c = target_pid_from_joint(
                row["collaborating"]["joint"], fn, n_out)
            i = target_pid_from_joint(
                row["isolated"]["joint"], fn, n_out)
            d_info = c["total_info_bits"] - i["total_info_bits"]
            d_syn = (c["synergistic_bits"]
                     - i["synergistic_bits"])
            d_red = (c["redundant_bits"] - i["redundant_bits"])
            per_seed.append({
                "seed": int(seed),
                "delta_total_info_bits": float(d_info),
                "delta_synergistic_bits": float(d_syn),
                "delta_redundant_bits": float(d_red),
                "delta_unique_bits": float(
                    (c["unique1_bits"] + c["unique2_bits"])
                    - (i["unique1_bits"] + i["unique2_bits"])),
                "redundancy_share_collaborating": float(
                    c["redundant_bits"] / c["total_info_bits"]
                    if c["total_info_bits"] > 0.0 else 0.0),
            })
        min_d_info = min(r["delta_total_info_bits"] for r in per_seed)
        eligible = all(
            r["delta_total_info_bits"] > 0.0
            and r["delta_synergistic_bits"]
            > r["delta_redundant_bits"]
            and abs(r["delta_synergistic_bits"]
                    - r["delta_redundant_bits"])
            >= SELECTION_SEPARATION_MIN_BITS
            and r["redundancy_share_collaborating"]
            <= SELECTION_REDUNDANCY_SHARE_MAX
            for r in per_seed)
        excluded = (name in REFERENCE_TARGETS
                    or name in INCUMBENT_FAMILY_TARGETS)
        rows.append({
            "target": name,
            "n_outcomes": int(n_out),
            "per_seed": per_seed,
            "min_delta_total_info_bits": float(min_d_info),
            "eligible": bool(eligible),
            "excluded_from_selection": bool(excluded),
        })
    selectable = [r for r in rows
                  if r["eligible"] and not r["excluded_from_selection"]]
    if selectable:
        best = max(selectable,
                   key=lambda r: r["min_delta_total_info_bits"])
        selected = best["target"]
    else:
        selected = None
    return {
        "sigma": float(sigma),
        "seeds": [int(s) for s in seeds],
        "candidates": rows,
        "selected_target": selected,
    }


# ---------------------------------------------------------------------------
# Exact pooled MAX-target PID per (seed, sigma) (design-B evolution)
# ---------------------------------------------------------------------------

def max_arm_distributions(sigma=SIGMA_REF,
                          generations=DEFAULT_GENERATIONS,
                          seed=DEFAULT_SEED, design="B"):
    """Exact pooled MAX-target PID for a 2-agent pair.

    Reuses pid.pair_arm_distributions for the exact
    pooled joint distributions, then decomposes
    I(X1,X2; Y = max(X1, X2)) in each arm by Williams
    & Beer I_min. Also returns the arm differences
    dI, dSyn, dRed, dUniq, which sum to dI exactly.
    """
    row = pid.pair_arm_distributions(
        sigma=sigma, generations=generations, seed=seed, design=design)
    for arm in ("collaborating", "isolated"):
        row[arm]["max_pid"] = max_pid_from_joint(row[arm]["joint"])
    collab = row["collaborating"]["max_pid"]
    isol = row["isolated"]["max_pid"]
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


def max_gap_vs_noise(sigmas=None, seeds=ALL_SEEDS,
                     generations=DEFAULT_GENERATIONS, design="B"):
    """The MAX-target PID gap decomposition per (seed, sigma)."""
    rows = []
    for seed in seeds:
        for sigma in (SIGMA_GRID if sigmas is None else sigmas):
            rows.append(max_arm_distributions(
                sigma=sigma, generations=generations,
                seed=int(seed), design=design))
    return rows


# ---------------------------------------------------------------------------
# Claim verdicts (lxviii)-(lxxii)
# ---------------------------------------------------------------------------

def claim_max_identity_verdict(seeds=ALL_SEEDS, sigmas=None,
                               generations=DEFAULT_GENERATIONS,
                               design="B", sweep=None):
    """(lxviii) MAX-target PID identity, canonical checks,
    sampled cross-check.

    PASS iff, for every seed, every sigma, and both arms:
    the four atoms sum to I(X1,X2;Y) within
    MAX_PID_IDENTITY_TOL_BITS and every atom is at least
    MAX_PID_ATOM_MIN_BITS; AND the canonical cases hold
    (independent uniform -> I = 1.7490, Syn = 1.0778,
    Red = 0.6712, Uniq = 0; X1 = X2 uniform -> I = 2,
    Syn = 0, Red = 2, Uniq = 0; X1 deterministic, X2
    uniform -> Uniq2 = 2, Syn = 0, Red = 0; X2
    deterministic, X1 uniform -> Uniq1 = 2, Syn = 0,
    Red = 0); AND at sigma = 0.25 the exact H(Y)
    agrees with the sampled run_collaboration (N = 2,
    design B) H(Y) within EXACT_SAMPLED_HY_TOL_BITS.
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else max_gap_vs_noise(
        sigmas, seeds, generations, design))
    worst_identity = 0.0
    worst_atom = 0.0
    for row in rows:
        for arm in ("collaborating", "isolated"):
            xpid = row[arm]["max_pid"]
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
    # (a) X1, X2 independent uniform.
    p = max_pid_from_joint(np.full((4, 4), 1.0 / 16.0))
    canonical["independent_uniform"] = {
        "synergistic_bits": p["synergistic_bits"],
        "redundant_bits": p["redundant_bits"],
        "unique1_bits": p["unique1_bits"],
        "unique2_bits": p["unique2_bits"],
        "total_info_bits": p["total_info_bits"],
    }
    checks["canonical_independent_uniform"] = bool(
        abs(p["total_info_bits"] - 1.7489992230622806)
        <= t["canonical_tol_bits"]
        and abs(p["synergistic_bits"] - 1.0778195311147831)
        <= t["canonical_tol_bits"]
        and abs(p["redundant_bits"] - 0.6711796919474974)
        <= t["canonical_tol_bits"]
        and abs(p["unique1_bits"]) <= t["canonical_tol_bits"]
        and abs(p["unique2_bits"]) <= t["canonical_tol_bits"])
    # (b) X1 = X2 uniform: Y = X1 = X2, all redundant.
    p = max_pid_from_joint(np.diag(np.full(4, 0.25)))
    canonical["perfectly_correlated"] = {
        "synergistic_bits": p["synergistic_bits"],
        "redundant_bits": p["redundant_bits"],
        "unique1_bits": p["unique1_bits"],
        "unique2_bits": p["unique2_bits"],
        "total_info_bits": p["total_info_bits"],
    }
    checks["canonical_perfectly_correlated"] = bool(
        abs(p["total_info_bits"] - 2.0) <= 1e-9
        and abs(p["synergistic_bits"]) <= 1e-9
        and abs(p["redundant_bits"] - 2.0) <= 1e-9
        and abs(p["unique1_bits"]) <= 1e-9
        and abs(p["unique2_bits"]) <= 1e-9)
    # (c) X1 deterministic, X2 uniform: all unique to X2.
    joint = np.zeros((4, 4))
    joint[0, :] = 0.25
    p = max_pid_from_joint(joint)
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
    # (d) X2 deterministic, X1 uniform: all unique to X1.
    joint = np.zeros((4, 4))
    joint[:, 0] = 0.25
    p = max_pid_from_joint(joint)
    canonical["other_source_deterministic"] = {
        "synergistic_bits": p["synergistic_bits"],
        "redundant_bits": p["redundant_bits"],
        "unique1_bits": p["unique1_bits"],
        "unique2_bits": p["unique2_bits"],
        "total_info_bits": p["total_info_bits"],
    }
    checks["canonical_other_source_deterministic"] = bool(
        abs(p["unique1_bits"] - 2.0) <= 1e-9
        and abs(p["synergistic_bits"]) <= 1e-9
        and abs(p["redundant_bits"]) <= 1e-9
        and abs(p["unique2_bits"]) <= 1e-9)
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
            exact["collaborating"]["max_pid"]["h_y_bits"]
            - sampled_h_y_max(sampled["collaborating"]["counts"]))
        d_isol = abs(
            exact["isolated"]["max_pid"]["h_y_bits"]
            - sampled_h_y_max(sampled["isolated"]["counts"]))
        worst_cross = max(worst_cross, d_collab, d_isol)
        cross.append({
            "seed": int(seed),
            "exact_h_y_collaborating_bits":
                exact["collaborating"]["max_pid"]["h_y_bits"],
            "sampled_h_y_collaborating_bits": float(
                sampled_h_y_max(sampled["collaborating"]["counts"])),
            "exact_h_y_isolated_bits":
                exact["isolated"]["max_pid"]["h_y_bits"],
            "sampled_h_y_isolated_bits": float(
                sampled_h_y_max(sampled["isolated"]["counts"])),
            "diff_collaborating_bits": float(d_collab),
            "diff_isolated_bits": float(d_isol),
        })
    checks["exact_matches_sampled_h_y"] = (
        worst_cross <= t["exact_sampled_hy_tol_bits"])
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxviii) MAX-target PID identity, canonical "
                 "checks, sampled cross-check",
        "passed": passed,
        "checks": checks,
        "worst_identity_error_bits": float(worst_identity),
        "worst_atom_bits": float(worst_atom),
        "worst_exact_sampled_h_y_diff_bits": float(worst_cross),
        "identity_tol_bits": t["identity_tol_bits"],
        "atom_min_bits": t["atom_min_bits"],
        "canonical_tol_bits": t["canonical_tol_bits"],
        "exact_sampled_h_y_tol_bits":
            t["exact_sampled_hy_tol_bits"],
        "canonical_cases": canonical,
        "cross_check_rows": cross,
    }


def claim_delta_info_positive_verdict(seeds=ALL_SEEDS,
                                      generations=DEFAULT_GENERATIONS,
                                      design="B", sweep=None):
    """(lxix) Collaboration raises total information about
    the MAX target at sigma = 0.25.

    PASS iff, on EVERY seed: delta-I > 0 at sigma =
    0.25. A sign claim with no magnitude bar: the XOR
    failure was a negative gap, so the test is whether
    the gap is positive at all.
    """
    rows = (sweep if sweep is not None else max_gap_vs_noise(
        (SIGMA_REF,), seeds, generations, design))
    per_seed = []
    checks = {}
    for seed in seeds:
        row = next(r for r in rows
                   if r["seed"] == int(seed)
                   and r["sigma"] == SIGMA_REF)
        d_info = row["delta_total_info_bits"]
        per_seed.append({
            "seed": int(seed),
            "i_collaborating_bits": float(
                row["collaborating"]["max_pid"]["total_info_bits"]),
            "i_isolated_bits": float(
                row["isolated"]["max_pid"]["total_info_bits"]),
            "delta_total_info_bits": float(d_info),
        })
        checks[f"seed_{seed}_delta_info_positive"] = bool(d_info > 0.0)
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxix) Collaboration raises total "
                 "information about the MAX target at "
                 "sigma = 0.25",
        "passed": passed,
        "checks": checks,
        "sigma": SIGMA_REF,
        "per_seed": per_seed,
    }


def claim_synergy_dominant_verdict(seeds=ALL_SEEDS,
                                   generations=DEFAULT_GENERATIONS,
                                   design="B", sweep=None):
    """(lxx) The information gap about the MAX target IS
    synergy, not redundancy, at sigma = 0.25.

    PASS iff, on EVERY seed: delta-synergy exceeds
    delta-redundancy AND delta-synergy is at least
    SYNERGY_SHARE_MIN of the information gap dI at
    sigma = 0.25.
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else max_gap_vs_noise(
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
        "claim": "(lxx) The information gap about the MAX "
                 "target IS synergy, not redundancy, at "
                 "sigma = 0.25",
        "passed": passed,
        "checks": checks,
        "sigma": SIGMA_REF,
        "synergy_share_min": t["synergy_share_min"],
        "per_seed": per_seed,
    }


def claim_redundancy_share_verdict(seeds=ALL_SEEDS, sigmas=None,
                                   generations=DEFAULT_GENERATIONS,
                                   design="B", sweep=None):
    """(lxxi) Redundancy stays below half the target
    information across the grid.

    PASS iff, on EVERY (seed, sigma) with I_collab > 0:
    Red_collab <= REDUNDANCY_SHARE_MAX *
    I_collab(X1,X2;Y).
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else max_gap_vs_noise(
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
            xpid = r["collaborating"]["max_pid"]
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
        checks[f"seed_{seed}_redundancy_share_below_half"] = bool(
            worst_share <= t["redundancy_share_max"])
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxxi) Redundancy stays below half the "
                 "target information across the grid",
        "passed": passed,
        "checks": checks,
        "redundancy_share_max": t["redundancy_share_max"],
        "per_seed": per_seed,
    }


def claim_delta_info_grid_verdict(seeds=ALL_SEEDS, sigmas=None,
                                  generations=DEFAULT_GENERATIONS,
                                  design="B", sweep=None):
    """(lxxii) Collaboration raises total information about
    the MAX target across the grid.

    PASS iff, on EVERY (seed, sigma): delta-I > 0.
    """
    rows = (sweep if sweep is not None else max_gap_vs_noise(
        sigmas, seeds, generations, design))
    per_seed = []
    checks = {}
    for seed in seeds:
        sub = [r for r in rows if r["seed"] == int(seed)]
        sub.sort(key=lambda r: r["sigma"])
        min_d_info = min(r["delta_total_info_bits"] for r in sub)
        min_sigma = next(r["sigma"] for r in sub
                         if r["delta_total_info_bits"] == min_d_info)
        per_seed.append({
            "seed": int(seed),
            "min_delta_total_info_bits": float(min_d_info),
            "min_delta_total_info_sigma": min_sigma,
            "delta_total_info_bits": [float(r["delta_total_info_bits"])
                                      for r in sub],
        })
        checks[f"seed_{seed}_delta_info_positive_everywhere"] = bool(
            min_d_info > 0.0)
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxxii) Collaboration raises total "
                 "information about the MAX target across "
                 "the grid",
        "passed": passed,
        "checks": checks,
        "per_seed": per_seed,
    }


def total_information_target_claims():
    """The five MAX-target claims (lxviii)-(lxxii), measured fresh.

    One shared sweep over all seeds and sigmas feeds all
    five verdicts, so the evaluation run touches each
    held-out seed once.
    """
    sweep = max_gap_vs_noise()
    claim_lxviii = claim_max_identity_verdict(sweep=sweep)
    claim_lxix = claim_delta_info_positive_verdict(sweep=sweep)
    claim_lxx = claim_synergy_dominant_verdict(sweep=sweep)
    claim_lxxi = claim_redundancy_share_verdict(sweep=sweep)
    claim_lxxii = claim_delta_info_grid_verdict(sweep=sweep)
    verdicts = [claim_lxviii, claim_lxix, claim_lxx,
                claim_lxxi, claim_lxxii]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_lxviii_max_identity": claim_lxviii,
        "claim_lxix_delta_info_positive": claim_lxix,
        "claim_lxx_synergy_dominant": claim_lxx,
        "claim_lxxi_redundancy_share": claim_lxxi,
        "claim_lxxii_delta_info_grid": claim_lxxii,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the MAX-target PID decomposition and the claims
    (lxviii)-(lxxii) verdicts."""
    print("Total-information target (MAX) -- claims "
          "(lxviii)-(lxxii)")
    print()
    screen = screen_candidates()
    print(f"candidate screen (calibration seeds "
          f"{screen['seeds']}, sigma = {screen['sigma']}): "
          f"selected target = {screen['selected_target']}")
    for r in screen["candidates"]:
        per = {s["seed"]: s for s in r["per_seed"]}
        print(f"  {r['target']:12s} min dI = "
              f"{r['min_delta_total_info_bits']:+.4f} "
              f"(42: {per[42]['delta_total_info_bits']:+.4f}, "
              f"7: {per[7]['delta_total_info_bits']:+.4f}), "
              f"eligible = {r['eligible']}, "
              f"excluded = {r['excluded_from_selection']}")
    print()
    verdicts = total_information_target_claims()
    lxviii = verdicts["claim_lxviii_max_identity"]
    print(f"worst identity error: "
          f"{lxviii['worst_identity_error_bits']:.2e} "
          f"bits (tol {lxviii['identity_tol_bits']:.0e}); worst atom: "
          f"{lxviii['worst_atom_bits']:.4f} bits")
    print(f"worst exact-vs-sampled H(Y) diff at sigma = 0.25: "
          f"{lxviii['worst_exact_sampled_h_y_diff_bits']:.4f} bits "
          f"(tol {lxviii['exact_sampled_h_y_tol_bits']:.2f})")
    print(f"claim (lxviii) verdict: "
          f"{'PASS' if lxviii['passed'] else 'FAIL'}")
    print()
    lxix = verdicts["claim_lxix_delta_info_positive"]
    for r in lxix["per_seed"]:
        print(f"seed {r['seed']}: I_collab = "
              f"{r['i_collaborating_bits']:.4f}, I_isolated = "
              f"{r['i_isolated_bits']:.4f}, dI = "
              f"{r['delta_total_info_bits']:+.4f}")
    print(f"claim (lxix) verdict: {'PASS' if lxix['passed'] else 'FAIL'}")
    print()
    lxx = verdicts["claim_lxx_synergy_dominant"]
    for r in lxx["per_seed"]:
        print(f"seed {r['seed']}: dI = {r['delta_total_info_bits']:+.4f}, "
              f"dSyn = {r['delta_synergistic_bits']:+.4f}, "
              f"dRed = {r['delta_redundant_bits']:+.4f}, "
              f"dUniq = {r['delta_unique_bits']:+.4f}, "
              f"synergy share = {r['synergy_share_of_gap']:.3f}")
    print(f"claim (lxx) verdict: {'PASS' if lxx['passed'] else 'FAIL'}")
    print()
    lxxi = verdicts["claim_lxxi_redundancy_share"]
    for r in lxxi["per_seed"]:
        print(f"seed {r['seed']}: worst Red_c/I_c = "
              f"{r['worst_redundancy_share']:.4f} at sigma = "
              f"{r['worst_redundancy_share_sigma']} "
              f"(bar {lxxi['redundancy_share_max']:.2f})")
    print(f"claim (lxxi) verdict: "
          f"{'PASS' if lxxi['passed'] else 'FAIL'}")
    print()
    lxxii = verdicts["claim_lxxii_delta_info_grid"]
    for r in lxxii["per_seed"]:
        print(f"seed {r['seed']}: min dI across grid = "
              f"{r['min_delta_total_info_bits']:+.4f} at sigma = "
              f"{r['min_delta_total_info_sigma']}")
    print(f"claim (lxxii) verdict: "
          f"{'PASS' if lxxii['passed'] else 'FAIL'}")
    print()
    print(f"claims (lxviii)-(lxxii): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
