# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for the seed-1234 diagnosis (v0.21.0, Job 2).

Every number pinned here was measured fresh by
seed_1234_diagnosis.py; the tests reproduce the
comparison numbers, so the diagnosis is re-derived
from the code on every run, not quoted from a doc.
Tolerances are 5e-4 on fractions/entropies and 1e-3
on the survey correlations, wider than the
floating-point noise of these deterministic seeded
computations.
"""

import numpy as np

import empathy_field as ef
import pid
import seed_1234_diagnosis as sd

TOL = 5e-4


def test_baseline_f_1234_is_nearly_double_the_others():
    """(a) Baseline f: 1234 = 0.3251 vs 0.1803 / 0.2469 / 0.1772."""
    f = {s: sd.baseline_field(s)["f_baseline"] for s in sd.FILE_SEEDS}
    assert abs(f[42] - 0.1803) < TOL
    assert abs(f[7] - 0.2469) < TOL
    assert abs(f[1234] - 0.3251) < TOL
    assert abs(f[2026] - 0.1772) < TOL
    assert f[1234] > 1.75 * f[42]
    assert f[1234] > 1.75 * f[2026]
    # Baseline R on 1234 matches seed 7, so R is not the outlier.
    assert abs(sd.baseline_field(1234)["mean_r"]
              - sd.baseline_field(7)["mean_r"]) < 0.001
    # Baseline count is highest on 1234 (20 vs 17 / 16 / 18).
    counts = {s: sd.baseline_field(s)["n_qualia"] for s in sd.FILE_SEEDS}
    assert counts == {42: 17, 7: 16, 1234: 20, 2026: 18}


def test_baseline_determinant_1234_is_mostly_negative():
    """The determinant distribution: 1234 mean -0.1556, 26/28 negative."""
    det = {s: sd.baseline_field(s) for s in sd.FILE_SEEDS}
    assert abs(det[1234]["det_mean"] - (-0.1556)) < TOL
    assert abs(det[1234]["det_median"] - (-0.1559)) < TOL
    assert det[1234]["n_det_negative"] == 26
    assert det[1234]["n_det_positive"] == 2
    assert abs(det[7]["det_mean"] - 0.1050) < TOL
    assert det[7]["n_det_negative"] == 5
    assert abs(det[42]["det_mean"] - (-0.0431)) < TOL
    assert abs(det[2026]["det_mean"] - 0.0101) < TOL
    # One agent is strongly peaked on 1234 (Born entropy 0.99 bits).
    assert min(sd.baseline_field(1234)["born_entropy_bits"]) < 1.0
    assert sd.baseline_field(1234)["d_min"] < 0.60


def test_pair_determinant_sign_rule():
    """The mechanism: det sign predicts the transform response.

    No positive-det pair ever falls under concern, and no
    negative-det pair ever falls under distress, on any
    file seed. On 1234, 21 of 26 negative-det pairs fall
    under concern (mean change -0.2084).
    """
    for seed in sd.FILE_SEEDS:
        p = sd.pair_transform_response(seed)
        assert p["frac_pos_det_fall_under_concern"] == 0.0
        assert p["frac_neg_det_fall_under_distress"] == 0.0
    p1234 = sd.pair_transform_response(1234)
    assert p1234["n_det_negative"] == 26
    assert abs(p1234["frac_neg_det_fall_under_concern"]
               - 21.0 / 26.0) < 1e-9
    assert abs(p1234["mean_delta_f_concern_neg_det"]
               - (-0.2084)) < TOL
    assert abs(p1234["mean_delta_f_distress_neg_det"]
               - 0.1627) < TOL
    # Seed 7 is the mirror image: only 5 negative-det pairs.
    assert sd.pair_transform_response(7)["n_det_negative"] == 5


def test_distress_only_sweep_is_the_mirror_image():
    """f(0, d) rises steeply on 1234, dips first on seed 7."""
    d1234 = {r["d"]: r["f"] for r in sd.distress_only_sweep(1234)}
    assert abs(d1234[0.0] - 0.3251) < TOL
    assert abs(d1234[0.5] - 0.5514) < TOL
    assert abs(d1234[1.0] - 0.5374) < TOL
    # Distress-heavy f on 1234 exceeds every other seed's.
    for seed in (42, 7, 2026):
        d = {r["d"]: r["f"] for r in sd.distress_only_sweep(seed)}
        assert d[1.0] < d1234[1.0]
    # Seed 7 dips first (positive-det seed).
    d7 = {r["d"]: r["f"] for r in sd.distress_only_sweep(7)}
    assert d7[0.25] < d7[0.0]


def test_two_channel_failures_sit_only_on_1234():
    """(l), (li), (liii) fail only on 1234; (lii) passes everywhere."""
    failures = sd.two_channel_failures()
    for seed in (42, 7, 2026):
        for name in ("l", "li", "lii", "liii"):
            assert failures[seed][name]["passed"], (seed, name)
    f1234 = failures[1234]
    assert not f1234["l"]["passed"]
    assert f1234["l"]["failed_checks"] == [
        "f_strictly_increasing_in_c", "count_at_c_half_is_ceiling"]
    assert f1234["l"]["count_at_c_half"] == 24
    assert f1234["l"]["f_concern"] == [0.3251, 0.1505, 0.2788, 0.5879]
    assert not f1234["li"]["passed"]
    assert f1234["li"]["failed_checks"] == [
        "count_non_increasing_in_d", "count_at_d1_at_most_max"]
    assert f1234["li"]["count_at_d1"] == 23
    assert f1234["li"]["counts"] == [24, 17, 14, 23]
    assert f1234["lii"]["passed"]
    assert f1234["lii"]["count_at_d2"] == 28
    assert not f1234["liii"]["passed"]
    assert f1234["liii"]["failed_checks"] == [
        "count_at_c_half_d1_at_most_max", "swap_f_diff_at_least_min"]
    assert abs(f1234["liii"]["swap_f_diff"] - 0.0504) < TOL
    assert abs(f1234["liii"]["f_distress_heavy"] - 0.5374) < TOL


def test_no_generation0_spike_on_1234():
    """Gen-0 coupling on 1234 is the LOWEST of the four seeds."""
    gen0 = {s: sd.gen0_conditions(s)["gen0_coupling_f"]
            for s in sd.FILE_SEEDS}
    assert abs(gen0[1234] - 0.3656) < TOL
    assert gen0[1234] == min(gen0.values())
    assert abs(gen0[42] - 0.5281) < TOL
    assert abs(gen0[7] - 0.4703) < TOL
    # The 1234 coupling trajectory is the flattest (max < 0.62).
    traj = sd.gen0_conditions(1234)["coupling_f"]
    assert max(traj) < 0.62
    assert abs(max(traj) - 0.609) < 0.01


def test_sigma0_is_identical_across_seeds():
    """At sigma = 0 the predictors are identical: no seed effect."""
    rows = sd.sigma0_identity()
    for key in ("mean_R", "mean_D", "max_D", "var_D",
                "post_R_sustained", "broadcast"):
        values = {rows[s][key] for s in sd.FILE_SEEDS}
        assert len(values) == 1, (key, values)
    assert abs(rows[42]["mean_R"] - 0.6221) < TOL
    assert abs(rows[42]["mean_D"] - 0.6274) < TOL


def test_cogitate_margin_1234_is_mean_d_not_mean_r():
    """(lx): r(mean_D) = 0.8839 beats r(mean_R) = 0.8447 on 1234."""
    c1234 = sd.cogitate_seed_table(1234)
    assert abs(c1234["correlations"]["mean_R"] - 0.8447) < TOL
    assert abs(c1234["correlations"]["mean_D"] - 0.8839) < TOL
    assert abs(c1234["lx_margin_mean_R_minus_mean_D"]
               - (-0.0393)) < TOL
    assert not c1234["lx_passes"]
    # The shape: mean_D peaks at sigma = 0.10 on 1234, at 0.0 elsewhere.
    assert c1234["sigma_of_max_mean_D"] == 0.1
    for seed in (42, 7, 2026):
        assert sd.cogitate_seed_table(seed)["sigma_of_max_mean_D"] == 0.0
    # mean_R on 1234 is unremarkable (inside the file-seed range).
    r_r = {s: sd.cogitate_seed_table(s)["correlations"]["mean_R"]
           for s in sd.FILE_SEEDS}
    assert min(r_r.values()) > 0.84 and max(r_r.values()) < 0.91
    # mean_D on 2026 is the worst predictor (0.3430): the shape varies.
    assert abs(sd.cogitate_seed_table(2026)["correlations"]["mean_D"]
               - 0.3430) < TOL


def test_isolated_switch_table_reproduces_pid_joint():
    """The switch table reconstructs pid's pooled isolated joint exactly."""
    for seed in sd.FILE_SEEDS:
        w = sd.isolated_switch_table(seed)
        row = pid.pair_arm_distributions(sigma=0.25, seed=seed)
        assert np.max(np.abs(w["joint"]
                             - row["isolated"]["joint"])) < 1e-12
    w = sd.isolated_switch_table(1234)
    assert w["concepts_agent0"] == [3, 3, 3, 3, 3, 3, 3, 3, 1, 1]
    assert w["concepts_agent1"] == [3, 3, 3, 3, 3, 1, 1, 2, 2, 2]
    assert w["n_joint_cells"] == 4
    assert w["joint_cells"] == [(1, 2, 0.2), (3, 1, 0.2),
                                (3, 2, 0.1), (3, 3, 0.5)]
    assert abs(w["xor_total_info_isolated_bits"] - 1.7610) < TOL
    assert abs(w["max_total_info_isolated_bits"] - 0.7219) < TOL
    # Calibration seeds have 2-3 cells, not 4.
    assert sd.isolated_switch_table(42)["n_joint_cells"] == 2
    assert sd.isolated_switch_table(7)["n_joint_cells"] == 3


def test_pid_arms_1234_squeezed_from_both_sides():
    """XOR: lowest I_collab AND highest I_isol on 1234; MAX clears."""
    arms = {s: sd.pid_arm_table(s) for s in sd.FILE_SEEDS}
    a = arms[1234]
    assert abs(a["xor_delta_info_bits"] - (-0.2591)) < TOL
    assert abs(a["xor_i_collaborating_bits"] - 1.5019) < TOL
    assert abs(a["xor_i_isolated_bits"] - 1.7610) < TOL
    assert a["xor_i_collaborating_bits"] == min(
        arms[s]["xor_i_collaborating_bits"] for s in sd.FILE_SEEDS)
    assert a["xor_i_isolated_bits"] == max(
        arms[s]["xor_i_isolated_bits"] for s in sd.FILE_SEEDS)
    # The collaborating pair is the most resonant pre-mix on 1234.
    assert abs(a["mean_r_pre"] - 0.526) < 0.005
    assert a["mean_r_pre"] == max(
        arms[s]["mean_r_pre"] for s in sd.FILE_SEEDS)
    assert a["collab_h_x1_bits"] < 1.30 and a["collab_h_x2_bits"] < 1.25
    # MAX clears 1234, narrowly, with the lowest collaborating info.
    assert abs(a["max_delta_info_bits"] - 0.3266) < TOL
    assert a["max_delta_info_bits"] > 0.0
    assert abs(a["max_i_collaborating_bits"] - 1.0485) < TOL
    assert a["max_i_collaborating_bits"] == min(
        arms[s]["max_i_collaborating_bits"] for s in sd.FILE_SEEDS)
    assert abs(a["max_i_isolated_bits"] - 0.7219) < TOL


def test_baseline_f_has_no_threshold_near_1234():
    """f(sigma) on 1234 is highest at every sigma in (0, 0.25]."""
    curves = {s: sd.baseline_f_vs_sigma(s) for s in sd.FILE_SEEDS}
    for k, sigma in enumerate(ef.SIGMA_GRID):
        if 0.0 < sigma <= 0.25:
            assert curves[1234][k] == max(
                curves[s][k] for s in sd.FILE_SEEDS)
    # At sigma = 0.50 and 1.00 seed 7 overtakes 1234 -- no
    # monotone "1234 is always highest" story, and no threshold.
    assert curves[7][5] > curves[1234][5]
    assert curves[7][6] > curves[1234][6]
    # No landmark sits near 0.3251: peak 0.1803, flip 0.7278.
    assert abs(curves[1234][4] - 0.3251) < TOL  # sigma = 0.25
    assert curves[1234][5] < 0.7278  # sigma = 0.50 still below f*


def test_survey_1234_is_extreme_but_statistics_uncorrelated():
    """12-seed survey: 1234 is extreme on all three, yet |r| < 0.5."""
    survey = sd.seed_survey()
    assert survey["seed_1234_max_baseline_f"]
    assert survey["seed_1234_min_xor_delta_info"]
    assert survey["seed_1234_min_lx_margin"]
    assert survey["seed_1234_min_max_delta_info"]
    assert abs(survey["pearson_f0_xor_delta_info"]
               - (-0.1236)) < 1e-3
    assert abs(survey["pearson_f0_lx_margin"]
               - (-0.2379)) < 1e-3
    assert abs(survey["pearson_xor_delta_info_lx_margin"]
               - (-0.2272)) < 1e-3
    for key in ("pearson_f0_xor_delta_info",
                "pearson_f0_lx_margin",
                "pearson_xor_delta_info_lx_margin"):
        assert abs(survey[key]) < 0.5
    # The survey reaches each extreme separately: seed 777 has
    # the largest XOR gap with a near-zero (lx) margin.
    by_seed = {r["seed"]: r for r in survey["rows"]}
    assert by_seed[777]["xor_delta_info_bits"] == max(
        r["xor_delta_info_bits"] for r in survey["rows"])
    assert abs(by_seed[777]["lx_margin"] - 0.0025) < TOL
    # (lx) is seed-fragile in general: seed 1 also fails the margin.
    assert by_seed[1]["lx_margin"] < 0.0
    assert abs(by_seed[1]["lx_margin"] - (-0.0206)) < TOL
    # (lx) is seed-fragile in general: the 0.10 margin fails
    # on 6 of the 12 survey seeds.
    failing = [r["seed"] for r in survey["rows"]
               if r["lx_margin"] < 0.10]
    assert failing == [1234, 1, 2, 777, 2024, 31337]
    negatives = [r["seed"] for r in survey["rows"]
                 if r["xor_delta_info_bits"] < 0.0]
    assert negatives == [1234]
    # MAX is positive on all 12 survey seeds.
    assert all(r["max_delta_info_bits"] > 0.0
               for r in survey["rows"])


def test_diagnose_verdict_is_independent_anomalies():
    """The full diagnosis returns the verdict with its evidence."""
    d = sd.diagnose()
    assert d["common_mechanism"] is False
    assert d["verdict"] == ("independent anomalies: "
                            "no common mechanism")
    ev = d["evidence"]
    assert ev["gen0_coupling_1234_lowest"] is True
    assert ev["f_1234_highest_at_every_sigma_0_to_0.25"] is True
    assert ev["survey_correlations_small"] is True
    assert ev["seed_1234_max_baseline_f"] is True
    assert ev["seed_1234_min_xor_delta_info"] is True
    assert ev["seed_1234_min_lx_margin"] is True
    assert ev["seed_1234_min_max_delta_info"] is True
