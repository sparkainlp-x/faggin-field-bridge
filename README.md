# Faggin Field Bridge

A measured mapping of Federico Faggin's quantum-field theory of
consciousness onto Jean's sparkainlp-x work. Version 0.1.0.

**Theory author: Federico Faggin** (with Giacomo Mauro D'Ariano).
**Bridge / test author: Jean-François Brisson (Spark AI NLP).**
Faggin has not reviewed or endorsed this software.

## What this is

Faggin's theory — Quantum Information Panpsychism (QIP) — says
consciousness is a fundamental property of quantum fields,
entanglement is the basis of the unity of experience, free will
arises from quantum indeterminacy, and love/attunement is a
fundamental principle. Those are metaphysical claims. **This
package does not test them.** It tests the *mapping*: each of
Faggin's concepts is given a measurable code quantity, built from
numbers already measured elsewhere in the sparkainlp-x account,
and the bridge reports what those numbers do.

The bridge's central quantity is **attunement**:

```
A(delta) = U * (1 + delta) - C
```

- **U — unity**: spooky correlation, the mean pairwise |dot| over
  5 noisy copies of the state (the Omega-Genesis definition).
- **C — cost**: normalized entropy, S / S_max, in [0, 1].
- **delta — calibrator**: one clipped scalar in [-0.05, 0.05]
  (the membrane-arena Yin bound). It scales the unity term only.

A is in [-1, 1]. Positive means unity exceeds the entropy cost
(the state holds together); negative means the cost dominates.

## The mapping

| Faggin concept | Bridge quantity | Source repo | Number |
|---|---|---|---|
| Unity of experience (entanglement) | Spooky correlation U | digital-to-wave-2-debroglie | 0.99999995 at σ = 0.01 (reproduced exactly) |
| Unity of experience (entanglement) | Spooky correlation U, Omega-Genesis run | sparkainlp-x-notebook-research | 0.9005 (notebook's reported value; synthetic reproduction 0.837, same regime, not exact) |
| Entropy / disorder cost | Mean single-qubit von Neumann entropy, / 1 bit | tensor-membrane | 0.955 bits (reproduced: 0.9553) |
| Free will (choice inside a bound) | Calibrator delta in [-0.05, 0.05], best improvement | digital-to-wave-2-debroglie | 0.022276 orders (reproduced exactly) |
| Love / attunement | Attunement A = U − C, adjusted by delta; empathy proxy E | this bridge (new definition) | A in [-1, 1]; empathy proxy default 0.5503 (notebook's reported value, supplied, not recomputed) |
| Gravity (Orch OR microtubules) | None — no gravity model | none | UNMEASURED |

## Measured results (SYNTHETIC)

Worked examples from `bridge.worked_example()`:

| Example | U | C | A(δ=0) | A(best, δ=+0.05) | Verdict |
|---|---|---|---|---|---|
| Primary: de Broglie unity + tensor cost | 0.99999995 | 0.9553 | 0.0447 | 0.0947 | PARTIAL |
| Omega-Genesis reported unity + tensor cost | 0.9005 | 0.9553 | −0.0548 | −0.0098 | DISSONANT |
| Omega-Genesis synthetic unity + tensor cost | 0.8373 | 0.9553 | −0.1181 | −0.0762 | DISSONANT |

Reading: the de Broglie unity is the only one high enough to
cover the 0.955 entropy cost, and only barely — PARTIAL. The
notebook's unity does not cover it even at the best delta. The
bounded calibrator moves A by at most 0.05 × U (~0.05); it cannot
make a high-entropy state attuned. At δ = −0.05 the primary
example flips to −0.0053: the calibrator can flip the verdict,
but it cannot rescue the state. That is the bridge's honest
result. Full numbers in [REPORT.md](REPORT.md).

Reproductions (recomputed fresh from the definitions, not copied
from the source repos' outputs):

- **de Broglie spooky**: 0.999999947 vs reported 0.99999995
  (σ = 0.01); 0.999998638 vs 0.99999864 (σ = 0.05);
  0.999642891 vs 0.99964289 (σ = 0.50). Exact.
- **Calibration identity**: best improvement 0.022276 orders =
  log10(1/0.95), at best δ = −0.05. Exact — a mathematical
  identity, not a fitted number.
- **Tensor-membrane entropy**: 0.9553 bits vs reported 0.955
  (tolerance 0.02 bits). Reproduced.
- **Omega-Genesis spooky**: synthetic 0.8373 vs reported 0.9005
  (difference 0.0632). Same regime, **not exact** — see the
  honest limits below.
- **Empathy 0.5503**: the notebook's reported value, recorded as
  the default empathy proxy. **Not recomputed** — the extraction
  gives no closed-form empathy formula.

## How to run

```sh
python3 -m pytest tests/ -q        # 50 tests, all passing
python3 bridge.py                   # the worked examples + verdicts
python3 unity.py                    # the unity reproductions
python3 cost.py                     # the entropy reproductions
python3 attunement.py               # attunement + calibration identity
python3 faggin_theory.py            # the theory summary + mapping table
```

Requires Python ≥ 3.11 and NumPy. No other dependencies.

## Modules

- `faggin_theory.py` — the theory as data: author, works, claims
  (each with a status), the mapping table, the gravity note.
  No physics claims.
- `unity.py` — spooky correlation (Gaussian and erasure copy
  models), the de Broglie log-gap state, the Omega-Genesis
  synthetic state, the CCI formula.
- `cost.py` — Shannon and von Neumann entropy (bits), the
  normalized cost, the tensor-membrane network reproduction.
- `attunement.py` — A = U·(1+δ) − C; Yang Observer (read-only,
  frozen observations); Yin Calibrator (one clipped scalar in
  [-0.05, 0.05]); the gap-calibration identity; the empathy proxy.
- `bridge.py` — wires observer → calibrator → attunement →
  verdict; the worked examples.

## Honest limits

1. **Faggin's theory is interpretive.** The claim that quantum
   fields ARE conscious is a philosophical interpretation of
   quantum physics, not a measured result. This package tests
   the mapping, not the metaphysics. No experiment has
   demonstrated a conscious quantum field.
2. **Empathy / love are supplied proxies, not measured human
   properties.** The bridge defines attunement as a code
   quantity (A = U − C) and takes empathy as a supplied
   parameter (default 0.5503, the notebook's reported value).
   A is a number computed from a synthetic state, not a human
   feeling.
3. **No real quantum entanglement is measured here.** Spooky
   correlation is self-similarity under noise. The bridge
   borrows Faggin's word "unity" for that classical quantity;
   it does not measure entanglement.
4. **No gravity model exists in this package.** Gravity enters
   only as the Orch OR discussion (Penrose-Hameroff: gravity-
   induced collapse in microtubules; Faggin's QIP does not
   invoke gravity) and is marked UNMEASURED. The notebook
   config's MICROTUBULE_RATIO (0.70) is a simulation parameter,
   not a measurement of microtubules.
5. **The private theory is excluded.** The private-always theory
   is not used or cited anywhere in this package (a test scans
   the code to enforce it).
6. **Everything is synthetic / classical** except the simulated
   tensor network. This bridge is classical code on a classical
   machine, so on Faggin's own account it has no interior: it
   computes quantities; it does not feel them.
7. **The Omega-Genesis spooky value does not reproduce exactly.**
   The notebook's 0.9005 comes from its evolved state after a
   10M-iteration run; that state is unavailable. The synthetic
   reproduction (32-dim state of the same shape, 5 copies under
   the notebook's own 20% erasure stress, seed 42) gives 0.8373
   — the same regime (0.8–0.9), a difference of 0.0632. The
   test asserts the regime, not the exact value, and the
   difference is printed, not hidden.
8. **The verdict thresholds (A ≥ 0.5, E ≥ 0.5) are chosen cut
   points of this bridge**, not measured constants. They are
   stated in `bridge.py` so they can be argued with.

## Credits

- **Federico Faggin** — theory author (Quantum Information
  Panpsychism, with Giacomo Mauro D'Ariano, arXiv:2012.06580;
  *Irreducible*, Essentia Books, 2024; memoir *Silicon*, 2021).
- **Jean-François Brisson (Spark AI NLP)** — bridge / test author.
- **Mun Seok Lee** — author of the Digital to Wave papers whose
  numbers the bridge reuses (Zenodo 21947108); the de Broglie
  and calibration reproductions use his paper's numbers.
- Source repos: digital-to-wave-2-debroglie, tensor-membrane,
  sparkainlp-x-notebook-research (Omega-Genesis, Untitled7).

## Licence

AGPL-3.0-only. See [LICENSE](LICENSE). No DOI yet — no Zenodo
record exists for this package (none invented).
