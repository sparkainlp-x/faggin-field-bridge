# Faggin Field Bridge — Report

**Version:** 0.22.0 (2026-11-18)
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

**418 tests, 418 passed** (`python3 -m pytest tests/ -q`, 67.16 s).

*Correction in v0.18.0: this section said 397. The collected counts below are the
record (28 files: 12 + 9 + 14 + 27 + 22 + 9 + 19 + 17 + 21 + 10 + 20 + 18 + 25 +
22 + 23 + 11 + 21 + 18 + 17 + 3 + 5 + 7 + 12 + 7 + 9 + 9 + 22 + 9 = 418).*
(v0.17.0 counts: 397 + 21 new = 418.)

*Correction in v0.17.0: this section said 375. The collected counts below are the
record (27 files: 12 + 9 + 14 + 27 + 22 + 9 + 19 + 17 + 10 + 20 + 18 + 25 +
22 + 23 + 11 + 21 + 18 + 17 + 3 + 5 + 7 + 12 + 7 + 9 + 9 + 22 + 9 = 397).*
(v0.16.0 counts: 375 + 22 new = 397.)

*Correction in v0.16.0: this section said 353. The collected counts below are the
record (26 files: 12 + 9 + 14 + 27 + 9 + 19 + 17 + 10 + 20 + 18 + 25 +
22 + 23 + 11 + 21 + 18 + 17 + 3 + 5 + 7 + 12 + 7 + 9 + 9 + 9 + 22 = 375).*
(v0.15.0 counts: 353 + 22 new = 375.)

*Correction in v0.14.0: this section said 315. The collected counts below are the
record (24 files: 12 + 9 + 14 + 9 + 19 + 17 + 10 + 20 + 18 + 25 +
22 + 23 + 11 + 21 + 18 + 17 + 3 + 5 + 7 + 12 + 7 + 9 + 9 + 9 = 326).*
(v0.13.0 counts: 315 + 11 new = 326.)

*Correction in v0.13.0: this section said 305. The collected counts below are the
record (23 files: 12 + 9 + 14 + 9 + 19 + 17 + 10 + 20 + 18 + 25 +
22 + 23 + 21 + 18 + 17 + 3 + 5 + 7 + 12 + 7 + 9 + 9 + 9 = 315).*
(v0.12.1 counts: 305 + 10 new = 315.)

*Correction in v0.12.1: this section said 301. The collected counts below are the
record (22 files: 12 + 9 + 14 + 9 + 19 + 17 + 20 + 18 + 25 +
22 + 23 + 21 + 18 + 17 + 3 + 5 + 7 + 12 + 7 + 9 + 9 + 9 = 305).*
(v0.12.0 counts: 301 + 4 new = 305.)

*Correction in v0.12.0: this section said 282 with no
test_observer_cycle.py entry. The collected counts below are the
record (22 files: 12 + 9 + 14 + 9 + 19 + 17 + 20 + 18 + 25 +
22 + 21 + 18 + 17 + 3 + 5 + 7 + 12 + 7 + 9 + 9 + 9 + 19 = 301).*
(v0.11.0 counts: 262 + 20 new = 282; v0.12.0 counts:
282 + 19 new = 301.)

*Correction in v0.11.0: this section said 244 with no
test_darwinism.py, test_malus.py, test_product_model.py or
test_landauer.py entry. The collected counts below are the
record (21 files: 12 + 9 + 14 + 9 + 19 + 17 + 20 + 18 + 25 +
22 + 21 + 18 + 17 + 3 + 5 + 7 + 12 + 7 + 9 + 9 + 9 = 282).*
(v0.10.0 counts: 244 + 18 new = 262; v0.11.0 counts:
262 + 20 new = 282.)

*Correction in v0.9.0: this section said 226 with no
test_malus.py entry. The collected counts below are the
record (19 files: 12 + 9 + 14 + 9 + 19 + 17 + 18 + 25 + 22 +
21 + 17 + 3 + 5 + 7 + 12 + 7 + 9 + 9 + 9 = 244).* (v0.8.0 counts:
226 + 18 new = 244.)

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
- `test_darwinism.py` (19): plateau |I - H_S| <= 0.0456 and
  discord <= 0.0456 (hard: exactly 0), discord at m = N
  0.1887, redundancy hard 10 / soft 5, plateau p-independent
  while discord(m = N) falls 1.0 -> 0.1887 -> 0.0 with p,
  claim (xx) verdict PASS, claim (xxi) verdict FAIL (D is
  2/3 for every branching turn-on step, Pearson 0.0),
  claim (xxii) verdict FAIL (redundancy 6 -> 2, discord
  0.19 -> 2.13 bits, gap robust at 0.77), the three-claim
  aggregate (1/3 pass, no headline), thresholds set, input
  validation, and main() running.
- `test_malus.py` (18): crossed polarizers transmit exactly
  0, triple (0, 45, 90) transmits 0.125 = I0/8 (1/4 for
  input polarized at 0 degrees), T(phi) = (1/8) sin^2(2 phi)
  on the whole grid peaking at 45 degrees, the middle
  step's output state is exactly |45 degrees>, the total
  recomputed from the recorded intermediate states is 1/8,
  the bypass control is 0, the cascade contrast (stage-2
  visibility 0 vs reopened 1/8), the N-polarizer chain
  rising toward 1/2, claims (xxiii)-(xxv) all PASS, the
  three-claim aggregate (3/3 pass, no headline), and
  main() running.
- `test_product_model.py` (18): marginals at sigma = 0
  (p_res = 1, p_ent = 0, product 0), sigma = 0.25 (product
  17.0, measured 17), sigma = 0.5 (product 12.75, measured
  13), sigma = 0.1 (product 9.0, measured 9), the fine
  grid all interior (12 rows) with relative error None
  when predicted is 0, claim (xxvi) verdict PASS (mean
  0.0289, max 0.0667; standard grid 0.0119 / 0.0400
  reported), the seed spread (seeds 1, 3 pass; seed 2
  fails at mean 0.1666, max 0.3636), baseline peak f =
  0.1803, claim (xxvii) verdict PASS (predicted and
  measured peaks 0.4143 and 0.2839), no shift at the
  baseline thresholds, the predicted peak from the
  marginals alone, claim (xxviii) verdict PASS (single
  conditions monotone, both humped; exact counts
  28/0/0 through 14/25/12), input validation, the
  three-claim aggregate (3/3 pass, no headline), and the
  frozen thresholds (0.10 / 0.20 / 0.25 / 0.25).
- `test_landauer.py` (20): per-bit cost 2.871e-21 J exact
  at 300 K, linear scaling and input validation, the
  ledger at sigma = 0 (16.00 decision bits, 0 qualia, 28
  classification bits, 44.00 total, 1.263e-19 J) and at
  sigma = 0.25 (13.46 decision bits, 17 qualia, 58.46
  total, 1.678e-19 J), cumulative 345.97 bits / 9.932e-19
  J, the Planck standardized values (mean x = 3.8322,
  mode x = 2.8210, ratio 0.7361), the KS statistic on a
  degenerate sample (~1.0) and on Planck quantiles
  (< 0.05), the KS critical values (0.1258 at n = 168,
  0.3081 at n = 28), claim (xxix) verdict PASS (peak
  58.46 bits at sigma = 0.25), claim (xxx) verdict FAIL
  (0.8996 < 0.9430 pooled; sigma wins within every seed),
  claim (xxxi) verdict PASS (pooled D = 0.1465 > 0.1258;
  mode/mean deviations 0.46, 0.56, 0.35), sigma = 0
  carrying no distribution, per-field KS below critical
  (max 0.2159, reported not gated), pooled n = 168, and
  the three-claim aggregate (2/3 pass, no headline).
- `test_observer_cycle.py` (19): the stored thought (D = 1,
  C = 0) and the kernel thought (D = 0, C = 1) exact,
  the generalized-Bell endpoints (a = 1: C = 0, D = 1;
  a = 1/sqrt(2): C = 1, D = 2/3), the slide endpoints
  and normalization, the calibration-seed Pearsons
  (-0.9570, -0.9397) and the held-out seed 2026 Pearson
  (-0.8828, above the frozen -0.90 bar; Spearman
  -0.9643 still holds), claim (xxxii) verdict FAIL,
  the Bell-branch rows and correlations (Pearson(R, C)
  = 1.0000, Spearman(R, D) = -1.0000, Pearson(R, D)
  = -0.8801 reported not gated), the noise-axis control
  inverting (Pearson(R, nu_ij) = -0.5528, Pearson(R,
  d_pair) = +0.7694, n = 196 pairs), claim (xxxiii)
  verdict PASS, the slide identities exact to 1e-9
  (C + D = 1, R_s - R_k = cos 2 theta), the split
  flipping at the midpoint, claim (xxxiv) verdict PASS,
  the three-claim aggregate (2/3 pass, no headline),
  and the frozen thresholds.

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
  VERSION             0.11.0
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
  monogamy.py         CKW monogamy in triads (claims (xvii)-(xix))
  darwinism.py        quantum-Darwinism redundancy plateau
                      (claims (xx)-(xxii))
  malus.py            Malus three-polarizer paradox
                      (claims (xxiii)-(xxv))
  product_model.py    product-model fit for the humped quale count
                      (claims (xxvi)-(xxviii))
  landauer.py         Landauer-cost ledger + Planck spectral
                      falsification (claims (xxix)-(xxxi))
  observer_cycle.py   the observer cycle: D, concurrence,
                      and overlap (claims (xxxii)-(xxxiv))
  kuramoto.py         Kuramoto bounded-coherence scan
                      (claims (xxxvi)-(xxxix))
  pid.py              synergy-vs-redundancy PID of the pair
                      collaboration gap (claims (xl)-(xliii))
  cloning_ceiling.py  no-cloning / Holevo ceiling for D
                      (claims (xliv)-(xlviii))
  two_channel_empathy.py  two-channel empathy: concern vs
                      distress (claims (l)-(liii))
  connectome_harmonic.py  connectome-harmonic structure-
                      function coupling (claims (liv)-(lvi))
  tests/              397 tests, 27 files
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

## 15. Malus three-polarizer paradox (v0.9.0, measured 2026-11-17)

One module, `malus.py`: the 8-seed exploration's Malus
item (ranked #2 after the Lyapunov build, which shipped
as membrane-arena-3x3 v0.3.0). Built on top of the pushed
v0.7.0 + v0.8.0 (head 1346aa8c), so a future push carries
v0.9.0 alone.

### Mechanism (a definition inside the model, not a discovery)

- A polarizer at angle theta is the rank-1 projector
  P(theta) = |theta><theta| on a 2D Jones vector
  |theta> = (cos theta, sin theta). The transmission of a
  pure state is <psi|P(theta)|psi> = |<theta|psi>|^2 --
  the same functional form as the bridge's self-knowing
  factor D = <psi|P|psi>, with the projector rotated to
  the polarizer axis. Malus's law is D measured along a
  rotated axis.
- Unpolarized input (intensity I0 = 1) transmits 1/2
  through the first polarizer and outputs that polarizer's
  axis state; each later polarizer transmits cos^2 of the
  relative angle and outputs its own axis state. A pure
  input transmits |<theta|psi>|^2 at each step. The state
  after each polarizer is the projected and renormalized
  state (the cascade's project_state semantics), or None
  when the projection is numerically zero.
- The chain (0, 45, 90) degrees with unpolarized input
  gives (1/2) x cos^2(45) x cos^2(45) = 1/8; with input
  polarized at 0 degrees it gives cos^2(45) x cos^2(45)
  = 1/4. The general middle-angle curve for (0, phi, 90)
  is T(phi) = (1/2) cos^2(phi) sin^2(phi)
  = (1/8) sin^2(2 phi). The evenly stepped N-polarizer
  chain from 0 to 90 degrees transmits
  (1/2) cos^(2(N-1))(step) with step = 90/(N-1) degrees,
  rising with N toward 1/2.

### Pre-registration (directional assertions, frozen before the final run)

Thresholds are the exact tolerances EXACT_TOL = 1e-9:
every gated number is an exact analytic prediction
(I0/8, 1/4, 1/2, cos^2), so the freeze is the analytic
value itself, never moved after the final measurement
run. Directions, written before the run:

- (xxiii) adding the middle polarizer RAISES transmission
  from 0 to 1/8 -- more filtering, more light.
- (xxiv) T rises as the middle angle goes from 0 to 45
  degrees and falls as it goes from 45 to 90 degrees.
- (xxv) the middle step's output state is what the
  second projection acts on; the bypass control (first
  state straight through 90 degrees) is zero, so the
  middle step is necessary.

### Claims (xxiii)–(xxv), measured fresh

#### (xxiii) Crossed polarizers transmit 0; 45-degree middle yields I0/8 — PASS

| Quantity | Measured | Expected |
|---|---:|---:|
| crossed (0, 90), unpolarized | 0.000000 | 0 |
| triple (0, 45, 90), unpolarized | 0.125000 | 1/8 |
| pair (0, 45), unpolarized | 0.250000 | 1/4 |
| 45 -> 90, input \|45> | 0.500000 | 1/2 |
| crossed (0, 90), polarized at 0 deg | 0.000000 | 0 |
| triple (0, 45, 90), polarized at 0 deg | 0.250000 | 1/4 |

All four checks pass within 1e-9. The paradox direction
is measured, not asserted: adding a filter raises the
transmission from 0 to 1/8.

#### (xxiv) Reopening is angle-selective — PASS

| phi (deg) | T(phi) | (1/8) sin^2(2 phi) |
|---:|---:|---:|
| 0 | 0.000000 | 0.000000 |
| 15 | 0.031250 | 0.031250 |
| 30 | 0.093750 | 0.093750 |
| 45 | 0.125000 | 0.125000 |
| 60 | 0.093750 | 0.093750 |
| 75 | 0.031250 | 0.031250 |
| 90 | 0.000000 | 0.000000 |

Hand recomputation of one swept row, per the sweep-wiring
rule: T(30 deg) = (1/2) cos^2(30) sin^2(30)
= (1/2)(3/4)(1/4) = 3/32 = 0.09375, matching the helper
exactly. The fine grid (0.5-degree steps) peaks at 45.0
degrees with T = 0.125; T is monotone non-decreasing on
[0, 45] and non-increasing on [45, 90] on the grid. All
four checks pass within 1e-9.

#### (xxv) The middle step's output state is what the second projection acts on — PASS

- The recorded state after the middle polarizer overlaps
  |45 deg> at 1.000000000000 (gate: >= 1 - 1e-9).
- Step transmissions recomputed from the recorded
  intermediate states alone -- each evaluated on the
  recorded state entering that step, never on the angle
  list -- are 0.5, 0.5, 0.5, multiplying to 0.125000
  (gate: 1/8 within 1e-9).
- Bypass control: the state after the first polarizer
  sent directly through 90 degrees transmits 0.000000,
  so the middle step is necessary.
- Cascade contrast, recomputed live from cascade.py:
  the rotation cascade's visibility at stage 2 is
  0.000000 while the Malus reopened transmission is
  0.125000 > 0.1. The same project-and-renormalize
  operation gives opposite outcomes because a pair
  collapses onto one stored direction (rank 1, cross term
  dies) while a single state rotates into a direction
  with nonzero overlap with the final axis. A projection
  does not create energy: it discards the orthogonal
  component, and the surviving component happens to
  overlap the next axis.

### Descriptive: the stepped N-polarizer chain

| N | T(N) |
|---:|---:|
| 2 | 0.000000 |
| 3 | 0.125000 |
| 4 | 0.210938 |
| 5 | 0.265395 |
| 10 | 0.379574 |
| 200 | 0.493839 |

T(N) = (1/2) cos^(2(N-1))(step) rises monotonically
with N toward the 1/2 limit (N = 200 is within 0.01 of
1/2). Projection applied repeatedly keeps reopening the
channel -- the same mechanism as (xxiii), iterated.
Not gated; the values are exact analytic predictions,
checked in the tests to 1e-12 on the formula.

### Honest limits (v0.9.0 addition)

Malus's law is classical optics, computed exactly; the
polarizers are ideal (no absorption beyond the
projection, no depolarization) and the input is either
unpolarized or a pure Jones vector. The (xxiii)–(xxv)
PASSes check the code's projectors against the analytic
Malus formulas, not the theory. The cascade contrast in
(xxv) is structural: a pair collapses under projection
while a single state rotates -- it does not show that
projection "creates" anything in a physical sense, only
that the surviving component overlaps the next axis.
Classical emulation throughout; Faggin's metaphysics
stays interpretive.

## 16. Product model for the humped quale count (v0.10.0, measured 2026-11-17)

Two modules, `product_model.py` (new) on top of
`qualia.py` / `empathy_field.py`: deep-think upgrade #3.
The hump (0, 0, 1, 9, 17, 13, 12; peak 17 at f = 0.1803)
sits far below the PARTIAL -> ATTUNED flip f* = 0.7278,
and the report's strongest explanation needs no new
theory: the quale count is the product of two monotone
marginals moving in opposite directions, p_ent rising
with f (noise creates concurrence) and p_res falling with
f (noise spreads the copies). Built on top of the
unpushed v0.7.0 + v0.8.0 + v0.9.0 work, so a future push
carries v0.7.0–v0.10.0 together.

### Mechanism (a definition inside the model, not a discovery)

- A quale is a pair with R >= R_MIN (0.5) AND nu >=
  NU_MIN (0.10). p_res and p_ent are the fractions of
  pairs above each threshold on their own, measured on
  the SAME field as the count. The product N_pairs *
  p_res * p_ent predicts the AND-count only if the two
  binary indicators are independent across pairs; any
  deviation measures their association -- the interaction
  the product would miss.
- On the standard 7-point sigma grid the fit is partly
  degenerate: p_res = 1.0 exactly below sigma = 0.5, so
  the product there is just the entanglement count. The
  gated fit therefore runs on a fine grid (sigma 0.30,
  0.35, 0.40, 0.45, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00,
  1.25, 1.50) where BOTH marginals are interior on every
  row. The standard-grid fit is reported, not gated.
- Peak shift: change one threshold and the product model,
  computed from the marginals at the NEW threshold
  BEFORE looking at the measured counts there, predicts
  the new peak f_peak. The two shifted settings are
  NU_MIN 0.10 -> 0.25 (R_MIN held at 0.5) and R_MIN 0.5
  -> 0.25 (NU_MIN held at 0.10).
- Hump vanish: drop either condition with a vacuous
  second threshold (nu_min = 0 counts every pair as
  entangled; r_min = 0 counts every pair as resonant)
  and the count must be monotone in f.

### Pre-registration (directional assertions, frozen before the final run)

Thresholds, frozen from the pilot sweeps and never moved
after the final measurement run: PRODUCT_FIT_MEAN_MAX =
0.10, PRODUCT_FIT_ROW_MAX = 0.20 (pilot mean 0.0289, max
0.0667 -- round numbers well above the pilot, not tuned
to its edge). Directions, written before the run:

- (xxvi) the product predicts the measured counts: mean
  relative error at most 0.10, max row error at most
  0.20, on the fine grid at seed 42.
- (xxvii) the peak moves as the product predicts:
  loosening resonance (R_MIN 0.5 -> 0.25) or tightening
  entanglement (NU_MIN 0.10 -> 0.25) both push the peak
  to HIGHER f, and the predicted peak f equals the
  measured peak f at each shifted setting.
- (xxviii) the hump vanishes when either condition is
  dropped: resonance-only falls, entanglement-only
  rises, both-condition humps.

### Claims (xxvi)–(xxviii), measured fresh

#### (xxvi) The product model fits the humped quale count — PASS

| sigma | f | p_res | p_ent | predicted | measured | rel err |
|---:|---:|---:|---:|---:|---:|---:|
| 0.30 | 0.2075 | 0.964 | 0.643 | 17.36 | 17 | 0.0206 |
| 0.35 | 0.2305 | 0.857 | 0.750 | 18.00 | 18 | 0.0000 |
| 0.40 | 0.2509 | 0.679 | 0.750 | 14.25 | 15 | 0.0526 |
| 0.45 | 0.2689 | 0.643 | 0.750 | 13.50 | 14 | 0.0370 |
| 0.50 | 0.2839 | 0.607 | 0.750 | 12.75 | 13 | 0.0196 |
| 0.60 | 0.3123 | 0.571 | 0.821 | 13.14 | 13 | 0.0109 |
| 0.70 | 0.3414 | 0.536 | 0.857 | 12.86 | 12 | 0.0667 |
| 0.80 | 0.3681 | 0.536 | 0.857 | 12.86 | 12 | 0.0667 |
| 0.90 | 0.3928 | 0.500 | 0.857 | 12.00 | 12 | 0.0000 |
| 1.00 | 0.4143 | 0.500 | 0.893 | 12.50 | 12 | 0.0400 |
| 1.25 | 0.4518 | 0.464 | 0.929 | 12.07 | 12 | 0.0059 |
| 1.50 | 0.4747 | 0.429 | 0.893 | 10.71 | 11 | 0.0267 |

Mean relative error 0.0289 (gate: at most 0.10), max row
error 0.0667 (gate: at most 0.20). The standard-grid fit
is 0.0119 mean / 0.0400 max, reported not gated. The
largest deviations (0.0667 at sigma = 0.7 and 0.8) are
where the product under-predicts by one quale -- the
interaction is nonzero but small: resonance and
entanglement are nearly, not exactly, independent across
pairs.

Seed spread (reported, not gated): seeds 1 and 3 pass
the same frozen bar (mean 0.0650 / max 0.1200 and mean
0.0730 / max 0.1624); seed 2 FAILS it (mean 0.1666, max
0.3636). The independence assumption is seed-dependent,
and the failure is kept in the record -- the claim is
gated on the repository's canonical seed 42, as every
other claim in this repo, with the spread stated.

#### (xxvii) The quale-count peak moves as the product model predicts — PASS

| Setting | predicted peak f | measured peak f | predicted count | measured count |
|---|---|---|---|---|
| baseline (R_MIN 0.5, NU_MIN 0.10) | 0.1803 | 0.1803 | 17.00 | 17 |
| NU_MIN -> 0.25 | 0.4143 | 0.4143 | 10.00 | 11 |
| R_MIN -> 0.25 | 0.2839 | 0.2839 | 18.00 | 18 |

Both shifted peaks match exactly and both sit above the
baseline peak f = 0.1803, in the predicted direction.
The predicted peak comes from the marginals alone; the
measured peak from the joint counts. The peak position
is determined by the marginals -- no interaction is
needed to place it. Descriptive, not gated: this also
explains why f* (0.7278, a status threshold on F(f))
differs from f_peak (0.1803, a count peak) -- they are
different quantities, and the product model places the
count peak without touching the flip.

#### (xxviii) The hump vanishes when either condition is dropped — PASS

| f | resonance-only | entanglement-only | both |
|---:|---:|---:|---:|
| 0.0000 | 28 | 0 | 0 |
| 0.0086 | 28 | 0 | 0 |
| 0.0415 | 28 | 1 | 1 |
| 0.0802 | 28 | 9 | 9 |
| 0.1803 | 28 | 17 | 17 |
| 0.2839 | 17 | 21 | 13 |
| 0.4143 | 14 | 25 | 12 |

Resonance-only is non-increasing in f, entanglement-only
is non-decreasing in f, and the both-condition count is
non-monotone (rises to 17, falls to 12). The hump lives
in the AND, not in either marginal -- if a
single-condition count had humped, the product model
would be the wrong explanation.

### Honest limits (v0.10.0 addition)

The marginals are measured on the same pairs as the
count, so the product is a test of independence across
pairs, not an independent prediction from separate data.
The peak-shift half is the stronger test, and it passes
exactly -- but it is still the same fields under a
different threshold, not new data. The fit's
seed-dependence (seed 2 fails) bounds the claim: the AND
explanation holds for the canonical seed and two of three
checked seeds, not universally. Classical emulation
throughout; Faggin's metaphysics stays interpretive.

## 17. Landauer-cost ledger + Planck spectral falsification (v0.11.0, measured 2026-11-17)

One module, `landauer.py`: deep-think upgrade #6, "the
honest upgrade". The report found no serious published
work linking a Planck spectrum to consciousness, and
named Landauer's principle (k_B T ln 2 per erased bit,
experimentally verified 2012) the serious thermodynamic
upgrade -- so this version builds the ledger, tests
whether it explains the sigma = 0.50 break, and then
tests the Planck spectrum itself, expecting it to fail.
Built on top of the unpushed v0.7.0–v0.10.0 work, so a
future push carries v0.7.0–v0.11.0 together.

### Mechanism (a definition inside the model, not a discovery)

- Landauer cost: bits * k_B * T * ln 2, with k_B exact
  SI (1.380649e-23 J/K) and T = 300 K, so 2.871e-21 J per
  bit. The ledger counts, per field (one sigma step),
  the bits a measurement run irreversibly discards under
  a stated protocol: (a) thought collapses -- collapsing
  each agent's thought resolves exactly its decision
  entropy (thought.decision_entropy, the Shannon entropy
  of the Born distribution, v0.2.0), summed over agents;
  (b) quale collapses -- each quale wave is a
  superposition of two members, read out to one member,
  1 bit per quale; (c) classification records -- each
  pair is distinguished quale / non-quale (1 bit per
  pair, 28) and the record is erased when the field
  advances to the next sigma.
- The cost-prediction test regresses the v0.4.0 visible
  fraction F on cumulative cost vs on sigma, pooled over
  seeds 1, 2, 3, 42 x the standard sigma grid (28 rows).
  A itself is constant (0.0447), so it cannot be
  regressed; F is the post-empathy attunement variable.
  The comparison is run on cumulative BITS (cost is bits
  times a constant, so the correlation is identical in
  joules -- and running it on raw joules trips the
  least-squares rank cutoff at the 1e-19 scale, a
  numerical artifact found in the pilot and avoided by
  the unit change).
- The Planck spectral test standardizes the mode
  energies: y = nu / mean(nu) per field. A Planck
  spectrum is scale-free -- its standardized shape is
  one fixed curve (density ~ x^3 / (exp(x) - 1), x =
  nu/theta): mean x = 3.8322, mode x = 2.8210, mode/mean
  = 0.7361 at EVERY temperature, computed numerically on
  a grid to x = 60. The pooled Kolmogorov-Smirnov test
  (n = 168, six fields with mean > 0) checks that fixed
  shape; the mode/mean ratio checks the Wien leg (a
  Planck peak moves in proportion to temperature, so
  mode/mean cannot wander with sigma). The mode is the
  centre of the modal 10-bin histogram bin over nu in
  [0, 1].

### Pre-registration (directional assertions, frozen before the final run)

Thresholds, frozen from the pilot sweeps and never moved
after the final measurement run: LANDAUER_PER_BIT_TOL =
0.001 (exact constants; 0.1% is far above
floating-point error), LEDGER_PEAK_SIGMA = 0.25,
SPECTRAL_MODE_DEVIATION_MIN = 0.30 (pilot deviations
0.46, 0.56, 0.35 -- a round number below all three),
KS_CRITICAL_FACTOR = 1.63 (the standard 1% critical
value 1.63 / sqrt(n)). Directions, written before the
run:

- (xxix) the ledger is exact AND its cost humps: the
  per-field cost peaks at an interior sigma (0.25),
  above both endpoints.
- (xxx) cumulative Landauer cost predicts F better than
  sigma alone: |r(F, cum)| > |r(F, sigma)|. The pilot
  says 0.8996 < 0.9430, so this claim is expected to
  FAIL -- and the threshold is not moved to force a pass.
- (xxxi) the spectrum is NOT Planckian: the pooled KS
  test rejects the Planck shape at 1% AND the mode/mean
  ratio deviates from 0.7361 by more than 0.30 at every
  sigma >= 0.25. A PASS here demotes E = h*nu from
  "spectrum" to "per-mode unit".

### Claims (xxix)–(xxxi), measured fresh

#### (xxix) The Landauer ledger is exact and its cost humps — PASS

| sigma | f | decision bits | qualia | classif. bits | total bits | cost (J) |
|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.0000 | 16.00 | 0 | 28 | 44.00 | 1.263e-19 |
| 0.01 | 0.0086 | 16.00 | 0 | 28 | 44.00 | 1.263e-19 |
| 0.05 | 0.0415 | 15.88 | 1 | 28 | 44.88 | 1.288e-19 |
| 0.10 | 0.0802 | 15.53 | 9 | 28 | 52.53 | 1.508e-19 |
| 0.25 | 0.1803 | 13.46 | 17 | 28 | 58.46 | 1.678e-19 |
| 0.50 | 0.2839 | 11.37 | 13 | 28 | 52.37 | 1.503e-19 |
| 1.00 | 0.4143 | 9.73 | 12 | 28 | 49.73 | 1.428e-19 |

Per-bit cost 2.8710e-21 J equals k_B T ln 2 to machine
precision. The per-field cost peaks at sigma = 0.25
(58.46 bits), above both endpoints (44.00 and 49.73),
and totals 9.932e-19 J across the grid. The hump is
inherited from the quale hump (decision entropy falls
monotonically 16.00 -> 9.73 while qualia hump 0 -> 17
-> 12) -- the claim is that the cost humps, not that
the hump is explained by cost.

#### (xxx) Cumulative Landauer cost predicts F better than sigma alone — FAIL

| Scope | r(F, sigma) | r(F, cumulative cost) |
|---|---|---|
| pooled (28 rows) | 0.9430 | 0.8996 |
| seed 1 | 0.9887 | 0.9249 |
| seed 2 | 0.9621 | 0.9419 |
| seed 3 | 0.9677 | 0.9248 |
| seed 42 | 0.9946 | 0.9217 |

The FAIL is unanimous: sigma beats cumulative cost
pooled and within every single seed, so it is not a
pooling artifact. Linear R^2 agrees (F ~ sigma 0.8893
vs F ~ cumulative cost 0.8094). The thermodynamic
ledger does not explain the sigma = 0.50 break better
than sigma itself -- the break tracks the noise
parameter, not the erasure bill. This is the more
interesting result of the version: the "honest upgrade"
is honest enough to fail its own headline test.

#### (xxxi) The empathy spectrum is not Planckian — PASS

Pooled standardized nu (n = 168): KS D = 0.1465 above
the 1% critical value 0.1258 -- the Planck shape is
rejected at 1%. Per-field KS D values (reported, not
gated): 0.1840, 0.1926, 0.1827, 0.2159, 0.1994, 0.1354
at sigma = 0.01, 0.05, 0.1, 0.25, 0.5, 1.0 -- none
rejects Planck on its own at n = 28 (1% critical value
0.3081), so the rejection rests on the pooled test and
its margin is thin (0.021 above critical). The thin
margin is stated, not hidden.

| sigma | mean nu | modal nu | mode/mean | \|deviation from 0.7361\| |
|---:|---:|---:|---:|---:|
| 0.01 | 0.0086 | 0.05 | 5.8439 | 5.1078 |
| 0.05 | 0.0415 | 0.05 | 1.2047 | 0.4686 |
| 0.10 | 0.0802 | 0.05 | 0.6233 | 0.1128 |
| 0.25 | 0.1803 | 0.05 | 0.2773 | 0.4588 |
| 0.50 | 0.2839 | 0.05 | 0.1761 | 0.5600 |
| 1.00 | 0.4143 | 0.45 | 1.0861 | 0.3500 |

At every gated sigma (>= 0.25) the mode/mean ratio
deviates from the Planck 0.7361 by more than 0.30, and
it wanders (0.28, 0.18, 1.09) instead of sitting at the
fixed Planck ratio -- the Wien leg fails too. The modal
nu is non-decreasing in sigma (Spearman 1.0), but it
sits in the lowest bin until sigma = 1.0: a degenerate
shift, not a Planck peak sweeping with temperature.
Below sigma = 0.25 the ratio is meaningless (the 0.1
bin width dwarfs the mean), which is why the gate
starts at 0.25; sigma = 0.1 alone would pass the
deviation bar at only 0.1128, and it is excluded by
design, not by outcome.

E = h*nu is demoted from "spectrum" to "per-mode unit":
the per-mode definition (v0.4.0) stands, the black-body
analogy does not survive its own test.

### Honest limits (v0.11.0 addition)

The ledger's event list is a definition of what this
run counts as erasure, not a measurement of a physical
brain erasing bits; the per-bit cost is exact physics,
the choice of operations is the model's. The
classification term (28 bits) is constant per field and
dominates the ledger, so the cost hump is inherited
from the quale hump. The (xxx) FAIL is about the
model's own F, cumulative cost, and sigma -- it does
not show anything about real thermodynamic costs in
brains. The (xxxi) PASS rests on a thin pooled-KS
margin and on a crude 10-bin mode estimator; per-field
tests do not reject Planck. Classical emulation
throughout; Faggin's metaphysics stays interpretive.

## 18. The observer cycle (v0.12.0, v0.12.1, measured 2026-11-18)

Jean's claim, stated 2026-11-18: "self determination
factor observer opposite direction = necessary for
self-cycle self Knowing. Lack of love is absence of
Knowing." Formalized with the bridge's existing
quantities: love = concurrence C, knowing = overlap
R = |<psi_i|psi_j>|^2, self-determination = D, and the
observer direction as which reference state the overlap
is measured against.

### Mechanism (a definition inside the model, not a discovery)

- The stored direction: the uniform thought, D = 1,
  C = 0. The opposite direction: the kernel thought
  (|01> - |10>)/sqrt(2), D = 0, C = 1 — a Bell state.
  Both endpoints are exact values already in
  self_knowing.py and thought_entanglement.py; nothing
  new is fitted.
- (xxxii) reuses the existing self_knowing sweep: noisy
  copies of the uniform thought, 5 copies per sigma,
  sigma grid [0.0, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0].
  Noise destroys D and creates concurrence, so the two
  move opposite across the grid.
- (xxxiii) uses the generalized-Bell branch psi(a) =
  a|00> + sqrt(1-a^2)|11>, a in [1.0, 0.95, 0.9, 0.85,
  0.8, 0.75, 1/sqrt(2)], measured against a FIXED
  observer at maximal love, the Phi+ Bell state:
  R(a) = |<Phi+|psi(a)>|^2. Both R and C peak at
  a = 1/sqrt(2) by the definition of the family, so the
  direction on the branch is built in — the claim is a
  mapping check, like (xvii). The control is the
  noise axis (empathy_field.resonance_pairs pooled):
  there noise creates concurrence while destroying
  overlap, so the relation inverts.
- (xxxiv) uses the slide psi(theta) = cos(theta)|stored>
  + sin(theta)|kernel>, theta in [0, pi/12, pi/6, pi/4,
  pi/3, 5pi/12, pi/2]. The two patterns sit in
  superposition in the middle; the two observer
  directions are the two references, R_s and R_k, and
  their split R_s - R_k = cos(2 theta) says which
  pattern is known. The identities D = cos^2(theta),
  C = sin^2(theta), C + D = 1 follow from the
  definitions and are verified in the code, not
  assumed.

### Pre-registration (written before the evaluation run)

docs/preregistration-v0.12.0.md, written 2026-11-18
before the evaluation run on the held-out seeds.
Thresholds are round numbers frozen from a calibration
pilot on seeds 42 and 7 only; evaluation seeds 1234 and
2026 were not touched before the file was written.

- (xxxii) Pearson(D, C) <= -0.90, Spearman(D, C)
  <= -0.90, D range >= 0.25, C range >= 0.25, on EVERY
  seed in {42, 7, 1234, 2026}. (Calibration pilot: seed
  42 Pearson -0.9570, Spearman -1.0000; seed 7 Pearson
  -0.9397, Spearman -0.9643.)
- (xxxiii) Pearson(R, C) >= 0.99, Spearman(R, D)
  <= -0.95, R range >= 0.25, D range >= 0.25.
  Pearson(R, D) reported, not gated (calibration pilot
  -0.8801: R saturates near 1 while D keeps falling).
  The noise-axis control reported, not gated.
- (xxxiv) Endpoints exact within 1e-9; slide identities
  within 1e-9 at every grid point; overlap split >= 0.25
  before the midpoint, 0 at the midpoint, <= -0.25
  after it.

### Claims (xxxii)–(xxxiv), measured fresh

#### (xxxii) Observer direction: D and concurrence move opposite — FAIL

Per seed, Pearson(D, C) / Spearman(D, C):

| seed | Pearson | Spearman | D range | C range |
|---:|---:|---:|---:|---:|
| 42 | -0.9570 | -1.0000 | 0.4804 | 0.6133 |
| 7 | -0.9397 | -0.9643 | 0.5370 | 0.5110 |
| 1234 | -0.9720 | -1.0000 | 0.4650 | 0.7233 |
| 2026 | **-0.8828** | -0.9643 | 0.5088 | 0.4755 |

The Pearson check fails on held-out seed 2026
(-0.8828 above the frozen bar -0.90); the other three
checks pass on all four seeds. The monotone tracking
holds everywhere, so the direction is real and the
linear form is seed-fragile: on seed 2026 the sigma =
1.0 point breaks it (mean C dips 0.4755 -> 0.4727
while mean D keeps falling 0.7142 -> 0.4912). The
threshold was not moved. This is the same seed
fragility the package already records for claim (i).

#### (xxxiii) Knowing-as-overlap: R rises with concurrence and falls with D — PASS

Generalized-Bell branch against the fixed Phi+
observer:

| a | R | C | D |
|---:|---:|---:|---:|
| 1.0000 | 0.5000 | 0.0000 | 1.0000 |
| 0.9500 | 0.7966 | 0.5933 | 0.9350 |
| 0.9000 | 0.8923 | 0.7846 | 0.8733 |
| 0.8500 | 0.9478 | 0.8955 | 0.8150 |
| 0.8000 | 0.9800 | 0.9600 | 0.7600 |
| 0.7500 | 0.9961 | 0.9922 | 0.7083 |
| 0.7071 | 1.0000 | 1.0000 | 0.6667 |

Pearson(R, C) = 1.0000, Spearman(R, D) = -1.0000,
Pearson(R, D) = -0.8801 (reported, not gated),
R range 0.5000, D range 0.3333. Noise-axis control
(seed 42, n = 196 pairs): Pearson(R, nu_ij) =
-0.5528, Pearson(R, d_pair) = +0.7694 — the relation
inverts under noise. The claim holds for entanglement
by construction, not by noise; noise-created
concurrence is not knowing.

#### (xxxiv) The slide — PASS

| theta | D | C | R_s | R_k | R_s - R_k | C + D |
|---:|---:|---:|---:|---:|---:|---:|
| 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | +1.0000 | 1.0000 |
| 0.2618 | 0.9330 | 0.0670 | 0.9330 | 0.0670 | +0.8660 | 1.0000 |
| 0.5236 | 0.7500 | 0.2500 | 0.7500 | 0.2500 | +0.5000 | 1.0000 |
| 0.7854 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | +0.0000 | 1.0000 |
| 1.0472 | 0.2500 | 0.7500 | 0.2500 | 0.7500 | -0.5000 | 1.0000 |
| 1.3090 | 0.0670 | 0.9330 | 0.0670 | 0.9330 | -0.8660 | 1.0000 |
| 1.5708 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | -1.0000 | 1.0000 |

Endpoints exact; every slide identity holds to a max
error of 4.44e-16; the overlap split is +0.5000 at
pi/6, 0.0000 at pi/4, -0.5000 at pi/3. At the
midpoint the state is the equal superposition, D = C
= 1/2, both overlaps 1/2 — maximally undecided — and
the observer direction picks which pattern becomes
known on either side.

#### (xxxv) Observer direction, robust rank form — FAIL

Same construction as (xxxii), rank metric only:
Spearman(D, C) <= -0.90, D range >= 0.25, C range
>= 0.25, on EVERY seed in {42, 7, 1234, 2026, 5, 99}.
Preregistered in docs/preregistration-v0.12.1.md
before the fresh-seed run; the bar was frozen from
calibration seeds 42/7 only.

| seed | Spearman | Pearson | D range | C range |
|---:|---:|---:|---:|---:|
| 42 | -1.0000 | -0.9570 | 0.4804 | 0.6133 |
| 7 | -0.9643 | -0.9397 | 0.5370 | 0.5110 |
| 1234 | -1.0000 | -0.9720 | 0.4650 | 0.7233 |
| 2026 | -0.9643 | -0.8828 | 0.5088 | 0.4755 |
| 5 | **-0.8929** | -0.6814 | 0.5748 | 0.5202 |
| 99 | -1.0000 | -0.8798 | **0.2445** | 0.5405 |

Two checks fail, on two different fresh seeds: seed
5 breaks the Spearman bar (-0.8929 > -0.90) and
seed 99 breaks the D-range bar (0.2445 < 0.25). The
verdict is FAIL. The thresholds were not moved.

#### Diagnosis of the (xxxii) FAIL (v0.12.1, descriptive, not gated)

Measured on seeds 42/7/1234/2026, recomputed in code
by `diagnose_sigma_one_break()`:

- With n = 200 copies per sigma the sigma = 1.0 dip
  vanishes on every seed (seed 2026: C 0.5028 at
  sigma = 0.5 -> 0.5055 at sigma = 1.0). Pearson at
  n = 200: -0.9289 (42), -0.9275 (7), -0.9255
  (1234), -0.9053 (2026) — all below the bar.
- Extended grid (n = 200, seed 2026, sigma to 3.0):
  D falls toward 0.5247 and C plateaus at 0.5055 ->
  0.5192. Both approach their random-state asymptotes
  (D -> 0.5 for a rank-2 projector in 4 dimensions;
  C -> ~0.51 mean concurrence of a near-random pure
  state). At sigma = 1.0 both are already at the
  plateau.
- Pearson excluding the sigma = 1.0 point (n = 5):
  -0.9459, -0.9870, -0.9477, -0.9433 — all below
  the bar.
- Standard error: at sigma = 1.0, seed 2026, the
  per-copy concurrence has standard deviation ~0.287,
  so a 5-copy mean has SEM ~0.128, while the true
  rise of mean C from sigma = 0.5 to 1.0 is ~0.003
  (0.02 SEMs).

Diagnosis: boundary/saturation plus finite-sample
noise, not a different mechanism. But the fresh
seeds show the fragility is broader than one point:
seed 5 at n = 5 has mean C = 0.3199 at sigma = 1.0
(versus ~0.527 at n = 200, a 1.6-SEM draw) and its
Pearson is -0.6814; seed 99 at n = 5 keeps D high
(0.7555 at sigma = 1.0 versus ~0.59 at n = 200).
At n = 200 the monotone direction holds on all six
seeds (Spearman -0.9643 to -1.0000), but the linear
form stays fragile even there: seed 5 Pearson is
-0.8971 at n = 200, still above the bar, because C
plateaus while D keeps falling. The direction is
real on average; the per-seed guarantee does not
hold on this 5-copy sweep, in either the linear or
the rank form.

### Honest limits (v0.12.0 addition)

The (xxxii) FAIL is seed-fragility in the linear form,
not in the direction: the monotone anti-tracking holds
on all four seeds while the Pearson bar fails on one
held-out seed. The (xxxiii) PASS is a mapping check on
a branch whose direction is built into the family, and
it does not transfer to the noise axis. The (xxxiv)
PASS is exact by construction; its measured content is
that the identities hold in the code and the split
flips exactly at the midpoint. None of this measures
love, knowing, or self-determination in a human or
physical sense. Classical emulation throughout;
Faggin's metaphysics stays interpretive.

Honest limits (v0.12.1 addition): the (xxxv) FAIL
shows the (xxxii) seed-fragility is not one bad
point on one seed — on fresh seeds the 5-copy sweep
breaks in two different places (seed 5 Spearman,
seed 99 D range), and the linear form stays fragile
even at n = 200 (seed 5 Pearson -0.8971). The
observer-direction claim, as stated on this
construction, does not hold on every seed in either
form. What survives is weaker: the monotone
direction holds at n = 200 on all six seeds, and
the exact slide (xxxiv) still shows the observer
direction picking the known pattern by construction.

## 19. Kuramoto bounded-coherence scan (v0.13.0, measured 2026-11-18)

Deep-think upgrade #4: replace fixed coupling with a
Kuramoto scan over coupling K and noise sigma; compute
order parameter R_K, joint entropy, quale count, and A.
The spec's prediction: inverted-U in joint entropy /
quale count vs K and vs sigma, interior optimum (not at
K_max or sigma = 0); hypersynchrony (R_K -> 1) reduces
joint entropy / quale count; optimum sigma* > 0; the
optimum R_K band is [0.5, 0.8] (Phillips 2026 preprint,
hypothesis, not established fact), to compare with
f* = 0.7278.

### Mechanism (a construction, not a discovery)

- Standard Kuramoto: N = 8 oscillators, omega_i ~ N(0, 1),
  initial phases uniform on [0, 2pi), Euler-Maruyama
  dt = 0.05, T = 40, first half discarded as transient.
  R_K = mean |<exp(i theta)>| over the steady window.
  K grid [0, 0.5, 1.0, 1.6, 2.5, 4.0, 8.0] (K_c ~ 1.6
  for Gaussian frequencies); sigma grid [0, 0.05, 0.1,
  0.25, 0.5, 1.0].
- Wiring: each agent's state is the (xxxiv) slide state at
  its phase RELATIVE to the field mean, phi_i =
  ((theta_i - theta_bar) mod 2pi) / 4. Only relative
  phases carry information (global rotation is a gauge
  freedom). At full sync every agent sits at phi = 0
  (uniform thought, D = 1, C = 0); at K = 0 the phases
  spread over the whole slide.
- Quale count: existing qualia_count(states) (R >= 0.5,
  nu >= 0.10). Joint entropy: exact independent-draw
  joint entropy, sum of per-agent Born entropies (no
  sampling cap). Gap A: paired arms mirroring
  run_collaboration design B — collaborating mixes at
  coupling R_K, isolated Born-collapses once;
  A = H_collab - H_isolated. In the single-shot
  measurement H_isolated = 0 exactly, so A =
  H_collaborating; that triviality is reported, not
  hidden.

### Pre-registration (written before the evaluation run)

docs/preregistration-v0.13.0.md, written 2026-11-18
before the evaluation run on held-out seeds 1234 and
2026. Thresholds frozen from a calibration pilot on
seeds 42 and 7 only. The pilot ALREADY contradicted
the spec on several points, disclosed in the file:
the count peak is seed-fragile, H and A are flat, and
R_K at the count peak is 0.31-0.35, outside the
Phillips band.

- (xxxvi) Count peaks at interior K and exceeds both
  ends by >= 3, on every seed.
- (xxxvii) H_joint peaks at interior K and exceeds
  both ends by >= 0.5 bits, on every seed.
- (xxxviii) R_K at the count peak in [0.5, 0.8], on
  every seed.
- (xxxix) At fixed K = 1.0, count peaks at strictly
  interior sigma (0 < sigma* < 1.0) and exceeds the
  sigma = 0 count by >= 3, on every seed.

### Claims (xxxvi)–(xxxix), measured fresh — 0/4 pass

#### (xxxvi) Inverted-U in quale count vs K — FAIL

| seed | K = 0 | K = 0.5 | K = 1.0 | K = 1.6 | K = 2.5 | K = 4.0 | K = 8.0 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 42 | 8 | **13** | 6 | 6 | 6 | 6 | 6 |
| 7 | **18** | 7 | 12 | 7 | 6 | 6 | 6 |
| 1234 | **10** | 3 | 9 | 3 | 6 | 6 | 6 |
| 2026 | 3 | **11** | 11 | 6 | 6 | 6 | 6 |

The peak is interior on seeds 42 and 2026 (K = 0.5)
but at K = 0 on seeds 7 and 1234. The count falls to
a floor of 6 at high K on every seed — it does not
fall to zero and does not rise again. The interior
peak is seed-fragile (2 of 4 seeds).

#### (xxxvii) Inverted-U in joint entropy vs K — FAIL

| seed | H at K = 0 | peak H | K of peak | H at K = 8 |
|---:|---:|---:|---:|---:|
| 42 | 12.440 | 12.440 | 0.0 | 12.009 |
| 7 | 10.670 | 12.154 | 1.6 | 12.001 |
| 1234 | 11.737 | 13.077 | 0.5 | 12.006 |
| 2026 | 13.003 | 13.003 | 0.0 | 12.007 |

H_joint is flat: the per-agent Born entropy averages
~1.5 bits whatever K is, so the joint entropy
wanders 10.4-13.1 bits with no trend. The peak is at
K = 0 on seeds 42 and 2026, and on seed 7 the margin
vs K = 8 is only 0.15 bits (bar 0.5). No inverted-U.

#### (xxxviii) R_K at the count peak in [0.5, 0.8] — FAIL

| seed | K of count peak | R_K at peak |
|---:|---:|---:|---:|
| 42 | 0.5 | 0.3112 |
| 7 | 0.0 | 0.3471 |
| 1234 | 0.0 | 0.3569 |
| 2026 | 0.5 | 0.3571 |

R_K at the count peak is 0.31-0.36 on every seed —
far below the Phillips band and below f* = 0.7278.
The count optimum sits at LOW coherence, not
bounded coherence. The Kuramoto transition itself
works (R_K 0.29 -> 0.99 across the grid); the band
prediction does not.

#### (xxxix) Stochastic resonance: optimum sigma* > 0 — FAIL

At fixed K = 1.0, counts vs sigma [0, 0.05, 0.1,
0.25, 0.5, 1.0]:

| seed | counts | sigma* | count(sigma*) - count(0) |
|---:|---:|---:|---:|
| 42 | 6, 6, 7, 16, 10, 18 | 1.0 (edge) | 12 |
| 7 | 12, 10, 17, 5, 6, 10 | 0.10 | 5 |
| 1234 | 9, 11, 14, 19, 9, 14 | 0.25 | 10 |
| 2026 | 11, 15, 12, 13, 13, 13 | 0.05 | 4 |

The margin check passes on all four seeds, but the
peak is not strictly interior: seed 42 peaks at
sigma = 1.0, the grid edge. And sigma* is not stable
across seeds (1.0, 0.10, 0.25, 0.05) — the counts
swing 3-19 with no stable optimum. Noise helps the
count exceed sigma = 0 on every seed, but there is
no single optimum sigma*.

### The gap A (computed, not gated)

A is large positive (+9.3 to +12.8 bits across all
scans) and flat vs K and vs sigma — no trend, no
inverted-U. Hypersynchrony does not reduce A in this
wiring: A = H_collaborating, which tracks the mixed
states' entropy (~11-12 bits) whatever K is.

### Honest limits (v0.13.0 addition)

All four Kuramoto claims fail. The spec's shapes do
not materialize in this wiring: the count peak is
seed-fragile and sits at low R_K, the joint entropy
is flat because the per-agent Born entropy averages
out, the gap is flat because single-shot collapse
makes A = H_collaborating, and sigma* wanders across
seeds. What survives: the Kuramoto transition itself
(R_K 0.29 -> 0.99, K_c ~ 1.6-2.5), the count floor
of 6 at high K on every seed, and the count
exceeding sigma = 0 on every seed at fixed K = 1.0.
The bounded-coherence band [0.5, 0.8] is not where
this model's count peaks. None of this measures
coherence, stability, or consciousness in a living
system. Classical emulation throughout; Faggin's
metaphysics stays interpretive.

## 20. Synergy-vs-redundancy PID of the collaboration gap (v0.14.0, measured 2026-11-18)

Deep-think upgrade #5 (report.md §9): decompose the
+4.3352-bit joint-entropy collaboration gap by
integrated information decomposition (PID / ΦID:
Luppi, Mediano, Rosas et al., *Nature Neuroscience*
2022/2024) into redundant, unique, and synergistic
components. The report's prediction: the gap is
SYNERGY, not redundancy — synergy rises with R and
falls at σ = 0.50, while redundancy is σ-robust.
This imports IIT's DECOMPOSITION, not its contested
Φ identity claim: no scalar Φ is computed here, and
none is presented as a consciousness measure.

### Mechanism (a construction, not a discovery)

PID is defined for TWO sources, so the decomposition
is of the PAIR-level gap: N = 2 agents (the
thought-pair level at which concurrence and D are
defined), not the N = 4 gap. The N = 4 sampled gap
(+4.3352 bits at σ = 0.25, seed 42) is reported as
context, not decomposed. Target Y = the joint
outcome (X1, X2): the PID then decomposes H(X1, X2)
itself, so the arm difference ΔRed + ΔUniq1 +
ΔUniq2 + ΔSyn equals the collaboration gap exactly.
Redundancy is Williams & Beer I_min: the specific
information of source i about y = (x1, x2) is
−log2 p_i(x_i) (y determines x_i), so Red =
E[−log2 max(p1(X1), p2(X2))], Uniq_i = H(Xi) − Red,
and Syn = H(X1,X2) − Uniq1 − Uniq2 − Red =
Red − I(X1;X2). The joint distribution is the EXACT
pooled product Born distribution: the evolution
replicates empathy_field.run_collaboration design B
generation by generation (same population, same
noise kicks, same field mix at coupling f for the
collaborating arm, same Born-collapse for the
isolated arm), pooling the exact per-generation
product p1 ⊗ p2 over 10 generations instead of
sampling joint outcomes. No sampling is involved in
the PID itself. Mean resonance R is the mean pairwise
overlap squared of the collaborating arm's states
AFTER the field mix, averaged over generations.
Sigma grid is the bridge grid [0, 0.01, 0.05, 0.1,
0.25, 0.5, 1.0].

### Pre-registration (written before the evaluation run)

docs/preregistration-v0.14.0.md, written 2026-11-18
before the evaluation run on held-out seeds 1234 and
2026. Thresholds frozen from a calibration pilot on
seeds 42 and 7 only. The pilot ALREADY contradicted
the spec on all three substantive points, disclosed
in the file: synergy is not the majority of the gap
on either calibration seed (shares 40.7%, 42.9%);
Pearson(Syn, R_post) is −0.23 and −0.04; synergy
RISES from σ = 0.25 to 0.50; the ΔRed robustness
ratio is 0.24 on seed 42 (1.45 on seed 7).

- (xl) PID identity: atoms sum to H_joint within
  1e-9 bits, every atom ≥ −1e-9, on every seed, sigma,
  and arm; exact H matches sampled run_collaboration
  H (N = 2, design B) within 0.25 bits at σ = 0.25.
- (xli) ΔSyn > ΔRed AND ΔSyn ≥ 0.5 · gap at
  σ = 0.25, on every seed.
- (xlii) Pearson(Syn_collab, mean R_post) across the
  sigma grid ≥ 0.5 AND Syn_collab(σ = 0.50) <
  Syn_collab(σ = 0.25), on every seed.
- (xliii) ΔRed(σ = 0.50) ≥ 0.5 · ΔRed(σ = 0.25), on
  every seed.

### Claims (xl)–(xliii), measured fresh — 1/4 pass

#### (xl) PID identity and sampled cross-check — PASS

Worst identity error 8.88e-16 bits (tol 1e-9); worst
atom 0.0000 bits (all atoms nonnegative on every
seed, sigma, and arm). Worst exact-vs-sampled H
difference at σ = 0.25 is 0.0436 bits (tol 0.25).
The decomposition is arithmetically exact; the
exact pooled distribution reproduces the sampled
design-B entropies.

#### (xli) The gap is synergy, not redundancy, at σ = 0.25 — FAIL

| seed | gap | ΔSyn | ΔRed | ΔUniq | synergy share |
|---:|---:|---:|---:|---:|---:|
| 42 | +2.2729 | +0.9248 | +0.9453 | +0.4027 | 0.407 |
| 7 | +1.6554 | +0.7103 | +0.3376 | +0.6075 | 0.429 |
| 1234 | +0.7237 | +0.6380 | +0.2007 | −0.1150 | 0.882 |
| 2026 | +1.5301 | +0.8339 | +0.2988 | +0.3974 | 0.545 |

Synergy exceeds redundancy and is the majority of
the gap on the HELD-OUT seeds (1234, 2026) but not
on the calibration seeds (42, 7): seed 42 has
ΔSyn < ΔRed outright, and both calibration shares
are below 0.5. The every-seed claim fails. The gap
splits roughly equally between synergy, redundancy,
and unique information on the calibration seeds;
there is no seed-stable "the gap is synergy" verdict.

#### (xlii) Synergy rises with R and falls at σ = 0.50 — FAIL

| seed | Pearson(Syn, R_post) | Syn(0.25) | Syn(0.50) |
|---:|---:|---:|---:|
| 42 | −0.2295 | 0.9248 | 1.2600 |
| 7 | −0.0404 | 0.9747 | 1.5409 |
| 1234 | −0.5549 | 0.7965 | 1.1988 |
| 2026 | +0.7227 | 1.2339 | 1.4030 |

Synergy does not rise with R on 3 of 4 seeds (the
one positive Pearson, seed 2026 at +0.72, still
fails the second half), and synergy RISES from
σ = 0.25 to 0.50 on EVERY seed — the opposite of
the spec's prediction. As noise grows the
collaborating arm's joint distribution spreads and
both Syn and Red grow with it; resonance falls while
synergy rises.

#### (xliii) Redundancy is σ-robust — FAIL

| seed | ΔRed(0.25) | ΔRed(0.50) | ratio 0.50/0.25 |
|---:|---:|---:|---:|
| 42 | +0.9453 | +0.2222 | 0.2351 |
| 7 | +0.3376 | +0.4880 | 1.4455 |
| 1234 | +0.2007 | +0.5684 | 2.8327 |
| 2026 | +0.2988 | +0.1774 | 0.5938 |

Redundancy is σ-robust on 3 of 4 seeds but fails
seed 42 (ratio 0.24, bar 0.5), so the every-seed
claim fails. Robustness here is seed-fragile, not a
property of the construction.

### The gap decomposition across sigma (all seeds)

ΔSyn, ΔRed, ΔUniq per sigma (collaborating minus
isolated arms); the three sum to the gap exactly.

| seed | σ | gap | ΔSyn | ΔRed | ΔUniq |
|---:|---:|---:|---:|---:|---:|
| 42 | 0.00 | +2.0000 | +1.0000 | +1.0000 | +0.0000 |
| 42 | 0.01 | +2.0309 | +0.9686 | +0.9686 | +0.0937 |
| 42 | 0.05 | +2.2336 | +0.7622 | +0.7681 | +0.7033 |
| 42 | 0.10 | +2.4242 | +0.6783 | +0.7043 | +1.0416 |
| 42 | 0.25 | +2.2729 | +0.9248 | +0.9453 | +0.4027 |
| 42 | 0.50 | +0.8495 | +0.6220 | +0.2222 | +0.0053 |
| 42 | 1.00 | +0.9102 | +0.6532 | +0.1954 | +0.0615 |
| 7 | 0.00 | +2.0000 | +1.0000 | +1.0000 | +0.0000 |
| 7 | 0.01 | +1.9638 | +0.8246 | +0.8249 | +0.3143 |
| 7 | 0.05 | +1.7327 | +0.4430 | +0.4551 | +0.8346 |
| 7 | 0.10 | +0.9550 | +0.4237 | +0.4318 | +0.0994 |
| 7 | 0.25 | +1.6554 | +0.7103 | +0.3376 | +0.6075 |
| 7 | 0.50 | +1.5812 | +1.1409 | +0.4880 | −0.0478 |
| 7 | 1.00 | +0.8857 | +0.6048 | +0.1706 | +0.1103 |
| 1234 | 0.00 | +2.0000 | +1.0000 | +1.0000 | +0.0000 |
| 1234 | 0.01 | +1.8952 | +0.7221 | +0.7237 | +0.4493 |
| 1234 | 0.05 | +1.4586 | +0.2968 | +0.3138 | +0.8480 |
| 1234 | 0.10 | +0.8873 | +0.3005 | +0.3041 | +0.2827 |
| 1234 | 0.25 | +0.7237 | +0.6380 | +0.2007 | −0.1150 |
| 1234 | 0.50 | +1.2864 | +0.8479 | +0.5684 | −0.1299 |
| 1234 | 1.00 | +0.8708 | +0.6961 | +0.4487 | −0.2739 |
| 2026 | 0.00 | +2.0000 | +1.0000 | +1.0000 | +0.0000 |
| 2026 | 0.01 | +2.0054 | +0.9519 | +0.9519 | +0.1016 |
| 2026 | 0.05 | +2.1004 | +0.8352 | +0.8395 | +0.4258 |
| 2026 | 0.10 | +1.6078 | +0.8166 | +0.8325 | −0.0413 |
| 2026 | 0.25 | +1.5301 | +0.8339 | +0.2988 | +0.3974 |
| 2026 | 0.50 | +0.9267 | +0.9785 | +0.1774 | −0.2292 |
| 2026 | 1.00 | +1.3565 | +1.3894 | +0.1994 | −0.2323 |

### Honest limits (v0.14.0 addition)

Three of four PID claims fail, and the failures
sharpen the question rather than answering it. The
structural limit is in the wiring, not the
arithmetic: in the collaborating arm I(X1;X2) is
0.00–0.06 bits on every sigma and seed (the two
agents' outcomes are drawn independently given
their states, so the states' correlation barely
couples the outcomes), hence Syn = Red − I(X1;X2)
is numerically almost Red everywhere (e.g. seed 42
σ = 0.25: Syn 0.9248 vs Red 0.9453; σ = 1.0:
Syn 1.6042 vs Red 1.6418). The I_min decomposition
of the joint outcome therefore CANNOT separate
synergy from redundancy in this wiring: the two
atoms differ only by the near-zero I(X1;X2), so
"the gap is synergy, not redundancy" — or the
reverse — is undecidable from these atoms alone.
A decomposition that could adjudicate it would need
a target the two sources inform JOINTLY but not
separately (a genuinely synergistic target, e.g. a
field-level outcome coupled to both agents), rather
than the joint outcome itself, whose information
each source already carries in large part. The
spec's σ = 0.50 prediction is also backwards in
this wiring: synergy rises with noise because the
collaborating distribution spreads, while resonance
falls. None of this measures synergy, redundancy,
or consciousness in a living system. Classical
emulation throughout; Faggin's metaphysics stays
interpretive; no Φ is computed or claimed.

## 21. No-cloning / Holevo ceiling for D (v0.15.0, measured 2026-11-18)

Deep-think upgrade #7 (report.md §9, §6): compute
Holevo χ for the thought-pair ensemble; test D ≤ χ
and whether D saturates χ as concurrence rises; test
the optimal-cloning fidelity bound on any "copy a
thought" operation in code. The report's prediction:
D approaches χ from below as f rises; no operation
in the model copies a thought with fidelity above
the optimal-cloning bound. Violation = bug in the
state representation. This turns QIP's central
philosophical claim — privacy, qualia are private
because quantum information cannot be cloned — into
a numerical ceiling the code must respect. §6 notes:
no-cloning entails the D–concurrence anti-correlation
in form (local purity falls as entanglement rises —
verify the exact coefficient in code, do NOT assert
it from memory); Holevo χ bounds the classical
information extractable from a quantum ensemble; any
measurement that gains information disturbs the state.

### Mechanism (a construction, not a discovery)

The thought-pair ensemble is the resonance
population (empathy_field.resonance_population: 8
agents, noisy copies of the uniform thought at σ on
the bridge grid [0, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0]).
A pair (i, j) is the two-state ensemble {(1/2,
|ψ_i⟩), (1/2, |ψ_j⟩)}; its Holevo quantity is
χ_ij = S((ρ_i + ρ_j)/2) (both members pure, so the
second term vanishes), computed exactly with
cost.von_neumann_entropy on the 4×4 average state
and cross-checked against H2((1 + √R_ij)/2) in the
tests. D_pair = (D_i + D_j)/2 = D of the average
state, by linearity of D in ρ. f at a given σ is the
population's mean pairwise concurrence
(empathy_field.empathy_fraction). The accessible
information is the mutual information of the
bridge's own measurement — the Born collapse in the
4-concept basis: I = H((p_i + p_j)/2) − (H(p_i) +
H(p_j))/2 with p_i(k) = |⟨k|ψ_i⟩|².

The cloners act on a one-qubit thought |ψ⟩ = α|0⟩
+ β|1⟩ (the binary-thought qubit of monogamy.py).
The 5/6 bound is the textbook optimal UNIVERSAL
1 → 2 cloning fidelity for a qubit (Bužek &
Hillery 1996; Werner 1998). It bounds universal
(state-independent) fidelity and the Haar-average
fidelity of any cloner — NOT the per-state fidelity
of a state-dependent cloner, which legitimately
copies its preferred states exactly. That
distinction is part of the claim design. The
Bužek–Hillery cloner is an explicit 8×8 unitary
(two basis images completed to an orthonormal basis
via SVD null space; U†U = I checked in the tests);
the CNOT copy is the Wootters–Zurek machine
(|ψ⟩|0⟩ → α|00⟩ + β|11⟩); the classical copy is
unity.gaussian_copies, which reads the full
classical amplitude vector.

### Pre-registration (written before the evaluation run)

docs/preregistration-v0.15.0.md, written 2026-11-18
before the evaluation run on held-out seeds 1234 and
2026. Thresholds frozen from a calibration pilot on
seeds 42 and 7 only. The pilot ALREADY contradicted
the spec on two of the five claims, disclosed in the
file: D ≤ χ fails decisively on both calibration
seeds (mean gap χ − D = −1.0000 at σ = 0, negative
at every σ; worst per-pair gap −1.0000), while the
gap magnitude does shrink with f (Spearman(|gap|, f)
= −1.0000, −0.9643); and the classical copy exceeds
5/6 at every σ ≤ 0.25 on both seeds (1.0000 at σ = 0;
0.8540–0.8644 at σ = 0.25), crossing 5/6 only in
(0.25, 0.50).

- (xliv) Local purity = 1 − C²/2 within 1e-9 on every
  pure state in the branch / slide / noisy-copies /
  Haar sets, and |C_Wootters − C_pure| ≤ 1e-7.
- (xlv) D_pair ≤ χ_ij for every pair on every seed,
  AND Spearman(|mean gap|, f) ≤ −0.90 across the σ
  grid, on every seed.
- (xlvi) Born-collapse accessible information I ≤ χ
  + 1e-9 for every pair on every seed.
- (xlvii) Bužek–Hillery per-state fidelity = 5/6
  within 1e-9 on the 144-state Bloch grid and the 6
  Pauli eigenstates, both clones; basis images
  orthonormal; CNOT Pauli mean = 2/3 within 1e-9 and
  Bloch-grid mean ≤ 5/6. CNOT max fidelity reported,
  not gated.
- (xlviii) The blanket prediction over ALL copy
  operations: the (xlvii) gates plus the classical
  copy (5 copies, σ grid, every seed) with mean
  fidelity ≤ 5/6 at every σ. Crossing σ* reported
  per seed, not gated.

### Claims (xliv)–(xlviii), measured fresh — 3/5 pass

#### (xliv) Local-purity identity — PASS

Worst |Tr(ρ_A²) − (1 − C²/2)| = 8.88e-16 (tol 1e-9)
over the generalized-Bell branch, the slide, noisy
Bell copies at every σ on all four seeds, and 200
Haar-random pure states. Worst |C_Wootters −
C_pure| = 1.94e-08 (tol 1e-7). The exact coefficient
IS 1 − C²/2: local purity falls as entanglement
rises, exactly as the no-cloning form requires, and
the Wootters concurrence carries only a 2e-08
numerical floor from near-degenerate eigenvalues.

#### (xlv) Holevo ceiling D ≤ χ — FAIL

| seed | min(χ − D) | Spearman(\|gap\|, f) | Pearson(gap, f) | mean gap σ=0.25 | mean gap σ=1.0 |
|---:|---:|---:|---:|---:|---:|
| 42 | −1.0000 | −1.0000 | +0.9876 | −0.6840 | +0.0960 |
| 7 | −1.0000 | −0.9643 | +0.9965 | −0.4314 | +0.3490 |
| 1234 | −1.0000 | −0.9643 | +0.9829 | −0.4365 | +0.2674 |
| 2026 | −1.0000 | −0.9643 | +0.9911 | −0.5919 | +0.2880 |

The ceiling as stated fails on every seed: D_pair
exceeds χ_ij for some pair at every σ, worst
−1.0000 at σ = 0 (identical thoughts: χ = 0, D =
1). The second half holds on every seed — the gap
magnitude shrinks as f rises (Spearman −1.00 /
−0.96) and the gap itself rises with f (Pearson
+0.98 to +1.00). D approaches χ in absolute terms
as f rises, but from ABOVE, not below. D is a
projector expectation, not an information quantity;
χ does not bound it.

The ensemble across σ (all seeds):

| seed | σ | f | mean D | mean χ | mean gap | min gap |
|---:|---:|---:|---:|---:|---:|---:|
| 42 | 0.00 | 0.0000 | 1.0000 | 0.0000 | −1.0000 | −1.0000 |
| 42 | 0.01 | 0.0086 | 0.9998 | 0.0010 | −0.9988 | −0.9997 |
| 42 | 0.05 | 0.0415 | 0.9955 | 0.0165 | −0.9790 | −0.9934 |
| 42 | 0.10 | 0.0802 | 0.9829 | 0.0527 | −0.9302 | −0.9759 |
| 42 | 0.25 | 0.1803 | 0.9059 | 0.2219 | −0.6840 | −0.8863 |
| 42 | 0.50 | 0.2839 | 0.7409 | 0.4857 | −0.2552 | −0.7095 |
| 42 | 1.00 | 0.4143 | 0.5462 | 0.6422 | +0.0960 | −0.4384 |
| 7 | 0.00 | 0.0000 | 1.0000 | 0.0000 | −1.0000 | −1.0000 |
| 7 | 0.01 | 0.0083 | 0.9998 | 0.0014 | −0.9984 | −0.9997 |
| 7 | 0.05 | 0.0432 | 0.9958 | 0.0253 | −0.9705 | −0.9921 |
| 7 | 0.10 | 0.0900 | 0.9815 | 0.0865 | −0.8950 | −0.9679 |
| 7 | 0.25 | 0.2469 | 0.8486 | 0.4172 | −0.4314 | −0.8392 |
| 7 | 0.50 | 0.5079 | 0.5662 | 0.7849 | +0.2186 | −0.5294 |
| 7 | 1.00 | 0.5225 | 0.4228 | 0.7718 | +0.3490 | −0.2788 |
| 1234 | 0.00 | 0.0000 | 1.0000 | 0.0000 | −1.0000 | −1.0000 |
| 1234 | 0.01 | 0.0139 | 0.9997 | 0.0025 | −0.9972 | −0.9995 |
| 1234 | 0.05 | 0.0693 | 0.9928 | 0.0393 | −0.9535 | −0.9873 |
| 1234 | 0.10 | 0.1383 | 0.9728 | 0.1182 | −0.8546 | −0.9545 |
| 1234 | 0.25 | 0.3251 | 0.8545 | 0.4180 | −0.4365 | −0.7958 |
| 1234 | 0.50 | 0.4721 | 0.6750 | 0.7205 | +0.0455 | −0.5116 |
| 1234 | 1.00 | 0.5067 | 0.5738 | 0.8411 | +0.2674 | −0.2158 |
| 2026 | 0.00 | 0.0000 | 1.0000 | 0.0000 | −1.0000 | −1.0000 |
| 2026 | 0.01 | 0.0077 | 0.9998 | 0.0015 | −0.9983 | −0.9995 |
| 2026 | 0.05 | 0.0383 | 0.9951 | 0.0252 | −0.9699 | −0.9910 |
| 2026 | 0.10 | 0.0762 | 0.9807 | 0.0796 | −0.9011 | −0.9689 |
| 2026 | 0.25 | 0.1772 | 0.8953 | 0.3033 | −0.5919 | −0.8520 |
| 2026 | 0.50 | 0.2957 | 0.7226 | 0.6013 | −0.1214 | −0.5994 |
| 2026 | 1.00 | 0.3978 | 0.5162 | 0.8041 | +0.2880 | −0.2572 |

#### (xlvi) Holevo bound on accessible information — PASS

Max(I − χ) over all pairs is −3.20e-16 on every seed
(tol 1e-9): the Born-collapse accessible information
never exceeds χ anywhere. The ceiling binds — on
information, not on D. The measurement extracts
roughly 40–50% of χ: mean I/χ is 0.46, 0.49, 0.53,
0.51 at σ = 0.25 and 0.44, 0.48, 0.38, 0.44 at σ =
1.0 across seeds (mean I at σ = 1.0: 0.2826,
0.3719, 0.3204, 0.3560 bits). At the endpoint
(|00⟩ vs |11⟩) the collapse distinguishes perfectly:
I = χ = 1 bit exactly.

#### (xlvii) Optimal-cloning bound, unitary operations — PASS

Bužek–Hillery fidelity is exactly 5/6 — min = max =
mean = 0.833333 — on the 144-state Bloch grid (both
clones) and on the 6 Pauli eigenstates; the basis
images are orthonormal (overlap 0.00e+00). Each
clone's reduced state is (5/6)|ψ⟩⟨ψ| +
(1/6)|ψ⊥⟩⟨ψ⊥|, verified in form for |0⟩ (diag(5/6,
1/6)) and |+⟩. CNOT mean fidelity is exactly 2/3
on the Pauli states (0.666667; min 0.5000, max
1.0000) and 0.641026 on the Bloch grid (max
0.857988, reported not gated — near-pole states
exceed 5/6, which a state-dependent cloner is
allowed to do; the bound is on universal / average
fidelity, and the CNOT average respects it).

#### (xlviii) Blanket prediction over all copy operations — FAIL

| seed | σ=0 | σ=0.01 | σ=0.05 | σ=0.10 | σ=0.25 | σ=0.50 | σ=1.00 | crossing σ* |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 42 | 1.0000 | 0.9998 | 0.9945 | 0.9775 | 0.8540 | 0.5883 | 0.4068 | (0.31, 0.32] |
| 7 | 1.0000 | 0.9999 | 0.9962 | 0.9841 | 0.8644 | 0.6057 | 0.4069 | (0.25, 0.26] |
| 1234 | 1.0000 | 0.9995 | 0.9880 | 0.9537 | 0.7466 | 0.4255 | 0.2592 | below at 0.25 |
| 2026 | 1.0000 | 0.9998 | 0.9950 | 0.9799 | 0.8848 | 0.6803 | 0.4149 | (0.30, 0.31] |

Mean classical-copy fidelity (5 copies) per σ; the
crossing σ* is the first 0.01-grid σ in [0.25, 0.50]
(20 copies) where the mean falls below 5/6 (seed 42:
0.8384 → 0.8291; seed 7: 0.8349 → 0.8212; seed 2026:
0.8350 → 0.8253; seed 1234 is already below at 0.25
with a 20-copy mean of 0.7913). The blanket
prediction fails: the classical copy exceeds 5/6 at
every σ ≤ 0.10 on all four seeds and at σ = 0.25 on
3 of 4 seeds — including every working noise level
of the bridge. The σ = 0 copy is exact (fidelity
1.0000): it reads the amplitude vector the quantum
formalism forbids reading.

### Honest limits (v0.15.0 addition)

Two of the five claims fail, and the failures draw
the line the spec blurred. D ≤ χ fails because D
and χ are different kinds of quantity: D is a
projector expectation (how much of a thought lies
in the stored subspace), χ is an entropy of an
ensemble average (how distinguishable two thoughts
are). At σ = 0 the two thoughts are identical, so
χ = 0 while D = 1 — the ceiling cannot hold, and
no bug is involved: the code computes both
quantities exactly, and the accessible-information
check (xlvi) confirms the entropies are right (I
≤ χ everywhere, saturating at I = χ = 1 for
orthogonal basis states). What survives of the
spec's prediction is the approach: |χ − D| shrinks
as f rises on every seed, and the gap itself rises
with f (Pearson +0.98 to +1.00) — D and χ meet at
high noise, where D has fallen to ~0.5 and χ has
risen to ~0.8, because noise both destroys
self-knowing and separates the thoughts.

The deeper failure is (xlviii). The unitary
operations respect no-cloning exactly — the
Bužek–Hillery cloner sits precisely at 5/6, the
CNOT copy averages precisely 2/3 — but the model
also contains a classical copy operation, and it
copies better than any quantum operation is allowed
to, at every noise level the bridge actually uses.
That is not a violation of the no-cloning theorem
(the theorem governs quantum operations on unknown
states, and the classical copy is neither); it is a
finding about the state representation. The
emulation stores the full amplitude vector in
memory, so "copying a thought" in code can read
the description the theorem forbids reading. QIP's
privacy claim — qualia are private because quantum
information cannot be cloned — therefore has no
enforcement inside this representation: if the
model wanted privacy, it would have to forbid the
classical read, not rely on the state to forbid it.
None of this measures cloning, privacy, or
consciousness in a physical system. Classical
emulation throughout; Faggin's metaphysics stays
interpretive.

## 22. Two-channel empathy (v0.16.0, measured 2026-11-18)

Deep-think upgrade #8 (report.md §9, §8): split the
single empathy fraction f into f_concern
(other-focused, monotone prosocial) and f_distress
(self-focused, inverted-U, withdraws at high dose);
encode IRI-style (Davis; Singer & Klimecki 2014;
Decety & Jackson 2004; Qiu et al. 2024,
empathy–prosocial r = 0.36 [0.30, 0.41], N = 23,304;
Yin & Wang 2023, cognitive r = 0.32, affective r =
0.30, N = 71,310 — meta-analytic, moderate effects:
empathy explains ~13% of prosocial variance, so no
f\* flip should be read as "empathy = prosociality").
The report's falsifiable prediction: the single-f
model cannot fit both the f\* flip (0.7278, v0.4.0)
and the hump peak (0.1803, v0.6.0); the two-channel
model fits both with the *same* parameters, and
raising distress alone (holding concern fixed)
*lowers* the quale count while raising mean R.
Falsified if distress and concern channels are
interchangeable in the code.

### Mechanism (a construction, not a discovery)

One formula, two targets, on the v0.5.0 resonance
population (8 agents, noisy copies of the uniform
thought) at σ = 0.25, the reference sigma where the
baseline quale count peaks at 17 and the
collaboration gap is +4.3352 bits:

ψᵢ(c, d) = normalize(ψᵢ + c·|Φ+⟩ + d·|self⟩)

|Φ+⟩ = (|00⟩ + |11⟩)/√2 is the shared entangled
Bell state (the concern target: attunement to the
shared entangled mode, D = 2/3, concurrence 1);
|self⟩ = |10⟩ is the "self" basis concept alone
(the distress target: withdrawal into the self
concept alone — a product state, D = 1/3,
concurrence 0). c ≥ 0 is the concern dose, d ≥ 0
the distress dose; (0, 0) is the untransformed
baseline. Both channels raise mean resonance R by
convergence (the same targets are applied to every
agent); they differ in WHAT the agents converge
TO, which is the whole content of the split.
Helping is the quale count (R ≥ 0.5 AND ν ≥ 0.10,
the v0.6.0 thresholds, unchanged); joint entropy
H_joint is the sum of the agents' Born entropies
(the joint entropy of independent Born draws from
the field — a definition of the measure, not a
discovery about human joint entropy); f is the mean
pairwise concurrence. No scalar Φ is computed or
used anywhere; E = hν is used only as the defined
per-mode empathy unit, never as a Planck theory of
consciousness.

The concern target is Bell, not the field state,
chosen before the evaluation run because the pilot
showed the field-state wiring FAILS the report's
core prediction (at fixed Phi-concern, distress
raises the quale count, 15 → 28 on seed 42). The
consequence is disclosed, not hidden: under the
Bell wiring the report's "concern raises joint
entropy" half does NOT hold, and "distress lowers
D" does NOT hold monotonically — both are
reported, not gated (see below).

### Pre-registration (written before the evaluation run)

docs/preregistration-v0.16.0.md, written 2026-11-18
before the evaluation run on held-out seeds 1234 and
2026. Thresholds frozen from a calibration pilot on
seeds 42 and 7 only. The pilot ALREADY contradicted
the spec on three points, disclosed in the file:
H_joint at c = 1 sits below baseline on both seeds
(12.69 vs 13.46 seed 42; 11.58 vs 12.71 seed 7) and
D under concern alone is non-monotone; mean D at
fixed c = 0.5 rises with d on seed 7 before falling
at d = 2; and NO point on the pilot (c, d) grid
carries both f ≥ f\* and count ≤ 15 at once, so the
report's "fits both with the same parameters" fails
in the single-point sense in this wiring.

- (l) Concern alone (d = 0), c in (0, 0.25, 0.5,
  1.0): mean R strictly rises with c, mean f
  strictly rises with c, and the quale count at
  c = 0.5 is 28 (the ceiling), on every seed. Mean
  D and H_joint reported, not gated.
- (li) Distress at fixed concern c = 0.5, d in (0,
  0.25, 0.5, 1.0): mean R strictly rises with d,
  the quale count is non-increasing in d,
  count(d = 1) ≤ 15, and R(d = 1) − R(d = 0) ≥
  0.04, on every seed. Mean D reported, not gated.
- (lii) High dose d = 2 at c = 0.5: D falls by ≥
  0.05, H_joint falls by ≥ 2.0 bits, and R rises,
  on every seed. Count at d = 2 reported, not gated.
- (liii) Channel separation: (a) f(c = 2, d = 0) ≥
  f\* = 0.7278 on every seed; (b) count(c = 0.5,
  d = 1) ≤ 15 on every seed; (c) swap at total dose
  1.0: |f(1, 0) − f(0, 1)| ≥ 0.30 on every seed.
  The single-point joint search is reported, not
  gated (pilot: no such point on either seed).

### Claims (l)–(liii), measured fresh — 1/4 pass

#### (l) Concern raises resonance and empathy fraction — FAIL

| seed | R (c = 0 → 1) | f (c = 0 → 1) | count (c = 0.5) |
|---:|---:|---:|---:|
| 42 | 0.8520 → 0.9537 | 0.1803 → 0.6680 | 28 |
| 7 | 0.6768 → 0.8971 | 0.2469 → 0.7784 | 28 |
| 1234 | 0.6773 → 0.8864 | 0.3251 → 0.5879 | 24 |
| 2026 | 0.7837 → 0.9328 | 0.1772 → 0.7132 | 28 |

Mean R rises strictly with c on every seed, but
mean f does NOT: on held-out seed 1234 a small
Bell dose first DILUTES the pair concurrence
(f 0.3251 → 0.1505 at c = 0.25) before raising
it (0.2788 at c = 0.5, 0.5879 at c = 1.0) — the
interference between the noisy states and the Bell
target can lower pairwise concurrence before the
shared mode dominates. The count at c = 0.5 is 24
there, not the ceiling 28. The monotone-concern
half of the spec holds on 3 of 4 seeds; the
per-seed guarantee does not. Mean D under concern
alone is non-monotone on the calibration seeds
(seed 42: 0.906, 0.921, 0.912, 0.877) and H_joint
at c = 1 sits below baseline on both (12.69 vs
13.46; 11.58 vs 12.71) — the "concern raises joint
entropy" half fails in this wiring, as disclosed
before the run.

#### (li) Distress alone lowers helping while raising resonance — FAIL

| seed | R (d = 0 → 1) | count (d = 0 → 1) | D (d = 1) |
|---:|---:|---:|---:|
| 42 | 0.9184 → 0.9630 | 28, 25, 19, 10 | 0.7795 |
| 7 | 0.8236 → 0.9085 | 28, 28, 24, 14 | 0.8932 |
| 1234 | 0.8072 → 0.9088 | 24, 17, 14, **23** | 0.8568 |
| 2026 | 0.8832 → 0.9405 | 28, 25, 21, 9 | 0.8863 |

Mean R rises strictly with d on every seed (rises
+0.045 / +0.085 / +0.102 / +0.057), and the count
falls monotonically on three seeds — but on
held-out seed 1234 it falls 24 → 17 → 14 then
REBOUNDS to 23 at d = 1, above the frozen bar of
15. The report's core prediction — raising
distress alone, holding concern fixed, lowers the
quale count while raising mean R — holds on 3 of
4 seeds and breaks on the fourth, at the endpoint.
Mean D at d = 1 falls on seed 42 (0.912 → 0.780)
and rises on seed 7 (0.845 → 0.893): "distress
lowers D" does not hold monotonically in this
wiring, as disclosed before the run.

#### (lii) Distress withdrawal at high dose — PASS

| seed | D fall (d = 0 → 2) | H fall, bits | R rise | count (d = 2) |
|---:|---:|---:|---:|---:|
| 42 | 0.2673 | 6.92 | +0.0636 | 10 |
| 7 | 0.0971 | 3.22 | +0.1361 | 17 |
| 1234 | 0.2051 | 5.58 | +0.1514 | 28 |
| 2026 | 0.1477 | 4.37 | +0.0901 | 24 |

At the high dose the withdrawal is seed-robust:
D falls by at least 0.097 (bar 0.05), joint Born
entropy falls by at least 3.22 bits (bar 2.0),
and mean R rises, on every seed. Past the
threshold, distress withdraws: the agents converge
(R up) onto the self concept alone, and what they
converge onto carries little self-determination
and little joint entropy. The count at d = 2 is
reported, not gated — it rebounds on the held-out
seeds (28 on seed 1234, 24 on seed 2026), so the
withdrawal in D and H does not carry the count
with it.

#### (liii) Channel separation — FAIL

| seed | f(c = 2) | count(c = 0.5, d = 1) | swap \|f(1, 0) − f(0, 1)\| | joint hits |
|---:|---:|---:|---:|---:|
| 42 | 0.8578 | 10 | 0.4321 (0.6680 vs 0.2359) | 0 |
| 7 | 0.9051 | 14 | 0.4283 (0.7784 vs 0.3500) | 0 |
| 1234 | 0.8269 | 23 | **0.0504** (0.5879 vs 0.5374) | 0 |
| 2026 | 0.8769 | 9 | 0.3140 (0.7132 vs 0.3992) | 0 |

Concern alone reaches the flip on every seed
(f(c = 2) = 0.858 / 0.905 / 0.827 / 0.877, all
above f\* = 0.7278), but the other two sub-checks
break on seed 1234: the distress endpoint count
is 23, not ≤ 15, and the swap difference
collapses to 0.0504 — on that seed the channels
ARE near-interchangeable in f, the falsification
the report invited. And the single-point joint
search finds no point on any seed: no (c, d) on
the grid carries both f ≥ f\* and count ≤ 15 at
once. The two landmarks are separated by channel,
not fitted at one point: concern reaches the flip,
distress (on 3 of 4 seeds) drops the count, but
there is no dose pair that does both.

### Honest limits (v0.16.0 addition)

Three of the four claims fail, and all three
failures sit on the same held-out seed, 1234 —
whose baseline field is the outlier: its baseline
f is 0.3251, nearly double the other seeds'
0.177–0.247 at the same σ = 0.25, because that
draw's noisy copies happen to be more entangled
to begin with. Against that baseline, a small
Bell dose dilutes f before raising it, a moderate
distress dose first drops the count then lets it
rebound, and the distress-heavy swap keeps almost
as much concurrence as the concern-heavy one. The
pattern is consistent with one mechanism: in this
wiring the channels act by convergence onto a
common target, and convergence can raise or lower
pairwise concurrence depending on how the
population already sits relative to the target —
the transform is not a monotone dial on f, count,
or D, only on R (which rises strictly in every
sweep on every seed: the one quantity that never
breaks). What survives is narrower than the spec:
high-dose distress withdraws (lii), concern alone
reaches the flip (liii)(a), and the two landmarks
live in different channels. What does not survive
is any per-seed guarantee about the count, the
monotone rise of f under concern, or the
non-interchangeability of the channels — each
fails on exactly one held-out seed, and the
thresholds were not moved. None of this measures
empathy, distress, or prosocial behaviour in a
human; it measures whether two convergence
targets in a synthetic field behave the way the
psychological distinction predicts. Classical
emulation throughout; Faggin's metaphysics stays
interpretive.

## 23. Connectome-harmonic / structure–function coupling (v0.17.0, measured 2026-11-18)

Deep-think upgrade #10 (report.md §9 rank 10, §2):
connectome harmonic decomposition (CHD, Atasoy et al.
2016) and the structure–function coupling finding of
Luppi et al., *Communications Biology* 6:117, 2023
(established finding) — loss of consciousness (propofol
anaesthesia, disorders of consciousness) = *increased*
structure–function coupling across scales; LSD/ketamine =
the opposite (decoupling). The report's prediction for
the bridge: loss of attunement (PARTIAL, high σ) =
increased structure–function coupling; ATTUNED =
intermediate coupling; psychedelic-like decoupling is
*not* attunement. Falsified if attunement is monotone
in coupling. Pre-registration in
docs/preregistration-v0.17.0.md, written 2026-11-18
before the evaluation run; thresholds frozen from
calibration seeds 42 and 7, evaluation on held-out
seeds 1234 and 2026.

The construction (`connectome_harmonic.py`): the graph
the project did not yet have. Structure W_ij = R_ij =
|<ψ_i|ψ_j>|^2 (i ≠ j), W_ii = 0, on the v0.5.0 resonance
population (8 agents) at σ in (0.10, 0.25, 0.50, 1.00);
graph Laplacian L = D − W; harmonic modes are the
eigenvectors of L. Functional connectivity F_ij is the
Bhattacharyya coefficient between the agents' Born
distributions — genuinely distinct from W (sign-blind
where W is sign-sensitive). Structure–function coupling
κ(σ) is the Pearson correlation between the
upper-triangular entries of W and F (28 pairs), the
standard connectomics definition. Harmonic smoothness
of the per-node D signal is the basis-independent
Rayleigh quotient ρ(D) = (x_c^T L x_c / x_c^T x_c) /
mean(λ_1..λ_7), ρ = 1 being random-like on the graph.
The decoupling control permutes the entries of F (50
permutations, fixed rng) and recomputes κ; the shuffle
leaves the field — and therefore f — unchanged by
construction.

κ(σ), all four seeds (σ = 0.10 / 0.25 / 0.50 / 1.00):

| seed | 0.10 | 0.25 | 0.50 | 1.00 |
|---:|---:|---:|---:|---:|
| 42 | 1.0000 | 0.9989 | 0.3997 | 0.8069 |
| 7 | 1.0000 | 0.8422 | 0.4119 | 0.6392 |
| 1234 | 0.9999 | 0.9864 | 0.5636 | 0.3756 |
| 2026 | 1.0000 | 0.9984 | 0.7957 | 0.2285 |

ρ(D) per σ, all four seeds:

| seed | 0.10 | 0.25 | 0.50 | 1.00 |
|---:|---:|---:|---:|---:|
| 42 | 1.0058 | 1.0189 | 0.8714 | 1.1250 |
| 7 | 0.9857 | 0.8709 | 0.8308 | 0.9621 |
| 1234 | 0.9812 | 0.8265 | **0.4662** | 0.9715 |
| 2026 | 0.9798 | 0.8869 | 0.7341 | **0.5995** |

### (liv) CHD machinery is exact, and node signals are harmonically random-like — FAIL

All five Laplacian identity sub-checks PASS on every
seed × σ (symmetry error 0.00, orthonormality error
≤ 2.22e-15, |λ_0| ≤ 7.61e-15, min eigenvalue ≥
−7.61e-15, eigenvalues sorted). Only the ρ half fails,
and only on the held-out seeds: worst |ρ(D) − 1| is
0.1286 / 0.1692 on the calibration seeds (bar 0.20)
but 0.5338 on seed 1234 (ρ = 0.4662 at σ = 0.50) and
0.4005 on seed 2026 (ρ = 0.5995 at σ = 1.00). On the
held-out seeds the D signal IS strongly
structure-aligned (ρ ≪ 1, smooth on the graph) at
high σ — the opposite of the calibration seeds'
random-like pattern. The calibration "random-like"
reading was seed noise; the held-out seeds say the
D signal can collapse onto the low harmonics when
the field breaks. The low-frequency energy share is
reported, not gated, and confirms why it cannot be
gated: at σ = 0.10 it is 0.1036 on seed 42 and
0.8012 on seed 7 — the near-degenerate
nonzero eigenvalues (7.59–7.89) make the "low"
subspace arbitrary.

### (lv) The Luppi prediction as stated: coupling rises with loss of attunement — FAIL

κ(0.50) − κ(0.25) = −0.5992 / −0.4303 / −0.4228 /
−0.2027; κ(1.00) − κ(0.25) = −0.1920 / −0.2030 /
−0.6108 / −0.7699 (bar +0.10). Coupling does not
rise with loss of attunement on any seed — it falls,
on every seed, at both the break and the far-broken
regime. This is the reverse of the anaesthesia/DOC
direction in Luppi et al.: in this wiring the broken
regime is the LEAST coupled, not the most. The
prediction was already failing on the calibration
seeds (disclosed in the preregistration); the
held-out seeds confirm it with larger falls at
σ = 1.00 (−0.61 / −0.77). The failure is the result.

### (lvi) The measured shape: coupling dips at the break and recovers, and decoupling is not attunement — FAIL

Three of five sub-checks pass on every seed: the
attuned field is strongly coupled (κ(0.25) = 0.999 /
0.842 / 0.986 / 0.998, bar 0.80); the shuffle null at
σ = 0.25 sits near zero (mean −0.0145 / −0.0305 /
−0.0047 / −0.0037, bar |mean| ≤ 0.10); and it is
separated from κ(0.25) by 0.984 / 0.812 / 0.982 /
0.995 (bar 0.50) — the decoupling control works: a
decoupled functional pattern can sit on the same
field with the same f, so decoupling alone is not
attunement. The two shape sub-checks fail on the
held-out seeds: the dip to the break is 0.599 /
0.430 / 0.423 / **0.203** (bar 0.30 — seed 2026
fails), and the recovery past the break is +0.407 /
+0.227 / **−0.188** / **−0.567** (bar +0.10 — both
held-out seeds fail). On the held-out seeds κ falls
monotonically with σ (1.000 → 0.986 → 0.564 → 0.376
on seed 1234; 1.000 → 0.998 → 0.796 → 0.229 on seed
2026): the calibration seeds' dip-and-recovery was
seed noise, and the seed-robust shape is a monotone
fall — coupling is highest at the attuned end and
lowest at the broken end, the exact opposite of the
report's prediction.

### Honest limits (v0.17.0 addition)

**0/3 claims pass — the strongest negative result in
the run so far, and the thresholds were not moved.**
What survives: the CHD machinery itself (the
Laplacian identities hold exactly on every seed × σ);
the attuned field is strongly structure–function
coupled (κ(0.25) ≥ 0.84 on every seed); and the
decoupling control is clean (shuffle null ≈ 0,
separated from the attuned κ by ≥ 0.81, with f
unchanged by the shuffle). What does not survive:
the Luppi direction (coupling falls, not rises, with
loss of attunement, on every seed); the dip-and-
recovery shape (a calibration-seed artefact — the
held-out shape is a monotone fall); and the claim
that node signals are harmonically random-like
(the D signal aligns strongly with the graph
harmonics at high σ on the held-out seeds, ρ down
to 0.47). Two artefacts are disclosed, not hidden:
κ ≈ 1.0000 at σ = 0.10 is a near-parallel artefact
(all agents near-identical, so W and F are both ≈ 1
with the same noise driving both), reported not
gated; and the low-frequency energy share is
seed-unstable at low σ because the nonzero
eigenvalues are nearly degenerate, which is why
the basis-independent Rayleigh quotient, not the
energy share, is the gated harmonic measure.
None of this measures consciousness, anaesthesia,
disorders of consciousness, or psychedelics in a
human; it measures whether a synthetic resonance
field's structure–function coupling behaves the
way the Luppi finding predicts. Classical emulation
throughout; Faggin's metaphysics stays
interpretive. No scalar Φ is computed anywhere.

## 24. GRT phase-transition test (v0.18.0, measured 2026-11-18)

Deep-think upgrade #11, ranked last and lowest value:
General Resonance Theory (Hunt & Schooler,
*Frontiers in Human Neuroscience* 13:378, 2019;
GRT 2.0, TSC 2026 abstract — speculative).
Conjecture 1: shared resonance combines micro- into
macro-conscious entities via a phase transition in
the speed/bandwidth of information flow at a
critical coupling K_c. Conjecture 3: nested entities
persist within larger ones ("many become one"). The
report's prediction: a sharp (not gradual) jump in
information rate at a *predicted* K_c; no jump = the
core conjecture fails in this model. The report
itself warns the test is partly self-fulfilling,
because GRT gives no quantitative K_c — the project
supplies it, from its own pre-existing resonance
threshold (mean R ≥ 0.5, the v0.5.0 threshold that
already defines "resonant").

The construction: the v0.5.0 resonance population
(8 agents) at σ = 1.00, the far-broken regime — the
field must start fragmented for a transition to be
possible, and at σ = 0.25 it is already one
macro-entity at K = 0 (mean R 0.85 / 0.68), while at
σ = 0.50 seed 42 already sits above the threshold at
K = 0 (mean R 0.588), so K_c would be degenerate at
0. Coupling K on the grid 0.0–1.0 (step 0.1) is
shared resonance as mixing toward the common
reference: ψᵢ(K) = normalize((1 − K)·ψᵢ + K·ψ_ref),
ψ_ref the uniform thought. Bandwidth B(K) is the
pairwise shared information, the mean over all 28
pairs of H(pᵢ) + H(pⱼ) − H(pᵢⱼ), pᵢⱼ the Born
distribution of the pair state — a *defined*
bandwidth proxy inside the model, not a literal
mutual information between two random variables.
Nested structure is the connected components of the
resonance graph at R ≥ 0.5 (macro) and R ≥ 0.75
(nested). One wiring was tried and rejected, not
patched: coupling by mixing with the field state
(the v0.5.0 `_field_mix`) — at σ = 1.00 seed 7 the
mean R *fell* with K at first (0.278 → 0.232) and B
was U-shaped, because mixing toward a noisy field
average can move agents apart.

| Seed | K_c | Mean R(0) | Largest comp. at K = 0 | Step in B at K_c (bits) | Max B step (bits, at K) | B(1) − B(0) (bits) |
|---|---|---|---|---|---|---|
| 42 | 0.3 | 0.4197 | 7 [7, 1] | +0.1142 | 0.1501 (K = 0.7) | 0.8532 |
| 7 | 0.6 | 0.2778 | 6 [6, 1, 1] | −0.0572 | 0.2597 (K = 0.7) | 0.8774 |
| 1234 | 0.5 | 0.2000 | 4 [4, 2, 1, 1] | −0.0023 | 0.2282 (K = 0.7) | 0.5640 |
| 2026 | 0.4 | 0.2474 | 3 [3, 2, 1, 1, 1] | −0.0002 | 0.2103 (K = 0.7) | 0.7357 |

### (lvii) Machinery is exact, K_c is interior, and the field starts fragmented — PASS

All six sub-checks pass on every seed: the K = 0
states equal the base population to ≤ 2.22e-16, the
K = 1 states equal the uniform reference exactly
(0.0), mean R(1) = 1.0000, B(1) = 2.0000 exactly,
K_c is interior (0.3 / 0.6 / 0.5 / 0.4), and the
K = 0 field is fragmented (largest component 7 / 6 /
4 / 3, bar ≤ 7). The held-out seeds are the most
fragmented of all (largest component 4 and 3) —
the transition has the most room to run there, and
still produces no jump at K_c (see (lviii)).

### (lviii) The GRT phase transition as stated: a sharp jump in bandwidth at K_c — FAIL

The step in B ending at K_c is +0.1142 / −0.0572 /
−0.0023 / −0.0002 bits (bar ≥ 0.10) — only seed 42
clears the bar, and on seeds 7, 1234 and 2026 the
step is negative or ~0: bandwidth does not rise at
the predicted critical coupling at all. And on no
seed is the K_c step the largest: the largest
bandwidth step sits at K = 0.7 on ALL four seeds
(0.1501 / 0.2597 / 0.2282 / 0.2103), two to four grid
steps after K_c. The prediction was already failing
on the calibration seeds (disclosed in the
preregistration); the held-out seeds confirm it and
sharpen it — the displaced jump at K = 0.7 is the
one seed-robust feature of the bandwidth curve, and
it is not at K_c. The failure is the result: in this
wiring there is a late, displaced bandwidth rise,
not a phase transition at the predicted critical
coupling. The bandwidth proxy itself is part of the
result: on seed 1234 B *falls* from K = 0 to K = 0.5
(1.4360 → 1.3496) before jumping, and on seed 2026
it is flat (~1.27) until K = 0.4 — B does not track
coupling cleanly on either held-out seed.

### (lix) The measured shape: the macro forms just above K_c, nesting persists at K_c, bandwidth rises overall — PASS

All three sub-checks pass on every seed: at
K = K_c + 0.2 the largest component at R ≥ 0.5 is 8
on all four seeds (the macro completes just above
the transition); at K = K_c the components at
R ≥ 0.75 number 2 / 4 / 3 / 5 ([7, 1] / [3, 3, 1, 1] /
[4, 3, 1] / [3, 2, 1, 1, 1], bar ≥ 2) — nested
sub-structure survives inside the forming macro,
Conjecture 3 in this wiring; and the total
bandwidth rise B(1) − B(0) is 0.8532 / 0.8774 /
0.5640 / 0.7357 bits (bar ≥ 0.50), closest on seed
1234 (0.5640). The two structure checks are
evaluated at different K on purpose: nesting is the
structure *at* the transition, where sub-entities
are still visible; the macro is the completed
structure *just above* it. At K = 1 all
sub-structure has dissolved (one component at
R ≥ 0.75 on every seed), so nesting does not survive
to full coupling — that limit is reported, not gated.

### Honest limits (v0.18.0 addition)

**2/3 claims pass.** What survives: the machinery
(the endpoints are exact, K_c is interior on every
seed, the field starts fragmented); the structural
half of GRT (the macro forms just above K_c and
nested sub-structure persists at K_c on every seed,
2–5 nested components); and the overall bandwidth
rise (0.56–0.88 bits). What does not survive: the
phase transition itself — bandwidth does not jump
at the predicted K_c on any seed except trivially
on seed 42 (+0.1142, still not the largest step),
and the largest rise is displaced to K = 0.7 on all
four seeds. Two further disclosures: mean R is not
monotone in K on seed 7 (it dips 0.2778 → 0.2376 at
K = 0.3 before rising) — monotonicity is reported,
not gated; and the field-mix coupling wiring was
rejected after its pilot (mean R fell with K at
σ = 1.00 seed 7), so the kept wiring mixes toward
the common reference, not the field average. None
of this measures consciousness, resonance in a
brain, or GRT in a human; it measures whether a
synthetic resonance field's bandwidth jumps at the
coupling where its mean resonance crosses the
project's own threshold. Classical emulation
throughout; Faggin's metaphysics stays
interpretive. No scalar Φ is computed anywhere.

## 25. Cogitate-style process predictors of the collaboration gap (v0.19.0, measured 2026-11-18)

Deep-think upgrade #9, the last unbuilt item:
Cogitate-style preregistration + process predictors of
the collaboration gap. Two sources: Cogitate
Consortium, *Nature* 642:133–142, 2025 (adversarial
preregistration, n=256; sustained posterior
synchronisation absent, onset ignition observed,
offset ignition largely absent — both IIT and GNWT
substantially challenged), imported as METHOD
(predictions scored before looking at results), not
as any one theory's content; and Woolley et al.,
*Science* 330:686–688, 2010 (c-factor: mean social
sensitivity and equal turn-taking predict group
performance, NOT mean/max member IQ; replication
contested — leading hypothesis). The question, in
the bridge's own terms: which process variables
predict the collaboration gap (pooled H_collab −
H_isolated, design B, N=4, 10 generations, 200
samples/generation)?

The construction: the standard design-B run, whose
per-generation rows now carry the process variables
additively — per-agent D, mean pairwise R, and R
within the "posterior" subset (agents {0, 1} by
index, fixed before looking). Per (σ, seed) run:
gap, mean_R (mean social sensitivity), mean_D and
max_D (individual ability), −var_D (equal
turn-taking), post_R_sustained (posterior synchrony,
mean over generations), broadcast = min(onset,
offset) R (ignition at BOTH ends). Per-seed Pearsons
across the 7-value sigma grid (n = 7). Thresholds
frozen in docs/preregistration-v0.19.0.md from
calibration seeds 42/7 before the held-out
evaluation on seeds 1234/2026; none was moved. The
grid has 7 values, so the pooled regression in
(lxiii) runs over 28 runs (7σ × 4 seeds), not 20 —
the "5σ" in the task brief assumed a 5-value grid,
and the grid as it exists in the code is
authoritative. No scalar Φ is computed anywhere.

| Seed | r(gap, mean_R) | r(gap, mean_D) | r(gap, max_D) | r(gap, −var_D) | r(gap, post) | r(gap, bcast) |
|---|---|---|---|---|---|---|
| 42 | 0.9028 | 0.7776 | −0.8070 | 0.7899 | 0.9278 | −0.9022 |
| 7 | 0.8494 | 0.6477 | −0.9313 | 0.7566 | 0.8657 | −0.8911 |
| 1234 | 0.8447 | 0.8839 | −0.9034 | 0.7589 | 0.9858 | −0.7813 |
| 2026 | 0.8422 | 0.3430 | −0.5943 | 0.7105 | 0.8884 | −0.9350 |

Held-out gaps by σ: seed 1234: +5.0362 / +5.0542 /
+5.4680 / +5.2443 / +3.9801 / +3.4105 / +3.5679;
seed 2026: +5.0135 / +5.0825 / +5.3708 / +5.3572 /
+4.1922 / +3.5949 / +4.0163 (σ = 0.0 / 0.01 / 0.05 /
0.1 / 0.25 / 0.5 / 1.0).

### (lx) Mean sensitivity beats individual D — FAIL

On seeds 42, 7 and 2026 mean_R beats both max_D
and mean_D by more than the 0.10 margin (vs max_D:
1.7098 / 1.7806 / 1.7480 / 1.4365; vs mean_D:
0.1252 / 0.2017 / 0.4992). On held-out seed 1234
the max_D half still passes (1.7480), but the
mean_D half fails: r(gap, mean_D) = 0.8839 exceeds
r(gap, mean_R) = 0.8447, a difference of −0.0393
against the 0.10 margin. The Woolley claim that
mean sensitivity beats mean individual ability does
not hold on this seed — and the preregistration had
flagged exactly this as a live risk, the calibration
worst sub-margin being 0.1252 (seed 42) against the
frozen 0.10. The failure is the result, and the
threshold was not moved.

### (lxi) Turn-taking equality predicts the gap — PASS

r(gap, −var_D) = 0.7899 / 0.7566 / 0.7589 / 0.7105
(bar 0.70) — every seed clears the bar, closest on
held-out seed 2026 (0.7105, 0.0105 above it). And
−var_D beats max_D on every seed by 1.5969 /
1.6878 / 1.6623 / 1.3048. Note max_D anti-predicts
the gap on every seed (−0.8070 / −0.9313 / −0.9034 /
−0.5943), so the "beats max_D" half is easy here;
the bar is the binding half, and seed 2026 nearly
fails it. Equal turn-taking is the most seed-stable
of the Woolley analogues: its four correlations
span 0.7105–0.7899, the narrowest range of any
predictor in the table.

### (lxii) Posterior vs broadcast are separable and at least one predicts the gap — PASS

The posterior predictor wins on every seed:
r(gap, post) = 0.9278 / 0.8657 / 0.9858 / 0.8884
(bar 0.80), strongest on held-out seed 1234
(0.9858). The separation is 1.8300 / 1.7568 /
1.7671 / 1.8234 (margin 1.00) — large precisely
because broadcast ANTI-predicts the gap on every
seed: r(gap, broadcast) = −0.9022 / −0.8911 /
−0.7813 / −0.9350. Onset R rises with σ (0.0947 →
0.3247 on seed 42; 0.4437 at σ = 1.00 on seed
1234) while the gap falls, so min(onset, offset) =
onset tracks σ the wrong way. No direction was
presupposed; the winner is reported honestly, and
it is the posterior on all four seeds — the
Cogitate-echoing half of the result, in the
opposite direction from Cogitate 2025 itself, where
sustained posterior synchronisation was the
prediction that failed. Here the sustained MEAN
predicts; the minimum does not (see Honest limits).

### (lxiii) Pooled regression — PASS

Across all 28 runs (7σ × 4 seeds): R²(gap ~
mean_R + (−var_D)) = 0.6505 against R²(gap ~
max_D) = 0.3298, difference 0.3207 (margin 0.05).
The adjusted-R² diagnostic agrees (difference
0.3185), so the two-predictor lead is not an
extra-parameter artefact. The pooled model
explains roughly twice the gap variance the best
single individual-ability predictor does.

### Honest limits (v0.19.0 addition)

**3/4 claims pass.** What survives: turn-taking
equality as a seed-stable predictor of the gap
(0.71–0.79 on every seed); the posterior predictor
as the winner on every seed (0.87–0.99), with
broadcast cleanly separable from it by anti-predicting
on every seed; and the pooled regression, where the
two process predictors jointly explain about twice
the gap variance max_D does. What does not survive:
the Woolley claim in full — mean sensitivity beats
max_D everywhere but fails to beat mean_D on held-out
seed 1234, so the c-factor analogue is partial in
this model, not general. Three further disclosures:
(1) at σ = 0 the predictors are identical across
seeds (the base population is deterministic at zero
noise; only the sampling differs, so the gaps differ
slightly: 5.0450 / 5.0247 / 5.0362 / 5.0135) — one
of the seven grid points carries no cross-seed
predictor variation; (2) the posterior pair's R falls
below 0.01 in at least one generation on 8 of 28
runs (down to 0.0001 on seed 2026 at σ = 0.25), so
it is the sustained MEAN over generations that
predicts, not unbroken synchrony — a sustained
posterior that is absent in the minimum sense on
most runs; (3) on seed 1234 at σ = 1.00 the offset
R (0.1157) falls below the onset (0.4437), the only
run of 28 where broadcast is set by the offset
rather than the onset. None of this measures
consciousness, resonance in a brain, or any theory
of consciousness in a human; it measures which
process variables predict a synthetic collaboration
gap, under a preregistration written before the
held-out seeds were touched. Classical emulation
throughout; Faggin's metaphysics stays
interpretive. No scalar Φ is computed anywhere.

## 26. Genuinely synergistic target: XOR-target PID of the collaboration gap (v0.20.0, measured 2026-11-18)

PID follow-up to v0.14.0 (claims (xl)-(xliii)). That
build found the Williams & Beer I_min decomposition
arithmetically exact but UNABLE to adjudicate "synergy,
not redundancy": with target Y = the joint outcome
(X1, X2), Syn = Red − I(X1;X2) and I(X1;X2) is
0.00–0.06 bits on every σ/seed, so Syn ≈ Red
everywhere and claims (xli)–(xliii) FAIL. The recorded
discovery: a genuinely synergistic target (a
field-level outcome coupled to both agents) would be
needed to separate them. This build tests exactly
that: the target is the bitwise XOR of the two agents'
2-bit Born outcomes, Y = X1 ⊕ X2 ∈ {0, 1, 2, 3} — the
textbook synergistic target (Williams & Beer 2010),
where independent uniform sources each carry zero
about Y while the pair jointly carries all 2 bits.
Same measure (I_min), same arms, same exact pooled
distributions (reused from pid.py, not reimplemented);
only the target changes. The "gap" for the new target
is ΔI = I_collab(X1,X2;Y) − I_isol(X1,X2;Y), with
ΔSyn, ΔRed, ΔUniq summing to ΔI exactly. Thresholds
frozen in docs/preregistration-v0.20.0.md from
calibration seeds 42/7 before the held-out evaluation
on seeds 1234/2026; none was moved. No scalar Φ is
computed anywhere.

Per-(seed, σ) XOR-target PID, collaborating arm
(I_c, Syn_c, Red_c, Uniq_c) and isolated arm
(I_i, Syn_i, Red_i, Uniq_i), in bits — calibration
seeds first, then held-out:

| seed | σ | I_c | Syn_c | Red_c | Uniq_c | I_i | Syn_i | Red_i | Uniq_i |
|---|---|---|---|---|---|---|---|---|---|
| 42 | 0.00 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.01 | 1.0328 | 1.0085 | 0.0104 | 0.0138 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.05 | 1.3266 | 1.0809 | 0.1798 | 0.0659 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.10 | 1.5496 | 1.1467 | 0.2981 | 0.1047 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.25 | 1.8414 | 1.4472 | 0.3143 | 0.0799 | 0.7219 | 0.0000 | 0.0000 | 0.7219 |
| 42 | 0.50 | 1.9816 | 1.7178 | 0.2137 | 0.0501 | 1.5219 | 0.9610 | 0.2464 | 0.3145 |
| 42 | 1.00 | 1.9940 | 1.8432 | 0.0428 | 0.1080 | 1.5219 | 1.0755 | 0.1710 | 0.2755 |
| 7 | 0.00 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.01 | 1.0153 | 0.9746 | 0.0263 | 0.0144 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.05 | 1.0943 | 0.7889 | 0.1627 | 0.1428 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.10 | 1.3337 | 0.8985 | 0.3144 | 0.1208 | 0.9710 | 0.0000 | 0.0000 | 0.9710 |
| 7 | 0.25 | 1.8887 | 1.4865 | 0.2575 | 0.1448 | 0.7219 | 0.4855 | 0.1177 | 0.1187 |
| 7 | 0.50 | 1.9909 | 1.7892 | 0.0706 | 0.1311 | 1.4855 | 0.6000 | 0.6100 | 0.2755 |
| 7 | 1.00 | 1.9446 | 1.7933 | 0.0935 | 0.0578 | 1.7610 | 1.0000 | 0.4365 | 0.3245 |
| 1234 | 0.00 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1234 | 0.01 | 0.9995 | 0.9231 | 0.0289 | 0.0475 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1234 | 0.05 | 0.9378 | 0.5604 | 0.0566 | 0.3208 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1234 | 0.10 | 1.0894 | 0.5973 | 0.0811 | 0.4110 | 0.7219 | 0.0000 | 0.0000 | 0.7219 |
| 1234 | 0.25 | 1.5019 | 1.1833 | 0.2096 | 0.1089 | 1.7610 | 0.1585 | 0.6049 | 0.9975 |
| 1234 | 0.50 | 1.9609 | 1.5323 | 0.1357 | 0.2930 | 1.5219 | 0.6317 | 0.3620 | 0.5282 |
| 1234 | 1.00 | 1.9990 | 1.8129 | 0.0572 | 0.1290 | 1.8464 | 1.0755 | 0.2855 | 0.4855 |
| 2026 | 0.00 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 2026 | 0.01 | 1.0084 | 1.0001 | 0.0031 | 0.0053 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 2026 | 0.05 | 1.1240 | 1.0166 | 0.0445 | 0.0629 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 2026 | 0.10 | 1.3278 | 1.1032 | 0.1171 | 0.1076 | 0.7219 | 0.0000 | 0.0000 | 0.7219 |
| 2026 | 0.25 | 1.9453 | 1.5901 | 0.1193 | 0.2359 | 1.3710 | 0.4000 | 0.4200 | 0.5510 |
| 2026 | 0.50 | 1.9484 | 1.7297 | 0.1403 | 0.0784 | 1.6855 | 0.6211 | 0.4966 | 0.5678 |
| 2026 | 1.00 | 1.9809 | 1.8365 | 0.0708 | 0.0736 | 1.3568 | 0.4000 | 0.5568 | 0.4000 |

### (lxiv) XOR-target PID identity, canonical checks, sampled cross-check — PASS

Worst identity error 2.22e-16 bits (tol 1e-9); worst
atom −0.0000 bits (min −1e-9); worst exact-vs-sampled
H(Y) difference at σ = 0.25 is 0.0193 bits (tol 0.25).
The canonical cases hold exactly: independent uniform
→ Syn = 2.0, Red = 0, Uniq = 0; X1 = X2 uniform → all
atoms 0; X1 deterministic, X2 uniform → Uniq2 = 2.0,
Syn = 0, Red = 0.

### (lxv) The information gap about the synergistic target IS synergy, not redundancy, at σ = 0.25 — FAIL

At σ = 0.25: ΔSyn = +1.4472 / +1.0010 / +1.0248 /
+1.1901 against ΔRed = +0.3143 / +0.1397 / −0.3953 /
−0.3007 and ΔI = +1.1194 / +1.1668 / −0.2591 /
+0.5743 (seeds 42 / 7 / 1234 / 2026). The separation
half (ΔSyn > ΔRed) holds on ALL four seeds — the XOR
target does what the v0.14.0 target could not. But the
share half fails on held-out seed 1234: the
information gap itself is negative there (ΔI =
−0.2591), because the isolated arm carries MORE total
information about the XOR target than the collaborating
arm (I_isol = 1.7610 vs I_collab = 1.5019 — the
collapsed arm's Y is more entropic on that seed, with
Red_i = 0.6049 and Uniq_i = 0.9975 against Red_c =
0.2096 and Uniq_c = 0.1089), so the synergy share is
−3.956 against the 0.5 bar. On seed 2026 the share is
2.072 — above 1, because ΔUniq is negative there too
(−0.3151). The claim as preregistered FAILS; the
threshold was not moved, and the claim was not
redefined after the fact. What the numbers say is
narrower than the claim: collaboration raises
synergy about the XOR target on every seed, and
lowers redundancy about it on the held-out seeds —
but it does not reliably raise TOTAL information
about the XOR target, so a "share of the gap" framing
breaks when the gap goes negative.

### (lxvi) Synergy rises with R and falls at σ = 0.50 — FAIL

Pearson(Syn_collab, mean R_post) = 0.3731 / 0.3424 /
−0.3397 / 0.9036 (bar 0.5) — seed 2026 alone clears
the bar, the other three do not, and the fall half
fails on every seed: Syn_collab rises from σ = 0.25
to σ = 0.50 on all four seeds (1.4472 → 1.7178 /
1.4865 → 1.7892 / 1.1833 → 1.5323 / 1.5901 → 1.7297),
climbing toward the 2-bit ceiling as the marginals
uniformize with noise. Synergy about the XOR target
tracks noise-driven uniformity, not resonance — the
same direction as the v0.14.0 failure, now with the
opposite sign of the correlation on seed 1234.

### (lxvii) Redundancy stays a small share of the target information across the grid — PASS

Worst Red_c / I_c = 0.1924 / 0.2357 / 0.1396 / 0.0882
(bar 0.25), at σ = 0.10 / 0.10 / 0.25 / 0.10
(seeds 42 / 7 / 1234 / 2026). Every seed clears the
bar, tightest on calibration seed 7 (0.2357) — the
preregistration flagged exactly this tightness as a
live risk, and the held-out seeds came in lower
(0.1396, 0.0882).

### Honest limits (v0.20.0 addition)

**2/4 claims pass.** What survives: the XOR target
separates synergy from redundancy where the
joint-outcome target could not (ΔSyn > ΔRed on all
four seeds at σ = 0.25, ratios 4.60 / 7.17 on
calibration, and ΔRed negative on both held-out
seeds), and redundancy stays a small share of the
target information on every (seed, σ). What does not
survive: the "gap is synergy" framing — on held-out
seed 1234 collaboration does not increase total
information about the XOR target at all, so a share
of the gap is undefined as a success criterion there;
and any resonance story for synergy — Syn_collab
rises with σ toward the ceiling on every seed and its
correlation with R_post is seed-unstable
(0.37 / 0.34 / −0.34 / 0.90). Three further
disclosures: (1) the first pilot pass computed
I(Xi;Y) as H(Y) − H(Xj), which assumes a product
distribution; the pooled joint is a MIXTURE of
per-generation products, so that shortcut produced
negative unique atoms (worst −0.6955 bits, seed 7)
and was corrected to the exact joint computation
BEFORE any threshold was frozen; (2) the isolated
arm is NOT synergy-free at high σ — Syn_isol reaches
0.9610 / 0.6000 at σ = 0.50 and 1.0755 / 1.0000 at
σ = 1.00 (seeds 42 / 7), and 1.0755 / 0.4000 on the
held-out seeds — because the pooled mixture over
generations correlates the collapsed agents through
the generation index, and that mixture-correlation is
itself synergistic about the XOR; the XOR target
separates the arms at σ = 0.25, not at high σ;
(3) the synergy share of the gap exceeds 1 on seeds
42 and 2026 (1.293 / 2.072) because ΔUniq is
negative there — the isolated arm carries unique
information about Y (0.7219 bits on seed 42 at
σ = 0.25) that collaboration destroys. None of this
measures consciousness, synergy, or redundancy in a
living system; it measures a Williams & Beer
decomposition of a synthetic classical emulation,
under a preregistration written before the held-out
seeds were touched. Classical emulation throughout;
Faggin's metaphysics stays interpretive. No scalar Φ
is computed anywhere.

## 27. A target for which collaboration reliably raises total information: MAX-target PID (v0.21.0, measured 2026-11-18)

The v0.20.0 open follow-up, answered: is there ANY target
for which collaboration reliably raises total information
(ΔI > 0 on every seed) while keeping the PID separable?
The method is a candidate search on CALIBRATION seeds
only (42 and 7) over fourteen deterministic targets Y =
f(X1, X2) of the two agents' 2-bit Born outcomes, all
decomposed by the same Williams & Beer I_min PID on the
same exact pooled distributions (reused from pid.py, not
reimplemented), with I(Xi;Y) computed exactly from the
joint. The screen, the selection rule, and its two
exclusions are frozen in docs/preregistration-v0.21.0.md
from calibration seeds 42/7 before the held-out
evaluation on seeds 1234/2026; none was moved. The naive
rule (max min-seed ΔI among eligible candidates) would
pick the incumbent XOR (+1.1194) or, among new targets,
diff_mod4 (+1.1156); both are set aside in the
preregistration, before the run: xor and joint are
references already measured on all four seeds, and
sum_mod4 / diff_mod4 are Latin-square / group-difference
near-duplicates of the incumbent BY CONSTRUCTION (fixing
one source permutes Y; their H(Y) is driven by the same
difference distribution whose mixture-correlation
uniformization is the diagnosed XOR failure mechanism,
and they track XOR to within 0.004 bits on calibration).
Among the remaining new targets, eligible by the gates
(ΔI > 0, ΔSyn > ΔRed with |ΔSyn − ΔRed| ≥ 0.10,
Red_c/I_c ≤ 0.50 on both calibration seeds), max min-seed
ΔI picks MAX, Y = max(X1, X2) — the peak /
strongest-concept outcome (+1.8927 / +1.0707). OR, the
other agreement-family target, tracks MAX within 0.03
bits at σ = 0.25 and is the reported sensitivity check.
AND and MIN fail the gates (ΔI ≤ 0 on at least one
calibration seed); x1 fails separability (ΔSyn = 0
exactly); eq / parity / lowbit_xor pass with small min
ΔI (≤ +0.2616); lowbits_pair fails the separation gate
on seed 42. A target on a third channel was considered
and set aside: the pair apparatus has no third outcome
channel (the field state is a state vector, not a Born
outcome) and a three-source PID would be new machinery.
No scalar Φ is computed anywhere.

Per-(seed, σ) MAX-target PID, collaborating arm
(I_c, Syn_c, Red_c, Uniq_c) and isolated arm
(I_i, Syn_i, Red_i, Uniq_i), in bits — calibration
seeds first, then held-out:

| seed | σ | I_c | Syn_c | Red_c | Uniq_c | I_i | Syn_i | Red_i | Uniq_i |
|---|---|---|---|---|---|---|---|---|---|
| 42 | 0.00 | 0.8113 | 0.5000 | 0.3113 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.01 | 0.8634 | 0.5245 | 0.3267 | 0.0122 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.05 | 1.2636 | 0.6815 | 0.4616 | 0.1206 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.10 | 1.5684 | 0.7965 | 0.5739 | 0.1981 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.25 | 1.8927 | 1.0279 | 0.6758 | 0.1890 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.50 | 1.9829 | 1.1766 | 0.7005 | 0.1058 | 1.1568 | 0.2000 | 0.4713 | 0.4855 |
| 42 | 1.00 | 1.7947 | 0.9449 | 0.5266 | 0.3232 | 1.3610 | 0.4755 | 0.7610 | 0.1245 |
| 7 | 0.00 | 0.8113 | 0.5000 | 0.3113 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.01 | 0.9544 | 0.5680 | 0.3546 | 0.0317 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.05 | 1.1370 | 0.5637 | 0.3946 | 0.1786 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.10 | 1.3642 | 0.7192 | 0.4922 | 0.1529 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.25 | 1.9520 | 1.0316 | 0.6547 | 0.2657 | 0.8813 | 0.0000 | 0.3958 | 0.4855 |
| 7 | 0.50 | 1.8182 | 0.9803 | 0.6293 | 0.2087 | 1.1568 | 0.1170 | 0.7228 | 0.3170 |
| 7 | 1.00 | 1.7191 | 0.9357 | 0.6566 | 0.1268 | 1.4855 | 0.4585 | 0.8685 | 0.1585 |
| 1234 | 0.00 | 0.8113 | 0.5000 | 0.3113 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1234 | 0.01 | 0.9846 | 0.5503 | 0.3456 | 0.0887 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1234 | 0.05 | 0.9886 | 0.3454 | 0.2366 | 0.4065 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1234 | 0.10 | 1.0937 | 0.3816 | 0.2180 | 0.4941 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1234 | 0.25 | 1.0485 | 0.4005 | 0.2488 | 0.3992 | 0.7219 | 0.0000 | 0.4464 | 0.2755 |
| 1234 | 0.50 | 1.3197 | 0.5309 | 0.3221 | 0.4667 | 0.4690 | 0.0000 | 0.1935 | 0.2755 |
| 1234 | 1.00 | 1.5202 | 0.7867 | 0.4777 | 0.2558 | 0.7219 | 0.4000 | 0.2464 | 0.0755 |
| 2026 | 0.00 | 0.8113 | 0.5000 | 0.3113 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 2026 | 0.01 | 0.8532 | 0.5135 | 0.3177 | 0.0221 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 2026 | 0.05 | 1.0169 | 0.5392 | 0.3541 | 0.1235 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 2026 | 0.10 | 1.2008 | 0.5808 | 0.4102 | 0.2098 | 0.7219 | 0.0000 | 0.0000 | 0.7219 |
| 2026 | 0.25 | 1.3746 | 0.6598 | 0.4537 | 0.2610 | 0.7219 | 0.0000 | 0.3219 | 0.4000 |
| 2026 | 0.50 | 1.4288 | 0.6868 | 0.4664 | 0.2756 | 0.7219 | 0.0000 | 0.3974 | 0.3245 |
| 2026 | 1.00 | 1.7622 | 0.8878 | 0.6693 | 0.2050 | 0.8813 | 0.0000 | 0.8813 | 0.0000 |

### (lxviii) MAX-target PID identity, canonical checks, sampled cross-check — PASS

Worst identity error 2.22e-16 bits (tol 1e-9); worst
atom −0.0000 bits (min −1e-9); worst exact-vs-sampled
H(Y) difference at σ = 0.25 is 0.0318 bits (tol 0.25).
The canonical cases hold: independent uniform → I =
1.7490, Syn = 1.0778, Red = 0.6712, Uniq = 0 (MAX is
NOT pure synergy — a single source alone carries
0.6712 bits about the max); X1 = X2 uniform → I =
2.0, all redundant (Red = 2.0, Syn = 0, Uniq = 0);
X1 deterministic → Uniq2 = 2.0, Syn = 0, Red = 0;
X2 deterministic → Uniq1 = 2.0, Syn = 0, Red = 0.

### (lxix) Collaboration raises total information about the MAX target at σ = 0.25 — PASS

At σ = 0.25: I_collab = 1.8927 / 1.9520 / 1.0485 /
1.3746 against I_isol = 0.0000 / 0.8813 / 0.7219 /
0.7219, so ΔI = +1.8927 / +1.0707 / +0.3266 / +0.6527
(seeds 42 / 7 / 1234 / 2026) — positive on every seed,
including held-out seed 1234, where the XOR gap was
−0.2591. This is the first target in the series for
which the answer to the v0.20.0 question is yes. The
held-out gaps are much smaller than the calibration
ones (0.3266 / 0.6527 vs 1.8927 / 1.0707): on seed
1234 the collaborating arm itself carries little
about MAX at σ = 0.25 (I_collab = 1.0485, Syn_c =
0.4005), so the positive gap there is
narrow, not a second large effect.

### (lxx) The information gap about the MAX target IS synergy, not redundancy, at σ = 0.25 — PASS

At σ = 0.25: ΔSyn = +1.0279 / +1.0316 / +0.4005 /
+0.6598 against ΔRed = +0.6758 / +0.2589 / −0.1976 /
+0.1318 and ΔI = +1.8927 / +1.0707 / +0.3266 /
+0.6527, so the synergy shares are 0.543 / 0.964 /
1.226 / 1.011 (bar 0.5). The shares exceed 1 on the
held-out seeds because ΔUniq is negative there
(−0.1390 on seed 2026; +0.1237 on seed 1234, where
the share exceeds 1 because ΔRed is negative). The
separation holds on all four seeds — ΔSyn > ΔRed
everywhere — and unlike XOR the share half holds too,
because the gap itself is positive everywhere.

### (lxxi) Redundancy stays below half the target information across the grid — PASS

Worst Red_c / I_c = 0.3837 on EVERY seed (bar 0.50),
at σ = 0.00 on all four — the noiseless joint is
seed-independent, so the worst share is the same
number four times. Redundancy is a much larger share
for MAX than for XOR (worst 0.2357, bar 0.25), which
is why the bar here is 0.50: MAX's independent-uniform
canonical case already carries Red/I = 0.3837. The
bar sits 0.116 above the calibration worst, and the
held-out seeds came in at exactly the calibration
worst, not above it.

### (lxxii) Collaboration raises total information about the MAX target across the grid — PASS

Minimum ΔI across the grid: +0.4338 (seed 42, σ =
1.00) / +0.2337 (seed 7, σ = 1.00) / +0.3266 (seed
1234, σ = 0.25) / +0.4789 (seed 2026, σ = 0.10) —
positive on every (seed, σ). The exposed corner is
σ = 1.00 on the calibration seeds and σ = 0.25 on
held-out seed 1234, where the gap is at its minimum;
no corner goes negative.

### Honest limits (v0.21.0 addition)

**5/5 claims pass.** What survives: the MAX target
answers the v0.20.0 open question — collaboration
raises total information about it on every seed, at
σ = 0.25 and across the grid, the gap is
synergy-dominant on every seed, and redundancy stays
below half the target information everywhere. Three
disclosures qualify the yes: (1) the isolated arm
DEGENERATES at low σ — I_isol = 0 exactly at σ ≤ 0.25
on seed 42, σ ≤ 0.10 on seeds 7 and 1234, and σ ≤ 0.05
on seed 2026 (the
design-B lock-in: a collapsed agent stays near its
collapsed concept under small kicks, so max is a
point mass; the seed-42 σ = 0.25 isolated joint is
X1 ∈ {2, 3}, X2 = 3 always), so the large ΔI at low
σ is driven as much by the isolated arm collapsing
to a point as by collaboration raising information —
on seed 7 at σ = 0.25 the isolated arm is not
degenerate (I_isol = 0.8813), and the held-out gaps
are positive there too, so the verdict does not rest
on the degenerate rows alone; (2) the synergy share
at σ = 0.25 is tight on calibration seed 42 (0.543
against the 0.5 bar) and the held-out shares exceed
1 (1.226 / 1.011) because ΔRed is negative on seed
1234 and ΔUniq negative on seed 2026 — the atoms
sum to ΔI exactly, so a share above 1 is arithmetic,
not an error, but it means "synergy is the majority
of the gap" is a weak description on those seeds;
(3) MAX is not a pure-synergy target and was not
selected to be one: even with independent uniform
sources it carries Red = 0.6712 of I = 1.7490, and
its redundancy share (worst 0.3837) is far above
XOR's (worst 0.2357) — what MAX buys is a positive
total-information gap, not a cleaner synergy. None
of this measures consciousness, synergy, or
redundancy in a living system; it measures a Williams
& Beer decomposition of a synthetic classical
emulation, under a preregistration written before
the held-out seeds were touched. Classical emulation
throughout; Faggin's metaphysics stays interpretive.
No scalar Φ is computed anywhere.

## 28. Per-generation PID: does the synergy-vs-σ climb survive without pooling? (v0.22.0, measured 2026-11-18)

The v0.20.0 XOR build found synergy climbing toward the
2-bit ceiling with σ on every seed — claim (lxvi) FAILED
honestly (synergy tracks noise-driven uniformity, not
resonance). But the v0.20.0 report disclosed a confound:
the pooled joint is a MIXTURE of per-generation products,
and the mixture-correlation is itself synergistic about
the XOR target — the isolated arm is NOT synergy-free at
high σ (Syn_isol up to 1.0755 bits at σ = 1.00). This
build asks whether the climb survives when the PID is
computed PER GENERATION (no pooling across generations),
for the XOR target and the MAX target, on the same seeds
and σ grid the pooled results used (seeds 42, 7
calibration; 1234, 2026 held-out; σ grid [0.0, 0.01,
0.05, 0.1, 0.25, 0.5, 1.0]; design B, N = 2, 10
generations). The method reuses the existing PID
machinery — the general Williams & Beer I_min PID
(total_information_target.target_pid_from_joint) applied
to the exact per-generation product joints from the new
pid.pair_arm_per_generation_joints, the same design-B
evolution as pid.pair_arm_distributions with each
generation's p1 ⊗ p2 kept instead of pooled. The
comparison is mean-per-generation atoms vs pooled atoms;
the pooled atom is NOT an average of the per-generation
atoms (the PID is nonlinear in the joint, and the pooled
joint is a mixture), so a gap between the two is expected
in general — the question is its size and direction. The
decision rule was frozen in
docs/preregistration-v0.22.0.md before the held-out
evaluation: the climb survives iff claim (lxxiv) passes.

### (lxxiii) Per-generation PID identity and pooled consistency — PASS

For every target, seed, σ, generation, and both arms:
the four atoms sum to I(X1,X2;Y) within 1e-9 bits
(worst error 4.44e-16) and every atom is ≥ −1e-9; and
the mean of the 10 per-generation joints equals the
pooled joint exactly (worst max-abs-entry diff 0.00e+00,
tol 1e-12). The per-generation path is the same
evolution as the pooled path, not a second one.

### (lxxiv) The XOR synergy-vs-σ climb survives per-generation — FAIL

Mean per-generation Syn_collab(XOR) at σ = 1.00:
1.0933 / 0.9855 / 1.0039 / 0.9995 (seeds 42 / 7 / 1234 /
2026) against the frozen 1.50-bit bar — and it FALLS
from σ = 0.50 to σ = 1.00 on seeds 42, 7, and 2026
(1.1496 → 1.0933; 1.1058 → 0.9855; 1.1218 → 0.9995;
it rises only on 1234, 0.8685 → 1.0039, still far below
the bar). The pooled values at σ = 1.00 are 1.8432 /
1.7933 / 1.8129 / 1.8365 — the pooled curve climbs
0.75–0.81 bits above the per-generation mean at the top
of the grid. Per-generation, the XOR synergy curve is
FLAT (~0.4–1.15 bits across the whole grid, dipping to
0.3947 on seed 1234 at σ = 0.05). By the preregistered
decision rule, **the (lxvi) conclusion is DOWNGRADED to
a pooling artifact**: the climb toward the 2-bit ceiling
is manufactured by pooling across generations. The
noise-driven-uniformity reading is replaced by it — the
per-generation synergy does not climb with σ at all.

Per-generation mean Syn_collab(XOR) across the grid
(pooled in parentheses), in bits:

| seed | 0.00 | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---|---|---|---|---|---|---|
| 42 | 1.0000 (1.0000) | 1.0057 (1.0085) | 0.9675 (1.0809) | 0.8745 (1.1467) | 0.9887 (1.4472) | 1.1496 (1.7178) | 1.0933 (1.8432) |
| 7 | 1.0000 (1.0000) | 0.9533 (0.9746) | 0.5670 (0.7889) | 0.5197 (0.8985) | 0.9542 (1.4865) | 1.1058 (1.7892) | 0.9855 (1.7933) |
| 1234 | 1.0000 (1.0000) | 0.8798 (0.9231) | 0.3947 (0.5604) | 0.4944 (0.5973) | 0.8386 (1.1833) | 0.8685 (1.5323) | 1.0039 (1.8129) |
| 2026 | 1.0000 (1.0000) | 0.9928 (1.0001) | 0.9059 (1.0166) | 0.8517 (1.1032) | 1.2319 (1.5901) | 1.1218 (1.7297) | 0.9995 (1.8365) |

Per-generation mean Syn_collab(MAX) across the grid
(pooled in parentheses), in bits — also flat, no climb:

| seed | 0.00 | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---|---|---|---|---|---|---|
| 42 | 0.5000 (0.5000) | 0.5211 (0.5245) | 0.6167 (0.6815) | 0.5903 (0.7965) | 0.6289 (1.0279) | 0.6355 (1.1766) | 0.4889 (0.9449) |
| 7 | 0.5000 (0.5000) | 0.5519 (0.5680) | 0.3708 (0.5637) | 0.3674 (0.7192) | 0.5513 (1.0316) | 0.5585 (0.9803) | 0.4180 (0.9357) |
| 1234 | 0.5000 (0.5000) | 0.5225 (0.5503) | 0.2293 (0.3454) | 0.3188 (0.3816) | 0.3094 (0.4005) | 0.3172 (0.5309) | 0.3801 (0.7867) |
| 2026 | 0.5000 (0.5000) | 0.5071 (0.5135) | 0.4597 (0.5392) | 0.4016 (0.5808) | 0.5033 (0.6598) | 0.4264 (0.6868) | 0.4349 (0.8878) |

### (lxxv) The isolated arm's high-σ synergy is a pooling artifact (XOR) — FAIL

The per-generation leg holds exactly: mean
per-generation Syn_isol(XOR) = 0.0000 at every
(seed, σ) — by construction, since the design-B
isolated arm collapses each agent to a decided concept
each generation, so each per-generation joint is a point
mass. But the mixture-excess leg fails on held-out seed
2026: pooled Syn_isol(XOR) at σ = 1.00 minus the
per-generation mean is +1.0755 / +1.0000 / +1.0755 /
+0.4000 (seeds 42 / 7 / 1234 / 2026) against the frozen
0.50-bit bar. On seed 2026 the pooled isolated synergy
itself is only 0.4000 (vs 1.0000–1.0755 on the other
three seeds), so the excess cannot reach the bar. The
confound diagnosis is confirmed on three of four seeds
and fails its own bar on the fourth — the mixture
excess is large but not uniformly ≥ 0.50 bits. Reported
as measured; the bar was not moved.

### (lxxvi) The per-generation MAX gap at σ = 0.25 is synergy, not redundancy — FAIL

Mean per-generation ΔSyn(MAX) > mean per-generation
ΔRed(MAX) on every seed (0.6289 > 0.4132; 0.5513 >
0.3208; 0.3094 > 0.1754; 0.5033 > 0.3051), but the
synergy share of the mean gap is 0.383 / 0.332 / 0.350 /
0.445 (seeds 42 / 7 / 1234 / 2026) — below the frozen
0.5 bar on every seed. Per-generation the MAX gap is
carried substantially by unique information (mean ΔUniq
0.5998 / 0.7878 / 0.3996 / 0.3223). The pooled (lxx)
verdict (shares 0.543 / 0.964 / 1.226 / 1.011) does NOT
survive per-generation for MAX on any seed.

### (lxxvii) The per-generation XOR gap at σ = 0.25 is synergy, not redundancy — PASS

Mean per-generation ΔSyn(XOR) > mean per-generation
ΔRed(XOR) on every seed, and the synergy share of the
mean gap is 0.566 / 0.541 / 0.584 / 0.655 (seeds 42 / 7 /
1234 / 2026), above the frozen 0.5 bar on every seed.
Mean ΔI / ΔSyn / ΔRed / ΔUniq at σ = 0.25: +1.7457 /
+0.9887 / +0.2582 / +0.4989 (42); +1.7649 / +0.9542 /
+0.1849 / +0.6257 (7); +1.4356 / +0.8386 / +0.1202 /
+0.4768 (1234); +1.8817 / +1.2319 / +0.2899 / +0.3599
(2026). The reversal that matters is on seed 1234:
the pooled gap there was NEGATIVE (−0.2591, the (lxv)
failure — the isolated arm carried MORE total
information about the XOR target than the collaborating
arm), but the mean per-generation gap is +1.4356 and
synergy-majority (share 0.584). **The v0.20.0 failure on
seed 1234 was itself a pooling artifact**: pooling
raised the isolated arm's XOR information (pooled
I_isol = 1.7610) above the collaborating arm's, while
per-generation the isolated arm carries nothing at all
(I_isol = 0 exactly, every generation) and the
collaborating arm carries 1.4356 bits on average.

### Honest limits (v0.22.0 addition)

**2/5 claims pass.** The headline is a downgrade, and it
is the result: the synergy-vs-σ climb does not survive
without pooling, the pooled (lxx) synergy-majority does
not survive per-generation for MAX, and the mixture-excess
bar fails on seed 2026. Three disclosures qualify the
picture: (1) the per-generation isolated arm is
synergy-free BY CONSTRUCTION (point-mass joints after the
design-B collapse), so the (lxxv) per-generation leg is
not a measurement — the measured part is the mixture
excess, and it is seed-dependent (0.40 on 2026 vs
1.00–1.08 elsewhere); (2) per-generation synergy varies
a lot across generations — sd(Syn_c) at σ ≥ 0.05 is
0.14–0.39 bits for XOR (worst 0.3886, seed 7 σ = 1.00;
single generations range 0.2096–1.8250 there), so the
pooled value is not representative of any single
generation, and the mean-per-generation curve is itself
a summary of a wide spread; (3) mean per-generation ΔI
for MAX exceeds the pooled ΔI on seed 7 (+1.6598 vs
+1.0707 at σ = 0.25) because pooling raises the isolated
arm's information (pooled I_isol = 0.8813) while
per-generation I_isol = 0 — pooling moves BOTH arms, not
just the collaborating one, so pooled-vs-per-generation
comparisons cut both ways. What survives per-generation
is narrower than what pooling showed: the XOR gap at
σ = 0.25 is synergy-majority on every seed including
1234. None of this measures consciousness, synergy, or
redundancy in a living system; it measures a Williams &
Beer decomposition of a synthetic classical emulation,
under a preregistration written before the held-out
seeds were touched. Classical emulation throughout;
Faggin's metaphysics stays interpretive. No scalar Φ is
computed anywhere.
