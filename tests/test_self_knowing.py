# test_self_knowing.py
#
# Tests for self_knowing.py (claim (iv)).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import math

import numpy as np

import self_knowing as sk
import thought as th


def test_stored_thoughts_are_fully_self_determined():
    """D = 1 for both stored thoughts (uniform and focused)."""
    assert abs(sk.self_knowing_factor(th.uniform_thought()) - 1.0) < 1e-9
    assert abs(sk.self_knowing_factor(
        th.focused_thought("attention")) - 1.0) < 1e-9


def test_non_stored_basis_state_is_one_third():
    """D = 1/3 for a basis state outside the stored pair."""
    for concept in ("memory", "self", "other"):
        d = sk.self_knowing_factor(th.focused_thought(concept))
        assert abs(d - 1.0 / 3.0) < 1e-9, f"{concept}: D = {d}"


def test_kernel_thought_is_invisible():
    """D = 0 for a thought orthogonal to the stored subspace."""
    kernel = np.array([0.0, 1.0, -1.0, 0.0], dtype=complex) / math.sqrt(2.0)
    assert abs(sk.self_knowing_factor(kernel)) < 1e-9


def test_maximally_mixed_state_is_half():
    """D = rank/dim = 1/2 for the maximally mixed state."""
    mixed = np.eye(4, dtype=complex) / 4.0
    assert abs(sk.self_knowing_of_state(mixed) - 0.5) < 1e-9


def test_gap_is_complement_of_d():
    """The gap is 1 - D."""
    psi = th.focused_thought("other")
    assert abs(sk.self_knowing_gap(psi)
               - (1.0 - sk.self_knowing_factor(psi))) < 1e-9


def test_spearman_is_exact_on_monotone_data():
    """Spearman is -1 on perfectly anti-monotone data, +1 on monotone."""
    assert abs(sk.spearman([1, 2, 3, 4], [4, 3, 2, 1]) + 1.0) < 1e-9
    assert abs(sk.spearman([1, 2, 3, 4], [1, 2, 3, 4]) - 1.0) < 1e-9


def test_claim_iv_verdict_passes():
    """Claim (iv): self-knowing measured via D."""
    verdict = sk.claim_self_knowing_verdict()
    print(f"claim (iv): passed={verdict['passed']}, "
          f"Spearman(sigma, D)={verdict['spearman_sigma_D']:.4f}, "
          f"Spearman(D, coherence)={verdict['spearman_D_coherence']:.4f}, "
          f"Pearson(D, coherence)={verdict['pearson_D_coherence']:.4f}, "
          f"Pearson(D, concurrence)={verdict['pearson_D_concurrence']:.4f}")
    assert verdict["passed"] is True
    assert verdict["checks"]["a_exact_values"] is True
    assert verdict["checks"]["b_D_decays_with_noise"] is True
    assert verdict["checks"]["c_D_tracks_coherence"] is True
    assert verdict["exact_values"]["D_other_basis"] == 1.0 / 3.0
