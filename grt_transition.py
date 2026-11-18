# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# grt_transition.py
#
# GRT phase-transition test (v0.18.0, deep-think upgrade
# #11, report.md section 9 rank 11 and section 2):
# General Resonance Theory (Hunt & Schooler, Frontiers
# in Human Neuroscience 13:378, 2019; GRT 2.0, TSC 2026
# abstract — speculative). Conjecture 1: shared
# resonance combines micro- into macro-conscious
# entities via a phase transition in the speed /
# bandwidth of information flow at a critical coupling
# K_c. Conjecture 3: nested entities persist within
# larger ones ("many become one").
#
# The construction (fixed before the pilot; see
# docs/preregistration-v0.18.0.md):
#   - Base field: the v0.5.0 resonance population (8
#     agents, noisy copies of the uniform thought) at
#     sigma = 1.00, the far-broken regime — the field
#     must start fragmented for a transition to be
#     possible, and at sigma = 0.25 it is already one
#     macro-entity at K = 0 (mean R 0.85 / 0.68).
#   - Coupling K on the grid 0.0, 0.1, ..., 1.0:
#     shared resonance as mixing toward the common
#     reference, psi_i(K) = normalize((1 - K) psi_i
#     + K psi_ref), psi_ref = the uniform thought.
#     K = 0 is the uncoupled field; K = 1 is every
#     agent identical to the reference.
#   - Bandwidth B(K): the pairwise shared information,
#     the mean over all 28 pairs of H(p_i) + H(p_j)
#     - H(p_ij), where p_i is agent i's Born
#     distribution and p_ij is the Born distribution
#     of the pair state (the normalized sum of the
#     two agents). B is a DEFINED bandwidth proxy
#     inside the model, not a literal mutual
#     information between two random variables.
#     At K = 1, B = 2.0000 bits exactly.
#   - Predicted critical coupling K_c: the FIRST grid
#     K at which the mean pairwise resonance mean R(K)
#     reaches the bridge's pre-existing resonance
#     threshold 0.5 (RESONANCE_R_MIN, v0.5.0). GRT
#     supplies no number; the 0.5 threshold is the
#     project's own, and K_c is read off it before
#     the bandwidth curve is examined.
#   - Nested structure: connected components of the
#     resonance graph at R >= 0.5 (macro level) and
#     at R >= 0.75 (nested level).
#
# Honesty, stated up front:
#   - This is a SYNTHETIC classical emulation. Nothing
#     here tests consciousness, resonance in a brain,
#     or GRT in a human. GRT is speculative; its core
#     conjecture has never been directly tested, and
#     the report ranks this upgrade last because GRT
#     gives no quantitative K_c — the project supplies
#     it, making the test partly self-fulfilling. No
#     scalar Phi is computed or used anywhere
#     (standing do-not list); E = h*nu is not used in
#     this module at all.
#   - The report's directional prediction already
#     FAILS on the calibration seeds: the largest
#     bandwidth step does not sit at K_c on either
#     seed (K = 0.7 vs K_c = 0.3 / 0.6), and on seed 7
#     the step at K_c is negative (-0.0572). Claim
#     (lviii) gates the report's prediction as stated
#     and is expected to FAIL; claim (lix) gates the
#     shape that IS measured (macro forms just above
#     K_c, nesting persists at K_c, bandwidth rises
#     overall).
#   - One rejected wiring is disclosed, not hidden:
#     coupling by mixing with the field state (the
#     v0.5.0 _field_mix) was tried first and rejected
#     — at sigma = 1.00 seed 7 the mean R FELL with K
#     at first (0.278 -> 0.232) and B was U-shaped,
#     because mixing toward a noisy field average can
#     move agents apart. The reference-mixing wiring
#     above replaces it.
#   - Mean R is NOT monotone in K on seed 7 even in
#     the kept wiring (0.2778 -> 0.2376 at K = 0.3
#     before rising). Monotonicity is REPORTED, not
#     gated. At K = 1 all sub-structure has dissolved
#     (one component at R >= 0.75 on both calibration
#     seeds), so nesting does not survive to full
#     coupling — that limit is reported, not gated.
#
# Pre-registered verdict rules for claims (lvii)-(lix),
# written before the evaluation run (see
# docs/preregistration-v0.18.0.md and the
# claim_*_verdict functions):
#   (lvii) Machinery exact, K_c interior, field starts
#       fragmented: on every seed, K = 0 states equal
#       the base to 1e-12, K = 1 states equal the
#       uniform reference to 1e-12, mean R(1) = 1 to
#       1e-12, B(1) = 2.0000 to 1e-12, 0 < K_c < 1.0,
#       and the largest component at R >= 0.5 at K = 0
#       is <= 7. (Calibration pilot: K_c = 0.3 / 0.6;
#       largest component at K = 0 is 7 / 6.)
#   (lviii) The GRT phase transition as stated: on
#       every seed, the bandwidth step ending at K_c
#       is >= 0.10 bits AND is the largest step on
#       the grid. (Calibration pilot: step at K_c =
#       0.1142 / -0.0572; max step 0.1501 / 0.2597 at
#       K = 0.7 — expected FAIL.)
#   (lix) The measured shape: on every seed, at
#       K = K_c + 0.2 the largest component at
#       R >= 0.5 is 8; at K = K_c the components at
#       R >= 0.75 number >= 2; and B(1) - B(0) >=
#       0.50 bits. (Calibration pilot: 8 / 8; 2 / 4
#       components; 0.8532 / 0.8774 bits.)

"""GRT phase-transition test, claims (lvii)-(lix)."""

import numpy as np

import bridge
import cost
import empathy_field as ef
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
# Pre-registered thresholds (frozen from the calibration pilot,
# docs/preregistration-v0.18.0.md; never moved after the run).
# ---------------------------------------------------------------------------

# The base field is the v0.5.0 resonance population at
# sigma = 1.00 (the far-broken regime): fragmented at
# K = 0, so a transition is possible at all. The
# attuned population (sigma = 0.25) is already one
# macro-entity at K = 0 and cannot transition.
SIGMA_BASE = 1.00
N_AGENTS = 8

# The coupling grid: shared-resonance mixing weight.
K_GRID = tuple(round(0.1 * k, 1) for k in range(11))
K_STEP = 0.1

# The resonance threshold that defines K_c: the
# bridge's pre-existing RESONANCE_R_MIN (v0.5.0).
# K_c is the first grid K with mean R(K) >= this.
RESONANCE_THRESHOLD = 0.5
# The nested level: components at this threshold must
# survive inside the forming macro (claim (lix)(b)).
NESTED_THRESHOLD = 0.75

# Exactness tolerance for the endpoint identities.
EXACT_TOL = 1e-12

# Claim (lvii)(c): the K = 0 field must start
# fragmented — its largest component at R >= 0.5 is
# at most this (8 would mean already one macro).
LARGEST_COMPONENT_START_MAX = 7

# Claim (lviii): the bandwidth step ending at K_c
# must be at least this (bits) and the largest step
# on the grid.
JUMP_MIN_BITS = 0.10

# Claim (lix): the macro must be complete (all agents)
# at K_c + 0.2; at least this many nested components
# must survive at K_c; the total bandwidth rise must
# be at least this (bits).
MACRO_SIZE = 8
NESTED_COMPONENTS_MIN = 2
TOTAL_RISE_MIN_BITS = 0.50


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("SIGMA_BASE", SIGMA_BASE),
        ("N_AGENTS", N_AGENTS),
        ("K_GRID", K_GRID),
        ("RESONANCE_THRESHOLD", RESONANCE_THRESHOLD),
        ("NESTED_THRESHOLD", NESTED_THRESHOLD),
        ("EXACT_TOL", EXACT_TOL),
        ("LARGEST_COMPONENT_START_MAX", LARGEST_COMPONENT_START_MAX),
        ("JUMP_MIN_BITS", JUMP_MIN_BITS),
        ("MACRO_SIZE", MACRO_SIZE),
        ("NESTED_COMPONENTS_MIN", NESTED_COMPONENTS_MIN),
        ("TOTAL_RISE_MIN_BITS", TOTAL_RISE_MIN_BITS),
    ) if value is None]
    if missing:
        raise ValueError(
            "grt-transition thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.18.0.md)")
    return {
        "sigma_base": float(SIGMA_BASE),
        "n_agents": int(N_AGENTS),
        "k_grid": tuple(float(k) for k in K_GRID),
        "resonance_threshold": float(RESONANCE_THRESHOLD),
        "nested_threshold": float(NESTED_THRESHOLD),
        "exact_tol": float(EXACT_TOL),
        "largest_component_start_max": int(LARGEST_COMPONENT_START_MAX),
        "jump_min_bits": float(JUMP_MIN_BITS),
        "macro_size": int(MACRO_SIZE),
        "nested_components_min": int(NESTED_COMPONENTS_MIN),
        "total_rise_min_bits": float(TOTAL_RISE_MIN_BITS),
    }


# ---------------------------------------------------------------------------
# Coupling, resonance, bandwidth, components
# ---------------------------------------------------------------------------

def _normalize(psi):
    """A state vector divided by its L2 norm."""
    psi = np.asarray(psi, dtype=complex)
    n = float(np.linalg.norm(psi))
    if n == 0.0:
        raise ValueError("a state cannot have zero norm")
    return psi / n


def reference_state():
    """psi_ref: the uniform thought all agents derive from."""
    return np.asarray(thought.uniform_thought(), dtype=complex)


def couple(states, k):
    """Shared resonance: psi_i(K) = normalize((1 - K) psi_i
    + K psi_ref). K = 0 is the uncoupled field; K = 1 is
    every agent identical to the reference."""
    ref = reference_state()
    k = float(k)
    if not 0.0 <= k <= 1.0:
        raise ValueError("coupling K must lie in [0, 1]")
    return [_normalize((1.0 - k) * np.asarray(s, dtype=complex)
                       + k * ref) for s in states]


def mean_resonance(states):
    """Mean pairwise resonance R = |<psi_i|psi_j>|^2."""
    states = list(states)
    if len(states) < 2:
        raise ValueError("need at least two agents for a field")
    values = [ef.overlap_squared(states[i], states[j])
              for i in range(len(states))
              for j in range(i + 1, len(states))]
    return float(np.mean(values))


def pair_shared_information(states):
    """B: the pairwise shared information (bits), the mean
    over all pairs of H(p_i) + H(p_j) - H(p_ij), where
    p_ij is the Born distribution of the pair state (the
    normalized sum of the two agents). A DEFINED bandwidth
    proxy inside the model, not a literal mutual
    information between two random variables."""
    states = list(states)
    if len(states) < 2:
        raise ValueError("need at least two agents for a field")
    values = []
    for i in range(len(states)):
        for j in range(i + 1, len(states)):
            p_i = thought.born_probabilities(states[i])
            p_j = thought.born_probabilities(states[j])
            p_ij = thought.born_probabilities(
                ef.pair_state(states[i], states[j]))
            values.append(cost.shannon_entropy(p_i)
                          + cost.shannon_entropy(p_j)
                          - cost.shannon_entropy(p_ij))
    return float(np.mean(values))


def resonance_components(states, threshold):
    """Connected-component sizes (descending) of the
    resonance graph at R >= threshold: two agents are
    linked when their pairwise resonance reaches the
    threshold."""
    states = list(states)
    n = len(states)
    adj = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if ef.overlap_squared(states[i], states[j]) >= threshold:
                adj[i].add(j)
                adj[j].add(i)
    seen = set()
    sizes = []
    for i in range(n):
        if i in seen:
            continue
        stack, comp = [i], set()
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u)
            stack.extend(adj[u] - comp)
        seen |= comp
        sizes.append(len(comp))
    return sorted(sizes, reverse=True)


def critical_coupling(rows):
    """K_c: the first grid K with mean R(K) >= the resonance
    threshold (0.5). None when the threshold is never
    reached (impossible on this grid in practice, since
    mean R(1) = 1)."""
    for row in rows:
        if row["mean_r"] >= RESONANCE_THRESHOLD:
            return float(row["k"])
    return None


def coupling_row(k, base_states):
    """One K row: the coupled states' mean R, bandwidth B,
    and component sizes at the macro and nested levels."""
    states = couple(base_states, k)
    return {
        "k": float(k),
        "mean_r": mean_resonance(states),
        "bandwidth_bits": pair_shared_information(states),
        "components_macro": resonance_components(
            states, RESONANCE_THRESHOLD),
        "components_nested": resonance_components(
            states, NESTED_THRESHOLD),
    }


def coupling_scan(seed, sigma=SIGMA_BASE, n_agents=N_AGENTS,
                  k_grid=None):
    """The full K sweep on one seed's base field, with K_c,
    the bandwidth steps, and the largest step."""
    base = ef.resonance_population(sigma, n_agents, seed)
    rows = [coupling_row(k, base)
            for k in (K_GRID if k_grid is None else k_grid)]
    k_c = critical_coupling(rows)
    steps = [rows[i + 1]["bandwidth_bits"] - rows[i]["bandwidth_bits"]
             for i in range(len(rows) - 1)]
    max_step = max(steps)
    max_step_k = rows[1 + int(np.argmax(np.array(steps)))]["k"]
    step_at_kc = None
    if k_c is not None and k_c > 0.0:
        idx = [r["k"] for r in rows].index(k_c)
        step_at_kc = steps[idx - 1]
    return {
        "seed": int(seed),
        "sigma": float(sigma),
        "k_c": k_c,
        "rows": rows,
        "bandwidth_steps": [float(s) for s in steps],
        "max_step_bits": float(max_step),
        "max_step_k": float(max_step_k),
        "step_at_kc_bits": (None if step_at_kc is None
                            else float(step_at_kc)),
        "bandwidth_total_rise_bits": float(
            rows[-1]["bandwidth_bits"] - rows[0]["bandwidth_bits"]),
        "mean_r_monotone": bool(all(
            rows[i + 1]["mean_r"] >= rows[i]["mean_r"] - 1e-12
            for i in range(len(rows) - 1))),
        "endpoint_k0_max_deviation": float(max(
            np.max(np.abs(np.asarray(s, dtype=complex)
                          - np.asarray(b, dtype=complex)))
            for s, b in zip(couple(base, 0.0), base))),
        "endpoint_k1_max_deviation": float(max(
            np.max(np.abs(np.asarray(s, dtype=complex)
                          - reference_state()))
            for s in couple(base, 1.0))),
    }


# ---------------------------------------------------------------------------
# Claim verdicts (lvii)-(lix)
# ---------------------------------------------------------------------------

def claim_machinery_verdict(seeds=None):
    """(lvii) Machinery is exact, K_c is interior, and the
    field starts fragmented.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
    (a) the coupling endpoints are exact — the K = 0
    states equal the base population to 1e-12, the K = 1
    states equal the uniform reference to 1e-12, mean
    R(1) = 1 to 1e-12, and B(1) = 2.0000 to 1e-12;
    (b) K_c is interior: 0 < K_c < 1.0;
    (c) the field starts fragmented: the largest
    component at R >= 0.5 at K = 0 is <= 7.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        scan = coupling_scan(seed)
        row0 = scan["rows"][0]
        row1 = scan["rows"][-1]
        per_seed.append({
            "seed": int(seed),
            "k_c": scan["k_c"],
            "endpoint_k0_max_deviation":
                scan["endpoint_k0_max_deviation"],
            "endpoint_k1_max_deviation":
                scan["endpoint_k1_max_deviation"],
            "mean_r_at_k1": float(row1["mean_r"]),
            "bandwidth_at_k1": float(row1["bandwidth_bits"]),
            "mean_r_at_k0": float(row0["mean_r"]),
            "largest_component_at_k0": int(
                row0["components_macro"][0]),
            "components_macro_at_k0": row0["components_macro"],
            "scan": scan,
        })
    checks = {
        "endpoint_k0_exact": all(
            r["endpoint_k0_max_deviation"] < t["exact_tol"]
            for r in per_seed),
        "endpoint_k1_exact": all(
            r["endpoint_k1_max_deviation"] < t["exact_tol"]
            for r in per_seed),
        "mean_r_at_k1_is_one": all(
            abs(r["mean_r_at_k1"] - 1.0) < t["exact_tol"]
            for r in per_seed),
        "bandwidth_at_k1_is_two": all(
            abs(r["bandwidth_at_k1"] - 2.0) < t["exact_tol"]
            for r in per_seed),
        "k_c_interior": all(
            r["k_c"] is not None and 0.0 < r["k_c"] < 1.0
            for r in per_seed),
        "field_fragmented_at_k0": all(
            r["largest_component_at_k0"]
            <= t["largest_component_start_max"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(lvii) machinery is exact, K_c is interior, "
                 "and the field starts fragmented",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_transition_verdict(seeds=None):
    """(lviii) The GRT phase transition as stated: a sharp
    jump in bandwidth at K_c.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
    (a) the bandwidth step ending at K_c is >= 0.10 bits;
    (b) that step is the largest step on the K grid.
    If K_c = 0 there is no step ending at K_c and the
    claim fails on that seed. Calibration pilot: step
    at K_c = 0.1142 / -0.0572; max step 0.1501 / 0.2597
    at K = 0.7 — the prediction fails on both
    calibration seeds, so this claim is expected to
    FAIL. The failure is the result.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        scan = coupling_scan(seed)
        per_seed.append({
            "seed": int(seed),
            "k_c": scan["k_c"],
            "step_at_kc_bits": scan["step_at_kc_bits"],
            "max_step_bits": scan["max_step_bits"],
            "max_step_k": scan["max_step_k"],
            "bandwidth_steps": scan["bandwidth_steps"],
            "scan": scan,
        })
    checks = {
        "step_at_kc_large_enough": all(
            r["step_at_kc_bits"] is not None
            and r["step_at_kc_bits"] >= t["jump_min_bits"]
            for r in per_seed),
        "step_at_kc_is_largest": all(
            r["step_at_kc_bits"] is not None
            and abs(r["step_at_kc_bits"] - r["max_step_bits"])
            < 1e-12
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(lviii) the GRT phase transition as stated: "
                 "a sharp jump in bandwidth at K_c",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_shape_verdict(seeds=None):
    """(lix) The measured shape: the macro forms just above
    K_c, nesting persists at K_c, bandwidth rises overall.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
    (a) at K = K_c + 0.2 the largest component at
    R >= 0.5 is 8 (the macro is complete just above
    the transition);
    (b) at K = K_c the components at R >= 0.75 number
    >= 2 (sub-structure survives inside the forming
    macro — Conjecture 3);
    (c) bandwidth rises overall: B(1) - B(0) >= 0.50 bits.
    (a) and (b) are evaluated at different K on purpose:
    (b) is the structure AT the transition, where
    sub-entities are still visible; (a) is the completed
    macro JUST ABOVE it.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        scan = coupling_scan(seed)
        k_c = scan["k_c"]
        by_k = {r["k"]: r for r in scan["rows"]}
        row_kc = by_k.get(k_c) if k_c is not None else None
        k_above = (None if k_c is None else
                   round(k_c + 2 * K_STEP, 1))
        row_above = by_k.get(k_above) if k_above is not None else None
        per_seed.append({
            "seed": int(seed),
            "k_c": k_c,
            "k_above": k_above,
            "largest_component_macro_at_kc_plus_0.2": (
                None if row_above is None else int(
                    row_above["components_macro"][0])),
            "n_nested_components_at_kc": (
                None if row_kc is None else int(
                    len(row_kc["components_nested"]))),
            "components_nested_at_kc": (
                None if row_kc is None else
                row_kc["components_nested"]),
            "bandwidth_total_rise_bits":
                scan["bandwidth_total_rise_bits"],
            "scan": scan,
        })
    checks = {
        "macro_complete_just_above_kc": all(
            r["largest_component_macro_at_kc_plus_0.2"]
            == t["macro_size"]
            for r in per_seed),
        "nesting_persists_at_kc": all(
            r["n_nested_components_at_kc"] is not None
            and r["n_nested_components_at_kc"]
            >= t["nested_components_min"]
            for r in per_seed),
        "bandwidth_rises_overall": all(
            r["bandwidth_total_rise_bits"]
            >= t["total_rise_min_bits"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(lix) the measured shape: the macro forms "
                 "just above K_c, nesting persists at K_c, "
                 "bandwidth rises overall",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def grt_transition_claims():
    """The three GRT phase-transition claims (lvii)-(lix), measured fresh."""
    claim_lvii = claim_machinery_verdict()
    claim_lviii = claim_transition_verdict()
    claim_lix = claim_shape_verdict()
    verdicts = [claim_lvii, claim_lviii, claim_lix]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_lvii_machinery": claim_lvii,
        "claim_lviii_transition": claim_lviii,
        "claim_lix_shape": claim_lix,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the K sweep, K_c, the bandwidth steps, the
    component structure, and the claims (lvii)-(lix)
    verdicts."""
    print("GRT phase-transition -- claims (lvii)-(lix)")
    print()
    verdicts = grt_transition_claims()
    lvii = verdicts["claim_lvii_machinery"]
    print("K_c and endpoints, per seed:")
    for r in lvii["per_seed"]:
        print(f"  seed {r['seed']}: K_c = {r['k_c']}, mean R(0) = "
              f"{r['mean_r_at_k0']:.4f}, largest component at K = 0 "
              f"is {r['largest_component_at_k0']} "
              f"{r['components_macro_at_k0']}, mean R(1) = "
              f"{r['mean_r_at_k1']:.4f}, B(1) = "
              f"{r['bandwidth_at_k1']:.4f}")
    print(f"claim (lvii) verdict: {'PASS' if lvii['passed'] else 'FAIL'}")
    print()
    lviii = verdicts["claim_lviii_transition"]
    for r in lviii["per_seed"]:
        print(f"  seed {r['seed']}: K_c = {r['k_c']}, step at K_c = "
              f"{r['step_at_kc_bits']:+.4f} bits, max step = "
              f"{r['max_step_bits']:.4f} bits at K = {r['max_step_k']}")
    print(f"claim (lviii) verdict: "
          f"{'PASS' if lviii['passed'] else 'FAIL'}")
    print()
    lix = verdicts["claim_lix_shape"]
    for r in lix["per_seed"]:
        print(f"  seed {r['seed']}: K_c = {r['k_c']}, macro at "
              f"K_c + 0.2 = {r['k_above']}: largest component = "
              f"{r['largest_component_macro_at_kc_plus_0.2']}, nested "
              f"components at K_c = "
              f"{r['n_nested_components_at_kc']} "
              f"{r['components_nested_at_kc']}, total B rise = "
              f"{r['bandwidth_total_rise_bits']:.4f} bits")
    print(f"claim (lix) verdict: {'PASS' if lix['passed'] else 'FAIL'}")
    print()
    print(f"{verdicts['n_passed']}/{verdicts['n_claims']} claims passed")


if __name__ == "__main__":
    main()
