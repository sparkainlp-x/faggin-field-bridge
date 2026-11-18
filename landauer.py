# landauer.py
#
# Landauer-cost ledger (deep-think upgrade #6, "the honest
# upgrade") + the Planck spectral falsification.
#
# The mechanism, defined inside the model (not discovered):
#   - Landauer's principle (Landauer 1961; verified by
#     Berut et al., Nature 2012): erasing one bit
#     irreversibly dissipates at least k_B T ln 2. At
#     T = 300 K that is 2.871e-21 J per bit (k_B exact SI).
#     The bridge's E = h*nu (v0.4.0) is a DEFINED per-mode
#     unit; the report found NO literature linking a Planck
#     spectrum to consciousness, so this version replaces
#     the black-body analogy with a ledger and then tests
#     the spectrum itself -- and expects the spectrum to
#     fail.
#   - The ledger counts the bits a measurement run
#     irreversibly discards, per field (one sigma step),
#     under a stated protocol:
#       (a) thought collapses: collapsing each agent's
#           thought resolves exactly its decision entropy
#           (thought.decision_entropy -- the Shannon entropy
#           of the Born distribution, v0.2.0). Summed over
#           agents: sum_i H(psi_i) bits.
#       (b) quale collapses: each quale wave is a
#           superposition of two members (qualia.py); reading
#           it out collapses it to one member -- 1 bit per
#           quale (binary which-member).
#       (c) classification records: each pair is
#           distinguished quale / non-quale (1 bit per pair)
#           and the record is erased when the field advances
#           to the next sigma -- N_pairs bits per field.
#     Cost = bits * k_B * T * ln 2. Every term is a count
#     the code measures, not a fitted parameter.
#   - The Planck spectral test standardizes the mode
#     energies: y = nu / mean(nu) per field. A Planck
#     spectrum is scale-free -- its standardized shape is
#     FIXED (density ~ x^3 / (exp(x) - 1), x = nu/theta):
#     mean x = 3.8322, mode x = 2.8210, so mode/mean =
#     0.7361 at EVERY temperature, and the standardized
#     CDF is one curve. If the empathy field were
#     Planckian, the pooled standardized nu distribution
#     would follow that curve (Kolmogorov-Smirnov test)
#     and mode/mean would sit at 0.7361 at every sigma.
#     The Wien leg is the same ratio: a Planck peak moves
#     in proportion to temperature, so mode/mean cannot
#     wander with sigma.
#
# Honesty, stated up front:
#   - The ledger's event list is a DEFINITION of what this
#     run counts as erasure, not a measurement of a physical
#     brain erasing bits. The per-bit cost is exact physics;
#     which operations count as erasures is the model's
#     choice, stated here so it can be challenged.
#   - The classification term (28 bits) is constant per
#     field and dominates the ledger; the sigma-dependence
#     comes from the decision-entropy sum (falls with sigma
#     as the copies spread) and the quale count (humped).
#     The ledger's hump is therefore inherited from the
#     quale hump, not independent evidence for it -- the
#     claim is that the cost humps, not that the hump is
#     explained by cost.
#   - A "quale" here is a DEFINED resonant+entangled mode
#     in code, NOT a measurement of subjective experience.
#     Classical emulation throughout. Faggin's metaphysics
#     is interpretive and is NOT tested here.
#   - Per-field KS tests (n = 28) do NOT reject Planck --
#     they lack power. Only the pooled test (n = 168) is
#     gated, and it is reported alongside the per-field
#     values so the thin margin is visible.
#
# Pre-registered verdict rules for claims (xxix)-(xxxi),
# frozen from the pilot sweeps and never moved after the
# final measurement run (see the claim_*_verdict functions
# and REPORT.md section 17):
#   (xxix) Landauer ledger PASSES iff the per-bit cost at
#       T = 300 K equals k_B T ln 2 within 0.1% (exact
#       constants -- a definition check) AND the per-field
#       cost attains its maximum at an INTERIOR sigma (not
#       an endpoint) AND the cost at sigma = 0.25 exceeds
#       the cost at sigma = 0.0 and at sigma = 1.0. Pilot:
#       44.00, 44.00, 44.88, 52.53, 58.46, 52.37, 49.73
#       bits -- peak 58.46 at sigma = 0.25.
#   (xxx) Cost predicts the break PASSES iff, pooled over
#       seeds 1, 2, 3, 42 x the standard sigma grid,
#       |Pearson r(F, cumulative cost)| > |Pearson r(F,
#       sigma)|, where F is the v0.4.0 visible fraction
#       (the post-empathy attunement variable). Pilot:
#       0.8996 < 0.9430 -- the cost does NOT beat sigma,
#       so the claim is expected to FAIL honestly: the
#       thermodynamic ledger does not explain the
#       sigma = 0.50 break better than sigma itself.
#   (xxxi) Planck spectral falsification PASSES iff the
#       pooled standardized nu distribution REJECTS the
#       Planck shape (KS D above the 1% critical value
#       1.63 / sqrt(n)) AND at every sigma >= 0.25 the
#       mode/mean ratio deviates from the Planck value
#       0.7361 by more than SPECTRAL_MODE_DEVIATION_MIN
#       (0.30). Pilot: pooled D = 0.1465 > 0.1257; ratios
#       0.28, 0.18, 1.09 (deviations 0.46, 0.56, 0.35).
#       A PASS here demotes E = h*nu from "spectrum" to
#       "per-mode unit" -- the falsification succeeding is
#       the result.
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Landauer-cost ledger and the Planck spectral falsification."""

import numpy as np

import bridge
import empathy_field as ef
import planck_empathy as pe
import qualia as qu
import thought as th

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_N_AGENTS = ef.DEFAULT_N_AGENTS_RESONANCE
DEFAULT_SEED = ef.DEFAULT_SEED
COST_PREDICTION_SEEDS = (1, 2, 3, 42)

# Boltzmann constant, exact SI (J/K). T = 300 K room temperature.
K_B_SI = 1.380649e-23
T_ROOM_K = 300.0

# ---------------------------------------------------------------------------
# Pre-registered thresholds (frozen from the pilot sweeps,
# REPORT.md section 17, and never moved after the final
# measurement run).
# ---------------------------------------------------------------------------

# Per-bit cost check: exact constants, 0.1% is a round
# number far above floating-point error (~1e-15).
LANDAUER_PER_BIT_TOL = 0.001

# The ledger's interior-peak sigma (pilot: peak at 0.25).
LEDGER_PEAK_SIGMA = 0.25

# Spectral falsification: mode/mean must deviate from the
# Planck ratio by more than this at every sigma >= 0.25.
# Pilot deviations: 0.46, 0.56, 0.35 -- 0.30 is a round
# number below all three, not tuned to the edge.
SPECTRAL_MODE_DEVIATION_MIN = 0.30
SPECTRAL_MODE_SIGMA_MIN = 0.25

# KS 1% critical value factor: D_crit = 1.63 / sqrt(n).
KS_CRITICAL_FACTOR = 1.63


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("LANDAUER_PER_BIT_TOL", LANDAUER_PER_BIT_TOL),
        ("LEDGER_PEAK_SIGMA", LEDGER_PEAK_SIGMA),
        ("SPECTRAL_MODE_DEVIATION_MIN",
         SPECTRAL_MODE_DEVIATION_MIN),
        ("KS_CRITICAL_FACTOR", KS_CRITICAL_FACTOR),
    ) if value is None]
    if missing:
        raise ValueError(
            "landauer thresholds are unset: run the pilot "
            "sweeps and set " + ", ".join(missing) + " first "
            "(REPORT.md section 17)")
    return {
        "per_bit_tol": float(LANDAUER_PER_BIT_TOL),
        "ledger_peak_sigma": float(LEDGER_PEAK_SIGMA),
        "mode_deviation_min": float(SPECTRAL_MODE_DEVIATION_MIN),
        "ks_factor": float(KS_CRITICAL_FACTOR),
    }


# ---------------------------------------------------------------------------
# Landauer cost
# ---------------------------------------------------------------------------

def landauer_cost_joules(n_bits, temperature_k=T_ROOM_K):
    """Landauer cost (J) of erasing n_bits at temperature_k.

    k_B T ln 2 per bit. n_bits may be fractional (decision
    entropies are real-valued, not integers).
    """
    temperature_k = float(temperature_k)
    if temperature_k <= 0.0:
        raise ValueError("temperature_k must be positive")
    n_bits = float(n_bits)
    if n_bits < 0.0:
        raise ValueError("n_bits must be non-negative")
    return n_bits * K_B_SI * temperature_k * np.log(2.0)


def landauer_per_bit_joules(temperature_k=T_ROOM_K):
    """The Landauer bound per bit (J) at temperature_k."""
    return landauer_cost_joules(1.0, temperature_k)


# ---------------------------------------------------------------------------
# The ledger: bits erased per field
# ---------------------------------------------------------------------------

def field_ledger(states, r_min=None, nu_min=None,
                 temperature_k=T_ROOM_K):
    """The Landauer ledger for one field.

    Bits: decision entropies (thought collapses) + quale
    count (quale collapses, 1 bit each) + N_pairs
    (classification records erased on the next field).
    Cost: bits * k_B T ln 2.
    """
    states = list(states)
    if len(states) < 2:
        raise ValueError("need at least two agents for a field")
    n_pairs = len(states) * (len(states) - 1) // 2
    decision_bits = float(
        sum(th.decision_entropy(s) for s in states))
    n_qualia = qu.qualia_count(states, r_min=r_min, nu_min=nu_min)
    classification_bits = float(n_pairs)
    total_bits = decision_bits + float(n_qualia) + classification_bits
    return {
        "n_agents": len(states),
        "n_pairs": n_pairs,
        "decision_bits": decision_bits,
        "n_qualia": int(n_qualia),
        "quale_bits": float(n_qualia),
        "classification_bits": classification_bits,
        "total_bits": total_bits,
        "cost_joules": landauer_cost_joules(
            total_bits, temperature_k),
    }


def ledger_vs_noise(sigmas=None, n_agents=DEFAULT_N_AGENTS,
                    seed=DEFAULT_SEED, temperature_k=T_ROOM_K):
    """One ledger row per sigma, with cumulative bits and cost."""
    rows = []
    cum_bits = 0.0
    for sigma in (ef.SIGMA_GRID if sigmas is None else sigmas):
        states = ef.resonance_population(sigma, n_agents, seed)
        ledger = field_ledger(states, temperature_k=temperature_k)
        cum_bits += ledger["total_bits"]
        f = float(ef.empathy_fraction(states))
        rows.append({
            "sigma": float(sigma),
            "f": f,
            "visible_fraction": pe.empathy_mapping(f)[
                "visible_fraction"],
            "decision_bits": ledger["decision_bits"],
            "n_qualia": ledger["n_qualia"],
            "classification_bits": ledger["classification_bits"],
            "total_bits": ledger["total_bits"],
            "cost_joules": ledger["cost_joules"],
            "cumulative_bits": cum_bits,
            "cumulative_cost_joules": landauer_cost_joules(
                cum_bits, temperature_k),
        })
    return rows


# ---------------------------------------------------------------------------
# Planck spectral shape (numerical, scale-free)
# ---------------------------------------------------------------------------

def _planck_standardized():
    """The standardized Planck shape: density, mean, mode.

    x = nu / theta; density ~ x^3 / (exp(x) - 1). The grid
    runs to x = 60, where the density is ~1e-24 of its peak.
    Returns (xs, cdf, mean_x, mode_x).
    """
    xs = np.linspace(0.0, 60.0, 60001)
    with np.errstate(divide="ignore", invalid="ignore"):
        dens = np.where(xs == 0.0, 0.0,
                        xs ** 3 / np.expm1(xs))
    dens = dens / np.trapz(dens, xs)
    mean_x = float(np.trapz(xs * dens, xs))
    cdf = np.cumsum(dens) * (xs[1] - xs[0])
    cdf = cdf / cdf[-1]
    mode_x = float(xs[np.argmax(dens)])
    return xs, cdf, mean_x, mode_x


_PLANCK_XS, _PLANCK_CDF, _PLANCK_MEAN_X, _PLANCK_MODE_X = (
    _planck_standardized())


def planck_mean_x():
    """Mean of x = nu/theta under the Planck shape (3.8322)."""
    return _PLANCK_MEAN_X


def planck_mode_x():
    """Mode of x = nu/theta under the Planck shape (2.8210)."""
    return _PLANCK_MODE_X


def planck_mode_mean_ratio():
    """Mode/mean under any Planck spectrum (0.7361, fixed)."""
    return _PLANCK_MODE_X / _PLANCK_MEAN_X


def _planck_cdf_y(y):
    """CDF of y = nu / mean(nu) under the Planck shape."""
    x = np.asarray(y, dtype=float) * _PLANCK_MEAN_X
    return np.interp(x, _PLANCK_XS, _PLANCK_CDF,
                     left=0.0, right=1.0)


def ks_statistic(samples):
    """Two-sided KS statistic of samples against the Planck shape.

    Samples are standardized nu values (nu / mean(nu) within
    their own field). Returns D in [0, 1].
    """
    s = np.sort(np.asarray(samples, dtype=float))
    if len(s) == 0:
        raise ValueError("need at least one sample for the KS test")
    n = len(s)
    ecdf = np.arange(1, n + 1) / n
    cdf_vals = _planck_cdf_y(s)
    d_plus = float(np.max(ecdf - cdf_vals))
    d_minus = float(np.max(cdf_vals - (np.arange(0, n) / n)))
    return max(d_plus, d_minus)


def ks_critical_value(n, factor=None):
    """The 1% KS critical value 1.63 / sqrt(n)."""
    factor = KS_CRITICAL_FACTOR if factor is None else float(factor)
    return factor / np.sqrt(float(n))


def spectral_rows(sigmas=None, n_agents=DEFAULT_N_AGENTS,
                 seed=DEFAULT_SEED, n_bins=10):
    """Per-sigma standardized nu: KS D, mode, mode/mean.

    The mode is the centre of the modal histogram bin over
    nu in [0, 1] (10 bins). Rows with mean nu == 0 carry no
    distribution to test (KS and mode are None).
    """
    rows = []
    for sigma in (ef.SIGMA_GRID if sigmas is None else sigmas):
        states = ef.resonance_population(sigma, n_agents, seed)
        nus = np.array([ef.pair_frequency(states[i], states[j])
                        for i in range(len(states))
                        for j in range(i + 1, len(states))])
        mean_nu = float(np.mean(nus))
        if mean_nu <= 0.0:
            rows.append({
                "sigma": float(sigma),
                "mean_nu": mean_nu,
                "n_pairs": len(nus),
                "ks_d": None,
                "mode_nu": None,
                "mode_mean_ratio": None,
            })
            continue
        y = nus / mean_nu
        hist, edges = np.histogram(nus, bins=n_bins, range=(0.0, 1.0))
        mode_nu = float(edges[int(np.argmax(hist))]
                        + 0.5 * (edges[1] - edges[0]))
        rows.append({
            "sigma": float(sigma),
            "mean_nu": mean_nu,
            "n_pairs": len(nus),
            "ks_d": ks_statistic(y),
            "mode_nu": mode_nu,
            "mode_mean_ratio": mode_nu / mean_nu,
        })
    return rows


def pooled_standardized_nu(sigmas=None, n_agents=DEFAULT_N_AGENTS,
                           seed=DEFAULT_SEED):
    """All per-field standardized nu values pooled (mean > 0 fields)."""
    pooled = []
    for sigma in (ef.SIGMA_GRID if sigmas is None else sigmas):
        states = ef.resonance_population(sigma, n_agents, seed)
        nus = np.array([ef.pair_frequency(states[i], states[j])
                        for i in range(len(states))
                        for j in range(i + 1, len(states))])
        if np.mean(nus) > 0.0:
            pooled.extend((nus / np.mean(nus)).tolist())
    return pooled


# ---------------------------------------------------------------------------
# Claims (xxix)-(xxxi): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_ledger_verdict(sigmas=None, n_agents=DEFAULT_N_AGENTS,
                         seed=DEFAULT_SEED,
                         temperature_k=T_ROOM_K):
    """(xxix) The Landauer ledger is exact and its cost humps.

    PASS iff the per-bit cost equals k_B T ln 2 within
    LANDAUER_PER_BIT_TOL AND the per-field cost attains its
    maximum at an interior sigma (not an endpoint) AND the
    cost at LEDGER_PEAK_SIGMA exceeds the cost at both
    endpoints of the grid.
    """
    t = _thresholds()
    per_bit = landauer_per_bit_joules(temperature_k)
    exact = K_B_SI * temperature_k * np.log(2.0)
    check_exact = abs(per_bit - exact) / exact <= t["per_bit_tol"]
    rows = ledger_vs_noise(sigmas, n_agents, seed, temperature_k)
    costs = [r["cost_joules"] for r in rows]
    peak_idx = int(np.argmax(costs))
    check_interior = 0 < peak_idx < len(rows) - 1
    peak_row = rows[peak_idx]
    check_peak_sigma = peak_row["sigma"] == t["ledger_peak_sigma"]
    check_above_ends = (peak_row["cost_joules"] > costs[0]
                        and peak_row["cost_joules"] > costs[-1])
    passed = bool(check_exact and check_interior
                  and check_peak_sigma and check_above_ends)
    return {
        "claim": "(xxix) the Landauer ledger is exact and its "
                 "cost humps",
        "passed": passed,
        "checks": {
            "per_bit_cost_exact": bool(check_exact),
            "peak_at_interior_sigma": bool(check_interior),
            "peak_at_registered_sigma": bool(check_peak_sigma),
            "peak_above_both_endpoints": bool(check_above_ends),
        },
        "per_bit_tol": t["per_bit_tol"],
        "per_bit_joules": per_bit,
        "kbt_ln2_joules": exact,
        "peak_sigma": peak_row["sigma"],
        "peak_bits": peak_row["total_bits"],
        "peak_cost_joules": peak_row["cost_joules"],
        "total_cost_joules": float(sum(costs)),
        "rows": rows,
    }


def claim_cost_predicts_verdict(seeds=COST_PREDICTION_SEEDS,
                                sigmas=None,
                                n_agents=DEFAULT_N_AGENTS,
                                temperature_k=T_ROOM_K):
    """(xxx) Cumulative Landauer cost predicts F better than sigma.

    PASS iff |Pearson r(F, cumulative cost)| > |Pearson
    r(F, sigma)|, pooled over the seeds x the sigma grid.
    F is the v0.4.0 visible fraction (the post-empathy
    attunement variable); A itself is constant, so it
    cannot be regressed. The cumulative cost is in bits
    (cost is bits times a constant, so the correlation is
    identical in joules). Pilot: 0.8996 < 0.9430 -- the
    claim is expected to FAIL, and the threshold is not
    moved to force a pass.
    """
    grid = ef.SIGMA_GRID if sigmas is None else sigmas
    sig_values, cum_values, f_values = [], [], []
    per_seed = []
    for seed in seeds:
        rows = ledger_vs_noise(grid, n_agents, seed, temperature_k)
        sig_values += [r["sigma"] for r in rows]
        cum_values += [r["cumulative_bits"] for r in rows]
        f_values += [r["visible_fraction"] for r in rows]
        per_seed.append({
            "seed": seed,
            "r_f_sigma": float(np.corrcoef(
                [r["visible_fraction"] for r in rows],
                [r["sigma"] for r in rows])[0, 1]),
            "r_f_cum": float(np.corrcoef(
                [r["visible_fraction"] for r in rows],
                [r["cumulative_bits"] for r in rows])[0, 1]),
        })
    r_sigma = float(np.corrcoef(f_values, sig_values)[0, 1])
    r_cum = float(np.corrcoef(f_values, cum_values)[0, 1])
    check = abs(r_cum) > abs(r_sigma)
    passed = bool(check)
    return {
        "claim": "(xxx) cumulative Landauer cost predicts F "
                 "better than sigma alone",
        "passed": passed,
        "checks": {
            "abs_r_cost_greater_than_abs_r_sigma": bool(check),
        },
        "r_f_sigma": r_sigma,
        "r_f_cumulative_cost": r_cum,
        "n_rows": len(f_values),
        "seeds": list(seeds),
        "per_seed": per_seed,
    }


def claim_planck_spectral_verdict(sigmas=None,
                                  n_agents=DEFAULT_N_AGENTS,
                                  seed=DEFAULT_SEED):
    """(xxxi) The empathy spectrum is NOT Planckian.

    PASS iff the pooled standardized nu distribution
    rejects the Planck shape (KS D above the 1% critical
    value 1.63 / sqrt(n)) AND at every sigma >=
    SPECTRAL_MODE_SIGMA_MIN the mode/mean ratio deviates
    from the Planck value by more than
    SPECTRAL_MODE_DEVIATION_MIN. A PASS demotes E = h*nu
    from "spectrum" to "per-mode unit".
    """
    t = _thresholds()
    pooled = pooled_standardized_nu(sigmas, n_agents, seed)
    d_pooled = ks_statistic(pooled)
    d_crit = ks_critical_value(len(pooled), t["ks_factor"])
    check_ks = d_pooled > d_crit
    rows = spectral_rows(sigmas, n_agents, seed)
    gated = [r for r in rows
             if r["mode_mean_ratio"] is not None
             and r["sigma"] >= SPECTRAL_MODE_SIGMA_MIN]
    planck_ratio = planck_mode_mean_ratio()
    deviations = [abs(r["mode_mean_ratio"] - planck_ratio)
                  for r in gated]
    check_mode = bool(gated) and all(
        dev > t["mode_deviation_min"] for dev in deviations)
    passed = bool(check_ks and check_mode)
    return {
        "claim": "(xxxi) the empathy spectrum is not Planckian",
        "passed": passed,
        "checks": {
            "pooled_ks_rejects_planck": bool(check_ks),
            "mode_mean_ratio_deviates_everywhere": bool(check_mode),
        },
        "ks_factor": t["ks_factor"],
        "pooled_n": len(pooled),
        "pooled_ks_d": d_pooled,
        "pooled_ks_critical_1pct": d_crit,
        "planck_mode_mean_ratio": planck_ratio,
        "mode_deviation_min": t["mode_deviation_min"],
        "mode_ratios": [(r["sigma"], r["mode_mean_ratio"],
                         abs(r["mode_mean_ratio"] - planck_ratio)
                         if r["mode_mean_ratio"] is not None
                         else None)
                        for r in rows],
        "per_field_ks": [(r["sigma"], r["ks_d"]) for r in rows],
        "rows": rows,
    }


def landauer_claims():
    """The three Landauer claims (xxix)-(xxxi), measured fresh."""
    claim_xxix = claim_ledger_verdict()
    claim_xxx = claim_cost_predicts_verdict()
    claim_xxxi = claim_planck_spectral_verdict()
    verdicts = [claim_xxix, claim_xxx, claim_xxxi]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_xxix_ledger": claim_xxix,
        "claim_xxx_cost_predicts": claim_xxx,
        "claim_xxxi_planck_spectral": claim_xxxi,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the ledger, the cost-prediction comparison, and
    the Planck spectral test with the claims (xxix)-(xxxi)
    verdicts."""
    print("Landauer-cost ledger + Planck spectral falsification "
          "-- claims (xxix)-(xxxi)")
    print()
    verdicts = landauer_claims()
    xxix = verdicts["claim_xxix_ledger"]
    print(f"Landauer per bit at {T_ROOM_K:.0f} K: "
          f"{xxix['per_bit_joules']:.4e} J "
          f"(k_B T ln 2 = {xxix['kbt_ln2_joules']:.4e} J)")
    print("Ledger per field (seed 42):")
    for r in xxix["rows"]:
        print(f"  sigma = {r['sigma']:>5}: decision = "
              f"{r['decision_bits']:5.2f} bits, qualia = "
              f"{r['n_qualia']:>2}, classif. = "
              f"{r['classification_bits']:4.0f}, total = "
              f"{r['total_bits']:5.2f} bits, cost = "
              f"{r['cost_joules']:.3e} J")
    print(f"  peak {xxix['peak_bits']:.2f} bits at sigma = "
          f"{xxix['peak_sigma']}, total across grid = "
          f"{xxix['total_cost_joules']:.3e} J")
    print(f"claim (xxix) verdict: {'PASS' if xxix['passed'] else 'FAIL'}")
    print()
    xxx = verdicts["claim_xxx_cost_predicts"]
    print("Cost vs sigma as predictors of F (visible fraction):")
    print(f"  pooled r(F, sigma) = {xxx['r_f_sigma']:.4f}")
    print(f"  pooled r(F, cumulative cost) = "
          f"{xxx['r_f_cumulative_cost']:.4f}")
    for s in xxx["per_seed"]:
        print(f"  seed {s['seed']}: r(F, sigma) = "
              f"{s['r_f_sigma']:.4f}, r(F, cum) = "
              f"{s['r_f_cum']:.4f}")
    print(f"claim (xxx) verdict: {'PASS' if xxx['passed'] else 'FAIL'}")
    print()
    xxxi = verdicts["claim_xxxi_planck_spectral"]
    print(f"Planck standardized shape: mean x = "
          f"{planck_mean_x():.4f}, mode x = {planck_mode_x():.4f}, "
          f"mode/mean = {xxxi['planck_mode_mean_ratio']:.4f}")
    print(f"  pooled KS D = {xxxi['pooled_ks_d']:.4f} "
          f"(1% crit {xxxi['pooled_ks_critical_1pct']:.4f}, "
          f"n = {xxxi['pooled_n']})")
    print("  per-field KS D (reported, not gated): "
          + ", ".join(f"{s}: {d:.4f}" if d is not None else f"{s}: None"
                      for s, d in xxxi["per_field_ks"]))
    print("  mode/mean per sigma (deviation from Planck in parens):")
    for sigma, ratio, dev in xxxi["mode_ratios"]:
        print(f"    sigma = {sigma:>5}: "
              + ("None" if ratio is None
                 else f"{ratio:.4f} ({dev:.4f})"))
    print(f"claim (xxxi) verdict: "
          f"{'PASS' if xxxi['passed'] else 'FAIL'}")
    print()
    print(f"claims (xxix)-(xxxi): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
