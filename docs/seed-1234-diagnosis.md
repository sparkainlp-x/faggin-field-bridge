# Seed-1234 diagnosis (v0.21.0, Job 2)

Local-only diagnosis, built in the v0.21.0 tree. No push, no PR, no
merge, no Zenodo change, no version bump. All numbers below are
reproduced in code by `seed_1234_diagnosis.py` and pinned by
`tests/test_seed_1234_diagnosis.py` (13 tests); run
`python3 seed_1234_diagnosis.py` to re-derive them.

## The question

Seed 1234 keeps breaking claims, in three different builds:

| Build | Claim(s) | What happened on seed 1234 |
|---|---|---|
| v0.16.0 two-channel empathy | (l), (li), (liii) FAIL; (lii) PASS | Baseline f = 0.3251, nearly double the other seeds (0.1803 / 0.2469 / 0.1772). Mean R never breaks — strictly rising in every sweep on every seed. |
| v0.19.0 Cogitate | (lx) FAIL | mean_D beats mean_R: r = 0.8839 vs 0.8447, margin −0.0393 vs the frozen 0.10 bar. |
| v0.20.0 XOR target | (lxv) FAIL | ΔI = −0.2591 bits (I_isol 1.7610 > I_collab 1.5019); the share-of-gap criterion is meaningless there. |
| v0.21.0 MAX target | (lxix)–(lxxii) PASS | First in the series to CLEAR seed 1234 (ΔI = +0.3266 at σ = 0.25), but with the smallest held-out gaps (0.33 / 0.65 vs calibration 1.89 / 1.07). |

Do the anomalies share one common mechanism — a baseline f near a
threshold, a generation-0 spike, a different operating regime — or
are they independent?

## Verdict: independent anomalies — no common mechanism

Three separate draw-level mechanisms coincide on the same seed.
There is no shared variable that explains all three, and the
generation-0 spike and threshold hypotheses are refuted by
measurement. The 12-seed diagnostic survey (below) finds the three
anomaly statistics essentially uncorrelated across seeds
(Pearson −0.12, −0.24, −0.23), and the survey seeds reach each
extreme separately.

A "seed" here is an RNG-stream label, and the mechanisms are
properties of draws from those streams. "Seed 1234 is extreme"
means its draws sit in the tail of the surveyed seed distribution
on these statistics — a descriptive finding, not a physical cause.
The survey seeds (1, 2, 3, 99, 123, 777, 2024, 31337) are
diagnostics run after the evaluation claims were frozen; they
change no threshold and no verdict in v0.16.0–v0.21.0.

## 1. Two-channel: the baseline pair determinant

Concurrence is `2|ad − bc|` of the pair state, and the uniform
thought has det = 0 exactly, so every nonzero det is noise-made.
The baseline resonance field (N = 8, σ = 0.25) differs across
seeds in the *sign distribution* of that determinant:

| Seed | f | R | D | count | det mean | det median | det < 0 |
|---|---|---|---|---|---|---|---|
| 42 | 0.1803 | 0.8520 | 0.9059 | 17 | −0.0431 | −0.0414 | 18/28 |
| 7 | 0.2469 | 0.6768 | 0.8486 | 16 | +0.1050 | +0.0895 | 5/28 |
| **1234** | **0.3251** | 0.6773 | 0.8545 | 20 | **−0.1556** | **−0.1559** | **26/28** |
| 2026 | 0.1772 | 0.7837 | 0.8953 | 18 | +0.0101 | +0.0109 | 12/28 |

The two channel targets move det in opposite directions. The
concern target |Φ+⟩ = (|00⟩ + |11⟩)/√2 adds to the a and d
amplitudes, pushing det *up*; the distress target |self⟩ = |10⟩
adds to the c amplitude, pushing det *down*. Since f = 2|det|,
a dose that pushes det *through zero* first destroys
concurrence and only then rebuilds it. The per-pair test at
dose 0.25 confirms the sign rule on every file seed:

- **No pair with det ≥ 0 ever falls under concern** (0/10, 0/23, 0/2, 0/16).
- **No pair with det < 0 ever falls under distress** (0/18, 0/5, 0/26, 0/12).
- On 1234, 21 of 26 negative-det pairs fall under concern
  (mean change −0.2084); on seed 7, whose det is mostly
  positive, no negative-det pair falls under concern at all.

That one sign effect produces all three two-channel failures on
1234:

- **(l):** f(c, 0) is U-shaped — 0.3251 → **0.1505** → 0.2788 →
  0.5879 — instead of strictly rising, and the count at c = 0.5
  is 24, not the ceiling 28.
- **(li):** the distress count re-rises — 24 → 17 → 14 → **23**
  (bar: ≤ 15 at d = 1) — because distress *raises* f on this
  seed: f(0, d) = 0.3251 → 0.4841 → 0.5514 → 0.5374 → 0.4073.
  On seed 7 the distress-only sweep dips first (0.2469 → 0.1862),
  the mirror image.
- **(liii):** the swap collapses — f(1, 0) = 0.5879 vs
  f(0, 1) = 0.5374, difference **0.0504** vs the 0.30 bar —
  because distress alone reaches f = 0.5374 on 1234, against
  0.2359 / 0.3500 / 0.3992 on the other seeds. The channels are
  not separated on this seed because the distress target
  *raises* concurrence here instead of only withdrawing.
- **(lii) passes** on 1234 (D fall 0.2051, H fall 5.58 bits,
  R rise 0.1514) — but the count at d = 2 is 28, the ceiling,
  against 10 / 17 / 24 on the other seeds (reported, not gated).

The baseline f = 0.3251 is a *symptom* of the same draw (a
strongly negative det distribution also makes |det|, hence f,
large), not itself the cause: what breaks the claims is the
*sign*, not the level. One agent on 1234 is also strongly peaked
(Born entropy 0.99 bits, max probability 0.77; D range
0.5470–0.9958, the widest of the four seeds), which is part of
the same noise draw.

## 2. Cogitate (lx): the mean_D trajectory shape

On seed 1234, mean_D is *hump-shaped like the gap*:

| Seed | r(gap, mean_R) | r(gap, mean_D) | (lx) margin | σ of max mean_D |
|---|---|---|---|---|
| 42 | 0.9028 | 0.7776 | +0.1252 | 0.00 |
| 7 | 0.8494 | 0.6477 | +0.2017 | 0.00 |
| **1234** | **0.8447** | **0.8839** | **−0.0393** | **0.10** |
| 2026 | 0.8422 | 0.3430 | +0.4992 | 0.00 |

Mean_D on 1234 rises from 0.6274 (σ = 0) to 0.6593 (σ = 0.10)
and then falls to 0.4775 (σ = 1.00), tracking the gap, which
also peaks at σ = 0.05–0.10 (5.4680 at σ = 0.05). On the other
file seeds mean_D is flat (42: 0.6274 → 0.5420) or U-shaped
(7: 0.6274 → 0.3158 → 0.4552; 2026: 0.6274 → 0.1975 → 0.5720),
so it predicts the gap badly there. Mean_R, by contrast, is
unremarkable on 1234 (0.8447, inside the file-seed range
0.8422–0.9028): the failure is mean_D being unusually *good*,
not mean_R being unusually bad, and the margin is narrow
(−0.0393).

This mechanism lives in the collaboration population (N = 4
Bell states, kicks seeded `seed + 1000·g + 10·i`), a different
population fed by independent RNG streams from the resonance
population behind mechanism 1 — no shared variable carries
one cause across both. And (lx) is seed-fragile in general,
not 1234-specific: in the 12-seed survey the 0.10 margin
fails on 6 of 12 seeds (1: −0.0206, 2: +0.0561,
1234: −0.0393, 777: +0.0025, 2024: +0.0375, 31337: +0.0916),
and r(mean_R) itself falls to 0.38–0.50 on seeds 1–3. Seed
31337 has an even higher r(mean_D), 0.8969, but passes
because its r(mean_R) is 0.9885.

Note (lxi) and (lxii) still pass on 1234 (r(−var_D) = 0.7589 ≥
0.70; r(post) = 0.9858, the highest posterior correlation on any
seed), so the Cogitate failure is confined to the (lx) margin.

## 3. XOR (lxv): a discrete switch pattern plus a concentrated pair

The isolated arm's pooled joint is a mixture of 10
per-generation point masses (design B: each generation the
agent Born-collapses and stays decided up to the noise kicks),
so its information takes *discrete* values set by the
concept-count table. The per-generation collapsed concepts at
σ = 0.25:

| Seed | Agent 0 (10 gens) | Agent 1 (10 gens) | Joint cells | I_isol(XOR) |
|---|---|---|---|---|
| 42 | 3 ×8, 2 ×2 | 3 ×10 | 2 | 0.7219 |
| 7 | 3 ×5, 2 ×5 | 3 ×7, 2 ×3 | 3 | 0.7219 |
| **1234** | **3 ×8, 1 ×2** | **3 ×5, 1 ×2, 2 ×3** | **4** | **1.7610** |
| 2026 | 2 ×4, 3 ×6 | 0 ×2, 3 ×3, 1 ×4, 2 ×1 | 4 | 1.3710 |

On 1234 *both* agents switch collapsed concepts mid-run at
staggered times (agent 1: 3 → 1 at generation 5, 1 → 2 at
generation 7; agent 0: 3 → 1 at generation 8), giving a
4-cell joint with counts (3,3)×5, (3,1)×2, (3,2)×1, (1,2)×2.
Its XOR information is 1.7610 bits — the highest isolated-arm
XOR value on any file seed at σ = 0.25, while the calibration
seeds sit at 0.7219 (one agent pinned, the other carrying
exactly the 8/2-split entropy H(0.8, 0.2) = 0.7219 bits).

At the same σ the *collaborating* pair is the most
concentrated on any file seed: mean R_pre = 0.526 (highest;
others 0.376 / 0.397 / 0.339) and marginal entropies 1.281 /
1.213 bits (lowest; others 1.47–1.86), so I_collab = 1.5019 is
the lowest. Neither half alone flips the sign — with the
calibration I_isol the gap would be +0.78, with the calibration
I_collab it would be +0.13 — the flip needs both halves.

The MAX target clears 1234 for the mirror-image reason. The
same concentrated collaborating pair gives I_collab(MAX) =
1.0485 (lowest by far), but the isolated MAX value is only
0.7219: the max of the same count table collapses to two
values (3 ×7, 2 ×3), so ΔI = +0.3266 stays positive — the
smallest MAX gap on any seed, but positive. MAX is positive
on all 12 survey seeds; XOR is negative on 1234 alone.

## Refuted hypotheses

- **Generation-0 spike: refuted.** Gen-0 coupling at σ = 0.25
  is the *lowest* on 1234 (0.3656 vs 0.5281 / 0.4703 /
  0.3903), and its coupling trajectory is the flattest
  (0.28–0.61, max 0.609; seed 42 reaches 0.854, seed 7
  0.865). No generation-0 spike exists anywhere in 1234's
  trajectories (r_mean rises steadily 0.277 → 0.854).
- **A threshold at baseline f: refuted.** No landmark sits
  near f = 0.3251 (quale-count peak f_peak = 0.1803,
  attunement flip f* = 0.7278), and f(σ) on 1234 is the
  highest of the four file seeds at every σ in (0, 0.25]
  but is *overtaken by seed 7* at σ = 0.50 and 1.00
  (0.508 / 0.522 vs 0.472 / 0.507) — smooth, with no crossing.
- **One common mechanism: refuted.** The three mechanisms
  live in different populations fed by independent RNG
  streams (resonance population seeded by `seed`; the
  collaboration population by `seed + i`; the kicks by
  `seed + 1000·g + 10·i`; the collapses by
  `seed + 4242 + 1000·g + 10·i`). At σ = 0 all seeds are
  identical by construction (mean_R 0.6221, mean_D 0.6274,
  max_D 0.8888, var_D 0.03941 on every seed), so every
  cross-seed difference is a noise-draw effect, not a
  structural regime difference.

## 12-seed diagnostic survey

| Seed | Baseline f | XOR ΔI (σ=0.25) | MAX ΔI (σ=0.25) | (lx) margin |
|---|---|---|---|---|
| 42 | 0.1803 | +1.1194 | +1.8927 | +0.1252 |
| 7 | 0.2469 | +1.1668 | +1.0707 | +0.2017 |
| **1234** | **0.3251** | **−0.2591** | **+0.3266** | **−0.0393** |
| 2026 | 0.1772 | +0.5743 | +0.6527 | +0.4992 |
| 1 | 0.2168 | +0.2056 | +0.6212 | −0.0206 |
| 2 | 0.2332 | +1.2596 | +0.9493 | +0.0561 |
| 3 | 0.2732 | +0.7578 | +0.6496 | +0.6135 |
| 99 | 0.2742 | +1.1822 | +1.8460 | +0.3548 |
| 123 | 0.2213 | +0.3688 | +1.5498 | +0.8517 |
| 777 | 0.2594 | +1.9952 | +1.9006 | +0.0025 |
| 2024 | 0.2462 | +1.8728 | +0.7609 | +0.0375 |
| 31337 | 0.2720 | +0.8187 | +0.9783 | +0.0916 |

Seed 1234 is the extreme seed on all three statistics at once
(highest baseline f, lowest XOR ΔI, lowest (lx) margin, lowest
MAX ΔI). But the statistics are uncorrelated across seeds:

- Pearson(baseline f, XOR ΔI) = −0.1236
- Pearson(baseline f, (lx) margin) = −0.2379
- Pearson(XOR ΔI, (lx) margin) = −0.2272

and the survey reaches each extreme separately: seed 777 has
the *largest* XOR gap (+1.9952) with a near-zero (lx) margin
(+0.0025); seed 1 fails the (lx) margin (−0.0206) with an
ordinary baseline f (0.2168); seed 3 has a high baseline f
(0.2732) with a large (lx) margin (+0.6135). Baseline f ranges
0.177–0.325 across the 12 seeds, so 1234 is the top of a broad
distribution, not an isolated outlier — but it is the only
seed where the XOR gap goes negative, and the only file seed
where all three two-channel failures coincide.

## What this means for the next builds

- **Two-channel (v0.16.0):** the gated claims are fragile to
  the *sign* of the baseline determinant, which is a property
  of one noise draw and is not visible in f, R, or D alone
  (seed 42 has mean det −0.0431 and passes; 1234 has −0.1556
  and fails). Any re-gating should condition on the det
  distribution or use a dose grid fine enough to see the
  U-shape — or accept that the concern/distress split does
  not hold for negative-det fields. The distress channel
  raising f is not a bug in the code; it is what the
  |self⟩ addition does to a negative-det pair.
- **Cogitate (lx):** the margin is seed-fragile in general
  (it fails the 0.10 bar on 6 of 12 surveyed seeds),
  because r(gap, mean_D) is driven by the *shape* of the
  mean_D trajectory, which varies from flat to U-shaped to
  hump-shaped across seeds. A per-seed "mean_R beats mean_D"
  bar at 0.10 does not survive fresh seeds; the pooled
  regression (lxiii) and the turn-taking predictor (lxi) are
  the sturdier claims.
- **XOR / MAX:** the isolated arm's information is quantized
  by the 10-generation concept-count table, so ΔI jumps
  between discrete levels as agents switch concepts; the
  σ = 0.25 XOR flip on 1234 is a two-half coincidence
  (concentrated collaborating pair + both-agents-switch
  isolated arm), not a regime change. MAX is the most
  seed-robust target in the series (positive ΔI on all 12
  surveyed seeds), but its 1234 gap (+0.3266) is small
  because the collaborating arm is itself unusually
  concentrated there.

## Honesty

Synthetic, classical emulation throughout. Nothing here
measures consciousness, empathy in a human, or any theory of
consciousness. No scalar Φ is computed anywhere and none is
presented as a consciousness measure; E = hν is used only as
the defined per-mode empathy unit (v0.11.0), never as a Planck
theory of consciousness. The diagnosis changes no threshold
and no verdict in v0.16.0–v0.21.0; the extra survey seeds are
diagnostics only.
