# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for per_generation_pid.py: per-generation PID (v0.22.0)."""

import numpy as np
import pytest

import per_generation_pid as pg
import pid


def test_per_generation_joints_reproduce_pooled():
    # The mean of the 10 per-generation joints is the
    # pooled joint, exactly (max abs diff 0.0), and the
    # mean R values agree too -- the v0.22.0 refactor of
    # pid.pair_arm_distributions changes nothing pooled.
    for seed in (42, 7, 1234, 2026):
        for sigma in (0.0, 0.25, 1.0):
            per_gen = pid.pair_arm_per_generation_joints(
                sigma=sigma, seed=seed)
            pooled = pid.pair_arm_distributions(
                sigma=sigma, seed=seed)
            for arm in ("collaborating", "isolated"):
                mean_joint = np.mean(per_gen[arm]["joints"], axis=0)
                assert np.max(np.abs(
                    mean_joint - pooled[arm]["joint"])) <= 1e-12
                assert per_gen[arm]["mean_r_post"] == pytest.approx(
                    pooled[arm]["mean_r_post"], abs=1e-12)
                assert len(per_gen[arm]["joints"]) == 10


def test_per_gen_xor_seed42_sigma025_values():
    # Calibration pilot values (exact per-generation
    # joints, XOR target). The pooled synergy (1.4472)
    # exceeds the per-generation mean (0.9887): the
    # pooled joint is a mixture, not an average.
    row = pg.per_generation_target_pid(sigma=0.25, seed=42,
                                       target="xor")
    assert row["mean_delta_total_info_bits"] == pytest.approx(
        1.7457, abs=1e-3)
    assert row["mean_delta_synergistic_bits"] == pytest.approx(
        0.9887, abs=1e-3)
    assert row["mean_delta_redundant_bits"] == pytest.approx(
        0.2582, abs=1e-3)
    assert row["mean_delta_unique_bits"] == pytest.approx(
        0.4989, abs=1e-3)
    assert (row["mean_delta_synergistic_bits"]
            + row["mean_delta_redundant_bits"]
            + row["mean_delta_unique_bits"]) == pytest.approx(
                row["mean_delta_total_info_bits"], abs=1e-9)
    assert row["collaborating"]["mean_pid"][
        "synergistic_bits"] == pytest.approx(0.9887, abs=1e-3)
    assert row["collaborating"]["pooled_pid"][
        "synergistic_bits"] == pytest.approx(1.4472, abs=1e-3)
    assert row["isolated"]["mean_pid"][
        "total_info_bits"] == pytest.approx(0.0, abs=1e-9)


def test_per_gen_xor_seed7_sigma025_values():
    row = pg.per_generation_target_pid(sigma=0.25, seed=7,
                                       target="xor")
    assert row["mean_delta_total_info_bits"] == pytest.approx(
        1.7649, abs=1e-3)
    assert row["mean_delta_synergistic_bits"] == pytest.approx(
        0.9542, abs=1e-3)
    assert row["mean_delta_redundant_bits"] == pytest.approx(
        0.1849, abs=1e-3)


def test_per_gen_xor_seed1234_sigma025_reversal():
    # The v0.20.0 failure on held-out seed 1234 was
    # itself a pooling artifact: pooled dI = -0.2591,
    # but the mean per-generation gap is +1.4356 and
    # synergy-majority (share 0.584).
    row = pg.per_generation_target_pid(sigma=0.25, seed=1234,
                                       target="xor")
    assert row["pooled_delta_total_info_bits"] == pytest.approx(
        -0.2591, abs=1e-3)
    assert row["mean_delta_total_info_bits"] == pytest.approx(
        1.4356, abs=1e-3)
    assert row["mean_delta_synergistic_bits"] == pytest.approx(
        0.8386, abs=1e-3)
    assert row["mean_delta_redundant_bits"] == pytest.approx(
        0.1202, abs=1e-3)


def test_per_gen_max_seed42_sigma025_values():
    # Calibration pilot values (MAX target). Per
    # generation the gap is NOT synergy-majority
    # (share 0.383): unique information carries
    # 0.5998 bits of the mean gap.
    row = pg.per_generation_target_pid(sigma=0.25, seed=42,
                                       target="max")
    assert row["mean_delta_total_info_bits"] == pytest.approx(
        1.6419, abs=1e-3)
    assert row["mean_delta_synergistic_bits"] == pytest.approx(
        0.6289, abs=1e-3)
    assert row["mean_delta_redundant_bits"] == pytest.approx(
        0.4132, abs=1e-3)
    assert row["mean_delta_unique_bits"] == pytest.approx(
        0.5998, abs=1e-3)
    assert row["collaborating"]["pooled_pid"][
        "synergistic_bits"] == pytest.approx(1.0279, abs=1e-3)


def test_per_gen_max_seed1234_sigma025_values():
    row = pg.per_generation_target_pid(sigma=0.25, seed=1234,
                                       target="max")
    assert row["mean_delta_total_info_bits"] == pytest.approx(
        0.8844, abs=1e-3)
    assert row["mean_delta_synergistic_bits"] == pytest.approx(
        0.3094, abs=1e-3)
    assert row["mean_delta_redundant_bits"] == pytest.approx(
        0.1754, abs=1e-3)


def test_per_gen_isolated_synergy_zero_everywhere():
    # The design-B isolated arm collapses each agent to
    # a decided concept each generation, so each
    # per-generation joint is a point mass: Syn_i = 0
    # exactly, on every seed and sigma, for both targets.
    for target in ("xor", "max"):
        for seed in (42, 7, 1234, 2026):
            for sigma in (0.0, 0.25, 0.5, 1.0):
                row = pg.per_generation_target_pid(
                    sigma=sigma, seed=seed, target=target)
                assert row["isolated"]["mean_pid"][
                    "synergistic_bits"] == pytest.approx(
                        0.0, abs=1e-9)
                assert row["isolated"]["mean_pid"][
                    "total_info_bits"] == pytest.approx(
                        0.0, abs=1e-9)


def test_per_gen_invalid_target_raises():
    with pytest.raises(ValueError):
        pg.per_generation_target_pid(target="joint")


def test_claim_lxxiii_per_gen_identity_passes():
    verdict = pg.claim_per_gen_identity_verdict()
    assert verdict["passed"] is True
    assert verdict["worst_identity_error_bits"] <= 1e-9
    assert verdict["worst_atom_bits"] >= -1e-9
    assert verdict["worst_pooled_consistency_diff"] <= 1e-12


def test_claim_lxxiv_xor_climb_fails():
    # The climb is a pooling artifact: the per-generation
    # mean synergy at sigma = 1.00 stays ~1.0 on every
    # seed (bar 1.50), while the pooled values reach
    # 1.79-1.84.
    verdict = pg.claim_xor_climb_survives_verdict()
    assert verdict["passed"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["mean_syn_collab_sigma_1.00_bits"] == (
        pytest.approx(1.0933, abs=1e-3))
    assert by_seed[7]["mean_syn_collab_sigma_1.00_bits"] == (
        pytest.approx(0.9855, abs=1e-3))
    assert by_seed[1234]["mean_syn_collab_sigma_1.00_bits"] == (
        pytest.approx(1.0039, abs=1e-3))
    assert by_seed[2026]["mean_syn_collab_sigma_1.00_bits"] == (
        pytest.approx(0.9995, abs=1e-3))
    for r in verdict["per_seed"]:
        assert r["pooled_syn_collab_sigma_1.00_bits"] >= 1.79


def test_claim_lxxv_isolated_synergy_mixture_fails():
    # The mixture excess is 1.0755 / 1.0000 / 1.0755 on
    # seeds 42 / 7 / 1234 -- but only 0.4000 on held-out
    # seed 2026, below the 0.50 bar. The pooled isolated
    # synergy at sigma = 1.00 is much smaller there
    # (0.4000 vs 1.0000-1.0755 elsewhere).
    verdict = pg.claim_isolated_synergy_is_mixture_verdict()
    assert verdict["passed"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["mixture_excess_sigma_1.00_bits"] == (
        pytest.approx(1.0755, abs=1e-3))
    assert by_seed[7]["mixture_excess_sigma_1.00_bits"] == (
        pytest.approx(1.0000, abs=1e-3))
    assert by_seed[1234]["mixture_excess_sigma_1.00_bits"] == (
        pytest.approx(1.0755, abs=1e-3))
    assert by_seed[2026]["mixture_excess_sigma_1.00_bits"] == (
        pytest.approx(0.4000, abs=1e-3))
    assert by_seed[2026]["pooled_syn_isol_sigma_1.00_bits"] == (
        pytest.approx(0.4000, abs=1e-3))
    for r in verdict["per_seed"]:
        assert r["mean_syn_isol_sigma_1.00_bits"] == pytest.approx(
            0.0, abs=1e-9)


def test_claim_lxxvi_max_gap_dominant_per_gen_fails():
    # The pooled (lxx) synergy-majority does not survive
    # per-generation for MAX on any seed: shares
    # 0.383 / 0.332 / 0.350 / 0.445, all below 0.5,
    # although mean dSyn > mean dRed everywhere.
    verdict = pg.claim_max_gap_dominant_per_gen_verdict()
    assert verdict["passed"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["synergy_share_of_mean_gap"] == (
        pytest.approx(0.383, abs=1e-3))
    assert by_seed[7]["synergy_share_of_mean_gap"] == (
        pytest.approx(0.332, abs=1e-3))
    assert by_seed[1234]["synergy_share_of_mean_gap"] == (
        pytest.approx(0.350, abs=1e-3))
    assert by_seed[2026]["synergy_share_of_mean_gap"] == (
        pytest.approx(0.445, abs=1e-3))
    for r in verdict["per_seed"]:
        assert (r["mean_delta_synergistic_bits"]
                > r["mean_delta_redundant_bits"])


def test_claim_lxxvii_xor_gap_dominant_per_gen_passes():
    # Per-generation, the XOR gap at sigma = 0.25 IS
    # synergy-majority on every seed -- including 1234,
    # where the pooled gap was negative.
    verdict = pg.claim_xor_gap_dominant_per_gen_verdict()
    assert verdict["passed"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["synergy_share_of_mean_gap"] == (
        pytest.approx(0.566, abs=1e-3))
    assert by_seed[7]["synergy_share_of_mean_gap"] == (
        pytest.approx(0.541, abs=1e-3))
    assert by_seed[1234]["synergy_share_of_mean_gap"] == (
        pytest.approx(0.584, abs=1e-3))
    assert by_seed[2026]["synergy_share_of_mean_gap"] == (
        pytest.approx(0.655, abs=1e-3))
    for r in verdict["per_seed"]:
        assert (r["mean_delta_synergistic_bits"]
                > r["mean_delta_redundant_bits"])


def test_per_generation_pid_claims_aggregate():
    verdicts = pg.per_generation_pid_claims()
    assert verdicts["n_claims"] == 5
    # 2/5 pass: (lxxiii) identity/consistency and
    # (lxxvii) per-generation XOR gap pass; (lxxiv) the
    # climb, (lxxv) the mixture-excess bar on seed 2026,
    # and (lxxvi) the per-generation MAX gap fail honestly.
    assert verdicts["n_passed"] == 2
    assert verdicts["claim_lxxiii_per_gen_identity"]["passed"] is True
    assert verdicts["claim_lxxiv_xor_climb_survives"]["passed"] is False
    assert verdicts[
        "claim_lxxv_isolated_synergy_is_mixture"]["passed"] is False
    assert verdicts[
        "claim_lxxvi_max_gap_dominant_per_gen"]["passed"] is False
    assert verdicts[
        "claim_lxxvii_xor_gap_dominant_per_gen"]["passed"] is True
