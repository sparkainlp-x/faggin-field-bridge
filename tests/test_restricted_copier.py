# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for the privacy-enforcing copier (v0.23.0,
claims (lxxviii)-(lxxxi))."""

import math

import numpy as np
import pytest

import cloning_ceiling as cc
import restricted_copier as rc
import thought
import unity

BOUND = 5.0 / 6.0


# ---------------------------------------------------------------------------
# The measurement channel
# ---------------------------------------------------------------------------

def test_born_probabilities_uniform():
    psi = thought.uniform_thought()
    p = rc.born_probabilities(psi)
    assert p == pytest.approx(np.full(4, 0.25), abs=1e-12)
    assert float(np.sum(p)) == pytest.approx(1.0, abs=1e-12)


def test_born_probabilities_basis_state():
    psi = np.array([0.0, 0.0, 1.0, 0.0], dtype=complex)
    p = rc.born_probabilities(psi)
    assert p == pytest.approx(np.array([0.0, 0.0, 1.0, 0.0]),
                              abs=1e-12)


def test_reconstruct_from_outcomes_is_sqrt_frequencies():
    # Four shots, one of each outcome: the copy is uniform.
    copy = rc.reconstruct_from_outcomes([0, 1, 2, 3])
    assert copy == pytest.approx(np.full(4, 0.5), abs=1e-12)
    # All shots one outcome: the copy is that basis state.
    copy = rc.reconstruct_from_outcomes([2, 2, 2])
    assert copy == pytest.approx(np.array([0.0, 0.0, 1.0, 0.0]),
                                 abs=1e-12)
    # Two shots on 0, one on 1: sqrt(2/3), sqrt(1/3), 0, 0.
    copy = rc.reconstruct_from_outcomes([0, 0, 1])
    assert copy == pytest.approx(np.array(
        [math.sqrt(2.0 / 3.0), math.sqrt(1.0 / 3.0), 0.0, 0.0]),
        abs=1e-12)


def test_restricted_copy_deterministic():
    psi = np.real(thought.uniform_thought())
    first = rc.restricted_copy(psi, 16, 42, 0)
    second = rc.restricted_copy(psi, 16, 42, 0)
    assert np.array_equal(first, second)
    # A different copy index draws a different measurement.
    third = rc.restricted_copy(psi, 16, 42, 1)
    assert not np.array_equal(first, third)


def test_single_shot_copy_is_a_basis_state():
    psi = np.real(thought.uniform_thought())
    for idx in range(10):
        copy = rc.restricted_copy(psi, 1, 42, idx)
        assert float(np.sum(copy)) == pytest.approx(1.0, abs=1e-12)
        assert int(np.count_nonzero(copy)) == 1


def test_presented_states_match_unrestricted_inputs():
    # The restricted copier is handed exactly the states
    # claim (xlviii) measured as "copies".
    for sigma in (0.0, 0.25, 1.0):
        presented = rc.presented_states(sigma, 42, 5)
        base = np.real(thought.uniform_thought())
        expected = unity.gaussian_copies(base, sigma, 5, 42)
        for got, want in zip(presented, expected):
            assert np.array_equal(got, want)


# ---------------------------------------------------------------------------
# Asymptotic leak (exact, no sampling)
# ---------------------------------------------------------------------------

def test_asymptotic_leak_uniform_is_one():
    psi = np.real(thought.uniform_thought())
    assert rc.asymptotic_leak_fidelity(psi) == pytest.approx(
        1.0, abs=1e-12)


def test_asymptotic_leak_basis_state_is_one():
    psi = np.array([0.0, 0.0, 1.0, 0.0])
    assert rc.asymptotic_leak_fidelity(psi) == pytest.approx(
        1.0, abs=1e-12)


def test_asymptotic_leak_sign_blindness_spot_value():
    # One negative component: (0.25 + 0.25 + 0.25 - 0.25)^2
    # = 0.25. The channel leaks amplitudes, never signs.
    psi = np.array([0.5, 0.5, 0.5, -0.5])
    assert rc.asymptotic_leak_fidelity(psi) == pytest.approx(
        0.25, abs=1e-12)


def test_asymptotic_leak_sweep_low_sigma_is_one():
    # At sigma <= 0.25 every presented component stays
    # positive on the calibration seeds, so |psi| = psi
    # and the infinite-budget reconstruction is exact.
    for seed in (42, 7):
        for sigma in (0.0, 0.01, 0.05, 0.10, 0.25):
            row = rc.asymptotic_leak_sweep(sigma, seed)
            assert row["mean_fidelity"] == pytest.approx(
                1.0, abs=1e-12)


# ---------------------------------------------------------------------------
# (lxxviii) Single-shot copier
# ---------------------------------------------------------------------------

def test_single_shot_sigma_zero_is_exactly_one_quarter():
    # The uniform thought: whichever outcome is drawn,
    # its probability is 1/4, so every fidelity is 0.25.
    for seed in (42, 7, 1234, 2026):
        row = rc.single_shot_fidelity(0.0, seed)
        assert row["mean_fidelity"] == pytest.approx(
            0.25, abs=1e-12)
        assert all(f == pytest.approx(0.25, abs=1e-12)
                   for f in row["fidelities"])


def test_single_shot_sweep_calibration_values():
    by_seed = {42: [0.2500, 0.2542, 0.2658, 0.2665, 0.2829,
                    0.3998, 0.3470],
               7: [0.2500, 0.2548, 0.2748, 0.3024, 0.4859,
                   0.4793, 0.5798]}
    for seed, expected in by_seed.items():
        got = [r["mean_fidelity"]
               for r in rc.single_shot_sweep(seed)]
        assert got == pytest.approx(expected, abs=1e-4)


def test_claim_lxxviii_verdict_pass():
    verdict = rc.claim_single_shot_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"]["single_shot_respects_bound"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    # Calibration seeds (frozen in the preregistration).
    assert by_seed[42]["max_mean_fidelity"] == pytest.approx(
        0.3998, abs=1e-4)
    assert by_seed[7]["max_mean_fidelity"] == pytest.approx(
        0.5798, abs=1e-4)
    # Held-out seeds (measured by the evaluation run).
    assert by_seed[1234]["max_mean_fidelity"] == pytest.approx(
        0.6243, abs=1e-4)
    assert by_seed[2026]["max_mean_fidelity"] == pytest.approx(
        0.4093, abs=1e-4)
    for r in verdict["per_seed"]:
        assert r["max_mean_fidelity"] <= BOUND


# ---------------------------------------------------------------------------
# (lxxix) 16-shot leak at sigma = 0
# ---------------------------------------------------------------------------

def test_m_shot_sigma_zero_budget_monotone():
    # More shots leak more: the mean fidelity rises with
    # M on both calibration seeds at sigma = 0.
    for seed in (42, 7):
        rows = rc.budget_sweep(0.0, seed)
        means = [r["mean_fidelity"] for r in rows]
        assert means == sorted(means)
        assert means[0] == pytest.approx(0.25, abs=1e-12)


def test_claim_lxxix_verdict_pass():
    verdict = rc.claim_m_shot_leak_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"][
        "m_shot_exceeds_bound_at_sigma_0"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    # Calibration seeds (frozen in the preregistration).
    assert by_seed[42]["mean_fidelity"] == pytest.approx(
        0.9526, abs=1e-4)
    assert by_seed[7]["mean_fidelity"] == pytest.approx(
        0.9396, abs=1e-4)
    # Held-out seeds (measured by the evaluation run).
    assert by_seed[1234]["mean_fidelity"] == pytest.approx(
        0.9375, abs=1e-4)
    assert by_seed[2026]["mean_fidelity"] == pytest.approx(
        0.9205, abs=1e-4)
    for r in verdict["per_seed"]:
        assert r["mean_fidelity"] > BOUND


# ---------------------------------------------------------------------------
# (lxxx) Budget gap at sigma = 0
# ---------------------------------------------------------------------------

def test_claim_lxxx_verdict_pass():
    verdict = rc.claim_budget_gap_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"]["budget_gap_at_least_0.30"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    # Calibration seeds (frozen in the preregistration).
    assert by_seed[42]["gap_m64_minus_m1"] == pytest.approx(
        0.7378, abs=1e-4)
    assert by_seed[7]["gap_m64_minus_m1"] == pytest.approx(
        0.7382, abs=1e-4)
    # Held-out seeds (measured by the evaluation run).
    assert by_seed[1234]["gap_m64_minus_m1"] == pytest.approx(
        0.7403, abs=1e-4)
    assert by_seed[2026]["gap_m64_minus_m1"] == pytest.approx(
        0.7365, abs=1e-4)
    for r in verdict["per_seed"]:
        assert r["gap_m64_minus_m1"] >= 0.30


# ---------------------------------------------------------------------------
# (lxxxi) The 16-shot leak is sigma-dependent
# ---------------------------------------------------------------------------

def test_claim_lxxxi_verdict_pass():
    verdict = rc.claim_sigma_dependence_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"][
        "leak_exceeds_bound_at_sigma_0.25"] is True
    assert verdict["checks"][
        "leak_below_bound_at_sigma_1.00"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    # Calibration seeds (frozen in the preregistration).
    assert by_seed[42]["mean_fidelity_sigma_0.25"] == pytest.approx(
        0.9333, abs=1e-4)
    assert by_seed[42]["mean_fidelity_sigma_1.00"] == pytest.approx(
        0.8079, abs=1e-4)
    assert by_seed[7]["mean_fidelity_sigma_0.25"] == pytest.approx(
        0.9365, abs=1e-4)
    assert by_seed[7]["mean_fidelity_sigma_1.00"] == pytest.approx(
        0.6331, abs=1e-4)
    # Held-out seeds (measured by the evaluation run).
    assert by_seed[1234]["mean_fidelity_sigma_0.25"] == pytest.approx(
        0.9225, abs=1e-4)
    assert by_seed[1234]["mean_fidelity_sigma_1.00"] == pytest.approx(
        0.6279, abs=1e-4)
    assert by_seed[2026]["mean_fidelity_sigma_0.25"] == pytest.approx(
        0.9245, abs=1e-4)
    assert by_seed[2026]["mean_fidelity_sigma_1.00"] == pytest.approx(
        0.7855, abs=1e-4)


# ---------------------------------------------------------------------------
# Reported, not claimed: restricted vs unrestricted
# ---------------------------------------------------------------------------

def test_restricted_vs_unrestricted_reported_shape():
    # The reported table has one row per sigma, on
    # identical presented states, with the restricted
    # copier far below the unrestricted copier at low
    # sigma and converging at high sigma. The targets
    # differ by construction (see the preregistration),
    # so this table is reported, not claimed.
    for seed in (42, 7):
        rows = rc.restricted_vs_unrestricted(seed)
        assert [r["sigma"] for r in rows] == list(rc.SIGMA_GRID)
        assert rows[0]["restricted_single_shot_mean"] == pytest.approx(
            0.25, abs=1e-12)
        assert rows[0]["unrestricted_mean"] == pytest.approx(
            1.0, abs=1e-12)
        assert rows[0]["difference"] == pytest.approx(
            -0.75, abs=1e-12)
        # At sigma = 1.00 the two copiers converge.
        assert abs(rows[-1]["difference"]) <= 0.20


def test_restricted_copier_claims_aggregate():
    verdicts = rc.restricted_copier_claims()
    assert verdicts["n_claims"] == 4
    # Measured by the evaluation run: 4/4 pass.
    assert verdicts["n_passed"] == 4
    assert verdicts["all_pass"] is True
