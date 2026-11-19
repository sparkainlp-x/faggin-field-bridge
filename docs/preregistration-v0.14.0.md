# Pre-registration — v0.14.0: Synergy-vs-redundancy PID of the collaboration gap (claims (xl)–(xliii))

Written 2026-11-18, BEFORE the evaluation run on the held-out
seeds 1234 and 2026. Thresholds are round numbers frozen from
a calibration pilot on seeds 42 and 7 only. No threshold in
this file may be moved after the evaluation run.

## The spec being tested

Deep-think upgrade #5 (report.md §9): decompose the
+4.3352-bit joint-entropy collaboration gap by integrated
information decomposition (PID / ΦID: Luppi, Mediano,
Rosas et al., Nat. Neurosci. 2022/2024) into redundant,
unique, and synergistic components. The report's
falsifiable prediction: the gap is SYNERGY, not
redundancy — synergy rises with R and falls at σ = 0.50,
while redundancy is σ-robust. Falsified if synergy ≤ 0
while the gap is positive. This imports IIT's
DECOMPOSITION, not its contested Φ identity claim. Φ
(scalar) is NOT imported as a consciousness measure
(explicit do-not from the report, Cogitate 2025).

## The construction (fixed before the pilot)

- PID is defined for TWO sources, so the decomposition is
  of the PAIR-level gap: N = 2 agents (the thought-pair
  level at which concurrence and D are defined), not the
  N = 4 gap. The N = 4 sampled gap (+4.3352 bits at
  σ = 0.25, seed 42) is reported alongside as context,
  not decomposed. The pair gap (exact, seed 42,
  σ = 0.25: +2.2729 bits; sampled +2.2556) is the
  pair-level analogue of the same design-B mechanism.
- Target Y = the joint outcome (X1, X2): the PID then
  decomposes H(X1, X2) itself, so the arm difference
  ΔRed + ΔUniq1 + ΔUniq2 + ΔSyn equals the collaboration
  gap EXACTLY (up to floating-point error). Sources X1,
  X2 are the two agents' Born outcomes (4 concepts each).
- Redundancy is Williams & Beer I_min:
  Red = Σ p(x1,x2) · min(I(X1; Y=(x1,x2)), I(X2; Y=(x1,x2))),
  where the specific information of source i about the
  joint outcome y = (x1, x2) is −log2 p_i(x_i) (the
  outcome y determines x_i). Hence Red = E[−log2
  max(p1(X1), p2(X2))], Uniq_i = H(Xi) − Red, and
  Syn = H(X1,X2) − Uniq1 − Uniq2 − Red = Red − I(X1;X2).
  All four atoms are therefore computable exactly from
  the joint distribution; no sampling is involved in
  the PID itself.
- Joint distribution: EXACT pooled product distribution.
  The evolution replicates empathy_field.run_collaboration
  design B generation by generation (same population,
  same noise kicks, same field mix with coupling f for
  the collaborating arm, same Born-collapse for the
  isolated arm), but instead of sampling joint outcomes
  it pools the exact per-generation product Born
  distribution p1 ⊗ p2 over the 10 generations. The
  cross-check in claim (xl) pins the exact H against
  the sampled H from run_collaboration.
- Mean resonance R: the mean pairwise overlap squared
  R = |<ψ1|ψ2>|² of the collaborating arm's states AFTER
  the field mix, averaged over generations (R_post).
  The pre-mix R is reported alongside, not gated.
- Sigma grid: the bridge grid [0, 0.01, 0.05, 0.1, 0.25,
  0.5, 1.0] (te.SIGMA_GRID). Generations = 10 (empathy_field default).
  Design B throughout.

## Calibration pilot (seeds 42 and 7) — disclosed before the run

The pilot CONTRADICTS the spec's predictions on every
substantive point. This is disclosed here, not hidden:
the held-out evaluation tests whether the contradiction
generalizes.

- Identity holds: components sum to H_joint to < 1e-12
  on every (seed, sigma, arm); every atom ≥ −1e-9.
  Exact vs sampled H at σ = 0.25: seed 42 H_collab
  2.9948 exact vs 2.9775 sampled (diff 0.0173),
  H_isolated identical 0.7219; seed 7 H_collab 3.1409
  vs 3.1654 (diff 0.0245), H_isolated identical 1.4855.
- (xli) at σ = 0.25: seed 42 ΔSyn = +0.9248,
  ΔRed = +0.9453 (ΔSyn < ΔRed), ΔSyn/gap = 40.7%;
  seed 7 ΔSyn = +0.7103, ΔRed = +0.3376,
  ΔSyn/gap = 42.9%. Synergy is NOT the majority of the
  gap on either seed; the gap splits roughly equally
  between synergy, redundancy, and unique information
  (ΔUniq: +0.4027 seed 42, +0.6075 seed 7).
- Structural note: in the collaborating arm
  I(X1;X2) ≈ 0.01–0.04 bits (the two agents' outcomes
  are drawn independently given their states, so the
  states' correlation barely couples the outcomes),
  hence Syn = Red − I(X1;X2) ≈ Red on every sigma
  (e.g. seed 42 σ = 0.25: Syn 0.9248 vs Red 0.9453;
  σ = 1.0: Syn 1.6042 vs Red 1.6418). The I_min
  decomposition of the joint outcome CANNOT separate
  synergy from redundancy in this wiring: the two
  atoms differ only by the near-zero I(X1;X2). Any
  claim that the gap is "synergy, not redundancy"
  (or the reverse) is undecidable from these atoms
  alone — that degeneracy is itself the finding.
- (xlii): Pearson(Syn_collab, R_post) across the sigma
  grid is −0.2295 (seed 42) and −0.0404 (seed 7) —
  synergy does NOT rise with R. Syn_collab RISES from
  σ = 0.25 to σ = 0.50 (0.9248 → 1.2600 seed 42;
  0.9747 → 1.5409 seed 7), it does not fall.
- (xliii): ΔRed ratio 0.50/0.25 is 0.2351 (seed 42,
  fails the 0.5 bar) and 1.4455 (seed 7, passes).
  Redundancy's σ-robustness is seed-fragile.

## Claims

### (xl) PID identity and sampled cross-check

For every seed in {42, 7, 1234, 2026}, every sigma on
the grid, and both arms: Red + Uniq1 + Uniq2 + Syn =
H_joint within 1e-9 bits, and every atom ≥ −1e-9 bits.
AND at σ = 0.25 the exact H_collab and H_isolated agree
with the sampled run_collaboration (N = 2, design B)
values within 0.25 bits on every seed. PASS iff all of
this holds. Frozen tolerances: 1e-9 (identity, the
round number at floating-point scale) and 0.25 bits
(cross-check, ~10x the calibration diffs 0.017–0.025).

### (xli) The gap is synergy, not redundancy, at σ = 0.25

ΔSyn > ΔRed AND ΔSyn ≥ 0.5 · gap at σ = 0.25. PASS iff
this holds on EVERY seed in {42, 7, 1234, 2026}.
Frozen bar: 0.5 (synergy is the majority of the gap).
Calibration: fails on both seeds (seed 42 ΔSyn <
ΔRed; shares 40.7% and 42.9%).

### (xlii) Synergy rises with R and falls at σ = 0.50

Pearson(Syn_collab, mean R_post) across the sigma grid
≥ 0.5 AND Syn_collab(σ = 0.50) < Syn_collab(σ = 0.25).
PASS iff both hold on EVERY seed in {42, 7, 1234,
2026}. Frozen bar: 0.5 (the round correlation bar used
elsewhere in this repo). Calibration: fails on both
seeds (Pearsons −0.23, −0.04; synergy rises at 0.50).

### (xliii) Redundancy is σ-robust

ΔRed(σ = 0.50) ≥ 0.5 · ΔRed(σ = 0.25). PASS iff this
holds on EVERY seed in {42, 7, 1234, 2026}. Frozen
bar: 0.5 (the round robustness ratio used in claim
(xxii)). Calibration: fails seed 42 (ratio 0.2351),
passes seed 7 (ratio 1.4455).

## Seeds

- Calibration: 42, 7 (thresholds frozen from these only).
- Evaluation: 1234, 2026 (held out; first touched by the
  evaluation run after this file was written).

## What would falsify

- (xl): any atom sum deviating from H_joint by > 1e-9,
  any atom < −1e-9, or any exact-vs-sampled H mismatch
  > 0.25 bits at σ = 0.25.
- (xli): ΔSyn ≤ ΔRed, or ΔSyn < 0.5 · gap, at σ = 0.25
  on any seed. (Also: synergy ≤ 0 while the gap is
  positive would falsify the spec's prediction in its
  strongest form; the pilot shows synergy is positive
  but not dominant.)
- (xlii): Pearson < 0.5, or Syn_collab not falling at
  σ = 0.50, on any seed.
- (xliii): ΔRed ratio 0.50/0.25 < 0.5 on any seed.
