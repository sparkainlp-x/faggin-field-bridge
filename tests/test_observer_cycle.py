# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for observer_cycle.py: the observer cycle (v0.12.0)."""

import math

import numpy as np
import pytest

import observer_cycle as oc


def test_stored_thought_exact_values():
    psi = oc.stored_thought()
    assert oc.sk.self_knowing_factor(psi) == pytest.approx(1.0, abs=1e-9)
    assert oc.te.concurrence_pure(psi) == pytest.approx(0.0, abs=1e-9)


def test_kernel_thought_exact_values():
    psi = oc.kernel_thought()
    assert oc.sk.self_knowing_factor(psi) == pytest.approx(0.0, abs=1e-9)
    assert oc.te.concurrence_pure(psi) == pytest.approx(1.0, abs=1e-9)


def test_generalized_bell_endpoints():
    psi_one = oc.generalized_bell(1.0)
    assert oc.te.concurrence_pure(psi_one) == pytest.approx(0.0, abs=1e-9)
    assert oc.sk.self_knowing_factor(psi_one) == pytest.approx(
        1.0, abs=1e-9)
    psi_half = oc.generalized_bell(1.0 / math.sqrt(2.0))
    assert oc.te.concurrence_pure(psi_half) == pytest.approx(
        1.0, abs=1e-9)
    assert oc.sk.self_knowing_factor(psi_half) == pytest.approx(
        2.0 / 3.0, abs=1e-9)


def test_generalized_bell_rejects_out_of_range():
    with pytest.raises(ValueError):
        oc.generalized_bell(1.5)
    with pytest.raises(ValueError):
        oc.generalized_bell(-0.1)


def test_slide_endpoints_are_the_two_patterns():
    assert np.allclose(oc.slide_state(0.0), oc.stored_thought())
    assert np.allclose(oc.slide_state(math.pi / 2), oc.kernel_thought())
    mid = oc.slide_state(math.pi / 4)
    expected = (oc.stored_thought() + oc.kernel_thought()) / math.sqrt(2.0)
    assert np.allclose(mid, expected)


def test_slide_state_is_normalized():
    for theta in oc.SLIDE_THETAS:
        assert float(np.linalg.norm(oc.slide_state(theta))) == pytest.approx(
            1.0, abs=1e-9)


def test_observer_direction_calibration_seeds():
    # Calibration seeds (42, 7): the numbers the thresholds
    # were frozen from. Held-out seeds are covered by the
    # verdict test below, which expects the honest FAIL.
    by_seed = {r["seed"]: r
               for r in (oc.observer_direction_sweep(s)
                         for s in oc.CALIBRATION_SEEDS)}
    assert by_seed[42]["pearson_d_c"] == pytest.approx(-0.9570, abs=1e-4)
    assert by_seed[42]["spearman_d_c"] == pytest.approx(-1.0, abs=1e-9)
    assert by_seed[7]["pearson_d_c"] == pytest.approx(-0.9397, abs=1e-4)
    assert by_seed[7]["spearman_d_c"] == pytest.approx(-0.9643, abs=1e-4)
    for r in by_seed.values():
        assert r["d_range"] >= 0.25
        assert r["c_range"] >= 0.25


def test_observer_direction_held_out_seed_2026_pearson():
    # The honest failure: on held-out seed 2026 the linear
    # anti-tracking is -0.8828, above the frozen bar -0.90.
    # The monotone (Spearman) tracking still holds. The
    # threshold is NOT moved to force a pass.
    r = oc.observer_direction_sweep(2026)
    assert r["pearson_d_c"] == pytest.approx(-0.8828, abs=1e-4)
    assert r["pearson_d_c"] > oc.PEARSON_D_C_MAX
    assert r["spearman_d_c"] == pytest.approx(-0.9643, abs=1e-4)
    assert r["spearman_d_c"] <= oc.SPEARMAN_D_C_MAX


def test_claim_xxxii_verdict_is_fail():
    verdict = oc.claim_observer_direction_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["pearson_at_most_max"] is False
    assert verdict["checks"]["spearman_at_most_max"] is True
    assert verdict["checks"]["d_range_at_least_min"] is True
    assert verdict["checks"]["c_range_at_least_min"] is True
    assert len(verdict["per_seed"]) == 4


def test_robust_rank_fresh_seeds():
    # Fresh seeds 5 and 99 (never evaluated before
    # preregistration-v0.12.1.md): the prospective test
    # of claim (xxxv). Seed 5 breaks the Spearman bar
    # (-0.8929 > -0.90); seed 99 breaks the D-range bar
    # (0.2445 < 0.25). Both are 5-copy sampling draws:
    # at n = 200 seed 5 Spearman is -0.9643 and seed 99
    # D range is 0.4101. The bars are NOT moved.
    by_seed = {r["seed"]: r
               for r in (oc.observer_direction_sweep(s)
                         for s in oc.FRESH_SEEDS_XXXV)}
    assert by_seed[5]["spearman_d_c"] == pytest.approx(-0.8929, abs=1e-4)
    assert by_seed[5]["pearson_d_c"] == pytest.approx(-0.6814, abs=1e-4)
    assert by_seed[5]["d_range"] == pytest.approx(0.5748, abs=1e-4)
    assert by_seed[5]["c_range"] == pytest.approx(0.5202, abs=1e-4)
    assert by_seed[99]["spearman_d_c"] == pytest.approx(-1.0, abs=1e-9)
    assert by_seed[99]["d_range"] == pytest.approx(0.2445, abs=1e-4)
    assert by_seed[99]["d_range"] < oc.D_RANGE_MIN
    assert by_seed[99]["c_range"] == pytest.approx(0.5405, abs=1e-4)


def test_claim_xxxv_verdict_is_fail():
    verdict = oc.claim_robust_rank_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["spearman_at_most_max"] is False
    assert verdict["checks"]["d_range_at_least_min"] is False
    assert verdict["checks"]["c_range_at_least_min"] is True
    assert len(verdict["per_seed"]) == 6
    fresh = {r["seed"]: r for r in verdict["per_seed"]}
    assert fresh[5]["spearman_d_c"] > oc.SPEARMAN_XXXV_MAX
    assert fresh[99]["d_range"] < oc.D_RANGE_MIN


def test_diagnosis_sigma_one_break_seed_2026():
    # The (xxxii) diagnosis, recomputed in code: at
    # n = 200 the sigma = 1.0 dip vanishes and Pearson
    # passes on every seed; excluding the boundary
    # point, Pearson passes at n = 5; the 5-copy mean
    # at sigma = 1.0 carries SEM ~0.02 at n = 200
    # (~0.13 at n = 5) while the true C rise from
    # sigma = 0.5 to 1.0 is ~0.003.
    d = oc.diagnose_sigma_one_break(2026)
    assert d["n200_pearson"] == pytest.approx(-0.9053, abs=1e-4)
    assert d["n200_spearman"] == pytest.approx(-1.0, abs=1e-9)
    assert d["pearson_excl_sigma_one"] == pytest.approx(-0.9433, abs=1e-4)
    assert d["c_rise_05_to_10_n200"] == pytest.approx(0.0027, abs=1e-4)
    assert d["sem_concurrence"][1.0] == pytest.approx(0.0203, abs=1e-4)
    ext = d["extended_rows"]
    assert ext[-1]["sigma"] == pytest.approx(3.0, abs=1e-9)
    assert ext[-1]["mean_D"] == pytest.approx(0.5247, abs=1e-4)
    assert ext[-1]["mean_concurrence"] == pytest.approx(0.5192, abs=1e-4)


def test_diagnosis_fresh_seeds_n200():
    # Fresh seeds at n = 200: the monotone direction
    # holds (Spearman -0.9643 / -1.0000) but the
    # linear form stays fragile — seed 5 Pearson is
    # -0.8971 even at n = 200, above the -0.90 bar,
    # because C plateaus while D keeps falling.
    d5 = oc.diagnose_sigma_one_break(5)
    assert d5["n200_pearson"] == pytest.approx(-0.8971, abs=1e-4)
    assert d5["n200_spearman"] == pytest.approx(-0.9643, abs=1e-4)
    assert d5["n200_pearson"] > oc.PEARSON_D_C_MAX
    d99 = oc.diagnose_sigma_one_break(99)
    assert d99["n200_pearson"] == pytest.approx(-0.9364, abs=1e-4)
    assert d99["n200_spearman"] == pytest.approx(-1.0, abs=1e-9)


def test_bell_branch_rows():
    branch = oc.bell_branch_sweep()
    rows = branch["rows"]
    assert len(rows) == len(oc.BELL_BRANCH_GRID)
    assert rows[0]["resonance"] == pytest.approx(0.5, abs=1e-9)
    assert rows[0]["concurrence"] == pytest.approx(0.0, abs=1e-9)
    assert rows[0]["d"] == pytest.approx(1.0, abs=1e-9)
    assert rows[-1]["resonance"] == pytest.approx(1.0, abs=1e-9)
    assert rows[-1]["concurrence"] == pytest.approx(1.0, abs=1e-9)
    assert rows[-1]["d"] == pytest.approx(2.0 / 3.0, abs=1e-9)
    # R, C rise and D falls monotonically along the branch.
    rs = [r["resonance"] for r in rows]
    cs = [r["concurrence"] for r in rows]
    ds = [r["d"] for r in rows]
    assert all(b >= a for a, b in zip(rs, rs[1:]))
    assert all(b >= a for a, b in zip(cs, cs[1:]))
    assert all(b <= a for a, b in zip(ds, ds[1:]))


def test_bell_branch_correlations():
    branch = oc.bell_branch_sweep()
    assert branch["pearson_r_c"] == pytest.approx(1.0, abs=1e-4)
    assert branch["spearman_r_d"] == pytest.approx(-1.0, abs=1e-9)
    # Pearson(R, D) is weaker than the monotone one: R
    # saturates near 1 while D keeps falling. Reported,
    # not gated.
    assert branch["pearson_r_d"] == pytest.approx(-0.8801, abs=1e-4)
    assert branch["r_range"] == pytest.approx(0.5, abs=1e-9)
    assert branch["d_range"] == pytest.approx(1.0 / 3.0, abs=1e-9)


def test_noise_axis_control_inverts():
    # The control: on the noise axis the relation inverts
    # (noise creates concurrence while destroying overlap).
    control = oc.noise_axis_control()
    assert control["n_pairs"] == 196
    assert control["pearson_r_nu"] == pytest.approx(-0.5528, abs=1e-4)
    assert control["pearson_r_d_pair"] == pytest.approx(0.7694, abs=1e-4)
    assert control["pearson_r_nu"] < 0.0
    assert control["pearson_r_d_pair"] > 0.0


def test_claim_xxxiii_verdict_is_pass():
    verdict = oc.claim_knowing_overlap_verdict()
    assert verdict["passed"] is True
    assert all(verdict["checks"].values())
    assert verdict["pearson_r_c"] >= oc.PEARSON_R_C_MIN
    assert verdict["spearman_r_d"] <= oc.SPEARMAN_R_D_MAX


def test_slide_identities_exact():
    rows = oc.slide_sweep()
    for r in rows:
        assert r["d"] == pytest.approx(r["d_exact"], abs=1e-9)
        assert r["concurrence"] == pytest.approx(r["c_exact"], abs=1e-9)
        assert r["r_stored"] == pytest.approx(r["r_s_exact"], abs=1e-9)
        assert r["r_kernel"] == pytest.approx(r["r_k_exact"], abs=1e-9)
        assert r["c_plus_d"] == pytest.approx(1.0, abs=1e-9)
        assert r["r_split"] == pytest.approx(r["split_exact"], abs=1e-9)


def test_slide_endpoints():
    rows = oc.slide_sweep()
    first, last = rows[0], rows[-1]
    assert first["d"] == pytest.approx(1.0, abs=1e-9)
    assert first["concurrence"] == pytest.approx(0.0, abs=1e-9)
    assert first["r_stored"] == pytest.approx(1.0, abs=1e-9)
    assert first["r_kernel"] == pytest.approx(0.0, abs=1e-9)
    assert last["d"] == pytest.approx(0.0, abs=1e-9)
    assert last["concurrence"] == pytest.approx(1.0, abs=1e-9)
    assert last["r_stored"] == pytest.approx(0.0, abs=1e-9)
    assert last["r_kernel"] == pytest.approx(1.0, abs=1e-9)


def test_slide_split_flips_at_midpoint():
    rows = oc.slide_sweep()
    before = [r for r in rows if r["theta"] < oc.SLIDE_MIDPOINT - 1e-9]
    at = [r for r in rows
          if abs(r["theta"] - oc.SLIDE_MIDPOINT) <= 1e-9]
    after = [r for r in rows if r["theta"] > oc.SLIDE_MIDPOINT + 1e-9]
    assert len(before) == 3 and len(at) == 1 and len(after) == 3
    assert all(r["r_split"] >= 0.25 for r in before)
    assert all(abs(r["r_split"]) <= 1e-9 for r in at)
    assert all(r["r_split"] <= -0.25 for r in after)
    # The midpoint is the equal superposition: D = C = 1/2,
    # both overlaps 1/2, maximally undecided.
    assert at[0]["d"] == pytest.approx(0.5, abs=1e-9)
    assert at[0]["concurrence"] == pytest.approx(0.5, abs=1e-9)
    assert at[0]["r_stored"] == pytest.approx(0.5, abs=1e-9)
    assert at[0]["r_kernel"] == pytest.approx(0.5, abs=1e-9)


def test_claim_xxxiv_verdict_is_pass():
    verdict = oc.claim_slide_verdict()
    assert verdict["passed"] is True
    assert all(verdict["checks"].values())
    assert verdict["max_identity_error"] <= 1e-9


def test_observer_cycle_aggregate():
    claims = oc.observer_cycle_claims()
    assert claims["n_claims"] == 4
    assert claims["n_passed"] == 2
    assert claims["all_pass"] is False
    assert claims["headline_allowed"] is False
    assert claims["claim_xxxii_observer_direction"]["passed"] is False
    assert claims["claim_xxxiii_knowing_overlap"]["passed"] is True
    assert claims["claim_xxxiv_slide"]["passed"] is True
    assert claims["claim_xxxv_robust_rank"]["passed"] is False


def test_thresholds_frozen():
    t = oc._thresholds()
    assert t["pearson_d_c_max"] == -0.90
    assert t["spearman_d_c_max"] == -0.90
    assert t["spearman_xxxv_max"] == -0.90
    assert t["d_range_min"] == 0.25
    assert t["c_range_min"] == 0.25
    assert t["pearson_r_c_min"] == 0.99
    assert t["spearman_r_d_max"] == -0.95
    assert t["r_range_min"] == 0.25
    assert t["d_branch_range_min"] == 0.25
    assert t["exact_tol"] == 1e-9
    assert t["split_margin_min"] == 0.25
