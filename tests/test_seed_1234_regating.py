# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for the seed-1234 design decisions (v0.24.0, claims
(lxxxii)-(lxxxvii)): re-gate the two-channel claims
(l)/(li)/(liii) on the baseline pair determinant-sign
distribution, and replace (lx)'s 0.10 margin with a pooled
rule.

Claim (lxxxvi) FAILS — the full re-gated claims do not hold
on all gated survey seeds (the gate rescues the
concurrence halves, not the quale-count halves). That
failure is asserted here, exactly as measured, with the
frozen thresholds unmoved. See
docs/preregistration-v0.24.0.md. The old verdicts stay on
the record: (l), (li), (liii) FAIL as originally stated,
and (lx) FAILS as originally stated.
"""

import pytest

import cogitate as cg
import seed_1234_regating as rg
import two_channel_empathy as tc


@pytest.fixture(scope="module")
def verdicts():
    return rg.regating_claims()


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

def test_gate_threshold_frozen():
    assert rg.GATE_DET_MEAN_MIN == -0.05
    assert rg.POOLED_MARGIN_MIN == 0.10
    t = rg._thresholds()
    assert t["gate_det_mean_min"] == -0.05
    assert t["pooled_margin_min"] == 0.10
    # The original v0.16.0 bars are reused unchanged.
    assert t["count_at_d1_max"] == 15
    assert t["r_rise_min"] == 0.04
    assert t["ceiling_count"] == 28
    assert t["f_star"] == 0.7278
    assert t["swap_f_diff_min"] == 0.30


def test_det_stats_known_values():
    expected = {
        42: (-0.0431, 18, True),
        7: (0.1050, 5, True),
        1234: (-0.1556, 26, False),
        2026: (0.0101, 12, True),
    }
    for seed, (det_mean, n_neg, gated_in) in expected.items():
        d = rg.det_stats(seed)
        assert d["det_mean"] == pytest.approx(det_mean, abs=1e-3)
        assert d["n_det_negative"] == n_neg
        assert d["n_pairs"] == 28
        assert d["gated_in"] is gated_in


def test_gate_admits_calibration_excludes_1234(verdicts):
    # The gate must admit both calibration seeds — otherwise
    # it would exclude the data the claims were frozen from.
    assert 42 in verdicts["gated_file_seeds"]
    assert 7 in verdicts["gated_file_seeds"]
    assert 1234 not in verdicts["gated_file_seeds"]
    assert verdicts["gated_file_seeds"] == [42, 7, 2026]
    assert verdicts["gated_survey_seeds"] == [
        42, 7, 2026, 1, 3, 99, 123, 31337]
    # The fraction-negative diagnostic agrees on 1234 but is
    # NOT the gate: it would admit seeds 777 and 2024.
    assert verdicts["det_stats"][777]["frac_det_negative"] == (
        pytest.approx(18 / 28))
    assert verdicts["det_stats"][777]["gated_in"] is False
    assert verdicts["det_stats"][2024]["gated_in"] is False
    assert verdicts["det_stats"][2]["gated_in"] is False


def test_sigma_zero_det_is_zero_gated_in():
    # At sigma = 0 the uniform thought has det = 0 exactly,
    # so every seed is gated in there — a degenerate gate
    # check, not a seed effect.
    for seed in (42, 1234):
        d = rg.det_stats(seed, sigma=0.0)
        assert d["det_mean"] == pytest.approx(0.0, abs=1e-12)
        assert d["gated_in"] is True


# ---------------------------------------------------------------------------
# Per-seed two-channel flags agree with the v0.16.0 verdicts
# ---------------------------------------------------------------------------

def test_per_seed_two_channel_agrees_with_v016_verdicts():
    # The per-seed recomputation must agree with the
    # original verdict functions on the file seeds.
    for seed in tc.ALL_SEEDS:
        per = rg.per_seed_two_channel(seed)
        vl = tc.claim_concern_verdict(seeds=(seed,))
        vli = tc.claim_distress_verdict(seeds=(seed,))
        vliii = tc.claim_separation_verdict(seeds=(seed,))
        row_l = vl["per_seed"][0]
        row_li = vli["per_seed"][0]
        row_liii = vliii["per_seed"][0]
        assert per["claim_l_pass"] == bool(
            row_l["r_strictly_increasing"]
            and row_l["f_strictly_increasing"]
            and row_l["count_at_c_half"] == 28)
        assert per["claim_li_pass"] == bool(
            row_li["r_strictly_increasing"]
            and row_li["count_non_increasing"]
            and row_li["count_at_d1"] <= 15
            and row_li["r_rise_d0_to_d1"] >= 0.04)
        assert per["claim_liii_pass"] == bool(
            row_liii["f_at_c2"] >= 0.7278
            and row_liii["count_at_c_half_d1"] <= 15
            and row_liii["swap_f_diff"] >= 0.30)


def test_per_seed_two_channel_file_seed_outcomes(verdicts):
    per = verdicts["per_seed_two_channel"]
    # The original failures sit on seed 1234 only.
    assert per[1234]["claim_l_pass"] is False
    assert per[1234]["claim_li_pass"] is False
    assert per[1234]["claim_liii_pass"] is False
    for seed in (42, 7, 2026):
        assert per[seed]["claim_l_pass"] is True
        assert per[seed]["claim_li_pass"] is True
        assert per[seed]["claim_liii_pass"] is True
    # The f-dip that breaks (l) on 1234, and the swap that
    # breaks (liii) there.
    assert per[1234]["f_concern"] == pytest.approx(
        [0.3251, 0.1505, 0.2788, 0.5879], abs=1e-3)
    assert per[1234]["swap_f_diff"] == pytest.approx(
        0.0504, abs=1e-3)


# ---------------------------------------------------------------------------
# (lxxxii)-(lxxxiv) Re-gated (l)/(li)/(liii) — PASS on gated file seeds
# ---------------------------------------------------------------------------

def test_claim_lxxxii_regated_concern_pass(verdicts):
    v = verdicts["claim_lxxxii_regated_concern"]
    assert v["passed"] is True
    assert v["gated_file_seeds"] == [42, 7, 2026]
    assert v["checks"]["seed_1234_excluded_by_gate"] is True
    for seed in (42, 7, 2026):
        assert v["per_seed"][seed]["claim_l_pass"] is True
        assert v["per_seed"][seed]["count_at_c_half"] == 28


def test_claim_lxxxiii_regated_distress_pass(verdicts):
    v = verdicts["claim_lxxxiii_regated_distress"]
    assert v["passed"] is True
    assert v["gated_file_seeds"] == [42, 7, 2026]
    expected_counts = {42: [28, 25, 19, 10], 7: [28, 28, 24, 14],
                       2026: [28, 25, 21, 9]}
    for seed, counts in expected_counts.items():
        assert v["per_seed"][seed]["claim_li_pass"] is True
        assert v["per_seed"][seed]["counts_distress"] == counts
        assert v["per_seed"][seed]["count_at_d1"] <= 15


def test_claim_lxxxiv_regated_separation_pass(verdicts):
    v = verdicts["claim_lxxxiv_regated_separation"]
    assert v["passed"] is True
    assert v["gated_file_seeds"] == [42, 7, 2026]
    expected_swap = {42: 0.4321, 7: 0.4283, 2026: 0.3140}
    for seed, swap in expected_swap.items():
        assert v["per_seed"][seed]["claim_liii_pass"] is True
        assert v["per_seed"][seed]["swap_f_diff"] == pytest.approx(
            swap, abs=1e-3)
        assert v["per_seed"][seed]["f_at_c2"] >= 0.7278


# ---------------------------------------------------------------------------
# (lxxxv) Determinant-sign-conditioned concurrence — PASS
# ---------------------------------------------------------------------------

def test_claim_lxxxv_sign_conditioned_concurrence_pass(verdicts):
    v = verdicts["claim_lxxxv_sign_conditioned_concurrence"]
    assert v["passed"] is True
    assert v["gated_survey_seeds"] == [
        42, 7, 2026, 1, 3, 99, 123, 31337]
    assert v["checks"][
        "concern_f_rises_on_every_gated_survey_seed"] is True
    assert v["checks"][
        "distress_f_non_increasing_on_every_gated_survey_seed"] \
        is True
    assert v["checks"][
        "no_positive_det_pair_falls_under_concern_on_any_seed"] \
        is True


def test_sign_rule_concern_half_exact_on_all_survey_seeds(verdicts):
    # No positive-det pair ever falls under concern, on any
    # of the 12 survey seeds — the exact half of the rule.
    for seed in rg.SURVEY_SEEDS:
        rule = verdicts["sign_rules"][seed]
        assert rule["frac_pos_det_fall_under_concern"] == 0.0
        # And the mean change has the predicted sign on
        # almost every seed: negative-det pairs fall,
        # positive-det pairs rise under concern.
        assert rule["mean_delta_f_concern_pos_det"] > 0.0
    # The distress half is NOT exact — reported, not gated.
    failing = {s: verdicts["sign_rules"][s][
        "frac_neg_det_fall_under_distress"]
        for s in rg.SURVEY_SEEDS
        if verdicts["sign_rules"][s][
            "frac_neg_det_fall_under_distress"] > 0.0}
    assert set(failing) == {1, 2, 777}
    assert failing[1] == pytest.approx(0.111, abs=1e-3)
    assert failing[777] == pytest.approx(0.278, abs=1e-3)


def test_excluded_seeds_fail_the_f_halves(verdicts):
    # The gate separates the f failures: the excluded seeds
    # (except seed 2) dip under concern and re-rise under
    # distress at fixed concern.
    per = verdicts["per_seed_two_channel"]
    for seed in (1234, 777, 2024):
        assert per[seed]["f_concern_strictly_increasing"] is False
        assert per[seed]["f_distress_non_increasing"] is False
    assert per[2]["f_concern_strictly_increasing"] is True
    assert per[2]["f_distress_non_increasing"] is True


# ---------------------------------------------------------------------------
# (lxxxvi) Full re-gated claims on gated survey seeds — FAIL
# ---------------------------------------------------------------------------

def test_claim_lxxxvi_survey_extension_fail(verdicts):
    v = verdicts["claim_lxxxvi_survey_extension"]
    assert v["passed"] is False
    assert v["n_gated_survey_seeds_passing_l"] == 4
    assert v["n_gated_survey_seeds_passing_li"] == 4
    assert v["n_gated_survey_seeds_passing_liii"] == 5
    # The count halves are what fail: count(c = 0.5) is
    # 24 / 25 / 26 / 27, not the 28 ceiling, on the gated
    # survey seeds that fail (l).
    failing_counts = {s: v["per_seed"][s]["count_at_c_half"]
                      for s in v["gated_survey_seeds"]
                      if not v["per_seed"][s]["claim_l_pass"]}
    assert failing_counts == {1: 24, 3: 25, 99: 26, 31337: 27}
    # And the swap fails on seed 3 by 0.0031 — the only
    # f-based sub-check to fail on a gated survey seed.
    assert v["per_seed"][3]["swap_f_diff"] == pytest.approx(
        0.2969, abs=1e-3)
    assert v["per_seed"][3]["claim_liii_pass"] is False
    # The gated file seeds still pass all three, inside the
    # extension table — the failure is a survey-seed effect.
    for seed in (42, 7, 2026):
        assert v["per_seed"][seed]["claim_l_pass"] is True
        assert v["per_seed"][seed]["claim_li_pass"] is True
        assert v["per_seed"][seed]["claim_liii_pass"] is True


# ---------------------------------------------------------------------------
# (lxxxvii) Pooled Cogitate rule — PASS
# ---------------------------------------------------------------------------

def test_pooled_correlations_identity(verdicts):
    pooled = verdicts["pooled_survey"]
    assert pooled["n_runs"] == 84  # 12 seeds x 7 sigma
    assert pooled["pooled_margin_mean_R_minus_mean_D"] == (
        pytest.approx(
            pooled["pooled"]["mean_R"]
            - pooled["pooled"]["mean_D"], abs=1e-12))
    assert pooled["pooled_top_predictor"] == "mean_R"


def test_claim_lxxxvii_pooled_cogitate_pass(verdicts):
    v = verdicts["claim_lxxxvii_pooled_cogitate"]
    assert v["passed"] is True
    assert v["n_runs"] == 84
    assert v["pooled"]["mean_R"] == pytest.approx(
        0.6658, abs=1e-3)
    assert v["pooled"]["mean_D"] == pytest.approx(
        0.2636, abs=1e-3)
    assert v["pooled_margin_mean_R_minus_mean_D"] == pytest.approx(
        0.4022, abs=1e-3)
    assert v["pooled_margin_mean_R_minus_mean_D"] >= 0.10
    # mean_R is the top-ranked pooled predictor (next: post).
    assert v["pooled"]["post"] == pytest.approx(
        0.5373, abs=1e-3)
    assert v["pooled"]["mean_R"] > v["pooled"]["post"]
    assert v["pooled_top_predictor"] == "mean_R"
    # Per-seed context, reported not gated: the per-seed
    # margin is fragile (median barely above the old bar).
    assert v["per_seed_margin_mean"] == pytest.approx(
        0.2312, abs=1e-3)
    assert v["per_seed_margin_median"] == pytest.approx(
        0.1084, abs=1e-3)
    assert v["n_per_seed_margins_positive"] == 10
    assert v["n_per_seed_margins_at_least_0.10"] == 6


def test_old_lx_still_fails_per_seed(verdicts):
    # The pooled rule does not erase the old verdict: a
    # per-seed 0.10 margin still fails on half the survey,
    # and (lx) itself is unchanged (see test_cogitate.py).
    v = verdicts["claim_lxxxvii_pooled_cogitate"]
    assert v["n_per_seed_margins_at_least_0.10"] == 6
    assert v["per_seed_margin_median"] < 0.11
    pooled = verdicts["pooled_survey"]
    assert pooled["per_seed"][1234]["lx_margin"] == pytest.approx(
        -0.0393, abs=1e-3)
    assert pooled["per_seed"][1]["lx_margin"] == pytest.approx(
        -0.0206, abs=1e-3)


# ---------------------------------------------------------------------------
# Fresh-seed diagnostic (reported, not gated)
# ---------------------------------------------------------------------------

def test_fresh_seed_diagnostic_reported_not_gated(verdicts):
    fresh = verdicts["fresh_seed_diagnostic"]
    assert fresh["seeds"] == [5, 11, 555, 4242]
    assert fresh["n_runs"] == 28
    # The pooled rule holds on fresh seeds too — but the
    # per-seed margins are wilder than on the survey.
    assert fresh["pooled_margin_mean_R_minus_mean_D"] == (
        pytest.approx(0.5270, abs=1e-3))
    assert fresh["pooled_top_predictor"] == "mean_R"
    assert fresh["pooled"]["mean_R"] == pytest.approx(
        0.5066, abs=1e-3)
    assert fresh["per_seed"][5]["lx_margin"] == pytest.approx(
        1.3257, abs=1e-3)
    assert fresh["per_seed"][11]["lx_margin"] == pytest.approx(
        -0.1963, abs=1e-3)
    assert fresh["per_seed"][555]["lx_margin"] == pytest.approx(
        0.5211, abs=1e-3)
    assert fresh["per_seed"][4242]["lx_margin"] == pytest.approx(
        -0.3788, abs=1e-3)
    # Two of four fresh seeds fail the old per-seed margin
    # outright — the per-seed framing is not rescued.
    assert sum(1 for v in fresh["per_seed"].values()
               if v["lx_margin"] > 0.0) == 2
    # The diagnostic changes no verdict: the claims dict
    # carries it separately.
    assert "fresh_seed_diagnostic" in verdicts
    assert verdicts["n_claims"] == 6


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def test_regating_claims_summary(verdicts):
    assert verdicts["n_claims"] == 6
    assert verdicts["n_passed"] == 5
    assert verdicts["all_pass"] is False
    assert verdicts["claim_lxxxii_regated_concern"]["passed"] is True
    assert verdicts["claim_lxxxiii_regated_distress"]["passed"] \
        is True
    assert verdicts["claim_lxxxiv_regated_separation"]["passed"] \
        is True
    assert verdicts[
        "claim_lxxxv_sign_conditioned_concurrence"]["passed"] \
        is True
    assert verdicts["claim_lxxxvi_survey_extension"]["passed"] \
        is False
    assert verdicts["claim_lxxxvii_pooled_cogitate"]["passed"] \
        is True


def test_main_output(capsys):
    rg.main()
    out = capsys.readouterr().out
    assert "(lxxxii)" in out and "PASS" in out
    assert "claims (lxxxii)-(lxxxvii): 5/6 pass" in out
    assert "gated file seeds: [42, 7, 2026]" in out
    assert "fresh-seed diagnostic [5, 11, 555, 4242]" in out
