# Pre-registration — v0.22.0: per-generation PID — does the synergy-vs-σ climb survive without pooling? Claims (lxxiii)–(lxxvii)

Written 2026-11-18, BEFORE the evaluation run on the held-out
seeds 1234 and 2026 for the per-generation computation.
Thresholds are round numbers frozen from a calibration
pilot on seeds 42 and 7 only. No threshold in this file
may be moved after the evaluation run, and no claim may
be redefined after the fact.

## The spec being tested

The v0.20.0 XOR build (claims (lxiv)–(lxvii)) found
synergy climbing toward the 2-bit ceiling with σ on
every seed — claim (lxvi) FAILED honestly: synergy
tracks noise-driven uniformity, not resonance
(Pearson(Syn_collab, R_post) = 0.3731 / 0.3424;
Syn_collab rises from σ = 0.25 to σ = 0.50). But the
v0.20.0 report disclosed a confound: the pooled joint
is a MIXTURE of per-generation products, and the
mixture-correlation is itself synergistic about the XOR
target — the isolated arm is NOT synergy-free at high σ
(Syn_isol up to 1.0755 bits at σ = 1.00). This build
asks whether the climb survives when the PID is computed
PER GENERATION (no pooling across generations), for the
XOR target and the MAX target, on the same seeds and σ
grid the pooled results used (seeds 42, 7 calibration;
1234, 2026 held-out; σ grid [0.0, 0.01, 0.05, 0.1,
0.25, 0.5, 1.0]; design B, N = 2, 10 generations).

The method reuses the existing PID machinery
(total_information_target.target_pid_from_joint — the
general Williams & Beer I_min PID for any deterministic
target Y = f(X1, X2) — and the same design-B evolution
as pid.pair_arm_distributions) and adds a
per-generation computation path: the exact per-generation
product joint p1 ⊗ p2 is kept for each of the 10
generations instead of being pooled. Nothing about the
PID measure changes. The comparison is mean-per-generation
atoms vs pooled atoms, and it is stated here before the
run that the pooled atom is NOT an average of the
per-generation atoms (the PID is nonlinear in the joint,
and the pooled joint is a mixture) — so a gap between
the two is expected in general; the question is its
size and direction.

## Decision rule, stated in advance

- "The climb survives per-generation" means claim
  (lxxiv) PASSES: the per-generation mean synergy about
  the XOR target still climbs toward the 2-bit ceiling
  at the top of the σ grid.
- "The climb is a pooling artifact" means claim
  (lxxiv) FAILS. If it fails, the (lxvi) conclusion —
  "synergy climbs toward the 2-bit ceiling with σ" — is
  DOWNGRADED to a pooling artifact: the climb is
  manufactured by pooling across generations, and the
  noise-driven-uniformity reading is replaced by it.
  If (lxxiv) passes, the noise-driven-uniformity
  conclusion hardens.
- Either outcome is a result; neither is softened.

## Calibration pilot (seeds 42 and 7) — disclosed before the run

Per-generation mean Syn_collab, XOR target (pooled in
parentheses), in bits:

| seed | 0.00 | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---|---|---|---|---|---|---|
| 42 per-gen | 1.0000 | 1.0057 | 0.9675 | 0.8745 | 0.9887 | 1.1496 | 1.0933 |
| 42 pooled | 1.0000 | 1.0085 | 1.0809 | 1.1467 | 1.4472 | 1.7178 | 1.8432 |
| 7 per-gen | 1.0000 | 0.9533 | 0.5670 | 0.5197 | 0.9542 | 1.1058 | 0.9855 |
| 7 pooled | 1.0000 | 0.9746 | 0.7889 | 0.8985 | 1.4865 | 1.7892 | 1.7933 |

Per-generation mean Syn_collab, MAX target (pooled in
parentheses), in bits:

| seed | 0.00 | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---|---|---|---|---|---|---|
| 42 per-gen | 0.5000 | 0.5211 | 0.6167 | 0.5903 | 0.6289 | 0.6355 | 0.4889 |
| 42 pooled | 0.5000 | 0.5245 | 0.6815 | 0.7965 | 1.0279 | 1.1766 | 0.9449 |
| 7 per-gen | 0.5000 | 0.5519 | 0.3708 | 0.3674 | 0.5513 | 0.5585 | 0.4180 |
| 7 pooled | 0.5000 | 0.5680 | 0.5637 | 0.7192 | 1.0316 | 0.9803 | 0.9357 |

Per-generation mean atoms at σ = 0.25 (calibration),
in bits — mean ΔI, ΔSyn, ΔRed, ΔUniq, and the synergy
share of the mean gap (mean ΔSyn / mean ΔI):

| target | seed | mean ΔI | mean ΔSyn | mean ΔRed | mean ΔUniq | share |
|---|---|---|---|---|---|---|
| xor | 42 | +1.7457 | +0.9887 | +0.2582 | +0.4989 | 0.566 |
| xor | 7 | +1.7649 | +0.9542 | +0.1849 | +0.6257 | 0.541 |
| max | 42 | +1.6419 | +0.6289 | +0.4132 | +0.5998 | 0.383 |
| max | 7 | +1.6598 | +0.5513 | +0.3208 | +0.7878 | 0.332 |

Pooled Syn_isol (XOR) vs per-generation mean Syn_isol
(XOR), in bits — the mixture excess:

| seed | σ = 0.50 pooled | σ = 0.50 per-gen | σ = 1.00 pooled | σ = 1.00 per-gen | excess at 1.00 |
|---|---|---|---|---|---|
| 42 | 0.9610 | 0.0000 | 1.0755 | 0.0000 | +1.0755 |
| 7 | 0.6000 | 0.0000 | 1.0000 | 0.0000 | +1.0000 |

Four disclosures, before the run:
1. The per-generation XOR synergy curve is FLAT on
   calibration (~0.5–1.15 bits, no climb toward 2
   bits) and FALLS from σ = 0.50 to σ = 1.00 on both
   seeds (1.1496 → 1.0933; 1.1058 → 0.9855), while
   the pooled curve climbs to 1.8432 / 1.7933. The
   pooled climb at σ = 1.00 exceeds the per-generation
   mean by 0.75 / 0.81 bits. Claim (lxxiv) is
   calibrated to FAIL.
2. The per-generation isolated-arm synergy is 0.0000
   EXACTLY at every (seed, σ) for both targets — by
   construction, not by measurement: the design-B
   isolated arm collapses each agent to a decided
   concept each generation, so each per-generation
   joint is a point mass and I = 0. The pooled
   isolated synergy at high σ is therefore ENTIRELY
   a mixture effect. Claim (lxxv) is calibrated to
   PASS.
3. Per-generation, the MAX gap at σ = 0.25 is NOT
   synergy-majority (shares 0.383 / 0.332, below the
   0.5 bar), although ΔSyn > ΔRed holds — the gap
   is carried substantially by unique information
   (0.5998 / 0.7878 bits). The pooled (lxx) verdict
   (shares 0.543 / 0.964) does not survive
   per-generation for MAX. Claim (lxxvi) is
   calibrated to FAIL.
4. Per-generation, the XOR gap at σ = 0.25 IS
   synergy-majority (shares 0.566 / 0.541) with
   ΔSyn > ΔRed — the (lxv)-style verdict survives
   per-generation for XOR, but only just on seed 7
   (0.541 vs the 0.5 bar). Held-out failure of
   (lxxvii) is a live possibility. Claim (lxxvii)
   is calibrated to PASS.
5. Per-generation synergy varies a lot across
   generations: sd(Syn_c) at σ ≥ 0.05 is 0.14–0.39
   bits (XOR, worst 0.3886, seed 7 σ = 1.00; single
   generations range 0.2096–1.8250 there). The pooled
   value is not representative of any single
   generation. Reported, not claimed.
6. Mean per-generation ΔI for MAX exceeds the pooled
   ΔI on seed 7 (e.g. +1.6598 vs +1.0707 at
   σ = 0.25) because pooling raises the isolated
   arm's information (pooled I_isol = 0.8813) while
   per-generation I_isol = 0. Reported, not claimed.

## Claims

### (lxxiii) Per-generation PID identity and pooled consistency

For every seed in {42, 7, 1234, 2026}, every sigma on
the grid, every generation (10), both arms, and both
targets (XOR, MAX): Red + Uniq1 + Uniq2 + Syn =
I(X1,X2;Y) within 1e-9 bits, and every atom ≥ −1e-9
bits. AND the mean of the 10 per-generation joints
equals the pooled joint (pid.pair_arm_distributions)
within 1e-12 in max absolute entry, for every
(seed, σ, arm). PASS iff all of this holds. Frozen
tolerances: 1e-9 (identity, floating-point scale),
1e-12 (consistency, exact-arithmetic scale).

### (lxxiv) The XOR synergy-vs-σ climb survives per-generation

Mean per-generation Syn_collab(XOR) at σ = 1.00 ≥ 1.50
bits AND mean per-generation Syn_collab(XOR) at
σ = 1.00 > mean per-generation Syn_collab(XOR) at
σ = 0.50. PASS iff both hold on EVERY seed in
{42, 7, 1234, 2026}. Frozen bar: 1.50 bits (a round
number between the per-generation calibration values
~1.0 and the pooled values ~1.8 — "climbs toward the
2-bit ceiling" means it gets at least three-quarters
of the way there). Calibration: fails on both seeds
(1.0933 / 0.9855; falls from 0.50 to 1.00).

### (lxxv) The isolated arm's high-σ synergy is a pooling artifact (XOR)

Pooled Syn_isol(XOR) − mean per-generation
Syn_isol(XOR) ≥ 0.50 bits at σ = 1.00 AND mean
per-generation Syn_isol(XOR) ≤ 0.10 bits at
σ ∈ {0.50, 1.00}. PASS iff both hold on EVERY seed
in {42, 7, 1234, 2026}. Frozen bar: 0.50 bits (a
round number; the calibration excess is 1.0755 /
1.0000). Calibration: passes on both seeds.

### (lxxvi) The per-generation MAX gap at σ = 0.25 is synergy, not redundancy

Mean per-generation ΔSyn(MAX) > mean per-generation
ΔRed(MAX) AND mean per-generation ΔSyn(MAX) ≥ 0.5 ·
mean per-generation ΔI(MAX) at σ = 0.25. PASS iff
this holds on EVERY seed in {42, 7, 1234, 2026}.
Frozen bar: 0.5 (the same bar as (xli), (lxv), and
(lxx), so the targets are judged identically —
now per-generation). Calibration: fails on both
seeds (shares 0.383 / 0.332, although ΔSyn > ΔRed
holds).

### (lxxvii) The per-generation XOR gap at σ = 0.25 is synergy, not redundancy

Mean per-generation ΔSyn(XOR) > mean per-generation
ΔRed(XOR) AND mean per-generation ΔSyn(XOR) ≥ 0.5 ·
mean per-generation ΔI(XOR) at σ = 0.25. PASS iff
this holds on EVERY seed in {42, 7, 1234, 2026}.
Frozen bar: 0.5 (the same bar as (lxxvi)). The
share is the ratio of the means (mean ΔSyn / mean
ΔI), not the mean of per-generation shares.
Calibration: passes on both seeds (shares 0.566 /
0.541 — tight on seed 7).

## Seeds

- Calibration: 42, 7 (pilot tables and thresholds
  frozen from these only).
- Evaluation: 1234, 2026 (held out; first touched by
  the evaluation run after this file was written).

## What would falsify

- (lxxiii): any atom sum deviating from I(X1,X2;Y)
  by > 1e-9, any atom < −1e-9, or any mean
  per-generation joint deviating from the pooled
  joint by > 1e-12.
- (lxxiv): mean per-generation Syn_c(XOR) at σ = 1.00
  < 1.50 bits, or not above its σ = 0.50 value, on
  any seed. (Calibrated to fail.)
- (lxxv): mixture excess at σ = 1.00 < 0.50 bits, or
  mean per-generation Syn_isol(XOR) > 0.10 bits at
  σ ∈ {0.50, 1.00}, on any seed.
- (lxxvi): mean ΔSyn ≤ mean ΔRed, or mean ΔSyn <
  0.5 · mean ΔI, for MAX at σ = 0.25 on any seed.
  (Calibrated to fail.)
- (lxxvii): mean ΔSyn ≤ mean ΔRed, or mean ΔSyn <
  0.5 · mean ΔI, for XOR at σ = 0.25 on any seed.
