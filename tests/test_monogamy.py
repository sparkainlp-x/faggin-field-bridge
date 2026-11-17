# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for monogamy.py: CKW monogamy in triads (v0.7.0)."""

import math

import numpy as np
import pytest

import monogamy as mg


def test_ghz_exact_values():
    analysis = mg.triad_analysis(mg.ghz_triad())
    m = analysis["members"][0]
    assert m["tau_one_to_rest"] == pytest.approx(1.0, abs=1e-9)
    assert m["tau_pair"][(0, 1)] == pytest.approx(0.0, abs=1e-9)
    assert m["tau_pair"][(0, 2)] == pytest.approx(0.0, abs=1e-9)
    assert m["residual"] == pytest.approx(1.0, abs=1e-9)
    assert m["d_member"] == pytest.approx(2.0 / 3.0, abs=1e-9)


def test_w_exact_values():
    analysis = mg.triad_analysis(mg.w_triad())
    m = analysis["members"][0]
    assert m["tau_one_to_rest"] == pytest.approx(8.0 / 9.0, abs=1e-9)
    assert m["tau_pair"][(0, 1)] == pytest.approx(4.0 / 9.0, abs=1e-9)
    assert m["tau_pair"][(0, 2)] == pytest.approx(4.0 / 9.0, abs=1e-9)
    assert m["residual"] == pytest.approx(0.0, abs=1e-9)
    assert m["d_member"] == pytest.approx(7.0 / 9.0, abs=1e-9)


def test_triad_members_symmetric():
    # GHZ and W are symmetric under member permutation: every
    # member sees the same tangles and the same D.
    for psi in (mg.ghz_triad(), mg.w_triad()):
        analysis = mg.triad_analysis(psi)
        members = analysis["members"]
        for m in (1, 2):
            assert (members[m]["tau_one_to_rest"]
                    == pytest.approx(members[0]["tau_one_to_rest"],
                                     abs=1e-9))
            assert (members[m]["residual"]
                    == pytest.approx(members[0]["residual"], abs=1e-9))
            assert (members[m]["d_member"]
                    == pytest.approx(members[0]["d_member"], abs=1e-9))


def test_partial_trace_dimensions():
    rho = mg.density_matrix(mg.ghz_triad())
    assert mg.partial_trace(rho, (0,)).shape == (2, 2)
    assert mg.partial_trace(rho, (0, 1)).shape == (4, 4)
    assert mg.partial_trace(rho, (1, 2)).shape == (4, 4)
    assert mg.partial_trace(rho, (0, 1, 2)).shape == (8, 8)
    # Tracing out nothing returns the state itself.
    assert np.allclose(mg.partial_trace(rho, (0, 1, 2)), rho)


def test_partial_trace_reduced_states():
    # GHZ reduced single-qubit state is maximally mixed; the
    # reduced pair is the classical mixture (|00><00| +
    # |11><11|)/2, so its concurrence is 0.
    rho = mg.density_matrix(mg.ghz_triad())
    assert np.allclose(mg.reduced_single(rho, 0),
                       np.eye(2, dtype=complex) / 2.0)
    pair = mg.reduced_pair(rho, 0, 1)
    assert np.allclose(pair, np.diag([0.5, 0.0, 0.0, 0.5]))


def test_embedded_member_state():
    # The embedding maps |0> -> |00> and |1> -> |10>: the
    # maximally mixed member embeds as diag(1/2, 0, 1/2, 0).
    rho_a = np.eye(2, dtype=complex) / 2.0
    embedded = mg.embed_member_state(rho_a)
    assert embedded.shape == (4, 4)
    assert np.allclose(embedded,
                       np.diag([0.5, 0.0, 0.5, 0.0]))
    assert float(np.real(np.trace(embedded))) == pytest.approx(1.0)


def test_generalized_ghz_pairwise_zero():
    # Pairwise tangle is exactly 0 on the whole generalized-
    # GHZ family; the one-to-rest tangle is 4 a^2 (1-a^2).
    for a in (0.5, 0.7, 1.0 / math.sqrt(2.0), 0.9, 1.0):
        analysis = mg.triad_analysis(mg.generalized_ghz(a))
        m = analysis["members"][0]
        assert m["tau_pair"][(0, 1)] == pytest.approx(0.0, abs=1e-9)
        assert m["tau_pair"][(0, 2)] == pytest.approx(0.0, abs=1e-9)
        assert m["tau_one_to_rest"] == pytest.approx(
            4.0 * a * a * (1.0 - a * a), abs=1e-9)
        assert m["d_member"] == pytest.approx(
            1.0 / 3.0 + (2.0 / 3.0) * a * a, abs=1e-9)


def test_ghz_w_interpolation_endpoints():
    assert np.allclose(mg.ghz_w_interpolation(0.0), mg.ghz_triad())
    assert np.allclose(mg.ghz_w_interpolation(math.pi / 2.0),
                       mg.w_triad())
    # The interpolation stays normalized (GHZ and W are
    # orthogonal: disjoint support).
    for deg in mg.INTERPOLATION_DEGREES:
        psi = mg.ghz_w_interpolation(math.radians(deg))
        assert float(np.linalg.norm(psi)) == pytest.approx(1.0, abs=1e-12)


def test_noisy_copies_stay_pure():
    # The unity.py noise model keeps triad copies pure, so
    # the 4 det(rho_A) formula stays valid at every sigma.
    for sigma in mg.SIGMA_GRID:
        copies = mg.noisy_triad_copies(mg.ghz_triad(), sigma, 5, 42)
        assert len(copies) == 5
        for c in copies:
            assert mg.triad_purity(c) == pytest.approx(1.0, abs=1e-9)
            assert float(np.linalg.norm(c)) == pytest.approx(1.0, abs=1e-9)


def test_ckw_min_margin_nonnegative():
    verdict = mg.claim_ckw_verdict()
    assert verdict["min_margin"] >= -mg.CKW_TOL
    assert verdict["min_margin"] == pytest.approx(0.0, abs=1e-9)
    # The zero is the product endpoint (a = 1.0, sigma = 0):
    # no entanglement, so the margin is 0 by construction.
    assert verdict["worst_row"]["state"] == "gen_ghz_a=1.0"
    assert verdict["n_rows"] == 52


def test_ckw_min_margin_noisy_positive():
    rows = mg.ckw_sweep()
    noisy = [r for r in rows if r["sigma"] > 0.0]
    assert min(r["min_margin"] for r in noisy) == pytest.approx(
        0.0012, abs=1e-3)
    assert all(r["min_purity"] == pytest.approx(1.0, abs=1e-9)
               for r in rows)


def test_claim_xvii_verdict_pass():
    verdict = mg.claim_ckw_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"]["min_margin_at_least_minus_tol"] is True


def test_claim_xviii_verdict_pass():
    verdict = mg.claim_ghz_vs_w_verdict()
    assert verdict["passed"] is True
    assert all(verdict["checks"].values())
    assert verdict["ghz"]["miss_fraction"] == pytest.approx(1.0)
    assert verdict["w"]["miss_fraction"] == pytest.approx(0.0)
    # Under noise the GHZ miss stays above 0.6 and the W miss
    # below 0.45: pairwise concurrence keeps missing most of
    # the GHZ entanglement at every sigma.
    ghz_rows = [r for r in verdict["noise_rows"] if r["state"] == "ghz"]
    w_rows = [r for r in verdict["noise_rows"] if r["state"] == "w"]
    assert all(r["mean_miss_fraction"] >= 0.6 for r in ghz_rows)
    assert all(r["mean_miss_fraction"] <= 0.45 for r in w_rows)


def test_ghz_noise_tau_ab_stays_small():
    # On noisy GHZ triads the pairwise sum stays small while
    # tau_A(BC) decays: the entanglement stays mostly
    # tripartite, not pairwise.
    rows = [r for r in mg.ghz_vs_w_noise() if r["state"] == "ghz"]
    assert rows[0]["mean_tau_one_to_rest"] == pytest.approx(1.0, abs=1e-9)
    assert rows[-1]["mean_tau_one_to_rest"] == pytest.approx(
        0.6504, abs=1e-3)
    assert all(r["mean_pairwise_sum"] <= 0.26 for r in rows)
    assert rows[-1]["mean_d_member"] == pytest.approx(0.6132, abs=1e-3)


def test_claim_xix_verdict_pass():
    verdict = mg.claim_d_vs_tau_verdict()
    assert verdict["passed"] is True
    assert verdict["checks"]["pearson_at_most_max"] is True
    assert verdict["checks"]["tau_ab_flat"] is True
    assert verdict["checks"]["d_range_at_least_min"] is True
    assert verdict["pearson_d_tau"] == pytest.approx(-0.9608, abs=1e-3)
    assert verdict["spearman_d_tau"] == pytest.approx(-1.0, abs=1e-9)
    assert verdict["max_tau_ab"] == pytest.approx(0.0, abs=1e-9)
    assert verdict["d_range"] == pytest.approx(1.0 / 3.0, abs=1e-9)


def test_xix_branch_endpoints():
    rows = mg.d_vs_tau_generalized_ghz()["rows"]
    assert rows[0]["a"] == pytest.approx(1.0 / math.sqrt(2.0))
    assert rows[0]["tau_one_to_rest"] == pytest.approx(1.0, abs=1e-9)
    assert rows[0]["d_member"] == pytest.approx(2.0 / 3.0, abs=1e-9)
    assert rows[-1]["a"] == pytest.approx(1.0)
    assert rows[-1]["tau_one_to_rest"] == pytest.approx(0.0, abs=1e-9)
    assert rows[-1]["d_member"] == pytest.approx(1.0, abs=1e-9)


def test_xix_interpolation_descriptive_not_gated():
    # Across the GHZ/W interpolation the correlation is only
    # -0.63: tau_AB rises to 4/9 along this family, so it
    # confounds the two entanglements. Reported, not gated.
    verdict = mg.claim_d_vs_tau_verdict()
    assert verdict["interpolation"]["pearson_d_tau"] == pytest.approx(
        -0.6316, abs=1e-3)


def test_xix_noise_sweep_descriptive_not_gated():
    # Under noise on GHZ, D_A and tau_A(BC) decay TOGETHER
    # (both fall with sigma) while tau_AB stays small: the
    # noise channel does not separate "entanglement with
    # the pair" from "entanglement with B". The separation
    # is in the state family, not the noise.
    verdict = mg.claim_d_vs_tau_verdict()
    ghz = verdict["ghz_noise_rows"]
    ds = [r["mean_d_member"] for r in ghz]
    taus = [r["mean_tau_one_to_rest"] for r in ghz]
    assert ds == sorted(ds, reverse=True)
    assert taus == sorted(taus, reverse=True)


def test_monogamy_claims_aggregate():
    verdicts = mg.monogamy_claims()
    assert verdicts["n_claims"] == 3
    assert verdicts["n_passed"] == 3
    assert verdicts["all_pass"] is True
    assert verdicts["headline_allowed"] is False


def test_thresholds_set():
    thresholds = mg._thresholds()
    assert thresholds["ckw_tol"] == pytest.approx(1e-9)
    assert thresholds["miss_ghz_min"] == pytest.approx(0.9)
    assert thresholds["miss_w_max"] == pytest.approx(0.1)
    assert thresholds["d_tau_pearson_max"] == pytest.approx(-0.95)
    assert thresholds["tau_ab_flat_max"] == pytest.approx(1e-9)
    assert thresholds["d_range_min"] == pytest.approx(0.25)


def test_input_validation():
    with pytest.raises(ValueError):
        mg.density_matrix(np.zeros(4, dtype=complex))
    with pytest.raises(ValueError):
        mg.partial_trace(np.eye(8, dtype=complex), ())
    with pytest.raises(ValueError):
        mg.partial_trace(np.eye(8, dtype=complex), (0, 0))
    with pytest.raises(ValueError):
        mg.partial_trace(np.eye(4, dtype=complex), (0,))
    with pytest.raises(ValueError):
        mg.generalized_ghz(1.5)
    with pytest.raises(ValueError):
        mg.embed_member_state(np.eye(4, dtype=complex))
    with pytest.raises(ValueError):
        mg.noisy_triad_copies(
            np.array([1j] + [0.0] * 7, dtype=complex), 0.25)


def test_main_runs(capsys):
    mg.main()
    out = capsys.readouterr().out
    assert "claims (xvii)-(xix): 3/3 pass" in out
    assert "claim (xvii) verdict: PASS" in out
    assert "claim (xviii) verdict: PASS" in out
    assert "claim (xix) verdict: PASS" in out
