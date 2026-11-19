# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Per-generation PID: does the synergy-vs-sigma climb survive without pooling? (v0.22.0).

Follow-up to v0.20.0 (claims (lxiv)-(lxvii)) and v0.21.0
(claims (lxviii)-(lxxii)). The v0.20.0 XOR build found
synergy climbing toward the 2-bit ceiling with sigma on
every seed -- claim (lxvi) FAILED honestly: synergy
tracks noise-driven uniformity, not resonance. But the
v0.20.0 report disclosed a confound: the pooled joint is
a MIXTURE of per-generation products, and the
mixture-correlation is itself synergistic about the XOR
target -- the isolated arm is NOT synergy-free at high
sigma (Syn_isol up to 1.0755 bits at sigma = 1.00).
This module asks whether the climb survives when the PID
is computed PER GENERATION (no pooling across
generations), for the XOR target and the MAX target, on
the same seeds and sigma grid the pooled results used.

The method reuses the existing PID machinery: the general
Williams & Beer I_min PID
(total_information_target.target_pid_from_joint, the same
measure as v0.20.0/v0.21.0) applied to the exact
per-generation product joints from
pid.pair_arm_per_generation_joints -- the same design-B
evolution as pid.pair_arm_distributions, with each
generation's p1 (x) p2 kept instead of pooled. Nothing
about the PID measure changes; only the distribution it
is applied to. The comparison is mean-per-generation
atoms vs pooled atoms, and the pooled atom is NOT an
average of the per-generation atoms (the PID is
nonlinear in the joint, and the pooled joint is a
mixture) -- so a gap between the two is expected in
general; the question is its size and direction.

Decision rule (frozen in docs/preregistration-v0.22.0.md
before the evaluation run): the climb survives iff
claim (lxxiv) passes. If (lxxiv) fails, the (lxvi)
conclusion -- "synergy climbs toward the 2-bit ceiling
with sigma" -- is DOWNGRADED to a pooling artifact.

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
  - The per-generation isolated-arm synergy is 0.0000
    EXACTLY at every (seed, sigma) for both targets --
    by construction, not by measurement: the design-B
    isolated arm collapses each agent to a decided
    concept each generation, so each per-generation
    joint is a point mass and I = 0. The pooled
    isolated synergy at high sigma is therefore
    ENTIRELY a mixture effect.
  - Per-generation synergy varies a lot across
    generations: sd(Syn_c) at sigma >= 0.05 is
    0.14-0.39 bits (XOR, worst 0.3886, seed 7
    sigma = 1.00; single generations range
    0.2096-1.8250 there). The pooled value is not
    representative of any single generation.
  - Mean per-generation delta-I for MAX exceeds the
    pooled delta-I on seed 7 (e.g. +1.6598 vs +1.0707
    at sigma = 0.25) because pooling raises the
    isolated arm's information (pooled I_isol =
    0.8813) while per-generation I_isol = 0.

Pre-registered verdict rules for claims
(lxxiii)-(lxxvii), written before the evaluation run
(see the claim_*_verdict functions and REPORT.md
section 28). Thresholds are round numbers set from
the calibration pilot on seeds 42 and 7 only and
never moved after the evaluation run.
"""

import math

import numpy as np

import bridge
import pid
import total_information_target as tt

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SIGMA_GRID = pid.SIGMA_GRID
DEFAULT_SEED = 42
DEFAULT_GENERATIONS = pid.DEFAULT_GENERATIONS
CALIBRATION_SEEDS = (42, 7)
EVALUATION_SEEDS = (1234, 2026)
ALL_SEEDS = CALIBRATION_SEEDS + EVALUATION_SEEDS
SIGMA_REF = 0.25
SIGMA_HIGH = 0.50
SIGMA_TOP = 1.00
TARGETS = ("xor", "max")

# ---------------------------------------------------------------------------
# Pre-registered thresholds (set from the calibration pilot,
# docs/preregistration-v0.22.0.md, and never moved after
# the evaluation run).
# ---------------------------------------------------------------------------

# (lxxiii) Identity tolerance: the atoms sum to
# I(X1,X2;Y) within this (floating-point scale); every
# atom is at least -ATOM_MIN_BITS. The mean of the 10
# per-generation joints equals the pooled joint within
# POOLED_CONSISTENCY_TOL_BITS in max absolute entry
# (exact-arithmetic scale).
PER_GEN_PID_IDENTITY_TOL_BITS = 1e-9
PER_GEN_PID_ATOM_MIN_BITS = -1e-9
POOLED_CONSISTENCY_TOL = 1e-12

# (lxxiv) Climb survival: the mean per-generation
# synergy about the XOR target at sigma = 1.00 reaches
# at least this, and exceeds its sigma = 0.50 value.
# Calibration per-generation values at sigma = 1.00 are
# 1.0933 / 0.9855 (pooled: 1.8432 / 1.7933).
XOR_CLIMB_MIN_BITS = 1.50

# (lxxv) Mixture excess: the pooled isolated synergy
# about XOR at sigma = 1.00 exceeds the per-generation
# mean by at least this, and the per-generation mean
# isolated synergy at sigma in {0.50, 1.00} is at most
# PER_GEN_SYN_ISOL_MAX_BITS. Calibration excess is
# 1.0755 / 1.0000; per-generation mean is 0.0000.
MIXTURE_EXCESS_MIN_BITS = 0.50
PER_GEN_SYN_ISOL_MAX_BITS = 0.10

# (lxxvi), (lxxvii) Synergy dominance per-generation:
# the mean per-generation delta-synergy must exceed the
# mean per-generation delta-redundancy and be at least
# this fraction of the mean per-generation information
# gap at sigma = 0.25. Calibration shares are 0.383 /
# 0.332 (MAX) and 0.566 / 0.541 (XOR).
PER_GEN_SYNERGY_SHARE_MIN = 0.5


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("PER_GEN_PID_IDENTITY_TOL_BITS",
         PER_GEN_PID_IDENTITY_TOL_BITS),
        ("PER_GEN_PID_ATOM_MIN_BITS", PER_GEN_PID_ATOM_MIN_BITS),
        ("POOLED_CONSISTENCY_TOL", POOLED_CONSISTENCY_TOL),
        ("XOR_CLIMB_MIN_BITS", XOR_CLIMB_MIN_BITS),
        ("MIXTURE_EXCESS_MIN_BITS", MIXTURE_EXCESS_MIN_BITS),
        ("PER_GEN_SYN_ISOL_MAX_BITS", PER_GEN_SYN_ISOL_MAX_BITS),
        ("PER_GEN_SYNERGY_SHARE_MIN", PER_GEN_SYNERGY_SHARE_MIN),
    ) if value is None]
    if missing:
        raise ValueError(
            "per_generation_pid thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.22.0.md)")
    return {
        "identity_tol_bits": float(PER_GEN_PID_IDENTITY_TOL_BITS),
        "atom_min_bits": float(PER_GEN_PID_ATOM_MIN_BITS),
        "pooled_consistency_tol": float(POOLED_CONSISTENCY_TOL),
        "xor_climb_min_bits": float(XOR_CLIMB_MIN_BITS),
        "mixture_excess_min_bits": float(MIXTURE_EXCESS_MIN_BITS),
        "per_gen_syn_isol_max_bits": float(
            PER_GEN_SYN_ISOL_MAX_BITS),
        "per_gen_synergy_share_min": float(
            PER_GEN_SYNERGY_SHARE_MIN),
    }


# ---------------------------------------------------------------------------
# Per-generation target PID per (seed, sigma)
# ---------------------------------------------------------------------------

def _mean_atoms(pids):
    """Mean of a list of target-PID dicts, per atom."""
    keys = ("h_y_bits", "total_info_bits", "i_x1_y_bits",
            "i_x2_y_bits", "redundant_bits", "unique1_bits",
            "unique2_bits", "synergistic_bits", "atom_sum_bits")
    return {k: float(np.mean([p[k] for p in pids])) for k in keys}


def per_generation_target_pid(sigma=SIGMA_REF,
                              generations=DEFAULT_GENERATIONS,
                              seed=DEFAULT_SEED, design="B",
                              target="xor"):
    """Per-generation PID for one target at one (seed, sigma).

    Reuses pid.pair_arm_per_generation_joints for the exact
    per-generation product joints and
    total_information_target.target_pid_from_joint for the
    Williams & Beer I_min decomposition of each
    generation's joint. Returns, per arm: the list of
    per-generation PIDs, their mean atoms, and the pooled
    PID (same measure, pooled joint) for comparison. The
    arm differences are means of per-generation
    differences: mean dSyn, mean dRed, mean dUniq sum to
    mean dI exactly.
    """
    if target not in TARGETS:
        raise ValueError("target must be 'xor' or 'max'")
    fn, n_out = tt.TARGET_FUNCTIONS[target]
    per_gen = pid.pair_arm_per_generation_joints(
        sigma=sigma, generations=generations, seed=seed, design=design)
    pooled = pid.pair_arm_distributions(
        sigma=sigma, generations=generations, seed=seed, design=design)
    arms = {}
    for arm in ("collaborating", "isolated"):
        pids = [tt.target_pid_from_joint(j, fn, n_out)
                for j in per_gen[arm]["joints"]]
        pooled_joint = pooled[arm]["joint"]
        pooled_pid = tt.target_pid_from_joint(
            pooled_joint, fn, n_out)
        arms[arm] = {
            "per_generation_pids": pids,
            "mean_pid": _mean_atoms(pids),
            "sd_synergistic_bits": float(np.std(
                [p["synergistic_bits"] for p in pids])),
            "pooled_pid": pooled_pid,
            "pooled_joint_max_abs_entry": float(
                np.max(np.abs(pooled_joint))),
            "mean_joint_vs_pooled_max_abs_diff": float(np.max(
                np.abs(np.mean(per_gen[arm]["joints"], axis=0)
                       - pooled_joint))),
            "mean_r_post": per_gen[arm]["mean_r_post"],
        }
    collab = arms["collaborating"]["mean_pid"]
    isol = arms["isolated"]["mean_pid"]
    row = {
        "target": target,
        "n_agents": 2,
        "sigma": float(sigma),
        "generations": int(generations),
        "seed": int(seed),
        "design": design,
        "collaborating": arms["collaborating"],
        "isolated": arms["isolated"],
        "mean_delta_total_info_bits": float(
            collab["total_info_bits"] - isol["total_info_bits"]),
        "mean_delta_synergistic_bits": float(
            collab["synergistic_bits"] - isol["synergistic_bits"]),
        "mean_delta_redundant_bits": float(
            collab["redundant_bits"] - isol["redundant_bits"]),
        "mean_delta_unique_bits": float(
            (collab["unique1_bits"] + collab["unique2_bits"])
            - (isol["unique1_bits"] + isol["unique2_bits"])),
        "pooled_delta_total_info_bits": float(
            arms["collaborating"]["pooled_pid"]["total_info_bits"]
            - arms["isolated"]["pooled_pid"]["total_info_bits"]),
        "pooled_delta_synergistic_bits": float(
            arms["collaborating"]["pooled_pid"]["synergistic_bits"]
            - arms["isolated"]["pooled_pid"]["synergistic_bits"]),
    }
    return row


def per_generation_gap_vs_noise(targets=TARGETS, sigmas=None,
                                seeds=ALL_SEEDS,
                                generations=DEFAULT_GENERATIONS,
                                design="B"):
    """The per-generation PID gap decomposition per
    (target, seed, sigma)."""
    rows = []
    for target in targets:
        for seed in seeds:
            for sigma in (SIGMA_GRID if sigmas is None else sigmas):
                rows.append(per_generation_target_pid(
                    sigma=sigma, generations=generations,
                    seed=int(seed), design=design, target=target))
    return rows


# ---------------------------------------------------------------------------
# Claim verdicts (lxxiii)-(lxxvii)
# ---------------------------------------------------------------------------

def claim_per_gen_identity_verdict(targets=TARGETS, seeds=ALL_SEEDS,
                                   sigmas=None,
                                   generations=DEFAULT_GENERATIONS,
                                   design="B", sweep=None):
    """(lxxiii) Per-generation PID identity and pooled consistency.

    PASS iff, for every target, seed, sigma, generation,
    and both arms: the four atoms sum to I(X1,X2;Y)
    within PER_GEN_PID_IDENTITY_TOL_BITS and every atom
    is at least PER_GEN_PID_ATOM_MIN_BITS; AND the mean
    of the 10 per-generation joints equals the pooled
    joint within POOLED_CONSISTENCY_TOL in max absolute
    entry.
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else
            per_generation_gap_vs_noise(targets, sigmas, seeds,
                                        generations, design))
    worst_identity = 0.0
    worst_atom = 0.0
    worst_consistency = 0.0
    for row in rows:
        for arm in ("collaborating", "isolated"):
            worst_consistency = max(
                worst_consistency,
                row[arm]["mean_joint_vs_pooled_max_abs_diff"])
            for p in row[arm]["per_generation_pids"]:
                err = abs(p["atom_sum_bits"] - p["total_info_bits"])
                worst_identity = max(worst_identity, err)
                worst_atom = min(worst_atom, p["redundant_bits"],
                                 p["unique1_bits"], p["unique2_bits"],
                                 p["synergistic_bits"])
    checks = {
        "atoms_sum_to_total_info": bool(
            worst_identity <= t["identity_tol_bits"]),
        "all_atoms_nonnegative": bool(
            worst_atom >= t["atom_min_bits"]),
        "mean_per_generation_joint_equals_pooled": bool(
            worst_consistency <= t["pooled_consistency_tol"]),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxxiii) Per-generation PID identity and "
                 "pooled consistency",
        "passed": passed,
        "checks": checks,
        "worst_identity_error_bits": float(worst_identity),
        "worst_atom_bits": float(worst_atom),
        "worst_pooled_consistency_diff": float(worst_consistency),
        "identity_tol_bits": t["identity_tol_bits"],
        "atom_min_bits": t["atom_min_bits"],
        "pooled_consistency_tol": t["pooled_consistency_tol"],
    }


def _rows_for(sweep, target, seeds):
    return [r for r in sweep
            if r["target"] == target and r["seed"] in seeds]


def claim_xor_climb_survives_verdict(seeds=ALL_SEEDS,
                                     generations=DEFAULT_GENERATIONS,
                                     design="B", sweep=None):
    """(lxxiv) The XOR synergy-vs-sigma climb survives per-generation.

    PASS iff, on EVERY seed: the mean per-generation
    Syn_collab(XOR) at sigma = 1.00 is at least
    XOR_CLIMB_MIN_BITS AND exceeds its sigma = 0.50
    value. This is the decision claim of the build:
    FAIL means the (lxvi) climb is a pooling artifact.
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else
            per_generation_gap_vs_noise(
                ("xor",), (SIGMA_HIGH, SIGMA_TOP), seeds,
                generations, design))
    xor_rows = _rows_for(rows, "xor", seeds)
    per_seed = []
    checks = {}
    for seed in seeds:
        by_sigma = {r["sigma"]: r for r in xor_rows
                    if r["seed"] == int(seed)}
        syn_050 = by_sigma[SIGMA_HIGH]["collaborating"][
            "mean_pid"]["synergistic_bits"]
        syn_100 = by_sigma[SIGMA_TOP]["collaborating"][
            "mean_pid"]["synergistic_bits"]
        pooled_100 = by_sigma[SIGMA_TOP]["collaborating"][
            "pooled_pid"]["synergistic_bits"]
        per_seed.append({
            "seed": int(seed),
            "mean_syn_collab_sigma_0.50_bits": float(syn_050),
            "mean_syn_collab_sigma_1.00_bits": float(syn_100),
            "pooled_syn_collab_sigma_1.00_bits": float(pooled_100),
            "pooled_minus_per_generation_sigma_1.00_bits": float(
                pooled_100 - syn_100),
        })
        checks[f"seed_{seed}_per_generation_synergy_reaches_1.50"] = (
            bool(syn_100 >= t["xor_climb_min_bits"]))
        checks[f"seed_{seed}_per_generation_synergy_still_climbing"] = (
            bool(syn_100 > syn_050))
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxxiv) The XOR synergy-vs-sigma climb "
                 "survives per-generation",
        "passed": passed,
        "checks": checks,
        "xor_climb_min_bits": t["xor_climb_min_bits"],
        "per_seed": per_seed,
    }


def claim_isolated_synergy_is_mixture_verdict(
        seeds=ALL_SEEDS, generations=DEFAULT_GENERATIONS,
        design="B", sweep=None):
    """(lxxv) The isolated arm's high-sigma synergy is a pooling artifact (XOR).

    PASS iff, on EVERY seed: the pooled Syn_isol(XOR)
    at sigma = 1.00 exceeds the mean per-generation
    Syn_isol(XOR) by at least MIXTURE_EXCESS_MIN_BITS,
    AND the mean per-generation Syn_isol(XOR) is at most
    PER_GEN_SYN_ISOL_MAX_BITS at sigma in {0.50, 1.00}.
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else
            per_generation_gap_vs_noise(
                ("xor",), (SIGMA_HIGH, SIGMA_TOP), seeds,
                generations, design))
    xor_rows = _rows_for(rows, "xor", seeds)
    per_seed = []
    checks = {}
    for seed in seeds:
        by_sigma = {r["sigma"]: r for r in xor_rows
                    if r["seed"] == int(seed)}
        syn_i_100 = by_sigma[SIGMA_TOP]["isolated"][
            "mean_pid"]["synergistic_bits"]
        pooled_i_100 = by_sigma[SIGMA_TOP]["isolated"][
            "pooled_pid"]["synergistic_bits"]
        syn_i_050 = by_sigma[SIGMA_HIGH]["isolated"][
            "mean_pid"]["synergistic_bits"]
        excess = pooled_i_100 - syn_i_100
        per_seed.append({
            "seed": int(seed),
            "mean_syn_isol_sigma_0.50_bits": float(syn_i_050),
            "mean_syn_isol_sigma_1.00_bits": float(syn_i_100),
            "pooled_syn_isol_sigma_1.00_bits": float(pooled_i_100),
            "mixture_excess_sigma_1.00_bits": float(excess),
        })
        checks[f"seed_{seed}_mixture_excess_at_least_half_bit"] = (
            bool(excess >= t["mixture_excess_min_bits"]))
        checks[f"seed_{seed}_per_generation_isolated_synergy_small"] = (
            bool(syn_i_050 <= t["per_gen_syn_isol_max_bits"]
                 and syn_i_100 <= t["per_gen_syn_isol_max_bits"]))
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxxv) The isolated arm's high-sigma "
                 "synergy is a pooling artifact (XOR)",
        "passed": passed,
        "checks": checks,
        "mixture_excess_min_bits": t["mixture_excess_min_bits"],
        "per_gen_syn_isol_max_bits":
            t["per_gen_syn_isol_max_bits"],
        "per_seed": per_seed,
    }


def _per_gen_gap_dominant_verdict(target, claim_label, seeds,
                                  generations, design, sweep):
    """Shared verdict for (lxxvi) MAX / (lxxvii) XOR: the
    mean per-generation gap at sigma = 0.25 is synergy,
    not redundancy."""
    t = _thresholds()
    rows = (sweep if sweep is not None else
            per_generation_gap_vs_noise(
                (target,), (SIGMA_REF,), seeds,
                generations, design))
    target_rows = _rows_for(rows, target, seeds)
    per_seed = []
    checks = {}
    for seed in seeds:
        row = next(r for r in target_rows
                   if r["seed"] == int(seed)
                   and r["sigma"] == SIGMA_REF)
        d_info = row["mean_delta_total_info_bits"]
        d_syn = row["mean_delta_synergistic_bits"]
        d_red = row["mean_delta_redundant_bits"]
        share = d_syn / d_info if d_info != 0.0 else float("nan")
        per_seed.append({
            "seed": int(seed),
            "mean_delta_total_info_bits": float(d_info),
            "mean_delta_synergistic_bits": float(d_syn),
            "mean_delta_redundant_bits": float(d_red),
            "mean_delta_unique_bits": float(
                row["mean_delta_unique_bits"]),
            "synergy_share_of_mean_gap": float(share),
            "pooled_delta_total_info_bits": float(
                row["pooled_delta_total_info_bits"]),
            "pooled_delta_synergistic_bits": float(
                row["pooled_delta_synergistic_bits"]),
        })
        checks[f"seed_{seed}_synergy_exceeds_redundancy"] = bool(
            d_syn > d_red)
        checks[f"seed_{seed}_synergy_majority_of_gap"] = bool(
            share >= t["per_gen_synergy_share_min"])
    passed = bool(all(checks.values()))
    return {
        "claim": claim_label,
        "passed": passed,
        "checks": checks,
        "sigma": SIGMA_REF,
        "per_gen_synergy_share_min":
            t["per_gen_synergy_share_min"],
        "per_seed": per_seed,
    }


def claim_max_gap_dominant_per_gen_verdict(
        seeds=ALL_SEEDS, generations=DEFAULT_GENERATIONS,
        design="B", sweep=None):
    """(lxxvi) The per-generation MAX gap at sigma = 0.25
    is synergy, not redundancy."""
    return _per_gen_gap_dominant_verdict(
        "max",
        "(lxxvi) The per-generation MAX gap at sigma = 0.25 "
        "is synergy, not redundancy",
        seeds, generations, design, sweep)


def claim_xor_gap_dominant_per_gen_verdict(
        seeds=ALL_SEEDS, generations=DEFAULT_GENERATIONS,
        design="B", sweep=None):
    """(lxxvii) The per-generation XOR gap at sigma = 0.25
    is synergy, not redundancy."""
    return _per_gen_gap_dominant_verdict(
        "xor",
        "(lxxvii) The per-generation XOR gap at sigma = "
        "0.25 is synergy, not redundancy",
        seeds, generations, design, sweep)


def per_generation_pid_claims():
    """The five per-generation PID claims (lxxiii)-(lxxvii), measured fresh.

    One shared sweep over both targets, all seeds and
    sigmas feeds all five verdicts, so the evaluation
    run touches each held-out seed once.
    """
    sweep = per_generation_gap_vs_noise()
    claim_lxxiii = claim_per_gen_identity_verdict(sweep=sweep)
    claim_lxxiv = claim_xor_climb_survives_verdict(sweep=sweep)
    claim_lxxv = claim_isolated_synergy_is_mixture_verdict(sweep=sweep)
    claim_lxxvi = claim_max_gap_dominant_per_gen_verdict(sweep=sweep)
    claim_lxxvii = claim_xor_gap_dominant_per_gen_verdict(sweep=sweep)
    verdicts = [claim_lxxiii, claim_lxxiv, claim_lxxv,
                claim_lxxvi, claim_lxxvii]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_lxxiii_per_gen_identity": claim_lxxiii,
        "claim_lxxiv_xor_climb_survives": claim_lxxiv,
        "claim_lxxv_isolated_synergy_is_mixture": claim_lxxv,
        "claim_lxxvi_max_gap_dominant_per_gen": claim_lxxvi,
        "claim_lxxvii_xor_gap_dominant_per_gen": claim_lxxvii,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the per-generation PID decomposition and the
    claims (lxxiii)-(lxxvii) verdicts."""
    print("Per-generation PID -- claims (lxxiii)-(lxxvii)")
    print()
    verdicts = per_generation_pid_claims()
    lxxiii = verdicts["claim_lxxiii_per_gen_identity"]
    print(f"worst identity error: "
          f"{lxxiii['worst_identity_error_bits']:.2e} "
          f"bits (tol {lxxiii['identity_tol_bits']:.0e}); worst atom: "
          f"{lxxiii['worst_atom_bits']:.4f} bits")
    print(f"worst mean-per-generation vs pooled joint diff: "
          f"{lxxiii['worst_pooled_consistency_diff']:.2e} "
          f"(tol {lxxiii['pooled_consistency_tol']:.0e})")
    print(f"claim (lxxiii) verdict: "
          f"{'PASS' if lxxiii['passed'] else 'FAIL'}")
    print()
    lxxiv = verdicts["claim_lxxiv_xor_climb_survives"]
    for r in lxxiv["per_seed"]:
        print(f"seed {r['seed']}: mean Syn_c(0.50) = "
              f"{r['mean_syn_collab_sigma_0.50_bits']:.4f}, "
              f"mean Syn_c(1.00) = "
              f"{r['mean_syn_collab_sigma_1.00_bits']:.4f} "
              f"(bar {lxxiv['xor_climb_min_bits']:.2f}), "
              f"pooled Syn_c(1.00) = "
              f"{r['pooled_syn_collab_sigma_1.00_bits']:.4f}")
    print(f"claim (lxxiv) verdict: "
          f"{'PASS' if lxxiv['passed'] else 'FAIL'}")
    print()
    lxxv = verdicts["claim_lxxv_isolated_synergy_is_mixture"]
    for r in lxxv["per_seed"]:
        print(f"seed {r['seed']}: mean Syn_i(0.50) = "
              f"{r['mean_syn_isol_sigma_0.50_bits']:.4f}, "
              f"mean Syn_i(1.00) = "
              f"{r['mean_syn_isol_sigma_1.00_bits']:.4f}, "
              f"pooled Syn_i(1.00) = "
              f"{r['pooled_syn_isol_sigma_1.00_bits']:.4f}, "
              f"mixture excess = "
              f"{r['mixture_excess_sigma_1.00_bits']:+.4f} "
              f"(bar {lxxv['mixture_excess_min_bits']:.2f})")
    print(f"claim (lxxv) verdict: "
          f"{'PASS' if lxxv['passed'] else 'FAIL'}")
    print()
    for key, label in (
            ("claim_lxxvi_max_gap_dominant_per_gen", "(lxxvi) MAX"),
            ("claim_lxxvii_xor_gap_dominant_per_gen", "(lxxvii) XOR")):
        v = verdicts[key]
        for r in v["per_seed"]:
            print(f"{label} seed {r['seed']}: mean dI = "
                  f"{r['mean_delta_total_info_bits']:+.4f}, "
                  f"mean dSyn = "
                  f"{r['mean_delta_synergistic_bits']:+.4f}, "
                  f"mean dRed = "
                  f"{r['mean_delta_redundant_bits']:+.4f}, "
                  f"mean dUniq = "
                  f"{r['mean_delta_unique_bits']:+.4f}, "
                  f"synergy share = "
                  f"{r['synergy_share_of_mean_gap']:.3f} "
                  f"(pooled dI = "
                  f"{r['pooled_delta_total_info_bits']:+.4f}, "
                  f"pooled dSyn = "
                  f"{r['pooled_delta_synergistic_bits']:+.4f})")
        print(f"claim {label.split()[0]} verdict: "
              f"{'PASS' if v['passed'] else 'FAIL'}")
        print()
    print(f"claims (lxxiii)-(lxxvii): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
