# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# restricted_copier.py
#
# Privacy-enforcing copier: is the 5/6 cloning bound
# restored when the representation enforces privacy?
# (v0.23.0; claims (lxxviii)-(lxxxi).)
#
# The question. Claim (xlviii) FAILED in v0.15.0: the
# classical copy (unity.gaussian_copies) exceeds the
# 5/6 Buzek-Hillery bound at every working sigma
# (1.0000 at sigma = 0), because the classical emulation
# stores the full amplitude vector and privacy is not
# enforced by the representation. The v0.15.0 report
# recorded this as a representation artifact: the
# classical copier sees the whole state. This build
# tests whether the bound is restored when the copier
# is RESTRICTED to measurement outcomes only -- a
# classical channel with bounded information about the
# state -- and never sees the amplitude vector.
#
# The construction (fixed before the pilot; see
# docs/preregistration-v0.23.0.md). Only mechanisms
# already in the tree are used:
#   - Presented states: the SAME states claim (xlviii)
#     measured as "copies" -- unity.gaussian_copies of
#     the uniform thought (5 copies, sigma grid, every
#     seed). The state presented to the restricted
#     copier at (sigma, seed) is exactly the state the
#     unrestricted copier produced there, so the two
#     copiers are compared on identical inputs. Sigma
#     now measures how concentrated / classical the
#     state being copied is, not how noisy the copier
#     is: at sigma = 0 the presented state is the
#     uniform thought; at sigma = 1.0 it is a noisy,
#     partly concentrated state.
#   - Measurement: the bridge's own Born collapse in
#     the 4-concept basis (the measurement behind
#     cloning_ceiling.pair_accessible_information):
#     outcome k with probability p(k) = |psi_k|^2.
#     The copier observes only the outcomes, never
#     psi. One outcome carries at most log2(4) = 2
#     bits about the state, and no phase information
#     at all.
#   - Single-shot copier (M = 1): one Born outcome k;
#     the copy is the basis state e_k. Fidelity with
#     the presented state is |<psi|e_k>|^2 = p(k);
#     its expectation over outcomes is sum_k p(k)^2
#     (0.25 for the uniform thought).
#   - M-shot copier: M independent Born outcomes on
#     the same presented state; the copy is the
#     maximum-likelihood amplitude reconstruction
#     sqrt(counts / M) (real, non-negative, unit
#     norm). Fidelity is the TRUE inner product
#     |<psi|copy>|^2 with psi's signs kept: the
#     reconstruction cannot recover signs, so any
#     negative component of psi subtracts. That
#     sign-blindness is part of the privacy
#     mechanism, not a bug in it.
#   - Asymptotic leak (reported, not claimed): as
#     M -> infinity the reconstruction tends to
#     |psi| componentwise, so the fidelity tends to
#     (sum_k psi_k |psi_k|)^2 exactly -- computable
#     in closed form with no sampling. It is the
#     ceiling of what the classical channel can ever
#     leak: amplitudes yes, signs and phases no.
#
# Honesty, stated up front:
#   - This is a SYNTHETIC classical emulation. Nothing
#     here tests privacy in a physical system or
#     quantum mechanics itself. The 5/6 bound is a
#     theorem about universal quantum cloners; what is
#     measured is whether the model's restricted
#     copier respects it.
#   - The restricted and unrestricted fidelities have
#     DIFFERENT targets by construction: the
#     unrestricted (xlviii) fidelity is |<uniform|
#     copy>|^2 (how well the copy reproduces the
#     original uniform thought), while the restricted
#     fidelity is |<presented|copy>|^2 (how well the
#     reconstruction reproduces the state the copier
#     was given). The restricted-vs-unrestricted table
#     is therefore REPORTED, not claimed: the numbers
#     are comparable as "the model's copy fidelity at
#     noise sigma", but they are not the same
#     measurement, and no claim in this build rests
#     on equating them.
#   - The single-shot copy of a CONCENTRATED state is
#     good: if psi is nearly a basis state, one
#     outcome identifies it and the fidelity is near
#     1. That is legitimate -- a state-dependent
#     copier copies its preferred states exactly
#     (v0.15.0 header: CNOT copies basis states with
#     fidelity 1) -- and it is why claim (lxxviii)
#     is a live question at high sigma rather than a
#     formality: the bound can be restored at low
#     sigma and still fail at high sigma, where the
#     state is nearly classical.
#   - The M-shot reconstruction of a REAL, POSITIVE
#     state (the uniform thought) converges to the
#     state itself as M grows: with enough shots the
#     classical channel leaks the full amplitude
#     vector. The restriction restores the bound
#     only while the measurement budget is small.
#     Claim (lxxix) tests exactly where that stops.
#
# Pre-registered verdict rules for claims
# (lxxviii)-(lxxxi), written before the evaluation run
# (see docs/preregistration-v0.23.0.md and the
# claim_*_verdict functions):
#   (lxxviii) Single-shot restricted copier (5 copies,
#       sigma grid, every seed): mean fidelity <= 5/6
#       at every sigma. (Calibration pilot: PASSES --
#       max mean fidelity 0.3998 / 0.5798, seeds 42 / 7.)
#   (lxxix) M-shot reconstruction at sigma = 0 (20
#       copies, M = 16 shots): mean fidelity > 5/6 on
#       every seed -- the bound is NOT restored once
#       the copier gets 16 shots. (Calibration pilot:
#       0.9526 / 0.9396, both above 5/6.)
#   (lxxx) Budget gap at sigma = 0 (20 copies): mean
#       fidelity at M = 64 exceeds mean fidelity at
#       M = 1 by >= 0.30 on every seed. (Calibration
#       pilot: gaps 0.7378 / 0.7382.)
#   (lxxxi) The 16-shot leak is sigma-dependent (20
#       copies): mean M = 16 fidelity > 5/6 at sigma =
#       0.25 AND < 5/6 at sigma = 1.00, on every seed.
#       (Calibration pilot: 0.9333 / 0.9365 at sigma =
#       0.25; 0.8079 / 0.6331 at sigma = 1.00. The
#       high-sigma leg is thin on seed 42 -- margin
#       0.025 -- so held-out failure is a live
#       possibility, disclosed in advance.)
#
"""Privacy-enforcing copier: claims (lxxviii)-(lxxxi)."""

import math

import numpy as np

import cloning_ceiling as cc
import thought
import thought_entanglement as te
import unity

# ---------------------------------------------------------------------------
# Seeds
# ---------------------------------------------------------------------------

# Calibration seeds: thresholds were frozen from these only.
CALIBRATION_SEEDS = (42, 7)
# Evaluation seeds: held out until the evaluation run.
EVALUATION_SEEDS = (1234, 2026)
ALL_SEEDS = CALIBRATION_SEEDS + EVALUATION_SEEDS

# ---------------------------------------------------------------------------
# Pre-registered thresholds (frozen from the calibration pilot,
# docs/preregistration-v0.23.0.md; never moved after the run).
# ---------------------------------------------------------------------------

# Claims (lxxviii)-(lxxxi): the optimal universal 1 -> 2
# cloning fidelity for a qubit (Buzek-Hillery 1996), the
# same bar claim (xlviii) used.
CLONING_BOUND = 5.0 / 6.0

# Claim (lxxix): the measurement budget at which the leak
# is tested (shots per presented state), and the budget
# sweep grid for claim (lxxx).
CLAIM_M_SHOTS = 16
BUDGET_M_GRID = (1, 4, 16, 64, 256)

# Claim (lxxx): the frozen budget gap at sigma = 0
# (mean fidelity at M = 64 minus mean fidelity at M = 1).
BUDGET_GAP_MIN = 0.30

# Construction constants.
N_COPIES = 5
N_BUDGET_COPIES = 20
SIGMA_GRID = te.SIGMA_GRID
# Claim (lxxxi): the two sigmas at which the 16-shot
# leak is tested (low sigma, where amplitudes leak;
# high sigma, where sign-blindness caps the leak).
LXXXI_SIGMA_LOW = 0.25
LXXXI_SIGMA_HIGH = 1.00


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("CLONING_BOUND", CLONING_BOUND),
        ("CLAIM_M_SHOTS", CLAIM_M_SHOTS),
        ("BUDGET_M_GRID", BUDGET_M_GRID),
        ("BUDGET_GAP_MIN", BUDGET_GAP_MIN),
    ) if value is None]
    if missing:
        raise ValueError(
            "restricted-copier thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.23.0.md)")
    return {
        "cloning_bound": float(CLONING_BOUND),
        "claim_m_shots": int(CLAIM_M_SHOTS),
        "budget_m_grid": [int(m) for m in BUDGET_M_GRID],
        "budget_gap_min": float(BUDGET_GAP_MIN),
    }


# ---------------------------------------------------------------------------
# The restricted copier
# ---------------------------------------------------------------------------

def _measurement_seed(seed, copy_index, n_shots):
    """Deterministic seed for the measurement RNG.

    Independent of the state-generation RNG (which is
    seeded with `seed` itself inside gaussian_copies):
    the measurement draws must not reuse the noise
    draws that built the presented state.
    """
    return (7919 * int(seed) + 104729 * int(copy_index)
            + int(n_shots))


def born_probabilities(psi):
    """p(k) = |psi_k|^2: the Born distribution of the
    bridge's own measurement in the 4-concept basis."""
    psi = np.asarray(psi, dtype=complex)
    p = np.abs(psi) ** 2
    return p / float(np.sum(p))


def measure_outcomes(psi, n_shots, seed, copy_index):
    """n_shots independent Born outcomes (concept indices)
    on the presented state psi, seeded deterministically.

    The copier observes only these outcomes, never psi.
    """
    p = born_probabilities(psi)
    rng = np.random.default_rng(
        _measurement_seed(seed, copy_index, n_shots))
    return rng.choice(len(p), size=int(n_shots), p=p)


def reconstruct_from_outcomes(outcomes, n_concepts=4):
    """The copy the restricted copier builds from its
    outcomes alone: sqrt(counts / M), real and
    non-negative. No amplitude, sign, or phase of the
    presented state enters this reconstruction."""
    counts = np.bincount(np.asarray(outcomes, dtype=int),
                         minlength=int(n_concepts)).astype(float)
    return np.sqrt(counts / float(np.sum(counts)))


def restricted_copy(psi, n_shots, seed, copy_index):
    """One restricted copy of the presented state psi:
    measure it n_shots times, rebuild from the outcomes
    only. At n_shots = 1 this is the observed basis
    state e_k."""
    outcomes = measure_outcomes(psi, n_shots, seed, copy_index)
    return reconstruct_from_outcomes(outcomes, len(psi))


def copy_fidelity(psi, copy):
    """Fidelity |<psi|copy>|^2 with the presented state,
    signs of psi kept: the reconstruction cannot recover
    them, so a negative component subtracts."""
    psi = np.asarray(psi, dtype=complex)
    copy = np.asarray(copy, dtype=complex)
    return float(abs(np.vdot(psi, copy)) ** 2)


def asymptotic_leak_fidelity(psi):
    """The M -> infinity ceiling of the reconstruction:
    the copy tends to |psi| componentwise, so the
    fidelity tends to (sum_k psi_k |psi_k|)^2 exactly.
    Amplitudes leak; signs and phases never do."""
    psi = np.asarray(psi, dtype=float)
    return float((np.sum(psi * np.abs(psi))) ** 2)


def presented_states(sigma, seed, n_copies=N_COPIES):
    """The states presented to the restricted copier at
    (sigma, seed): unity.gaussian_copies of the uniform
    thought -- exactly the states claim (xlviii)
    measured as 'copies', now reinterpreted as the
    states to be copied."""
    base = np.real(thought.uniform_thought())
    return unity.gaussian_copies(base, sigma, n_copies, seed)


# ---------------------------------------------------------------------------
# (lxxviii) Single-shot sweep
# ---------------------------------------------------------------------------

def single_shot_fidelity(sigma, seed, n_copies=N_COPIES):
    """Mean single-shot restricted-copy fidelity per
    presented state at (sigma, seed): one Born outcome
    per state, copy = the observed basis state."""
    states = presented_states(sigma, seed, n_copies)
    fids = []
    for idx, psi in enumerate(states):
        copy = restricted_copy(psi, 1, seed, idx)
        fids.append(copy_fidelity(psi, copy))
    return {
        "sigma": float(sigma),
        "seed": int(seed),
        "n_shots": 1,
        "mean_fidelity": float(np.mean(fids)),
        "min_fidelity": float(min(fids)),
        "max_fidelity": float(max(fids)),
        "fidelities": [float(f) for f in fids],
    }


def single_shot_sweep(seed, n_copies=N_COPIES):
    """Mean single-shot fidelity per sigma, one seed."""
    return [single_shot_fidelity(sigma, seed, n_copies)
            for sigma in SIGMA_GRID]


# ---------------------------------------------------------------------------
# (lxxix)-(lxxxi) M-shot reconstruction and the budget sweep
# ---------------------------------------------------------------------------

def m_shot_fidelity(sigma, seed, n_shots,
                    n_copies=N_BUDGET_COPIES):
    """Mean M-shot reconstruction fidelity at (sigma,
    seed): each presented state is measured n_shots
    times and rebuilt from the outcomes only."""
    states = presented_states(sigma, seed, n_copies)
    fids = []
    for idx, psi in enumerate(states):
        copy = restricted_copy(psi, n_shots, seed, idx)
        fids.append(copy_fidelity(psi, copy))
    return {
        "sigma": float(sigma),
        "seed": int(seed),
        "n_shots": int(n_shots),
        "n_copies": int(n_copies),
        "mean_fidelity": float(np.mean(fids)),
        "min_fidelity": float(min(fids)),
        "max_fidelity": float(max(fids)),
        "fidelities": [float(f) for f in fids],
    }


def budget_sweep(sigma, seed, m_grid=None,
                 n_copies=N_BUDGET_COPIES):
    """Mean M-shot fidelity across the budget grid at
    one (sigma, seed)."""
    return [m_shot_fidelity(sigma, seed, m, n_copies)
            for m in (BUDGET_M_GRID if m_grid is None
                      else m_grid)]


def asymptotic_leak_sweep(sigma, seed, n_copies=N_COPIES):
    """Mean M -> infinity leak fidelity at (sigma, seed),
    computed exactly per presented state (reported, not
    claimed)."""
    states = presented_states(sigma, seed, n_copies)
    fids = [asymptotic_leak_fidelity(psi) for psi in states]
    return {
        "sigma": float(sigma),
        "seed": int(seed),
        "mean_fidelity": float(np.mean(fids)),
        "min_fidelity": float(min(fids)),
        "max_fidelity": float(max(fids)),
    }


def restricted_vs_unrestricted(seed, n_copies=N_COPIES):
    """REPORTED, not claimed: the restricted single-shot
    mean fidelity beside the unrestricted (xlviii)
    classical-copy mean fidelity at the same (sigma,
    seed), on identical presented states.

    The targets differ by construction (restricted:
    |<presented|copy>|^2; unrestricted: |<uniform|
    copy>|^2), so this table compares the models'
    copy fidelities at noise sigma, not the same
    measurement."""
    rows = []
    for sigma in SIGMA_GRID:
        restricted = single_shot_fidelity(sigma, seed, n_copies)
        unrestricted = cc.classical_copy_fidelity(
            sigma, seed, n_copies)
        rows.append({
            "sigma": float(sigma),
            "seed": int(seed),
            "restricted_single_shot_mean": restricted["mean_fidelity"],
            "unrestricted_mean": unrestricted["mean_fidelity"],
            "difference": float(restricted["mean_fidelity"]
                                - unrestricted["mean_fidelity"]),
        })
    return rows


# ---------------------------------------------------------------------------
# Claim verdicts (lxxviii)-(lxxxi)
# ---------------------------------------------------------------------------

def claim_single_shot_verdict(seeds=None):
    """(lxxviii) Single-shot restricted copier: mean
    fidelity <= 5/6 at every sigma on every seed.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026},
    the 5-copy mean single-shot fidelity is <= 5/6 at
    every sigma on the grid. Calibration: PASSES --
    the max mean fidelity is 0.3998 / 0.5798 (seeds
    42 / 7), far below 5/6 even at sigma = 1.00: the
    state never concentrates enough for one outcome
    to identify it.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        rows = single_shot_sweep(seed)
        per_seed.append({
            "seed": int(seed),
            "max_mean_fidelity": float(max(
                r["mean_fidelity"] for r in rows)),
            "rows": rows,
        })
    checks = {
        "single_shot_respects_bound": all(
            r["max_mean_fidelity"] <= t["cloning_bound"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxxviii) single-shot restricted copier "
                 "respects the 5/6 bound at every sigma",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_m_shot_leak_verdict(seeds=None):
    """(lxxix) M-shot reconstruction at sigma = 0 (20
    copies, M = 16 shots): mean fidelity > 5/6 on every
    seed -- the bound is NOT restored once the copier
    gets 16 shots.

    PASS iff the 20-copy mean M-shot fidelity at sigma
    = 0 exceeds 5/6 on EVERY seed in {42, 7, 1234,
    2026}. Calibration: 0.9526 / 0.9396 (seeds 42 / 7),
    both above 5/6.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        row = m_shot_fidelity(0.0, seed, t["claim_m_shots"])
        per_seed.append({
            "seed": int(seed),
            "sigma": 0.0,
            "n_shots": t["claim_m_shots"],
            "mean_fidelity": row["mean_fidelity"],
            "min_fidelity": row["min_fidelity"],
            "max_fidelity": row["max_fidelity"],
        })
    checks = {
        "m_shot_exceeds_bound_at_sigma_0": all(
            r["mean_fidelity"] > t["cloning_bound"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxxix) 16-shot reconstruction at sigma = 0 "
                 "exceeds the 5/6 bound (amplitudes leak)",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_budget_gap_verdict(seeds=None):
    """(lxxx) Budget gap at sigma = 0 (20 copies): the
    mean fidelity at M = 64 exceeds the mean fidelity
    at M = 1 by >= 0.30 on every seed -- the
    measurement budget controls the leak.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026},
    mean(M = 64) - mean(M = 1) >= 0.30 at sigma = 0.
    Calibration: gaps 0.7378 / 0.7382 (seeds 42 / 7).
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        rows = budget_sweep(0.0, seed)
        by_m = {r["n_shots"]: r["mean_fidelity"] for r in rows}
        per_seed.append({
            "seed": int(seed),
            "sigma": 0.0,
            "rows": rows,
            "gap_m64_minus_m1": float(by_m[64] - by_m[1]),
        })
    checks = {
        "budget_gap_at_least_0.30": all(
            r["gap_m64_minus_m1"] >= t["budget_gap_min"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxxx) measurement-budget gap at sigma = 0 "
                 "is >= 0.30 (M = 64 vs M = 1)",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_sigma_dependence_verdict(seeds=None):
    """(lxxxi) The 16-shot leak is sigma-dependent (20
    copies): mean M = 16 fidelity > 5/6 at sigma = 0.25
    AND < 5/6 at sigma = 1.00, on every seed.

    The mechanism: at low sigma the presented state
    stays real and positive, so the amplitude
    reconstruction converges to the state itself and
    the bound is exceeded; at high sigma the noise
    creates negative components the outcome-only
    reconstruction cannot see, and the sign-blindness
    caps the leak below the bound (the M -> infinity
    ceiling there is (sum_k psi_k |psi_k|)^2 < 1).
    PASS iff both legs hold on EVERY seed in {42, 7,
    1234, 2026}. Calibration: 0.9333 / 0.9365 at
    sigma = 0.25; 0.8079 / 0.6331 at sigma = 1.00.
    The high-sigma leg is thin on seed 42 (margin
    0.025), so held-out failure is a live possibility.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        low = m_shot_fidelity(LXXXI_SIGMA_LOW, seed,
                              t["claim_m_shots"])
        high = m_shot_fidelity(LXXXI_SIGMA_HIGH, seed,
                               t["claim_m_shots"])
        per_seed.append({
            "seed": int(seed),
            "n_shots": t["claim_m_shots"],
            "mean_fidelity_sigma_0.25": low["mean_fidelity"],
            "mean_fidelity_sigma_1.00": high["mean_fidelity"],
        })
    checks = {
        "leak_exceeds_bound_at_sigma_0.25": all(
            r["mean_fidelity_sigma_0.25"] > t["cloning_bound"]
            for r in per_seed),
        "leak_below_bound_at_sigma_1.00": all(
            r["mean_fidelity_sigma_1.00"] < t["cloning_bound"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxxxi) 16-shot leak exceeds 5/6 at sigma = "
                 "0.25 and falls below 5/6 at sigma = 1.00",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def restricted_copier_claims():
    """The four restricted-copier claims
    (lxxviii)-(lxxxi), measured fresh."""
    claim_lxxviii = claim_single_shot_verdict()
    claim_lxxix = claim_m_shot_leak_verdict()
    claim_lxxx = claim_budget_gap_verdict()
    claim_lxxxi = claim_sigma_dependence_verdict()
    verdicts = [claim_lxxviii, claim_lxxix, claim_lxxx,
                claim_lxxxi]
    return {
        "headline_allowed": False,
        "claim_lxxviii_single_shot": claim_lxxviii,
        "claim_lxxix_m_shot_leak": claim_lxxix,
        "claim_lxxx_budget_gap": claim_lxxx,
        "claim_lxxxi_sigma_dependence": claim_lxxxi,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the single-shot sweep, the budget sweep,
    the 16-shot sigma curve, and the claims
    (lxxviii)-(lxxxi) verdicts."""
    print("Privacy-enforcing copier -- claims (lxxviii)-(lxxxi)")
    print()
    verdicts = restricted_copier_claims()
    lx = verdicts["claim_lxxviii_single_shot"]
    print("Single-shot mean fidelity per sigma:")
    for r in lx["per_seed"]:
        print(f"  seed {r['seed']}: max mean = "
              f"{r['max_mean_fidelity']:.4f} "
              f"(bound 5/6 = {CLONING_BOUND:.4f})")
        for row in r["rows"]:
            print(f"    sigma = {row['sigma']:>4}: "
                  f"{row['mean_fidelity']:.4f}")
    print(f"claim (lxxviii) verdict: "
          f"{'PASS' if lx['passed'] else 'FAIL'}")
    print()
    ly = verdicts["claim_lxxix_m_shot_leak"]
    print("16-shot mean fidelity at sigma = 0:")
    for r in ly["per_seed"]:
        print(f"  seed {r['seed']}: {r['mean_fidelity']:.4f}")
    print(f"claim (lxxix) verdict: "
          f"{'PASS' if ly['passed'] else 'FAIL'}")
    print()
    lz = verdicts["claim_lxxx_budget_gap"]
    print("Budget sweep at sigma = 0 (mean fidelity):")
    for r in lz["per_seed"]:
        cells = "  ".join(
            f"M={row['n_shots']}:{row['mean_fidelity']:.4f}"
            for row in r["rows"])
        print(f"  seed {r['seed']}: {cells}  "
              f"gap M64-M1 = {r['gap_m64_minus_m1']:.4f}")
    print(f"claim (lxxx) verdict: "
          f"{'PASS' if lz['passed'] else 'FAIL'}")
    print()
    lw = verdicts["claim_lxxxi_sigma_dependence"]
    print("16-shot mean fidelity at sigma = 0.25 / 1.00:")
    for r in lw["per_seed"]:
        print(f"  seed {r['seed']}: sigma = 0.25: "
              f"{r['mean_fidelity_sigma_0.25']:.4f}, "
              f"sigma = 1.00: "
              f"{r['mean_fidelity_sigma_1.00']:.4f}")
    print(f"claim (lxxxi) verdict: "
          f"{'PASS' if lw['passed'] else 'FAIL'}")
    print()
    print(f"Restricted copier: {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} claims pass")


if __name__ == "__main__":
    main()
