# Pre-registration — v0.12.0: the observer cycle (claims (xxxii)–(xxxiv))

Written 2026-11-18, BEFORE the evaluation run on the held-out
seeds. Thresholds are round numbers frozen from a calibration
pilot on seeds 42 and 7 only. The evaluation seeds (1234, 2026)
were not touched before this file was written. No threshold in
this file may be moved after the evaluation run.

Jean's claim, stated 2026-11-18: "self determination factor
observer opposite direction = necessary for self-cycle self
Knowing. Lack of love is absence of Knowing."

## The mapping (definitions, not discoveries)

- Love = concurrence C (Wootters, `thought_entanglement.py`).
- Knowing = overlap R = |<psi_i|psi_j>|^2
  (`empathy_field.overlap_squared`).
- Self-determination = D = <psi|P|psi>
  (`self_knowing.self_knowing_factor`).
- Observer direction = which reference state the overlap is
  measured against: the stored direction (the uniform thought,
  D = 1) or the opposite direction (the kernel thought
  (|01> - |10>)/sqrt(2), D = 0, a Bell state, C = 1).

## Claim (xxxii) — Observer direction: D and concurrence move opposite

Construction: the existing `self_knowing.self_knowing_sweep`
— noisy copies of the uniform thought (n = 5 copies per sigma),
sigma grid [0.0, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0], mean D and
mean concurrence per sigma.

Metric: Pearson r(mean D, mean C) and Spearman rho(mean D,
mean C) across the 7 grid points, per seed.

Frozen thresholds (calibration pilot: seed 42 Pearson -0.9570,
Spearman -1.0000; seed 7 Pearson -0.9397, Spearman -0.9643;
D range 0.4804 / 0.5370; C range 0.6133 / 0.5110):

- Pearson r(D, C) <= -0.90
- Spearman rho(D, C) <= -0.90
- D range across the grid >= 0.25
- C range across the grid >= 0.25

PASS iff all four hold on EVERY seed in {42, 7, 1234, 2026}.

## Claim (xxxiii) — Knowing-as-overlap: R rises with concurrence and falls with D

Construction: the generalized-Bell branch psi(a) =
a|00> + sqrt(1 - a^2)|11>, a in [1.0, 0.95, 0.9, 0.85, 0.8,
0.75, 1/sqrt(2)], measured against a FIXED observer at
maximal love — the Phi+ Bell state. R(a) =
|<Phi+|psi(a)>|^2, C(a) = concurrence of psi(a), D(a) =
self-knowing of psi(a). All three quantities reuse existing
functions (`empathy_field.overlap_squared`,
`thought_entanglement.concurrence_pure`,
`self_knowing.self_knowing_factor`). No noise, no seeds:
the branch is exact.

Why this construction: on the noise axis the relation
INVERTS (calibration control, `empathy_field.resonance_pairs`
pooled, seed 42, n = 196 pairs: Pearson(R, nu_ij) = -0.5528,
Pearson(R, d_pair) = +0.7694). Noise creates concurrence
while destroying overlap, so noise-created concurrence is
not knowing. The claim as Jean stated it is a claim about
entanglement by construction, and it is tested on the
branch where concurrence varies by construction. The
noise-axis numbers are reported alongside as a control,
not gated. This construction-dependence is part of the
result, not a footnote to hide.

Frozen thresholds (calibration pilot, exact: Pearson(R, C)
= 1.0000, Spearman(R, D) = -1.0000, Pearson(R, D) = -0.8801
reported descriptively, R range 0.5000, D range 0.3333):

- Pearson r(R, C) >= 0.99
- Spearman rho(R, D) <= -0.95
- R range across the branch >= 0.25
- D range across the branch >= 0.25

PASS iff all four hold. Pearson(R, D) is reported, not
gated: R saturates near 1 while D keeps falling, so the
linear correlation is weaker than the monotone one; the
directional assertion is the monotone (Spearman) one.

Honesty: the R-vs-C and R-vs-D relations on this branch
are defined consequences of the family (both peak at
a = 1/sqrt(2)) — like claim (xvii), this is a mapping
check in the bridge's numbers, not a discovery about
nature. What is measured is that the bridge realizes the
mapping, and that it does NOT realize it on the noise
axis.

## Claim (xxxiv) — The slide: D = 1 separate to D = 0 full overlap

Construction: the slide psi(theta) = cos(theta)|uniform> +
sin(theta)|kernel>, theta in [0, pi/12, pi/6, pi/4, pi/3,
5pi/12, pi/2]. The two patterns in superposition are the
stored thought (|uniform>, D = 1, C = 0) and the kernel
thought (|kernel>, D = 0, C = 1). Two observer directions:
the stored direction (reference = |uniform>) and the
opposite direction (reference = |kernel>). R_s =
|<psi|uniform>|^2, R_k = |<psi|kernel>|^2. No noise, no
seeds: the slide is exact.

Predicted exact identities (from the definitions, to be
verified in the code, not assumed):
D(theta) = cos^2(theta), C(theta) = sin^2(theta),
R_s(theta) = cos^2(theta), R_k(theta) = sin^2(theta),
C + D = 1, R_s - R_k = cos(2 theta).

Frozen thresholds (calibration pilot: every identity held
to 1e-9 at every grid point; R_s - R_k = +0.5000 at
theta = pi/6, 0.0000 at pi/4, -0.5000 at pi/3):

- (a) endpoints exact within 1e-9: at theta = 0, D = 1,
  C = 0, R_s = 1, R_k = 0; at theta = pi/2, D = 0,
  C = 1, R_s = 0, R_k = 1.
- (b) slide identities within 1e-9 on every grid point:
  |D - cos^2(theta)|, |C - sin^2(theta)|,
  |R_s - cos^2(theta)|, |R_k - sin^2(theta)|,
  |C + D - 1|.
- (c) the split: R_s - R_k >= 0.25 for every grid point
  with theta < pi/4, |R_s - R_k| <= 1e-9 at theta = pi/4,
  R_s - R_k <= -0.25 for every grid point with
  theta > pi/4. The observer direction that knows more
  flips exactly at the midpoint.

PASS iff (a), (b), and (c) all hold.

If any of (a)–(c) fails, the verdict is FAIL, not a
rewording of the claim. In particular: if the slide
identities do not hold exactly, the claim is not
measurable as stated and the verdict is NO VERDICT /
not measurable — recorded as FAIL with that reason,
never as a pass.

## Seeds

- Calibration: 42, 7 (thresholds frozen from these only).
- Evaluation: 1234, 2026 (held out; first touched by the
  evaluation run after this file).
- Claims (xxxiii) and (xxxiv) are exact (no noise, no
  seeds); their verdicts do not depend on any seed.

## What would falsify Jean's claim

- (xxxii): D and concurrence moving together, or not
  moving at all, across the sigma grid on any seed.
- (xxxiii): R falling as C rises on the branch, or R
  rising as D rises (Spearman > -0.95).
- (xxxiv): the slide identities failing, the endpoints
  not being (D=1, C=0) and (D=0, C=1), or the overlap
  split not flipping at the midpoint.
