# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Seed-1234 diagnosis (v0.21.0, Job 2): why one seed keeps breaking claims.

Seed 1234 is the seed that breaks claims in three builds:

  (a) v0.16.0 two-channel empathy (l), (li), (liii): all three
      failures sit on seed 1234 (only (lii) passes there).
      Its baseline empathy fraction is f = 0.3251, nearly
      double the other seeds' (0.1803 / 0.2469 / 0.1772).
      Mean R never breaks -- it is strictly rising in every
      sweep on every seed.
  (b) v0.19.0 Cogitate (lx): failed on held-out seed 1234 --
      mean_D beats mean_R there (r = 0.8839 vs 0.8447,
      margin -0.0393 against the frozen 0.10 bar).
  (c) v0.20.0 XOR target (lxv): failed on held-out seed 1234 --
      delta-I = -0.2591 bits (I_isol 1.7610 > I_collab
      1.5019), so the share-of-gap criterion was meaningless.
  (d) v0.21.0 MAX target: the first in the series to CLEAR
      seed 1234 (delta-I = +0.3266 at sigma = 0.25), but
      with the smallest held-out gaps (0.33 / 0.65 vs
      calibration 1.89 / 1.07).

Verdict (measured here, not assumed): the anomalies are
INDEPENDENT. There is no one common mechanism, no
generation-0 spike, and no threshold that seed 1234
crosses. Three separate draw-level mechanisms coincide
on the same seed:

  1. Two-channel: the baseline pair-state determinant
     ad - bc. Concurrence is 2|ad - bc| (the uniform
     thought has det = 0). On seed 1234, 26 of 28
     baseline pairs have det < 0 (mean -0.1556, median
     -0.1559); on the other seeds the mean det is
     -0.0431 / +0.1050 / +0.0101. The concern target
     |Phi+> adds to a and d, so it pushes det UP: on a
     negative-det pair det first crosses zero and
     concurrence FALLS (21 of 26 negative-det pairs
     fall at c = 0.25, mean change -0.2084), while the
     distress target |self> = |10> adds to c, pushing
     det further negative, so concurrence RISES
     (f(0, 1) = 0.5374, the highest distress f on any
     seed). The per-pair sign rule is exact in one
     direction on every file seed: NO pair with det
     >= 0 ever falls under concern, and NO pair with
     det < 0 ever falls under distress. The U-shaped
     f(c, 0) on 1234 (0.3251 -> 0.1505 -> 0.2788 ->
     0.5879) and the re-rising distress count (24 ->
     17 -> 14 -> 23) are both this one sign effect.
  2. Cogitate: the mean_D-vs-sigma TRAJECTORY shape.
     On seed 1234 mean_D is hump-shaped like the gap
     (0.6274 -> 0.6345 -> 0.6551 -> 0.6593 -> 0.5922
     -> 0.5580 -> 0.4775, peaking at sigma = 0.10
     where the gap also peaks), so r(gap, mean_D) =
     0.8839 -- the second-highest mean_D correlation
     in a 12-seed survey (seed 31337: 0.8969). On the
     other file seeds mean_D is flat (42) or U-shaped
     (7: 0.6274 -> 0.3158 -> 0.4552; 2026: 0.6274 ->
     0.1975 -> 0.5720), so it predicts the gap badly
     there (r = 0.7776 / 0.6477 / 0.3430). Mean_R, by
     contrast, is unremarkable on 1234 (r = 0.8447,
     inside the file-seed range 0.8422-0.9028). The
     (lx) failure is a narrow margin failure (-0.0393)
     of a claim that is seed-fragile in general: in
     the 12-seed survey the 0.10 margin FAILS on 6 of
     12 seeds (1: -0.0206, 2: +0.0561, 1234: -0.0393,
     777: +0.0025, 2024: +0.0375, 31337: +0.0916), and
     r(mean_R) itself falls to 0.38-0.50 on seeds 1-3.
  3. XOR: a DISCRETE switch pattern in the isolated
     arm plus a concentrated collaborating arm. The
     isolated pooled joint is a mixture of 10
     per-generation point masses, so its information
     takes discrete values set by the concept-count
     table. On seed 1234 at sigma = 0.25 BOTH agents
     switch collapsed concepts mid-run at staggered
     times (agent 0: 3 x8 then 1 x2; agent 1: 3 x5,
     1 x2, 2 x3), giving a 4-cell joint (counts
     5/2/1/2) with I_isol = 1.7610 -- the highest
     isolated-arm XOR value on any file seed at
     sigma = 0.25, while calibration seeds have
     2-cell joints (I_isol = 0.7219). At the same
     sigma the collaborating pair is the most
     concentrated on any file seed (mean R_pre =
     0.526, the highest; marginal entropies 1.281 /
     1.213 bits, the lowest), so I_collab = 1.5019
     is the lowest. Neither half alone flips the
     sign; the flip needs both. The MAX target
     clears 1234 for the mirror-image reason: the
     same concentrated collaborating pair gives
     I_collab(MAX) = 1.0485 (lowest), but the
     isolated MAX value is only 0.7219 -- the max
     of the same count table collapses to two
     values (3 x7, 2 x3) -- so the gap stays
     positive (+0.3266), the smallest on any seed.

Refuted hypotheses (measured, see docs/seed-1234-diagnosis.md):

  - Generation-0 spike: gen-0 coupling on seed 1234
    is the LOWEST of the four file seeds (0.3656 vs
    0.5281 / 0.4703 / 0.3903 at sigma = 0.25), and
    its coupling trajectory is the flattest
    (0.28-0.61). At sigma = 0 all seeds are identical
    by construction (the base population is
    deterministic at zero noise).
  - A threshold at baseline f: no landmark sits near
    f = 0.3251 (quale-count peak f_peak = 0.1803,
    attunement flip f* = 0.7278), and f(sigma) on
    1234 is the highest of the four file seeds at
    every sigma in (0, 0.25] (at sigma = 0.50 and
    1.00 seed 7 overtakes it: 0.508 / 0.522 vs
    0.472 / 0.507), smoothly, with no crossing.
  - One common mechanism: the three statistics are
    uncorrelated across a 12-seed diagnostic survey
    (Pearson(f0, XOR delta-I) and Pearson(f0,
    Cogitate margin) are both small in magnitude;
    the survey seeds reach each extreme separately --
    e.g. seed 777 has the largest XOR delta-I,
    +1.9952, with a near-zero Cogitate margin,
    +0.0025). The three mechanisms live in different
    populations fed by independent RNG streams
    (resonance population seeded by `seed`; the
    collaboration population by `seed + i`; the
    kicks by `seed + 1000*g + 10*i`; the collapses
    by `seed + 4242 + 1000*g + 10*i`), so no shared
    variable can carry one cause across all three.

Honesty, stated up front:
  - This is a SYNTHETIC, CLASSICAL emulation. Nothing
    here measures consciousness, empathy in a human,
    or any theory of consciousness. No scalar Phi is
    computed anywhere and none is presented as a
    consciousness measure (standing do-not list);
    E = h*nu is used only as the defined per-mode
    empathy unit (v0.11.0), never as a Planck theory
    of consciousness.
  - The diagnosis is descriptive, not causal in a
    physical sense: a "seed" is an RNG-stream label,
    and the mechanisms are properties of the draws
    from those streams. "Seed 1234 is extreme" means
    its draws sit in the tail of the surveyed
    seed distribution on these statistics -- the
    12-seed survey is diagnostic only, not a claim
    about all seeds.
  - The extra survey seeds (1, 2, 3, 99, 123, 777,
    2024, 31337) are diagnostics run AFTER the
    evaluation claims were frozen; they change no
    threshold and no verdict in v0.16.0-v0.21.0.
"""

import math

import numpy as np

import cogitate as cg
import cost
import empathy_field as ef
import pid
import synergistic_target as st
import thought
import total_information_target as tt
import two_channel_empathy as tc

# ---------------------------------------------------------------------------
# Seeds
# ---------------------------------------------------------------------------

FILE_SEEDS = (42, 7, 1234, 2026)
# Diagnostic survey seeds (not claims seeds): chosen before
# the survey run as small integers plus the seed already used
# in tests (99) and a large one (31337). They change no
# threshold and no verdict.
SURVEY_SEEDS = FILE_SEEDS + (1, 2, 3, 99, 123, 777, 2024, 31337)
SIGMA_REF = 0.25
N_RESONANCE = 8


# ---------------------------------------------------------------------------
# 1. Baseline resonance field and the pair determinant
# ---------------------------------------------------------------------------

def pair_determinant(psi_i, psi_j):
    """det = a*d - b*c of the normalized pair state.

    The pair state is the normalized sum of the two
    agents; concurrence is 2|det| (thought_entanglement
    .concurrence_pure). The uniform thought has det = 0
    exactly, so every nonzero det is noise-made.
    """
    ps = ef.pair_state(psi_i, psi_j)
    a, b, c, d = (complex(x) for x in ps)
    return float(np.real(a * d - b * c))


def baseline_field(seed, sigma=SIGMA_REF, n_agents=N_RESONANCE):
    """Baseline resonance field summary + determinant stats.

    field_summary is the two-channel summary (mean R,
    mean D, f, quale count, H_joint); the determinant
    stats are the per-pair det distribution, and the
    per-agent Born concentration (max probability and
    entropy) that shows which agent, if any, is peaked.
    """
    states = ef.resonance_population(sigma, n_agents, seed)
    summary = tc.field_summary(states)
    dets = [pair_determinant(states[i], states[j])
            for i in range(len(states))
            for j in range(i + 1, len(states))]
    dets = np.asarray(dets, dtype=float)
    born_max = [float(max(thought.born_probabilities(s)))
                for s in states]
    born_h = [float(cost.shannon_entropy(
        thought.born_probabilities(s))) for s in states]
    ds = [ef.agent_self_determinism(s) for s in states]
    return {
        "seed": int(seed),
        "sigma": float(sigma),
        "n_agents": int(n_agents),
        "mean_r": summary["mean_r"],
        "mean_d": summary["mean_d"],
        "f_baseline": summary["f_mean_pair_concurrence"],
        "n_qualia": summary["n_qualia"],
        "h_joint_bits": summary["h_joint_bits"],
        "det_mean": float(np.mean(dets)),
        "det_median": float(np.median(dets)),
        "det_min": float(np.min(dets)),
        "det_max": float(np.max(dets)),
        "n_det_negative": int(np.sum(dets < 0.0)),
        "n_det_positive": int(np.sum(dets > 0.0)),
        "n_pairs": int(len(dets)),
        "d_min": float(min(ds)),
        "d_max": float(max(ds)),
        "born_max_prob": born_max,
        "born_entropy_bits": born_h,
    }


def baseline_f_vs_sigma(seed, n_agents=N_RESONANCE):
    """Baseline f on the sigma grid (the threshold test)."""
    return [float(ef.empathy_fraction(
        ef.resonance_population(sigma, n_agents, seed)))
        for sigma in ef.SIGMA_GRID]


# ---------------------------------------------------------------------------
# 2. The determinant mechanism: per-pair transform response
# ---------------------------------------------------------------------------

def pair_transform_response(seed, sigma=SIGMA_REF,
                            n_agents=N_RESONANCE, dose=0.25):
    """Per-pair concurrence change under each channel.

    For every pair: baseline det and f, the change in
    pairwise concurrence when the concern dose (c =
    dose, d = 0) is applied to both agents, and the
    change when the distress dose (c = 0, d = dose)
    is applied. The mechanism predicts the sign rule:
    a negative-det pair falls under concern (the
    |Phi+> addition pushes det up through zero) and
    rises under distress (the |self> addition pushes
    det further negative); a positive-det pair does
    the reverse. Aggregates count how often each
    direction of the rule holds.
    """
    base = ef.resonance_population(sigma, n_agents, seed)
    ct = np.asarray(tc.concern_target(), dtype=complex)
    dt = np.asarray(tc.distress_target(), dtype=complex)
    rows = []
    for i in range(len(base)):
        for j in range(i + 1, len(base)):
            det = pair_determinant(base[i], base[j])
            f0 = ef.pair_frequency(base[i], base[j])
            ci = tc._normalize(
                np.asarray(base[i], dtype=complex) + dose * ct)
            cj = tc._normalize(
                np.asarray(base[j], dtype=complex) + dose * ct)
            fc = ef.pair_frequency(ci, cj)
            di = tc._normalize(
                np.asarray(base[i], dtype=complex) + dose * dt)
            dj = tc._normalize(
                np.asarray(base[j], dtype=complex) + dose * dt)
            fd = ef.pair_frequency(di, dj)
            rows.append({
                "i": i, "j": j,
                "det": float(det),
                "f_baseline": float(f0),
                "delta_f_concern": float(fc - f0),
                "delta_f_distress": float(fd - f0),
            })
    neg = [r for r in rows if r["det"] < 0.0]
    pos = [r for r in rows if r["det"] >= 0.0]

    def _frac(rs, key):
        if not rs:
            return None
        return float(sum(1 for r in rs if r[key] < 0.0) / len(rs))

    def _mean(rs, key):
        if not rs:
            return None
        return float(sum(r[key] for r in rs) / len(rs))

    return {
        "seed": int(seed),
        "sigma": float(sigma),
        "dose": float(dose),
        "rows": rows,
        "n_pairs": len(rows),
        "n_det_negative": len(neg),
        "n_det_positive": len(pos),
        "frac_neg_det_fall_under_concern": _frac(
            neg, "delta_f_concern"),
        "frac_pos_det_fall_under_concern": _frac(
            pos, "delta_f_concern"),
        "frac_neg_det_fall_under_distress": _frac(
            neg, "delta_f_distress"),
        "frac_pos_det_fall_under_distress": _frac(
            pos, "delta_f_distress"),
        "mean_delta_f_concern_neg_det": _mean(
            neg, "delta_f_concern"),
        "mean_delta_f_concern_pos_det": _mean(
            pos, "delta_f_concern"),
        "mean_delta_f_distress_neg_det": _mean(
            neg, "delta_f_distress"),
        "mean_delta_f_distress_pos_det": _mean(
            pos, "delta_f_distress"),
    }


def distress_only_sweep(seed, sigma=SIGMA_REF, n_agents=N_RESONANCE):
    """f(0, d) for d in the distress grid: the mirror image.

    The module's sweeps only cover distress at fixed
    concern c = 0.5; this sweep isolates the distress
    channel (c = 0), which is what the determinant
    mechanism predicts will RISE on a negative-det
    seed (seed 1234) and dip on a positive-det seed
    (seed 7).
    """
    doses = (0.0, 0.25, 0.5, 1.0, 2.0)
    return [{
        "d": float(d),
        "f": float(tc.field_summary(
            tc.two_channel_field(0.0, d, sigma, n_agents, seed))
            ["f_mean_pair_concurrence"]),
    } for d in doses]


# ---------------------------------------------------------------------------
# 3. Two-channel failures, per seed (reused verdicts)
# ---------------------------------------------------------------------------

def two_channel_failures(seeds=FILE_SEEDS):
    """Which two-channel sub-checks fail, on which seed.

    Reuses the v0.16.0 verdict functions and reports the
    failing sub-checks with their measured values, so the
    diagnosis states exactly what broke where instead of
    "seed 1234 fails (l), (li), (liii)".
    """
    verdicts = {
        "l": tc.claim_concern_verdict(),
        "li": tc.claim_distress_verdict(),
        "lii": tc.claim_withdrawal_verdict(),
        "liii": tc.claim_separation_verdict(),
    }
    per_seed = {}
    for seed in seeds:
        failures = {}
        for name, v in verdicts.items():
            row = next(r for r in v["per_seed"]
                       if r["seed"] == int(seed))
            failed = [k for k, ok in v["checks"].items()
                      if not ok] if not v["passed"] else []
            # Per-seed failure: a check fails globally only
            # because of some seed; recompute per-seed from
            # the row so each seed carries its own verdict.
            if name == "l":
                own = []
                if not row["r_strictly_increasing"]:
                    own.append("r_strictly_increasing_in_c")
                if not row["f_strictly_increasing"]:
                    own.append("f_strictly_increasing_in_c")
                if row["count_at_c_half"] != 28:
                    own.append("count_at_c_half_is_ceiling")
                failures[name] = {
                    "passed": not own,
                    "failed_checks": own,
                    "count_at_c_half": row["count_at_c_half"],
                    "f_concern": [round(r["f_mean_pair_concurrence"], 4)
                                  for r in row["rows"]],
                }
            elif name == "li":
                own = []
                if not row["r_strictly_increasing"]:
                    own.append("r_strictly_increasing_in_d")
                if not row["count_non_increasing"]:
                    own.append("count_non_increasing_in_d")
                if row["count_at_d1"] > 15:
                    own.append("count_at_d1_at_most_max")
                if row["r_rise_d0_to_d1"] < 0.04:
                    own.append("r_rise_at_least_min")
                failures[name] = {
                    "passed": not own,
                    "failed_checks": own,
                    "count_at_d1": row["count_at_d1"],
                    "counts": [r["n_qualia"] for r in row["rows"]],
                    "f_distress": [round(r["f_mean_pair_concurrence"], 4)
                                   for r in row["rows"]],
                }
            elif name == "lii":
                own = []
                if row["d_fall"] < 0.05:
                    own.append("d_falls_by_at_least_min")
                if row["h_fall_bits"] < 2.0:
                    own.append("h_falls_by_at_least_min")
                if row["r_rise"] <= 0.0:
                    own.append("r_rises")
                failures[name] = {
                    "passed": not own,
                    "failed_checks": own,
                    "d_fall": round(row["d_fall"], 4),
                    "h_fall_bits": round(row["h_fall_bits"], 4),
                    "r_rise": round(row["r_rise"], 4),
                    "count_at_d2": row["count_at_d2"],
                }
            elif name == "liii":
                own = []
                if row["f_at_c2"] < 0.7278:
                    own.append("concern_alone_reaches_f_star")
                if row["count_at_c_half_d1"] > 15:
                    own.append("count_at_c_half_d1_at_most_max")
                if row["swap_f_diff"] < 0.30:
                    own.append("swap_f_diff_at_least_min")
                failures[name] = {
                    "passed": not own,
                    "failed_checks": own,
                    "f_at_c2": round(row["f_at_c2"], 4),
                    "count_at_c_half_d1": row["count_at_c_half_d1"],
                    "swap_f_diff": round(row["swap_f_diff"], 4),
                    "f_concern_heavy": round(row["f_concern_heavy"], 4),
                    "f_distress_heavy": round(row["f_distress_heavy"], 4),
                }
        per_seed[int(seed)] = failures
    return per_seed


# ---------------------------------------------------------------------------
# 4. Generation-0 conditions and trajectories (N=4, design B)
# ---------------------------------------------------------------------------

def gen0_conditions(seed, sigma=SIGMA_REF, n_agents=4,
                    generations=10):
    """Gen-0 coupling and the per-generation trajectories.

    The coupling_f rows of run_collaboration are the
    per-generation empathy fraction BEFORE the field
    mix; r_mean is the mean pairwise overlap AFTER
    the mix (collaborating arm). A generation-0 spike
    would show as coupling_f[0] far above the other
    seeds' and above the run's own later values.
    """
    result = ef.run_collaboration(
        n_agents=n_agents, sigma=sigma, generations=generations,
        seed=int(seed), design="B")
    rows = result["collaborating"]["rows"]
    return {
        "seed": int(seed),
        "sigma": float(sigma),
        "gap_bits": float(result["gap_bits"]),
        "gen0_coupling_f": float(rows[0]["coupling_f"]),
        "coupling_f": [float(r["coupling_f"]) for r in rows],
        "r_mean": [float(r["r_mean"]) for r in rows],
        "r_posterior_mean": [float(r["r_posterior_mean"])
                             for r in rows],
        "mean_d_per_generation": [
            float(sum(r["d_per_agent"]) / len(r["d_per_agent"]))
            for r in rows],
        "h_joint_per_generation": [float(r["h_joint_bits"])
                                   for r in rows],
    }


def sigma0_identity(seeds=FILE_SEEDS):
    """At sigma = 0 every seed's predictors are identical.

    The base populations are deterministic at zero noise,
    so any cross-seed difference at sigma = 0 would be a
    bug, not a seed effect. Only the sampled gap differs
    slightly (the sampling RNG is seeded by `seed`).
    """
    rows = {}
    for seed in seeds:
        runs = cg.seed_sweep(seed, sigmas=[0.0])
        rows[int(seed)] = runs[0]
    return rows


# ---------------------------------------------------------------------------
# 5. Cogitate per-seed table (the (lx) failure)
# ---------------------------------------------------------------------------

def cogitate_seed_table(seed):
    """Per-seed Cogitate sweep, correlations, and the (lx) margin.

    Also records the SHAPE of the mean_D trajectory: the
    sigma where mean_D peaks and whether it rises then
    falls (hump-shaped like the gap) or falls then rises
    (U-shaped) or stays flat. The shape is the mechanism
    behind r(gap, mean_D) on each seed.
    """
    runs = cg.seed_sweep(seed)
    corrs = cg.per_seed_correlations(runs)
    mean_ds = [r["mean_D"] for r in runs]
    gaps = [r["gap_bits"] for r in runs]
    peak_d = ef.SIGMA_GRID[int(np.argmax(mean_ds))]
    peak_gap = ef.SIGMA_GRID[int(np.argmax(gaps))]
    margin = (corrs["mean_R"] - corrs["mean_D"]
              if corrs["mean_R"] is not None
              and corrs["mean_D"] is not None else None)
    return {
        "seed": int(seed),
        "runs": runs,
        "correlations": corrs,
        "lx_margin_mean_R_minus_mean_D": margin,
        "lx_passes": bool(margin is not None and margin >= cg.MARGIN_LX),
        "mean_d_by_sigma": [float(v) for v in mean_ds],
        "gap_by_sigma": [float(v) for v in gaps],
        "mean_r_by_sigma": [float(r["mean_R"]) for r in runs],
        "sigma_of_max_mean_D": float(peak_d),
        "sigma_of_max_gap": float(peak_gap),
    }


# ---------------------------------------------------------------------------
# 6. Isolated-arm switch table (the XOR failure)
# ---------------------------------------------------------------------------

def isolated_switch_table(seed, sigma=SIGMA_REF, generations=10):
    """Per-generation collapsed concepts in the isolated arm.

    Replicates the pid.pair_arm_distributions design-B
    loop exactly (same base population, same noise-kick
    seeds seed + 1000*g + 10*i, same collapse seeds
    seed + 4242 + 1000*g + 10*i) while recording each
    agent's collapsed concept per generation. The pooled
    isolated joint is the count table of these 10 pairs,
    so the joint cells, the marginal entropies, and the
    XOR / MAX isolated informations are all read off
    the table. The reconstructed joint is checked
    against pid's joint by the tests.
    """
    base = ef.collaboration_population(2, sigma, seed)
    states = [s.copy() for s in base]
    seq = [[], []]
    for g in range(int(generations)):
        states = [ef._noise_kick(s, sigma, seed + 1000 * g + 10 * i)
                  for i, s in enumerate(states)]
        for i, s in enumerate(states):
            idx, decided = thought.collapse(
                s, seed=seed + 4242 + 1000 * g + 10 * i)
            seq[i].append(int(idx))
            states[i] = np.asarray(decided, dtype=complex)
    joint = np.zeros((4, 4))
    for a, b in zip(seq[0], seq[1]):
        joint[a, b] += 1.0
    joint /= float(generations)
    p1 = joint.sum(axis=1)
    p2 = joint.sum(axis=0)
    h1 = cost.shannon_entropy(p1)
    h2 = cost.shannon_entropy(p2)
    mi = h1 + h2 - cost.shannon_entropy(joint.flatten())
    xor = st.xor_pid_from_joint(joint)
    mx = tt.max_pid_from_joint(joint)
    cells = [(int(a), int(b), float(joint[a, b]))
             for a in range(4) for b in range(4)
             if joint[a, b] > 0.0]
    return {
        "seed": int(seed),
        "sigma": float(sigma),
        "concepts_agent0": [int(v) for v in seq[0]],
        "concepts_agent1": [int(v) for v in seq[1]],
        "distinct_agent0": len(set(seq[0])),
        "distinct_agent1": len(set(seq[1])),
        "joint": joint,
        "joint_cells": cells,
        "n_joint_cells": len(cells),
        "h_x1_bits": float(h1),
        "h_x2_bits": float(h2),
        "mutual_info_bits": float(mi),
        "xor_total_info_isolated_bits": float(
            xor["total_info_bits"]),
        "max_total_info_isolated_bits": float(
            mx["total_info_bits"]),
    }


def pid_arm_table(seed, sigma=SIGMA_REF):
    """XOR + MAX arm values and pooled marginals per (seed, sigma)."""
    x = st.xor_arm_distributions(sigma=sigma, seed=int(seed))
    m = tt.max_arm_distributions(sigma=sigma, seed=int(seed))
    joint_c = x["collaborating"]["joint"]
    joint_i = x["isolated"]["joint"]

    def _marg(joint):
        p1 = joint.sum(axis=1)
        p2 = joint.sum(axis=0)
        h1 = cost.shannon_entropy(p1)
        h2 = cost.shannon_entropy(p2)
        mi = h1 + h2 - cost.shannon_entropy(joint.flatten())
        return float(h1), float(h2), float(mi)

    h1c, h2c, mic = _marg(joint_c)
    h1i, h2i, mii = _marg(joint_i)
    return {
        "seed": int(seed),
        "sigma": float(sigma),
        "xor_delta_info_bits": float(x["delta_total_info_bits"]),
        "xor_i_collaborating_bits": float(
            x["collaborating"]["xor_pid"]["total_info_bits"]),
        "xor_i_isolated_bits": float(
            x["isolated"]["xor_pid"]["total_info_bits"]),
        "xor_syn_collaborating_bits": float(
            x["collaborating"]["xor_pid"]["synergistic_bits"]),
        "xor_syn_isolated_bits": float(
            x["isolated"]["xor_pid"]["synergistic_bits"]),
        "max_delta_info_bits": float(m["delta_total_info_bits"]),
        "max_i_collaborating_bits": float(
            m["collaborating"]["max_pid"]["total_info_bits"]),
        "max_i_isolated_bits": float(
            m["isolated"]["max_pid"]["total_info_bits"]),
        "collab_h_x1_bits": h1c,
        "collab_h_x2_bits": h2c,
        "collab_mutual_info_bits": mic,
        "isol_h_x1_bits": h1i,
        "isol_h_x2_bits": h2i,
        "isol_mutual_info_bits": mii,
        "mean_r_pre": float(x["collaborating"]["mean_r_pre"]),
        "mean_r_post_collaborating": float(
            x["collaborating"]["mean_r_post"]),
        "mean_r_post_isolated": float(
            x["isolated"]["mean_r_post"]),
    }


# ---------------------------------------------------------------------------
# 7. Cross-seed survey (diagnostic only) and the verdict
# ---------------------------------------------------------------------------

def seed_survey(seeds=SURVEY_SEEDS):
    """One row per survey seed: the three anomaly statistics.

    f0 is the baseline resonance empathy fraction
    (two-channel), xor_delta_info is the v0.20.0 gap
    at sigma = 0.25, max_delta_info is the v0.21.0
    gap at sigma = 0.25, and lx_margin is the
    Cogitate (lx) margin r(mean_R) - r(mean_D). The
    correlations across seeds test whether one
    variable carries all three anomalies.
    """
    rows = []
    for seed in seeds:
        base = baseline_field(seed)
        arms = pid_arm_table(seed)
        cog = cogitate_seed_table(seed)
        rows.append({
            "seed": int(seed),
            "baseline_f": base["f_baseline"],
            "det_mean": base["det_mean"],
            "n_det_negative": base["n_det_negative"],
            "xor_delta_info_bits": arms["xor_delta_info_bits"],
            "xor_i_collaborating_bits": arms["xor_i_collaborating_bits"],
            "xor_i_isolated_bits": arms["xor_i_isolated_bits"],
            "max_delta_info_bits": arms["max_delta_info_bits"],
            "max_i_collaborating_bits": arms["max_i_collaborating_bits"],
            "max_i_isolated_bits": arms["max_i_isolated_bits"],
            "lx_margin": cog["lx_margin_mean_R_minus_mean_D"],
            "r_mean_R": cog["correlations"]["mean_R"],
            "r_mean_D": cog["correlations"]["mean_D"],
        })
    f0 = [r["baseline_f"] for r in rows]
    return {
        "seeds": [int(s) for s in seeds],
        "rows": rows,
        "pearson_f0_xor_delta_info": cg.pearson(
            f0, [r["xor_delta_info_bits"] for r in rows]),
        "pearson_f0_lx_margin": cg.pearson(
            f0, [r["lx_margin"] for r in rows]),
        "pearson_xor_delta_info_lx_margin": cg.pearson(
            [r["xor_delta_info_bits"] for r in rows],
            [r["lx_margin"] for r in rows]),
        "seed_1234_max_baseline_f": bool(
            max(rows, key=lambda r: r["baseline_f"])["seed"] == 1234),
        "seed_1234_min_xor_delta_info": bool(
            min(rows, key=lambda r: r["xor_delta_info_bits"])["seed"]
            == 1234),
        "seed_1234_min_lx_margin": bool(
            min(rows, key=lambda r: r["lx_margin"])["seed"] == 1234),
        "seed_1234_min_max_delta_info": bool(
            min(rows, key=lambda r: r["max_delta_info_bits"])["seed"]
            == 1234),
    }


def diagnose(seeds=FILE_SEEDS):
    """The full diagnosis: tables plus the verdict.

    common_mechanism is False when no single variable
    explains all three anomalies: the determinant
    mechanism lives in the resonance population only,
    the Cogitate margin is a D-trajectory shape effect
    in the collaboration population, the XOR flip is
    a discrete switch-pattern effect in the isolated
    arm, the generation-0 spike is absent, no
    threshold sits near f = 0.3251, and the survey
    correlations between the three statistics are
    small. The function returns the evidence, not
    just the verdict, so the doc can quote numbers.
    """
    baselines = {s: baseline_field(s) for s in seeds}
    f_sigmas = {s: baseline_f_vs_sigma(s) for s in seeds}
    pairs = {s: pair_transform_response(s) for s in seeds}
    distress = {s: distress_only_sweep(s) for s in seeds}
    failures = two_channel_failures(seeds)
    gen0 = {s: gen0_conditions(s) for s in seeds}
    s0 = sigma0_identity(seeds)
    cog = {s: cogitate_seed_table(s) for s in seeds}
    switches = {s: isolated_switch_table(s) for s in seeds}
    arms = {s: pid_arm_table(s) for s in seeds}
    survey = seed_survey()
    # Refutation checks, as booleans with the numbers.
    gen0_1234_lowest = bool(
        min(gen0, key=lambda s: gen0[s]["gen0_coupling_f"]) == 1234)
    f_1234_highest_low_sigma = bool(all(
        f_sigmas[1234][k] == max(f_sigmas[s][k] for s in seeds)
        for k in range(len(ef.SIGMA_GRID))
        if 0.0 < ef.SIGMA_GRID[k] <= SIGMA_REF))
    corrs = [survey["pearson_f0_xor_delta_info"],
             survey["pearson_f0_lx_margin"],
             survey["pearson_xor_delta_info_lx_margin"]]
    small_corrs = bool(all(
        c is not None and abs(c) < 0.5 for c in corrs))
    common = False
    return {
        "verdict": "independent anomalies: no common mechanism",
        "common_mechanism": common,
        "evidence": {
            "gen0_coupling_1234_lowest": gen0_1234_lowest,
            "gen0_coupling_f": {s: round(gen0[s]["gen0_coupling_f"], 4)
                                for s in seeds},
            "f_1234_highest_at_every_sigma_0_to_0.25":
                f_1234_highest_low_sigma,
            "f_vs_sigma": {s: [round(v, 4) for v in f_sigmas[s]]
                           for s in seeds},
            "survey_correlations_small": small_corrs,
            "pearson_f0_xor_delta_info":
                survey["pearson_f0_xor_delta_info"],
            "pearson_f0_lx_margin": survey["pearson_f0_lx_margin"],
            "pearson_xor_delta_info_lx_margin":
                survey["pearson_xor_delta_info_lx_margin"],
            "seed_1234_max_baseline_f":
                survey["seed_1234_max_baseline_f"],
            "seed_1234_min_xor_delta_info":
                survey["seed_1234_min_xor_delta_info"],
            "seed_1234_min_lx_margin":
                survey["seed_1234_min_lx_margin"],
            "seed_1234_min_max_delta_info":
                survey["seed_1234_min_max_delta_info"],
        },
        "baselines": baselines,
        "pair_transform_response": pairs,
        "distress_only": distress,
        "two_channel_failures": failures,
        "gen0": gen0,
        "sigma0_identity": s0,
        "cogitate": cog,
        "isolated_switches": switches,
        "pid_arms": arms,
        "survey": survey,
    }


def main():
    """Print the seed-1234 diagnosis."""
    d = diagnose()
    print("Seed-1234 diagnosis -- verdict: " + d["verdict"])
    print()
    print("Baseline resonance field, N=8, sigma=0.25:")
    for s, b in d["baselines"].items():
        print(f"  seed {s}: R={b['mean_r']:.4f} D={b['mean_d']:.4f} "
              f"f={b['f_baseline']:.4f} count={b['n_qualia']} "
              f"det mean={b['det_mean']:+.4f} median={b['det_median']:+.4f} "
              f"neg={b['n_det_negative']}/{b['n_pairs']} "
              f"D range=[{b['d_min']:.4f}, {b['d_max']:.4f}]")
    print()
    print("Pair determinant mechanism (dose 0.25):")
    for s, p in d["pair_transform_response"].items():
        print(f"  seed {s}: det<0 pairs {p['n_det_negative']}/{p['n_pairs']}; "
              f"fall under concern: neg-det "
              f"{p['frac_neg_det_fall_under_concern']:.2f}, pos-det "
              f"{p['frac_pos_det_fall_under_concern']:.2f}; "
              f"fall under distress: neg-det "
              f"{p['frac_neg_det_fall_under_distress']:.2f}, pos-det "
              f"{p['frac_pos_det_fall_under_distress']:.2f}")
    print()
    print("Distress-only f(0, d):")
    for s, rows in d["distress_only"].items():
        print(f"  seed {s}: " +
              ", ".join(f"d={r['d']}: {r['f']:.4f}" for r in rows))
    print()
    print("Two-channel failures per seed:")
    for s, f in d["two_channel_failures"].items():
        failed = {k: v["failed_checks"] for k, v in f.items()
                  if not v["passed"]}
        print(f"  seed {s}: " + (str(failed) if failed else "none"))
    print()
    print("Generation-0 coupling (sigma=0.25, N=4):")
    for s, g in d["gen0"].items():
        print(f"  seed {s}: gen0={g['gen0_coupling_f']:.4f}, "
              f"trajectory={[round(v, 3) for v in g['coupling_f']]}")
    print()
    print("Cogitate (lx) per seed:")
    for s, c in d["cogitate"].items():
        print(f"  seed {s}: r(mean_R)={c['correlations']['mean_R']:.4f}, "
              f"r(mean_D)={c['correlations']['mean_D']:.4f}, "
              f"margin={c['lx_margin_mean_R_minus_mean_D']:+.4f}, "
              f"mean_D peaks at sigma={c['sigma_of_max_mean_D']}")
    print()
    print("Isolated-arm switch table, sigma=0.25:")
    for s, w in d["isolated_switches"].items():
        print(f"  seed {s}: agent0={w['concepts_agent0']} "
              f"agent1={w['concepts_agent1']} cells={w['n_joint_cells']} "
              f"I_isol(XOR)={w['xor_total_info_isolated_bits']:.4f} "
              f"I_isol(MAX)={w['max_total_info_isolated_bits']:.4f}")
    print()
    print("XOR / MAX arms, sigma=0.25:")
    for s, a in d["pid_arms"].items():
        print(f"  seed {s}: XOR dI={a['xor_delta_info_bits']:+.4f} "
              f"(Ic={a['xor_i_collaborating_bits']:.4f}, "
              f"Ii={a['xor_i_isolated_bits']:.4f}), "
              f"MAX dI={a['max_delta_info_bits']:+.4f} "
              f"(Ic={a['max_i_collaborating_bits']:.4f}, "
              f"Ii={a['max_i_isolated_bits']:.4f}), "
              f"R_pre={a['mean_r_pre']:.3f}")
    print()
    print("12-seed survey:")
    for r in d["survey"]["rows"]:
        print(f"  seed {r['seed']}: f0={r['baseline_f']:.4f} "
              f"XOR dI={r['xor_delta_info_bits']:+.4f} "
              f"MAX dI={r['max_delta_info_bits']:+.4f} "
              f"(lx) margin={r['lx_margin']:+.4f}")
    print(f"  Pearson(f0, XOR dI)="
          f"{d['survey']['pearson_f0_xor_delta_info']:+.4f}, "
          f"Pearson(f0, margin)="
          f"{d['survey']['pearson_f0_lx_margin']:+.4f}, "
          f"Pearson(XOR dI, margin)="
          f"{d['survey']['pearson_xor_delta_info_lx_margin']:+.4f}")
    print()
    print("Verdict: " + d["verdict"])


if __name__ == "__main__":
    main()
