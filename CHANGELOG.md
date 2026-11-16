# Changelog — Faggin Field Bridge

## 0.3.1 (2026-11-16)

Bugfix release, from an external review of the v0.3.0 repo
(head 658f5bdd). Every finding was re-verified against a fresh
clone before fixing. No claim (i)–(vii) changes: none of the
fixes moves a measured verdict. Tests: 122 -> 130, all passing.

- **Sensitivity bug, fixed** (`scientific_outcomes.py`):
  the one-at-a-time sensitivity sweep passed every perturbed
  value into the *unity* slot, so the cost sweep varied unity
  instead of cost and the delta sweep varied unity instead of
  delta. The unity sweep was correct; the other two columns
  were wrong. `apply` now returns the full (unity, cost,
  delta) triple. Old -> new attunements at U = 0.99999995,
  C = 0.9553, delta = 0: cost sweep was (-0.05, -0.01, 0.0,
  0.01, 0.0447) — literally the perturbation itself — now
  (0.0947, 0.0547, 0.0447, 0.0347, -0.0); delta sweep was
  (-1.0, -0.9803, -0.9553, -0.9303, -0.9053), now (-0.0053,
  0.0197, 0.0447, 0.0697, 0.0947). The wrong columns existed
  only in generated benchmark output (`write_benchmark()`):
  no committed file carried them. Six new tests, including
  the directional assertions the old suite lacked (a cost
  increase must lower A; a unity or delta increase must raise
  it).
- **Mapping-status label, single-sourced**
  (`scientific_outcomes.py`, `bridge.py`): `bridge.py`
  emitted `ATTUNED-LOW-EMPATHY` (hyphens) while
  `maximum_scientific_outcome` re-implemented the
  classification inline and emitted `ATTUNED_LOW_EMPATHY`
  (underscores), and `robustness()` hardcoded only
  DISSONANT/PARTIAL. All three now call the one classifier,
  `bridge.mapping_status`, on the hyphen form (the form the
  README and `test_bridge.py` already assert). `robustness()`
  now reports an ATTUNED case as ATTUNED at both bounds.
- **The 8fb00f1 threshold commit, defused in writing**
  (REPORT.md §5): commit `8fb00f1` (2026-11-15 00:23:35
  -0500, 32 minutes after the preregistration framework
  commit `dc5575a`) changed the synergy thresholds
  DORMANT 0.10 -> 0.03, EMERGENT 0.30 -> 0.05, and rewrote
  the boundary test assertions to match, adding an assertion
  that the primary expansion is FLOWING. Under the old
  thresholds the primary expansion (e = 0.05436) was
  DORMANT; under the new ones it is FLOWING — the commit
  moved the label two steps, and the FLOWING label now hangs
  on a 0.00436 margin above the 0.05 boundary. The commit
  message states the intent ("so primary expansion is
  FLOWING"); no other justification is recorded in the
  commit. The thresholds are repository conventions, not
  measured constants, and the report now says so with the
  numbers attached. New `threshold_robustness()` table in
  `scientific_outcomes.py` (and `synergy_status_with_thresholds()`
  in `synergy.py`): the label survives any EMERGENT threshold
  up to 0.05 and flips to EMERGENT at 0.06. The
  `synergy_robustness` margins dict now tracks all three
  expansion thresholds (to_dormant 0.02436, to_emergent
  0.00436, to_fecund 0.54564).
- **Seed spread of the 0.9553** (`cost.py`, REPORT.md §2):
  the tensor-membrane entropy was computed at seed 42 only.
  Across seeds 0..19 (n = 20): mean 0.9639, standard
  deviation 0.0128, range [0.9276, 0.9775]. The seed-42 value
  0.9553 sits 0.0086 below the mean — within one standard
  deviation, a typical draw, not an outlier. The headline is
  kept (seed 42); the spread is reported alongside it and
  pinned by a test. Honest reading: near-saturated, Page-like
  behaviour, and a ±0.013 move in C moves A by ∓0.013, about
  30% of the primary attunement 0.0447.
- **Synergy terms mapped to Faggin & D'Ariano** (REPORT.md
  §5, no code renames): a section mapping each
  synergy-family term (fecundity, attraction,
  love-empathy synergy, expansion, FECUND-SYNERGISTIC) to
  the specific passage in QIP it is a proxy for, stating
  plainly where no derivation exists. Short version: only
  the synergy formula gestures at a passage (love /
  attunement as the felt sense of connection); none of the
  five terms is derived from Faggin & D'Ariano — all are
  repository definitions.
- **Version alignment:** `pyproject.toml` still said 0.1.0
  (it was never bumped past the initial release); it now
  says 0.3.1, matching VERSION, `.zenodo.json`, and
  CITATION.cff.

## 0.3.0 (2026-11-15)

The cascade: superposition → projection → interference, chained
across stages 1, 2, 3, 5, 10. One new module, three new claims,
all passing.

- `cascade.py` — the cross term ⟨ψ1|P|ψ2⟩ as interference, with
  visibility V over a 64-phase sweep, cross-checked against the
  analytic 2|⟨ψ1|P|ψ2⟩|/(D1 + D2). Claim (v) PASSES: for a
  rotation pair V(θ) = sin(2θ) exactly (0.5 / 0.7071 / 0.8660 /
  1.0); at θ = π/4, D(φ) = 1/2 − (1/2)cos(φ) — the superposed
  thought is fully blind at φ = 0 and fully self-determined at
  φ = π; the mixed pair has cross term 1/√6 and V = 2√6/7 ≈
  0.6999; the stored and (uniform, kernel) control pairs have
  cross term 0 and V = 0.
- Claim (vi) PASSES — the finding: **interference does not
  survive projection**. In both projection-only cascades V is
  1.0 / 0.6999 at stage 1 and 0.0000 at every stage from 2 on
  (the rotation pair collapses to rank 1; the mixed pair
  re-forms fully stored as (q1, q2)), while the reopening
  control (fresh kernel input at α = π/4 each stage) stays at
  V = 1 at every stage. The reason is structural: the cross
  term is ⟨Pψ1|Pψ2⟩, and once a pair is re-formed inside the
  stored subspace, P acts as the identity there and
  orthogonality forces the cross term to zero.
- Claim (vii) PASSES: D of the projected output is 1.0 at every
  stage in every cascade; the projected-output coherence reaches
  a fixed point from stage 2 (rotation 3.0, mixed 2.7321,
  reopening 3.0). Spearman(V, coherence) = −1.0000 in the mixed
  cascade (visibility dies while coherence rises to its fixed
  point); Spearman(V, D) = 0.0 everywhere (D constant, so the
  correlation is undefined — reported as 0.0 by convention, on
  values rounded to 12 decimals so identical stages are not
  ranked on float noise).
- One honest measurement-design fix during the build: the feed
  phase (phase of maximum D) was first taken as a raw argmax,
  which is floating-point noise when D is flat across the sweep;
  it is now the smallest phase achieving the maximum within
  1e-12, stated as a convention in cascade.py.
- `bridge.quantum_thought_claims()` now unifies seven claims;
  `scientific_outcomes` carries them under "quantum_thoughts".
  The preregistration non-claims keep their original wording
  and gain an interference/cascade scoping entry.
- Tests: 108 -> 122, all passing.

## 0.2.0 (2026-11-15)

Quantum thoughts: three new modules, four new claims, all passing.

- `thought_entanglement.py` — concurrence (Wootters, exact) and
  reduced-state entropy for a two-thought Bell state. Claim (i)
  PASSES: concurrence 0.9998 at noise sigma = 0.01 (spooky 0.9998
  on the same copies); depolarizing concurrence reproduces
  max(0, 1 - 3p/2) exactly and dies at p = 2/3; reduced entropy
  stays 1 bit throughout (it cannot see the death). Spooky first
  falls below 0.9 at sigma = 0.25 while mean concurrence never
  falls below 0.6520 under vector noise: spooky and concurrence
  part ways, which is why spooky was never entanglement.
- `thought.py` — a thought as a superposition over four basis
  concepts. Claim (ii) PASSES: coherence half-life measured
  14 / 7 / 3 / 1 steps at p = 0.05 / 0.1 / 0.25 / 0.5 against
  analytic 13.51 / 6.58 / 2.41 / 1.00. Claim (iii) PASSES:
  fully dephased uniform thought has entropy 2 bits, a collapsed
  thought 0; decision entropy 2 bits before collapse, 0 after;
  attention bias +0.018739 at delta = +0.05, -0.018738 at -0.05.
- `self_knowing.py` — D = <psi|P|psi>, the self-determinism
  factor vendored from the symmetry-entropy package (own
  implementation, provenance cited). Claim (iv) PASSES: exact
  values D = 1 (stored), 1/3 (non-stored basis), 0 (kernel),
  1/2 (maximally mixed); Spearman(sigma, D) = -1.0;
  Spearman(D, coherence) = 0.9643. Surprise, measured: D
  ANTI-tracks concurrence (Pearson -0.9570), because the noise
  that destroys self-knowing creates entanglement in a product
  thought.
- `bridge.quantum_thought_claims()` unifies the four claims;
  `scientific_outcomes` carries them under "quantum_thoughts".
  The claims registry now distinguishes entanglement measured
  in the model (True) from physical entanglement in hardware
  (still False). The preregistration non-claims keep their
  original wording and gain a scoping entry.
- Copyright line added to `bridge.py`, `scientific_outcomes.py`,
  `synergy.py` (they were missing it).
- Tests: 80 -> 108, all passing.

## 0.1.0 (2026-11-14)

Initial release: attunement A(delta) = U * (1 + delta) - C with
spooky unity, entropy cost, observer/calibrator, mapping status,
maximum-scientific-outcomes framework, and the synergy expansion
(added by Jean in 7 commits on 2026-11-15, with the synergy
robustness analysis). 80 tests.
