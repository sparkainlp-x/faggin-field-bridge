# test_bridge.py
#
# Tests for bridge.py (wiring + mapping status + worked examples).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import pytest

import bridge


def test_mapping_status_dissonant():
    """A < 0 is DISSONANT whatever the empathy."""
    assert bridge.mapping_status(-0.1, 0.55)["label"] == "DISSONANT"
    assert bridge.mapping_status(-0.9, 0.9)["label"] == "DISSONANT"


def test_mapping_status_partial():
    """0 <= A < 0.5 is PARTIAL whatever the empathy."""
    assert bridge.mapping_status(0.0, 0.55)["label"] == "PARTIAL"
    assert bridge.mapping_status(0.2, 0.1)["label"] == "PARTIAL"
    assert bridge.mapping_status(0.49, 0.9)["label"] == "PARTIAL"


def test_mapping_status_attuned_needs_both():
    """A >= 0.5 and E >= 0.5 is ATTUNED."""
    v = bridge.mapping_status(0.7, 0.55)
    assert v["label"] == "ATTUNED"
    assert v["empathy_gate_met"] is True


def test_mapping_status_attuned_low_empathy():
    """A >= 0.5 but E < 0.5 is ATTUNED-LOW-EMPATHY."""
    v = bridge.mapping_status(0.7, 0.3)
    assert v["label"] == "ATTUNED-LOW-EMPATHY"
    assert v["empathy_gate_met"] is False


def test_mapping_status_boundary_at_threshold():
    """Exactly at A = 0.5 with E at the gate is ATTUNED."""
    assert bridge.mapping_status(0.5, 0.5)["label"] == "ATTUNED"
    assert bridge.mapping_status(0.5, 0.49)["label"] == "ATTUNED-LOW-EMPATHY"


def test_bridge_returns_every_step():
    """bridge() returns observation, both attunements, delta, mapping status."""
    r = bridge.bridge(0.9, 0.3, empathy=0.55)
    assert r["observation"].unity == pytest.approx(0.9)
    assert r["observation"].cost == pytest.approx(0.3)
    assert r["uncalibrated_attunement"] == pytest.approx(0.6)
    assert r["best_delta"] == pytest.approx(0.05)
    assert r["best_attunement"] == pytest.approx(0.9 * 1.05 - 0.3)
    assert r["calibrated_attunement"] == pytest.approx(r["best_attunement"])
    assert r["mapping_status"]["label"] == "ATTUNED"


def test_bridge_from_entropy():
    """bridge_from_entropy normalizes the entropy into the cost."""
    r = bridge.bridge_from_entropy(0.9, 0.9553, 1.0, empathy=0.55)
    assert r["observation"].cost == pytest.approx(0.9553)
    assert r["uncalibrated_attunement"] == pytest.approx(0.9 - 0.9553)


def test_worked_example_primary_is_partial():
    """The primary worked example (de Broglie unity, tensor cost)
    is PARTIAL: near-perfect unity, but the 0.955 entropy cost
    eats almost all of it. The calibrator cannot rescue it."""
    ex = bridge.worked_example()
    primary = ex["primary_debroglie_tensor"]
    assert primary["observation"].unity == pytest.approx(0.99999995, abs=1e-6)
    assert primary["observation"].cost == pytest.approx(0.9553, abs=1e-3)
    assert primary["mapping_status"]["label"] == "PARTIAL"
    assert primary["best_delta"] == pytest.approx(0.05)
    # Even at the best delta, attunement stays below the 0.5 threshold.
    assert primary["best_attunement"] < 0.5
    # And at the worst delta it goes negative.
    import attunement as at
    assert at.attunement(primary["observation"].unity,
                         primary["observation"].cost, -0.05) < 0.0


def test_worked_example_omega_variants():
    """The Omega-Genesis variants run and are DISSONANT.

    With the notebook's unity (0.9005 reported, 0.837 synthetic)
    against the same 0.955 tensor cost, the cost exceeds unity
    even at the best delta (+0.05): 0.9005 * 1.05 - 0.9553 < 0.
    The de Broglie unity (0.99999995) is the only one high enough
    to stay PARTIAL. That contrast is the bridge's honest result:
    the notebook's unity does not cover the tensor cost."""
    ex = bridge.worked_example()
    assert ex["omega_reported"]["mapping_status"]["label"] == "DISSONANT"
    assert ex["omega_synthetic"]["mapping_status"]["label"] == "DISSONANT"
    assert ex["omega_reported"]["best_attunement"] < 0.0
    assert ex["omega_synthetic"]["best_attunement"] < 0.0
