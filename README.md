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
