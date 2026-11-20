# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for the wave direction (v0.25.0, claims
(lxxxviii)-(xcii)): opposite and perpendicular, all
possible directions.

Claims (xci) and (xcii) FAIL — the noisy direction sweep
does not hold from every starting direction. Claim (xci)
fails on two held-out legs: seed 2026 stored Pearson
-0.8828 (the known (xxxii) failure, reproduced exactly)
and seed 2026 opposite D range 0.2490 vs the 0.25 bar (a
miss of 0.0010). Claim (xcii) fails on every seed, and on
the held-out seeds the perpendicular correlation is
POSITIVE (+0.5109 / +0.8297): from the equal
superposition D and C move together, not opposite. Those
failures are asserted here, exactly as measured, with the
frozen thresholds unmoved. See
docs/preregistration-v0.25.0.md. The old verdicts stay on
the record: (xxxii) FAILS as originally stated, and
(xxxv) FAILS as originally stated.
"""

import math

import pytest

import wave_direction as wd


@pytest.fixture(scope="module")
def verdicts():
    return wd.wave_direction_claims()


# ---------------------------------------------------------------------------
# Frozen thresholds
# ---------------------------------------------------------------------------

def test_thresholds_frozen():
    assert wd.PEARSON_D_C_MAX == -0.90
    assert wd.SPEARMAN_D_C_MAX == -0.90
    assert wd.D_RANGE_MIN == 0.25
    assert wd.C_RANGE_MIN == 0.25
    assert wd.EXACT_TOL == 1e-9
    t = wd._thresholds()
    assert t["pearson_d_c_max"] == -0.90
    assert t["spearman_d_c_max"] == -0.90
    assert t["d_range_min"] == 0.25
    assert t["c_range_min"] == 0.25
    assert t["exact_tol"] == 1e-9
    assert wd.N_GRID == 24
    assert len(wd.DIRECTION_GRID) == 24
    assert wd.OPPOSITE_SHIFT == math.pi
    assert wd.PERPENDICULAR_SHIFT == math.pi / 2


# ---------------------------------------------------------------------------
# Slide and rotation pair on the full circle: exact values
# ---------------------------------------------------------------------------

def test_slide_exact_values_on_cardinal_directions():
    rows = {r["theta"]: r for r in wd.slide_full_circle()}
    # theta = 0: stored alone.
    r0 = rows[0.0]
    assert r0["d"] == pytest.approx(1.0, abs=1e-9)
    assert r0["concurrence"] == pytest.approx(0.0, abs=1e-9)
    assert r0["r_stored"] == pytest.approx(1.0, abs=1e-9)
    assert r0["r_kernel"] == pytest.approx(0.0, abs=1e-9)
    # theta = pi/4: the equal superposition.
    rq = rows[math.pi / 4]
    assert rq["d"] == pytest.approx(0.5, abs=1e-9)
    assert rq["concurrence"] == pytest.approx(0.5, abs=1e-9)
    assert rq["r_stored"] == pytest.approx(0.5, abs=1e-9)
    assert rq["r_kernel"] == pytest.approx(0.5, abs=1e-9)
    assert rq["r_split"] == pytest.approx(0.0, abs=1e-9)
    # theta = pi/2: opposite alone.
    rh = rows[math.pi / 2]
    assert rh["d"] == pytest.approx(0.0, abs=1e-9)
    assert rh["concurrence"] == pytest.approx(1.0, abs=1e-9)
    assert rh["r_stored"] == pytest.approx(0.0, abs=1e-9)
    assert rh["r_kernel"] == pytest.approx(1.0, abs=1e-9)
    # theta = pi: back to stored (global phase -1).
    rp = rows[math.pi]
    assert rp["d"] == pytest.approx(1.0, abs=1e-9)
    assert rp["concurrence"] == pytest.approx(0.0, abs=1e-9)
    # theta = 3pi/2: back to opposite.
    r3 = rows[3 * math.pi / 2]
    assert r3["d"] == pytest.approx(0.0, abs=1e-9)
    assert r3["concurrence"] == pytest.approx(1.0, abs=1e-9)
    # C + D = 1 everywhere on the circle.
    for r in rows.values():
        assert r["c_plus_d"] == pytest.approx(1.0, abs=1e-9)
        assert r["d"] == pytest.approx(r["d_exact"], abs=1e-9)
        assert r["concurrence"] == pytest.approx(r["c_exact"], abs=1e-9)
        assert r["r_split"] == pytest.approx(r["split_exact"], abs=1e-9)


def test_rotation_pair_exact_values_on_cardinal_directions():
    rows = {r["theta"]: r for r in wd.rotation_pair_full_circle()}
    # theta = 0: (q1, k1); theta = pi/4: max visibility.
    r0 = rows[0.0]
    assert r0["d1"] == pytest.approx(1.0, abs=1e-9)
    assert r0["d2"] == pytest.approx(0.0, abs=1e-9)
    assert r0["cross_real"] == pytest.approx(0.0, abs=1e-9)
    assert r0["visibility_sweep"] == pytest.approx(0.0, abs=1e-9)
    rq = rows[math.pi / 4]
    assert rq["d1"] == pytest.approx(0.5, abs=1e-9)
    assert rq["d2"] == pytest.approx(0.5, abs=1e-9)
    assert rq["cross_real"] == pytest.approx(-0.5, abs=1e-9)
    assert rq["visibility_sweep"] == pytest.approx(1.0, abs=1e-9)
    # theta = pi/2: (k1, -q1); theta = pi: (-q1, -k1).
    rh = rows[math.pi / 2]
    assert rh["d1"] == pytest.approx(0.0, abs=1e-9)
    assert rh["d2"] == pytest.approx(1.0, abs=1e-9)
    assert rh["cross_real"] == pytest.approx(0.0, abs=1e-9)
    rp = rows[math.pi]
    assert rp["d1"] == pytest.approx(1.0, abs=1e-9)
    assert rp["d2"] == pytest.approx(0.0, abs=1e-9)
    assert rp["cross_real"] == pytest.approx(0.0, abs=1e-9)
    for r in rows.values():
        assert r["cross_imag"] == pytest.approx(0.0, abs=1e-9)
        assert r["cross_real"] == pytest.approx(r["cross_exact"],
                                                abs=1e-9)
        assert r["visibility_sweep"] == pytest.approx(
            r["visibility_exact"], abs=1e-9)
        assert r["visibility_analytic"] == pytest.approx(
            r["visibility_exact"], abs=1e-9)


# ---------------------------------------------------------------------------
# (lxxxviii) Opposite direction: the wave returns to itself
# ---------------------------------------------------------------------------

def test_opposite_shift_worst_differences(verdicts):
    v = verdicts["claim_lxxxviii_opposite_direction"]
    assert v["passed"] is True
    for name, value in v["worst_differences"].items():
        assert value <= 1e-9, name
    # The worst difference is float noise, orders below the bar.
    assert max(v["worst_differences"].values()) <= 1e-12
    assert all(v["checks"].values())


def test_opposite_slide_spot_values():
    # Key by rounded theta: 2*pi*k/24 and pi/12 take different
    # rounding paths to the same float, so exact dict keys fail.
    rows = {round(r["theta"], 9): r
            for r in wd.slide_full_circle()}
    # theta and theta + pi agree on every slide quantity.
    for theta in (0.0, math.pi / 12, math.pi / 4, math.pi / 3):
        a = rows[round(theta, 9)]
        b = rows[round((theta + math.pi) % (2 * math.pi), 9)]
        assert abs(b["d"] - a["d"]) <= 1e-9
        assert abs(b["concurrence"] - a["concurrence"]) <= 1e-9
        assert abs(b["r_stored"] - a["r_stored"]) <= 1e-9
        assert abs(b["r_kernel"] - a["r_kernel"]) <= 1e-9


# ---------------------------------------------------------------------------
# (lxxxix) Perpendicular direction: the swap
# ---------------------------------------------------------------------------

def test_perpendicular_shift_worst_differences(verdicts):
    v = verdicts["claim_lxxxix_perpendicular_direction"]
    assert v["passed"] is True
    for name, value in v["worst_differences"].items():
        assert value <= 1e-9, name
    assert max(v["worst_differences"].values()) <= 1e-12
    assert all(v["checks"].values())


def test_perpendicular_swap_spot_values():
    slide = {r["theta"]: r for r in wd.slide_full_circle()}
    pair = {r["theta"]: r for r in wd.rotation_pair_full_circle()}
    # theta = 0 -> pi/2: D and C exchange, R_s and R_k exchange.
    assert slide[math.pi / 2]["d"] == pytest.approx(
        slide[0.0]["concurrence"], abs=1e-9)
    assert slide[math.pi / 2]["concurrence"] == pytest.approx(
        slide[0.0]["d"], abs=1e-9)
    assert slide[math.pi / 2]["r_stored"] == pytest.approx(
        slide[0.0]["r_kernel"], abs=1e-9)
    # theta = pi/4 -> 3pi/4: the cross term flips sign, |chi| stays.
    assert pair[3 * math.pi / 4]["cross_real"] == pytest.approx(
        -pair[math.pi / 4]["cross_real"], abs=1e-9)
    assert pair[3 * math.pi / 4]["cross_real"] == pytest.approx(
        0.5, abs=1e-9)
    assert pair[3 * math.pi / 4]["visibility_sweep"] == pytest.approx(
        pair[math.pi / 4]["visibility_sweep"], abs=1e-9)


# ---------------------------------------------------------------------------
# (xc) All-directions sweep
# ---------------------------------------------------------------------------

def test_cross_term_profile(verdicts):
    v = verdicts["claim_xc_all_directions"]
    prof = v["profile"]
    assert prof["worst_chi_error"] <= 1e-9
    assert prof["worst_chi_imag"] <= 1e-9
    assert prof["worst_v_error"] <= 1e-9
    assert [round(z, 9) for z in sorted(prof["zeros"])] == [
        0.0, round(math.pi / 2, 9), round(math.pi, 9),
        round(3 * math.pi / 2, 9)]
    assert prof["max_abs_chi"] == pytest.approx(0.5, abs=1e-9)
    assert len(prof["extrema"]) == 4
    for e in prof["extrema"]:
        assert abs(e % (math.pi / 2) - math.pi / 4) <= 1e-9


def test_cascade_direction_table(verdicts):
    v = verdicts["claim_xc_all_directions"]
    assert v["passed"] is True
    assert v["checks"]["a_cross_term_profile_exact"] is True
    assert v["checks"]["b_cascade_death_direction_independent"] is True
    for row in v["cascade_rows"]:
        if row["axis"]:
            assert row["v_stage_1"] == pytest.approx(0.0, abs=1e-9)
        else:
            assert row["v_stage_1"] == pytest.approx(
                abs(math.sin(2 * row["theta"])), abs=1e-9)
        assert all(abs(x) <= 1e-9 for x in row["v_from_stage_2"])
        assert all(not p for p in row["pair_exists_from_stage_2"])
    # Spot values: max visibility at pi/4, zero on the axes.
    by_theta = {r["theta"]: r for r in v["cascade_rows"]}
    assert by_theta[math.pi / 4]["v_stage_1"] == pytest.approx(
        1.0, abs=1e-9)
    assert by_theta[0.0]["v_stage_1"] == pytest.approx(0.0, abs=1e-9)
    assert by_theta[math.pi / 2]["v_stage_1"] == pytest.approx(
        0.0, abs=1e-9)


# ---------------------------------------------------------------------------
# (xci) Noisy direction sweep, stored and opposite — FAIL
# ---------------------------------------------------------------------------

_XCI_EXPECTED = {
    (42, "stored"): (-0.9570, -1.0000, 0.4804, 0.6133),
    (42, "opposite"): (-0.9987, -1.0000, 0.4380, 0.7789),
    (7, "stored"): (-0.9397, -0.9643, 0.5370, 0.5110),
    (7, "opposite"): (-0.9038, -0.9643, 0.2884, 0.4628),
    (1234, "stored"): (-0.9720, -1.0000, 0.4650, 0.7233),
    (1234, "opposite"): (-0.9889, -1.0000, 0.3834, 0.5757),
    (2026, "stored"): (-0.8828, -0.9643, 0.5088, 0.4755),
    (2026, "opposite"): (-0.9710, -1.0000, 0.2490, 0.4107),
}


def test_noisy_stored_opposite_known_values(verdicts):
    v = verdicts["claim_xci_noisy_direction"]
    assert len(v["per_combo"]) == 8
    for r in v["per_combo"]:
        pearson, spearman, d_range, c_range = _XCI_EXPECTED[
            (r["seed"], r["direction"])]
        assert r["pearson_d_c"] == pytest.approx(pearson, abs=1e-4)
        assert r["spearman_d_c"] == pytest.approx(spearman, abs=1e-4)
        assert r["d_range"] == pytest.approx(d_range, abs=1e-4)
        assert r["c_range"] == pytest.approx(c_range, abs=1e-4)


def test_noisy_stored_opposite_fails_honestly(verdicts):
    v = verdicts["claim_xci_noisy_direction"]
    assert v["passed"] is False
    # Seed 2026 stored Pearson is the known (xxxii) failure,
    # reproduced exactly.
    stored_2026 = next(
        r for r in v["per_combo"]
        if r["seed"] == 2026 and r["direction"] == "stored")
    assert stored_2026["pearson_d_c"] == pytest.approx(
        -0.8828, abs=1e-4)
    assert stored_2026["pearson_d_c"] > -0.90
    # Seed 2026 opposite D range misses the 0.25 bar by 0.0010.
    opp_2026 = next(
        r for r in v["per_combo"]
        if r["seed"] == 2026 and r["direction"] == "opposite")
    assert opp_2026["d_range"] == pytest.approx(0.2490, abs=1e-4)
    assert opp_2026["d_range"] < 0.25
    # Everything else in the claim passes its bars.
    assert v["checks"]["spearman_at_most_max"] is True
    assert v["checks"]["c_range_at_least_min"] is True
    assert v["checks"]["pearson_at_most_max"] is False
    assert v["checks"]["d_range_at_least_min"] is False


def test_noisy_stored_opposite_starting_values(verdicts):
    v = verdicts["claim_xci_noisy_direction"]
    for r in v["per_combo"]:
        if r["direction"] == "stored":
            assert r["d_at_sigma_0"] == pytest.approx(1.0, abs=1e-9)
            assert r["c_at_sigma_0"] == pytest.approx(0.0, abs=1e-9)
        else:
            assert r["d_at_sigma_0"] == pytest.approx(0.0, abs=1e-9)
            assert r["c_at_sigma_0"] == pytest.approx(1.0, abs=1e-9)


# ---------------------------------------------------------------------------
# (xcii) Noisy perpendicular direction — FAIL
# ---------------------------------------------------------------------------

_XCII_EXPECTED = {
    42: (-0.7982, -0.9643, 0.2936, 0.2183),
    7: (0.1661, 0.1071, 0.1050, 0.1643),
    1234: (0.5109, 0.7500, 0.1200, 0.2575),
    2026: (0.8297, 0.6071, 0.1285, 0.1252),
}


def test_noisy_perpendicular_known_values(verdicts):
    v = verdicts["claim_xcii_noisy_perpendicular"]
    assert len(v["per_combo"]) == 4
    for r in v["per_combo"]:
        pearson, spearman, d_range, c_range = _XCII_EXPECTED[r["seed"]]
        assert r["pearson_d_c"] == pytest.approx(pearson, abs=1e-4)
        assert r["spearman_d_c"] == pytest.approx(spearman, abs=1e-4)
        assert r["d_range"] == pytest.approx(d_range, abs=1e-4)
        assert r["c_range"] == pytest.approx(c_range, abs=1e-4)
        assert r["d_at_sigma_0"] == pytest.approx(0.5, abs=1e-9)
        # The sigma = 0 concurrence goes through the mixed-state
        # Wootters formula (density matrix + eigendecomposition),
        # whose float error is ~1e-8, not the 1e-15 of the pure
        # formula: the tolerance is 1e-6 here, not 1e-9.
        assert r["c_at_sigma_0"] == pytest.approx(0.5, abs=1e-6)


def test_noisy_perpendicular_fails_honestly(verdicts):
    v = verdicts["claim_xcii_noisy_perpendicular"]
    assert v["passed"] is False
    # On the held-out seeds the correlation is POSITIVE: D and C
    # move together from the equal superposition, not opposite.
    held_out = {r["seed"]: r for r in v["per_combo"]
                if r["seed"] in (1234, 2026)}
    assert held_out[1234]["pearson_d_c"] > 0.0
    assert held_out[2026]["pearson_d_c"] > 0.0
    assert held_out[1234]["spearman_d_c"] > 0.0
    assert held_out[2026]["spearman_d_c"] > 0.0
    # Every seed fails at least one bar; seed 7 fails all four.
    assert v["checks"]["pearson_at_most_max"] is False
    assert v["checks"]["spearman_at_most_max"] is False
    assert v["checks"]["d_range_at_least_min"] is False
    assert v["checks"]["c_range_at_least_min"] is False


# ---------------------------------------------------------------------------
# Aggregate
# ---------------------------------------------------------------------------

def test_aggregate_three_of_five(verdicts):
    assert verdicts["n_claims"] == 5
    assert verdicts["n_passed"] == 3
    assert verdicts["all_pass"] is False
    assert verdicts["headline_allowed"] is False
    assert verdicts["claim_lxxxviii_opposite_direction"]["passed"] is True
    assert verdicts["claim_lxxxix_perpendicular_direction"]["passed"] is True
    assert verdicts["claim_xc_all_directions"]["passed"] is True
    assert verdicts["claim_xci_noisy_direction"]["passed"] is False
    assert verdicts["claim_xcii_noisy_perpendicular"]["passed"] is False


def test_main_runs(capsys):
    wd.main()
    out = capsys.readouterr().out
    assert "claims (lxxxviii)-(xcii): 3/5 pass" in out
    assert "claim (lxxxviii) verdict: PASS" in out
    assert "claim (lxxxix) verdict: PASS" in out
    assert "claim (xc) verdict: PASS" in out
    assert "claim (xci) verdict: FAIL" in out
    assert "claim (xcii) verdict: FAIL" in out
