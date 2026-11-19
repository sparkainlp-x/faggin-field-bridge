# Pre-registration — v0.21.0: a target for which collaboration reliably raises total information, claims (lxviii)–(lxxii)

Written 2026-11-18, BEFORE the evaluation run on the held-out
seeds 1234 and 2026 for the new target. Thresholds are round
numbers frozen from a calibration pilot on seeds 42 and 7
only. No threshold in this file may be moved after the
evaluation run, and no claim may be redefined after the fact.

## The spec being tested

The v0.20.0 XOR build (claims (lxiv)–(lxvii)) separated
synergy from redundancy (ΔSyn > ΔRed on all four seeds at
σ = 0.25) but the "gap is synergy" framing broke: on
held-out seed 1234 collaboration did NOT raise total
information about the XOR target at all (ΔI = −0.2591,
I_isol = 1.7610 > I_collab = 1.5019), so a share-of-gap
criterion was meaningless there. This build asks the
open follow-up question from v0.20.0: whether ANY target
exists for which collaboration reliably raises total
information (ΔI > 0 on every seed) while keeping the PID
separable — i.e. the decomposition still separates
synergy from redundancy (ΔSyn > ΔRed, not Syn ≈ Red as
in the v0.14.0 joint-outcome target).

The method is a candidate search on CALIBRATION seeds
only (42 and 7), over target definitions built from
mechanisms already in the tree — deterministic functions
Y = f(X1, X2) of the two agents' 2-bit Born outcomes,
decomposed by the same Williams & Beer I_min PID on the
same exact pooled distributions (pid.pair_arm_distributions,
design B, N = 2, 10 generations), with I(Xi;Y) computed
exactly from the joint (the v0.20.0 pitfall: never the
H(Y) − H(Xj) product shortcut, which produced negative
unique atoms on the pooled mixture). A target on a third
channel was considered and set aside: the pair apparatus
has no third outcome channel — the field state is a
superposed state vector, not a Born outcome — and a
three-source PID would be new machinery, not a mechanism
already in the tree. Φ (scalar) is NOT imported as a
consciousness measure (explicit do-not from the
deep-think report, Cogitate 2025), and E = hν is not
presented as a Planck theory of consciousness.

## The candidate screen (calibration seeds 42 and 7 only)

Fourteen targets at σ = 0.25. I_c / I_i are the total
informations I(X1,X2;Y) = H(Y) in each arm; ΔSyn, ΔRed
are the arm differences of the I_min atoms; Red_c/I_c
is the collaborating arm's redundancy share.

| target | ΔI 42 | ΔI 7 | min ΔI | ΔSyn 42 | ΔSyn 7 | ΔRed 42 | ΔRed 7 | Red_c/I_c 42 | Red_c/I_c 7 |
|---|---|---|---|---|---|---|---|---|---|
| xor (v0.20.0, reference) | +1.1194 | +1.1668 | +1.1194 | +1.4472 | +1.0010 | +0.3143 | +0.1397 | 0.1707 | 0.1363 |
| and | −0.0363 | −0.3480 | −0.3480 | +0.3742 | +0.3704 | +0.2694 | −0.1505 | 0.3929 | 0.3762 |
| or | +1.8634 | +1.0433 | +1.0433 | +1.0480 | +1.0827 | +0.6709 | +0.2504 | 0.3600 | 0.3358 |
| sum_mod4 | +1.1256 | +0.4452 | +0.4452 | +1.4472 | +1.2221 | +0.3205 | −0.3608 | 0.1735 | 0.1551 |
| diff_mod4 | +1.1156 | +1.1660 | +1.1156 | +1.4242 | +1.0010 | +0.2874 | +0.1390 | 0.1564 | 0.1360 |
| sum_int | +1.5594 | +0.7834 | +0.7834 | +1.4189 | +1.1973 | +0.7259 | −0.0473 | 0.3182 | 0.2701 |
| min | +0.0711 | −0.2003 | −0.2003 | +0.4360 | +0.4365 | +0.2965 | −0.1086 | 0.3738 | 0.3592 |
| max | +1.8927 | +1.0707 | +1.0707 | +1.0279 | +1.0316 | +0.6758 | +0.2589 | 0.3571 | 0.3354 |
| eq | +0.2745 | +0.2616 | +0.2616 | +0.7850 | +0.3030 | +0.1909 | +0.0082 | 0.1915 | 0.1281 |
| parity | +0.2338 | +0.2583 | +0.2338 | +0.8448 | +0.3606 | +0.1044 | −0.0284 | 0.1093 | 0.0911 |
| lowbit_xor | +0.2338 | +0.2583 | +0.2338 | +0.8448 | +0.3606 | +0.1044 | −0.0284 | 0.1093 | 0.0911 |
| lowbits_pair | +0.9926 | +0.2546 | +0.2546 | +0.5885 | +0.3142 | +0.6069 | −0.0786 | 0.3540 | 0.3342 |
| x1 | +0.7478 | +0.5096 | +0.5096 | −0.0000 | −0.0000 | +0.0204 | −0.3727 | 0.0139 | 0.0153 |
| joint (v0.14.0, reference) | +2.2729 | +1.6554 | +1.6554 | +0.9248 | +0.7103 | +0.9453 | +0.3376 | 0.3156 | 0.3177 |

Full-grid ΔI (calibration seeds), per target — the
grid-wide picture behind the σ = 0.25 screen:

| target | s42: 0.00 / 0.01 / 0.05 / 0.10 / 0.25 / 0.50 / 1.00 | s7: 0.00 / 0.01 / 0.05 / 0.10 / 0.25 / 0.50 / 1.00 |
|---|---|---|
| xor | +1.000 / +1.033 / +1.327 / +1.550 / +1.119 / +0.460 / +0.472 | +1.000 / +1.015 / +1.094 / +0.363 / +1.167 / +0.505 / +0.184 |
| and | +0.811 / +0.793 / +0.685 / +0.619 / −0.036 / −0.839 / −0.337 | +0.811 / +0.658 / +0.396 / −0.657 / −0.348 / −0.155 / −0.313 |
| or | +0.811 / +0.863 / +1.260 / +1.554 / +1.863 / +1.012 / +0.656 | +0.811 / +0.954 / +1.136 / +1.358 / +1.043 / +0.547 / +0.316 |
| sum_mod4 | +1.500 / +1.516 / +1.621 / +1.683 / +1.126 / +0.484 / +0.413 | +1.500 / +1.482 / +1.333 / +0.450 / +0.445 / +0.969 / +0.008 |
| diff_mod4 | +1.500 / +1.514 / +1.555 / +1.581 / +1.116 / +0.258 / +0.056 | +1.500 / +1.478 / +1.290 / +0.426 / +1.166 / +0.143 / +0.284 |
| sum_int | +1.500 / +1.533 / +1.795 / +1.979 / +1.559 / +0.735 / +0.728 | +1.500 / +1.491 / +1.421 / +0.604 / +0.783 / +0.656 / +0.048 |
| min | +0.811 / +0.793 / +0.689 / +0.643 / +0.071 / −0.514 / +0.043 | +0.811 / +0.658 / +0.398 / −0.639 / −0.200 / −0.042 / −0.167 |
| max | +0.811 / +0.863 / +1.264 / +1.568 / +1.893 / +0.826 / +0.434 | +0.811 / +0.954 / +1.137 / +1.364 / +1.071 / +0.661 / +0.234 |
| eq | +1.000 / +1.000 / +0.991 / +0.978 / +0.275 / −0.071 / −0.211 | +1.000 / +0.998 / +0.904 / −0.054 / +0.262 / −0.015 / −0.107 |
| parity | +1.000 / +1.000 / +0.981 / +0.931 / +0.234 / +0.276 / +0.025 | +1.000 / +0.998 / +0.886 / −0.114 / +0.258 / −0.000 / +0.028 |
| lowbit_xor | +1.000 / +1.000 / +0.981 / +0.931 / +0.234 / +0.276 / +0.025 | +1.000 / +0.998 / +0.886 / −0.114 / +0.258 / −0.000 / +0.028 |
| lowbits_pair | +2.000 / +1.997 / +1.859 / +1.686 / +0.993 / +0.522 / +0.183 | +2.000 / +1.945 / +1.498 / +0.380 / +0.255 / +0.142 / +0.258 |
| x1 | +1.000 / +1.022 / +1.149 / +1.223 / +0.748 / +0.076 / +0.034 | +1.000 / +0.988 / +0.914 / +0.006 / +0.510 / +0.270 / +0.051 |
| joint | +2.000 / +2.031 / +2.234 / +2.424 / +2.273 / +0.849 / +0.910 | +2.000 / +1.964 / +1.733 / +0.955 / +1.655 / +1.581 / +0.886 |

## The selection rule, and the two exclusions — disclosed before the run

The naive rule (max min-seed ΔI at σ = 0.25 among
eligible candidates, eligible = ΔI > 0, ΔSyn > ΔRed
with |ΔSyn − ΔRed| ≥ 0.10, Red_c/I_c ≤ 0.50 on both
calibration seeds) would pick the incumbent XOR
(min ΔI +1.1194) or, among new targets, diff_mod4
(min ΔI +1.1156). Both are set aside, for reasons
stated here before the evaluation run:

1. xor and joint are REFERENCES, not candidates: both
   were already measured on all four seeds (v0.20.0,
   v0.14.0). Re-selecting XOR would re-run v0.20.0
   under a new version number; the joint target is
   already known to fail separability (Syn ≈ Red).
2. sum_mod4 and diff_mod4 are near-duplicates of the
   incumbent BY CONSTRUCTION, not by hindsight: they
   are Latin-square / group-difference targets
   (fixing one source permutes Y), so under uniform
   independent sources each source alone carries zero
   about Y — the same pure-synergy construction as
   XOR — and their H(Y) is driven by the same
   difference distribution that the pooled-mixture
   correlation uniformizes, which is the diagnosed
   mechanism of the XOR failure on held-out seed
   1234. On calibration they track XOR to within
   0.004 bits (diff_mod4 ΔI 1.1156 / 1.1660 vs XOR
   1.1194 / 1.1668). Selecting one would test the
   known-failed mechanism again, not a new target.

The selection actually applied: among the remaining
new targets, eligible by the gates above, pick max
min-seed ΔI at σ = 0.25. That picks **MAX,
Y = max(X1, X2)** — the peak / strongest-concept
outcome — with min ΔI +1.0707 (seeds 42 / 7:
+1.8927 / +1.0707). OR, the other agreement-family
target, is the sensitivity check: it tracks MAX
within 0.03 bits at σ = 0.25 (ΔI +1.8634 / +1.0433,
shares 0.5624 / 1.0378 vs MAX 0.5431 / 0.9635), so
the choice between the two agreement targets does
not drive the verdict. AND and MIN fail the gates
(ΔI ≤ 0 on at least one calibration seed); x1 fails
separability (ΔSyn = 0 exactly — a single-source
target cannot be synergistic); eq / parity /
lowbit_xor pass the gates but with small min ΔI
(≤ +0.2616); lowbits_pair fails the separation gate
on seed 42 (ΔSyn 0.5885 < ΔRed 0.6069).

## The chosen target: MAX

Y = max(X1, X2) ∈ {0, 1, 2, 3} — the larger of the
two agents' concepts. Unlike XOR it is an
agreement-family target: when collaboration makes
the agents similar, Y follows the shared concept,
and H(Y) is driven by the spread of the shared
marginal, not by a difference distribution. The
decomposition is the same I_min PID, the same arms,
the same exact pooled distributions — only the
target changes, exactly as in v0.20.0.

Per-(seed, σ) MAX-target PID, collaborating arm
(I_c, Syn_c, Red_c, Uniq_c) and isolated arm
(I_i, Syn_i, Red_i, Uniq_i), in bits — calibration
seeds only:

| seed | σ | I_c | Syn_c | Red_c | Uniq_c | I_i | Syn_i | Red_i | Uniq_i |
|---|---|---|---|---|---|---|---|---|---|
| 42 | 0.00 | 0.8113 | 0.5000 | 0.3113 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.01 | 0.8634 | 0.5245 | 0.3267 | 0.0122 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.05 | 1.2636 | 0.6815 | 0.4616 | 0.1206 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.10 | 1.5684 | 0.7965 | 0.5739 | 0.1981 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.25 | 1.8927 | 1.0279 | 0.6758 | 0.1890 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 42 | 0.50 | 1.9829 | 1.1766 | 0.7005 | 0.1058 | 1.1568 | 0.2000 | 0.4713 | 0.4855 |
| 42 | 1.00 | 1.7947 | 0.9449 | 0.5266 | 0.3232 | 1.3610 | 0.4755 | 0.7610 | 0.1245 |
| 7 | 0.00 | 0.8113 | 0.5000 | 0.3113 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.01 | 0.9544 | 0.5680 | 0.3546 | 0.0317 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.05 | 1.1370 | 0.5637 | 0.3946 | 0.1786 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.10 | 1.3642 | 0.7192 | 0.4922 | 0.1529 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 7 | 0.25 | 1.9520 | 1.0316 | 0.6547 | 0.2657 | 0.8813 | 0.0000 | 0.3958 | 0.4855 |
| 7 | 0.50 | 1.8182 | 0.9803 | 0.6293 | 0.2087 | 1.1568 | 0.1170 | 0.7228 | 0.3170 |
| 7 | 1.00 | 1.7191 | 0.9357 | 0.6566 | 0.1268 | 1.4855 | 0.4585 | 0.8685 | 0.1585 |

Four disclosures, before the run:
1. The isolated arm DEGENERATES at low σ: I_isol = 0
   exactly at σ ≤ 0.25 on seed 42 and σ ≤ 0.10 on
   seed 7 — the design-B lock-in (a collapsed agent
   stays near its collapsed concept under small kicks,
   so both agents sit on one concept and max is a
   point mass; the seed-42 σ = 0.25 isolated joint is
   X1 ∈ {2, 3}, X2 = 3 always). The large ΔI at low σ
   is therefore driven as much by the isolated arm
   collapsing to a point as by collaboration raising
   information. The σ = 0.25 claim (lxix) is the one
   that matters, and on seed 7 there the isolated arm
   is NOT degenerate (I_isol = 0.8813).
2. The synergy share at σ = 0.25 is tight on seed 42:
   0.5431 against the 0.5 bar (seed 7: 0.9635). Claim
   (lxx) is calibrated to pass, but only just on one
   seed — held-out failure is a live possibility.
3. The redundancy share Red_c / I_c peaks at 0.3837
   (seed 42, σ = 0.00) on calibration; the (lxxi) bar
   0.50 sits 0.116 above it. Redundancy is a much
   larger share for MAX than for XOR (worst 0.2357)
   — MAX is not a pure-synergy target: even with
   independent uniform sources it carries Red =
   0.6712 of I = 1.7490 (canonical case below).
4. The grid-wide ΔI is positive everywhere on
   calibration, but its minimum is 0.2337 (seed 7,
   σ = 1.00) and it falls steeply past σ = 0.25
   (seed 42: 1.8927 → 0.8261 → 0.4338). Claim
   (lxxii) is calibrated to pass, with the σ = 1.00
   corner the exposed one.

Canonical cases for MAX (exact values):
- X1, X2 independent uniform: I = 1.7490, Syn =
  1.0778, Red = 0.6712, Uniq1 = Uniq2 = 0,
  I(X1;Y) = I(X2;Y) = 0.6712. (MAX is NOT pure
  synergy: a single source alone carries 0.6712 bits
  about the max.)
- X1 = X2 uniform: I = 2.0, Syn = 0, Red = 2.0,
  Uniq = 0 (all redundant — each source alone
  determines Y).
- X1 deterministic, X2 uniform: I = 2.0, Syn = 0,
  Red = 0, Uniq2 = 2.0 (all unique to X2); and
  symmetrically X2 deterministic → Uniq1 = 2.0.

Sampled cross-check (calibration): at σ = 0.25 the
exact H(Y) agrees with the sampled run_collaboration
(N = 2, design B) H(Y) — computed from the sampled
joint counts via Y = max(X1, X2) — within 0.0087
bits (seed 42 collaborating; 0.0000 isolated;
seed 7: 0.0016 / 0.0000).

## Claims

### (lxviii) MAX-target PID identity, canonical checks, sampled cross-check

For every seed in {42, 7, 1234, 2026}, every sigma on
the grid, and both arms: Red + Uniq1 + Uniq2 + Syn =
I(X1,X2;Y) within 1e-9 bits, and every atom ≥ −1e-9
bits. AND the canonical cases hold: (a) X1, X2
independent uniform → I = 1.7490, Syn = 1.0778,
Red = 0.6712, Uniq1 = Uniq2 = 0 (tol 1e-3); (b)
X1 = X2 uniform → I = 2.0, Syn = 0, Red = 2.0,
Uniq = 0; (c) X1 deterministic, X2 uniform →
Uniq2 = 2.0, Syn = 0, Red = 0; (d) X2 deterministic,
X1 uniform → Uniq1 = 2.0, Syn = 0, Red = 0.
AND at σ = 0.25 the exact H(Y) agrees with the
sampled run_collaboration (N = 2, design B) H(Y)
within 0.25 bits on every seed, both arms. PASS iff
all of this holds. Frozen tolerances: 1e-9
(identity, floating-point scale), 1e-3 (canonical
values), 0.25 bits (cross-check, the round number
used in (xl) and (lxiv)).

### (lxix) Collaboration raises total information about the MAX target at σ = 0.25

ΔI = I_collab − I_isol > 0 at σ = 0.25. PASS iff
this holds on EVERY seed in {42, 7, 1234, 2026}.
This is the core question of the build, stated as a
sign claim with no magnitude bar: the XOR failure
was a negative gap, so the test is whether the gap
is positive at all. Calibration: +1.8927 / +1.0707.

### (lxx) The information gap about the MAX target IS synergy, not redundancy, at σ = 0.25

ΔSyn > ΔRed AND ΔSyn ≥ 0.5 · ΔI at σ = 0.25. PASS
iff this holds on EVERY seed in {42, 7, 1234,
2026}. Frozen bar: 0.5 (the same bar as (xli) and
(lxv), so the three targets are judged identically).
Calibration: passes on both seeds (ΔSyn/ΔRed =
1.0279 / 0.6758 and 1.0316 / 0.2589; shares 0.5431
/ 0.9635 — tight on seed 42).

### (lxxi) Redundancy stays below half the target information across the grid

Red_collab ≤ 0.50 · I_collab(X1,X2;Y) on every
(seed, σ) with I_collab > 0. PASS iff this holds on
EVERY seed in {42, 7, 1234, 2026}. Frozen bar: 0.50
(a round number above the calibration worst share
0.3837, seed 42 at σ = 0.00; the bar is looser than
the 0.25 used for XOR because MAX is not a
pure-synergy target — its independent-uniform
canonical case already carries Red/I = 0.3837).
Calibration: passes on both seeds (worst shares
0.3837 / 0.3837).

### (lxxii) Collaboration raises total information about the MAX target across the grid

ΔI > 0 on every (seed, σ). PASS iff this holds on
EVERY seed in {42, 7, 1234, 2026} and every sigma on
the grid. Calibration: passes on both seeds
(minimum ΔI +0.2337, seed 7 at σ = 1.00).

## Seeds

- Calibration: 42, 7 (screen, selection, and
  thresholds frozen from these only).
- Evaluation: 1234, 2026 (held out; first touched by
  the evaluation run after this file was written).

## What would falsify

- (lxviii): any atom sum deviating from I(X1,X2;Y)
  by > 1e-9, any atom < −1e-9, any canonical case
  failing, or any exact-vs-sampled H(Y) mismatch
  > 0.25 bits at σ = 0.25.
- (lxix): ΔI ≤ 0 at σ = 0.25 on any seed.
- (lxx): ΔSyn ≤ ΔRed, or ΔSyn < 0.5 · ΔI, at
  σ = 0.25 on any seed.
- (lxxi): Red_collab > 0.50 · I_collab on any
  (seed, σ) with I_collab > 0.
- (lxxii): ΔI ≤ 0 on any (seed, σ).
