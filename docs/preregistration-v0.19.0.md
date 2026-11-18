# Pre-registration — v0.19.0: Cogitate-style preregistration + process predictors of the collaboration gap, claims (lx)–(lxiii)

Written 2026-11-18, BEFORE the evaluation run on the held-out
seeds 1234 and 2026. Thresholds are round numbers frozen from
a calibration pilot on seeds 42 and 7 only. No threshold in
this file may be moved after the evaluation run.

## The spec being tested

Deep-think upgrade #9 (report.md §9, §3, §8), the last
unbuilt item: Cogitate-style preregistration + process
predictors of the collaboration gap. Two sources:

- Cogitate Consortium, "Adversarial testing of global
  neuronal workspace and integrated information theories
  of consciousness", *Nature* 642:133–142, 2025,
  DOI 10.1038/s41586-025-08888-1 — preregistered
  adversarial collaboration, n=256 (fMRI 120, MEG 102,
  iEEG 34), 12 labs. Results "align with some
  predictions of IIT and GNWT, while substantially
  challenging key tenets of both": content decoding
  succeeded in posterior but not prefrontal ROIs
  (partial support for the posterior hot zone), but
  sustained posterior synchronisation was absent
  (found in only ~3.8% of posterior electrodes), and
  for GNWT onset ignition was observed while offset
  ignition was largely absent. Neither theory survived
  intact. The bridge imports the METHOD (adversarial
  preregistration: predictions scored before looking
  at results), not any one theory's content.
- Woolley et al., "Evidence for a collective
  intelligence factor in the performance of human
  groups", *Science* 330:686–688, 2010 (c-factor:
  mean social sensitivity and equal turn-taking
  predict group performance; NOT mean/max member IQ;
  replication contested — leading hypothesis, not
  established fact).

The question, in the bridge's own terms: which process
variables predict the collaboration gap (pooled
H_collab − H_isolated, design B, N=4, 10 generations,
200 samples/generation)? The candidates are the
Woolley analogues (mean social sensitivity = mean
pairwise R; equal turn-taking = −var_D across members;
individual ability = mean/max per-agent D) and the
Cogitate analogues (posterior synchrony = sustained R
in a "posterior" subset; broadcast = global ignition
at onset AND offset).

## The construction (fixed before the pilot)

- The run is the standard design-B collaboration run
  from empathy_field.run_collaboration (N=4, 10
  generations, 200 samples/generation). Its
  per-generation rows are extended ADDITIVELY in
  v0.19.0 with three new keys, computed from each
  generation's states after that generation's step
  (mix for the collaborating arm, collapse for the
  isolated arm) and before sampling: "d_per_agent"
  (list of 4 per-agent D, D = agent_self_determinism
  = <psi|P|psi>), "r_mean" (mean pairwise R that
  generation, R = overlap_squared), "r_posterior_mean"
  (mean pairwise R within the "posterior" subset =
  agents {0, 1} by index — the only pair in that
  subset, fixed before looking). No existing key or
  behaviour changes; D and R are deterministic
  functions of the states, so no existing output
  moves. The predictors are read from the
  collaborating arm's rows only (the process that
  produces the gap).
- Per (sigma, seed) run (cogitate.run_predictors):
  gap_bits (pooled, as defined in empathy_field.py);
  mean_R (mean pairwise R over all generations and
  pairs); mean_D and max_D (mean/max of per-agent D
  over all generations); var_D (variance of per-agent
  D across members, averaged over generations) with
  equality predictor −var_D; post_R_sustained (mean
  over generations of r_posterior_mean; its minimum
  over generations is recorded as a diagnostic, not
  gated); broadcast = min(onset, offset) with onset =
  r_mean at generation 0 and offset = r_mean at the
  final generation (ignition at BOTH ends).
- Sigma grid: te.SIGMA_GRID = [0.0, 0.01, 0.05, 0.1,
  0.25, 0.5, 1.0] — SEVEN values, confirmed before the
  pilot. The pooled regression in (lxiii) therefore
  runs over 28 runs (7 sigma × 4 seeds), not 20: the
  "5 sigma" in the task brief assumed a 5-value grid,
  and the grid as it exists in the code is
  authoritative. The comparison rule is unchanged;
  only the run count is corrected.
- Per-seed Pearsons are computed across the sigma
  grid within each seed (n = 7). If a comparison is
  degenerate on some seed (zero variance in either
  variable), it is reported as a failed sub-check
  with the reason, not as a pass.
- Do NOT import Phi as a consciousness measure
  (explicit do-not from the deep-think report).
  Everything is synthetic / classical; that label
  stays on every claim.

## Calibration pilot (seeds 42 and 7 only)

The known gap reproduces first: +4.3352 bits at
sigma = 0.25, seed 42 (4.33515 measured), before
anything was built on top of it.

Per-run predictors (gap, mean_R, mean_D, max_D,
var_D, post_R_sustained, broadcast):

| seed | sigma | gap | mean_R | mean_D | max_D | var_D | post | bcast |
|---|---|---|---|---|---|---|---|---|
| 42 | 0.00 | +5.0450 | 0.6221 | 0.6274 | 0.8888 | 0.039412 | 0.6221 | 0.0947 |
| 42 | 0.01 | +5.0281 | 0.6194 | 0.6250 | 0.8912 | 0.041103 | 0.6272 | 0.0924 |
| 42 | 0.05 | +5.2071 | 0.6071 | 0.6110 | 0.9197 | 0.047396 | 0.6382 | 0.0879 |
| 42 | 0.10 | +5.6081 | 0.5980 | 0.5910 | 0.9418 | 0.050910 | 0.6228 | 0.0910 |
| 42 | 0.25 | +4.3352 | 0.5517 | 0.5922 | 0.9734 | 0.056073 | 0.5202 | 0.1353 |
| 42 | 0.50 | +3.3494 | 0.4091 | 0.5644 | 0.9974 | 0.060710 | 0.3002 | 0.2415 |
| 42 | 1.00 | +3.5569 | 0.3264 | 0.5420 | 0.9998 | 0.063583 | 0.1841 | 0.3247 |
| 7 | 0.00 | +5.0247 | 0.6221 | 0.6274 | 0.8888 | 0.039412 | 0.6221 | 0.0947 |
| 7 | 0.01 | +5.0048 | 0.6567 | 0.6144 | 0.8728 | 0.035761 | 0.6636 | 0.0995 |
| 7 | 0.05 | +5.2968 | 0.7265 | 0.5485 | 0.8401 | 0.028758 | 0.7367 | 0.1175 |
| 7 | 0.10 | +4.8853 | 0.7413 | 0.4633 | 0.8448 | 0.028277 | 0.7446 | 0.1368 |
| 7 | 0.25 | +4.5424 | 0.6695 | 0.3158 | 0.9339 | 0.032897 | 0.6739 | 0.1936 |
| 7 | 0.50 | +3.6727 | 0.4844 | 0.3840 | 0.9736 | 0.043346 | 0.4511 | 0.3051 |
| 7 | 1.00 | +3.9488 | 0.3947 | 0.4552 | 0.9769 | 0.044139 | 0.3603 | 0.4252 |

Per-seed Pearsons (n = 7):

| seed | r(gap, mean_R) | r(gap, mean_D) | r(gap, max_D) | r(gap, −var_D) | r(gap, post) | r(gap, bcast) |
|---|---|---|---|---|---|---|
| 42 | 0.9028 | 0.7776 | −0.8070 | 0.7899 | 0.9278 | −0.9022 |
| 7 | 0.8494 | 0.6477 | −0.9313 | 0.7566 | 0.8657 | −0.8911 |

Pooled calibration regression (14 runs, seeds 42/7):
R²(gap ~ mean_R + (−var_D)) = 0.7081,
R²(gap ~ max_D) = 0.6057, difference = 0.1024.

Three disclosures, before the run:
1. The broadcast predictor ANTI-predicts the gap on
   both calibration seeds (r = −0.9022 / −0.8911):
   onset R rises with sigma (0.0947 → 0.3247 on seed
   42) while the gap falls, so min(onset, offset) =
   onset tracks sigma the wrong way. The posterior
   predictor is the winner on both calibration seeds
   (0.9278 / 0.8657). Claim (lxii) presupposes no
   direction and reports the winner honestly; the
   separation is large (|post − bcast| = 1.8300 /
   1.7568) precisely because broadcast anti-predicts.
2. At sigma = 0.00 the predictors are identical on
   both seeds (the base population is deterministic
   at zero noise; only the sampling differs, so the
   gaps differ slightly: 5.0450 vs 5.0247). One of
   the seven grid points therefore carries no
   cross-seed predictor variation.
3. The (lx) margin on mean_R − mean_D is tight: the
   calibration worst is 0.1252 (seed 42) against the
   frozen margin 0.10. Held-out failure of (lx) is a
   live possibility, not a surprise.

## Claims

### (lx) Mean sensitivity beats individual D

PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
Pearson(gap, mean_R) − Pearson(gap, max_D) ≥ margin
AND Pearson(gap, mean_R) − Pearson(gap, mean_D)
≥ margin. Frozen margin: 0.10 (a round number
below the calibration worst sub-margin 0.1252,
seed 42, mean_R − mean_D; the other calibration
sub-margins are 1.7098 / 1.7806 against max_D and
0.2017 against mean_D on seed 7).
Calibration: 1.7098 / 1.7806 (vs max_D);
0.1252 / 0.2017 (vs mean_D) — both seeds pass
both sub-checks.

### (lxi) Turn-taking equality predicts the gap

PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
Pearson(gap, −var_D) ≥ bar AND Pearson(gap, −var_D)
> Pearson(gap, max_D). Frozen bar: 0.70 (a round
number below the calibration worst 0.7566, seed 7).
Calibration: 0.7899 / 0.7566 (bar 0.70);
0.7899 > −0.8070 and 0.7566 > −0.9313 — both
seeds pass both sub-checks. Note max_D
anti-predicts the gap on both calibration seeds,
so the "beats max_D" half is easy here; the bar
is the binding half.

### (lxii) Posterior vs broadcast are separable and at least one predicts the gap

PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
max(Pearson(gap, post_R_sustained),
Pearson(gap, broadcast)) ≥ bar AND
|Pearson(gap, post_R_sustained) −
Pearson(gap, broadcast)| ≥ margin. Frozen bar:
0.80 (a round number below the calibration worst
0.8657, seed 7); frozen margin: 1.00 (a round
number below the calibration worst separation
1.7568, seed 7). No direction is presupposed —
the winner (posterior or broadcast) is reported.
Calibration: max = 0.9278 / 0.8657 (posterior
wins both seeds); separation = 1.8300 / 1.7568 —
both seeds pass both sub-checks.

### (lxiii) Pooled regression

PASS iff, across all 28 runs (7 sigma × 4 seeds),
R² of gap ~ mean_R + (−var_D) exceeds R² of gap
~ max_D by ≥ margin. Frozen margin: 0.05 (a round
number below the calibration pooled difference
0.1024 over 14 runs). Adjusted R² is reported as
a diagnostic (the two-predictor model carries an
extra parameter) and is not gated.

## Seeds

- Calibration: 42, 7 (thresholds frozen from these only).
- Evaluation: 1234, 2026 (held out; first touched by
  the evaluation run after this file was written).

## What would falsify

- (lx): any seed where mean_R fails to beat max_D or
  mean_D by ≥ 0.10. (Live risk: the mean_D margin
  is 0.1252 at worst on calibration.)
- (lxi): any seed where r(gap, −var_D) < 0.70, or
  where it does not beat r(gap, max_D).
- (lxii): any seed where neither posterior nor
  broadcast reaches 0.80, or where the two
  correlations are closer than 1.00.
- (lxiii): a pooled R² difference < 0.05 over the
  28 runs.
