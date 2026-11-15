# Faggin Field Bridge — Report

**Version:** 0.1.0 (2026-11-14)
**Theory author:** Federico Faggin (with Giacomo Mauro D'Ariano)
**Bridge / test author:** Jean-François Brisson (Spark AI NLP)
**Status:** SYNTHETIC. Classical computation on synthetic states.
No physical, biological or safety claim is made.

## 1. What was built

A five-module Python package (stdlib + NumPy only) that maps
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

**80 tests, 80 passed** (`python3 -m pytest tests/ -q`, 1.34 s).

- `test_unity.py` (9): spooky bounds, identical copies = 1.0,
  independent states low, no mutation, de Broglie reproduction
  at three sigmas, state-vector shape, Omega synthetic regime,
  CCI bounds.
- `test_cost.py` (8): Shannon uniform/certain, von Neumann pure
  / maximally mixed, normalized-cost bounds and errors, tensor
  entropy reproduction, tensor cost = entropy / 1 bit, Shannon
  of a uniform 32-dim state.
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
- `test_maximum_scientific_outcomes.py` (19): input validation
  and delta clipping, bootstrap interval ordering and
  determinism, sensitivity coverage, point estimates, mapping
  status before and after calibration (PARTIAL in both),
  robustness sign-flip reporting, preregistration non-claims,
  provenance hash determinism, benchmark file writing, and
  the synergy-expansion bootstrap and robustness tests below.
- `test_synergy.py` (11): synergy threshold ordering, input
  validation, fecundity / attraction / synergy / expansion
  definitions and bounds, status boundaries, primary worked
  values (FLOWING), and the non-claims record.

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

## 7. Files

```
faggin-field-bridge/
  README.md           summary + how to run + maximum scientific outcome
  REPORT.md           this file
  LICENSE             full AGPL v3 text
  .zenodo.json        Brisson, ORCID 0009-0000-9778-5374 (no DOI yet)
  CITATION.cff        no DOI (none invented)
  VERSION             0.1.0
  Makefile            test / coverage / benchmark / clean
  pyproject.toml      setuptools + pytest config
  faggin_theory.py    theory as data
  unity.py            spooky correlation
  cost.py             entropy
  attunement.py       A, observer, calibrator, empathy proxy
  bridge.py           wiring + mapping status + worked examples
  scientific_outcomes.py  maximum scientific outcomes framework
  synergy.py          fecundity-driven attraction expansion
  tests/              80 tests, 8 files
```

GitHub: https://github.com/sparkainlp-x/faggin-field-bridge
(main head f2056a77 as of 2026-11-15; the maximum scientific
outcomes framework, coverage reporting, and synergy expansion
were added by Jean in 7 commits on 2026-11-15, and the synergy
robustness analysis in this report was added the same day.)

Zenodo: no record yet. Release (toggle + tag + release notes) is
the next step; see the Priority 1 launch sheet. When releasing,
tag the current head — the repo has moved past the v0.1.0
originally pushed, and the release should archive the work as
it stands.
