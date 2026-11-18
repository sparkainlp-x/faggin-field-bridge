# product_model.py
#
# Product-model fit for the humped quale count (deep-think
# upgrade #3): the hump is an AND-gate, not a new mechanism.
#
# The mechanism, defined inside the model (not discovered):
#   - A quale is a pair that is BOTH resonant (R >= R_MIN)
#     AND entangled (nu >= NU_MIN) (qualia.py, v0.6.0). The
#     quale count vs empathy fraction f is HUMPED (0, 0, 1, 9,
#     17, 13, 12; peak 17 at f = 0.1803) while the
#     PARTIAL -> ATTUNED flip sits at f* = 0.7278 (v0.4.0).
#   - The product model says the count is N_pairs *
#     p_res(f) * p_ent(f), where p_res and p_ent are the two
#     marginals measured INDEPENDENTLY on the same field
#     (the fraction of pairs above each threshold on its
#     own). The two factors move in opposite directions with
#     f: p_ent rises with f (noise creates concurrence in
#     the uniform thought, v0.2.0) while p_res falls with f
#     (noise spreads the copies, v0.5.0). Their product is
#     necessarily humped, with its peak where the two
#     log-derivatives balance -- no new physics, just the
#     AND of two monotone factors (Yerkes-Dodson 1908;
#     stochastic resonance, De Ridder et al. 2024).
#   - The product predicts the count ONLY IF the two binary
#     indicators (resonant, entangled) are independent
#     across pairs. Any deviation of the measured count
#     from the product measures their association -- the
#     interaction the product model would miss. A fit that
#     fails is itself a discovery: a genuine interaction,
#     not just AND.
#   - Peak shift: change one threshold and the product
#     model, computed from the marginals at the NEW
#     threshold BEFORE looking at the measured counts there,
#     predicts the new peak f_peak. If the measured peak
#     moves with it, the peak position is determined by the
#     marginals. If it does not, an interaction sets the
#     peak.
#   - Hump vanish: drop either condition and the count must
#     be monotone in f (resonance-only falls, entanglement-
#     only rises). If a single-condition count still humps,
#     the hump is in a marginal, not in the AND.
#
# Honesty, stated up front:
#   - The marginals are measured on the SAME pairs as the
#     count, so the product is a test of independence across
#     pairs, not an independent prediction from separate
#     data. The peak-shift test is the stronger half: the
#     predicted peak comes from the marginals, the measured
#     peak from the joint counts, and they are compared
#     before either is allowed to inform the other.
#   - On the standard 7-point sigma grid the fit is partly
#     degenerate: p_res = 1.0 exactly below sigma = 0.5 at
#     the baseline thresholds, so the product there is just
#     the entanglement count. The gated fit therefore runs
#     on a FINER grid (sigma 0.30-1.50) where BOTH marginals
#     are interior on every row. The standard-grid fit is
#     reported, not gated.
#   - A "quale" here is a DEFINED resonant+entangled mode
#     in code, NOT a measurement of subjective experience.
#     Classical emulation throughout. Faggin's metaphysics
#     is interpretive and is NOT tested here.
#
# Pre-registered verdict rules for claims (xxvi)-(xxviii),
# frozen from the pilot sweeps and never moved after the
# final measurement run (see the claim_*_verdict functions
# and REPORT.md section 16):
#   (xxvi) Product-model fit PASSES iff, on the fine grid
#       at seed 42 and the baseline thresholds, the mean
#       relative error |measured - predicted| / predicted
#       over rows with predicted > 0 is at most
#       PRODUCT_FIT_MEAN_MAX (0.10) AND the largest single
#       row error is at most PRODUCT_FIT_ROW_MAX (0.20).
#       Pilot: mean 0.0289, max 0.0667 -- the margins are
#       wide, the thresholds are not tuned to the edge.
#   (xxvii) Peak shift PASSES iff, at each of the two
#       shifted settings (NU_MIN 0.10 -> 0.25 with R_MIN
#       0.5; R_MIN 0.5 -> 0.25 with NU_MIN 0.10), the
#       product-predicted peak f equals the measured peak f
#       exactly (same grid point), AND both measured peaks
#       sit ABOVE the baseline peak f = 0.1803 (the
#       predicted direction: loosening resonance or
#       tightening entanglement both push the peak to
#       higher f). Pilot: NU_MIN = 0.25 predicts and
#       measures 0.4143; R_MIN = 0.25 predicts and measures
#       0.2839.
#   (xxviii) Hump vanish PASSES iff the resonance-only
#       count is non-increasing in f AND the entanglement-
#       only count is non-decreasing in f on the standard
#       grid, while the both-condition count is non-monotone
#       in f. Pilot: 28, 28, 28, 28, 28, 17, 14 (falling);
#       0, 0, 1, 9, 17, 21, 25 (rising); 0, 0, 1, 9, 17,
#       13, 12 (humped).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Product model for the humped quale count: N * p_res * p_ent."""

import numpy as np

import bridge
import empathy_field as ef
import qualia as qu

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_N_AGENTS = ef.DEFAULT_N_AGENTS_RESONANCE
DEFAULT_SEED = ef.DEFAULT_SEED

# ---------------------------------------------------------------------------
# Pre-registered thresholds (frozen from the pilot sweeps,
# REPORT.md section 16, and never moved after the final
# measurement run).
# ---------------------------------------------------------------------------

# Fine sigma grid for the gated fit: every row has BOTH
# marginals interior (0 < p_res < 1, 0 < p_ent < 1) at the
# baseline thresholds, so the fit tests independence rather
# than a degenerate p_res = 1.
PRODUCT_FIT_SIGMA_GRID = (0.30, 0.35, 0.40, 0.45, 0.50, 0.60,
                          0.70, 0.80, 0.90, 1.00, 1.25, 1.50)

# Fit tolerances: pilot mean relative error 0.0289, max
# 0.0667 (seed 42, fine grid); 0.10 / 0.20 are round numbers
# well above the pilot, not tuned to its edge.
PRODUCT_FIT_MEAN_MAX = 0.10
PRODUCT_FIT_ROW_MAX = 0.20

# Peak-shift settings: NU_MIN 0.10 -> 0.25 (R_MIN held at
# 0.5) and R_MIN 0.5 -> 0.25 (NU_MIN held at 0.10). Pilot
# predicted and measured peaks: 0.4143 and 0.2839, both
# above the baseline peak f = 0.1803.
PEAK_SHIFT_NU_MIN = 0.25
PEAK_SHIFT_R_MIN = 0.25


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("PRODUCT_FIT_MEAN_MAX", PRODUCT_FIT_MEAN_MAX),
        ("PRODUCT_FIT_ROW_MAX", PRODUCT_FIT_ROW_MAX),
        ("PEAK_SHIFT_NU_MIN", PEAK_SHIFT_NU_MIN),
        ("PEAK_SHIFT_R_MIN", PEAK_SHIFT_R_MIN),
    ) if value is None]
    if missing:
        raise ValueError(
            "product-model thresholds are unset: run the pilot "
            "sweeps and set " + ", ".join(missing) + " first "
            "(REPORT.md section 16)")
    return {
        "fit_mean_max": float(PRODUCT_FIT_MEAN_MAX),
        "fit_row_max": float(PRODUCT_FIT_ROW_MAX),
        "peak_shift_nu_min": float(PEAK_SHIFT_NU_MIN),
        "peak_shift_r_min": float(PEAK_SHIFT_R_MIN),
    }


# ---------------------------------------------------------------------------
# Marginals and the product prediction
# ---------------------------------------------------------------------------

def pair_marginals(states, r_min=None, nu_min=None):
    """The two marginals of one field: p_res, p_ent, and counts.

    p_res = fraction of pairs with R >= r_min; p_ent =
    fraction with nu >= nu_min. The marginals are measured on
    the same pairs as the quale count -- the product built
    from them tests independence of the two indicators
    across pairs.
    """
    r_min = ef.RESONANCE_R_MIN if r_min is None else float(r_min)
    nu_min = qu.QUALIA_NU_MIN if nu_min is None else float(nu_min)
    states = list(states)
    if len(states) < 2:
        raise ValueError("need at least two agents for a field")
    n_pairs = len(states) * (len(states) - 1) // 2
    n_res = 0
    n_ent = 0
    for i in range(len(states)):
        for j in range(i + 1, len(states)):
            if ef.overlap_squared(states[i], states[j]) >= r_min:
                n_res += 1
            if ef.pair_frequency(states[i], states[j]) >= nu_min:
                n_ent += 1
    return {
        "n_pairs": n_pairs,
        "n_resonant": n_res,
        "n_entangled": n_ent,
        "p_res": n_res / n_pairs,
        "p_ent": n_ent / n_pairs,
    }


def product_prediction(states, r_min=None, nu_min=None):
    """The product-model predicted quale count: N * p_res * p_ent."""
    m = pair_marginals(states, r_min, nu_min)
    return {
        "predicted": m["n_pairs"] * m["p_res"] * m["p_ent"],
        "measured": qu.qualia_count(states, r_min=r_min,
                                    nu_min=nu_min),
        "p_res": m["p_res"],
        "p_ent": m["p_ent"],
        "n_pairs": m["n_pairs"],
        "n_resonant": m["n_resonant"],
        "n_entangled": m["n_entangled"],
    }


def product_fit_rows(sigmas=None, n_agents=DEFAULT_N_AGENTS,
                     seed=DEFAULT_SEED, r_min=None, nu_min=None):
    """One row per sigma: f, marginals, predicted vs measured count.

    The relative error is None on rows with predicted == 0
    (no prediction to compare -- an empty field, not a zero
    error).
    """
    rows = []
    for sigma in (PRODUCT_FIT_SIGMA_GRID
                  if sigmas is None else sigmas):
        states = ef.resonance_population(sigma, n_agents, seed)
        pred = product_prediction(states, r_min=r_min, nu_min=nu_min)
        predicted = pred["predicted"]
        measured = pred["measured"]
        rows.append({
            "sigma": float(sigma),
            "f": float(ef.empathy_fraction(states)),
            "p_res": pred["p_res"],
            "p_ent": pred["p_ent"],
            "n_resonant": pred["n_resonant"],
            "n_entangled": pred["n_entangled"],
            "n_pairs": pred["n_pairs"],
            "predicted": float(predicted),
            "measured": int(measured),
            "relative_error": (
                None if predicted == 0.0
                else float(abs(measured - predicted) / predicted)),
            "interior": (0.0 < pred["p_res"] < 1.0
                         and 0.0 < pred["p_ent"] < 1.0),
        })
    return rows


def peak_from_rows(rows, key):
    """The row with the largest `key` value (first on ties)."""
    return max(rows, key=lambda r: r[key])


# ---------------------------------------------------------------------------
# Peak shift: predict the peak from the marginals, then measure it
# ---------------------------------------------------------------------------

def peak_shift_setting(r_min=None, nu_min=None, sigmas=None,
                       n_agents=DEFAULT_N_AGENTS, seed=DEFAULT_SEED):
    """Predicted vs measured peak f at one threshold setting.

    The predicted curve is built from the marginals only
    (p_res, p_ent per sigma); the measured curve is the
    joint AND-count. The two peaks are compared after both
    are computed -- the marginals never see the counts.
    """
    rows = product_fit_rows(sigmas, n_agents, seed,
                            r_min=r_min, nu_min=nu_min)
    pred_peak = peak_from_rows(rows, "predicted")
    meas_peak = peak_from_rows(rows, "measured")
    return {
        "r_min": (ef.RESONANCE_R_MIN if r_min is None
                  else float(r_min)),
        "nu_min": (qu.QUALIA_NU_MIN if nu_min is None
                   else float(nu_min)),
        "predicted_peak_f": pred_peak["f"],
        "predicted_peak_count": pred_peak["predicted"],
        "measured_peak_f": meas_peak["f"],
        "measured_peak_count": meas_peak["measured"],
        "peak_f_match": pred_peak["f"] == meas_peak["f"],
        "rows": rows,
    }


def baseline_peak_f(n_agents=DEFAULT_N_AGENTS, seed=DEFAULT_SEED):
    """The measured peak f at the baseline thresholds."""
    rows = product_fit_rows(ef.SIGMA_GRID, n_agents, seed)
    return peak_from_rows(rows, "measured")["f"]


# ---------------------------------------------------------------------------
# Single-condition counts (the hump-vanish control)
# ---------------------------------------------------------------------------

def single_condition_rows(sigmas=None, n_agents=DEFAULT_N_AGENTS,
                          seed=DEFAULT_SEED):
    """Resonance-only, entanglement-only, and both counts vs f.

    The single-condition counts use a vacuous second
    threshold (nu_min = 0 counts every pair as entangled;
    r_min = 0 counts every pair as resonant), so each row
    is the marginal count on its own.
    """
    rows = []
    for sigma in (ef.SIGMA_GRID if sigmas is None else sigmas):
        states = ef.resonance_population(sigma, n_agents, seed)
        f = float(ef.empathy_fraction(states))
        n_res = qu.qualia_count(states, nu_min=0.0)
        n_ent = qu.qualia_count(states, r_min=0.0)
        n_both = qu.qualia_count(states)
        rows.append({
            "sigma": float(sigma),
            "f": f,
            "n_resonant_only": int(n_res),
            "n_entangled_only": int(n_ent),
            "n_both": int(n_both),
        })
    return rows


def _is_non_increasing(values):
    return all(values[i + 1] <= values[i]
               for i in range(len(values) - 1))


def _is_non_decreasing(values):
    return all(values[i + 1] >= values[i]
               for i in range(len(values) - 1))


# ---------------------------------------------------------------------------
# Claims (xxvi)-(xxviii): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_product_fit_verdict(sigmas=None,
                              n_agents=DEFAULT_N_AGENTS,
                              seed=DEFAULT_SEED):
    """(xxvi) The product model fits the humped quale count.

    PASS iff, on the fine grid at seed 42, the mean
    relative error over rows with predicted > 0 is at most
    PRODUCT_FIT_MEAN_MAX and the largest single-row error
    is at most PRODUCT_FIT_ROW_MAX. The standard-grid fit
    is reported, not gated: p_res = 1.0 below sigma = 0.5
    there, so the product is degenerate on those rows.
    """
    t = _thresholds()
    rows = product_fit_rows(sigmas, n_agents, seed)
    scored = [r for r in rows if r["relative_error"] is not None]
    mean_err = (float(np.mean([r["relative_error"] for r in scored]))
                if scored else None)
    max_err = (float(max(r["relative_error"] for r in scored))
               if scored else None)
    check_mean = mean_err is not None and mean_err <= t["fit_mean_max"]
    check_max = max_err is not None and max_err <= t["fit_row_max"]
    standard = product_fit_rows(ef.SIGMA_GRID, n_agents, seed)
    scored_std = [r for r in standard
                  if r["relative_error"] is not None]
    passed = bool(check_mean and check_max)
    return {
        "claim": "(xxvi) the product model fits the humped quale count",
        "passed": passed,
        "checks": {
            "mean_relative_error_at_most_max": bool(check_mean),
            "max_row_error_at_most_max": bool(check_max),
        },
        "fit_mean_max": t["fit_mean_max"],
        "fit_row_max": t["fit_row_max"],
        "mean_relative_error": mean_err,
        "max_relative_error": max_err,
        "n_scored_rows": len(scored),
        "n_interior_rows": sum(1 for r in rows if r["interior"]),
        "standard_grid_mean_error": (
            float(np.mean([r["relative_error"] for r in scored_std]))
            if scored_std else None),
        "standard_grid_max_error": (
            float(max(r["relative_error"] for r in scored_std))
            if scored_std else None),
        "rows": rows,
    }


def claim_peak_shift_verdict(sigmas=None,
                             n_agents=DEFAULT_N_AGENTS,
                             seed=DEFAULT_SEED):
    """(xxvii) The peak moves as the product model predicts.

    PASS iff, at each shifted setting, the product-predicted
    peak f equals the measured peak f, AND both measured
    peaks sit above the baseline peak f. The predicted peak
    is computed from the marginals alone; the measured peak
    from the joint counts.
    """
    t = _thresholds()
    base_f = baseline_peak_f(n_agents, seed)
    # The peak shift is judged on the STANDARD grid (the
    # hump's home grid, REPORT.md section 12) -- not the
    # fine fit grid, whose extra sigmas would move the peak
    # by grid resolution alone.
    grid = ef.SIGMA_GRID if sigmas is None else sigmas
    nu_shift = peak_shift_setting(
        nu_min=t["peak_shift_nu_min"], sigmas=grid,
        n_agents=n_agents, seed=seed)
    r_shift = peak_shift_setting(
        r_min=t["peak_shift_r_min"], sigmas=grid,
        n_agents=n_agents, seed=seed)
    check_nu = bool(nu_shift["peak_f_match"])
    check_r = bool(r_shift["peak_f_match"])
    check_dir_nu = nu_shift["measured_peak_f"] > base_f
    check_dir_r = r_shift["measured_peak_f"] > base_f
    passed = bool(check_nu and check_r and check_dir_nu
                  and check_dir_r)
    return {
        "claim": "(xxvii) the quale-count peak moves as the "
                 "product model predicts",
        "passed": passed,
        "checks": {
            "nu_shift_predicted_peak_matches": check_nu,
            "r_shift_predicted_peak_matches": check_r,
            "nu_shift_peak_above_baseline": bool(check_dir_nu),
            "r_shift_peak_above_baseline": bool(check_dir_r),
        },
        "baseline_peak_f": base_f,
        "nu_shift": {k: nu_shift[k] for k in (
            "r_min", "nu_min", "predicted_peak_f",
            "predicted_peak_count", "measured_peak_f",
            "measured_peak_count", "peak_f_match")},
        "r_shift": {k: r_shift[k] for k in (
            "r_min", "nu_min", "predicted_peak_f",
            "predicted_peak_count", "measured_peak_f",
            "measured_peak_count", "peak_f_match")},
    }


def claim_hump_vanish_verdict(sigmas=None,
                              n_agents=DEFAULT_N_AGENTS,
                              seed=DEFAULT_SEED):
    """(xxviii) The hump vanishes when either condition is dropped.

    PASS iff the resonance-only count is non-increasing in
    f AND the entanglement-only count is non-decreasing in
    f, while the both-condition count is non-monotone in f
    (it rises then falls). If a single-condition count
    still humps, the hump lives in a marginal, not in the
    AND -- and the product model is the wrong explanation.
    """
    rows = single_condition_rows(sigmas, n_agents, seed)
    ordered = sorted(rows, key=lambda r: r["f"])
    res_counts = [r["n_resonant_only"] for r in ordered]
    ent_counts = [r["n_entangled_only"] for r in ordered]
    both_counts = [r["n_both"] for r in ordered]
    check_res = _is_non_increasing(res_counts)
    check_ent = _is_non_decreasing(ent_counts)
    check_both = not (_is_non_increasing(both_counts)
                      or _is_non_decreasing(both_counts))
    passed = bool(check_res and check_ent and check_both)
    return {
        "claim": "(xxviii) the hump vanishes when either "
                 "condition is dropped",
        "passed": passed,
        "checks": {
            "resonance_only_non_increasing": bool(check_res),
            "entanglement_only_non_decreasing": bool(check_ent),
            "both_condition_non_monotone": bool(check_both),
        },
        "counts_vs_f": [(r["f"], r["n_resonant_only"],
                         r["n_entangled_only"], r["n_both"])
                        for r in ordered],
        "rows": rows,
    }


def product_model_claims():
    """The three product-model claims (xxvi)-(xxviii), measured fresh."""
    claim_xxvi = claim_product_fit_verdict()
    claim_xxvii = claim_peak_shift_verdict()
    claim_xxviii = claim_hump_vanish_verdict()
    verdicts = [claim_xxvi, claim_xxvii, claim_xxviii]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_xxvi_product_fit": claim_xxvi,
        "claim_xxvii_peak_shift": claim_xxvii,
        "claim_xxviii_hump_vanish": claim_xxviii,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the product-model fit, the peak shifts, and the
    hump-vanish control with the claims (xxvi)-(xxviii)
    verdicts."""
    print("Product model for the humped quale count "
          "-- claims (xxvi)-(xxviii)")
    print()
    verdicts = product_model_claims()
    xxvi = verdicts["claim_xxvi_product_fit"]
    print("Product fit on the fine grid (seed 42):")
    for r in xxvi["rows"]:
        err = ("None" if r["relative_error"] is None
               else f"{r['relative_error']:.4f}")
        print(f"  sigma = {r['sigma']:>5}: f = {r['f']:.4f}, "
              f"p_res = {r['p_res']:.3f}, p_ent = {r['p_ent']:.3f}, "
              f"predicted = {r['predicted']:5.2f}, "
              f"measured = {r['measured']:>2}, rel err = {err}")
    print(f"  mean rel err = {xxvi['mean_relative_error']:.4f} "
          f"(max {xxvi['fit_mean_max']}), "
          f"max row err = {xxvi['max_relative_error']:.4f} "
          f"(max {xxvi['fit_row_max']})")
    print(f"  standard grid (reported, not gated): mean "
          f"{xxvi['standard_grid_mean_error']:.4f}, max "
          f"{xxvi['standard_grid_max_error']:.4f}")
    print(f"claim (xxvi) verdict: {'PASS' if xxvi['passed'] else 'FAIL'}")
    print()
    xxvii = verdicts["claim_xxvii_peak_shift"]
    print(f"Peak shift (baseline peak f = "
          f"{xxvii['baseline_peak_f']:.4f}):")
    for name, shift in (("NU_MIN -> 0.25", xxvii["nu_shift"]),
                        ("R_MIN -> 0.25", xxvii["r_shift"])):
        print(f"  {name}: predicted peak f = "
              f"{shift['predicted_peak_f']:.4f} "
              f"({shift['predicted_peak_count']:.2f}), measured peak f = "
              f"{shift['measured_peak_f']:.4f} "
              f"({shift['measured_peak_count']})")
    print(f"claim (xxvii) verdict: "
          f"{'PASS' if xxvii['passed'] else 'FAIL'}")
    print()
    xxviii = verdicts["claim_xxviii_hump_vanish"]
    print("Single-condition counts vs f (res / ent / both):")
    for f, n_res, n_ent, n_both in xxviii["counts_vs_f"]:
        print(f"  f = {f:.4f}: {n_res:>2} / {n_ent:>2} / {n_both:>2}")
    print(f"claim (xxviii) verdict: "
          f"{'PASS' if xxviii['passed'] else 'FAIL'}")
    print()
    print(f"claims (xxvi)-(xxviii): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
