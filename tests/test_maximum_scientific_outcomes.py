# Tests for maximum-scientific-outcomes logic.

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
