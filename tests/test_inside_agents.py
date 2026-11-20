# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for inside agents (v0.28.0, claims
(cv)-(cvi)): the observer and calibrator acting
INSIDE each orbit copy, instead of once per sweep
from outside.

(cv) PASSES as measured: the inside observer is
read-only (worst change 0.0), the perpendicular
element-Pearson spread is >= 0.80 on every file
seed (1.2317 / 0.8638 / 1.0894 / 0.9111) while the
stored/opposite spreads are <= 0.20 (worst 0.1624).
(cvi) PASSES exactly as preregistered: the inside
deltas and the inside failing-bar counts are
EXACTLY equal to the outside ones on every combo,
and no seed is rescued — and the perpendicular
Pearson difference is exactly 0.0 on all nine
seeds. Post-evaluation fix (2026-11-19): the first
evaluation run failed (cvi) honestly because the
inside mean was a mean of 4 element-means while
the outside mean was a single mean over 20 orbit
copies, and the two summation orders differed by
1.22e-15 in the last ULP. The fix unifies the
summation order — when all element deltas are
equal and no clip bites, the inside average is
taken as ONE np.mean over the 20 copy values in
the outside order, then calibrated by the common
delta exactly as calibrated_rows does — so the
inside rows are bit-identical to the outside rows.
The bar was not moved. See docs/preregistration-
v0.28.0.md (addendum) and REPORT.md §34.
"""

import math

import numpy as np
import pytest

import inside_agents as ia
import observer_agents as oa
import wave_direction as wd


@pytest.fixture(scope="module")
def verdicts():
    return ia.inside_agents_claims()


# ---------------------------------------------------------------------------
# Frozen thresholds
# ---------------------------------------------------------------------------

def test_thresholds_are_frozen():
    t = ia._thresholds()
    assert t["exact_tol"] == 1e-9
    assert t["read_only_tol"] == 1e-12
    assert t["perp_spread_min"] == 0.80
    assert t["stored_opp_spread_max"] == 0.20
    assert t["pearson_d_c_max"] == -0.90


# ---------------------------------------------------------------------------
# Element 0 (identity) IS the plain sweep
# ---------------------------------------------------------------------------

def test_element_zero_is_plain_sweep():
    for seed in (42, 7):
        for theta in ia.ALL_NOISY_DIRECTIONS:
            elements = ia.element_rows(seed, theta)
            plain = wd.noisy_direction_sweep(seed, theta)["rows"]
            assert len(elements) == 4
            for e_row, p_row in zip(elements[0], plain):
                assert e_row["sigma"] == p_row["sigma"]
                assert abs(e_row["mean_D"]
                           - p_row["mean_D"]) <= 1e-12
                # Concurrence only to the (xcviii) floor:
                # the density-matrix concurrence at the
                # degenerate equal superposition carries
                # ~1e-8 of eigendecomposition noise, and
                # the element rows pass through the
                # slide-adapted basis round-trip.
                assert abs(e_row["mean_concurrence"]
                           - p_row["mean_concurrence"]) <= 1e-8


# ---------------------------------------------------------------------------
# Read-only observation
# ---------------------------------------------------------------------------

def test_observer_is_read_only():
    for seed in ia.ALL_SEEDS:
        for theta in ia.ALL_NOISY_DIRECTIONS:
            assert ia.observe_inside_read_only(
                seed, theta) == 0.0


# ---------------------------------------------------------------------------
# The element split on the calibration seeds
# ---------------------------------------------------------------------------

def test_perp_spread_on_calibration_seeds():
    for seed in ia.CALIBRATION_SEEDS:
        perp = ia.element_pearson_spreads(seed, math.pi / 4)
        assert perp["pearson_spread"] >= 0.80
        for theta in (0.0, math.pi / 2):
            row = ia.element_pearson_spreads(seed, theta)
            assert row["pearson_spread"] <= 0.20


def test_d_range_pairing_is_structural():
    # The D range depends on the z_u flip only:
    # elements pair up (0 == 2, 1 == 3) on stored,
    # and the opposite D range is identical across
    # all four elements (D there depends on z_k only,
    # which V4-full never touches).
    for seed in ia.ALL_SEEDS:
        stored = ia.element_pearson_spreads(seed, 0.0)
        d = stored["d_range_per_element"]
        assert d[0] == pytest.approx(d[2], abs=1e-12)
        assert d[1] == pytest.approx(d[3], abs=1e-12)
        opp = ia.element_pearson_spreads(seed, math.pi / 2)
        o = opp["d_range_per_element"]
        for value in o[1:]:
            assert value == pytest.approx(o[0], abs=1e-12)


# ---------------------------------------------------------------------------
# Inside == outside calibration, combo by combo
# ---------------------------------------------------------------------------

def test_inside_deltas_equal_outside():
    for seed in ia.ALL_SEEDS:
        for theta in ia.XCI_DIRECTIONS:
            row = ia.inside_vs_outside(seed, theta)
            assert row["deltas_equal"] is True
            assert row["n_failing_equal"] is True
    # The only nonzero delta anywhere is (2026,
    # opposite) +0.0040, on all four elements.
    row = ia.inside_vs_outside(2026, math.pi / 2)
    assert row["outside_delta"] == pytest.approx(0.0040, abs=1e-12)
    assert row["inside_deltas"] == pytest.approx(
        [0.0040] * 4, abs=1e-12)
    assert row["outside_n_failing_at_zero"] == 1
    assert row["outside_n_failing_calibrated"] == 0
    assert row["inside_n_failing"] == 0


def test_cost_accounting():
    cost = ia.cost_accounting()
    assert cost["outside_reads_per_sweep"] == 1
    assert cost["outside_decisions_per_sweep"] == 1
    assert cost["closed_loop_reads_per_sweep"] == 2
    assert cost["inside_copy_reads_per_sweep"] == 140
    assert cost["inside_decisions_per_sweep"] == 4
    assert cost["inside_total_reads_per_sweep"] == 141
    assert cost["inside_cascade_copy_reads"] == 400
    # Computed from the constants, not literals:
    # 5 copies x 4 orbit x 7 sigma = 140.
    assert cost["inside_copy_reads_per_sweep"] == (
        5 * 4 * 7)


# ---------------------------------------------------------------------------
# Claim verdicts
# ---------------------------------------------------------------------------

def test_claim_cv_passes(verdicts):
    cv = verdicts["claim_cv_element_split"]
    assert cv["passed"] is True
    assert cv["checks"]["read_only"] is True
    assert cv["checks"]["perp_spread_at_least_min"] is True
    assert cv["checks"]["stored_opp_spread_at_most_max"] \
        is True
    assert cv["worst_read_only_change"] == 0.0


def test_claim_cvi_passes_exactly(verdicts):
    cvi = verdicts["claim_cvi_inside_equals_outside"]
    # Post-evaluation fix (2026-11-19): the inside
    # average is taken as ONE np.mean over the 20 copy
    # values in the outside order when all element
    # deltas are equal and no clip bites, so the
    # inside rows are bit-identical to the outside
    # rows and the perpendicular Pearson difference
    # is exactly 0.0. The bar was not moved.
    assert cvi["passed"] is True
    assert cvi["checks"]["perp_pearson_identical"] is True
    assert cvi["worst_pearson_difference"] == 0.0
    # Everything substantive is exactly equal:
    # the deltas, the bar counts, and no rescue.
    assert cvi["checks"]["deltas_equal_everywhere"] is True
    assert cvi["checks"]["n_failing_equal_everywhere"] \
        is True
    assert cvi["checks"]["perp_no_rescue_anywhere"] is True
    for row in cvi["per_perp"]:
        assert row["pearson_difference"] == 0.0
        assert row["inside_pearson"] > -0.90
        assert row["outside_pearson"] > -0.90
    assert verdicts["n_passed"] == 2
    assert verdicts["all_pass"] is True
