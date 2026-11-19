# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for kuramoto.py: the Kuramoto bounded-coherence scan (v0.13.0)."""

import math

import numpy as np
import pytest

import kuramoto as ku


def test_kuramoto_run_order_parameter_rises_with_k():
    # The Kuramoto transition works: R_K rises from the
    # finite-size floor (~0.29 at K = 0, N = 8) to near 1.
    r0 = ku.kuramoto_run(0.0, 0.0, seed=42)
    r8 = ku.kuramoto_run(8.0, 0.0, seed=42)
    assert r0["rk_steady"] == pytest.approx(0.2871, abs=1e-4)
    assert r8["rk_steady"] == pytest.approx(0.9925, abs=1e-4)
    assert 0.0 <= r0["rk_steady"] <= 1.0
    assert 0.0 <= r8["rk_steady"] <= 1.0
    assert len(r0["theta_final"]) == ku.N_AGENTS
    assert len(r0["rk_series"]) == ku.N_STEPS


def test_slide_angles_are_relative_and_bounded():
    # Angles live on [0, pi/2): the relative phase divided by 4.
    # Fully synced phases all map to angle 0 (the uniform thought).
    synced = np.zeros(ku.N_AGENTS)
    angles = ku.slide_angles(synced)
    assert np.allclose(angles, 0.0)
    run = ku.kuramoto_run(0.0, 0.0, seed=42)
    angles = ku.slide_angles(run["theta_final"])
    assert np.all(angles >= 0.0)
    assert np.all(angles < math.pi / 2)
    # Each slide state is normalized with D = cos^2(angle).
    for a in angles:
        psi = ku.oc.slide_state(float(a))
        assert float(np.linalg.norm(psi)) == pytest.approx(1.0, abs=1e-9)
        assert ku.oc.sk.self_knowing_factor(psi) == pytest.approx(
            math.cos(float(a)) ** 2, abs=1e-9)


def test_kuramoto_point_seed_42_k0():
    p = ku.kuramoto_point(0.0, 0.0, seed=42)
    assert p["rk"] == pytest.approx(0.2871, abs=1e-4)
    assert p["n_qualia"] == 8
    assert p["h_joint_bits"] == pytest.approx(12.440, abs=1e-3)
    assert p["gap_bits"] == pytest.approx(12.223, abs=1e-3)
    # The single-shot collapse leaves the isolated arm at
    # exactly zero joint entropy: A = H_collaborating.
    assert p["h_isolated_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["gap_bits"] == pytest.approx(
        p["h_collaborating_bits"], abs=1e-9)


def test_count_floor_at_high_k():
    # At high K the count falls to a floor of 6 on every seed
    # — it does not fall to zero, and it does not rise again.
    for seed in ku.ALL_SEEDS:
        p = ku.kuramoto_point(8.0, 0.0, seed=seed)
        assert p["n_qualia"] == 6
        assert p["rk"] >= 0.98


def test_claim_xxxvi_verdict_is_fail():
    verdict = ku.claim_count_inverted_u_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["peak_interior"] is False
    assert verdict["checks"]["peak_above_k0"] is False
    assert verdict["checks"]["peak_above_kmax"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["k_peak"] == pytest.approx(0.5, abs=1e-9)
    assert by_seed[42]["count_peak"] == 13
    assert by_seed[7]["k_peak"] == pytest.approx(0.0, abs=1e-9)
    assert by_seed[7]["count_peak"] == 18
    assert by_seed[1234]["k_peak"] == pytest.approx(0.0, abs=1e-9)
    assert by_seed[1234]["count_peak"] == 10
    assert by_seed[2026]["k_peak"] == pytest.approx(0.5, abs=1e-9)
    assert by_seed[2026]["count_peak"] == 11


def test_claim_xxxvii_verdict_is_fail():
    verdict = ku.claim_h_inverted_u_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["peak_interior"] is False
    assert verdict["checks"]["peak_above_k0"] is False
    assert verdict["checks"]["peak_above_kmax"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["k_peak"] == pytest.approx(0.0, abs=1e-9)
    assert by_seed[42]["h_peak"] == pytest.approx(12.440, abs=1e-3)
    assert by_seed[7]["k_peak"] == pytest.approx(1.6, abs=1e-9)
    assert by_seed[7]["h_peak"] == pytest.approx(12.154, abs=1e-3)
    assert by_seed[1234]["k_peak"] == pytest.approx(0.5, abs=1e-9)
    assert by_seed[1234]["h_peak"] == pytest.approx(13.077, abs=1e-3)
    assert by_seed[2026]["k_peak"] == pytest.approx(0.0, abs=1e-9)
    assert by_seed[2026]["h_peak"] == pytest.approx(13.003, abs=1e-3)


def test_claim_xxxviii_verdict_is_fail():
    # R_K at the count peak is 0.31-0.36 on every seed — far
    # below the Phillips band [0.5, 0.8] and below f* = 0.7278.
    # The count optimum sits at LOW coherence, not bounded
    # coherence.
    verdict = ku.claim_rk_band_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["rk_in_band"] is False
    assert verdict["f_star"] == pytest.approx(0.7278, abs=1e-4)
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["rk_at_peak"] == pytest.approx(0.3112, abs=1e-4)
    assert by_seed[7]["rk_at_peak"] == pytest.approx(0.3471, abs=1e-4)
    assert by_seed[1234]["rk_at_peak"] == pytest.approx(0.3569, abs=1e-4)
    assert by_seed[2026]["rk_at_peak"] == pytest.approx(0.3571, abs=1e-4)
    for r in verdict["per_seed"]:
        assert r["rk_at_peak"] < 0.5


def test_claim_xxxix_verdict_is_fail():
    # The margin check passes on all four seeds (peak exceeds
    # sigma = 0 by >= 3), but the peak is not strictly
    # interior: seed 42 peaks at sigma = 1.0, the grid edge.
    # sigma* is not stable across seeds (1.0, 0.10, 0.25, 0.05).
    verdict = ku.claim_sigma_resonance_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["peak_interior"] is False
    assert verdict["checks"]["peak_above_sigma0"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["sigma_peak"] == pytest.approx(1.0, abs=1e-9)
    assert by_seed[42]["count_peak"] == 18
    assert by_seed[7]["sigma_peak"] == pytest.approx(0.10, abs=1e-9)
    assert by_seed[7]["count_peak"] == 17
    assert by_seed[1234]["sigma_peak"] == pytest.approx(0.25, abs=1e-9)
    assert by_seed[1234]["count_peak"] == 19
    assert by_seed[2026]["sigma_peak"] == pytest.approx(0.05, abs=1e-9)
    assert by_seed[2026]["count_peak"] == 15


def test_kuramoto_aggregate():
    claims = ku.kuramoto_claims()
    assert claims["n_claims"] == 4
    assert claims["n_passed"] == 0
    assert claims["all_pass"] is False
    assert claims["headline_allowed"] is False
    assert claims["claim_xxxvi_count_inverted_u"]["passed"] is False
    assert claims["claim_xxxvii_h_inverted_u"]["passed"] is False
    assert claims["claim_xxxviii_rk_band"]["passed"] is False
    assert claims["claim_xxxix_sigma_resonance"]["passed"] is False


def test_thresholds_frozen():
    t = ku._thresholds()
    assert t["count_peak_margin_min"] == 3
    assert t["h_peak_margin_min"] == 0.5
    assert t["rk_band_lo"] == 0.5
    assert t["rk_band_hi"] == 0.8
    assert t["fixed_k_xxxix"] == 1.0
    assert t["count_sigma_margin_min"] == 3
