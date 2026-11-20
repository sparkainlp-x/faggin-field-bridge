# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for the symmetry sweep (v0.27.0, claims
(xcviii)-(cii)): the V4-full orbit-averaged noisy
direction sweep, built to fix the two v0.25.0 FAILs
from outside the calibrator.

Four of five claims PASS as measured. V4-full fixes
the (xci) claim 8/8 with the frozen calibrator rule
— (2026, stored) Pearson -0.8828 -> -0.9253 by
orbit-averaging alone, and the only nonzero delta
is (2026, opposite) +0.0040, D range 0.2490 ->
0.2500. The perpendicular inversion survives
symmetrization on every seed (Pearson -0.7256 /
+0.6364 / +0.3704 / +0.7481; D range < 0.25 on
every seed). Claim (xcviii) FAILS honestly: the
1e-12 bar is tighter than the concurrence
function's own numerical floor — the orbit
estimator itself is exact (D to 1e-16, relabelling
to 2.22e-16), but the density-matrix concurrence
at the degenerate equal superposition carries
~1e-8 of eigendecomposition noise (worst sigma = 0
error 6.57e-09, worst Z2-vs-pair difference
8.44e-09). The bar was not moved to force a pass.
The (xci), (xcii) and (xxxii) verdicts stay FAIL
on the record as originally stated. See
docs/preregistration-v0.27.0.md.
"""

import math

import numpy as np
import pytest

import symmetry_sweep as ss
import unity
import wave_direction as wd


@pytest.fixture(scope="module")
def verdicts():
    return ss.symmetry_sweep_claims()


# ---------------------------------------------------------------------------
# Frozen thresholds and the slide-adapted basis
# ---------------------------------------------------------------------------

def test_thresholds_are_frozen():
    t = ss._thresholds()
    assert t["orbit_tol"] == 1e-12
    assert t["exact_tol"] == 1e-9
    assert t["pearson_d_c_max"] == -0.90
    assert t["spearman_d_c_max"] == -0.90
    assert t["d_range_min"] == 0.25
    assert t["c_range_min"] == 0.25


def test_slide_basis_is_orthonormal():
    assert ss.basis_orthonormality_error() <= 1e-15


def test_basis_coordinates_round_trip():
    rng = np.random.default_rng(42)
    for _ in range(10):
        z = rng.standard_normal(4)
        assert np.max(np.abs(ss.from_coords(ss.to_coords(z)) - z)) \
            <= 1e-14


def test_noise_draws_reproduce_gaussian_copies_bit_for_bit():
    import observer_cycle as oc
    for seed in (42, 7, 1234, 2026):
        start = np.real(oc.slide_state(0.0))
        mine = [start + 0.25 * z for z in ss.draw_noise(seed)]
        mine = [v / np.linalg.norm(v) for v in mine]
        theirs = unity.gaussian_copies(start, 0.25, 5, seed)
        assert max(float(np.max(np.abs(a - b)))
                   for a, b in zip(mine, theirs)) == 0.0


# ---------------------------------------------------------------------------
# Groups
# ---------------------------------------------------------------------------

def test_group_orbit_sizes():
    assert len(ss.group_transforms("Z2-antipodal")) == 2
    assert len(ss.group_transforms("V4-plane")) == 4
    assert len(ss.group_transforms("D4-plane")) == 8
    assert len(ss.group_transforms("swap-only")) == 2
    assert len(ss.group_transforms("B4")) == 16
    assert len(ss.group_transforms("V4-full")) == 4


def test_unknown_group_raises():
    with pytest.raises(ValueError):
        ss.group_transforms("no-such-group")


def test_v4_full_never_flips_z_k():
    # Every V4-full transform leaves the kernel coordinate
    # untouched: z_k is never flipped.
    for f in ss.group_transforms("V4-full"):
        assert f((0.3, -0.7, 1.1, -0.2))[2] == pytest.approx(1.1)


def test_rejected_groups_break_opposite_d_range():
    # The (2026, opposite) D range under every group
    # that touches z_k falls below the rescuable bound
    # 0.25/1.05 = 0.2381; V4-full alone preserves 0.2490.
    expected = {
        "Z2-antipodal": 0.2042,
        "V4-plane": 0.2042,
        "D4-plane": 0.2214,
        "swap-only": 0.2317,
        "B4": 0.2042,
    }
    for name, d_range in expected.items():
        r = ss.symmetrized_sweep(2026, math.pi / 2, name)
        assert r["d_range"] == pytest.approx(d_range, abs=1e-4)
        assert r["d_range"] < 0.25 / 1.05
    v4 = ss.symmetrized_sweep(2026, math.pi / 2, "V4-full")
    assert v4["d_range"] == pytest.approx(0.2490, abs=1e-4)


# ---------------------------------------------------------------------------
# The V4-full sweep reproduces the pilot table
# ---------------------------------------------------------------------------

def test_v4_full_pilot_table():
    expected = {
        (42, 0.0): (-0.9472, 0.5713),
        (42, math.pi / 4): (-0.7256, 0.2365),
        (42, math.pi / 2): (-0.9736, 0.4380),
        (7, 0.0): (-0.9303, 0.4542),
        (7, math.pi / 4): (0.6364, 0.0514),
        (7, math.pi / 2): (-0.9672, 0.2884),
        (1234, 0.0): (-0.9460, 0.4908),
        (1234, math.pi / 4): (0.3704, 0.1141),
        (1234, math.pi / 2): (-0.9734, 0.3834),
        (2026, 0.0): (-0.9253, 0.4382),
        (2026, math.pi / 4): (0.7481, 0.0561),
        (2026, math.pi / 2): (-0.9878, 0.2490),
    }
    for (seed, theta), (pearson, d_range) in expected.items():
        r = ss.v4_full_sweep(seed, theta)
        assert r["pearson_d_c"] == pytest.approx(pearson, abs=1e-4)
        assert r["d_range"] == pytest.approx(d_range, abs=1e-4)


# ---------------------------------------------------------------------------
# Claim (xcviii): orbit estimator exactness — FAILS honestly
# ---------------------------------------------------------------------------

def test_claim_xcviii_fails_honestly(verdicts):
    claim = verdicts["claim_xcviii_orbit_estimator_exactness"]
    assert claim["passed"] is False
    # The D leg is exact and the relabelling leg passes;
    # the C leg carries the concurrence function's own
    # ~1e-8 eigendecomposition floor at the degenerate
    # equal superposition.
    assert claim["checks"]["relabel_invariant"] is True
    assert claim["checks"]["sigma0_exact"] is False
    assert claim["checks"]["z2_equals_pair_average"] is False
    assert claim["worst_sigma0_error"] == pytest.approx(
        6.57e-09, rel=0.05)
    assert claim["worst_relabel_change"] <= 1e-12
    assert claim["worst_pair_difference"] == pytest.approx(
        8.44e-09, rel=0.05)
    # The floor is in the density-matrix concurrence, not
    # in the orbit code: D is exact, concurrence_pure is
    # exact to ~1e-16, and only concurrence(density_matrix)
    # carries the ~1e-8 error at theta = pi/4.
    import self_knowing as sk
    import thought_entanglement as te
    import observer_cycle as oc
    psi = np.real(oc.slide_state(math.pi / 4))
    assert abs(sk.self_knowing_factor(psi) - 0.5) <= 1e-15
    assert abs(te.concurrence_pure(psi) - 0.5) <= 1e-15
    assert abs(te.concurrence(te.density_matrix(psi)) - 0.5) \
        == pytest.approx(6.54e-09, rel=0.05)


# ---------------------------------------------------------------------------
# Claim (xcix): stored Pearson rescue — PASS
# ---------------------------------------------------------------------------

def test_claim_xcix_passes(verdicts):
    claim = verdicts["claim_xcix_stored_pearson_rescue"]
    assert claim["passed"] is True
    by_seed = {r["seed"]: r for r in claim["per_seed"]}
    assert by_seed[2026]["pearson_d_c"] == pytest.approx(
        -0.9253, abs=1e-4)
    assert by_seed[42]["pearson_d_c"] == pytest.approx(
        -0.9472, abs=1e-4)
    assert by_seed[7]["pearson_d_c"] == pytest.approx(
        -0.9303, abs=1e-4)
    assert by_seed[1234]["pearson_d_c"] == pytest.approx(
        -0.9460, abs=1e-4)


# ---------------------------------------------------------------------------
# Claim (c): (xci) under symmetry + calibration — PASS
# ---------------------------------------------------------------------------

def test_claim_c_passes(verdicts):
    claim = verdicts["claim_c_symmetry_calibrated_xci"]
    assert claim["passed"] is True
    assert all(claim["checks"].values())
    deltas = {(r["seed"], r["direction"]): r["delta"]
              for r in claim["per_combo"]}
    # The only nonzero delta in the whole table.
    nonzero = {k: v for k, v in deltas.items() if v != 0.0}
    assert nonzero == {(2026, "opposite"): pytest.approx(0.0040)}
    combo = [r for r in claim["per_combo"]
             if r["seed"] == 2026
             and r["direction"] == "opposite"][0]
    assert combo["uncalibrated"]["d_range"] == pytest.approx(
        0.2490, abs=1e-4)
    assert combo["calibrated"]["d_range"] == pytest.approx(
        0.2500, abs=1e-4)
    assert combo["n_failing_at_zero"] == 1
    assert combo["n_failing_calibrated"] == 0


def test_calibrated_symmetry_sweep_reuses_frozen_rule():
    # The rule is the v0.26.0 rule, unchanged: the same
    # function object path (SweepCalibrator.choose_delta)
    # picks the delta, and delta = 0 is the identity.
    import observer_agents as oa
    sym = ss.v4_full_sweep(2026, math.pi / 2)
    choice = oa.SweepCalibrator().choose_delta(sym["rows"])
    assert choice["delta"] == pytest.approx(0.0040)
    rows0 = oa.calibrated_rows(sym["rows"], 0.0)
    assert max(abs(a["mean_D"] - b["mean_D"])
               for a, b in zip(rows0, sym["rows"])) == 0.0


# ---------------------------------------------------------------------------
# Claim (ci): perpendicular stands — PASS
# ---------------------------------------------------------------------------

def test_claim_ci_passes(verdicts):
    claim = verdicts["claim_ci_perpendicular_stands"]
    assert claim["passed"] is True
    assert all(claim["checks"].values())
    expected = {
        42: (-0.7256, 0.2365),
        7: (0.6364, 0.0514),
        1234: (0.3704, 0.1141),
        2026: (0.7481, 0.0561),
    }
    for r in claim["per_seed"]:
        pearson, d_range = expected[r["seed"]]
        assert r["pearson_d_c"] == pytest.approx(pearson, abs=1e-4)
        assert r["d_range"] == pytest.approx(d_range, abs=1e-4)
        assert r["d_range"] < 0.25
        assert r["n_failing"] >= 1
        # The frozen calibrator holds delta = 0 on every
        # perpendicular seed: no delta improves the count.
        assert r["calibrated_delta"] == 0.0
        assert r["calibrated_n_failing"] == r["n_failing"]


# ---------------------------------------------------------------------------
# Claim (cii): two failure kinds — PASS
# ---------------------------------------------------------------------------

def test_claim_cii_passes(verdicts):
    claim = verdicts["claim_cii_two_failure_kinds"]
    assert claim["passed"] is True
    assert all(claim["checks"].values())
    by_key = {(r["seed"], r["direction"]): r
              for r in claim["per_combo"]}
    assert by_key[(2026, "stored")]["pearson_no_sigma1"] \
        == pytest.approx(-0.9433, abs=1e-4)
    expected_perp = {
        42: -0.8091,
        7: -0.4620,
        1234: 0.8013,
        2026: 0.8348,
    }
    for seed, value in expected_perp.items():
        r = by_key[(seed, "perpendicular")]
        assert r["pearson_no_sigma1"] == pytest.approx(
            value, abs=1e-4)
        assert r["pearson_no_sigma1"] > -0.90


# ---------------------------------------------------------------------------
# Controls and rejected candidates (pilot tables, reproducible)
# ---------------------------------------------------------------------------

def test_n_copies_control():
    # The Pearson rescue is variance reduction: plain
    # copies rescue it too. n=10 breaks the opposite
    # D range to 0.2387; n=20 passes (xci) outright.
    r10 = ss.plain_n_copies_sweep(2026, 0.0, 10)
    assert r10["pearson_d_c"] == pytest.approx(-0.9323, abs=1e-4)
    r10_opp = ss.plain_n_copies_sweep(2026, math.pi / 2, 10)
    assert r10_opp["d_range"] == pytest.approx(0.2387, abs=1e-4)
    r20 = ss.plain_n_copies_sweep(2026, 0.0, 20)
    assert r20["pearson_d_c"] == pytest.approx(-0.9289, abs=1e-4)
    r20_opp = ss.plain_n_copies_sweep(2026, math.pi / 2, 20)
    assert r20_opp["d_range"] == pytest.approx(0.3213, abs=1e-4)


def test_mirror_average_candidate_fails():
    # Candidate 3a: symmetrizing the start makes the
    # perpendicular worse, not better, on every seed.
    for thetas, expected in (
            ((math.pi / 4, -math.pi / 4),
             {42: -0.2626, 7: -0.3603, 1234: 0.3290,
              2026: 0.8745}),
            ((math.pi / 4, 3 * math.pi / 4),
             {42: -0.1870, 7: -0.8389, 1234: -0.4526,
              2026: 0.8569})):
        for seed, pearson in expected.items():
            r = ss.mirror_average(seed, thetas)
            assert r["pearson_d_c"] == pytest.approx(
                pearson, abs=1e-4)
            assert r["d_range"] < 0.25


def test_symmetrized_state_candidate_fails():
    # Candidate 3b: the mean-density-matrix start fails
    # on every seed (seed 2026 Pearson +0.9431 /
    # +0.9818); its C range is 0.5000 on every seed.
    for thetas, expected in (
            ((math.pi / 4, -math.pi / 4),
             {42: -0.2924, 7: 0.7103, 1234: 0.7943,
              2026: 0.9431}),
            ((math.pi / 4, 3 * math.pi / 4),
             {42: -0.6459, 7: 0.0174, 1234: 0.5736,
              2026: 0.9818})):
        for seed, pearson in expected.items():
            r = ss.symmetrized_state_sweep(seed, thetas)
            assert r["pearson_d_c"] == pytest.approx(
                pearson, abs=1e-4)
            assert r["c_range"] == pytest.approx(0.5, abs=1e-4)


def test_h_quad_diagnostic_is_anti_predictive():
    # Seed 2026 has the highest H_quad (1.92/2.0) yet
    # holds the stored failure; seed 7 has the lowest
    # (0.97) yet stored passes. Quadrant occupation
    # does not diagnose the Pearson failure.
    d2026 = ss.orbit_diagnostics(2026, 0.0)
    d7 = ss.orbit_diagnostics(7, 0.0)
    assert d2026["H_quad"] == pytest.approx(1.92, abs=0.01)
    assert d7["H_quad"] == pytest.approx(0.97, abs=0.01)
    assert d2026["pearson"] == pytest.approx(-0.8828, abs=1e-4)
    assert d7["pearson"] == pytest.approx(-0.9397, abs=1e-4)
    assert d2026["pearson_no_sigma1"] == pytest.approx(
        -0.9433, abs=1e-4)


# ---------------------------------------------------------------------------
# Whole-claims summary
# ---------------------------------------------------------------------------

def test_symmetry_sweep_claims_summary(verdicts):
    assert verdicts["n_claims"] == 5
    assert verdicts["n_passed"] == 4
    assert verdicts["all_pass"] is False
    assert verdicts["claim_xcviii_orbit_estimator_exactness"][
        "passed"] is False
    assert verdicts["claim_xcix_stored_pearson_rescue"][
        "passed"] is True
    assert verdicts["claim_c_symmetry_calibrated_xci"][
        "passed"] is True
    assert verdicts["claim_ci_perpendicular_stands"][
        "passed"] is True
    assert verdicts["claim_cii_two_failure_kinds"][
        "passed"] is True
