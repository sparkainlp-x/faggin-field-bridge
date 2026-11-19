# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for synergistic_target.py: XOR-target PID (v0.20.0)."""

from collections import Counter

import numpy as np
import pytest

import synergistic_target as st


def test_xor_pid_independent_uniform():
    # X1, X2 independent uniform over 4 concepts: Y = X1 (+) X2
    # is uniform, each source alone carries ZERO about Y, the
    # pair jointly carries all 2 bits -- pure synergy.
    joint = np.full((4, 4), 1.0 / 16.0)
    p = st.xor_pid_from_joint(joint)
    assert p["h_y_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["total_info_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["i_x1_y_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["i_x2_y_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["redundant_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique1_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique2_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["synergistic_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["atom_sum_bits"] == pytest.approx(
        p["total_info_bits"], abs=1e-9)


def test_xor_pid_perfectly_correlated():
    # X1 = X2 uniform: Y = 0 always, no information at all.
    joint = np.diag(np.full(4, 0.25))
    p = st.xor_pid_from_joint(joint)
    assert p["h_y_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["total_info_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["redundant_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique1_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique2_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["synergistic_bits"] == pytest.approx(0.0, abs=1e-9)


def test_xor_pid_one_source_deterministic():
    # X1 fixed, X2 uniform: Y = X2, all 2 bits unique to X2;
    # nothing redundant, nothing synergistic.
    joint = np.zeros((4, 4))
    joint[0, :] = 0.25
    p = st.xor_pid_from_joint(joint)
    assert p["h_y_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["redundant_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique1_bits"] == pytest.approx(0.0, abs=1e-9)
    assert p["unique2_bits"] == pytest.approx(2.0, abs=1e-9)
    assert p["synergistic_bits"] == pytest.approx(0.0, abs=1e-9)


def test_xor_pid_invalid_joint_raises():
    with pytest.raises(ValueError):
        st.xor_pid_from_joint(np.zeros((4, 4)))
    with pytest.raises(ValueError):
        st.xor_pid_from_joint(np.full((3, 3), 1.0 / 9.0))
    with pytest.raises(ValueError):
        st.xor_pid_from_joint(np.full((4, 4), -1.0 / 16.0))


def test_sampled_h_y():
    # Y = 0 always.
    assert st.sampled_h_y(Counter({(0, 0): 50, (1, 1): 50})) == (
        pytest.approx(0.0, abs=1e-9))
    # Y uniform over {0, 1}.
    assert st.sampled_h_y(Counter(
        {(0, 1): 25, (1, 0): 25, (0, 0): 25, (1, 1): 25})) == (
        pytest.approx(1.0, abs=1e-9))
    with pytest.raises(ValueError):
        st.sampled_h_y(Counter())


def test_xor_seed42_sigma025_values():
    # Calibration pilot values (exact pooled distribution).
    row = st.xor_arm_distributions(sigma=0.25, seed=42)
    assert row["delta_total_info_bits"] == pytest.approx(
        1.1194, abs=1e-3)
    assert row["delta_synergistic_bits"] == pytest.approx(
        1.4472, abs=1e-3)
    assert row["delta_redundant_bits"] == pytest.approx(
        0.3143, abs=1e-3)
    assert row["delta_unique_bits"] == pytest.approx(
        -0.6421, abs=1e-3)
    # The atoms' differences sum to the information gap exactly.
    assert (row["delta_synergistic_bits"]
            + row["delta_redundant_bits"]
            + row["delta_unique_bits"]) == pytest.approx(
                row["delta_total_info_bits"], abs=1e-9)
    # Synergy separates from redundancy in the collaborating
    # arm, where the joint-outcome target could not: Syn_c is
    # 4.6x Red_c here, against Syn ~= Red in v0.14.0.
    assert row["collaborating"]["xor_pid"]["synergistic_bits"] == (
        pytest.approx(1.4472, abs=1e-3))
    assert row["collaborating"]["xor_pid"]["redundant_bits"] == (
        pytest.approx(0.3143, abs=1e-3))
    assert row["isolated"]["xor_pid"]["h_y_bits"] == pytest.approx(
        0.7219, abs=1e-3)


def test_xor_seed7_sigma025_values():
    row = st.xor_arm_distributions(sigma=0.25, seed=7)
    assert row["delta_total_info_bits"] == pytest.approx(
        1.1668, abs=1e-3)
    assert row["delta_synergistic_bits"] == pytest.approx(
        1.0010, abs=1e-3)
    assert row["delta_redundant_bits"] == pytest.approx(
        0.1397, abs=1e-3)


def test_xor_seed1234_sigma025_negative_gap():
    # Held-out seed 1234: the isolated arm carries MORE total
    # information about the XOR target than the collaborating
    # arm (I_i = 1.7610 vs I_c = 1.5019), so the information
    # gap itself is negative -- while delta-synergy stays
    # positive (+1.0248) and delta-redundancy goes negative
    # (-0.3953: the isolated arm is MORE redundant about Y).
    row = st.xor_arm_distributions(sigma=0.25, seed=1234)
    assert row["delta_total_info_bits"] == pytest.approx(
        -0.2591, abs=1e-3)
    assert row["delta_synergistic_bits"] == pytest.approx(
        1.0248, abs=1e-3)
    assert row["delta_redundant_bits"] == pytest.approx(
        -0.3953, abs=1e-3)
    assert row["isolated"]["xor_pid"]["total_info_bits"] == (
        pytest.approx(1.7610, abs=1e-3))


def test_claim_lxiv_xor_identity_passes():
    verdict = st.claim_xor_identity_verdict()
    assert verdict["passed"] is True
    assert verdict["worst_identity_error_bits"] <= 1e-9
    assert verdict["worst_atom_bits"] >= -1e-9
    assert verdict["worst_exact_sampled_h_y_diff_bits"] <= 0.25


def test_claim_lxv_synergy_share_fails_on_held_out_seed():
    # Calibration passes (shares 1.293 / 0.858), but the
    # claim FAILS on held-out seed 1234: the information
    # gap itself is negative there (-0.2591 bits), so the
    # synergy share is -3.956. The separation half
    # (dSyn > dRed) still holds on every seed, including
    # 1234 (+1.0248 > -0.3953); only the share-of-gap
    # half fails, because the gap framing breaks.
    verdict = st.claim_synergy_dominant_verdict()
    assert verdict["passed"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["synergy_share_of_gap"] == pytest.approx(
        1.293, abs=1e-3)
    assert by_seed[7]["synergy_share_of_gap"] == pytest.approx(
        0.858, abs=1e-3)
    assert by_seed[1234]["synergy_share_of_gap"] == pytest.approx(
        -3.956, abs=1e-3)
    assert by_seed[2026]["synergy_share_of_gap"] == pytest.approx(
        2.072, abs=1e-3)
    for r in verdict["per_seed"]:
        assert (r["delta_synergistic_bits"]
                > r["delta_redundant_bits"])


def test_claim_lxvi_synergy_does_not_rise_with_r():
    verdict = st.claim_synergy_rises_falls_verdict()
    assert verdict["passed"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["pearson_synergy_r_post"] == pytest.approx(
        0.3731, abs=1e-3)
    assert by_seed[7]["pearson_synergy_r_post"] == pytest.approx(
        0.3424, abs=1e-3)
    assert by_seed[1234]["pearson_synergy_r_post"] == pytest.approx(
        -0.3397, abs=1e-3)
    assert by_seed[2026]["pearson_synergy_r_post"] == pytest.approx(
        0.9036, abs=1e-3)
    # Synergy RISES from sigma = 0.25 to 0.50, it does
    # not fall, on every seed -- it climbs toward the
    # 2-bit ceiling as the marginals uniformize.
    for r in verdict["per_seed"]:
        assert (r["synergy_collab_sigma_0.50_bits"]
                > r["synergy_collab_sigma_0.25_bits"])


def test_claim_lxvii_redundancy_share_small():
    verdict = st.claim_redundancy_share_verdict()
    assert verdict["passed"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["worst_redundancy_share"] == pytest.approx(
        0.1924, abs=1e-3)
    assert by_seed[7]["worst_redundancy_share"] == pytest.approx(
        0.2357, abs=1e-3)
    assert by_seed[1234]["worst_redundancy_share"] == pytest.approx(
        0.1396, abs=1e-3)
    assert by_seed[2026]["worst_redundancy_share"] == pytest.approx(
        0.0882, abs=1e-3)


def test_synergistic_target_claims_aggregate():
    verdicts = st.synergistic_target_claims()
    assert verdicts["n_claims"] == 4
    # 2/4 pass: the identity and the redundancy-share
    # claims pass; the "gap is synergy" claim fails on
    # held-out seed 1234 (negative information gap) and
    # the "synergy rises with R and falls at 0.50" claim
    # fails on every seed (synergy tracks noise-driven
    # uniformity, not resonance).
    assert verdicts["n_passed"] == 2
    assert verdicts["claim_lxiv_xor_identity"]["passed"] is True
    assert verdicts["claim_lxv_synergy_dominant"]["passed"] is False
    assert verdicts["claim_lxvi_synergy_rises_falls"]["passed"] is False
    assert verdicts["claim_lxvii_redundancy_share"]["passed"] is True
