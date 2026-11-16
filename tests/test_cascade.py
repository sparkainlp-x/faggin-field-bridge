# test_cascade.py
#
# Tests for the cascade module (claims (v), (vi), (vii)): interference
# via the cross term, cascade visibility, and coherence/D tracking.
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import math

import numpy as np

import bridge
import cascade as ca
import self_knowing as sk
import thought as th

TOL = 1e-9


def _overlap(a, b):
    return abs(complex(np.vdot(a, b)))


def test_rotation_pair_orthonormal_and_visibility():
    """V(theta) = sin(2 theta); cross term = -sin(theta) cos(theta)."""
    for theta in ca.THETA_GRID:
        psi1, psi2 = ca.rotation_pair(theta)
        assert _overlap(psi1, psi2) <= 1e-12
        assert abs(sk.self_knowing_factor(psi1) - math.cos(theta) ** 2) <= TOL
        assert abs(sk.self_knowing_factor(psi2) - math.sin(theta) ** 2) <= TOL
        cross = ca.cross_term(psi1, psi2)
        assert abs(cross + math.sin(theta) * math.cos(theta)) <= TOL
        v_sweep, v_analytic = ca.visibility(psi1, psi2)
        assert abs(v_sweep - math.sin(2.0 * theta)) <= TOL
        assert abs(v_analytic - math.sin(2.0 * theta)) <= TOL


def test_max_pair_phase_swing():
    """D(phi) = 1/2 - (1/2) cos(phi): blind at 0, determined at pi."""
    psi1, psi2 = ca.rotation_pair(math.pi / 4)
    for phi, expected in ((0.0, 0.0), (math.pi / 2, 0.5), (math.pi, 1.0)):
        assert abs(ca.projected_norm(phi, psi1, psi2) - expected) <= TOL
    # The superpositions ARE the kernel thought (phi = 0) and the
    # uniform thought (phi = pi).
    assert _overlap(ca.superposed(psi1, psi2, 0.0), ca.kernel_direction()) > 1 - TOL
    assert _overlap(ca.superposed(psi1, psi2, math.pi),
                    th.uniform_thought()) > 1 - TOL


def test_mixed_pair():
    """Cross term 1/sqrt(6), V = 2 sqrt(6)/7."""
    m1, m2 = ca.mixed_pair()
    assert _overlap(m1, m2) <= 1e-12
    assert abs(sk.self_knowing_factor(m1) - 0.5) <= TOL
    assert abs(sk.self_knowing_factor(m2) - 2.0 / 3.0) <= TOL
    assert abs(ca.cross_term(m1, m2) - 1.0 / math.sqrt(6.0)) <= TOL
    v_sweep, v_analytic = ca.visibility(m1, m2)
    assert abs(v_sweep - 2.0 * math.sqrt(6.0) / 7.0) <= TOL
    assert abs(v_analytic - 2.0 * math.sqrt(6.0) / 7.0) <= TOL


def test_control_pairs_have_no_interference():
    """Stored pair and (uniform, kernel) pair: cross term 0, V 0."""
    for pair in (ca.stored_pair(), ca.uniform_kernel_pair()):
        assert abs(ca.cross_term(pair[0], pair[1])) <= TOL
        v_sweep, v_analytic = ca.visibility(pair[0], pair[1])
        assert v_sweep <= TOL
        assert v_analytic <= TOL


def test_kernel_thought_projects_to_nothing():
    """The kernel thought has no stored component: no projected state."""
    assert ca.project_state(ca.kernel_direction()) is None
    v1, v2, rank = ca.project_pair(*ca.uniform_kernel_pair())
    assert v1 is None and v2 is None and rank == 0


def test_projection_collapses_rotation_pair():
    """The rotation pair's projected vectors are parallel: rank 1."""
    psi1, psi2 = ca.rotation_pair(math.pi / 4)
    v1, v2, rank = ca.project_pair(psi1, psi2)
    assert rank == 1
    assert _overlap(v1, v2) > 1 - TOL
    assert ca.reform_pair(v1, v2) is None


def test_projection_reforms_mixed_pair_fully_stored():
    """The mixed pair stays rank 2 and re-forms as (q1, q2)."""
    m1, m2 = ca.mixed_pair()
    v1, v2, rank = ca.project_pair(m1, m2)
    assert rank == 2
    reformed = ca.reform_pair(v1, v2)
    assert reformed is not None
    q1, q2 = ca.stored_basis()
    assert _overlap(reformed[0], q1) > 1 - TOL
    assert _overlap(reformed[1], q2) > 1 - TOL
    assert abs(ca.cross_term(reformed[0], reformed[1])) <= TOL


def test_cascade_rotation_dies_at_stage_2():
    """V = 1 at stage 1, 0 at every stage >= 2; pair collapses."""
    rows = ca.cascade_projection_only(
        pair_fn=lambda: ca.rotation_pair(math.pi / 4))
    assert [r["stage"] for r in rows] == ca.STAGES
    assert abs(rows[0]["visibility"] - 1.0) <= TOL
    assert rows[0]["pair_exists"] is True
    for r in rows[1:]:
        assert abs(r["visibility"]) <= TOL
        assert r["pair_exists"] is False
        assert abs(r["D_projected_output"] - 1.0) <= TOL
        assert abs(r["coherence_projected_output"] - 3.0) <= TOL


def test_cascade_mixed_dies_at_stage_2():
    """V = 2 sqrt(6)/7 at stage 1, 0 at every stage >= 2; pair stored."""
    rows = ca.cascade_projection_only(pair_fn=ca.mixed_pair)
    assert abs(rows[0]["visibility"] - 2.0 * math.sqrt(6.0) / 7.0) <= TOL
    assert abs(rows[0]["coherence_projected_output"]
               - 2.327673435381233) <= TOL
    for r in rows[1:]:
        assert abs(r["visibility"]) <= TOL
        assert r["pair_exists"] is True
        assert abs(r["D_projected_output"] - 1.0) <= TOL
        assert abs(r["coherence_projected_output"]
                   - 2.732050807568877) <= TOL


def test_cascade_reopening_survives_every_stage():
    """Fresh kernel input each stage: V = 1 at every stage."""
    rows = ca.cascade_reopening(alpha=math.pi / 4)
    assert [r["stage"] for r in rows] == ca.STAGES
    for r in rows:
        assert abs(r["visibility"] - 1.0) <= TOL
        assert abs(r["D_projected_output"] - 1.0) <= TOL
        assert abs(r["coherence_projected_output"] - 3.0) <= TOL


def test_claim_v_interference_passes():
    """Claim (v): interference measured via the cross term."""
    verdict = ca.claim_interference_verdict()
    assert verdict["passed"] is True
    assert all(verdict["checks"].values())


def test_claim_vi_cascade_passes_and_finding_is_death():
    """Claim (vi): interference does not survive projection."""
    verdict = ca.claim_cascade_verdict()
    assert verdict["passed"] is True
    assert verdict["finding"] == "interference_does_not_survive_projection"
    assert verdict["survives_projection"] is False
    assert all(verdict["checks"].values())


def test_claim_vii_tracking_passes():
    """Claim (vii): D = 1 everywhere; coherence fixed point from stage 2."""
    verdict = ca.claim_cascade_tracking_verdict()
    assert verdict["passed"] is True
    assert all(verdict["checks"].values())
    # Mixed cascade: visibility dies while coherence rises to its
    # fixed point -- perfect anti-tracking across the transition.
    mixed = verdict["tables"]["mixed"]
    assert abs(mixed["spearman_V_coherence"] + 1.0) <= TOL
    # D is constant, so its rank correlation is undefined (0.0).
    assert mixed["spearman_V_D"] == 0.0


def test_bridge_carries_seven_claims():
    """bridge.quantum_thought_claims() now unifies seven claims."""
    result = bridge.quantum_thought_claims()
    assert result["headline_allowed"] is False
    assert result["n_claims"] == 7
    assert result["n_passed"] == 7
    assert result["all_pass"] is True
    for key in ("claim_i_entanglement", "claim_ii_coherence",
                "claim_iii_collapse", "claim_iv_self_knowing",
                "claim_v_interference", "claim_vi_cascade",
                "claim_vii_cascade_tracking"):
        assert result[key]["passed"] is True
