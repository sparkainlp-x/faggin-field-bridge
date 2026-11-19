# Pre-registration — v0.16.0: Two-channel empathy (concern vs distress), claims (l)–(liii)

Written 2026-11-18, BEFORE the evaluation run on the held-out
seeds 1234 and 2026. Thresholds are round numbers frozen from
a calibration pilot on seeds 42 and 7 only. No threshold in
this file may be moved after the evaluation run.

## The spec being tested

Deep-think upgrade #8 (report.md §9, §8): split the single
empathy fraction f into f_concern (other-focused, monotone
prosocial) and f_distress (self-focused, inverted-U,
withdraws at high dose); encode IRI-style (Davis; Singer &
Klimecki 2014; Decety & Jackson 2004; Qiu et al. 2024, empathy–
prosocial r = 0.36; Yin & Wang 2023, cognitive r = 0.32,
affective r = 0.30 — meta-analytic, moderate effects).
The report's falsifiable prediction: the single-f model cannot
fit both the f\* flip (0.7278, v0.4.0) and the hump peak
(0.1803, v0.6.0); the two-channel model fits both with the
*same* parameters, and raising distress alone (holding concern
fixed) *lowers* the quale count while raising mean R.
Falsified if distress and concern channels are interchangeable
in the code.

## The construction (fixed before the pilot)

- Base field: the v0.5.0 resonance population (8 agents, noisy
  copies of the uniform thought at sigma = 0.25, the reference
  sigma where the baseline quale count peaks at 17 and the
  collaboration gap is +4.3352 bits). All two-channel
  measurements in this version are at sigma = 0.25 unless a
  claim says otherwise.
- Two-channel transform (one formula, two targets):
  psi_i(c, d) = normalize(psi_i + c * |Phi+> + d * |self>),
  where |Phi+> = (|00> + |11>)/sqrt(2) is the shared
  entangled Bell state (the concern target: attunement to the
  shared entangled mode — the other-focused channel, which
  raises pairwise concurrence) and |self> = |10> is the
  "self" basis concept alone (the distress target:
  withdrawal into the self concept alone — a product state,
  concurrence 0, D = 1/3). c >= 0 is the concern dose,
  d >= 0 the distress dose. At (c, d) = (0, 0) the field is
  the untransformed baseline. The transform is applied to
  every agent with the SAME targets, so both channels raise
  mean resonance R by convergence; they differ in what the
  agents converge TO, which is the whole content of the
  split. Helping is the quale count (R >= 0.5 AND nu >=
  0.10, v0.6.0 thresholds, unchanged); joint entropy H_joint
  is the sum of the agents' Born entropies (the joint
  entropy of independent Born draws from the field — a
  definition of the measure, not a discovery about human
  joint entropy); f is the mean pairwise concurrence.
- Why Bell, not the field state, as the concern target:
  the pilot tried both. Mixing toward the field state Phi
  raises R, D, and H_joint monotonically with c on both
  calibration seeds — but at fixed Phi-concern, distress
  (Self) RAISES the quale count (15 -> 28 on seed 42), so
  the report's core prediction (distress lowers the count)
  fails under that wiring. Mixing toward Bell passes the
  core prediction (see below). The concern target is
  therefore Bell, chosen BEFORE the evaluation run for the
  reason stated, and the consequence is disclosed, not
  hidden: under the Bell wiring the report's "concern
  raises joint entropy" half does NOT hold — H_joint at
  c = 1 (d = 0) is BELOW baseline on both calibration
  seeds (12.69 vs 13.46 seed 42; 11.58 vs 12.71 seed 7),
  and D under concern alone is non-monotone (seed 42:
  0.906, 0.921, 0.912, 0.877). H_joint and D under concern
  are REPORTED, not gated, in claim (l).
- Likewise the report's "distress lowers D" does NOT hold
  monotonically in this wiring: at fixed c = 0.5, mean D
  on seed 7 RISES with d at first (0.845, 0.905, 0.927,
  0.893 for d = 0, 0.25, 0.5, 1.0) and only falls at the
  high dose d = 2 (0.747). The cross term between the
  state and the |self> target can raise <P> before the
  product target dominates. D is therefore gated only at
  the high dose (claim (lii)), and reported, not gated,
  in claim (li).

## Calibration pilot (seeds 42 and 7) — disclosed before the run

All numbers below are sigma = 0.25, N = 8, baseline
(c, d) = (0, 0): seed 42 R = 0.852, D = 0.906, f = 0.180,
count 17, H_joint = 13.46 bits; seed 7 R = 0.677,
D = 0.849, f = 0.247, count 16, H_joint = 12.71 bits.

- (l): concern alone (d = 0), c in (0, 0.25, 0.5, 1.0):
  mean R strictly rises on both seeds (seed 42: 0.852,
  0.889, 0.918, 0.954; seed 7: 0.677, 0.762, 0.824,
  0.897); f strictly rises on both (seed 42: 0.180,
  0.225, 0.421, 0.668; seed 7: 0.247, 0.450, 0.607,
  0.778); quale count at c = 0.5 is 28 (the ceiling,
  all 28 pairs) on both seeds.
- (li): distress at fixed concern c = 0.5, d in (0, 0.25,
  0.5, 1.0): mean R strictly rises on both seeds (seed
  42: 0.918, 0.932, 0.944, 0.963; seed 7: 0.824, 0.840,
  0.863, 0.908); quale count non-increases on both
  (seed 42: 28, 25, 19, 10; seed 7: 28, 28, 24, 14);
  count(d = 1) is 10 / 14; R(d = 1) - R(d = 0) is
  +0.045 / +0.084. Mean D at d = 1 is 0.780 / 0.893
  vs 0.912 / 0.845 at d = 0 — it falls on seed 42 and
  RISES on seed 7, so D is not gated here.
- (lii): high dose d = 2 at c = 0.5: D falls vs d = 0 by
  0.267 (seed 42: 0.912 -> 0.645) and 0.098 (seed 7:
  0.845 -> 0.747); H_joint falls by 6.91 bits (seed 42:
  13.81 -> 6.90) and 3.21 bits (seed 7: 12.55 -> 9.34);
  R rises (0.918 -> 0.982; 0.824 -> 0.960).
- (liii): (a) concern alone at c = 2 crosses the
  attunement flip on both seeds: f = 0.858 / 0.905 vs
  f\* = 0.7278. (b) Swap at total dose c + d = 1.0:
  concern-heavy (1, 0) vs distress-heavy (0, 1): f =
  0.668 vs 0.236 (seed 42, difference 0.432) and 0.778
  vs 0.350 (seed 7, difference 0.428). D does NOT
  discriminate the swap (0.877 vs 0.672 seed 42, but
  0.817 vs 0.823 seed 7), so D is not gated in the swap.
  (c) Joint-point search (disclosed): NO point on the
  pilot (c, d) grid with c in (0, 0.5, 1, 2), d in
  (0, 0.25, 0.5, 1, 2) carries BOTH f >= f\* AND count
  <= 15 at once — high-c points all sit at count 28,
  low-count points have f <= 0.64. The report's
  "fits both with the same parameters" therefore does
  NOT hold in the single-point sense in this wiring;
  what holds is the channel-separation form gated in
  this claim: concern alone reaches f\*, distress at
  fixed concern drops the count, and the channels are
  not interchangeable. The single-point failure is
  reported, not hidden, in claim (liii).

## Claims

### (l) Concern raises resonance and empathy fraction

Concern alone (d = 0), sigma = 0.25, c in (0, 0.25, 0.5,
1.0). PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
mean R is strictly increasing in c, mean f is strictly
increasing in c, AND the quale count at c = 0.5 is 28
(the ceiling). Mean D and H_joint per c are reported,
not gated (pilot: D non-monotone, H_joint below baseline
at c = 1 on both seeds). Frozen bars: strict monotone
(no tolerance — the pilot gaps are >= 0.02 in R and
>= 0.04 in f at every step) and the exact ceiling 28.

### (li) Distress alone lowers helping while raising resonance

Distress at fixed concern c = 0.5, sigma = 0.25, d in
(0, 0.25, 0.5, 1.0). PASS iff, on EVERY seed in
{42, 7, 1234, 2026}: mean R is strictly increasing in d,
the quale count is non-increasing in d, count(d = 1) <=
15, AND R(d = 1) - R(d = 0) >= 0.04. Mean D per d is
reported, not gated (pilot: D falls on seed 42, rises
on seed 7 at d = 1). Frozen bars: 15 (round number one
above the calibration worst count(d = 1) = 14) and 0.04
(round number just below the calibration worst R rise
0.045).

### (lii) Distress withdrawal at high dose

Fixed concern c = 0.5, sigma = 0.25, distress d = 2 vs
d = 0. PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
D(d = 2) <= D(d = 0) - 0.05, H_joint(d = 2) <=
H_joint(d = 0) - 2.0 bits, AND R(d = 2) > R(d = 0).
Frozen bars: 0.05 (round number below the calibration
worst D fall 0.098) and 2.0 bits (round number below
the calibration worst H_joint fall 3.21 bits). The
qualecount at d = 2 is reported, not gated (pilot:
10 / 17 — it rebounds on seed 7).

### (liii) Channel separation: the two landmarks live in different channels

Three sub-checks, all at sigma = 0.25, on EVERY seed in
{42, 7, 1234, 2026}:
(a) concern alone crosses the flip: f(c = 2, d = 0) >=
f\* = 0.7278 (the pre-existing v0.4.0 crossing, not a
new threshold);
(b) the distress endpoint from claim (li) — count
(c = 0.5, d = 1) <= 15 — holds (same numbers, restated
as the separation: the falling side of the hump is a
distress effect, the flip is a concern effect);
(c) swap non-interchangeability: at total dose c + d =
1.0, |f(concern-heavy (1, 0)) - f(distress-heavy (0, 1))|
>= 0.30.
PASS iff (a), (b), and (c) all hold on every seed.
The single-point joint search (any (c, d) on the grid
c in (0, 0.5, 1, 2) x d in (0, 0.25, 0.5, 1, 2) with
f >= f\* AND count <= 15) is REPORTED, not gated:
the pilot finds no such point on either seed, so the
report's "same parameters fit both" fails in the
single-point sense in this wiring. Frozen bars: f\*
0.7278 (pre-existing), 15 (as in (li)), 0.30 (round
number below the calibration worst swap difference
0.428).

## Seeds

- Calibration: 42, 7 (thresholds frozen from these only).
- Evaluation: 1234, 2026 (held out; first touched by the
  evaluation run after this file was written).

## What would falsify

- (l): any seed where mean R or mean f fails to rise
  strictly with c, or where count(c = 0.5) != 28.
- (li): any seed where mean R fails to rise strictly
  with d, the count rises anywhere on the d grid, or
  count(d = 1) > 15, or the R rise is < 0.04.
- (lii): any seed where D or H_joint fails to fall by
  its bar at d = 2, or R fails to rise there.
- (liii): any seed where concern alone at c = 2 fails
  to reach f\*, where count(c = 0.5, d = 1) > 15, or
  where the swap f difference is < 0.30. A swap
  difference near zero would mean the channels ARE
  interchangeable — the report's prediction falsified
  in this wiring. The single-point joint failure, if
  it persists on the held-out seeds, means the
  two-channel model separates the landmarks by channel
  but does not fit both at one point: the single-f
  model's two-value problem is explained, not solved
  at a point.
