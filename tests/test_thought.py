# test_thought.py
#
# Tests for thought.py (claims (ii) and (iii)).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import numpy as np

import thought as th


def test_uniform_thought_coherence_is_maximal():
    """l1-coherence of the uniform thought is 3.0 (the 4-dim maximum)."""
    rho = th.density_matrix(th.uniform_thought())
    assert abs(th.l1_coherence(rho) - 3.0) < 1e-9


def test_decided_thought_has_no_coherence():
    """A basis thought has zero off-diagonal mass."""
    for concept in th.CONCEPTS:
        rho = th.density_matrix(th.focused_thought(concept))
        assert abs(th.l1_coherence(rho)) < 1e-9


def test_dephasing_formula():
    """Coherence after n steps is C(0)(1-p)^n, exactly."""
    rho0 = th.density_matrix(th.uniform_thought())
    c0 = th.l1_coherence(rho0)
    for p in (0.05, 0.1, 0.25, 0.5):
        for n in (1, 3, 7):
            c_n = th.l1_coherence(th.dephase_steps(rho0, p, n))
            assert abs(c_n - c0 * (1.0 - p) ** n) < 1e-9


def test_dephasing_keeps_born_probabilities():
    """Dephasing touches only coherence; the diagonals are untouched."""
    rho0 = th.density_matrix(th.uniform_thought())
    rho1 = th.dephase(rho0, 0.5)
    assert np.allclose(np.diag(rho1), np.diag(rho0))


def test_claim_ii_verdict_passes():
    """Claim (ii): coherence half-life measured."""
    verdict = th.claim_coherence_verdict()
    for row in verdict["rows"]:
        print(f"claim (ii): p={row['p']}, half-life measured="
              f"{row['half_life_measured_steps']}, analytic="
              f"{row['half_life_analytic_steps']:.2f}")
        assert row["half_life_match"] is True
        assert row["formula_match"] is True
    assert verdict["passed"] is True


def test_claim_iii_verdict_passes():
    """Claim (iii): collapse cost measured."""
    verdict = th.claim_collapse_verdict()
    print(f"claim (iii): dephased entropy="
          f"{verdict['dephased_entropy_bits']:.4f} bits, decision "
          f"entropy before={verdict['decision_entropy_before_bits']:.4f}, "
          f"after={verdict['decision_entropy_after_bits']:.4f}, "
          f"collapsed to {verdict['collapsed_concept']!r}, attention "
          f"bias +0.05={verdict['attention_bias_plus']:+.6f}, "
          f"-0.05={verdict['attention_bias_minus']:+.6f}")
    assert verdict["passed"] is True
    assert verdict["checks"]["dephased_entropy_2_bits"] is True
    assert verdict["checks"]["collapsed_entropy_0"] is True
    assert verdict["checks"]["decision_entropy_2_bits"] is True
    assert verdict["checks"]["decision_entropy_after_collapse_0"] is True
    assert verdict["checks"]["attention_bias_positive"] is True
    assert verdict["checks"]["attention_bias_negative"] is True
    assert verdict["checks"]["attention_bias_symmetric"] is True


def test_collapse_is_deterministic_with_seed():
    """The same seed collapses to the same concept."""
    psi = th.uniform_thought()
    idx1, _ = th.collapse(psi, seed=42)
    idx2, _ = th.collapse(psi, seed=42)
    assert idx1 == idx2
    idx3, _ = th.collapse(psi, seed=7)
    assert idx3 in range(th.N_CONCEPTS)


def test_collapse_of_decided_thought_is_certain():
    """Collapsing a focused thought returns that concept."""
    for concept in th.CONCEPTS:
        psi = th.focused_thought(concept)
        idx, collapsed = th.collapse(psi, seed=1)
        assert th.CONCEPTS[idx] == concept
        assert np.allclose(collapsed, psi)


def test_attention_bias_clips_to_yin_bound():
    """A delta beyond +-0.05 behaves exactly like +-0.05."""
    psi = th.uniform_thought()
    _, bias_big = th.attention_bias(psi, "attention", +1.0)
    _, bias_bound = th.attention_bias(psi, "attention", +0.05)
    assert bias_big == bias_bound
    _, bias_neg = th.attention_bias(psi, "attention", -1.0)
    _, bias_neg_bound = th.attention_bias(psi, "attention", -0.05)
    assert bias_neg == bias_neg_bound
