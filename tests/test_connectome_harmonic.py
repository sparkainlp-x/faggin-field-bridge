# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for connectome-harmonic structure-function coupling
(v0.17.0, claims (liv)-(lvi))."""

import numpy as np
import pytest

import connectome_harmonic as ch
import empathy_field as ef


# ---------------------------------------------------------------------------
# Graph and Laplacian
# ---------------------------------------------------------------------------

def test_coupling_matrix_is_resonance_off_diagonal():
    states = ef.resonance_population(0.25, 8, 42)
    w = ch.coupling_matrix(states)
    assert w.shape == (8, 8)
    assert np.all(np.diag(w) == 0.0)
    assert np.all(w >= 0.0)
    assert np.all(w <= 1.0)
    assert np.max(np.abs(w - w.T)) == pytest.approx(0.0, abs=1e-12)
    # Off-diagonal entries are the pairwise resonance R_ij.
    assert w[0, 1] == pytest.approx(
        ef.overlap_squared(states[0], states[1]), abs=1e-12)


def test_coupling_matrix_needs_two_agents():
    with pytest.raises(ValueError):
        ch.coupling_matrix([np.array([1.0, 0.0, 0.0, 0.0])])


def test_laplacian_is_degree_minus_coupling():
    states = ef.resonance_population(0.25, 8, 42)
    w = ch.coupling_matrix(states)
    lap = ch.graph_laplacian(w)
    assert np.allclose(np.diag(lap), np.sum(w, axis=1))
    assert np.allclose(lap + w, np.diag(np.sum(w, axis=1)))
    # Row sums are zero.
    assert np.max(np.abs(np.sum(lap, axis=1))) <= 1e-12


def test_laplacian_rejects_negative_weights():
    with pytest.raises(ValueError):
        ch.graph_laplacian(np.array([[-1.0, 1.0], [1.0, -1.0]]))
    with pytest.raises(ValueError):
        ch.graph_laplacian(np.array([[1.0, 2.0, 3.0]]))


def test_harmonic_modes_sorted_eigenvalues():
    states = ef.resonance_population(0.25, 8, 42)
    h = ch.harmonic_modes(ch.coupling_matrix(states))
    values = h["eigenvalues"]
    assert values[0] == pytest.approx(0.0, abs=1e-12)
    assert np.all(np.diff(values) >= 0.0)
    assert np.all(values >= -1e-12)
    # Orthonormal modes.
    assert np.max(np.abs(h["modes"].T @ h["modes"]
                         - np.eye(8))) <= 1e-12


def test_functional_connectivity_is_bhattacharyya():
    states = ef.resonance_population(0.25, 8, 42)
    f = ch.functional_connectivity(states)
    assert f.shape == (8, 8)
    assert np.all(np.diag(f) == 0.0)
    assert np.all(f >= 0.0)
    assert np.all(f <= 1.0)
    # F differs from W: sign-blind Born overlap vs
    # sign-sensitive amplitude overlap.
    w = ch.coupling_matrix(states)
    assert not np.allclose(f, w)
    assert np.max(np.abs(f - w)) > 0.05


# ---------------------------------------------------------------------------
# kappa vs noise (measured values)
# ---------------------------------------------------------------------------

def test_kappa_calibration_seeds():
    for seed, expected in (
            (42, [1.0000, 0.9989, 0.3997, 0.8069]),
            (7, [1.0000, 0.8422, 0.4119, 0.6392])):
        rows = ch.coupling_vs_noise(seed)
        assert [r["kappa"] for r in rows] == pytest.approx(
            expected, abs=1e-3)


def test_kappa_held_out_seeds_fall_monotonically():
    # On the held-out seeds kappa falls monotonically with
    # sigma after the near-parallel plateau: no dip-and-
    # recovery, the reverse of the Luppi direction.
    for seed, expected in (
            (1234, [0.9999, 0.9864, 0.5636, 0.3756]),
            (2026, [1.0000, 0.9984, 0.7957, 0.2285])):
        rows = ch.coupling_vs_noise(seed)
        assert [r["kappa"] for r in rows] == pytest.approx(
            expected, abs=1e-3)
        kappas = [r["kappa"] for r in rows]
        assert all(kappas[i + 1] < kappas[i]
                   for i in range(len(kappas) - 1))


def test_kappa_at_sigma_010_is_near_parallel_artefact():
    # kappa ~= 1 at sigma = 0.10 on every seed: both W and F
    # are ~= 1 with the same noise driving both deviations.
    # Reported, not gated.
    for seed in (42, 7, 1234, 2026):
        rows = ch.coupling_vs_noise(seed)
        assert rows[0]["kappa"] == pytest.approx(1.0, abs=1e-3)


def test_rho_d_calibration_seeds():
    for seed, expected in (
            (42, [1.0058, 1.0189, 0.8714, 1.1250]),
            (7, [0.9857, 0.8709, 0.8308, 0.9621])):
        rows = ch.coupling_vs_noise(seed)
        assert [r["rho_d"] for r in rows] == pytest.approx(
            expected, abs=1e-3)


def test_rho_d_held_out_seeds_align_at_high_sigma():
    # On the held-out seeds the D signal is strongly
    # structure-aligned (rho << 1, smooth on the graph)
    # at high sigma: seed 1234 rho = 0.4662 at sigma =
    # 0.50, seed 2026 rho = 0.5995 at sigma = 1.00.
    rows = ch.coupling_vs_noise(1234)
    assert [r["rho_d"] for r in rows] == pytest.approx(
        [0.9812, 0.8265, 0.4662, 0.9715], abs=1e-3)
    rows = ch.coupling_vs_noise(2026)
    assert [r["rho_d"] for r in rows] == pytest.approx(
        [0.9798, 0.8869, 0.7341, 0.5995], abs=1e-3)


def test_low2_share_is_seed_unstable():
    # The degeneracy artefact: the low-2-mode energy share
    # of the D signal at sigma = 0.10 is 0.1036 on seed 42
    # and 0.8012 on seed 7. Reported, not gated.
    rows42 = ch.coupling_vs_noise(42)
    rows7 = ch.coupling_vs_noise(7)
    assert rows42[0]["low2_energy_share_d"] == pytest.approx(
        0.1036, abs=1e-3)
    assert rows7[0]["low2_energy_share_d"] == pytest.approx(
        0.8012, abs=1e-3)


def test_field_row_seed_42_sigma_025():
    row = ch.field_row(0.25, seed=42)
    assert row["kappa"] == pytest.approx(0.9989, abs=1e-3)
    assert row["rho_d"] == pytest.approx(1.0189, abs=1e-3)
    assert row["f_mean_pair_concurrence"] == pytest.approx(
        0.1803, abs=1e-3)
    assert row["mean_r"] == pytest.approx(0.8520, abs=1e-3)


def test_rayleigh_quotient_rejects_constant_signal():
    states = ef.resonance_population(0.25, 8, 42)
    with pytest.raises(ValueError):
        ch.rayleigh_quotient_ratio(states, [0.5] * 8)
    with pytest.raises(ValueError):
        ch.rayleigh_quotient_ratio(states, [0.5] * 7)


# ---------------------------------------------------------------------------
# Shuffle null (decoupling control)
# ---------------------------------------------------------------------------

def test_shuffle_null_near_zero_every_seed():
    for seed, expected_mean in (
            (42, -0.0145), (7, -0.0305),
            (1234, -0.0047), (2026, -0.0037)):
        null = ch.shuffle_null_row(0.25, seed=seed)
        assert null["shuffle_mean"] == pytest.approx(
            expected_mean, abs=1e-3)
        assert abs(null["shuffle_mean"]) <= 0.10
        # The shuffle leaves f unchanged by construction.
        assert null["f_mean_pair_concurrence"] == pytest.approx(
            ch.field_row(0.25, seed=seed)["f_mean_pair_concurrence"],
            abs=1e-12)


def test_shuffle_null_deterministic():
    states = ef.resonance_population(0.25, 8, 42)
    first = ch.shuffle_null(states, 42)
    second = ch.shuffle_null(states, 42)
    assert first["mean"] == second["mean"]
    assert first["values"] == second["values"]


# ---------------------------------------------------------------------------
# (liv) Machinery
# ---------------------------------------------------------------------------

def test_claim_liv_verdict_fail_on_rho_only():
    verdict = ch.claim_machinery_verdict()
    assert verdict["passed"] is False
    # All five Laplacian identity sub-checks pass on every seed.
    assert verdict["checks"]["laplacian_symmetric"] is True
    assert verdict["checks"]["laplacian_psd"] is True
    assert verdict["checks"]["lambda_0_near_zero"] is True
    assert verdict["checks"]["eigenvalues_sorted"] is True
    assert verdict["checks"]["eigenvectors_orthonormal"] is True
    # Only the rho half fails, on the held-out seeds only.
    assert verdict["checks"]["rho_d_within_bar"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["rho_deviation_max"] == pytest.approx(
        0.1286, abs=1e-3)
    assert by_seed[7]["rho_deviation_max"] == pytest.approx(
        0.1692, abs=1e-3)
    assert by_seed[1234]["rho_deviation_max"] == pytest.approx(
        0.5338, abs=1e-3)
    assert by_seed[2026]["rho_deviation_max"] == pytest.approx(
        0.4005, abs=1e-3)


# ---------------------------------------------------------------------------
# (lv) Luppi prediction as stated
# ---------------------------------------------------------------------------

def test_claim_lv_verdict_fail_every_seed():
    verdict = ch.claim_luppi_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["kappa_rises_to_break"] is False
    assert verdict["checks"]["kappa_rises_to_far"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["rise_to_break"] == pytest.approx(
        -0.5992, abs=1e-3)
    assert by_seed[7]["rise_to_break"] == pytest.approx(
        -0.4303, abs=1e-3)
    assert by_seed[1234]["rise_to_break"] == pytest.approx(
        -0.4228, abs=1e-3)
    assert by_seed[2026]["rise_to_break"] == pytest.approx(
        -0.2027, abs=1e-3)
    assert by_seed[42]["rise_to_far"] == pytest.approx(
        -0.1920, abs=1e-3)
    assert by_seed[7]["rise_to_far"] == pytest.approx(
        -0.2030, abs=1e-3)
    assert by_seed[1234]["rise_to_far"] == pytest.approx(
        -0.6108, abs=1e-3)
    assert by_seed[2026]["rise_to_far"] == pytest.approx(
        -0.7699, abs=1e-3)


# ---------------------------------------------------------------------------
# (lvi) Measured shape
# ---------------------------------------------------------------------------

def test_claim_lvi_verdict_fail():
    verdict = ch.claim_shape_verdict()
    assert verdict["passed"] is False
    # The attuned, shuffle-null, and separation sub-checks pass.
    assert verdict["checks"]["kappa_attuned_at_least_min"] is True
    assert verdict["checks"]["shuffle_null_near_zero"] is True
    assert verdict["checks"][
        "shuffle_separated_from_attuned"] is True
    # The dip fails on seed 2026 only; the recovery fails on
    # both held-out seeds.
    assert verdict["checks"]["kappa_dips_at_break"] is False
    assert verdict["checks"]["kappa_recovers_past_break"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["dip_to_break"] == pytest.approx(
        0.5992, abs=1e-3)
    assert by_seed[7]["dip_to_break"] == pytest.approx(
        0.4303, abs=1e-3)
    assert by_seed[1234]["dip_to_break"] == pytest.approx(
        0.4228, abs=1e-3)
    assert by_seed[2026]["dip_to_break"] == pytest.approx(
        0.2027, abs=1e-3)
    assert by_seed[42]["recovery_to_far"] == pytest.approx(
        0.4073, abs=1e-3)
    assert by_seed[7]["recovery_to_far"] == pytest.approx(
        0.2273, abs=1e-3)
    assert by_seed[1234]["recovery_to_far"] == pytest.approx(
        -0.1880, abs=1e-3)
    assert by_seed[2026]["recovery_to_far"] == pytest.approx(
        -0.5672, abs=1e-3)
    assert by_seed[42]["shuffle_separation"] == pytest.approx(
        0.9844, abs=1e-3)
    assert by_seed[7]["shuffle_separation"] == pytest.approx(
        0.8117, abs=1e-3)


# ---------------------------------------------------------------------------
# Aggregate, thresholds, main
# ---------------------------------------------------------------------------

def test_connectome_harmonic_claims_aggregate():
    verdicts = ch.connectome_harmonic_claims()
    assert verdicts["n_claims"] == 3
    assert verdicts["n_passed"] == 0
    assert verdicts["all_pass"] is False
    assert verdicts["headline_allowed"] is False


def test_thresholds_set():
    thresholds = ch._thresholds()
    assert thresholds["sigma_grid"] == (0.10, 0.25, 0.50, 1.00)
    assert thresholds["n_agents"] == 8
    assert thresholds["exact_tol"] == pytest.approx(1e-12)
    assert thresholds["rho_deviation_max"] == pytest.approx(0.20)
    assert thresholds["kappa_rise_min"] == pytest.approx(0.10)
    assert thresholds["kappa_attuned_min"] == pytest.approx(0.80)
    assert thresholds["kappa_dip_min"] == pytest.approx(0.30)
    assert thresholds["kappa_recovery_min"] == pytest.approx(0.10)
    assert thresholds["shuffle_mean_max"] == pytest.approx(0.10)
    assert thresholds["shuffle_separation_min"] == pytest.approx(0.50)
    assert thresholds["n_shuffles"] == 50


def test_main_runs(capsys):
    ch.main()
    out = capsys.readouterr().out
    assert "0/3 claims passed" in out
    assert "claim (liv) verdict: FAIL" in out
    assert "claim (lv) verdict: FAIL" in out
    assert "claim (lvi) verdict: FAIL" in out
