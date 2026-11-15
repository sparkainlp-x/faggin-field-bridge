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

**50 tests, 50 passed** (`python3 -m pytest tests/ -q`, 1.23 s).

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

## 5. Honest limits (repeated from the README — they are the point)

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

## 6. Files

```
faggin-field-bridge/
  README.md           this report's summary + how to run
  REPORT.md           this file
  LICENSE             full AGPL v3 text
  .zenodo.json        Brisson, ORCID 0009-0000-9778-5374 (no DOI yet)
  CITATION.cff        no DOI (none invented)
  VERSION             0.1.0
  pyproject.toml      setuptools + pytest config
  faggin_theory.py    theory as data
  unity.py            spooky correlation
  cost.py             entropy
  attunement.py       A, observer, calibrator, empathy proxy
  bridge.py           wiring + mapping status + worked examples
  tests/              50 tests, 6 files
```

No GitHub repo exists for this package yet. Repo creation is
Jean's web step; nothing was pushed.
