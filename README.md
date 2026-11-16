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

Run `bridge.quantum_thought_claims()` for the four verdicts, or
see REPORT.md §8.

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

AGPL-3.0-only. See `LICENSE`.
