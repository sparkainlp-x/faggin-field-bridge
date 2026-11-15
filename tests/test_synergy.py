# Tests for fecundity-driven attraction expansion and love-empathy synergy.

import pytest

from synergy import (
    attraction,
    expansion,
    fecundity,
    love_empathy_synergy,
    maximum_synergy_outcome,
    synergy_status,
    validate_synergy_inputs,
)


def test_validate_synergy_inputs_accepts_valid_values():
    result = validate_synergy_inputs(
        unity=0.99999995,
        cost=0.9553,
        love=0.5503,
        empathy=0.5503,
        delta=0.05,
    )
    assert result["unity"] == pytest.approx(0.99999995)
    assert result["cost"] == pytest.approx(0.9553)
    assert result["love"] == pytest.approx(0.5503)
    assert result["empathy"] == pytest.approx(0.5503)
    assert result["delta"] == pytest.approx(0.05)


def test_validate_synergy_inputs_rejects_invalid_love():
    with pytest.raises(ValueError):
        validate_synergy_inputs(0.5, 0.5, 1.2, 0.5)


def test_validate_synergy_inputs_rejects_invalid_empathy():
    with pytest.raises(ValueError):
        validate_synergy_inputs(0.5, 0.5, 0.5, -0.1)


def test_fecundity_is_unity_retained_after_cost():
    result = fecundity(0.99999995, 0.9553)
    assert result == pytest.approx(0.99999995 * (1.0 - 0.9553))


def test_attraction_scales_fecundity():
    f = fecundity(0.99999995, 0.9553)
    result = attraction(f, 0.05)
    assert result == pytest.approx(f * 1.05)


def test_love_empathy_synergy_is_bounded():
    result = love_empathy_synergy(1.0, 1.0, 1.0)
    assert result == pytest.approx(1.0)


def test_expansion_is_bounded():
    result = expansion(1.0, 1.0)
    assert result == pytest.approx(1.0)


def test_synergy_status_boundaries():
    assert synergy_status(0.05, 0.9) == "DORMANT"
    assert synergy_status(0.2, 0.9) == "EMERGENT"
    assert synergy_status(0.5, 0.9) == "FLOWING"
    assert synergy_status(0.8, 0.9) == "FECUND-SYNERGISTIC"
    assert synergy_status(0.8, 0.4) == "EXPANDING"


def test_maximum_synergy_outcome_primary_values():
    result = maximum_synergy_outcome(
        unity=0.99999995,
        cost=0.9553,
        love=0.5503,
        empathy=0.5503,
        delta=0.05,
    )

    expected_f = 0.99999995 * (1.0 - 0.9553)
    expected_x = expected_f * 1.05
    expected_s = (0.5503 * 0.5503 * (1.0 + expected_f)) / 2.0
    expected_e = min(1.0, expected_x * (1.0 + expected_s))

    assert result["fecundity"] == pytest.approx(expected_f)
    assert result["attraction"] == pytest.approx(expected_x)
    assert result["love_empathy_synergy"] == pytest.approx(expected_s)
    assert result["expansion"] == pytest.approx(expected_e)
    assert result["bridge_mapping_status"] == "PARTIAL"


def test_maximum_synergy_outcome_contains_non_claims():
    result = maximum_synergy_outcome(
        unity=0.99999995,
        cost=0.9553,
    )
    claims = result["claims"]
    assert claims["consciousness_tested"] is False
    assert claims["love_measured"] is False
    assert claims["empathy_measured"] is False
    assert claims["entanglement_measured"] is False
    assert claims["synthetic_classical_mapping"] is True
