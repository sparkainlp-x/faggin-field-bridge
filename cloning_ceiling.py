# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# cloning_ceiling.py
#
# No-cloning / Holevo ceiling for D (v0.15.0, deep-think
# upgrade #7, report.md section 9 rank 7 and section 6).
#
# The ceiling, as theorems (established):
#   - No-cloning (1982): an unknown quantum state cannot
#     be copied. The optimal UNIVERSAL 1 -> 2 cloning
#     fidelity for a qubit is 5/6 (Buzek-Hillery 1996;
#     Werner 1998). The bound is on universal
#     (state-independent) fidelity and on the
#     Haar-average fidelity of any cloner -- NOT on the
#     per-state fidelity of a state-dependent cloner,
#     which legitimately copies its preferred states
#     exactly (Wootters-Zurek CNOT copy: fidelity 1 on
#     basis states, 1/2 on equatorial states, mean 2/3).
#   - Holevo bound: the classical information any
#     measurement extracts from a quantum ensemble is at
#     most the Holevo quantity chi = S(rho_bar) -
#     sum_k p_k S(rho_k). For the thought-pair ensemble
#     {(1/2, |psi_i>), (1/2, |psi_j>)} both members are
#     pure, so chi_ij = S((rho_i + rho_j) / 2).
#   - No-cloning entails the D-concurrence
#     anti-correlation in form: local purity falls as
#     entanglement rises. The exact coefficient is
#     verified in code here, not asserted: for a pure
#     two-qubit state, Tr(rho_A^2) = 1 - C^2 / 2.
#
# The construction (fixed before the pilot; see
# docs/preregistration-v0.15.0.md):
#   - Thought-pair ensemble: the resonance population
#     (empathy_field.resonance_population, 8 agents,
#     noisy copies of the uniform thought at sigma on
#     the bridge grid). Per pair, chi_ij = S((rho_i +
#     rho_j) / 2) exactly (cost.von_neumann_entropy),
#     D_pair = (D_i + D_j) / 2 = D of the average state
#     by linearity, and the accessible information is
#     the mutual information of the bridge's own Born
#     collapse in the 4-concept basis. f at a sigma is
#     the population's mean pairwise concurrence.
#   - Qubit thought for cloning: a one-qubit thought
#     |psi> = a|0> + b|1> (the binary-thought qubit of
#     monogamy.py). The Buzek-Hillery cloner is an
#     explicit 8x8 unitary (two basis images completed
#     to an orthonormal basis via SVD null space);
#     the CNOT copy is the Wootters-Zurek machine.
#   - Classical copy: unity.gaussian_copies -- the
#     model's own "copy" operation, which reads the
#     full classical amplitude vector.
#
# Honesty, stated up front:
#   - This is a SYNTHETIC classical emulation. Nothing
#     here tests consciousness, privacy in a physical
#     system, or quantum mechanics itself. The theorems
#     are established; what is measured is whether the
#     model's states and operations respect them.
#   - D is a projector expectation, not an information
#     quantity in bits. Comparing D <= chi compares a
#     probability with a bit count; both lie in [0, 1]
#     for this ensemble, so the comparison is
#     numerically well-defined, but it is NOT a theorem
#     -- it is the report's prediction, tested as
#     stated. The ceiling that is a theorem, and that
#     binds, is on accessible information (claim
#     (xlvi)), not on D (claim (xlv)).
#   - The classical copy (xlviii) reads the amplitude
#     vector the quantum formalism forbids reading.
#     Its excess over 5/6 is a finding about the
#     representation, not a violation of the theorem:
#     privacy in this model is not enforced by the
#     representation and would have to be enforced by
#     restricting operations.
#
# Pre-registered verdict rules for claims
# (xliv)-(xlviii), written before the evaluation run
# (see docs/preregistration-v0.15.0.md and the
# claim_*_verdict functions):
#   (xliv) Local purity = 1 - C^2/2 within 1e-9 on
#       every pure state in the branch / slide / noisy
#       copies / Haar sets, and |C_Wootters - C_pure|
#       <= 1e-7. (Calibration pilot: identity worst
#       8.88e-16; Wootters-vs-pure worst 1.94e-08.)
#   (xlv) D_pair <= chi_ij for every pair on every
#       seed in {42, 7, 1234, 2026}, AND Spearman(
#       |mean gap|, f) <= -0.90 on every seed.
#       (Calibration pilot: the ceiling FAILS -- worst
#       per-pair chi - D = -1.0000 at sigma = 0 on
#       both seeds, negative at every sigma; the gap
#       magnitude DOES shrink with f, Spearman
#       -1.0000 / -0.9643. D approaches chi from
#       ABOVE, not below.)
#   (xlvi) Born-collapse accessible information
#       I <= chi + 1e-9 for every pair on every seed.
#       (Calibration pilot: max(I - chi) = -3.20e-16
#       at sigma = 0, -0.049 / -0.122 at sigma = 1.0.)
#   (xlvii) Buzek-Hillery fidelity = 5/6 within 1e-9
#       for every state on the Bloch grid and the 6
#       Pauli eigenstates, both clones; CNOT mean
#       fidelity over the Pauli states = 2/3 within
#       1e-9 and Bloch-grid mean <= 5/6. CNOT max
#       fidelity is REPORTED, not gated.
#       (Calibration pilot: BH min = max = mean =
#       0.833333; CNOT Pauli mean 0.6667, grid mean
#       0.6389, grid max 0.8472, Pauli max 1.0000.)
#   (xlviii) The blanket prediction over ALL copy
#       operations: the (xlvii) gates PLUS the
#       classical copy (5 copies, sigma grid, every
#       seed) with mean fidelity <= 5/6 at every
#       sigma. (Calibration pilot: FAILS -- classical
#       copy exceeds 5/6 at every sigma <= 0.25:
#       1.0000, 0.9998-0.9999, 0.9945-0.9962,
#       0.9775-0.9841, 0.8540-0.8644; crossing sigma*
#       in (0.25, 0.50).)

"""No-cloning / Holevo ceiling for D: claims (xliv)-(xlviii)."""

import math

import numpy as np

import bridge
import cost
import empathy_field as ef
import observer_cycle as oc
import self_knowing as sk
import thought
import thought_entanglement as te
import unity

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
# docs/preregistration-v0.15.0.md; never moved after the run).
# ---------------------------------------------------------------------------

# Claim (xliv): local-purity identity tolerance, and the
# Wootters-concurrence numerical floor.
PURITY_TOL = 1e-9
WOOTTERS_TOL = 1e-7

# Claim (xlv): D <= chi is checked with a float-noise
# tolerance of 1e-9 (the measured violations are >= 0.27,
# so the tolerance cannot change the verdict); the gap
# magnitude must shrink with f at Spearman <= -0.90.
D_CHI_TOL = 1e-9
SPEARMAN_ABS_GAP_MAX = -0.90

# Claim (xlvi): accessible information <= chi + this.
HOLEVO_TOL = 1e-9

# Claim (xlvii): Buzek-Hillery exactness, basis-image
# orthonormality, CNOT Pauli-mean exactness.
BH_FIDELITY_TOL = 1e-9
BH_ORTHONORMALITY_TOL = 1e-12
CNOT_PAULI_MEAN_TOL = 1e-9

# Claims (xlvii)-(xlviii): the optimal universal 1 -> 2
# cloning fidelity for a qubit (Buzek-Hillery 1996).
CLONING_BOUND = 5.0 / 6.0

# Construction constants.
N_AGENTS = 8
N_COPIES = 5
N_HAAR = 200
HAAR_SEED = 42
SIGMA_GRID = te.SIGMA_GRID
# Bloch grid: 12 thetas (uniform in cos theta, poles
# excluded) x 12 phis = 144 states, deterministic.
BLOCH_N_THETA = 12
BLOCH_N_PHI = 12
# Classical-copy crossing search: 0.01 grid from 0.25
# to 0.50, 20 copies per sigma.
CROSSING_LO = 0.25
CROSSING_HI = 0.50
CROSSING_STEP = 0.01
CROSSING_N_COPIES = 20


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("PURITY_TOL", PURITY_TOL),
        ("WOOTTERS_TOL", WOOTTERS_TOL),
        ("D_CHI_TOL", D_CHI_TOL),
        ("SPEARMAN_ABS_GAP_MAX", SPEARMAN_ABS_GAP_MAX),
        ("HOLEVO_TOL", HOLEVO_TOL),
        ("BH_FIDELITY_TOL", BH_FIDELITY_TOL),
        ("BH_ORTHONORMALITY_TOL", BH_ORTHONORMALITY_TOL),
        ("CNOT_PAULI_MEAN_TOL", CNOT_PAULI_MEAN_TOL),
        ("CLONING_BOUND", CLONING_BOUND),
    ) if value is None]
    if missing:
        raise ValueError(
            "cloning-ceiling thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.15.0.md)")
    return {
        "purity_tol": float(PURITY_TOL),
        "wootters_tol": float(WOOTTERS_TOL),
        "d_chi_tol": float(D_CHI_TOL),
        "spearman_abs_gap_max": float(SPEARMAN_ABS_GAP_MAX),
        "holevo_tol": float(HOLEVO_TOL),
        "bh_fidelity_tol": float(BH_FIDELITY_TOL),
        "bh_orthonormality_tol": float(BH_ORTHONORMALITY_TOL),
        "cnot_pauli_mean_tol": float(CNOT_PAULI_MEAN_TOL),
        "cloning_bound": float(CLONING_BOUND),
    }


# ---------------------------------------------------------------------------
# (xliv) Local purity
# ---------------------------------------------------------------------------

def local_purity(rho):
    """Tr(rho_A^2): purity of the reduced one-qubit state.

    rho is a 4x4 two-qubit density matrix; qubit 0 is
    kept, qubit 1 traced out (thought_entanglement
    convention). Pure product state: 1. Bell state: 1/2.
    """
    red = te.reduced_density_matrix(np.asarray(rho, dtype=complex),
                                    keep=0)
    return float(np.real(np.trace(red @ red)))


def purity_identity_error(psi):
    """|Tr(rho_A^2) - (1 - C^2/2)| for a pure thought-pair
    state, with C the exact pure-state concurrence
    2|ad - bc|."""
    psi = np.asarray(psi, dtype=complex)
    rho = te.density_matrix(psi)
    c = te.concurrence_pure(psi)
    return float(abs(local_purity(rho) - (1.0 - c * c / 2.0)))


def haar_pure_states(n=N_HAAR, seed=HAAR_SEED):
    """n Haar-random pure two-qubit states (complex
    Gaussian components, normalized), seeded."""
    rng = np.random.default_rng(int(seed))
    out = []
    for _ in range(int(n)):
        z = (rng.standard_normal(4) + 1j * rng.standard_normal(4)) \
            / math.sqrt(2.0)
        out.append(z / np.linalg.norm(z))
    return out


def purity_sweep(seeds=None):
    """The local-purity identity over every state family.

    Generalized-Bell branch (7 a-values), the slide (7
    thetas), noisy Bell copies (5 copies x sigma grid x
    every seed), and 200 Haar-random pure states (seed
    42). Returns the worst identity error (exact pure
    concurrence), the worst |C_Wootters - C_pure|, and
    the per-family worst errors.
    """
    families = {}
    worst = 0.0
    worst_cc = 0.0

    def check(psi, family):
        nonlocal worst, worst_cc
        err = purity_identity_error(psi)
        rho = te.density_matrix(np.asarray(psi, dtype=complex))
        cc = abs(te.concurrence(rho) - te.concurrence_pure(psi))
        worst = max(worst, err)
        worst_cc = max(worst_cc, cc)
        families[family] = max(families.get(family, 0.0), err)

    for a in oc.BELL_BRANCH_GRID:
        check(oc.generalized_bell(a), "generalized_bell_branch")
    for t in oc.SLIDE_THETAS:
        check(oc.slide_state(t), "slide")
    for seed in (ALL_SEEDS if seeds is None else seeds):
        for sigma in SIGMA_GRID:
            for v in te.noisy_bell_copies(sigma, N_COPIES, seed):
                check(np.asarray(v, dtype=complex),
                      f"noisy_bell_seed_{seed}")
    for z in haar_pure_states():
        check(z, "haar_random")
    return {
        "worst_identity_error": float(worst),
        "worst_wootters_vs_pure": float(worst_cc),
        "families": {k: float(v) for k, v in families.items()},
    }


# ---------------------------------------------------------------------------
# (xlv)-(xlvi) Thought-pair ensemble: Holevo chi, D, accessible info
# ---------------------------------------------------------------------------

def pair_holevo_chi(psi_i, psi_j):
    """chi_ij = S((rho_i + rho_j) / 2): the Holevo quantity
    of the two-state thought-pair ensemble.

    Both members are pure, so chi is the von Neumann
    entropy of the average state. 0 when the thoughts
    are identical, 1 bit when they are orthogonal.
    """
    rho_bar = 0.5 * (te.density_matrix(psi_i)
                     + te.density_matrix(psi_j))
    return float(cost.von_neumann_entropy(rho_bar))


def pair_holevo_chi_analytic(psi_i, psi_j):
    """chi_ij from the overlap alone: H2((1 + s) / 2) with
    s = |<psi_i|psi_j>| = sqrt(R_ij).

    The average of two pure states has eigenvalues
    (1 +- s) / 2. Cross-check for pair_holevo_chi in
    the tests.
    """
    s = math.sqrt(ef.overlap_squared(psi_i, psi_j))
    p = (1.0 + s) / 2.0
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return float(-p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p))


def pair_accessible_information(psi_i, psi_j):
    """I(index; outcome) for the bridge's own measurement:
    the Born collapse in the 4-concept basis.

    I = H((p_i + p_j) / 2) - (H(p_i) + H(p_j)) / 2 with
    p_i(k) = |<k|psi_i>|^2. Holevo's theorem requires
    I <= chi_ij for every measurement; this is the
    measurement the bridge actually performs.
    """
    p_i = np.abs(np.asarray(psi_i, dtype=complex)) ** 2
    p_j = np.abs(np.asarray(psi_j, dtype=complex)) ** 2
    mix = 0.5 * (p_i + p_j)
    return float(cost.shannon_entropy(mix) - 0.5 * (
        cost.shannon_entropy(p_i) + cost.shannon_entropy(p_j)))


def pair_ensemble_rows(sigma, seed):
    """One row per pair (i, j) of the resonance population
    at (sigma, seed): chi, D_pair, accessible information,
    and the gap chi - D."""
    states = ef.resonance_population(sigma, N_AGENTS, seed)
    rows = []
    for i in range(len(states)):
        for j in range(i + 1, len(states)):
            chi = pair_holevo_chi(states[i], states[j])
            d_pair = 0.5 * (sk.self_knowing_factor(states[i])
                            + sk.self_knowing_factor(states[j]))
            acc = pair_accessible_information(states[i],
                                              states[j])
            rows.append({
                "sigma": float(sigma),
                "i": i,
                "j": j,
                "resonance": ef.overlap_squared(states[i],
                                                states[j]),
                "holevo_chi_bits": chi,
                "d_pair": float(d_pair),
                "gap_chi_minus_d": float(chi - d_pair),
                "accessible_information_bits": acc,
                "accessible_minus_chi_bits": float(acc - chi),
            })
    return rows


def ensemble_sweep(seed):
    """Per-sigma aggregates of the thought-pair ensemble
    for one seed: mean D, mean chi, mean gap, mean |gap|,
    worst (smallest) per-pair chi - D, max(I - chi), and
    f = mean pairwise concurrence of the population."""
    rows = []
    for sigma in SIGMA_GRID:
        pairs = pair_ensemble_rows(sigma, seed)
        states = ef.resonance_population(sigma, N_AGENTS, seed)
        f = ef.empathy_fraction(states)
        gaps = [p["gap_chi_minus_d"] for p in pairs]
        accs = [p["accessible_information_bits"] for p in pairs]
        chis = [p["holevo_chi_bits"] for p in pairs]
        ds = [p["d_pair"] for p in pairs]
        mean_chi = float(np.mean(chis))
        mean_i = float(np.mean(accs))
        rows.append({
            "seed": int(seed),
            "sigma": float(sigma),
            "f_mean_pair_concurrence": float(f),
            "mean_d": float(np.mean(ds)),
            "mean_chi_bits": mean_chi,
            "mean_gap_bits": float(np.mean(gaps)),
            "mean_abs_gap_bits": float(np.mean([abs(g)
                                                for g in gaps])),
            "min_gap_bits": float(min(gaps)),
            "mean_accessible_information_bits": mean_i,
            "mean_accessible_over_chi": (
                float(mean_i / mean_chi) if mean_chi > 0.0 else None),
            "max_accessible_minus_chi_bits": float(max(
                p["accessible_minus_chi_bits"] for p in pairs)),
            "n_pairs": len(pairs),
        })
    return rows


# ---------------------------------------------------------------------------
# (xlvii)-(xlviii) Copy operations: Buzek-Hillery, CNOT, classical
# ---------------------------------------------------------------------------

def bh_basis_images():
    """The Buzek-Hillery basis images (qubit order A, B, C;
    A most significant bit).

    |0>|0>|0> -> sqrt(2/3)|000> + sqrt(1/6)|011>
        + sqrt(1/6)|101>
    |1>|0>|0> -> sqrt(2/3)|111> + sqrt(1/6)|010>
        + sqrt(1/6)|100>
    (Buzek & Hillery, Phys. Rev. A 54, 1844, 1996.)
    The two images are orthonormal; the full unitary is
    built from them in bh_unitary().
    """
    s23 = math.sqrt(2.0 / 3.0)
    s16 = math.sqrt(1.0 / 6.0)
    img0 = np.zeros(8, dtype=complex)
    img0[0b000] = s23
    img0[0b011] = s16
    img0[0b101] = s16
    img1 = np.zeros(8, dtype=complex)
    img1[0b111] = s23
    img1[0b010] = s16
    img1[0b100] = s16
    return img0, img1


def bh_unitary():
    """The full 8x8 Buzek-Hillery unitary.

    Columns 0 and 4 are the basis images (inputs
    |0>|0>|0> and |1>|0>|0>); the other six columns
    complete them to an orthonormal basis via the SVD
    null space, so U^dagger U = I exactly.
    """
    img0, img1 = bh_basis_images()
    # Null space of the two images: SVD of the 2x8 row
    # matrix [img0-dagger; img1-dagger] (full_matrices
    # gives vh 8x8); its last six rows are orthogonal
    # to both images, so their conjugates complete the
    # basis.
    rows = np.vstack([img0.conj(), img1.conj()])
    _, _, vh = np.linalg.svd(rows, full_matrices=True)
    null = vh[2:].conj().T
    u = np.zeros((8, 8), dtype=complex)
    u[:, 0] = img0
    u[:, 4] = img1
    cols = [c for c in range(8) if c not in (0, 4)]
    for k, c in enumerate(cols):
        u[:, c] = null[:, k]
    return u


def _clone_reduced_state(out, keep):
    """Reduced 2x2 state of one qubit of a 3-qubit output
    vector (qubit order A, B, C)."""
    t = np.asarray(out, dtype=complex).reshape(2, 2, 2)
    if keep == 0:
        rho = np.tensordot(t, t.conj(), axes=([1, 2], [1, 2]))
    elif keep == 1:
        rho = np.tensordot(t, t.conj(), axes=([0, 2], [0, 2]))
    elif keep == 2:
        rho = np.tensordot(t, t.conj(), axes=([0, 1], [0, 1]))
    else:
        raise ValueError("keep must be 0, 1, or 2")
    return rho.reshape(2, 2)


def clone_fidelity(psi, rho):
    """Fidelity <psi|rho|psi> of a clone's reduced state
    with the original qubit thought."""
    psi = np.asarray(psi, dtype=complex)
    return float(np.real(psi.conj() @ np.asarray(rho) @ psi))


def bh_clone(psi):
    """Buzek-Hillery clone: the 8-dim output of U on
    |psi>_A |0>_B |0>_C."""
    psi = np.asarray(psi, dtype=complex)
    if psi.shape != (2,):
        raise ValueError("bh_clone needs a one-qubit thought")
    u = bh_unitary()
    vec = np.zeros(8, dtype=complex)
    vec[0] = psi[0]
    vec[4] = psi[1]
    return u @ vec


def cnot_clone(psi):
    """CNOT (Wootters-Zurek) copy: |psi>_A |0>_B -> the
    4-dim output a|00> + b|11>."""
    psi = np.asarray(psi, dtype=complex)
    if psi.shape != (2,):
        raise ValueError("cnot_clone needs a one-qubit thought")
    cnot = np.array([[1, 0, 0, 0], [0, 1, 0, 0],
                     [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    return cnot @ np.kron(psi, np.array([1.0, 0.0], dtype=complex))


def bloch_grid_states(n_theta=BLOCH_N_THETA, n_phi=BLOCH_N_PHI):
    """Deterministic Bloch-sphere grid: thetas uniform in
    cos(theta) (poles excluded), phis uniform. Returns
    n_theta * n_phi one-qubit states."""
    cos_thetas = np.linspace(-1.0, 1.0, int(n_theta) + 2)[1:-1]
    phis = np.linspace(0.0, 2.0 * math.pi, int(n_phi),
                       endpoint=False)
    states = []
    for cos_t in cos_thetas:
        theta = math.acos(float(cos_t))
        for phi in phis:
            states.append(np.array(
                [math.cos(theta / 2.0),
                 math.sin(theta / 2.0)
                 * complex(math.cos(float(phi)),
                           math.sin(float(phi)))],
                dtype=complex))
    return states


def pauli_eigenstates():
    """The 6 Pauli eigenstates: +-z, +-x, +-y."""
    s = 1.0 / math.sqrt(2.0)
    return [
        np.array([1.0, 0.0], dtype=complex),
        np.array([0.0, 1.0], dtype=complex),
        np.array([s, s], dtype=complex),
        np.array([s, -s], dtype=complex),
        np.array([s, 1j * s], dtype=complex),
        np.array([s, -1j * s], dtype=complex),
    ]


def cloning_sweep():
    """Fidelities of the unitary cloners on the Bloch grid
    and the Pauli states."""
    bh_grid, cnot_grid = [], []
    for psi in bloch_grid_states():
        out = bh_clone(psi)
        for keep in (0, 1):
            bh_grid.append(clone_fidelity(
                psi, _clone_reduced_state(out, keep)))
        out2 = cnot_clone(psi)
        rho2 = te.density_matrix(out2)
        for keep in (0, 1):
            cnot_grid.append(clone_fidelity(
                psi, te.reduced_density_matrix(rho2, keep=keep)))
    bh_pauli, cnot_pauli = [], []
    for psi in pauli_eigenstates():
        out = bh_clone(psi)
        for keep in (0, 1):
            bh_pauli.append(clone_fidelity(
                psi, _clone_reduced_state(out, keep)))
        out2 = cnot_clone(psi)
        rho2 = te.density_matrix(out2)
        for keep in (0, 1):
            cnot_pauli.append(clone_fidelity(
                psi, te.reduced_density_matrix(rho2, keep=keep)))
    img0, img1 = bh_basis_images()
    return {
        "bh_grid_fidelities": bh_grid,
        "bh_grid_min": float(min(bh_grid)),
        "bh_grid_max": float(max(bh_grid)),
        "bh_grid_mean": float(np.mean(bh_grid)),
        "bh_pauli_fidelities": bh_pauli,
        "bh_pauli_min": float(min(bh_pauli)),
        "bh_pauli_max": float(max(bh_pauli)),
        "bh_images_overlap": float(abs(np.vdot(img0, img1))),
        "bh_images_norms": (float(np.linalg.norm(img0)),
                            float(np.linalg.norm(img1))),
        "cnot_grid_fidelities": cnot_grid,
        "cnot_grid_min": float(min(cnot_grid)),
        "cnot_grid_max": float(max(cnot_grid)),
        "cnot_grid_mean": float(np.mean(cnot_grid)),
        "cnot_pauli_fidelities": cnot_pauli,
        "cnot_pauli_min": float(min(cnot_pauli)),
        "cnot_pauli_max": float(max(cnot_pauli)),
        "cnot_pauli_mean": float(np.mean(cnot_pauli)),
    }


# ---------------------------------------------------------------------------
# (xlviii) Classical copy
# ---------------------------------------------------------------------------

def classical_copy_fidelity(sigma, seed, n_copies=N_COPIES):
    """Mean fidelity |<psi|copy>|^2 of the model's
    classical copies of the uniform thought at sigma:
    unity.gaussian_copies reads the full amplitude
    vector, adds Gaussian noise, and renormalizes.
    At sigma = 0 the copy is exact (fidelity 1)."""
    base = np.real(thought.uniform_thought())
    copies = unity.gaussian_copies(base, sigma, n_copies, seed)
    fids = [float(abs(np.vdot(base, c)) ** 2) for c in copies]
    return {
        "sigma": float(sigma),
        "seed": int(seed),
        "mean_fidelity": float(np.mean(fids)),
        "min_fidelity": float(min(fids)),
        "max_fidelity": float(max(fids)),
    }


def classical_copy_sweep(seed):
    """Mean classical-copy fidelity per sigma, one seed."""
    return [classical_copy_fidelity(sigma, seed)
            for sigma in SIGMA_GRID]


def classical_copy_crossing(seed):
    """The sigma* bracket where the classical copy's mean
    fidelity falls below the 5/6 cloning bound: the
    first sigma on a 0.01 grid from 0.25 to 0.50 (20
    copies) with mean fidelity < 5/6, and the grid
    point just before it. None when no crossing is
    found in the bracket (reported, not gated)."""
    prev = None
    for i in range(int(round((CROSSING_HI - CROSSING_LO)
                             / CROSSING_STEP)) + 1):
        sigma = CROSSING_LO + i * CROSSING_STEP
        row = classical_copy_fidelity(sigma, seed,
                                      CROSSING_N_COPIES)
        if row["mean_fidelity"] < CLONING_BOUND:
            return {
                "seed": int(seed),
                "sigma_below": float(sigma),
                "fidelity_below": row["mean_fidelity"],
                "sigma_above": (float(prev["sigma"])
                                if prev is not None else None),
                "fidelity_above": (float(prev["mean_fidelity"])
                                   if prev is not None else None),
            }
        prev = row
    return {"seed": int(seed), "sigma_below": None,
            "fidelity_below": None, "sigma_above": None,
            "fidelity_above": None}


# ---------------------------------------------------------------------------
# Claim verdicts (xliv)-(xlviii)
# ---------------------------------------------------------------------------

def claim_local_purity_verdict(seeds=None):
    """(xliv) Local-purity identity: Tr(rho_A^2) = 1 - C^2/2.

    PASS iff, on every pure state in the branch / slide /
    noisy copies / Haar sets, the identity holds within
    PURITY_TOL (1e-9) with the exact pure-state
    concurrence, and the Wootters concurrence agrees
    with the exact pure form within WOOTTERS_TOL
    (1e-7).
    """
    t = _thresholds()
    sweep = purity_sweep(seeds)
    checks = {
        "identity_exact": (
            sweep["worst_identity_error"] <= t["purity_tol"]),
        "wootters_agrees_with_pure": (
            sweep["worst_wootters_vs_pure"] <= t["wootters_tol"]),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xliv) local purity = 1 - C^2/2 (the exact "
                 "no-cloning coefficient)",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "worst_identity_error":
            sweep["worst_identity_error"],
        "worst_wootters_vs_pure":
            sweep["worst_wootters_vs_pure"],
        "families": sweep["families"],
    }


def claim_holevo_ceiling_verdict(seeds=None):
    """(xlv) Holevo ceiling D <= chi on the thought-pair
    ensemble.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
    (a) D_pair <= chi_ij for every pair (min gap >=
    -D_CHI_TOL), and (b) the gap magnitude shrinks as
    f rises: Spearman(|mean gap|, f) <= -0.90 across
    the sigma grid. Calibration: (a) fails (worst
    per-pair chi - D = -1.0000 at sigma = 0 on both
    seeds); (b) passes (-1.0000, -0.9643). D
    approaches chi from ABOVE, not below.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        rows = ensemble_sweep(seed)
        min_gap = min(r["min_gap_bits"] for r in rows)
        abs_gaps = [r["mean_abs_gap_bits"] for r in rows]
        fs = [r["f_mean_pair_concurrence"] for r in rows]
        per_seed.append({
            "seed": int(seed),
            "min_gap_bits": float(min_gap),
            "spearman_abs_gap_f": sk.spearman(abs_gaps, fs),
            "pearson_gap_f": sk.pearson(
                [r["mean_gap_bits"] for r in rows], fs),
            "rows": rows,
        })
    checks = {
        "d_at_most_chi_every_pair": all(
            r["min_gap_bits"] >= -t["d_chi_tol"] for r in per_seed),
        "abs_gap_shrinks_with_f": all(
            r["spearman_abs_gap_f"] <= t["spearman_abs_gap_max"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xlv) Holevo ceiling D <= chi on the "
                 "thought-pair ensemble",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_accessible_information_verdict(seeds=None):
    """(xlvi) Holevo bound on accessible information.

    PASS iff, for EVERY pair on EVERY seed in
    {42, 7, 1234, 2026}, the Born-collapse accessible
    information satisfies I <= chi + HOLEVO_TOL
    (1e-9). Calibration: max(I - chi) = -3.20e-16 at
    sigma = 0, -0.049 / -0.122 at sigma = 1.0.
    """
    t = _thresholds()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        rows = ensemble_sweep(seed)
        per_seed.append({
            "seed": int(seed),
            "max_accessible_minus_chi_bits": float(max(
                r["max_accessible_minus_chi_bits"] for r in rows)),
            "rows": rows,
        })
    checks = {
        "accessible_at_most_chi_every_pair": all(
            r["max_accessible_minus_chi_bits"] <= t["holevo_tol"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xlvi) Holevo bound on accessible "
                 "information: I <= chi",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_unitary_cloning_verdict():
    """(xlvii) Optimal-cloning bound for unitary copy
    operations.

    PASS iff: the Buzek-Hillery per-state fidelity is
    5/6 within BH_FIDELITY_TOL (1e-9) for every state
    on the Bloch grid and the 6 Pauli eigenstates,
    both clones; the BH basis images are orthonormal
    (overlap <= 1e-12); the CNOT mean fidelity over
    the Pauli states is 2/3 within 1e-9 (hence <=
    5/6); and the CNOT Bloch-grid mean is <= 5/6.
    The CNOT max fidelity (1.0000 on basis states)
    is reported, not gated: the 5/6 bound is on
    universal / average fidelity.
    """
    t = _thresholds()
    sweep = cloning_sweep()
    checks = {
        "bh_grid_fidelity_is_5_6": (
            abs(sweep["bh_grid_min"] - t["cloning_bound"])
            <= t["bh_fidelity_tol"]
            and abs(sweep["bh_grid_max"] - t["cloning_bound"])
            <= t["bh_fidelity_tol"]),
        "bh_pauli_fidelity_is_5_6": (
            abs(sweep["bh_pauli_min"] - t["cloning_bound"])
            <= t["bh_fidelity_tol"]
            and abs(sweep["bh_pauli_max"] - t["cloning_bound"])
            <= t["bh_fidelity_tol"]),
        "bh_images_orthonormal": (
            sweep["bh_images_overlap"]
            <= t["bh_orthonormality_tol"]),
        "cnot_pauli_mean_is_2_3": (
            abs(sweep["cnot_pauli_mean"] - 2.0 / 3.0)
            <= t["cnot_pauli_mean_tol"]),
        "cnot_grid_mean_at_most_bound": (
            sweep["cnot_grid_mean"] <= t["cloning_bound"]),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xlvii) optimal-cloning bound for unitary "
                 "copy operations: BH = 5/6, CNOT mean 2/3",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "bh_grid_min": sweep["bh_grid_min"],
        "bh_grid_max": sweep["bh_grid_max"],
        "bh_grid_mean": sweep["bh_grid_mean"],
        "bh_pauli_min": sweep["bh_pauli_min"],
        "bh_pauli_max": sweep["bh_pauli_max"],
        "bh_images_overlap": sweep["bh_images_overlap"],
        "cnot_grid_min": sweep["cnot_grid_min"],
        "cnot_grid_max": sweep["cnot_grid_max"],
        "cnot_grid_mean": sweep["cnot_grid_mean"],
        "cnot_pauli_min": sweep["cnot_pauli_min"],
        "cnot_pauli_max": sweep["cnot_pauli_max"],
        "cnot_pauli_mean": sweep["cnot_pauli_mean"],
    }


def claim_blanket_cloning_verdict(seeds=None):
    """(xlviii) The blanket prediction over ALL copy
    operations in the model.

    PASS iff the (xlvii) unitary gates hold AND the
    classical copy (unity.gaussian_copies, 5 copies,
    sigma grid, every seed in {42, 7, 1234, 2026})
    has mean fidelity <= 5/6 at every sigma. The
    crossing sigma* per seed (first 0.01-grid sigma
    in [0.25, 0.50] where the 20-copy mean fidelity
    falls below 5/6) is reported, not gated.
    Calibration: FAILS -- the classical copy exceeds
    5/6 at every sigma <= 0.25 (1.0000 at sigma = 0;
    0.8540-0.8644 at sigma = 0.25).
    """
    t = _thresholds()
    unitary = claim_unitary_cloning_verdict()
    per_seed = []
    for seed in (ALL_SEEDS if seeds is None else seeds):
        rows = classical_copy_sweep(seed)
        per_seed.append({
            "seed": int(seed),
            "max_mean_fidelity": float(max(
                r["mean_fidelity"] for r in rows)),
            "crossing": classical_copy_crossing(seed),
            "rows": rows,
        })
    checks = {
        "unitary_cloners_respect_bound": bool(unitary["passed"]),
        "classical_copy_respects_bound": all(
            r["max_mean_fidelity"] <= t["cloning_bound"]
            for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xlviii) blanket prediction: no copy "
                 "operation in the model exceeds 5/6",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "unitary_verdict": unitary,
        "per_seed": per_seed,
    }


def cloning_ceiling_claims():
    """The five no-cloning / Holevo-ceiling claims
    (xliv)-(xlviii), measured fresh."""
    claim_xliv = claim_local_purity_verdict()
    claim_xlv = claim_holevo_ceiling_verdict()
    claim_xlvi = claim_accessible_information_verdict()
    claim_xlvii = claim_unitary_cloning_verdict()
    claim_xlviii = claim_blanket_cloning_verdict()
    verdicts = [claim_xliv, claim_xlv, claim_xlvi,
                claim_xlvii, claim_xlviii]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_xliv_local_purity": claim_xliv,
        "claim_xlv_holevo_ceiling": claim_xlv,
        "claim_xlvi_accessible_information": claim_xlvi,
        "claim_xlvii_unitary_cloning": claim_xlvii,
        "claim_xlviii_blanket_cloning": claim_xlviii,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the purity identity, the thought-pair
    ensemble, the cloners, the classical copy, and the
    claims (xliv)-(xlviii) verdicts."""
    print("No-cloning / Holevo ceiling -- claims (xliv)-(xlviii)")
    print()
    verdicts = cloning_ceiling_claims()
    xliv = verdicts["claim_xliv_local_purity"]
    print(f"local purity: worst |purity - (1 - C^2/2)| = "
          f"{xliv['worst_identity_error']:.2e}, worst "
          f"|C_Wootters - C_pure| = "
          f"{xliv['worst_wootters_vs_pure']:.2e}")
    print(f"claim (xliv) verdict: {'PASS' if xliv['passed'] else 'FAIL'}")
    print()
    xlv = verdicts["claim_xlv_holevo_ceiling"]
    print("Thought-pair ensemble (mean D, mean chi, mean gap, "
          "min gap, f) per sigma:")
    for r in xlv["per_seed"]:
        print(f"  seed {r['seed']}: min(chi - D) = "
              f"{r['min_gap_bits']:+.4f}, "
              f"Spearman(|gap|, f) = "
              f"{r['spearman_abs_gap_f']:.4f}, "
              f"Pearson(gap, f) = {r['pearson_gap_f']:.4f}")
        for row in r["rows"]:
            print(f"    sigma = {row['sigma']:>4}: f = "
                  f"{row['f_mean_pair_concurrence']:.4f}, mean D = "
                  f"{row['mean_d']:.4f}, mean chi = "
                  f"{row['mean_chi_bits']:.4f}, mean gap = "
                  f"{row['mean_gap_bits']:+.4f}, min gap = "
                  f"{row['min_gap_bits']:+.4f}")
    print(f"claim (xlv) verdict: {'PASS' if xlv['passed'] else 'FAIL'}")
    print()
    xlvi = verdicts["claim_xlvi_accessible_information"]
    for r in xlvi["per_seed"]:
        print(f"  seed {r['seed']}: max(I - chi) = "
              f"{r['max_accessible_minus_chi_bits']:+.2e}")
    print(f"claim (xlvi) verdict: "
          f"{'PASS' if xlvi['passed'] else 'FAIL'}")
    print()
    xlvii = verdicts["claim_xlvii_unitary_cloning"]
    print(f"Buzek-Hillery fidelity: grid "
          f"[{xlvii['bh_grid_min']:.6f}, {xlvii['bh_grid_max']:.6f}] "
          f"(mean {xlvii['bh_grid_mean']:.6f}), Pauli "
          f"[{xlvii['bh_pauli_min']:.6f}, "
          f"{xlvii['bh_pauli_max']:.6f}], images overlap = "
          f"{xlvii['bh_images_overlap']:.2e}")
    print(f"CNOT fidelity: Pauli mean = "
          f"{xlvii['cnot_pauli_mean']:.6f} (min "
          f"{xlvii['cnot_pauli_min']:.4f}, max "
          f"{xlvii['cnot_pauli_max']:.4f}), grid mean = "
          f"{xlvii['cnot_grid_mean']:.6f}, grid max = "
          f"{xlvii['cnot_grid_max']:.6f} (reported, not gated)")
    print(f"claim (xlvii) verdict: "
          f"{'PASS' if xlvii['passed'] else 'FAIL'}")
    print()
    xlviii = verdicts["claim_xlviii_blanket_cloning"]
    for r in xlviii["per_seed"]:
        c = r["crossing"]
        if c["sigma_above"] is None:
            bracket = (f"already below 5/6 at "
                       f"{c['sigma_below']:.2f} "
                       f"(fidelity {c['fidelity_below']:.4f})")
        else:
            bracket = (f"sigma* in ({c['sigma_above']:.2f}, "
                       f"{c['sigma_below']:.2f}] with fidelities "
                       f"{c['fidelity_above']:.4f} -> "
                       f"{c['fidelity_below']:.4f}")
        print(f"  seed {r['seed']}: max mean classical-copy "
              f"fidelity = {r['max_mean_fidelity']:.4f}, crossing "
              f"{bracket}")
        print("    sigma: " + ", ".join(
            f"{row['sigma']}: {row['mean_fidelity']:.4f}"
            for row in r["rows"]))
    print(f"claim (xlviii) verdict: "
          f"{'PASS' if xlviii['passed'] else 'FAIL'}")
    print()
    print(f"{verdicts['n_passed']}/{verdicts['n_claims']} claims passed")


if __name__ == "__main__":
    main()
