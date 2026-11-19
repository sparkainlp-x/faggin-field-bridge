# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for pid.py: synergy-vs-redundancy PID (v0.14.0)."""

import numpy as np
import pytest

import pid


def test_pid_independent_uniform():
    # X1, X2 independent uniform over 4 concepts: H = 4 bits,
    # Red = 2, Uniq = 0, Syn = 2 (the pair together carries
    # the joint outcome; neither alone carries any of it
    # beyond the shared 2 bits -- here Red = Syn because
    # I(X1;X2) = 0).
    joint = np.full((4, 4), 1.0 / 16.0)
    p = pid.pid_from_joint(joint)
    assert p["h_joint_bits"] == pytest.approx(4.0, abs=1e-9)
    assert p["h1_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["mutual_information_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["redundant_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["unique1_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique2_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["synergistic_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["atom_sum_bits"] == pytest.approx(
        p["h_joint_bits"], abs=1e-9)


def test_pid_perfectly_correlated():
    # X1 = X2 uniform: H = 2 bits, all of it redundant,
    # no unique and no synergistic information.
    joint = np.diag(np.full(4, 0.25))
    p = pid.pid_from_joint(joint)
    assert p["h_joint_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["mutual_information_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["redundant_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["unique1_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique2_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["synergistic_bits"] == pytest.approx(0.0, abs=1e-9)


def test_pid_one_source_deterministic():
    # X1 fixed, X2 uniform: H = 2 bits, all of it unique
    # to X2; nothing redundant, nothing synergistic.
    joint = np.zeros((4, 4))
    joint[0, :] = 0.25
    p = pid.pid_from_joint(joint)
    assert p["h_joint_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["redundant_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique1_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique2_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["synergistic_bits"] == pytest.approx(0.0, abs=1e-9)


def test_pid_invalid_joint_raises():
    with pytest.raises(ValueError):
        pid.pid_from_joint(np.zeros((4, 4)))
    with pytest.raises(ValueError):
        pid.pid_from_joint(np.full((3, 3), 1.0 / 9.0))
    with pytest.raises(ValueError):
        pid.pid_from_joint(np.full((4, 4), -1.0 / 16.0))


def test_pair_arm_seed42_sigma025_values():
    # Calibration pilot values (exact pooled distribution).
    row = pid.pair_arm_distributions(sigma=0.25, seed=42)
    assert row["gap_bits"] == pytest.approx(2.2729, abs=1e-3)
    assert row["delta_synergistic_bits"] == pytest.approx(
        0.9248, abs=1e-3)
    assert row["delta_redundant_bits"] == pytest.approx(
        0.9453, abs=1e-3)
    assert row["delta_unique_bits"] == pytest.approx(0.4027, abs=1e-3)
    # The atoms' differences sum to the gap exactly.
    assert (row["delta_synergistic_bits"]
            + row["delta_redundant_bits"]
            + row["delta_unique_bits"]) == pytest.approx(
                row["gap_bits"], abs=1e-9)
    assert row["collaborating"]["pid"]["h_joint_bits"] == pytest.approx(
        2.9948, abs=1e-3)
    assert row["isolated"]["pid"]["h_joint_bits"] == pytest.approx(
        0.7219, abs=1e-3)
    # Synergy and redundancy are nearly equal in the
    # collaborating arm: I(X1;X2) is ~0.02 bits.
    assert row["collaborating"]["pid"]["mutual_information_bits"] == (
        pytest.approx(0.0204, abs=1e-3))
    assert abs(row["collaborating"]["pid"]["synergistic_bits"]
               - row["collaborating"]["pid"]["redundant_bits"]) < 0.05


def test_pair_arm_seed7_sigma025_values():
    row = pid.pair_arm_distributions(sigma=0.25, seed=7)
    assert row["gap_bits"] == pytest.approx(1.6554, abs=1e-3)
    assert row["delta_synergistic_bits"] == pytest.approx(
        0.7103, abs=1e-3)
    assert row["delta_redundant_bits"] == pytest.approx(
        0.3376, abs=1e-3)


def test_claim_xl_identity_passes():
    verdict = pid.claim_pid_identity_verdict()
    assert verdict["passed"] is True
    assert verdict["worst_identity_error_bits"] <= 1e-9
    assert verdict["worst_atom_bits"] >= -1e-9
    assert verdict["worst_exact_sampled_diff_bits"] <= 0.25


def test_claim_xli_synergy_not_dominant():
    # Calibration: seed 42 dSyn < dRed and both shares
    # < 50% -- the spec's "gap is synergy" prediction
    # fails, honestly.
    verdict = pid.claim_synergy_dominant_verdict()
    assert verdict["passed"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["delta_synergistic_bits"] < (
        by_seed[42]["delta_redundant_bits"])
    assert by_seed[42]["synergy_share_of_gap"] == pytest.approx(
        0.4069, abs=1e-3)
    assert by_seed[7]["synergy_share_of_gap"] == pytest.approx(
        0.4291, abs=1e-3)


def test_claim_xlii_synergy_does_not_rise_with_r():
    verdict = pid.claim_synergy_rises_falls_verdict()
    assert verdict["passed"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["pearson_synergy_r_post"] == pytest.approx(
        -0.2295, abs=1e-3)
    assert by_seed[7]["pearson_synergy_r_post"] == pytest.approx(
        -0.0404, abs=1e-3)
    # Synergy RISES from sigma = 0.25 to 0.50, it does
    # not fall, on both calibration seeds.
    assert (by_seed[42]["synergy_collab_sigma_0.50_bits"]
            > by_seed[42]["synergy_collab_sigma_0.25_bits"])
    assert (by_seed[7]["synergy_collab_sigma_0.50_bits"]
            > by_seed[7]["synergy_collab_sigma_0.25_bits"])


def test_claim_xliii_redundancy_robustness_seed_fragile():
    verdict = pid.claim_redundancy_robust_verdict()
    assert verdict["passed"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["robustness_ratio_050_over_025"] == (
        pytest.approx(0.2351, abs=1e-3))
    assert by_seed[7]["robustness_ratio_050_over_025"] == (
        pytest.approx(1.4455, abs=1e-3))


def test_pid_claims_aggregate():
    verdicts = pid.pid_claims()
    assert verdicts["n_claims"] == 4
    # Only the identity claim passes; the three
    # substantive spec predictions fail honestly.
    assert verdicts["n_passed"] == 1
    assert verdicts["claim_xl_pid_identity"]["passed"] is True
    assert verdicts["claim_xli_synergy_dominant"]["passed"] is False
    assert verdicts["claim_xlii_synergy_rises_falls"]["passed"] is False
    assert verdicts["claim_xliii_redundancy_robust"]["passed"] is False
    # The N = 4 context gap is the known +4.3352 bits.
    assert verdicts["n4_sampled_gap_seed42_sigma025_bits"] == (
        pytest.approx(4.3352, abs=1e-3))
