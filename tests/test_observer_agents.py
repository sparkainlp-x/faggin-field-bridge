# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for the observer and calibration agents (v0.26.0,
claims (xciii)-(xcvii)): the read-only observer and the
bounded calibrator, inserted into the wave-direction /
observer-cycle setup.

All five claims PASS as measured. The agent rescues the
(xci) D-range miss — (2026, opposite) D range 0.2490 ->
0.2500 at delta = +0.0040 — but the (2026, stored)
Pearson miss survives: no delta in the bound moves
Pearson to -0.90 or below (the clip at D = 1.0 moves it
the wrong way, toward zero). The perpendicular inversion
survives bounded calibration on every seed (Pearson
+0.5109 / +0.8297 held-out, agent holding delta = 0).
The (xci) and (xcii) verdicts stay FAIL on the record as
originally stated. See docs/preregistration-v0.26.0.md.
"""

import dataclasses
import math

import numpy as np
import pytest

import observer_agents as oa
import observer_cycle as oc
import wave_direction as wd


@pytest.fixture(scope="module")
def verdicts():
    return oa.observer_agents_claims()


# ---------------------------------------------------------------------------
# Frozen thresholds and bounds
# ---------------------------------------------------------------------------

def test_thresholds_frozen():
    assert oa.DELTA_MIN == -0.05
    assert oa.DELTA_MAX == 0.05
    assert oa.DELTA_GRID_POINTS == 201
    assert oa.EXACT_TOL == 1e-9
    assert oa.READ_ONLY_TOL == 1e-12
    assert oa.PEARSON_D_C_MAX == -0.90
    assert oa.SPEARMAN_D_C_MAX == -0.90
    assert oa.D_RANGE_MIN == 0.25
    assert oa.C_RANGE_MIN == 0.25
    t = oa._thresholds()
    assert t["delta_min"] == -0.05
    assert t["delta_max"] == 0.05
    assert t["delta_grid_points"] == 201
    assert t["exact_tol"] == 1e-9
    assert t["read_only_tol"] == 1e-12
    assert oa.min_rescuable_d_range() == pytest.approx(0.25 / 1.05)


# ---------------------------------------------------------------------------
# Observer agent: read-only, reports the direct quantities
# ---------------------------------------------------------------------------

def test_observer_state_unchanged():
    observer = oa.DirectionObserver()
    worst = 0.0
    for theta in wd.DIRECTION_GRID:
        psi = oc.slide_state(theta)
        before = psi.copy()
        observer.observe_slide(psi)
        worst = max(worst, float(np.max(np.abs(psi - before))))
    assert worst == 0.0
    assert worst <= oa.READ_ONLY_TOL


def test_observer_report_matches_direct():
    verdict = oa.claim_observer_read_only_verdict()
    assert verdict["worst_state_change"] == 0.0
    assert verdict["worst_report_error"] == 0.0
    assert verdict["worst_report_error"] <= oa.EXACT_TOL


def test_observer_report_endpoint_values():
    observer = oa.DirectionObserver()
    stored = observer.observe_direction(0.0)
    assert stored.d == pytest.approx(1.0, abs=1e-9)
    assert stored.concurrence == pytest.approx(0.0, abs=1e-9)
    assert stored.r_stored == pytest.approx(1.0, abs=1e-9)
    assert stored.r_kernel == pytest.approx(0.0, abs=1e-9)
    opposite = observer.observe_direction(math.pi / 2)
    assert opposite.d == pytest.approx(0.0, abs=1e-9)
    assert opposite.concurrence == pytest.approx(1.0, abs=1e-9)
    assert opposite.r_stored == pytest.approx(0.0, abs=1e-9)
    assert opposite.r_kernel == pytest.approx(1.0, abs=1e-9)
    mid = observer.observe_direction(math.pi / 4)
    assert mid.d == pytest.approx(0.5, abs=1e-9)
    assert mid.concurrence == pytest.approx(0.5, abs=1e-9)
    assert mid.c_plus_d == pytest.approx(1.0, abs=1e-9)


def test_observer_observation_is_frozen_and_deterministic():
    observer = oa.DirectionObserver()
    first = observer.observe_direction(math.pi / 6)
    second = observer.observe_direction(math.pi / 6)
    assert first == second
    with pytest.raises(dataclasses.FrozenInstanceError):
        first.d = 0.0


# ---------------------------------------------------------------------------
# Calibrator agent: bounded, delta = 0 is the identity
# ---------------------------------------------------------------------------

def test_calibrator_clips_to_bound():
    calibrator = oa.SweepCalibrator()
    assert calibrator.set_delta(0.5) == 0.05
    assert calibrator.set_delta(-0.5) == -0.05
    assert calibrator.set_delta(0.03) == 0.03
    assert calibrator.delta == 0.03
    assert calibrator.set_delta(0.0) == 0.0


def test_calibrator_delta_zero_is_identity():
    sweep = wd.noisy_direction_sweep(42, 0.0)
    rows0 = oa.calibrated_rows(sweep["rows"], 0.0)
    assert max(abs(a["mean_D"] - b["mean_D"])
               for a, b in zip(rows0, sweep["rows"])) == 0.0
    assert max(abs(a["mean_concurrence"] - b["mean_concurrence"])
               for a, b in zip(rows0, sweep["rows"])) == 0.0


def test_calibrated_rows_scale_d_only():
    sweep = wd.noisy_direction_sweep(42, math.pi / 2)
    rows = oa.calibrated_rows(sweep["rows"], 0.05)
    for raw, cal in zip(sweep["rows"], rows):
        assert cal["mean_concurrence"] == raw["mean_concurrence"]
        assert cal["mean_D"] == pytest.approx(
            raw["mean_D"] * 1.05, abs=1e-15)


# ---------------------------------------------------------------------------
# The clip finding: invariance holds only where no clipping bites
# ---------------------------------------------------------------------------

def test_correlations_invariant_where_no_clip_bites():
    for seed in (42, 7):
        for theta in (math.pi / 2, math.pi / 4):
            sweep = wd.noisy_direction_sweep(seed, theta)
            base = oa.sweep_bars(sweep["rows"])
            assert not oa.clip_affected(sweep["rows"], 0.05)
            for delta in (-0.05, 0.05):
                bars = oa.sweep_bars(
                    oa.calibrated_rows(sweep["rows"], delta))
                assert abs(bars["pearson_d_c"]
                           - base["pearson_d_c"]) <= 1e-12
                assert abs(bars["spearman_d_c"]
                           - base["spearman_d_c"]) <= 1e-12


def test_clip_moves_stored_direction_correlations():
    for seed in (42, 7):
        sweep = wd.noisy_direction_sweep(seed, 0.0)
        assert oa.clip_affected(sweep["rows"], 0.05)
        base = oa.sweep_bars(sweep["rows"])
        bars = oa.sweep_bars(
            oa.calibrated_rows(sweep["rows"], 0.05))
        # The D = 1.0 sigma = 0 point clips: the correlations
        # move toward zero, never toward the bar.
        assert bars["pearson_d_c"] > base["pearson_d_c"] + 0.01
        assert bars["spearman_d_c"] > base["spearman_d_c"] + 0.05
        # And the D range shrinks, it does not grow.
        assert bars["d_range"] < base["d_range"]


def test_unrescuable_below_min_range():
    # Synthetic sweep: D range 0.20, below the 0.2381 rescue
    # bound — no delta inside [-0.05, 0.05] reaches 0.25.
    rows = [{"sigma": s,
             "mean_D": 0.30 + 0.20 * i / 6.0,
             "mean_concurrence": 0.60 - 0.40 * i / 6.0}
            for i, s in enumerate(
                [0.0, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0])]
    assert oa.sweep_bars(rows)["d_range"] == pytest.approx(0.20)
    assert oa.sweep_bars(rows)["d_range"] < oa.min_rescuable_d_range()
    for delta in np.linspace(-0.05, 0.05, 201):
        bars = oa.sweep_bars(oa.calibrated_rows(rows, float(delta)))
        assert bars["d_range"] < 0.25


# ---------------------------------------------------------------------------
# The frozen rule
# ---------------------------------------------------------------------------

def test_rule_holds_zero_on_calibration_combos():
    for seed in (42, 7):
        for theta in (0.0, math.pi / 4, math.pi / 2):
            sweep = wd.noisy_direction_sweep(seed, theta)
            choice = oa.SweepCalibrator().choose_delta(sweep["rows"])
            assert choice["delta"] == 0.0


def test_rule_holds_zero_on_perpendicular_every_seed():
    for seed in (42, 7, 1234, 2026):
        result = oa.agent_sweep(seed, math.pi / 4)
        assert result["delta"] == 0.0
        assert result["n_failing_calibrated"] == \
            result["n_failing_at_zero"]


# ---------------------------------------------------------------------------
# Claims (xciii)-(xcvii)
# ---------------------------------------------------------------------------

def test_claim_xciii_observer_read_only_passes(verdicts):
    claim = verdicts["claim_xciii_observer_read_only"]
    assert claim["passed"] is True
    assert claim["worst_state_change"] == 0.0
    assert claim["worst_report_error"] == 0.0


def test_claim_xciv_calibrator_bounded_passes(verdicts):
    claim = verdicts["claim_xciv_calibrator_bounded"]
    assert claim["passed"] is True
    assert claim["clip_plus"] == 0.05
    assert claim["clip_minus"] == -0.05
    assert claim["worst_identity_error"] == 0.0
    assert all(-0.05 <= d <= 0.05 for d in claim["picked_deltas"])


def test_claim_xcv_d_range_rescue_passes(verdicts):
    claim = verdicts["claim_xcv_calibrated_d_range"]
    assert claim["passed"] is True
    per_combo = {(r["seed"], r["direction"]): r
                 for r in claim["per_combo"]}
    # Only (2026, opposite) needs a nonzero delta, and it is
    # the grid point the exact range requires: the exact
    # uncalibrated range is 0.2490105483 (the published
    # 0.2490 was a 4-decimal rounding), needing
    # delta >= 0.0039735; the first grid point is +0.0040.
    rescue = per_combo[(2026, "opposite")]
    assert rescue["delta"] == pytest.approx(0.0040, abs=1e-12)
    assert rescue["uncalibrated"]["d_range"] < 0.25
    assert rescue["calibrated"]["d_range"] >= 0.25
    assert rescue["n_failing_at_zero"] == 1
    assert rescue["n_failing_calibrated"] == 0
    for key, r in per_combo.items():
        if key != (2026, "opposite"):
            assert r["delta"] == 0.0
        assert r["calibrated"]["d_range"] >= 0.25
    # The (2026, stored) Pearson miss survives: the rule
    # holds delta = 0 there and the failing count stays 1.
    stored = per_combo[(2026, "stored")]
    assert stored["delta"] == 0.0
    assert stored["n_failing_calibrated"] == 1
    assert stored["calibrated"]["pearson_d_c"] == pytest.approx(
        -0.8828, abs=1e-4)


def test_claim_xcvi_perpendicular_survives_passes(verdicts):
    claim = verdicts["claim_xcvi_perpendicular_survives"]
    assert claim["passed"] is True
    expected = {42: -0.7982, 7: 0.1661, 1234: 0.5109,
                2026: 0.8297}
    for r in claim["per_seed"]:
        assert r["delta"] == 0.0
        assert r["calibrated"]["pearson_d_c"] > -0.90
        assert r["calibrated"]["pearson_d_c"] == pytest.approx(
            expected[r["seed"]], abs=1e-4)
        assert r["calibrated"]["pearson_d_c"] == \
            r["uncalibrated"]["pearson_d_c"]


def test_claim_xcvii_closed_loop_passes(verdicts):
    claim = verdicts["claim_xcvii_closed_loop"]
    assert claim["passed"] is True
    assert len(claim["per_combo"]) == 12
    for r in claim["per_combo"]:
        assert r["rounds"] == 2
        assert r["reads"] == 2
        assert r["delta_change"] == 0.0
        assert r["round2_max_row_error"] == 0.0
    rescue = [r for r in claim["per_combo"]
              if r["seed"] == 2026
              and r["direction"] == "opposite"][0]
    assert rescue["delta_round1"] == pytest.approx(
        0.0040, abs=1e-12)
    assert rescue["delta_held_round2"] == pytest.approx(
        0.0040, abs=1e-12)


def test_claims_aggregator(verdicts):
    assert verdicts["n_claims"] == 5
    assert verdicts["n_passed"] == 5
    assert verdicts["all_pass"] is True
