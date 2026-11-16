# test_cost.py
#
# Tests for cost.py (entropy).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import math

import numpy as np
import pytest

import cost


def test_shannon_uniform_is_log2_n():
    """Uniform distribution over n outcomes: S = log2(n) bits."""
    assert abs(cost.shannon_entropy(np.ones(32)) - 5.0) < 1e-12
    assert abs(cost.shannon_entropy(np.ones(2)) - 1.0) < 1e-12


def test_shannon_certain_is_zero():
    """A certain outcome carries no entropy."""
    assert cost.shannon_entropy([1.0, 0.0, 0.0]) == 0.0
    assert cost.shannon_entropy_of_state(np.array([1.0, 0.0])) == 0.0


def test_von_neumann_pure_is_zero():
    """A pure state has zero von Neumann entropy."""
    rho = np.array([[1.0, 0.0], [0.0, 0.0]])
    assert cost.von_neumann_entropy(rho) == 0.0


def test_von_neumann_maximally_mixed_qubit_is_one():
    """A maximally mixed qubit has 1 bit of entropy."""
    rho = 0.5 * np.eye(2)
    assert abs(cost.von_neumann_entropy(rho) - 1.0) < 1e-12


def test_normalized_cost_bounds_and_errors():
    """C = S / S_max is in [0, 1]; bad inputs raise."""
    assert cost.normalized_entropy_cost(0.0, 1.0) == 0.0
    assert cost.normalized_entropy_cost(1.0, 1.0) == 1.0
    assert cost.normalized_entropy_cost(0.5, 1.0) == 0.5
    assert cost.normalized_entropy_cost(2.0, 1.0) == 1.0  # clipped
    assert cost.normalized_entropy_cost(-0.5, 1.0) == 0.0  # clipped
    with pytest.raises(ValueError):
        cost.normalized_entropy_cost(0.5, 0.0)


def test_tensor_membrane_entropy_reproduces():
    """Mean single-qubit entropy reproduces 0.955 bits (within 0.02).

    Recomputed fresh on the 7-qubit network (19 Haar unitaries,
    layers 6/7/6, seed 42), not copied from the repo's output.
    """
    value = cost.tensor_membrane_mean_entropy()
    print(f"\ntensor-membrane entropy: {value:.4f} bits vs reported "
          f"{cost.TENSOR_MEMBRANE_ENTROPY_REPORTED} bits")
    assert abs(value - cost.TENSOR_MEMBRANE_ENTROPY_REPORTED) < 0.02


def test_tensor_membrane_entropy_seed_spread():
    """The 0.9553 headline is one draw: spread over seeds 0..19.

    Mean 0.9639, standard deviation 0.0128 (n = 20). The seed-42
    value 0.9553 sits 0.0086 below the 20-seed mean — within one
    standard deviation — so the headline is a typical draw, not
    an outlier. But the spread is real: it is near-saturated,
    Page-like behaviour (random circuits concentrate near the
    1-bit maximum), and a +-0.013 move in C moves A by -+0.013,
    about 30% of the primary attunement 0.0447. The headline is
    kept (seed 42); the spread is reported alongside it.
    """
    import statistics

    values = [cost.tensor_membrane_mean_entropy(seed=s) for s in range(20)]
    mean = statistics.mean(values)
    std = statistics.stdev(values)
    print(f"\nseed spread (n=20): mean {mean:.4f}, std {std:.4f}, "
          f"min {min(values):.4f}, max {max(values):.4f}")
    assert mean == pytest.approx(0.9639, abs=1e-3)
    assert std == pytest.approx(0.0128, abs=1e-3)
    assert min(values) == pytest.approx(0.9276, abs=1e-3)
    assert max(values) == pytest.approx(0.9775, abs=1e-3)
    assert abs(cost.tensor_membrane_mean_entropy(seed=42) - mean) < std


def test_tensor_membrane_cost_is_entropy_over_one_bit():
    """Single-qubit maximum is 1 bit, so C = S here."""
    assert abs(cost.tensor_membrane_cost()
               - cost.tensor_membrane_mean_entropy()) < 1e-12
    assert 0.0 <= cost.tensor_membrane_cost() <= 1.0


def test_shannon_entropy_of_state_max():
    """A uniform 32-dim state has Shannon entropy 5 bits."""
    state = np.ones(32) / math.sqrt(32.0)
    assert abs(cost.shannon_entropy_of_state(state) - 5.0) < 1e-9
