# Pre-registration — v0.13.0: Kuramoto bounded-coherence scan (claims (xxxvi)–(xxxix))

Written 2026-11-18, BEFORE the evaluation run on the held-out
seeds 1234 and 2026. Thresholds are round numbers frozen from
a calibration pilot on seeds 42 and 7 only. No threshold in
this file may be moved after the evaluation run.

## The spec being tested

Deep-think upgrade #4 (report.md §9): replace fixed coupling
with a Kuramoto scan over coupling K and noise sigma; compute
order parameter R_K, joint entropy, quale count, and A.
Prediction: inverted-U in joint entropy / quale count vs K and
vs sigma, with interior optimum (not at K_max or sigma = 0);
hypersynchrony (R_K -> 1) reduces joint entropy / quale count
(dimensional collapse); optimum sigma* > 0. Predict the
optimum R_K band BEFORE the scan and compare with f* = 0.7278.
The band R ~ 0.5-0.8 is the Phillips 2026 preprint hypothesis
(Zenodo, not peer-reviewed): a prediction to test, not an
established fact.

## The construction (fixed before the pilot)

- Standard Kuramoto: N = 8 oscillators, omega_i ~ N(0, 1),
  initial phases uniform on [0, 2pi), Euler-Maruyama dt = 0.05,
  T = 40, first half discarded as transient. R_K = mean
  |<exp(i theta)>| over the steady window.
- Wiring: each agent's state is the (xxxiv) slide state at its
  phase RELATIVE to the field mean, phi_i = ((theta_i -
  theta_bar) mod 2pi) / 4, theta_bar the circular mean phase.
  Only relative phases carry information (global rotation is a
  gauge freedom of the Kuramoto model). At full sync every
  agent sits at phi = 0 (uniform thought, D = 1, C = 0); at
  K = 0 the phases spread over the whole slide.
- Quale count: existing qualia_count(states) (R >= 0.5,
  nu >= 0.10). Joint entropy: exact independent-draw joint
  entropy, sum of per-agent Born entropies (no sampling cap).
  Gap A: paired arms mirroring run_collaboration design B —
  collaborating mixes at coupling R_K, isolated
  Born-collapses once; A = H_collab - H_isolated. In the
  single-shot measurement H_isolated = 0 exactly, so
  A = H_collaborating; that triviality is reported, not hidden.
- K grid [0, 0.5, 1.0, 1.6, 2.5, 4.0, 8.0] (K_c ~ 1.6 for
  Gaussian frequencies); sigma grid [0, 0.05, 0.1, 0.25,
  0.5, 1.0].

## Calibration pilot (seeds 42 and 7) — disclosed before the run

The pilot CONTRADICTS the spec's predictions on several
points. This is disclosed here, not hidden: the held-out
evaluation tests whether the contradiction generalizes.

- R_K works: 0.29 -> 0.99 (seed 42), 0.35 -> 1.00 (seed 7)
  across the K grid; the Kuramoto transition is at K ~ 1.6-2.5.
- Quale count vs K (sigma = 0): seed 42: 8, 13, 6, 6, 6, 6, 6
  (peak at K = 0.5, margins 5 vs K = 0 and 7 vs K = 8);
  seed 7: 18, 7, 12, 7, 6, 6, 6 (peak at K = 0). The count
  falls to a floor of 6, not to zero; the interior peak is
  seed-fragile (1 of 2 seeds).
- Joint entropy vs K: flat. Seed 42: 12.44, 11.69, 12.02,
  11.68, 12.02, 12.02, 12.01 (peak at K = 0). Seed 7: 10.67,
  11.67, 11.41, 12.15, 11.98, 12.00, 12.00 (peak at K = 1.6,
  margin 0.15 vs K = 8). No inverted-U: the per-agent Born
  entropy averages ~1.5 bits whatever K is.
- Gap A vs K: large positive (+10.3 to +12.2 bits) and flat
  (seed 42 range 1.26 bits, seed 7 range 0.99 bits). No
  inverted-U; hypersynchrony does not reduce A in this
  wiring (A = H_collaborating, which tracks the mixed
  states' entropy).
- R_K at the count peak: 0.31 (seed 42, K = 0.5), 0.35
  (seed 7, K = 0) — both OUTSIDE the Phillips band [0.5, 0.8].
- Sigma scan at fixed K = 1.0: seed 42 counts 6, 6, 7, 16,
  10, 18 (peak at sigma = 1.0, the grid edge); seed 7
  counts 12, 10, 17, 5, 6, 10 (peak at sigma = 0.10,
  margin 5 vs sigma = 0). The counts swing wildly (5-18)
  with no stable optimum; sigma* is not stable across seeds.

## Claims

### (xxxvi) Inverted-U in quale count vs K (sigma = 0)

The count peaks at an INTERIOR grid point (0 < K < 8.0) and
exceeds both ends by at least 3 counts:
count(K_peak) - count(K = 0) >= 3 AND count(K_peak) -
count(K = 8.0) >= 3. PASS iff this holds on EVERY seed in
{42, 7, 1234, 2026}. Frozen margin: 3 is the round number
below the seed-42 pilot margins (5, 7).

### (xxxvii) Inverted-U in joint entropy vs K (sigma = 0)

H_joint peaks at an INTERIOR grid point and exceeds both
ends by at least 0.5 bits. PASS iff this holds on EVERY
seed in {42, 7, 1234, 2026}. Frozen margin: 0.5 bits is
the round number below the seed-7 pilot margin vs K = 0
(1.48 bits); the seed-7 margin vs K = 8 is only 0.15 bits.

### (xxxviii) Optimum R_K band

R_K at the count peak (the K where the count is maximal;
ties broken by the smallest such K) lies in [0.5, 0.8],
the Phillips band. PASS iff this holds on EVERY seed in
{42, 7, 1234, 2026}. f* = 0.7278 is reported alongside
for comparison, not as a target. The band is the spec's
prediction, not a calibrated threshold.

### (xxxix) Stochastic resonance: optimum sigma* > 0

At fixed K = 1.0 (near the critical coupling, where noise
matters most — fixed before the pilot), the count peaks at
a STRICTLY INTERIOR sigma (0 < sigma* < 1.0) and exceeds
the sigma = 0 count by at least 3: count(sigma*) -
count(sigma = 0) >= 3. PASS iff this holds on EVERY seed
in {42, 7, 1234, 2026}. Frozen margin: 3 counts, the
round number below the seed-7 pilot margin (5).

The gap A is computed and reported on every scan but is
NOT gated by any claim: the pilot shows it is flat, and
gating a claim on a flat quantity would be testing the
pilot, not the spec.

## Seeds

- Calibration: 42, 7 (thresholds frozen from these only).
- Evaluation: 1234, 2026 (held out; first touched by the
  evaluation run after this file was written).

## What would falsify

- (xxxvi): count peak at K = 0 or K = 8.0, or a peak that
  does not exceed an end by 3, on any seed.
- (xxxvii): H_joint peak at an end, or a peak that does not
  exceed an end by 0.5 bits, on any seed.
- (xxxviii): R_K at the count peak outside [0.5, 0.8] on
  any seed.
- (xxxix): count peak at sigma = 0 or sigma = 1.0, or a
  peak that does not exceed the sigma = 0 count by 3, on
  any seed.
