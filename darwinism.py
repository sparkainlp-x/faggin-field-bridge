# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only

"""Quantum-Darwinism redundancy plateau (v0.8.0).

An environment of N fragments redundantly encodes the
system's pointer-state information. The system S is a
thought in a superposition of two pointer states; each
environment fragment is a qubit that records which pointer
state the system is in (a CNOT-like branching interaction).
For a fragment F of m environment qubits:

  I(S:F)  = H(rho_S) + H(rho_F) - H(rho_SF)  (quantum mutual
            information, exact von Neumann entropies)
  chi     = H(rho_F) - sum_k p_k H(rho_F|k)  (Holevo quantity
            of the ensemble obtained by measuring S in the
            pointer basis: the classical information a
            fragment carries about S)
  discord = I - chi  (the quantum part of the correlations)
  R_delta = N / m*   (redundancy: the number of disjoint
            fragments of size m* that fit in the environment,
            where m* is the smallest fragment size with
            I(S:F) >= (1 - delta) H_S)

Two branching families:
  hard: the environment record states are orthogonal
    (|e_0> = |0>, |e_1> = |1>), so one environment qubit
    already carries the full classical bit.
  soft: the record states overlap (<e_0|e_1> = c > 0), so
    a fragment needs several qubits to capture the bit,
    and the discord rises gradually as m -> N.

Einselection is a dephasing channel in the pointer basis
(strength p): p = 0 is the pure branching state, p = 1
is the pointer mixture. The dephasing kills the quantum
excess (discord at m = N) while the classical plateau
(I = H_S for m < N) is p-independent: the classical
information is robust, the quantum information fragile.

Implementation note: the fragment state rho_SF is built
DIRECTLY from the branching construction (closed form),
not by partial-tracing the full 2^(N+n_sys)-dim density
matrix: rho_SF = (1/2) sum_k |p_k><p_k| (x) |e_k^m><e_k^m|
+ ((1-p)/2) c^(N-m) (|p_0><p_1| (x) |e_0^m><e_1^m| + h.c.),
where c = <e_0|e_1>. The fragment state is exactly rank
2 (it lives in the span of the two branch vectors), so
its entropies have the closed form in
analytic_fragment_values, and plateau_sweep evaluates
that form directly: a 4096-dim eigvalsh would compute
the same two nonzero eigenvalues at O(d^3) cost. The
general partial trace (partial_trace_general) and the
full numeric fragment_quantities are kept and used in
the tests to cross-check the closed form on small N and
on a subset of (m, phi, p) at N = 10 (they agree to
1e-9 hard, 2e-15 soft). The noisy-copy sweep has no
closed form -- the copies are genuinely high-rank -- so
it uses the full numeric path throughout.

Honesty, stated up front:
  - Quantum Darwinism is an ESTABLISHED theory (Zurek
    2009) verified in superconducting circuits in 2025
    (Zhu et al., arXiv:2504.00781 / Science Advances
    2025: 12 qubits, mutual information saturates at
    H_S, discord -> 0 for small fragments), and emergent
    classicality is a theorem (Brandao et al., Quantum
    2021). What is measured here is the same structure
    in the model's own states, computed exactly with
    NumPy. The system and environment are defined in
    code, not physical systems. Classical emulation
    throughout. Faggin's metaphysics is interpretive
    and is NOT tested here.
  - The binary-thought embedding is the SAME definition
    as monogamy.py (|0> -> |00> attention, |1> -> |10>
    self). The Bell-system pointer states are |00> and
    |11>.
  - Claim (xx) is a CODE CHECK in the same sense as
    (xvii): the plateau and the discord structure follow
    analytically from the branching construction (see the
    analytic cross-checks in the tests); a deviation
    would be a defect in the code's entropies, not a
    result about the theorem.
  - The headline numbers sit near saturation (REPORT.md
    section 5, v0.3.1 review): the curves -- I vs m,
    discord vs m, redundancy vs sigma -- are the science,
    not the points.

Pre-registered verdict rules for claims (xx)-(xxii),
written before the final measurement run (see the
claim_*_verdict functions and REPORT.md section 14).
Thresholds are round numbers set from the pilot sweep
and never moved after the final measurement run.

Directional assertions (frozen from pilots A/B/C):
  (xx) Redundancy plateau: as m grows, I(S:F) rises to
    H_S and STAYS there until m = N; discord stays ~0 on
    the plateau and rises only at m = N. Redundancy
    R_delta >= 1 with m* small. Expected PASS (pilot:
    hard m* = 1, R = 10; soft m* = 2, R = 5; plateau
    |I - H_S| <= 0.0456; discord <= 0.0456 on the
    plateau; discord(m = N) = 0.1887).
  (xxi) D tracks the classical, not the quantum: as the
    branching turns on (k = 0 -> N), D rises with
    redundancy / chi (Pearson >= 0.9) while concurrence
    falls (C(N)/C(0) <= 0.1); D anti-tracks discord
    (Pearson <= -0.9). Expected FAIL: D is exactly 2/3
    for every k (the off-diagonal |00><11| never
    contributes to Tr(P rho) and the diagonal is always
    (1/2, 1/2)), so Pearson(D, R) = Pearson(D, chi_1)
    = 0.0. The quantity that tracks the classical is
    chi, not D. Concurrence falls (hard 0.5 -> 0, soft
    0.5 -> 0.0005).
  (xxii) The sigma = 0.50 non-transfer explained: across
    the bridge's sigma grid the collaboration gap and the
    redundancy are sigma-ROBUST (sigma = 0.50 value >=
    0.5x the sigma = 0.25 value) while the discord at
    m = N is FRAGILE (sigma = 0.50 value <= 0.5x the
    sigma = 0.25 value); the gap tracks redundancy
    (Pearson >= 0.9), not discord. Falsified if the gap
    tracks discord instead (Pearson(gap, discord) >=
    0.9). Expected FAIL: under the bridge's vector noise
    the redundancy FALLS 6 -> 2 (m* grows 1 -> 3: the
    size-1 fragment's I drops to 0.37) and the discord
    RISES 0.1887 -> 0.6697 (the noise entangles S with
    F). The gap is robust (0.77) but tracks neither:
    Pearson(gap, R) ~ 0.35, Pearson(gap, discord) ~
    -0.54. The gap's sigma-survival is a property of
    the design-B mechanism, not of redundant classical
    encoding. (The dephasing picture -- classical robust,
    quantum fragile -- holds for the einselection
    parameter p, not for the vector-noise sigma.)
"""

import math

import numpy as np

import bridge
import cost
import empathy_field as ef
import monogamy as mg
import self_knowing as sk
import thought_entanglement as te
import unity

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Environment size: 10 fragments, matching Zhu et al. (2025),
# whose environment is 10 qubits beside a 2-qubit system.
N_ENV = 10

# Fragment sizes swept: every m from 0 (no environment) to N.
FRAGMENT_GRID = list(range(N_ENV + 1))

# Dephasing grid (einselection strength): 0 = pure branching,
# 1 = pointer mixture.
DEPHASING_GRID = [0.0, 0.25, 0.5, 0.75, 1.0]

# Reference dephasing for the plateau claim: partial
# einselection, where the quantum excess at m = N is
# nonzero but the plateau is classical.
DEPHASING_REF = 0.5

# Soft-branching overlap: <e_0|e_1> = cos(phi), phi = pi/3.
SOFT_PHI = math.pi / 3.0
SOFT_OVERLAP = math.cos(SOFT_PHI)

# Redundancy deficit: a fragment carries the pointer
# information when I(S:F) >= (1 - delta) H_S.
REDUNDANCY_DELTA = 0.1

SIGMA_GRID = te.SIGMA_GRID
DEFAULT_N_COPIES = 5
DEFAULT_SEED = 42

# Environment size for the noise sweep: 6 qubits. The
# plateau structure (plateau at H_S, discord rising only
# at m = N) is N-independent -- verified at N = 10 in
# claim (xx) and at N = 6 here -- and 6 keeps the
# largest fragment matrix at 2^8, so the full numeric
# path (eigvalsh on every fragment state) stays fast.
# At N = 10 the same sweep would spend minutes in
# 4096-dim eigvalsh calls.
N_NOISE = 6

# ---------------------------------------------------------------------------
# Pre-registered thresholds (set from the pilot sweep,
# REPORT.md section 14, and never moved after the final
# measurement run).
# ---------------------------------------------------------------------------

# Plateau tolerance: I(S:F) is within this of H_S on the
# plateau. The pilot's soft-model edge values are 0.0456
# (m = 2 and m = N - 1), so 0.10 is the round number with
# a 2.2x margin; the hard model is exact.
PLATEAU_TOL_BITS = 0.10

# Discord on the plateau must be at most this. The
# pilot's soft-model maximum on the plateau is 0.0456
# (m = N - 1), so 0.10 is the round number with a 2.2x
# margin; the hard model is exactly 0.
DISCORD_PLATEAU_MAX_BITS = 0.10

# Discord at the full environment (m = N, p = 0.5) must be
# at least this: the quantum excess is real, not noise.
# The pilot measures 0.1887, so 0.10 is the round number
# with a 1.9x margin.
DISCORD_FULL_ENV_MIN_BITS = 0.10

# The plateau must start at small m: m* <= this.
PLATEAU_START_MAX = 5

# Claim (xxi) gates: D must rise with redundancy / chi
# (Pearson >= this) while concurrence falls, and D must
# anti-track discord (Pearson <= the negative of this).
D_TRACK_MIN = 0.9
D_ANTITRACK_MAX = -0.9

# Claim (xxii) gates: the collaboration gap and the
# redundancy are sigma-ROBUST (their sigma = 0.50 value
# is at least this fraction of their sigma = 0.25 value),
# while the discord is FRAGILE (its sigma = 0.50 value
# is at most this fraction of its sigma = 0.25 value).
ROBUST_RATIO_MIN = 0.5
FRAGILE_RATIO_MAX = 0.5


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("PLATEAU_TOL_BITS", PLATEAU_TOL_BITS),
        ("DISCORD_PLATEAU_MAX_BITS", DISCORD_PLATEAU_MAX_BITS),
        ("DISCORD_FULL_ENV_MIN_BITS", DISCORD_FULL_ENV_MIN_BITS),
        ("PLATEAU_START_MAX", PLATEAU_START_MAX),
        ("D_TRACK_MIN", D_TRACK_MIN),
        ("D_ANTITRACK_MAX", D_ANTITRACK_MAX),
        ("ROBUST_RATIO_MIN", ROBUST_RATIO_MIN),
        ("FRAGILE_RATIO_MAX", FRAGILE_RATIO_MAX),
    ) if value is None]
    if missing:
        raise ValueError(
            "darwinism thresholds are unset: run the pilot "
            "sweep and set " + ", ".join(missing) + " first "
            "(REPORT.md section 14)")
    return {
        "plateau_tol_bits": float(PLATEAU_TOL_BITS),
        "discord_plateau_max_bits": float(DISCORD_PLATEAU_MAX_BITS),
        "discord_full_env_min_bits": float(DISCORD_FULL_ENV_MIN_BITS),
        "plateau_start_max": int(PLATEAU_START_MAX),
        "d_track_min": float(D_TRACK_MIN),
        "d_antitrack_max": float(D_ANTITRACK_MAX),
        "robust_ratio_min": float(ROBUST_RATIO_MIN),
        "fragile_ratio_max": float(FRAGILE_RATIO_MAX),
    }


# ---------------------------------------------------------------------------
# Branching states
# ---------------------------------------------------------------------------

def record_states(phi):
    """The environment record states |e_0>, |e_1>.

    |e_0> = |0>; |e_1> = cos(phi)|0> + sin(phi)|1>.
    phi = pi/2 is hard branching (orthogonal records,
    overlap 0); phi = pi/3 is soft branching (overlap
    1/2). The overlap is cos(phi).
    """
    return (np.array([1.0, 0.0], dtype=complex),
            np.array([math.cos(float(phi)), math.sin(float(phi))],
                     dtype=complex))


def record_overlap(phi):
    """<e_0|e_1> = cos(phi)."""
    return float(math.cos(float(phi)))


def _kron_many(vectors):
    """Kronecker product of a list of vectors, in order."""
    out = np.array([1.0], dtype=complex)
    for v in vectors:
        out = np.kron(out, np.asarray(v, dtype=complex))
    return out


def pointer_states(system):
    """The system's pointer basis vectors.

    "bell": |00> and |11> (indices 0 and 3).
    "binary": |0> and |1> (indices 0 and 1).
    """
    if system == "bell":
        return (np.array([1.0, 0.0, 0.0, 0.0], dtype=complex),
                np.array([0.0, 0.0, 0.0, 1.0], dtype=complex))
    if system == "binary":
        return (np.array([1.0, 0.0], dtype=complex),
                np.array([0.0, 1.0], dtype=complex))
    raise ValueError("system must be 'bell' or 'binary'")


def pointer_indices(system):
    """Computational-basis indices of the pointer states."""
    return tuple(int(np.argmax(np.abs(p)))
                 for p in pointer_states(system))


def pointer_sector(index, n_sys):
    """Which side of the pointer measurement a system basis
    index falls on: 0 or 1.

    The pointer observable is the qubit that distinguishes
    the two pointer states -- qubit 0, the most
    significant bit (Bell: |00> vs |11>; binary: |0> vs
    |1>). Sector 0 is the half of the system basis with
    that qubit 0, sector 1 the half with it 1. Measuring
    it is a COMPLETE projective measurement (the two
    sector projectors sum to the identity), so the
    Holevo chi it defines obeys chi <= I and the
    discord I - chi is never negative -- unlike the
    incomplete two-projector pointer measurement, which
    drops the non-pointer outcomes and reports a negative
    discord once vector noise populates them.
    """
    return int(index) >> (int(n_sys) - 1)


def system_n_qubits(system):
    """Number of system qubits: 2 for 'bell', 1 for 'binary'."""
    if system == "bell":
        return 2
    if system == "binary":
        return 1
    raise ValueError("system must be 'bell' or 'binary'")


def pointer_entropy_bits(system="bell"):
    """H_S of the pointer distribution: 1 bit (two pointer
    states, equal weight)."""
    return float(math.log2(len(pointer_states(system))))


def branching_state(n_env=N_ENV, system="bell", phi=math.pi / 2.0):
    """The branching state vector: system + N environment
    qubits, qubit order [system | env_0..N-1].

    (|p_0>|e_0>^N + |p_1>|e_1>^N) / sqrt(2). Returns
    (psi, pointers).
    """
    n_env = int(n_env)
    if n_env < 1:
        raise ValueError("need at least one environment qubit")
    pointers = pointer_states(system)
    e0, e1 = record_states(phi)
    branch0 = _kron_many([pointers[0]] + [e0] * n_env)
    branch1 = _kron_many([pointers[1]] + [e1] * n_env)
    psi = (branch0 + branch1) / math.sqrt(2.0)
    return psi, pointers


def density_matrix(psi):
    """rho = |psi><psi|."""
    psi = np.asarray(psi, dtype=complex)
    return np.outer(psi, psi.conj())


# ---------------------------------------------------------------------------
# Closed-form fragment state (the fast path)
# ---------------------------------------------------------------------------

def fragment_state_direct(m, n_env=N_ENV, system="bell",
                          phi=math.pi / 2.0, p=DEPHASING_REF):
    """rho_SF for a fragment of m environment qubits, built
    directly from the branching construction.

    rho_SF = (1/2) sum_k |p_k><p_k| (x) |e_k^m><e_k^m|
      + ((1-p)/2) c^(N-m) (|p_0><p_1| (x) |e_0^m><e_1^m|
      + h.c.), where c = <e_0|e_1> = cos(phi). At m = 0
    this is the system's reduced state. The general
    partial trace (below) reproduces this exactly; it is
    cross-checked in the tests on small N.
    """
    m = int(m)
    n_env = int(n_env)
    if not 0 <= m <= n_env:
        raise ValueError("fragment size m must satisfy 0 <= m <= N")
    pointers = pointer_states(system)
    e0, e1 = record_states(phi)
    c = record_overlap(phi)
    p = float(p)
    if not 0.0 <= p <= 1.0:
        raise ValueError("dephasing strength p must be in [0, 1]")
    rec0 = _kron_many([e0] * m) if m > 0 else np.array([1.0],
                                                      dtype=complex)
    rec1 = _kron_many([e1] * m) if m > 0 else np.array([1.0],
                                                      dtype=complex)
    rho = 0.5 * (np.kron(np.outer(pointers[0], pointers[0].conj()),
                         np.outer(rec0, rec0.conj()))
                 + np.kron(np.outer(pointers[1], pointers[1].conj()),
                           np.outer(rec1, rec1.conj())))
    if p < 1.0:
        off = ((1.0 - p) / 2.0) * (c ** (n_env - m))
        if off != 0.0:
            rho = rho + off * (
                np.kron(np.outer(pointers[0], pointers[1].conj()),
                        np.outer(rec0, rec1.conj()))
                + np.kron(np.outer(pointers[1], pointers[0].conj()),
                          np.outer(rec1, rec0.conj())))
    return rho


def system_state_direct(n_env=N_ENV, system="bell",
                        phi=math.pi / 2.0, p=DEPHASING_REF):
    """The system's reduced state: fragment_state_direct
    with m = 0."""
    return fragment_state_direct(0, n_env, system, phi, p)


def dephase_fragment(rho_sf, n_sys, m, system, p):
    """Dephase a fragment state in the pointer basis.

    rho_SF -> (1 - p) rho_SF + p sum_b P_b rho_SF P_b,
    P_b the projector onto pointer sector b (x) I_F.
    The two sectors are the halves of the system basis
    split by the pointer-distinguishing qubit (see
    pointer_sector). Used for the noisy-copy sweep, where
    rho_SF comes from a pure copy vector. On the noiseless
    branching state this is exactly the old pointer-block
    dephasing: the only nonzero off-diagonal system block
    is the pointer-pointer one, and it is cross-sector.
    """
    p = float(p)
    if not 0.0 <= p <= 1.0:
        raise ValueError("dephasing strength p must be in [0, 1]")
    rho_sf = np.asarray(rho_sf, dtype=complex)
    if p == 0.0:
        return rho_sf.copy()
    n_sys = int(n_sys)
    d_s = 1 << n_sys
    d_f = 1 << int(m)
    sectors = np.array([pointer_sector(i, n_sys)
                        for i in range(d_s)])
    # Mask on the system axes: 1 within a sector,
    # (1 - p) across sectors.
    mask = np.where(sectors[:, None] == sectors[None, :],
                    1.0, 1.0 - p)
    tensor = rho_sf.reshape(d_s, d_f, d_s, d_f)
    dephased = tensor * mask[:, None, :, None]
    return dephased.reshape(rho_sf.shape)


# ---------------------------------------------------------------------------
# General partial trace (cross-check path)
# ---------------------------------------------------------------------------

def partial_trace_general(rho, keep, n_qubits):
    """Reduced density matrix keeping the qubits in `keep`.

    rho is 2^n x 2^n; keep is a non-empty tuple of distinct
    qubit indices in {0..n-1}. Qubit 0 is the most
    significant bit (the monogamy.py convention). The kept
    qubits come out in ascending index order.
    """
    rho = np.asarray(rho, dtype=complex)
    n_qubits = int(n_qubits)
    if rho.shape != (1 << n_qubits, 1 << n_qubits):
        raise ValueError("rho shape does not match n_qubits")
    keep = tuple(int(q) for q in keep)
    if not keep or not set(keep) <= set(range(n_qubits)) \
            or len(set(keep)) != len(keep):
        raise ValueError("keep must be a non-empty tuple of "
                         "distinct qubit indices in range")
    remaining = list(range(n_qubits))
    t = rho.reshape([2] * (2 * n_qubits))
    for q in sorted(set(range(n_qubits)) - set(keep), reverse=True):
        idx = remaining.index(q)
        t = np.trace(t, axis1=idx, axis2=len(remaining) + idx)
        remaining.pop(idx)
    d = 1 << len(keep)
    return t.reshape(d, d)


def fragment_state(rho_joint, n_sys, n_env, m):
    """rho_SF via the general partial trace: the system plus
    the first m environment qubits (the other N - m traced
    out). m = 0 returns the system's reduced state alone.
    Cross-checks fragment_state_direct in the tests.
    """
    n_sys = int(n_sys)
    n_env = int(n_env)
    m = int(m)
    if not 0 <= m <= n_env:
        raise ValueError("fragment size m must satisfy 0 <= m <= N")
    keep = tuple(range(n_sys + m))
    return partial_trace_general(rho_joint, keep, n_sys + n_env)


def fragment_state_from_vector(psi, n_sys, n_env, m):
    """rho_SF for a PURE joint state vector, via reshape +
    X X-dagger. Qubit order [system | fragment | rest],
    so the vector reshapes to (d_SF, d_rest) directly.
    """
    psi = np.asarray(psi, dtype=complex)
    n_sys = int(n_sys)
    n_env = int(n_env)
    m = int(m)
    if psi.shape != (1 << (n_sys + n_env),):
        raise ValueError("psi shape does not match n_sys + n_env")
    if not 0 <= m <= n_env:
        raise ValueError("fragment size m must satisfy 0 <= m <= N")
    x = psi.reshape(1 << (n_sys + m), 1 << (n_env - m))
    return x @ x.conj().T


def dephase_pointer(rho, pointers, n_sys, n_env, p):
    """Dephase a joint density matrix in the pointer basis.

    rho -> (1 - p) rho + p sum_k P_k rho P_k, P_k the
    system pointer projector (identity on the
    environment). Used in the tests to cross-check the
    closed form against the traced construction.
    """
    if not 0.0 <= float(p) <= 1.0:
        raise ValueError("dephasing strength p must be in [0, 1]")
    rho = np.asarray(rho, dtype=complex)
    dim_env = 1 << int(n_env)
    p = float(p)
    if p == 0.0:
        return rho.copy()
    mixed = np.zeros_like(rho)
    for pk in pointers:
        proj = np.kron(np.outer(pk, pk.conj()),
                       np.eye(dim_env, dtype=complex))
        mixed = mixed + proj @ rho @ proj
    return (1.0 - p) * rho + p * mixed


# ---------------------------------------------------------------------------
# Fragment quantities: I, chi, discord
# ---------------------------------------------------------------------------

def holevo_chi(rho_sf, n_sys, system):
    """Holevo chi(S:F): the classical information a fragment
    carries about the system.

    Measure S in the pointer observable -- the qubit that
    distinguishes the pointer states (see pointer_sector):
    outcome b has probability p_b and leaves the fragment
    in rho_F|b, the sector-b diagonal block of rho_SF.
    chi = H(rho_F) - sum_b p_b H(rho_F|b). The measurement
    is complete (the two sector projectors sum to the
    identity), so chi <= I by data processing and the
    discord I - chi is never negative. On the noiseless
    branching state the non-pointer basis states have
    probability 0, so this is identical to the
    two-pointer-projector form. A zero-probability
    outcome contributes nothing.
    """
    rho_sf = np.asarray(rho_sf, dtype=complex)
    n_sys = int(n_sys)
    d_s = 1 << n_sys
    d_f = rho_sf.shape[0] // d_s
    if rho_sf.shape != (d_s * d_f, d_s * d_f):
        raise ValueError("rho_sf shape does not match n_sys")
    tensor = rho_sf.reshape(d_s, d_f, d_s, d_f)
    rho_f = np.trace(tensor, axis1=0, axis2=2)
    h_f = cost.von_neumann_entropy(rho_f)
    cond = 0.0
    for b in (0, 1):
        block = None
        for i in range(d_s):
            if pointer_sector(i, n_sys) != b:
                continue
            block = (tensor[i, :, i, :] if block is None
                     else block + tensor[i, :, i, :])
        p_b = float(np.real(np.trace(block)))
        if p_b <= 0.0:
            continue
        cond += p_b * cost.von_neumann_entropy(block / p_b)
    return float(h_f - cond)


def fragment_quantities(rho_sf, n_sys, system):
    """I, chi, discord and the entropies for one fragment.

    Returns H_S, H_F, H_SF, I(S:F), chi(S:F), discord =
    I - chi. For m = 0 (no fragment) I, chi and discord
    are 0 and H_SF = H_S.
    """
    rho_sf = np.asarray(rho_sf, dtype=complex)
    n_sys = int(n_sys)
    d_s = 1 << n_sys
    d_f = rho_sf.shape[0] // d_s
    m = int(round(math.log2(d_f))) if d_f > 1 else 0
    # Read the reduced states off the tensor directly
    # (no big reshape): rho_S[a, c] = sum_b T[a, b, c, b],
    # rho_F[b, d] = sum_a T[a, b, a, d].
    tensor = rho_sf.reshape(d_s, d_f, d_s, d_f)
    rho_s = np.trace(tensor, axis1=1, axis2=3)
    rho_f = (np.trace(tensor, axis1=0, axis2=2) if m > 0
             else np.array([[1.0]], dtype=complex))
    h_s = cost.von_neumann_entropy(rho_s)
    h_f = cost.von_neumann_entropy(rho_f)
    h_sf = cost.von_neumann_entropy(rho_sf)
    mutual = float(h_s + h_f - h_sf)
    chi = holevo_chi(rho_sf, n_sys, system) if m > 0 else 0.0
    return {
        "h_system_bits": float(h_s),
        "h_fragment_bits": float(h_f),
        "h_joint_bits": float(h_sf),
        "mutual_information_bits": mutual,
        "holevo_chi_bits": float(chi),
        "discord_bits": float(mutual - chi),
    }


# ---------------------------------------------------------------------------
# Analytic cross-checks (binary system)
# ---------------------------------------------------------------------------

def analytic_fragment_values(m, n_env=N_ENV, overlap=0.0, p=0.0):
    """Exact I, chi, discord for the binary branching state.

    With overlap c = <e_0|e_1> and dephasing p:
      H_S  = H2((1 + c^N (1-p)) / 2)
      H_F  = H2((1 + c^m) / 2)          (m >= 1; 0 at m = 0)
      H_SF = H2((1 + (1-p) c^(N-m)) / 2)
      chi  = H_F                         (the conditioned
             fragment states are pure)
      I    = H_S + H_F - H_SF
      discord = I - chi = H_S - H_SF
    H2 is the binary entropy. These are the formulas the
    numerical fragment quantities must reproduce to 1e-9.
    """
    m = int(m)
    n_env = int(n_env)
    c = float(overlap)
    p = float(p)
    if not 0 <= m <= n_env:
        raise ValueError("fragment size m must satisfy 0 <= m <= N")

    def h2(x):
        x = min(1.0, max(0.0, float(x)))
        if x == 0.0 or x == 1.0:
            return 0.0
        return float(-x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x))

    h_s = h2((1.0 + (c ** n_env) * (1.0 - p)) / 2.0)
    if m == 0:
        return {
            "h_system_bits": h_s,
            "h_fragment_bits": 0.0,
            "h_joint_bits": h_s,
            "mutual_information_bits": 0.0,
            "holevo_chi_bits": 0.0,
            "discord_bits": 0.0,
        }
    h_f = h2((1.0 + c ** m) / 2.0)
    h_sf = h2((1.0 + (1.0 - p) * (c ** (n_env - m))) / 2.0)
    mutual = h_s + h_f - h_sf
    return {
        "h_system_bits": h_s,
        "h_fragment_bits": h_f,
        "h_joint_bits": h_sf,
        "mutual_information_bits": mutual,
        "holevo_chi_bits": h_f,
        "discord_bits": mutual - h_f,
    }


# ---------------------------------------------------------------------------
# Sweeps
# ---------------------------------------------------------------------------

def plateau_sweep(n_env=N_ENV, system="binary", phi=math.pi / 2.0,
                  p=DEPHASING_REF):
    """I, chi, discord per fragment size m = 0..N.

    One row per m, evaluated in the closed form
    (analytic_fragment_values): the fragment state is
    exactly rank 2, so the closed form IS the evaluation
    of the same quantities the numeric fragment_quantities
    computes -- the tests pin numeric == closed form to
    1e-9 (hard) / 2e-15 (soft) at N = 10. The plateau is
    the run of m where I is at H_S; the discord is 0 on
    it (hard branching) or exponentially suppressed
    (soft branching) and rises only as m -> N.
    """
    n_sys = system_n_qubits(system)
    h_pointer = pointer_entropy_bits(system)
    c = record_overlap(phi)
    rows = []
    for m in range(int(n_env) + 1):
        q = analytic_fragment_values(m, n_env, c, p)
        rows.append({
            "m": m,
            "h_system_bits": q["h_system_bits"],
            "h_fragment_bits": q["h_fragment_bits"],
            "h_joint_bits": q["h_joint_bits"],
            "mutual_information_bits": q["mutual_information_bits"],
            "holevo_chi_bits": q["holevo_chi_bits"],
            "discord_bits": q["discord_bits"],
            "h_pointer_bits": h_pointer,
        })
    return rows


def plateau_start(rows, delta=REDUNDANCY_DELTA):
    """The smallest m >= 1 with I(S:F) >= (1 - delta) H_S.

    None when no fragment size reaches the threshold.
    """
    for r in rows:
        if r["m"] >= 1 and r["mutual_information_bits"] >= (
                1.0 - float(delta)) * r["h_pointer_bits"]:
            return int(r["m"])
    return None


def redundancy(rows, n_env=N_ENV, delta=REDUNDANCY_DELTA):
    """R_delta: the number of disjoint size-m* fragments
    that fit in the environment, m* = plateau_start.

    R_delta = N // m*. 0 when no fragment size reaches
    (1 - delta) H_S. For hard branching m* = 1 and
    R_delta = N: every single environment qubit carries
    the full classical bit.
    """
    m_star = plateau_start(rows, delta)
    if m_star is None:
        return 0
    return int(n_env) // int(m_star)


def system_concurrence(rho_s):
    """Concurrence of a 4x4 system state (Bell system).

    The binary system has a single qubit and no
    concurrence; callers pass None for it.
    """
    return float(te.concurrence(np.asarray(rho_s, dtype=complex)))


def system_self_knowing(rho_s, system):
    """D of the system's reduced state, via the existing
    self-knowing projector.

    Bell system: the 4-dim reduced state is a thought, so
    D = Tr(P rho_S) directly. Binary system: the 2x2
    reduced state is embedded in thought space first
    (monogamy.py's embedding).
    """
    rho_s = np.asarray(rho_s, dtype=complex)
    if system == "bell":
        return float(sk.self_knowing_of_state(rho_s))
    if system == "binary":
        return float(sk.self_knowing_of_state(
            mg.embed_member_state(rho_s)))
    raise ValueError("system must be 'bell' or 'binary'")


def branching_turn_on(n_env=N_ENV, system="bell",
                      phi=math.pi / 2.0, p=DEPHASING_REF):
    """D, concurrence, chi and redundancy as the branching
    turns on: k = 0..N environment qubits interacted.

    The system's reduced state after k interactions is
    the closed form with overlap c^k: rho_S(k) = (1/2)
    sum_k |p_k><p_k| + ((1-p)/2) c^k (|p_0><p_1| + h.c.).
    At k = 0 the system is the pure superposition
    (concurrence 1 for the Bell system); at k >= 1 the
    environment records the pointer value. chi and
    redundancy are read off the k-qubit plateau sweep
    (a size-1 fragment of the interacted qubits). At
    k = 0 there is no fragment and both are 0.
    """
    n_sys = system_n_qubits(system)
    c = record_overlap(phi)
    rows = []
    for k in range(int(n_env) + 1):
        rho_s = fragment_state_direct(0, k, system, phi, p) \
            if k > 0 else system_state_direct(0, system, phi, p)
        # The m = 0 closed form with N replaced by k:
        # off-diagonal (1-p)/2 * c^k. fragment_state_direct
        # with n_env = k gives exactly that (c^(k-0)).
        conc = (system_concurrence(rho_s)
                if system == "bell" else None)
        d_sys = system_self_knowing(rho_s, system)
        if k == 0:
            chi_1, red, disc_full = 0.0, 0, 0.0
        else:
            sub = plateau_sweep(k, system, phi, p)
            chi_1 = sub[1]["holevo_chi_bits"]
            red = redundancy(sub, k)
            disc_full = sub[k]["discord_bits"]
        rows.append({
            "k_interacted": int(k),
            "system_concurrence": conc,
            "system_d": float(d_sys),
            "chi_fragment_1_bits": float(chi_1),
            "redundancy": int(red),
            "discord_full_bits": float(disc_full),
        })
    return rows


def noisy_branching_quantities(sigma, n_env=N_ENV, system="bell",
                               phi=math.pi / 2.0, p=DEPHASING_REF,
                               n_copies=DEFAULT_N_COPIES,
                               seed=DEFAULT_SEED):
    """Darwinism quantities under the bridge's vector noise.

    The branching state (real vector) gets the unity.py
    Gaussian-copy noise at sigma; per copy, the plateau
    value (mean I over 1 <= m <= N-1), the discord at
    m = N, the redundancy, the system concurrence and
    the system D are computed, then averaged over copies.
    What the noise does to these quantities is measured
    by claim (xxii); nothing about robustness is assumed
    here. (The vector noise is not a dephasing channel:
    it adds random components that entangle S with F, so
    the classical/quantum split under it is not the
    dephasing picture.)
    """
    psi, pointers = branching_state(n_env, system, phi)
    n_sys = system_n_qubits(system)
    copies = unity.gaussian_copies(np.real(psi), sigma, n_copies,
                                   seed)
    plateau_is, discords, reds, concs, ds = [], [], [], [], []
    for cvec in copies:
        psi_c = np.asarray(cvec, dtype=complex)
        plateau, discord_full = [], None
        rows = []
        for m in range(int(n_env) + 1):
            rho_sf = fragment_state_from_vector(psi_c, n_sys,
                                                n_env, m)
            rho_sf = dephase_fragment(rho_sf, n_sys, m, system, p)
            q = fragment_quantities(rho_sf, n_sys, system)
            rows.append({
                "m": m,
                "mutual_information_bits":
                    q["mutual_information_bits"],
                "h_pointer_bits": pointer_entropy_bits(system),
            })
            if 1 <= m <= int(n_env) - 1:
                plateau.append(q["mutual_information_bits"])
            if m == int(n_env):
                discord_full = q["discord_bits"]
        plateau_is.append(float(np.mean(plateau)))
        discords.append(float(discord_full))
        reds.append(redundancy(rows, n_env))
        rho_s = fragment_state_from_vector(psi_c, n_sys, n_env, 0)
        rho_s = dephase_fragment(rho_s, n_sys, 0, system, p)
        concs.append(system_concurrence(rho_s)
                     if system == "bell" else None)
        ds.append(system_self_knowing(rho_s, system))
    conc_mean = (float(np.mean([c for c in concs if c is not None]))
                 if any(c is not None for c in concs) else None)
    return {
        "sigma": float(sigma),
        "plateau_mutual_information_bits": float(np.mean(plateau_is)),
        "discord_full_env_bits": float(np.mean(discords)),
        "redundancy": float(np.mean(reds)),
        "system_concurrence": conc_mean,
        "system_d": float(np.mean(ds)),
    }


def noise_sweep(sigmas=None, n_env=N_NOISE, **kwargs):
    """The noisy branching quantities across the sigma grid.

    Default environment N_NOISE = 6 (see the constant):
    the plateau structure is N-independent, and 6 keeps
    the full numeric path fast.
    """
    rows = []
    for sigma in (SIGMA_GRID if sigmas is None else sigmas):
        rows.append(noisy_branching_quantities(sigma, n_env=n_env,
                                               **kwargs))
    return rows


# ---------------------------------------------------------------------------
# Claim verdicts (xx)-(xxii)
# ---------------------------------------------------------------------------

def claim_plateau_verdict():
    """(xx) Redundancy plateau: I(S:F) plateaus at H_S for
    small m; discord -> 0 on the plateau and rises only
    as m -> N.

    PASS iff, for all four (system, branching) combos at
    p = 0.5, N = 10: the plateau starts at m* <=
    PLATEAU_START_MAX (5); on m in [m*, N-1] the mutual
    information is within PLATEAU_TOL_BITS (0.10) of H_S
    and the discord is at most DISCORD_PLATEAU_MAX_BITS
    (0.10); the discord at m = N is at least
    DISCORD_FULL_ENV_MIN_BITS (0.10); the redundancy is
    at least 1. The dephasing sweep (p in {0, 0.5, 1},
    hard binary) is reported, not gated: the classical
    plateau is p-independent while the discord at m = N
    falls with p.
    """
    t = _thresholds()
    combos = []
    checks = {}
    for system in ("binary", "bell"):
        for name, phi in (("hard", math.pi / 2.0),
                          ("soft", SOFT_PHI)):
            rows = plateau_sweep(N_ENV, system, phi, DEPHASING_REF)
            m_star = plateau_start(rows)
            red = redundancy(rows, N_ENV)
            h_s = rows[0]["h_pointer_bits"]
            plateau_rows = [r for r in rows
                            if m_star is not None
                            and m_star <= r["m"] <= N_ENV - 1]
            max_i_dev = (max(abs(r["mutual_information_bits"] - h_s)
                             for r in plateau_rows)
                         if plateau_rows else float("inf"))
            max_disc = (max(r["discord_bits"] for r in plateau_rows)
                        if plateau_rows else float("inf"))
            disc_full = rows[N_ENV]["discord_bits"]
            key = f"{system}_{name}"
            combos.append({
                "system": system,
                "branching": name,
                "m_star": m_star,
                "redundancy": red,
                "h_system_bits": h_s,
                "max_plateau_i_deviation_bits": float(max_i_dev),
                "max_plateau_discord_bits": float(max_disc),
                "discord_full_env_bits": float(disc_full),
                "rows": rows,
            })
            checks[f"{key}_plateau_starts_small"] = (
                m_star is not None and m_star <= t["plateau_start_max"])
            checks[f"{key}_plateau_i_at_h_s"] = (
                max_i_dev <= t["plateau_tol_bits"])
            checks[f"{key}_plateau_discord_small"] = (
                max_disc <= t["discord_plateau_max_bits"])
            checks[f"{key}_discord_full_env_real"] = (
                disc_full >= t["discord_full_env_min_bits"])
            checks[f"{key}_redundancy_at_least_one"] = red >= 1
    # Dephasing picture (reported, not gated): the plateau
    # is p-independent, the full-env discord falls with p.
    p_rows = []
    for p in (0.0, DEPHASING_REF, 1.0):
        rows = plateau_sweep(N_ENV, "binary", math.pi / 2.0, p)
        p_rows.append({
            "p": p,
            "plateau_i_bits": float(np.mean(
                [r["mutual_information_bits"]
                 for r in rows[1:N_ENV]])),
            "discord_full_env_bits": float(rows[N_ENV]["discord_bits"]),
        })
    passed = bool(all(checks.values()))
    return {
        "claim": "(xx) Redundancy plateau: I plateaus at H_S, "
                 "discord ~0 on the plateau, rising only at m = N",
        "passed": passed,
        "checks": checks,
        "combos": combos,
        "dephasing_rows": p_rows,
    }


def claim_d_tracks_classical_verdict():
    """(xxi) D tracks the classical, not the quantum: local
    self-knowing D rises with redundancy / chi while
    concurrence falls -- D anti-tracks discord, not just
    concurrence.

    PASS iff, for both branching families (Bell, p = 0.5),
    as the branching turns on (k = 0..N): Pearson(D, R) >=
    D_TRACK_MIN (0.9), Pearson(D, chi_1) >= D_TRACK_MIN
    (0.9), concurrence falls to <= 0.1x its k = 0 value,
    and Pearson(D, discord_full) <= D_ANTITRACK_MAX
    (-0.9). Measured: D is exactly 2/3 for every k, so
    the Pearsons are 0.0 and the claim FAILS -- the
    quantity that tracks the classical is chi, not D.
    """
    t = _thresholds()
    families = []
    checks = {}
    for name, phi in (("hard", math.pi / 2.0),
                      ("soft", SOFT_PHI)):
        rows = branching_turn_on(N_ENV, "bell", phi, DEPHASING_REF)
        ds = [r["system_d"] for r in rows]
        rs = [float(r["redundancy"]) for r in rows]
        chis = [r["chi_fragment_1_bits"] for r in rows]
        discs = [r["discord_full_bits"] for r in rows]
        concs = [r["system_concurrence"] for r in rows]
        pearson_d_r = sk.pearson(ds, rs)
        pearson_d_chi = sk.pearson(ds, chis)
        pearson_d_disc = sk.pearson(ds, discs)
        conc_ratio = (concs[N_ENV] / concs[0] if concs[0] else None)
        families.append({
            "branching": name,
            "pearson_d_redundancy": float(pearson_d_r),
            "pearson_d_chi": float(pearson_d_chi),
            "pearson_d_discord": float(pearson_d_disc),
            "concurrence_k0": float(concs[0]),
            "concurrence_kN": float(concs[N_ENV]),
            "concurrence_ratio": (float(conc_ratio)
                                  if conc_ratio is not None else None),
            "d_min": float(min(ds)),
            "d_max": float(max(ds)),
            "rows": rows,
        })
        checks[f"{name}_d_rises_with_redundancy"] = (
            pearson_d_r >= t["d_track_min"])
        checks[f"{name}_d_rises_with_chi"] = (
            pearson_d_chi >= t["d_track_min"])
        checks[f"{name}_concurrence_falls"] = (
            conc_ratio is not None and conc_ratio <= 0.1)
        checks[f"{name}_d_anti_tracks_discord"] = (
            pearson_d_disc <= t["d_antitrack_max"])
    passed = bool(all(checks.values()))
    return {
        "claim": "(xxi) D tracks the classical, not the quantum: "
                 "D rises with redundancy / chi while concurrence "
                 "falls, D anti-tracks discord",
        "passed": passed,
        "checks": checks,
        "families": families,
    }


def claim_non_transfer_verdict():
    """(xxii) The sigma = 0.50 non-transfer explained: the
    collaboration gap (+4.3352 bits at sigma = 0.25)
    tracks classical redundancy (sigma-robust) while
    concurrence tracks discord (fragile). Falsified if
    the gap tracks discord instead.

    PASS iff, across the bridge's sigma grid (Bell hard,
    p = 0.5, N = 6): the gap and the redundancy are
    sigma-robust at the 0.25 -> 0.50 step (ratio >=
    ROBUST_RATIO_MIN, 0.5) and across the grid (min
    redundancy >= 0.5x its sigma = 0 value), the discord
    is fragile (sigma = 0.50 value <= 0.5x the sigma =
    0.25 value; sigma = 1.0 value <= 0.5x the sigma = 0
    value), the gap tracks redundancy (Pearson >= 0.9)
    and does NOT track discord (Pearson < 0.9), and
    concurrence tracks discord (Pearson >= 0.9).
    Measured: the gap is robust (0.77) but the redundancy
    falls 6 -> 2 and the discord RISES 0.19 -> 2.13 under
    the vector noise, so the claim FAILS -- the gap's
    sigma-survival is a property of the design-B
    mechanism, not of redundant classical encoding.
    The dephasing sweep (p in {0, 0.5, 1}, hard binary,
    sigma = 0) is reported, not gated: the classical
    plateau is p-independent while the full-env discord
    falls with p -- the dephasing picture holds for p,
    not for sigma.
    """
    t = _thresholds()
    noise_rows = noise_sweep()
    gap_rows = ef.collaboration_gap_vs_noise()
    conc_rows = te.entanglement_sweep()
    sigmas = [r["sigma"] for r in noise_rows]
    gaps = [next(g["gap_bits"] for g in gap_rows
                 if g["sigma"] == s) for s in sigmas]
    reds = [r["redundancy"] for r in noise_rows]
    discs = [r["discord_full_env_bits"] for r in noise_rows]
    concs = [next(c["mean_concurrence"] for c in conc_rows
                  if c["sigma"] == s) for s in sigmas]
    i_025 = sigmas.index(0.25)
    i_050 = sigmas.index(0.5)
    gap_ratio = gaps[i_050] / gaps[i_025]
    red_ratio = reds[i_050] / reds[i_025]
    disc_ratio = discs[i_050] / discs[i_025]
    red_grid_ratio = min(reds) / reds[0]
    disc_grid_ratio = discs[-1] / discs[0]
    pearson_gap_r = sk.pearson(gaps, reds)
    pearson_gap_disc = sk.pearson(gaps, discs)
    pearson_conc_disc = sk.pearson(concs, discs)
    checks = {
        "gap_robust_step": gap_ratio >= t["robust_ratio_min"],
        "redundancy_robust_step": red_ratio >= t["robust_ratio_min"],
        "discord_fragile_step": disc_ratio <= t["fragile_ratio_max"],
        "redundancy_robust_grid": (
            red_grid_ratio >= t["robust_ratio_min"]),
        "discord_fragile_grid": (
            disc_grid_ratio <= t["fragile_ratio_max"]),
        "gap_tracks_redundancy": (
            pearson_gap_r >= t["d_track_min"]),
        "gap_does_not_track_discord": pearson_gap_disc < 0.9,
        "concurrence_tracks_discord": (
            pearson_conc_disc >= t["d_track_min"]),
    }
    p_rows = []
    for p in (0.0, DEPHASING_REF, 1.0):
        rows = plateau_sweep(N_ENV, "binary", math.pi / 2.0, p)
        p_rows.append({
            "p": p,
            "plateau_i_bits": float(np.mean(
                [r["mutual_information_bits"]
                 for r in rows[1:N_ENV]])),
            "discord_full_env_bits": float(rows[N_ENV]["discord_bits"]),
        })
    passed = bool(all(checks.values()))
    return {
        "claim": "(xxii) The sigma = 0.50 non-transfer explained: "
                 "the collaboration gap tracks classical redundancy "
                 "(sigma-robust) while concurrence tracks discord "
                 "(fragile)",
        "passed": passed,
        "checks": checks,
        "sigmas": sigmas,
        "gaps_bits": [float(g) for g in gaps],
        "redundancies": [float(r) for r in reds],
        "discords_full_env_bits": [float(d) for d in discs],
        "concurrences": [float(c) for c in concs],
        "gap_ratio_050_over_025": float(gap_ratio),
        "redundancy_ratio_050_over_025": float(red_ratio),
        "discord_ratio_050_over_025": float(disc_ratio),
        "redundancy_grid_ratio": float(red_grid_ratio),
        "discord_grid_ratio": float(disc_grid_ratio),
        "pearson_gap_redundancy": float(pearson_gap_r),
        "pearson_gap_discord": float(pearson_gap_disc),
        "pearson_concurrence_discord": float(pearson_conc_disc),
        "noise_rows": noise_rows,
        "dephasing_rows": p_rows,
    }


def darwinism_claims():
    """The three quantum-Darwinism claims (xx)-(xxii),
    measured fresh."""
    claim_xx = claim_plateau_verdict()
    claim_xxi = claim_d_tracks_classical_verdict()
    claim_xxii = claim_non_transfer_verdict()
    verdicts = [claim_xx, claim_xxi, claim_xxii]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_xx_plateau": claim_xx,
        "claim_xxi_d_tracks_classical": claim_xxi,
        "claim_xxii_non_transfer": claim_xxii,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the plateau sweeps, the branching turn-on,
    the noise sweep, and the claims (xx)-(xxii) verdicts."""
    print("Quantum-Darwinism redundancy plateau -- claims (xx)-(xxii)")
    print()
    verdicts = darwinism_claims()
    xx = verdicts["claim_xx_plateau"]
    for combo in xx["combos"]:
        print(f"{combo['system']} {combo['branching']}: "
              f"m* = {combo['m_star']}, R = {combo['redundancy']}, "
              f"max |I - H_S| on plateau = "
              f"{combo['max_plateau_i_deviation_bits']:.4f}, "
              f"max discord on plateau = "
              f"{combo['max_plateau_discord_bits']:.4f}, "
              f"discord(m = N) = {combo['discord_full_env_bits']:.4f}")
    print("dephasing (hard binary, sigma = 0): "
          + ", ".join(
              f"p = {r['p']}: plateau I = {r['plateau_i_bits']:.4f}, "
              f"discord(N) = {r['discord_full_env_bits']:.4f}"
              for r in xx["dephasing_rows"]))
    print(f"claim (xx) verdict: {'PASS' if xx['passed'] else 'FAIL'}")
    print()
    xxi = verdicts["claim_xxi_d_tracks_classical"]
    for fam in xxi["families"]:
        print(f"{fam['branching']}: Pearson(D, R) = "
              f"{fam['pearson_d_redundancy']:.4f}, "
              f"Pearson(D, chi_1) = {fam['pearson_d_chi']:.4f}, "
              f"Pearson(D, discord) = {fam['pearson_d_discord']:.4f}, "
              f"C(k = 0) = {fam['concurrence_k0']:.4f} -> "
              f"C(k = N) = {fam['concurrence_kN']:.4f}, "
              f"D in [{fam['d_min']:.4f}, {fam['d_max']:.4f}]")
    print(f"claim (xxi) verdict: {'PASS' if xxi['passed'] else 'FAIL'}")
    print()
    xxii = verdicts["claim_xxii_non_transfer"]
    print("sigma grid: " + ", ".join(
        f"{s}" for s in xxii["sigmas"]))
    print("gap (bits): " + ", ".join(
        f"{g:+.4f}" for g in xxii["gaps_bits"]))
    print("redundancy: " + ", ".join(
        f"{r:.1f}" for r in xxii["redundancies"]))
    print("discord(m = N): " + ", ".join(
        f"{d:.4f}" for d in xxii["discords_full_env_bits"]))
    print("mean concurrence: " + ", ".join(
        f"{c:.4f}" for c in xxii["concurrences"]))
    print(f"gap ratio 0.50/0.25 = {xxii['gap_ratio_050_over_025']:.4f}, "
          f"redundancy ratio = "
          f"{xxii['redundancy_ratio_050_over_025']:.4f}, "
          f"discord ratio = {xxii['discord_ratio_050_over_025']:.4f}")
    print(f"Pearson(gap, R) = {xxii['pearson_gap_redundancy']:.4f}, "
          f"Pearson(gap, discord) = {xxii['pearson_gap_discord']:.4f}, "
          f"Pearson(C, discord) = "
          f"{xxii['pearson_concurrence_discord']:.4f}")
    print(f"claim (xxii) verdict: "
          f"{'PASS' if xxii['passed'] else 'FAIL'}")
    print()
    print(f"{verdicts['n_passed']}/{verdicts['n_claims']} claims passed")


if __name__ == "__main__":
    main()
