# test_quantum_thought_claims.py
#
# Tests for the unified quantum-thought claims (bridge.py) and the
# updated claims registry (scientific_outcomes.py).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import bridge
import scientific_outcomes as so


def test_quantum_thought_claims_all_pass():
    """All four quantum-thought claims pass; no headline is emitted."""
    result = bridge.quantum_thought_claims()
    assert result["headline_allowed"] is False
    assert bridge.HEADLINE_ALLOWED is False
    assert result["n_claims"] == 4
    assert result["n_passed"] == 4
    assert result["all_pass"] is True
    for key in ("claim_i_entanglement", "claim_ii_coherence",
                "claim_iii_collapse", "claim_iv_self_knowing"):
        assert result[key]["passed"] is True


def test_maximum_outcome_includes_quantum_thoughts():
    """maximum_scientific_outcome carries the quantum-thought claims."""
    result = so.maximum_scientific_outcome(0.99999995, 0.9553, n_boot=100)
    qt = result["quantum_thoughts"]
    assert qt["all_pass"] is True
    assert qt["n_passed"] == 4
    # Physical entanglement in hardware is still not measured;
    # entanglement as a quantity of the model is.
    assert result["claims"]["entanglement_measured"] is False
    assert result["claims"]["entanglement_measured_in_model"] is True
    assert result["claims"]["consciousness_tested"] is False
    assert result["claims"]["faggin_endorsed"] is False


def test_preregistration_keeps_old_non_claims_and_scopes_entanglement():
    """The original non-claims stay verbatim; the model scope is added."""
    plan = so.preregistration()
    assert "This does not test consciousness." in plan["non_claims"]
    assert "This does not measure quantum entanglement." in plan["non_claims"]
    assert any("only as a quantity of the model" in c
               for c in plan["non_claims"])
