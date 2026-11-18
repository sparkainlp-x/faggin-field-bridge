# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Synergy-vs-redundancy PID of the collaboration gap (v0.14.0).

Deep-think upgrade #5 (report.md section 9): decompose the
+4.3352-bit joint-entropy collaboration gap by integrated
information decomposition (PID / PhiID: Luppi, Mediano,
Rosas et al., Nature Neuroscience 2022/2024) into
redundant, unique, and synergistic components.

The construction (fixed in docs/preregistration-v0.14.0.md
before the evaluation run):

  - PID is defined for TWO sources, so the decomposition
    is of the PAIR-level gap: N = 2 agents (the
    thought-pair level at which concurrence and D are
    defined). The N = 4 sampled gap (+4.3352 bits at
    sigma = 0.25, seed 42) is reported as context, not
    decomposed.
  - Target Y = the joint outcome (X1, X2): the PID then
    decomposes H(X1, X2) itself, so the arm difference
    dRed + dUniq1 + dUniq2 + dSyn equals the
    collaboration gap EXACTLY. Sources X1, X2 are the
    two agents' Born outcomes (4 concepts each).
  - Redundancy is Williams & Beer I_min: the specific
    information of source i about the joint outcome
    y = (x1, x2) is -log2 p_i(x_i) (y determines x_i),
    so Red = E[-log2 max(p1(X1), p2(X2))],
    Uniq_i = H(Xi) - Red, and
    Syn = H(X1,X2) - Uniq1 - Uniq2 - Red
        = Red - I(X1;X2).
  - Joint distribution: the EXACT pooled product
    distribution. The evolution replicates
    empathy_field.run_collaboration design B generation
    by generation (same population, same noise kicks,
    same field mix with coupling f for the collaborating
    arm, same Born-collapse for the isolated arm), but
    instead of sampling joint outcomes it pools the
    exact per-generation product Born distribution
    p1 (x) p2 over the 10 generations. No sampling is
    involved in the PID itself.

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
  - The collaboration gap decomposed here is the
    pair-level (N = 2) gap, not the N = 4 +4.3352-bit
    gap itself; the N = 4 value is context.
  - Structural degeneracy, disclosed in the
    preregistration: in the collaborating arm
    I(X1;X2) is ~0.01-0.04 bits (the two agents'
    outcomes are drawn independently given their
    states), so Syn = Red - I(X1;X2) is numerically
    almost Red on every sigma. The I_min decomposition
    of the joint outcome cannot separate synergy from
    redundancy in this wiring; the two atoms differ
    only by the near-zero I(X1;X2).

Pre-registered verdict rules for claims (xl)-(xliii),
written before the evaluation run (see the claim_*_
verdict functions and REPORT.md section 20).
Thresholds are round numbers set from the calibration
pilot on seeds 42 and 7 only and never moved after
the evaluation run.
"""

import math

import numpy as np

import bridge
import cost
import empathy_field as ef
import self_knowing as sk
import thought

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SIGMA_GRID = ef.SIGMA_GRID
DEFAULT_SEED = 42
DEFAULT_N_AGENTS = 2
DEFAULT_GENERATIONS = ef.DEFAULT_GENERATIONS
CALIBRATION_SEEDS = (42, 7)
EVALUATION_SEEDS = (1234, 2026)
ALL_SEEDS = CALIBRATION_SEEDS + EVALUATION_SEEDS
SIGMA_REF = 0.25
SIGMA_HIGH = 0.50

# ---------------------------------------------------------------------------
# Pre-registered thresholds (set from the calibration pilot,
# docs/preregistration-v0.14.0.md, and never moved after
# the evaluation run).
# ---------------------------------------------------------------------------

# (xl) Identity tolerance: the atoms sum to H_joint within
# this (floating-point scale); every atom is at least
# -ATOM_MIN_BITS. The calibration pilot's worst identity
# error is < 1e-12.
PID_IDENTITY_TOL_BITS = 1e-9
PID_ATOM_MIN_BITS = -1e-9

# (xl) Cross-check: the exact H agrees with the sampled
# run_collaboration (N = 2, design B) H within this at
# sigma = 0.25. Calibration diffs are 0.017-0.025 bits,
# so 0.25 is the round number with a ~10x margin.
EXACT_SAMPLED_TOL_BITS = 0.25

# (xli) Synergy dominance: delta-synergy must exceed
# delta-redundancy and be at least this fraction of the
# gap at sigma = 0.25. Calibration shares are 40.7%
# (seed 42) and 42.9% (seed 7).
SYNERGY_SHARE_MIN = 0.5

# (xlii) Synergy must rise with R: Pearson(synergy,
# mean R_post) across the sigma grid at least this.
# Calibration Pearsons are -0.32 (seed 42) and -0.14
# (seed 7).
SYNERGY_R_PEARSON_MIN = 0.5

# (xliii) Redundancy sigma-robustness: the delta-
# redundancy at sigma = 0.50 is at least this fraction
# of its sigma = 0.25 value. Calibration ratios are
# 0.2351 (seed 42) and 1.4455 (seed 7).
ROBUST_RATIO_MIN = 0.5


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("PID_IDENTITY_TOL_BITS", PID_IDENTITY_TOL_BITS),
        ("PID_ATOM_MIN_BITS", PID_ATOM_MIN_BITS),
        ("EXACT_SAMPLED_TOL_BITS", EXACT_SAMPLED_TOL_BITS),
        ("SYNERGY_SHARE_MIN", SYNERGY_SHARE_MIN),
        ("SYNERGY_R_PEARSON_MIN", SYNERGY_R_PEARSON_MIN),
        ("ROBUST_RATIO_MIN", ROBUST_RATIO_MIN),
    ) if value is None]
    if missing:
        raise ValueError(
            "pid thresholds are unset: run the calibration "
            "pilot and set " + ", ".join(missing) + " first "
            "(docs/preregistration-v0.14.0.md)")
    return {
        "identity_tol_bits": float(PID_IDENTITY_TOL_BITS),
        "atom_min_bits": float(PID_ATOM_MIN_BITS),
        "exact_sampled_tol_bits": float(EXACT_SAMPLED_TOL_BITS),
        "synergy_share_min": float(SYNERGY_SHARE_MIN),
        "synergy_r_pearson_min": float(SYNERGY_R_PEARSON_MIN),
        "robust_ratio_min": float(ROBUST_RATIO_MIN),
    }


# ---------------------------------------------------------------------------
# PID of a joint distribution (Williams & Beer I_min)
# ---------------------------------------------------------------------------

def pid_from_joint(joint):
    """Williams & Beer I_min PID of H(X1, X2), target Y = (X1, X2).

    joint is a 4x4 array p(x1, x2). Returns H1, H2,
    H_joint, I(X1;X2), Red, Uniq1, Uniq2, Syn. The four
    atoms sum to H_joint by construction (Syn is defined
    as the remainder), so the identity is a check on the
    arithmetic, not on a theorem.
    """
    joint = np.asarray(joint, dtype=float)
    if joint.shape != (4, 4):
        raise ValueError("joint must be a 4x4 distribution")
    if np.any(joint < 0.0):
        raise ValueError("joint probabilities must be nonnegative")
    total = float(np.sum(joint))
    if total <= 0.0:
        raise ValueError("joint distribution sums to zero")
    joint = joint / total
    p1 = joint.sum(axis=1)
    p2 = joint.sum(axis=0)
    h1 = cost.shannon_entropy(p1)
    h2 = cost.shannon_entropy(p2)
    h12 = cost.shannon_entropy(joint.flatten())
    mutual = h1 + h2 - h12
    red = 0.0
    for a in range(4):
        for b in range(4):
            if joint[a, b] > 0.0:
                # Specific info of source 1 about y = (a, b)
                # is -log2 p1[a]; of source 2, -log2 p2[b];
                # I_min takes the smaller, i.e. -log2 max.
                red += joint[a, b] * (-math.log2(max(p1[a], p2[b])))
    uniq1 = h1 - red
    uniq2 = h2 - red
    syn = h12 - uniq1 - uniq2 - red
    return {
        "h1_bits": float(h1),
        "h2_bits": float(h2),
        "h_joint_bits": float(h12),
        "mutual_information_bits": float(mutual),
        "redundant_bits": float(red),
        "unique1_bits": float(uniq1),
        "unique2_bits": float(uniq2),
        "synergistic_bits": float(syn),
        "atom_sum_bits": float(red + uniq1 + uniq2 + syn),
    }


# ---------------------------------------------------------------------------
# Exact pooled pair distributions (design-B evolution)
# ---------------------------------------------------------------------------

def pair_arm_distributions(sigma=SIGMA_REF,
                           generations=DEFAULT_GENERATIONS,
                           seed=DEFAULT_SEED, design="B"):
    """Exact pooled joint distributions for a 2-agent pair.

    Replicates empathy_field.run_collaboration design B
    generation by generation (same population, same noise
    kicks, same field mix at coupling f for the
    collaborating arm, same Born-collapse for the
    isolated arm), but pools the exact per-generation
    product Born distribution p1 (x) p2 instead of
    sampling joint outcomes. Also returns the mean
    pairwise resonance R before the mix (R_pre) and
    after the mix / collapse (R_post) per arm.
    """
    if design not in ("A", "B"):
        raise ValueError("design must be 'A' or 'B'")
    base = ef.collaboration_population(DEFAULT_N_AGENTS, sigma, seed)
    arms = {}
    for arm in ("collaborating", "isolated"):
        states = [s.copy() for s in base]
        pooled = np.zeros((4, 4))
        r_pre, r_post = [], []
        for g in range(int(generations)):
            states = [ef._noise_kick(s, sigma, seed + 1000 * g + 10 * i)
                      for i, s in enumerate(states)]
            r_pre.append(ef.overlap_squared(states[0], states[1]))
            if arm == "collaborating":
                coupling = (ef.empathy_fraction(states)
                            if len(states) >= 2 else 0.0)
                states = ef._field_mix(states, coupling)
            else:
                coupling = 0.0
                if design == "B":
                    collapsed = []
                    for i, s in enumerate(states):
                        _, decided = thought.collapse(
                            s, seed=seed + 4242 + 1000 * g + 10 * i)
                        collapsed.append(np.asarray(decided,
                                                    dtype=complex))
                    states = collapsed
            r_post.append(ef.overlap_squared(states[0], states[1]))
            p1 = thought.born_probabilities(states[0])
            p2 = thought.born_probabilities(states[1])
            pooled += np.outer(p1, p2)
        pooled /= float(generations)
        arms[arm] = {
            "joint": pooled,
            "pid": pid_from_joint(pooled),
            "mean_r_pre": float(np.mean(r_pre)),
            "mean_r_post": float(np.mean(r_post)),
        }
    return {
        "n_agents": DEFAULT_N_AGENTS,
        "sigma": float(sigma),
        "generations": int(generations),
        "seed": int(seed),
        "design": design,
        "collaborating": arms["collaborating"],
        "isolated": arms["isolated"],
        "gap_bits": (arms["collaborating"]["pid"]["h_joint_bits"]
                     - arms["isolated"]["pid"]["h_joint_bits"]),
        "delta_synergistic_bits": (
            arms["collaborating"]["pid"]["synergistic_bits"]
            - arms["isolated"]["pid"]["synergistic_bits"]),
        "delta_redundant_bits": (
            arms["collaborating"]["pid"]["redundant_bits"]
            - arms["isolated"]["pid"]["redundant_bits"]),
        "delta_unique_bits": (
            (arms["collaborating"]["pid"]["unique1_bits"]
             + arms["collaborating"]["pid"]["unique2_bits"])
            - (arms["isolated"]["pid"]["unique1_bits"]
               + arms["isolated"]["pid"]["unique2_bits"])),
    }


def pid_gap_vs_noise(sigmas=None, seeds=ALL_SEEDS,
                     generations=DEFAULT_GENERATIONS, design="B"):
    """The PID gap decomposition per (seed, sigma)."""
    rows = []
    for seed in seeds:
        for sigma in (SIGMA_GRID if sigmas is None else sigmas):
            rows.append(pair_arm_distributions(
                sigma=sigma, generations=generations,
                seed=int(seed), design=design))
    return rows


# ---------------------------------------------------------------------------
# Claim verdicts (xl)-(xliii)
# ---------------------------------------------------------------------------

def claim_pid_identity_verdict(seeds=ALL_SEEDS, sigmas=None,
                               generations=DEFAULT_GENERATIONS,
                               design="B", sweep=None):
    """(xl) PID identity and sampled cross-check.

    PASS iff, for every seed, every sigma, and both arms:
    the four atoms sum to H_joint within
    PID_IDENTITY_TOL_BITS and every atom is at least
    PID_ATOM_MIN_BITS; AND at sigma = 0.25 the exact H
    agrees with the sampled run_collaboration (N = 2,
    design B) H within EXACT_SAMPLED_TOL_BITS.
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else pid_gap_vs_noise(
        sigmas, seeds, generations, design))
    worst_identity = 0.0
    worst_atom = 0.0
    checks = {}
    for row in rows:
        for arm in ("collaborating", "isolated"):
            pid = row[arm]["pid"]
            err = abs(pid["atom_sum_bits"] - pid["h_joint_bits"])
            worst_identity = max(worst_identity, err)
            worst_atom = min(worst_atom, pid["redundant_bits"],
                             pid["unique1_bits"], pid["unique2_bits"],
                             pid["synergistic_bits"])
    checks["atoms_sum_to_h_joint"] = (
        worst_identity <= t["identity_tol_bits"])
    checks["all_atoms_nonnegative"] = (
        worst_atom >= t["atom_min_bits"])
    cross = []
    worst_cross = 0.0
    for seed in seeds:
        exact = next(r for r in rows
                     if r["seed"] == int(seed)
                     and r["sigma"] == SIGMA_REF)
        sampled = ef.run_collaboration(
            n_agents=DEFAULT_N_AGENTS, sigma=SIGMA_REF,
            generations=generations, seed=int(seed), design=design)
        d_collab = abs(exact["collaborating"]["pid"]["h_joint_bits"]
                       - sampled["collaborating"]["h_joint_bits"])
        d_isol = abs(exact["isolated"]["pid"]["h_joint_bits"]
                     - sampled["isolated"]["h_joint_bits"])
        worst_cross = max(worst_cross, d_collab, d_isol)
        cross.append({
            "seed": int(seed),
            "exact_h_collaborating_bits":
                exact["collaborating"]["pid"]["h_joint_bits"],
            "sampled_h_collaborating_bits":
                sampled["collaborating"]["h_joint_bits"],
            "exact_h_isolated_bits":
                exact["isolated"]["pid"]["h_joint_bits"],
            "sampled_h_isolated_bits":
                sampled["isolated"]["h_joint_bits"],
            "diff_collaborating_bits": float(d_collab),
            "diff_isolated_bits": float(d_isol),
        })
    checks["exact_matches_sampled_h"] = (
        worst_cross <= t["exact_sampled_tol_bits"])
    passed = bool(all(checks.values()))
    return {
        "claim": "(xl) PID identity and sampled cross-check",
        "passed": passed,
        "checks": checks,
        "worst_identity_error_bits": float(worst_identity),
        "worst_atom_bits": float(worst_atom),
        "worst_exact_sampled_diff_bits": float(worst_cross),
        "identity_tol_bits": t["identity_tol_bits"],
        "atom_min_bits": t["atom_min_bits"],
        "exact_sampled_tol_bits": t["exact_sampled_tol_bits"],
        "cross_check_rows": cross,
    }


def claim_synergy_dominant_verdict(seeds=ALL_SEEDS,
                                   generations=DEFAULT_GENERATIONS,
                                   design="B", sweep=None):
    """(xli) The gap is synergy, not redundancy, at sigma = 0.25.

    PASS iff, on EVERY seed: delta-synergy exceeds
    delta-redundancy AND delta-synergy is at least
    SYNERGY_SHARE_MIN of the gap at sigma = 0.25.
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else pid_gap_vs_noise(
        (SIGMA_REF,), seeds, generations, design))
    per_seed = []
    checks = {}
    for seed in seeds:
        row = next(r for r in rows
                   if r["seed"] == int(seed)
                   and r["sigma"] == SIGMA_REF)
        gap = row["gap_bits"]
        d_syn = row["delta_synergistic_bits"]
        d_red = row["delta_redundant_bits"]
        share = d_syn / gap if gap != 0.0 else float("nan")
        per_seed.append({
            "seed": int(seed),
            "gap_bits": float(gap),
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
        "claim": "(xli) The gap is synergy, not redundancy, "
                 "at sigma = 0.25",
        "passed": passed,
        "checks": checks,
        "sigma": SIGMA_REF,
        "synergy_share_min": t["synergy_share_min"],
        "per_seed": per_seed,
    }


def claim_synergy_rises_falls_verdict(seeds=ALL_SEEDS, sigmas=None,
                                      generations=DEFAULT_GENERATIONS,
                                      design="B", sweep=None):
    """(xlii) Synergy rises with R and falls at sigma = 0.50.

    PASS iff, on EVERY seed: Pearson(synergy_collab,
    mean R_post) across the sigma grid is at least
    SYNERGY_R_PEARSON_MIN AND synergy_collab at sigma =
    0.50 is below synergy_collab at sigma = 0.25.
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else pid_gap_vs_noise(
        sigmas, seeds, generations, design))
    per_seed = []
    checks = {}
    for seed in seeds:
        sub = [r for r in rows if r["seed"] == int(seed)]
        sub.sort(key=lambda r: r["sigma"])
        syns = [r["collaborating"]["pid"]["synergistic_bits"]
                for r in sub]
        rs = [r["collaborating"]["mean_r_post"] for r in sub]
        pearson = sk.pearson(syns, rs)
        by_sigma = {r["sigma"]: r for r in sub}
        syn_025 = by_sigma[SIGMA_REF]["collaborating"]["pid"][
            "synergistic_bits"]
        syn_050 = by_sigma[SIGMA_HIGH]["collaborating"]["pid"][
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
        "claim": "(xlii) Synergy rises with R and falls at "
                 "sigma = 0.50",
        "passed": passed,
        "checks": checks,
        "synergy_r_pearson_min": t["synergy_r_pearson_min"],
        "per_seed": per_seed,
    }


def claim_redundancy_robust_verdict(seeds=ALL_SEEDS,
                                    generations=DEFAULT_GENERATIONS,
                                    design="B", sweep=None):
    """(xliii) Redundancy is sigma-robust.

    PASS iff, on EVERY seed: delta-redundancy at sigma =
    0.50 is at least ROBUST_RATIO_MIN of its sigma =
    0.25 value.
    """
    t = _thresholds()
    rows = (sweep if sweep is not None else pid_gap_vs_noise(
        (SIGMA_REF, SIGMA_HIGH), seeds, generations, design))
    per_seed = []
    checks = {}
    for seed in seeds:
        by_sigma = {r["sigma"]: r for r in rows
                    if r["seed"] == int(seed)}
        d_red_025 = by_sigma[SIGMA_REF]["delta_redundant_bits"]
        d_red_050 = by_sigma[SIGMA_HIGH]["delta_redundant_bits"]
        ratio = (d_red_050 / d_red_025 if d_red_025 != 0.0
                 else float("nan"))
        per_seed.append({
            "seed": int(seed),
            "delta_redundant_sigma_0.25_bits": float(d_red_025),
            "delta_redundant_sigma_0.50_bits": float(d_red_050),
            "robustness_ratio_050_over_025": float(ratio),
        })
        checks[f"seed_{seed}_redundancy_robust"] = bool(
            ratio >= t["robust_ratio_min"])
    passed = bool(all(checks.values()))
    return {
        "claim": "(xliii) Redundancy is sigma-robust",
        "passed": passed,
        "checks": checks,
        "robust_ratio_min": t["robust_ratio_min"],
        "per_seed": per_seed,
    }


def pid_claims():
    """The four PID claims (xl)-(xliii), measured fresh.

    One shared sweep over all seeds and sigmas feeds all
    four verdicts, so the evaluation run touches each
    held-out seed once. The N = 4 sampled gap at sigma =
    0.25, seed 42 (+4.3352 bits) is reported as context:
    the PID decomposes the pair-level gap, not the N = 4
    gap.
    """
    sweep = pid_gap_vs_noise()
    claim_xl = claim_pid_identity_verdict(sweep=sweep)
    claim_xli = claim_synergy_dominant_verdict(sweep=sweep)
    claim_xlii = claim_synergy_rises_falls_verdict(sweep=sweep)
    claim_xliii = claim_redundancy_robust_verdict(sweep=sweep)
    n4 = ef.run_collaboration(n_agents=4, sigma=SIGMA_REF,
                              seed=CALIBRATION_SEEDS[0], design="B")
    verdicts = [claim_xl, claim_xli, claim_xlii, claim_xliii]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_xl_pid_identity": claim_xl,
        "claim_xli_synergy_dominant": claim_xli,
        "claim_xlii_synergy_rises_falls": claim_xlii,
        "claim_xliii_redundancy_robust": claim_xliii,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
        "n4_sampled_gap_seed42_sigma025_bits": float(n4["gap_bits"]),
    }


def main():
    """Print the PID gap decomposition and the claims
    (xl)-(xliii) verdicts."""
    print("Synergy-vs-redundancy PID -- claims (xl)-(xliii)")
    print()
    verdicts = pid_claims()
    xl = verdicts["claim_xl_pid_identity"]
    print(f"worst identity error: {xl['worst_identity_error_bits']:.2e} "
          f"bits (tol {xl['identity_tol_bits']:.0e}); worst atom: "
          f"{xl['worst_atom_bits']:.4f} bits")
    print(f"worst exact-vs-sampled H diff at sigma = 0.25: "
          f"{xl['worst_exact_sampled_diff_bits']:.4f} bits "
          f"(tol {xl['exact_sampled_tol_bits']:.2f})")
    print(f"claim (xl) verdict: {'PASS' if xl['passed'] else 'FAIL'}")
    print()
    xli = verdicts["claim_xli_synergy_dominant"]
    for r in xli["per_seed"]:
        print(f"seed {r['seed']}: gap = {r['gap_bits']:+.4f}, "
              f"dSyn = {r['delta_synergistic_bits']:+.4f}, "
              f"dRed = {r['delta_redundant_bits']:+.4f}, "
              f"dUniq = {r['delta_unique_bits']:+.4f}, "
              f"synergy share = {r['synergy_share_of_gap']:.3f}")
    print(f"N = 4 sampled gap (context, seed 42, sigma = 0.25): "
          f"{verdicts['n4_sampled_gap_seed42_sigma025_bits']:+.4f} bits")
    print(f"claim (xli) verdict: {'PASS' if xli['passed'] else 'FAIL'}")
    print()
    xlii = verdicts["claim_xlii_synergy_rises_falls"]
    for r in xlii["per_seed"]:
        print(f"seed {r['seed']}: Pearson(Syn, R_post) = "
              f"{r['pearson_synergy_r_post']:+.4f}, Syn(0.25) = "
              f"{r['synergy_collab_sigma_0.25_bits']:.4f}, Syn(0.50) = "
              f"{r['synergy_collab_sigma_0.50_bits']:.4f}")
    print(f"claim (xlii) verdict: "
          f"{'PASS' if xlii['passed'] else 'FAIL'}")
    print()
    xliii = verdicts["claim_xliii_redundancy_robust"]
    for r in xliii["per_seed"]:
        print(f"seed {r['seed']}: dRed(0.25) = "
              f"{r['delta_redundant_sigma_0.25_bits']:+.4f}, "
              f"dRed(0.50) = "
              f"{r['delta_redundant_sigma_0.50_bits']:+.4f}, "
              f"ratio = {r['robustness_ratio_050_over_025']:.4f}")
    print(f"claim (xliii) verdict: "
          f"{'PASS' if xliii['passed'] else 'FAIL'}")
    print()
    print(f"claims (xl)-(xliii): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
