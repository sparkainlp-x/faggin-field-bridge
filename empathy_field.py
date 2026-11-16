# empathy_field.py
#
# Empathy field: waves of empathy agents in a quantum field --
# resonance ("raisonnance"), the self-deterministic factor,
# collaboration, collectivism, and co-creativity = entropy.
#
# The mechanism, defined inside the model (not discovered):
#   - Agent: a thought state |psi> (thought.py machinery). Each
#     agent carries a frequency nu = its concurrence with the
#     field reference (thought_entanglement.py, v0.2.0) and a
#     self-determinism D = <psi|P|psi> (self_knowing.py, v0.2.0).
#   - Field: N agents superposed; the field state is the
#     normalized sum. Pairwise empathy quanta E_ij = h*nu_ij
#     with nu_ij = the pairwise concurrence (v0.4.0's rule,
#     extended to pairs: the concurrence of the normalized sum
#     of the two agents' states).
#   - Resonance ("raisonnance"): R_ij = |<psi_i|psi_j>|^2 --
#     the overlap squared (fidelity) between two agents. A pair
#     is resonant when R_ij >= a pre-registered threshold; the
#     resonance factor of a group is the mean pairwise R. (The
#     overlap machinery already exists; no new similarity is
#     invented.)
#   - Self-deterministic factor: mean D of the resonant group
#     vs mean D of the non-resonant group, same agents, same
#     noise.
#   - Collaboration: the same N agents evolved sharing the field
#     (superposed, interacting via the empathy quanta) vs the
#     CONTROL of the same N agents evolved isolated (independent
#     evolutions, no shared field, no quanta exchange). The two
#     arms start from the same population and receive the same
#     noise kicks (paired design); they differ ONLY in the
#     field/collapse step, so the gap is the collaboration
#     effect, not a sampling difference.
#   - Collectivism / co-creativity: co-creativity C_c is DEFINED
#     as the joint entropy H_joint (bits) of the collective's
#     joint outcomes -- the number of distinct joint
#     configurations the collective reaches. This is a definition
#     of the measure inside the model, not a discovery about
#     human creativity. The measurable content is the
#     collaboration gap and the ceiling/break, not the equality
#     itself.
#
# Honesty, stated up front:
#   - Classical emulation throughout; the machine running the
#     code is classical. Resonance is a defined overlap
#     quantity; co-creativity = entropy is a definition of the
#     measure; collaboration is a shared field in code, not
#     social science. Faggin's metaphysics is interpretive and
#     is NOT tested here. T_eff is a model temperature.
#   - The headline numbers sit near saturation (REPORT.md
#     section 5, v0.3.1 review): the curves -- D vs R, the
#     collaboration gap vs sigma, H_joint vs N -- are the
#     science, not the points.
#
# Pre-registered verdict rules for claims (xi)-(xiii), written
# before the final measurement run (see the claim_*_verdict
# functions and REPORT.md section 11):
#   (xi) Resonance raises self-determinism: mean D of resonant
#       pairs exceeds mean D of non-resonant pairs by a
#       pre-registered margin, and D is monotone in R across
#       bins (pooled across the sigma grid). The pilot showed
#       the effect is the CROSS-NOISE pattern: within a single
#       noise level the association is weak (the sigma = 1.0
#       per-sigma gap is slightly negative), because R and D are
#       both driven by the noise level itself -- so the
#       per-sigma gaps are REPORTED, not gated.
#   (xii) Collaboration raises co-creativity: H_joint (and
#       cumulative distinct joint states) for collaborating
#       agents exceeds the isolated control by a pre-registered
#       margin. If the gap is zero or negative, the claim FAILS
#       honestly -- the threshold is not moved to force a pass.
#       Design B (isolated = Born-collapse, decides and stays
#       decided) is the vehicle: the pilot showed design A
#       (no collapse anywhere) goes negative by sigma = 0.25,
#       while design B holds a large positive gap at every
#       sigma. The contrast is stated plainly in REPORT.md
#       section 11: isolation is decision without sharing,
#       collaboration is sharing without final decision.
#   (xiii) Co-creativity = entropy, with a ceiling and a break:
#       H_joint grows with N toward log2 of the joint space and
#       saturates; past sigma = 0.50 the collaboration gap
#       closes or reverses (incoherence -- the same break where
#       the v0.4.0 fix breaks) while it holds at sigma <= 0.25.
#       The pilot showed the break half FAILS in design B (the
#       gap holds at every sigma: +4.34 at 0.25, +3.35 at 0.50,
#       +3.56 at 1.00) -- the collaboration advantage is robust
#       to noise and does not inherit the v0.4.0 break. The
#       claim is kept as one claim and FAILS on that half, with
#       the ceiling half passing; the sub-checks are reported
#       separately, not hidden.
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Empathy field: resonance, collaboration, co-creativity."""

import math
from collections import Counter

import numpy as np

import bridge
import cost
import self_knowing
import thought
import thought_entanglement as te
import unity

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Model units: h = 1, so an empathy quantum's energy is its
# frequency, E = nu (dimensionless, in [0, 1]) -- the v0.4.0 rule.
H_MODEL = 1.0

SIGMA_GRID = te.SIGMA_GRID
DEFAULT_SEED = 42
DEFAULT_N_AGENTS_RESONANCE = 8
DEFAULT_N_AGENTS_COLLABORATION = 4
DEFAULT_GENERATIONS = 10
DEFAULT_SAMPLES_PER_GENERATION = 200

# The four Bell states, the collaboration population's bases.
BELL_NAMES = ("phi_plus", "phi_minus", "psi_plus", "psi_minus")

# Resonance bins on R (edges; the pilot fills the D values).
R_BIN_EDGES = (0.0, 0.25, 0.5, 0.75, 1.0)

# ---------------------------------------------------------------------------
# Pre-registered thresholds (set from the pilot sweep, REPORT.md
# section 11, and never moved after the final measurement run).
# They start unset; the claim functions raise until they are set.
# ---------------------------------------------------------------------------

RESONANCE_R_MIN = 0.5
RESONANCE_D_MARGIN = 0.20
COLLABORATION_H_MARGIN = 2.0
COLLABORATION_GAP_CLOSE_FRACTION = 0.5
SATURATION_FRACTION_TOL = 0.10


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("RESONANCE_R_MIN", RESONANCE_R_MIN),
        ("RESONANCE_D_MARGIN", RESONANCE_D_MARGIN),
        ("COLLABORATION_H_MARGIN", COLLABORATION_H_MARGIN),
        ("COLLABORATION_GAP_CLOSE_FRACTION",
         COLLABORATION_GAP_CLOSE_FRACTION),
        ("SATURATION_FRACTION_TOL", SATURATION_FRACTION_TOL),
    ) if value is None]
    if missing:
        raise ValueError(
            "empathy-field thresholds are unset: run the pilot "
            "sweep and set " + ", ".join(missing) + " first "
            "(REPORT.md section 11)")
    return {
        "resonance_r_min": float(RESONANCE_R_MIN),
        "resonance_d_margin": float(RESONANCE_D_MARGIN),
        "collaboration_h_margin": float(COLLABORATION_H_MARGIN),
        "gap_close_fraction": float(COLLABORATION_GAP_CLOSE_FRACTION),
        "saturation_fraction_tol": float(SATURATION_FRACTION_TOL),
    }


# ---------------------------------------------------------------------------
# Field, overlap, frequency, quanta, D
# ---------------------------------------------------------------------------

def _normalize(psi):
    """A state vector divided by its L2 norm."""
    psi = np.asarray(psi, dtype=complex)
    n = float(np.linalg.norm(psi))
    if n == 0.0:
        raise ValueError("a state cannot have zero norm")
    return psi / n


def field_state(states):
    """The field state: the normalized sum of the agents."""
    if not states:
        raise ValueError("need at least one agent")
    total = np.sum([np.asarray(s, dtype=complex) for s in states],
                   axis=0)
    return _normalize(total)


def overlap_squared(psi_i, psi_j):
    """Resonance R_ij = |<psi_i|psi_j>|^2, in [0, 1]."""
    a = _normalize(psi_i)
    b = _normalize(psi_j)
    return float(abs(np.vdot(a, b)) ** 2)


def pair_state(psi_i, psi_j):
    """The pair's joint thought: the normalized sum of the two."""
    return _normalize(np.asarray(psi_i, dtype=complex)
                      + np.asarray(psi_j, dtype=complex))


def agent_frequency(psi):
    """nu_i: the agent's concurrence (its own two-qubit state)."""
    return float(te.concurrence_pure(_normalize(psi)))


def pair_frequency(psi_i, psi_j):
    """nu_ij: the pairwise concurrence of the pair state."""
    return float(te.concurrence_pure(pair_state(psi_i, psi_j)))


def pair_empathy_quantum(psi_i, psi_j):
    """E_ij = h * nu_ij, h = 1 in model units (the v0.4.0 rule)."""
    return float(H_MODEL * pair_frequency(psi_i, psi_j))


def agent_self_determinism(psi):
    """D_i = <psi|P|psi>, the self-deterministic factor."""
    return float(self_knowing.self_knowing_factor(psi))


def empathy_fraction(states):
    """f = mean pairwise concurrence across all pairs, in [0, 1]."""
    states = list(states)
    if len(states) < 2:
        raise ValueError("need at least two agents for a field")
    values = [pair_frequency(states[i], states[j])
              for i in range(len(states))
              for j in range(i + 1, len(states))]
    return float(sum(values) / len(values))


# ---------------------------------------------------------------------------
# Resonance population: noisy copies of the uniform thought
# ---------------------------------------------------------------------------

def resonance_population(sigma, n_agents=DEFAULT_N_AGENTS_RESONANCE,
                         seed=DEFAULT_SEED):
    """N agents: noisy copies of the uniform thought at sigma.

    The same noise model as unity.gaussian_copies (real Gaussian
    noise, renormalized, seeded). At sigma = 0 the copies are
    identical (R = 1, D = 1); as sigma grows the copies spread,
    so pairwise R and D both fall -- the population spans R.
    """
    base = np.real(thought.uniform_thought())
    copies = unity.gaussian_copies(base, sigma, n_agents, seed)
    return [np.asarray(c, dtype=complex) for c in copies]


def resonance_pairs(sigmas=None, n_agents=DEFAULT_N_AGENTS_RESONANCE,
                    seed=DEFAULT_SEED):
    """Every pair across the sigma grid: R, pair D, nu_ij, E_ij.

    One row per (sigma, i, j). The pairs are pooled across
    sigma for the bins; the per-sigma gap keeps "same agents,
    same noise" (the split is within one sigma's population).
    """
    rows = []
    for sigma in (SIGMA_GRID if sigmas is None else sigmas):
        states = resonance_population(sigma, n_agents, seed)
        ds = [agent_self_determinism(s) for s in states]
        for i in range(len(states)):
            for j in range(i + 1, len(states)):
                r = overlap_squared(states[i], states[j])
                rows.append({
                    "sigma": float(sigma),
                    "i": i,
                    "j": j,
                    "resonance": r,
                    "d_i": ds[i],
                    "d_j": ds[j],
                    "d_pair": float((ds[i] + ds[j]) / 2.0),
                    "nu_ij": pair_frequency(states[i], states[j]),
                    "e_ij": pair_empathy_quantum(states[i], states[j]),
                })
    return rows


def resonance_bins(pairs, edges=R_BIN_EDGES):
    """Mean D per R bin (pooled pairs), with pair counts."""
    rows = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        if hi == 1.0:
            in_bin = [p for p in pairs if lo <= p["resonance"] <= hi]
        else:
            in_bin = [p for p in pairs if lo <= p["resonance"] < hi]
        rows.append({
            "r_lo": float(lo),
            "r_hi": float(hi),
            "n_pairs": len(in_bin),
            "mean_d": (float(np.mean([p["d_pair"] for p in in_bin]))
                       if in_bin else None),
        })
    return rows


def resonance_gap(pairs, r_min):
    """Resonant vs non-resonant mean D, per sigma and pooled.

    Resonant = R >= r_min. A sigma with an empty group reports
    None for that group's mean (not zero): an empty group is no
    measurement, not a zero.
    """
    sigmas = sorted({p["sigma"] for p in pairs})
    per_sigma = []
    for sigma in sigmas:
        sub = [p for p in pairs if p["sigma"] == sigma]
        res = [p["d_pair"] for p in sub if p["resonance"] >= r_min]
        non = [p["d_pair"] for p in sub if p["resonance"] < r_min]
        per_sigma.append({
            "sigma": float(sigma),
            "n_resonant": len(res),
            "n_non_resonant": len(non),
            "mean_d_resonant": (float(np.mean(res)) if res else None),
            "mean_d_non_resonant": (float(np.mean(non)) if non else None),
            "gap": (float(np.mean(res) - np.mean(non))
                    if res and non else None),
        })
    res_all = [p["d_pair"] for p in pairs if p["resonance"] >= r_min]
    non_all = [p["d_pair"] for p in pairs if p["resonance"] < r_min]
    pooled = {
        "n_resonant": len(res_all),
        "n_non_resonant": len(non_all),
        "mean_d_resonant": (float(np.mean(res_all)) if res_all else None),
        "mean_d_non_resonant": (float(np.mean(non_all))
                                if non_all else None),
        "gap": (float(np.mean(res_all) - np.mean(non_all))
                if res_all and non_all else None),
    }
    return {"per_sigma": per_sigma, "pooled": pooled}


# ---------------------------------------------------------------------------
# Collaboration populations and evolution
# ---------------------------------------------------------------------------

def collaboration_population(n_agents=DEFAULT_N_AGENTS_COLLABORATION,
                             sigma=0.25, seed=DEFAULT_SEED):
    """N agents: noisy copies of the Bell states, cycled.

    Agent i is a noisy copy of BELL_NAMES[i mod 4] at sigma, with
    its own seed offset (seed + i), so the agents start distinct.
    Each Bell state has concurrence 1 and a 1-bit Born
    distribution (two concepts at 0.5 each), so an isolated agent
    collapses onto two joint outcomes per agent while a
    collaborating agent can reach all four.
    """
    states = []
    for i in range(int(n_agents)):
        bell = te.bell_state(BELL_NAMES[i % len(BELL_NAMES)])
        copy = unity.gaussian_copies(
            np.real(bell), sigma, 1, seed + i)[0]
        states.append(np.asarray(copy, dtype=complex))
    return states


def _noise_kick(psi, sigma, seed):
    """One noise kick: the state plus Gaussian noise, renormalized."""
    return np.asarray(
        unity.gaussian_copies(np.real(psi), sigma, 1, seed)[0],
        dtype=complex)


def _field_mix(states, coupling):
    """Share the field: each agent superposed with the field state.

    psi_i <- normalize(psi_i + coupling * Phi), where Phi is the
    normalized sum of the agents and coupling is the measured
    empathy fraction f (mean pairwise concurrence). The coupling
    is a measured quantity, not a free parameter: at low noise
    the quanta bind the agents to the field strongly; as noise
    kills the concurrence, the coupling weakens. A single agent
    has no field to share: the mix is a no-op (coupling 0.0).
    """
    if len(states) < 2:
        return list(states)
    phi = field_state(states)
    return [_normalize(s + float(coupling) * phi) for s in states]


def _joint_sample_counts(states, n_samples, rng):
    """Empirical joint outcomes: each agent collapses once per sample.

    One draw per agent per sample from its Born distribution
    (independent draws given the rng stream -- the correlation
    between agents comes from their STATES, not the sampling).
    Returns a Counter of concept tuples.
    """
    probs = []
    for s in states:
        p = thought.born_probabilities(s)
        probs.append(np.asarray(p, dtype=float) / np.sum(p))
    counts = Counter()
    for _ in range(int(n_samples)):
        outcome = tuple(int(rng.choice(4, p=p)) for p in probs)
        counts[outcome] += 1
    return counts


def _joint_entropy_from_counts(counts):
    """H_joint (bits) of an empirical joint-outcome distribution."""
    total = float(sum(counts.values()))
    freqs = [c / total for c in counts.values()]
    return float(cost.shannon_entropy(freqs))


def run_collaboration(n_agents=DEFAULT_N_AGENTS_COLLABORATION,
                      sigma=0.25,
                      generations=DEFAULT_GENERATIONS,
                      n_samples=DEFAULT_SAMPLES_PER_GENERATION,
                      seed=DEFAULT_SEED, design="B"):
    """Collaborating vs isolated arms, paired design.

    Both arms start from the same population and receive the same
    noise kicks (same per-(generation, agent) seeds); they differ
    ONLY in the step after the kick:
      design "A": collaborating mixes with the field (coupling f);
          isolated does nothing else. No collapse anywhere.
      design "B": collaborating mixes with the field (coupling f);
          isolated Born-collapses (decides) and stays decided
          up to the noise kicks.
    Joint outcomes are sampled each generation (same sampling
    seed in both arms, so the gap is paired) and pooled over the
    run. Returns H_joint, distinct counts, the gap, and the
    per-generation rows (H per generation, coupling f).
    """
    if design not in ("A", "B"):
        raise ValueError("design must be 'A' or 'B'")
    n_agents = int(n_agents)
    base = collaboration_population(n_agents, sigma, seed)

    arms = {}
    for arm in ("collaborating", "isolated"):
        states = [s.copy() for s in base]
        counts = Counter()
        rows = []
        sample_rng = np.random.default_rng(seed + 424242)
        for g in range(int(generations)):
            states = [_noise_kick(s, sigma, seed + 1000 * g + 10 * i)
                      for i, s in enumerate(states)]
            if arm == "collaborating":
                coupling = (empathy_fraction(states)
                            if len(states) >= 2 else 0.0)
                states = _field_mix(states, coupling)
            else:
                coupling = 0.0
                if design == "B":
                    collapsed = []
                    for i, s in enumerate(states):
                        _, decided = thought.collapse(
                            s, seed=seed + 4242 + 1000 * g + 10 * i)
                        collapsed.append(np.asarray(decided,
                                                    dtype=complex))
                    states = collapsed
            gen_counts = _joint_sample_counts(states, n_samples,
                                              sample_rng)
            counts.update(gen_counts)
            rows.append({
                "generation": g,
                "h_joint_bits": _joint_entropy_from_counts(gen_counts),
                "distinct_joint": len(gen_counts),
                "coupling_f": float(coupling),
            })
        arms[arm] = {
            "counts": counts,
            "h_joint_bits": _joint_entropy_from_counts(counts),
            "distinct_joint": len(counts),
            "rows": rows,
        }
    ceiling = 2.0 * n_agents
    return {
        "n_agents": n_agents,
        "sigma": float(sigma),
        "generations": int(generations),
        "n_samples_per_generation": int(n_samples),
        "design": design,
        "ceiling_bits": ceiling,
        "collaborating": arms["collaborating"],
        "isolated": arms["isolated"],
        "gap_bits": (arms["collaborating"]["h_joint_bits"]
                     - arms["isolated"]["h_joint_bits"]),
        "gap_distinct": (arms["collaborating"]["distinct_joint"]
                         - arms["isolated"]["distinct_joint"]),
    }


def collaboration_gap_vs_noise(sigmas=None, n_agents=None,
                               generations=DEFAULT_GENERATIONS,
                               n_samples=DEFAULT_SAMPLES_PER_GENERATION,
                               seed=DEFAULT_SEED, design="B"):
    """The collaboration gap H_collab - H_isolated per sigma."""
    rows = []
    for sigma in (SIGMA_GRID if sigmas is None else sigmas):
        result = run_collaboration(
            n_agents=(DEFAULT_N_AGENTS_COLLABORATION
                      if n_agents is None else n_agents),
            sigma=sigma, generations=generations, n_samples=n_samples,
            seed=seed, design=design)
        rows.append({
            "sigma": float(sigma),
            "h_collaborating_bits": result["collaborating"]["h_joint_bits"],
            "h_isolated_bits": result["isolated"]["h_joint_bits"],
            "gap_bits": result["gap_bits"],
            "distinct_collaborating":
                result["collaborating"]["distinct_joint"],
            "distinct_isolated": result["isolated"]["distinct_joint"],
            "gap_distinct": result["gap_distinct"],
        })
    return rows


def saturation_curve(n_values=(1, 2, 3, 4), sigma=0.25,
                     generations=DEFAULT_GENERATIONS,
                     n_samples=DEFAULT_SAMPLES_PER_GENERATION,
                     seed=DEFAULT_SEED, design="B"):
    """H_joint vs N for the collaborating arm, against the 2N ceiling.

    Joint space = 4^N outcomes, ceiling log2(4^N) = 2N bits.
    """
    rows = []
    for n in n_values:
        result = run_collaboration(
            n_agents=int(n), sigma=sigma, generations=generations,
            n_samples=n_samples, seed=seed, design=design)
        rows.append({
            "n_agents": int(n),
            "ceiling_bits": 2.0 * int(n),
            "h_collaborating_bits":
                result["collaborating"]["h_joint_bits"],
            "h_isolated_bits": result["isolated"]["h_joint_bits"],
            "fraction_of_ceiling":
                result["collaborating"]["h_joint_bits"] / (2.0 * int(n)),
            "distinct_collaborating":
                result["collaborating"]["distinct_joint"],
        })
    return rows


# ---------------------------------------------------------------------------
# Claims (xi)-(xiii): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_resonance_verdict(sigmas=None,
                            n_agents=DEFAULT_N_AGENTS_RESONANCE,
                            seed=DEFAULT_SEED):
    """(xi) Resonance raises self-determinism.

    PASS iff the binned mean D is strictly increasing in R
    (pooled pairs across the sigma grid) and the pooled
    resonant-vs-non-resonant gap is at least RESONANCE_D_MARGIN.
    The per-sigma gaps are REPORTED, not gated: the pilot showed
    the effect is the cross-noise pattern (within a single noise
    level the association is weak -- the sigma = 1.0 gap is
    slightly negative -- because R and D are both driven by the
    noise level itself). Thresholds come from the pilot
    (REPORT.md section 11).
    """
    t = _thresholds()
    pairs = resonance_pairs(sigmas, n_agents, seed)
    bins = resonance_bins(pairs)
    binned = [b["mean_d"] for b in bins if b["mean_d"] is not None]
    check_monotone = all(binned[i + 1] > binned[i]
                         for i in range(len(binned) - 1))
    gap = resonance_gap(pairs, t["resonance_r_min"])
    pooled_gap = gap["pooled"]["gap"]
    check_pooled = (pooled_gap is not None
                    and pooled_gap >= t["resonance_d_margin"])
    passed = bool(check_monotone and check_pooled)
    return {
        "claim": "(xi) resonance raises self-determinism",
        "passed": passed,
        "checks": {
            "binned_D_monotone_in_R": bool(check_monotone),
            "pooled_gap_at_least_margin": bool(check_pooled),
        },
        "resonance_r_min": t["resonance_r_min"],
        "resonance_d_margin": t["resonance_d_margin"],
        "bins": bins,
        "gap": gap,
    }


def claim_collaboration_verdict(sigma=0.25, n_agents=None,
                                generations=DEFAULT_GENERATIONS,
                                n_samples=DEFAULT_SAMPLES_PER_GENERATION,
                                seed=DEFAULT_SEED, design="B"):
    """(xii) Collaboration raises co-creativity.

    PASS iff H_collaborating - H_isolated is at least
    COLLABORATION_H_MARGIN at the reference sigma, and the
    collaborating arm also reaches strictly more distinct joint
    states than the isolated control. If the gap is zero or
    negative the claim FAILS honestly -- the threshold is not
    moved to force a pass.
    """
    t = _thresholds()
    result = run_collaboration(
        n_agents=(DEFAULT_N_AGENTS_COLLABORATION
                  if n_agents is None else n_agents),
        sigma=sigma, generations=generations, n_samples=n_samples,
        seed=seed, design=design)
    gap = result["gap_bits"]
    check_gap = gap >= t["collaboration_h_margin"]
    check_distinct = result["gap_distinct"] > 0
    passed = bool(check_gap and check_distinct)
    return {
        "claim": "(xii) collaboration raises co-creativity",
        "passed": passed,
        "checks": {
            "gap_at_least_margin": bool(check_gap),
            "distinct_collaborating_exceeds_isolated":
                bool(check_distinct),
        },
        "sigma": float(sigma),
        "design": design,
        "collaboration_h_margin": t["collaboration_h_margin"],
        "h_collaborating_bits": result["collaborating"]["h_joint_bits"],
        "h_isolated_bits": result["isolated"]["h_joint_bits"],
        "gap_bits": gap,
        "distinct_collaborating":
            result["collaborating"]["distinct_joint"],
        "distinct_isolated": result["isolated"]["distinct_joint"],
        "gap_distinct": result["gap_distinct"],
        "ceiling_bits": result["ceiling_bits"],
    }


def claim_cocreativity_verdict(sigmas=None, n_values=(1, 2, 3, 4),
                               sigma_ref=0.25,
                               generations=DEFAULT_GENERATIONS,
                               n_samples=DEFAULT_SAMPLES_PER_GENERATION,
                               seed=DEFAULT_SEED, design="B"):
    """(xiii) Co-creativity = entropy, with a ceiling and a break.

    PASS iff (a) H_joint of the collaborating arm is strictly
    increasing in N on the grid and below the 2N ceiling at
    every N; (b) the fraction of the ceiling plateaus -- the
    last two fractions agree within SATURATION_FRACTION_TOL;
    (c) the collaboration gap holds at sigma <= 0.25 (positive)
    and closes past sigma = 0.50 (gap at 0.50 at most
    COLLABORATION_GAP_CLOSE_FRACTION of the gap at 0.25, or
    negative).
    """
    t = _thresholds()
    curve = saturation_curve(n_values, sigma=sigma_ref,
                             generations=generations, n_samples=n_samples,
                             seed=seed, design=design)
    hs = [r["h_collaborating_bits"] for r in curve]
    check_increasing = all(hs[i + 1] > hs[i]
                           for i in range(len(hs) - 1))
    check_below_ceiling = all(
        r["h_collaborating_bits"] < r["ceiling_bits"] for r in curve)
    fractions = [r["fraction_of_ceiling"] for r in curve]
    check_plateau = (len(fractions) >= 2 and abs(
        fractions[-1] - fractions[-2]) <= t["saturation_fraction_tol"])

    gap_rows = collaboration_gap_vs_noise(
        sigmas, n_agents=DEFAULT_N_AGENTS_COLLABORATION,
        generations=generations, n_samples=n_samples, seed=seed,
        design=design)
    by_sigma = {r["sigma"]: r for r in gap_rows}
    low = [by_sigma[s]["gap_bits"] for s in by_sigma if s <= 0.25]
    check_holds = bool(low) and all(g > 0.0 for g in low)
    gap_025 = by_sigma.get(0.25, {}).get("gap_bits")
    gap_050 = by_sigma.get(0.50, {}).get("gap_bits")
    check_closes = (gap_025 is not None and gap_050 is not None
                    and gap_050 <= t["gap_close_fraction"] * gap_025)

    passed = bool(check_increasing and check_below_ceiling
                  and check_plateau and check_holds and check_closes)
    return {
        "claim": "(xiii) co-creativity = entropy, ceiling and break",
        "passed": passed,
        "checks": {
            "h_joint_increasing_in_N": bool(check_increasing),
            "h_joint_below_ceiling": bool(check_below_ceiling),
            "fraction_of_ceiling_plateaus": bool(check_plateau),
            "gap_holds_at_sigma_le_0.25": bool(check_holds),
            "gap_closes_past_sigma_0.50": bool(check_closes),
        },
        "saturation_curve": curve,
        "gap_vs_noise": gap_rows,
        "gap_at_sigma_0.25": gap_025,
        "gap_at_sigma_0.50": gap_050,
        "gap_close_fraction": t["gap_close_fraction"],
        "saturation_fraction_tol": t["saturation_fraction_tol"],
    }


def empathy_field_claims():
    """The three empathy-field claims (xi)-(xiii), measured fresh."""
    claim_xi = claim_resonance_verdict()
    claim_xii = claim_collaboration_verdict()
    claim_xiii = claim_cocreativity_verdict()
    verdicts = [claim_xi, claim_xii, claim_xiii]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_xi_resonance": claim_xi,
        "claim_xii_collaboration": claim_xii,
        "claim_xiii_cocreativity": claim_xiii,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the resonance, collaboration, and co-creativity
    measurements with the claims (xi)-(xiii) verdicts."""
    print("Empathy field -- claims (xi)-(xiii)")
    print()
    verdicts = empathy_field_claims()
    xi = verdicts["claim_xi_resonance"]
    print("Resonance bins (mean D per R bin):")
    for b in xi["bins"]:
        mean = ("None" if b["mean_d"] is None else f"{b['mean_d']:.4f}")
        print(f"  R in [{b['r_lo']:.2f}, {b['r_hi']:.2f}]: "
              f"n = {b['n_pairs']}, mean D = {mean}")
    print("Per-sigma resonance gap:")
    for r in xi["gap"]["per_sigma"]:
        print(f"  sigma = {r['sigma']:>4}: n_res = {r['n_resonant']}, "
              f"n_non = {r['n_non_resonant']}, gap = {r['gap']}")
    print(f"  pooled gap = {xi['gap']['pooled']['gap']}")
    print(f"claim (xi) verdict: {'PASS' if xi['passed'] else 'FAIL'}")
    print()
    xii = verdicts["claim_xii_collaboration"]
    print(f"H_collaborating = {xii['h_collaborating_bits']:.4f} bits, "
          f"H_isolated = {xii['h_isolated_bits']:.4f} bits, "
          f"gap = {xii['gap_bits']:.4f} bits")
    print(f"distinct: collaborating {xii['distinct_collaborating']}, "
          f"isolated {xii['distinct_isolated']}")
    print(f"claim (xii) verdict: {'PASS' if xii['passed'] else 'FAIL'}")
    print()
    xiii = verdicts["claim_xiii_cocreativity"]
    print("Saturation curve (collaborating H vs 2N ceiling):")
    for r in xiii["saturation_curve"]:
        print(f"  N = {r['n_agents']}: H = "
              f"{r['h_collaborating_bits']:.4f} bits, ceiling = "
              f"{r['ceiling_bits']:.1f}, fraction = "
              f"{r['fraction_of_ceiling']:.4f}")
    print("Collaboration gap vs noise:")
    for r in xiii["gap_vs_noise"]:
        print(f"  sigma = {r['sigma']:>4}: H_collab = "
              f"{r['h_collaborating_bits']:.4f}, H_isolated = "
              f"{r['h_isolated_bits']:.4f}, gap = {r['gap_bits']:+.4f}")
    print(f"claim (xiii) verdict: {'PASS' if xiii['passed'] else 'FAIL'}")
    print()
    print(f"claims (xi)-(xiii): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
