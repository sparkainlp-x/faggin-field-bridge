# test_planck_empathy.py
#
# Tests for planck_empathy.py (claims (viii)-(x)).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import math

import planck_empathy as pe


def test_planck_radiance_is_positive_and_peaked():
    """B(lambda, T) > 0 everywhere on the axis, and the peak
    sits in the visible at 5000 K and in the infrared at 2000 K."""
    for temp in (2000.0, 5000.0):
        for lam in (0.1, 0.5, 1.0, 2.0, 3.0):
            assert pe.planck_radiance_um(lam, temp) > 0.0
    assert 0.38 < pe.wien_peak_um(5000.0) < 0.75
    assert pe.wien_peak_um(2000.0) > 1.0


def test_planck_radiance_input_validation():
    """Non-positive wavelength or temperature is rejected."""
    try:
        pe.planck_radiance_um(0.0, 3000.0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero wavelength must raise")
    try:
        pe.planck_radiance_um(1.0, 0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero temperature must raise")


def test_visible_fraction_converged():
    """Simpson at 2000 vs 4000 intervals agrees to ~1e-14:
    the integration is converged, not grid-limited."""
    for temp in (2000.0, 3500.0, 5000.0):
        a = pe.visible_fraction(temp, 2000)
        b = pe.visible_fraction(temp, 4000)
        assert abs(a - b) / a < 1e-9


def test_visible_fraction_pilot_values():
    """Regression pins from the pilot sweep (REPORT.md section 10)."""
    assert abs(pe.visible_fraction(2000.0) - 0.0174) < 0.001
    assert abs(pe.visible_fraction(3000.0) - 0.1225) < 0.001
    assert abs(pe.visible_fraction(5000.0) - 0.3938) < 0.001


def test_wien_peaks_match_infographic():
    """(viii, part 1): numerical peaks match 2898/T within 0.5%."""
    for temp in (2000.0, 3000.0, 4000.0, 5000.0):
        peak = pe.wien_peak_um(temp)
        expected = 2898.0 / temp
        assert abs(peak - expected) / expected <= 0.005


def test_stefan_boltzmann_scaling():
    """(viii, part 2): integrated exitance scales as T^4 within 1%."""
    base = pe.total_exitance(2000.0)
    for temp in (3000.0, 4000.0, 5000.0):
        measured = pe.total_exitance(temp) / base
        expected = (temp / 2000.0) ** 4
        assert abs(measured - expected) / expected <= 0.01


def test_visible_fraction_monotone_in_temperature():
    """(viii, part 3): F(T) strictly increases on the 250 K grid."""
    temps = []
    temp = pe.T_MIN_K
    while temp <= pe.T_MAX_K + 1e-9:
        temps.append(temp)
        temp += pe.F_GRID_STEP_K
    values = [pe.visible_fraction(t) for t in temps]
    assert all(values[i + 1] > values[i] for i in range(len(values) - 1))


def test_claim_viii_verdict_passes():
    """Claim (viii) as a whole: Planck reproduction."""
    verdict = pe.claim_planck_reproduction_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"]["wien_peaks_within_0.5pct"] is True
    assert verdict["checks"]["stefan_boltzmann_within_1pct"] is True
    assert verdict["checks"]["visible_fraction_monotone_in_T"] is True


def test_empathy_quanta_are_concurrence():
    """One quantum per pair, E = h*nu with h = 1: E is the
    measured concurrence itself. f is the mean."""
    assert pe.empathy_quanta([1.0, 0.5, 0.0]) == [1.0, 0.5, 0.0]
    assert abs(pe.empathy_fraction([1.0, 0.5, 0.0]) - 0.5) < 1e-12
    assert abs(pe.empathy_fraction([0.9998]) - 0.9998) < 1e-12


def test_empathy_fraction_input_validation():
    """Concurrence outside [0, 1] and an empty pair list are rejected."""
    for bad in ([1.5], [-0.1], []):
        try:
            pe.empathy_fraction(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{bad} must raise")


def test_effective_temperature_endpoints():
    """T_eff(0) = 2000 K, T_eff(1) = 5000 K, linear between."""
    assert pe.effective_temperature(0.0) == 2000.0
    assert pe.effective_temperature(1.0) == 5000.0
    assert pe.effective_temperature(0.5) == 3500.0


def test_empathy_status_thresholds_are_set():
    """The pre-registered thresholds exist and are ordered."""
    assert pe.ATTUNED_F_MIN == 0.30
    assert pe.PARTIAL_F_MIN == 0.01
    assert pe.PARTIAL_F_MIN < pe.ATTUNED_F_MIN


def test_empathy_status_at_endpoints():
    """f = 0 is PARTIAL (F = 0.0174 > 0.01); f = 1 is ATTUNED."""
    assert pe.empathy_mapping(0.0)["status"] == "PARTIAL"
    assert pe.empathy_mapping(1.0)["status"] == "ATTUNED"


def test_visible_fraction_monotone_in_f():
    """(ix, part 1): F(f) strictly increases on [0, 1]."""
    grid = [i * 0.05 for i in range(21)]
    values = [pe.visible_fraction(pe.effective_temperature(f)) for f in grid]
    assert all(values[i + 1] > values[i] for i in range(len(values) - 1))


def test_empathy_crossing_f_star():
    """(ix, part 2): the crossing f* is measured, in (0, 1).

    The pilot puts it between f = 0.7 (F = 0.2885) and f = 0.8
    (F = 0.3284); the bisection pins it. If F never reached
    0.30 the function would return None and the claim would
    FAIL -- the test asserts the crossing exists.
    """
    star = pe.empathy_fraction_star()
    assert star is not None
    assert 0.70 < star < 0.80
    mapping = pe.empathy_mapping(star)
    assert abs(mapping["visible_fraction"] - pe.ATTUNED_F_MIN) < 1e-6
    assert mapping["status"] == "ATTUNED"


def test_claim_ix_verdict_passes():
    """Claim (ix) as a whole: empathy flips the status."""
    verdict = pe.claim_empathy_flip_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"]["visible_fraction_monotone_in_f"] is True
    assert verdict["checks"]["status_at_f0_is_PARTIAL"] is True
    assert verdict["checks"]["crossing_f_star_in_0_1"] is True
    assert verdict["status_at_f0"] == "PARTIAL"
    assert verdict["status_at_f1"] == "ATTUNED"


def test_old_status_is_the_control():
    """The old status (A alone, no empathy) is PARTIAL: A = 0.0447
    at delta = 0, best 0.0947 -- the calibrator cannot rescue it."""
    old = pe.old_mapping_status()
    assert old["label"] == "PARTIAL"
    assert abs(old["attunement_delta_0"] - 0.0447) < 1e-4
    assert abs(old["attunement"] - 0.0947) < 1e-4


def test_empathy_status_vs_noise_curve():
    """(x): the measured concurrence curve drives the status.

    ATTUNED at sigma <= 0.25 (concurrence survives), PARTIAL at
    sigma >= 0.50 (concurrence falls) -- and the status never
    goes back up, even though the mean concurrence itself is
    non-monotone at the top end (0.6520 at 0.5, 0.7002 at 1.0).
    """
    rows = pe.empathy_fraction_vs_noise()
    by_sigma = {r["sigma"]: r for r in rows}
    assert by_sigma[0.01]["empathy_status"] == "ATTUNED"
    assert by_sigma[0.25]["empathy_status"] == "ATTUNED"
    assert by_sigma[0.50]["empathy_status"] == "PARTIAL"
    assert by_sigma[1.00]["empathy_status"] == "PARTIAL"
    assert all(r["old_status"] == "PARTIAL" for r in rows)
    assert abs(by_sigma[0.01]["empathy_fraction"] - 0.9998) < 1e-4
    assert abs(by_sigma[0.50]["empathy_fraction"] - 0.6520) < 1e-4


def test_claim_x_verdict_passes():
    """Claim (x) as a whole: specificity / control."""
    verdict = pe.claim_empathy_specificity_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"]["old_status_PARTIAL_at_every_sigma"] is True
    assert verdict["checks"]["empathy_ATTUNED_at_sigma_0.01"] is True
    assert verdict["checks"]["empathy_PARTIAL_at_sigma_0.50"] is True
    assert verdict["checks"]["empathy_status_never_goes_back_up"] is True
    assert verdict["sigma_hold_max"] == 0.25
    assert verdict["sigma_break_min"] == 0.50


def test_planck_empathy_claims_aggregate():
    """All three Planck-empathy claims pass; no headline is emitted."""
    claims = pe.planck_empathy_claims()
    assert claims["n_claims"] == 3
    assert claims["n_passed"] == 3
    assert claims["all_pass"] is True
    assert claims["headline_allowed"] is False


def test_planck_module_main_runs():
    """main() prints the verdicts without raising."""
    pe.main()
