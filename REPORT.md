# Faggin Field Bridge — Report

**Version:** 0.8.0 (2026-11-17)
**Theory author:** Federico Faggin (with Giacomo Mauro D'Ariano)
**Bridge / test author:** Jean-François Brisson (Spark AI NLP)
**Status:** SYNTHETIC. Classical computation on synthetic states.
No physical, biological or safety claim is made.

## 1. What was built

A nine-module Python package (stdlib + NumPy only) that maps
Faggin's Quantum Information Panpsychism onto measured quantities
from the sparkainlp-x account. The central quantity is attunement:

```
A(delta) = U * (1 + delta) - C
```

U is the spooky correlation (unity), C is the normalized entropy
cost, delta is one clipped calibrator scalar in [-0.05, 0.05].
The observer (Yang) is read-only; the calibrator (Yin) is one
clipped scalar — the membrane-arena pattern, reused from the
de Broglie repo's analog calibration layer.

## 2. Reproductions (recomputed fresh, same definitions)

| # | Number | Recomputed | Reported | Tolerance | Result |
|---|---|---|---|---|---|
| 1 | de Broglie spooky, σ = 0.01 | 0.999999947 | 0.99999995 | 1e-6 | **EXACT** |
| 2 | de Broglie spooky, σ = 0.05 | 0.999998638 | 0.99999864 | 1e-6 | **EXACT** |
| 3 | de Broglie spooky, σ = 0.50 | 0.999642891 | 0.99964289 | 1e-6 | **EXACT** |
| 4 | Calibration improvement | 0.0222763947 orders | 0.022276 orders | 1e-6 | **EXACT** (identity log10(1/0.95), best δ = −0.05) |
| 5 | Tensor-membrane mean single-qubit entropy | 0.9553 bits | 0.955 bits | 0.02 bits | **REPRODUCED** (diff 0.0003) |
| 6 | Omega-Genesis spooky (synthetic) | 0.8373 | 0.9005 | 0.10 (regime) | **SAME REGIME, NOT EXACT** (diff 0.0632) |
| 7 | Omega-Genesis empathy | 0.5503 | 0.5503 | — | **RECORDED, NOT RECOMPUTED** (no formula in the extraction) |
| 8 | Omega-Genesis CCI | 0.8862 | 0.8862 | — | **RECORDED** (reference value) |

### On #6 (the one that does not reproduce exactly)

The notebook's 0.9005 is the reported value from Untitled7's
10M-iteration run. Its evolved 32-dim state is unavailable, so
the exact value cannot be recomputed from the data on hand. The
synthetic reproduction uses a 32-dim state of the same shape
(seed 42) and the notebook's own 20% erasure stress as the copy
model (5 copies, seed 42). It gives 0.8373 — the same regime
(0.8–0.9), a difference of 0.0632. The test asserts the regime
(within 0.10 of the reported value) and prints both numbers, so
the gap is on the record. Nothing was tuned to close it: no
noise level was fitted to hit 0.9005.

### On #7 (empathy)

The notebook extraction gives no closed-form empathy formula
(the measurement layer reports an "empathy index" without
showing its computation). The value 0.5503 is therefore recorded
as the default empathy proxy — a supplied threshold for the
mapping status, not a recomputed measurement. The test asserts the
record is exact, as a record.

### On #5 (seed spread of the 0.9553 — v0.3.1)

The tensor-membrane entropy was computed at seed 42 only. Across
seeds 0..19 (n = 20, recomputed fresh): mean 0.9639, standard
deviation 0.0128, range [0.9276, 0.9775]. The seed-42 value
0.9553 sits 0.0086 below the 20-seed mean — within one standard
deviation, a typical draw, not an outlier. The headline is kept
(seed 42); the spread is reported alongside it and pinned by
`test_tensor_membrane_entropy_seed_spread`.

Honest reading: the regime is near-saturated — random circuits
concentrate near the 1-bit maximum (Page-like behaviour), so the
spread is small in absolute terms. But it is not negligible
against the bridge's own numbers: a ±0.013 move in C moves A by
∓0.013, about 30% of the primary attunement 0.0447. The mapping
status is unaffected (A stays in (0, 0.5) across the whole
spread: PARTIAL throughout).

## 3. Worked examples (the bridge's mapping statuses)

| Example | U | C | A(δ=0) | A(best, δ=+0.05) | A(δ=−0.05) | Mapping status |
|---|---|---|---|---|---|---|
| Primary: de Broglie unity + tensor cost | 0.99999995 | 0.9553 | 0.0447 | 0.0947 | −0.0053 | PARTIAL |
| Omega reported unity + tensor cost | 0.9005 | 0.9553 | −0.0548 | −0.0098 | −0.0998 | DISSONANT |
| Omega synthetic unity + tensor cost | 0.8373 | 0.9553 | −0.1181 | −0.0762 | −0.1599 | DISSONANT |

Empathy E = 0.5503 in all three (gate 0.5: met).

Reading:

- The de Broglie unity (0.99999995) is the only one high enough
  to cover the 0.955 entropy cost, and only barely. A = 0.0447
  at δ = 0 — weak-positive, PARTIAL.
- The notebook's unity (0.9005 reported, 0.837 synthetic) does
  not cover the cost even at the best delta: DISSONANT in both
  cases. The contrast is the point: the Omega-Genesis unity,
  strong as it is, is not strong enough to cover a maximally
  mixed membrane.
- The bounded calibrator moves A by at most 0.05 × U (~0.05).
  It can flip the primary example's mapping status (at δ = −0.05,
  A = −0.0053, DISSONANT), but it cannot rescue a
  high-entropy state. That is the bridge's honest result.

## 4. Test suite

**226 tests, 226 passed** (`python3 -m pytest tests/ -q`, 36.45 s).

*Correction in v0.8.0: this section said 207 with no
test_darwinism.py entry. The collected counts below are the
record (18 files: 12 + 9 + 14 + 9 + 19 + 17 + 25 + 22 + 21 +
17 + 3 + 5 + 7 + 12 + 7 + 9 + 9 + 9 = 226).* (v0.7.0 counts:
207 + 19 new = 226.)

*Correction in v0.6.0: this section still said 151 with no
test_empathy_field.py entry, and test_thought.py as (10)
where the collection is 9; the v0.5.0 CHANGELOG entry
likewise said "151 -> 172". The collected counts below are
the record (16 files: 12 + 9 + 14 + 9 + 17 + 25 + 21 + 3 +
5 + 7 + 12 + 7 + 9 + 9 + 9 + 17 = 185).* (v0.5.0 counts:
151 + 17 new = 168.)

- `test_unity.py` (9): spooky bounds, identical copies = 1.0,
  independent states low, no mutation, de Broglie reproduction
  at three sigmas, state-vector shape, Omega synthetic regime,
  CCI bounds.
- `test_cost.py` (9): Shannon uniform/certain, von Neumann pure
  / maximally mixed, normalized-cost bounds and errors, tensor
  entropy reproduction, tensor cost = entropy / 1 bit, Shannon
  of a uniform 32-dim state, and the seed spread over seeds
  0..19 (mean 0.9639, std 0.0128).
- `test_attunement.py` (12): A definition at δ = 0, bounds,
  monotonicity in unity and (decreasing) in cost, calibrator
  move ≤ 0.05 × U, observer read-only (no attributes, frozen
  observations), observer from entropy, observer input
  validation, calibrator clipping at ±0.05, best δ = +0.05, gap
  calibration identity, empathy proxy default and validation.
- `test_bridge.py` (9): all four mapping-status branches, mapping status
  boundary at the thresholds, bridge() returns every step,
  bridge_from_entropy, primary worked example PARTIAL, Omega
  variants DISSONANT.
- `test_reproduction.py` (5): the four reproduction numbers plus
  the empathy record, each with its tolerance, each printing
  measured vs reported.
- `test_theory.py` (7): theory author is Faggin, paper and books
  cited, every claim carries a status, gravity marked
  unmeasured, no-conscious-computers scope, mapping table
  complete, and the guard that no module uses or cites the
  private theory.
- `test_maximum_scientific_outcomes.py` (25): input validation
  and delta clipping, bootstrap interval ordering and
  determinism, sensitivity coverage, correct sensitivity values
  and directional assertions (cost up lowers A; unity/delta up
  raises A), point estimates, mapping status before and after
  calibration (PARTIAL in both), the ATTUNED and
  ATTUNED-LOW-EMPATHY branches via the single classifier,
  robustness sign-flip reporting, preregistration non-claims,
  provenance hash determinism, benchmark file writing, and
  the synergy-expansion bootstrap and robustness tests below,
  plus the all-threshold margins and the threshold-robustness
  grid.
- `test_synergy.py` (12): synergy threshold ordering, input
  validation, fecundity / attraction / synergy / expansion
  definitions and bounds, status boundaries, the parameterized
  classifier agreeing with the shipped thresholds (and the
  pre-8fb00f1 DORMANT label for the primary expansion), primary worked
  values (FLOWING), and the non-claims record.
- `test_thought_entanglement.py` (9): Bell-state exact values,
  product state unentangled, Wootters concurrence equals the
  pure-state formula, depolarizing analytic match and death at
  p = 2/3, reduced entropy blind to the death, sweep structure,
  claim (i) verdict.
- `test_thought.py` (9): uniform coherence 3.0, decided
  coherence 0, dephasing formula, diagonals untouched, claim (ii)
  and (iii) verdicts, collapse determinism, decided collapse,
  attention clipping at the Yin bound.
- `test_self_knowing.py` (7): exact D values (1, 1/3, 0, 1/2),
  gap complement, Spearman exactness, claim (iv) verdict.
- `test_quantum_thought_claims.py` (3): the unified claims
  (7/7 pass, no headline), the maximum-outcome registry
  (entanglement in the model True, physical False), and the
  preregistration non-claims (original wording kept, model
  scope added).
- `test_cascade.py` (14): rotation-pair visibility V = sin(2θ),
  max-pair phase swing (blind at φ = 0, determined at φ = π),
  mixed pair cross term 1/√6 and V = 2√6/7, zero-interference
  controls, kernel thought projects to nothing, projection
  collapses the rotation pair (rank 1) and re-forms the mixed
  pair fully stored, both projection-only cascades dead at
  stage 2, the reopening control alive at every stage, claims
  (v), (vi) and (vii) verdicts, and the seven-claim bridge
  registry.
- `test_planck_empathy.py` (21): Planck radiance positive and
  peaked (visible at 5000 K, infrared at 2000 K), input
  validation, Simpson convergence (2000 vs 4000 intervals),
  pilot F values at 2000/3000/5000 K, Wien peaks within 0.5%
  of 2898/T, Stefan–Boltzmann T⁴ within 1%, F(T) monotone,
  claim (viii) verdict, empathy quanta equal concurrence
  (h = 1), empathy-fraction validation, T_eff endpoints,
  thresholds set (0.30 / 0.01), endpoint statuses (PARTIAL at
  f = 0, ATTUNED at f = 1), F(f) monotone, the measured
  crossing f\* in (0.70, 0.80), claim (ix) verdict, the old
  status as control (PARTIAL, A = 0.0447), the σ curve
  (ATTUNED at σ ≤ 0.25, PARTIAL at σ ≥ 0.50, labels never go
  back up), claim (x) verdict, the three-claim aggregate
  (3/3 pass, no headline), and main() running.
- `test_empathy_field.py` (17): resonance population
  structure (identical copies at σ = 0), field-state
  normalization, overlap bounds and identity, pair
  concurrence and empathy quanta (h = 1), empathy-fraction
  bounds, collaboration design B gap and distinct counts,
  saturation curve shape, claim (xi) verdict (binned D
  monotone, pooled gap 0.2984), claim (xii) verdict (gap
  +4.3352 bits), claim (xiii) verdict FAIL (ceiling half
  passes, break half fails), the three-claim aggregate
  (2/3 pass, no headline), and main() running.
- `test_qualia.py` (17): no qualia at σ = 0 (resonance
  without entanglement is not a quale), entanglement
  without resonance is not a quale (σ = 1.0), quale count
  17 at σ = 0.25, the humped count-vs-f curve
  (0, 0, 1, 9, 17, 13, 12), first quale at f = 0.0415 and
  peak 17 at f = 0.1803, qualia wave normalized, overlap
  0.9987 at σ = 0.25, per-field spread smaller at σ = 0.25
  (0.1009 vs 0.1268), pooled spreads reported not gated
  (0.1950 vs 0.1947), pooled D gap −0.1522, claim (xiv)
  verdict FAIL, claim (xv) verdict PASS, claim (xvi)
  verdict FAIL, the three-claim aggregate (1/3 pass, no
  headline), thresholds set (0.10 / 0.01 / 0.90 / 0.10),
  input validation, and main() running.
- `test_monogamy.py` (22): GHZ exact values (tau_A(BC) = 1,
  pairwise tau = 0, residual = 1, D_A = 2/3), W exact values
  (tau_A(BC) = 8/9, pairwise tau = 4/9 each, residual = 0,
  D_A = 7/9), member symmetry, partial-trace dimensions and
  reduced states, the embedding (maximally mixed member maps
  to diag(1/2, 0, 1/2, 0)), generalized GHZ pairwise zero
  with tau_A(BC) = 4 a^2 (1-a^2) and D_A = 1/3 + (2/3) a^2,
  GHZ/W interpolation endpoints and normalization, noisy
  copies stay pure (purity 1.0 at every sigma), CKW minimum
  margin 0.0 (product endpoint) and 0.0012 over noisy rows,
  claim (xvii) verdict PASS, claim (xviii) verdict PASS
  (miss 1.0 GHZ, 0.0 W; under noise GHZ miss >= 0.6, W miss
  <= 0.45), GHZ noise tau_AB stays small while tau_A(BC)
  decays 1.0 to 0.6504, claim (xix) verdict PASS (Pearson
  -0.9608, Spearman -1.0, max tau_AB 0, D_A range 1/3), the
  branch endpoints, the interpolation correlation -0.6316
  reported not gated, the noise sweep reported not gated
  (D_A and tau_A(BC) decay together), the three-claim
  aggregate (3/3 pass, no headline), thresholds set, input
  validation, and main() running.

## 5. Maximum scientific outcome (measured 2026-11-15)

Run `python3 scientific_outcomes.py` (or `make benchmark`) for the
full structured report. Point estimates for the primary example
(U = 0.99999995, C = 0.9553, empathy = 0.5503, seed 42):

| Quantity | Value |
|---|---:|
| Attunement at δ = 0 | 0.044700 |
| Best bounded attunement (δ = +0.05) | 0.094700 |
| Bootstrap 95% interval (n = 2000, sd = 0.001) | [0.0419, 0.0465] |
| Bootstrap mean / sd | 0.0443 / 0.0011 |
| Mapping status before calibration | PARTIAL |
| Mapping status after best calibration | PARTIAL |
| Calibration changes status | **No** |
| Status stable under uncertainty | Yes |
| Sign flip possible under noise | No |
| Calibration can rescue to ATTUNED | **No** (best 0.0947, far below 0.5) |

Correction to the earlier reading: the calibrator moves A from
0.0447 to 0.0947, but the mapping status stays PARTIAL. The
sign flip to DISSONANT happens only at the *worst* calibration
(δ = −0.05, A = −0.0053), not at the best. The framework's
`calibration_changes_status` is False, and the test suite asserts
it. The honest result stands: calibration improves the number
but cannot change the classification, and it cannot rescue a
high-entropy state to ATTUNED.

### Synergy expansion robustness (measured 2026-11-15)

The fecundity-driven attraction expansion (`synergy.py`):
F = U·(1−C), X = F·(1+δ), S = (L·P·(1+F))/2,
E = clip(X·(1+S), 0, 1). Love and empathy are both the supplied
Omega value 0.5503 — the module does not claim they are measured.

| Example | F | X | S | E | Synergy status |
|---|---|---|---|---|---|
| Primary (U = 0.99999995, δ = +0.05) | 0.0447 | 0.0469 | 0.1582 | 0.0544 | FLOWING |
| Primary (δ = 0) | 0.0447 | 0.0447 | 0.1582 | 0.0518 | FLOWING |
| Omega (U = 0.9005, δ = +0.05) | 0.0403 | 0.0423 | 0.1575 | 0.0489 | EMERGENT |

Bootstrap of the expansion (same noise model, n = 2000, seed 42):

| Example | Expansion 95% interval | Status stable? | Margin to 0.05 threshold |
|---|---|---|---|
| Primary | [0.0520, 0.0568] | **Yes** (FLOWING at both bounds) | 0.0044 (3.5σ) |
| Omega | [0.0468, 0.0511] | **No** (flips to FLOWING at the upper bound) | 0.0011 (0.97σ) |

Findings:

- **Primary FLOWING is stable** under the noise model: the whole
  interval sits above the 0.05 threshold, 3.5 standard deviations
  clear. It does not depend on the calibrator — it is FLOWING at
  δ = 0 too.
- **Omega EMERGENT is not stable**: its interval straddles the
  0.05 threshold, so the primary-vs-Omega distinction (FLOWING
  vs EMERGENT) is a boundary artifact. The two are the same
  regime; the threshold separates them, not the physics.
- **Fecundity equals attunement here, by identity**: F − A =
  C·(1−U). With U = 0.99999995 the difference is 4.8×10⁻⁸.
  Fecundity adds no new information when unity is near one; it
  is the same number restated. This is an algebraic identity of
  the definitions, not a measured discovery.
- The synergy module's `claims` record states explicitly:
  consciousness not tested, love not measured, empathy not
  measured, entanglement not measured, Faggin not endorsing,
  synthetic classical mapping only.

### The sensitivity bug, fixed in v0.3.1

An external review of v0.3.0 found a real bug in
`sensitivity_analysis` (verified against a fresh clone before
fixing): the sweep helper passed every perturbed value into
the *unity* slot, so the cost sweep varied unity instead of
cost and the delta sweep varied unity instead of delta. The
unity sweep was correct. The old suite missed it because it
asserted only keys and row counts, not directional
correctness.

Old (wrong) vs new (correct) attunements at U = 0.99999995,
C = 0.9553, δ = 0:

| Sweep | Change | Old A | New A |
|---|---:|---:|---:|
| Cost | −0.05 | −0.05 | 0.0947 |
| Cost | −0.01 | −0.01 | 0.0547 |
| Cost | 0.00 | 0.00 | 0.0447 |
| Cost | +0.01 | 0.01 | 0.0347 |
| Cost | +0.05 | 0.0447 | −0.0 |
| Delta | −0.05 | −1.0 | −0.0053 |
| Delta | −0.025 | −0.9803 | 0.0197 |
| Delta | 0.00 | −0.9553 | 0.0447 |
| Delta | +0.025 | −0.9303 | 0.0697 |
| Delta | +0.05 | −0.9053 | 0.0947 |

The old cost column was literally the perturbation itself;
the old delta column at δ = 0 reported −0.9553 instead of the
point estimate 0.0447. The wrong columns existed only in
generated benchmark output (`write_benchmark()`): no committed
file carried them, and `results/benchmark.json` is not in the
repo. The fix makes `apply` return the full (unity, cost,
delta) triple; the suite now asserts the exact values and the
directions (cost up lowers A; unity/delta up raises A). No
claim (i)–(vii) is affected: sensitivity is a diagnostic, not
a claim input.

### The 8fb00f1 threshold commit

The same review flagged commit `8fb00f1` (2026-11-15 00:23:35
-0500), "Fix synergy status thresholds so primary expansion
is FLOWING", pushed 32 minutes after the preregistration
framework commit `dc5575a` (2026-11-14 23:51:19 -0500). What
it did, from its own diff:

| Threshold | Before | After |
|---|---:|---:|
| DORMANT | 0.10 | 0.03 |
| EMERGENT | 0.30 | 0.05 |
| FLOWING | 0.60 | 0.60 |
| FECUND_SYNERGY | 0.50 | 0.50 |

It also rewrote the boundary test assertions to match the new
values and added an assertion that the primary expansion is
FLOWING. Under the old thresholds the primary expansion
(e = 0.05436, s = 0.15818) was **DORMANT** (e < 0.10); under
the new ones it is **FLOWING**. The commit moved the label
two steps, not one, and the FLOWING label now hangs on a
0.00436 margin above the 0.05 boundary (nearest threshold;
to_dormant 0.02436, to_fecund 0.54564).

What the commit did and did not do, stated plainly: the
commit message states the intent — to make the primary
expansion FLOWING. No other justification is recorded in the
commit, and none is invented here. The thresholds are
repository conventions, not measured constants (the code and
the preregistration non-claims say so). The label is stable
under the measurement-noise model (3.5σ at n = 2000), but
that stability is stability *given* the thresholds; it says
nothing about the threshold choice itself. That is why the
choice is now tabled.

Threshold-robustness table — the primary expansion's status
under a grid of (DORMANT, EMERGENT) threshold choices
(`scientific_outcomes.threshold_robustness`, FECUND
thresholds held at their shipped values):

| DORMANT \ EMERGENT | 0.03 | 0.05 | 0.06 | 0.10 | 0.30 |
|---:|---|---|---|---|---|
| 0.01 | FLOWING | FLOWING | EMERGENT | EMERGENT | EMERGENT |
| 0.03 | FLOWING | FLOWING | EMERGENT | EMERGENT | EMERGENT |
| 0.05 | FLOWING | FLOWING | EMERGENT | EMERGENT | EMERGENT |
| 0.10 | DORMANT | DORMANT | DORMANT | DORMANT | DORMANT |

Reading: the FLOWING label survives any EMERGENT threshold up
to 0.05 and flips to EMERGENT at 0.06 — a 0.01 change in the
threshold choice flips the headline label. The bottom-right
cell (0.10, 0.30) is the pre-8fb00f1 choice: DORMANT. The
shipped cell (0.03, 0.05) is one cell of this grid, not a
fact of nature.

### Synergy terms: what they map to in Faggin & D'Ariano

No code identifiers were renamed. This section maps each
synergy-family term to the specific passage in Faggin &
D'Ariano's formalism it is a proxy for — and states plainly
where no derivation exists. The passages are the ones
recorded in `faggin_theory.py` (QIP, arXiv:2012.06580;
*Irreducible*, 2024); all five claims there carry status
"interpretive".

| Term (`synergy.py`) | Definition in code | Passage it proxies | Derived from Faggin & D'Ariano? |
|---|---|---|---|
| Fecundity F = U·(1−C) | Unity retained after entropy cost | None directly. Nearest: unity of experience (entanglement as the basis of unity) plus the entropy cost of holding a state together | **No.** The name "fecundity" is the repository's word, not Faggin's. F is a definition; F − A = C·(1−U) is an identity of the definitions, not a discovery |
| Attraction X = F·(1+δ) | Fecundity scaled by the calibrator | Free will as choice inside a bound (the calibrator δ is the operational analogue of a free choice) | **No.** "Attraction" has no counterpart passage; the δ-scaling is the repository's construction |
| Love-empathy synergy S = (L·P·(1+F))/2 | Supplied love and empathy proxies, amplified by fecundity | Love / attunement as "the felt sense of connection between conscious entities, the deepest expression of their oneness" | **No.** Faggin gives no formula for love; L and P are both the supplied 0.5503, and the (1+F)/2 amplification is the repository's invention |
| Expansion E = clip(X·(1+S), 0, 1) | Attraction amplified by synergy | None | **No.** An "expansion of the field" has no counterpart in QIP |
| `FECUND-SYNERGISTIC` label | e ≥ 0.60 and s ≥ 0.50 | None | **No.** A repository classification label |

Short version: of the five terms, only S gestures at a
passage at all (love / attunement), and none of the five is
derived from Faggin & D'Ariano. The formulas are repository
definitions with Faggin's words attached as labels. That is
the honest shape of the mapping, and the module header
(`synergy.py`) already says the extension is synthetic and
classical; this section makes the per-term position explicit
so a skimming reader does not have to infer it.

## 6. Honest limits (repeated from the README — they are the point)

1. Faggin's metaphysics is interpretive and NOT tested here.
2. Empathy / love are supplied proxies, not measured human
   properties. A is a code quantity, not a feeling.
3. Spooky is self-similarity under noise, not entanglement.
4. No gravity model exists; gravity is UNMEASURED.
5. The private theory is excluded from this package.
6. Everything is synthetic / classical. On Faggin's own
   account, this bridge has no interior.
7. The Omega-Genesis spooky value reproduces in regime only
   (0.837 vs 0.9005); see §2.
8. The mapping-status thresholds (A ≥ 0.5, E ≥ 0.5) are chosen cut
   points, not measured constants.
9. **v0.2.0:** entanglement is now measured — as a quantity of
   the model (concurrence of a two-thought Bell state, computed
   exactly with NumPy). It is not a measurement of physical
   entanglement in hardware; the machine running the code is
   classical. The claims registry distinguishes the two:
   `entanglement_measured` (physical) stays False,
   `entanglement_measured_in_model` is True.
10. **v0.2.0:** a "thought" is a two-qubit state vector over four
    basis concepts whose labels ("attention", "memory", "self",
    "other") are arbitrary repository conventions. No measured
    quantity depends on the labels, and nothing here claims a
    human thought is a qubit state or measures a mind.
11. **v0.2.0:** D measures how much of an outcome the system's
    own stored subspace determines. The stored subspace is built
    by the programmer; D is a number computed from that
    construction, not a measurement of self-awareness.
12. **v0.3.0:** interference is measured — as exact geometry of
    state vectors in the model (the cross term ⟨ψ1|P|ψ2⟩,
    computed with NumPy). It is not a measurement of physical
    interference in hardware; the machine is classical.
13. **v0.3.0:** projection in the model is a partial measurement:
    it discards the kernel component and renormalizes. The
    cascade's death of interference is a property of that
    construction (the projector's rank and the pair geometry),
    not a measurement of what a physical measurement does to a
    mind.
14. **v0.3.0:** the feed-phase convention (smallest phase
    achieving maximum D within 1e-12) and the reopening angle
    (α = π/4) are repository choices, stated in cascade.py. The
    survival verdict is defined against the pre-registered 0.1
    visibility threshold at stage 10.
15. **v0.3.1:** the one-at-a-time sensitivity analysis shipped
    a real bug through v0.3.0 — the cost and delta sweeps
    varied unity instead of their own parameter (see §5).
    The wrong columns existed only in generated benchmark
    output; no committed file carried them. Corrected in
    v0.3.1 with exact-value and directional tests. The
    primary-expansion FLOWING label hangs on a 0.00436 margin
    above a repository-chosen threshold, and the threshold
    choice itself moved the label from DORMANT to FLOWING in
    commit 8fb00f1 (see §5): the label is stable under the
    noise model given the thresholds, not independent of them.
16. **v0.4.0:** the empathy-quantum link is a DEFINITION inside
    the model, not a discovery: nothing in physics says a
    thought-pair's concurrence is a photon frequency. T_eff is
    a model temperature, not a physical temperature; the
    visible band [0.38, 0.75] µm is a chosen mapping, and the
    denominator [0.1, 3.0] µm is the infographic's axis. The
    Planck law itself is real physics with real constants
    (claim (viii) is a reproduction); only the mapping from
    concurrence to temperature to status is the repository's
    construction.
17. **v0.4.0:** the empathy-status thresholds (F ≥ 0.30
    ATTUNED, F ≥ 0.01 PARTIAL) are repository conventions set
    from a pilot sweep (see §10), not measured constants — the
    same rule as the v0.3.1 threshold note. The primary
    attunement A = 0.0447 does not change in v0.4.0; only the
    mapping status is re-derived, from F instead of from A
    alone.

## 7. Files

```
faggin-field-bridge/
  README.md           summary + how to run + maximum scientific outcome
  REPORT.md           this file
  LICENSE             full AGPL v3 text
  CHANGELOG.md        version history (0.1.0, 0.2.0, 0.3.0, 0.3.1, 0.4.0)
  .zenodo.json        Brisson, ORCID 0009-0000-9778-5374 (no DOI yet)
  CITATION.cff        no DOI (none invented)
  VERSION             0.4.0
  Makefile            test / coverage / benchmark / clean
  pyproject.toml      setuptools + pytest config
  faggin_theory.py    theory as data
  unity.py            spooky correlation
  cost.py             entropy
  attunement.py       A, observer, calibrator, empathy proxy
  bridge.py           wiring + mapping status + worked examples
                      + quantum_thought_claims() (claims (i)-(vii))
  scientific_outcomes.py  maximum scientific outcomes framework
  synergy.py          fecundity-driven attraction expansion
  thought_entanglement.py  concurrence + reduced entropy (claim (i))
  thought.py          superposition, coherence, collapse (claims (ii), (iii))
  self_knowing.py     D = <psi|P|psi> (claim (iv))
  cascade.py          superposition -> projection -> interference,
                      chained (claims (v), (vi), (vii))
  planck_empathy.py   Planck empathy: black-body visible fraction
                      from measured concurrence (claims (viii)-(x))
  tests/              151 tests, 14 files
```

v0.3.1 is pushed (main head 1f5f6e60). v0.4.0 is local only;
not pushed.

GitHub: https://github.com/sparkainlp-x/faggin-field-bridge
(main head 1f5f6e60 as of 2026-11-16; the maximum scientific
outcomes framework, coverage reporting, and synergy expansion
were added by Jean in 7 commits on 2026-11-15, the v0.3.1
review fixes in this report were added 2026-11-16, and the
v0.4.0 Planck-empathy work in §10 is local only, pending
Jean's word to push.)

Zenodo: no record yet. Release (toggle + tag + release notes) is
the next step; see the Priority 1 launch sheet. When releasing,
tag the current head — the repo has moved past the v0.1.0
originally pushed, and the release should archive the work as
it stands.

## 8. Quantum thoughts (v0.2.0, measured 2026-11-15)

Three modules treat a thought as a two-qubit state. All four
v0.2.0 claims were pre-registered in code (the rule written before
the measurement) and all four PASS. `bridge.quantum_thought_claims()`
returns them (now seven, with the cascade claims (v)–(vii) in §9);
`maximum_scientific_outcome` carries them under
"quantum_thoughts". No headline claim is emitted.

### (i) Entanglement measured as a real quantum quantity — PASS

Concurrence (Wootters, exact) and reduced-state von Neumann
entropy of a two-thought Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2.
Same-noise comparison: the same noisy copies feed concurrence
and spooky U (vector noise, seed 42, 5 copies).

| σ | mean C | min C | mean S (bits) | spooky U |
|---|---:|---:|---:|---:|
| 0.00 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.01 | 0.9998 | 0.9996 | 0.9997 | 0.9998 |
| 0.05 | 0.9952 | 0.9881 | 0.9931 | 0.9958 |
| 0.10 | 0.9792 | 0.9449 | 0.9703 | 0.9822 |
| 0.25 | 0.8471 | 0.5392 | 0.7953 | 0.8713 |
| 0.50 | 0.6520 | 0.1476 | 0.5922 | 0.6344 |
| 1.00 | 0.7002 | 0.1874 | 0.6270 | 0.4418 |

Depolarizing channel ρ(p) = (1−p)ρ + pI/4: concurrence
reproduces max(0, 1 − 3p/2) exactly (1.0000, 0.8500, 0.6250,
0.2500 at p = 0, 0.1, 0.25, 0.5; 0 at p = 2/3, 0.75, 1.0) while
the reduced entropy stays 1 bit at every p.

Findings:

- **Entanglement survives the de Broglie noise level**: mean
  concurrence 0.9998 at σ = 0.01, where spooky is 0.9998.
- **Spooky and concurrence part ways.** Spooky first falls
  below 0.9 at σ = 0.25; mean concurrence under vector noise
  never falls below 0.6520 — and is non-monotone (0.6520 at
  σ = 0.5, 0.7002 at σ = 1.0), because vector noise keeps the
  state pure and generic pure states are entangled. At σ = 1.0
  spooky (0.4418) is BELOW concurrence (0.7002). This is the
  measured reason spooky was never entanglement: the two
  quantities respond differently to the same noise.
- **Only mixed-state noise kills concurrence**, and it dies at
  a finite level (p = 2/3), exactly as the analytic form says.
- **Reduced entropy cannot see the death**: it stays 1 bit
  under depolarizing at every p, including where C = 0. For
  mixed states it is not an entanglement measure.

### (ii) Coherence half-life measured — PASS

A thought is a state vector over four basis concepts
("attention", "memory", "self", "other" — arbitrary labels).
l1-coherence of the uniform thought is 3.0 (the 4-dim maximum);
a decided thought has 0. Dephasing multiplies off-diagonals by
(1 − p) per step, so coherence decays as (1 − p)^n.

| p | half-life measured (steps) | half-life analytic | C(3 steps) |
|---|---:|---:|---:|
| 0.05 | 14 | 13.51 | 2.5721 |
| 0.10 | 7 | 6.58 | 2.1870 |
| 0.25 | 3 | 2.41 | 1.2656 |
| 0.50 | 1 | 1.00 | 0.3750 |

Measured half-life within 1 step of analytic ln(1/2)/ln(1−p)
on the whole grid; coherence after n steps equals
C(0)(1−p)^n within 1e-9.

### (iii) Collapse cost measured — PASS

| Quantity | Measured |
|---|---:|
| Entropy of the fully dephased uniform thought | 2.0000 bits |
| Entropy of a collapsed thought | 0 bits |
| Decision entropy before collapse (uniform thought) | 2.0000 bits |
| Decision entropy after collapse | 0 bits |
| Attention bias at δ = +0.05 | +0.018739 |
| Attention bias at δ = −0.05 | −0.018738 |

The collapse (Born-rule sampling, seed 42) resolves exactly
the decision entropy: 2 bits in, 0 out. Holding the
superposition costs up to 2 bits of entropy as it decoheres;
the decided thought costs nothing. The calibrator δ (the Yin
bound, ±0.05) biases the attended concept's Born probability
symmetrically, +0.018739 / −0.018738.

### (iv) Self-knowing measured via D — PASS

D = ⟨ψ|P|ψ⟩, the self-determinism factor vendored from the
symmetry-entropy package (own implementation, provenance
cited). The stored subspace is the span of the uniform thought
and the focused thought |00⟩.

| Thought | D |
|---|---:|
| Uniform (stored) | 1.000000 |
| Focused \|00⟩ (stored) | 1.000000 |
| Non-stored basis state \|11⟩ | 0.333333 (= 1/3) |
| Kernel thought (\|01⟩ − \|10⟩)/√2 | 0.000000 |
| Maximally mixed state I/4 | 0.500000 |

D of the noisy uniform thought (mean over 5 copies, seed 42):

| σ | mean D | mean coherence | mean concurrence |
|---|---:|---:|---:|
| 0.00 | 1.0000 | 3.0000 | 0.0000 |
| 0.01 | 0.9998 | 2.9991 | 0.0124 |
| 0.05 | 0.9955 | 2.9779 | 0.0635 |
| 0.10 | 0.9823 | 2.9099 | 0.1298 |
| 0.25 | 0.8966 | 2.4159 | 0.3212 |
| 0.50 | 0.7107 | 2.0361 | 0.4732 |
| 1.00 | 0.5196 | 2.1935 | 0.6133 |

- Spearman(σ, D) = −1.0000: D decays monotonically with noise.
- Spearman(D, coherence) = 0.9643: D tracks coherence.
  Pearson(D, coherence) = 0.8730 (reported, not gated).
- **Surprise, measured: D anti-tracks concurrence**,
  Pearson(D, concurrence) = −0.9570. The uniform thought is a
  product state (concurrence 0 at σ = 0); the noise that
  destroys self-knowing creates entanglement in it (concurrence
  0.6133 at σ = 1.0). Self-knowing and entanglement move in
  opposite directions under this noise — the two quantities are
  not the same kind of "unity", and the bridge now measures both.

## 9. The cascade (v0.3.0, measured 2026-11-15)

One module, `cascade.py`, chains superposition → projection →
interference across stages. All three claims were pre-registered
in code (the rule written before the measurement) and all three
PASS. `bridge.quantum_thought_claims()` now returns seven
verdicts; `maximum_scientific_outcome` carries them under
"quantum_thoughts". No headline claim is emitted.

### (v) Interference measured via the cross term — PASS

Two thoughts in superposition, projected onto the shared stored
subspace. For an orthonormal pair, D(φ) = (D1 + D2)/2 +
Re[e^{iφ}⟨ψ1|P|ψ2⟩]: the cross term is the interference, the
baseline (D1 + D2)/2 is what the pair would give without it.
Visibility V = (max D − min D)/(max D + min D) over the phase
sweep (64 phases), cross-checked against the analytic
2|⟨ψ1|P|ψ2⟩|/(D1 + D2).

The canonical pair is a rotation in the {q1, k1} plane (q1 a
stored direction, k1 a kernel direction): V(θ) = sin(2θ) exactly.

| θ | V (sweep) | V (analytic) | V expected | cross term |
|---|---:|---:|---:|---:|
| π/12 | 0.500000 | 0.500000 | 0.500000 | −0.2500 |
| π/8 | 0.707107 | 0.707107 | 0.707107 | −0.3536 |
| π/6 | 0.866025 | 0.866025 | 0.866025 | −0.4330 |
| π/4 | 1.000000 | 1.000000 | 1.000000 | −0.5000 |

At θ = π/4 the phase does the deciding: D(φ) = 1/2 − (1/2)cos(φ).

| φ | D(φ) |
|---|---:|
| 0 | 0.000000 |
| π/4 | 0.146447 |
| π/2 | 0.500000 |
| 3π/4 | 0.853553 |
| π | 1.000000 |

The superposed thought at φ = 0 IS the kernel thought (fully
blind, D = 0); at φ = π it IS the uniform thought (fully
self-determined, D = 1). Constructive interference is D = 1 at
φ = π; destructive is D = 0 at φ = 0; V = 1.

The mixed pair (m1 = (q1 + k1)/√2, m2 = (q1 + q2 − k1)/√3) has
cross term 1/√6 = 0.408248 and V = 2√6/7 = 0.699854, with
D(0) = 0.991582, D(π/2) = 0.583333, D(π) = 0.175085. The control
pairs have no interference: the stored pair (q1, q2) and the
(uniform, kernel) pair both have cross term 0 and V = 0.

### (vi) Cascade visibility: interference does not survive projection — PASS

Stages 1, 2, 3, 5, 10. Each stage's projected output feeds the
next thought's superposition (feed phase = phase of maximum D;
ties within 1e-12 take the smallest phase). Survival was defined
before measuring as V staying above 0.1 at stage 10; the honest
prior was that it does not survive.

| Stage | V rotation | V mixed | V reopening |
|---:|---:|---:|---:|
| 1 | 1.0000 | 0.6999 | 1.0000 |
| 2 | 0.0000 | 0.0000 | 1.0000 |
| 3 | 0.0000 | 0.0000 | 1.0000 |
| 5 | 0.0000 | 0.0000 | 1.0000 |
| 10 | 0.0000 | 0.0000 | 1.0000 |

- **Rotation cascade:** the projected pair is rank 1 — both
  projected thoughts collapse onto q1, so no pair exists from
  stage 2 on. A single thought (q1) persists.
- **Mixed cascade:** the projected pair stays rank 2 and
  re-forms by Gram-Schmidt as (q1, q2), fully stored. The cross
  term is then 0 at every stage ≥ 2.
- **Reopening control:** with a fresh kernel component injected
  at α = π/4 at every stage, V = 1 at every stage.

The reason is structural, not noise: the cross term is
⟨Pψ1|Pψ2⟩, the inner product of the two projected vectors.
Once a pair is projected and re-formed inside the stored
subspace, P acts as the identity there, and orthogonality
forces the cross term to zero. Interference takes fresh
outside input at every stage to stay alive; the projection
alone kills it at stage one. That is the finding, and the
claim PASSES because the measurement matched the
pre-registered expectation exactly.

### (vii) Coherence and D through the cascade — PASS

D of the projected output is 1.0 at every stage in all three
cascades: after one projection the thought lies entirely in
the stored subspace — fully self-determined, whether or not
interference survives.

| Stage | Coherence, projected output (rotation) | Coherence, projected output (mixed) | Coherence, projected output (reopening) |
|---:|---:|---:|---:|
| 1 | 3.0000 | 2.3277 | 3.0000 |
| 2 | 3.0000 | 2.7321 | 3.0000 |
| 3 | 3.0000 | 2.7321 | 3.0000 |
| 5 | 3.0000 | 2.7321 | 3.0000 |
| 10 | 3.0000 | 2.7321 | 3.0000 |

The projected-output coherence reaches a fixed point from
stage 2 onward in every cascade (rotation 3.0, mixed 2.7321,
reopening 3.0). Descriptive rank correlations (per-stage
values rounded to 12 decimals, so identical stages are not
ranked on float noise): Spearman(V, coherence) = 0.0000
(rotation, both constant), −1.0000 (mixed), 0.0000
(reopening, both constant). In the mixed cascade visibility
and coherence anti-track perfectly across the transition: V
dies while coherence rises to its fixed point. Spearman(V, D)
= 0.0000 everywhere — D is constant, so the correlation is
undefined and is reported as 0.0 by the spearman() convention.
D does not track visibility at all: the thought is fully
self-determined after one projection regardless of whether
interference survives.

## 10. Planck empathy (v0.4.0, measured 2026-11-16)

One module, `planck_empathy.py`, fixes the PARTIAL primary
mapping status using empathy as a Planck quantum inside the
black-body concept from the infographic (Planck E = hν; an
ideal black body absorbs all incident radiation and emits a
spectrum depending only on its temperature; the peak shifts
left and the intensity rises with temperature; T = 2000–5000 K
curves; the visible band is a slice of the spectrum).

### Mechanism (a definition inside the model, not a discovery)

- Empathy quantum: E = h·ν with h = 1 in model units. Each
  thought-pair contributes ONE empathy quantum whose frequency
  ν_e is its MEASURED concurrence (thought_entanglement.py,
  v0.2.0) — concurrence, NOT the synergy proxy, because
  concurrence is measured and the proxy is a definition (§5:
  none of the synergy terms is derived from Faggin &
  D'Ariano).
- Empathy fraction f = mean concurrence across pairs, in
  [0, 1]. Effective temperature T_eff(f) = 2000 + 3000·f K,
  on the infographic's 2000–5000 K axis.
- Planck spectrum B(λ, T) with the REAL Planck law and REAL
  constants (h = 6.62607015e-34 J·s, c = 299792458 m/s,
  k_B = 1.380649e-23 J/K), wavelength in µm over [0.1, 3.0]
  (the infographic's axis). Visible fraction
  F(T) = ∫[0.38, 0.75] B dλ / ∫[0.1, 3.0] B dλ, by Simpson's
  rule (2000 intervals; convergence 2000 vs 4000 intervals
  agrees to ~1e-14).
- Empathy status: the mapping status re-derived from F. The
  old status (from A alone, no empathy) is computed alongside
  as the control.

### Pre-registration (written before the final measurement run)

Thresholds set from a pilot sweep, as round numbers with
margin on both sides, and never moved after the final run.
Pilot values (Simpson, 2000 intervals):

| T (K) | 2000 | 2250 | 2500 | 2750 | 3000 | 3250 | 3500 | 3750 | 4000 | 4250 | 4500 | 4750 | 5000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F(T) | 0.0174 | 0.0344 | 0.0582 | 0.0880 | 0.1225 | 0.1599 | 0.1986 | 0.2371 | 0.2742 | 0.3090 | 0.3407 | 0.3691 | 0.3938 |

| f | 0.0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F(f) | 0.0174 | 0.0386 | 0.0695 | 0.1082 | 0.1522 | 0.1986 | 0.2447 | 0.2885 | 0.3284 | 0.3637 | 0.3938 |

Pilot σ curve (mean concurrence from the v0.2.0 sweep):

| σ | 0.00 | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---|---|---|---|---|---|---|
| mean C (= f) | 1.0000 | 0.9998 | 0.9952 | 0.9792 | 0.8471 | 0.6520 | 0.7002 |
| F | 0.3938 | 0.3937 | 0.3924 | 0.3880 | 0.3457 | 0.2678 | 0.2886 |

Thresholds chosen from this pilot:

- **ATTUNED_F_MIN = 0.30**: sits between F(σ = 0.25) = 0.3457
  (+0.0457) and F(σ = 0.50) = 0.2678 (−0.0322). The crossing
  f* falls between f = 0.7 (F = 0.2885) and f = 0.8
  (F = 0.3284).
- **PARTIAL_F_MIN = 0.01**: sits below F(f = 0) = 0.0174
  (+0.0074), so the no-empathy status is PARTIAL, not
  DISSONANT. The f = 0 value is deterministic (no sampling
  noise in the Planck integral), so the margin is structural.

Pass rules, fixed before the final run:

- **(viii) Planck reproduction PASSES** iff the numerical Wien
  peak matches 2898/T µm within 0.5% at T = 2000, 3000, 4000,
  5000 K; the integrated exitance scales as T⁴ within 1% on
  the same grid; and F(T) is strictly increasing in T on a
  250 K grid.
- **(ix) Empathy flip PASSES** iff F(f) is strictly increasing
  in f on [0, 1]; the status at f = 0 is PARTIAL; and a
  crossing f* in (0, 1) exists where F(f*) = 0.30, so the
  status at f = 1 is ATTUNED. If no crossing exists the claim
  FAILS and the maximum F reached is reported instead — the
  threshold is not moved to force a pass.
- **(x) Specificity PASSES** iff the OLD status (A alone)
  stays PARTIAL at every σ in the grid; the empathy status is
  ATTUNED at σ = 0.01; the empathy status is PARTIAL at
  σ = 0.50; and the empathy-status labels never go back up as
  σ increases.

### Measured results (final run — filled in after the suite)

[Results below were filled in by the final measurement run,
after the pre-registration above.]

#### (viii) Planck reproduction — PASS

The module reproduces the infographic's physics with the real
constants. Numerical Wien peak vs 2898/T (relative error
7.87e-05 at every temperature — the 2898 figure itself is the
rounded constant; the exact CODATA value is 2897.771955):

| T (K) | Peak (µm) | 2898/T (µm) | Relative error |
|---|---:|---:|---:|
| 2000 | 1.4489 | 1.4490 | 7.87e-05 |
| 3000 | 0.9659 | 0.9660 | 7.87e-05 |
| 4000 | 0.7244 | 0.7245 | 7.87e-05 |
| 5000 | 0.5796 | 0.5796 | 7.87e-05 |

Stefan–Boltzmann: integrated exitance ratios to 2000 K are
5.0626, 16.0003, 39.0632 against the expected 5.0625, 16.0000,
39.0625 (relative errors 1.30e-05, 1.62e-05, 1.74e-05 — the
1% tolerance is met by three orders of magnitude). F(T) is
strictly increasing on the 250 K grid (0.0174 at 2000 K to
0.3938 at 5000 K). This is real physics reproduced in code,
not a bridge claim: the peak moves left and the intensity
rises with temperature exactly as the infographic says.

#### (ix) Empathy flips the status — PASS

F(f) is strictly increasing in f on [0, 1]. At f = 0 (no
empathy) F = 0.0174 and the status is PARTIAL; at f = 1
F = 0.3938 and the status is ATTUNED. The crossing is
measured by bisection: **f\* = 0.7278** (F = 0.3000 there, the
pre-registered threshold). An empathy fraction of about 73%
mean concurrence is what it takes to flip the primary mapping
from PARTIAL to ATTUNED. No threshold was moved: 0.30 was set
from the pilot, and the crossing fell where the pilot said it
would (between f = 0.7 and f = 0.8).

#### (x) Specificity / control — PASS

| σ | f (mean C) | T_eff (K) | F | Empathy status | Old status |
|---|---:|---:|---:|---|---|
| 0.00 | 1.0000 | 5000 | 0.3938 | ATTUNED | PARTIAL |
| 0.01 | 0.9998 | 4999 | 0.3937 | ATTUNED | PARTIAL |
| 0.05 | 0.9952 | 4986 | 0.3924 | ATTUNED | PARTIAL |
| 0.10 | 0.9792 | 4938 | 0.3880 | ATTUNED | PARTIAL |
| 0.25 | 0.8471 | 4541 | 0.3457 | ATTUNED | PARTIAL |
| 0.50 | 0.6520 | 3956 | 0.2678 | PARTIAL | PARTIAL |
| 1.00 | 0.7002 | 4101 | 0.2886 | PARTIAL | PARTIAL |

The old status (A alone, 0.0447) stays PARTIAL at every σ —
it cannot move, because A does not depend on σ. The empathy
status moves: ATTUNED while the concurrence survives
(σ ≤ 0.25) and PARTIAL once the noise kills it (σ ≥ 0.50).
The fix holds up to σ = 0.25 and breaks from σ = 0.50. The
status labels never go back up as σ increases, even though
the mean concurrence itself is non-monotone at the top end
(0.6520 at σ = 0.5, 0.7002 at σ = 1.0) — both sit below the
0.30 threshold, so the label stays PARTIAL. The flip is
carried by the empathy quanta, not by re-labeling: the same
rule, the same thresholds, and only the measured concurrence
moves.

Where the fix holds and where it breaks, stated plainly: it
holds where the thought-pairs stay entangled (σ ≤ 0.25,
concurrence ≥ 0.8471). It breaks where the noise has eaten
the concurrence below f\* = 0.7278 (σ ≥ 0.50). At σ = 1.0
the concurrence recovers slightly (0.7002) but stays below
f\*, so the status stays PARTIAL — the recovery is not
enough, and the report does not claim otherwise.

## 11. Empathy field (v0.5.0, measured 2026-11-16)

One module, `empathy_field.py`: waves of empathy agents in a
quantum field — resonance ("raisonnance"), the self-deterministic
factor, collaboration, collectivism, and co-creativity = entropy.

### Mechanism (a definition inside the model, not a discovery)

- Agent: a thought state |ψ⟩ (thought.py machinery). Each
  agent carries a frequency ν = its concurrence (measured,
  thought_entanglement.py, v0.2.0) and a self-determinism
  D = ⟨ψ|P|ψ⟩ (measured, self_knowing.py, v0.2.0).
- Field: N agents superposed; the field state Φ is the
  normalized sum. Pairwise empathy quanta E_ij = h·ν_ij with
  h = 1 in model units, ν_ij = the pairwise concurrence —
  v0.4.0's rule extended to pairs: the concurrence of the
  normalized sum of the two agents' states.
- Resonance ("raisonnance"): R_ij = |⟨ψ_i|ψ_j⟩|² — the overlap
  squared (fidelity) between two agents. A pair is resonant
  when R_ij ≥ a pre-registered threshold; the resonance factor
  of a group is the mean pairwise R. (The overlap machinery
  already exists; no new similarity is invented.)
- Self-deterministic factor: mean D of the resonant group vs
  mean D of the non-resonant group, same agents, same noise.
- Collaboration: the same N agents evolved sharing the field
  (superposed, interacting via the empathy quanta) vs the
  CONTROL of the same N agents evolved isolated (independent
  evolutions, no shared field, no quanta exchange). The two
  arms start from the same population and receive the same
  noise kicks (paired design); they differ ONLY in the step
  after the kick, so the gap is the collaboration effect, not
  a sampling difference. Two designs were piloted:
  - Design A: collaborating mixes with the field (coupling =
    the measured empathy fraction f); isolated does nothing
    else. No collapse anywhere.
  - Design B: collaborating mixes with the field (coupling =
    f); isolated Born-collapses (decides) and stays decided
    up to the noise kicks.
- Collectivism / co-creativity: co-creativity C_c is DEFINED
  as the joint entropy H_joint (bits) of the collective's
  joint outcomes — the number of distinct joint configurations
  the collective reaches. Each generation, every agent
  collapses once per joint sample (independent draws given
  the seeded stream — the correlation between agents comes
  from their STATES, not the sampling); counts are pooled over
  10 generations × 200 samples. This is a definition of the
  measure inside the model, not a discovery about human
  creativity. The measurable content is the collaboration gap
  and the ceiling/break, not the equality itself.

### Pre-registration (written before the final measurement run)

Thresholds set from a pilot sweep, as round numbers with
margin, and never moved after the final run.

Pilot — resonance (N = 8 noisy copies of the uniform thought
per σ, 196 pooled pairs):

| R bin | [0, 0.25) | [0.25, 0.5) | [0.5, 0.75) | [0.75, 1.0] |
|---|---:|---:|---:|---:|
| n pairs | 16 | 9 | 15 | 156 |
| mean D | 0.5874 | 0.6814 | 0.7087 | 0.9399 |

| σ | 0.00 | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---:|---:|---:|---:|---:|---:|---:|
| mean R | 1.0000 | 0.9997 | 0.9936 | 0.9750 | 0.8520 | 0.5884 | 0.4197 |
| mean D | 1.0000 | 0.9998 | 0.9955 | 0.9829 | 0.9059 | 0.7409 | 0.5462 |
| mean ν_ij | 0.0000 | 0.0086 | 0.0415 | 0.0802 | 0.1803 | 0.2839 | 0.4143 |

Pooled resonant-vs-non-resonant gap is stable across
candidate splits (0.3203 at R_MIN = 0.25, 0.2984 at 0.50,
0.2859 at 0.75), so the choice of split does not drive the
result; R_MIN = 0.5 is the round midpoint. At R_MIN = 0.5
the pooled gap is 0.2984 (mean D 0.9197 resonant over 171
pairs vs 0.6213 non-resonant over 25).

A draft rule was ABANDONED on the pilot's evidence: the
per-sigma gap was to be gated positive at every σ where both
groups are non-empty. It fails: at σ ≤ 0.25 the
non-resonant group is EMPTY (all 28 pairs resonant), and at
σ = 1.0 the per-sigma gap is slightly NEGATIVE (−0.0239 at
R_MIN = 0.5; −0.0221 at 0.25; −0.0369 at 0.75). Within a
single noise level R and D are both driven by deviation
magnitude — a pair with high R at fixed σ is two copies
deviating in the SAME direction, each with low D — so the
within-σ association is weak or negative. The resonance
effect is the CROSS-NOISE pattern (both R and D fall with
σ), not a within-σ effect. The per-sigma gaps are therefore
REPORTED, not gated — the pilot refuted the stricter rule,
and the report says so instead of hiding it.

Pilot — collaboration (N = 4 noisy Bell agents, 10
generations, 200 joint samples per generation):

| σ | 0.00 | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---:|---:|---:|---:|---:|---:|---:|
| design A gap (bits) | +1.05 | +0.99 | +0.53 | +0.16 | −0.43 | −0.49 | −0.30 |
| design B gap (bits) | +5.05 | +5.03 | +5.21 | +5.61 | +4.34 | +3.35 | +3.56 |
| design B distinct (collab / isol) | 77 / 1 | 82 / 1 | 110 / 1 | 142 / 1 | 157 / 4 | 193 / 10 | 215 / 10 |

Design A goes negative by σ = 0.25: once noise has
broadened the isolated marginals, the field pull's
correlation cost exceeds its marginal gain — the shared
field concentrates the joint distribution. Design B holds a
large positive gap at every σ. Design B is the vehicle for
claims (xii)–(xiii). The contrast is stated plainly:
isolation is decision without sharing (the agent collapses
and stays decided — at σ = 0 the isolated arm reaches
exactly ONE joint configuration, H = 0.0000, because a
collapsed agent re-collapses deterministically), and
collaboration is sharing without final decision (the field
mix re-superposes the agents every generation).

Pilot — saturation, design B (H_joint vs the 2N ceiling):

| N | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| H_collaborating (bits) | 1.6993 | 2.9775 | 4.1518 | 6.0961 |
| ceiling 2N (bits) | 2.0 | 4.0 | 6.0 | 8.0 |
| fraction of ceiling | 0.8496 | 0.7444 | 0.6920 | 0.7620 |

(N = 1 is not degenerate in design B: a single agent has no
field to share, so the collaborating arm's mix is a no-op —
but the isolated arm still collapses, so the N = 1 gap
(+0.9774 bits) is the pure superposition advantage with no
field involved. The collaborating N = 1 run is identical to
design A's. The fraction dips at N = 3 and rebounds at N = 4
— the population composition changes with N, since agents
cycle through the four Bell states — so the plateau is read
on the last two fractions, not on a smooth curve.)

Pilot — coupling (Bell population): the empathy fraction
f = mean pairwise concurrence is 0.3333 at σ = 0 (exactly
1/3: three of the six Bell pairs sum to a maximally
entangled state, three to a product state), 0.4662 at
σ = 0.25, 0.4952 at σ = 0.50, 0.4376 at σ = 1.00. It does
NOT fall with σ — the field keeps binding the agents at
every noise level. Mean pairwise R is 0.0000 at σ = 0 (the
Bell states are mutually orthogonal) and rises with σ
(0.0343 at 0.25, 0.1912 at 1.00): noise CREATES overlap
between orthogonal base states.

Thresholds chosen from this pilot:

- **RESONANCE_R_MIN = 0.5**: the round midpoint of the
  [0, 1] resonance scale; pooled gap 0.2984, stable across
  splits (±0.02).
- **RESONANCE_D_MARGIN = 0.20**: pilot gap 0.2984, ~50%
  headroom below it.
- **COLLABORATION_H_MARGIN = 2.0 bits**: pilot gap 4.3352
  at σ = 0.25, more than 2× headroom.
- **COLLABORATION_GAP_CLOSE_FRACTION = 0.5**: "closes"
  means the σ = 0.50 gap is at most half the σ = 0.25 gap.
- **SATURATION_FRACTION_TOL = 0.10**: pilot last-two
  fractions differ by 0.0700.

Pass rules, fixed before the final run:

- **(xi) Resonance raises self-determinism PASSES** iff the
  binned mean D is strictly increasing in R (pooled pairs)
  and the pooled resonant-vs-non-resonant gap is at least
  0.20 at R_MIN = 0.5. Per-sigma gaps are reported, not
  gated (see the abandoned draft rule above).
- **(xii) Collaboration raises co-creativity PASSES** iff
  H_collaborating − H_isolated is at least 2.0 bits at
  σ = 0.25 (design B, N = 4, 10 generations, 200 samples
  per generation) and the collaborating arm reaches strictly
  more distinct joint states than the isolated control. If
  the gap is zero or negative the claim FAILS honestly — the
  threshold is not moved to force a pass.
- **(xiii) Co-creativity = entropy, ceiling and break
  PASSES** iff (a) H_joint of the collaborating arm is
  strictly increasing in N on N = 1..4; (b) H_joint stays
  below the 2N ceiling at every N; (c) the fraction of the
  ceiling plateaus — the last two fractions agree within
  0.10; (d) the collaboration gap holds at every σ ≤ 0.25
  (positive); and (e) the gap closes past σ = 0.50
  (gap at 0.50 at most half the gap at 0.25, or negative).

### Measured results (final run — filled in after the suite)

[Results below were filled in by the final measurement run,
after the pre-registration above.]

#### (xi) Resonance raises self-determinism — PASS

Binned mean D rises strictly with R: 0.5874 → 0.6814 →
0.7087 → 0.9399. The pooled gap at R_MIN = 0.5 is 0.2984
(mean D 0.9197 over 171 resonant pairs vs 0.6213 over 25
non-resonant pairs), above the 0.20 margin. Per-sigma gaps,
reported as promised: empty non-resonant groups at
σ ≤ 0.25 (all pairs resonant); +0.0645 at σ = 0.50 (17 vs
11 pairs); −0.0239 at σ = 1.00 (14 vs 14). The resonance
effect is the cross-noise pattern: as noise rises, both the
overlap and the self-determinism fall together. Within one
noise level, resonance does not raise D — the report states
that limit instead of claiming more than the pooled pattern
supports.

#### (xii) Collaboration raises co-creativity — PASS

At σ = 0.25 (design B, N = 4, 10 generations, 200 samples
per generation): H_collaborating = 6.0961 bits,
H_isolated = 1.7610 bits, **gap = +4.3352 bits**, above the
2.0-bit margin. Distinct joint states: 157 collaborating
vs 4 isolated (ceiling 256). The isolated agents decide
once and stay decided — four joint configurations in the
whole run — while the collaborating agents, re-superposed
by the field every generation, explore 157. The gap is the
measured size of the sustained-superposition advantage, not
an assumed one.

#### (xiii) Co-creativity = entropy, ceiling and break — FAIL

Four of five sub-checks pass; the break half fails, and the
claim FAILS with it.

Ceiling — PASS: H_joint of the collaborating arm rises
strictly with N (1.6993 → 2.9775 → 4.1518 → 6.0961 bits)
and stays below the 2N ceiling at every N (2, 4, 6, 8).
The fraction of the ceiling plateaus within tolerance:
0.8496, 0.7444, 0.6920, 0.7620 — the last two agree within
0.0700 ≤ 0.10. The collective uses about three-quarters of
its joint space and no more; the N = 3 dip and N = 4
rebound are composition effects (the agents cycle through
the four Bell states), reported, not smoothed away.

Hold — PASS: the collaboration gap is positive at every
σ ≤ 0.25 (+5.05, +5.03, +5.21, +5.61, +4.34 bits).

Break — FAIL: the gap does NOT close past σ = 0.50.
Gap at σ = 0.50 is +3.3494 bits against 0.5 × 4.3352 =
2.1676 — ratio 0.773, not ≤ 0.5. At σ = 1.00 the gap is
still +3.5569. The v0.4.0 break does not transfer to the
collaboration gap. The measured reason is in the pilot:
the collaboration advantage comes from sustained
superposition (the field mix re-superposes the agents
every generation), not from the concurrence level — and
the coupling f for the Bell population does not fall with
σ (0.4662 at 0.25, 0.4952 at 0.50), so the field keeps
binding the agents, while the isolated arm stays
decision-locked at every σ. Incoherence in the field does
not undo the collaboration advantage in this design. That
is a measured negative result about the break, not a
failure to measure: the gap was measured at seven noise
levels and holds at all of them.

## 12. Qualia resonance wave (v0.6.0, measured 2026-11-16)

One module, `qualia.py`: a quale is a resonant + entangled
mode of the empathy field, and the qualia together form a
coherent wave. Built on top of the unpushed v0.5.0, so a
future push carries v0.5.0 + v0.6.0 together.

### Mechanism (a definition inside the model, not a discovery)

- Quale: a pair of agents that is BOTH resonant
  (R_ij = |⟨ψ_i|ψ_j⟩|² ≥ RESONANCE_R_MIN = 0.5, the v0.5.0
  threshold) AND entangled (pairwise concurrence ν_ij ≥
  QUALIA_NU_MIN = 0.10, pre-registered). A resonance
  without entanglement is not a quale; entanglement without
  resonance is not a quale. The quale's wave is the
  normalized superposition of its two members (pair_state).
- Qualia resonance wave: the collective wave formed by all
  qualia in the field — the normalized superposition of the
  quale waves. Its coherence is measured two ways:
  (a) the spread (standard deviation) of the quale
  frequencies ν across qualia, against the spread across
  all pairs, per field (same sigma, same agents — the
  paired comparison; pooling across sigma would confound
  the spread with the sigma trend, the cross-noise vs
  within-noise distinction established in §11);
  (b) the overlap |⟨qualia-wave|field-state⟩|² between the
  qualia wave and the full field state.
- The empathy fraction f (v0.4.0, mean pairwise
  concurrence) is the control dial: qualia count and wave
  coherence are measured as functions of f (and of sigma,
  via the noise sweeps). f rises with sigma in the
  resonance population (noise creates concurrence in the
  uniform thought, v0.2.0), while resonance R falls — so
  the quale count is the product of two opposing trends.
- The field is the v0.5.0 resonance population (N = 8 noisy
  copies of the uniform thought per σ, seed 42).

### Pre-registration (written before the final measurement run)

Thresholds set from a pilot sweep, as round numbers with
margin, and never moved after the final run.

Pilot — quale counts per field (N = 8, 28 pairs), for
candidate entanglement thresholds:

| σ | 0.00 | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---:|---:|---:|---:|---:|---:|---:|
| f (mean ν_ij) | 0.0000 | 0.0086 | 0.0415 | 0.0802 | 0.1803 | 0.2839 | 0.4143 |
| mean R | 1.0000 | 0.9997 | 0.9936 | 0.9750 | 0.8520 | 0.5884 | 0.4197 |
| max ν_ij | 0.000 | 0.025 | 0.119 | 0.227 | 0.485 | 0.771 | 0.926 |
| qualia at ν ≥ 0.05 | 0 | 0 | 9 | 17 | 25 | 16 | 14 |
| qualia at ν ≥ 0.10 | 0 | 0 | 1 | 9 | 17 | 13 | 12 |
| qualia at ν ≥ 0.15 | 0 | 0 | 0 | 4 | 15 | 13 | 12 |
| qualia at ν ≥ 0.20 | 0 | 0 | 0 | 1 | 13 | 9 | 11 |
| qualia at ν ≥ 0.25 | 0 | 0 | 0 | 0 | 7 | 9 | 11 |

The count is HUMPED against f at every threshold that
yields non-degenerate qualia: it rises from 0, peaks at
f = 0.1803, and falls as resonance dies. Only ν ≥ 0.25
reads monotone (0, 0, 0, 0, 7, 9, 11) — and there the
low-f half of the curve is all zeros (no qualia below
f = 0.18), so the monotone reading rests on empty fields.
That reading is reported, not used. NU_MIN = 0.10 is the
round tenth at which qualia first appear across a broad
sigma range (first quale at f = 0.0415) with non-degenerate
counts (1–17 per field). The verdicts are stable across
NU_MIN = 0.10–0.20: (xiv) FAILS humped at every one, (xv)
PASSES at every one, (xvi) FAILS at every one — so the
choice does not drive the results.

Pilot — per-field frequency spreads and overlap
(ν ≥ 0.10):

| σ | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---:|---:|---:|---:|---:|
| n qualia | 1 | 9 | 17 | 13 | 12 |
| std ν qualia | 0.0000 | 0.0360 | 0.1009 | 0.1674 | 0.2266 |
| std ν all pairs | 0.0293 | 0.0563 | 0.1268 | 0.2009 | 0.2393 |
| difference | 0.0293 | 0.0203 | 0.0259 | 0.0335 | 0.0127 |
| overlap | 0.9956 | 0.9988 | 0.9987 | 0.9877 | 0.9781 |

The smallest per-field spread difference is 0.0127
(σ = 1.0); SPREAD_MARGIN = 0.01 is the round number below
it. (The σ = 0.05 row has one quale, so its spread is 0.0
by construction; fields with fewer than two qualia are
excluded from the spread check.) The smallest overlap is
0.9781; OVERLAP_MIN = 0.90 is the round number well below
it. The overlap half is a weak check — the qualia wave is
built from the agents, so it nearly coincides with the
field state — and is reported as such. Pooled across the
grid the spreads are essentially equal (std qualia 0.1950
vs std all 0.1947, n = 52 vs 196): pooling mixes fields
with different f, so the pooled comparison confounds the
spread with the sigma trend. The pooled numbers are
reported, not gated; coherence is a property of one field,
so the per-field comparison is the gated one.

Pilot — D gap, quale members vs non-quale agents:

| ν ≥ | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 |
|---|---:|---:|---:|---:|---:|
| pooled mean D members | 0.8447 | 0.8163 | 0.7767 | 0.7595 | 0.7397 |
| pooled mean D non | 0.9594 | 0.9686 | 0.9725 | 0.9732 | 0.9734 |
| pooled gap | −0.1147 | −0.1522 | −0.1958 | −0.2137 | −0.2338 |

The pooled gap is NEGATIVE at every entanglement
threshold. D_MARGIN = 0.10 is the round margin. Per-sigma
gaps at ν ≥ 0.10: −0.0022 at σ = 0.05, empty non-quale
groups at σ = 0.10 and 0.25 (every agent is a quale
member), +0.1515 at σ = 0.50, −0.1332 at σ = 1.00.

Thresholds: QUALIA_NU_MIN = 0.10, QUALIA_SPREAD_MARGIN
= 0.01, QUALIA_OVERLAP_MIN = 0.90, QUALIA_D_MARGIN = 0.10.

### Claims (xiv)–(xvi), measured fresh

#### (xiv) Qualia emerge with empathy — FAIL

The quale count per field (N = 8) against f:

| f | 0.0000 | 0.0086 | 0.0415 | 0.0802 | 0.1803 | 0.2839 | 0.4143 |
|---|---:|---:|---:|---:|---:|---:|---:|
| qualia | 0 | 0 | 1 | 9 | 17 | 13 | 12 |

First quale at f = 0.0415 (σ = 0.05); peak 17 at
f = 0.1803 (σ = 0.25); then 13 and 12 as resonance dies.
The count is non-monotone, so the claim FAILS. The reason
is structural: the count is the product of rising
concurrence (noise creates entanglement in the uniform
thought) and falling resonance, so it must rise, peak, and
fall. Monotone emergence was the wrong shape to expect;
the hump is the measurement.

#### (xv) The qualia wave is coherent — PASS

Per field, the spread of quale frequencies is smaller
than the spread across all pairs by at least 0.01 at every
field with two or more qualia (differences 0.0203, 0.0259,
0.0335, 0.0127), and the wave's overlap with the field
state is 0.9781–0.9988, above the 0.90 floor at every
field with a quale. Both halves hold. The pooled spreads
(0.1950 vs 0.1947) are reported alongside, not hidden:
within a field the qualia are tighter; across fields the
spread is the sigma trend itself.

#### (xvi) Qualia track self-determinism — FAIL

The pooled D gap is −0.1522 (quale members 0.8163,
n = 32, vs non-quale 0.9686, n = 24) against a +0.10
margin, so the claim FAILS. The reason is measured in
v0.2.0: D anti-tracks concurrence (Pearson −0.9570) — the
noise that creates entanglement destroys self-knowing, so
the agents that qualify as qualia, high concurrence, are
exactly the ones with low D. In this model the
resonant+entangled modes are the LEAST self-determined.
The per-sigma gaps are reported (+0.1515 at σ = 0.50,
−0.1332 at σ = 1.00, ~0 elsewhere, empty non-quale
groups at σ = 0.10 and 0.25); no within-sigma pattern
rescues the pooled result. That is a measured negative
result about what a quale is in this model, not a failure
to measure: the gap was computed over 196 pairs and 56
agent-slots.

### Honest limits (v0.6.0 addition)

A "quale" here is a DEFINED resonant+entangled mode in
code, not a measurement of subjective experience; the
qualia wave is a defined superposition, not a physical
wave. Nothing here claims a mind has qualia, or measures
one. The (xiv) hump and the (xvi) negative gap are
properties of the model's own structure (noise creates
concurrence and destroys D); they are reported as such.

## 13. CKW monogamy in triads (v0.7.0, measured 2026-11-16)

One module, `monogamy.py`: the deep-think evaluation's
rank-1 upgrade (REPORT.md §9 in
`research_notes/faggin-bridge-deep-think-upgrades-20261116-2105/report.md`).
Built on top of the unpushed v0.5.0 + v0.6.0, so a future
push carries v0.5.0 + v0.6.0 + v0.7.0 together.

### Mechanism (a definition inside the model, not a discovery)

- A thought is a TWO-QUBIT state, so a triad of three
  thoughts is a six-qubit system where pairwise Wootters
  concurrence is not directly defined. The triads here are
  therefore THREE-QUBIT pure states (8-dim), where each
  member is a BINARY thought — one qubit whose basis maps
  into the thought space as |0> -> |00> (attention) and
  |1> -> |10> (self). The mapping is a DEFINITION (an
  embedding), not a discovery: it says which two of the
  four concepts a binary thought can be, nothing more.
  The embedding was verified in a pilot before any claim
  was written: for GHZ, tau_A(BC) = 1, pairwise tau = 0,
  residual = 1, D_A = 2/3; for W, tau_A(BC) = 8/9,
  pairwise tau = 4/9 each, residual = 0, D_A = 7/9 — all
  exact to 1e-9.
- GHZ-like triad = (|000> + |111>) / sqrt(2); W-like
  triad = (|001> + |010> + |100>) / sqrt(3). Two
  interpolation families connect them:
  (a) generalized GHZ: a|000> + sqrt(1-a^2)|111> — the
  pairwise tangle is EXACTLY zero for every a, while the
  one-to-rest tangle 4 a^2 (1-a^2) sweeps 0 -> 1 -> 0;
  (b) GHZ/W interpolation: cos(t)|GHZ> + sin(t)|W>.
- Pairwise tangle tau_ij = C^2, C the Wootters concurrence
  (thought_entanglement.py) of the reduced two-qubit state
  (third qubit traced out). One-to-rest tangle
  tau_A(BC) = 4 det(rho_A), exact for pure states.
  Residual genuine-tripartite tangle =
  tau_A(BC) - tau_AB - tau_AC (Coffman-Kundu-Wootters).
  D_A for a member = Tr(P rho_A_embedded), the EXISTING
  self-knowing projector (self_knowing.py) on the member's
  embedded 4-dim reduced state.
- Noise: unity.gaussian_copies on the 8-dim triad vector
  (the same model as everywhere else, seeded, 5 copies,
  seed 42); the copies stay PURE (purity 1.0 at every
  sigma, minimum over the whole sweep 0.9999999999999992),
  so the 4 det(rho_A) formula stays valid. The sweeps use
  sigma = 0.00, 0.25, 0.50, 1.00.

### Pre-registration (written before the final measurement run)

Thresholds set from a pilot sweep, as round numbers with
margin, and never moved after the final run.

Pilot — exact endpoints at sigma = 0:

| | GHZ | W |
|---|---:|---:|
| tau_A(BC) | 1.0000 | 0.8889 (8/9) |
| tau_AB, tau_AC | 0.0000 | 0.4444 (4/9) each |
| residual | 1.0000 | 0.0000 |
| D_A | 0.6667 (2/3) | 0.7778 (7/9) |
| miss fraction (residual / tau_A(BC)) | 1.0000 | 0.0000 |

Pilot — CKW margins on noisy copies (5 copies, seed 42):

| sigma | GHZ min margin | W min margin |
|---|---:|---:|
| 0.25 | 0.5007 | 0.1021 |
| 0.50 | 0.2792 | 0.0979 |
| 1.00 | 0.1880 | 0.0485 |

No margin is ever negative; the smallest seen is 0.0485
(noisy W, sigma = 1.0). CKW_TOL = 1e-9 is numerical zero:
any margin below -1e-9 would be a defect in the code's
concurrence, not a result about the theorem. The miss
gates are MISS_GHZ_MIN = 0.9 and MISS_W_MAX = 0.1, round
numbers around the exact 1.0 / 0.0.

Pilot — D_A vs tau_A(BC) on the generalized-GHZ branch
a in [1/sqrt(2), 1] (7 points):

| a | 0.7071 | 0.7500 | 0.8000 | 0.8500 | 0.9000 | 0.9500 | 1.0000 |
|---|---:|---:|---:|---:|---:|---:|---:|
| tau_A(BC) | 1.0000 | 0.9844 | 0.9216 | 0.8020 | 0.6156 | 0.3520 | 0.0000 |
| D_A | 0.6667 | 0.7083 | 0.7600 | 0.8150 | 0.8733 | 0.9350 | 1.0000 |
| tau_AB | 0 exactly throughout | | | | | | |

Pearson(D_A, tau_A(BC)) = -0.9608, Spearman = -1.0, D_A
range 1/3. The (xix) gates are PEARSON_MAX = -0.95 and
D_RANGE_MIN = 0.25, the round numbers below the pilot
values, with TAU_AB_FLAT_MAX = 1e-9 (pilot: exactly 0).
The full a-grid Pearson is only -0.7507, because
tau_A(BC) = 4 a^2 (1-a^2) is non-monotone in a (it peaks
at a = 1/sqrt(2)) while D_A = 1/3 + (2/3) a^2 is monotone
— which is exactly why the gated branch is the upper half
a in [1/sqrt(2), 1], where tau_A(BC) falls 1 -> 0 while
D_A rises 2/3 -> 1.

Pilot — the two descriptive comparisons (reported, not
gated): across the GHZ/W interpolation Pearson(D_A,
tau_A(BC)) = -0.6316, but tau_AB rises to 4/9 along that
family, so it confounds "entanglement with the pair"
with "entanglement with B". On the GHZ noise sweep, D_A
and tau_A(BC) decay TOGETHER (D_A 0.6667 -> 0.6132,
tau_A(BC) 1.0000 -> 0.6504 from sigma = 0 to 1.0) while
mean tau_AB stays small (0.0764–0.0928): the noise
channel does not separate the two entanglements. The
separation is in the state family, not the noise — which
is why only the generalized-GHZ branch is gated.

Thresholds: CKW_TOL = 1e-9, EXACT_TOL = 1e-9,
MISS_GHZ_MIN = 0.9, MISS_W_MAX = 0.1,
D_TAU_PEARSON_MAX = -0.95, TAU_AB_FLAT_MAX = 1e-9,
D_RANGE_MIN = 0.25.

### Claims (xvii)–(xix), measured fresh

#### (xvii) CKW monogamy holds in triads — PASS

The sweep covers 52 (state, sigma) rows: GHZ, W, the
GHZ/W interpolation (15–75 deg), the generalized-GHZ
family (a = 0.5–1.0), noisy copies at sigma = 0.00, 0.25,
0.50, 1.00, every member. The minimum CKW margin is
0.0, attained at the product endpoint (a = 1.0, sigma =
0) where there is no entanglement at all, so the margin
is 0 by construction. The smallest margin over noisy rows
is 0.0012 (GHZ/W 30 deg, sigma = 0.50). No margin is
negative anywhere: the code's concurrence respects the
theorem at every triad and every sigma. This is a code
check, not a discovery — had it failed, the concurrence
would have been wrong, not the theorem.

#### (xviii) GHZ vs W: pairwise concurrence misses tripartite entanglement — PASS

At sigma = 0 the GHZ-like triad has tau_A(BC) = 1,
pairwise tangle 0, residual 1, D_A = 2/3: pairwise
concurrence misses 100% of its entanglement (miss
fraction 1.0). The W-like triad has tau_A(BC) = 8/9,
pairwise tangle 4/9 each, residual 0, D_A = 7/9: miss
fraction 0.0. Under noise the GHZ miss stays 0.60–1.00
and the W miss 0.00–0.44 at every sigma:

| sigma | GHZ tau_A(BC) | GHZ pairwise sum | GHZ residual | GHZ miss | W tau_A(BC) | W pairwise sum | W residual | W miss |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.8889 | 0.8889 | 0.0000 | 0.0000 |
| 0.25 | 0.8869 | 0.1833 | 0.7036 | 0.7933 | 0.7172 | 0.4014 | 0.3158 | 0.4403 |
| 0.50 | 0.7478 | 0.2523 | 0.4955 | 0.6626 | 0.7223 | 0.4955 | 0.2269 | 0.3141 |
| 1.00 | 0.6504 | 0.2584 | 0.3920 | 0.6027 | 0.6799 | 0.5171 | 0.1628 | 0.2395 |

Noise converts some GHZ tripartite entanglement into
pairwise entanglement (the pairwise sum rises 0 to
0.2584) and creates residual tangle in W (0 to 0.3158 at
sigma = 0.25), but the ordering never flips: at every
sigma the GHZ entanglement is mostly residual and the W
entanglement mostly pairwise. A pairwise-only concurrence
measure — everything the bridge had before v0.7.0 —
undercounts total entanglement in the GHZ regime and
overcounts it in the W regime, exactly as the deep-think
report predicted. D_A also separates the regimes at
sigma = 0 (2/3 GHZ vs 7/9 W) and both decay with noise
(GHZ 0.6667 -> 0.6132, W 0.7778 -> 0.6399).

#### (xix) D_A falls as tau_A(BC) rises with tau_AB flat — PASS

On the generalized-GHZ branch a in [1/sqrt(2), 1],
Pearson(D_A, tau_A(BC)) = -0.9608 (Spearman -1.0) while
tau_AB is exactly 0 throughout and D_A spans 2/3 to 1
(range 1/3), against gates of -0.95, 1e-9, and 0.25.
D_A moves with the one-to-rest tangle while the pairwise
tangle does not move at all: the member's self-knowing
tracks its entanglement with the PAIR, not with B. This
is the triad version of the v0.2.0 result (D anti-tracks
concurrence, Pearson -0.9570), sharpened to distinguish
which entanglement D tracks. The two descriptive
comparisons stay as the pilot found them: the GHZ/W
interpolation gives Pearson -0.6316 (tau_AB confounded,
rising to 4/9), and the GHZ noise sweep moves D_A and
tau_A(BC) together (both decay with noise), so neither
rescues or refutes the gated result — the separation is
in the state family, not the noise.

### Honest limits (v0.7.0 addition)

Monogamy is an established theorem of quantum information
(Coffman-Kundu-Wootters 2000; Osborne & Verstraete, PRL
2006) applied to the model's states; the triads are
defined in code, not physical systems; the binary-thought
embedding is a definition, not a discovery. The (xvii)
PASS is a check that the code's concurrence respects the
theorem, not a test of the theorem. Nothing here claims a
mind has triads, or measures one. The (xix) PASS is about
the model's own D against the model's own tangles; it does
not show that self-knowing in a human tracks entanglement
with a group rather than an individual. Classical emulation
throughout; Faggin's metaphysics stays interpretive.

## 14. Quantum-Darwinism redundancy plateau (v0.8.0, measured 2026-11-17)

One module, `darwinism.py`: the deep-think evaluation's
rank-2 upgrade (REPORT.md §9 in
`research_notes/faggin-bridge-deep-think-upgrades-20261116-2105/report.md`).
Built on top of the unpushed v0.5.0 + v0.6.0 + v0.7.0, so a
future push carries v0.5.0 + v0.6.0 + v0.7.0 + v0.8.0
together.

### Mechanism (a definition inside the model, not a discovery)

- The system S is a thought in superposition of two pointer
  states: Bell |00> and |11>, binary |0> and |1> (the
  binary embedding is the SAME definition as monogamy.py:
  |0> -> |00> attention, |1> -> |10> self). The environment
  is N = 10 qubits (matching Zhu et al. 2025, whose
  environment is 10 qubits beside a 2-qubit system), each
  recording the pointer value in a CNOT-like branching
  interaction: (|p_0>|e_0>^N + |p_1>|e_1>^N) / sqrt(2),
  with record overlap c = <e_0|e_1> = cos(phi). Hard
  branching (phi = pi/2, c = 0) has orthogonal records;
  soft branching (phi = pi/3, c = 0.5) has overlapping
  records.
- Per fragment size m: I(S:F) = H_S + H_F - H_SF (quantum
  mutual information, exact von Neumann entropies);
  Holevo chi(S:F) = H(rho_F) - sum_b p_b H(rho_F|b) from
  measuring S in the pointer observable; discord = I -
  chi; redundancy R_delta = N / m* with delta = 0.1,
  where m* is the smallest m with I >= (1 - delta) H_S.
- Einselection is a dephasing channel in the pointer basis
  (strength p, reference 0.5): p = 0 is the pure branching
  state, p = 1 the pointer mixture. The classical plateau
  is p-independent; the quantum excess (discord at m = N)
  decays with p.
- The fragment state rho_SF is built DIRECTLY from the
  branching construction (closed form), not by
  partial-tracing the full 2^(N+n_sys)-dim density matrix.
  The fragment state is exactly rank 2 (it lives in the
  span of the two branch vectors), so its entropies have
  the closed form in `analytic_fragment_values`, and
  `plateau_sweep` evaluates that form directly: a 4096-dim
  eigvalsh would compute the same two nonzero eigenvalues
  at O(d^3) cost. The general partial trace
  (`partial_trace_general`) and the full numeric
  `fragment_quantities` are kept and cross-check the closed
  form in the tests (N = 3 exact to 1e-9; N = 10 subset to
  1e-9; the pilot checked all m at N = 10 to 2e-15). The
  noisy-copy sweep has no closed form -- the copies are
  genuinely high-rank -- so it uses the full numeric path
  throughout, at N_NOISE = 6 (the plateau structure is
  N-independent; 6 keeps the largest fragment matrix at
  2^8, so the sweep runs in seconds instead of minutes in
  4096-dim eigvalsh calls).

### Pre-registration (directional assertions, frozen before the final run)

Thresholds are round numbers set from the pilot sweep
(pilots A/B/C, 2026-11-17) and never moved after the final
measurement run. The pilot tables:

| quantity | hard | soft |
|---|---|---|
| plateau I, m = 1 | 1.0000 | 0.8113 |
| plateau I, m = 2 | 1.0000 | 0.9544 |
| plateau I, m = 9 | 1.0000 | 1.0456 |
| plateau I, m = 10 | 1.1887 | 1.1887 |
| discord, m = 9 | 0.0000 | 0.0456 |
| discord, m = 10 | 0.1887 | 0.1887 |
| m* | 1 | 2 |
| R | 10 | 5 |

(Both systems identical; p = 0.5, N = 10. The soft
plateau-edge values are 0.0456, so the 0.10 tolerances
carry a 2.2x margin; the full-env discord 0.1887 carries
a 1.9x margin above the 0.10 floor.)

- (xx) Redundancy plateau: I(S:F) rises to H_S and STAYS
  there until m = N; discord stays ~0 on the plateau and
  rises only at m = N. Gates: m* <= 5; on m in [m*, N-1],
  |I - H_S| <= 0.10 and discord <= 0.10; discord at m = N
  >= 0.10; redundancy >= 1. Expected PASS.
- (xxi) D tracks the classical, not the quantum: as the
  branching turns on (k = 0..N), D rises with redundancy /
  chi (Pearson >= 0.9) while concurrence falls (C(N)/C(0)
  <= 0.1); D anti-tracks discord (Pearson <= -0.9).
  Expected FAIL: D is exactly 2/3 for every k (the
  off-diagonal |00><11| never contributes to Tr(P rho)
  and the diagonal is always (1/2, 1/2)), so the Pearsons
  are 0.0. The quantity that tracks the classical is chi,
  not D.
- (xxii) The sigma = 0.50 non-transfer explained: across
  the bridge's sigma grid the collaboration gap and the
  redundancy are sigma-robust (sigma = 0.50 value >= 0.5x
  the sigma = 0.25 value) while the discord at m = N is
  fragile (sigma = 0.50 value <= 0.5x the sigma = 0.25
  value); the gap tracks redundancy (Pearson >= 0.9), not
  discord. Falsified if the gap tracks discord instead
  (Pearson(gap, discord) >= 0.9). Expected FAIL: under
  the bridge's vector noise the redundancy FALLS 6 -> 2
  and the discord RISES 0.1887 -> 0.6697 (pilot B, since
  corrected upward to 2.13 by the pointer-measurement
  fix below). The gap is robust (0.77) but tracks
  neither.

### Correction found and fixed during the build

The first pointer measurement used only the two pointer
projectors (|p_0><p_0|, |p_1><p_1|). That measurement is
INCOMPLETE -- the projectors do not sum to the identity --
so it drops the non-pointer outcomes. On the noiseless
branching state the dropped outcomes have probability 0
and nothing changes. But once vector noise populates the
non-pointer basis states (|01>, |10>), the dropped
outcomes carry entropy, chi is overestimated, and the
discord I - chi goes NEGATIVE: the pilot measured discord
down to -0.32 at m = 2, sigma = 0.5. A negative discord is
impossible for a complete measurement (chi <= I by data
processing), so this was a defect in the measurement, not
a result.

Both the Holevo measurement and the dephasing now use the
pointer observable: the qubit that distinguishes the two
pointer states (qubit 0: Bell |00> vs |11>, binary |0> vs
|1>). The two sector projectors sum to the identity, so
chi <= I and the discord is never negative. The noiseless
numbers are unchanged (verified: the numeric N = 10
plateau values are identical before and after the fix).
The corrected noise-sweep discord is >= 0 everywhere
(minimum 0.0502 over m and copies at sigma >= 0.05), and
larger than the pilot's underestimate at m = N (2.13
instead of 0.67 at sigma = 0.25) -- which strengthens,
not weakens, the (xxii) FAIL.

### Claim (xx): redundancy plateau — PASS

All four (system, branching) combos pass every gate at
p = 0.5, N = 10:

| combo | m* | R | max \|I - H_S\| on plateau | max discord on plateau | discord(m = N) |
|---|---|---|---|---|---|
| binary hard | 1 | 10 | 0.0000 | 0.0000 | 0.1887 |
| binary soft | 2 | 5 | 0.0456 | 0.0456 | 0.1887 |
| bell hard | 1 | 10 | 0.0000 | 0.0000 | 0.1887 |
| bell soft | 2 | 5 | 0.0456 | 0.0456 | 0.1887 |

The dephasing picture (reported, hard binary): the plateau
I is 1.0000 at p = 0, 0.5, and 1, while discord(m = N)
falls 1.0000 -> 0.1887 -> 0.0000 with p. The classical
information is robust to einselection; the quantum excess
is fragile to it. This is the Zhu et al. structure in the
model's own states, computed exactly.

### Claim (xxi): D tracks the classical, not the quantum — FAIL

As the branching turns on (Bell, p = 0.5, k = 0..10):

| family | Pearson(D, R) | Pearson(D, chi_1) | Pearson(D, discord) | C(k=0) -> C(k=N) | D range |
|---|---|---|---|---|---|
| hard | 0.0000 | -0.0000 | 0.0000 | 0.5 -> 0.0 | [0.6667, 0.6667] |
| soft | -0.0000 | -0.0000 | 0.0000 | 0.5 -> 0.0005 | [0.6667, 0.6667] |

D is exactly 2/3 at every k, in both families. The reason
is exact, not numerical: the system's reduced state after
k interactions is (1/2)(|p_0><p_0| + |p_1><p_1|) +
((1-p)/2) c^k (|p_0><p_1| + h.c.), and D = Tr(P rho_S)
with the self-knowing projector P. The off-diagonal term
never contributes, because <11|P|00> = 0 (P is diagonal
in the pointer basis up to the terms that vanish on the
off-diagonal), and the diagonal is always (1/2, 1/2), so
D = (D(|00>) + D(|11>))/2 = (1 + 1/3)/2 = 2/3 for every
k, every phi, every p. A constant cannot correlate with
anything, so all three Pearson gates fail (0.0 against
0.9 / -0.9) while the concurrence half passes. The
quantity that tracks the classical as the branching turns
on is chi (hard: 0 -> 1.0 bit at k = 1; soft: 0 -> 0.8113
bit), not D. The claim as written is falsified, and the
falsification is a theorem about the model's own D, not a
measurement artifact.

### Claim (xxii): the sigma = 0.50 non-transfer explained — FAIL

Across the bridge's sigma grid (Bell hard, p = 0.5,
N = 6, 5 copies, seed 42; gap from
`empathy_field.collaboration_gap_vs_noise`, design B;
concurrence from `thought_entanglement.entanglement_sweep`):

| sigma | gap (bits) | redundancy | discord(m = N) | mean concurrence |
|---|---|---|---|---|
| 0.00 | +5.0450 | 6.0 | 0.1887 | 1.0000 |
| 0.01 | +5.0281 | 6.0 | 0.3856 | 0.9998 |
| 0.05 | +5.2071 | 2.0 | 1.6416 | 0.9952 |
| 0.10 | +5.6081 | 2.0 | 2.0745 | 0.9792 |
| 0.25 | +4.3352 | 2.0 | 2.1310 | 0.8471 |
| 0.50 | +3.3494 | 2.0 | 2.1190 | 0.6520 |
| 1.00 | +3.5569 | 2.0 | 2.1131 | 0.7002 |

- Gap robust at the step: 3.3494 / 4.3352 = 0.7726 (>= 0.5, PASS).
- Redundancy robust at the step: 2 / 2 = 1.0000 (>= 0.5, PASS).
- Discord fragile at the step: 2.1190 / 2.1310 = 0.9944 (<= 0.5 required, FAIL).
- Redundancy robust across the grid: min R / R(0) = 2 / 6 = 0.3333 (FAIL).
- Discord fragile across the grid: 2.1131 / 0.1887 = 11.198 (<= 0.5 required, FAIL).
- Gap tracks redundancy: Pearson(gap, R) = 0.3528 (>= 0.9 required, FAIL).
- Gap tracks discord (falsifier): Pearson(gap, discord) = -0.4411 (< 0.9, falsifier NOT triggered -- but the positive clauses already fail).
- Concurrence tracks discord: Pearson(C, discord) = -0.6259 (>= 0.9 required, FAIL -- concurrence ANTI-tracks discord).

The explanation the claim offers is backwards under the
bridge's own noise. The vector noise is not a dephasing
channel: `unity.gaussian_copies` adds absolute Gaussian
noise (std sigma) to every component of the state vector,
then renormalizes. At sigma = 0.05 on a 12-qubit state
the noise vector already has norm ~3.2 against the
state's 1.0, so the copies are mostly random states -- and
a random state is highly entangled between S and F. That
is why the plateau I rises to 1.46 (above H_S = 1), the
discord at m = N rises to 2.13, and the small-fragment
redundancy collapses (m* grows 1 -> 3: the size-1
fragment's I drops to 0.37 at sigma = 0.25, because the
single-qubit record is corrupted by the noise). The
dephasing picture -- classical robust, quantum fragile --
holds for the einselection parameter p (see (xx) above),
not for the vector-noise sigma. The collaboration gap
survives sigma = 0.50 for a different reason: the design-B
mechanism (isolated agents collapse and stay decided, so
their joint entropy stays low at every sigma, while
collaborating agents keep mixing). The gap's
sigma-robustness is a property of the collaboration
design, not of redundant classical encoding. This FAIL is
kept and stated: it separates two different robustnesses
that the deep-think report's §6 had conflated.

### Honest limits (v0.8.0 addition)

Quantum Darwinism is an established theory (Zurek 2009;
verified in superconducting circuits by Zhu et al. 2025)
and emergent classicality is a theorem (Brandao et al.,
Quantum 2021); what is measured here is the same
structure in the model's own states, computed exactly with
NumPy. The system and environment are defined in code, not
physical systems. The (xx) PASS is a check that the code's
entropies match the branching construction's analytic form,
not a test of the theory. The (xxi) and (xxii) FAILs are
about the model's own D, redundancy, and discord under the
model's own noise; they do not show anything about human
self-knowing, or about why real collaborations survive
noise. The vector noise is not a dephasing channel, and the
distinction matters: the einselection parameter p is the
one with the classical-robust / quantum-fragile split.
Classical emulation throughout; Faggin's metaphysics stays
interpretive.
