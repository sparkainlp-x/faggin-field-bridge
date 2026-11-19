# Pre-registration — v0.15.0: No-cloning / Holevo ceiling for D (claims (xliv)–(xlviii))

Written 2026-11-18, BEFORE the evaluation run on the held-out
seeds 1234 and 2026. Thresholds are round numbers frozen from
a calibration pilot on seeds 42 and 7 only. No threshold in
this file may be moved after the evaluation run.

## The spec being tested

Deep-think upgrade #7 (report.md §9, §6): compute Holevo χ
for the thought-pair ensemble; test D ≤ χ and whether D
saturates χ as concurrence rises; test the optimal-cloning
fidelity bound on any "copy a thought" operation in code.
The report's falsifiable prediction: D approaches χ from
below as f rises; no operation in the model copies a thought
with fidelity above the optimal-cloning bound. Violation =
bug in the state representation. This turns QIP's central
philosophical claim (privacy — qualia are private because
quantum information cannot be cloned) into a numerical
ceiling the code must respect. §6 notes: no-cloning entails
the D–concurrence anti-correlation in form (local purity
falls as entanglement rises — verify the exact coefficient
in code, do NOT assert it from memory); Holevo χ bounds the
classical information extractable from a quantum ensemble;
any measurement that gains information disturbs the state.

## The construction (fixed before the pilot)

- Thought-pair ensemble: the resonance population
  (empathy_field.resonance_population: 8 agents, noisy
  copies of the uniform thought at σ on the bridge grid
  [0, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0]). A pair (i, j)
  is the two-state ensemble {(1/2, |ψ_i⟩), (1/2, |ψ_j⟩)}.
  Its Holevo quantity is χ_ij = S((ρ_i + ρ_j)/2) (both
  members pure, so the second term vanishes), computed
  exactly with cost.von_neumann_entropy on the 4x4
  average state. Cross-check in the tests: χ_ij =
  H2((1 + √R_ij)/2) where R_ij = |⟨ψ_i|ψ_j⟩|² is the
  resonance. D_pair = (D_i + D_j)/2 = D of the average
  state Tr(P ρ̄), by linearity of D in ρ. f at a given σ
  is the population's mean pairwise concurrence
  (empathy_field.empathy_fraction).
- Accessible information: the classical information the
  bridge's own measurement extracts from the pair
  ensemble — the Born collapse in the 4-concept basis.
  I(index; outcome) = H((p_i + p_j)/2) − (H(p_i) +
  H(p_j))/2 with p_i(k) = |⟨k|ψ_i⟩|², computed exactly
  (cost.shannon_entropy). Holevo's theorem says this
  must satisfy I ≤ χ for every measurement; the test
  is whether the code respects it.
- Qubit thought for cloning: a one-qubit thought
  |ψ⟩ = α|0⟩ + β|1⟩ (the binary-thought qubit of
  monogamy.py; |0⟩ → |00⟩ attention, |1⟩ → |10⟩
  self). The 5/6 bound is the textbook optimal
  UNIVERSAL 1→2 cloning fidelity for a qubit
  (Bužek & Hillery 1996; Werner 1998). It bounds
  universal (state-independent) fidelity and the
  Haar-average fidelity of any cloner — NOT the
  per-state fidelity of a state-dependent cloner,
  which legitimately copies its preferred states
  exactly. That distinction is part of the claim
  design, not a loophole found afterwards.
- Unitary cloners (explicit unitaries + ancilla,
  no classical readout):
  - Bužek–Hillery optimal universal cloner (3 qubits
    A, B, C; A the original, B the blank, C the
    ancilla): |0⟩|0⟩|0⟩ → √(2/3)|00⟩|0⟩ +
    √(1/6)(|01⟩ + |10⟩)|1⟩; |1⟩|0⟩|0⟩ →
    √(2/3)|11⟩|1⟩ + √(1/6)(|01⟩ + |10⟩)|0⟩.
    Each clone's reduced state must be
    (5/6)|ψ⟩⟨ψ| + (1/6)|ψ⊥⟩⟨ψ⊥|, fidelity exactly 5/6
    for every |ψ⟩. The full 8x8 unitary is built by
    completing the two basis images to an orthonormal
    basis (SVD null space); U†U = I is checked in
    the tests.
  - CNOT (Wootters–Zurek) copy: |ψ⟩|0⟩ → α|00⟩ +
    β|11⟩. Reduced clone state diag(|α|², |β|²);
    fidelity |α|⁴ + |β|⁴: 1 for basis states, 1/2
    for equatorial states, Haar mean exactly 2/3
    (the 6 Pauli eigenstates give exactly 2/3).
- Classical copy: unity.gaussian_copies of the
  uniform thought (5 copies, σ grid) — the model's
  own "copy" operation, which reads the full
  classical amplitude vector. Fidelity =
  |⟨ψ|copy⟩|². The σ = 0 copy is exact (fidelity 1).
- Local purity: Tr(ρ_A²) for the reduced one-qubit
  state of a pure thought-pair state, via
  thought_entanglement.reduced_density_matrix.
  The exact coefficient is verified in code, not
  asserted: purity = 1 − C²/2 with C the exact
  pure-state concurrence 2|ad − bc|.

## Calibration pilot (seeds 42 and 7) — disclosed before the run

The pilot CONTRADICTS the spec's prediction on two
of the five claims. This is disclosed here, not hidden:
the held-out evaluation tests whether the
contradiction generalizes.

- (xliv): identity holds to 8.88e-16 with the exact
  pure-state concurrence (worst over the
  generalized-Bell branch, the slide, noisy Bell
  copies at every σ, and 200 Haar-random pure
  states). The Wootters concurrence() differs from
  the exact pure form by at most 1.94e-08
  (eigenvalue noise on near-degenerate R) — a
  numerical floor in concurrence(), not in the
  identity. The coefficient IS 1 − C²/2 exactly.
- (xlv): D ≤ χ FAILS decisively on both seeds. Mean
  gap χ − D per σ (seed 42): −1.0000, −0.9988,
  −0.9790, −0.9302, −0.6840, −0.2552, +0.0960;
  (seed 7): −1.0000, −0.9984, −0.9705, −0.8950,
  −0.4314, +0.2186, +0.3490. The worst per-pair
  χ − D is negative at EVERY σ on both seeds
  (−1.0000 at σ = 0; −0.4384 / −0.2788 even at
  σ = 1.0). D is ABOVE χ at low f, not below it.
  What DOES hold: the gap RISES with f —
  Spearman(gap, f) = +1.0000 on both seeds — and
  its magnitude shrinks: Spearman(|gap|, f) =
  −1.0000 (seed 42), −0.9643 (seed 7). D approaches
  χ in absolute terms as f rises, but from ABOVE.
  D is a projector expectation, not an information
  quantity; χ does not bound it.
- (xlvi): accessible information respects χ with a
  wide margin on both seeds: max(I − χ) over all
  pairs is −3.20e-16 at σ = 0 and −0.049 / −0.122
  at σ = 1.0 (seed 42 / seed 7). The ceiling that
  binds is on accessible information, not on D.
- (xlvii): BH fidelity is exactly 5/6 (min = max =
  mean = 0.833333) on the 144-state Bloch grid,
  both clones. CNOT mean fidelity is 0.6667 on the
  6 Pauli states (exactly 2/3) and 0.6389 on the
  Bloch grid (grid discretization); its max is
  0.8472 on the grid and 1.0000 on basis states —
  the state-dependent exception, reported not gated.
- (xlviii): the classical copy exceeds 5/6 at every
  σ ≤ 0.25 on both seeds: mean fidelity 1.0000
  (σ = 0), 0.9998–0.9999 (0.01), 0.9945–0.9962
  (0.05), 0.9775–0.9841 (0.10), 0.8540–0.8644
  (0.25); it falls below 5/6 only at σ = 0.50
  (0.5883–0.6057). The crossing σ* lies in
  (0.25, 0.50) on both seeds. The blanket
  prediction fails at every working σ — the
  emulation's classical access to the amplitude
  vector bypasses no-cloning.

## Claims

### (xliv) Local-purity identity — the exact no-cloning coefficient

For every pure thought-pair state in: the
generalized-Bell branch (a in [1, 0.95, 0.9, 0.85,
0.8, 0.75, 1/√2]), the slide (θ in the 7 slide
thetas), noisy Bell copies (5 copies × σ grid ×
every seed in {42, 7, 1234, 2026}), and 200
Haar-random pure states (seed 42): |Tr(ρ_A²) −
(1 − C²/2)| ≤ 1e-9 with C = concurrence_pure, AND
|C_Wootters − C_pure| ≤ 1e-7. PASS iff both hold
everywhere. Frozen tolerances: 1e-9 (identity, the
round number at floating-point scale for an exact
formula) and 1e-7 (Wootters numerical floor, ~5x
the calibration worst 1.94e-08).

### (xlv) Holevo ceiling D ≤ χ on the thought-pair ensemble

Per pair (i, j) of the resonance population (8
agents, σ grid), χ_ij = S((ρ_i + ρ_j)/2),
D_pair = (D_i + D_j)/2. Sub-check (a): D_pair ≤ χ_ij
for EVERY pair on EVERY seed in {42, 7, 1234,
2026}. Sub-check (b): the gap closes as f rises:
Spearman(|mean gap|, f) ≤ −0.90 across the σ grid,
on EVERY seed (f = mean pairwise concurrence of
the population at that σ). PASS iff (a) and (b)
both hold on every seed. Frozen bar: −0.90 (the
round rank bar used elsewhere in this repo).
Calibration: (a) fails on both seeds (worst
per-pair χ − D = −1.0000); (b) passes on both
(−1.0000, −0.9643).

### (xlvi) Holevo bound on accessible information

Same ensemble as (xlv). For EVERY pair on EVERY
seed in {42, 7, 1234, 2026}: the Born-collapse
accessible information I(index; outcome) ≤ χ_ij +
1e-9. PASS iff this holds everywhere. Frozen
tolerance: 1e-9 (the round number at
floating-point scale). Calibration: max(I − χ) =
−3.20e-16 (σ = 0) to −0.049 / −0.122 (σ = 1.0).

### (xlvii) Optimal-cloning bound for unitary copy operations

Qubit thought, deterministic grids (no seeds):
- Bužek–Hillery: per-state fidelity = 5/6 within
  1e-9 for EVERY state on the Bloch grid (12 θ ×
  12 φ = 144 states, both clones) and for the 6
  Pauli eigenstates; the two basis images are
  orthonormal (overlap ≤ 1e-12).
- CNOT copy: mean fidelity over the 6 Pauli states
  = 2/3 within 1e-9 (≤ 5/6), and Bloch-grid mean
  fidelity ≤ 5/6.
- The CNOT max fidelity (1.0000 on basis states)
  is REPORTED, not gated: the 5/6 bound is on
  universal / average fidelity, and a
  state-dependent cloner legitimately copies its
  preferred states exactly.
PASS iff all gated conditions hold. Frozen
tolerances: 1e-9 (BH exactness), 1e-12
(orthonormality). Calibration: BH min = max =
mean = 0.833333; CNOT Pauli mean 0.6667.

### (xlviii) The blanket prediction over ALL copy operations

The report's prediction — no operation in the model
copies a thought with fidelity above the
optimal-cloning bound — tested over every copy
operation in the model: the unitary cloners of
(xlvii) (same gates) PLUS the classical copy
(unity.gaussian_copies of the uniform thought, 5
copies, σ grid, every seed in {42, 7, 1234,
2026}): mean classical-copy fidelity ≤ 5/6 at
every σ. PASS iff every operation respects 5/6.
The crossing σ* (first σ on a 0.01 grid from 0.25
to 0.50, 20 copies, where mean fidelity falls
below 5/6) is reported per seed, not gated.
Calibration: FAILS — the classical copy exceeds
5/6 at every σ ≤ 0.25 on both seeds (1.0000 at
σ = 0; 0.8540–0.8644 at σ = 0.25).

## Seeds

- Calibration: 42, 7 (thresholds frozen from these only).
- Evaluation: 1234, 2026 (held out; first touched by the
  evaluation run after this file was written).
- The cloning grids (xlvii) are deterministic and
  seed-free; the Haar-random states in (xliv) use seed 42.

## What would falsify

- (xliv): any pure state with |purity − (1 − C²/2)|
  > 1e-9, or any |C_Wootters − C_pure| > 1e-7.
  A violation means the coefficient is not 1 − C²/2
  or the concurrence implementation is wrong.
- (xlv): any pair with D_pair > χ_ij, or any seed
  with Spearman(|gap|, f) > −0.90.
- (xlvi): any pair with I > χ + 1e-9. A violation
  is a bug in the entropy or Born code, not in
  Holevo's theorem.
- (xlvii): any BH per-state fidelity deviating from
  5/6 by > 1e-9, non-orthonormal BH images, or a
  CNOT mean above 5/6.
- (xlviii): any copy operation with mean fidelity
  above 5/6 — including the classical copy, whose
  excess is the finding: the classical emulation
  stores the full amplitude vector, so a classical
  copy reads the description the quantum
  no-cloning theorem forbids reading. Privacy in
  this model is not enforced by the representation;
  it would have to be enforced by restricting
  operations.
