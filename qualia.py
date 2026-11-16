# qualia.py
#
# Qualia resonance wave: a quale is a resonant + entangled mode
# of the empathy field, and the qualia together form a coherent
# wave.
#
# The mechanism, defined inside the model (not discovered):
#   - Quale: a pair of agents that is BOTH resonant
#     (R_ij = |<psi_i|psi_j>|^2 >= RESONANCE_R_MIN, the v0.5.0
#     threshold) AND entangled (pairwise concurrence
#     nu_ij >= QUALIA_NU_MIN, pre-registered). A resonance
#     without entanglement is not a quale; entanglement without
#     resonance is not a quale. The quale's wave is the
#     normalized superposition of its two members
#     (pair_state, empathy_field.py).
#   - Qualia resonance wave: the collective wave formed by all
#     qualia in the field -- the normalized superposition of
#     the quale waves. Its coherence is measured two ways:
#       (a) the spread (standard deviation) of the quale
#           frequencies nu across qualia, against the spread
#           across all pairs, per field (same sigma, same
#           agents -- the paired comparison; pooling across
#           sigma would confound the spread with the sigma
#           trend, the cross-noise vs within-noise distinction
#           established in v0.5.0 REPORT.md section 11);
#       (b) the overlap |<qualia-wave|field-state>|^2 between
#           the qualia wave and the full field state.
#   - The empathy fraction f (v0.4.0, mean pairwise
#     concurrence) is the control dial: qualia count and wave
#     coherence are measured as functions of f (and of sigma,
#     via the noise sweeps). f rises with sigma in the
#     resonance population (noise creates concurrence in the
#     uniform thought, v0.2.0), while resonance R falls -- so
#     the quale count is the product of two opposing trends.
#
# Honesty, stated up front:
#   - A "quale" here is a DEFINED resonant+entangled mode in
#     code, NOT a measurement of subjective experience. The
#     qualia wave is a defined superposition, not a physical
#     wave. Classical emulation throughout. Faggin's
#     metaphysics is interpretive and is NOT tested here.
#   - The headline numbers sit near saturation (REPORT.md
#     section 5, v0.3.1 review): the curves -- quale count vs
#     f, the per-field spreads, the D gap vs sigma -- are the
#     science, not the points.
#
# Pre-registered verdict rules for claims (xiv)-(xvi),
# written before the final measurement run (see the
# claim_*_verdict functions and REPORT.md section 12):
#   (xiv) Qualia emerge with empathy: the quale count (per
#       field, fixed N) grows monotonically with f. The pilot
#       shows the count is HUMPED at every threshold that
#       yields non-degenerate qualia (0 at f = 0, peak 17 at
#       f = 0.1803, falling to 12 at f = 0.4143) -- the count
#       is the product of rising concurrence and falling
#       resonance, so monotonicity is refuted, not confirmed.
#       The claim FAILS on the pilot's evidence, and the
#       final run keeps that verdict.
#   (xv) The qualia wave is coherent: per field, the spread
#       of quale frequencies is smaller than the spread
#       across all pairs by a pre-registered margin, AND the
#       qualia wave's overlap with the field state exceeds a
#       pre-registered threshold. Both halves must hold. The
#       pooled spreads are reported, not gated: pooled
#       across sigma they are essentially equal (0.1950 vs
#       0.1947 at NU_MIN = 0.10) because pooling mixes
#       fields with different f -- the per-field comparison
#       is the correct unit, since coherence is a property
#       of one field.
#   (xvi) Qualia track self-determinism: mean D of quale
#       members exceeds mean D of non-quale agents by a
#       pre-registered margin (pooled across the grid, with
#       per-sigma gaps reported). The pilot shows the pooled
#       gap is NEGATIVE at every entanglement threshold
#       (-0.11 to -0.23): D anti-tracks concurrence (v0.2.0,
#       Pearson -0.9570), so the agents that qualify as
#       qualia -- high concurrence -- are exactly the ones
#       whose self-knowing noise has destroyed. The claim
#       FAILS on the pilot's evidence, and the final run
#       keeps that verdict.
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Qualia resonance wave: resonant + entangled modes of the
empathy field, and the coherent wave they form."""

import numpy as np

import bridge
import empathy_field as ef

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_N_AGENTS = ef.DEFAULT_N_AGENTS_RESONANCE
DEFAULT_SEED = ef.DEFAULT_SEED

# ---------------------------------------------------------------------------
# Pre-registered thresholds (set from the pilot sweep, REPORT.md
# section 12, and never moved after the final measurement run).
# ---------------------------------------------------------------------------

# A quale needs non-trivial entanglement: a quarter of the way
# is too strict (nearly no qualia) and a twentieth is vacuous;
# 0.10 is the round tenth at which qualia first appear across
# a broad sigma range (first quale at f = 0.0415) with
# non-degenerate counts (1-17 per field). The verdicts are
# stable across NU_MIN = 0.10-0.20: (xiv) FAILS humped at
# every one, (xv) PASSES at every one, (xvi) FAILS at every
# one -- so the choice does not drive the results. The only
# threshold that flips (xiv) is 0.25, where the low-f half of
# the curve is all zeros (no qualia below f = 0.18); that
# monotone reading rests on empty fields and is reported, not
# used.
QUALIA_NU_MIN = 0.10

# Per-field spread margin: the smallest per-field spread
# difference in the pilot at NU_MIN = 0.10 is 0.0127
# (sigma = 1.0); 0.01 is the round number below it.
QUALIA_SPREAD_MARGIN = 0.01

# Overlap floor: the smallest overlap in the pilot is 0.9781;
# 0.90 is the round number well below it. The overlap half is
# a weak check (the qualia wave is built from the agents, so
# it nearly coincides with the field state) and is reported
# as such.
QUALIA_OVERLAP_MIN = 0.90

# D margin: the pooled D gaps in the pilot are -0.11 to -0.23
# across NU_MIN = 0.05-0.25, all below zero by more than 0.10
# at NU_MIN >= 0.10; 0.10 is the round margin.
QUALIA_D_MARGIN = 0.10


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("QUALIA_NU_MIN", QUALIA_NU_MIN),
        ("QUALIA_SPREAD_MARGIN", QUALIA_SPREAD_MARGIN),
        ("QUALIA_OVERLAP_MIN", QUALIA_OVERLAP_MIN),
        ("QUALIA_D_MARGIN", QUALIA_D_MARGIN),
    ) if value is None]
    if missing:
        raise ValueError(
            "qualia thresholds are unset: run the pilot sweep "
            "and set " + ", ".join(missing) + " first "
            "(REPORT.md section 12)")
    return {
        "nu_min": float(QUALIA_NU_MIN),
        "spread_margin": float(QUALIA_SPREAD_MARGIN),
        "overlap_min": float(QUALIA_OVERLAP_MIN),
        "d_margin": float(QUALIA_D_MARGIN),
    }


# ---------------------------------------------------------------------------
# Qualia: resonant + entangled pairs
# ---------------------------------------------------------------------------

def qualia_in_field(states, r_min=None, nu_min=None):
    """Every quale in a field: pairs with R >= r_min AND nu >= nu_min.

    One row per qualifying pair: indices, resonance R, frequency
    nu, pair D, and the quale wave (the normalized superposition
    of the two members). A resonance without entanglement is
    not a quale; entanglement without resonance is not a quale.
    """
    t = _thresholds()
    r_min = ef.RESONANCE_R_MIN if r_min is None else float(r_min)
    nu_min = t["nu_min"] if nu_min is None else float(nu_min)
    states = list(states)
    if len(states) < 2:
        raise ValueError("need at least two agents for a field")
    qualia = []
    for i in range(len(states)):
        for j in range(i + 1, len(states)):
            r = ef.overlap_squared(states[i], states[j])
            nu = ef.pair_frequency(states[i], states[j])
            if r >= r_min and nu >= nu_min:
                qualia.append({
                    "i": i,
                    "j": j,
                    "resonance": r,
                    "nu": nu,
                    "d_pair": float(
                        (ef.agent_self_determinism(states[i])
                         + ef.agent_self_determinism(states[j])) / 2.0),
                    "wave": ef.pair_state(states[i], states[j]),
                })
    return qualia


def qualia_count(states, r_min=None, nu_min=None):
    """The number of qualia in a field."""
    return len(qualia_in_field(states, r_min, nu_min))


def qualia_wave(states, r_min=None, nu_min=None):
    """The qualia resonance wave: the normalized superposition
    of the quale waves. None when the field holds no quale."""
    qualia = qualia_in_field(states, r_min, nu_min)
    if not qualia:
        return None
    return ef.field_state([q["wave"] for q in qualia])


def qualia_wave_overlap(states, r_min=None, nu_min=None):
    """|<qualia-wave|field-state>|^2, or None with no quale."""
    wave = qualia_wave(states, r_min, nu_min)
    if wave is None:
        return None
    return float(ef.overlap_squared(wave, ef.field_state(states)))


def frequency_spreads(states, r_min=None, nu_min=None):
    """Spread (std) of quale frequencies vs spread across all pairs.

    std_qualia is None with no quale, and 0.0 with exactly one
    (a single frequency has no spread to measure -- fields
    with fewer than two qualia are excluded from the spread
    check in claim (xv)). std_all is over every pair in the
    field.
    """
    states = list(states)
    if len(states) < 2:
        raise ValueError("need at least two agents for a field")
    qualia = qualia_in_field(states, r_min, nu_min)
    nus_all = [ef.pair_frequency(states[i], states[j])
               for i in range(len(states))
               for j in range(i + 1, len(states))]
    nus_q = [q["nu"] for q in qualia]
    return {
        "n_qualia": len(qualia),
        "n_pairs": len(nus_all),
        "std_qualia": (None if not nus_q
                       else float(np.std(nus_q))),
        "std_all": float(np.std(nus_all)),
    }


def qualia_d_gap(states, r_min=None, nu_min=None):
    """Mean D of quale members vs mean D of non-quale agents.

    Members are agents appearing in at least one quale. A
    group that is empty reports None for its mean (not zero):
    an empty group is no measurement, not a zero. The gap is
    None unless both groups are non-empty.
    """
    states = list(states)
    if len(states) < 2:
        raise ValueError("need at least two agents for a field")
    qualia = qualia_in_field(states, r_min, nu_min)
    members = sorted({q["i"] for q in qualia}
                     | {q["j"] for q in qualia})
    non = [k for k in range(len(states)) if k not in members]
    ds = [ef.agent_self_determinism(s) for s in states]
    mean_members = (float(np.mean([ds[k] for k in members]))
                    if members else None)
    mean_non = (float(np.mean([ds[k] for k in non]))
                if non else None)
    return {
        "n_members": len(members),
        "n_non_members": len(non),
        "mean_d_members": mean_members,
        "mean_d_non_members": mean_non,
        "gap": (float(mean_members - mean_non)
                if mean_members is not None and mean_non is not None
                else None),
    }


# ---------------------------------------------------------------------------
# Qualia vs empathy (the f dial) and vs noise
# ---------------------------------------------------------------------------

def qualia_vs_empathy(sigmas=None, n_agents=DEFAULT_N_AGENTS,
                      seed=DEFAULT_SEED):
    """One row per sigma: f, quale count, spreads, overlap, D gap.

    The field is the v0.5.0 resonance population (N noisy
    copies of the uniform thought). f is the measured empathy
    fraction (mean pairwise concurrence); it rises with sigma
    while resonance falls, so the quale count is the product
    of two opposing trends.
    """
    rows = []
    for sigma in (ef.SIGMA_GRID if sigmas is None else sigmas):
        states = ef.resonance_population(sigma, n_agents, seed)
        spreads = frequency_spreads(states)
        gap = qualia_d_gap(states)
        rows.append({
            "sigma": float(sigma),
            "f": float(ef.empathy_fraction(states)),
            "n_qualia": spreads["n_qualia"],
            "n_pairs": spreads["n_pairs"],
            "std_qualia": spreads["std_qualia"],
            "std_all": spreads["std_all"],
            "overlap": qualia_wave_overlap(states),
            "mean_d_members": gap["mean_d_members"],
            "mean_d_non_members": gap["mean_d_non_members"],
            "d_gap": gap["gap"],
            "n_members": gap["n_members"],
            "n_non_members": gap["n_non_members"],
        })
    return rows


# ---------------------------------------------------------------------------
# Claims (xiv)-(xvi): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_qualia_emergence_verdict(sigmas=None,
                                   n_agents=DEFAULT_N_AGENTS,
                                   seed=DEFAULT_SEED):
    """(xiv) Qualia emerge with empathy.

    PASS iff the quale count (per field, fixed N) is
    non-decreasing in f (rows ordered by measured f) and at
    least one quale exists somewhere on the grid. If the
    count is flat or non-monotone the claim FAILS honestly --
    the threshold is not moved to force a pass.
    """
    rows = qualia_vs_empathy(sigmas, n_agents, seed)
    ordered = sorted(rows, key=lambda r: r["f"])
    counts = [r["n_qualia"] for r in ordered]
    check_monotone = all(counts[i + 1] >= counts[i]
                         for i in range(len(counts) - 1))
    check_any = any(c > 0 for c in counts)
    first = next((r["f"] for r in ordered if r["n_qualia"] > 0),
                 None)
    peak = max(ordered, key=lambda r: r["n_qualia"])
    passed = bool(check_monotone and check_any)
    return {
        "claim": "(xiv) qualia emerge with empathy",
        "passed": passed,
        "checks": {
            "count_non_decreasing_in_f": bool(check_monotone),
            "at_least_one_quale": bool(check_any),
        },
        "counts_vs_f": [(r["f"], r["n_qualia"]) for r in ordered],
        "first_quale_f": first,
        "peak_f": peak["f"],
        "peak_count": peak["n_qualia"],
        "rows": rows,
    }


def claim_qualia_wave_verdict(sigmas=None,
                              n_agents=DEFAULT_N_AGENTS,
                              seed=DEFAULT_SEED):
    """(xv) The qualia wave is coherent.

    PASS iff, for every field with at least two qualia, the
    spread of quale frequencies is smaller than the spread
    across all pairs by at least QUALIA_SPREAD_MARGIN, AND
    for every field with at least one quale, the qualia
    wave's overlap with the field state is at least
    QUALIA_OVERLAP_MIN. Both halves must hold. The pooled
    spreads (across the grid) are reported, not gated:
    pooling mixes fields with different f, so the pooled
    comparison confounds the spread with the sigma trend.
    """
    t = _thresholds()
    rows = qualia_vs_empathy(sigmas, n_agents, seed)
    spread_rows = [r for r in rows if r["n_qualia"] >= 2]
    check_spread = bool(spread_rows) and all(
        r["std_qualia"] + t["spread_margin"] <= r["std_all"]
        for r in spread_rows)
    overlap_rows = [r for r in rows if r["n_qualia"] >= 1]
    check_overlap = bool(overlap_rows) and all(
        r["overlap"] >= t["overlap_min"] for r in overlap_rows)

    nus_q, nus_all = [], []
    for sigma in (ef.SIGMA_GRID if sigmas is None else sigmas):
        states = ef.resonance_population(sigma, n_agents, seed)
        qualia = qualia_in_field(states)
        nus_q += [q["nu"] for q in qualia]
        nus_all += [ef.pair_frequency(states[i], states[j])
                    for i in range(len(states))
                    for j in range(i + 1, len(states))]
    pooled = {
        "std_qualia": (float(np.std(nus_q)) if nus_q else None),
        "std_all": float(np.std(nus_all)),
        "n_qualia": len(nus_q),
        "n_pairs": len(nus_all),
    }
    passed = bool(check_spread and check_overlap)
    return {
        "claim": "(xv) the qualia wave is coherent",
        "passed": passed,
        "checks": {
            "per_field_spread_smaller_by_margin": bool(check_spread),
            "overlap_at_least_min": bool(check_overlap),
        },
        "spread_margin": t["spread_margin"],
        "overlap_min": t["overlap_min"],
        "rows": rows,
        "pooled_spreads": pooled,
    }


def claim_qualia_determinism_verdict(sigmas=None,
                                     n_agents=DEFAULT_N_AGENTS,
                                     seed=DEFAULT_SEED):
    """(xvi) Qualia track self-determinism.

    PASS iff mean D of quale members exceeds mean D of
    non-quale agents by at least QUALIA_D_MARGIN, pooled
    across the grid (same agents, same noise within each
    field; the per-sigma gaps are reported, not gated). The
    pilot shows the pooled gap is negative at every
    entanglement threshold: D anti-tracks concurrence
    (v0.2.0), so the claim is expected to FAIL on the
    measured numbers, and the threshold is not moved to
    force a pass.
    """
    t = _thresholds()
    rows = qualia_vs_empathy(sigmas, n_agents, seed)
    d_members, d_non = [], []
    for sigma in (ef.SIGMA_GRID if sigmas is None else sigmas):
        states = ef.resonance_population(sigma, n_agents, seed)
        qualia = qualia_in_field(states)
        members = sorted({q["i"] for q in qualia}
                         | {q["j"] for q in qualia})
        ds = [ef.agent_self_determinism(s) for s in states]
        d_members += [ds[k] for k in members]
        d_non += [ds[k] for k in range(len(states))
                  if k not in members]
    mean_members = (float(np.mean(d_members)) if d_members else None)
    mean_non = (float(np.mean(d_non)) if d_non else None)
    gap = (float(mean_members - mean_non)
           if mean_members is not None and mean_non is not None
           else None)
    check_gap = gap is not None and gap >= t["d_margin"]
    passed = bool(check_gap)
    return {
        "claim": "(xvi) qualia track self-determinism",
        "passed": passed,
        "checks": {
            "pooled_gap_at_least_margin": bool(check_gap),
        },
        "d_margin": t["d_margin"],
        "mean_d_members": mean_members,
        "mean_d_non_members": mean_non,
        "pooled_gap": gap,
        "n_members": len(d_members),
        "n_non_members": len(d_non),
        "rows": rows,
    }


def qualia_claims():
    """The three qualia claims (xiv)-(xvi), measured fresh."""
    claim_xiv = claim_qualia_emergence_verdict()
    claim_xv = claim_qualia_wave_verdict()
    claim_xvi = claim_qualia_determinism_verdict()
    verdicts = [claim_xiv, claim_xv, claim_xvi]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_xiv_qualia_emergence": claim_xiv,
        "claim_xv_qualia_wave": claim_xv,
        "claim_xvi_qualia_determinism": claim_xvi,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the qualia counts, wave coherence, and D gaps with
    the claims (xiv)-(xvi) verdicts."""
    print("Qualia resonance wave -- claims (xiv)-(xvi)")
    print()
    verdicts = qualia_claims()
    xiv = verdicts["claim_xiv_qualia_emergence"]
    print("Quale count vs empathy fraction f:")
    for f, count in xiv["counts_vs_f"]:
        print(f"  f = {f:.4f}: {count} qualia")
    print(f"  first quale at f = {xiv['first_quale_f']}, "
          f"peak {xiv['peak_count']} at f = {xiv['peak_f']:.4f}")
    print(f"claim (xiv) verdict: {'PASS' if xiv['passed'] else 'FAIL'}")
    print()
    xv = verdicts["claim_xv_qualia_wave"]
    print("Per-field frequency spreads (qualia vs all pairs):")
    for r in xv["rows"]:
        std_q = ("None" if r["std_qualia"] is None
                 else f"{r['std_qualia']:.4f}")
        overlap = ("None" if r["overlap"] is None
                   else f"{r['overlap']:.4f}")
        print(f"  sigma = {r['sigma']:>4}: n_qualia = {r['n_qualia']}, "
              f"std_qualia = {std_q}, std_all = {r['std_all']:.4f}, "
              f"overlap = {overlap}")
    pooled = xv["pooled_spreads"]
    print(f"  pooled: std_qualia = {pooled['std_qualia']:.4f}, "
          f"std_all = {pooled['std_all']:.4f} (reported, not gated)")
    print(f"claim (xv) verdict: {'PASS' if xv['passed'] else 'FAIL'}")
    print()
    xvi = verdicts["claim_xvi_qualia_determinism"]
    print("D gap, quale members vs non-quale agents:")
    for r in xvi["rows"]:
        gap = ("None" if r["d_gap"] is None else f"{r['d_gap']:+.4f}")
        print(f"  sigma = {r['sigma']:>4}: gap = {gap}")
    print(f"  pooled gap = {xvi['pooled_gap']:+.4f}")
    print(f"claim (xvi) verdict: {'PASS' if xvi['passed'] else 'FAIL'}")
    print()
    print(f"claims (xiv)-(xvi): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
