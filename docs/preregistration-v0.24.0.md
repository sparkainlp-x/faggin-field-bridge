# Pre-registration — v0.24.0: seed-1234 design decisions — re-gate the two-channel claims on the determinant sign, replace (lx)'s 0.10 margin with a pooled rule. Claims (lxxxii)–(lxxxvii)

Written 2026-11-18, BEFORE the evaluation run of the new
claims. The pilot tables below are calibration / diagnostic
data measured before this file was written (the v0.21.0
12-seed survey plus the two-channel per-seed verdicts
recomputed for the survey seeds); the new-claim verdicts
(lxxxii)–(lxxxvii) are computed only after this file exists.
No threshold in this file may be moved after the evaluation
run, and no claim may be redefined after the fact. The old
verdicts stay on the record: (l), (li), (liii) FAIL as
originally stated (every file seed), and (lx) FAILS as
originally stated (frozen 0.10 margin). The new claims are
NEW claims, not rewrites.

## The spec being tested

The v0.21.0 seed-1234 diagnosis (docs/seed-1234-diagnosis.md)
found three independent anomalies, no common mechanism, and
left two design decisions open for the next build:

(a) Re-gate the two-channel empathy claims (l)/(li)/(liii)
conditional on the baseline pair determinant-sign
distribution. The diagnosis showed the failures sit in the
SIGN of the baseline determinant det = ad − bc of the pair
state, not in its level: on seed 1234, 26/28 baseline pairs
have det < 0 (mean −0.1556) vs −0.0431 / +0.1050 / +0.0101
on the other file seeds. The concern target |Φ+⟩ adds to
the a and d amplitudes, pushing det UP; the distress target
|self⟩ = |10⟩ adds to the c amplitude, pushing det DOWN.
Since f = 2|det|, a dose that pushes det through zero first
destroys concurrence and only then rebuilds it. The
per-pair sign rule was verified exactly on all four file
seeds at dose 0.25: no pair with det ≥ 0 ever falls under
concern, and no pair with det < 0 ever falls under
distress.

(b) Replace (lx)'s 0.10 margin with a new preregistered rule
justified from the 12-seed survey. The diagnosis showed the
(lx) margin r(gap, mean_R) − r(gap, mean_D) fails the 0.10
bar on 6 of 12 surveyed seeds (1: −0.0206, 2: +0.0561,
1234: −0.0393, 777: +0.0025, 2024: +0.0375,
31337: +0.0916), because r(gap, mean_D) is driven by the
SHAPE of the mean_D trajectory, which varies from flat to
U-shaped to hump-shaped across seeds — while r(gap, mean_R)
itself falls to 0.38–0.50 on seeds 1–3. A per-seed
"mean_R beats mean_D by 0.10" bar does not survive fresh
seeds.

## The gate (job a) — frozen

A seed is GATED IN iff its baseline resonance field (N = 8,
σ = 0.25) has

    mean baseline pair determinant >= GATE_DET_MEAN_MIN = -0.05.

Justification, from the calibration seeds only: the
calibration det means are −0.0431 (seed 42) and +0.1050
(seed 7). Any gate must admit both calibration seeds —
otherwise it would exclude the very data the claims were
frozen from. −0.05 is the tightest round number below the
calibration minimum (−0.0431). The gate is a statement
about the field's determinant distribution, fixed before
the evaluation; which seeds it admits is then a
measurement, not a choice. On the 12-seed survey it admits
8 seeds (42, 7, 2026, 1, 3, 99, 123, 31337) and excludes 4
(1234, 2, 777, 2024).

Two alternatives were considered and REJECTED before the run:

1. A fraction-negative gate (n_det_negative / 28 ≤ 0.75):
   the calibration fractions are 18/28 (0.643) and 5/28
   (0.179), so 0.75 admits the calibration seeds — but on
   the survey it admits 11/12 seeds, including 777 and
   2024, whose f(c, 0) DIPS under concern (0.2594 → 0.2575
   and 0.2462 → 0.2174 at c = 0.25). The count of negative
   pairs does not carry the mechanism; the MEAN does,
   because a strongly negative mean means the typical pair
   sits far below zero and must cross it. The fraction is
   reported as a diagnostic, not used in the gate.
2. A gate on the baseline level f0 (e.g. f0 ≤ 0.30): refuted
   already in the diagnosis — no landmark sits near
   f = 0.3251, and f0 does not separate the f-monotonicity
   failures (seed 3 has f0 = 0.2732 and passes the
   f-monotonicity; seed 2 has f0 = 0.2332 and is excluded
   by the det gate but passes it). What breaks the claims
   is the sign, not the level.

## Per-generation note (v0.22.0) — stated explicitly

The two-channel claims (l)–(liii) involve NO pooling across
generations: each claim is measured on a single N = 8 field
(28 pairs) at one σ, with no generation index anywhere. So
no per-generation restatement applies to them, and none is
attempted here. The one pooled claim in the seed-1234
diagnosis, the XOR (lxv) failure, was ALREADY corrected at
the per-generation level in v0.22.0: claim (lxxvii) PASSES —
the mean per-generation XOR gap on seed 1234 is +1.4356
bits (synergy-majority, share 0.584) against the pooled
gap of −0.2591, because per-generation the isolated arm
carries nothing at all (I_isol = 0 exactly, every
generation) while pooling raises its information to 1.7610
bits. The v0.20.0 seed-1234 XOR failure was itself a
pooling artifact, and that result stands; no separate XOR
re-gating is attempted in this build.

## Calibration pilot (job a) — disclosed before the run

Baseline determinant stats, N = 8, σ = 0.25, all 12 survey
seeds (recomputed for the survey seeds; file seeds match
docs/seed-1234-diagnosis.md):

| seed | det mean | det median | det < 0 | f0 | gated in |
|---|---|---|---|---|---|
| 42 | −0.0431 | −0.0414 | 18/28 | 0.1803 | yes |
| 7 | +0.1050 | +0.0895 | 5/28 | 0.2469 | yes |
| 1234 | −0.1556 | −0.1559 | 26/28 | 0.3251 | NO |
| 2026 | +0.0101 | +0.0109 | 12/28 | 0.1772 | yes |
| 1 | −0.0494 | — | 18/28 | 0.2168 | yes |
| 2 | −0.0877 | — | 19/28 | 0.2332 | NO |
| 3 | −0.0123 | — | 14/28 | 0.2732 | yes |
| 99 | −0.0011 | — | 15/28 | 0.2742 | yes |
| 123 | −0.0315 | — | 19/28 | 0.2213 | yes |
| 777 | −0.0717 | — | 18/28 | 0.2594 | NO |
| 2024 | −0.0528 | — | 21/28 | 0.2462 | NO |
| 31337 | −0.0216 | — | 17/28 | 0.2720 | yes |

The gate separates the concurrence (f) failures exactly on
the survey. Concern f(c, 0) over c in (0, 0.25, 0.5, 1.0):

- Every gated seed: strictly rising (e.g. seed 1:
  0.2168 → 0.2322 → 0.4234 → 0.6741; seed 3:
  0.2732 → 0.3084 → 0.4569 → 0.6909; seed 31337:
  0.2720 → 0.2954 → 0.4531 → 0.6878).
- Every excluded seed except seed 2: DIPS at c = 0.25
  (1234: 0.3251 → 0.1505; 777: 0.2594 → 0.2575;
  2024: 0.2462 → 0.2174). Seed 2 rises
  (0.2332 → 0.2381 → 0.3693 → 0.6352) but is excluded
  anyway: the gate is a sufficient condition for the
  mechanism regime, not a necessary one, and no claim
  here asserts necessity.

Distress f(0.5, d) over d in (0, 0.25, 0.5, 1.0):

- Every gated seed: non-increasing (e.g. seed 42:
  0.4207 → 0.2695 → 0.1694 → 0.0902; seed 99:
  0.4710 → 0.3192 → 0.2332 → 0.1557).
- Every excluded seed except seed 2: RE-RISES at d = 1
  (1234: 0.1154 → 0.2082; 777: 0.1476 → 0.1508;
  2024: 0.1354 → 0.1425). Seed 2 is non-increasing.

The per-pair sign rule at dose 0.25, all 12 survey seeds:

- Positive-det pairs falling under concern: 0.000 on ALL
  12 seeds (0 pairs everywhere) — the concern half of the
  sign rule is EXACT on the whole survey, not just the
  file seeds. Mean Δf under concern for negative-det pairs
  is negative on 11/12 seeds (−0.21 to −0.02; exception
  seed 7: +0.1114 on only 5 negative-det pairs) and
  positive for positive-det pairs on all 12 (+0.22 to
  +0.28).
- Negative-det pairs falling under distress: 0.000 on 9/12
  seeds, but NOT exact — 0.111 on seed 1 (2/18 pairs),
  0.158 on seed 2 (3/19), 0.278 on seed 777 (5/18). The
  distress half of the sign rule does NOT hold universally,
  so no claim in this build asserts it exactly; it is
  reported, not gated. (The diagnosis verified it exactly
  on the four file seeds only.)

The gate does NOT rescue the quale-count sub-checks, on the
survey. With all original sub-checks, on the 8 gated survey
seeds: claim (l) passes on 4/8 (42, 7, 2026, 123) —
count(c = 0.5) is 24 / 25 / 26 / 27, not the 28 ceiling,
on seeds 1 / 3 / 99 / 31337; claim (li) passes on 4/8 (the
same four) — the count is non-increasing fails on seed 1
(24 → 25 at d = 0.25) and count(d = 1) is 17 / 16 / 16,
above the 15 bar, on seeds 3 / 99 / 31337; claim (liii)
passes on 5/8 (42, 7, 2026, 1, 123) — count(c = 0.5,
d = 1) is 17 / 16 / 16 on seeds 3 / 99 / 31337, and the
swap fails on seed 3 by 0.0031 (0.2969 vs the 0.30 bar).
The count is a thresholded quantity (per pair, R ≥ 0.5
AND ν ≥ 0.10) that depends on the R distribution, not
just on the det sign — so the determinant gate governs
the concurrence response, not the count. Claims
(lxxxii)–(lxxxiv) are the re-gating on the file seeds
(where all three passed originally on the gated seeds);
claim (lxxxvi) is the survey extension, calibrated to
FAIL.

## Calibration pilot (job b) — disclosed before the run

The 12-seed Cogitate survey (recomputed; file seeds match
docs/seed-1234-diagnosis.md):

| seed | r(gap, mean_R) | r(gap, mean_D) | r(gap, max_D) | margin | mean_D peak σ | shape |
|---|---|---|---|---|---|---|
| 42 | 0.9028 | 0.7776 | −0.8070 | +0.1252 | 0.00 | falling |
| 7 | 0.8494 | 0.6477 | −0.9313 | +0.2017 | 0.00 | falling |
| 1234 | 0.8447 | 0.8839 | −0.9034 | −0.0393 | 0.10 | hump |
| 2026 | 0.8422 | 0.3430 | −0.5943 | +0.4992 | 0.00 | falling |
| 1 | 0.3813 | 0.4019 | −0.8020 | −0.0206 | 0.01 | hump |
| 2 | 0.4044 | 0.3483 | −0.2060 | +0.0561 | 0.10 | hump |
| 3 | 0.5000 | −0.1136 | −0.8243 | +0.6135 | 0.10 | hump |
| 99 | 0.7454 | 0.3906 | −0.6455 | +0.3548 | 0.25 | hump |
| 123 | 0.8823 | 0.0306 | −0.7542 | +0.8517 | 0.25 | hump |
| 777 | 0.8485 | 0.8459 | −0.9581 | +0.0025 | 0.00 | falling |
| 2024 | 0.7546 | 0.7171 | −0.0561 | +0.0375 | 0.00 | falling |
| 31337 | 0.9885 | 0.8969 | −0.0457 | +0.0916 | 0.05 | hump |

Margins sorted: −0.0393, −0.0206, +0.0025, +0.0375,
+0.0561, +0.0916, +0.1252, +0.2017, +0.3548, +0.4992,
+0.6135, +0.8517. Mean margin +0.2312, median margin
+0.1084, 10/12 positive, 6/12 ≥ 0.10. So a per-seed rule
with ANY bar ≥ 0.10 still fails on half the survey — the
per-seed framing is abandoned, not repaired.

A shape gate was considered and REJECTED: hump-shaped
mean_D does not separate the failures — seeds 3, 99, 123
are hump-shaped yet pass the 0.10 margin (+0.61, +0.35,
+0.85) because their r(mean_D) is low or negative, while
falling seeds 777 and 2024 fail it (+0.0025, +0.0375)
because their r(mean_D) ≈ r(mean_R). The shape is the
mechanism on 1234, but it is not the whole story: what
varies across seeds is r(mean_D) itself (−0.11 to +0.90),
and no per-seed shape statistic tames that spread.

What IS stable across the survey is the POOLED comparison.
Pooling all 84 runs (12 seeds × 7 σ values):

| predictor | pooled r(gap, ·) |
|---|---|
| mean_R | +0.6658 |
| post_R_sustained | +0.5373 |
| neg_var_D | +0.3791 |
| mean_D | +0.2636 |
| max_D | −0.5253 |
| broadcast | −0.5916 |

Pooled margin r(gap, mean_R) − r(gap, mean_D) = +0.4022.
Pooled, mean_R is the TOP-ranked of the six predictors
(next: post, +0.5373). Per-seed, mean_R ranks 1st on 4
seeds (2, 3, 99, 31337), 2nd on 6 (42, 7, 2026, 123, 777,
2024), 3rd on 1234, 4th on seed 1 — so the pooled
top-rank is not a per-seed claim in disguise; it is a
different statistical level, the same level as the pooled
regression in (lxiii), which passed (R² 0.6505 vs 0.3298
over 28 runs). Pooling averages out the per-seed
trajectory-shape noise that makes r(mean_D) swing from
−0.11 to +0.90, and asks the question (lx) was really
asking — does mean sensitivity predict the gap better
than individual D, in general — at the level where the
comparison is stable.

## Claims

### (lxxxii) Re-gated (l): concern raises resonance and empathy fraction, on gated seeds

The ORIGINAL claim (l) sub-checks (mean R strictly rising
in c, mean f strictly rising in c, quale count at c = 0.5
is the 28 ceiling), evaluated ONLY on the gated file seeds
— seeds in {42, 7, 1234, 2026} with baseline det mean
≥ −0.05, i.e. {42, 7, 2026} (1234 is excluded by the gate,
not by hand). PASS iff all sub-checks hold on every gated
file seed. Frozen thresholds: the original v0.16.0 bars,
unchanged. Calibration: passes (all three gated file seeds
passed (l) originally).

### (lxxxiii) Re-gated (li): distress lowers helping while raising resonance, on gated seeds

The ORIGINAL claim (li) sub-checks (at fixed concern
c = 0.5: mean R strictly rising in d, quale count
non-increasing in d, count(d = 1) ≤ 15,
R(d = 1) − R(d = 0) ≥ 0.04), evaluated ONLY on the gated
file seeds {42, 7, 2026}. PASS iff all sub-checks hold on
every gated file seed. Frozen thresholds: the original
v0.16.0 bars, unchanged. Calibration: passes.

### (lxxxiv) Re-gated (liii): channel separation, on gated seeds

The ORIGINAL claim (liii) sub-checks ((a) f(c = 2, d = 0)
≥ f* = 0.7278; (b) count(c = 0.5, d = 1) ≤ 15; (c) swap
|f(1, 0) − f(0, 1)| ≥ 0.30), evaluated ONLY on the gated
file seeds {42, 7, 2026}. PASS iff all sub-checks hold on
every gated file seed. Frozen thresholds: the original
v0.16.0 bars, unchanged. Calibration: passes.

### (lxxxv) Determinant-sign-conditioned concurrence, on the 12-seed survey

The mechanism-governed halves of (l) and (li), stated
against f only (no count sub-checks), on the whole
12-seed survey: (a) f(c, 0) strictly rises with c on
every GATED survey seed (8 seeds); (b) f(0.5, d) is
non-increasing in d on every GATED survey seed; (c) the
exact sign rule: no pair with det ≥ 0 ever falls under
concern at dose 0.25, on ANY of the 12 survey seeds
(0 pairs everywhere). PASS iff all three legs hold.
Frozen bar: exactness for (c) (0 pairs), strict
monotonicity for (a), non-increasing for (b).
Calibration: passes on all three legs (see pilot tables).
The distress half of the sign rule is NOT claimed: it
fails exactly on seeds 1, 2, 777 (see pilot).

### (lxxxvi) Full re-gated claims on all gated survey seeds

Claims (l), (li), (liii) with ALL original sub-checks
(including the quale-count sub-checks), evaluated on
every GATED survey seed (8 seeds). PASS iff all three
claims hold on every gated survey seed. Frozen
thresholds: the original v0.16.0 bars, unchanged.
Calibration: FAILS — (l) passes on 4/8, (li) on 4/8,
(liii) on 5/8 gated survey seeds (see pilot). This claim
is the survey extension of (lxxxii)–(lxxxiv), and its
expected FAIL is the finding: the determinant gate
rescues the concurrence halves, not the count halves.

### (lxxxvii) Pooled Cogitate rule replacing (lx)'s margin

The (lx) question — does mean sensitivity beat mean
individual D as a predictor of the gap — asked at the
POOLED level instead of per-seed: over all 84 runs (12
survey seeds × 7 σ values), (1) the pooled Pearson
margin r(gap, mean_R) − r(gap, mean_D) ≥ 0.10 AND
(2) r(gap, mean_R) is the largest of the six pooled
Pearson correlations (mean_R, mean_D, max_D, neg_var_D,
post, broadcast). PASS iff both legs hold. Frozen bar:
0.10 (the same bar (lx) used, now applied to the pooled
margin, so the new rule is judged on the old scale).
Calibration: passes (pooled margin +0.4022; pooled
r(mean_R) = +0.6658, top-ranked). This is a NEW claim at
a different statistical level; the old (lx) verdict
(FAIL, honest, per-seed 0.10 margin) stands unchanged,
and no per-seed margin bar is claimed here — a per-seed
rule with any bar ≥ 0.10 fails on half the survey (see
pilot), and the pooled rule does not erase that.

## Seeds

- Calibration (job a): 42, 7 (gate frozen from these
  only: det means −0.0431 / +0.1050).
- File seeds (job a, claims (lxxxii)–(lxxxiv)): 42, 7,
  1234, 2026, gated by the rule above.
- Survey seeds (job a, claims (lxxxv)–(lxxxvi); job b,
  claim (lxxxvii)): 42, 7, 1234, 2026, 1, 2, 3, 99, 123,
  777, 2024, 31337 (the v0.21.0 diagnostic survey; its
  numbers are the calibration data for the new rules and
  are disclosed in full in the pilot tables above).
- Fresh seeds (diagnostic only, NOT gated, reported
  alongside (lxxxvii)): 5, 11, 555, 4242 — never used
  anywhere in the tree before this build. The diagnostic
  computes the per-seed (lx)-margins and the pooled
  margin over these 4 fresh seeds only (28 runs) and
  reports them; it changes no verdict. If the fresh-seed
  pooled margin is below 0.10, that is reported as a
  limit on (lxxxvii), not hidden.

## What would falsify

- (lxxxii): any gated file seed failing any original (l)
  sub-check.
- (lxxxiii): any gated file seed failing any original
  (li) sub-check.
- (lxxxiv): any gated file seed failing any original
  (liii) sub-check.
- (lxxxv): any gated survey seed where f(c, 0) does not
  strictly rise, any gated survey seed where f(0.5, d)
  re-rises, or any survey seed with a det ≥ 0 pair
  falling under concern at dose 0.25.
- (lxxxvi): any gated survey seed failing any original
  sub-check of (l), (li), or (liii). (Calibrated to fail.)
- (lxxxvii): pooled margin < 0.10, or any other predictor
  with a higher pooled correlation than mean_R.

## Honesty

Synthetic, classical emulation throughout. Nothing here
measures consciousness, empathy in a human, or any theory
of consciousness. No scalar Φ is computed anywhere and
none is presented as a consciousness measure; E = hν is
used only as the defined per-mode empathy unit (v0.11.0),
never as a Planck theory of consciousness. The gate is a
condition on a measured property of a noise draw (the
baseline determinant distribution of one RNG stream), not
a physical regime boundary; a "seed" is an RNG-stream
label. The new Cogitate rule (lxxxvii) was frozen from the
same 12-seed survey it is evaluated on — it is a
calibration result, not a held-out test — and the
fresh-seed diagnostic (seeds 5, 11, 555, 4242) is the
only held-out check in this build for job (b). The
re-gated claims (lxxxii)–(lxxxiv) exclude seed 1234 by a
stated rule, not by hand, and claim (lxxxvi) reports
exactly where that rule stops working on fresh survey
seeds. No threshold was moved to force a pass: the count
sub-checks fail under the gate on the survey, and that
failure is claimed as (lxxxvi), not hidden.
