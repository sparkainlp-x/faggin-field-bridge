# test_empathy_field.py
#
# Tests for empathy_field.py (v0.5.0): resonance, collaboration,
# co-creativity = entropy. Exact values where the machinery
# gives them; the claim verdicts are tested as measured
# (including (xiii) FAILING on the break half -- that is the
# measured outcome, and the test documents it rather than
# hiding it).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Tests for the empathy field (claims (xi)-(xiii))."""

import math

import numpy as np
import pytest

import empathy_field as ef
import self_knowing
import thought
import thought_entanglement as te

TOL = 1e-9


def test_field_state_normalized():
    states = [thought.uniform_thought(),
              thought.focused_thought("attention")]
    phi = ef.field_state(states)
    assert abs(float(np.linalg.norm(phi)) - 1.0) <= TOL
    # The field of identical states is the state itself.
    same = [thought.uniform_thought()] * 3
    assert np.allclose(ef.field_state(same),
                       thought.uniform_thought(), atol=TOL)


def test_field_state_needs_agents():
    with pytest.raises(ValueError):
        ef.field_state([])


def test_overlap_exact_values():
    u = thought.uniform_thought()
    a = thought.focused_thought("attention")
    m = thought.focused_thought("memory")
    assert abs(ef.overlap_squared(u, a) - 0.25) <= TOL
    assert abs(ef.overlap_squared(a, m)) <= TOL
    assert abs(ef.overlap_squared(a, a) - 1.0) <= TOL
    assert abs(ef.overlap_squared(u, u) - 1.0) <= TOL
    kernel = np.array([0.0, 1.0, -1.0, 0.0], dtype=complex) / math.sqrt(2.0)
    assert abs(ef.overlap_squared(u, kernel)) <= TOL
    assert abs(ef.overlap_squared(m, kernel) - 0.5) <= TOL


def test_overlap_bounds():
    rng = np.random.default_rng(7)
    for _ in range(20):
        a = rng.standard_normal(4)
        b = rng.standard_normal(4)
        r = ef.overlap_squared(a, b)
        assert 0.0 <= r <= 1.0 + TOL


def test_pair_concurrence_exact_values():
    u = thought.uniform_thought()
    phi_plus = te.bell_state("phi_plus")
    phi_minus = te.bell_state("phi_minus")
    # The uniform + phi_plus pair state has concurrence 1/sqrt(2).
    assert abs(ef.pair_frequency(u, phi_plus) - 1.0 / math.sqrt(2.0)) <= TOL
    # Two opposite Bell states sum to a basis state: concurrence 0.
    assert abs(ef.pair_frequency(phi_plus, phi_minus)) <= TOL
    assert abs(ef.pair_frequency(phi_plus, phi_plus) - 1.0) <= TOL


def test_agent_frequency_bounds():
    assert abs(ef.agent_frequency(thought.uniform_thought())) <= TOL
    assert abs(ef.agent_frequency(te.bell_state("phi_plus")) - 1.0) <= TOL


def test_pair_quanta_are_concurrences():
    u = thought.uniform_thought()
    phi_plus = te.bell_state("phi_plus")
    assert abs(ef.pair_empathy_quantum(u, phi_plus)
               - ef.pair_frequency(u, phi_plus)) <= TOL
    assert 0.0 <= ef.pair_empathy_quantum(u, phi_plus) <= 1.0 + TOL


def test_self_determinism_exact_values():
    assert abs(ef.agent_self_determinism(thought.uniform_thought())
               - 1.0) <= TOL
    kernel = np.array([0.0, 1.0, -1.0, 0.0], dtype=complex) / math.sqrt(2.0)
    assert abs(ef.agent_self_determinism(kernel)) <= TOL
    assert abs(self_knowing.self_knowing_factor(
        thought.focused_thought("other")) - 1.0 / 3.0) <= TOL


def test_empathy_fraction_bell_population_exact():
    # At sigma = 0 the four Bell states pair up as (1, 1, 1, 0, 0, 0):
    # three pairs have concurrence 1, three have 0 -- mean 1/3.
    states = ef.collaboration_population(4, 0.0, 42)
    assert abs(ef.empathy_fraction(states) - 1.0 / 3.0) <= TOL


def test_resonance_pairs_count_and_sigma_zero():
    pairs = ef.resonance_pairs(sigmas=[0.0])
    assert len(pairs) == 28  # C(8, 2)
    assert all(abs(p["resonance"] - 1.0) <= TOL for p in pairs)
    assert all(abs(p["d_pair"] - 1.0) <= TOL for p in pairs)
    assert all(abs(p["nu_ij"]) <= TOL for p in pairs)


def test_resonance_bins_sum_to_total():
    pairs = ef.resonance_pairs()
    assert len(pairs) == 7 * 28  # 7 sigmas, C(8, 2) pairs each
    bins = ef.resonance_bins(pairs)
    assert sum(b["n_pairs"] for b in bins) == len(pairs)


def test_resonance_gap_rmin_half():
    pairs = ef.resonance_pairs()
    gap = ef.resonance_gap(pairs, 0.5)
    assert gap["pooled"]["n_resonant"] == 171
    assert gap["pooled"]["n_non_resonant"] == 25
    assert abs(gap["pooled"]["gap"] - 0.2983840571478532) <= 1e-9
    # At sigma = 1.0 the within-sigma gap is slightly NEGATIVE:
    # the resonance effect is the cross-noise pattern, not a
    # within-sigma effect (REPORT.md section 11).
    last = gap["per_sigma"][-1]
    assert last["sigma"] == 1.0
    assert last["gap"] < 0.0


def test_thresholds_set_from_pilot():
    assert ef.RESONANCE_R_MIN == 0.5
    assert ef.RESONANCE_D_MARGIN == 0.20
    assert ef.COLLABORATION_H_MARGIN == 2.0
    assert ef.COLLABORATION_GAP_CLOSE_FRACTION == 0.5
    assert ef.SATURATION_FRACTION_TOL == 0.10


def test_collaboration_n1_single_agent():
    # A single agent has no field to share, so the collaborating
    # arm's mix is a no-op -- but the arms still differ in design
    # B, because the isolated arm collapses (decides) while the
    # collaborating arm stays superposed. The N = 1 gap is the
    # pure superposition advantage, with no field involved; and
    # the collaborating N = 1 run is identical to design A's
    # (kick only, no mix, no collapse).
    result_b = ef.run_collaboration(n_agents=1, sigma=0.25, design="B")
    result_a = ef.run_collaboration(n_agents=1, sigma=0.25, design="A")
    assert result_b["gap_bits"] > 0.0
    assert result_b["collaborating"]["h_joint_bits"] == pytest.approx(
        result_a["collaborating"]["h_joint_bits"])
    assert result_b["collaborating"]["h_joint_bits"] == pytest.approx(
        result_a["isolated"]["h_joint_bits"])
    assert result_b["ceiling_bits"] == 2.0


def test_collaboration_design_b_gap_positive_at_025():
    result = ef.run_collaboration(sigma=0.25, design="B")
    assert result["gap_bits"] > 2.0
    assert result["gap_distinct"] > 0
    assert result["collaborating"]["distinct_joint"] == 157
    assert result["isolated"]["distinct_joint"] == 4


def test_collaboration_design_a_gap_negative_at_025():
    # The reason design B is the vehicle: design A (no collapse
    # anywhere) goes negative by sigma = 0.25 -- the field pull
    # concentrates the joint distribution once noise has
    # broadened the isolated marginals.
    result = ef.run_collaboration(sigma=0.25, design="A")
    assert result["gap_bits"] < 0.0


def test_claims_xi_xii_xiii():
    verdicts = ef.empathy_field_claims()
    xi = verdicts["claim_xi_resonance"]
    assert xi["passed"] is True
    assert xi["checks"]["binned_D_monotone_in_R"] is True
    assert xi["checks"]["pooled_gap_at_least_margin"] is True
    means = [b["mean_d"] for b in xi["bins"]]
    assert means == sorted(means) and len(set(means)) == len(means)

    xii = verdicts["claim_xii_collaboration"]
    assert xii["passed"] is True
    assert xii["gap_bits"] > 2.0
    assert xii["distinct_collaborating"] > xii["distinct_isolated"]

    xiii = verdicts["claim_xiii_cocreativity"]
    # The ceiling half passes; the break half FAILS: the gap
    # holds at every sigma (+4.34 at 0.25, +3.35 at 0.50,
    # +3.56 at 1.00) and does not close past sigma = 0.50.
    assert xiii["passed"] is False
    assert xiii["checks"]["h_joint_increasing_in_N"] is True
    assert xiii["checks"]["h_joint_below_ceiling"] is True
    assert xiii["checks"]["fraction_of_ceiling_plateaus"] is True
    assert xiii["checks"]["gap_holds_at_sigma_le_0.25"] is True
    assert xiii["checks"]["gap_closes_past_sigma_0.50"] is False
    assert xiii["gap_at_sigma_0.50"] > 0.5 * xiii["gap_at_sigma_0.25"]
    assert verdicts["n_passed"] == 2
    assert verdicts["n_claims"] == 3
