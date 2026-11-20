# Pre-registration — v0.25.0: the wave direction — opposite and perpendicular, all possible directions. Claims (lxxxviii)–(xcii)

Written 2026-11-19, BEFORE the evaluation run of the new
claims. The pilot tables below are calibration data measured
before this file was written (the exact full-circle sweeps,
which are seed-free, and the noisy direction sweep on the
calibration seeds 42/7 only); the held-out noisy numbers
(seeds 1234/2026) are computed only after this file exists.
No threshold in this file may be moved after the evaluation
run, and no claim may be redefined after the fact. The old
verdicts stay on the record: (xxxii) FAILS as originally
stated (held-out seed 2026 Pearson −0.8828), and (xxxv)
FAILS as originally stated (fresh seeds 5/99).

## The spec being tested

Jean's directive, 2026-11-19: check the opposite wave
direction and the perpendicular wave direction — all
possible directions — under "do all logic for maximum
scientific outcomes". The target is the Faggin bridge (the
live arc), grounded in his Matrix logic (2026-11-18): the
observer facing the opposite direction is necessary for
the self-cycle of self-knowing.

The wave direction in the code is the angle theta in the
{stored, kernel} plane, in two places that already exist:

- the slide state psi(theta) = cos(theta)|stored> +
  sin(theta)|kernel> (observer_cycle.slide_state), run
  before only on theta in [0, pi/2];
- the rotation pair psi1 = cos(theta) q1 + sin(theta) k1,
  psi2 = -sin(theta) q1 + cos(theta) k1
  (cascade.rotation_pair), run before only on theta in
  {pi/12, pi/8, pi/6, pi/4}.

This build sweeps theta over the full circle [0, 2 pi) on
a 24-point grid (every 15 degrees) and asks what the wave
does at theta + pi (opposite) and theta + pi/2
(perpendicular).

## The exact structure (derivable by hand, verified in code)

Slide: D(theta) = cos^2(theta), C(theta) = sin^2(theta),
R_s(theta) = cos^2(theta), R_k(theta) = sin^2(theta),
R_s - R_k = cos(2 theta), C + D = 1. Rotation pair:
D1(theta) = cos^2(theta), D2(theta) = sin^2(theta),
cross term chi(theta) = -sin(theta) cos(theta)
= -(1/2) sin(2 theta), V(theta) = |sin(2 theta)|.

- Opposite (theta + pi): cos^2 and sin^2 are unchanged,
  so EVERY slide and rotation-pair quantity is identical
  — the wave returns to itself, up to a global phase
  of -1. The self-cycle closes.
- Perpendicular (theta + pi/2): cos^2 and sin^2 swap,
  so the slide swaps D with C and R_s with R_k, and the
  rotation pair swaps D1 with D2 and flips the sign of
  chi, while |chi| and V are unchanged. The perpendicular
  direction knows the opposite pattern.
- The signed cross term has four lobes: zero at every
  multiple of pi/2, extrema +/-0.5 at odd multiples of
  pi/4; V peaks at 1.0 at theta = pi/4 + k pi/2 and
  vanishes at theta = k pi/2.
- The rotation cascade: off-axis (theta not a multiple of
  pi/2) both projected vectors are parallel to q1 (rank 1),
  so the pair is gone from stage 2 and V = 0 from stage 2
  on, exactly as in claim (vi); on-axis one member
  projects to zero, so V = 0 already at stage 1 and no
  pair exists.

## Calibration pilot — exact sweeps (seed-free)

Worst differences over the 24-point grid (all within
1e-9; the largest are float noise at 1e-15):

- Opposite shift: worst 1.22e-15 (slide D).
- Perpendicular shift: worst 1.78e-15 (slide D swap).
- Cross-term profile: worst |chi + (1/2) sin 2theta| =
  1.67e-16, worst |V - |sin 2theta|| = 3.33e-16,
  zeros at 0, pi/2, pi, 3pi/2, extrema at pi/4, 3pi/4,
  5pi/4, 7pi/4, max |chi| = 0.5000.
- Cascade by direction: off-axis V_1 = |sin 2theta|
  (0.5 / 0.8660 / 1.0 at pi/12 / pi/6 / pi/4 and their
  rotations), V_k = 0 for every stage k >= 2, pair gone
  from stage 2; on-axis (0, pi/2, pi, 3pi/2) V_1 = 0
  and no pair from stage 2.

## Calibration pilot — noisy direction sweep (seeds 42/7 only)

The same noise model and construction as
self_knowing.self_knowing_sweep (5 noisy copies per
sigma on the grid [0, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0]),
with the uniform thought replaced by the slide state
psi(theta). Bars are the (xxxii) bars, reused for the
same construction: Pearson <= -0.90, Spearman <= -0.90,
D range >= 0.25, C range >= 0.25.

| seed | direction | D(σ=0) | C(σ=0) | Pearson | Spearman | D range | C range |
|---|---|---|---|---|---|---|---|
| 42 | stored (0) | 1.0000 | 0.0000 | −0.9570 | −1.0000 | 0.4804 | 0.6133 |
| 42 | perpendicular (π/4) | 0.5000 | 0.5000 | −0.7982 | −0.9643 | 0.2936 | 0.2183 |
| 42 | opposite (π/2) | 0.0000 | 1.0000 | −0.9987 | −1.0000 | 0.4380 | 0.7789 |
| 7 | stored (0) | 1.0000 | 0.0000 | −0.9397 | −0.9643 | 0.5370 | 0.5110 |
| 7 | perpendicular (π/4) | 0.5000 | 0.5000 | +0.1661 | +0.1071 | 0.1050 | 0.1643 |
| 7 | opposite (π/2) | 0.0000 | 1.0000 | −0.9038 | −0.9643 | 0.2884 | 0.4628 |

Per-sigma rows, perpendicular start:

- Seed 42: D 0.5000 → 0.5057 → 0.5286 → 0.5576 →
  0.6499 → 0.7936 → 0.6297 (humps, peaks at σ = 0.50);
  C 0.5000 → 0.4931 → 0.4646 → 0.4260 → 0.2817 →
  0.3399 → 0.4208 (dips, bottoms at σ = 0.25).
- Seed 7: D 0.5000 → 0.4965 → 0.4815 → 0.4618 →
  0.4230 → 0.4321 → 0.3950 (drifts down); C 0.5000 →
  0.5068 → 0.5336 → 0.5643 → 0.6043 → 0.4833 →
  0.4400 (humps, peaks at σ = 0.25).

Per-sigma rows, opposite start (mirror image of stored):

- Seed 42: D 0.0000 → 0.0001 → 0.0029 → 0.0125 →
  0.0834 → 0.2783 → 0.4380 (rises); C 1.0000 → 0.9998
  → 0.9954 → 0.9810 → 0.8775 → 0.5458 → 0.2211
  (falls).
- Seed 7: D 0.0000 → 0.0001 → 0.0032 → 0.0115 →
  0.0516 → 0.1323 → 0.2884 (rises); C 1.0000 → 0.9998
  → 0.9939 → 0.9759 → 0.8595 → 0.5372 → 0.5430
  (falls, with a small rise at the last step).

What the pilot decides. The stored and opposite
directions pass all four bars on both calibration seeds
(seed 7 opposite Pearson −0.9038 is a thin pass, 0.0038
inside the bar — disclosed, not widened). The
perpendicular direction FAILS on both calibration seeds:
seed 42 fails Pearson (−0.7982) and the C range
(0.2183); seed 7 fails all four bars, with the
correlation actually positive (+0.1661). The
perpendicular start sits on the saturation plateau
(D = C = 0.5), so noise has no systematic direction to
move the quantities: the trajectories trace the fixed
noise directions and differ by seed (D humps to 0.79 on
seed 42, drifts down to 0.395 on seed 7). So the noisy
claim is SPLIT: (xci) covers stored and opposite
(calibration passes), (xcii) covers perpendicular alone
(calibration fails). The split is made here, before the
evaluation run, from the pilot — not after seeing the
held-out numbers.

An alternative was considered and REJECTED: relaxing
the (xci)/(xcii) bars for the perpendicular start (e.g.
a Pearson bar of −0.70 or a range bar of 0.10) so that
one combined claim passes. The bars are the (xxxii)
bars, reused for the same construction; moving them for
one direction would be moving a threshold to force a
pass, which this repo does not do. The perpendicular
failure is claimed as (xcii), not hidden.

## Claims

### (lxxxviii) Opposite direction: the wave returns to itself

On the 24-point full-circle grid, every slide quantity
(D, C, R_s, R_k, split, C + D) and every rotation-pair
quantity (D1, D2, cross term real and imag, V sweep,
V analytic) at theta + pi equals the same quantity at
theta within 1e-9. PASS iff all twelve worst differences
are <= 1e-9. Calibration: passes (worst 1.22e-15).

### (lxxxix) Perpendicular direction: the swap

On the same grid, the slide swaps D with C and R_s with
R_k at theta + pi/2, and the rotation pair swaps D1
with D2 and negates the cross term while |cross| and V
are unchanged, all within 1e-9. PASS iff all ten worst
swap errors are <= 1e-9. Calibration: passes (worst
1.78e-15).

### (xc) All-directions sweep: the directional profile and the cascade's direction dependence

(a) chi(theta) = -(1/2) sin(2 theta) within 1e-9 and
V(theta) = |sin(2 theta)| within 1e-9 on the grid, with
the zeros at every multiple of pi/2 (four zeros) and the
extrema at +/-0.5 at odd multiples of pi/4 (four
extrema). (b) The rotation cascade at every grid theta:
off-axis (theta not a multiple of pi/2) V_k = 0 within
1e-9 for every stage k >= 2, with the pair gone from
stage 2; on-axis V_1 = 0 within 1e-9, with no pair from
stage 2. PASS iff both legs hold. Calibration: passes
on both legs.

### (xci) Noisy direction sweep, stored and opposite directions

D-vs-C anti-correlation across the sigma grid from
theta = 0 (stored) and theta = pi/2 (opposite, the
kernel thought), on every seed in {42, 7, 1234, 2026}.
PASS iff, on EVERY (seed, direction) in the 4 x 2 set:
Pearson(D, C) <= -0.90, Spearman(D, C) <= -0.90,
D range >= 0.25, C range >= 0.25. Frozen bars: the
(xxxii) bars, unchanged. Calibration: passes on both
calibration seeds (seed 7 opposite Pearson -0.9038,
thinnest pass).

### (xcii) Noisy perpendicular direction

The same four bars from theta = pi/4 (the equal
superposition, D = C = 0.5), on every seed in
{42, 7, 1234, 2026}. PASS iff all four bars hold on
every seed. Frozen bars: the (xxxii) bars, unchanged.
Calibration: FAILS on both calibration seeds (seed 42:
Pearson -0.7982, C range 0.2183; seed 7: Pearson
+0.1661, Spearman +0.1071, D range 0.1050, C range
0.1643). This claim is calibrated to FAIL; the failure
is the finding — the observer-direction
anti-correlation holds from the stored and opposite
directions and breaks at the perpendicular one.

## Seeds

- Calibration: 42, 7 (exact sweeps are seed-free; the
  noisy pilot and the frozen bars come from these only).
- Evaluation (noisy claims (xci)/(xcii)): 42, 7, 1234,
  2026 — the (xxxii) file seeds. Held-out seeds 1234
  and 2026 are computed only after this file exists.
- No fresh seeds in this build: the perpendicular
  finding is a calibration result about the construction,
  and the held-out seeds test whether it generalizes.

## What would falsify

- (lxxxviii): any grid quantity differing between
  theta and theta + pi by more than 1e-9.
- (lxxxix): any grid swap identity violated by more
  than 1e-9.
- (xc): any grid chi or V off its exact form by more
  than 1e-9, a missing/extra zero or extremum, any
  off-axis cascade with V_k != 0 for k >= 2 or a pair
  surviving past stage 1, or any on-axis cascade with
  V_1 != 0 or a pair existing from stage 2.
- (xci): any (seed, direction) in the 4 x 2 set failing
  any of the four bars.
- (xcii): any seed failing any of the four bars.
  (Calibrated to fail.)

## Honesty

Synthetic, classical emulation throughout. Nothing here
measures consciousness, empathy in a human, or any theory
of consciousness. No scalar Phi is computed anywhere and
none is presented as a consciousness measure; E = hnu is
not used anywhere in this build. Claims (lxxxviii)-(xc)
are exact identities, like (xxxiv): the measured content
is that the code realizes them on the full circle to
1e-9, including the negative-amplitude quadrants the
existing code never ran — a failure would be a defect in
the code's quantities, not a result about a theorem.
Claims (xci)/(xcii) are statistical claims on 5-copy
means, like (xxxii)/(xxxv): the same saturation and
finite-sample fragility applies, and a FAIL is a finding
about the direction sweep, not a defect. The split of
the noisy claim into (xci) and (xcii) was made from the
calibration pilot before the evaluation run, and the
rejected alternative (relaxing the bars for the
perpendicular start) is recorded above. The (xxxii)
verdict (FAIL, honest, held-out seed 2026) and the
(xxxv) verdict (FAIL, honest, fresh seeds 5/99) stand
unchanged. No threshold was moved to force a pass.
