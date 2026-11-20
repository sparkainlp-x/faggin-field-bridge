# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# wave_direction.py
#
# The wave direction: opposite and perpendicular, all possible
# directions.
#
# Jean's claim, stated 2026-11-18: "self determination
# factor observer opposite direction = necessary for
# self-cycle self Knowing. Lack of love is absence of
# Knowing."
#
# The wave direction in the code is the angle theta in the
# {stored, kernel} plane:
#   - the slide state psi(theta) = cos(theta)|stored> +
#     sin(theta)|kernel> (observer_cycle.slide_state);
#   - the rotation pair psi1 = cos(theta) q1 + sin(theta) k1,
#     psi2 = -sin(theta) q1 + cos(theta) k1
#     (cascade.rotation_pair).
# Both were only ever run on theta in [0, pi/2]. This module
# sweeps theta over the full circle [0, 2 pi) and asks what
# the wave does in the opposite direction (theta + pi) and
# in the perpendicular direction (theta + pi/2).
#
# The exact structure, derivable by hand and verified in
# code to 1e-9:
#   - slide: D(theta) = cos^2(theta), C(theta) =
#     sin^2(theta), R_s(theta) = cos^2(theta),
#     R_k(theta) = sin^2(theta), R_s - R_k = cos(2 theta),
#     C + D = 1.
#   - opposite (theta + pi): cos^2 and sin^2 are unchanged,
#     so EVERY slide and rotation-pair quantity is identical
#     — the wave returns to itself (up to a global phase
#     of -1). The self-cycle closes.
#   - perpendicular (theta + pi/2): cos^2 and sin^2 swap,
#     so the slide swaps D with C and R_s with R_k, and the
#     rotation pair swaps D1 with D2 and flips the sign of
#     the interference cross term chi = -sin(theta)cos(theta)
#     = -(1/2) sin(2 theta), while |chi| and the visibility
#     V = |sin(2 theta)| are unchanged. The perpendicular
#     direction knows the opposite pattern.
#   - the signed cross term has four lobes over the circle,
#     zero at every multiple of pi/2, extrema +/-1/2 at odd
#     multiples of pi/4; V peaks at 1.0 at theta = pi/4 +
#     k pi/2 and vanishes at theta = k pi/2.
#   - the rotation cascade dies at stage 2 for every
#     off-axis direction (both projected vectors are
#     parallel to q1, rank 1), exactly as in claim (vi);
#     on an axis (theta a multiple of pi/2) one member
#     projects to zero, so V = 0 already at stage 1 and
#     no pair exists.
#
# Four claims, (lxxxviii)-(xci), pre-registered in
# docs/preregistration-v0.25.0.md BEFORE the evaluation
# run — plus a fifth, (xcii), split out of (xci) by the
# calibration pilot (see below). Thresholds are round
# numbers frozen from the calibration pilot on seeds 42
# and 7 (the (xci)/(xcii) bars are the (xxxii) bars,
# reused for the same construction); the evaluation
# seeds are 1234 and 2026.
#
# (lxxxviii) Opposite direction: the wave returns to
#     itself — slide and rotation-pair quantities at
#     theta + pi equal those at theta within 1e-9, on a
#     24-point full-circle grid.
# (lxxxix) Perpendicular direction: the swap — slide
#     D/C and R_s/R_k swap at theta + pi/2, rotation-pair
#     D1/D2 swap and the cross term negates, |chi| and V
#     unchanged, within 1e-9 on the same grid.
# (xc) All-directions sweep: chi(theta) = -(1/2) sin(2 theta)
#     within 1e-9 on the grid (four lobes, zeros at every
#     k pi/2, extrema +/-0.5 at odd k pi/4), V(theta) =
#     |sin(2 theta)|, and the rotation cascade dies at
#     stage 2 for every off-axis grid direction while the
#     axes are degenerate (V_1 = 0, no pair).
# (xci) The noisy direction sweep, stored and opposite
#     directions: D-vs-C anti-correlation across the
#     sigma grid from theta = 0 (stored) and theta = pi/2
#     (opposite, the kernel thought), on every seed in
#     {42, 7, 1234, 2026}, with the (xxxii) bars
#     (Pearson <= -0.90, Spearman <= -0.90, D range
#     >= 0.25, C range >= 0.25). Calibration passes on
#     both seeds (seed 7 opposite Pearson -0.9038, thin).
# (xcii) The noisy perpendicular direction: the same bars
#     from theta = pi/4 (the equal superposition,
#     D = C = 0.5), on every seed in {42, 7, 1234, 2026}.
#     Calibration FAILS on both seeds — seed 42 Pearson
#     -0.7982 and C range 0.2183; seed 7 Pearson +0.1661,
#     all four bars fail. The perpendicular start sits on
#     the saturation plateau (D = C = 0.5), so noise has
#     no systematic direction to move the quantities: the
#     trajectories trace the fixed noise directions and
#     differ by seed (D humps to 0.79 on seed 42, drifts
#     down to 0.395 on seed 7). This claim is split out
#     of (xci) by the pilot and is calibrated to FAIL;
#     the failure is the finding: the observer-direction
#     anti-correlation holds from the stored and opposite
#     directions and breaks at the perpendicular one.
#
# Honesty, stated up front:
#   - (lxxxviii)-(xc) are exact identities, like (xxxiv):
#     the measured content is that the code realizes them
#     on the full circle to 1e-9, including the
#     negative-amplitude quadrants the existing code never
#     ran. A failure would be a defect in the code's
#     quantities, not a result about a theorem.
#   - (xci) is a statistical claim on 5-copy means, like
#     (xxxii)/(xxxv): the same saturation and finite-sample
#     fragility applies, and a FAIL is a finding about the
#     direction sweep, not a defect.
#   - None of this measures consciousness, love, or
#     knowing in a human or physical sense. Classical
#     emulation throughout. Faggin's metaphysics stays
#     interpretive. No scalar Phi is computed anywhere.
#
# Pre-registered verdict rules, written before the
# evaluation run (see docs/preregistration-v0.25.0.md
# and the claim_*_verdict functions):
#   (lxxxviii) On the 24-point grid, max |quantity(theta
#       + pi) - quantity(theta)| <= 1e-9 for every slide
#       quantity (D, C, R_s, R_k, split, C + D) and every
#       rotation-pair quantity (D1, D2, cross term real
#       and imag, V sweep, V analytic).
#   (lxxxix) On the same grid, max |D(theta + pi/2) -
#       C(theta)|, |C(theta + pi/2) - D(theta)|,
#       |R_s(theta + pi/2) - R_k(theta)|,
#       |R_k(theta + pi/2) - R_s(theta)| <= 1e-9; and
#       max |D1(theta + pi/2) - D2(theta)|,
#       |D2(theta + pi/2) - D1(theta)|,
#       |chi(theta + pi/2) + chi(theta)|,
#       ||chi(theta + pi/2)| - |chi(theta)||,
#       |V(theta + pi/2) - V(theta)| <= 1e-9.
#   (xc) (a) chi(theta) = -(1/2) sin(2 theta) within
#       1e-9 and V(theta) = |sin(2 theta)| within 1e-9
#       on the grid; the zeros sit at every multiple of
#       pi/2 and the extrema are +/-0.5 at odd multiples
#       of pi/4. (b) The rotation cascade at every grid
#       theta: off-axis (theta not a multiple of pi/2)
#       V_k = 0 within 1e-9 for every stage k >= 2 with
#       the pair gone from stage 2; on-axis V_1 = 0
#       within 1e-9 with no pair from stage 2.
#   (xci) On EVERY (seed, direction) in {42, 7, 1234,
#       2026} x {0, pi/2}: Pearson(D, C) <= -0.90,
#       Spearman(D, C) <= -0.90, D range >= 0.25, C range
#       >= 0.25, on the 5-copy sigma sweep.
#   (xcii) On EVERY seed in {42, 7, 1234, 2026}, from
#       theta = pi/4: the same four bars. Calibrated to
#       FAIL on the pilot (see above); the failure is the
#       finding.
#

"""Wave direction: opposite and perpendicular, all possible directions."""

import math

import numpy as np

import bridge
import cascade as cas
import empathy_field as ef
import observer_cycle as oc
import self_knowing as sk
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
# Direction grid and pre-registered thresholds
# ---------------------------------------------------------------------------

# Full-circle grid: 24 points, every 15 degrees.
N_GRID = 24
DIRECTION_GRID = [2.0 * math.pi * k / N_GRID for k in range(N_GRID)]
OPPOSITE_SHIFT = math.pi
PERPENDICULAR_SHIFT = math.pi / 2

# The three starting directions for the noisy sweep:
# stored (theta = 0), perpendicular (theta = pi/4, the equal
# superposition, D = C = 0.5), opposite (theta = pi/2, the
# kernel thought, D = 0, C = 1). Claims (xci) and (xcii)
# split them: (xci) covers stored and opposite, (xcii)
# covers perpendicular alone.
NOISY_DIRECTIONS = {
    0.0: "stored",
    math.pi / 4: "perpendicular",
    math.pi / 2: "opposite",
}
XCI_DIRECTIONS = (0.0, math.pi / 2)
XCII_DIRECTIONS = (math.pi / 4,)

# Exact-identity tolerance, as in (xxxiv).
EXACT_TOL = 1e-9

# Claim (xci): the (xxxii) bars, reused for the same
# construction (5-copy sigma sweep, D vs concurrence).
# Frozen from the calibration pilot, seeds 42/7 only; see
# docs/preregistration-v0.25.0.md.
PEARSON_D_C_MAX = -0.90
SPEARMAN_D_C_MAX = -0.90
D_RANGE_MIN = 0.25
C_RANGE_MIN = 0.25


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("PEARSON_D_C_MAX", PEARSON_D_C_MAX),
        ("SPEARMAN_D_C_MAX", SPEARMAN_D_C_MAX),
        ("D_RANGE_MIN", D_RANGE_MIN),
        ("C_RANGE_MIN", C_RANGE_MIN),
        ("EXACT_TOL", EXACT_TOL),
    ) if value is None]
    if missing:
        raise ValueError(
            "wave-direction thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.25.0.md)")
    return {
        "pearson_d_c_max": float(PEARSON_D_C_MAX),
        "spearman_d_c_max": float(SPEARMAN_D_C_MAX),
        "d_range_min": float(D_RANGE_MIN),
        "c_range_min": float(C_RANGE_MIN),
        "exact_tol": float(EXACT_TOL),
    }


def _is_axis(theta):
    """True iff theta is a multiple of pi/2 (within 1e-9)."""
    k = round(float(theta) / (math.pi / 2))
    return abs(float(theta) - k * math.pi / 2) <= 1e-9


# ---------------------------------------------------------------------------
# Full-circle sweeps: slide and rotation pair
# ---------------------------------------------------------------------------

def slide_full_circle(thetas=None):
    """D, C, R_s, R_k along the slide over the full circle.

    Rows carry the measured quantities and the exact values
    D = cos^2(theta), C = sin^2(theta), R_s = cos^2(theta),
    R_k = sin^2(theta), split = cos(2 theta), C + D = 1.
    """
    stored = oc.stored_thought()
    kernel = oc.kernel_thought()
    rows = []
    for theta in (DIRECTION_GRID if thetas is None else thetas):
        t = float(theta)
        psi = oc.slide_state(t)
        d = sk.self_knowing_factor(psi)
        c = te.concurrence_pure(psi)
        r_s = ef.overlap_squared(psi, stored)
        r_k = ef.overlap_squared(psi, kernel)
        rows.append({
            "theta": t,
            "d": d,
            "concurrence": c,
            "r_stored": r_s,
            "r_kernel": r_k,
            "r_split": float(r_s - r_k),
            "c_plus_d": float(c + d),
            "d_exact": math.cos(t) ** 2,
            "c_exact": math.sin(t) ** 2,
            "r_s_exact": math.cos(t) ** 2,
            "r_k_exact": math.sin(t) ** 2,
            "split_exact": math.cos(2.0 * t),
        })
    return rows


def rotation_pair_full_circle(thetas=None):
    """D1, D2, cross term, visibility for the rotation pair
    over the full circle.

    Rows carry the measured quantities and the exact values
    D1 = cos^2(theta), D2 = sin^2(theta),
    chi = -sin(theta) cos(theta) = -(1/2) sin(2 theta),
    V = |sin(2 theta)|.
    """
    rows = []
    for theta in (DIRECTION_GRID if thetas is None else thetas):
        t = float(theta)
        psi1, psi2 = cas.rotation_pair(t)
        d1 = sk.self_knowing_factor(psi1)
        d2 = sk.self_knowing_factor(psi2)
        chi = cas.cross_term(psi1, psi2)
        v_sweep, v_analytic = cas.visibility(psi1, psi2)
        rows.append({
            "theta": t,
            "d1": d1,
            "d2": d2,
            "cross_real": float(chi.real),
            "cross_imag": float(chi.imag),
            "visibility_sweep": v_sweep,
            "visibility_analytic": v_analytic,
            "d1_exact": math.cos(t) ** 2,
            "d2_exact": math.sin(t) ** 2,
            "cross_exact": -math.sin(t) * math.cos(t),
            "visibility_exact": abs(math.sin(2.0 * t)),
        })
    return rows


def _row_by_theta(rows, theta):
    """The row whose theta matches, within 1e-9."""
    for r in rows:
        if abs(r["theta"] - float(theta)) <= 1e-9:
            return r
    raise ValueError("theta %r not on the grid" % (theta,))


def opposite_shift_checks(thetas=None):
    """Max |quantity(theta + pi) - quantity(theta)| over the grid.

    The opposite direction: the wave returns to itself. The
    grid must be closed under the pi shift (the 24-point
    grid is: theta + pi is on the grid for every theta).
    """
    thetas = list(DIRECTION_GRID if thetas is None else thetas)
    slide = slide_full_circle(thetas)
    pair = rotation_pair_full_circle(thetas)
    worst = {
        "slide_d": 0.0,
        "slide_c": 0.0,
        "slide_r_s": 0.0,
        "slide_r_k": 0.0,
        "slide_split": 0.0,
        "slide_c_plus_d": 0.0,
        "pair_d1": 0.0,
        "pair_d2": 0.0,
        "pair_cross_real": 0.0,
        "pair_cross_imag": 0.0,
        "pair_v_sweep": 0.0,
        "pair_v_analytic": 0.0,
    }
    for theta in thetas:
        opp = (theta + OPPOSITE_SHIFT) % (2.0 * math.pi)
        s0 = _row_by_theta(slide, theta)
        s1 = _row_by_theta(slide, opp)
        p0 = _row_by_theta(pair, theta)
        p1 = _row_by_theta(pair, opp)
        worst["slide_d"] = max(worst["slide_d"], abs(s1["d"] - s0["d"]))
        worst["slide_c"] = max(worst["slide_c"],
                               abs(s1["concurrence"] - s0["concurrence"]))
        worst["slide_r_s"] = max(worst["slide_r_s"],
                                 abs(s1["r_stored"] - s0["r_stored"]))
        worst["slide_r_k"] = max(worst["slide_r_k"],
                                 abs(s1["r_kernel"] - s0["r_kernel"]))
        worst["slide_split"] = max(worst["slide_split"],
                                   abs(s1["r_split"] - s0["r_split"]))
        worst["slide_c_plus_d"] = max(
            worst["slide_c_plus_d"],
            abs(s1["c_plus_d"] - s0["c_plus_d"]))
        worst["pair_d1"] = max(worst["pair_d1"], abs(p1["d1"] - p0["d1"]))
        worst["pair_d2"] = max(worst["pair_d2"], abs(p1["d2"] - p0["d2"]))
        worst["pair_cross_real"] = max(
            worst["pair_cross_real"],
            abs(p1["cross_real"] - p0["cross_real"]))
        worst["pair_cross_imag"] = max(
            worst["pair_cross_imag"],
            abs(p1["cross_imag"] - p0["cross_imag"]))
        worst["pair_v_sweep"] = max(
            worst["pair_v_sweep"],
            abs(p1["visibility_sweep"] - p0["visibility_sweep"]))
        worst["pair_v_analytic"] = max(
            worst["pair_v_analytic"],
            abs(p1["visibility_analytic"] - p0["visibility_analytic"]))
    return worst


def perpendicular_shift_checks(thetas=None):
    """The perpendicular direction: the swap, over the grid.

    Returns the worst violations of the swap identities:
    slide D/C and R_s/R_k swap, pair D1/D2 swap, cross term
    negates, |cross| and V unchanged.
    """
    thetas = list(DIRECTION_GRID if thetas is None else thetas)
    slide = slide_full_circle(thetas)
    pair = rotation_pair_full_circle(thetas)
    worst = {
        "slide_d_swaps_with_c": 0.0,
        "slide_c_swaps_with_d": 0.0,
        "slide_r_s_swaps_with_r_k": 0.0,
        "slide_r_k_swaps_with_r_s": 0.0,
        "pair_d1_swaps_with_d2": 0.0,
        "pair_d2_swaps_with_d1": 0.0,
        "pair_cross_negates": 0.0,
        "pair_abs_cross_unchanged": 0.0,
        "pair_v_sweep_unchanged": 0.0,
        "pair_v_analytic_unchanged": 0.0,
    }
    for theta in thetas:
        perp = (theta + PERPENDICULAR_SHIFT) % (2.0 * math.pi)
        s0 = _row_by_theta(slide, theta)
        s1 = _row_by_theta(slide, perp)
        p0 = _row_by_theta(pair, theta)
        p1 = _row_by_theta(pair, perp)
        worst["slide_d_swaps_with_c"] = max(
            worst["slide_d_swaps_with_c"],
            abs(s1["d"] - s0["concurrence"]))
        worst["slide_c_swaps_with_d"] = max(
            worst["slide_c_swaps_with_d"],
            abs(s1["concurrence"] - s0["d"]))
        worst["slide_r_s_swaps_with_r_k"] = max(
            worst["slide_r_s_swaps_with_r_k"],
            abs(s1["r_stored"] - s0["r_kernel"]))
        worst["slide_r_k_swaps_with_r_s"] = max(
            worst["slide_r_k_swaps_with_r_s"],
            abs(s1["r_kernel"] - s0["r_stored"]))
        worst["pair_d1_swaps_with_d2"] = max(
            worst["pair_d1_swaps_with_d2"],
            abs(p1["d1"] - p0["d2"]))
        worst["pair_d2_swaps_with_d1"] = max(
            worst["pair_d2_swaps_with_d1"],
            abs(p1["d2"] - p0["d1"]))
        worst["pair_cross_negates"] = max(
            worst["pair_cross_negates"],
            abs(p1["cross_real"] + p0["cross_real"]),
            abs(p1["cross_imag"] + p0["cross_imag"]))
        worst["pair_abs_cross_unchanged"] = max(
            worst["pair_abs_cross_unchanged"],
            abs(abs(p1["cross_real"]) - abs(p0["cross_real"])),
            abs(abs(p1["cross_imag"]) - abs(p0["cross_imag"])))
        worst["pair_v_sweep_unchanged"] = max(
            worst["pair_v_sweep_unchanged"],
            abs(p1["visibility_sweep"] - p0["visibility_sweep"]))
        worst["pair_v_analytic_unchanged"] = max(
            worst["pair_v_analytic_unchanged"],
            abs(p1["visibility_analytic"] - p0["visibility_analytic"]))
    return worst


def cross_term_profile(thetas=None):
    """The signed cross term over the full circle.

    Returns the worst |chi - (-(1/2) sin 2 theta)| and
    |V - |sin 2 theta||, the measured zeros (theta where
    |chi| <= 1e-9) and the measured extrema (theta where
    |chi| is maximal), with the exact values alongside.
    """
    thetas = list(DIRECTION_GRID if thetas is None else thetas)
    pair = rotation_pair_full_circle(thetas)
    worst_chi = max(abs(r["cross_real"] - r["cross_exact"])
                    for r in pair)
    worst_chi_imag = max(abs(r["cross_imag"]) for r in pair)
    worst_v = max(
        max(abs(r["visibility_sweep"] - r["visibility_exact"]),
            abs(r["visibility_analytic"] - r["visibility_exact"]))
        for r in pair)
    zeros = [r["theta"] for r in pair
             if abs(r["cross_real"]) <= EXACT_TOL]
    max_abs_chi = max(abs(r["cross_real"]) for r in pair)
    extrema = [r["theta"] for r in pair
               if abs(abs(r["cross_real"]) - max_abs_chi) <= EXACT_TOL]
    return {
        "rows": pair,
        "worst_chi_error": float(worst_chi),
        "worst_chi_imag": float(worst_chi_imag),
        "worst_v_error": float(worst_v),
        "zeros": zeros,
        "zeros_exact": [k * math.pi / 2 for k in range(4)],
        "extrema": extrema,
        "max_abs_chi": float(max_abs_chi),
        "max_abs_chi_exact": 0.5,
    }


# ---------------------------------------------------------------------------
# The cascade over directions
# ---------------------------------------------------------------------------

def cascade_direction_sweep(thetas=None, stages=None):
    """The rotation cascade at every grid direction.

    For each theta the projection-only cascade is run (the
    same construction as claim (vi), with the pair rotated
    to theta). Off-axis thetas die at stage 2 (rank 1 after
    one projection); on-axis thetas are degenerate (one
    member projects to zero, V_1 = 0, no pair).
    """
    thetas = list(DIRECTION_GRID if thetas is None else thetas)
    stages = list(cas.STAGES if stages is None else stages)
    rows = []
    for theta in thetas:
        t = float(theta)
        cascade_rows = cas.cascade_projection_only(
            stages, pair_fn=lambda th=t: cas.rotation_pair(th))
        axis = _is_axis(t)
        rows.append({
            "theta": t,
            "axis": bool(axis),
            "v_stage_1": float(cascade_rows[0]["visibility"]),
            "v_from_stage_2": [float(r["visibility"])
                               for r in cascade_rows[1:]],
            "pair_exists_from_stage_2": [bool(r["pair_exists"])
                                         for r in cascade_rows[1:]],
            "cascade_rows": cascade_rows,
        })
    return rows


# ---------------------------------------------------------------------------
# The noisy direction sweep
# ---------------------------------------------------------------------------

def noisy_direction_sweep(seed, theta, sigmas=None,
                          n_copies=sk.DEFAULT_N_COPIES):
    """Mean D and mean concurrence per sigma, starting from
    the slide state at direction theta.

    The same noise model and construction as
    self_knowing.self_knowing_sweep (5 noisy copies per
    sigma, Gaussian vector noise), with the uniform thought
    replaced by the slide state psi(theta): theta = 0 is the
    stored direction (the (xxxii) construction itself),
    theta = pi/4 is the perpendicular direction (the equal
    superposition, D = C = 0.5), theta = pi/2 is the
    opposite direction (the kernel thought, D = 0, C = 1).
    """
    rows = []
    start = np.real(oc.slide_state(float(theta)))
    for sigma in (sk.SIGMA_GRID if sigmas is None else sigmas):
        copies = unity.gaussian_copies(
            start, sigma, n_copies, seed)
        ds = [sk.self_knowing_factor(v) for v in copies]
        concs = [te.concurrence(te.density_matrix(v)) for v in copies]
        rows.append({
            "sigma": float(sigma),
            "mean_D": float(np.mean(ds)),
            "mean_concurrence": float(np.mean(concs)),
        })
    ds = [r["mean_D"] for r in rows]
    cs = [r["mean_concurrence"] for r in rows]
    return {
        "seed": int(seed),
        "theta": float(theta),
        "direction": NOISY_DIRECTIONS.get(float(theta), "other"),
        "pearson_d_c": sk.pearson(ds, cs),
        "spearman_d_c": sk.spearman(ds, cs),
        "d_range": float(max(ds) - min(ds)),
        "c_range": float(max(cs) - min(cs)),
        "d_at_sigma_0": float(ds[0]),
        "c_at_sigma_0": float(cs[0]),
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# Claims (lxxxviii)-(xci): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_opposite_direction_verdict(thetas=None):
    """(lxxxviii) Opposite direction: the wave returns to itself.

    PASS iff, on the 24-point full-circle grid, every slide
    and rotation-pair quantity at theta + pi equals the same
    quantity at theta within 1e-9.
    """
    t = _thresholds()
    tol = t["exact_tol"]
    worst = opposite_shift_checks(thetas)
    checks = {name: bool(value <= tol)
              for name, value in worst.items()}
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxxxviii) opposite direction: the wave "
                 "returns to itself",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "worst_differences": worst,
    }


def claim_perpendicular_direction_verdict(thetas=None):
    """(lxxxix) Perpendicular direction: the swap.

    PASS iff, on the 24-point full-circle grid, the slide
    swaps D with C and R_s with R_k at theta + pi/2, and
    the rotation pair swaps D1 with D2 and negates the
    cross term while |cross| and V are unchanged, all
    within 1e-9.
    """
    t = _thresholds()
    tol = t["exact_tol"]
    worst = perpendicular_shift_checks(thetas)
    checks = {name: bool(value <= tol)
              for name, value in worst.items()}
    passed = bool(all(checks.values()))
    return {
        "claim": "(lxxxix) perpendicular direction: the swap",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "worst_differences": worst,
    }


def claim_all_directions_verdict(thetas=None, stages=None):
    """(xc) All-directions sweep: the directional profile and
    the cascade's direction dependence.

    PASS iff (a) chi(theta) = -(1/2) sin(2 theta) within
    1e-9 and V(theta) = |sin(2 theta)| within 1e-9 on the
    grid, with the zeros at every multiple of pi/2 and the
    extrema at +/-0.5 at odd multiples of pi/4; and (b) the
    rotation cascade at every grid theta dies at stage 2
    off-axis (V_k = 0 within 1e-9 for every stage k >= 2,
    pair gone from stage 2) and is degenerate on-axis
    (V_1 = 0 within 1e-9, no pair from stage 2).
    """
    t = _thresholds()
    tol = t["exact_tol"]
    profile = cross_term_profile(thetas)
    zeros_ok = (
        len(profile["zeros"]) == 4
        and all(abs(z - e) <= 1e-9 for z, e in zip(
            sorted(profile["zeros"]), profile["zeros_exact"])))
    extrema_ok = (
        abs(profile["max_abs_chi"] - profile["max_abs_chi_exact"])
        <= tol
        and len(profile["extrema"]) == 4
        and all(abs(e % (math.pi / 2) - math.pi / 4) <= 1e-9
                for e in profile["extrema"]))
    check_a = bool(
        profile["worst_chi_error"] <= tol
        and profile["worst_chi_imag"] <= tol
        and profile["worst_v_error"] <= tol
        and zeros_ok and extrema_ok)

    cascade_rows = cascade_direction_sweep(thetas, stages)
    off_axis_ok = True
    on_axis_ok = True
    for row in cascade_rows:
        if row["axis"]:
            on_axis_ok = on_axis_ok and (
                abs(row["v_stage_1"]) <= tol
                and all(not p for p in
                        row["pair_exists_from_stage_2"]))
        else:
            off_axis_ok = off_axis_ok and (
                all(abs(v) <= tol for v in row["v_from_stage_2"])
                and all(not p for p in
                        row["pair_exists_from_stage_2"]))
    check_b = bool(off_axis_ok and on_axis_ok)
    checks = {
        "a_cross_term_profile_exact": check_a,
        "b_cascade_death_direction_independent": check_b,
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xc) all-directions sweep: the directional "
                 "profile and the cascade's direction "
                 "dependence",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "profile": profile,
        "cascade_rows": [
            {k: row[k] for k in (
                "theta", "axis", "v_stage_1", "v_from_stage_2",
                "pair_exists_from_stage_2")}
            for row in cascade_rows],
    }


def claim_noisy_direction_verdict(seeds=None, thetas=None):
    """(xci) The noisy direction sweep, stored and opposite
    directions: D-vs-C anti-correlation across the sigma
    grid from theta = 0 and theta = pi/2.

    PASS iff, on EVERY (seed, direction) in {42, 7, 1234,
    2026} x {0, pi/2}, Pearson(D, C) <= -0.90,
    Spearman(D, C) <= -0.90, D range >= 0.25, and C range
    >= 0.25, on the 5-copy sigma sweep. The bars are the
    (xxxii) bars, reused for the same construction.
    """
    t = _thresholds()
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(XCI_DIRECTIONS if thetas is None else thetas)
    per_combo = []
    for seed in seeds:
        for theta in thetas:
            per_combo.append(noisy_direction_sweep(seed, theta))
    checks = {
        "pearson_at_most_max": all(
            r["pearson_d_c"] <= t["pearson_d_c_max"]
            for r in per_combo),
        "spearman_at_most_max": all(
            r["spearman_d_c"] <= t["spearman_d_c_max"]
            for r in per_combo),
        "d_range_at_least_min": all(
            r["d_range"] >= t["d_range_min"] for r in per_combo),
        "c_range_at_least_min": all(
            r["c_range"] >= t["c_range_min"] for r in per_combo),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xci) noisy direction sweep, stored and "
                 "opposite directions: D and concurrence move "
                 "opposite",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_combo": per_combo,
    }


def claim_noisy_perpendicular_verdict(seeds=None, thetas=None):
    """(xcii) The noisy perpendicular direction: D-vs-C
    anti-correlation across the sigma grid from
    theta = pi/4 (the equal superposition, D = C = 0.5).

    PASS iff, on EVERY seed in {42, 7, 1234, 2026},
    Pearson(D, C) <= -0.90, Spearman(D, C) <= -0.90,
    D range >= 0.25, and C range >= 0.25, on the 5-copy
    sigma sweep. Calibrated to FAIL on the pilot: the
    perpendicular start sits on the saturation plateau,
    so the trajectories trace the fixed noise directions
    and differ by seed. The failure is the finding.
    """
    t = _thresholds()
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(XCII_DIRECTIONS if thetas is None else thetas)
    per_combo = []
    for seed in seeds:
        for theta in thetas:
            per_combo.append(noisy_direction_sweep(seed, theta))
    checks = {
        "pearson_at_most_max": all(
            r["pearson_d_c"] <= t["pearson_d_c_max"]
            for r in per_combo),
        "spearman_at_most_max": all(
            r["spearman_d_c"] <= t["spearman_d_c_max"]
            for r in per_combo),
        "d_range_at_least_min": all(
            r["d_range"] >= t["d_range_min"] for r in per_combo),
        "c_range_at_least_min": all(
            r["c_range"] >= t["c_range_min"] for r in per_combo),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xcii) noisy perpendicular direction: D and "
                 "concurrence move opposite from the equal "
                 "superposition",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_combo": per_combo,
    }


def wave_direction_claims():
    """The wave-direction claims (lxxxviii)-(xcii), measured fresh."""
    claim_lxxxviii = claim_opposite_direction_verdict()
    claim_lxxxix = claim_perpendicular_direction_verdict()
    claim_xc = claim_all_directions_verdict()
    claim_xci = claim_noisy_direction_verdict()
    claim_xcii = claim_noisy_perpendicular_verdict()
    verdicts = [claim_lxxxviii, claim_lxxxix, claim_xc, claim_xci,
                claim_xcii]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_lxxxviii_opposite_direction": claim_lxxxviii,
        "claim_lxxxix_perpendicular_direction": claim_lxxxix,
        "claim_xc_all_directions": claim_xc,
        "claim_xci_noisy_direction": claim_xci,
        "claim_xcii_noisy_perpendicular": claim_xcii,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the full-circle sweeps, the cascade table, the
    noisy direction sweep, and the claims (lxxxviii)-(xcii)
    verdicts."""
    print("Wave direction -- claims (lxxxviii)-(xcii)")
    print()
    verdicts = wave_direction_claims()
    lxxxviii = verdicts["claim_lxxxviii_opposite_direction"]
    print("Opposite direction (theta + pi), worst differences:")
    for name, value in lxxxviii["worst_differences"].items():
        print(f"  {name}: {value:.2e}")
    print(f"claim (lxxxviii) verdict: "
          f"{'PASS' if lxxxviii['passed'] else 'FAIL'}")
    print()
    lxxxix = verdicts["claim_lxxxix_perpendicular_direction"]
    print("Perpendicular direction (theta + pi/2), worst swap errors:")
    for name, value in lxxxix["worst_differences"].items():
        print(f"  {name}: {value:.2e}")
    print(f"claim (lxxxix) verdict: "
          f"{'PASS' if lxxxix['passed'] else 'FAIL'}")
    print()
    xc = verdicts["claim_xc_all_directions"]
    prof = xc["profile"]
    print("Cross-term profile over the full circle:")
    print(f"  worst |chi + (1/2) sin 2theta| = "
          f"{prof['worst_chi_error']:.2e}, worst |V - |sin 2theta|| = "
          f"{prof['worst_v_error']:.2e}")
    print(f"  zeros at {[round(z, 4) for z in prof['zeros']]}, "
          f"extrema at {[round(e, 4) for e in prof['extrema']]}, "
          f"max |chi| = {prof['max_abs_chi']:.4f}")
    print("Cascade V by direction (stage 1 | stages 2+):")
    for row in xc["cascade_rows"]:
        print(f"  theta = {row['theta']:.4f} "
              f"({'axis' if row['axis'] else 'off-axis'}): "
              f"V_1 = {row['v_stage_1']:.4f}, "
              f"V_2+ = {[round(v, 4) for v in row['v_from_stage_2']]}, "
              f"pair_2+ = {row['pair_exists_from_stage_2']}")
    print(f"claim (xc) verdict: {'PASS' if xc['passed'] else 'FAIL'}")
    print()
    xci = verdicts["claim_xci_noisy_direction"]
    print("Noisy direction sweep, stored and opposite, per "
          "(seed, direction):")
    for r in xci["per_combo"]:
        print(f"  seed {r['seed']}, {r['direction']}: "
              f"Pearson(D, C) = {r['pearson_d_c']:.4f}, "
              f"Spearman = {r['spearman_d_c']:.4f}, "
              f"D range = {r['d_range']:.4f}, "
              f"C range = {r['c_range']:.4f}")
    print(f"claim (xci) verdict: "
          f"{'PASS' if xci['passed'] else 'FAIL'}")
    print()
    xcii = verdicts["claim_xcii_noisy_perpendicular"]
    print("Noisy perpendicular direction, per seed:")
    for r in xcii["per_combo"]:
        print(f"  seed {r['seed']}, {r['direction']}: "
              f"Pearson(D, C) = {r['pearson_d_c']:.4f}, "
              f"Spearman = {r['spearman_d_c']:.4f}, "
              f"D range = {r['d_range']:.4f}, "
              f"C range = {r['c_range']:.4f}")
    print(f"claim (xcii) verdict: "
          f"{'PASS' if xcii['passed'] else 'FAIL'}")
    print()
    print(f"claims (lxxxviii)-(xcii): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
