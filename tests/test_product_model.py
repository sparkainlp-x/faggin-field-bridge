# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for product_model.py: product-model fit for the humped
quale count (v0.10.0, deep-think upgrade #3)."""

import numpy as np
import pytest

import bridge
import empathy_field as ef
import product_model as pm
import qualia as qu


def _states(sigma, n=8, seed=42):
    return ef.resonance_population(sigma, n, seed)


def test_marginals_at_zero_noise():
    # At sigma = 0 every pair is resonant (R = 1) and none is
    # entangled (nu = 0): the product is 0, and so is the count.
    m = pm.pair_marginals(_states(0.0))
    assert m["n_pairs"] == 28
    assert m["p_res"] == pytest.approx(1.0)
    assert m["p_ent"] == pytest.approx(0.0)
    assert m["n_resonant"] == 28
    assert m["n_entangled"] == 0
    pred = pm.product_prediction(_states(0.0))
    assert pred["predicted"] == pytest.approx(0.0)
    assert pred["measured"] == 0


def test_marginals_at_sigma_025():
    # p_res is still exactly 1.0 at sigma = 0.25, so the
    # product is just the entanglement count: 17.
    m = pm.pair_marginals(_states(0.25))
    assert m["p_res"] == pytest.approx(1.0)
    assert m["p_ent"] == pytest.approx(17 / 28)
    assert m["n_entangled"] == 17
    pred = pm.product_prediction(_states(0.25))
    assert pred["predicted"] == pytest.approx(17.0)
    assert pred["measured"] == 17


def test_marginals_at_sigma_05():
    # The first row where both marginals are interior:
    # 17/28 resonant, 21/28 entangled, product 12.75 vs 13.
    m = pm.pair_marginals(_states(0.5))
    assert m["p_res"] == pytest.approx(17 / 28)
    assert m["p_ent"] == pytest.approx(21 / 28)
    assert m["n_resonant"] == 17
    assert m["n_entangled"] == 21
    pred = pm.product_prediction(_states(0.5))
    assert pred["predicted"] == pytest.approx(12.75)
    assert pred["measured"] == 13


def test_product_prediction_at_sigma_01():
    pred = pm.product_prediction(_states(0.1))
    assert pred["predicted"] == pytest.approx(9.0)
    assert pred["measured"] == 9


def test_fit_rows_fine_grid_all_interior():
    # The gated fine grid was chosen so both marginals are
    # interior on every row -- the fit tests independence,
    # not a degenerate p_res = 1.
    rows = pm.product_fit_rows()
    assert len(rows) == 12
    assert all(r["interior"] for r in rows)
    assert all(r["relative_error"] is not None for r in rows)


def test_fit_rows_relative_error_none_when_predicted_zero():
    rows = pm.product_fit_rows(sigmas=[0.0, 0.01])
    assert all(r["predicted"] == pytest.approx(0.0) for r in rows)
    assert all(r["relative_error"] is None for r in rows)
    assert all(r["measured"] == 0 for r in rows)


def test_claim_xxvi_passes_with_measured_numbers():
    verdict = pm.claim_product_fit_verdict()
    assert verdict["passed"] is True
    assert verdict["mean_relative_error"] == pytest.approx(
        0.0289, abs=1e-3)
    assert verdict["max_relative_error"] == pytest.approx(
        0.0667, abs=1e-3)
    assert verdict["n_scored_rows"] == 12
    assert verdict["n_interior_rows"] == 12
    assert verdict["standard_grid_mean_error"] == pytest.approx(
        0.0119, abs=1e-3)
    assert verdict["standard_grid_max_error"] == pytest.approx(
        0.0400, abs=1e-3)


def test_claim_xxvi_seed_spread():
    # Seeds 1 and 3 pass the same frozen bar; seed 2 does
    # not -- the independence assumption is seed-dependent,
    # and the failure is reported, not hidden.
    for seed in (1, 3):
        verdict = pm.claim_product_fit_verdict(seed=seed)
        assert verdict["passed"] is True
    verdict2 = pm.claim_product_fit_verdict(seed=2)
    assert verdict2["passed"] is False
    assert verdict2["mean_relative_error"] == pytest.approx(
        0.1666, abs=1e-3)
    assert verdict2["max_relative_error"] == pytest.approx(
        0.3636, abs=1e-3)


def test_baseline_peak_f():
    assert pm.baseline_peak_f() == pytest.approx(0.1803, abs=1e-4)


def test_claim_xxvii_passes_with_measured_peaks():
    verdict = pm.claim_peak_shift_verdict()
    assert verdict["passed"] is True
    assert verdict["baseline_peak_f"] == pytest.approx(
        0.1803, abs=1e-4)
    nu_shift = verdict["nu_shift"]
    assert nu_shift["predicted_peak_f"] == pytest.approx(
        0.4143, abs=1e-4)
    assert nu_shift["measured_peak_f"] == pytest.approx(
        0.4143, abs=1e-4)
    assert nu_shift["predicted_peak_count"] == pytest.approx(10.0)
    assert nu_shift["measured_peak_count"] == 11
    r_shift = verdict["r_shift"]
    assert r_shift["predicted_peak_f"] == pytest.approx(
        0.2839, abs=1e-4)
    assert r_shift["measured_peak_f"] == pytest.approx(
        0.2839, abs=1e-4)
    assert r_shift["predicted_peak_count"] == pytest.approx(18.0)
    assert r_shift["measured_peak_count"] == 18


def test_peak_shift_no_shift_at_baseline():
    # At the baseline thresholds the peak sits at 0.1803 --
    # the direction check in (xxvii) bites: no threshold
    # change, no shift.
    setting = pm.peak_shift_setting(sigmas=ef.SIGMA_GRID)
    assert setting["measured_peak_f"] == pytest.approx(
        0.1803, abs=1e-4)
    assert setting["measured_peak_f"] == pm.baseline_peak_f()


def test_peak_from_marginals_only():
    # The predicted peak is computed from the marginals
    # alone: the rows carry predicted and measured as
    # separate columns, and the predicted peak never reads
    # the measured column.
    rows = pm.product_fit_rows(
        ef.SIGMA_GRID, nu_min=pm.PEAK_SHIFT_NU_MIN)
    pred_peak = pm.peak_from_rows(rows, "predicted")
    meas_peak = pm.peak_from_rows(rows, "measured")
    assert pred_peak["f"] == meas_peak["f"]
    assert pred_peak["predicted"] == pytest.approx(10.0)


def test_claim_xxviii_passes():
    verdict = pm.claim_hump_vanish_verdict()
    assert verdict["passed"] is True
    assert verdict["counts_vs_f"] == [
        (pytest.approx(0.0), 28, 0, 0),
        (pytest.approx(0.0086, abs=1e-4), 28, 0, 0),
        (pytest.approx(0.0415, abs=1e-4), 28, 1, 1),
        (pytest.approx(0.0802, abs=1e-4), 28, 9, 9),
        (pytest.approx(0.1803, abs=1e-4), 28, 17, 17),
        (pytest.approx(0.2839, abs=1e-4), 17, 21, 13),
        (pytest.approx(0.4143, abs=1e-4), 14, 25, 12),
    ]


def test_single_condition_counts_exact():
    rows = pm.single_condition_rows()
    by_f = {round(r["f"], 4): r for r in rows}
    last = by_f[0.4143]
    assert last["n_resonant_only"] == 14
    assert last["n_entangled_only"] == 25
    assert last["n_both"] == 12
    first = by_f[0.0]
    assert first["n_resonant_only"] == 28
    assert first["n_entangled_only"] == 0
    assert first["n_both"] == 0


def test_pair_marginals_errors():
    with pytest.raises(ValueError):
        pm.pair_marginals(_states(0.25)[:1])
    with pytest.raises(ValueError):
        pm.product_prediction([])


def test_product_model_claims_summary():
    verdicts = pm.product_model_claims()
    assert verdicts["n_claims"] == 3
    assert verdicts["n_passed"] == 3
    assert verdicts["all_pass"] is True
    assert verdicts["headline_allowed"] is bridge.HEADLINE_ALLOWED
    assert verdicts["headline_allowed"] is False


def test_thresholds_are_frozen_numbers():
    t = pm._thresholds()
    assert t["fit_mean_max"] == pytest.approx(0.10)
    assert t["fit_row_max"] == pytest.approx(0.20)
    assert t["peak_shift_nu_min"] == pytest.approx(0.25)
    assert t["peak_shift_r_min"] == pytest.approx(0.25)
    assert len(pm.PRODUCT_FIT_SIGMA_GRID) == 12
    assert pm.PRODUCT_FIT_SIGMA_GRID[0] == pytest.approx(0.30)
    assert pm.PRODUCT_FIT_SIGMA_GRID[-1] == pytest.approx(1.50)


def test_fit_explains_f_star_vs_f_peak_gap():
    # Descriptive, not gated: the product peak (0.1803) and
    # the attunement flip f* (0.7278) are different
    # quantities -- a count peak vs a status threshold -- so
    # the product model explains why they differ without
    # any extra mechanism.
    assert pm.baseline_peak_f() == pytest.approx(0.1803, abs=1e-4)
    assert qu.QUALIA_NU_MIN == pytest.approx(0.10)
