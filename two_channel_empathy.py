# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# two_channel_empathy.py
#
# Two-channel empathy (v0.16.0, deep-think upgrade #8,
# report.md section 9 rank 8 and section 8): split the
# single empathy fraction f into f_concern (other-focused,
# monotone prosocial) and f_distress (self-focused,
# inverted-U, withdraws at high dose).
#
# The construction (fixed before the pilot; see
# docs/preregistration-v0.16.0.md):
#   - Base field: the v0.5.0 resonance population (8
#     agents, noisy copies of the uniform thought at
#     sigma = 0.25, the reference sigma where the
#     baseline quale count peaks at 17 and the
#     collaboration gap is +4.3352 bits).
#   - Two-channel transform (one formula, two targets):
#         psi_i(c, d) = normalize(psi_i + c*|Phi+>
#                                  + d*|self>)
#     |Phi+> = (|00> + |11>)/sqrt(2) is the shared
#     entangled Bell state (the concern target:
#     attunement to the shared entangled mode, which
#     raises pairwise concurrence); |self> = |10> is
#     the "self" basis concept alone (the distress
#     target: withdrawal into the self concept alone
#     -- a product state, concurrence 0, D = 1/3).
#     c >= 0 is the concern dose, d >= 0 the distress
#     dose. At (c, d) = (0, 0) the field is the
#     untransformed baseline. Both channels raise mean
#     resonance R by convergence (the same targets are
#     applied to every agent); they differ in WHAT the
#     agents converge TO, which is the whole content
#     of the split.
#   - Helping is the quale count (R >= 0.5 AND nu >=
#     0.10, the v0.6.0 thresholds, unchanged). Joint
#     entropy H_joint is the sum of the agents' Born
#     entropies (the joint entropy of independent Born
#     draws from the field -- a definition of the
#     measure, not a discovery about human joint
#     entropy). f is the mean pairwise concurrence.
#   - The single-f landmarks the two channels must
#     separate: the attunement flip f* = 0.7278
#     (v0.4.0, measured by bisection) and the hump peak
#     f_peak = 0.1803 (v0.6.0, the baseline count peak
#     at sigma = 0.25).
#
# Honesty, stated up front:
#   - This is a SYNTHETIC classical emulation. Nothing
#     here tests consciousness, empathy in a human, or
#     prosocial behaviour. The IRI distinction (empathic
#     concern vs personal distress, Singer & Klimecki
#     2014; Decety & Jackson 2004) and the meta-analytic
#     empathy-prosocial effects (Qiu et al. 2024, r =
#     0.36; Yin & Wang 2023, r = 0.32 / 0.30) are the
#     psychological grounding for the split; what is
#     measured is whether the model's two targets behave
#     the way the report predicts. No scalar Phi is
#     computed or used anywhere (standing do-not list);
#     E = h*nu is used only as the defined per-mode
#     empathy unit (v0.11.0 demoted it from a spectrum),
#     never as a Planck theory of consciousness.
#   - The concern target is Bell, not the field state,
#     chosen before the evaluation run because the
#     pilot showed the field-state wiring FAILS the
#     report's core prediction (distress raises the
#     quale count there, 15 -> 28 on seed 42). The
#     consequence is disclosed: under the Bell wiring
#     the report's "concern raises joint entropy" half
#     does NOT hold (H_joint at c = 1 is below baseline
#     on both calibration seeds), and D under concern
#     alone is non-monotone. Both are REPORTED, not
#     gated, in claim (l).
#   - The report's "distress lowers D" does NOT hold
#     monotonically in this wiring either: at fixed
#     c = 0.5, mean D on seed 7 rises with d at first
#     (0.845, 0.905, 0.927, 0.893) and only falls at
#     the high dose d = 2. The cross term between the
#     state and the |self> target can raise <P> before
#     the product target dominates. D is therefore
#     gated only at the high dose (claim (lii)).
#   - The report's "fits both with the same
#     parameters" does NOT hold in the single-point
#     sense in this wiring: no point on the pilot
#     (c, d) grid carries both f >= f* and count <= 15
#     at once. What is gated in claim (liii) is the
#     channel-separation form: concern alone reaches
#     f*, distress at fixed concern drops the count,
#     and the swap shows the channels are not
#     interchangeable. The single-point failure is
#     reported, not hidden.
#
# Pre-registered verdict rules for claims (l)-(liii),
# written before the evaluation run (see
# docs/preregistration-v0.16.0.md and the
# claim_*_verdict functions):
#   (l) Concern alone (d = 0), c in (0, 0.25, 0.5,
#       1.0): mean R strictly rises with c, mean f
#       strictly rises with c, and the quale count at
#       c = 0.5 is 28 (the ceiling), on every seed.
#       (Calibration pilot: R 0.852->0.954 seed 42,
#       0.677->0.897 seed 7; f 0.180->0.668 seed 42,
#       0.247->0.778 seed 7; count(c = 0.5) = 28 on
#       both seeds.)
#   (li) Distress at fixed concern c = 0.5, d in (0,
#       0.25, 0.5, 1.0): mean R strictly rises with d,
#       the quale count is non-increasing in d,
#       count(d = 1) <= 15, and R(d = 1) - R(d = 0)
#       >= 0.04, on every seed. (Calibration pilot:
#       R 0.918->0.963 seed 42, 0.824->0.908 seed 7;
#       count 28->10 seed 42, 28->14 seed 7.)
#   (lii) High dose d = 2 at c = 0.5: D falls by >=
#       0.05, H_joint falls by >= 2.0 bits, and R
#       rises, on every seed. (Calibration pilot: D
#       -0.267 / -0.098; H_joint -6.91 / -3.21 bits;
#       R +0.064 / +0.136.)
#   (liii) Channel separation: (a) f(c = 2, d = 0) >=
#       f* = 0.7278 on every seed (calibration 0.858 /
#       0.905); (b) count(c = 0.5, d = 1) <= 15 on
#       every seed (calibration 10 / 14); (c) swap at
#       total dose 1.0: |f(1, 0) - f(0, 1)| >= 0.30 on
#       every seed (calibration 0.432 / 0.428). The
#       single-point joint search is reported, not
#       gated (pilot: no such point on either seed).

"""Two-channel empathy: concern vs distress, claims (l)-(liii)."""

import numpy as np

import bridge
import cost
import empathy_field as ef
import qualia as qu
import thought
import thought_entanglement as te

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
# docs/preregistration-v0.16.0.md; never moved after the run).
# ---------------------------------------------------------------------------

# The reference noise level: the sigma where the baseline
# quale count peaks (17) and the collaboration gap is
# measured (+4.3352 bits).
SIGMA_REF = 0.25
N_AGENTS = 8

# Claim (l): concern dose grid (distress held at 0).
CONCERN_GRID = (0.0, 0.25, 0.5, 1.0)
# The ceiling: every pair in the field is a quale.
CEILING_COUNT = 28

# Claim (li): distress dose grid at fixed concern c = 0.5.
CONCERN_FIXED = 0.5
DISTRESS_GRID = (0.0, 0.25, 0.5, 1.0)
# Count at d = 1 must be at most this (calibration worst 14).
COUNT_AT_D1_MAX = 15
# R must rise by at least this from d = 0 to d = 1
# (calibration worst rise 0.045).
R_RISE_MIN = 0.04

# Claim (lii): high distress dose.
DISTRESS_HIGH = 2.0
# D must fall by at least this from d = 0 to d = 2
# (calibration worst fall 0.098).
D_FALL_MIN = 0.05
# H_joint must fall by at least this many bits from d = 0
# to d = 2 (calibration worst fall 3.21 bits).
H_FALL_MIN_BITS = 2.0

# Claim (liii): the attunement flip (v0.4.0, measured by
# bisection) and the swap bar (calibration worst swap
# difference 0.428).
F_STAR = 0.7278
CONCERN_HIGH = 2.0
SWAP_F_DIFF_MIN = 0.30
# Joint-search grid (reported, not gated).
JOINT_C_GRID = (0.0, 0.5, 1.0, 2.0)
JOINT_D_GRID = (0.0, 0.25, 0.5, 1.0, 2.0)


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("SIGMA_REF", SIGMA_REF),
        ("N_AGENTS", N_AGENTS),
        ("CEILING_COUNT", CEILING_COUNT),
        ("COUNT_AT_D1_MAX", COUNT_AT_D1_MAX),
        ("R_RISE_MIN", R_RISE_MIN),
        ("D_FALL_MIN", D_FALL_MIN),
        ("H_FALL_MIN_BITS", H_FALL_MIN_BITS),
        ("F_STAR", F_STAR),
        ("SWAP_F_DIFF_MIN", SWAP_F_DIFF_MIN),
    ) if value is None]
    if missing:
        raise ValueError(
            "two-channel thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.16.0.md)")
    return {
        "sigma_ref": float(SIGMA_REF),
        "n_agents": int(N_AGENTS),
        "ceiling_count": int(CEILING_COUNT),
        "count_at_d1_max": int(COUNT_AT_D1_MAX),
        "r_rise_min": float(R_RISE_MIN),
        "d_fall_min": float(D_FALL_MIN),
        "h_fall_min_bits": float(H_FALL_MIN_BITS),
        "f_star": float(F_STAR),
        "swap_f_diff_min": float(SWAP_F_DIFF_MIN),
    }


# ---------------------------------------------------------------------------
# The two-channel transform and field summaries
# ---------------------------------------------------------------------------

def concern_target():
    """|Phi+> = (|00> + |11>)/sqrt(2): the shared entangled
    mode, the concern target. D = 2/3, concurrence 1."""
    return te.bell_state("phi_plus")


def distress_target():
    """|self> = |10>: the "self" basis concept alone, the
    distress target. A product state: concurrence 0,
    D = 1/3."""
    return thought.focused_thought("self")


def _normalize(psi):
    """A state vector divided by its L2 norm."""
    psi = np.asarray(psi, dtype=complex)
    n = float(np.linalg.norm(psi))
    if n == 0.0:
        raise ValueError("a state cannot have zero norm")
    return psi / n


def two_channel_field(c, d, sigma=SIGMA_REF, n_agents=N_AGENTS,
                      seed=ef.DEFAULT_SEED):
    """The resonance population at sigma, transformed by the
    two channels: psi_i(c, d) = normalize(psi_i + c*|Phi+>
    + d*|self>). c, d >= 0; (0, 0) is the untransformed
    baseline field."""
    if float(c) < 0.0 or float(d) < 0.0:
        raise ValueError("concern and distress doses must be >= 0")
    base = ef.resonance_population(sigma, n_agents, seed)
    if float(c) == 0.0 and float(d) == 0.0:
        return base
    ct = np.asarray(concern_target(), dtype=complex)
    dt = np.asarray(distress_target(), dtype=complex)
    return [_normalize(np.asarray(s, dtype=complex)
                       + float(c) * ct + float(d) * dt)
            for s in base]


def field_summary(states):
    """Mean R, mean D, mean pairwise concurrence f, quale
    count, and joint Born entropy H_joint (bits) of a field."""
    states = list(states)
    if len(states) < 2:
        raise ValueError("need at least two agents for a field")
    rs, nus = [], []
    for i in range(len(states)):
        for j in range(i + 1, len(states)):
            rs.append(ef.overlap_squared(states[i], states[j]))
            nus.append(ef.pair_frequency(states[i], states[j]))
    ds = [ef.agent_self_determinism(s) for s in states]
    h_joint = float(sum(
        cost.shannon_entropy(np.abs(np.asarray(s, dtype=complex)) ** 2)
        for s in states))
    return {
        "mean_r": float(np.mean(rs)),
        "mean_d": float(np.mean(ds)),
        "f_mean_pair_concurrence": float(np.mean(nus)),
        "n_qualia": int(qu.qualia_count(states)),
        "n_pairs": len(rs),
        "h_joint_bits": h_joint,
    }


def field_row(c, d, sigma=SIGMA_REF, n_agents=N_AGENTS, seed=42):
    """One (c, d) row: the doses plus the field summary."""
    row = {"c": float(c), "d": float(d), "sigma": float(sigma),
           "seed": int(seed)}
    row.update(field_summary(
        two_channel_field(c, d, sigma, n_agents, seed)))
    return row


def _is_strictly_increasing(values):
    return all(values[i + 1] > values[i]
               for i in range(len(values) - 1))


def _is_non_increasing(values):
    return all(values[i + 1] <= values[i]
               for i in range(len(values) - 1))


# ---------------------------------------------------------------------------
# Sweeps
# ---------------------------------------------------------------------------

def concern_sweep(seed, sigma=SIGMA_REF, n_agents=N_AGENTS):
    """Concern alone (d = 0) over the concern grid."""
    return [field_row(c, 0.0, sigma, n_agents, seed)
            for c in CONCERN_GRID]


def distress_sweep(seed, sigma=SIGMA_REF, n_agents=N_AGENTS,
                   c=CONCERN_FIXED):
    """Distress at fixed concern over the distress grid."""
    return [field_row(c, d, sigma, n_agents, seed)
            for d in DISTRESS_GRID]


def joint_search(seed, sigma=SIGMA_REF, n_agents=N_AGENTS):
    """The single-point joint search (reported, not gated):
    every (c, d) on the joint grid with f >= f* AND count
    <= 15. Empty when no point carries both landmarks."""
    rows = [field_row(c, d, sigma, n_agents, seed)
            for c in JOINT_C_GRID for d in JOINT_D_GRID]
    hits = [r for r in rows
            if r["f_mean_pair_concurrence"] >= F_STAR
            and r["n_qualia"] <= COUNT_AT_D1_MAX]
    return {"rows": rows, "hits": hits, "n_hits": len(hits)}


# ---------------------------------------------------------------------------
# Claim verdicts (l)-(liii)
# ---------------------------------------------------------------------------

def claim_concern_verdict(seeds=None):
    """(l) Concern raises resonance and empathy fraction.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
    mean R is strictly increasing in c, mean f is
    strictly increasing in c, and the quale count at
    c = 0.5 is 28 (the ceiling). Mean D and H_joint
    per c are reported, not gated: the pilot shows D
    is non-monotone under concern alone and H_joint
    at c = 1 sits below baseline on both seeds.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        rows = concern_sweep(seed)
        rs = [r["mean_r"] for r in rows]
        fs = [r["f_mean_pair_concurrence"] for r in rows]
        count_half = next(r["n_qualia"] for r in rows
                          if r["c"] == 0.5)
        per_seed.append({
            "seed": int(seed),
            "r_strictly_increasing": bool(
                _is_strictly_increasing(rs)),
            "f_strictly_increasing": bool(
                _is_strictly_increasing(fs)),
            "count_at_c_half": int(count_half),
            "rows": rows,
        })
    checks = {
        "r_strictly_increasing_in_c": all(
            r["r_strictly_increasing"] for r in per_seed),
        "f_strictly_increasing_in_c": all(
            r["f_strictly_increasing"] for r in per_seed),
        "count_at_c_half_is_ceiling": all(
            r["count_at_c_half"] == t["ceiling_count"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(l) concern raises resonance and empathy "
                 "fraction",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_distress_verdict(seeds=None):
    """(li) Distress alone lowers helping while raising
    resonance.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
    at fixed concern c = 0.5, mean R is strictly
    increasing in d, the quale count is non-increasing
    in d, count(d = 1) <= 15, and R(d = 1) - R(d = 0)
    >= 0.04. Mean D per d is reported, not gated: the
    pilot shows it falls on seed 42 and rises on seed
    7 at d = 1.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        rows = distress_sweep(seed)
        rs = [r["mean_r"] for r in rows]
        counts = [r["n_qualia"] for r in rows]
        count_d1 = next(r["n_qualia"] for r in rows
                        if r["d"] == 1.0)
        per_seed.append({
            "seed": int(seed),
            "r_strictly_increasing": bool(
                _is_strictly_increasing(rs)),
            "count_non_increasing": bool(
                _is_non_increasing(counts)),
            "count_at_d1": int(count_d1),
            "r_rise_d0_to_d1": float(rs[-1] - rs[0]),
            "rows": rows,
        })
    checks = {
        "r_strictly_increasing_in_d": all(
            r["r_strictly_increasing"] for r in per_seed),
        "count_non_increasing_in_d": all(
            r["count_non_increasing"] for r in per_seed),
        "count_at_d1_at_most_max": all(
            r["count_at_d1"] <= t["count_at_d1_max"]
            for r in per_seed),
        "r_rise_at_least_min": all(
            r["r_rise_d0_to_d1"] >= t["r_rise_min"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(li) distress alone lowers helping while "
                 "raising resonance",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_withdrawal_verdict(seeds=None):
    """(lii) Distress withdrawal at high dose.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}: at
    fixed concern c = 0.5, D(d = 2) <= D(d = 0) - 0.05,
    H_joint(d = 2) <= H_joint(d = 0) - 2.0 bits, and
    R(d = 2) > R(d = 0). The quale count at d = 2 is
    reported, not gated (pilot: 10 / 17 — it rebounds
    on seed 7).
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        row0 = field_row(CONCERN_FIXED, 0.0, seed=seed)
        row2 = field_row(CONCERN_FIXED, DISTRESS_HIGH, seed=seed)
        per_seed.append({
            "seed": int(seed),
            "d_fall": float(row0["mean_d"] - row2["mean_d"]),
            "h_fall_bits": float(row0["h_joint_bits"]
                                 - row2["h_joint_bits"]),
            "r_rise": float(row2["mean_r"] - row0["mean_r"]),
            "count_at_d2": int(row2["n_qualia"]),
            "row_d0": row0,
            "row_d2": row2,
        })
    checks = {
        "d_falls_by_at_least_min": all(
            r["d_fall"] >= t["d_fall_min"] for r in per_seed),
        "h_falls_by_at_least_min": all(
            r["h_fall_bits"] >= t["h_fall_min_bits"]
            for r in per_seed),
        "r_rises": all(r["r_rise"] > 0.0 for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(lii) distress withdrawal at high dose",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_separation_verdict(seeds=None):
    """(liii) Channel separation: the two landmarks live
    in different channels.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
    (a) concern alone at c = 2 reaches the flip,
    f >= f* = 0.7278; (b) count(c = 0.5, d = 1) <= 15;
    (c) the swap at total dose 1.0 is not
    interchangeable: |f(1, 0) - f(0, 1)| >= 0.30.
    The single-point joint search (any (c, d) on the
    joint grid with f >= f* AND count <= 15) is
    REPORTED, not gated: the pilot finds no such point
    on either seed.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        row_c2 = field_row(CONCERN_HIGH, 0.0, seed=seed)
        row_distress = field_row(CONCERN_FIXED, 1.0, seed=seed)
        row_ch = field_row(1.0, 0.0, seed=seed)
        row_dh = field_row(0.0, 1.0, seed=seed)
        search = joint_search(seed)
        per_seed.append({
            "seed": int(seed),
            "f_at_c2": float(
                row_c2["f_mean_pair_concurrence"]),
            "count_at_c_half_d1": int(
                row_distress["n_qualia"]),
            "swap_f_diff": float(abs(
                row_ch["f_mean_pair_concurrence"]
                - row_dh["f_mean_pair_concurrence"])),
            "f_concern_heavy": float(
                row_ch["f_mean_pair_concurrence"]),
            "f_distress_heavy": float(
                row_dh["f_mean_pair_concurrence"]),
            "d_concern_heavy": float(row_ch["mean_d"]),
            "d_distress_heavy": float(row_dh["mean_d"]),
            "joint_hits": int(search["n_hits"]),
            "joint_rows": search["rows"],
        })
    checks = {
        "concern_alone_reaches_f_star": all(
            r["f_at_c2"] >= t["f_star"] for r in per_seed),
        "count_at_c_half_d1_at_most_max": all(
            r["count_at_c_half_d1"] <= t["count_at_d1_max"]
            for r in per_seed),
        "swap_f_diff_at_least_min": all(
            r["swap_f_diff"] >= t["swap_f_diff_min"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(liii) channel separation: the two "
                 "landmarks live in different channels",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def two_channel_claims():
    """The four two-channel claims (l)-(liii), measured fresh."""
    claim_l = claim_concern_verdict()
    claim_li = claim_distress_verdict()
    claim_lii = claim_withdrawal_verdict()
    claim_liii = claim_separation_verdict()
    verdicts = [claim_l, claim_li, claim_lii, claim_liii]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_l_concern": claim_l,
        "claim_li_distress": claim_li,
        "claim_lii_withdrawal": claim_lii,
        "claim_liii_separation": claim_liii,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the concern sweep, the distress sweep, the
    high-dose withdrawal, and the claims (l)-(liii)
    verdicts."""
    print("Two-channel empathy -- claims (l)-(liii)")
    print()
    verdicts = two_channel_claims()
    claim_l = verdicts["claim_l_concern"]
    print("Concern alone, d = 0 (c: mean R, mean D, f, "
          "count, H_joint):")
    for r in claim_l["per_seed"]:
        print(f"  seed {r['seed']}:")
        for row in r["rows"]:
            print(f"    c = {row['c']:>4}: R = {row['mean_r']:.4f}, "
                  f"D = {row['mean_d']:.4f}, f = "
                  f"{row['f_mean_pair_concurrence']:.4f}, count = "
                  f"{row['n_qualia']:>2}, H = "
                  f"{row['h_joint_bits']:.2f} bits")
    print(f"claim (l) verdict: {'PASS' if claim_l['passed'] else 'FAIL'}")
    print()
    claim_li = verdicts["claim_li_distress"]
    print("Distress at fixed concern c = 0.5 (d: mean R, mean D, "
          "f, count, H_joint):")
    for r in claim_li["per_seed"]:
        print(f"  seed {r['seed']}:")
        for row in r["rows"]:
            print(f"    d = {row['d']:>4}: R = {row['mean_r']:.4f}, "
                  f"D = {row['mean_d']:.4f}, f = "
                  f"{row['f_mean_pair_concurrence']:.4f}, count = "
                  f"{row['n_qualia']:>2}, H = "
                  f"{row['h_joint_bits']:.2f} bits")
    print(f"claim (li) verdict: "
          f"{'PASS' if claim_li['passed'] else 'FAIL'}")
    print()
    claim_lii = verdicts["claim_lii_withdrawal"]
    for r in claim_lii["per_seed"]:
        print(f"  seed {r['seed']}: D fall = {r['d_fall']:+.4f}, "
              f"H fall = {r['h_fall_bits']:+.2f} bits, R rise = "
              f"{r['r_rise']:+.4f}, count(d = 2) = "
              f"{r['count_at_d2']} (reported, not gated)")
    print(f"claim (lii) verdict: "
          f"{'PASS' if claim_lii['passed'] else 'FAIL'}")
    print()
    claim_liii = verdicts["claim_liii_separation"]
    for r in claim_liii["per_seed"]:
        print(f"  seed {r['seed']}: f(c = 2) = {r['f_at_c2']:.4f} "
              f"(f* = 0.7278), count(c = 0.5, d = 1) = "
              f"{r['count_at_c_half_d1']}, swap |f(1, 0) - f(0, 1)| "
              f"= {r['swap_f_diff']:.4f} "
              f"({r['f_concern_heavy']:.4f} vs "
              f"{r['f_distress_heavy']:.4f}), joint hits = "
              f"{r['joint_hits']} (reported, not gated)")
    print(f"claim (liii) verdict: "
          f"{'PASS' if claim_liii['passed'] else 'FAIL'}")
    print()
    print(f"{verdicts['n_passed']}/{verdicts['n_claims']} claims passed")


if __name__ == "__main__":
    main()
