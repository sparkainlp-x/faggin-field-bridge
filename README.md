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
