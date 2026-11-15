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
