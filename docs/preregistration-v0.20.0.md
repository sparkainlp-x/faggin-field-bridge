# Pre-registration — v0.20.0: Genuinely synergistic target (PID follow-up), claims (lxiv)–(lxvii)

Written 2026-11-18, BEFORE the evaluation run on the held-out
seeds 1234 and 2026. Thresholds are round numbers frozen from
a calibration pilot on seeds 42 and 7 only. No threshold in
this file may be moved after the evaluation run.

## The spec being tested

The v0.14.0 PID build (claims (xl)–(xliii)) found the
Williams & Beer I_min decomposition arithmetically exact
but UNABLE to adjudicate "synergy, not redundancy" in
its wiring: with target Y = the joint outcome (X1, X2),
Syn = Red − I(X1;X2) and I(X1;X2) is 0.00–0.06 bits on
every σ/seed, so Syn ≈ Red everywhere and claims
(xli)–(xliii) FAIL. The recorded discovery: a genuinely
synergistic target (a field-level outcome coupled to both
agents) would be needed to separate them. This build
tests exactly that: replace the target with the canonical
synergistic target and ask whether the PID decomposition
can now separate synergy from redundancy.

The target is the bitwise XOR of the two agents' 2-bit
Born outcomes: Y = X1 ⊕ X2 ∈ {0, 1, 2, 3}. This is the
textbook synergistic target (Williams & Beer 2010; the
XOR example in the PID literature): with X1, X2
independent and uniform, each source alone carries ZERO
information about Y (I(X1;Y) = I(X2;Y) = 0) while the
pair jointly determines Y completely
(I(X1,X2;Y) = H(Y) = 2 bits) — pure synergy, zero
redundancy, zero unique information. Any redundancy or
unique information that appears in the measured
decomposition therefore comes from the agents'
non-uniform marginals and from the pooled mixture, not
from the target's construction. The decomposition is
again Williams & Beer I_min, the same redundancy
measure as v0.14.0, so the comparison is apples to
apples: same measure, same arms, same exact pooled
distributions — only the target changes. Φ (scalar) is
NOT imported as a consciousness measure (explicit
do-not from the deep-think report, Cogitate 2025), and
E = hν is not presented as a Planck theory of
consciousness.

## The construction (fixed before the pilot)

- Sources X1, X2 are the two agents' Born outcomes (4
  concepts each); target Y = X1 ⊕ X2. The joint
  distribution is the EXACT pooled distribution from
  pid.pair_arm_distributions (design B, N = 2, 10
  generations): the same evolution as v0.14.0, reused,
  not reimplemented.
- p(y) = Σ_{x1⊕x2=y} p(x1, x2). I(X1,X2;Y) = H(Y),
  because Y is a deterministic function of (X1, X2).
- Redundancy is Williams & Beer I_min: Red =
  Σ_y p(y) · min(I(X1; Y=y), I(X2; Y=y)), where the
  specific information I(Xi; Y=y) =
  D_KL(p(xi|y) || p(xi)), computed exactly from the
  joint. Uniq_i = I(Xi;Y) − Red, Syn =
  I(X1,X2;Y) − Red − Uniq1 − Uniq2.
- I(X1;Y) and I(X2;Y) are computed EXACTLY from the
  joint (p(x1,y) = p(x1, x1⊕y)). They are NOT computed
  as H(Y) − H(X2): that shortcut assumes the pooled
  joint is a product distribution, and it is not — it
  is a MIXTURE of per-generation products, so X1 and
  X2 are correlated through the generation index and
  H(Y|X1) ≠ H(X2). The first pilot pass used the
  shortcut and produced negative unique atoms (worst
  −0.6955 bits, seed 7); the exact computation
  restores all atoms to ≥ −0.0000 bits. This
  correction was made BEFORE any threshold was frozen
  and is disclosed here, not hidden.
- The "gap" for the new target is ΔI =
  I_collab(X1,X2;Y) − I_isol(X1,X2;Y), with
  ΔSyn, ΔRed, ΔUniq defined the same way; the four
  arm differences sum to ΔI exactly.
- Sigma grid: the bridge grid [0, 0.01, 0.05, 0.1,
  0.25, 0.5, 1.0] (te.SIGMA_GRID). Generations = 10
  (empathy_field default). Design B throughout.
- Mean resonance R: the mean pairwise overlap squared
  R_post of the collaborating arm's states AFTER the
  field mix, averaged over generations (from
  pid.pair_arm_distributions, reused).

## Calibration pilot (seeds 42 and 7) — disclosed before the run

Per-(seed, σ) XOR-target PID, collaborating arm
(I_c, Syn_c, Red_c, Uniq_c) and isolated arm
(I_i, Syn_i, Red_i, Uniq_i), in bits:

| seed | σ | I_c | Syn_c | Red_c | Uniq_c | I_i | Syn_i | Red_i | Uniq_i |
|---|---|---|---|---|---|---|---|---|---|
| 42 | 0.00 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.01 | 1.0328 | 1.0085 | 0.0104 | 0.0138 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.05 | 1.3266 | 1.0809 | 0.1798 | 0.0659 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.10 | 1.5496 | 1.1467 | 0.2981 | 0.1047 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.25 | 1.8414 | 1.4472 | 0.3143 | 0.0799 | 0.7219 | 0.0000 | 0.0000 | 0.7219 |
| 42 | 0.50 | 1.9816 | 1.7178 | 0.2137 | 0.0501 | 1.5219 | 0.9610 | 0.2464 | 0.3145 |
| 42 | 1.00 | 1.9940 | 1.8432 | 0.0428 | 0.1080 | 1.5219 | 1.0755 | 0.1710 | 0.2755 |
| 7 | 0.00 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.01 | 1.0153 | 0.9746 | 0.0263 | 0.0144 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.05 | 1.0943 | 0.7889 | 0.1627 | 0.1428 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.10 | 1.3337 | 0.8985 | 0.3144 | 0.1208 | 0.9710 | 0.0000 | 0.0000 | 0.9710 |
| 7 | 0.25 | 1.8887 | 1.4865 | 0.2575 | 0.1448 | 0.7219 | 0.4855 | 0.1177 | 0.1187 |
| 7 | 0.50 | 1.9909 | 1.7892 | 0.0706 | 0.1311 | 1.4855 | 0.6000 | 0.6100 | 0.2755 |
| 7 | 1.00 | 1.9446 | 1.7933 | 0.0935 | 0.0578 | 1.7610 | 1.0000 | 0.4365 | 0.3245 |

Three disclosures, before the run:
1. The separation at σ = 0.25 is real and large:
   ΔSyn = +1.4472 / +1.0010 against ΔRed = +0.3143 /
   +0.1397 (ratios 4.60 / 7.17), and ΔSyn is 129.3% /
   85.8% of ΔI (+1.1194 / +1.1668). The share exceeds
   100% on seed 42 because ΔUniq is negative there
   (−0.6420: the isolated arm carries 0.7219 bits of
   UNIQUE information about Y at σ = 0.25 that
   collaboration destroys — in the collapsed arm one
   agent alone predicts Y, since the other is nearly
   fixed that generation). The PID DOES separate
   synergy from redundancy for this target, where it
   could not for the joint-outcome target. Claim (lxv)
   is calibrated to pass.
2. But synergy does NOT track resonance and does NOT
   fall at σ = 0.50: Pearson(Syn_collab, R_post) =
   0.3731 / 0.3424 (bar 0.5), and Syn_collab RISES
   from σ = 0.25 to σ = 0.50 (1.4472 → 1.7178;
   1.4865 → 1.7892), climbing toward the 2-bit
   ceiling as the marginals uniformize with noise.
   Synergy here tracks noise-driven uniformity, not
   resonance. Claim (lxvi) is calibrated to FAIL.
3. The redundancy share Red_c / I_c peaks at 0.192
   (seed 42, σ = 0.10) and 0.236 (seed 7, σ = 0.10)
   — the (lxvii) bar 0.25 sits only 0.014 above the
   calibration worst. Held-out failure of (lxvii) is
   a live possibility, not a surprise. Also, the
   isolated arm is NOT synergy-free at high σ: Syn_i
   reaches 0.9610 / 0.6000 at σ = 0.50 and 1.0755 /
   1.0000 at σ = 1.00 — the pooled mixture over
   generations correlates the collapsed agents
   through the generation index, and that
   mixture-correlation is itself synergistic about
   the XOR. The XOR target separates the arms at
   σ = 0.25, not at high σ (ΔSyn at σ = 0.50 is
   +0.7568 / +1.1892 but ΔI is only +0.4596 /
   +0.5055, and at σ = 1.00 ΔSyn = +0.7678 /
   +0.7933 against ΔI = +0.4721 / +0.1837).

## Claims

### (lxiv) XOR-target PID identity, canonical checks, sampled cross-check

For every seed in {42, 7, 1234, 2026}, every sigma on
the grid, and both arms: Red + Uniq1 + Uniq2 + Syn =
I(X1,X2;Y) within 1e-9 bits, and every atom ≥ −1e-9
bits. AND the canonical cases hold exactly: (a)
X1, X2 independent uniform → Syn = 2.0, Red = 0,
Uniq1 = Uniq2 = 0; (b) X1 = X2 uniform → all atoms 0
(I = 0); (c) X1 deterministic, X2 uniform → Uniq2 =
2.0, Syn = 0, Red = 0. AND at σ = 0.25 the exact H(Y)
agrees with the sampled run_collaboration (N = 2,
design B) H(Y) — computed from the sampled joint
counts via Y = X1 ⊕ X2 — within 0.25 bits on every
seed, both arms. PASS iff all of this holds. Frozen
tolerances: 1e-9 (identity, floating-point scale) and
0.25 bits (cross-check, the round number used in
(xl)).

### (lxv) The information gap about the synergistic target IS synergy, not redundancy, at σ = 0.25

ΔSyn > ΔRed AND ΔSyn ≥ 0.5 · ΔI at σ = 0.25. PASS iff
this holds on EVERY seed in {42, 7, 1234, 2026}.
Frozen bar: 0.5 (synergy is the majority of the
gap — the same bar as (xli), so the two targets are
judged identically). Calibration: passes on both
seeds (ΔSyn/ΔRed = 4.60 / 7.17; shares 1.293 /
0.858). Note the share may exceed 1 when ΔUniq is
negative; the bar is on the share as defined, and
ΔSyn > ΔRed is the binding comparison.

### (lxvi) Synergy rises with R and falls at σ = 0.50

Pearson(Syn_collab, mean R_post) across the sigma grid
≥ 0.5 AND Syn_collab(σ = 0.50) < Syn_collab(σ = 0.25).
PASS iff both hold on EVERY seed in {42, 7, 1234,
2026}. Frozen bar: 0.5 (the round correlation bar
used elsewhere in this repo; the same bar as (xlii),
so the two targets are judged identically).
Calibration: fails on both seeds (Pearsons 0.3731 /
0.3424; synergy rises at 0.50).

### (lxvii) Redundancy stays a small share of the target information across the grid

Red_collab ≤ 0.25 · I_collab(X1,X2;Y) on every
(seed, σ) with I_collab > 0. PASS iff this holds on
EVERY seed in {42, 7, 1234, 2026}. Frozen bar: 0.25
(a round number just above the calibration worst
share 0.236, seed 7 at σ = 0.10). Calibration:
passes on both seeds (worst shares 0.192 / 0.236),
tightest on seed 7.

## Seeds

- Calibration: 42, 7 (thresholds frozen from these only).
- Evaluation: 1234, 2026 (held out; first touched by
  the evaluation run after this file was written).

## What would falsify

- (lxiv): any atom sum deviating from I(X1,X2;Y) by
  > 1e-9, any atom < −1e-9, any canonical case
  failing, or any exact-vs-sampled H(Y) mismatch
  > 0.25 bits at σ = 0.25.
- (lxv): ΔSyn ≤ ΔRed, or ΔSyn < 0.5 · ΔI, at σ = 0.25
  on any seed.
- (lxvi): Pearson < 0.5, or Syn_collab not falling at
  σ = 0.50, on any seed.
- (lxvii): Red_collab > 0.25 · I_collab on any
  (seed, σ) with I_collab > 0.
