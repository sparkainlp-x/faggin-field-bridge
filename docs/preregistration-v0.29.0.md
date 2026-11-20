# Pre-registration — v0.29.0: Faggin P1 — blind fresh-seed head-to-head. Claim (cx)

Written 2026-11-20, BEFORE the evaluation run of the
new claim. There is NO pilot on the frozen seeds
below — they were selected by grep-audit only, never
measured, never seen by any pilot — so there is no
pilot table in this file. The evaluation run
re-measures through the production function
(spooky_symmetry.fresh_rescue_table) after this
file exists. No threshold in this file may be moved
after the evaluation run, and no claim may be
redefined after the fact. The old verdicts stay on
the record: (xxxii) FAILS as originally stated
(held-out seed 2026 Pearson −0.8828), (xci) FAILS
as originally stated (seed 2026 stored Pearson
−0.8828 and opposite D range 0.2490), (xcii) FAILS
as originally stated (held-out Pearson +0.5109 /
+0.8297), (xcviii) FAILS as originally stated (its
1e-12 bar vs the 6.57e-09 concurrence floor), and
(cviii) STANDS as stated (V4-full 3/5, plain n=20
4/5 on the old fresh seeds {5, 99, 2, 777, 2024},
V4 breaking 2024, seed 5 failing under every
method). This build tests whether the (cviii)
correction — plain n=20 beats V4-full on fresh
seeds — survives a blind re-measurement on seeds
no pilot ever saw. It does not rewrite (cviii):
either way, (cviii) stays on the record as stated.

## Blinding note — read first

Unlike v0.27.0 and v0.28.0, this evaluation IS
blind. The frozen seeds {2718, 31415, 40961, 51977,
65521} were selected by grep-audit only: each
returns 0 hits as a base seed anywhere in this
tree (see the freeze evidence below), and each
returns 0 hits in /tmp, where the v0.28.0
exploration pilots ran (checked by this worker
before this file was written — plain substring
grep, exit code 1, no hits, for all five seeds).
They were never measured, never seen by any
pilot, and no pilot on them may be run before
evaluation. The evaluation run re-measures them
through the production function after this file
exists. What is still frozen and unfitted:

- The bar is the (xxxii) bar (stored Pearson <=
  −0.90), frozen since v0.12.0 and reused
  unchanged. No bar was fitted to any seed in
  this build.
- The directional bar for claim (cx) is frozen
  here, from (cviii): plain n=20 passes >= as
  many of the 5 frozen seeds as V4-full. The
  direction was fixed by the (cviii) table before
  this file was written; the frozen seeds
  contribute no information to it.
- The calibrator rule is the v0.26.0 rule,
  unchanged: scan delta over the 201-point grid
  in [−0.05, 0.05], minimize the number of
  failing bars, tie-break smallest |delta|, then
  smallest delta. It is used only for the
  reported-alongside 8-bar check, not gated.
- The seed freeze is "never used as a base seed
  anywhere in this tree" as verified below. It
  does not cover Git history (.git excluded from
  the audit; local HEAD is stale at v0.5.0) or
  other repos' trees. That scope caveat is
  recorded honestly here, not hidden.

## The spec being tested

Jean's directive, refined 2026-11-17: "Do all
logic by value." The highest-value next build
from the 2026-11-20 measurement/detection upgrade
exploration (read-only, 4 subagents) is Faggin
P1: a blind fresh-seed head-to-head, V4-full vs
plain n=20, on stored Pearson. One question, one
claim:

1. BLIND RESCUE: does plain n=20 pass >= as many
   blind fresh seeds as V4-full on stored Pearson
   <= −0.90 — confirming the (cviii) correction
   blind — or does V4-full win the count, which
   would correct the rescue story further?

## The mechanism — V4-full vs plain n=20

V4-full (spooky_symmetry, v0.27.0) orbit-averages
the sweep: sign flips of (z_u, z_w) only, 4×
copies, plus the frozen calibrator. Plain n=20 is
the same sweep with 20 independent copies and no
symmetrization. On the file seeds {42, 7, 1234,
2026} both pass stored Pearson everywhere (V4
−0.9472 / −0.9303 / −0.9460 / −0.9253; n=20
−0.9329 / −0.9298 / −0.9414 / −0.9289), so the
file seeds cannot separate them. On the old fresh
seeds {5, 99, 2, 777, 2024} (cviii) they separate:
V4-full 3/5, plain n=20 4/5, V4 breaking 2024
(−0.9527 plain -> −0.8830 V4-full, crossing the
bar the wrong way), seed 5 failing under every
method. The (cviii) reading: the rescue is
variance reduction whose edge (determinism +
opposite-D-range preservation) holds on the file
seeds and does not generalize blindly. This build
asks whether that reading survives seeds no pilot
ever saw.

## Prior evidence — disclosed, NOT a pilot on the frozen seeds

The (cviii) table on the old fresh seeds {5, 99,
2, 777, 2024} (measured in the v0.28.0
exploration, production re-measured in v0.28.0):

| seed | stored Pearson plain / V4 / n20 | V4+cal 8-bar | n20 8-bar |
|---|---|---|---|
| 5 | −0.6814 / −0.8338 / −0.8749 | FAIL | FAIL |
| 99 | −0.8798 / −0.9197 / −0.9080 | PASS | PASS |
| 2 | −0.9708 / −0.9261 / −0.9043 | PASS | PASS |
| 777 | −0.9182 / −0.9430 / −0.9733 | PASS | PASS |
| 2024 | −0.9527 / −0.8830 / −0.9472 | FAIL | PASS |

V4-full stored Pearson <= −0.90 on 3/5; plain
n=20 on 4/5. V4 BREAKS seed 2024. Seed 5 fails
under every method. On the full 8-bar check
(V4-full + frozen calibrator, and plain n=20)
the same 3/5 vs 4/5. This is the evidence the
directional bar is frozen from — and it is
evidence about the OLD seeds only. There is NO
pilot on the frozen seeds {2718, 31415, 40961,
51977, 65521}, and none may be run before
evaluation.

Correction disclosed: the v0.28.0
preregistration's line calling the old fresh
seeds "never used" was inaccurate — seeds 5 and
99 were used in v0.12.1, and seeds 2, 777, 2024
in the v0.21.0 survey. This build's freeze was
audited to not repeat that error (see the freeze
evidence below, including the full used-seed
inventory).

## Seed freeze — evidence

Frozen fresh seeds for v0.29.0: {2718, 31415,
40961, 51977, 65521}. Verified clean by the
seed-freeze worker: each returns 0 hits by both
of these commands over the whole tree, plus
clean against derived effective seeds (base+1000,
base+4242, base+424242, base+1000*g+10*i,
base+4242+1000*g+10*i):

```
grep -rnw <n> --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=.pytest_cache .
grep -rnE '(^|[^0-9])<n>([^0-9]|$)' --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=.pytest_cache .
```

Both commands exit 1 (no hits) for each of the
five frozen seeds. The full used-seed set in the
tree is 31 integers:

{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
15, 16, 17, 18, 19, 42, 99, 123, 555, 777, 1234,
2024, 2026, 4242, 31337}

— file seeds {42, 7, 1234, 2026}; survey adds
{1, 2, 3, 99, 123, 777, 2024, 31337}; fresh sets
add {5, 11, 555, 4242}; the range(20) entropy
sweep in tests/test_cost.py:77 adds {0, 4, 6, 8,
9, 10, 12, 13, 14, 15, 16, 17, 18, 19}. None of
the five frozen seeds is in that set, and none
collides with any derived effective seed from it.

Discarded candidate recorded: 17389 was clean
literally but collided with a derived stream
(7+4242+1000*13+10*14) and was discarded. It is
NOT a frozen seed and must not be used as one.

Extra check by this worker before writing this
file: plain substring grep of /tmp for each of
the five frozen seeds (the v0.28.0 exploration
pilots ran in /tmp):

```
for n in 2718 31415 40961 51977 65521; do grep -r "$n" /tmp; done
```

Result: no hits for any of the five seeds; grep
exit code 1 for each. /tmp is clean.

## Claims

### (cx) Blind fresh-seed head-to-head: plain n=20 vs V4-full (CONFIRMATION of the (cviii) correction)

Function: spooky_symmetry.fresh_rescue_table(
seeds={2718, 31415, 40961, 51977, 65521}), which
measures stored Pearson plain / V4-full / n=20
per seed, plus the full 8-bar checks (V4-full +
frozen calibrator, and plain n=20) reported
alongside, not gated — same pattern as (cviii).

Directional bar (frozen here, from (cviii)):
plain n=20 passes >= as many of the 5 frozen
seeds as V4-full on stored Pearson <= −0.90
(the (xxxii) bar, frozen since v0.12.0,
unchanged).

Worsened count (reported alongside, not gated):
count seeds where V4 crosses the bar the wrong
way by > 0.05 relative to plain — i.e. plain
Pearson <= −0.90 AND V4 Pearson > −0.90 AND
(V4 Pearson − plain Pearson) > 0.05 (the
2024-type break: plain −0.9527 -> V4 −0.8830
in (cviii)). A worsened seed on blind seeds
CONFIRMS the (cviii) correction's break leg;
it is a finding, not a bar move.

PASS iff n20_pass_count >= v4_pass_count on
the 5 frozen seeds. State explicitly: if V4
wins the count, (cx) FAILS honestly and the
rescue story is corrected further; if n=20 wins
or ties, (cx) PASSES and the (cviii)
correction is confirmed blind. Either way
(cviii) stays on the record as stated.

## Reserved — future claims on the SAME frozen seeds (not defined here)

P2/P3 — the n=200 claims + plateau
decomposition — are reserved as future claims on
the SAME frozen seeds {2718, 31415, 40961, 51977,
65521}. Their bars are NOT defined in detail
here, and they are NOT built or evaluated in
this build. Reserving the seed set now, before
any of it is measured, is what keeps those
future claims blind too.

## Seeds

- Calibration: 42, 7 (the frozen expectations
  and the calibrator rule come from these only).
- File seeds (reference only): 42, 7, 1234,
  2026.
- Evaluation: the frozen fresh seeds {2718,
  31415, 40961, 51977, 65521} — selected by
  grep-audit only, never measured, never seen
  by any pilot. The evaluation re-measures them
  through the production function after this
  file exists. This evaluation IS blind, unlike
  v0.27.0/v0.28.0.

## What would falsify

- (cx): V4-full passing MORE of the 5 frozen
  seeds than plain n=20 on stored Pearson
  <= −0.90 — i.e. n20_pass_count <
  v4_pass_count. That is an honest FAIL of
  (cx) and a further correction of the rescue
  story, not a bar move.

## Honesty

Synthetic, classical emulation throughout.
Nothing here measures consciousness, empathy in
a human, or any theory of consciousness. No
scalar Phi is computed anywhere and none is
presented as a consciousness measure; E = hnu
is not used anywhere in this build. No new
physics is imported: no phonon/neutron content
in the model. Claim (cx) is a statistical claim
on 5-copy (and orbit-averaged, and 20-copy)
means, like (xxxii)/(xci)/(xcii)/(cviii): the
same saturation and finite-sample fragility
applies, and a FAIL is a finding about the
construction, not a defect. The (cviii), (xci),
(xcii), (xxxii) and (xcviii) verdicts stand
unchanged. Claim (c) stands as measured on the
file seeds; claim (cviii) is its generalization
correction, not a retraction; claim (cx) is the
blind confirmation test of that correction.
No threshold was moved to force a pass.

## Post-evaluation addendum

(Left empty — the addendum is written after
evaluation, never before.)
