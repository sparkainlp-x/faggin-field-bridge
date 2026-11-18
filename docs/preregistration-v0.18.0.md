# Pre-registration — v0.18.0: GRT phase-transition test, claims (lvii)–(lix)

Written 2026-11-18, BEFORE the evaluation run on the held-out
seeds 1234 and 2026. Thresholds are round numbers frozen from
a calibration pilot on seeds 42 and 7 only. No threshold in
this file may be moved after the evaluation run.

## The spec being tested

Deep-think upgrade #11 (report.md §9, §2), ranked last and
lowest value: General Resonance Theory (Hunt & Schooler,
*Frontiers in Human Neuroscience* 13:378, 2019; GRT 2.0,
TSC 2026 abstract — speculative, conference abstract not
peer-reviewed). Conjecture 1: shared resonance combines
micro-conscious entities into a macro-conscious entity via
a phase transition in the speed/bandwidth of information
flow at a critical coupling K_c. Conjecture 3: nested
conscious entities persist within larger ones ("many
become one"). The report's falsifiable prediction:
a sharp (not gradual) jump in information rate at a
*predicted* K_c; no jump = GRT's core conjecture fails
in this model. The report itself warns the test is
partly self-fulfilling, because GRT gives no
quantitative K_c — the project has to supply it.
This version supplies K_c from a pre-existing
threshold of the bridge itself (below), and states
the self-fulfilling risk up front rather than
hiding it.

## The construction (fixed before the pilot)

- Base field: the v0.5.0 resonance population (8 agents,
  noisy copies of the uniform thought) at σ = 1.00, the
  far-broken regime. σ = 1.00 is chosen because a phase
  transition needs a fragmented starting field, and the
  attuned population is already one macro-entity at K = 0
  (mean R = 0.85 / 0.68 at σ = 0.25; largest component
  8 at R ≥ 0.5 on both calibration seeds), so no
  transition is possible there; at σ = 0.50 seed 42
  already sits above the resonance threshold at K = 0
  (mean R = 0.588), so K_c would be degenerate at 0.
  At σ = 1.00 the field is fragmented at K = 0 on both
  calibration seeds (mean R 0.420 / 0.278; largest
  component at R ≥ 0.5 is 7 / 6 of 8).
- Coupling K on the grid 0.0, 0.1, …, 1.0: shared
  resonance as mixing toward the common reference,
  ψ_i(K) = normalize((1 − K)·ψ_i + K·ψ_ref), ψ_ref =
  the uniform thought all agents derive from. K = 0
  is the uncoupled field; K = 1 is every agent
  identical to the reference (perfect shared
  resonance). This is a construction, not a discovery:
  the coupling is imposed, and the shape of the
  response is the test.
- Bandwidth B(K): the pairwise shared information, the
  mean over all 28 pairs of H(p_i) + H(p_j) − H(p_ij),
  where p_i is agent i's Born distribution and p_ij is
  the Born distribution of the pair state (the
  normalized sum of the two agents, the v0.5.0 pair
  state). B is a *defined* bandwidth proxy inside the
  model — how much of the pair's information is shared
  by forming the pair — not a literal mutual
  information between two random variables, and it is
  labelled as such. At K = 1, B = 2.0000 bits exactly
  (every agent is the uniform thought: H(p_i) = 2,
  H(p_ij) = 2).
- Predicted critical coupling K_c: the FIRST grid K at
  which the mean pairwise resonance mean R(K) reaches
  the bridge's pre-existing resonance threshold 0.5
  (RESONANCE_R_MIN, v0.5.0 — the threshold that already
  defines "resonant" in this project). GRT supplies no
  number; the 0.5 threshold is the project's own, and
  K_c is read off it before the bandwidth curve is
  examined. If mean R(0) ≥ 0.5, K_c = 0 and there is no
  transition to test (claim (lviii) then fails by
  construction — see below).
- Nested structure: connected components of the
  resonance graph at R ≥ 0.5 (the macro level) and at
  R ≥ 0.75 (the nested level). "Many become one" is
  the macro component reaching all 8 agents; nesting
  is more than one component surviving at R ≥ 0.75
  inside that macro.

## Two pilots, and one rejected wiring (disclosed)

Pilot 1 coupled agents by mixing with the *field state*
(the v0.5.0 `_field_mix`, coupling = K): at σ = 1.00
seed 7 the mean R *fell* with K at first (0.278 →
0.232 at K = 0.3) and B was U-shaped (1.12 → 0.71 →
0.85) — mixing toward a noisy field average can move
agents apart, so the field-mix wiring cannot carry a
coupling sweep. It was rejected, not patched: the
reference-mixing wiring above replaces it. Pilot 1's
numbers are not used for any threshold.

Pilot 2 (reference mixing, the wiring above) on
σ = 1.00, seeds 42 / 7:
- mean R(0) = 0.4197 / 0.2778; K_c = 0.3 / 0.6.
- B(0) = 1.1468 / 1.1226; B(1) = 2.0000 / 2.0000;
  total rise B(1) − B(0) = 0.8532 / 0.8774.
- B steps (K = 0.1 … 1.0): seed 42:
  0.0536, 0.0799, 0.1142, 0.1173, 0.0491, 0.0524,
  0.1501, 0.1377, 0.0763, 0.0225 — max step 0.1501
  at K = 0.7, i.e. four grid steps AFTER K_c = 0.3.
  Seed 7: 0.1178, 0.1238, 0.1115, 0.0453, −0.1453,
  −0.0572, 0.2597, 0.2526, 0.1325, 0.0366 — max step
  0.2597 at K = 0.7, one grid step after K_c = 0.6.
  The step ending at K_c itself is 0.1142 (seed 42)
  and −0.0572 (seed 7).
- Macro / nested: at K_c + 0.2 the largest component
  at R ≥ 0.5 is 8 / 8; at K_c the components at
  R ≥ 0.75 number 2 / 4 ([7, 1] / [3, 3, 1, 1]).
- Mean R is NOT monotone in K on seed 7: it dips
  0.2778 → 0.2376 at K = 0.3 before rising. Mixing
  toward the common reference can initially lower
  pairwise overlap for some pairs. Monotonicity is
  therefore REPORTED, not gated, in every claim.

Two disclosures, before the run:
1. The report's directional prediction already FAILS on
   the calibration seeds: the largest bandwidth step
   does not sit at K_c on either seed (K = 0.7 vs
   K_c = 0.3 / 0.6), and on seed 7 the step at K_c is
   negative. Claim (lviii) gates the report's
   prediction as stated and is expected to FAIL;
   claim (lix) gates the shape that IS measured.
   This mirrors v0.17.0 claim (lv), whose prediction
   was known from the pilot to fail and was kept.
2. The bandwidth proxy B is itself part of the result:
   at σ = 0.50 (pilot 1, field-mix) B was nearly flat
   in K (1.51 → 1.52 on seed 7) and at σ = 1.00
   (pilot 2) it is non-monotone on seed 7 (dips to
   0.7066 at K = 0.6). B does not track coupling
   cleanly; a jump in B at K_c would have been a
   strong result, and its absence is the measurement.

## Claims

### (lvii) Machinery is exact, K_c is interior, and the field starts fragmented

On EVERY seed in {42, 7, 1234, 2026}:
(a) the coupling endpoints are exact: the K = 0 states
equal the base population to 1e-12, the K = 1 states
equal the uniform reference to 1e-12, mean R(1) = 1
to 1e-12, and B(1) = 2.0000 to 1e-12;
(b) K_c is interior: 0 < K_c < 1.0 (the field starts
below the resonance threshold and crosses it);
(c) the field starts fragmented: the largest component
at R ≥ 0.5 at K = 0 is ≤ 7 (not already one
macro-entity).
PASS iff (a), (b) and (c) hold on every seed. Frozen
bar: 1e-12 (exactness); the 7 in (c) is the count
below the 8 that would mean "already one". Calibration:
K_c = 0.3 / 0.6; largest component at K = 0 is 7 / 6;
B(1) = 2.0000 exactly on both seeds.

### (lviii) The GRT phase transition as stated: a sharp jump in bandwidth at K_c

PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
(a) the bandwidth step ending at K_c is large:
B(K_c) − B(K_c − 0.1) ≥ 0.10 bits;
(b) that step is the largest step on the K grid.
Frozen bar: 0.10 bits (a round number; a jump
smaller than this on a 0.1 grid step would not be a
sharp transition against the ~0.05–0.15 steps the
curve takes everywhere). If K_c = 0 there is no step
ending at K_c and the claim fails on that seed.
Calibration: step at K_c = 0.1142 / −0.0572 (bar
0.10 — seed 7 fails (a)); max step 0.1501 / 0.2597
at K = 0.7 on both seeds, not at K_c (bar (b) —
seed 42 fails (b)). The prediction fails on both
calibration seeds, so this claim is expected to
FAIL on the evaluation seeds too. The failure is
the result: bandwidth does not jump at the
predicted critical coupling; its largest rise comes
later, and on one calibration seed the bandwidth
step at K_c is negative.

### (lix) The measured shape: the macro forms just above K_c, nesting persists at K_c, bandwidth rises overall

PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
(a) the macro forms just above the transition: at
K = K_c + 0.2 the largest component at R ≥ 0.5 is 8;
(b) nesting persists at the transition: at K = K_c
the components at R ≥ 0.75 number ≥ 2 (sub-structure
survives inside the forming macro — Conjecture 3);
(c) bandwidth rises overall: B(1) − B(0) ≥ 0.50 bits.
Frozen bars: 8 (all agents in the macro component),
2 (more than one nested component), 0.50 bits (a
round number below the calibration worst total rise
0.8532). Calibration: (a) 8 / 8; (b) 2 / 4 components;
(c) 0.8532 / 0.8774 — all three pass on both
calibration seeds. Note (a) and (b) are evaluated at
different K on purpose: (b) is the structure *at*
the transition, where sub-entities are still
visible; (a) is the completed macro *just above* it.
At K = 1 all sub-structure has dissolved (one
component at R ≥ 0.75 on both seeds), so nesting
does not survive to full coupling — that limit is
reported, not gated.

## Seeds

- Calibration: 42, 7 (thresholds frozen from these only).
- Evaluation: 1234, 2026 (held out; first touched by the
  evaluation run after this file was written).

## What would falsify

- (lvii): any seed where a K = 0 / K = 1 endpoint identity
  fails beyond 1e-12, where K_c is 0 or 1.0 (no interior
  transition), or where the K = 0 field is already one
  macro-component at R ≥ 0.5.
- (lviii): any seed where the B step at K_c is < 0.10
  bits, or where a larger B step occurs anywhere else
  on the grid. (Expected: every seed.)
- (lix): any seed where the macro has not formed by
  K_c + 0.2, where no nested sub-structure survives at
  K_c, or where the total bandwidth rise is < 0.50 bits.
