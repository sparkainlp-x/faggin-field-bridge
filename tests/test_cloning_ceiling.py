# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for the no-cloning / Holevo ceiling (v0.15.0,
claims (xliv)-(xlviii))."""

import math

import numpy as np
import pytest

import cloning_ceiling as cc
import empathy_field as ef
import observer_cycle as oc
import self_knowing as sk
import thought_entanglement as te


# ---------------------------------------------------------------------------
# (xliv) Local purity
# ---------------------------------------------------------------------------

def test_local_purity_known_values():
    bell = te.density_matrix(te.bell_state("phi_plus"))
    assert cc.local_purity(bell) == pytest.approx(0.5, abs=1e-12)
    product = te.density_matrix(
        np.array([1.0, 0.0, 0.0, 0.0], dtype=complex))
    assert cc.local_purity(product) == pytest.approx(1.0, abs=1e-12)
    mixed = np.eye(4, dtype=complex) / 4.0
    assert cc.local_purity(mixed) == pytest.approx(0.5, abs=1e-12)


def test_purity_identity_branch_and_slide():
    for a in oc.BELL_BRANCH_GRID:
        assert cc.purity_identity_error(
            oc.generalized_bell(a)) <= 1e-9
    for t in oc.SLIDE_THETAS:
        assert cc.purity_identity_error(oc.slide_state(t)) <= 1e-9
    # Spot values: the coefficient is 1 - C^2/2 exactly.
    psi = oc.generalized_bell(1.0 / math.sqrt(2.0))
    assert te.concurrence_pure(psi) == pytest.approx(1.0, abs=1e-12)
    assert cc.local_purity(te.density_matrix(psi)) == pytest.approx(
        0.5, abs=1e-12)


def test_purity_identity_haar_random():
    for z in cc.haar_pure_states(50, seed=7):
        assert cc.purity_identity_error(z) <= 1e-9


def test_purity_sweep_worst_errors():
    sweep = cc.purity_sweep()
    assert sweep["worst_identity_error"] == pytest.approx(
        8.88e-16, abs=1e-15)
    # Wootters-vs-pure worst is a max over 200+ states of an
    # eigenvalue difference, so it is platform-sensitive at
    # the ~15% level (calibration pilot 1.94e-08; measured
    # 1.85e-08 on CPython 3.12 / NumPy 2.5.5 and 2.12e-08
    # on CPython 3.11 / NumPy 2.5.5, different argmax Haar
    # states, same order of magnitude). The pin below is a
    # sanity band around the pilot value, NOT a claim
    # threshold: the frozen (xliv) bar is WOOTTERS_TOL =
    # 1e-7 and is unchanged — both platforms pass it with
    # ~5x margin.
    assert sweep["worst_wootters_vs_pure"] == pytest.approx(
        1.94e-08, abs=5e-09)


def test_claim_xliv_verdict_pass():
    verdict = cc.claim_local_purity_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"]["identity_exact"] is True
    assert verdict["checks"]["wootters_agrees_with_pure"] is True
    assert verdict["worst_identity_error"] <= 1e-9
    assert verdict["worst_wootters_vs_pure"] <= 1e-7


# ---------------------------------------------------------------------------
# (xlv)-(xlvi) Thought-pair ensemble
# ---------------------------------------------------------------------------

def test_pair_chi_matches_analytic_form():
    for sigma in te.SIGMA_GRID:
        for row in cc.pair_ensemble_rows(sigma, 42):
            states = ef.resonance_population(sigma, 8, 42)
            psi_i, psi_j = states[row["i"]], states[row["j"]]
            assert row["holevo_chi_bits"] == pytest.approx(
                cc.pair_holevo_chi_analytic(psi_i, psi_j), abs=1e-12)


def test_pair_chi_endpoints():
    uniform = np.array([0.5, 0.5, 0.5, 0.5], dtype=complex)
    assert cc.pair_holevo_chi(uniform, uniform) == pytest.approx(
        0.0, abs=1e-12)
    assert cc.pair_accessible_information(uniform, uniform) == \
        pytest.approx(0.0, abs=1e-12)
    ket00 = np.array([1.0, 0.0, 0.0, 0.0], dtype=complex)
    ket11 = np.array([0.0, 0.0, 0.0, 1.0], dtype=complex)
    assert cc.pair_holevo_chi(ket00, ket11) == pytest.approx(
        1.0, abs=1e-12)
    # Orthogonal basis states are perfectly distinguished
    # by the Born collapse: I = chi = 1 bit here.
    assert cc.pair_accessible_information(ket00, ket11) == \
        pytest.approx(1.0, abs=1e-12)
    # D_pair of (|00>, |11>) is (1 + 1/3) / 2 = 2/3.
    assert 0.5 * (sk.self_knowing_factor(ket00)
                  + sk.self_knowing_factor(ket11)) == pytest.approx(
                      2.0 / 3.0, abs=1e-12)


def test_accessible_information_never_exceeds_chi():
    for seed in (42, 7):
        for sigma in te.SIGMA_GRID:
            for row in cc.pair_ensemble_rows(sigma, seed):
                assert row["accessible_minus_chi_bits"] <= 1e-9


def test_ensemble_sweep_seed_42_sigma_025():
    rows = cc.ensemble_sweep(42)
    row = next(r for r in rows if r["sigma"] == 0.25)
    assert row["f_mean_pair_concurrence"] == pytest.approx(
        0.1803, abs=1e-3)
    assert row["mean_d"] == pytest.approx(0.9059, abs=1e-3)
    assert row["mean_chi_bits"] == pytest.approx(0.2219, abs=1e-3)
    assert row["mean_gap_bits"] == pytest.approx(-0.6840, abs=1e-3)
    assert row["min_gap_bits"] == pytest.approx(-0.8863, abs=1e-3)
    assert row["n_pairs"] == 28


def test_claim_xlv_verdict_fail():
    verdict = cc.claim_holevo_ceiling_verdict()
    assert verdict["passed"] is False
    # The ceiling as stated fails on every seed ...
    assert verdict["checks"]["d_at_most_chi_every_pair"] is False
    # ... while the gap magnitude DOES shrink with f.
    assert verdict["checks"]["abs_gap_shrinks_with_f"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    for seed in (42, 7, 1234, 2026):
        assert by_seed[seed]["min_gap_bits"] == pytest.approx(
            -1.0, abs=1e-9)
    assert by_seed[42]["spearman_abs_gap_f"] == pytest.approx(
        -1.0, abs=1e-9)
    for seed in (7, 1234, 2026):
        assert by_seed[seed]["spearman_abs_gap_f"] == pytest.approx(
            -0.9643, abs=1e-4)
    # The gap rises with f (Pearson > 0.98 on every seed):
    # D approaches chi from ABOVE, not below.
    for seed in (42, 7, 1234, 2026):
        assert by_seed[seed]["pearson_gap_f"] >= 0.98


def test_claim_xlvi_verdict_pass():
    verdict = cc.claim_accessible_information_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"]["accessible_at_most_chi_every_pair"] \
        is True
    for r in verdict["per_seed"]:
        assert r["max_accessible_minus_chi_bits"] == pytest.approx(
            -3.20e-16, abs=1e-12)


# ---------------------------------------------------------------------------
# (xlvii) Unitary cloners
# ---------------------------------------------------------------------------

def test_bh_images_orthonormal():
    img0, img1 = cc.bh_basis_images()
    assert np.linalg.norm(img0) == pytest.approx(1.0, abs=1e-12)
    assert np.linalg.norm(img1) == pytest.approx(1.0, abs=1e-12)
    assert abs(np.vdot(img0, img1)) <= 1e-12


def test_bh_unitary_is_unitary():
    u = cc.bh_unitary()
    assert np.max(np.abs(u.conj().T @ u - np.eye(8))) <= 1e-12
    # Columns 0 and 4 are the basis images.
    img0, img1 = cc.bh_basis_images()
    assert np.max(np.abs(u[:, 0] - img0)) <= 1e-12
    assert np.max(np.abs(u[:, 4] - img1)) <= 1e-12


def test_bh_clone_reduced_state_form():
    # For |0>: each clone is diag(5/6, 1/6).
    psi = np.array([1.0, 0.0], dtype=complex)
    out = cc.bh_clone(psi)
    assert np.linalg.norm(out) == pytest.approx(1.0, abs=1e-12)
    for keep in (0, 1):
        rho = cc._clone_reduced_state(out, keep)
        assert rho[0, 0] == pytest.approx(5.0 / 6.0, abs=1e-12)
        assert rho[1, 1] == pytest.approx(1.0 / 6.0, abs=1e-12)
        assert abs(rho[0, 1]) <= 1e-12
    # For |+>: the clone is (5/6)|+><+| + (1/6)|-><-|.
    psi = np.array([1.0, 1.0], dtype=complex) / math.sqrt(2.0)
    out = cc.bh_clone(psi)
    rho = cc._clone_reduced_state(out, 0)
    expected = (5.0 / 6.0) * np.outer(psi, psi.conj()) \
        + (1.0 / 6.0) * np.outer(
            np.array([1.0, -1.0], dtype=complex) / math.sqrt(2.0),
            np.array([1.0, -1.0], dtype=complex).conj()
            / math.sqrt(2.0))
    assert np.max(np.abs(rho - expected)) <= 1e-12


def test_bh_fidelity_exactly_5_6():
    sweep = cc.cloning_sweep()
    assert sweep["bh_grid_min"] == pytest.approx(
        5.0 / 6.0, abs=1e-9)
    assert sweep["bh_grid_max"] == pytest.approx(
        5.0 / 6.0, abs=1e-9)
    assert sweep["bh_grid_mean"] == pytest.approx(
        5.0 / 6.0, abs=1e-9)
    assert sweep["bh_pauli_min"] == pytest.approx(
        5.0 / 6.0, abs=1e-9)
    assert sweep["bh_pauli_max"] == pytest.approx(
        5.0 / 6.0, abs=1e-9)
    assert len(sweep["bh_grid_fidelities"]) == 144 * 2


def test_cnot_clone_known_values():
    # Basis states copy exactly; equatorial states give 1/2.
    for psi, expected in (
            (np.array([1.0, 0.0], dtype=complex), 1.0),
            (np.array([0.0, 1.0], dtype=complex), 1.0),
            (np.array([1.0, 1.0], dtype=complex) / math.sqrt(2.0),
             0.5),
            (np.array([1.0, -1.0], dtype=complex) / math.sqrt(2.0),
             0.5)):
        out = cc.cnot_clone(psi)
        rho = te.density_matrix(out)
        for keep in (0, 1):
            assert cc.clone_fidelity(
                psi, te.reduced_density_matrix(rho, keep=keep)) == \
                pytest.approx(expected, abs=1e-12)


def test_cnot_pauli_mean_exactly_2_3():
    sweep = cc.cloning_sweep()
    assert sweep["cnot_pauli_mean"] == pytest.approx(
        2.0 / 3.0, abs=1e-9)
    assert sweep["cnot_pauli_min"] == pytest.approx(0.5, abs=1e-12)
    assert sweep["cnot_pauli_max"] == pytest.approx(1.0, abs=1e-12)
    assert sweep["cnot_grid_mean"] == pytest.approx(
        0.641026, abs=1e-4)
    assert sweep["cnot_grid_max"] == pytest.approx(
        0.857988, abs=1e-4)


def test_claim_xlvii_verdict_pass():
    verdict = cc.claim_unitary_cloning_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"]["bh_grid_fidelity_is_5_6"] is True
    assert verdict["checks"]["bh_pauli_fidelity_is_5_6"] is True
    assert verdict["checks"]["bh_images_orthonormal"] is True
    assert verdict["checks"]["cnot_pauli_mean_is_2_3"] is True
    assert verdict["checks"]["cnot_grid_mean_at_most_bound"] is True
    assert verdict["bh_grid_mean"] == pytest.approx(
        5.0 / 6.0, abs=1e-9)
    assert verdict["cnot_pauli_mean"] == pytest.approx(
        2.0 / 3.0, abs=1e-9)


# ---------------------------------------------------------------------------
# (xlviii) Classical copy
# ---------------------------------------------------------------------------

def test_classical_copy_exact_at_zero_noise():
    for seed in (42, 7, 1234, 2026):
        row = cc.classical_copy_fidelity(0.0, seed)
        assert row["mean_fidelity"] == pytest.approx(1.0, abs=1e-12)


def test_classical_copy_exceeds_bound_at_working_sigma():
    # At every working sigma <= 0.10 the classical copy is
    # above 5/6 on every seed; at sigma = 1.0 it is below.
    for seed in (42, 7, 1234, 2026):
        rows = cc.classical_copy_sweep(seed)
        by_sigma = {r["sigma"]: r for r in rows}
        for sigma in (0.0, 0.01, 0.05, 0.1):
            assert by_sigma[sigma]["mean_fidelity"] > 5.0 / 6.0
        assert by_sigma[1.0]["mean_fidelity"] < 5.0 / 6.0


def test_classical_copy_sigma_025_seed_42():
    row = cc.classical_copy_fidelity(0.25, 42)
    assert row["mean_fidelity"] == pytest.approx(0.8540, abs=1e-3)


def test_classical_copy_crossings():
    assert cc.classical_copy_crossing(42)["sigma_below"] == \
        pytest.approx(0.32, abs=1e-9)
    assert cc.classical_copy_crossing(42)["sigma_above"] == \
        pytest.approx(0.31, abs=1e-9)
    assert cc.classical_copy_crossing(7)["sigma_below"] == \
        pytest.approx(0.26, abs=1e-9)
    assert cc.classical_copy_crossing(2026)["sigma_below"] == \
        pytest.approx(0.31, abs=1e-9)
    # Seed 1234 is already below 5/6 at the bracket start.
    crossing_1234 = cc.classical_copy_crossing(1234)
    assert crossing_1234["sigma_below"] == pytest.approx(
        0.25, abs=1e-9)
    assert crossing_1234["sigma_above"] is None


def test_claim_xlviii_verdict_fail():
    verdict = cc.claim_blanket_cloning_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["unitary_cloners_respect_bound"] is True
    assert verdict["checks"]["classical_copy_respects_bound"] is False
    for r in verdict["per_seed"]:
        assert r["max_mean_fidelity"] == pytest.approx(
            1.0, abs=1e-12)


# ---------------------------------------------------------------------------
# Aggregate, thresholds, validation, main
# ---------------------------------------------------------------------------

def test_cloning_ceiling_claims_aggregate():
    verdicts = cc.cloning_ceiling_claims()
    assert verdicts["n_claims"] == 5
    assert verdicts["n_passed"] == 3
    assert verdicts["all_pass"] is False
    assert verdicts["headline_allowed"] is False


def test_thresholds_set():
    thresholds = cc._thresholds()
    assert thresholds["purity_tol"] == pytest.approx(1e-9)
    assert thresholds["wootters_tol"] == pytest.approx(1e-7)
    assert thresholds["d_chi_tol"] == pytest.approx(1e-9)
    assert thresholds["spearman_abs_gap_max"] == pytest.approx(-0.90)
    assert thresholds["holevo_tol"] == pytest.approx(1e-9)
    assert thresholds["bh_fidelity_tol"] == pytest.approx(1e-9)
    assert thresholds["bh_orthonormality_tol"] == pytest.approx(1e-12)
    assert thresholds["cnot_pauli_mean_tol"] == pytest.approx(1e-9)
    assert thresholds["cloning_bound"] == pytest.approx(5.0 / 6.0)


def test_input_validation():
    with pytest.raises(ValueError):
        cc.bh_clone(np.array([1.0, 0.0, 0.0], dtype=complex))
    with pytest.raises(ValueError):
        cc.cnot_clone(np.array([1.0, 0.0, 0.0], dtype=complex))
    with pytest.raises(ValueError):
        cc._clone_reduced_state(np.zeros(8, dtype=complex), 3)


def test_main_runs(capsys):
    cc.main()
    out = capsys.readouterr().out
    assert "3/5 claims passed" in out
    assert "claim (xliv) verdict: PASS" in out
    assert "claim (xlv) verdict: FAIL" in out
    assert "claim (xlvi) verdict: PASS" in out
    assert "claim (xlvii) verdict: PASS" in out
    assert "claim (xlviii) verdict: FAIL" in out
