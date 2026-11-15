# test_unity.py
#
# Tests for unity.py (spooky correlation).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import numpy as np

import unity


def test_spooky_bounds():
    """Spooky correlation is always in [0, 1]."""
    rng = np.random.default_rng(7)
    state = rng.standard_normal(32)
    state = state / np.linalg.norm(state)
    for sigma in (0.0, 0.01, 0.1, 0.5, 1.0):
        v = unity.spooky_correlation(state, sigma)
        assert 0.0 <= v <= 1.0
    for p in (0.0, 0.2, 0.5):
        v = unity.spooky_correlation_erasure(state, p)
        assert 0.0 <= v <= 1.0


def test_spooky_identical_copies_is_one():
    """Zero noise: every copy is the state, so spooky = 1.0."""
    rng = np.random.default_rng(7)
    state = rng.standard_normal(32)
    state = state / np.linalg.norm(state)
    assert unity.spooky_correlation(state, 0.0) == 1.0
    assert unity.spooky_correlation_erasure(state, 0.0) == 1.0


def test_spooky_independent_states_is_low():
    """Independent random states are nearly orthogonal in 32 dims:
    mean pairwise |dot| is small, far below the Omega-Genesis 0.9."""
    rng = np.random.default_rng(7)
    vecs = []
    for _ in range(5):
        v = rng.standard_normal(32)
        vecs.append(v / np.linalg.norm(v))
    assert unity.spooky_from_vectors(vecs) < 0.4


def test_spooky_does_not_mutate_state():
    """Computing spooky never modifies the input state."""
    rng = np.random.default_rng(7)
    state = rng.standard_normal(32)
    state = state / np.linalg.norm(state)
    before = state.copy()
    unity.spooky_correlation(state, 0.1)
    unity.spooky_correlation_erasure(state, 0.2)
    assert np.array_equal(state, before)


def test_debroglie_spooky_reproduces():
    """de Broglie spooky reproduces 0.99999995 at sigma = 0.01."""
    value = unity.debroglie_spooky(noise_sigma=0.01)
    assert abs(value - unity.DEBROGLIE_SPOOKY_REPORTED) < 1e-6
    assert abs(value - 0.99999995) < 1e-6


def test_debroglie_spooky_other_sigmas():
    """The same reproduction at sigma = 0.05 and 0.50."""
    assert abs(unity.debroglie_spooky(noise_sigma=0.05) - 0.99999864) < 1e-6
    assert abs(unity.debroglie_spooky(noise_sigma=0.50) - 0.99964289) < 1e-6


def test_debroglie_state_vector_shape():
    """The de Broglie state is 10 log-gaps, all positive; the
    macroscopic cases (indices 4-9) are all >= 10 orders short.
    The electron and proton are not macroscopic, so their gaps
    are smaller (4.7-8.4 orders) -- the FAIL criterion applies
    to macroscopic masses only."""
    vec = unity.debroglie_state_vector()
    assert vec.shape == (10,)
    assert np.all(vec > 0.0)
    assert np.all(vec[4:] > 10.0)


def test_omega_genesis_synthetic_in_regime():
    """Synthetic Omega-Genesis spooky is in the notebook's regime.

    The notebook's reported 0.9005 comes from its evolved state,
    which is unavailable, so the synthetic reproduction (32-dim
    state, 20% erasure, seed 42) is 0.837 -- the same regime, not
    the same number. The test asserts the regime (within 0.10 of
    the reported value) and prints both, so the difference is
    visible, not hidden.
    """
    value = unity.omega_genesis_spooky()
    print(f"\nOmega-Genesis spooky: synthetic {value:.4f} vs "
          f"reported {unity.OMEGA_GENESIS_SPOOKY_REPORTED} "
          f"(diff {abs(value - unity.OMEGA_GENESIS_SPOOKY_REPORTED):.4f})")
    assert 0.75 <= value <= 0.98
    assert abs(value - unity.OMEGA_GENESIS_SPOOKY_REPORTED) < 0.10


def test_cci_bounds():
    """The conscious coherence index is in [0, 1]."""
    rng = np.random.default_rng(7)
    for _ in range(5):
        state = rng.standard_normal(32)
        cci = unity.conscious_coherence_index(state)
        assert 0.0 <= cci <= 1.0
    # A near-uniform state has a high CCI; a spiky one lower.
    uniform = np.ones(32) + 0.01 * rng.standard_normal(32)
    spiky = np.zeros(32)
    spiky[0] = 1.0
    assert (unity.conscious_coherence_index(uniform)
            > unity.conscious_coherence_index(spiky))
