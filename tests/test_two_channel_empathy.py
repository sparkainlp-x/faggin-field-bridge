# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for two-channel empathy (v0.16.0, claims (l)-(liii))."""

import numpy as np
import pytest

import empathy_field as ef
import self_knowing as sk
import thought_entanglement as te
import two_channel_empathy as tc


# ---------------------------------------------------------------------------
# Targets and transform
# ---------------------------------------------------------------------------

def test_concern_target_is_bell_phi_plus():
    target = tc.concern_target()
    assert te.concurrence_pure(target) == pytest.approx(1.0, abs=1e-12)
    assert sk.self_knowing_factor(target) == pytest.approx(
        2.0 / 3.0, abs=1e-12)


def test_distress_target_is_self_product_state():
    target = tc.distress_target()
    assert te.concurrence_pure(target) == pytest.approx(0.0, abs=1e-12)
    assert sk.self_knowing_factor(target) == pytest.approx(
        1.0 / 3.0, abs=1e-12)


def test_zero_doses_reproduce_baseline_field():
    for seed in (42, 7, 1234, 2026):
        states = tc.two_channel_field(0.0, 0.0, seed=seed)
        base = ef.resonance_population(0.25, 8, seed)
        for a, b in zip(states, base):
            assert np.max(np.abs(a - b)) <= 1e-12


def test_transformed_states_are_normalized():
    for c, d in ((0.5, 0.0), (0.0, 1.0), (0.5, 1.0), (2.0, 2.0)):
        for s in tc.two_channel_field(c, d, seed=42):
            assert np.linalg.norm(s) == pytest.approx(1.0, abs=1e-12)


def test_negative_doses_rejected():
    with pytest.raises(ValueError):
        tc.two_channel_field(-0.1, 0.0, seed=42)
    with pytest.raises(ValueError):
        tc.two_channel_field(0.0, -1.0, seed=42)


def test_field_summary_baseline_seed_42():
    row = tc.field_row(0.0, 0.0, seed=42)
    assert row["mean_r"] == pytest.approx(0.8520, abs=1e-3)
    assert row["mean_d"] == pytest.approx(0.9059, abs=1e-3)
    assert row["f_mean_pair_concurrence"] == pytest.approx(
        0.1803, abs=1e-3)
    assert row["n_qualia"] == 17
    assert row["n_pairs"] == 28
    assert row["h_joint_bits"] == pytest.approx(13.46, abs=1e-2)


# ---------------------------------------------------------------------------
# (l) Concern alone
# ---------------------------------------------------------------------------

def test_concern_sweep_seed_42():
    rows = tc.concern_sweep(42)
    assert [r["mean_r"] for r in rows] == pytest.approx(
        [0.8520, 0.8893, 0.9184, 0.9537], abs=1e-3)
    assert [r["f_mean_pair_concurrence"] for r in rows] == \
        pytest.approx([0.1803, 0.2253, 0.4207, 0.6680], abs=1e-3)
    assert [r["n_qualia"] for r in rows] == [17, 21, 28, 28]


def test_concern_sweep_seed_7():
    rows = tc.concern_sweep(7)
    assert [r["f_mean_pair_concurrence"] for r in rows] == \
        pytest.approx([0.2469, 0.4500, 0.6067, 0.7784], abs=1e-3)
    assert [r["n_qualia"] for r in rows] == [16, 28, 28, 28]


def test_concern_f_dips_on_seed_1234():
    # The held-out seed breaks the monotone-f half: adding a
    # small Bell dose first DILUTES the pair concurrence
    # (0.3251 -> 0.1505) before raising it.
    rows = tc.concern_sweep(1234)
    assert rows[0]["f_mean_pair_concurrence"] == pytest.approx(
        0.3251, abs=1e-3)
    assert rows[1]["f_mean_pair_concurrence"] == pytest.approx(
        0.1505, abs=1e-3)
    assert rows[1]["f_mean_pair_concurrence"] < \
        rows[0]["f_mean_pair_concurrence"]
    # And the count at c = 0.5 is 24 there, not the ceiling.
    assert rows[2]["n_qualia"] == 24
    # Mean R still rises strictly on that seed.
    rs = [r["mean_r"] for r in rows]
    assert all(rs[i + 1] > rs[i] for i in range(len(rs) - 1))


def test_claim_l_verdict_fail():
    verdict = tc.claim_concern_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["r_strictly_increasing_in_c"] is True
    assert verdict["checks"]["f_strictly_increasing_in_c"] is False
    assert verdict["checks"]["count_at_c_half_is_ceiling"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["count_at_c_half"] == 28
    assert by_seed[7]["count_at_c_half"] == 28
    assert by_seed[1234]["count_at_c_half"] == 24
    assert by_seed[2026]["count_at_c_half"] == 28
    assert by_seed[42]["f_strictly_increasing"] is True
    assert by_seed[1234]["f_strictly_increasing"] is False


# ---------------------------------------------------------------------------
# (li) Distress at fixed concern
# ---------------------------------------------------------------------------

def test_distress_sweep_seed_42():
    rows = tc.distress_sweep(42)
    assert [r["mean_r"] for r in rows] == pytest.approx(
        [0.9184, 0.9318, 0.9442, 0.9630], abs=1e-3)
    assert [r["n_qualia"] for r in rows] == [28, 25, 19, 10]
    assert [r["f_mean_pair_concurrence"] for r in rows] == \
        pytest.approx([0.4207, 0.2695, 0.1694, 0.0902], abs=1e-3)


def test_distress_sweep_seed_2026():
    rows = tc.distress_sweep(2026)
    assert [r["n_qualia"] for r in rows] == [28, 25, 21, 9]
    assert rows[-1]["mean_r"] - rows[0]["mean_r"] == pytest.approx(
        0.0573, abs=1e-3)


def test_distress_count_rebounds_on_seed_1234():
    # The held-out seed breaks the count half: the count
    # falls 24 -> 17 -> 14, then rebounds to 23 at d = 1.
    rows = tc.distress_sweep(1234)
    assert [r["n_qualia"] for r in rows] == [24, 17, 14, 23]
    # Mean R still rises strictly there.
    rs = [r["mean_r"] for r in rows]
    assert all(rs[i + 1] > rs[i] for i in range(len(rs) - 1))


def test_claim_li_verdict_fail():
    verdict = tc.claim_distress_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["r_strictly_increasing_in_d"] is True
    assert verdict["checks"]["count_non_increasing_in_d"] is False
    assert verdict["checks"]["count_at_d1_at_most_max"] is False
    assert verdict["checks"]["r_rise_at_least_min"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["count_at_d1"] == 10
    assert by_seed[7]["count_at_d1"] == 14
    assert by_seed[1234]["count_at_d1"] == 23
    assert by_seed[2026]["count_at_d1"] == 9
    assert by_seed[42]["r_rise_d0_to_d1"] == pytest.approx(
        0.0446, abs=1e-3)
    assert by_seed[7]["r_rise_d0_to_d1"] == pytest.approx(
        0.0849, abs=1e-3)


# ---------------------------------------------------------------------------
# (lii) High-dose withdrawal
# ---------------------------------------------------------------------------

def test_claim_lii_verdict_pass():
    verdict = tc.claim_withdrawal_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"]["d_falls_by_at_least_min"] is True
    assert verdict["checks"]["h_falls_by_at_least_min"] is True
    assert verdict["checks"]["r_rises"] is True
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["d_fall"] == pytest.approx(0.2673, abs=1e-3)
    assert by_seed[7]["d_fall"] == pytest.approx(0.0971, abs=1e-3)
    assert by_seed[1234]["d_fall"] == pytest.approx(
        0.2051, abs=1e-3)
    assert by_seed[2026]["d_fall"] == pytest.approx(
        0.1477, abs=1e-3)
    assert by_seed[42]["h_fall_bits"] == pytest.approx(
        6.92, abs=1e-2)
    assert by_seed[7]["h_fall_bits"] == pytest.approx(
        3.22, abs=1e-2)
    assert by_seed[1234]["h_fall_bits"] == pytest.approx(
        5.58, abs=1e-2)
    assert by_seed[2026]["h_fall_bits"] == pytest.approx(
        4.37, abs=1e-2)
    # The count at d = 2 is reported, not gated: it rebounds
    # on the held-out seeds (28 on seed 1234).
    assert by_seed[42]["count_at_d2"] == 10
    assert by_seed[7]["count_at_d2"] == 17
    assert by_seed[1234]["count_at_d2"] == 28
    assert by_seed[2026]["count_at_d2"] == 24


# ---------------------------------------------------------------------------
# (liii) Channel separation
# ---------------------------------------------------------------------------

def test_concern_alone_reaches_f_star_every_seed():
    for seed in (42, 7, 1234, 2026):
        f = tc.field_row(2.0, 0.0, seed=seed)[
            "f_mean_pair_concurrence"]
        assert f >= tc.F_STAR
    assert tc.field_row(2.0, 0.0, seed=42)[
        "f_mean_pair_concurrence"] == pytest.approx(0.8578, abs=1e-3)
    assert tc.field_row(2.0, 0.0, seed=1234)[
        "f_mean_pair_concurrence"] == pytest.approx(0.8269, abs=1e-3)


def test_swap_f_diff_near_zero_on_seed_1234():
    # On seed 1234 the channels ARE near-interchangeable in f:
    # concern-heavy 0.5879 vs distress-heavy 0.5374.
    verdict = tc.claim_separation_verdict()
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["swap_f_diff"] == pytest.approx(
        0.4321, abs=1e-3)
    assert by_seed[7]["swap_f_diff"] == pytest.approx(
        0.4283, abs=1e-3)
    assert by_seed[1234]["swap_f_diff"] == pytest.approx(
        0.0504, abs=1e-3)
    assert by_seed[2026]["swap_f_diff"] == pytest.approx(
        0.3140, abs=1e-3)


def test_joint_search_finds_no_point():
    # No (c, d) point carries both f >= f* and count <= 15,
    # on any seed: the single-point form of "fits both"
    # fails in this wiring.
    for seed in (42, 7, 1234, 2026):
        assert tc.joint_search(seed)["n_hits"] == 0


def test_claim_liii_verdict_fail():
    verdict = tc.claim_separation_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"][
        "concern_alone_reaches_f_star"] is True
    assert verdict["checks"][
        "count_at_c_half_d1_at_most_max"] is False
    assert verdict["checks"]["swap_f_diff_at_least_min"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[1234]["count_at_c_half_d1"] == 23
    assert by_seed[2026]["count_at_c_half_d1"] == 9


# ---------------------------------------------------------------------------
# Aggregate, thresholds, main
# ---------------------------------------------------------------------------

def test_two_channel_claims_aggregate():
    verdicts = tc.two_channel_claims()
    assert verdicts["n_claims"] == 4
    assert verdicts["n_passed"] == 1
    assert verdicts["all_pass"] is False
    assert verdicts["headline_allowed"] is False


def test_thresholds_set():
    thresholds = tc._thresholds()
    assert thresholds["sigma_ref"] == pytest.approx(0.25)
    assert thresholds["ceiling_count"] == 28
    assert thresholds["count_at_d1_max"] == 15
    assert thresholds["r_rise_min"] == pytest.approx(0.04)
    assert thresholds["d_fall_min"] == pytest.approx(0.05)
    assert thresholds["h_fall_min_bits"] == pytest.approx(2.0)
    assert thresholds["f_star"] == pytest.approx(0.7278)
    assert thresholds["swap_f_diff_min"] == pytest.approx(0.30)


def test_main_runs(capsys):
    tc.main()
    out = capsys.readouterr().out
    assert "1/4 claims passed" in out
    assert "claim (l) verdict: FAIL" in out
    assert "claim (li) verdict: FAIL" in out
    assert "claim (lii) verdict: PASS" in out
    assert "claim (liii) verdict: FAIL" in out
