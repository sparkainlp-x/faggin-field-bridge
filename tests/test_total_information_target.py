# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for total_information_target.py: MAX-target PID (v0.21.0)."""

from collections import Counter

import numpy as np
import pytest

import synergistic_target as st
import total_information_target as tt


def test_general_pid_reproduces_xor():
    # The general target_pid_from_joint with f = XOR must
    # reproduce synergistic_target.xor_pid_from_joint
    # exactly, on every canonical joint.
    joints = [
        np.full((4, 4), 1.0 / 16.0),
        np.diag(np.full(4, 0.25)),
        np.array([[0.25, 0.25, 0.25, 0.25],
                  [0.0, 0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0, 0.0]]),
    ]
    for joint in joints:
        mine = tt.target_pid_from_joint(joint, lambda a, b: a ^ b, 4)
        ref = st.xor_pid_from_joint(joint)
        for key in ("h_y_bits", "total_info_bits", "i_x1_y_bits",
                    "i_x2_y_bits", "redundant_bits", "unique1_bits",
                    "unique2_bits", "synergistic_bits"):
            assert mine[key] == pytest.approx(ref[key], abs=1e-9)


def test_max_pid_independent_uniform():
    # X1, X2 independent uniform over 4 concepts: Y =
    # max(X1, X2) takes 0/1/2/3 with probabilities
    # 1/16, 3/16, 5/16, 7/16. MAX is NOT pure synergy:
    # a single source alone carries 0.6712 bits about Y.
    joint = np.full((4, 4), 1.0 / 16.0)
    p = tt.max_pid_from_joint(joint)
    assert p["h_y_bits"] == pytest.approx(1.7490, abs=1e-3)
    assert p["total_info_bits"] == pytest.approx(1.7490, abs=1e-3)
    assert p["i_x1_y_bits"] == pytest.approx(0.6712, abs=1e-3)
    assert p["i_x2_y_bits"] == pytest.approx(0.6712, abs=1e-3)
    assert p["redundant_bits"] == pytest.approx(0.6712, abs=1e-3)
    assert p["unique1_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique2_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["synergistic_bits"] == pytest.approx(1.0778, abs=1e-3)
    assert p["atom_sum_bits"] == pytest.approx(
        p["total_info_bits"], abs=1e-9)


def test_max_pid_perfectly_correlated():
    # X1 = X2 uniform: Y = X1 = X2, all 2 bits redundant.
    joint = np.diag(np.full(4, 0.25))
    p = tt.max_pid_from_joint(joint)
    assert p["h_y_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["total_info_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["redundant_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["unique1_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique2_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["synergistic_bits"] == pytest.approx(0.0, abs=1e-9)


def test_max_pid_one_source_deterministic():
    # X1 fixed, X2 uniform: Y = X2, all 2 bits unique to X2;
    # and symmetrically X2 fixed -> all unique to X1.
    joint = np.zeros((4, 4))
    joint[0, :] = 0.25
    p = tt.max_pid_from_joint(joint)
    assert p["h_y_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["redundant_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique1_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique2_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["synergistic_bits"] == pytest.approx(0.0, abs=1e-9)
    joint = np.zeros((4, 4))
    joint[:, 0] = 0.25
    p = tt.max_pid_from_joint(joint)
    assert p["unique1_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["unique2_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["synergistic_bits"] == pytest.approx(0.0, abs=1e-9)


def test_target_pid_invalid_joint_raises():
    with pytest.raises(ValueError):
        tt.target_pid_from_joint(
            np.zeros((4, 4)), lambda a, b: max(a, b), 4)
    with pytest.raises(ValueError):
        tt.target_pid_from_joint(
            np.full((3, 3), 1.0 / 9.0), lambda a, b: max(a, b), 4)
    with pytest.raises(ValueError):
        tt.target_pid_from_joint(
            np.full((4, 4), -1.0 / 16.0), lambda a, b: max(a, b), 4)
    with pytest.raises(ValueError):
        tt.target_pid_from_joint(
            np.full((4, 4), 1.0 / 16.0), lambda a, b: 99, 4)


def test_sampled_h_y_max():
    # Y = max = 3 always.
    assert tt.sampled_h_y_max(Counter({(3, 3): 50, (2, 3): 50})) == (
        pytest.approx(0.0, abs=1e-9))
    # Y uniform over {2, 3}.
    assert tt.sampled_h_y_max(Counter(
        {(2, 2): 50, (3, 3): 50})) == (
        pytest.approx(1.0, abs=1e-9))
    with pytest.raises(ValueError):
        tt.sampled_h_y_max(Counter())


def test_screen_selects_max():
    # The candidate screen (calibration seeds only) picks
    # MAX; the incumbents are eligible-or-not but excluded,
    # AND/MIN fail the gates, OR tracks MAX within 0.03 bits.
    screen = tt.screen_candidates()
    assert screen["selected_target"] == "max"
    by_target = {r["target"]: r for r in screen["candidates"]}
    assert len(screen["candidates"]) == 14
    assert by_target["xor"]["eligible"] is True
    assert by_target["xor"]["excluded_from_selection"] is True
    assert by_target["joint"]["excluded_from_selection"] is True
    assert by_target["diff_mod4"]["excluded_from_selection"] is True
    assert by_target["sum_mod4"]["excluded_from_selection"] is True
    assert by_target["and"]["eligible"] is False
    assert by_target["min"]["eligible"] is False
    assert by_target["x1"]["eligible"] is False
    assert by_target["max"]["min_delta_total_info_bits"] == (
        pytest.approx(1.0707, abs=1e-3))
    assert by_target["or"]["min_delta_total_info_bits"] == (
        pytest.approx(1.0433, abs=1e-3))
    assert by_target["max"]["eligible"] is True


def test_max_seed42_sigma025_values():
    # Calibration pilot values (exact pooled distribution).
    # The isolated arm is degenerate here (I_isol = 0):
    # the design-B lock-in puts both collapsed agents on
    # one concept, so max is a point mass.
    row = tt.max_arm_distributions(sigma=0.25, seed=42)
    assert row["delta_total_info_bits"] == pytest.approx(
        1.8927, abs=1e-3)
    assert row["delta_synergistic_bits"] == pytest.approx(
        1.0279, abs=1e-3)
    assert row["delta_redundant_bits"] == pytest.approx(
        0.6758, abs=1e-3)
    assert row["delta_unique_bits"] == pytest.approx(
        0.1890, abs=1e-3)
    assert (row["delta_synergistic_bits"]
            + row["delta_redundant_bits"]
            + row["delta_unique_bits"]) == pytest.approx(
                row["delta_total_info_bits"], abs=1e-9)
    assert row["isolated"]["max_pid"]["total_info_bits"] == (
        pytest.approx(0.0, abs=1e-9))
    assert row["collaborating"]["max_pid"]["synergistic_bits"] == (
        pytest.approx(1.0279, abs=1e-3))


def test_max_seed7_sigma025_values():
    # Calibration: the isolated arm is NOT degenerate here.
    row = tt.max_arm_distributions(sigma=0.25, seed=7)
    assert row["delta_total_info_bits"] == pytest.approx(
        1.0707, abs=1e-3)
    assert row["delta_synergistic_bits"] == pytest.approx(
        1.0316, abs=1e-3)
    assert row["delta_redundant_bits"] == pytest.approx(
        0.2589, abs=1e-3)
    assert row["isolated"]["max_pid"]["total_info_bits"] == (
        pytest.approx(0.8813, abs=1e-3))


def test_max_held_out_seeds_positive_gap():
    # Held-out seeds: the gap stays positive at sigma =
    # 0.25, where the XOR gap went negative on seed 1234.
    row = tt.max_arm_distributions(sigma=0.25, seed=1234)
    assert row["delta_total_info_bits"] == pytest.approx(
        0.3266, abs=1e-3)
    assert row["collaborating"]["max_pid"]["total_info_bits"] == (
        pytest.approx(1.0485, abs=1e-3))
    assert row["isolated"]["max_pid"]["total_info_bits"] == (
        pytest.approx(0.7219, abs=1e-3))
    row = tt.max_arm_distributions(sigma=0.25, seed=2026)
    assert row["delta_total_info_bits"] == pytest.approx(
        0.6527, abs=1e-3)
    assert row["collaborating"]["max_pid"]["total_info_bits"] == (
        pytest.approx(1.3746, abs=1e-3))


def test_claim_lxviii_max_identity_passes():
    verdict = tt.claim_max_identity_verdict()
    assert verdict["passed"] is True
    assert verdict["worst_identity_error_bits"] <= 1e-9
    assert verdict["worst_atom_bits"] >= -1e-9
    assert verdict["worst_exact_sampled_h_y_diff_bits"] <= 0.25


def test_claim_lxix_delta_info_positive_passes():
    verdict = tt.claim_delta_info_positive_verdict()
    assert verdict["passed"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["delta_total_info_bits"] == pytest.approx(
        1.8927, abs=1e-3)
    assert by_seed[7]["delta_total_info_bits"] == pytest.approx(
        1.0707, abs=1e-3)
    assert by_seed[1234]["delta_total_info_bits"] == pytest.approx(
        0.3266, abs=1e-3)
    assert by_seed[2026]["delta_total_info_bits"] == pytest.approx(
        0.6527, abs=1e-3)


def test_claim_lxx_synergy_dominant_passes():
    verdict = tt.claim_synergy_dominant_verdict()
    assert verdict["passed"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["synergy_share_of_gap"] == pytest.approx(
        0.543, abs=1e-3)
    assert by_seed[7]["synergy_share_of_gap"] == pytest.approx(
        0.964, abs=1e-3)
    assert by_seed[1234]["synergy_share_of_gap"] == pytest.approx(
        1.226, abs=1e-3)
    assert by_seed[2026]["synergy_share_of_gap"] == pytest.approx(
        1.011, abs=1e-3)
    for r in verdict["per_seed"]:
        assert (r["delta_synergistic_bits"]
                > r["delta_redundant_bits"])


def test_claim_lxxi_redundancy_share_below_half():
    verdict = tt.claim_redundancy_share_verdict()
    assert verdict["passed"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    # The worst share sits at sigma = 0 on every seed
    # (the noiseless joint is seed-independent there).
    for seed in (42, 7, 1234, 2026):
        assert by_seed[seed]["worst_redundancy_share"] == (
            pytest.approx(0.3837, abs=1e-3))
        assert by_seed[seed]["worst_redundancy_share_sigma"] == 0.0


def test_claim_lxxii_delta_info_grid_passes():
    verdict = tt.claim_delta_info_grid_verdict()
    assert verdict["passed"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["min_delta_total_info_bits"] == (
        pytest.approx(0.4338, abs=1e-3))
    assert by_seed[42]["min_delta_total_info_sigma"] == 1.0
    assert by_seed[7]["min_delta_total_info_bits"] == (
        pytest.approx(0.2337, abs=1e-3))
    assert by_seed[7]["min_delta_total_info_sigma"] == 1.0
    assert by_seed[1234]["min_delta_total_info_bits"] == (
        pytest.approx(0.3266, abs=1e-3))
    assert by_seed[1234]["min_delta_total_info_sigma"] == 0.25
    assert by_seed[2026]["min_delta_total_info_bits"] == (
        pytest.approx(0.4789, abs=1e-3))
    assert by_seed[2026]["min_delta_total_info_sigma"] == 0.1


def test_total_information_target_claims_aggregate():
    verdicts = tt.total_information_target_claims()
    assert verdicts["n_claims"] == 5
    # 5/5 pass: the MAX target answers the v0.20.0 open
    # question -- collaboration raises total information
    # about it on every seed, at sigma = 0.25 and across
    # the grid, and the gap is synergy-dominant with
    # redundancy below half the target information.
    assert verdicts["n_passed"] == 5
    assert verdicts["claim_lxviii_max_identity"]["passed"] is True
    assert verdicts["claim_lxix_delta_info_positive"]["passed"] is True
    assert verdicts["claim_lxx_synergy_dominant"]["passed"] is True
    assert verdicts["claim_lxxi_redundancy_share"]["passed"] is True
    assert verdicts["claim_lxxii_delta_info_grid"]["passed"] is True
