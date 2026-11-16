# Changelog — Faggin Field Bridge

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
