# test_thought_entanglement.py
#
# Tests for thought_entanglement.py (claim (i)).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import numpy as np

import thought_entanglement as te


def test_bell_state_is_maximally_entangled():
    """Concurrence 1, reduced entropy 1 bit, by construction."""
    rho = te.density_matrix(te.bell_state("phi_plus"))
    assert abs(te.concurrence(rho) - 1.0) < 1e-9
    assert abs(te.reduced_entropy(rho) - 1.0) < 1e-9
    assert abs(te.concurrence_pure(te.bell_state("phi_plus")) - 1.0) < 1e-9


def test_all_bell_states_maximally_entangled():
    """All four Bell states have concurrence 1."""
    for which in ("phi_plus", "phi_minus", "psi_plus", "psi_minus"):
        rho = te.density_matrix(te.bell_state(which))
        assert abs(te.concurrence(rho) - 1.0) < 1e-9


def test_product_state_has_no_entanglement():
    """A product state: concurrence 0, reduced entropy 0."""
    psi = np.array([1.0, 0.0, 0.0, 0.0], dtype=complex)
    rho = te.density_matrix(psi)
    assert abs(te.concurrence(rho)) < 1e-9
    assert abs(te.reduced_entropy(rho)) < 1e-9
    assert abs(te.concurrence_pure(psi)) < 1e-9


def test_concurrence_matches_pure_formula():
    """Wootters concurrence equals 2|ad - bc| on pure states.

    Tolerance is 1e-7, not 1e-9: eigvals of the non-Hermitian
    R matrix carries ~1e-8 numerical noise where eigenvalues are
    near-degenerate. The Bell-diagonal cases in claim (i) are
    exact to 1e-9; this generic cross-check is limited by the
    eigensolver, not by the formula.
    """
    rng = np.random.default_rng(7)
    for _ in range(5):
        psi = rng.standard_normal(4) + 1j * rng.standard_normal(4)
        psi = psi / np.linalg.norm(psi)
        rho = te.density_matrix(psi)
        assert abs(te.concurrence(rho) - te.concurrence_pure(psi)) < 1e-7


def test_depolarizing_matches_analytic_form():
    """Depolarized Bell concurrence is max(0, 1 - 3p/2), exactly."""
    rho0 = te.density_matrix(te.bell_state("phi_plus"))
    for p in te.DEPOLARIZING_GRID:
        rho = te.depolarizing(rho0, p)
        assert abs(te.concurrence(rho) - te.depolarizing_concurrence_exact(p)) < 1e-9


def test_depolarizing_kills_entanglement_at_two_thirds():
    """Concurrence is 0 at p = 2/3 and above."""
    rho0 = te.density_matrix(te.bell_state("phi_plus"))
    assert abs(te.concurrence(te.depolarizing(rho0, 2.0 / 3.0))) < 1e-9
    assert abs(te.concurrence(te.depolarizing(rho0, 1.0))) < 1e-9


def test_reduced_entropy_cannot_see_the_death():
    """The reduced state of a Werner state is maximally mixed at every p.

    Reduced entropy stays 1 bit even where the concurrence is 0:
    for mixed states it is not an entanglement measure.
    """
    rho0 = te.density_matrix(te.bell_state("phi_plus"))
    for p in (0.0, 0.5, 2.0 / 3.0, 1.0):
        rho = te.depolarizing(rho0, p)
        assert abs(te.reduced_entropy(rho) - 1.0) < 1e-9


def test_sweep_structure_and_zero_noise():
    """The sweep has one row per sigma; zero noise is exact."""
    sweep = te.entanglement_sweep()
    assert len(sweep) == len(te.SIGMA_GRID)
    assert sweep[0]["sigma"] == 0.0
    assert abs(sweep[0]["mean_concurrence"] - 1.0) < 1e-9
    assert abs(sweep[0]["spooky"] - 1.0) < 1e-9


def test_claim_i_verdict_passes():
    """Claim (i): entanglement measured as a real quantum quantity."""
    verdict = te.claim_entanglement_verdict()
    print(f"claim (i): passed={verdict['passed']}, "
          f"C(sigma=0.01)={verdict['concurrence_sigma_0.01']:.4f}, "
          f"spooky(sigma=0.01)={verdict['spooky_sigma_0.01']:.4f}, "
          f"sigma spooky<0.9={verdict['sigma_spooky_below_0.9']}, "
          f"min mean C={verdict['min_mean_concurrence_vector_noise']:.4f}")
    assert verdict["passed"] is True
    assert verdict["checks"]["a_zero_noise_exact"] is True
    assert verdict["checks"]["b_survives_debroglie_noise"] is True
    assert verdict["checks"]["c_depolarizing_analytic"] is True
    assert verdict["sigma_spooky_below_0.9"] == 0.25
    assert verdict["min_mean_concurrence_vector_noise"] >= 0.5
