# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for darwinism.py: quantum-Darwinism redundancy plateau (v0.8.0)."""

import math

import numpy as np
import pytest

import darwinism as dw


def test_record_states_hard_orthogonal_soft_overlap_half():
    e0, e1 = dw.record_states(math.pi / 2.0)
    assert abs(np.vdot(e0, e1)) == pytest.approx(0.0, abs=1e-12)
    assert dw.record_overlap(math.pi / 2.0) == pytest.approx(0.0, abs=1e-12)
    assert dw.record_overlap(math.pi / 3.0) == pytest.approx(0.5, abs=1e-12)
    for phi in (math.pi / 2.0, math.pi / 3.0):
        a, b = dw.record_states(phi)
        assert float(np.linalg.norm(a)) == pytest.approx(1.0, abs=1e-12)
        assert float(np.linalg.norm(b)) == pytest.approx(1.0, abs=1e-12)


def test_branching_state_normalized():
    for system in ("bell", "binary"):
        for n_env in (1, 3, 10):
            psi, _ = dw.branching_state(n_env, system)
            assert psi.shape == (1 << (dw.system_n_qubits(system) + n_env),)
            assert float(np.linalg.norm(psi)) == pytest.approx(1.0, abs=1e-12)


def test_closed_form_vs_partial_trace_small_n():
    # The closed-form fragment state is exact: it agrees
    # with the general partial trace to 1e-9 at N = 3.
    for system in ("bell", "binary"):
        n_sys = dw.system_n_qubits(system)
        for phi in (math.pi / 2.0, math.pi / 3.0):
            for p in (0.0, 0.5, 1.0):
                psi, _ = dw.branching_state(3, system, phi)
                rho = dw.density_matrix(psi)
                rho = dw.dephase_pointer(rho, dw.pointer_states(system),
                                         n_sys, 3, p)
                for m in range(4):
                    traced = dw.fragment_state(rho, n_sys, 3, m)
                    direct = dw.fragment_state_direct(m, 3, system, phi, p)
                    assert np.allclose(traced, direct, atol=1e-9)


def test_numeric_vs_analytic_subset_n10():
    # Numeric fragment quantities agree with the analytic
    # closed form at N = 10 (subset of m, to keep the
    # 2048-dim eigvalsh cost down; the pilot checked all
    # m to 2e-15).
    for phi, ms in ((math.pi / 2.0, (0, 1, 5, 10)),
                    (math.pi / 3.0, (1, 5))):
        c = dw.record_overlap(phi)
        for m in ms:
            rho_sf = dw.fragment_state_direct(m, 10, "binary", phi, 0.5)
            q = dw.fragment_quantities(rho_sf, 1, "binary")
            a = dw.analytic_fragment_values(m, 10, c, 0.5)
            for key in ("h_system_bits", "h_fragment_bits",
                        "h_joint_bits", "mutual_information_bits",
                        "holevo_chi_bits", "discord_bits"):
                assert q[key] == pytest.approx(a[key], abs=1e-9)


def test_plateau_hard_exact():
    rows = dw.plateau_sweep(10, "binary", math.pi / 2.0, 0.5)
    for r in rows[1:10]:
        assert r["mutual_information_bits"] == pytest.approx(1.0, abs=1e-9)
        assert r["holevo_chi_bits"] == pytest.approx(1.0, abs=1e-9)
        assert r["discord_bits"] == pytest.approx(0.0, abs=1e-9)
    assert rows[10]["mutual_information_bits"] == pytest.approx(
        1.1887, abs=1e-3)
    assert rows[10]["discord_bits"] == pytest.approx(0.1887, abs=1e-3)
    assert rows[0]["mutual_information_bits"] == pytest.approx(0.0, abs=1e-9)


def test_plateau_soft_values():
    rows = dw.plateau_sweep(10, "binary", math.pi / 3.0, 0.5)
    assert rows[1]["mutual_information_bits"] == pytest.approx(
        0.8113, abs=1e-3)
    assert rows[2]["mutual_information_bits"] == pytest.approx(
        0.9544, abs=1e-3)
    assert rows[9]["mutual_information_bits"] == pytest.approx(
        1.0456, abs=1e-3)
    assert rows[9]["discord_bits"] == pytest.approx(0.0456, abs=1e-3)
    assert rows[10]["discord_bits"] == pytest.approx(0.1887, abs=1e-3)
    # Discord is below 1e-4 through m = 4 and only then
    # starts rising visibly (exponentially suppressed in
    # N - m: 5e-7, 3e-6, 1e-5, 4e-5 at m = 1..4).
    for r in rows[1:5]:
        assert r["discord_bits"] <= 1e-4


def test_redundancy_values():
    for system in ("binary", "bell"):
        hard = dw.plateau_sweep(10, system, math.pi / 2.0, 0.5)
        soft = dw.plateau_sweep(10, system, math.pi / 3.0, 0.5)
        assert dw.plateau_start(hard) == 1
        assert dw.redundancy(hard, 10) == 10
        assert dw.plateau_start(soft) == 2
        assert dw.redundancy(soft, 10) == 5


def test_systems_agree():
    # The analytic structure is system-independent: binary
    # and Bell give identical I / chi / discord.
    for phi in (math.pi / 2.0, math.pi / 3.0):
        a = dw.plateau_sweep(10, "binary", phi, 0.5)
        b = dw.plateau_sweep(10, "bell", phi, 0.5)
        for ra, rb in zip(a, b):
            for key in ("mutual_information_bits", "holevo_chi_bits",
                        "discord_bits"):
                assert ra[key] == pytest.approx(rb[key], abs=1e-9)


def test_discord_nonnegative_under_noise():
    # The pointer measurement is complete (sector
    # projectors sum to the identity), so chi <= I and the
    # discord is never negative -- even once vector noise
    # populates the non-pointer basis states.
    import unity
    for sigma in (0.05, 0.25):
        psi, _ = dw.branching_state(6, "bell", math.pi / 2.0)
        copies = unity.gaussian_copies(np.real(psi), sigma, 5, 42)
        for cvec in copies:
            for m in range(1, 7):
                rho_sf = dw.fragment_state_from_vector(
                    np.asarray(cvec, dtype=complex), 2, 6, m)
                rho_sf = dw.dephase_fragment(rho_sf, 2, m, "bell", 0.5)
                q = dw.fragment_quantities(rho_sf, 2, "bell")
                assert q["discord_bits"] >= -1e-9


def test_dephasing_picture():
    # The classical plateau is p-independent; the quantum
    # excess at m = N falls with the einselection strength.
    for p, disc in ((0.0, 1.0), (0.5, 0.1887), (1.0, 0.0)):
        rows = dw.plateau_sweep(10, "binary", math.pi / 2.0, p)
        assert np.mean([r["mutual_information_bits"]
                        for r in rows[1:10]]) == pytest.approx(
                            1.0, abs=1e-9)
        assert rows[10]["discord_bits"] == pytest.approx(disc, abs=1e-3)


def test_turn_on_hard():
    rows = dw.branching_turn_on(10, "bell", math.pi / 2.0, 0.5)
    assert rows[0]["system_concurrence"] == pytest.approx(0.5, abs=1e-9)
    assert rows[0]["chi_fragment_1_bits"] == pytest.approx(0.0, abs=1e-9)
    assert rows[0]["redundancy"] == 0
    for r in rows:
        assert r["system_d"] == pytest.approx(2.0 / 3.0, abs=1e-9)
    for r in rows[1:]:
        assert r["system_concurrence"] == pytest.approx(0.0, abs=1e-9)
        assert r["chi_fragment_1_bits"] == pytest.approx(1.0, abs=1e-9)
        assert r["redundancy"] == r["k_interacted"]


def test_turn_on_soft():
    rows = dw.branching_turn_on(10, "bell", math.pi / 3.0, 0.5)
    for k, r in enumerate(rows):
        assert r["system_concurrence"] == pytest.approx(
            0.5 * 0.5 ** k, abs=1e-9)
        assert r["system_d"] == pytest.approx(2.0 / 3.0, abs=1e-9)
    for r in rows[1:]:
        assert r["chi_fragment_1_bits"] == pytest.approx(0.8113, abs=1e-3)
    assert [r["redundancy"] for r in rows] == [0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5]


def test_claim_xx_verdict_pass():
    verdict = dw.claim_plateau_verdict()
    assert verdict["passed"] is True
    assert all(verdict["checks"].values())
    combos = {c["system"] + "_" + c["branching"]: c
              for c in verdict["combos"]}
    assert combos["binary_hard"]["m_star"] == 1
    assert combos["binary_hard"]["redundancy"] == 10
    assert combos["binary_soft"]["m_star"] == 2
    assert combos["binary_soft"]["redundancy"] == 5
    assert combos["bell_hard"]["redundancy"] == 10
    assert combos["bell_soft"]["redundancy"] == 5
    for c in verdict["combos"]:
        assert c["discord_full_env_bits"] == pytest.approx(0.1887, abs=1e-3)


def test_claim_xxi_verdict_fail():
    # D is exactly 2/3 for every k, so it cannot rise with
    # redundancy or chi and cannot anti-track discord. The
    # concurrence half passes; the D half fails.
    verdict = dw.claim_d_tracks_classical_verdict()
    assert verdict["passed"] is False
    for fam in verdict["families"]:
        assert fam["pearson_d_redundancy"] == pytest.approx(0.0, abs=1e-9)
        assert fam["pearson_d_chi"] == pytest.approx(0.0, abs=1e-9)
        assert fam["pearson_d_discord"] == pytest.approx(0.0, abs=1e-9)
        assert fam["d_min"] == pytest.approx(2.0 / 3.0, abs=1e-9)
        assert fam["d_max"] == pytest.approx(2.0 / 3.0, abs=1e-9)
    hard = verdict["families"][0]
    soft = verdict["families"][1]
    assert hard["concurrence_k0"] == pytest.approx(0.5, abs=1e-9)
    assert hard["concurrence_kN"] == pytest.approx(0.0, abs=1e-9)
    assert soft["concurrence_kN"] == pytest.approx(0.0005, abs=1e-3)
    assert verdict["checks"]["hard_concurrence_falls"] is True
    assert verdict["checks"]["soft_concurrence_falls"] is True
    assert verdict["checks"]["hard_d_rises_with_redundancy"] is False
    assert verdict["checks"]["hard_d_rises_with_chi"] is False
    assert verdict["checks"]["hard_d_anti_tracks_discord"] is False


def test_claim_xxii_verdict_fail():
    # The gap is robust (0.77) and the redundancy is robust
    # at the 0.25 -> 0.50 step (1.0), but the discord is
    # NOT fragile -- it rises 11x across the grid -- and
    # the gap tracks neither redundancy (0.35) nor discord
    # (-0.44). Concurrence anti-tracks discord (-0.63).
    verdict = dw.claim_non_transfer_verdict()
    assert verdict["passed"] is False
    assert verdict["gap_ratio_050_over_025"] == pytest.approx(
        0.7726, abs=1e-3)
    assert verdict["redundancy_ratio_050_over_025"] == pytest.approx(
        1.0, abs=1e-9)
    assert verdict["discord_ratio_050_over_025"] == pytest.approx(
        0.9944, abs=1e-3)
    assert verdict["redundancy_grid_ratio"] == pytest.approx(
        1.0 / 3.0, abs=1e-9)
    assert verdict["discord_grid_ratio"] == pytest.approx(11.198, abs=1e-2)
    assert verdict["pearson_gap_redundancy"] == pytest.approx(
        0.3528, abs=1e-3)
    assert verdict["pearson_gap_discord"] == pytest.approx(
        -0.4411, abs=1e-3)
    assert verdict["pearson_concurrence_discord"] == pytest.approx(
        -0.6259, abs=1e-3)
    assert verdict["checks"]["gap_robust_step"] is True
    assert verdict["checks"]["redundancy_robust_step"] is True
    assert verdict["checks"]["discord_fragile_step"] is False
    assert verdict["checks"]["redundancy_robust_grid"] is False
    assert verdict["checks"]["discord_fragile_grid"] is False
    assert verdict["checks"]["gap_tracks_redundancy"] is False
    assert verdict["checks"]["gap_does_not_track_discord"] is True
    assert verdict["checks"]["concurrence_tracks_discord"] is False
    # The measured series themselves.
    assert verdict["redundancies"] == [6.0, 6.0, 2.0, 2.0, 2.0, 2.0, 2.0]
    assert verdict["gaps_bits"][4] == pytest.approx(4.3352, abs=1e-3)
    assert verdict["gaps_bits"][5] == pytest.approx(3.3494, abs=1e-3)


def test_darwinism_claims_aggregate():
    verdicts = dw.darwinism_claims()
    assert verdicts["n_claims"] == 3
    assert verdicts["n_passed"] == 1
    assert verdicts["all_pass"] is False
    assert verdicts["headline_allowed"] is False


def test_thresholds_set():
    thresholds = dw._thresholds()
    assert thresholds["plateau_tol_bits"] == pytest.approx(0.10)
    assert thresholds["discord_plateau_max_bits"] == pytest.approx(0.10)
    assert thresholds["discord_full_env_min_bits"] == pytest.approx(0.10)
    assert thresholds["plateau_start_max"] == 5
    assert thresholds["d_track_min"] == pytest.approx(0.9)
    assert thresholds["d_antitrack_max"] == pytest.approx(-0.9)
    assert thresholds["robust_ratio_min"] == pytest.approx(0.5)
    assert thresholds["fragile_ratio_max"] == pytest.approx(0.5)


def test_input_validation():
    with pytest.raises(ValueError):
        dw.pointer_states("ghz")
    with pytest.raises(ValueError):
        dw.system_n_qubits("ghz")
    with pytest.raises(ValueError):
        dw.branching_state(0)
    with pytest.raises(ValueError):
        dw.fragment_state(np.eye(4, dtype=complex), 1, 1, 2)
    with pytest.raises(ValueError):
        dw.dephase_fragment(np.eye(4, dtype=complex), 1, 0, "binary", 1.5)
    with pytest.raises(ValueError):
        dw.fragment_state_from_vector(np.zeros(7, dtype=complex), 1, 2, 1)


def test_main_runs(capsys):
    dw.main()
    out = capsys.readouterr().out
    assert "1/3 claims passed" in out
    assert "claim (xx) verdict: PASS" in out
    assert "claim (xxi) verdict: FAIL" in out
    assert "claim (xxii) verdict: FAIL" in out
