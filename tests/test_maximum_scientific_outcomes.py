# Tests for maximum-scientific-outcomes logic.

import json

import numpy as np
import pytest

from scientific_outcomes import (
    bootstrap_attunement,
    maximum_scientific_outcome,
    preregistration,
    provenance,
    sensitivity_analysis,
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
