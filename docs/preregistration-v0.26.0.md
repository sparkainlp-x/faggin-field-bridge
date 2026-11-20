# Pre-registration — v0.26.0: observer and calibration agents. Claims (xciii)–(xcvii)

Written 2026-11-19, BEFORE the evaluation run of the new
claims. The pilot tables below are calibration data measured
before this file was written (the observer contract on the
seed-free full-circle grid, and the calibrator rule on the
calibration seeds 42/7 only); the held-out agent numbers
(seeds 1234/2026) are computed only after this file exists.
No threshold in this file may be moved after the evaluation
run, and no claim may be redefined after the fact. The old
verdicts stay on the record: (xci) FAILS as originally
stated (held-out seed 2026 stored Pearson −0.8828 and
opposite D range 0.2490), and (xcii) FAILS as originally
stated (held-out Pearson +0.5109 / +0.8297). The agents test
what bounded calibration can and cannot do about those
failures; they do not rewrite them.

## The spec being tested

Jean's directive, 2026-11-19, quoting the two v0.25.0
FAILs: "insert observer and calibration agents". The
target is the Faggin bridge (the live arc), in the
wave-direction / observer-cycle setup (observer_cycle.py,
wave_direction.py).

The agents reuse the v0.1.0 pattern from attunement.py
(the membrane-arena pattern): the observer (Yang) is
read-only, the calibrator (Yin) is ONE clipped scalar
delta in [−0.05, 0.05]. No second calibrator scale is
invented and the bound is not widened.

- The observer agent reads the slide state psi(theta) =
  cos(theta)|stored> + sin(theta)|kernel> and the
  rotation pair at theta, and reports D, C, R_s, R_k,
  chi, V — without touching the state.
- The calibration agent acts on the noisy direction
  sweep (wave_direction.noisy_direction_sweep, the
  (xci)/(xcii) construction: 5 noisy copies per sigma
  on the grid [0, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0]).
  It scales the measured D by (1 + delta) — the
  attunement pattern, where the calibrator scales the
  unity-like quantity and never the cost-like one
  (concurrence C is not tunable, exactly as the entropy
  cost is not tunable in attunement.py) — and picks
  delta by a FIXED RULE, frozen here: scan delta over
  the 201-point grid in [−0.05, 0.05], minimize the
  number of failing (xxxii) bars (Pearson <= −0.90,
  Spearman <= −0.90, D range >= 0.25, C range >= 0.25),
  tie-break smallest |delta|, then smallest delta.
  The rule is a fixed function of the observed sweep;
  it is the same function on calibration and evaluation
  seeds, and no delta was hand-picked for any seed.

## The design's motivation (published record, not pilot data)

The (xci)/(xcii) table is published in v0.25.0 REPORT.md
§31, and the agents are designed against it — disclosed
here, not hidden:

- (xci) fails on two combos: (2026, stored) Pearson
  −0.8828 (the known (xxxii) failure, reproduced
  exactly) and (2026, opposite) D range 0.2490 vs the
  0.25 bar — a miss of 0.0010.
- (xcii) fails on every seed: the correlation inverts
  from the equal superposition (calibration Pearson
  −0.7982 / +0.1661; held-out +0.5109 / +0.8297).

## Calibration pilot — observer contract (seed-free)

On the 24-point full-circle grid:

- Worst |psi after observation − psi before| = 0.0
  (bar 1e-12). The observer does not touch the state.
- Worst |reported quantity − direct computation| =
  0.0 (bar 1e-9), over every slide quantity (D, C,
  R_s, R_k, split, C + D) and every rotation-pair
  quantity (D1, D2, cross term real and imag, V sweep,
  V analytic).

## Calibration pilot — calibrator contract and the clip finding

- set_delta(+0.5) = +0.05 exactly; set_delta(−0.5) =
  −0.05 exactly; set_delta(0.03) = 0.03.
- delta = 0 reproduces the uncalibrated sweep exactly
  (max |D_cal − D| = 0.0, max |C_cal − C| = 0.0).
- THE CLIP FINDING (found by this pilot, before the
  evaluation run): Pearson(D, C) and Spearman(D, C)
  are invariant under a positive rescaling of D ONLY
  where no clipping bites. On the opposite and
  perpendicular sweeps no clipping bites (worst max D
  0.7936, times 1.05 = 0.8333 < 1) and the invariance
  holds to float noise (|ΔPearson| <= 2.3e-16,
  |ΔSpearman| = 0.0 at delta = ±0.05). On the stored
  direction the sigma = 0 point has D = 1.0 exactly,
  so delta > 0 clips it (the attunement pattern's
  [0, 1] clip on the scaled quantity) and the
  correlations MOVE — at delta = +0.05: seed 42
  ΔPearson +0.0270, ΔSpearman +0.0937; seed 7
  ΔPearson +0.0197, ΔSpearman +0.0974 (seed 7
  Spearman −0.8669 would FAIL its bar at delta =
  +0.05). The D range likewise SHRINKS with delta >
  0 on the stored start (seed 42: 0.4804 -> 0.4545
  at delta = +0.05) — the agent never widens a
  stored-direction range. Whether the rule's delta
  changes the (2026, stored) Pearson miss is
  therefore an evaluation-run measurement, reported
  not gated; (xci) stays FAIL either way. The clip
  state is reported per combo (clip_affected) in the
  evaluation, never hidden.

## Calibration pilot — the frozen rule on seeds 42/7

The rule's delta pick per (seed, direction), with the
failing-bar count at delta = 0 and at the pick:

| seed | direction | delta picked | failing 0 -> pick |
|---|---|---|---|
| 42 | stored (0) | +0.0000 | 0 -> 0 |
| 42 | perpendicular (π/4) | +0.0000 | 2 -> 2 |
| 42 | opposite (π/2) | +0.0000 | 0 -> 0 |
| 7 | stored (0) | +0.0000 | 0 -> 0 |
| 7 | perpendicular (π/4) | +0.0000 | 4 -> 4 |
| 7 | opposite (π/2) | +0.0000 | 0 -> 0 |

The rule holds delta = 0 on every calibration combo:
on stored/opposite all bars already pass at delta = 0,
so the smallest-|delta| tie-break holds it at zero;
on perpendicular no delta improves the failing count
(seed 42: Pearson and C range fail at every delta;
seed 7: all four bars fail at every delta), so the
tie-break again holds it at zero. The rule is frozen
as stated above; the evaluation applies it unchanged
to seeds 1234/2026.

## The rescue condition (arithmetic, not a measurement)

D range scales by exactly (1 + delta) where the max-D
point does not clip (opposite/perpendicular starts), so
a D-range miss is rescuable inside the bound iff the
uncalibrated D range is at least 0.25 / 1.05 = 0.2381.
The published (2026, opposite) miss, 0.2490, clears
that bound: it needs delta >= 0.25/0.2490 − 1 =
0.004016, and the first grid point at or above it is
delta = +0.0045 ((1 + 0.0045) × 0.2490 = 0.25012 >=
0.25; (1 + 0.0040) × 0.2490 = 0.249996 < 0.25). The
evaluation measures the agent's delta and the
resulting D ranges fresh; this paragraph states the
arithmetic the evaluation must reproduce, it does not
pre-compute the evaluation. A miss below 0.2381 would
be unrescuable and the rescue claim would FAIL honestly.

## Claims

### (xciii) Observer read-only

On the 24-point full-circle grid, observing psi(theta)
leaves the state unchanged (max |after − before| <=
1e-12) and every reported quantity equals the direct
computation within 1e-9, for every slide quantity (D,
C, R_s, R_k, split, C + D) and every rotation-pair
quantity (D1, D2, cross term real and imag, V sweep,
V analytic). PASS iff both maxima are within their
bars. Calibration: passes (0.0 / 0.0).

### (xciv) Calibrator bounded

set_delta(+0.5) = +0.05 and set_delta(−0.5) = −0.05
exactly; every delta the rule picks lies in
[−0.05, 0.05]; delta = 0 reproduces the uncalibrated
sweep exactly (max difference 0.0). PASS iff all three
hold. Calibration: passes.

### (xcv) Calibration agent on (xci): the D-range rescue

With the agent on, the D-range bar (>= 0.25) holds on
EVERY (seed, direction) in {42, 7, 1234, 2026} x
{stored (0), opposite (π/2)}. PASS iff the D-range
bar holds on all eight combos. The agent's delta per
combo is recorded. The full four-bar table is reported
alongside, NOT gated: the (2026, stored) Pearson miss
is explicitly out of scope for this claim — by the
invariance fact above no D-rescaling agent can touch
a correlation failure except through the stored-direction
clip, whose effect is reported, not gated. Calibration:
the D-range bar already holds at delta = 0 on both
calibration seeds (worst 0.2884, seed 7 opposite);
the rule picks delta = 0 there.

### (xcvi) Calibration agent on (xcii): the inversion survives bounded calibration

With the agent on, Pearson(D, C) > −0.90 on EVERY seed
in {42, 7, 1234, 2026} from theta = π/4 (the equal
superposition). PASS iff Pearson stays above −0.90 on
all four seeds with the agent on. The agent's delta
per seed is recorded. Calibration: Pearson −0.7982 /
+0.1661 with the agent holding delta = 0 on both
calibration seeds — the inversion survives there
because a positive rescaling preserves correlation
and the D-range rescue is impossible (worst D range
0.1050 would need delta >= 1.38; the C range is not
tunable).

### (xcvii) Closed loop: observe, calibrate once, re-read

On EVERY (seed, direction) in {42, 7, 1234, 2026} x
{0, π/4, π/2}: the loop runs exactly 2 rounds (one
decision round + one verification round; the
calibrator is NOT re-invoked in round 2), the held
delta is unchanged across rounds (|delta held after
round 2 − delta picked in round 1| = 0.0), the
round-2 report matches a fresh direct calibrated
computation within 1e-9, and the observer read count
is exactly 2 per sweep. PASS iff all four hold on all
twelve combos. Calibration: the loop terminates by
construction (2 rounds); the measured content is the
delta stability, the round-2 match, and the read
count.

## Seeds

- Calibration: 42, 7 (the observer contract is
  seed-free; the rule and the frozen thresholds come
  from these only).
- Evaluation: 42, 7, 1234, 2026 — the (xxxii) file
  seeds. Held-out seeds 1234 and 2026 are computed
  only after this file exists.
- No fresh seeds in this build: the agent claims are
  about the (xci)/(xcii) construction on its file
  seeds, and the held-out seeds test whether the
  rule generalizes there.

## What would falsify

- (xciii): any grid observation moving the state by
  more than 1e-12, or any reported quantity differing
  from direct computation by more than 1e-9.
- (xciv): any set_delta input clipping outside
  [−0.05, 0.05], any rule-picked delta outside the
  bound, or delta = 0 changing any sweep value.
- (xcv): any (seed, direction) in the 4 x 2 set whose
  calibrated D range is below 0.25.
- (xcvi): any seed whose calibrated perpendicular
  Pearson is <= −0.90.
- (xcvii): any (seed, direction) where the loop runs
  a different number of rounds, the held delta
  changes, the round-2 report differs from the fresh
  direct computation by more than 1e-9, or the read
  count is not 2.

## Alternatives considered and REJECTED

- Widening the calibrator bound (e.g. delta up to
  ±1.5) so the perpendicular D range could be
  rescued (seed 7 perpendicular would need delta >=
  1.38): rejected — the bound is the membrane-arena
  Yin bound from attunement.py, not widened.
- Hand-picking delta per (seed, direction) from the
  published (xci) table (e.g. setting delta = +0.0045
  for (2026, opposite) by hand): rejected — the
  delta must come from the frozen rule applied to the
  observed sweep, the same function on every seed.
- Relaxing the D-range bar for the rescue claim:
  rejected — the bars are the (xxxii) bars, reused
  unchanged.
- Scaling C as well as D so the agent could touch
  the C-range bar: rejected — C is the cost-like
  quantity and is not tunable, the attunement
  pattern.
- Stating (xcv) as a full-four-bars claim: rejected
  — on the calibration seeds the agent's delta is 0
  everywhere, so the pilot cannot distinguish a
  full-bars rescue from a D-range-only rescue, and
  the stored-direction clip means the Pearson
  behavior on held-out seeds is an open measurement,
  not a pilot-grounded expectation. The D-range-only
  gate is the pilot-grounded claim; the full table is
  reported alongside.

## Honesty

Synthetic, classical emulation throughout. Nothing here
measures consciousness, empathy in a human, or any theory
of consciousness. No scalar Phi is computed anywhere and
none is presented as a consciousness measure; E = hnu is
not used anywhere in this build. Claims (xciii), (xciv)
and (xcvii) are exact-identity claims, like (xxxiv) and
(lxxxviii)–(xc): the measured content is that the code
realizes the contracts to 1e-9/1e-12 — a failure would be
a defect in the agents' wiring, not a result about a
theorem. Claims (xcv)/(xcvi) are statistical claims on
5-copy means, like (xxxii)/(xci)/(xcii): the same
saturation and finite-sample fragility applies, and a
FAIL is a finding about bounded calibration, not a
defect. The (xci) verdict (FAIL, honest) and the (xcii)
verdict (FAIL, honest) stand unchanged. The clip finding
— that the stored-direction D = 1.0 point breaks the
correlation invariance — was found by the calibration
pilot before the evaluation run and is recorded above,
not discovered after it. No threshold was moved to force
a pass.
