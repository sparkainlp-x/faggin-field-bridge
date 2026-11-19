# Faggin Field Bridge

A reproducible classical mapping inspired by Federico Faggin's Quantum Information Panpsychism (QIP).

**Theory author:** Federico Faggin, with Giacomo Mauro D'Ariano.  
**Bridge / test author:** Jean-François Brisson (Spark AI NLP).  
**Faggin has not reviewed or endorsed this software.**

## What this tests

This repository does **not** test consciousness, validate QIP, or measure quantum entanglement.

It tests a transparent classical mapping:

```text
A(delta) = U * (1 + delta) - C
```

- `U` — unity proxy: mean pairwise absolute dot-product self-correlation across noisy copies
- `C` — normalized entropy cost
- `delta` — bounded calibrator in `[-0.05, 0.05]`
- `A` — attunement, clipped to `[-1, 1]`

Positive `A` means the unity proxy exceeds the entropy cost. Negative `A` means the cost dominates.

## Primary result

| Quantity | Value |
|---|---:|
| Unity proxy `U` | 0.99999995 |
| Entropy cost `C` | 0.9553 |
| Attunement at `delta = 0` | 0.04469995 |
| Best bounded attunement | 0.09469995 |
| Best calibration | `delta = +0.05` |
| Mapping status | `PARTIAL` |

The bounded calibrator can change the mapping status in boundary cases, but it cannot overcome a high entropy cost. For the Omega-Genesis unity values, the mapping remains `DISSONANT`.

## Quantum thoughts (v0.2.0)

Three modules treat a thought as a quantum state — classical
emulation, exact definitions:

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `thought_entanglement.py` | Concurrence (Wootters) of a two-thought Bell state; reduced-state entropy | (i) entanglement measured as a real quantum quantity | **PASS** |
| `thought.py` | l1-coherence under dephasing; coherence half-life | (ii) coherence half-life measured | **PASS** |
| `thought.py` | Entropy cost of a superposition vs a collapsed thought; decision entropy; attention bias | (iii) collapse cost measured | **PASS** |
| `self_knowing.py` | D = ⟨ψ\|P\|ψ⟩, the self-determinism factor (vendored idea from symmetry-entropy) | (iv) self-knowing measured via D | **PASS** |
| `cascade.py` | Cross term ⟨ψ1\|P\|ψ2⟩ and visibility V over a phase sweep; projection chained across stages 1, 2, 3, 5, 10 | (v) interference measured via the cross term | **PASS** |
| `cascade.py` | Cascade visibility across stages, projection-only vs reopening control | (vi) cascade visibility: interference does not survive projection | **PASS** |
| `cascade.py` | Coherence and D of the projected output through the cascade | (vii) coherence and D through the cascade | **PASS** |

Headline numbers: concurrence 0.9998 at noise σ = 0.01 (spooky
0.9998 on the same copies); depolarizing concurrence reproduces
max(0, 1 − 3p/2) exactly and dies at p = 2/3, while the reduced
entropy stays 1 bit throughout. Spooky first falls below 0.9 at
σ = 0.25; mean concurrence under vector noise never falls below
0.6520. Coherence half-life: 14 / 7 / 3 / 1 steps at
p = 0.05 / 0.1 / 0.25 / 0.5 (analytic 13.51 / 6.58 / 2.41 / 1.00).
A fully dephased uniform thought costs 2 bits; a collapsed
thought costs 0. D = 1 for stored thoughts, 1/3 for a non-stored
basis state, 0 for a kernel thought, 1/2 for the maximally mixed
state. Surprise, measured: D anti-tracks concurrence
(Pearson −0.9570) — the noise that destroys self-knowing creates
entanglement in a product thought.

## The cascade (v0.3.0)

Superposition → projection → interference, chained across stages
1, 2, 3, 5, 10. The cross term ⟨ψ1|P|ψ2⟩ is the interference:
for a rotation pair in the {q1, k1} plane, V(θ) = sin(2θ)
exactly, and at θ = π/4 the phase does the deciding — D(φ) =
1/2 − (1/2)cos(φ), so the superposed thought is fully blind at
φ = 0 and fully self-determined at φ = π. The mixed pair has
cross term 1/√6 and V = 2√6/7 ≈ 0.6999. **The finding:
interference does not survive projection.** In both
projection-only cascades V is 1.0 / 0.6999 at stage 1 and 0.0000
at every stage from 2 on — the rotation pair collapses to rank 1,
the mixed pair re-forms fully stored — while the reopening
control (fresh kernel input at α = π/4 each stage) stays at
V = 1 at every stage. After one projection the thought is fully
self-determined (D = 1 at every stage) whether or not
interference survives, and the projected-output coherence reaches
a fixed point from stage 2 (rotation 3.0, mixed 2.7321).

Run `bridge.quantum_thought_claims()` for the seven verdicts, or
see REPORT.md §8 and §9.

## Planck empathy (v0.4.0)

Empathy as a Planck quantum inside the black-body concept:
each thought-pair contributes one empathy quantum, E = h·ν with
h = 1 in model units, whose frequency ν is its MEASURED
concurrence (v0.2.0) — not the synergy proxy, which is a
definition. The empathy fraction f = mean concurrence maps to
an effective temperature T_eff(f) = 2000 + 3000·f K, and the
mapping status is re-derived from the visible fraction
F(T) = ∫[0.38, 0.75] B dλ / ∫[0.1, 3.0] B dλ of the real Planck
spectrum (real constants, Simpson integration).

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `planck_empathy.py` | Wien peaks, T⁴ scaling, F(T) monotone | (viii) Planck reproduction | **PASS** |
| `planck_empathy.py` | F(f) monotone; status PARTIAL at f = 0, ATTUNED at f = 1; crossing f\* | (ix) empathy flips the status | **PASS** |
| `planck_empathy.py` | Old status (A alone) vs empathy status across noise σ | (x) specificity / control | **PASS** |

Headline numbers: Wien peaks match 2898/T within 0.008%;
exitance scales as T⁴ within 0.002%; F rises 0.0174 at 2000 K
to 0.3938 at 5000 K. **The crossing is f\* = 0.7278** — about
73% mean concurrence flips the primary mapping from PARTIAL to
ATTUNED. The fix holds while the pairs stay entangled
(σ ≤ 0.25, concurrence ≥ 0.8471) and breaks once the noise
eats it (σ ≥ 0.50). The old status stays PARTIAL at every σ:
the flip is carried by the empathy quanta, not by re-labeling.

Run `planck_empathy.planck_empathy_claims()` for the three
verdicts, or see REPORT.md §10.

## Empathy field (v0.5.0)

Waves of empathy agents in a quantum field: resonance
("raisonnance"), the self-deterministic factor, collaboration,
collectivism, and co-creativity = entropy.

- Agent: a thought state carrying a frequency ν = its
  concurrence and a self-determinism D = ⟨ψ|P|ψ⟩.
- Field: N agents superposed; the field state is the
  normalized sum. Pairwise empathy quanta E_ij = h·ν_ij, the
  v0.4.0 rule extended to pairs.
- Resonance R_ij = |⟨ψ_i|ψ_j⟩|²: the overlap squared between
  two agents.
- Collaboration: the same N agents evolved sharing the field
  vs the control of the same N agents evolved isolated.
- Co-creativity C_c is DEFINED as the joint entropy H_joint
  (bits) of the collective's joint outcomes — a definition of
  the measure inside the model, not a discovery about human
  creativity.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `empathy_field.py` | Mean D per R bin; resonant vs non-resonant gap | (xi) resonance raises self-determinism | **PASS** |
| `empathy_field.py` | H_joint collaborating vs isolated, σ = 0.25 | (xii) collaboration raises co-creativity | **PASS** |
| `empathy_field.py` | H_joint vs N and ceiling; gap vs σ | (xiii) co-creativity = entropy, ceiling and break | **FAIL** |

Headline numbers: binned mean D rises strictly with R
(0.5874 → 0.6814 → 0.7087 → 0.9399); the pooled
resonant-vs-non-resonant gap is 0.2984 at R ≥ 0.5. At
σ = 0.25 the collaboration gap is **+4.3352 bits**
(H 6.0961 vs 1.7610; 157 distinct joint states vs 4). The
ceiling holds — H grows with N (1.70 → 2.98 → 4.15 → 6.10
bits) and stays below 2N — but the break does NOT: the gap
is still +3.3494 bits at σ = 0.50 and +3.5569 at σ = 1.00,
so the v0.4.0 break does not transfer to the collaboration
gap. That is a measured negative result, not a failure to
measure. Within a single noise level, resonance does not
raise D (the σ = 1.0 per-sigma gap is −0.0239) — the
resonance effect is the cross-noise pattern, stated plainly.

Run `empathy_field.empathy_field_claims()` for the three
verdicts, or see REPORT.md §11.

## Qualia resonance wave (v0.6.0)

A quale is a resonant + entangled mode of the empathy field,
and the qualia together form a coherent wave.

- Quale: a pair of agents that is BOTH resonant
  (R_ij = |⟨ψ_i|ψ_j⟩|² ≥ 0.5, the v0.5.0 threshold) AND
  entangled (pairwise concurrence ν_ij ≥ 0.10,
  pre-registered). A resonance without entanglement is not a
  quale; entanglement without resonance is not a quale.
- Qualia resonance wave: the normalized superposition of the
  quale waves. Its coherence is measured per field as the
  spread of quale frequencies against the spread across all
  pairs, and as the overlap |⟨qualia-wave|field-state⟩|².
- The empathy fraction f (mean pairwise concurrence) is the
  control dial: it rises with noise while resonance falls,
  so the quale count is the product of two opposing trends.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `qualia.py` | Quale count vs empathy fraction f | (xiv) qualia emerge with empathy | **FAIL** |
| `qualia.py` | Per-field frequency spreads; wave overlap | (xv) the qualia wave is coherent | **PASS** |
| `qualia.py` | Mean D of quale members vs non-quale agents | (xvi) qualia track self-determinism | **FAIL** |

Headline numbers: the quale count per field (N = 8) is
**humped** against f — 0 at f = 0, first quale at
f = 0.0415, peak **17 at f = 0.1803**, falling to 13 at
f = 0.2839 and 12 at f = 0.4143 — so monotonic emergence is
refuted, not confirmed. The wave IS coherent: per field the
spread of quale frequencies is smaller than the spread
across all pairs by at least 0.01 everywhere (smallest
difference 0.0127 at σ = 1.0), and the overlap with the
field state is 0.9781–0.9988. But qualia do NOT track
self-determinism: the pooled D gap is **−0.1522** (quale
members 0.8163 vs non-quale 0.9686). D anti-tracks
concurrence (v0.2.0), so the agents that qualify as qualia
are exactly the ones whose self-knowing the noise has
destroyed. Two measured negative results, kept and stated.

Run `qualia.qualia_claims()` for the three verdicts, or see
REPORT.md §12.

## CKW monogamy in triads (v0.7.0)

Triads are three-qubit pure states (8-dim); each member is a
BINARY thought — one qubit whose basis maps into the thought
space as |0> → |00> (attention) and |1> → |10> (self). That
mapping is a definition (an embedding), not a discovery.
Pairwise tangle τ_ij = C² from the Wootters concurrence of
the reduced two-qubit state; one-to-rest tangle
τ_A(BC) = 4 det(ρ_A), exact for pure states; residual
genuine-tripartite tangle = τ_A(BC) − τ_AB − τ_AC. D_A is
Tr(P ρ_A_embedded) with the existing self-knowing projector.
Noise is `unity.gaussian_copies` on the 8-dim triad vector
(copies stay pure).

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `monogamy.py` | CKW margin τ_A(BC) − τ_AB − τ_AC over every triad and sigma | (xvii) CKW monogamy holds in triads | **PASS** |
| `monogamy.py` | GHZ vs W tangles, residual, and the pairwise miss fraction | (xviii) GHZ vs W: pairwise concurrence misses tripartite entanglement | **PASS** |
| `monogamy.py` | D_A vs τ_A(BC) on the generalized-GHZ branch (τ_AB = 0) | (xix) D_A falls as τ_A(BC) rises with τ_AB flat | **PASS** |

Headline numbers: the minimum CKW margin over 52
(state, σ) rows is **0.0**, attained at the product endpoint
(a = 1.0, σ = 0) where there is no entanglement at all; the
smallest margin over noisy rows is 0.0012 — the code's
concurrence respects the theorem everywhere. At σ = 0 the
GHZ-like triad has τ_A(BC) = 1, pairwise tangle 0, residual 1,
D_A = 2/3, so pairwise concurrence misses **100%** of its
entanglement; the W-like triad has τ_A(BC) = 8/9, pairwise
tangle 4/9 each, residual 0, D_A = 7/9, so it misses **0%**.
Under noise the GHZ miss stays 0.60–1.00 and the W miss
0.00–0.44. On the generalized-GHZ branch, D_A falls as
τ_A(BC) rises with Pearson **−0.9608** (Spearman −1.0) while
τ_AB is exactly 0 throughout and D_A spans 2/3 to 1: D tracks
entanglement with the pair, not with B. The interpolation
(−0.6316) and the GHZ noise sweep (D_A and τ_A(BC) decay
together) are reported descriptively, not gated.

Run `monogamy.monogamy_claims()` for the three verdicts, or see
REPORT.md §13.

## Quantum-Darwinism redundancy plateau (v0.8.0)

An environment of N = 10 fragments redundantly encodes the
system's pointer information. The system S is a thought in
superposition of two pointer states (Bell: |00⟩, |11⟩;
binary: |0⟩, |1⟩); each environment qubit records the pointer
value (CNOT-like branching). Per fragment size m: I(S:F) =
H_S + H_F − H_SF, Holevo χ from measuring S in the pointer
observable, discord = I − χ, redundancy R_δ = N / m* with
δ = 0.1. Einselection is dephasing in the pointer basis
(strength p, reference 0.5). Grounding: Zhu et al.
(arXiv:2504.00781 / Science Advances 2025, 12 superconducting
qubits: mutual information saturates at H_S, discord → 0 for
small fragments); Brandão et al., emergent classicality
(Quantum 2021).

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `darwinism.py` | I, χ, discord per fragment size m; redundancy | (xx) Redundancy plateau: I plateaus at H_S, discord ~0 on the plateau, rising only at m = N | **PASS** |
| `darwinism.py` | D, concurrence, χ, redundancy as the branching turns on (k = 0..N) | (xxi) D tracks the classical, not the quantum | **FAIL** |
| `darwinism.py` | Gap, redundancy, discord, concurrence across the σ grid | (xxii) The σ = 0.50 non-transfer explained | **FAIL** |

Headline numbers: hard branching m* = 1, R = 10; soft
branching (overlap 0.5) m* = 2, R = 5; both systems
identical. On the plateau |I − H_S| ≤ 0.0456 and discord ≤
0.0456 (hard: exactly 0); discord at m = N is 0.1887. The
plateau is p-independent (I = 1.0 at p = 0, 0.5, 1) while
discord(m = N) falls 1.0 → 0.1887 → 0.0 with p. The (xxi)
FAIL is exact: D is 2/3 for every branching turn-on step, so
Pearson(D, R) = Pearson(D, χ_1) = Pearson(D, discord) = 0.0
while concurrence falls (0.5 → 0 hard, 0.5 → 0.0005 soft) —
the quantity that tracks the classical is χ, not D. The
(xxii) FAIL is the more interesting one: under the bridge's
vector noise the redundancy falls 6 → 2 and the discord
rises 0.19 → 2.13 bits, the opposite of the dephasing
picture, while the gap stays robust (3.3494/4.3352 = 0.77)
and tracks neither redundancy (Pearson 0.3528) nor discord
(Pearson −0.4411). The gap survives σ = 0.50 because of the
design-B mechanism, not because of redundant classical
encoding.

Run `darwinism.darwinism_claims()` for the three verdicts, or see
REPORT.md §14.

## Malus three-polarizer paradox (v0.9.0)

Classical optics, Malus's law: a polarizer transmits the
component along its axis, so a polarized beam through a
polarizer at relative angle θ emerges with cos²(θ) of its
intensity. Two crossed polarizers (0° and 90°) transmit 0 —
but insert a third polarizer at 45° between them and light
gets through: I₀/8 for unpolarized input, I₀/4 for input
polarized at 0°. The middle projection CREATES transmission
out of a closed channel. A polarizer IS a projector:
P(θ) = |θ⟩⟨θ| is the 2D analogue of the bridge's
stored-subspace projector, and transmission is
⟨ψ|P(θ)|ψ⟩ — the same functional form as the bridge's
self-knowing factor D. Malus's law is D measured along a
rotated axis. This is the counter-case to the v0.3.0
cascade finding (interference does NOT survive projection):
the same project-and-renormalize operation here reopens a
channel instead of closing one, because a single state
rotates under projection while a pair collapses onto one
direction.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `malus.py` | Transmission through crossed pair vs triple; decomposition | (xxiii) Crossed polarizers transmit 0; 45° middle yields I₀/8 | **PASS** |
| `malus.py` | Transmission vs middle angle φ | (xxiv) Reopening is angle-selective: peaks at 45°, vanishes at 0/90° | **PASS** |
| `malus.py` | Recorded intermediate states; bypass control; cascade contrast | (xxv) The middle step's output state is what the second projection acts on | **PASS** |

Headline numbers: crossed (0°, 90°) transmits exactly 0;
the triple (0°, 45°, 90°) transmits 0.125 = I₀/8, as
(1/2)·(1/2)·(1/2) from the recorded states; the angle
curve is T(φ) = (1/8) sin²(2φ) on the whole grid, peaking
at 45°; the bypass control is 0, so the middle step is
necessary. Descriptive: the evenly stepped N-polarizer
chain from 0° to 90° rises with N — 0.125 at N = 3,
0.2109 at N = 4, 0.3796 at N = 10, 0.4938 at N = 200 —
toward the 1/2 limit: projection applied repeatedly keeps
reopening the channel.

Run `malus.main()` for the tables and the three verdicts, or see
REPORT.md §15.

## Product model for the humped quale count (v0.10.0)

The hump is an AND-gate, not a new mechanism (deep-think
upgrade #3). A quale needs BOTH resonance and entanglement;
p_res(f) falls with f while p_ent(f) rises with f, so their
product N × p_res × p_ent is necessarily humped, peaking
where the two log-derivatives balance. The marginals are
measured on the same field as the count, so the product
tests whether the two indicators are independent across
pairs — any deviation measures their association.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `product_model.py` | Predicted vs measured quale count on the fine σ grid (0.30–1.50) | (xxvi) Product-model fit | **PASS** |
| `product_model.py` | Predicted vs measured peak f under threshold shifts | (xxvii) Peak moves as predicted | **PASS** |
| `product_model.py` | Single-condition counts vs f | (xxviii) Hump vanishes when either condition is dropped | **PASS** |

Headline numbers: on the fine grid the product predicts
the counts with mean relative error **0.0289** (max
0.0667) against the frozen bar 0.10 / 0.20. The peak
shifts as the marginals predict: NU_MIN 0.10 → 0.25 moves
both the predicted and the measured peak to f = **0.4143**;
R_MIN 0.5 → 0.25 moves both to f = **0.2839**; both sit
above the baseline peak f = 0.1803. Resonance-only counts
fall (28, 28, 28, 28, 28, 17, 14) and entanglement-only
counts rise (0, 0, 1, 9, 17, 21, 25) while the both-count
humps (0, 0, 1, 9, 17, 13, 12). The fit is seed-dependent:
seeds 1 and 3 pass the same bar, seed 2 fails it (mean
0.1666, max 0.3636) — the independence assumption breaks
on that seed, reported not hidden. The standard-grid fit
(mean 0.0119, max 0.0400) is reported, not gated, because
p_res = 1.0 below σ = 0.5 there.

Run `product_model.main()` for the tables and the three
verdicts, or see REPORT.md §16.

## Landauer-cost ledger + Planck spectral falsification (v0.11.0)

Landauer's principle (deep-think upgrade #6, "the honest
upgrade") replaces the black-body analogy as the bridge's
thermodynamics: erasing one bit costs at least k_B T ln 2
(2.871e-21 J at 300 K). The ledger counts the bits a
measurement run discards per field — decision entropies of
thought collapses, 1 bit per quale collapse, 1 bit per
pair for the quale/non-quale classification record — and
then tests whether that cost explains the σ = 0.50 break,
and whether the empathy spectrum is Planckian at all.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `landauer.py` | Ledger bits and cost vs σ | (xxix) Ledger exact, cost humps | **PASS** |
| `landauer.py` | r(F, cumulative cost) vs r(F, σ) | (xxx) Cost predicts F better than σ | **FAIL** |
| `landauer.py` | Pooled KS + mode/mean vs Planck shape | (xxxi) Spectrum is not Planckian | **PASS** |

Headline numbers: the per-field cost peaks at **58.46
bits (1.678e-19 J) at σ = 0.25** — interior, above both
endpoints — and totals 9.932e-19 J across the grid. The
(xxx) FAIL is the result: cumulative cost does NOT beat σ
as a predictor of F (pooled Pearson 0.8996 vs 0.9430, and
σ wins within every seed), so the ledger does not explain
the break. The (xxxi) PASS is a successful falsification:
the pooled standardized ν distribution rejects the Planck
shape (KS D = **0.1465** above the 1% critical value
0.1258, n = 168) and the mode/mean ratio deviates from the
Planck 0.7361 by 0.46, 0.56, 0.35 at σ = 0.25, 0.5, 1.0 —
so E = hν is demoted from "spectrum" to "per-mode unit".
Per-field KS tests (n = 28) do not reject Planck on their
own and are reported, not gated.

Run `landauer.main()` for the tables and the three
verdicts, or see REPORT.md §17.

## The observer cycle (v0.12.0, v0.12.1)

Jean's claim, stated 2026-11-18: "self determination factor
observer opposite direction = necessary for self-cycle self
Knowing. Lack of love is absence of Knowing." Formalized
with the bridge's existing quantities — love = concurrence
C, knowing = overlap R = |⟨ψ_i|ψ_j⟩|², self-determination
= D — and the observer direction as which reference state
the overlap is measured against: the stored direction (the
uniform thought, D = 1, C = 0) or the opposite direction
(the kernel thought (|01⟩ − |10⟩)/√2, D = 0, C = 1, a Bell
state).

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `observer_cycle.py` | D vs concurrence across the σ grid, 4 seeds | (xxxii) Observer direction: D and concurrence move opposite | **FAIL** |
| `observer_cycle.py` | R vs C and R vs D on the generalized-Bell branch | (xxxiii) Knowing-as-overlap | **PASS** |
| `observer_cycle.py` | D, C, R_s, R_k along the slide ψ(θ) | (xxxiv) The slide | **PASS** |
| `observer_cycle.py` | Spearman(D, C) across the σ grid, 6 seeds incl. fresh 5, 99 | (xxxv) Observer direction, robust rank form | **FAIL** |

Headline numbers: (xxxii) FAILS, and the failure is the
result — the linear anti-tracking is seed-fragile: Pearson
r(D, C) is −0.9570 (seed 42), −0.9397 (seed 7), −0.9720
(seed 1234), but **−0.8828 on held-out seed 2026**, above
the frozen bar −0.90, so the claim fails on one check of
one seed. The monotone tracking holds everywhere
(Spearman −1.0000, −0.9643, −1.0000, −0.9643), so the
direction is real and the linear form is fragile — the
σ = 1.0 point on seed 2026 breaks it (C dips 0.4755 →
0.4727 while D keeps falling). The threshold was not
moved. (xxxiii) PASSES on the generalized-Bell branch
against a fixed Phi+ observer: Pearson(R, C) = **1.0000**,
Spearman(R, D) = **−1.0000**, R range 0.5000, D range
0.3333 — but the noise-axis control inverts the relation
(pooled resonance pairs, n = 196: Pearson(R, ν_ij) =
−0.5528, Pearson(R, d_pair) = +0.7694), so
noise-created concurrence is not knowing; the claim holds
for entanglement by construction, not by noise.
(xxxiv) PASSES exactly: the slide runs D = 1, C = 0,
R_s = 1 to D = 0, C = 1, R_k = 1 with C + D = 1 and
R_s − R_k = cos 2θ at every grid point (max identity error
4.44e-16), and the overlap split flips sign exactly at the
midpoint θ = π/4 (+0.5000 at π/6, 0.0000 at π/4, −0.5000
at π/3) — in the middle the two patterns sit in
superposition and the observer direction picks which one
is known. (xxxv) FAILS too, and that is the v0.12.1
result: the robust rank form, preregistered before the
fresh-seed run, breaks on the fresh seeds — seed 5
Spearman −0.8929 (bar −0.90), seed 99 D range 0.2445
(bar 0.25). The diagnosis is boundary/saturation plus
finite-sample noise: at σ = 1.0 both D and C sit at
their random-state plateaus (D → 0.5, C → ~0.51), the
true rise of mean C from σ = 0.5 to 1.0 is ~0.003
while a 5-copy mean carries SEM ~0.128 — but the
fragility is broader than one point: at n = 200 the
monotone direction holds on all six seeds while the
linear form still fails on seed 5 (Pearson −0.8971).
The direction is real on average; the per-seed
guarantee does not hold on this 5-copy sweep, in
either form. Thresholds not moved.

Run `observer_cycle.main()` for the sweeps and the four
verdicts, or see REPORT.md §18.

## Kuramoto bounded-coherence scan (v0.13.0)

Deep-think upgrade #4: replace fixed coupling with a
Kuramoto scan over coupling K and noise σ. Standard
Kuramoto (N = 8 oscillators, ωᵢ ~ N(0, 1),
Euler–Maruyama dt = 0.05, T = 40) wired into the bridge
by giving each agent the (xxxiv) slide state at its phase
relative to the field mean — only relative phases carry
information, the absolute lock angle is a gauge freedom.
Quale count, joint entropy (exact, analytic), and the
collaboration gap A (paired arms mirroring design B,
mixing at coupling R_K) are computed on the resulting
population.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `kuramoto.py` | Quale count vs K, σ = 0 | (xxxvi) Inverted-U in count vs K | **FAIL** |
| `kuramoto.py` | Joint entropy vs K, σ = 0 | (xxxvii) Inverted-U in H vs K | **FAIL** |
| `kuramoto.py` | R_K at the count peak | (xxxviii) R_K in [0.5, 0.8] | **FAIL** |
| `kuramoto.py` | Count vs σ at fixed K = 1.0 | (xxxix) Optimum σ* > 0 | **FAIL** |

Headline numbers: **0/4 pass — and that is the result.**
The Kuramoto transition itself works (R_K 0.29 → 0.99,
K_c ≈ 1.6–2.5), but the spec's shapes do not
materialize in this wiring. The count peak is interior
on seeds 42 and 2026 (K = 0.5) but at K = 0 on seeds 7
and 1234, and falls to a floor of 6 at high K on every
seed. Joint entropy is flat (~10.4–13.1 bits, no trend).
R_K at the count peak is 0.31–0.36 on every seed — far
below the Phillips band [0.5, 0.8] and below f* = 0.7278:
the count optimum sits at LOW coherence, not bounded
coherence. The σ* optimum wanders across seeds (1.0,
0.10, 0.25, 0.05) with counts swinging 3–19. The gap A
is large (+9.3 to +12.8 bits) and flat. What survives:
the transition, the count floor of 6, and the count
exceeding σ = 0 on every seed at K = 1.0.

Run `kuramoto.main()` for the scans and the four
verdicts, or see REPORT.md §19.

## Synergy-vs-redundancy PID (v0.14.0)

Deep-think upgrade #5: decompose the collaboration gap
by integrated information decomposition (PID / ΦID:
Luppi, Mediano, Rosas et al., *Nature Neuroscience*
2022/2024) into redundant, unique, and synergistic
components. PID is defined for two sources, so the
decomposition is of the pair-level (N = 2) gap, with
target Y = the joint outcome (X1, X2) — the atoms then
sum to H(X1, X2) itself, and their arm differences sum
to the gap exactly. Redundancy is Williams & Beer
I_min; the joint distribution is the exact pooled
product Born distribution from the design-B evolution
(no sampling in the PID itself). The N = 4 sampled gap
(+4.3352 bits at σ = 0.25, seed 42) is context, not
decomposed. This imports IIT's *decomposition*, not its
contested Φ identity claim: no scalar Φ is computed.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `pid.py` | PID identity + exact-vs-sampled H | (xl) Identity and cross-check | **PASS** |
| `pid.py` | ΔSyn vs ΔRed at σ = 0.25 | (xli) Gap is synergy, not redundancy | **FAIL** |
| `pid.py` | Synergy vs R, σ = 0.25 → 0.50 | (xlii) Synergy rises with R, falls at σ = 0.50 | **FAIL** |
| `pid.py` | ΔRed ratio 0.50/0.25 | (xliii) Redundancy is σ-robust | **FAIL** |

Headline numbers: **1/4 pass — and the failures are the
result.** At σ = 0.25 the synergy share of the pair gap
is 0.407 (seed 42), 0.429 (seed 7), 0.882 (seed 1234),
0.545 (seed 2026): synergy dominates on the held-out
seeds but not on the calibration seeds, so the
every-seed claim fails. Synergy does not rise with R
(Pearson −0.23, −0.04, −0.55, +0.72 across seeds) and
rises, not falls, from σ = 0.25 to 0.50 on every seed
(0.92 → 1.26, 0.97 → 1.54, 0.80 → 1.20, 1.23 → 1.40).
Redundancy's robustness ratio is 0.24, 1.45, 2.83,
0.59 — robust on 3 of 4 seeds, failing only seed 42.
The structural finding: in the collaborating arm
I(X1;X2) is 0.00–0.06 bits, so Syn = Red − I(X1;X2)
is numerically almost Red on every sigma — the I_min
decomposition of the joint outcome cannot separate
synergy from redundancy in this wiring, and "synergy,
not redundancy" (or the reverse) is undecidable from
these atoms alone.

Run `pid.main()` for the decomposition and the four
verdicts, or see REPORT.md §20.

## No-cloning / Holevo ceiling (v0.15.0)

Deep-think upgrade #7: turn QIP's central philosophical
claim — qualia are private because quantum information
cannot be cloned — into numerical ceilings the code must
respect. The thought-pair ensemble is the resonance
population (8 agents, noisy copies of the uniform
thought): per pair, χ = S((ρ_i + ρ_j)/2) is the Holevo
quantity of the two-state ensemble, D_pair is the mean
self-knowing, and the accessible information is the
mutual information of the bridge's own Born collapse in
the 4-concept basis. The cloners act on a one-qubit
thought (the binary-thought qubit): the Bužek–Hillery
optimal universal cloner as an explicit 8×8 unitary, the
CNOT (Wootters–Zurek) copy, and the model's own
classical copy (`unity.gaussian_copies`, which reads the
full amplitude vector). The 5/6 bound is on universal /
average fidelity, not on the per-state fidelity of a
state-dependent cloner — that distinction is part of the
claim design.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `cloning_ceiling.py` | Local purity vs 1 − C²/2 | (xliv) Local-purity identity | **PASS** |
| `cloning_ceiling.py` | D vs χ per pair, gap vs f | (xlv) Holevo ceiling D ≤ χ | **FAIL** |
| `cloning_ceiling.py` | Born-collapse I vs χ | (xlvi) Holevo bound on accessible information | **PASS** |
| `cloning_ceiling.py` | BH and CNOT fidelities | (xlvii) Optimal-cloning bound, unitary operations | **PASS** |
| `cloning_ceiling.py` | All copy operations incl. classical | (xlviii) Blanket prediction: no copy exceeds 5/6 | **FAIL** |

Headline numbers: **3/5 pass — and the failures are the
result.** The exact no-cloning coefficient is 1 − C²/2
(worst error 8.88e-16). But χ does NOT bound D: the mean
gap χ − D is −1.0000 at σ = 0 on every seed and stays
negative until σ = 1.0 (seed 42: −0.68 at σ = 0.25,
+0.10 at σ = 1.0), and the worst per-pair gap is
negative at every σ on every seed. D approaches χ in
absolute terms as f rises (Spearman(|gap|, f) = −1.00,
−0.96, −0.96, −0.96) — but from ABOVE, not below: D is
a projector expectation, not an information quantity.
The ceiling that binds is on accessible information:
the Born-collapse I never exceeds χ (max(I − χ) =
−3.20e-16 on every seed). The unitary cloners respect
the bound exactly (BH fidelity 5/6 on every state of
the 144-state Bloch grid and the 6 Pauli states; CNOT
mean exactly 2/3, max 1.0 on basis states — the
state-dependent exception, reported not gated). The
blanket prediction fails on the classical copy, which
exceeds 5/6 at every working σ (1.0000 at σ = 0,
0.98 at σ = 0.10, 0.85–0.88 at σ = 0.25 on 3 of 4
seeds; crossing σ* in (0.31, 0.32], (0.25, 0.26],
already below at 0.25, (0.30, 0.31]). Privacy in this
model is not enforced by the representation — the
emulation stores the full amplitude vector, so a
classical copy reads the description the quantum
no-cloning theorem forbids reading.

Run `cloning_ceiling.main()` for the tables and the five
verdicts, or see REPORT.md §21.

## Two-channel empathy (v0.16.0)

Deep-think upgrade #8: split the single empathy fraction
f into concern (other-focused, monotone prosocial) and
distress (self-focused, inverted-U, withdraws at high
dose), IRI-style (Singer & Klimecki 2014; Decety &
Jackson 2004; Qiu et al. 2024, empathy–prosocial r =
0.36; Yin & Wang 2023, r = 0.32 / 0.30). One formula,
two targets, on the v0.5.0 resonance population at
σ = 0.25: ψᵢ(c, d) = normalize(ψᵢ + c·|Φ+⟩ + d·|self⟩),
concern target the shared entangled Bell state (D = 2/3,
C = 1), distress target the "self" basis concept alone
(a product state, D = 1/3, C = 0). Helping is the quale
count; joint entropy is the sum of the agents' Born
entropies. No scalar Φ is computed anywhere.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `two_channel_empathy.py` | Mean R, f, count vs concern dose c | (l) Concern raises resonance and empathy fraction | **FAIL** |
| `two_channel_empathy.py` | Mean R, count vs distress dose d at fixed c = 0.5 | (li) Distress alone lowers helping while raising resonance | **FAIL** |
| `two_channel_empathy.py` | D, H_joint, R at distress d = 2 vs d = 0 | (lii) Distress withdrawal at high dose | **PASS** |
| `two_channel_empathy.py` | f(c = 2), count(c = 0.5, d = 1), swap at total dose 1.0 | (liii) Channel separation | **FAIL** |

Headline numbers: **1/4 pass — and the failures are the
result.** The high-dose withdrawal is the only
seed-robust effect: at d = 2, D falls by 0.267 / 0.097 /
0.205 / 0.148 (bar 0.05), joint entropy falls by 6.92 /
3.22 / 5.58 / 4.37 bits (bar 2.0), and mean R rises, on
every seed. Everything else breaks on held-out seed
1234: concern alone first *dilutes* f there (0.3251 →
0.1505 at c = 0.25) before raising it, and the count at
c = 0.5 is 24, not the ceiling 28; the distress count
falls 24 → 17 → 14 then rebounds to 23 at d = 1 (bar
≤ 15); the swap difference collapses to 0.0504 there
(concern-heavy f 0.5879 vs distress-heavy 0.5374), so
the channels are near-interchangeable in f on that
seed. And no (c, d) point carries both f ≥ f\* = 0.7278
and count ≤ 15 on any seed — the two landmarks are
separated by channel (concern alone reaches f\* on
every seed: 0.858 / 0.905 / 0.827 / 0.877), not fitted
at one point. The report's "concern raises joint
entropy" half also fails under this wiring (H_joint at
c = 1 below baseline on both calibration seeds), and
"distress lowers D" fails monotonically (seed 7 D
rises with d before falling at d = 2) — both disclosed
in the preregistration, reported not gated.

Run `two_channel_empathy.main()` for the sweeps and the
four verdicts, or see REPORT.md §22.

## Connectome-harmonic / structure–function coupling (v0.17.0)

Deep-think upgrade #10: connectome harmonic
decomposition (CHD, Atasoy et al. 2016) and the
structure–function coupling finding of Luppi et al.,
*Communications Biology* 6:117, 2023 (established) —
loss of consciousness = *increased*
structure–function coupling; psychedelics = the
opposite (decoupling). The graph the project did not
yet have: structure W_ij = R_ij = |⟨ψᵢ|ψⱼ⟩|² (i ≠ j)
on the v0.5.0 resonance population (8 agents) at
σ = 0.10 / 0.25 / 0.50 / 1.00; graph Laplacian
L = D − W; harmonic modes are the eigenvectors of L.
Functional connectivity F_ij is the Bhattacharyya
coefficient between the agents' Born distributions
(sign-blind where W is sign-sensitive). Coupling
κ(σ) is the Pearson correlation between the
upper-triangular entries of W and F (28 pairs). The
per-node harmonic measure is the basis-independent
Rayleigh quotient ρ(D), ρ = 1 being random-like on
the graph. The decoupling control permutes F (50
permutations) and recomputes κ; the shuffle leaves f
unchanged by construction. No scalar Φ is computed
anywhere.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `connectome_harmonic.py` | Laplacian identities + ρ(D) vs 1, every seed × σ | (liv) CHD machinery exact, node signals harmonically random-like | **FAIL** |
| `connectome_harmonic.py` | κ(0.50), κ(1.00) vs κ(0.25) | (lv) Luppi prediction: coupling rises with loss of attunement | **FAIL** |
| `connectome_harmonic.py` | κ(0.25), dip to 0.50, recovery to 1.00, shuffle null | (lvi) Measured shape: dip at the break, recovery, decoupling ≠ attunement | **FAIL** |

Headline numbers: **0/3 pass — the strongest negative
result in the run so far.** Coupling falls, not rises,
with loss of attunement on every seed: κ(0.50) −
κ(0.25) = −0.599 / −0.430 / −0.423 / −0.203 and
κ(1.00) − κ(0.25) = −0.192 / −0.203 / −0.611 / −0.770
(bar +0.10) — the reverse of the anaesthesia/DOC
direction. The calibration seeds' dip-and-recovery
shape was seed noise: on the held-out seeds κ falls
monotonically with σ (0.999 → 0.986 → 0.564 → 0.376
on seed 1234; 1.000 → 0.998 → 0.796 → 0.229 on seed
2026), so the dip sub-check fails on seed 2026
(0.203 < 0.30) and the recovery fails on both
held-out seeds (−0.188 / −0.567). The ρ half of (liv)
fails on the held-out seeds only: the D signal is
strongly structure-aligned at high σ there (ρ = 0.4662
at σ = 0.50 on seed 1234; ρ = 0.5995 at σ = 1.00 on
seed 2026; bar |ρ − 1| ≤ 0.20), while all five
Laplacian identity sub-checks pass exactly on every
seed × σ. What survives: the attuned field is strongly
coupled (κ(0.25) = 0.999 / 0.842 / 0.986 / 0.998), and
the decoupling control is clean (shuffle null mean
−0.015 / −0.031 / −0.005 / −0.004, separated from
κ(0.25) by ≥ 0.81, f unchanged) — decoupling alone is
not attunement. Disclosed artefacts: κ ≈ 1.0000 at
σ = 0.10 is near-parallel (both W and F ≈ 1, same
noise driving both), reported not gated; the
low-frequency energy share is seed-unstable at low σ
(0.104 on seed 42 vs 0.801 on seed 7) because the
nonzero eigenvalues are nearly degenerate, which is
why ρ, not the energy share, is gated.

Run `connectome_harmonic.main()` for the tables and the
three verdicts, or see REPORT.md §23.

## GRT phase-transition test (v0.18.0)

Deep-think upgrade #11, ranked last and lowest value:
General Resonance Theory (Hunt & Schooler,
*Frontiers in Human Neuroscience* 13:378, 2019; GRT
2.0, TSC 2026 abstract — speculative). Conjecture 1:
shared resonance combines micro- into
macro-conscious entities via a phase transition in
the speed/bandwidth of information flow at a
critical coupling K_c; Conjecture 3: nested entities
persist within larger ones ("many become one"). The
base field is the v0.5.0 resonance population (8
agents) at σ = 1.00, the far-broken regime — the
field must start fragmented for a transition to be
possible, and at σ = 0.25 it is already one
macro-entity at K = 0. Coupling K on the grid
0.0–1.0 (step 0.1) is shared resonance as mixing
toward the common reference: ψᵢ(K) =
normalize((1 − K)·ψᵢ + K·ψ_ref), ψ_ref the uniform
thought. Bandwidth B(K) is the pairwise shared
information, the mean over all 28 pairs of
H(pᵢ) + H(pⱼ) − H(pᵢⱼ), pᵢⱼ the Born distribution of
the pair state — a *defined* bandwidth proxy inside
the model, not a literal mutual information. K_c is
the first grid K where mean R(K) reaches the
bridge's pre-existing resonance threshold 0.5; GRT
supplies no number, so the test is partly
self-fulfilling, stated up front. No scalar Φ is
computed anywhere.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `grt_transition.py` | Endpoints exact, K_c interior, fragmented at K = 0 | (lvii) Machinery exact, K_c interior, field starts fragmented | **PASS** |
| `grt_transition.py` | B step at K_c vs largest B step on the grid | (lviii) GRT phase transition: sharp jump in bandwidth at K_c | **FAIL** |
| `grt_transition.py` | Macro at K_c + 0.2, nested components at K_c, total B rise | (lix) Measured shape: macro forms just above K_c, nesting persists, bandwidth rises | **PASS** |

Headline numbers: **2/3 pass — and the failure is the
result.** K_c is interior on every seed (0.3 / 0.6 /
0.5 / 0.4) and the field starts fragmented (largest
component 7 / 6 / 4 / 3), but bandwidth does not jump
at K_c: the step there is +0.1142 / −0.0572 / −0.0023 /
−0.0002 bits (bar ≥ 0.10), and the largest step sits
at K = 0.7 on ALL four seeds (0.1501 / 0.2597 / 0.2282 /
0.2103) — a late, displaced rise, not a phase
transition at the predicted coupling. What survives:
the structural half of GRT — the macro completes at
K_c + 0.2 (largest component 8 on every seed) while
2 / 4 / 3 / 5 nested components survive at K_c, and
bandwidth rises 0.85 / 0.88 / 0.56 / 0.74 bits
overall. Disclosed: mean R is not monotone in K on
seed 7 (dips 0.2778 → 0.2376 at K = 0.3), reported
not gated; the field-mix coupling wiring was tried
and rejected (mean R fell with K at σ = 1.00 seed 7);
nesting dissolves by K = 1 (one component at
R ≥ 0.75 on every seed).

Run `grt_transition.main()` for the sweep and the
three verdicts, or see REPORT.md §24.

## Cogitate-style process predictors of the collaboration gap (v0.19.0)

Deep-think upgrade #9, the last unbuilt item: Cogitate-style
preregistration + process predictors of the collaboration gap
(Cogitate Consortium, *Nature* 642:133–142, 2025 — adversarial
preregistration, n=256; Woolley et al., *Science* 330:686–688,
2010 — c-factor: mean social sensitivity and equal turn-taking
predict group performance, NOT mean/max member IQ; replication
contested). The run is the standard design-B collaboration run
(N=4, 10 generations, 200 samples/generation), whose
per-generation rows now carry the process variables additively:
per-agent D, mean pairwise R, and R within the "posterior"
subset (agents {0, 1} by index, fixed before looking). Per
(σ, seed) run: gap, mean_R (mean social sensitivity), mean_D
and max_D (individual ability), −var_D (equal turn-taking),
post_R_sustained (posterior synchrony), broadcast =
min(onset, offset) R (ignition at BOTH ends). Per-seed Pearsons
across the 7-value sigma grid; thresholds frozen from
calibration seeds 42/7 in docs/preregistration-v0.19.0.md
before the held-out evaluation on seeds 1234/2026. Note the
grid has 7 values, so the pooled regression runs over 28 runs
(7σ × 4 seeds), not 20. No scalar Φ is computed anywhere.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `cogitate.py` | mean_R vs max_D and mean_D, every seed | (lx) Mean sensitivity beats individual D | **FAIL** |
| `cogitate.py` | r(gap, −var_D) vs bar, and vs r(gap, max_D) | (lxi) Turn-taking equality predicts the gap | **PASS** |
| `cogitate.py` | max(r(post), r(bcast)) and separation, every seed | (lxii) Posterior vs broadcast separable, one predicts | **PASS** |
| `cogitate.py` | Pooled R²(gap ~ mean_R + (−var_D)) vs R²(gap ~ max_D) | (lxiii) Pooled regression | **PASS** |

Headline numbers: **3/4 pass — and the failure is the
result.** Turn-taking equality predicts the gap on every
seed (r = 0.7899 / 0.7566 / 0.7589 / 0.7105, bar 0.70; seed
2026 closest at 0.7105) and beats max_D everywhere; the
posterior predictor wins on every seed (r = 0.9278 / 0.8657 /
0.9858 / 0.8884, bar 0.80) with separation 1.83 / 1.76 /
1.77 / 1.82 (margin 1.00), while broadcast anti-predicts the
gap on every seed (r = −0.9022 / −0.8911 / −0.7813 / −0.9350)
because onset R rises with σ while the gap falls; the pooled
regression over 28 runs gives R² = 0.6505 against 0.3298
(difference 0.3207, margin 0.05; adjusted-R² difference
0.3185). But mean sensitivity does NOT beat mean individual
D: claim (lx) fails on held-out seed 1234, where r(gap,
mean_D) = 0.8839 exceeds r(gap, mean_R) = 0.8447 — the tight
calibration margin (worst 0.1252 vs frozen 0.10) had flagged
this as a live risk. Disclosed: at σ = 0 the predictors are
identical across seeds (only the sampling differs); the
posterior pair's R falls to ~0.0001 in at least one
generation on most runs, so it is the sustained MEAN that
predicts, not unbroken synchrony; on seed 1234 at σ = 1.00
the offset R (0.1157) falls below the onset (0.4437), the
only run where it does.

Run `cogitate.main()` for the sweep and the four verdicts,
or see REPORT.md §25.

## Genuinely synergistic target: XOR-target PID of the collaboration gap (v0.20.0)

PID follow-up to v0.14.0, which found the Williams & Beer
I_min decomposition unable to adjudicate "synergy, not
redundancy" because with target Y = the joint outcome
(X1, X2), Syn = Red − I(X1;X2) and I(X1;X2) is ~0.00–0.06
bits everywhere, so Syn ≈ Red on every σ/seed. This build
replaces the target with the canonical synergistic target
Y = X1 ⊕ X2 (bitwise XOR of the two agents' 2-bit Born
outcomes): with independent uniform sources each alone
carries zero about Y while the pair jointly carries all
2 bits — pure synergy by construction. Same measure
(I_min), same arms, same exact pooled distributions
(reused from `pid.py`); only the target changes. The
information gap is now ΔI = I_collab(X1,X2;Y) −
I_isol(X1,X2;Y), with ΔSyn, ΔRed, ΔUniq summing to it
exactly. Thresholds frozen from calibration seeds 42/7
in docs/preregistration-v0.20.0.md before the held-out
evaluation on seeds 1234/2026.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `synergistic_target.py` | Identity, canonical XOR cases, sampled H(Y) cross-check | (lxiv) XOR-target PID identity | **PASS** |
| `synergistic_target.py` | ΔSyn vs ΔRed and ΔSyn / ΔI at σ = 0.25, every seed | (lxv) The gap IS synergy, not redundancy | **FAIL** |
| `synergistic_target.py` | Pearson(Syn_collab, R_post) and Syn(0.50) vs Syn(0.25) | (lxvi) Synergy rises with R and falls at σ = 0.50 | **FAIL** |
| `synergistic_target.py` | Red_collab / I_collab across the grid, every seed | (lxvii) Redundancy stays a small share | **PASS** |

Headline numbers: **2/4 pass — and the failures are the
result.** The XOR target DOES separate synergy from
redundancy: at σ = 0.25 ΔSyn exceeds ΔRed on all four
seeds (+1.4472 / +1.0010 / +1.0248 / +1.1901 vs +0.3143 /
+0.1397 / −0.3953 / −0.3007), where the v0.14.0 target had
Syn ≈ Red everywhere. But claim (lxv) fails on held-out
seed 1234 because the information gap itself is negative
there (ΔI = −0.2591 bits: the isolated arm carries more
XOR information, I_isol = 1.7610 vs I_collab = 1.5019),
so the synergy share is −3.956; and claim (lxvi) fails
everywhere — synergy does not track resonance (Pearsons
0.3731 / 0.3424 / −0.3397 / 0.9036, bar 0.5) and rises
from σ = 0.25 to 0.50 on every seed, climbing toward the
2-bit ceiling as the marginals uniformize with noise.
Redundancy stays small throughout (worst shares 0.1924 /
0.2357 / 0.1396 / 0.0882, bar 0.25). Disclosed: the first
pilot pass computed I(Xi;Y) as H(Y) − H(Xj), which
assumes a product distribution — the pooled joint is a
mixture of per-generation products, so that shortcut
produced negative unique atoms (worst −0.6955, seed 7)
and was corrected to the exact joint computation before
any threshold was frozen; and the isolated arm is NOT
synergy-free at high σ (Syn_isol up to 1.0755 bits at
σ = 1.00), because the pooled mixture correlates the
collapsed agents through the generation index.

Run `synergistic_target.main()` for the sweep and the four
verdicts, or see REPORT.md §26.

## A target for which collaboration reliably raises total information: MAX-target PID (v0.21.0)

The v0.20.0 open follow-up, answered by a candidate search
on calibration seeds only: fourteen deterministic targets
Y = f(X1, X2), same I_min measure, same arms, same exact
pooled distributions — only the target changes. The screen
picks MAX, Y = max(X1, X2), the peak / strongest-concept
outcome: max min-seed ΔI at σ = 0.25 among eligible new
targets (+1.8927 / +1.0707 on seeds 42 / 7), after
excluding the incumbents (xor, joint — already measured on
all four seeds) and the Latin-square difference targets
(sum_mod4, diff_mod4 — near-duplicates of the failed XOR
mechanism by construction). OR tracks MAX within 0.03 bits
and is the reported sensitivity check. Thresholds frozen
from calibration seeds 42/7 in
docs/preregistration-v0.21.0.md before the held-out
evaluation on seeds 1234/2026.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `total_information_target.py` | Identity, canonical MAX cases, sampled H(Y) cross-check | (lxviii) MAX-target PID identity | **PASS** |
| `total_information_target.py` | ΔI at σ = 0.25, every seed | (lxix) Collaboration raises total information about MAX | **PASS** |
| `total_information_target.py` | ΔSyn vs ΔRed and ΔSyn / ΔI at σ = 0.25, every seed | (lxx) The gap IS synergy, not redundancy | **PASS** |
| `total_information_target.py` | Red_collab / I_collab across the grid, every seed | (lxxi) Redundancy stays below half | **PASS** |
| `total_information_target.py` | ΔI across the grid, every seed | (lxxii) Collaboration raises total information everywhere | **PASS** |

Headline numbers: **5/5 pass — the first target in the
series for which collaboration reliably raises total
information.** At σ = 0.25 ΔI = +1.8927 / +1.0707 /
+0.3266 / +0.6527 (seeds 42 / 7 / 1234 / 2026), positive
on every seed including held-out seed 1234, where the XOR
gap was −0.2591; and positive on every (seed, σ), minimum
+0.2337 (seed 7, σ = 1.00). The gap is synergy-dominant
on every seed (shares 0.543 / 0.964 / 1.226 / 1.011, bar
0.5 — above 1 on the held-out seeds because ΔRed is
negative on 1234 and ΔUniq negative on 2026), and
redundancy stays below half the target information
everywhere (worst share 0.3837 on every seed, bar 0.50).
Disclosed: the isolated arm degenerates at low σ (I_isol
= 0 exactly at σ ≤ 0.25 on seed 42, σ ≤ 0.10 on seeds 7
and 1234 — the design-B lock-in), so the large ΔI at low
σ is driven as much by the isolated arm collapsing to a
point as by collaboration raising information; and MAX is
not a pure-synergy target (independent uniform sources:
Red = 0.6712 of I = 1.7490) — what it buys is a positive
total-information gap, not a cleaner synergy.

Run `total_information_target.main()` for the screen, the
sweep and the five verdicts, or see REPORT.md §27.

## Per-generation PID: does the synergy-vs-σ climb survive without pooling? (v0.22.0)

The v0.20.0 confound, tested: the pooled joint is a
mixture of per-generation products, and the
mixture-correlation is itself synergistic about the XOR
target. This build computes the PID per generation (no
pooling across generations) for the XOR and MAX targets,
same seeds and σ grid, same Williams & Beer I_min
measure — only the distribution changes. Thresholds
frozen from calibration seeds 42/7 in
docs/preregistration-v0.22.0.md before the held-out
evaluation on seeds 1234/2026, with the decision rule
stated in advance: the climb survives iff (lxxiv) passes.

| Module | What it measures | Claim | Verdict |
|---|---|---|---|
| `per_generation_pid.py` | Identity, pooled consistency (mean per-gen joint = pooled joint) | (lxxiii) Per-generation PID identity | **PASS** |
| `per_generation_pid.py` | Mean per-gen Syn_c(XOR) at σ = 1.00 vs 1.50-bit bar, and vs σ = 0.50 | (lxxiv) The XOR climb survives per-generation | **FAIL** |
| `per_generation_pid.py` | Pooled Syn_i(XOR) − mean per-gen Syn_i(XOR) at σ = 1.00 vs 0.50-bit bar | (lxxv) Isolated-arm high-σ synergy is a pooling artifact | **FAIL** |
| `per_generation_pid.py` | Mean per-gen ΔSyn vs ΔRed and share of mean gap, MAX at σ = 0.25 | (lxxvi) Per-generation MAX gap is synergy | **FAIL** |
| `per_generation_pid.py` | Mean per-gen ΔSyn vs ΔRed and share of mean gap, XOR at σ = 0.25 | (lxxvii) Per-generation XOR gap is synergy | **PASS** |

Headline numbers: **2/5 pass — the climb is a pooling
artifact.** Per-generation mean Syn_c(XOR) at σ = 1.00
is 1.0933 / 0.9855 / 1.0039 / 0.9995 (seeds 42 / 7 /
1234 / 2026) against the 1.50-bit bar, while the pooled
values reach 1.8432 / 1.7933 / 1.8129 / 1.8365 — so the
(lxvi) conclusion "synergy climbs toward the 2-bit
ceiling with σ" is downgraded to a pooling artifact.
The pooled (lxx) synergy-majority for MAX does not
survive per-generation either (shares 0.383 / 0.332 /
0.350 / 0.445, bar 0.5). The mixture-excess bar fails
on held-out seed 2026 (+0.4000 vs the 0.50 bar; pooled
Syn_i there is only 0.4000, vs 1.0000–1.0755 elsewhere).
What survives per-generation is the XOR gap at
σ = 0.25: synergy shares 0.566 / 0.541 / 0.584 / 0.655
— including on seed 1234, where the pooled gap was
negative (−0.2591) but the mean per-generation gap is
+1.4356. The v0.20.0 failure on seed 1234 was itself a
pooling artifact. Disclosed: the per-generation
isolated arm is synergy-free by construction (point-mass
joints after the design-B collapse), and per-generation
synergy varies widely across generations (sd up to 0.39
bits), so the pooled value represents no single
generation.

Run `per_generation_pid.main()` for the sweep and the
five verdicts, or see REPORT.md §28.

## Maximum scientific outcome

Run:

```bash
python3 scientific_outcomes.py
```

This produces a structured outcome containing:

- Point estimates
- Mapping status before and after calibration
- Bootstrap uncertainty
- One-at-a-time sensitivity analysis
- Robustness classification
- Preregistered decision rules
- SHA-256 input provenance
- Explicit non-claims
- JSON and Markdown benchmark reports

The benchmark writes:

```text
results/benchmark.json
results/BENCHMARK.md
```

## Mapping status

| Status | Rule |
|---|---|
| `DISSONANT` | `A < 0` |
| `PARTIAL` | `0 <= A < 0.5` |
| `ATTUNED` | `A >= 0.5` and empathy proxy `>= 0.5` |
| `ATTUNED-LOW-EMPATHY` | `A >= 0.5` and empathy proxy `< 0.5` |

These thresholds are repository conventions, not measured physical or psychological constants.

**v0.4.0:** the mapping status can also be re-derived from the
visible fraction F: `ATTUNED` if F ≥ 0.30, `PARTIAL` if
F ≥ 0.01, else `DISSONANT`. Those thresholds were set from a
pilot sweep (REPORT.md §10) and are repository conventions,
not measured constants. The primary attunement A = 0.0447 does
not change; only the status derivation changes.

## Honest limits

- Faggin's QIP is an interpretive metaphysical framework; this repository does not test it.
- The unity proxy is classical self-correlation under noise, not quantum entanglement.
- The empathy value is a supplied reference, not a measured human property.
- No gravity or microtubule model is measured.
- The Omega-Genesis synthetic reproduction is in the same regime as the reported value but does not reproduce it exactly.
- All results are synthetic classical computations.
- **v0.2.0:** entanglement is now measured — as a quantity of the
  model (concurrence of a two-thought Bell state, computed
  exactly). It is not a measurement of physical entanglement in
  hardware. The machine running the code is classical.
- **v0.2.0:** a "thought" is a two-qubit state vector over four
  arbitrarily labelled basis concepts. Nothing here claims a
  human thought is a qubit state, or measures a mind. D measures
  how much of an outcome the system's own stored subspace
  determines — nothing more.
- **v0.3.0:** interference is measured — as exact geometry of
  state vectors in the model (the cross term ⟨ψ1|P|ψ2⟩,
  computed with NumPy). It is not a measurement of physical
  interference in hardware; the machine is classical.
- **v0.3.0:** projection in the model is a partial measurement:
  it discards the kernel component and renormalizes. The
  cascade's death of interference is a property of that
  construction (the projector's rank and the pair geometry), not
  a measurement of what a physical measurement does to a mind.
- **v0.3.0:** the feed-phase convention (smallest phase
  achieving maximum D within 1e-12) and the reopening angle
  (α = π/4) are repository choices, stated in cascade.py. The
  survival verdict is defined against the pre-registered 0.1
  visibility threshold at stage 10.
- **v0.4.0:** the empathy-quantum link is a definition inside
  the model, not a discovery: nothing in physics says a
  thought-pair's concurrence is a photon frequency. T_eff is a
  model temperature, not a physical temperature; the visible
  band [0.38, 0.75] µm is a chosen mapping. The Planck law
  itself is real physics with real constants (claim (viii) is a
  reproduction); only the mapping from concurrence to
  temperature to status is the repository's construction.
- **v0.4.0:** the empathy-status thresholds (F ≥ 0.30 ATTUNED,
  F ≥ 0.01 PARTIAL) are repository conventions set from a pilot
  sweep, not measured constants.
- **v0.5.0:** resonance is a defined overlap quantity
  (|⟨ψ_i|ψ_j⟩|²), not a measured physical resonance;
  co-creativity = entropy is a definition of the measure
  (joint entropy of the collective's joint outcomes), not a
  discovery about human creativity; collaboration is a shared
  field in code, not social science. The (xi) resonance effect
  is the cross-noise pattern — within a single noise level it
  is weak or negative. The (xiii) break does not hold: the
  collaboration gap survives every noise level tested, and the
  claim FAILS on that half.
- **v0.6.0:** a "quale" is a DEFINED resonant+entangled
  mode in code, not a measurement of subjective experience;
  the qualia wave is a defined superposition, not a physical
  wave. The (xiv) count is humped against f (peak 17 at
  f = 0.1803) and the (xvi) pooled D gap is negative
  (−0.1522): in this model the resonant+entangled modes are
  the least self-determined, because the noise that creates
  concurrence destroys self-knowing.
- **v0.7.0:** monogamy is an established theorem (CKW 2000;
  Osborne & Verstraete 2006) applied to the model's states;
  the triads are defined in code, not physical systems, and
  the binary-thought embedding is a definition, not a
  discovery. The (xvii) PASS checks the code's concurrence
  against the theorem; it does not test the theorem. The
  (xix) PASS is about the model's own D against the model's
  own tangles, not about human self-knowing.
- **v0.8.0:** quantum Darwinism is an established theory
  (Zurek 2009; Zhu et al. 2025) applied to the model's
  states; the environment is defined in code, not a physical
  system. The (xx) PASS checks the code's entropies against
  the branching construction's analytic form, not the
  theory. The (xxi) and (xxii) FAILs are about the model's
  own D, redundancy, and discord under the model's own
  noise; they do not show anything about human self-knowing
  or about why real collaborations survive noise. The
  vector noise is not a dephasing channel: it entangles the
  system with the environment, so the classical/quantum
  split under σ is not the einselection picture — that
  picture holds for the dephasing parameter p.
- **v0.9.0:** Malus's law is classical optics, computed
  exactly; the polarizers are ideal and the input is either
  unpolarized or a pure Jones vector. The (xxiii)–(xxv)
  PASSes check the code's projectors against the analytic
  Malus formulas, not the theory. The cascade contrast in
  (xxv) is structural: a pair collapses under projection
  while a single state rotates — it does not show that
  projection "creates" anything in a physical sense, only
  that the surviving component overlaps the next axis.
  Classical emulation throughout; Faggin's metaphysics stays
  interpretive.
- **v0.10.0:** the product model is a test of independence
  of the two quale indicators across pairs, not an
  independent prediction from separate data — the
  marginals are measured on the same pairs as the count.
  The gated fit runs on the fine σ grid because the
  standard-grid fit is partly degenerate (p_res = 1.0
  below σ = 0.5). The fit is seed-dependent: it passes at
  seeds 1, 3, 42 and fails at seed 2.
- **v0.11.0:** the ledger's event list is a definition of
  what this run counts as erasure, not a measurement of a
  physical brain erasing bits; the per-bit cost is exact
  physics, the choice of operations is the model's. The
  classification term (28 bits) is constant per field and
  dominates the ledger. The (xxx) FAIL means the ledger
  does not explain the σ = 0.50 break better than σ
  itself. The (xxxi) PASS demotes E = hν from a spectrum
  to a per-mode unit; the pooled KS rejection is thin
  (0.1465 vs 0.1258) and per-field tests do not reject
  Planck on their own.
- **v0.12.0:** the (xxxii) FAIL is seed-fragility in the
  linear form, not in the direction: the monotone
  anti-tracking of D and concurrence holds on all four
  seeds (Spearman −1.0000 to −0.9643) while the Pearson
  bar fails on held-out seed 2026 (−0.8828 vs −0.90).
  The (xxxiii) PASS is a mapping check on a branch whose
  direction is built into the family, and it does NOT
  transfer to the noise axis, where the relation inverts
  — noise-created concurrence is not knowing. The
  (xxxiv) PASS is exact by construction (the slide is
  built from the two patterns); its measured content is
  that the identities hold in the code to 4.44e-16 and
  the overlap split flips exactly at the midpoint.
- **v0.12.1:** the (xxxv) FAIL shows the seed-fragility
  is broader than one point on one seed: on fresh seeds
  the 5-copy sweep breaks in two different places (seed
  5 Spearman −0.8929, seed 99 D range 0.2445), and the
  linear form stays fragile even at n = 200 (seed 5
  Pearson −0.8971). The observer-direction claim, as
  stated on this construction, does not hold on every
  seed in either form. What survives is weaker: the
  monotone direction holds at n = 200 on all six seeds.
- **v0.13.0:** all four Kuramoto claims fail. The spec's
  shapes do not materialize in this wiring: the count
  peak is seed-fragile (interior on 2 of 4 seeds) and
  sits at R_K 0.31–0.36, far below the Phillips band
  [0.5, 0.8]; joint entropy is flat because the
  per-agent Born entropy averages ~1.5 bits whatever K
  is; the gap A is flat because single-shot collapse
  makes A = H_collaborating; σ* wanders across seeds
  (1.0, 0.10, 0.25, 0.05). What survives is the
  Kuramoto transition itself (R_K 0.29 → 0.99), the
  count floor of 6 at high K on every seed, and the
  count exceeding σ = 0 on every seed at K = 1.0.
- **v0.14.0:** three of four PID claims fail. The
  collaboration gap is not synergy-dominant on every
  seed (synergy share 0.41–0.43 on calibration seeds,
  0.55–0.88 on held-out seeds); synergy does not rise
  with R and rises, not falls, at σ = 0.50 on every
  seed; redundancy is σ-robust on 3 of 4 seeds but
  fails seed 42 (ratio 0.24). The decomposition itself
  is exact (identity error 8.88e-16 bits). The
  structural limit is that Syn ≈ Red in this wiring
  because I(X1;X2) ≈ 0 in the collaborating arm, so
  the atoms cannot adjudicate "synergy, not
  redundancy" either way.
- **v0.15.0:** three of five no-cloning / Holevo
  claims pass. The exact coefficient is 1 − C²/2
  (worst error 8.88e-16), and the Born-collapse
  accessible information never exceeds χ; the
  Bužek–Hillery cloner is exactly 5/6 and the CNOT
  copy averages exactly 2/3. But χ does not bound D
  — D sits above χ at low f and approaches it from
  above (Spearman(|gap|, f) = −1.00 / −0.96) — and
  the model's own classical copy exceeds 5/6 at every
  working σ (1.0000 at σ = 0, 0.85–0.88 at σ = 0.25).
  Privacy is not enforced by the representation.
- **v0.16.0:** three of four two-channel claims fail,
  all on held-out seed 1234 (baseline f 0.3251, nearly
  double the other seeds at the same σ = 0.25): concern
  alone first dilutes f (0.3251 → 0.1505) before raising
  it, the distress count rebounds to 23 at d = 1, and
  the swap difference collapses to 0.0504 — the channels
  are near-interchangeable in f on that seed. Only the
  high-dose withdrawal (lii) is seed-robust, and no
  (c, d) point carries both f ≥ f\* and count ≤ 15 on
  any seed. The transform raises mean R strictly in
  every sweep on every seed, but is not a monotone dial
  on f, count, or D. No scalar Φ is computed anywhere.
- **v0.17.0:** zero of three connectome-harmonic claims
  pass. Coupling falls, not rises, with loss of
  attunement on every seed (κ(0.50) − κ(0.25) = −0.60 /
  −0.43 / −0.42 / −0.20) — the reverse of the Luppi
  anaesthesia/DOC direction. The dip-and-recovery shape
  was a calibration-seed artefact: on the held-out seeds
  κ falls monotonically with σ. The D signal aligns
  strongly with the graph harmonics at high σ on the
  held-out seeds (ρ down to 0.47), while the Laplacian
  identities hold exactly everywhere. What survives: the
  attuned field is strongly coupled (κ(0.25) ≥ 0.84) and
  the shuffle decoupling control is clean (null ≈ 0,
  separated by ≥ 0.81, f unchanged). No scalar Φ is
  computed anywhere.
- **v0.18.0:** two of three GRT phase-transition claims
  pass. The machinery is exact (endpoints to 1e-12,
  B(1) = 2.0000), K_c is interior on every seed (0.3 /
  0.6 / 0.5 / 0.4), the macro completes at K_c + 0.2
  (largest component 8) while 2–5 nested components
  survive at K_c, and bandwidth rises 0.56–0.88 bits
  overall. But there is no phase transition at K_c:
  the bandwidth step there is +0.11 / −0.06 / −0.00 /
  −0.00 bits (bar 0.10), and the largest step sits at
  K = 0.7 on all four seeds (0.15 / 0.26 / 0.23 /
  0.21) — a late, displaced rise. Mean R is not even
  monotone in K on seed 7. No scalar Φ is computed
  anywhere.
- **v0.19.0:** three of four Cogitate-style process-predictor
  claims pass. Turn-taking equality predicts the collaboration
  gap on every seed (r(gap, −var_D) = 0.79 / 0.76 / 0.76 /
  0.71, bar 0.70) and beats max_D everywhere; the posterior
  predictor wins on every seed (r = 0.93 / 0.87 / 0.99 / 0.89,
  bar 0.80) while broadcast anti-predicts it on every seed
  (r = −0.90 / −0.89 / −0.78 / −0.94); the pooled regression
  over 28 runs gives R² = 0.65 for gap ~ mean_R + (−var_D)
  against 0.33 for gap ~ max_D (difference 0.32, margin 0.05).
  But mean sensitivity does NOT beat mean individual D: claim
  (lx) fails on held-out seed 1234, where r(gap, mean_D) =
  0.8839 exceeds r(gap, mean_R) = 0.8447. All thresholds were
  preregistered from calibration seeds 42/7 before the
  held-out evaluation; none was moved. No scalar Φ is computed
  anywhere.
- **v0.20.0:** two of four XOR-target PID claims pass. The
  XOR target Y = X1 ⊕ X2 DOES separate synergy from
  redundancy at σ = 0.25 (ΔSyn exceeds ΔRed on all four
  seeds: +1.45 / +1.00 / +1.02 / +1.19 vs +0.31 / +0.14 /
  −0.40 / −0.30), where the v0.14.0 joint-outcome target had
  Syn ≈ Red everywhere. But the "gap is synergy" claim fails
  on held-out seed 1234, where the information gap itself is
  negative (ΔI = −0.26 bits), and synergy does NOT rise with
  R or fall at σ = 0.50 (Pearsons 0.37 / 0.34 / −0.34 / 0.90,
  bar 0.5; synergy rises 0.25 → 0.50 on every seed).
  Redundancy stays a small share of the target information
  (worst 0.19 / 0.24 / 0.14 / 0.09, bar 0.25). All thresholds
  were preregistered from calibration seeds 42/7 before the
  held-out evaluation; none was moved. No scalar Φ is computed
  anywhere.
- **v0.21.0:** five of five MAX-target PID claims pass — the
  first target for which collaboration reliably raises total
  information. A calibration-only search over fourteen
  deterministic targets picks MAX, Y = max(X1, X2), by max
  min-seed ΔI among eligible new targets, excluding the
  incumbents (xor, joint) and the Latin-square difference
  targets (sum_mod4, diff_mod4) as near-duplicates of the
  failed XOR mechanism. At σ = 0.25 ΔI = +1.89 / +1.07 /
  +0.33 / +0.65 (seeds 42 / 7 / 1234 / 2026), positive on
  every seed including held-out seed 1234, where the XOR gap
  was −0.26; positive on every (seed, σ), minimum +0.23
  (seed 7, σ = 1.00). The gap is synergy-dominant on every
  seed (shares 0.54 / 0.96 / 1.23 / 1.01, bar 0.5) and
  redundancy stays below half the target information
  everywhere (worst 0.38, bar 0.50). Disclosed: the isolated
  arm degenerates at low σ (I_isol = 0 exactly — the
  design-B lock-in), and MAX is not a pure-synergy target
  (independent uniform sources: Red = 0.67 of I = 1.75).
  All thresholds were preregistered from calibration seeds
  42/7 before the held-out evaluation; none was moved. No
  scalar Φ is computed anywhere.
- **v0.22.0:** two of five per-generation PID claims pass —
  and the headline is a downgrade: the synergy-vs-σ climb
  does NOT survive without pooling. Per-generation mean
  Syn_c(XOR) at σ = 1.00 stays ~1.0 bits on every seed
  (1.09 / 0.99 / 1.00 / 1.00, bar 1.50) while the pooled
  values reach 1.79–1.84, so the (lxvi) conclusion is
  downgraded to a pooling artifact; the pooled (lxx)
  synergy-majority for MAX does not survive per-generation
  either (shares 0.38 / 0.33 / 0.35 / 0.45, bar 0.5); and
  the mixture-excess bar fails on held-out seed 2026
  (+0.40 vs 0.50). What survives per-generation is the XOR
  gap at σ = 0.25 (shares 0.57 / 0.54 / 0.58 / 0.66) —
  including on seed 1234, where the pooled gap was −0.26
  but the mean per-generation gap is +1.44. Disclosed: the
  per-generation isolated arm is synergy-free by
  construction, and per-generation synergy varies widely
  across generations (sd up to 0.39 bits). All thresholds
  were preregistered from calibration seeds 42/7 before
  the held-out evaluation; none was moved. No scalar Φ is
  computed anywhere.

## Run tests

```bash
python3 -m pytest tests/ -q
```

Or:

```bash
make test
```

## Generate benchmark

```bash
make benchmark
```

## License

Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP).
AGPL-3.0-only. See `LICENSE`.
