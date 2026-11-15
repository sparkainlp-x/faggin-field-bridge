# test_attunement.py
#
# Tests for attunement.py (observer, calibrator, A, calibration identity).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

from dataclasses import FrozenInstanceError

import pytest

import attunement as at


def test_attunement_definition_at_zero_delta():
    """At delta = 0, A = U - C."""
    assert at.attunement(0.9, 0.3, 0.0) == pytest.approx(0.6)
    assert at.attunement(0.5, 0.5, 0.0) == pytest.approx(0.0)
    assert at.attunement(0.2, 0.8, 0.0) == pytest.approx(-0.6)


def test_attunement_bounds():
    """A is always in [-1, 1], even at the extremes."""
    assert at.attunement(1.0, 0.0, 0.05) == pytest.approx(1.0)  # clipped
    assert at.attunement(0.0, 1.0, -0.05) == pytest.approx(-1.0)
    for u in (0.0, 0.25, 0.5, 0.75, 1.0):
        for c in (0.0, 0.25, 0.5, 0.75, 1.0):
            for d in (-0.05, 0.0, 0.05):
                a = at.attunement(u, c, d)
                assert -1.0 <= a <= 1.0


def test_attunement_monotone_in_unity():
    """More unity means more attunement, at fixed cost."""
    for c in (0.0, 0.3, 0.9):
        prev = None
        for u in (0.0, 0.25, 0.5, 0.75, 1.0):
            a = at.attunement(u, c, 0.0)
            if prev is not None:
                assert a > prev
            prev = a


def test_attunement_monotone_decreasing_in_cost():
    """More entropy cost means less attunement, at fixed unity."""
    for u in (0.2, 0.6, 1.0):
        prev = None
        for c in (0.0, 0.25, 0.5, 0.75, 1.0):
            a = at.attunement(u, c, 0.0)
            if prev is not None:
                assert a < prev
            prev = a


def test_attunement_calibrator_moves_at_most_005_times_unity():
    """The bounded calibrator can move A by at most 0.05 * U.

    The move is exactly 0.05 * U except where the [-1, 1] clip
    binds (U = 1, C = 0 at delta = +0.05 clips at 1.0)."""
    for u, c in ((1.0, 0.0), (0.9, 0.3), (0.5, 0.5)):
        base = at.attunement(u, c, 0.0)
        up = at.attunement(u, c, 0.05)
        down = at.attunement(u, c, -0.05)
        assert up - base <= 0.05 * u + 1e-12
        assert base - down <= 0.05 * u + 1e-12
    # Exact away from the clip.
    assert (at.attunement(0.9, 0.3, 0.05)
            - at.attunement(0.9, 0.3, 0.0)) == pytest.approx(0.05 * 0.9)
    assert (at.attunement(0.9, 0.3, 0.0)
            - at.attunement(0.9, 0.3, -0.05)) == pytest.approx(0.05 * 0.9)


def test_observer_is_read_only():
    """The observer holds no mutable state and returns frozen data.

    - It has no attributes (no __dict__ entries).
    - Two identical observations are equal.
    - The returned observation is frozen: editing it raises.
    """
    obs = at.AttunementObserver()
    assert obs.__dict__ == {}
    o1 = obs.observe(0.9, 0.3)
    o2 = obs.observe(0.9, 0.3)
    assert o1 == o2
    assert o1.attunement == pytest.approx(0.6)
    with pytest.raises(FrozenInstanceError):
        o1.unity = 0.5
    assert obs.__dict__ == {}


def test_observer_from_entropy_normalizes_cost():
    """observe_from_entropy computes C = S / S_max."""
    obs = at.AttunementObserver()
    o = obs.observe_from_entropy(0.9, 0.9553, 1.0)
    assert o.cost == pytest.approx(0.9553)
    assert o.entropy_bits == pytest.approx(0.9553)
    assert o.max_entropy_bits == pytest.approx(1.0)
    assert o.attunement == pytest.approx(0.9 - 0.9553)


def test_observer_rejects_out_of_range():
    """Unity and cost outside [0, 1] raise."""
    obs = at.AttunementObserver()
    with pytest.raises(ValueError):
        obs.observe(1.5, 0.3)
    with pytest.raises(ValueError):
        obs.observe(0.5, -0.1)
    with pytest.raises(ValueError):
        obs.observe_from_entropy(0.5, 1.0, 0.0)


def test_calibrator_clips_at_plus_minus_005():
    """set_delta never lets delta exceed [-0.05, 0.05]."""
    cal = at.AttunementCalibrator()
    assert cal.set_delta(1.0) == pytest.approx(0.05)
    assert cal.delta == pytest.approx(0.05)
    assert cal.set_delta(-1.0) == pytest.approx(-0.05)
    assert cal.delta == pytest.approx(-0.05)
    assert cal.set_delta(0.03) == pytest.approx(0.03)
    assert cal.set_delta(0.0) == pytest.approx(0.0)


def test_calibrator_best_delta_is_plus_005():
    """The sweep finds +0.05 (A is linear in delta, slope U >= 0)."""
    cal = at.AttunementCalibrator()
    best_d, best_a = cal.best_delta(0.9, 0.3)
    assert best_d == pytest.approx(0.05)
    assert best_a == pytest.approx(at.attunement(0.9, 0.3, 0.05))
    # The sweep does not change the calibrator's held delta.
    assert cal.delta == pytest.approx(0.0)


def test_gap_calibration_identity():
    """Best bounded calibration buys exactly log10(1/0.95) orders.

    The identity 0.022276..., reproduced by the sweep, not fitted.
    """
    gap = at.gap_calibration(1.68e19)
    assert gap["best_delta"] == pytest.approx(-0.05)
    assert gap["improvement_orders"] == pytest.approx(
        at.CALIBRATION_IMPROVEMENT_ORDERS, abs=1e-9
    )
    assert gap["improvement_orders"] == pytest.approx(0.022276, abs=1e-6)
    print(f"\ncalibration improvement: {gap['improvement_orders']:.6f} "
          f"orders (identity {at.CALIBRATION_IMPROVEMENT_ORDERS:.6f})")


def test_empathy_proxy_default_and_validation():
    """Default empathy is the notebook's reported 0.5503; bad values raise."""
    assert at.empathy_proxy() == pytest.approx(0.5503)
    assert at.empathy_proxy(0.3) == pytest.approx(0.3)
    with pytest.raises(ValueError):
        at.empathy_proxy(1.5)
    with pytest.raises(ValueError):
        at.empathy_proxy(-0.1)
