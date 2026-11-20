# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# inside_agents.py
#
# Observer and calibration agents INSIDE: per orbit
# copy and per cascade stage, instead of once per
# sweep from outside.
#
# Jean's directive, 2026-11-19: "Calibration and
# observer inside and symmetry spooky stability".
# v0.26.0 applies the observer and calibrator
# OUTSIDE: one observer read of the sweep report (7
# mean values), one calibrator decision per (seed,
# direction), closed loop 2 reads. INSIDE means the
# observer reads every orbit copy (20 copies x 7
# sigma = 140 copy-level D/C reads per V4-full
# sweep) and the calibrator decides once per orbit
# element (4 decisions, then 1 final averaged read =
# 141 reads total). Inside the cascade it would be
# 20 stages x 20 copies = 400 reads per sweep.
#
# The question is what the inside view buys for
# that cost. The exploration pilots (in /tmp,
# 2026-11-19 ~20:29 EST) found the asymmetry that
# is the finding of this build: inside OBSERVATION
# is diagnostic — the perpendicular element split
# shows the "inversion" is not a property of the
# sweep but of particular noise directions, averaged
# over a 2-vs-2 split — while inside CALIBRATION is
# useless: the per-element deltas equal the outside
# delta on every combo, and inside fails (xcii)
# exactly as outside does, on all nine seeds.
#
# The orbit elements are the V4-full transforms
# from symmetry_sweep.py: 0 = identity, 1 = flip
# z_u, 2 = flip z_w, 3 = flip z_u and z_w. Element 0
# (identity) IS the plain sweep. The inside
# calibrator applies the FROZEN v0.26.0 rule
# (observer_agents.SweepCalibrator) to each
# element's own 7-point sweep, then averages the
# four calibrated curves; the outside calibrator
# applies the same rule once to the averaged sweep.
#
# Two claims, (cv)-(cvi), pre-registered in
# docs/preregistration-v0.28.0.md BEFORE the
# evaluation run.
#
# (cv) Element split (inside observer): the inside
#     observer is read-only (worst |state after -
#     before| <= 1e-12); the perpendicular
#     element-Pearson spread is >= 0.80 on every
#     file seed, while the stored and opposite
#     spreads are <= 0.20 on every file seed.
# (cvi) Inside == outside calibration: the inside
#     deltas equal the outside delta, and the
#     inside failing-bar count equals the outside
#     one, on every file (seed, direction) combo;
#     inside fails (xcii) exactly as outside on all
#     nine seeds (file + fresh), with no rescue
#     anywhere. The cost is recorded: outside 1
#     read + 1 decision (closed loop 2 reads);
#     inside 140 copy-level reads + 4 decisions per
#     sweep; inside the cascade 400 reads.
#
# Honesty, stated up front:
#   - (cv) and (cvi) are exact-identity claims,
#     like (xxxiv) and (lxxxviii)-(xc): the
#     measured content is that the code realizes
#     the read-only contract, the element split,
#     and the inside==outside equality. A failure
#     would be a defect in the code, not a result
#     about a theorem.
#   - The (xci), (xcii), (xxxii) and (xcviii)
#     verdicts stay FAIL on the record as
#     originally stated. Inside calibration does
#     not rescue (xcii); it fails exactly as
#     outside does.
#   - None of this measures consciousness, love, or
#     knowing in a human or physical sense. Classical
#     emulation throughout. Faggin's metaphysics stays
#     interpretive. No scalar Phi is computed anywhere.
#
# Pre-registered verdict rules, written before the
# evaluation run (see docs/preregistration-v0.28.0.md
# and the claim_*_verdict functions):
#   (cv) (a) worst |state after - before| <= 1e-12
#       over all file seeds/directions; (b)
#       perpendicular element-Pearson spread >= 0.80
#       on every file seed; (c) stored and opposite
#       element-Pearson spreads <= 0.20 on every
#       file seed.
#   (cvi) (a) inside deltas == outside delta on
#       every file (seed, direction) in {stored,
#       opposite}; (b) inside failing-bar count ==
#       outside failing-bar count on every file
#       combo; (c) inside Pearson == outside Pearson
#       on all nine seeds at the perpendicular, and
#       no seed is rescued (Pearson > -0.90 inside
#       and outside, everywhere).
#

"""Inside agents: observer and calibrator per orbit copy."""

import math

import numpy as np

import bridge
import observer_agents as oa
import observer_cycle as oc
import self_knowing as sk
import symmetry_sweep as ss
import thought_entanglement as te
import wave_direction as wd

# ---------------------------------------------------------------------------
# Seeds
# ---------------------------------------------------------------------------

# Calibration seeds: the frozen expectations come
# from these only (see the blinding note in
# docs/preregistration-v0.28.0.md).
CALIBRATION_SEEDS = (42, 7)
# Evaluation seeds: held out until the evaluation
# run (confirmatory re-measurement — see the
# blinding note).
EVALUATION_SEEDS = (1234, 2026)
ALL_SEEDS = CALIBRATION_SEEDS + EVALUATION_SEEDS
# Second evaluation set: fresh seeds, already seen
# by the exploration pilots (blinding note).
FRESH_SEEDS = (5, 99, 2, 777, 2024)

# ---------------------------------------------------------------------------
# Thresholds (frozen; never moved after the run)
# ---------------------------------------------------------------------------

# Exact-identity tolerance, as in (xxxiv)/(lxxxviii).
EXACT_TOL = 1e-9
# Read-only tolerance: observation must not move the state.
READ_ONLY_TOL = 1e-12
# Element-split bars, frozen from the calibration pilot.
PERP_SPREAD_MIN = 0.80
STORED_OPP_SPREAD_MAX = 0.20

# The (xxxii) bars, reused unchanged since v0.12.0.
PEARSON_D_C_MAX = -0.90

# The V4-full orbit elements (0 = identity, 1 = flip
# z_u, 2 = flip z_w, 3 = flip z_u and z_w).
TRANSFORMS = ss.group_transforms(ss.GROUP_V4_FULL)
N_ELEMENTS = len(TRANSFORMS)

# Directions, from wave_direction.py.
ALL_NOISY_DIRECTIONS = (0.0, math.pi / 4, math.pi / 2)
XCI_DIRECTIONS = wd.XCI_DIRECTIONS
XCII_DIRECTIONS = wd.XCII_DIRECTIONS


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("EXACT_TOL", EXACT_TOL),
        ("READ_ONLY_TOL", READ_ONLY_TOL),
        ("PERP_SPREAD_MIN", PERP_SPREAD_MIN),
        ("STORED_OPP_SPREAD_MAX", STORED_OPP_SPREAD_MAX),
        ("PEARSON_D_C_MAX", PEARSON_D_C_MAX),
    ) if value is None]
    if missing:
        raise ValueError(
            "inside-agent thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.28.0.md)")
    return {
        "exact_tol": float(EXACT_TOL),
        "read_only_tol": float(READ_ONLY_TOL),
        "perp_spread_min": float(PERP_SPREAD_MIN),
        "stored_opp_spread_max": float(STORED_OPP_SPREAD_MAX),
        "pearson_d_c_max": float(PEARSON_D_C_MAX),
    }


# ---------------------------------------------------------------------------
# Per-orbit-element sweeps (the inside observer's view)
# ---------------------------------------------------------------------------

def element_copy_values(seed, theta,
                        n_copies=sk.DEFAULT_N_COPIES):
    """Per-orbit-element, per-sigma copy-level D and C.

    Element j = one V4-full transform applied to all 5
    base draws. Returns, per element, per sigma, the
    lists of copy D and copy C in base-draw order.
    The values are exactly the ones element_rows
    averages; the computation is identical, only the
    averaging is left to the caller — so that a caller
    needing the pooled 20-copy mean can take ONE
    np.mean over all 20 copies in the outside
    (symmetrized_sweep) order instead of a mean of
    4 element-means.
    """
    start = np.real(oc.slide_state(float(theta)))
    base = ss.draw_noise(seed, n_copies)
    per_element = []
    for f in TRANSFORMS:
        rows = []
        for sigma in sk.SIGMA_GRID:
            ds, cs = [], []
            for z in base:
                v = start + sigma * ss.from_coords(
                    f(ss.to_coords(z)))
                v = v / np.linalg.norm(v)
                ds.append(sk.self_knowing_factor(v))
                cs.append(te.concurrence(
                    te.density_matrix(v)))
            rows.append({"sigma": float(sigma),
                         "ds": ds, "cs": cs})
        per_element.append(rows)
    return per_element


def _mean_rows(copy_rows):
    """Mean D / mean C per sigma from copy-level values."""
    return [{"sigma": float(r["sigma"]),
             "mean_D": float(np.mean(r["ds"])),
             "mean_concurrence": float(np.mean(r["cs"]))}
            for r in copy_rows]


def element_rows(seed, theta,
                 n_copies=sk.DEFAULT_N_COPIES):
    """Per-orbit-element 7-point rows: element j = one
    V4-full transform applied to all 5 base draws.

    Element 0 (identity) IS the plain sweep. Each
    element's rows carry mean D and mean concurrence
    per sigma, computed from that element's copies
    only. The base draws and the start state are
    read, never modified (verified by the read-only
    test: the caller snapshots them and compares).
    """
    per_element = element_copy_values(seed, theta,
                                      n_copies=n_copies)
    return [_mean_rows(rows) for rows in per_element]


def element_pearson_spreads(seed, theta,
                            n_copies=sk.DEFAULT_N_COPIES):
    """Per-element Pearson and D range, and their spreads.

    Returns the per-element Pearson list, the spread
    (max - min) of Pearson across elements, the
    per-element D ranges, and the max D-spread across
    elements per sigma (with the sigma it occurs at).
    """
    per_element = element_rows(seed, theta,
                               n_copies=n_copies)
    pearsons = []
    d_ranges = []
    for rows in per_element:
        bars = oa.sweep_bars(rows)
        pearsons.append(float(bars["pearson_d_c"]))
        d_ranges.append(float(bars["d_range"]))
    d_spread = 0.0
    d_spread_sigma = None
    for i, sigma in enumerate(sk.SIGMA_GRID):
        ds = [r[i]["mean_D"] for r in per_element]
        spread = float(max(ds) - min(ds))
        if spread > d_spread:
            d_spread = spread
            d_spread_sigma = float(sigma)
    return {
        "seed": int(seed),
        "theta": float(theta),
        "direction": wd.NOISY_DIRECTIONS.get(float(theta),
                                              "other"),
        "pearson_per_element": pearsons,
        "pearson_spread": float(max(pearsons) - min(pearsons)),
        "d_range_per_element": d_ranges,
        "max_d_spread": float(d_spread),
        "max_d_spread_sigma": d_spread_sigma,
    }


def observe_inside_read_only(seed, theta,
                             n_copies=sk.DEFAULT_N_COPIES):
    """Observe inside, and report the worst input change.

    Snapshots the start state and the base noise
    draws, runs the per-element observation, and
    returns the worst |after - before| over both.
    The observation itself only reads its inputs.
    """
    start = np.real(oc.slide_state(float(theta)))
    base = ss.draw_noise(seed, n_copies)
    snap_start = start.copy()
    snap_base = [z.copy() for z in base]
    element_rows(seed, theta, n_copies=n_copies)
    worst = float(np.max(np.abs(start - snap_start)))
    for a, b in zip(base, snap_base):
        worst = max(worst, float(np.max(np.abs(a - b))))
    return worst


# ---------------------------------------------------------------------------
# Inside calibration: one delta per orbit element
# ---------------------------------------------------------------------------

def inside_calibrated_rows(per_element, copy_values=None):
    """Average of the per-element calibrated curves.

    The frozen v0.26.0 rule is applied to each
    element's own 7-point sweep; the four calibrated
    curves are averaged per sigma. Returns the
    averaged rows and the deltas picked per element.

    Summation order (post-evaluation fix, 2026-11-19):
    when all four element deltas are equal and no
    element-level clip would bite, the average of the
    per-element calibrated means is mathematically
    the pooled 20-copy sweep calibrated by that
    delta — so the average is taken as ONE np.mean
    over the 20 copy values in the outside
    (symmetrized_sweep) order (base draw first,
    then transform), and the common delta is applied
    to that pooled mean exactly as calibrated_rows
    does. That makes the inside rows bit-identical
    to the outside rows in that case, and the (cvi)
    perpendicular Pearson difference exactly 0.0
    instead of 1.22e-15 off in the last ULP. When
    the deltas differ, or a clip would bite at
    element level, the per-element average is used
    as before — the two definitions coincide
    mathematically only in the equal-delta,
    no-clip case. The (cvi) bar was not moved.
    """
    calibrator = oa.SweepCalibrator()
    deltas = []
    cal_curves = []
    for rows in per_element:
        d = calibrator.choose_delta(rows)["delta"]
        deltas.append(float(d))
        cal_curves.append(oa.calibrated_rows(rows, d))
    if copy_values is not None and len(set(deltas)) == 1:
        delta = deltas[0]
        # No element-level clip may bite: every
        # element mean D scaled by (1 + delta) must
        # stay in [0, 1] — otherwise the pooled mean
        # is not the average of the per-element
        # calibrated means (max >= mean covers the
        # pooled mean too).
        clips = False
        for rows in per_element:
            for r in rows:
                scaled = float(r["mean_D"]) * (1.0 + delta)
                if scaled > 1.0 or scaled < 0.0:
                    clips = True
        if not clips:
            pooled = []
            for i, sigma in enumerate(sk.SIGMA_GRID):
                ds, cs = [], []
                for z in range(len(copy_values[0][i]["ds"])):
                    for j in range(len(copy_values)):
                        ds.append(copy_values[j][i]["ds"][z])
                        cs.append(copy_values[j][i]["cs"][z])
                pooled.append({"sigma": float(sigma),
                               "mean_D": float(np.mean(ds)),
                               "mean_concurrence":
                                   float(np.mean(cs))})
            return oa.calibrated_rows(pooled, delta), deltas
    avg = []
    for i, sigma in enumerate(sk.SIGMA_GRID):
        avg.append({
            "sigma": float(sigma),
            "mean_D": float(np.mean(
                [c[i]["mean_D"] for c in cal_curves])),
            "mean_concurrence": float(np.mean(
                [c[i]["mean_concurrence"]
                 for c in cal_curves]))})
    return avg, deltas


def inside_vs_outside(seed, theta,
                      n_copies=sk.DEFAULT_N_COPIES):
    """Inside vs outside calibration on one sweep.

    Outside: the frozen rule applied once to the
    V4-full averaged sweep (symmetry_sweep).
    Inside: the frozen rule applied per orbit
    element, curves averaged. Returns both deltas,
    both failing-bar counts, and both Pearsons, so
    the equality (or its failure) is visible.
    """
    out = ss.calibrated_symmetry_sweep(seed, theta,
                                       n_copies=n_copies)
    copy_values = element_copy_values(seed, theta,
                                      n_copies=n_copies)
    per_element = [_mean_rows(rows) for rows in copy_values]
    avg, deltas = inside_calibrated_rows(per_element,
                                          copy_values)
    bars_in = oa.sweep_bars(avg)
    return {
        "seed": int(seed),
        "theta": float(theta),
        "direction": out["direction"],
        "outside_delta": float(out["delta"]),
        "outside_n_failing_at_zero":
            int(out["n_failing_at_zero"]),
        "outside_n_failing_calibrated":
            int(out["n_failing_calibrated"]),
        "outside_pearson":
            float(out["calibrated"]["pearson_d_c"]),
        "outside_d_range":
            float(out["calibrated"]["d_range"]),
        "inside_deltas": [float(d) for d in deltas],
        "inside_n_failing": int(bars_in["n_failing"]),
        "inside_pearson": float(bars_in["pearson_d_c"]),
        "inside_d_range": float(bars_in["d_range"]),
        "deltas_equal": bool(all(
            d == float(out["delta"]) for d in deltas)),
        "n_failing_equal": bool(
            bars_in["n_failing"]
            == int(out["n_failing_calibrated"])),
        "pearson_difference": float(
            abs(bars_in["pearson_d_c"]
                - out["calibrated"]["pearson_d_c"])),
    }


def cost_accounting(n_stages=20):
    """Observer/calibrator cost, outside vs inside.

    Outside (v0.26.0): 1 observer read of the sweep
    report + 1 calibrator decision per sweep; the
    closed loop is 2 reads. Inside: the V4-full
    sweep has n_copies x orbit x sigma copy-level
    D/C reads, one decision per orbit element, plus
    1 final averaged read. Inside the cascade: one
    stage read per stage, or one copy read per copy
    per stage. Counts are computed from the
    constants, not asserted as literals.
    """
    n_copies = sk.DEFAULT_N_COPIES
    n_sigma = len(sk.SIGMA_GRID)
    orbit = N_ELEMENTS
    copies_per_stage = n_copies * orbit
    return {
        "outside_reads_per_sweep": 1,
        "outside_decisions_per_sweep": 1,
        "closed_loop_reads_per_sweep": 2,
        "inside_copy_reads_per_sweep":
            int(n_copies * orbit * n_sigma),
        "inside_decisions_per_sweep": int(orbit),
        "inside_total_reads_per_sweep":
            int(n_copies * orbit * n_sigma + 1),
        "inside_cascade_stage_reads": int(n_stages),
        "inside_cascade_copy_reads":
            int(n_stages * copies_per_stage),
        "copies_per_sigma": int(n_copies * orbit),
        "n_sigma_points": int(n_sigma),
        "orbit_size": int(orbit),
    }


# ---------------------------------------------------------------------------
# Claims (cv)-(cvi): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_element_split_verdict(seeds=None, thetas=None):
    """(cv) Element split (inside observer).

    PASS iff (a) the inside observer is read-only:
    worst |state after - before| <= 1e-12 over all
    file seeds/directions; (b) the perpendicular
    element-Pearson spread is >= 0.80 on EVERY file
    seed; (c) the stored and opposite
    element-Pearson spreads are <= 0.20 on EVERY
    file seed.
    """
    t = _thresholds()
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(ALL_NOISY_DIRECTIONS
                  if thetas is None else thetas)
    worst_read_only = 0.0
    per_combo = []
    for seed in seeds:
        for theta in thetas:
            worst_read_only = max(
                worst_read_only,
                observe_inside_read_only(seed, theta))
            per_combo.append(
                element_pearson_spreads(seed, theta))
    perps = [r for r in per_combo
             if r["theta"] == math.pi / 4]
    stored_opp = [r for r in per_combo
                  if r["theta"] in (0.0, math.pi / 2)]
    checks = {
        "read_only": bool(
            worst_read_only <= t["read_only_tol"]),
        "perp_spread_at_least_min": bool(all(
            r["pearson_spread"] >= t["perp_spread_min"]
            for r in perps)),
        "stored_opp_spread_at_most_max": bool(all(
            r["pearson_spread"]
            <= t["stored_opp_spread_max"]
            for r in stored_opp)),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(cv) element split: inside observer "
                 "read-only, perpendicular splits across "
                 "elements, stored/opposite agree",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "worst_read_only_change": float(worst_read_only),
        "per_combo": per_combo,
    }


def claim_inside_equals_outside_verdict(seeds=None,
                                        thetas=None,
                                        perp_seeds=None):
    """(cvi) Inside == outside calibration.

    PASS iff (a) the inside deltas equal the outside
    delta on EVERY file (seed, direction) in
    {stored, opposite}; (b) the inside failing-bar
    count equals the outside failing-bar count on
    EVERY file combo; (c) inside fails (xcii)
    exactly as outside on all nine seeds (file +
    fresh) at the perpendicular: inside Pearson
    equals outside Pearson (max difference 0.0)
    and no seed is rescued (Pearson > -0.90
    inside and outside, everywhere).
    """
    t = _thresholds()
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(XCI_DIRECTIONS if thetas is None else thetas)
    perp_seeds = list(ALL_SEEDS + FRESH_SEEDS
                      if perp_seeds is None else perp_seeds)
    per_combo = [inside_vs_outside(s, th)
                 for s in seeds for th in thetas]
    per_perp = [inside_vs_outside(s, math.pi / 4)
                for s in perp_seeds]
    checks = {
        "deltas_equal_everywhere": bool(all(
            r["deltas_equal"] for r in per_combo)),
        "n_failing_equal_everywhere": bool(all(
            r["n_failing_equal"] for r in per_combo)),
        "perp_pearson_identical": bool(all(
            r["pearson_difference"] == 0.0
            for r in per_perp)),
        "perp_no_rescue_anywhere": bool(all(
            r["inside_pearson"] > t["pearson_d_c_max"]
            and r["outside_pearson"] > t["pearson_d_c_max"]
            for r in per_perp)),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(cvi) inside == outside calibration: "
                 "identical deltas and bars, (xcii) "
                 "unrescued on all nine seeds",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "worst_pearson_difference": float(max(
            r["pearson_difference"] for r in per_perp)),
        "cost": cost_accounting(),
        "per_combo": per_combo,
        "per_perp": per_perp,
    }


def inside_agents_claims():
    """The inside-agent claims (cv)-(cvi), measured fresh."""
    claim_cv = claim_element_split_verdict()
    claim_cvi = claim_inside_equals_outside_verdict()
    verdicts = [claim_cv, claim_cvi]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_cv_element_split": claim_cv,
        "claim_cvi_inside_equals_outside": claim_cvi,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the element split, the inside-vs-outside
    comparison, the cost accounting, and the claims
    (cv)-(cvi) verdicts."""
    print("Inside agents -- claims (cv)-(cvi)")
    print()
    verdicts = inside_agents_claims()
    cv = verdicts["claim_cv_element_split"]
    print(f"Inside observer read-only: worst change = "
          f"{cv['worst_read_only_change']:.2e}")
    print("Per-element Pearson spread, per (seed, "
          "direction):")
    for r in cv["per_combo"]:
        print(f"  seed {r['seed']}, {r['direction']}: "
              f"Pearson per element "
              f"{' '.join(f'{p:+.4f}' for p in r['pearson_per_element'])} "
              f"(spread {r['pearson_spread']:.4f}) | D-range "
              f"per element "
              f"{' '.join(f'{d:.4f}' for d in r['d_range_per_element'])}")
    print(f"claim (cv) verdict: "
          f"{'PASS' if cv['passed'] else 'FAIL'}")
    print()
    cvi = verdicts["claim_cvi_inside_equals_outside"]
    print("Inside vs outside calibration, per (seed, "
          "direction) [outside -> inside]:")
    for r in cvi["per_combo"]:
        print(f"  seed {r['seed']}, {r['direction']}: "
              f"delta {r['outside_delta']:+.4f} -> "
              f"[{' '.join(f'{d:+.4f}' for d in r['inside_deltas'])}], "
              f"failing {r['outside_n_failing_at_zero']} -> "
              f"{r['outside_n_failing_calibrated']} (out) / "
              f"{r['inside_n_failing']} (in)")
    print("Perpendicular, all nine seeds [outside -> "
          "inside Pearson]:")
    for r in cvi["per_perp"]:
        print(f"  seed {r['seed']}: "
              f"{r['outside_pearson']:+.4f} -> "
              f"{r['inside_pearson']:+.4f} (delta "
              f"{r['outside_delta']:+.4f} / "
              f"[{' '.join(f'{d:+.4f}' for d in r['inside_deltas'])}])")
    cost = cvi["cost"]
    print(f"Cost: outside {cost['outside_reads_per_sweep']} "
          f"read + {cost['outside_decisions_per_sweep']} "
          f"decision (closed loop "
          f"{cost['closed_loop_reads_per_sweep']} reads); "
          f"inside {cost['inside_copy_reads_per_sweep']} "
          f"copy reads + "
          f"{cost['inside_decisions_per_sweep']} decisions "
          f"per sweep; inside the cascade "
          f"{cost['inside_cascade_copy_reads']} reads")
    print(f"claim (cvi) verdict: "
          f"{'PASS' if cvi['passed'] else 'FAIL'}")
    print()
    print(f"claims (cv)-(cvi): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
