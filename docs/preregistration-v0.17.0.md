# Pre-registration — v0.17.0: Connectome-harmonic / structure–function coupling analogue, claims (liv)–(lvi)

Written 2026-11-18, BEFORE the evaluation run on the held-out
seeds 1234 and 2026. Thresholds are round numbers frozen from
a calibration pilot on seeds 42 and 7 only. No threshold in
this file may be moved after the evaluation run.

## The spec being tested

Deep-think upgrade #10 (report.md §9, §2): connectome
harmonic decomposition (CHD, Atasoy et al. 2016) and the
structure–function coupling finding of Luppi et al.,
*Communications Biology* 6:117, 2023 (established finding):
loss of consciousness (propofol anaesthesia, disorders of
consciousness) = *increased* structure–function coupling
across scales; LSD/ketamine = the opposite (decoupling),
correlating with subjective scores. The report's falsifiable
prediction for the bridge: loss of attunement (PARTIAL, high
σ) = *increased* structure–function coupling (activity
collapses onto structure, as in anaesthesia/DOC); ATTUNED =
intermediate coupling; psychedelic-like decoupling is *not*
attunement. Falsified if attunement is monotone in coupling
(report.md §9 rank 10). Lower rank only because it needs a
graph construction the project does not yet have — this
version builds that graph.

## The construction (fixed before the pilot)

- Base field: the v0.5.0 resonance population (8 agents,
  noisy copies of the uniform thought), on the noise grid
  σ in (0.10, 0.25, 0.50, 1.00). σ = 0.25 is the attuned
  reference (the v0.4.0 fix holds at σ ≤ 0.25 and breaks
  at σ ≥ 0.50); σ = 0.50 is the break; σ = 1.00 is the
  far-broken regime.
- Structure graph: the coupling matrix W with W_ij = R_ij
  = |<ψ_i|ψ_j>|^2 for i ≠ j, W_ii = 0 (the thought-pair
  coupling matrix — the graph the project did not yet
  have). Graph Laplacian L = D − W, D_ii = Σ_j W_ij.
  Harmonic modes are the eigenvectors of L, eigenvalues
  λ_0 = 0 ≤ λ_1 ≤ … ≤ λ_7 (Atasoy et al. 2016 CHD).
- Functional connectivity: F_ij = the Bhattacharyya
  coefficient Σ_k √(p_ik · p_jk) between the agents'
  Born distributions p_i, p_j. F is genuinely distinct
  from W: W is the squared overlap of the amplitude
  vectors (phase/sign-sensitive), F is the overlap of
  the probability vectors (sign-blind). At low σ the
  two track each other almost exactly (see the
  near-parallel disclosure below); at σ = 0.50 they
  part ways, which is where the measurement lives.
- Structure–function coupling κ(σ) = the Pearson
  correlation between the upper-triangular entries of
  W and of F (28 pairs). This is the standard
  connectomics definition of structure–function
  coupling (correlation of structural and functional
  connectivity), applied to the bridge's graph.
- Harmonic smoothness of a per-node functional signal
  x (here x = mean-D vector D_i, the self-determinism
  per agent): the Rayleigh quotient RQ(x) = x_c^T L x_c
  / x_c^T x_c on the centred signal, normalised by the
  mean nonzero eigenvalue, ρ(x) = RQ(x) / mean(λ_1..λ_7).
  ρ < 1 means smoother than random on the graph
  (structure-aligned); ρ ≈ 1 means random-like
  (decoupled); ρ > 1 means rougher than random. RQ is
  basis-independent, which matters here: at low σ the
  graph is near-complete and λ_1..λ_7 are nearly
  degenerate (7.59–7.89 at σ = 0.10 on seed 42), so a
  low-frequency energy share depends on an arbitrary
  choice of basis inside the degenerate subspace and
  is NOT used as a gated measure. (Pilot 1: the
  low-2-mode energy share of the D signal is
  seed-unstable — 0.10/0.80 at σ = 0.10, 0.25/0.68
  at σ = 0.25 — exactly the degeneracy artefact.
  It is reported in the module docstring, not gated.)
- Decoupling control: permute the entries of F (50
  permutations, fixed rng seed 1000 + seed) and
  recompute κ. The shuffle detaches function from
  structure while leaving the field — and therefore
  f, the attunement status — unchanged by
  construction, so it is the psychedelic-like
  decoupling analogue: low coupling without any
  change in attunement.

## Calibration pilot (seeds 42 and 7) — disclosed before the run

κ(σ), seeds 42 / 7:
σ = 0.10: 1.0000 / 1.0000; σ = 0.25: 0.9989 / 0.8422;
σ = 0.50: 0.3997 / 0.4119; σ = 1.00: 0.8069 / 0.6392.
Shuffle null (mean of 50 perms): |mean| ≤ 0.039 at every
σ on both seeds (mean |κ_shuf| 0.15–0.18, max |κ_shuf|
≤ 0.66 on a single draw — the null is centred on zero
with a wide single-draw spread, which is why the mean
over 50 perms, not a single draw, is gated).
ρ(D): 1.006 / 0.986 (σ = 0.10), 1.019 / 0.871 (σ = 0.25),
0.871 / 0.831 (σ = 0.50), 1.125 / 0.962 (σ = 1.00);
worst |ρ − 1| = 0.169. Shuffled-D null: mean ρ ≈ 1.00
(sd ≤ 0.20) at every σ — the D signal is harmonically
indistinguishable from a random permutation of itself.

Two disclosures, before the run:
1. The report's directional prediction already FAILS on
   the calibration seeds: κ(0.50) is BELOW κ(0.25) by
   0.599 / 0.430, and κ(1.00) is below κ(0.25) by
   0.192 / 0.203. Loss of attunement does NOT raise
   coupling in this wiring — the broken regime is the
   LEAST coupled, not the most. Claim (lv) gates the
   report's prediction as stated and is expected to
   FAIL; claim (lvi) gates the shape that IS measured.
   This mirrors v0.5.0 claim (xiii), whose break half
   was known from the pilot to fail and was kept.
2. κ ≈ 1.0000 at σ = 0.10 on both seeds is a
   near-parallel artefact, not a discovery: at σ = 0.10
   all agents are near-identical (sd(W) ≈ 0.02), so W
   and F are both ≈ 1 with the same noise driving both
   deviations, and their correlation is trivially ≈ 1.
   κ(0.10) is therefore REPORTED, not gated, in every
   claim. The gated shape uses σ = 0.25 / 0.50 / 1.00.

## Claims

### (liv) CHD machinery is exact, and node signals are harmonically random-like

On EVERY seed in {42, 7, 1234, 2026} and EVERY σ in
(0.10, 0.25, 0.50, 1.00):
(a) the Laplacian identities hold exactly: L is
symmetric (max |L − L^T| < 1e-12), L is positive
semidefinite (min eigenvalue ≥ −1e-12), λ_0 ≈ 0
(|λ_0| < 1e-12), eigenvalues are sorted ascending,
and the eigenvectors are orthonormal (max |U^T U − I|
< 1e-12);
(b) the D signal is harmonically random-like:
|ρ(D) − 1| ≤ 0.20.
PASS iff (a) and (b) hold on every seed × σ. Frozen
bar: 0.20 (round number just above the calibration
worst |ρ − 1| = 0.169). The low-frequency energy share
is reported, not gated (degeneracy artefact, above).

### (lv) The Luppi prediction as stated: coupling rises with loss of attunement

κ(σ) = corr(W, F) on the σ grid. PASS iff, on EVERY
seed in {42, 7, 1234, 2026}: κ(0.50) ≥ κ(0.25) + 0.10
AND κ(1.00) ≥ κ(0.25) + 0.10. Frozen bar: 0.10 (a
rise smaller than this would not be a meaningful
increase against the shuffle null's single-draw
spread). Calibration: κ(0.50) − κ(0.25) = −0.599 /
−0.430; κ(1.00) − κ(0.25) = −0.192 / −0.203 — the
prediction fails on both calibration seeds, so this
claim is expected to FAIL on the evaluation seeds
too. The failure is the result: in this wiring the
broken regime is less coupled than the attuned one,
the reverse of the anaesthesia/DOC direction.

### (lvi) The measured shape: coupling dips at the break and recovers, and decoupling is not attunement

PASS iff, on EVERY seed in {42, 7, 1234, 2026}:
(a) the attuned field is strongly coupled:
κ(0.25) ≥ 0.80;
(b) coupling dips at the break: κ(0.50) ≤
κ(0.25) − 0.30;
(c) coupling recovers past the break: κ(1.00) ≥
κ(0.50) + 0.10;
(d) the decoupling control sits near zero while the
attuned field sits high: |mean κ over 50 shuffles
at σ = 0.25| ≤ 0.10 AND κ(0.25) − |mean shuffled κ
at σ = 0.25| ≥ 0.50.
The shuffle leaves f unchanged by construction (it
permutes F entries only), so (d) is the
decoupling-is-not-attunement check: a decoupled
functional pattern can sit on the same field with
the same attunement status. Frozen bars: 0.80
(round number below the calibration worst κ(0.25)
= 0.842), 0.30 (round number below the calibration
worst dip 0.430), 0.10 (round number below the
calibration worst recovery 0.227), 0.10 (round
number above the calibration worst |shuffle mean|
= 0.039), 0.50 (round number below the calibration
worst κ(0.25) − |shuffle mean| = 0.812).

## Seeds

- Calibration: 42, 7 (thresholds frozen from these only).
- Evaluation: 1234, 2026 (held out; first touched by the
  evaluation run after this file was written).

## What would falsify

- (liv): any seed × σ where a Laplacian identity fails
  beyond 1e-12, or where |ρ(D) − 1| > 0.20 (a signal
  strongly aligned with, or strongly anti-aligned
  against, the graph harmonics).
- (lv): any seed where κ does not rise by at least 0.10
  from σ = 0.25 to σ = 0.50 or to σ = 1.00. (Expected:
  every seed.)
- (lvi): any seed where the attuned κ(0.25) < 0.80,
  where the dip to σ = 0.50 is < 0.30, where the
  recovery to σ = 1.00 is < 0.10, or where the shuffle
  null at σ = 0.25 is not near zero / not separated
  from κ(0.25) by 0.50. A κ(0.25) near the shuffle null
  would mean the attuned field is itself decoupled —
  the CHD analogue would carry no signal at all.
