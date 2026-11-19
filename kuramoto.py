# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# kuramoto.py
#
# Kuramoto bounded-coherence / stochastic-resonance scan
# (deep-think upgrade #4, v0.13.0).
#
# The construction, stated up front:
#   - Kuramoto model (established): N phase oscillators,
#     natural frequencies omega_i ~ N(0, 1), coupling K,
#     Langevin noise sigma. Euler-Maruyama, dt = 0.05,
#     T = 40, first half discarded as transient. Order
#     parameter R_K = |<exp(i theta)>| averaged over the
#     steady window.
#   - Wiring into the bridge: each agent's state is the
#     (xxxiv) slide state at its phase RELATIVE to the
#     field mean, phi_i = ((theta_i - theta_bar) mod 2pi)
#     / 4, theta_bar the circular mean phase. Only
#     relative phases carry information — the Kuramoto
#     model has a global rotational symmetry, so the
#     absolute lock angle is a gauge freedom and is
#     removed by the rotation. At full sync every agent
#     sits at phi = 0 (the uniform thought, D = 1,
#     C = 0); at K = 0 the phases spread over the whole
#     slide. The slide states reuse observer_cycle
#     exactly: D = cos^2(phi), C = sin^2(phi).
#   - Quale count: the existing qualia_count(states)
#     (R >= 0.5, nu >= 0.10). Joint entropy: the exact
#     independent-draw joint entropy, sum of per-agent
#     Born entropies (no sampling cap — with N agents
#     the sampled estimator saturates at log2(n_samples)
#     and the gap would compress; the analytic value is
#     exact for the product distribution). The
#     collaboration gap A: paired arms on the same
#     Kuramoto population, mirroring run_collaboration
#     design B — collaborating mixes with the field at
#     coupling R_K (the MEASURED order parameter, a
#     measured quantity in [0, 1], the same role f plays
#     in run_collaboration), isolated Born-collapses
#     (decides) once; A = H_collab - H_isolated. In the
#     single-shot measurement the collapse leaves each
#     isolated agent in a basis state, so H_isolated = 0
#     exactly and A = H_collaborating; that triviality
#     is reported, not hidden. (In run_collaboration the
#     noise kicks re-noise the decided states across
#     generations, so H_isolated > 0 there.)
#   - The bounded-coherence band R ~ 0.5-0.8 is the
#     Phillips 2026 preprint hypothesis (Zenodo,
#     not peer-reviewed): used as a prediction to test,
#     not as an established fact. f* = 0.7278 (the
#     bridge's PARTIAL -> ATTUNED flip) is reported
#     alongside the measured optimum band for
#     comparison, not as a target the scan must hit.
#
# Claims (xxxvi)-(xxxix), pre-registered in
# docs/preregistration-v0.13.0.md BEFORE the evaluation
# run. Thresholds are round numbers frozen from a
# calibration pilot on seeds 42 and 7; the evaluation
# seeds are 1234 and 2026.
#
# Honesty, stated up front:
#   - The wiring (slide states from relative phases,
#     mixing at coupling R_K) is a construction, not a
#     discovery: the inverted-U, if present, is a
#     property of this construction — the product of
#     two opposing trends (the R condition improves as
#     the cluster tightens, the nu condition worsens as
#     the cluster centres on the uniform end). Like the
#     product model (v0.10.0), the shape is the test.
#   - The analytic joint entropy is not the sampled
#     joint entropy of run_collaboration; the Kuramoto
#     gap A is the same concept (H_collab - H_isolated)
#     with an exact estimator, and the two As are
#     reported side by side, not equated.
#   - None of this measures coherence, stability, or
#     consciousness in a living system. Classical
#     emulation throughout. Faggin's metaphysics stays
#     interpretive.
#

"""Kuramoto bounded-coherence scan: R_K, joint entropy, quale count, and A."""

import math

import numpy as np

import bridge
import cost
import empathy_field as ef
import observer_cycle as oc
import qualia
import thought

# ---------------------------------------------------------------------------
# Seeds
# ---------------------------------------------------------------------------

# Calibration seeds: thresholds were frozen from these only.
CALIBRATION_SEEDS = (42, 7)
# Evaluation seeds: held out until the evaluation run.
EVALUATION_SEEDS = (1234, 2026)
ALL_SEEDS = CALIBRATION_SEEDS + EVALUATION_SEEDS

# ---------------------------------------------------------------------------
# Kuramoto construction (fixed before the pilot; not thresholds)
# ---------------------------------------------------------------------------

N_AGENTS = 8
DT = 0.05
T_TOTAL = 40.0
N_STEPS = int(T_TOTAL / DT)
BURN_IN_STEPS = N_STEPS // 2

# Coupling grid: spans below and above the critical coupling
# K_c ~ 1.6 for Gaussian natural frequencies (K_c = 2 / (pi
# g(0)), g(0) = 1/sqrt(2 pi)).
K_GRID = [0.0, 0.5, 1.0, 1.6, 2.5, 4.0, 8.0]
# Noise grid: the Kuramoto Langevin noise sigma.
SIGMA_GRID = [0.0, 0.05, 0.1, 0.25, 0.5, 1.0]

# ---------------------------------------------------------------------------
# Pre-registered thresholds (frozen from the calibration pilot,
# docs/preregistration-v0.13.0.md; never moved after the run).
# ---------------------------------------------------------------------------

# Claim (xxxvi): inverted-U in quale count vs K at sigma = 0.
# Peak count must exceed both ends by at least this margin.
COUNT_PEAK_MARGIN_MIN = 3
# Claim (xxxvii): inverted-U in joint entropy vs K at sigma = 0.
# Peak H must exceed both ends by at least this margin (bits).
H_PEAK_MARGIN_MIN = 0.5
# Claim (xxxviii): R_K at the count peak inside the Phillips band.
RK_BAND_LO = 0.5
RK_BAND_HI = 0.8
# Claim (xxxix): stochastic resonance — at fixed K (the
# count-optimal K from calibration), the count peaks at
# sigma* > 0; the peak count must exceed the sigma = 0 count
# by at least this margin. K fixed at 1.0 (near the critical
# coupling, where noise matters most — fixed before the pilot).
FIXED_K_XXXIX = 1.0
COUNT_SIGMA_MARGIN_MIN = 3


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("COUNT_PEAK_MARGIN_MIN", COUNT_PEAK_MARGIN_MIN),
        ("H_PEAK_MARGIN_MIN", H_PEAK_MARGIN_MIN),
        ("RK_BAND_LO", RK_BAND_LO),
        ("RK_BAND_HI", RK_BAND_HI),
        ("FIXED_K_XXXIX", FIXED_K_XXXIX),
        ("COUNT_SIGMA_MARGIN_MIN", COUNT_SIGMA_MARGIN_MIN),
    ) if value is None]
    if missing:
        raise ValueError(
            "kuramoto thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.13.0.md)")
    return {
        "count_peak_margin_min": int(COUNT_PEAK_MARGIN_MIN),
        "h_peak_margin_min": float(H_PEAK_MARGIN_MIN),
        "rk_band_lo": float(RK_BAND_LO),
        "rk_band_hi": float(RK_BAND_HI),
        "fixed_k_xxxix": float(FIXED_K_XXXIX),
        "count_sigma_margin_min": int(COUNT_SIGMA_MARGIN_MIN),
    }


# ---------------------------------------------------------------------------
# Kuramoto dynamics (standard model, established)
# ---------------------------------------------------------------------------

def kuramoto_run(k_coupling, sigma, n_agents=N_AGENTS, seed=42,
                 dt=DT, t_total=T_TOTAL):
    """Run Kuramoto dynamics and return the steady state.

    Natural frequencies omega_i ~ N(0, 1), initial phases
    uniform on [0, 2pi), both seeded. Euler-Maruyama:
    dtheta_i = (omega_i + (K/N) sum_j sin(theta_j - theta_i)) dt
    + sigma dW_i. Returns the final phases, the steady-window
    mean order parameter R_K, and the per-step R_K series.
    """
    rng = np.random.default_rng(int(seed))
    n = int(n_agents)
    steps = int(t_total / float(dt))
    burn = steps // 2
    omega = rng.standard_normal(n)
    theta = rng.uniform(0.0, 2.0 * math.pi, n)
    rk_series = []
    for _ in range(steps):
        mean_sin = np.mean(np.sin(theta))
        mean_cos = np.mean(np.cos(theta))
        interaction = (mean_sin * np.cos(theta)
                       - mean_cos * np.sin(theta))
        noise = (rng.standard_normal(n) * math.sqrt(dt)
                 if float(sigma) > 0.0 else 0.0)
        theta = theta + (omega + float(k_coupling) * interaction) * dt + float(sigma) * noise
        theta = np.mod(theta, 2.0 * math.pi)
        rk_series.append(float(abs(np.mean(np.exp(1j * theta)))))
    rk_steady = float(np.mean(rk_series[burn:]))
    return {
        "k": float(k_coupling),
        "sigma": float(sigma),
        "seed": int(seed),
        "n_agents": n,
        "theta_final": theta,
        "rk_steady": rk_steady,
        "rk_series": rk_series,
    }


def slide_angles(theta):
    """Relative slide angles: phases relative to the field mean.

    phi_i = ((theta_i - theta_bar) mod 2pi) / 4 in [0, pi/2),
    theta_bar the circular mean phase. The global rotation is
    a gauge freedom of the Kuramoto model and is removed.
    """
    theta = np.asarray(theta, dtype=float)
    mean_phase = float(np.angle(np.mean(np.exp(1j * theta))))
    rel = np.mod(theta - mean_phase, 2.0 * math.pi)
    return rel / 4.0


def kuramoto_states(k_coupling, sigma, n_agents=N_AGENTS, seed=42):
    """Agent states from a Kuramoto run: slide states at the
    relative phases. Returns the run, the angles, and the states."""
    run = kuramoto_run(k_coupling, sigma, n_agents=n_agents,
                       seed=seed)
    angles = slide_angles(run["theta_final"])
    states = [oc.slide_state(float(a)) for a in angles]
    return {
        "run": run,
        "angles": angles,
        "states": states,
        "rk": run["rk_steady"],
    }


# ---------------------------------------------------------------------------
# Bridge quantities on a Kuramoto population
# ---------------------------------------------------------------------------

def joint_entropy_analytic(states):
    """Exact independent-draw joint entropy (bits): the sum of
    the per-agent Born entropies. No sampling cap."""
    total = 0.0
    for s in states:
        p = np.asarray(thought.born_probabilities(s), dtype=float)
        p = p / np.sum(p)
        total += cost.shannon_entropy([float(v) for v in p])
    return float(total)


def kuramoto_collaboration_gap(states, rk, seed=42):
    """Paired arms on one Kuramoto population, mirroring
    run_collaboration design B.

    Collaborating mixes with the field at coupling R_K (the
    measured order parameter); isolated Born-collapses
    (decides) once, with the per-agent seeds of
    run_collaboration (seed + 4242 + 10*i). A =
    H_collab - H_isolated, analytic joint entropies.
    Note: a single-shot collapse leaves each isolated
    agent in a basis state, so H_isolated = 0 exactly and
    A = H_collaborating — reported as such, not hidden.
    (In run_collaboration the noise kicks re-noise the
    decided states across generations, so H_isolated > 0
    there; the single-shot Kuramoto measurement has no
    generations, and the trivial isolated arm is part of
    the result, not a defect to paper over.)
    """
    mixed = ef._field_mix(list(states), float(rk))
    collapsed = []
    for i, s in enumerate(list(states)):
        _, decided = thought.collapse(s, seed=int(seed) + 4242 + 10 * i)
        collapsed.append(np.asarray(decided, dtype=complex))
    return {
        "h_collaborating_bits": joint_entropy_analytic(mixed),
        "h_isolated_bits": joint_entropy_analytic(collapsed),
        "gap_bits": (joint_entropy_analytic(mixed)
                     - joint_entropy_analytic(collapsed)),
    }


def kuramoto_point(k_coupling, sigma, n_agents=N_AGENTS, seed=42):
    """One (K, sigma) point: R_K, quale count, joint entropy, A."""
    pop = kuramoto_states(k_coupling, sigma, n_agents=n_agents,
                          seed=seed)
    states = pop["states"]
    rk = pop["rk"]
    gap = kuramoto_collaboration_gap(states, rk, seed=seed)
    return {
        "k": float(k_coupling),
        "sigma": float(sigma),
        "seed": int(seed),
        "rk": rk,
        "n_qualia": qualia.qualia_count(states),
        "h_joint_bits": joint_entropy_analytic(states),
        "gap_bits": gap["gap_bits"],
        "h_collaborating_bits": gap["h_collaborating_bits"],
        "h_isolated_bits": gap["h_isolated_bits"],
    }


def kuramoto_scan_k(sigmas=0.0, k_grid=None, n_agents=N_AGENTS,
                    seed=42):
    """Scan over K at fixed sigma (default 0.0)."""
    rows = []
    for k in (K_GRID if k_grid is None else k_grid):
        rows.append(kuramoto_point(k, sigmas, n_agents=n_agents,
                                   seed=seed))
    return rows


def kuramoto_scan_sigma(k_fixed, sigma_grid=None, n_agents=N_AGENTS,
                        seed=42):
    """Scan over sigma at fixed K."""
    rows = []
    for sigma in (SIGMA_GRID if sigma_grid is None else sigma_grid):
        rows.append(kuramoto_point(k_fixed, sigma, n_agents=n_agents,
                                   seed=seed))
    return rows


# ---------------------------------------------------------------------------
# Claims (xxxvi)-(xxxix): pre-registered verdicts
# ---------------------------------------------------------------------------

def _peak_row(rows, key):
    """The row with the maximal value of key; ties broken by
    the smallest grid coordinate (K or sigma)."""
    best = None
    for r in rows:
        if best is None or r[key] > best[key]:
            best = r
    return best


def claim_count_inverted_u_verdict(seeds=None):
    """(xxxvi) Inverted-U in quale count vs K at sigma = 0.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}, the
    count peaks at an INTERIOR grid point (0 < K < 8.0)
    and exceeds both ends by at least COUNT_PEAK_MARGIN_MIN.
    """
    t = _thresholds()
    per_seed = []
    for s in (ALL_SEEDS if seeds is None else seeds):
        rows = kuramoto_scan_k(seed=s)
        peak = _peak_row(rows, "n_qualia")
        per_seed.append({
            "seed": int(s),
            "rows": rows,
            "k_peak": peak["k"],
            "count_peak": peak["n_qualia"],
            "count_k0": rows[0]["n_qualia"],
            "count_kmax": rows[-1]["n_qualia"],
            "rk_at_peak": peak["rk"],
        })
    checks = {
        "peak_interior": all(
            0.0 < r["k_peak"] < K_GRID[-1] for r in per_seed),
        "peak_above_k0": all(
            r["count_peak"] - r["count_k0"]
            >= t["count_peak_margin_min"] for r in per_seed),
        "peak_above_kmax": all(
            r["count_peak"] - r["count_kmax"]
            >= t["count_peak_margin_min"] for r in per_seed),
    }
    return {
        "claim": "(xxxvi) inverted-U in quale count vs K",
        "passed": bool(all(checks.values())),
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_h_inverted_u_verdict(seeds=None):
    """(xxxvii) Inverted-U in joint entropy vs K at sigma = 0.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}, H_joint
    peaks at an INTERIOR grid point and exceeds both ends
    by at least H_PEAK_MARGIN_MIN bits.
    """
    t = _thresholds()
    per_seed = []
    for s in (ALL_SEEDS if seeds is None else seeds):
        rows = kuramoto_scan_k(seed=s)
        peak = _peak_row(rows, "h_joint_bits")
        per_seed.append({
            "seed": int(s),
            "rows": rows,
            "k_peak": peak["k"],
            "h_peak": peak["h_joint_bits"],
            "h_k0": rows[0]["h_joint_bits"],
            "h_kmax": rows[-1]["h_joint_bits"],
        })
    checks = {
        "peak_interior": all(
            0.0 < r["k_peak"] < K_GRID[-1] for r in per_seed),
        "peak_above_k0": all(
            r["h_peak"] - r["h_k0"] >= t["h_peak_margin_min"]
            for r in per_seed),
        "peak_above_kmax": all(
            r["h_peak"] - r["h_kmax"] >= t["h_peak_margin_min"]
            for r in per_seed),
    }
    return {
        "claim": "(xxxvii) inverted-U in joint entropy vs K",
        "passed": bool(all(checks.values())),
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_rk_band_verdict(seeds=None):
    """(xxxviii) R_K at the count peak inside the Phillips band.

    The K where the count is maximal (ties: smallest such K);
    R_K there must lie in [RK_BAND_LO, RK_BAND_HI] on EVERY
    seed in {42, 7, 1234, 2026}. f* = 0.7278 is reported
    alongside, not gated.
    """
    t = _thresholds()
    per_seed = []
    for s in (ALL_SEEDS if seeds is None else seeds):
        rows = kuramoto_scan_k(seed=s)
        peak = _peak_row(rows, "n_qualia")
        per_seed.append({
            "seed": int(s),
            "k_peak": peak["k"],
            "count_peak": peak["n_qualia"],
            "rk_at_peak": peak["rk"],
        })
    checks = {
        "rk_in_band": all(
            t["rk_band_lo"] <= r["rk_at_peak"] <= t["rk_band_hi"]
            for r in per_seed),
    }
    return {
        "claim": "(xxxviii) R_K at the count peak in [0.5, 0.8]",
        "passed": bool(all(checks.values())),
        "checks": checks,
        "thresholds": t,
        "f_star": 0.7278,
        "per_seed": per_seed,
    }


def claim_sigma_resonance_verdict(seeds=None):
    """(xxxix) Stochastic resonance: optimum sigma* > 0.

    At fixed K = FIXED_K_XXXIX, PASS iff, on EVERY seed in
    {42, 7, 1234, 2026}, the count peaks at a STRICTLY
    INTERIOR sigma (0 < sigma* < 1.0) and exceeds the
    sigma = 0 count by at least COUNT_SIGMA_MARGIN_MIN.
    """
    t = _thresholds()
    per_seed = []
    for s in (ALL_SEEDS if seeds is None else seeds):
        rows = kuramoto_scan_sigma(t["fixed_k_xxxix"], seed=s)
        peak = _peak_row(rows, "n_qualia")
        per_seed.append({
            "seed": int(s),
            "rows": rows,
            "sigma_peak": peak["sigma"],
            "count_peak": peak["n_qualia"],
            "count_sigma0": rows[0]["n_qualia"],
        })
    checks = {
        "peak_interior": all(
            0.0 < r["sigma_peak"] < SIGMA_GRID[-1]
            for r in per_seed),
        "peak_above_sigma0": all(
            r["count_peak"] - r["count_sigma0"]
            >= t["count_sigma_margin_min"] for r in per_seed),
    }
    return {
        "claim": "(xxxix) stochastic resonance: optimum sigma* > 0",
        "passed": bool(all(checks.values())),
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def kuramoto_claims():
    """The Kuramoto claims (xxxvi)-(xxxix), measured fresh."""
    claim_xxxvi = claim_count_inverted_u_verdict()
    claim_xxxvii = claim_h_inverted_u_verdict()
    claim_xxxviii = claim_rk_band_verdict()
    claim_xxxix = claim_sigma_resonance_verdict()
    verdicts = [claim_xxxvi, claim_xxxvii, claim_xxxviii,
                claim_xxxix]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_xxxvi_count_inverted_u": claim_xxxvi,
        "claim_xxxvii_h_inverted_u": claim_xxxvii,
        "claim_xxxviii_rk_band": claim_xxxviii,
        "claim_xxxix_sigma_resonance": claim_xxxix,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the K scan at sigma = 0 and the sigma scan at the
    count-optimal K, for the calibration seed."""
    print("Kuramoto bounded-coherence scan -- claims (xxxvi)-(xxxix)")
    print()
    verdicts = kuramoto_claims()
    xxxvi = verdicts["claim_xxxvi_count_inverted_u"]
    print("Quale count vs K (sigma = 0), per seed:")
    for r in xxxvi["per_seed"]:
        print(f"  seed {r['seed']}: peak count "
              f"{r['count_peak']} at K = {r['k_peak']}, "
              f"K = 0: {r['count_k0']}, K = 8: {r['count_kmax']}, "
              f"R_K at peak = {r['rk_at_peak']:.4f}")
    print(f"claim (xxxvi) verdict: "
          f"{'PASS' if xxxvi['passed'] else 'FAIL'}")
    print()
    xxxvii = verdicts["claim_xxxvii_h_inverted_u"]
    print("Joint entropy vs K (sigma = 0), per seed:")
    for r in xxxvii["per_seed"]:
        print(f"  seed {r['seed']}: peak H = {r['h_peak']:.4f} "
              f"bits at K = {r['k_peak']}, K = 0: "
              f"{r['h_k0']:.4f}, K = 8: {r['h_kmax']:.4f}")
    print(f"claim (xxxvii) verdict: "
          f"{'PASS' if xxxvii['passed'] else 'FAIL'}")
    print()
    xxxviii = verdicts["claim_xxxviii_rk_band"]
    print("R_K at the count peak (Phillips band [0.5, 0.8], "
          f"f* = {xxxviii['f_star']}):")
    for r in xxxviii["per_seed"]:
        print(f"  seed {r['seed']}: R_K = {r['rk_at_peak']:.4f} "
              f"at K = {r['k_peak']}")
    print(f"claim (xxxviii) verdict: "
          f"{'PASS' if xxxviii['passed'] else 'FAIL'}")
    print()
    xxxix = verdicts["claim_xxxix_sigma_resonance"]
    print(f"Count vs sigma at fixed K = "
          f"{xxxix['thresholds']['fixed_k_xxxix']}, per seed:")
    for r in xxxix["per_seed"]:
        print(f"  seed {r['seed']}: peak count "
              f"{r['count_peak']} at sigma = {r['sigma_peak']}, "
              f"sigma = 0: {r['count_sigma0']}")
    print(f"claim (xxxix) verdict: "
          f"{'PASS' if xxxix['passed'] else 'FAIL'}")
    print()
    print(f"claims (xxxvi)-(xxxix): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
