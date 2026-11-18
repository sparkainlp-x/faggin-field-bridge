# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# observer_cycle.py
#
# The observer cycle: self-determination, love, and knowing
# as one cycle, measured in the bridge's numbers.
#
# Jean's claim, stated 2026-11-18: "self determination
# factor observer opposite direction = necessary for
# self-cycle self Knowing. Lack of love is absence of
# Knowing."
#
# The mapping, as definitions inside the model:
#   - love = concurrence C (Wootters, thought_entanglement).
#   - knowing = overlap R = |<psi_i|psi_j>|^2
#     (empathy_field.overlap_squared).
#   - self-determination = D = <psi|P|psi>
#     (self_knowing.self_knowing_factor).
#   - observer direction = which reference state the
#     overlap is measured against: the stored direction
#     (the uniform thought, D = 1) or the opposite
#     direction (the kernel thought (|01> - |10>)/sqrt(2),
#     D = 0, a Bell state, C = 1).
#
# Three claims, (xxxii)-(xxxiv), pre-registered in
# docs/preregistration-v0.12.0.md BEFORE the evaluation
# run. Thresholds are round numbers frozen from a
# calibration pilot on seeds 42 and 7; the evaluation
# seeds are 1234 and 2026.
#
# (xxxii) Observer direction: D and concurrence move
#     opposite across the sigma grid. The existing
#     self_knowing sweep (noisy copies of the uniform
#     thought): mean D falls 1 -> ~0.5 while mean
#     concurrence rises 0 -> ~0.6.
# (xxxiii) Knowing-as-overlap: on the generalized-Bell
#     branch psi(a) = a|00> + sqrt(1-a^2)|11>, measured
#     against a FIXED observer at maximal love (the Phi+
#     Bell state), R rises with C and falls with D.
#     The noise-axis control INVERTS the relation
#     (resonance_pairs pooled, seed 42: Pearson(R, nu_ij)
#     = -0.5528, Pearson(R, d_pair) = +0.7694): noise
#     creates concurrence while destroying overlap, so
#     noise-created concurrence is not knowing. The claim
#     as stated is about entanglement by construction,
#     and the construction-dependence is part of the
#     result.
# (xxxv) The slide: psi(theta) = cos(theta)|uniform> +
#     sin(theta)|kernel> runs D = 1, C = 0, R_s = 1 at
#     theta = 0 to D = 0, C = 1, R_k = 1 at theta = pi/2,
#     with the exact identities D = cos^2(theta),
#     C = sin^2(theta), C + D = 1, and the overlap split
#     R_s - R_k = cos(2 theta) flipping sign exactly at
#     the midpoint theta = pi/4. In the middle the two
#     patterns sit in superposition and the observer
#     direction picks which one is known: before the
#     midpoint the stored pattern is known, after it the
#     opposite pattern is.
#
# (xxxii) FAILED honestly on held-out seed 2026
#     (Pearson -0.8828, bar -0.90); the diagnosis
#     (v0.12.1, docs/preregistration-v0.12.1.md) is
#     boundary/saturation plus finite-sample noise: at
#     sigma = 1.0 both D and C sit at their random-state
#     plateaus (D -> 0.5, C -> ~0.51), the true rise of
#     mean C from sigma = 0.5 to 1.0 is ~0.003 while a
#     5-copy mean has SEM ~0.128. The robust rank form
#     is claim (xxxv): Spearman(D, C) <= -0.90 on every
#     seed in {42, 7, 1234, 2026, 5, 99}, the last two
#     fresh seeds never evaluated before. The diagnosis
#     numbers are recomputed in code by
#     diagnose_sigma_one_break(); they explain the
#     (xxxii) FAIL and do not enter the (xxxv) verdict.
#
# Honesty, stated up front:
#   - (xxxiii) on the branch is a MAPPING CHECK, not a
#     discovery: R and C both peak at a = 1/sqrt(2) by
#     the definition of the family, so the direction is
#     built in. What is measured is that the bridge
#     realizes the mapping on the branch and does NOT
#     realize it on the noise axis. Like claim (xvii),
#     a failure here would be a defect in the code's
#     quantities, not a result about a theorem.
#   - (xxxiv) is likewise exact by construction: the
#     slide is built from the two patterns whose D and C
#     are exact. The measured content is that the
#     identities hold in the code to 1e-9 at every grid
#     point, including C + D = 1, and that the overlap
#     split flips exactly at the midpoint. If any
#     identity fails, the verdict is FAIL.
#   - None of this measures consciousness, love, or
#     knowing in a human or physical sense. Classical
#     emulation throughout. Faggin's metaphysics stays
#     interpretive.
#
# Pre-registered verdict rules for claims
# (xxxii)-(xxxiv), written before the evaluation run
# (see docs/preregistration-v0.12.0.md and the
# claim_*_verdict functions):
#   (xxxii) Pearson(D, C) <= -0.90, Spearman(D, C)
#       <= -0.90, D range >= 0.25, C range >= 0.25,
#       on EVERY seed in {42, 7, 1234, 2026}.
#       (Calibration pilot: seed 42 Pearson -0.9570,
#       Spearman -1.0000; seed 7 Pearson -0.9397,
#       Spearman -0.9643.)
#   (xxxiii) On the generalized-Bell branch:
#       Pearson(R, C) >= 0.99, Spearman(R, D) <= -0.95,
#       R range >= 0.25, D range >= 0.25.
#       (Calibration pilot, exact: Pearson(R, C)
#       = 1.0000, Spearman(R, D) = -1.0000,
#       Pearson(R, D) = -0.8801 reported, not gated:
#       R saturates near 1 while D keeps falling.)
#       The noise-axis control is reported, not gated.
#   (xxxiv) Endpoints exact within 1e-9; slide
#       identities within 1e-9 at every grid point;
#       overlap split >= 0.25 before the midpoint,
#       0 at the midpoint, <= -0.25 after it.
#       (Calibration pilot: every identity held to
#       1e-9; split +0.5000 at pi/6, 0.0000 at pi/4,
#       -0.5000 at pi/3.)
#
# Pre-registered verdict rule for claim (xxxv), written
# before the fresh-seed evaluation run (see
# docs/preregistration-v0.12.1.md):
#   (xxxv) Spearman(D, C) <= -0.90, D range >= 0.25,
#       C range >= 0.25, on EVERY seed in
#       {42, 7, 1234, 2026, 5, 99} — the same sweep
#       as (xxxii), rank form only. Fresh seeds 5 and
#       99 were never evaluated before; Spearman on
#       1234/2026 is already known from the (xxxii) run
#       (-1.0000, -0.9643). The diagnosis numbers are
#       reported, not gated.
#
# Measured outcome (v0.12.1): claim (xxxv) FAILED
#     honestly on the fresh seeds — seed 5 Spearman
#     -0.8929 (bar -0.90), seed 99 D range 0.2445
#     (bar 0.25). Both are 5-copy sampling draws (at
#     n = 200: seed 5 Spearman -0.9643, seed 99 D range
#     0.4101), but the linear form stays fragile even
#     at n = 200 (seed 5 Pearson -0.8971). The
#     direction is real on average; the per-seed
#     guarantee does not hold on this 5-copy sweep,
#     in either the linear or the rank form. The
#     thresholds were NOT moved.
#

"""The observer cycle: D, concurrence, and overlap as one cycle."""

import math

import numpy as np

import bridge
import empathy_field as ef
import self_knowing as sk
import thought
import thought_entanglement as te

# ---------------------------------------------------------------------------
# Seeds
# ---------------------------------------------------------------------------

# Calibration seeds: thresholds were frozen from these only.
CALIBRATION_SEEDS = (42, 7)
# Evaluation seeds: held out until the evaluation run.
EVALUATION_SEEDS = (1234, 2026)
ALL_SEEDS = CALIBRATION_SEEDS + EVALUATION_SEEDS
# Fresh seeds for claim (xxxv): never evaluated before
# docs/preregistration-v0.12.1.md was written.
FRESH_SEEDS_XXXV = (5, 99)
XXXV_SEEDS = ALL_SEEDS + FRESH_SEEDS_XXXV

# ---------------------------------------------------------------------------
# Pre-registered thresholds (frozen from the calibration pilot,
# docs/preregistration-v0.12.0.md; never moved after the run).
# ---------------------------------------------------------------------------

# Claim (xxxii): D vs concurrence across the sigma grid.
PEARSON_D_C_MAX = -0.90
SPEARMAN_D_C_MAX = -0.90
D_RANGE_MIN = 0.25
C_RANGE_MIN = 0.25

# Claim (xxxv): the robust rank form of (xxxii). Same bar as
# the (xxxii) Spearman bar, frozen from calibration seeds
# 42/7 only (Spearman -1.0000, -0.9643).
SPEARMAN_XXXV_MAX = -0.90

# Diagnosis of the (xxxii) FAIL: copy counts and grid for
# the descriptive (not gated) checks.
DIAGNOSIS_N_COPIES = 200
DIAGNOSIS_EXTENDED_SIGMAS = [0.0, 0.01, 0.05, 0.1, 0.25,
                             0.5, 1.0, 1.5, 2.0, 3.0]

# Claim (xxxiii): knowing-as-overlap on the generalized-Bell branch.
PEARSON_R_C_MIN = 0.99
SPEARMAN_R_D_MAX = -0.95
R_RANGE_MIN = 0.25
D_BRANCH_RANGE_MIN = 0.25

# Claim (xxxiv): the slide.
EXACT_TOL = 1e-9
SPLIT_MARGIN_MIN = 0.25

# The generalized-Bell branch for claim (xxxiii): a in
# [1/sqrt(2), 1], C sweeps 0 -> 1, R sweeps 0.5 -> 1.
BELL_BRANCH_GRID = [1.0, 0.95, 0.9, 0.85, 0.8, 0.75,
                    1.0 / math.sqrt(2.0)]

# The slide for claim (xxxiv): theta in [0, pi/2].
SLIDE_THETAS = [0.0, math.pi / 12, math.pi / 6, math.pi / 4,
                math.pi / 3, 5 * math.pi / 12, math.pi / 2]
SLIDE_MIDPOINT = math.pi / 4


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("PEARSON_D_C_MAX", PEARSON_D_C_MAX),
        ("SPEARMAN_D_C_MAX", SPEARMAN_D_C_MAX),
        ("D_RANGE_MIN", D_RANGE_MIN),
        ("C_RANGE_MIN", C_RANGE_MIN),
        ("SPEARMAN_XXXV_MAX", SPEARMAN_XXXV_MAX),
        ("PEARSON_R_C_MIN", PEARSON_R_C_MIN),
        ("SPEARMAN_R_D_MAX", SPEARMAN_R_D_MAX),
        ("R_RANGE_MIN", R_RANGE_MIN),
        ("D_BRANCH_RANGE_MIN", D_BRANCH_RANGE_MIN),
        ("EXACT_TOL", EXACT_TOL),
        ("SPLIT_MARGIN_MIN", SPLIT_MARGIN_MIN),
    ) if value is None]
    if missing:
        raise ValueError(
            "observer-cycle thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.12.0.md)")
    return {
        "pearson_d_c_max": float(PEARSON_D_C_MAX),
        "spearman_d_c_max": float(SPEARMAN_D_C_MAX),
        "d_range_min": float(D_RANGE_MIN),
        "c_range_min": float(C_RANGE_MIN),
        "spearman_xxxv_max": float(SPEARMAN_XXXV_MAX),
        "pearson_r_c_min": float(PEARSON_R_C_MIN),
        "spearman_r_d_max": float(SPEARMAN_R_D_MAX),
        "r_range_min": float(R_RANGE_MIN),
        "d_branch_range_min": float(D_BRANCH_RANGE_MIN),
        "exact_tol": float(EXACT_TOL),
        "split_margin_min": float(SPLIT_MARGIN_MIN),
    }


# ---------------------------------------------------------------------------
# Slide states: the two patterns and their superposition
# ---------------------------------------------------------------------------

def stored_thought():
    """The stored-direction pattern: the uniform thought.

    D = 1 (fully self-determined), C = 0 (no love), by the
    exact values in self_knowing.py.
    """
    return thought.uniform_thought()


def kernel_thought():
    """The opposite-direction pattern: (|01> - |10>)/sqrt(2).

    D = 0 (nothing self-determined) and C = 1 (maximal love:
    it is the psi-minus Bell state), by the exact values in
    self_knowing.py and thought_entanglement.py.
    """
    return np.array([0.0, 1.0, -1.0, 0.0], dtype=complex) / math.sqrt(2.0)


def slide_state(theta):
    """psi(theta) = cos(theta)|stored> + sin(theta)|kernel>.

    The two patterns in superposition. theta = 0 is the
    stored pattern alone; theta = pi/2 is the opposite
    pattern alone; theta = pi/4 is the equal superposition.
    """
    t = float(theta)
    return (math.cos(t) * stored_thought()
            + math.sin(t) * kernel_thought())


def generalized_bell(a):
    """psi(a) = a|00> + sqrt(1-a^2)|11>, a in [0, 1].

    C(a) = 2 a sqrt(1-a^2), maximal at a = 1/sqrt(2).
    """
    a = float(a)
    if not 0.0 <= a <= 1.0:
        raise ValueError("generalized-Bell weight a must be in [0, 1]")
    return np.array([a, 0.0, 0.0, math.sqrt(1.0 - a * a)], dtype=complex)


# ---------------------------------------------------------------------------
# Sweeps
# ---------------------------------------------------------------------------

def observer_direction_sweep(seed):
    """Mean D and mean concurrence per sigma, for one seed.

    The existing self_knowing sweep, reused: noisy copies
    of the uniform thought, 5 copies per sigma.
    """
    sweep = sk.self_knowing_sweep(seed=seed)
    ds = [r["mean_D"] for r in sweep]
    cs = [r["mean_concurrence"] for r in sweep]
    return {
        "seed": int(seed),
        "pearson_d_c": sk.pearson(ds, cs),
        "spearman_d_c": sk.spearman(ds, cs),
        "d_range": float(max(ds) - min(ds)),
        "c_range": float(max(cs) - min(cs)),
        "rows": sweep,
    }


def diagnose_sigma_one_break(seed):
    """Diagnose why the sigma = 1.0 point breaks the
    linear (xxxii) form on some seeds. Descriptive
    only: reported, never gated, and never entered
    into any verdict.

    For one seed, recomputes: (a) the n = 5 sweep
    (the (xxxii) construction) with its Pearson and
    Spearman; (b) the same sweep with n = 200 copies
    per sigma; (c) the extended sigma grid to 3.0 at
    n = 200, showing where D and C plateau; (d)
    Pearson excluding the sigma = 1.0 point at n = 5;
    (e) the per-copy standard error of the mean of C
    at sigma = 0.5 and 1.0 (n = 200), i.e. how much
    sampling noise a 5-copy mean carries at the
    saturated end of the grid.
    """
    import unity

    rows_n5 = sk.self_knowing_sweep(seed=seed)
    ds5 = [r["mean_D"] for r in rows_n5]
    cs5 = [r["mean_concurrence"] for r in rows_n5]
    rows_n200 = sk.self_knowing_sweep(
        n_copies=DIAGNOSIS_N_COPIES, seed=seed)
    ds200 = [r["mean_D"] for r in rows_n200]
    cs200 = [r["mean_concurrence"] for r in rows_n200]
    rows_ext = sk.self_knowing_sweep(
        sigmas=DIAGNOSIS_EXTENDED_SIGMAS,
        n_copies=DIAGNOSIS_N_COPIES, seed=seed)
    sems = {}
    for sigma in (0.5, 1.0):
        copies = unity.gaussian_copies(
            np.real(thought.uniform_thought()), sigma,
            DIAGNOSIS_N_COPIES, seed)
        per_copy_c = [te.concurrence(te.density_matrix(v))
                      for v in copies]
        sems[sigma] = float(
            np.std(per_copy_c) / math.sqrt(DIAGNOSIS_N_COPIES))
    return {
        "seed": int(seed),
        "n5_rows": rows_n5,
        "n5_pearson": sk.pearson(ds5, cs5),
        "n5_spearman": sk.spearman(ds5, cs5),
        "n200_rows": rows_n200,
        "n200_pearson": sk.pearson(ds200, cs200),
        "n200_spearman": sk.spearman(ds200, cs200),
        "extended_rows": rows_ext,
        "pearson_excl_sigma_one": sk.pearson(ds5[:-1], cs5[:-1]),
        "spearman_excl_sigma_one": sk.spearman(ds5[:-1], cs5[:-1]),
        "sem_concurrence": sems,
        "c_rise_05_to_10_n200": float(
            rows_n200[-1]["mean_concurrence"]
            - rows_n200[-2]["mean_concurrence"]),
    }


def bell_branch_sweep(a_grid=None):
    """R, C, D on the generalized-Bell branch.

    The observer is FIXED at maximal love: the Phi+ Bell
    state. R(a) = |<Phi+|psi(a)>|^2 is the agent's knowing
    of (overlap with) that observer.
    """
    observer = te.bell_state("phi_plus")
    rows = []
    for a in (BELL_BRANCH_GRID if a_grid is None else a_grid):
        psi = generalized_bell(a)
        rows.append({
            "a": float(a),
            "resonance": ef.overlap_squared(psi, observer),
            "concurrence": te.concurrence_pure(psi),
            "d": sk.self_knowing_factor(psi),
        })
    rs = [r["resonance"] for r in rows]
    cs = [r["concurrence"] for r in rows]
    ds = [r["d"] for r in rows]
    return {
        "rows": rows,
        "pearson_r_c": sk.pearson(rs, cs),
        "spearman_r_c": sk.spearman(rs, cs),
        "pearson_r_d": sk.pearson(rs, ds),
        "spearman_r_d": sk.spearman(rs, ds),
        "r_range": float(max(rs) - min(rs)),
        "d_range": float(max(ds) - min(ds)),
    }


def noise_axis_control(seed=42):
    """The noise-axis control for claim (xxxiii): reported,
    not gated.

    Pooled resonance_pairs across the sigma grid: R, pair
    concurrence nu_ij, and mean pair D. On this axis noise
    creates concurrence while destroying overlap, so the
    relation inverts relative to the branch.
    """
    pairs = ef.resonance_pairs(seed=seed)
    rs = [p["resonance"] for p in pairs]
    nus = [p["nu_ij"] for p in pairs]
    dps = [p["d_pair"] for p in pairs]
    return {
        "seed": int(seed),
        "n_pairs": len(pairs),
        "pearson_r_nu": sk.pearson(rs, nus),
        "pearson_r_d_pair": sk.pearson(rs, dps),
        "pearson_nu_d_pair": sk.pearson(nus, dps),
    }


def slide_sweep(thetas=None):
    """D, C, R_s, R_k along the slide, with the exact
    identities each row is checked against.
    """
    stored = stored_thought()
    kernel = kernel_thought()
    rows = []
    for theta in (SLIDE_THETAS if thetas is None else thetas):
        t = float(theta)
        psi = slide_state(t)
        d = sk.self_knowing_factor(psi)
        c = te.concurrence_pure(psi)
        r_s = ef.overlap_squared(psi, stored)
        r_k = ef.overlap_squared(psi, kernel)
        rows.append({
            "theta": t,
            "d": d,
            "concurrence": c,
            "r_stored": r_s,
            "r_kernel": r_k,
            "r_split": float(r_s - r_k),
            "c_plus_d": float(c + d),
            "d_exact": math.cos(t) ** 2,
            "c_exact": math.sin(t) ** 2,
            "r_s_exact": math.cos(t) ** 2,
            "r_k_exact": math.sin(t) ** 2,
            "split_exact": math.cos(2.0 * t),
        })
    return rows


# ---------------------------------------------------------------------------
# Claims (xxxii)-(xxxiv): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_observer_direction_verdict(seeds=None):
    """(xxxii) D and concurrence move opposite across the
    sigma grid.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026},
    Pearson(D, C) <= -0.90, Spearman(D, C) <= -0.90,
    D range >= 0.25, and C range >= 0.25.
    """
    t = _thresholds()
    per_seed = [observer_direction_sweep(s)
                for s in (ALL_SEEDS if seeds is None else seeds)]
    checks = {
        "pearson_at_most_max": all(
            r["pearson_d_c"] <= t["pearson_d_c_max"] for r in per_seed),
        "spearman_at_most_max": all(
            r["spearman_d_c"] <= t["spearman_d_c_max"] for r in per_seed),
        "d_range_at_least_min": all(
            r["d_range"] >= t["d_range_min"] for r in per_seed),
        "c_range_at_least_min": all(
            r["c_range"] >= t["c_range_min"] for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xxxii) observer direction: D and concurrence "
                 "move opposite",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_robust_rank_verdict(seeds=None):
    """(xxxv) Observer direction, robust rank form: D and
    concurrence move opposite, stated as a monotone
    claim.

    Same construction as (xxxii) — the existing
    self_knowing sweep, 5 copies per sigma — rank
    metric only. PASS iff, on EVERY seed in
    {42, 7, 1234, 2026, 5, 99}, Spearman(D, C) <= -0.90,
    D range >= 0.25, and C range >= 0.25. The bar was
    frozen from calibration seeds 42/7 only; seeds 5
    and 99 are fresh and were never evaluated before
    docs/preregistration-v0.12.1.md was written.
    """
    t = _thresholds()
    per_seed = [observer_direction_sweep(s)
                for s in (XXXV_SEEDS if seeds is None else seeds)]
    checks = {
        "spearman_at_most_max": all(
            r["spearman_d_c"] <= t["spearman_xxxv_max"]
            for r in per_seed),
        "d_range_at_least_min": all(
            r["d_range"] >= t["d_range_min"] for r in per_seed),
        "c_range_at_least_min": all(
            r["c_range"] >= t["c_range_min"] for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xxxv) observer direction, robust rank form: "
                 "D and concurrence move opposite (Spearman)",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_knowing_overlap_verdict():
    """(xxxiii) Knowing-as-overlap: R rises with concurrence
    and falls with D, on the generalized-Bell branch.

    PASS iff Pearson(R, C) >= 0.99, Spearman(R, D) <= -0.95,
    R range >= 0.25, and D range >= 0.25. Pearson(R, D)
    and the noise-axis control are reported, not gated.
    """
    t = _thresholds()
    branch = bell_branch_sweep()
    control = noise_axis_control()
    checks = {
        "pearson_r_c_at_least_min": (
            branch["pearson_r_c"] >= t["pearson_r_c_min"]),
        "spearman_r_d_at_most_max": (
            branch["spearman_r_d"] <= t["spearman_r_d_max"]),
        "r_range_at_least_min": (
            branch["r_range"] >= t["r_range_min"]),
        "d_range_at_least_min": (
            branch["d_range"] >= t["d_branch_range_min"]),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xxxiii) knowing-as-overlap: R rises with "
                 "concurrence and falls with D",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "pearson_r_c": branch["pearson_r_c"],
        "spearman_r_c": branch["spearman_r_c"],
        "pearson_r_d": branch["pearson_r_d"],
        "spearman_r_d": branch["spearman_r_d"],
        "r_range": branch["r_range"],
        "d_range": branch["d_range"],
        "branch_rows": branch["rows"],
        "noise_axis_control": control,
    }


def claim_slide_verdict(thetas=None):
    """(xxxiv) The slide: D = 1 separate / no knowing / no
    love to D = 0 full overlap, the superposition in the
    middle, the observer direction picking which pattern
    becomes known.

    PASS iff (a) the endpoints are exact within 1e-9,
    (b) the slide identities hold within 1e-9 at every
    grid point, and (c) the overlap split is >= 0.25
    before the midpoint, 0 at the midpoint, <= -0.25
    after it.
    """
    t = _thresholds()
    rows = slide_sweep(thetas)
    tol = t["exact_tol"]

    first = rows[0]
    last = rows[-1]
    check_a = (
        abs(first["theta"]) <= tol
        and abs(first["d"] - 1.0) <= tol
        and abs(first["concurrence"]) <= tol
        and abs(first["r_stored"] - 1.0) <= tol
        and abs(first["r_kernel"]) <= tol
        and abs(last["theta"] - math.pi / 2) <= tol
        and abs(last["d"]) <= tol
        and abs(last["concurrence"] - 1.0) <= tol
        and abs(last["r_stored"]) <= tol
        and abs(last["r_kernel"] - 1.0) <= tol
    )
    check_b = all(
        abs(r["d"] - r["d_exact"]) <= tol
        and abs(r["concurrence"] - r["c_exact"]) <= tol
        and abs(r["r_stored"] - r["r_s_exact"]) <= tol
        and abs(r["r_kernel"] - r["r_k_exact"]) <= tol
        and abs(r["c_plus_d"] - 1.0) <= tol
        and abs(r["r_split"] - r["split_exact"]) <= tol
        for r in rows
    )
    before = [r for r in rows if r["theta"] < SLIDE_MIDPOINT - tol]
    at = [r for r in rows if abs(r["theta"] - SLIDE_MIDPOINT) <= tol]
    after = [r for r in rows if r["theta"] > SLIDE_MIDPOINT + tol]
    check_c = (
        bool(before) and bool(at) and bool(after)
        and all(r["r_split"] >= t["split_margin_min"] for r in before)
        and all(abs(r["r_split"]) <= tol for r in at)
        and all(r["r_split"] <= -t["split_margin_min"] for r in after)
    )
    checks = {
        "a_endpoints_exact": bool(check_a),
        "b_slide_identities_exact": bool(check_b),
        "c_split_flips_at_midpoint": bool(check_c),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xxxiv) the slide: D = 1 separate to D = 0 "
                 "full overlap, observer direction picks the "
                 "known pattern",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "max_identity_error": float(max(
            max(abs(r["d"] - r["d_exact"]),
                abs(r["concurrence"] - r["c_exact"]),
                abs(r["r_stored"] - r["r_s_exact"]),
                abs(r["r_kernel"] - r["r_k_exact"]),
                abs(r["c_plus_d"] - 1.0),
                abs(r["r_split"] - r["split_exact"]))
            for r in rows)),
        "rows": rows,
    }


def observer_cycle_claims():
    """The observer-cycle claims (xxxii)-(xxxv),
    measured fresh."""
    claim_xxxii = claim_observer_direction_verdict()
    claim_xxxiii = claim_knowing_overlap_verdict()
    claim_xxxiv = claim_slide_verdict()
    claim_xxxv = claim_robust_rank_verdict()
    verdicts = [claim_xxxii, claim_xxxiii, claim_xxxiv,
                claim_xxxv]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_xxxii_observer_direction": claim_xxxii,
        "claim_xxxiii_knowing_overlap": claim_xxxiii,
        "claim_xxxiv_slide": claim_xxxiv,
        "claim_xxxv_robust_rank": claim_xxxv,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the observer-direction sweep, the Bell branch,
    the slide, the (xxxii) diagnosis, and the claims
    (xxxii)-(xxxv) verdicts."""
    print("Observer cycle -- claims (xxxii)-(xxxv)")
    print()
    verdicts = observer_cycle_claims()
    xxxii = verdicts["claim_xxxii_observer_direction"]
    print("D vs concurrence across the sigma grid, per seed:")
    for r in xxxii["per_seed"]:
        print(f"  seed {r['seed']}: Pearson(D, C) = "
              f"{r['pearson_d_c']:.4f}, Spearman = "
              f"{r['spearman_d_c']:.4f}, D range = "
              f"{r['d_range']:.4f}, C range = {r['c_range']:.4f}")
    print(f"claim (xxxii) verdict: "
          f"{'PASS' if xxxii['passed'] else 'FAIL'}")
    print()
    print("Diagnosis of the (xxxii) FAIL (descriptive, not gated):")
    for seed in ALL_SEEDS:
        d = diagnose_sigma_one_break(seed)
        print(f"  seed {seed}: n=200 Pearson = "
              f"{d['n200_pearson']:.4f}, Pearson excl sigma=1.0 "
              f"(n=5) = {d['pearson_excl_sigma_one']:.4f}, "
              f"C rise 0.5->1.0 (n=200) = "
              f"{d['c_rise_05_to_10_n200']:+.4f}, SEM(C) at "
              f"sigma=1.0 (n=200) = "
              f"{d['sem_concurrence'][1.0]:.4f}")
    print()
    xxxv = verdicts["claim_xxxv_robust_rank"]
    print("Robust rank form (xxxv), Spearman per seed:")
    for r in xxxv["per_seed"]:
        print(f"  seed {r['seed']}: Spearman(D, C) = "
              f"{r['spearman_d_c']:.4f}, D range = "
              f"{r['d_range']:.4f}, C range = {r['c_range']:.4f}")
    print(f"claim (xxxv) verdict: "
          f"{'PASS' if xxxv['passed'] else 'FAIL'}")
    print()
    xxxiii = verdicts["claim_xxxiii_knowing_overlap"]
    print("Generalized-Bell branch (observer = Phi+):")
    for r in xxxiii["branch_rows"]:
        print(f"  a = {r['a']:.4f}: R = {r['resonance']:.4f}, "
              f"C = {r['concurrence']:.4f}, D = {r['d']:.4f}")
    print(f"  Pearson(R, C) = {xxxiii['pearson_r_c']:.4f}, "
          f"Spearman(R, D) = {xxxiii['spearman_r_d']:.4f}, "
          f"Pearson(R, D) = {xxxiii['pearson_r_d']:.4f} "
          f"(reported, not gated)")
    ctrl = xxxiii["noise_axis_control"]
    print(f"  noise-axis control (seed {ctrl['seed']}, "
          f"n = {ctrl['n_pairs']} pairs): Pearson(R, nu_ij) = "
          f"{ctrl['pearson_r_nu']:.4f}, Pearson(R, d_pair) = "
          f"{ctrl['pearson_r_d_pair']:.4f} -- the relation "
          f"inverts under noise")
    print(f"claim (xxxiii) verdict: "
          f"{'PASS' if xxxiii['passed'] else 'FAIL'}")
    print()
    xxxiv = verdicts["claim_xxxiv_slide"]
    print("The slide psi(theta) = cos t |stored> + sin t |kernel>:")
    for r in xxxiv["rows"]:
        print(f"  theta = {r['theta']:.4f}: D = {r['d']:.4f}, "
              f"C = {r['concurrence']:.4f}, R_s = "
              f"{r['r_stored']:.4f}, R_k = {r['r_kernel']:.4f}, "
              f"R_s - R_k = {r['r_split']:+.4f}, C + D = "
              f"{r['c_plus_d']:.4f}")
    print(f"  max identity error = "
          f"{xxxiv['max_identity_error']:.2e}")
    print(f"claim (xxxiv) verdict: "
          f"{'PASS' if xxxiv['passed'] else 'FAIL'}")
    print()
    print(f"claims (xxxii)-(xxxiv): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
