# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for the Cogitate-style preregistration + process
predictors of the collaboration gap (v0.19.0, claims
(lx)-(lxiii)).

Claim (lx) FAILS on the held-out seed 1234 (mean_D
beats mean_R there) — that failure is asserted here,
exactly as measured, with the frozen threshold
unmoved. See docs/preregistration-v0.19.0.md.
"""

import pytest

import cogitate as cg
import empathy_field as ef
import thought_entanglement as te


# ---------------------------------------------------------------------------
# Machinery: additive rows, predictors, Pearson
# ---------------------------------------------------------------------------

def test_run_collaboration_rows_carry_process_keys():
    result = ef.run_collaboration(design="B", n_agents=4, sigma=0.25,
                                  generations=10, n_samples=200, seed=42)
    for arm in ("collaborating", "isolated"):
        rows = result[arm]["rows"]
        assert len(rows) == 10
        for row in rows:
            assert len(row["d_per_agent"]) == 4
            assert all(0.0 <= d <= 1.0 for d in row["d_per_agent"])
            assert 0.0 <= row["r_mean"] <= 1.0
            assert 0.0 <= row["r_posterior_mean"] <= 1.0
        # Pre-existing keys are untouched.
        assert all("h_joint_bits" in row and "coupling_f" in row
                   for row in rows)


def test_gap_reproduces_before_predictors():
    # The known gap, unchanged by the additive rows.
    result = ef.run_collaboration(design="B", n_agents=4, sigma=0.25,
                                  generations=10, n_samples=200, seed=42)
    assert result["gap_bits"] == pytest.approx(4.3352, abs=1e-3)


def test_sigma_zero_population_is_pair_symmetric():
    # At sigma = 0 the four base agents are pairwise
    # symmetric, so the posterior pair's R equals the
    # mean R in every generation (collaborating arm).
    result = ef.run_collaboration(design="B", n_agents=4, sigma=0.0,
                                  generations=10, n_samples=200, seed=42)
    for row in result["collaborating"]["rows"]:
        assert row["r_posterior_mean"] == pytest.approx(row["r_mean"])


def test_run_predictors_known_values():
    run = cg.run_predictors(0.25, 42)
    assert run["gap_bits"] == pytest.approx(4.3352, abs=1e-3)
    assert run["mean_R"] == pytest.approx(0.5517, abs=1e-3)
    assert run["mean_D"] == pytest.approx(0.5922, abs=1e-3)
    assert run["max_D"] == pytest.approx(0.9734, abs=1e-3)
    assert run["var_D"] == pytest.approx(0.056073, abs=1e-5)
    assert run["neg_var_D"] == pytest.approx(-run["var_D"])
    assert run["post_R_sustained"] == pytest.approx(0.5202, abs=1e-3)
    assert run["post_R_min"] == pytest.approx(0.0005, abs=1e-3)
    assert run["broadcast"] == pytest.approx(0.1353, abs=1e-3)
    assert run["onset_R"] == pytest.approx(0.1353, abs=1e-3)
    assert run["offset_R"] == pytest.approx(0.9202, abs=1e-3)


def test_seed_sweep_covers_sigma_grid():
    assert te.SIGMA_GRID == [0.0, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0]
    runs = cg.seed_sweep(42)
    assert len(runs) == 7
    assert [r["sigma"] for r in runs] == te.SIGMA_GRID
    assert all(r["seed"] == 42 for r in runs)


def test_pearson_known_and_degenerate():
    assert cg.pearson([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)
    assert cg.pearson([1, 2, 3], [3, 2, 1]) == pytest.approx(-1.0)
    assert cg.pearson([1, 1, 1], [1, 2, 3]) is None
    assert cg.pearson([1, 2, 3], [2, 2, 2]) is None
    assert cg.pearson([1], [1]) is None


def test_per_seed_correlations_calibration():
    corrs = cg.per_seed_correlations(cg.seed_sweep(42))
    assert corrs["mean_R"] == pytest.approx(0.9028, abs=1e-3)
    assert corrs["mean_D"] == pytest.approx(0.7776, abs=1e-3)
    assert corrs["max_D"] == pytest.approx(-0.8070, abs=1e-3)
    assert corrs["neg_var_D"] == pytest.approx(0.7899, abs=1e-3)
    assert corrs["post"] == pytest.approx(0.9278, abs=1e-3)
    assert corrs["broadcast"] == pytest.approx(-0.9022, abs=1e-3)


# ---------------------------------------------------------------------------
# (lx) Mean sensitivity beats individual D — FAILS (seed 1234)
# ---------------------------------------------------------------------------

def test_claim_lx_verdict_fail():
    verdict = cg.evaluate_claims()
    assert verdict["lx"]["pass"] is False
    per_seed = verdict["lx"]["per_seed"]
    # The failing sub-check: on seed 1234 mean_D beats mean_R.
    assert per_seed[1234]["pass"] is False
    ok, detail = per_seed[1234]["checks"]["mean_D"]
    assert ok is False
    assert "mean_R - mean_D = -0.0393" in detail
    # The max_D half passes on every seed.
    for seed in cg.ALL_SEEDS:
        assert per_seed[seed]["checks"]["max_D"][0] is True
    assert per_seed[42]["checks"]["mean_D"][1].startswith(
        "mean_R - mean_D = 0.1252")
    assert per_seed[7]["checks"]["mean_D"][1].startswith(
        "mean_R - mean_D = 0.2017")
    assert per_seed[2026]["checks"]["mean_D"][1].startswith(
        "mean_R - mean_D = 0.4992")


def test_claim_lx_held_out_correlations():
    verdict = cg.evaluate_claims()
    corrs = verdict["correlations"]
    assert corrs[1234]["mean_R"] == pytest.approx(0.8447, abs=1e-3)
    assert corrs[1234]["mean_D"] == pytest.approx(0.8839, abs=1e-3)
    assert corrs[2026]["mean_R"] == pytest.approx(0.8422, abs=1e-3)
    assert corrs[2026]["mean_D"] == pytest.approx(0.3430, abs=1e-3)


# ---------------------------------------------------------------------------
# (lxi) Turn-taking equality predicts the gap — PASS
# ---------------------------------------------------------------------------

def test_claim_lxi_verdict_pass():
    verdict = cg.evaluate_claims()
    assert verdict["lxi"]["pass"] is True
    expected = {42: 0.7899, 7: 0.7566, 1234: 0.7589, 2026: 0.7105}
    for seed, value in expected.items():
        per = verdict["lxi"]["per_seed"][seed]
        assert per["pass"] is True
        assert per["bar"][0] is True
        assert "r(gap, -var_D) = %.4f" % value in per["bar"][1]
        assert per["beats_max_D"][0] is True


# ---------------------------------------------------------------------------
# (lxii) Posterior vs broadcast — PASS, posterior wins
# ---------------------------------------------------------------------------

def test_claim_lxii_verdict_pass():
    verdict = cg.evaluate_claims()
    assert verdict["lxii"]["pass"] is True
    expected_post = {42: 0.9278, 7: 0.8657, 1234: 0.9858, 2026: 0.8884}
    expected_bcast = {42: -0.9022, 7: -0.8911, 1234: -0.7813,
                      2026: -0.9350}
    expected_sep = {42: 1.8300, 7: 1.7568, 1234: 1.7671, 2026: 1.8234}
    for seed in cg.ALL_SEEDS:
        per = verdict["lxii"]["per_seed"][seed]
        assert per["pass"] is True
        assert per["winner"] == "posterior"
        assert per["best"][0] is True
        assert ("max(r) = %.4f (posterior" % expected_post[seed]
                in per["best"][1])
        assert per["separation"][0] is True
        assert ("|r(post) - r(bcast)| = %.4f" % expected_sep[seed]
                in per["separation"][1])
    corrs = verdict["correlations"]
    for seed, value in expected_bcast.items():
        assert corrs[seed]["broadcast"] == pytest.approx(value, abs=1e-3)


def test_broadcast_anti_predicts_on_every_seed():
    # Broadcast (ignition at both ends) anti-predicts the
    # gap on all four seeds: onset R rises with sigma
    # while the gap falls. Reported, not hidden.
    verdict = cg.evaluate_claims()
    for seed in cg.ALL_SEEDS:
        assert verdict["correlations"][seed]["broadcast"] < -0.75


# ---------------------------------------------------------------------------
# (lxiii) Pooled regression — PASS over 28 runs
# ---------------------------------------------------------------------------

def test_claim_lxiii_verdict_pass():
    verdict = cg.evaluate_claims()
    lxiii = verdict["lxiii"]
    assert lxiii["pass"] is True
    assert lxiii["n_runs"] == 28  # 7 sigma x 4 seeds, not 20
    assert lxiii["r2_two"] == pytest.approx(0.6505, abs=1e-3)
    assert lxiii["r2_one"] == pytest.approx(0.3298, abs=1e-3)
    assert lxiii["difference"] == pytest.approx(0.3207, abs=1e-3)
    assert lxiii["difference"] >= cg.MARGIN_LXIII
    # The adjusted-R^2 diagnostic agrees: the two-predictor
    # lead is not an extra-parameter artefact.
    assert lxiii["adj_difference"] == pytest.approx(0.3185, abs=1e-3)
    assert lxiii["adj_difference"] > 0.0


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def test_evaluate_claims_summary():
    verdict = cg.evaluate_claims()
    passed = sum(1 for key in ("lx", "lxi", "lxii", "lxiii")
                 if verdict[key]["pass"])
    assert passed == 3
    assert verdict["lx"]["pass"] is False
    assert verdict["lxi"]["pass"] is True
    assert verdict["lxii"]["pass"] is True
    assert verdict["lxiii"]["pass"] is True


def test_main_output(capsys):
    cg.main()
    out = capsys.readouterr().out
    assert "(lx) FAIL" in out
    assert "(lxi) PASS" in out
    assert "(lxii) PASS" in out
    assert "(lxiii) PASS" in out
