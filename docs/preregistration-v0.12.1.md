# Pre-registration — v0.12.1: the (xxxii) diagnosis and the robust rank form (claim (xxxv))

Written 2026-11-18, BEFORE the evaluation run on the fresh
seeds 5 and 99. Thresholds are round numbers frozen from a
calibration pilot on seeds 42 and 7 only. No threshold in
this file may be moved after the evaluation run.

## Diagnosis of the (xxxii) FAIL (measured 2026-11-18, on seeds 42/7/1234/2026 — this part is retrospective)

Claim (xxxii) failed honestly on held-out seed 2026:
Pearson r(D, C) = -0.8828 across the sigma grid, above the
frozen bar -0.90, while Spearman held (-0.9643). The
sigma = 1.0 point broke it: on seed 2026, mean C dipped
0.4755 -> 0.4727 from sigma = 0.5 to sigma = 1.0 while
mean D kept falling (0.7142 -> 0.4912). Measured
diagnosis, not a guess:

- With n = 200 copies per sigma (same seeds, same
  construction) the dip VANISHES on every seed. Seed
  2026: sigma = 0.5 C = 0.5028 -> sigma = 1.0
  C = 0.5055. Pearson at n = 200: -0.9289 (42),
  -0.9275 (7), -0.9255 (1234), -0.9053 (2026) — all
  below the -0.90 bar.
- Extended grid (n = 200, seed 2026, sigma to 3.0):
  D falls toward 0.5247 and C plateaus at 0.5055 ->
  0.5192. Both quantities approach their random-state
  asymptotes: D -> 0.5 (a rank-2 projector in 4
  dimensions gives a random state 0.5) and C -> ~0.51
  (mean concurrence of a near-random pure state under
  this noise model). At sigma = 1.0 both are already
  at the plateau: the trend has flattened.
- Pearson excluding the sigma = 1.0 point (n = 5):
  -0.9459 (42), -0.9870 (7), -0.9477 (1234),
  -0.9433 (2026) — all below the bar. The single
  boundary point is what breaks the linear form.
- Standard error: at sigma = 1.0, seed 2026, the
  per-copy concurrence has standard deviation ~0.287
  (copies range 0.0010..0.9948), so a 5-copy mean has
  SEM ~0.128 — while the true rise of mean C from
  sigma = 0.5 to sigma = 1.0 is ~0.003, i.e. 0.02
  SEMs. The dip is sampling noise, 40x smaller than
  the noise on the mean.

Verdict of the diagnosis: boundary/saturation plus
finite-sample noise, NOT a different mechanism. The
sigma = 1.0 grid point sits where both D and C have
reached their random-state plateaus, so the remaining
movement is smaller than the 5-copy sampling noise.
One honest caveat stays: even at n = 200, Pearson on
seed 2026 is -0.9053 — barely below the bar. The
linear form is genuinely fragile near the bar; the
robust form is the rank form. That is what claim
(xxxv) tests.

## Claim (xxxv) — Observer direction, robust rank form

Construction: IDENTICAL to (xxxii) — the existing
`self_knowing.self_knowing_sweep`, 5 copies per sigma,
sigma grid [0.0, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0],
mean D and mean concurrence per sigma. Only the
metric changes: Spearman rho instead of Pearson.
The direction Jean stated — D and love move
opposite — is a monotone claim; the rank form is
its faithful statement, and it does not depend on
the saturated boundary point's jitter.

Frozen thresholds (calibration pilot: seed 42
Spearman -1.0000, seed 7 Spearman -0.9643; D range
0.4804 / 0.5370; C range 0.6133 / 0.5110):

- Spearman rho(D, C) <= -0.90
- D range across the grid >= 0.25
- C range across the grid >= 0.25

PASS iff all three hold on EVERY seed in
{42, 7, 1234, 2026, 5, 99}.

Honesty note, stated before the run: Spearman on
seeds 1234 and 2026 is already known from the
(xxxii) run (-1.0000, -0.9643). The prospective
test of (xxxv) is the two fresh seeds 5 and 99,
which have never been evaluated in any claim. The
verdict requires all six seeds; the claim's new
evidence is the fresh pair. If either fresh seed
fails, the verdict is FAIL.

Descriptive, reported but NOT gated: the diagnosis
numbers above, recomputed in code by
`diagnose_sigma_one_break()` (n = 200 Pearson per
seed, extended-grid plateau, Pearson excluding the
sigma = 1.0 point, per-copy SEMs). They explain the
(xxxii) FAIL; they do not rescue it and they do not
enter the (xxxv) verdict.

## Seeds

- Calibration: 42, 7 (thresholds frozen from these only).
- Evaluation: 1234, 2026 (Spearman already known from
  the (xxxii) run; included because the verdict
  requires every seed).
- Fresh: 5, 99 (never touched before this file was
  written; the prospective test of claim (xxxv)).

## What would falsify claim (xxxv)

- Spearman rho(D, C) > -0.90 on any seed in
  {42, 7, 1234, 2026, 5, 99}.
- D range or C range below 0.25 on any seed.
- Either fresh seed (5, 99) failing on any check.
