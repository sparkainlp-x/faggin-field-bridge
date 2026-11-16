# Tests for maximum-scientific-outcomes logic.
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import json

import numpy as np
import pytest

from scientific_outcomes import (
    bootstrap_attunement,
    bootstrap_expansion,
    maximum_scientific_outcome,
    preregistration,
    provenance,
    sensitivity_analysis,
    synergy_robustness,
    threshold_robustness,
    validate_inputs,
    write_benchmark,
)


def test_validate_inputs_accepts_valid_values():
    result = validate_inputs(0.99999995, 0.9553, 0.05)
    assert result["unity"] == pytest.approx(0.99999995)
    assert result["cost"] == pytest.approx(0.9553)
    assert result["delta"] == pytest.approx(0.05)


def test_validate_inputs_rejects_invalid_unity():
    with pytest.raises(ValueError):
        validate_inputs(1.1, 0.5)


def test_validate_inputs_rejects_invalid_cost():
    with pytest.raises(ValueError):
        validate_inputs(0.5, -0.1)


def test_validate_inputs_clips_delta():
    result = validate_inputs(0.5, 0.5, 10.0)
    assert result["delta"] == pytest.approx(0.05)


def test_bootstrap_returns_ordered_interval():
    result = bootstrap_attunement(0.99999995, 0.9553, n_boot=500, seed=42)
    assert result["lower"] <= result["mean"] <= result["upper"]
    assert result["n_boot"] == 500


def test_bootstrap_is_deterministic():
    first = bootstrap_attunement(0.99999995, 0.9553, n_boot=300, seed=42)
    second = bootstrap_attunement(0.99999995, 0.9553, n_boot=300, seed=42)
    assert first["mean"] == second["mean"]
    assert first["lower"] == second["lower"]
    assert first["upper"] == second["upper"]


def test_sensitivity_contains_all_parameters():
    result = sensitivity_analysis(0.99999995, 0.9553)
    assert set(result) == {"unity", "cost", "delta"}
    assert len(result["unity"]) == 5
    assert len(result["cost"]) == 5
    assert len(result["delta"]) == 5


def test_sensitivity_correct_values():
    """Each sweep perturbs only its own parameter (v0.3.1 fix).

    Through v0.3.0 the cost sweep fed the perturbed cost into the
    unity slot (so its "attunement" column was the perturbation
    itself: -0.05, -0.01, 0.0, 0.01, 0.0447) and the delta sweep
    fed delta into the unity slot (so delta = 0 reported -0.9553
    instead of the point estimate 0.0447). Correct values at
    U = 0.99999995, C = 0.9553, delta = 0:
    """
    result = sensitivity_analysis(0.99999995, 0.9553)
    assert [row["attunement"] for row in result["unity"]] == pytest.approx(
        [-0.0053, 0.0347, 0.0447, 0.0447, 0.0447], abs=1e-4
    )
    assert [row["attunement"] for row in result["cost"]] == pytest.approx(
        [0.0947, 0.0547, 0.0447, 0.0347, -0.0], abs=1e-4
    )
    assert [row["attunement"] for row in result["delta"]] == pytest.approx(
        [-0.0053, 0.0197, 0.0447, 0.0697, 0.0947], abs=1e-4
    )
    # The "value" column carries the perturbed parameter itself.
    assert [row["value"] for row in result["cost"]] == pytest.approx(
        [0.9053, 0.9453, 0.9553, 0.9653, 1.0], abs=1e-4
    )
    assert [row["value"] for row in result["delta"]] == pytest.approx(
        [-0.05, -0.025, 0.0, 0.025, 0.05], abs=1e-4
    )


def test_sensitivity_directional():
    """Directional correctness: the sign each parameter must have.

    A cost increase must lower A; a unity or delta increase must
    raise it. This is the assertion the v0.3.0 suite lacked — it
    checked only keys and row counts, which the bug passed.
    """
    result = sensitivity_analysis(0.99999995, 0.9553)
    cost_a = [row["attunement"] for row in result["cost"]]
    assert all(b < a for a, b in zip(cost_a, cost_a[1:]))
    unity_a = [row["attunement"] for row in result["unity"]]
    assert all(b >= a for a, b in zip(unity_a, unity_a[1:]))
    delta_a = [row["attunement"] for row in result["delta"]]
    assert all(b > a for a, b in zip(delta_a, delta_a[1:]))


def test_robustness_reports_attuned_case():
    """robustness() must not force an ATTUNED case into PARTIAL.

    Through v0.3.0 the bound statuses were hardcoded to
    DISSONANT/PARTIAL. Now they come from the single classifier.
    """
    from scientific_outcomes import robustness

    result = robustness(1.0, 0.0, empathy=0.9, n_boot=200, seed=42)
    assert result["reported_status"] == "ATTUNED"
    assert result["status_at_lower_bound"] == "ATTUNED"
    assert result["status_at_upper_bound"] == "ATTUNED"
    assert result["status_stable_under_uncertainty"] is True


def test_maximum_scientific_outcome_attuned_low_empathy_hyphen():
    """The uncalibrated status uses the hyphen label, single-sourced.

    Through v0.3.0 maximum_scientific_outcome re-implemented the
    classification inline and emitted "ATTUNED_LOW_EMPATHY"
    (underscores) while bridge.mapping_status emits
    "ATTUNED-LOW-EMPATHY" (hyphens). Both now call the one
    classifier.
    """
    result = maximum_scientific_outcome(
        unity=1.0, cost=0.0, empathy=0.49, n_boot=200, seed=42,
    )
    assert result["mapping_status"]["before_calibration"] == "ATTUNED-LOW-EMPATHY"
    assert result["mapping_status"]["after_best_calibration"] == "ATTUNED-LOW-EMPATHY"
    assert result["preregistration"]["decision_rule"]["ATTUNED-LOW-EMPATHY"] == (
        "A >= 0.5 and empathy < 0.5"
    )
    assert "ATTUNED_LOW_EMPATHY" not in result["preregistration"]["decision_rule"]


def test_synergy_robustness_margins_cover_all_thresholds():
    """The margins dict tracks every expansion threshold (v0.3.1).

    Primary expansion e = 0.05436 sits 0.00436 above the EMERGENT
    boundary (the FLOWING label hangs on that margin), 0.02436
    above DORMANT, 0.54564 below FECUND.
    """
    result = synergy_robustness(
        0.99999995, 0.9553, love=0.5503, empathy=0.5503, delta=0.05,
        n_boot=200, seed=42,
    )
    assert result["margins"]["to_emergent"] == pytest.approx(0.00436, abs=1e-4)
    assert result["margins"]["to_dormant"] == pytest.approx(0.02436, abs=1e-4)
    assert result["margins"]["to_fecund"] == pytest.approx(0.54564, abs=1e-4)
    assert result["margin_to_nearest_threshold"] == pytest.approx(
        result["margins"]["to_emergent"], abs=1e-12
    )


def test_threshold_robustness_grid():
    """The FLOWING label under other threshold choices (v0.3.1).

    Shipped thresholds (0.03, 0.05) label the primary expansion
    FLOWING. The label survives any EMERGENT threshold up to 0.05
    and flips to EMERGENT at 0.06. Under the pre-8fb00f1
    thresholds (DORMANT 0.10, EMERGENT 0.30) the same expansion
    was DORMANT — the commit moved the label two steps, not one.
    """
    result = threshold_robustness(0.99999995, 0.9553)
    assert result["shipped_status"] == "FLOWING"
    assert result["dormant_grid"] == [0.01, 0.03, 0.05, 0.10]
    assert result["emergent_grid"] == [0.03, 0.05, 0.06, 0.10, 0.30]
    assert len(result["statuses"]) == 4
    assert all(len(row) == 5 for row in result["statuses"])
    # Shipped cell (dormant 0.03, emergent 0.05).
    assert result["statuses"][1][1] == "FLOWING"
    # EMERGENT threshold 0.06 flips it.
    assert result["statuses"][1][2] == "EMERGENT"
    # Pre-8fb00f1 cell (dormant 0.10, emergent 0.30).
    assert result["statuses"][3][4] == "DORMANT"


def test_maximum_scientific_outcome_primary_values():
    result = maximum_scientific_outcome(
        unity=0.99999995,
        cost=0.9553,
        empathy=0.5503,
        n_boot=300,
        seed=42,
    )
    point = result["point_estimate"]
    assert point["unity"] == pytest.approx(0.99999995)
    assert point["entropy_cost"] == pytest.approx(0.9553)
    assert point["attunement_delta_zero"] == pytest.approx(0.04469995)
    assert point["best_attunement"] == pytest.approx(0.09469995)


def test_mapping_status_before_and_after_calibration():
    result = maximum_scientific_outcome(
        unity=0.99999995,
        cost=0.9553,
        empathy=0.5503,
        n_boot=300,
        seed=42,
    )
    status = result["mapping_status"]
    assert status["before_calibration"] == "PARTIAL"
    assert status["after_best_calibration"] == "PARTIAL"
    assert status["calibration_changes_status"] is False


def test_robustness_reports_sign_flip_possibility():
    result = maximum_scientific_outcome(
        unity=0.99999995,
        cost=0.9553,
        n_boot=500,
        seed=42,
    )
    robust = result["robustness"]
    assert isinstance(robust["sign_flip_possible"], bool)
    assert robust["calibration_can_rescue"] is False


def test_bootstrap_expansion_returns_ordered_interval():
    result = bootstrap_expansion(
        0.99999995, 0.9553, love=0.5503, empathy=0.5503, delta=0.05,
        n_boot=500, seed=42,
    )
    assert result["lower"] <= result["mean"] <= result["upper"]
    assert result["n_boot"] == 500


def test_bootstrap_expansion_is_deterministic():
    first = bootstrap_expansion(
        0.99999995, 0.9553, love=0.5503, empathy=0.5503, delta=0.05,
        n_boot=300, seed=42,
    )
    second = bootstrap_expansion(
        0.99999995, 0.9553, love=0.5503, empathy=0.5503, delta=0.05,
        n_boot=300, seed=42,
    )
    assert first["mean"] == second["mean"]
    assert first["lower"] == second["lower"]
    assert first["upper"] == second["upper"]


def test_synergy_robustness_primary_flowing_is_stable():
    result = synergy_robustness(
        0.99999995, 0.9553, love=0.5503, empathy=0.5503, delta=0.05,
        n_boot=500, seed=42,
    )
    assert result["reported_status"] == "FLOWING"
    assert result["status_stable_under_uncertainty"] is True
    # Margin to the EMERGENT threshold is several standard deviations.
    assert result["margin_in_standard_deviations"] > 3.0


def test_synergy_robustness_omega_emergent_is_not_stable():
    result = synergy_robustness(
        0.9005, 0.9553, love=0.5503, empathy=0.5503, delta=0.05,
        n_boot=500, seed=42,
    )
    assert result["reported_status"] == "EMERGENT"
    # The Omega expansion interval straddles the 0.05 threshold, so
    # its EMERGENT status flips to FLOWING within the noise model.
    assert result["status_stable_under_uncertainty"] is False
    assert result["margin_in_standard_deviations"] < 1.5


def test_fecundity_minus_attunement_is_identity():
    result = synergy_robustness(
        0.99999995, 0.9553, love=0.5503, empathy=0.5503, delta=0.05,
        n_boot=200, seed=42,
    )
    # F - A = C * (1 - U). With U ~ 1 the difference is ~5e-8.
    expected = 0.9553 * (1.0 - 0.99999995)
    assert result["fecundity_minus_attunement"] == pytest.approx(expected, abs=1e-12)
    assert result["fecundity_minus_attunement_identity"] == "C * (1 - U)"


def test_maximum_scientific_outcome_includes_synergy_robustness():
    result = maximum_scientific_outcome(
        unity=0.99999995,
        cost=0.9553,
        empathy=0.5503,
        n_boot=200,
        seed=42,
    )
    assert "synergy_robustness" in result
    assert result["synergy_robustness"]["reported_status"] == "FLOWING"


def test_preregistration_contains_non_claims():
    plan = preregistration()
    assert plan["primary_endpoint"] == "attunement at delta = 0"
    assert "This does not test consciousness." in plan["non_claims"]
    assert "This does not measure quantum entanglement." in plan["non_claims"]


def test_provenance_hash_is_deterministic():
    inputs = {"unity": 0.99999995, "cost": 0.9553}
    first = provenance(inputs, seed=42)
    second = provenance(inputs, seed=42)
    assert first["input_hash_sha256"] == second["input_hash_sha256"]
    assert first["random_seed"] == 42


def test_write_benchmark_creates_files(tmp_path):
    result = maximum_scientific_outcome(
        unity=0.99999995,
        cost=0.9553,
        n_boot=200,
        seed=42,
    )
    paths = write_benchmark(
        result,
        json_path=tmp_path / "benchmark.json",
        markdown_path=tmp_path / "BENCHMARK.md",
    )
    parsed = json.loads((tmp_path / "benchmark.json").read_text(encoding="utf-8"))
    assert parsed["claims"]["consciousness_tested"] is False
    assert (tmp_path / "BENCHMARK.md").exists()
    assert paths["json"].endswith("benchmark.json")
