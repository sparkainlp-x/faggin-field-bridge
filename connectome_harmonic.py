# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# connectome_harmonic.py
#
# Connectome-harmonic / structure-function coupling analogue
# (v0.17.0, deep-think upgrade #10, report.md section 9
# rank 10 and section 2): connectome harmonic decomposition
# (CHD, Atasoy et al. 2016) and the structure-function
# coupling finding of Luppi et al., Communications Biology
# 6:117, 2023 (established finding) — loss of consciousness
# (propofol anaesthesia, disorders of consciousness) =
# increased structure-function coupling across scales;
# LSD/ketamine = the opposite (decoupling).
#
# The construction (fixed before the pilot; see
# docs/preregistration-v0.17.0.md):
#   - Base field: the v0.5.0 resonance population (8 agents,
#     noisy copies of the uniform thought), on the noise
#     grid sigma in (0.10, 0.25, 0.50, 1.00). Sigma = 0.25
#     is the attuned reference (the v0.4.0 fix holds at
#     sigma <= 0.25 and breaks at sigma >= 0.50); sigma =
#     0.50 is the break; sigma = 1.00 is the far-broken
#     regime.
#   - Structure graph: the coupling matrix W with W_ij =
#     R_ij = |<psi_i|psi_j>|^2 for i != j, W_ii = 0 (the
#     thought-pair coupling matrix — the graph the project
#     did not yet have). Graph Laplacian L = D - W,
#     D_ii = sum_j W_ij. Harmonic modes are the
#     eigenvectors of L, eigenvalues lambda_0 = 0 <=
#     lambda_1 <= ... <= lambda_7.
#   - Functional connectivity: F_ij = the Bhattacharyya
#     coefficient sum_k sqrt(p_ik * p_jk) between the
#     agents' Born distributions p_i, p_j. F is genuinely
#     distinct from W: W is the squared overlap of the
#     amplitude vectors (phase/sign-sensitive), F is the
#     overlap of the probability vectors (sign-blind).
#   - Structure-function coupling kappa(sigma) = the
#     Pearson correlation between the upper-triangular
#     entries of W and of F (28 pairs). This is the
#     standard connectomics definition of
#     structure-function coupling (correlation of
#     structural and functional connectivity), applied
#     to the bridge's graph.
#   - Harmonic smoothness of a per-node functional
#     signal x (here x = the D_i vector): the Rayleigh
#     quotient RQ(x) = x_c^T L x_c / x_c^T x_c on the
#     centred signal, normalised by the mean nonzero
#     eigenvalue, rho(x) = RQ(x) / mean(lambda_1..7).
#     rho < 1 means smoother than random on the graph
#     (structure-aligned); rho ~= 1 means random-like
#     (decoupled); rho > 1 means rougher than random.
#     RQ is basis-independent, which matters here: at
#     low sigma the graph is near-complete and
#     lambda_1..lambda_7 are nearly degenerate (7.59-
#     7.89 at sigma = 0.10 on seed 42), so a
#     low-frequency energy share depends on an
#     arbitrary choice of basis inside the degenerate
#     subspace and is NOT used as a gated measure.
#   - Decoupling control: permute the entries of F (50
#     permutations, fixed rng seed 1000 + seed) and
#     recompute kappa. The shuffle detaches function
#     from structure while leaving the field — and
#     therefore f, the attunement status — unchanged
#     by construction, so it is the psychedelic-like
#     decoupling analogue: low coupling without any
#     change in attunement.
#
# Honesty, stated up front:
#   - This is a SYNTHETIC classical emulation. Nothing
#     here tests consciousness, anaesthesia, disorders
#     of consciousness, or psychedelics in a human.
#     Luppi et al. 2023 is the empirical grounding for
#     the coupling direction being tested; what is
#     measured is whether the model's coupling behaves
#     that way. No scalar Phi is computed or used
#     anywhere (standing do-not list); E = h*nu is not
#     used in this module at all.
#   - The report's directional prediction already FAILS
#     on the calibration seeds: kappa(0.50) is BELOW
#     kappa(0.25) by 0.599 / 0.430, and kappa(1.00) is
#     below kappa(0.25) by 0.192 / 0.203. Loss of
#     attunement does NOT raise coupling in this wiring
#     — the broken regime is the LEAST coupled, not
#     the most. Claim (lv) gates the report's
#     prediction as stated and is expected to FAIL;
#     claim (lvi) gates the shape that IS measured
#     (dip at the break, recovery past it, decoupling
#     control near zero).
#   - kappa ~= 1.0000 at sigma = 0.10 on both seeds is
#     a near-parallel artefact, not a discovery: at
#     sigma = 0.10 all agents are near-identical
#     (sd(W) ~= 0.02), so W and F are both ~= 1 with
#     the same noise driving both deviations, and
#     their correlation is trivially ~= 1. kappa(0.10)
#     is REPORTED, not gated, in every claim.
#   - The per-node harmonic route is a null result in
#     this wiring: the D signal's Rayleigh quotient
#     sits at rho ~= 1 (worst |rho - 1| = 0.169 on the
#     calibration seeds), indistinguishable from a
#     random permutation of itself, and the
#     low-frequency energy share is seed-unstable
#     (0.10 / 0.80 at sigma = 0.10) — the degenerate-
#     subspace artefact. The graph is too dense and
#     near-complete for node signals to carry harmonic
#     structure; the coupling signal lives in the
#     pair-level correlation kappa, not in node
#     harmonics. Both are reported.
#
# Pre-registered verdict rules for claims (liv)-(lvi),
# written before the evaluation run (see
# docs/preregistration-v0.17.0.md and the
# claim_*_verdict functions):
#   (liv) CHD machinery exact, node signals harmonically
#       random-like: on every seed x sigma, the
#       Laplacian identities hold to 1e-12 (symmetric,
#       PSD, lambda_0 ~= 0, sorted eigenvalues,
#       orthonormal eigenvectors) AND |rho(D) - 1| <=
#       0.20. (Calibration pilot: worst |rho - 1| =
#       0.169.)
#   (lv) The Luppi prediction as stated: kappa(0.50) >=
#       kappa(0.25) + 0.10 AND kappa(1.00) >=
#       kappa(0.25) + 0.10, on every seed.
#       (Calibration pilot: kappa(0.50) - kappa(0.25)
#       = -0.599 / -0.430; kappa(1.00) - kappa(0.25)
#       = -0.192 / -0.203 — expected FAIL.)
#   (lvi) The measured shape: on every seed,
#       kappa(0.25) >= 0.80; kappa(0.50) <=
#       kappa(0.25) - 0.30; kappa(1.00) >=
#       kappa(0.50) + 0.10; and at sigma = 0.25 the
#       shuffle null is near zero (|mean kappa over 50
#       shuffles| <= 0.10) and separated from
#       kappa(0.25) by >= 0.50. (Calibration pilot:
#       kappa(0.25) = 0.999 / 0.842; dip 0.599 / 0.430;
#       recovery 0.407 / 0.227; |shuffle mean| <= 0.039;
#       separation >= 0.812.)

"""Connectome-harmonic structure-function coupling, claims (liv)-(lvi)."""

import numpy as np

import bridge
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
# docs/preregistration-v0.17.0.md; never moved after the run).
# ---------------------------------------------------------------------------

# The noise grid: 0.25 is the attuned reference (v0.4.0 fix
# holds at sigma <= 0.25), 0.50 is the break, 1.00 is the
# far-broken regime. 0.10 is reported, not gated (the
# near-parallel artefact: kappa ~= 1 there trivially).
SIGMA_GRID = (0.10, 0.25, 0.50, 1.00)
SIGMA_ATTUNED = 0.25
SIGMA_BREAK = 0.50
SIGMA_FAR = 1.00
N_AGENTS = 8

# Exactness tolerance for the Laplacian identities.
EXACT_TOL = 1e-12

# Claim (liv): the D signal's Rayleigh quotient must sit
# within this of 1 (random-like) on every seed x sigma
# (calibration worst |rho - 1| = 0.169).
RHO_DEVIATION_MAX = 0.20

# Claim (lv): the report's predicted rise, from the attuned
# sigma to the break and to the far-broken regime.
KAPPA_RISE_MIN = 0.10

# Claim (lvi): the measured shape.
KAPPA_ATTUNED_MIN = 0.80
KAPPA_DIP_MIN = 0.30
KAPPA_RECOVERY_MIN = 0.10
# The shuffle null at sigma = 0.25: its mean over 50
# permutations must be within this of zero (calibration
# worst |mean| = 0.039), and kappa(0.25) must exceed it
# by at least this (calibration worst separation 0.812).
SHUFFLE_MEAN_MAX = 0.10
SHUFFLE_SEPARATION_MIN = 0.50
N_SHUFFLES = 50


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("SIGMA_GRID", SIGMA_GRID),
        ("N_AGENTS", N_AGENTS),
        ("EXACT_TOL", EXACT_TOL),
        ("RHO_DEVIATION_MAX", RHO_DEVIATION_MAX),
        ("KAPPA_RISE_MIN", KAPPA_RISE_MIN),
        ("KAPPA_ATTUNED_MIN", KAPPA_ATTUNED_MIN),
        ("KAPPA_DIP_MIN", KAPPA_DIP_MIN),
        ("KAPPA_RECOVERY_MIN", KAPPA_RECOVERY_MIN),
        ("SHUFFLE_MEAN_MAX", SHUFFLE_MEAN_MAX),
        ("SHUFFLE_SEPARATION_MIN", SHUFFLE_SEPARATION_MIN),
        ("N_SHUFFLES", N_SHUFFLES),
    ) if value is None]
    if missing:
        raise ValueError(
            "connectome-harmonic thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.17.0.md)")
    return {
        "sigma_grid": tuple(float(s) for s in SIGMA_GRID),
        "n_agents": int(N_AGENTS),
        "exact_tol": float(EXACT_TOL),
        "rho_deviation_max": float(RHO_DEVIATION_MAX),
        "kappa_rise_min": float(KAPPA_RISE_MIN),
        "kappa_attuned_min": float(KAPPA_ATTUNED_MIN),
        "kappa_dip_min": float(KAPPA_DIP_MIN),
        "kappa_recovery_min": float(KAPPA_RECOVERY_MIN),
        "shuffle_mean_max": float(SHUFFLE_MEAN_MAX),
        "shuffle_separation_min": float(SHUFFLE_SEPARATION_MIN),
        "n_shuffles": int(N_SHUFFLES),
    }


# ---------------------------------------------------------------------------
# The graph, its harmonics, and the coupling
# ---------------------------------------------------------------------------

def coupling_matrix(states):
    """W_ij = R_ij = |<psi_i|psi_j>|^2 for i != j, W_ii = 0:
    the thought-pair coupling matrix — the structure graph."""
    states = list(states)
    if len(states) < 2:
        raise ValueError("need at least two agents for a graph")
    n = len(states)
    w = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                w[i, j] = ef.overlap_squared(states[i], states[j])
    return w


def graph_laplacian(w):
    """L = D - W, D_ii = sum_j W_ij."""
    w = np.asarray(w, dtype=float)
    if w.ndim != 2 or w.shape[0] != w.shape[1]:
        raise ValueError("coupling matrix must be square")
    if np.any(w < 0.0):
        raise ValueError("coupling weights must be >= 0")
    return np.diag(np.sum(w, axis=1)) - w


def harmonic_modes(w):
    """Eigen-decomposition of the graph Laplacian: eigenvalues
    sorted ascending (lambda_0 = 0 first) and the harmonic
    modes (eigenvectors) as columns."""
    lap = graph_laplacian(w)
    values, vectors = np.linalg.eigh(lap)
    return {"laplacian": lap, "eigenvalues": values,
            "modes": vectors}


def laplacian_identities(w):
    """The exact identities the Laplacian must satisfy:
    symmetric, positive semidefinite, lambda_0 ~= 0, sorted
    eigenvalues, orthonormal eigenvectors. Returns the worst
    violation of each, all of which must sit below EXACT_TOL
    (up to the PSD floor, which is one-sided)."""
    h = harmonic_modes(w)
    lap = h["laplacian"]
    values = h["eigenvalues"]
    modes = h["modes"]
    return {
        "symmetry_error": float(np.max(np.abs(lap - lap.T))),
        "min_eigenvalue": float(values[0]),
        "lambda_0_abs": float(abs(values[0])),
        "sorted": bool(np.all(np.diff(values) >= 0.0)),
        "orthonormality_error": float(np.max(np.abs(
            modes.T @ modes - np.eye(modes.shape[1])))),
        "eigenvalues": values,
    }


def born_probabilities(states):
    """Each agent's Born distribution over the four concepts."""
    return [thought.born_probabilities(s) for s in states]


def functional_connectivity(states):
    """F_ij = the Bhattacharyya coefficient sum_k
    sqrt(p_ik * p_jk) between the agents' Born
    distributions: the functional connectivity, genuinely
    distinct from W (sign-blind where W is
    sign-sensitive)."""
    probs = born_probabilities(states)
    n = len(probs)
    f = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                f[i, j] = float(np.sum(np.sqrt(probs[i] * probs[j])))
    return f


def _upper_triangular(matrix):
    """The upper-triangular entries (i < j) as a flat array."""
    matrix = np.asarray(matrix, dtype=float)
    n = matrix.shape[0]
    return np.array([matrix[i, j] for i in range(n)
                     for j in range(i + 1, n)])


def _pearson(a, b):
    """Pearson correlation, or NaN when either side is constant."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if float(np.std(a)) < 1e-12 or float(np.std(b)) < 1e-12:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def structure_function_coupling(states):
    """kappa = Pearson correlation between the upper-triangular
    entries of W (structure) and of F (function)."""
    w = coupling_matrix(states)
    f = functional_connectivity(states)
    return _pearson(_upper_triangular(w), _upper_triangular(f))


def rayleigh_quotient_ratio(states, signal):
    """rho(x) = (x_c^T L x_c / x_c^T x_c) / mean(lambda_1..N-1):
    the harmonic smoothness of a centred per-node signal,
    normalised so rho = 1 is random-like on the graph.
    Also returns the low-frequency (modes 1..2) energy share
    of the centred signal, reported not gated: at low sigma
    the nonzero eigenvalues are nearly degenerate, so the
    share depends on an arbitrary basis choice inside the
    degenerate subspace (pilot 1)."""
    states = list(states)
    w = coupling_matrix(states)
    h = harmonic_modes(w)
    lap = h["laplacian"]
    values = h["eigenvalues"]
    modes = h["modes"]
    x = np.asarray(signal, dtype=float)
    if x.shape[0] != len(states):
        raise ValueError("signal must have one entry per agent")
    xc = x - float(np.mean(x))
    denom = float(xc @ xc)
    if denom <= 1e-18:
        raise ValueError("signal is constant: no harmonic content")
    rq = float(xc @ lap @ xc) / denom
    mean_nonzero = float(np.mean(values[1:]))
    coeffs = modes.T @ xc
    power = coeffs ** 2
    total = float(np.sum(power[1:]))
    low2_share = (float(np.sum(power[1:3])) / total
                  if total > 0.0 else float("nan"))
    return {"rho": float(rq / mean_nonzero),
            "rayleigh_quotient": rq,
            "mean_nonzero_eigenvalue": mean_nonzero,
            "low2_energy_share": low2_share,
            "eigenvalues": values}


def field_row(sigma, n_agents=N_AGENTS, seed=42):
    """One sigma row: kappa, rho(D), the low-2 share, the
    eigenvalues, and the field's f and mean R for context."""
    states = ef.resonance_population(sigma, n_agents, seed)
    w = coupling_matrix(states)
    ident = laplacian_identities(w)
    ds = [ef.agent_self_determinism(s) for s in states]
    harm = rayleigh_quotient_ratio(states, ds)
    return {
        "sigma": float(sigma),
        "seed": int(seed),
        "kappa": float(structure_function_coupling(states)),
        "rho_d": float(harm["rho"]),
        "low2_energy_share_d": float(harm["low2_energy_share"]),
        "eigenvalues": harm["eigenvalues"],
        "symmetry_error": ident["symmetry_error"],
        "min_eigenvalue": ident["min_eigenvalue"],
        "lambda_0_abs": ident["lambda_0_abs"],
        "sorted": bool(ident["sorted"]),
        "orthonormality_error": ident["orthonormality_error"],
        "f_mean_pair_concurrence": float(ef.empathy_fraction(states)),
        "mean_r": float(np.mean(_upper_triangular(w))),
    }


def coupling_vs_noise(seed, sigmas=None, n_agents=N_AGENTS):
    """kappa (and the harmonic diagnostics) across the sigma grid."""
    return [field_row(sigma, n_agents, seed)
            for sigma in (SIGMA_GRID if sigmas is None else sigmas)]


def shuffle_null(states, seed, n_shuffles=N_SHUFFLES):
    """The decoupling control: permute the entries of F and
    recompute kappa. The shuffle detaches function from
    structure while leaving the field — and therefore f —
    unchanged by construction. Returns the mean, the mean
    absolute value, and the max absolute value over the
    permutations (fixed rng stream: seed 1000 + seed)."""
    w = _upper_triangular(coupling_matrix(states))
    f = _upper_triangular(functional_connectivity(states))
    rng = np.random.default_rng(1000 + int(seed))
    values = [_pearson(w, rng.permutation(f))
              for _ in range(int(n_shuffles))]
    values = [v for v in values if not np.isnan(v)]
    if not values:
        raise ValueError("functional connectivity is constant: "
                         "no shuffle null exists")
    return {"n_shuffles": len(values),
            "mean": float(np.mean(values)),
            "mean_abs": float(np.mean(np.abs(values))),
            "max_abs": float(np.max(np.abs(values))),
            "values": values}


def shuffle_null_row(sigma, n_agents=N_AGENTS, seed=42):
    """The shuffle null at one sigma, with kappa for comparison."""
    states = ef.resonance_population(sigma, n_agents, seed)
    null = shuffle_null(states, seed)
    return {"sigma": float(sigma), "seed": int(seed),
            "kappa": float(structure_function_coupling(states)),
            "f_mean_pair_concurrence": float(
                ef.empathy_fraction(states)),
            "shuffle_mean": null["mean"],
            "shuffle_mean_abs": null["mean_abs"],
            "shuffle_max_abs": null["max_abs"]}


# ---------------------------------------------------------------------------
# Claim verdicts (liv)-(lvi)
# ---------------------------------------------------------------------------

def claim_machinery_verdict(seeds=None):
    """(liv) CHD machinery is exact, and node signals are
    harmonically random-like.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026} and
    EVERY sigma in (0.10, 0.25, 0.50, 1.00): the Laplacian
    identities hold (symmetric, PSD, lambda_0 ~= 0, sorted
    eigenvalues, orthonormal eigenvectors, all to 1e-12)
    AND |rho(D) - 1| <= 0.20. The low-frequency energy
    share is reported, not gated (degeneracy artefact).
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        rows = coupling_vs_noise(seed)
        worst_sym = max(r["symmetry_error"] for r in rows)
        worst_orth = max(r["orthonormality_error"] for r in rows)
        worst_l0 = max(r["lambda_0_abs"] for r in rows)
        min_eig = min(r["min_eigenvalue"] for r in rows)
        worst_rho_dev = max(abs(r["rho_d"] - 1.0) for r in rows)
        per_seed.append({
            "seed": int(seed),
            "symmetry_error_max": float(worst_sym),
            "orthonormality_error_max": float(worst_orth),
            "lambda_0_abs_max": float(worst_l0),
            "min_eigenvalue": float(min_eig),
            "eigenvalues_sorted": bool(all(r["sorted"] for r in rows)),
            "rho_deviation_max": float(worst_rho_dev),
            "rows": rows,
        })
    checks = {
        "laplacian_symmetric": all(
            r["symmetry_error_max"] < t["exact_tol"] for r in per_seed),
        "laplacian_psd": all(
            r["min_eigenvalue"] >= -t["exact_tol"] for r in per_seed),
        "lambda_0_near_zero": all(
            r["lambda_0_abs_max"] < t["exact_tol"] for r in per_seed),
        "eigenvalues_sorted": all(
            r["eigenvalues_sorted"] for r in per_seed),
        "eigenvectors_orthonormal": all(
            r["orthonormality_error_max"] < t["exact_tol"]
            for r in per_seed),
        "rho_d_within_bar": all(
            r["rho_deviation_max"] <= t["rho_deviation_max"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(liv) CHD machinery is exact, and node signals "
                 "are harmonically random-like",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def _kappa_by_sigma(seed, n_agents=N_AGENTS):
    rows = coupling_vs_noise(seed, n_agents=n_agents)
    return {r["sigma"]: r for r in rows}


def claim_luppi_verdict(seeds=None):
    """(lv) The Luppi prediction as stated: coupling rises
    with loss of attunement.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
    kappa(0.50) >= kappa(0.25) + 0.10 AND kappa(1.00) >=
    kappa(0.25) + 0.10. Calibration pilot: kappa(0.50) -
    kappa(0.25) = -0.599 / -0.430; kappa(1.00) -
    kappa(0.25) = -0.192 / -0.203 — the prediction fails
    on both calibration seeds, so this claim is expected
    to FAIL. The failure is the result.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        by_sigma = _kappa_by_sigma(seed)
        k025 = by_sigma[SIGMA_ATTUNED]["kappa"]
        k050 = by_sigma[SIGMA_BREAK]["kappa"]
        k100 = by_sigma[SIGMA_FAR]["kappa"]
        per_seed.append({
            "seed": int(seed),
            "kappa_0.25": float(k025),
            "kappa_0.50": float(k050),
            "kappa_1.00": float(k100),
            "rise_to_break": float(k050 - k025),
            "rise_to_far": float(k100 - k025),
            "rows": [by_sigma[s] for s in SIGMA_GRID],
        })
    checks = {
        "kappa_rises_to_break": all(
            r["rise_to_break"] >= t["kappa_rise_min"]
            for r in per_seed),
        "kappa_rises_to_far": all(
            r["rise_to_far"] >= t["kappa_rise_min"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(lv) the Luppi prediction as stated: coupling "
                 "rises with loss of attunement",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_shape_verdict(seeds=None):
    """(lvi) The measured shape: coupling dips at the break
    and recovers, and decoupling is not attunement.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
    (a) kappa(0.25) >= 0.80; (b) kappa(0.50) <=
    kappa(0.25) - 0.30; (c) kappa(1.00) >= kappa(0.50)
    + 0.10; (d) at sigma = 0.25 the shuffle null is near
    zero (|mean kappa over 50 shuffles| <= 0.10) and
    separated from kappa(0.25) by >= 0.50. The shuffle
    leaves f unchanged by construction (it permutes F
    entries only), so (d) is the decoupling-is-not-
    attunement check.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        by_sigma = _kappa_by_sigma(seed)
        k025 = by_sigma[SIGMA_ATTUNED]["kappa"]
        k050 = by_sigma[SIGMA_BREAK]["kappa"]
        k100 = by_sigma[SIGMA_FAR]["kappa"]
        null = shuffle_null_row(SIGMA_ATTUNED, seed=seed)
        per_seed.append({
            "seed": int(seed),
            "kappa_0.25": float(k025),
            "kappa_0.50": float(k050),
            "kappa_1.00": float(k100),
            "dip_to_break": float(k025 - k050),
            "recovery_to_far": float(k100 - k050),
            "shuffle_mean": float(null["shuffle_mean"]),
            "shuffle_separation": float(
                k025 - abs(null["shuffle_mean"])),
            "f_at_0.25": float(null["f_mean_pair_concurrence"]),
            "rows": [by_sigma[s] for s in SIGMA_GRID],
        })
    checks = {
        "kappa_attuned_at_least_min": all(
            r["kappa_0.25"] >= t["kappa_attuned_min"]
            for r in per_seed),
        "kappa_dips_at_break": all(
            r["dip_to_break"] >= t["kappa_dip_min"]
            for r in per_seed),
        "kappa_recovers_past_break": all(
            r["recovery_to_far"] >= t["kappa_recovery_min"]
            for r in per_seed),
        "shuffle_null_near_zero": all(
            abs(r["shuffle_mean"]) <= t["shuffle_mean_max"]
            for r in per_seed),
        "shuffle_separated_from_attuned": all(
            r["shuffle_separation"] >= t["shuffle_separation_min"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(lvi) the measured shape: coupling dips at "
                 "the break and recovers, and decoupling is "
                 "not attunement",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def connectome_harmonic_claims():
    """The three connectome-harmonic claims (liv)-(lvi), measured fresh."""
    claim_liv = claim_machinery_verdict()
    claim_lv = claim_luppi_verdict()
    claim_lvi = claim_shape_verdict()
    verdicts = [claim_liv, claim_lv, claim_lvi]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_liv_machinery": claim_liv,
        "claim_lv_luppi": claim_lv,
        "claim_lvi_shape": claim_lvi,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print kappa vs noise, the harmonic diagnostics, the
    shuffle null, and the claims (liv)-(lvi) verdicts."""
    print("Connectome-harmonic -- claims (liv)-(lvi)")
    print()
    verdicts = connectome_harmonic_claims()
    liv = verdicts["claim_liv_machinery"]
    print("kappa vs noise, rho(D), low-2 share (sigma: kappa, "
          "rho(D), low2, f):")
    for r in liv["per_seed"]:
        print(f"  seed {r['seed']}:")
        for row in r["rows"]:
            print(f"    sigma = {row['sigma']:>4}: kappa = "
                  f"{row['kappa']:+.4f}, rho(D) = {row['rho_d']:.4f}, "
                  f"low2 = {row['low2_energy_share_d']:.4f}, f = "
                  f"{row['f_mean_pair_concurrence']:.4f}")
    print(f"claim (liv) verdict: {'PASS' if liv['passed'] else 'FAIL'}")
    print()
    lv = verdicts["claim_lv_luppi"]
    for r in lv["per_seed"]:
        print(f"  seed {r['seed']}: kappa(0.25) = {r['kappa_0.25']:.4f}, "
              f"kappa(0.50) = {r['kappa_0.50']:.4f} "
              f"(rise {r['rise_to_break']:+.4f}), kappa(1.00) = "
              f"{r['kappa_1.00']:.4f} (rise {r['rise_to_far']:+.4f})")
    print(f"claim (lv) verdict: {'PASS' if lv['passed'] else 'FAIL'}")
    print()
    lvi = verdicts["claim_lvi_shape"]
    for r in lvi["per_seed"]:
        print(f"  seed {r['seed']}: kappa(0.25) = {r['kappa_0.25']:.4f}, "
              f"dip to 0.50 = {r['dip_to_break']:.4f}, recovery to "
              f"1.00 = {r['recovery_to_far']:.4f}, shuffle mean = "
              f"{r['shuffle_mean']:+.4f} (separation "
              f"{r['shuffle_separation']:.4f}), f(0.25) = "
              f"{r['f_at_0.25']:.4f} (unchanged by the shuffle)")
    print(f"claim (lvi) verdict: {'PASS' if lvi['passed'] else 'FAIL'}")
    print()
    print(f"{verdicts['n_passed']}/{verdicts['n_claims']} claims passed")


if __name__ == "__main__":
    main()
