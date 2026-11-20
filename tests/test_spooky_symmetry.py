# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for spooky symmetry (v0.28.0, claims
(cvii)-(cix)): the spooky correlation under the
V4-full orbit average, and the fresh-seed
correction to the v0.27.0 rescue story.

All three claims PASS as measured. (cvii): max
|dU| 0.002274 at sigma <= 0.05 (bar 0.003) and
0.009930 at sigma <= 0.1 (bar 0.01 — thin by
construction, margin 0.00007, disclosed), and the
break at sigma = 0.5 (0.183794 > 0.01); the worst
case is always seed 7 perpendicular. (cviii): the
CORRECTION — V4-full stored Pearson <= -0.90 on
exactly 3/5 fresh seeds [2, 99, 777], plain n=20
on exactly 4/5 [2, 99, 777, 2024]; V4 BREAKS seed
2024 (-0.9527 -> -0.8830); seed 5 fails under
every method (-0.6814 / -0.8338 / -0.8749). Claim
(c) stands as measured on the file seeds. (cix):
V4-full perpendicular D range < 0.25 on every
fresh seed (max 0.1767), Pearson positive on 6/9
seeds plain and 5/9 under V4-full. See
docs/preregistration-v0.28.0.md.
"""

import math

import numpy as np
import pytest

import spooky_symmetry as sp


@pytest.fixture(scope="module")
def verdicts():
    return sp.spooky_symmetry_claims()


# ---------------------------------------------------------------------------
# Frozen thresholds
# ---------------------------------------------------------------------------

def test_thresholds_are_frozen():
    t = sp._thresholds()
    assert t["exact_tol"] == 1e-9
    assert t["du_max_low_sigma"] == 0.003
    assert t["du_max_mid_sigma"] == 0.01
    assert t["pearson_d_c_max"] == -0.90


# ---------------------------------------------------------------------------
# The orbit construction
# ---------------------------------------------------------------------------

def test_du_zero_at_sigma_zero():
    for seed in sp.ALL_SEEDS:
        for theta in sp.ALL_NOISY_DIRECTIONS:
            table = sp.spooky_orbit_table(seed, theta)
            assert table["rows"][0]["sigma"] == 0.0
            assert table["rows"][0]["du"] == 0.0


def test_orbit_copies_are_twenty_normalized():
    copies = sp.orbit_copies(42, 0.0, 0.25)
    assert len(copies) == 20
    for v in copies:
        assert abs(np.linalg.norm(v) - 1.0) <= 1e-12


def test_du_worst_case_is_seed7_perpendicular():
    by_sigma = sp.max_du_by_sigma()
    assert by_sigma[0.05]["max_abs_du"] == pytest.approx(
        0.002274, abs=1e-6)
    assert by_sigma[0.05]["worst_at"] == (7, math.pi / 4)
    assert by_sigma[0.1]["max_abs_du"] == pytest.approx(
        0.009930, abs=1e-6)
    assert by_sigma[0.1]["worst_at"] == (7, math.pi / 4)
    assert by_sigma[0.5]["max_abs_du"] == pytest.approx(
        0.183794, abs=1e-6)


# ---------------------------------------------------------------------------
# Claim verdicts
# ---------------------------------------------------------------------------

def test_claim_cvii_passes_and_sigma_01_leg_is_thin(
        verdicts):
    cvii = verdicts["claim_cvii_spooky_preserved"]
    assert cvii["passed"] is True
    assert cvii["checks"]["preserved_at_sigma_le_0.05"] \
        is True
    assert cvii["checks"]["preserved_at_sigma_le_0.1"] \
        is True
    assert cvii["checks"]["breaks_at_sigma_0.5"] is True
    assert cvii["worst_low_sigma"] <= 0.003
    # Thin by construction: the sigma = 0.1 maximum
    # sits 0.00007 below the 0.01 bar. Disclosed,
    # not widened.
    assert 0.009 <= cvii["worst_mid_sigma"] <= 0.01
    assert cvii["break_at_sigma_0.5"] > 0.01


def test_claim_cviii_passes(verdicts):
    cviii = verdicts["claim_cviii_rescue_fragility"]
    assert cviii["passed"] is True
    assert cviii["checks"]["v4_passes_3_of_5"] is True
    assert cviii["checks"]["n20_passes_4_of_5"] is True
    assert cviii["checks"]["v4_breaks_2024"] is True
    assert cviii["checks"]["seed_5_fails_every_method"] \
        is True
    assert cviii["v4_passing_seeds"] == [2, 99, 777]
    assert cviii["n20_passing_seeds"] == [2, 99, 777, 2024]
    # The full 8-bar check agrees with the Pearson
    # counts: V4+cal 3/5, n=20 4/5.
    assert sum(1 for r in cviii["per_seed"]
               if r["v4_8bar_passes"]) == 3
    assert sum(1 for r in cviii["per_seed"]
               if r["n20_8bar_passes"]) == 4
    seed_2024 = [r for r in cviii["per_seed"]
                 if r["seed"] == 2024][0]
    assert seed_2024["plain_pearson"] == pytest.approx(
        -0.9527, abs=1e-4)
    assert seed_2024["v4_pearson"] == pytest.approx(
        -0.8830, abs=1e-4)
    seed_5 = [r for r in cviii["per_seed"]
              if r["seed"] == 5][0]
    assert seed_5["plain_pearson"] == pytest.approx(
        -0.6814, abs=1e-4)
    assert seed_5["v4_pearson"] == pytest.approx(
        -0.8338, abs=1e-4)
    assert seed_5["n20_pearson"] == pytest.approx(
        -0.8749, abs=1e-4)


def test_claim_cix_passes(verdicts):
    cix = verdicts["claim_cix_perpendicular_fresh"]
    assert cix["passed"] is True
    assert cix["checks"][
        "d_range_below_min_on_every_fresh_seed"] is True
    assert cix["checks"]["plain_positive_on_6_of_9"] is True
    assert cix["checks"]["v4_positive_on_5_of_9"] is True
    assert cix["plain_positive_seeds"] == [
        5, 7, 99, 1234, 2024, 2026]
    assert cix["v4_positive_seeds"] == [5, 7, 1234, 2024,
                                        2026]
    assert cix["max_v4_d_range_fresh"] <= 0.18
    assert verdicts["n_passed"] == 3
    assert verdicts["all_pass"] is True


def test_file_seed_rescue_stands():
    # Claim (c) stands as measured on the file
    # seeds: V4-full stored Pearson <= -0.90 on all
    # four, and n=20 too. (cviii) corrects the
    # generalization, it does not retract (c).
    import symmetry_sweep as ss
    for seed in sp.ALL_SEEDS:
        v4 = ss.v4_full_sweep(seed, 0.0)
        n20 = ss.plain_n_copies_sweep(seed, 0.0, 20)
        assert v4["pearson_d_c"] <= -0.90
        assert n20["pearson_d_c"] <= -0.90
