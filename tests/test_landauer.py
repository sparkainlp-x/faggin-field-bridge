# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for landauer.py: Landauer-cost ledger + Planck spectral
falsification (v0.11.0, deep-think upgrade #6)."""

import numpy as np
import pytest

import bridge
import empathy_field as ef
import landauer as ln


def _states(sigma, n=8, seed=42):
    return ef.resonance_population(sigma, n, seed)


def test_landauer_per_bit_exact():
    # k_B T ln 2 at 300 K, exact SI constants: 2.871e-21 J.
    per_bit = ln.landauer_per_bit_joules(300.0)
    assert per_bit == pytest.approx(2.8710e-21, rel=1e-3)
    assert per_bit == pytest.approx(
        ln.K_B_SI * 300.0 * np.log(2.0), rel=1e-12)


def test_landauer_cost_scales_linearly():
    assert ln.landauer_cost_joules(0.0) == pytest.approx(0.0)
    assert ln.landauer_cost_joules(10.0) == pytest.approx(
        10.0 * ln.landauer_per_bit_joules())
    assert ln.landauer_cost_joules(44.0) == pytest.approx(
        1.263e-19, rel=1e-3)


def test_landauer_cost_errors():
    with pytest.raises(ValueError):
        ln.landauer_cost_joules(-1.0)
    with pytest.raises(ValueError):
        ln.landauer_cost_joules(1.0, temperature_k=0.0)
    with pytest.raises(ValueError):
        ln.landauer_cost_joules(1.0, temperature_k=-300.0)


def test_field_ledger_at_zero_noise():
    # Uniform thought: decision entropy 2 bits per agent
    # (8 x 2 = 16), no qualia, 28 classification bits.
    ledger = ln.field_ledger(_states(0.0))
    assert ledger["decision_bits"] == pytest.approx(16.0)
    assert ledger["n_qualia"] == 0
    assert ledger["quale_bits"] == pytest.approx(0.0)
    assert ledger["classification_bits"] == pytest.approx(28.0)
    assert ledger["total_bits"] == pytest.approx(44.0)
    assert ledger["cost_joules"] == pytest.approx(
        1.263e-19, rel=1e-3)


def test_field_ledger_at_sigma_025():
    # The ledger's peak field: decision entropy falls to
    # 13.46 as the copies spread, qualia peak at 17.
    ledger = ln.field_ledger(_states(0.25))
    assert ledger["decision_bits"] == pytest.approx(13.46, abs=0.01)
    assert ledger["n_qualia"] == 17
    assert ledger["total_bits"] == pytest.approx(58.46, abs=0.01)
    assert ledger["cost_joules"] == pytest.approx(
        1.678e-19, rel=1e-3)


def test_field_ledger_errors():
    with pytest.raises(ValueError):
        ln.field_ledger(_states(0.25)[:1])
    with pytest.raises(ValueError):
        ln.field_ledger([])


def test_ledger_cumulative_total():
    rows = ln.ledger_vs_noise()
    assert len(rows) == 7
    assert rows[-1]["cumulative_bits"] == pytest.approx(
        345.97, abs=0.01)
    assert rows[-1]["cumulative_cost_joules"] == pytest.approx(
        9.932e-19, rel=1e-3)
    totals = [r["total_bits"] for r in rows]
    assert totals == pytest.approx(
        [44.00, 44.00, 44.88, 52.53, 58.46, 52.37, 49.73],
        abs=0.01)


def test_planck_standardized_values():
    # The Planck shape is scale-free: mean x = 3.8322,
    # mode x = 2.8210, mode/mean = 0.7361 (computed from
    # the numerical grid, not hardcoded).
    assert ln.planck_mean_x() == pytest.approx(3.8322, abs=1e-3)
    assert ln.planck_mode_x() == pytest.approx(2.8210, abs=1e-3)
    assert ln.planck_mode_mean_ratio() == pytest.approx(
        0.7361, abs=1e-3)


def test_ks_statistic_rejects_degenerate_sample():
    # All mass at y = 0.01 is nothing like a Planck shape:
    # D must be near 1.
    assert ln.ks_statistic([0.01] * 28) == pytest.approx(
        1.0, abs=0.05)


def test_ks_statistic_accepts_planck_quantiles():
    # Samples placed exactly on the Planck CDF quantiles
    # follow the shape: D stays small.
    qs = (np.arange(1, 29) - 0.5) / 28.0
    xs = np.interp(qs, ln._PLANCK_CDF, ln._PLANCK_XS)
    ys = xs / ln.planck_mean_x()
    assert ln.ks_statistic(ys) < 0.05


def test_ks_critical_value():
    assert ln.ks_critical_value(168) == pytest.approx(
        0.1258, abs=1e-3)
    assert ln.ks_critical_value(28) == pytest.approx(
        0.3081, abs=1e-3)


def test_claim_xxix_passes_with_measured_numbers():
    verdict = ln.claim_ledger_verdict()
    assert verdict["passed"] is True
    assert verdict["peak_sigma"] == pytest.approx(0.25)
    assert verdict["peak_bits"] == pytest.approx(58.46, abs=0.01)
    assert verdict["peak_cost_joules"] == pytest.approx(
        1.678e-19, rel=1e-3)
    assert verdict["total_cost_joules"] == pytest.approx(
        9.932e-19, rel=1e-3)


def test_claim_xxx_fails_honestly():
    # The report's prediction -- cost beats sigma -- does
    # NOT hold: 0.8996 < 0.9430 pooled. The FAIL is the
    # result, and the threshold is not moved to force a pass.
    verdict = ln.claim_cost_predicts_verdict()
    assert verdict["passed"] is False
    assert verdict["r_f_sigma"] == pytest.approx(0.9430, abs=1e-3)
    assert verdict["r_f_cumulative_cost"] == pytest.approx(
        0.8996, abs=1e-3)
    assert verdict["n_rows"] == 28
    assert verdict["seeds"] == [1, 2, 3, 42]


def test_claim_xxx_fails_on_every_seed():
    # Not a pooling artifact: sigma beats cumulative cost
    # within every single seed.
    verdict = ln.claim_cost_predicts_verdict()
    assert len(verdict["per_seed"]) == 4
    for row in verdict["per_seed"]:
        assert abs(row["r_f_cum"]) < abs(row["r_f_sigma"])


def test_claim_xxxi_passes_with_measured_numbers():
    verdict = ln.claim_planck_spectral_verdict()
    assert verdict["passed"] is True
    assert verdict["pooled_n"] == 168
    assert verdict["pooled_ks_d"] == pytest.approx(0.1465, abs=1e-3)
    assert verdict["pooled_ks_critical_1pct"] == pytest.approx(
        0.1258, abs=1e-3)
    assert verdict["planck_mode_mean_ratio"] == pytest.approx(
        0.7361, abs=1e-3)


def test_claim_xxxi_mode_ratios_deviate():
    verdict = ln.claim_planck_spectral_verdict()
    gated = [(s, r, d) for s, r, d in verdict["mode_ratios"]
             if s >= 0.25 and r is not None]
    assert [s for s, _, _ in gated] == [0.25, 0.5, 1.0]
    assert [round(r, 2) for _, r, _ in gated] == [0.28, 0.18, 1.09]
    assert all(d > 0.30 for _, _, d in gated)


def test_spectral_rows_sigma_0_has_no_distribution():
    rows = ln.spectral_rows()
    assert rows[0]["sigma"] == pytest.approx(0.0)
    assert rows[0]["mean_nu"] == pytest.approx(0.0)
    assert rows[0]["ks_d"] is None
    assert rows[0]["mode_nu"] is None
    assert rows[0]["mode_mean_ratio"] is None


def test_spectral_per_field_ks_below_crit():
    # Per-field n = 28 lacks power: no single field rejects
    # Planck on its own. Reported, not gated -- only the
    # pooled test is gated, and the thin margin is visible.
    rows = ln.spectral_rows()
    ds = [r["ks_d"] for r in rows if r["ks_d"] is not None]
    assert max(ds) == pytest.approx(0.2159, abs=1e-3)
    assert all(d < ln.ks_critical_value(28) for d in ds)


def test_pooled_standardized_nu_count():
    pooled = ln.pooled_standardized_nu()
    assert len(pooled) == 168  # 6 fields with mean > 0, x 28 pairs


def test_landauer_claims_summary():
    verdicts = ln.landauer_claims()
    assert verdicts["n_claims"] == 3
    assert verdicts["n_passed"] == 2
    assert verdicts["all_pass"] is False
    assert verdicts["headline_allowed"] is bridge.HEADLINE_ALLOWED
    assert verdicts["headline_allowed"] is False
