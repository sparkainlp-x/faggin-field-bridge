# Faggin Field Bridge — Report

**Version:** 0.3.1 (2026-11-16)
**Theory author:** Federico Faggin (with Giacomo Mauro D'Ariano)
**Bridge / test author:** Jean-François Brisson (Spark AI NLP)
**Status:** SYNTHETIC. Classical computation on synthetic states.
No physical, biological or safety claim is made.

## 1. What was built

A eight-module Python package (stdlib + NumPy only) that maps
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

**130 tests, 130 passed** (`python3 -m pytest tests/ -q`, 5.1 s).

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
- `test_thought.py` (10): uniform coherence 3.0, decided
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

## 7. Files

```
faggin-field-bridge/
  README.md           summary + how to run + maximum scientific outcome
  REPORT.md           this file
  LICENSE             full AGPL v3 text
  CHANGELOG.md        version history (0.1.0, 0.2.0, 0.3.0, 0.3.1)
  .zenodo.json        Brisson, ORCID 0009-0000-9778-5374 (no DOI yet)
  CITATION.cff        no DOI (none invented)
  VERSION             0.3.1
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
  tests/              130 tests, 13 files
```

v0.3.0 is pushed (main head 658f5bdd). v0.3.1 is local only;
not pushed.

GitHub: https://github.com/sparkainlp-x/faggin-field-bridge
(main head 658f5bdd as of 2026-11-16; the maximum scientific
outcomes framework, coverage reporting, and synergy expansion
were added by Jean in 7 commits on 2026-11-15, and the synergy
robustness analysis in this report was added the same day.
The v0.3.1 review fixes are local only, pending Jean's word
to push.)

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
