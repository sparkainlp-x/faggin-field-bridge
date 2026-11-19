# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for the GRT phase-transition test
(v0.18.0, claims (lvii)-(lix))."""

import numpy as np
import pytest

import empathy_field as ef
import grt_transition as g


# ---------------------------------------------------------------------------
# Coupling, resonance, bandwidth
# ---------------------------------------------------------------------------

def test_couple_k0_is_identity():
    base = ef.resonance_population(1.00, 8, 42)
    coupled = g.couple(base, 0.0)
    for a, b in zip(coupled, base):
        assert np.max(np.abs(a - b)) <= 1e-12


def test_couple_k1_is_reference():
    base = ef.resonance_population(1.00, 8, 42)
    ref = g.reference_state()
    for s in g.couple(base, 1.0):
        assert np.max(np.abs(s - ref)) <= 1e-12
    assert g.mean_resonance(g.couple(base, 1.0)) == pytest.approx(
        1.0, abs=1e-12)
    assert g.pair_shared_information(g.couple(base, 1.0)) == \
        pytest.approx(2.0, abs=1e-12)


def test_couple_rejects_out_of_range():
    base = ef.resonance_population(1.00, 8, 42)
    with pytest.raises(ValueError):
        g.couple(base, -0.1)
    with pytest.raises(ValueError):
        g.couple(base, 1.1)


def test_mean_resonance_curves():
    for seed, expected in (
            (42, [0.4197, 0.4538, 0.4974, 0.5553, 0.6346, 0.7361,
                  0.8393, 0.9188, 0.9680, 0.9929, 1.0]),
            (7, [0.2778, 0.2586, 0.2423, 0.2376, 0.2608, 0.3689,
                 0.5949, 0.7953, 0.9209, 0.9831, 1.0]),
            (1234, [0.2000, 0.2290, 0.2736, 0.3395, 0.4363, 0.5699,
                    0.7211, 0.8515, 0.9398, 0.9865, 1.0]),
            (2026, [0.2474, 0.2837, 0.3378, 0.4147, 0.5160, 0.6358,
                    0.7589, 0.8661, 0.9435, 0.9870, 1.0])):
        scan = g.coupling_scan(seed)
        assert [r["mean_r"] for r in scan["rows"]] == pytest.approx(
            expected, abs=1e-3)


def test_mean_resonance_not_monotone_seed_7():
    # Reported, not gated: mixing toward the common reference
    # can initially lower pairwise overlap for some pairs.
    # On seed 7 mean R dips 0.2778 -> 0.2376 at K = 0.3
    # before rising; on the other three seeds it is monotone.
    scan = g.coupling_scan(7)
    assert scan["mean_r_monotone"] is False
    assert scan["rows"][3]["mean_r"] == pytest.approx(
        0.2376, abs=1e-3)
    for seed in (42, 1234, 2026):
        assert g.coupling_scan(seed)["mean_r_monotone"] is True


def test_bandwidth_curves_calibration_seeds():
    for seed, expected in (
            (42, [1.1468, 1.2004, 1.2804, 1.3946, 1.5119, 1.5610,
                  1.6134, 1.7635, 1.9012, 1.9775, 2.0]),
            (7, [1.1226, 1.2404, 1.3643, 1.4758, 1.5211, 1.3758,
                 1.3186, 1.5782, 1.8309, 1.9634, 2.0])):
        scan = g.coupling_scan(seed)
        assert [r["bandwidth_bits"] for r in scan["rows"]] == \
            pytest.approx(expected, abs=1e-3)


def test_bandwidth_curves_held_out_seeds():
    # On seed 1234 B FALLS from K = 0 to K = 0.5 (1.4360 ->
    # 1.3496) before jumping; on seed 2026 it is flat
    # (~1.27) until K = 0.4 and then rises. Bandwidth does
    # not track coupling cleanly on either held-out seed.
    for seed, expected in (
            (1234, [1.4360, 1.4109, 1.3923, 1.3693, 1.3518, 1.3496,
                    1.4478, 1.6759, 1.8657, 1.9697, 2.0]),
            (2026, [1.2643, 1.2802, 1.2795, 1.2733, 1.2731, 1.3391,
                    1.5034, 1.7136, 1.8779, 1.9718, 2.0])):
        scan = g.coupling_scan(seed)
        assert [r["bandwidth_bits"] for r in scan["rows"]] == \
            pytest.approx(expected, abs=1e-3)
    scan = g.coupling_scan(1234)
    assert scan["rows"][5]["bandwidth_bits"] < \
        scan["rows"][0]["bandwidth_bits"]


def test_critical_coupling_values():
    for seed, expected_kc in ((42, 0.3), (7, 0.6),
                              (1234, 0.5), (2026, 0.4)):
        scan = g.coupling_scan(seed)
        assert scan["k_c"] == pytest.approx(expected_kc)


def test_max_bandwidth_step_at_k07_every_seed():
    # The displaced jump: the largest bandwidth step sits at
    # K = 0.7 on ALL four seeds, well after K_c (0.3 / 0.6 /
    # 0.5 / 0.4). This is the measured shape behind the
    # (lviii) failure, not a calibration artefact.
    for seed, expected_max in ((42, 0.1501), (7, 0.2597),
                               (1234, 0.2282), (2026, 0.2103)):
        scan = g.coupling_scan(seed)
        assert scan["max_step_k"] == pytest.approx(0.7)
        assert scan["max_step_bits"] == pytest.approx(
            expected_max, abs=1e-3)


def test_bandwidth_steps_at_kc():
    # The step ending at K_c: +0.1142 on seed 42 (the only
    # seed where it clears the 0.10 bar), negative or ~0 on
    # the other three seeds.
    for seed, expected in ((42, 0.1142), (7, -0.0572),
                           (1234, -0.0023), (2026, -0.0002)):
        scan = g.coupling_scan(seed)
        assert scan["step_at_kc_bits"] == pytest.approx(
            expected, abs=1e-3)


# ---------------------------------------------------------------------------
# Components: macro and nested
# ---------------------------------------------------------------------------

def test_field_fragmented_at_k0():
    for seed, expected in ((42, [7, 1]), (7, [6, 1, 1]),
                           (1234, [4, 2, 1, 1]),
                           (2026, [3, 2, 1, 1, 1])):
        scan = g.coupling_scan(seed)
        assert scan["rows"][0]["components_macro"] == expected
        assert scan["rows"][0]["components_macro"][0] <= 7


def test_macro_forms_just_above_kc():
    for seed in (42, 7, 1234, 2026):
        scan = g.coupling_scan(seed)
        k_above = round(scan["k_c"] + 0.2, 1)
        row = [r for r in scan["rows"] if r["k"] == k_above][0]
        assert row["components_macro"] == [8]


def test_nested_components_persist_at_kc():
    for seed, expected in ((42, [7, 1]), (7, [3, 3, 1, 1]),
                           (1234, [4, 3, 1]),
                           (2026, [3, 2, 1, 1, 1])):
        scan = g.coupling_scan(seed)
        row = [r for r in scan["rows"] if r["k"] == scan["k_c"]][0]
        assert row["components_nested"] == expected
        assert len(row["components_nested"]) >= 2


def test_nesting_dissolves_at_full_coupling():
    # Reported, not gated: at K = 1 all sub-structure has
    # dissolved (one component at R >= 0.75 on every seed),
    # so nesting does not survive to full coupling.
    for seed in (42, 7, 1234, 2026):
        scan = g.coupling_scan(seed)
        assert scan["rows"][-1]["components_nested"] == [8]


def test_coupling_row_fields():
    base = ef.resonance_population(1.00, 8, 42)
    row = g.coupling_row(0.5, base)
    assert row["k"] == pytest.approx(0.5)
    assert row["mean_r"] == pytest.approx(0.7361, abs=1e-3)
    assert row["bandwidth_bits"] == pytest.approx(1.5610, abs=1e-3)
    assert row["components_macro"] == [8]
    assert row["components_nested"] == [7, 1]


# ---------------------------------------------------------------------------
# (lvii) Machinery
# ---------------------------------------------------------------------------

def test_claim_lvii_verdict_pass():
    verdict = g.claim_machinery_verdict()
    assert verdict["passed"] is True
    assert all(verdict["checks"].values())
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["k_c"] == pytest.approx(0.3)
    assert by_seed[7]["k_c"] == pytest.approx(0.6)
    assert by_seed[1234]["k_c"] == pytest.approx(0.5)
    assert by_seed[2026]["k_c"] == pytest.approx(0.4)
    assert by_seed[42]["largest_component_at_k0"] == 7
    assert by_seed[7]["largest_component_at_k0"] == 6
    assert by_seed[1234]["largest_component_at_k0"] == 4
    assert by_seed[2026]["largest_component_at_k0"] == 3
    for r in verdict["per_seed"]:
        assert r["endpoint_k0_max_deviation"] <= 1e-12
        assert r["endpoint_k1_max_deviation"] <= 1e-12
        assert r["bandwidth_at_k1"] == pytest.approx(2.0, abs=1e-12)


# ---------------------------------------------------------------------------
# (lviii) GRT phase transition as stated
# ---------------------------------------------------------------------------

def test_claim_lviii_verdict_fail():
    verdict = g.claim_transition_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["step_at_kc_large_enough"] is False
    assert verdict["checks"]["step_at_kc_is_largest"] is False
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    # Only seed 42 clears the 0.10-bit bar at K_c; the
    # other three steps are negative or ~0.
    assert by_seed[42]["step_at_kc_bits"] == pytest.approx(
        0.1142, abs=1e-3)
    assert by_seed[7]["step_at_kc_bits"] == pytest.approx(
        -0.0572, abs=1e-3)
    assert by_seed[1234]["step_at_kc_bits"] == pytest.approx(
        -0.0023, abs=1e-3)
    assert by_seed[2026]["step_at_kc_bits"] == pytest.approx(
        -0.0002, abs=1e-3)
    # And on no seed is the K_c step the largest: the max
    # step is at K = 0.7 on every seed.
    for r in verdict["per_seed"]:
        assert r["max_step_k"] == pytest.approx(0.7)


# ---------------------------------------------------------------------------
# (lix) Measured shape
# ---------------------------------------------------------------------------

def test_claim_lix_verdict_pass():
    verdict = g.claim_shape_verdict()
    assert verdict["passed"] is True
    assert all(verdict["checks"].values())
    by_seed = {r["seed"]: r for r in verdict["per_seed"]}
    assert by_seed[42]["largest_component_macro_at_kc_plus_0.2"] == 8
    assert by_seed[7]["largest_component_macro_at_kc_plus_0.2"] == 8
    assert by_seed[1234]["largest_component_macro_at_kc_plus_0.2"] == 8
    assert by_seed[2026]["largest_component_macro_at_kc_plus_0.2"] == 8
    assert by_seed[42]["n_nested_components_at_kc"] == 2
    assert by_seed[7]["n_nested_components_at_kc"] == 4
    assert by_seed[1234]["n_nested_components_at_kc"] == 3
    assert by_seed[2026]["n_nested_components_at_kc"] == 5
    assert by_seed[42]["bandwidth_total_rise_bits"] == pytest.approx(
        0.8532, abs=1e-3)
    assert by_seed[7]["bandwidth_total_rise_bits"] == pytest.approx(
        0.8774, abs=1e-3)
    assert by_seed[1234]["bandwidth_total_rise_bits"] == pytest.approx(
        0.5640, abs=1e-3)
    assert by_seed[2026]["bandwidth_total_rise_bits"] == pytest.approx(
        0.7357, abs=1e-3)


# ---------------------------------------------------------------------------
# Aggregate, thresholds, main
# ---------------------------------------------------------------------------

def test_grt_transition_claims_aggregate():
    verdicts = g.grt_transition_claims()
    assert verdicts["n_claims"] == 3
    assert verdicts["n_passed"] == 2
    assert verdicts["all_pass"] is False
    assert verdicts["headline_allowed"] is False


def test_thresholds_set():
    thresholds = g._thresholds()
    assert thresholds["sigma_base"] == pytest.approx(1.00)
    assert thresholds["n_agents"] == 8
    assert thresholds["k_grid"] == tuple(
        round(0.1 * k, 1) for k in range(11))
    assert thresholds["resonance_threshold"] == pytest.approx(0.5)
    assert thresholds["nested_threshold"] == pytest.approx(0.75)
    assert thresholds["exact_tol"] == pytest.approx(1e-12)
    assert thresholds["largest_component_start_max"] == 7
    assert thresholds["jump_min_bits"] == pytest.approx(0.10)
    assert thresholds["macro_size"] == 8
    assert thresholds["nested_components_min"] == 2
    assert thresholds["total_rise_min_bits"] == pytest.approx(0.50)


def test_main_runs(capsys):
    g.main()
    out = capsys.readouterr().out
    assert "2/3 claims passed" in out
    assert "claim (lvii) verdict: PASS" in out
    assert "claim (lviii) verdict: FAIL" in out
    assert "claim (lix) verdict: PASS" in out
