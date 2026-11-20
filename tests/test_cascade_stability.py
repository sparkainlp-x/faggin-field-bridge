# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for cascade stability (v0.28.0, claims
(ciii)-(civ)): the reopened cascade's fixed point
and the spooky correlation surviving projection
where visibility dies.

Both claims PASS as measured. (ciii): V_k =
sin(2 alpha) from stage 2 on, worst deviation
3.89e-16, feed phase pi from stage 2 (stage-1
mixed-pair exception phi* = 0 recorded, not
hidden). (civ): rotation-start U_out 0.9958 /
0.9002 / 0.6806 at sigma 0.05 / 0.25 / 0.50,
identical across stages 1-10 under BOTH rules
(range 0.00e+00, rule difference 0.00e+00) while
V dies at stage 2 under projection-only; mixed
start takes exactly one step then stays constant
(worst tail range 3.33e-16). See
docs/preregistration-v0.28.0.md.
"""

import math

import numpy as np
import pytest

import cascade as cas
import cascade_stability as cst


@pytest.fixture(scope="module")
def verdicts():
    return cst.cascade_stability_claims()


# ---------------------------------------------------------------------------
# Frozen thresholds
# ---------------------------------------------------------------------------

def test_thresholds_are_frozen():
    t = cst._thresholds()
    assert t["exact_tol"] == 1e-9


# ---------------------------------------------------------------------------
# The reset rule reproduces the published reopening control
# ---------------------------------------------------------------------------

def test_reset_rule_matches_published_control():
    mine = cst.reopened_cascade_stages(
        lambda: cas.rotation_pair(math.pi / 4),
        math.pi / 4, "reset", n_stages=20)
    published = cas.cascade_reopening(
        stages=list(range(1, 21)), theta=math.pi / 4,
        alpha=math.pi / 4)
    assert len(mine) == len(published) == 20
    for a, b in zip(mine, published):
        assert a["visibility"] == b["visibility"]
        assert a["feed_phase"] == b["feed_phase"]


# ---------------------------------------------------------------------------
# (ciii): the fixed point, one alpha, all rules and starts
# ---------------------------------------------------------------------------

def test_fixed_point_one_alpha_all_rules_and_starts():
    for rule in cst.RULES:
        for name, start_fn in cst._start_fns():
            rows = cst.reopened_cascade_stages(
                start_fn, math.pi / 4, rule, n_stages=20)
            target = math.sin(2.0 * math.pi / 4)
            for row in rows[1:]:  # stages >= 2
                assert abs(row["visibility"] - target) <= 1e-9
                assert abs(row["feed_phase"] - math.pi) <= 1e-9
            # The pair from stage 2 on is a rotation pair
            # at alpha: the stored-direction angle of e1
            # is constant.
            angles = [r["e1_angle"] for r in rows]
            assert max(angles) - min(angles) <= 1e-12


def test_mixed_stage1_feed_phase_is_zero_every_rule():
    for rule in cst.RULES:
        rows = cst.reopened_cascade_stages(
            cas.mixed_pair, math.pi / 4, rule, n_stages=20)
        # The mixed pair's cross term is +1/sqrt(6),
        # so D is maximal at phi = 0 at stage 1.
        assert rows[0]["feed_phase"] == 0.0
        assert rows[0]["visibility"] == pytest.approx(
            2.0 * math.sqrt(6.0) / 7.0, abs=1e-9)
        # From stage 2 the pair is a rotation pair
        # at alpha and the feed phase is pi.
        for row in rows[1:]:
            assert abs(row["feed_phase"] - math.pi) <= 1e-9


# ---------------------------------------------------------------------------
# (civ): spooky survives projection while V dies
# ---------------------------------------------------------------------------

def test_projection_only_v_dies_at_stage_2():
    rows = cst.projection_only_stages(
        lambda: cas.rotation_pair(math.pi / 4), n_stages=10)
    assert abs(rows[0]["visibility"] - 1.0) <= 1e-9
    for row in rows[1:]:
        assert row["pair_exists"] is False
        assert row["visibility"] == 0.0


def test_u_rotation_constant_both_rules():
    start = lambda: cas.rotation_pair(math.pi / 4)
    proj = cst.projection_only_stages(start, n_stages=10)
    reop = cst.reopened_cascade_stages(
        start, math.pi / 4, "reset", n_stages=10)
    for sigma in cst.SIGMAS_U:
        u_proj = [r["u_out"][sigma] for r in proj]
        u_reop = [r["u_out"][sigma] for r in reop]
        assert max(u_proj) - min(u_proj) == 0.0
        assert max(u_reop) - min(u_reop) == 0.0
        assert u_proj == u_reop
    assert proj[0]["u_out"][0.05] == pytest.approx(
        0.9958, abs=1e-4)
    assert proj[0]["u_out"][0.25] == pytest.approx(
        0.9002, abs=1e-4)
    assert proj[0]["u_out"][0.50] == pytest.approx(
        0.6806, abs=1e-4)


def test_u_mixed_one_step_then_constant():
    start = cas.mixed_pair
    proj = cst.projection_only_stages(start, n_stages=10)
    reop = cst.reopened_cascade_stages(
        start, math.pi / 4, "reset", n_stages=10)
    expected_drops = {0.05: 0.0008, 0.25: 0.0168,
                      0.50: 0.0314}
    expected_rises = {0.05: 0.0011, 0.25: 0.0169,
                      0.50: 0.0330}
    for sigma in cst.SIGMAS_U:
        u_proj = [r["u_out"][sigma] for r in proj]
        u_reop = [r["u_out"][sigma] for r in reop]
        # Projection-only falls; reopening rises to the
        # rotation value; then constant from stage 2.
        assert u_proj[0] - u_proj[1] == pytest.approx(
            expected_drops[sigma], abs=1e-4)
        assert u_reop[1] - u_reop[0] == pytest.approx(
            expected_rises[sigma], abs=1e-4)
        assert max(u_proj[1:]) - min(u_proj[1:]) <= 1e-9
        assert max(u_reop[1:]) - min(u_reop[1:]) <= 1e-9
    # Reopening's mixed-start fixed point IS the
    # rotation value (0.9958 / 0.9002 / 0.6806).
    rot = cst.projection_only_stages(
        lambda: cas.rotation_pair(math.pi / 4), n_stages=10)
    for sigma in cst.SIGMAS_U:
        assert reop[1]["u_out"][sigma] == pytest.approx(
            rot[0]["u_out"][sigma], abs=1e-12)


# ---------------------------------------------------------------------------
# Claim verdicts
# ---------------------------------------------------------------------------

def test_claim_ciii_passes(verdicts):
    ciii = verdicts["claim_ciii_fixed_point"]
    assert ciii["passed"] is True
    assert ciii["checks"]["v_fixed_point_from_stage_2"] is True
    assert ciii["checks"]["feed_phase_pi_from_stage_2"] is True
    assert ciii["worst_v_deviation"] <= 1e-9
    assert ciii["worst_phi_deviation"] == 0.0
    # 3 rules x 4 starts x 5 alphas = 60 combos.
    assert len(ciii["per_combo"]) == 60


def test_claim_civ_passes(verdicts):
    civ = verdicts["claim_civ_spooky_survives"]
    assert civ["passed"] is True
    assert civ["checks"]["rotation_u_constant_both_rules"] \
        is True
    assert civ["checks"]["rotation_u_rule_independent"] is True
    assert civ["checks"]["mixed_u_constant_from_stage_2"] \
        is True
    assert civ["checks"]["v_dies_while_u_survives"] is True
    assert civ["worst_u_range_rotation"] == 0.0
    assert civ["worst_u_rule_difference"] == 0.0
    assert civ["worst_u_range_mixed_from_stage2"] <= 1e-9
    assert verdicts["n_passed"] == 2
    assert verdicts["all_pass"] is True
