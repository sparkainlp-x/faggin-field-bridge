# Pre-registration — v0.23.0: privacy-enforcing copier — is the 5/6 bound restored when the representation enforces privacy? Claims (lxxviii)–(lxxxi)

Written 2026-11-18, BEFORE the evaluation run on the held-out
seeds 1234 and 2026. Thresholds are round numbers frozen from a
calibration pilot on seeds 42 and 7 only. No threshold in this file
may be moved after the evaluation run, and no claim may be
redefined after the fact.

## The spec being tested

Claim (xlviii) FAILED in v0.15.0: the classical copy
(unity.gaussian_copies) exceeds the 5/6 Bužek–Hillery bound at
every working σ (1.0000 at σ = 0), because the classical emulation
stores the full amplitude vector and privacy is not enforced by
the representation. The v0.15.0 report recorded this as a
representation artifact: the classical copier sees the whole
state. This build asks whether the bound is restored when the
copier is RESTRICTED to measurement outcomes only — a classical
channel with bounded information about the state — and never
sees the amplitude vector.

The construction uses only mechanisms already in the tree:

- Presented states: the SAME states claim (xlviii) measured as
  "copies" — unity.gaussian_copies of the uniform thought (5
  copies, σ grid [0.0, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0], every
  seed). The state presented to the restricted copier at (σ, seed)
  is exactly the state the unrestricted copier produced there, so
  the two copiers are compared on identical inputs. σ now measures
  how concentrated / classical the state being copied is, not how
  noisy the copier is: at σ = 0 the presented state is the uniform
  thought; at σ = 1.0 it is a noisy, partly concentrated state.
- Measurement: the bridge's own Born collapse in the 4-concept
  basis (the measurement behind
  cloning_ceiling.pair_accessible_information): outcome k with
  probability p(k) = |ψ_k|². The copier observes only the
  outcomes, never ψ. One outcome carries at most log2(4) = 2 bits
  about the state, and no phase information at all.
- Single-shot copier (M = 1): one Born outcome k; the copy is the
  basis state e_k. Fidelity with the presented state is
  |⟨ψ|e_k⟩|² = p(k); its expectation over outcomes is Σ_k p(k)²
  (0.25 for the uniform thought).
- M-shot copier: M independent Born outcomes on the same presented
  state; the copy is the maximum-likelihood amplitude
  reconstruction sqrt(counts / M) (real, non-negative, unit norm).
  Fidelity is the TRUE inner product |⟨ψ|copy⟩|² with ψ's signs
  kept: the reconstruction cannot recover signs, so any negative
  component of ψ subtracts. That sign-blindness is part of the
  privacy mechanism, not a bug in it.
- Asymptotic leak (reported, not claimed): as M → ∞ the
  reconstruction tends to |ψ| componentwise, so the fidelity tends
  to (Σ_k ψ_k |ψ_k|)² exactly — computable in closed form with no
  sampling. It is the ceiling of what the classical channel can
  ever leak: amplitudes yes, signs and phases no.

## Decision rule, stated in advance

- "The bound is restored under the restricted representation"
  means claim (lxxviii) PASSES: the single-shot restricted copier
  respects 5/6 at every σ on every seed.
- "The restriction restores the bound only while the measurement
  budget is small" means claim (lxxix) PASSES: a 16-shot copier
  already exceeds 5/6 at σ = 0. Both (lxxviii) and (lxxix) can
  pass together — they are about different budgets, not
  contradictory readings. If (lxxviii) fails, the violation is
  NOT (only) a representation artifact: even a copier that sees
  nothing but measurement outcomes exceeds the bound.
- Either outcome is a result; neither is softened.

## Calibration pilot (seeds 42 and 7) — disclosed before the run

Single-shot mean fidelity per σ (5 copies):

| seed | 0.00 | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 | max |
|---|---|---|---|---|---|---|---|---|
| 42 | 0.2500 | 0.2542 | 0.2658 | 0.2665 | 0.2829 | 0.3998 | 0.3470 | 0.3998 |
| 7 | 0.2500 | 0.2548 | 0.2748 | 0.3024 | 0.4859 | 0.4793 | 0.5798 | 0.5798 |

Budget sweep at σ = 0 (20 copies), mean fidelity per M:

| seed | M = 1 | M = 4 | M = 16 | M = 64 | M = 256 | gap M64 − M1 |
|---|---|---|---|---|---|---|
| 42 | 0.2500 | 0.5933 | 0.9526 | 0.9878 | 0.9965 | 0.7378 |
| 7 | 0.2500 | 0.6178 | 0.9396 | 0.9882 | 0.9977 | 0.7382 |

16-shot mean fidelity per σ (20 copies):

| seed | 0.00 | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---|---|---|---|---|---|---|
| 42 | 0.9526 | 0.9502 | 0.9481 | 0.9298 | 0.9333 | 0.8425 | 0.8079 |
| 7 | 0.9396 | 0.9438 | 0.9465 | 0.9402 | 0.9365 | 0.7840 | 0.6331 |

Asymptotic (M → ∞) leak, mean fidelity per σ (5 copies, exact):

| seed | 0.00 | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---|---|---|---|---|---|---|
| 42 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8146 | 0.7583 |
| 7 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8606 | 0.7891 |

Restricted (single-shot) vs unrestricted (xlviii) mean fidelity
per σ — REPORTED, not claimed (the targets differ; see below):

| seed | copier | 0.00 | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---|---|---|---|---|---|---|---|
| 42 | restricted 1-shot | 0.2500 | 0.2542 | 0.2658 | 0.2665 | 0.2829 | 0.3998 | 0.3470 |
| 42 | unrestricted | 1.0000 | 0.9998 | 0.9945 | 0.9775 | 0.8540 | 0.5883 | 0.4068 |
| 7 | restricted 1-shot | 0.2500 | 0.2548 | 0.2748 | 0.3024 | 0.4859 | 0.4793 | 0.5798 |
| 7 | unrestricted | 1.0000 | 0.9999 | 0.9962 | 0.9841 | 0.8644 | 0.6057 | 0.4069 |

Four disclosures, before the run:

1. The single-shot copier is calibrated to PASS (lxxviii): its max
   mean fidelity is 0.3998 / 0.5798, far below 5/6 even at
   σ = 1.00. The concentration effect that could have broken the
   bound at high σ does not: the noisy state never concentrates
   enough for one outcome to identify it. The bound IS restored
   for the single-shot copier.
2. The 16-shot copier is calibrated to PASS (lxxix): 0.9526 /
   0.9396 at σ = 0, both above 5/6. With 16 shots the classical
   channel already leaks the amplitude vector of a real, positive
   state almost exactly. The restriction restores the bound only
   while the measurement budget is small — one shot, not sixteen.
3. The budget gap is calibrated to PASS (lxxx) with a wide margin
   (0.7378 / 0.7382 against the 0.30 bar): the measurement budget
   controls the leak, monotonically (M = 1 → 256 rises
   0.25 → 0.99 on both seeds at σ = 0).
4. Claim (lxxxi) is calibrated to PASS, but the high-σ leg is
   THIN on seed 42: the 16-shot mean fidelity at σ = 1.00 is
   0.8079, only 0.025 below the 5/6 bar (seed 7: 0.6331, margin
   0.20). Held-out failure of (lxxxi) on seed 1234 or 2026 is a
   live possibility, disclosed in advance. The mechanism behind
   the leg is exact and reported, not claimed: the M → ∞ leak
   ceiling is 1.0000 at every σ ≤ 0.25 (the presented state stays
   real and positive there, so |ψ| = ψ and the reconstruction is
   exact in the limit) and drops to 0.7583 / 0.7891 at σ = 1.00
   (negative components appear, and the outcome-only
   reconstruction cannot see their signs). At σ = 0.50 the
   ceiling is 0.8146 / 0.8606 — seed 7 already above 5/6 there —
   so the ceiling crosses the bound somewhere in (0.50, 1.00).
5. A crossing comparison in the v0.15.0 style was considered and
   REJECTED before the run: the single-shot fidelity never exceeds
   5/6 anywhere on the grid, so a "first σ where it falls below
   5/6" is degenerate (it is already below at the first grid
   point). There is no restricted crossing σ* to compare against
   the unrestricted crossing (0.32 / 0.26 on seeds 42 / 7). The
   σ-dependence claim (lxxxi) replaces it.
6. The restricted and unrestricted fidelities have DIFFERENT
   targets by construction: the unrestricted (xlviii) fidelity is
   |⟨uniform|copy⟩|² (how well the copy reproduces the original
   uniform thought), while the restricted fidelity is
   |⟨presented|copy⟩|² (how well the reconstruction reproduces
   the state the copier was given). The restricted-vs-unrestricted
   table above is therefore REPORTED, not claimed: the numbers are
   comparable as "the model's copy fidelity at noise σ", but they
   are not the same measurement, and no claim in this build rests
   on equating them. Note the table's shape anyway: the restricted
   copier is far below the unrestricted copier at low σ (0.25 vs
   1.00 at σ = 0) and the two converge at high σ (0.35–0.58 vs
   0.41 at σ = 1.00) — at high σ both copiers are limited by the
   same noisy state, not by their access to it.

## Claims

### (lxxviii) Single-shot restricted copier respects the 5/6 bound at every σ

Mean single-shot restricted-copy fidelity (5 copies) ≤ 5/6 at
every σ on the grid. PASS iff this holds on EVERY seed in
{42, 7, 1234, 2026}. Frozen bar: 5/6 (the same bar claim
(xlviii) used, so the restricted and unrestricted copiers are
judged identically). Calibration: passes on both seeds (max mean
0.3998 / 0.5798).

### (lxxix) 16-shot reconstruction at σ = 0 exceeds the 5/6 bound

Mean 16-shot reconstruction fidelity at σ = 0 (20 copies) > 5/6.
PASS iff this holds on EVERY seed in {42, 7, 1234, 2026}. Frozen
bar: 5/6; frozen budget M = 16 shots (chosen in the pilot as the
smallest budget on the {1, 4, 16, 64, 256} grid that clears the
bound on both calibration seeds — M = 4 gives 0.5933 / 0.6178,
below the bound). Calibration: passes on both seeds (0.9526 /
0.9396).

### (lxxx) Measurement-budget gap at σ = 0 is ≥ 0.30

Mean fidelity at M = 64 minus mean fidelity at M = 1, at σ = 0
(20 copies), ≥ 0.30. PASS iff this holds on EVERY seed in
{42, 7, 1234, 2026}. Frozen bar: 0.30 (a round number; the
calibration gaps are 0.7378 / 0.7382). Calibration: passes on
both seeds.

### (lxxxi) The 16-shot leak is σ-dependent

Mean 16-shot reconstruction fidelity (20 copies) > 5/6 at
σ = 0.25 AND < 5/6 at σ = 1.00. PASS iff both legs hold on EVERY
seed in {42, 7, 1234, 2026}. Frozen bar: 5/6; frozen budget
M = 16 shots (the same budget as (lxxix)). Calibration: passes
on both seeds (0.9333 / 0.9365 at σ = 0.25; 0.8079 / 0.6331 at
σ = 1.00) — with the high-σ leg thin on seed 42 (margin 0.025).

## Seeds

- Calibration: 42, 7 (pilot tables and thresholds frozen from
  these only).
- Evaluation: 1234, 2026 (held out; first touched by the
  evaluation run after this file was written).

## What would falsify

- (lxxviii): any seed with a 5-copy mean single-shot fidelity
  > 5/6 at any σ.
- (lxxix): any seed with a 20-copy mean 16-shot fidelity at
  σ = 0 ≤ 5/6.
- (lxxx): any seed with a mean-fidelity gap M = 64 − M = 1 at
  σ = 0 < 0.30.
- (lxxxi): any seed with a 20-copy mean 16-shot fidelity ≤ 5/6
  at σ = 0.25, or ≥ 5/6 at σ = 1.00.
