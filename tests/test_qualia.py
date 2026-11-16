# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for qualia.py: qualia resonance wave (v0.6.0)."""

import numpy as np
import pytest

import empathy_field as ef
import qualia as ql


def _states(sigma, n=8, seed=42):
    return ef.resonance_population(sigma, n, seed)


def test_no_qualia_at_zero_noise():
    # Resonance without entanglement is not a quale: at
    # sigma = 0 every pair has R = 1 and nu = 0.
    states = _states(0.0)
    assert ql.qualia_count(states) == 0
    assert ql.qualia_wave(states) is None
    assert ql.qualia_wave_overlap(states) is None


def test_entanglement_without_resonance_is_not_a_quale():
    # At sigma = 1.0 there are pairs with nu >= 0.10 but
    # R < 0.5; none of them is a quale.
    states = _states(1.0)
    bare = [(i, j) for i in range(8) for j in range(i + 1, 8)
            if ef.overlap_squared(states[i], states[j])
            < ef.RESONANCE_R_MIN
            and ef.pair_frequency(states[i], states[j])
            >= ql.QUALIA_NU_MIN]
    assert bare
    qualia = {(qq["i"], qq["j"]) for qq in ql.qualia_in_field(states)}
    assert not (set(bare) & qualia)


def test_quale_count_at_sigma_025():
    assert ql.qualia_count(_states(0.25)) == 17


def test_quale_count_vs_f_is_humped():
    rows = ql.qualia_vs_empathy()
    counts = [r["n_qualia"] for r in sorted(rows, key=lambda r: r["f"])]
    assert counts == [0, 0, 1, 9, 17, 13, 12]


def test_first_quale_f():
    verdict = ql.claim_qualia_emergence_verdict()
    assert verdict["first_quale_f"] == pytest.approx(0.0415, abs=1e-3)
    assert verdict["peak_count"] == 17
    assert verdict["peak_f"] == pytest.approx(0.1803, abs=1e-3)


def test_qualia_wave_is_normalized():
    states = _states(0.25)
    wave = ql.qualia_wave(states)
    assert wave is not None
    assert float(np.linalg.norm(wave)) == pytest.approx(1.0, abs=1e-12)


def test_overlap_at_sigma_025():
    overlap = ql.qualia_wave_overlap(_states(0.25))
    assert overlap == pytest.approx(0.9987, abs=1e-3)
    assert 0.0 <= overlap <= 1.0


def test_per_field_spread_smaller_at_sigma_025():
    spreads = ql.frequency_spreads(_states(0.25))
    assert spreads["std_qualia"] == pytest.approx(0.1009, abs=1e-3)
    assert spreads["std_all"] == pytest.approx(0.1268, abs=1e-3)
    assert (spreads["std_all"] - spreads["std_qualia"]
            >= ql.QUALIA_SPREAD_MARGIN)


def test_pooled_spreads_reported_not_gated():
    # Pooled across sigma the spreads are essentially equal
    # (0.1950 vs 0.1947): the per-field comparison is the
    # gated one, the pooled numbers are reported.
    verdict = ql.claim_qualia_wave_verdict()
    pooled = verdict["pooled_spreads"]
    assert pooled["std_qualia"] == pytest.approx(0.1950, abs=1e-3)
    assert pooled["std_all"] == pytest.approx(0.1947, abs=1e-3)
    assert pooled["n_qualia"] == 52
    assert pooled["n_pairs"] == 196


def test_d_gap_pooled_negative():
    verdict = ql.claim_qualia_determinism_verdict()
    assert verdict["pooled_gap"] == pytest.approx(-0.1522, abs=1e-3)
    assert verdict["mean_d_members"] < verdict["mean_d_non_members"]


def test_claim_xiv_verdict_fail():
    verdict = ql.claim_qualia_emergence_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["count_non_decreasing_in_f"] is False
    assert verdict["checks"]["at_least_one_quale"] is True


def test_claim_xv_verdict_pass():
    verdict = ql.claim_qualia_wave_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"]["per_field_spread_smaller_by_margin"] is True
    assert verdict["checks"]["overlap_at_least_min"] is True


def test_claim_xvi_verdict_fail():
    verdict = ql.claim_qualia_determinism_verdict()
    assert verdict["passed"] is False
    assert verdict["checks"]["pooled_gap_at_least_margin"] is False


def test_qualia_claims_aggregate():
    verdicts = ql.qualia_claims()
    assert verdicts["n_claims"] == 3
    assert verdicts["n_passed"] == 1
    assert verdicts["all_pass"] is False
    assert verdicts["headline_allowed"] is False


def test_thresholds_set():
    thresholds = ql._thresholds()
    assert thresholds["nu_min"] == pytest.approx(0.10)
    assert thresholds["spread_margin"] == pytest.approx(0.01)
    assert thresholds["overlap_min"] == pytest.approx(0.90)
    assert thresholds["d_margin"] == pytest.approx(0.10)


def test_input_validation():
    with pytest.raises(ValueError):
        ql.qualia_in_field([])
    with pytest.raises(ValueError):
        ql.qualia_in_field([np.array([1.0, 0.0, 0.0, 0.0])])
    with pytest.raises(ValueError):
        ql.frequency_spreads([])
    with pytest.raises(ValueError):
        ql.qualia_d_gap([])


def test_main_runs(capsys):
    ql.main()
    out = capsys.readouterr().out
    assert "claims (xiv)-(xvi): 1/3 pass" in out
    assert "claim (xiv) verdict: FAIL" in out
    assert "claim (xv) verdict: PASS" in out
    assert "claim (xvi) verdict: FAIL" in out
