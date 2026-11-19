# Changelog — Faggin Field Bridge

## 0.21.0 (2026-11-18)

A target for which collaboration reliably raises total
information (follow-up to v0.20.0): a calibration-only
candidate search over fourteen deterministic targets
Y = f(X1, X2), same Williams & Beer I_min PID, same
arms, same exact pooled distributions — only the target
changes — preregistered with frozen bars from calibration
seeds 42/7 before the held-out evaluation on seeds
1234/2026. Five of five claims pass, and this time the
passes are the result: (lxix) ΔI > 0 at σ = 0.25 on
every seed (+1.8927 / +1.0707 / +0.3266 / +0.6527,
seeds 42 / 7 / 1234 / 2026) — the first target in the
series for which collaboration raises total information
on held-out seed 1234, where the XOR gap was −0.2591;
(lxxii) ΔI > 0 on every (seed, σ), minimum +0.2337
(seed 7, σ = 1.00); (lxx) the gap is synergy-dominant
on every seed (ΔSyn +1.0279 / +1.0316 / +0.4005 /
+0.6598 vs ΔRed +0.6758 / +0.2589 / −0.1976 / +0.1318;
shares 0.543 / 0.964 / 1.226 / 1.011, bar 0.5 — above 1
on the held-out seeds because ΔRed is negative on 1234
and ΔUniq negative on 2026); (lxxi) redundancy stays
below half the target information everywhere (worst
share 0.3837 on every seed, at σ = 0.00, bar 0.50);
(lxviii) the identity (worst error 2.22e-16, all atoms
≥ −0.0000), the canonical MAX cases (independent uniform
→ I = 1.7490, Syn = 1.0778, Red = 0.6712; X1 = X2 →
all redundant, Red = 2.0; one source deterministic →
all unique to the other) and the sampled cross-check
(worst H(Y) diff 0.0318 bits, tol 0.25). The search
selected MAX, Y = max(X1, X2), by max min-seed ΔI among
eligible new targets after excluding the incumbents (xor,
joint — already measured on all four seeds) and the
Latin-square difference targets (sum_mod4, diff_mod4) as
near-duplicates of the failed XOR mechanism by
construction (they track XOR to within 0.004 bits on
calibration); OR, the other agreement-family target,
tracks MAX within 0.03 bits at σ = 0.25 and is the
reported sensitivity check. AND and MIN fail the gates
(ΔI ≤ 0 on at least one calibration seed); x1 fails
separability (ΔSyn = 0 exactly). Disclosed: the isolated
arm degenerates at low σ (I_isol = 0 exactly at σ ≤ 0.25
on seed 42, σ ≤ 0.10 on seeds 7 and 1234, σ ≤ 0.05 on
seed 2026 — the design-B lock-in), so the large ΔI at
low σ is driven as much by the isolated arm collapsing
to a point as by collaboration raising information; MAX
is not a pure-synergy target (independent uniform sources
already carry Red = 0.6712 of I = 1.7490) — what it buys
is a positive total-information gap, not a cleaner
synergy; and the held-out gaps are much smaller than the
calibration ones (0.3266 / 0.6527 vs 1.8927 / 1.0707).
No claim (i)–(lxvii) changes verdict. Tests: 446 ->
462, all passing.

- **Mechanism** (`total_information_target.py`, new module;
  `pid.py`, reused, not reimplemented):
  target_pid_from_joint (general Williams & Beer I_min
  PID of I(X1,X2; Y = f(X1, X2)) with I(Xi;Y) computed
  exactly from the joint; cross-checked to reproduce
  synergistic_target.xor_pid_from_joint exactly),
  TARGET_FUNCTIONS (the fourteen screened targets),
  screen_candidates (the calibration-only screen with
  the preregistered gates and exclusions, selecting
  "max"), max_pid_from_joint / sampled_h_y_max /
  max_arm_distributions / max_gap_vs_noise (exact pooled
  MAX-target PID per (seed, σ)), and the five claim
  verdicts (lxviii)-(lxxii). Pre-registration in
  docs/preregistration-v0.21.0.md, written before the
  evaluation run.

## 0.20.0 (2026-11-18)

Genuinely synergistic target (PID follow-up to v0.14.0):
the XOR target Y = X1 (+) X2 replaces the joint-outcome
target in the Williams & Beer I_min PID, preregistered
with frozen bars from calibration seeds 42/7 before the
held-out evaluation on seeds 1234/2026. Two of four
claims pass, and the failures are the result: (lxv) the
"gap is synergy" claim fails on held-out seed 1234,
where the information gap itself is negative (−0.2591
bits — the isolated arm carries MORE total information
about the XOR target than the collaborating arm,
I_isol = 1.7610 vs I_collab = 1.5019), so the synergy
share is −3.956 even though delta-synergy stays
positive (+1.0248) and exceeds delta-redundancy
(−0.3953) on every seed; (lxvi) synergy does NOT rise
with R and does NOT fall at σ = 0.50 — Pearsons
0.3731 / 0.3424 / −0.3397 / 0.9036 (bar 0.5), synergy
rising 0.25 → 0.50 on every seed (1.4472 → 1.7178 /
1.4865 → 1.7892 / 1.1833 → 1.5323 / 1.5901 → 1.7297),
climbing toward the 2-bit ceiling as the marginals
uniformize with noise. What survives: (lxiv) the
identity (worst error 2.22e-16, all atoms ≥ −0.0000),
the canonical XOR cases (independent uniform → pure
synergy 2.0 bits, zero redundancy; X1 = X2 → nothing;
X1 deterministic → all unique to X2) and the sampled
cross-check (worst H(Y) diff 0.0193 bits, tol 0.25);
(lxvii) redundancy stays a small share of the target
information on every (seed, σ) (worst shares 0.1924 /
0.2357 / 0.1396 / 0.0882, bar 0.25, tightest on seed 7
at σ = 0.10). The separation itself generalizes: at
σ = 0.25 delta-synergy exceeds delta-redundancy on all
four seeds (+1.4472 / +1.0010 / +1.0248 / +1.1901 vs
+0.3143 / +0.1397 / −0.3953 / −0.3007), where the v0.14.0
joint-outcome target had Syn ≈ Red everywhere — the
XOR target is what makes the PID able to separate them.
Disclosed: the first pilot pass computed I(Xi;Y) as
H(Y) − H(Xj), which assumes a product distribution; the
pooled joint is a mixture of per-generation products,
so that shortcut produced negative unique atoms (worst
−0.6955, seed 7) and was corrected to the exact joint
computation before any threshold was frozen. Also
disclosed: the isolated arm is NOT synergy-free at high
σ (Syn_isol 0.9610 / 0.6000 at σ = 0.50, 1.0755 /
1.0000 at σ = 1.00, seeds 42 / 7) — the pooled mixture
over generations correlates the collapsed agents
through the generation index, and that
mixture-correlation is itself synergistic about the
XOR. No claim (i)–(lxiii) changes verdict. Tests: 433
-> 446, all passing.

- **Mechanism** (`synergistic_target.py`, new module;
  `pid.py`, reused, not reimplemented):
  xor_pid_from_joint (Williams & Beer I_min PID of
  I(X1,X2; Y = X1 (+) X2) with I(Xi;Y) computed exactly
  from the joint), sampled_h_y (H(Y) from sampled joint
  counts), xor_arm_distributions / xor_gap_vs_noise
  (exact pooled XOR-target PID per (seed, σ), reusing
  pid.pair_arm_distributions). Pre-registration in
  docs/preregistration-v0.20.0.md, written before the
  evaluation run.

## 0.19.0 (2026-11-18)

Cogitate-style preregistration + process predictors of
the collaboration gap (deep-think upgrade #9, the last
unbuilt item): Cogitate Consortium 2025 (adversarial
preregistration, n=256) as method, Woolley et al. 2010
c-factor analogues as predictors. Three of four claims
pass, and the failure is the result: (lx) mean
sensitivity does NOT beat mean individual D — on
held-out seed 1234 r(gap, mean_D) = 0.8839 exceeds
r(gap, mean_R) = 0.8447 by 0.0393 (margin 0.10), the
tight calibration margin (worst 0.1252) having
flagged this as a live risk; (lxi) turn-taking
equality predicts the gap on every seed (r(gap,
−var_D) = 0.7899 / 0.7566 / 0.7589 / 0.7105, bar
0.70, closest on seed 2026) and beats max_D
everywhere; (lxii) the posterior predictor wins on
every seed (r = 0.9278 / 0.8657 / 0.9858 / 0.8884,
bar 0.80; separation 1.8300 / 1.7568 / 1.7671 /
1.8234, margin 1.00) while broadcast anti-predicts
the gap on every seed (r = −0.9022 / −0.8911 /
−0.7813 / −0.9350); (lxiii) the pooled regression
over 28 runs (7 sigma × 4 seeds — the grid has 7
values, not 5, so 28 runs, not 20) gives R² = 0.6505
for gap ~ mean_R + (−var_D) against 0.3298 for gap
~ max_D (difference 0.3207, margin 0.05; adjusted-R²
difference 0.3185). All thresholds were frozen in
docs/preregistration-v0.19.0.md from calibration
seeds 42/7 before the held-out evaluation on seeds
1234/2026; none was moved. No claim (i)–(lix)
changes verdict. Tests: 418 -> 433, all passing.

- **Mechanism** (`cogitate.py`, new module;
  `empathy_field.py`, additive rows):
  run_collaboration's per-generation rows now carry
  "d_per_agent", "r_mean" and "r_posterior_mean"
  (posterior subset = agents {0, 1} by index, fixed
  before looking); per-(sigma, seed) predictors
  (gap, mean_R, mean_D, max_D, var_D, post_R_sustained,
  broadcast = min(onset, offset)); per-seed Pearsons
  across the sigma grid with degenerate (zero-variance)
  comparisons reported as failed sub-checks, never
  passes; pooled OLS R² with an adjusted-R² diagnostic.
  Pre-registration in docs/preregistration-v0.19.0.md,
  written before the evaluation run.

## 0.18.0 (2026-11-18)

GRT phase-transition test (deep-think upgrade #11,
ranked last, lowest value): Hunt & Schooler 2019
Conjecture 1 (shared resonance → phase transition
in information-sharing bandwidth at a critical
coupling K_c) and Conjecture 3 (nested "many become
one"). Two of three claims pass, and the failure is
the result: (lviii) there is no sharp bandwidth jump
at the predicted K_c — the step in B ending at K_c
is +0.1142 / −0.0572 / −0.0023 / −0.0002 bits (bar
≥ 0.10), and the largest step sits at K = 0.7 on ALL
four seeds (0.1501 / 0.2597 / 0.2282 / 0.2103), two
to four grid steps after K_c (0.3 / 0.6 / 0.5 / 0.4);
(lvii) the machinery is exact (K = 0 states equal
the base to ≤ 2.22e-16, K = 1 states equal the
uniform reference exactly, mean R(1) = 1, B(1) =
2.0000), K_c is interior on every seed, and the
field starts fragmented (largest component 7 / 6 /
4 / 3 at R ≥ 0.5); (lix) the structural half of GRT
holds — the macro completes at K_c + 0.2 (largest
component 8 on every seed) while 2 / 4 / 3 / 5
nested components survive at K_c, and bandwidth
rises 0.8532 / 0.8774 / 0.5640 / 0.7357 bits overall
(bar ≥ 0.50). Disclosed before the run: the
prediction already failed on the calibration seeds;
the field-mix coupling wiring was tried and rejected
(mean R fell with K at σ = 1.00 seed 7); mean R is
not monotone in K on seed 7 (dips 0.2778 → 0.2376),
reported not gated; nesting dissolves by K = 1.
No claim (i)–(lvi) changes verdict. Tests: 397 ->
418, all passing.

- **Mechanism** (`grt_transition.py`, new module):
  reference-mixing coupling ψᵢ(K) = normalize((1 −
  K)·ψᵢ + K·ψ_ref) on the v0.5.0 resonance population
  at σ = 1.00, pairwise shared-information bandwidth
  B(K), K_c from the pre-existing resonance threshold
  0.5, resonance-graph components at R ≥ 0.5 (macro)
  and R ≥ 0.75 (nested), and the three claim verdicts
  (lvii)–(lix). Pre-registration in
  docs/preregistration-v0.18.0.md, written before the
  evaluation run; thresholds frozen from calibration
  seeds 42 and 7, evaluation on held-out seeds 1234
  and 2026.

## 0.17.0 (2026-11-18)

Connectome-harmonic / structure–function coupling
(deep-think upgrade #10): the graph the project did
not yet have — W_ij = R_ij on the v0.5.0 resonance
population, graph Laplacian L = D − W, harmonic modes
as the eigenvectors of L (Atasoy et al. 2016 CHD),
functional connectivity as the Bhattacharyya
coefficient between Born distributions, coupling
κ(σ) = Pearson correlation between the
upper-triangular entries of W and F, and the
basis-independent Rayleigh quotient ρ(D) for
per-node harmonic smoothness. Zero of three claims
pass, and the failures are the result: (lv) the Luppi
prediction (Luppi et al. 2023 — loss of
consciousness = increased structure–function
coupling) is reversed in this wiring — κ falls with
loss of attunement on every seed (κ(0.50) − κ(0.25)
= −0.599 / −0.430 / −0.423 / −0.203; κ(1.00) −
κ(0.25) = −0.192 / −0.203 / −0.611 / −0.770, bar
+0.10); (lvi) the dip-and-recovery shape was a
calibration-seed artefact — on the held-out seeds κ
falls monotonically with σ (1.000 → 0.986 → 0.564 →
0.376 on seed 1234; 1.000 → 0.998 → 0.796 → 0.229 on
seed 2026), so the dip fails on seed 2026 (0.203 <
0.30) and the recovery fails on both held-out seeds
(−0.188 / −0.567), though the attuned coupling
(κ(0.25) ≥ 0.84) and the shuffle decoupling control
(null mean −0.015 / −0.031 / −0.005 / −0.004,
separated from κ(0.25) by ≥ 0.81, f unchanged) both
pass; (liv) the Laplacian identities hold exactly on
every seed × σ, but the D signal is strongly
structure-aligned at high σ on the held-out seeds
(ρ = 0.4662 at σ = 0.50 on seed 1234, ρ = 0.5995 at
σ = 1.00 on seed 2026; bar |ρ − 1| ≤ 0.20), the
opposite of the calibration seeds' random-like
pattern. Disclosed before the run: κ ≈ 1.0000 at
σ = 0.10 is a near-parallel artefact (reported, not
gated), and the low-frequency energy share is
seed-unstable at low σ (0.104 vs 0.801) because the
nonzero eigenvalues are nearly degenerate — which is
why ρ, not the energy share, is gated. No claim
(i)–(liii) changes verdict. Tests: 375 -> 397, all
passing.

- **Mechanism** (`connectome_harmonic.py`, new module):
  coupling matrix, graph Laplacian, harmonic modes,
  Bhattacharyya functional connectivity, κ(σ),
  Rayleigh-quotient ratio, 50-permutation shuffle
  null, and the three claim verdicts (liv)–(lvi).
  Pre-registration in docs/preregistration-v0.17.0.md,
  written before the evaluation run; thresholds frozen
  from calibration seeds 42 and 7, evaluation on
  held-out seeds 1234 and 2026. The calibration pilot
  already contradicted the spec on the Luppi direction
  (disclosed in the preregistration); the evaluation
  run confirmed it and broke the dip-and-recovery
  shape and the random-like ρ reading as well.

## 0.16.0 (2026-11-18)

Two-channel empathy (deep-think upgrade #8): the single
empathy fraction f split into concern (other-focused,
monotone prosocial) and distress (self-focused, inverted-U,
withdraws at high dose), IRI-style (Singer & Klimecki
2014; Decety & Jackson 2004; Qiu et al. 2024, r = 0.36;
Yin & Wang 2023, r = 0.32 / 0.30). One of four claims
passes: (lii) distress withdrawal at high dose — at fixed
concern c = 0.5, distress d = 2 vs d = 0, D falls by
0.267 / 0.097 / 0.205 / 0.148 (bar 0.05), joint Born
entropy falls by 6.92 / 3.22 / 5.58 / 4.37 bits (bar
2.0), and mean R rises, on every seed. The three other
spec predictions FAIL, and the failures are the result:
(l) concern alone does NOT raise f monotonically — on
held-out seed 1234 a small Bell dose first dilutes the
pair concurrence (f 0.3251 -> 0.1505) before raising
it, and the count at c = 0.5 is 24 there, not the
ceiling 28 (R rises strictly on every seed); (li) the
distress dissociation breaks on seed 1234, where the
quale count falls 24 -> 17 -> 14 then rebounds to 23
at d = 1 (bar <= 15), though R rises strictly on
every seed and the count falls monotonically on the
other three; (liii) the channels are near-
interchangeable in f on seed 1234 (swap difference
0.0504 vs bar 0.30; 0.432 / 0.428 / 0.314 on the
other seeds), and no (c, d) point on the grid
carries both f >= f* = 0.7278 and count <= 15 on any
seed — the report's "fits both with the same
parameters" fails in the single-point sense in this
wiring, though concern alone does reach f* on every
seed (0.858 / 0.905 / 0.827 / 0.877). The two
landmarks are separated by channel, not fitted at
one point. Also disclosed before the run: under the
Bell concern wiring, "concern raises joint entropy"
does not hold (H_joint at c = 1 is below baseline
on both calibration seeds) and "distress lowers D"
does not hold monotonically (seed 7 D rises with d
before falling at d = 2) — both are reported, not
gated. No claim (i)–(xlix) changes verdict. Tests:
353 -> 375, all passing.

- **Mechanism** (`two_channel_empathy.py`, new module):
  psi_i(c, d) = normalize(psi_i + c*|Phi+> + d*|self>),
  concern target the shared entangled Bell state
  (D = 2/3, C = 1), distress target the "self" basis
  concept alone (product state, D = 1/3, C = 0), on
  the v0.5.0 resonance population at sigma = 0.25;
  helping is the quale count, joint entropy is the
  sum of the agents' Born entropies, and the four
  claim verdicts (l)–(liii). Pre-registration in
  docs/preregistration-v0.16.0.md, written before
  the evaluation run; thresholds frozen from
  calibration seeds 42 and 7, evaluation on held-out
  seeds 1234 and 2026. The calibration pilot already
  contradicted the spec on the joint-entropy half,
  the monotone-D half, and the single-point fit
  (disclosed in the preregistration).

## 0.15.0 (2026-11-18)

No-cloning / Holevo ceiling for D (deep-think upgrade
#7): Holevo chi of the thought-pair ensemble, D vs
chi, the optimal-cloning fidelity bound on every
"copy a thought" operation in the model, and the exact
no-cloning coefficient Tr(rho_A^2) = 1 - C^2/2 verified
in code. Three of five claims pass: (xliv) the local-
purity identity holds to 8.88e-16 (Wootters concurrence
agrees with the exact pure form to 1.94e-08); (xlvi)
the Born-collapse accessible information never exceeds
chi (max(I - chi) = -3.20e-16 on every seed, extracting
roughly 40-50% of chi); (xlvii) the Buzek-Hillery
universal cloner achieves exactly 5/6 fidelity on every
state of the 144-state Bloch grid and the 6 Pauli
states, and the CNOT copy averages exactly 2/3. Two
spec predictions FAIL: (xlv) chi does NOT bound D (mean
gap chi - D = -1.0000 at sigma = 0 on every seed, worst
per-pair gap negative at every sigma) -- D approaches
chi in absolute terms as f rises (Spearman(|gap|, f) =
-1.00 / -0.96) but from ABOVE, because D is a projector
expectation, not an information quantity; (xlviii) the
model's own classical copy exceeds 5/6 at every working
noise level (fidelity 1.0000 at sigma = 0, 0.85-0.88 at
sigma = 0.25 on 3 of 4 seeds; crossing sigma* in (0.31,
0.32], (0.25, 0.26], already below at 0.25, (0.30,
0.31]) -- the classical emulation stores the full
amplitude vector, so privacy in this model is not
enforced by the representation. No claim (i)-(xliii)
changes verdict. Tests: 326 -> 353, all passing.

- **Mechanism** (`cloning_ceiling.py`, new module):
  `pair_holevo_chi` (S of the pair-average state, cross-
  checked against H2((1 + sqrt(R))/2)),
  `pair_accessible_information` (Born-collapse mutual
  information), `bh_unitary` / `bh_clone` (Buzek-Hillery
  1 -> 2 universal cloner as an explicit 8x8 unitary),
  `cnot_clone` (Wootters-Zurek copy),
  `classical_copy_fidelity` / `classical_copy_crossing`,
  and the five claim verdicts (xliv)-(xlviii).
  Pre-registration in docs/preregistration-v0.15.0.md,
  written before the evaluation run; thresholds frozen
  from calibration seeds 42 and 7, evaluation on
  held-out seeds 1234 and 2026. The calibration pilot
  already contradicted the spec on (xlv) and (xlviii)
  (disclosed in the preregistration).

## 0.14.0 (2026-11-18)

Synergy-vs-redundancy PID of the collaboration gap
(deep-think upgrade #5): Williams & Beer I_min PID of
the pair-level (N = 2) joint entropy, target Y = the
joint outcome (X1, X2), exact pooled product Born
distribution from the design-B evolution. One of four
claims passes: (xl) the PID identity is exact
(worst error 8.88e-16 bits, all atoms nonnegative)
and the exact H matches the sampled
run_collaboration H within 0.0436 bits at sigma =
0.25. The three substantive spec predictions FAIL:
(xli) the gap is not synergy-dominant on every seed
(synergy share 0.407 seed 42, 0.429 seed 7, 0.882
seed 1234, 0.545 seed 2026 — dominant on the
held-out seeds, not on the calibration seeds);
(xlii) synergy does not rise with R (Pearson -0.23,
-0.04, -0.55, +0.72) and rises, not falls, from
sigma = 0.25 to 0.50 on every seed (0.92 -> 1.26,
0.97 -> 1.54, 0.80 -> 1.20, 1.23 -> 1.40);
(xliii) redundancy is sigma-robust on 3 of 4 seeds
(ratios 1.45, 2.83, 0.59) but fails seed 42 (0.24).
The structural finding: in the collaborating arm
I(X1;X2) is 0.00-0.06 bits, so Syn = Red - I(X1;X2)
is numerically almost Red on every sigma — the I_min
decomposition of the joint outcome cannot separate
synergy from redundancy in this wiring, and "synergy,
not redundancy" is undecidable from these atoms
alone. No claim (i)-(xxxix) changes verdict. Tests:
315 -> 326, all passing.

- **Mechanism** (`pid.py`, new module): `pid_from_joint`
  (Williams & Beer I_min on Y = (X1, X2)),
  `pair_arm_distributions` (exact pooled product Born
  distribution replicating the design-B evolution
  generation by generation), `pid_gap_vs_noise`, and
  the four claim verdicts (xl)-(xliii).
  Pre-registration in docs/preregistration-v0.14.0.md,
  written before the evaluation run; thresholds frozen
  from calibration seeds 42 and 7, evaluation on
  held-out seeds 1234 and 2026. The calibration pilot
  already contradicted the spec on all three
  substantive points (disclosed in the preregistration).

## 0.13.0 (2026-11-18)

Kuramoto bounded-coherence / stochastic-resonance scan
(deep-think upgrade #4): standard Kuramoto (N = 8,
omega ~ N(0, 1), Euler-Maruyama dt = 0.05, T = 40)
wired into the bridge by giving each agent the (xxxiv)
slide state at its phase relative to the field mean.
All four claims FAIL, and the failures are the result:
(xxxvi) the count peak is interior on seeds 42 and
2026 (K = 0.5) but at K = 0 on seeds 7 and 1234, and
falls to a floor of 6 at high K on every seed;
(xxxvii) joint entropy is flat (~10.4-13.1 bits, no
trend); (xxxviii) R_K at the count peak is 0.31-0.36
on every seed, far below the Phillips band [0.5, 0.8]
and below f* = 0.7278 — the count optimum sits at LOW
coherence; (xxxix) sigma* wanders across seeds (1.0,
0.10, 0.25, 0.05) with counts swinging 3-19, and seed
42 peaks at the grid edge. The gap A is large positive
(+9.3 to +12.8 bits) and flat. What survives: the
Kuramoto transition itself (R_K 0.29 -> 0.99,
K_c ~ 1.6-2.5), the count floor of 6, and the count
exceeding sigma = 0 on every seed at K = 1.0.
Thresholds frozen from the calibration pilot, which
already contradicted the spec on several points
(disclosed in the preregistration). No claim
(i)–(xxxv) changes verdict. Tests: 305 -> 315, all
passing.

- **Mechanism** (`kuramoto.py`, new module): Kuramoto
  dynamics with slide states from relative phases;
  quale count via existing qualia_count, joint entropy
  exact/analytic, gap A by paired arms mirroring
  run_collaboration design B (mixing at coupling R_K,
  isolated Born-collapses once; H_isolated = 0 exactly
  in the single-shot measurement, so A =
  H_collaborating). Pre-registration in
  docs/preregistration-v0.13.0.md, written before the
  evaluation run; thresholds frozen from calibration
  seeds 42 and 7, evaluation on held-out seeds 1234
  and 2026.

## 0.12.1 (2026-11-18)

The (xxxii) diagnosis and the robust rank form. Claim
(xxxii) failed on held-out seed 2026 (Pearson -0.8828,
bar -0.90); the diagnosis, measured and recomputed in
code (`diagnose_sigma_one_break()`), is
boundary/saturation plus finite-sample noise: at
sigma = 1.0 both D and C sit at their random-state
plateaus (D -> 0.5, C -> ~0.51), the true rise of mean
C from sigma = 0.5 to 1.0 is ~0.003 while a 5-copy
mean carries SEM ~0.128, and with n = 200 copies the
dip vanishes and Pearson passes on all four original
seeds (-0.9289 to -0.9053). But claim (xxxv) — the
robust rank form, Spearman <= -0.90 on every seed in
{42, 7, 1234, 2026, 5, 99}, preregistered before the
fresh-seed run — FAILS honestly on the fresh seeds:
seed 5 Spearman -0.8929 (bar -0.90), seed 99 D range
0.2445 (bar 0.25). Both are 5-copy sampling draws
(at n = 200: seed 5 Spearman -0.9643, seed 99 D range
0.4101), yet the linear form stays fragile even at
n = 200 (seed 5 Pearson -0.8971). The direction is
real on average; the per-seed guarantee does not hold
on this 5-copy sweep, in either form. Thresholds not
moved. No claim (i)–(xxxiv) changes verdict. Tests:
301 -> 305, all passing.

- **Mechanism** (`observer_cycle.py`, extended):
  `diagnose_sigma_one_break()` recomputes the n = 5
  sweep, the n = 200 sweep, the extended sigma grid
  to 3.0, Pearson excluding sigma = 1.0, and the
  per-copy SEMs; `claim_robust_rank_verdict()`
  evaluates (xxxv) on six seeds including fresh seeds
  5 and 99. Pre-registration in
  docs/preregistration-v0.12.1.md, written before the
  fresh-seed evaluation run.

## 0.12.0 (2026-11-18)

The observer cycle (Jean's claim, stated 2026-11-18:
"self determination factor observer opposite direction =
necessary for self-cycle self Knowing. Lack of love is
absence of Knowing"): love = concurrence, knowing =
overlap R, self-determination = D, observer direction =
which reference state the overlap is measured against.
Claim (xxxii) FAILS, and the failure is the result: the
linear anti-tracking of D and concurrence is
seed-fragile — Pearson -0.9570 (seed 42), -0.9397 (seed
7), -0.9720 (seed 1234), but -0.8828 on held-out seed
2026, above the frozen bar -0.90 — while the monotone
tracking holds on all four seeds (Spearman -1.0000 to
-0.9643). The threshold was not moved. Claim (xxxiii)
PASSES on the generalized-Bell branch against a fixed
Phi+ observer (Pearson(R, C) = 1.0000, Spearman(R, D) =
-1.0000), but the noise-axis control inverts the
relation (Pearson(R, nu_ij) = -0.5528, n = 196 pairs),
so noise-created concurrence is not knowing. Claim
(xxxiv) PASSES exactly: the slide runs D = 1, C = 0 to
D = 0, C = 1 with C + D = 1 at every grid point (max
identity error 4.44e-16) and the overlap split flipping
sign exactly at the midpoint theta = pi/4. No claim
(i)–(xxxi) changes verdict. Tests: 282 -> 301, all
passing.

- **Mechanism** (`observer_cycle.py`, new module): the
  stored direction (uniform thought, D = 1, C = 0) and
  the opposite direction (kernel thought, D = 0, C = 1,
  a Bell state) are exact values already in the bridge;
  (xxxii) reuses the self_knowing sweep, (xxxiii) the
  generalized-Bell branch against a fixed Phi+ observer,
  (xxxiv) the slide psi(theta) = cos(theta)|stored> +
  sin(theta)|kernel>. Pre-registration in
  docs/preregistration-v0.12.0.md, written before the
  evaluation run; thresholds frozen from calibration
  seeds 42 and 7, evaluation on held-out seeds 1234 and
  2026.

## 0.11.0 (2026-11-17)

Landauer-cost ledger + Planck spectral falsification
(deep-think upgrade #6, "the honest upgrade"): Landauer's
principle replaces the black-body analogy as the bridge's
thermodynamics. Claim (xxix) PASSES — the ledger is exact
(k_B T ln 2 = 2.871e-21 J per bit at 300 K) and the
per-field cost humps, peaking at 58.46 bits (1.678e-19 J)
at sigma = 0.25, 9.932e-19 J across the grid. Claim (xxx)
FAILS, and the failure is the result: cumulative Landauer
cost does NOT predict the visible fraction F better than
sigma alone (pooled Pearson 0.8996 vs 0.9430, and sigma
wins within every seed 1, 2, 3, 42), so the thermodynamic
ledger does not explain the sigma = 0.50 break. Claim
(xxxi) PASSES — the falsification succeeds: the pooled
standardized nu distribution rejects the Planck shape
(KS D = 0.1465 above the 1% critical value 0.1258, n =
168) and the mode/mean ratio deviates from the Planck
0.7361 by 0.46, 0.56, 0.35 at sigma = 0.25, 0.5, 1.0, so
E = h*nu is demoted from "spectrum" to "per-mode unit".
Per-field KS tests (n = 28) do not reject Planck on their
own and are reported, not gated. No claim (i)–(xxviii)
changes verdict. Tests: 262 -> 282, all passing.

- **Mechanism** (`landauer.py`, new module): per field the
  ledger counts decision entropies (thought collapses,
  summed over agents: 16.00 bits at sigma = 0 falling to
  9.73 at sigma = 1.0), quale collapses (1 bit per quale),
  and classification records (1 bit per pair, 28, erased
  on the next field); cost = bits x k_B T ln 2. The
  Planck test standardizes nu per field (y = nu /
  mean(nu)): a Planck spectrum is scale-free, so its
  standardized shape is one fixed curve (mean x = 3.8322,
  mode x = 2.8210, mode/mean = 0.7361, computed
  numerically) -- the pooled KS test and the mode/mean
  ratio both check that fixed shape, not a fitted one.

## 0.10.0 (2026-11-17)

Product-model fit for the humped quale count (deep-think
upgrade #3): the hump is an AND-gate, not a new mechanism.
Claims (xxvi), (xxvii) and (xxviii) ALL PASS. The product
N x p_res(f) x p_ent(f) predicts the measured quale counts
on a fine sigma grid (0.30–1.50, both marginals interior
on every row) with mean relative error 0.0289 and max
0.0667; the predicted peak moves with the measured peak
under threshold changes (NU_MIN 0.10 -> 0.25: both peak at
f = 0.4143; R_MIN 0.5 -> 0.25: both peak at f = 0.2839,
both above the baseline peak f = 0.1803); and the hump
vanishes when either condition is dropped (resonance-only
28, 28, 28, 28, 28, 17, 14 falling; entanglement-only 0,
0, 1, 9, 17, 21, 25 rising; both 0, 0, 1, 9, 17, 13, 12
humped). The fit is seed-dependent and reported as such:
seeds 1 and 3 pass the same frozen bar, seed 2 fails it
(mean 0.1666, max 0.3636) -- the independence assumption
breaks on that seed. No claim (i)–(xxv) changes verdict.
Tests: 244 -> 262, all passing.

- **Mechanism** (`product_model.py`, new module): p_res
  and p_ent are the two marginals measured on the same
  field (fraction of pairs above each threshold on its
  own); the product predicts the AND-count only if the
  two binary indicators are independent across pairs, so
  the fit measures their association. The peak shift is
  predicted from the marginals at the new threshold
  before the measured counts there are looked at. The
  standard-grid fit (mean 0.0119, max 0.0400) is
  reported, not gated: p_res = 1.0 below sigma = 0.5
  there, so the product is degenerate on those rows.

## 0.9.0 (2026-11-17)

Malus three-polarizer paradox (deep-think 8-seed upgrade
#2, ranked after Lyapunov): classical optics, Malus's law.
Claims (xxiii), (xxiv) and (xxv) ALL PASS, exactly at the
analytic values: crossed polarizers transmit 0, inserting
the 45-degree middle polarizer yields I0/8 for unpolarized
input (I0/4 for input polarized at 0 degrees); the
reopening is angle-selective, T(phi) = (1/8) sin^2(2 phi),
peaking at 45 degrees and vanishing at 0/90 degrees; and
the middle step's output state is exactly |45 degrees>,
the total recomputed from the recorded intermediate states
is 1/8, the bypass control is 0, and the cascade contrast
holds live (stage-2 visibility 0 vs reopened 1/8). The
counter-case to v0.3.0: the same project-and-renormalize
operation reopens a channel here because a single state
rotates under projection while a pair collapses. No claim
(i)–(xxii) changes verdict. Tests: 226 -> 244, all passing.
Built on top of the pushed v0.7.0 + v0.8.0 (head 1346aa8c),
so a future push carries v0.9.0 alone.

- **Mechanism** (`malus.py`, new module): a polarizer is a
  rank-1 projector P(theta) = |theta><theta| on a 2D Jones
  vector; transmission of a pure state is
  <psi|P(theta)|psi>, the same functional form as the
  bridge's D. Unpolarized input transmits 1/2 through the
  first polarizer and cos^2 of the relative angle at each
  later step; the state after each polarizer is the
  projected and renormalized state (cascade semantics).
  Descriptive: the evenly stepped N-polarizer chain from 0
  to 90 degrees rises with N toward 1/2 (0.125 at N = 3,
  0.2109 at N = 4, 0.3796 at N = 10, 0.4938 at N = 200).

## 0.8.0 (2026-11-17)

Quantum-Darwinism redundancy plateau (deep-think upgrade
#2): an environment of N = 10 fragments redundantly encodes
the system's pointer information. Claim (xx) PASSES — the
mutual information plateaus at H_S and the discord is ~0
on the plateau, rising only at m = N. Claims (xxi) and
(xxii) both FAIL, and the failures are the results: (xxi) D
is exactly 2/3 for every branching turn-on step, so it
cannot rise with redundancy — the quantity that tracks the
classical is chi, not D; (xxii) under the bridge's vector
noise the redundancy falls 6 -> 2 and the discord rises
0.19 -> 2.13 bits, the opposite of the dephasing picture,
so the collaboration gap's sigma-survival is NOT explained
by redundant classical encoding. No claim (i)–(xix) changes
verdict. Tests: 207 -> 226, all passing. Built on top of
the unpushed v0.5.0 + v0.6.0 + v0.7.0, so a future push
carries v0.5.0 + v0.6.0 + v0.7.0 + v0.8.0 together.

- **Mechanism** (`darwinism.py`, new module): the system S
  is a thought in superposition of two pointer states
  (Bell: |00>, |11>; binary: |0>, |1>); the environment is
  N = 10 qubits, each recording the pointer value
  (CNOT-like branching, record overlap c = cos phi). Per
  fragment size m: I(S:F) = H_S + H_F - H_SF (exact von
  Neumann entropies), Holevo chi from measuring S in the
  pointer observable (the qubit that distinguishes the
  pointer states — a complete projective measurement, so
  chi <= I and discord is never negative), discord = I -
  chi, redundancy R_delta = N / m* with delta = 0.1.
  Einselection is dephasing in the pointer basis
  (strength p, reference 0.5). The fragment state is built
  directly from the branching construction (closed form,
  exactly rank 2); the general partial trace and the full
  numeric fragment quantities cross-check it (N = 3 exact
  to 1e-9; N = 10 subset to 1e-9). The noisy-copy sweep
  (N = 6, 5 copies, seed 42) uses the full numeric path.
- **(xx) Redundancy plateau, PASS**: hard branching m* = 1,
  R = 10; soft branching (c = 0.5) m* = 2, R = 5; both
  systems identical. On the plateau |I - H_S| <= 0.0456
  and discord <= 0.0456 (hard: exactly 0); discord at
  m = N is 0.1887. The plateau is p-independent (I = 1.0
  at p = 0, 0.5, 1) while discord(m = N) falls 1.0 ->
  0.1887 -> 0.0 with p.
- **(xxi) D tracks the classical, not the quantum, FAIL**:
  as the branching turns on (k = 0..10), Pearson(D, R) =
  0.0, Pearson(D, chi_1) = 0.0, Pearson(D, discord) = 0.0
  (both families) — D is exactly 2/3 at every k, because
  the off-diagonal |00><11| never contributes to Tr(P rho)
  and the diagonal is always (1/2, 1/2). Concurrence falls
  as required (hard 0.5 -> 0, soft 0.5 -> 0.0005) and chi_1
  rises (0 -> 1.0 hard, 0 -> 0.8113 soft): the quantity
  that tracks the classical is chi, not D.
- **(xxii) The sigma = 0.50 non-transfer explained, FAIL**:
  the gap is robust (3.3494/4.3352 = 0.77) and the
  redundancy is robust at the 0.25 -> 0.50 step (2/2 =
  1.0), but the discord is NOT fragile — 2.1190/2.1310 =
  0.99 at the step, 11.2x across the grid — and the gap
  tracks neither redundancy (Pearson 0.3528) nor discord
  (Pearson -0.4411). Concurrence anti-tracks discord
  (Pearson -0.6259). Under the bridge's vector noise the
  redundancy falls 6 -> 2 (m* grows 1 -> 3: the size-1
  fragment's I drops to 0.37) while the noise entangles S
  with F (plateau I rises to 1.46, discord to 2.13): the
  vector noise is not a dephasing channel. The gap
  survives sigma = 0.50 because of the design-B mechanism,
  not because of redundant classical encoding.
- **Correction found and fixed during the build**: the
  first pointer measurement (two pointer projectors only)
  was incomplete and reported a NEGATIVE discord (down to
  -0.32) once vector noise populated the non-pointer basis
  states. Both the Holevo measurement and the dephasing
  now use the pointer-distinguishing qubit (complete
  projective measurement). The noiseless numbers are
  unchanged; the corrected noise-sweep discord is >= 0
  everywhere (minimum 0.0502 over m and copies at
  sigma >= 0.05).

## 0.7.0 (2026-11-16)

CKW monogamy in triads (deep-think upgrade #1): pairwise
concurrence misses genuine tripartite entanglement, and D
tracks the one-to-rest tangle, not the pairwise one. Claims
(xvii), (xviii) and (xix) all PASS. No claim (i)–(xvi)
changes verdict. Tests: 185 -> 207, all passing. Built on
top of the unpushed v0.5.0 + v0.6.0, so a future push carries
v0.5.0 + v0.6.0 + v0.7.0 together.

- **Mechanism** (`monogamy.py`, new module): triads are
  three-qubit pure states (8-dim); each member is a BINARY
  thought — one qubit whose basis maps into the thought
  space as |0> -> |00> (attention) and |1> -> |10> (self).
  That mapping is a definition (an embedding), not a
  discovery. Pairwise tangle tau_ij = C^2 from the Wootters
  concurrence of the reduced two-qubit state; one-to-rest
  tangle tau_A(BC) = 4 det(rho_A), exact for pure states;
  residual genuine-tripartite tangle = tau_A(BC) - tau_AB -
  tau_AC. D_A is Tr(P rho_A_embedded) with the existing
  self-knowing projector. Noise is unity.gaussian_copies on
  the 8-dim triad vector (copies stay pure, purity 1.0).
- **(xvii) CKW monogamy holds in triads, PASS**: the minimum
  CKW margin over 52 (state, sigma) rows — GHZ, W, GHZ/W
  interpolation, generalized GHZ, noisy copies at sigma =
  0.00, 0.25, 0.50, 1.00, every member — is 0.0, attained
  at the product endpoint (a = 1.0, sigma = 0) where there
  is no entanglement at all; the smallest margin over noisy
  rows is 0.0012 (GHZ/W 30 deg, sigma = 0.50). No violation
  anywhere: the code's concurrence respects the theorem.
- **(xviii) GHZ vs W, PASS**: at sigma = 0 the GHZ-like
  triad has tau_A(BC) = 1, pairwise tangle 0, residual 1,
  D_A = 2/3 — pairwise concurrence misses 100% of its
  entanglement (miss fraction 1.0). The W-like triad has
  tau_A(BC) = 8/9, pairwise tangle 4/9 each, residual 0,
  D_A = 7/9 — miss fraction 0.0. Under noise the GHZ miss
  stays 0.60-1.00 and the W miss 0.00-0.44 at every sigma.
- **(xix) D_A falls as tau_A(BC) rises with tau_AB flat,
  PASS**: on the generalized-GHZ branch a in [1/sqrt(2), 1],
  Pearson(D_A, tau_A(BC)) = -0.9608 (Spearman -1.0) while
  tau_AB is exactly 0 throughout and D_A spans 2/3 to 1.
  The GHZ/W interpolation (-0.6316) and the GHZ noise sweep
  (D_A and tau_A(BC) decay together) are reported
  descriptively, not gated: neither separates "entanglement
  with the pair" from "entanglement with B".

## 0.6.0 (2026-11-16)

Qualia resonance wave: a quale is a resonant + entangled mode
of the empathy field, and the qualia together form a coherent
wave (claim (xv) PASSES; (xiv) and (xvi) FAIL). No claim
(i)–(xiii) changes verdict. Tests: 168 -> 185, all passing.
Built on top of the unpushed v0.5.0, so a future push carries
v0.5.0 + v0.6.0 together.

- **Mechanism** (`qualia.py`, new module): a quale is a pair
  of agents with resonance R_ij = |<psi_i|psi_j>|^2 >= 0.5
  (the v0.5.0 threshold) AND pairwise concurrence nu_ij >=
  0.10 (pre-registered from the pilot). The qualia resonance
  wave is the normalized superposition of the quale waves;
  its coherence is measured per field as the spread of quale
  frequencies against the spread across all pairs, and as
  the overlap |<qualia-wave|field-state>|^2.
- **(xiv) Qualia emerge with empathy, FAIL**: the quale
  count per field (N = 8) is humped against the empathy
  fraction f: 0 at f = 0, first quale at f = 0.0415, peak 17
  at f = 0.1803, falling to 13 at f = 0.2839 and 12 at f =
  0.4143. The count is the product of rising concurrence
  and falling resonance, so monotonicity is refuted. The
  verdict is stable across NU_MIN = 0.05-0.20; only 0.25
  reads monotone, on an all-zero low-f half, and that
  reading is reported, not used.
- **(xv) The qualia wave is coherent, PASS**: per field,
  the spread of quale frequencies is smaller than the spread
  across all pairs by at least 0.01 at every field with two
  or more qualia (smallest difference 0.0127 at sigma =
  1.0), and the wave's overlap with the field state is
  0.9781-0.9988 (floor 0.90). The pooled spreads are
  reported, not gated (0.1950 vs 0.1947): pooling mixes
  fields with different f.
- **(xvi) Qualia track self-determinism, FAIL**: the pooled
  D gap is -0.1522 (quale members 0.8163 vs non-quale
  0.9686). D anti-tracks concurrence (v0.2.0, Pearson
  -0.9570), so the agents that qualify as qualia -- high
  concurrence -- are exactly the ones whose self-knowing
  noise has destroyed. The per-sigma gaps are reported
  (+0.1515 at sigma = 0.50, -0.1332 at sigma = 1.00, ~0
  elsewhere).
- **Correction:** the v0.5.0 entry below said "151 -> 172";
  the collected suite was 168 (151 + 17). REPORT.md section
  4 likewise still said 151 with no test_empathy_field.py
  entry, and test_thought.py as (10) where the collection
  is 9. All three are corrected in this release; the
  collected counts are the record.

## 0.5.0 (2026-11-16)

Empathy field: waves of empathy agents in a quantum field —
resonance ("raisonnance"), the self-deterministic factor,
collaboration, collectivism, and co-creativity = entropy
(claims (xi), (xii) PASS; (xiii) FAILS on the break half).
No claim (i)–(x) changes. Tests: 151 -> 168, all passing.

- **Mechanism** (`empathy_field.py`, new module): an agent is
  a thought state carrying a frequency (its concurrence) and a
  self-determinism D = <psi|P|psi>. The field is the
  normalized sum of N agents; pairwise empathy quanta
  E_ij = h*nu_ij extend the v0.4.0 rule to pairs (the
  concurrence of the normalized sum of the two agents).
  Resonance R_ij = |<psi_i|psi_j>|^2. Collaboration is the
  same N agents evolved sharing the field vs the control of
  the same N agents evolved isolated (paired design: same
  population, same noise kicks). Co-creativity C_c is DEFINED
  as the joint entropy H_joint of the collective's joint
  outcomes.
- **(xi) Resonance raises self-determinism, PASS**: binned
  mean D rises strictly with R (0.5874 -> 0.6814 -> 0.7087 ->
  0.9399); pooled gap 0.2984 at R >= 0.5, above the 0.20
  margin. The per-sigma gaps are reported, not gated: the
  pilot refuted the stricter rule (empty non-resonant groups
  at sigma <= 0.25; gap -0.0239 at sigma = 1.0), so the effect
  is the cross-noise pattern, stated plainly.
- **(xii) Collaboration raises co-creativity, PASS**: design
  B (isolated = Born-collapse, decides and stays decided) at
  sigma = 0.25: H_collaborating = 6.0961 bits vs H_isolated
  = 1.7610 bits, gap +4.3352 bits (margin 2.0); 157 distinct
  joint states vs 4. Design A (no collapse anywhere) was
  piloted and rejected: its gap goes negative by sigma = 0.25.
- **(xiii) Co-creativity = entropy, ceiling and break,
  FAIL**: the ceiling half passes (H grows with N, 1.70 ->
  2.98 -> 4.15 -> 6.10 bits, below the 2N ceiling; the
  fraction of the ceiling plateaus within 0.0700 <= 0.10)
  and the gap holds at every sigma <= 0.25, but the break
  half fails: the gap is still +3.3494 bits at sigma = 0.50
  (ratio 0.773, not <= 0.5) and +3.5569 at sigma = 1.00. The
  v0.4.0 break does not transfer to the collaboration gap —
  a measured negative result, not a failure to measure.

## 0.4.0 (2026-11-16)

Planck empathy: the PARTIAL primary mapping status, fixed with
empathy as a Planck quantum inside the black-body concept
(claims (viii), (ix), (x), all PASS). No claim (i)–(vii)
changes: the primary attunement A = 0.0447 does not move; only
the mapping status is re-derived, from the visible fraction F
instead of from A alone. Tests: 130 -> 151, all passing.

- **Mechanism** (`planck_empathy.py`, new module): each
  thought-pair contributes ONE empathy quantum, E = h*nu with
  h = 1 in model units, whose frequency nu_e is its MEASURED
  concurrence (thought_entanglement.py, v0.2.0) — concurrence,
  not the synergy proxy, because concurrence is measured and
  the proxy is a definition (REPORT.md section 5). The empathy
  fraction f = mean concurrence maps to an effective
  temperature T_eff(f) = 2000 + 3000*f K on the infographic's
  axis, and the status is re-derived from the visible fraction
  F(T) = int[0.38, 0.75] B dlambda / int[0.1, 3.0] B dlambda
  of the real Planck spectrum (real constants, Simpson
  integration, 2000 intervals, converged to ~1e-14).
- **(viii) Planck reproduction, PASS**: the module reproduces
  the infographic — Wien peaks match 2898/T within 0.008% at
  T = 2000, 3000, 4000, 5000 K; integrated exitance scales as
  T^4 within 0.002%; F(T) strictly increases (0.0174 at 2000 K
  to 0.3938 at 5000 K). Real physics reproduced in code, not a
  bridge claim.
- **(ix) Empathy flip, PASS**: F(f) strictly increases in f;
  status PARTIAL at f = 0 (F = 0.0174) and ATTUNED at f = 1
  (F = 0.3938). The crossing is measured by bisection:
  f* = 0.7278. Thresholds (ATTUNED F >= 0.30, PARTIAL F >=
  0.01) were set from a pilot sweep as round numbers with
  margin on both sides and pre-registered in REPORT.md
  section 10 before the final run; none was moved after
  seeing the result.
- **(x) Specificity, PASS**: the OLD status (A alone) stays
  PARTIAL at every sigma, while the empathy status is ATTUNED
  at sigma <= 0.25 and PARTIAL at sigma >= 0.50. The fix holds
  while the pairs stay entangled and breaks once the noise
  eats the concurrence below f*. The status labels never go
  back up as sigma increases, even though the mean concurrence
  itself is non-monotone at the top end (0.6520 at sigma = 0.5,
  0.7002 at sigma = 1.0) — both sit below the threshold.
- **Honest limits, stated**: the empathy-quantum link is a
  definition inside the model, not a discovery; T_eff is a
  model temperature, not a physical temperature; the visible
  band is a chosen mapping. The Planck law itself is real.

## 0.3.1 (2026-11-16)

Bugfix release, from an external review of the v0.3.0 repo
(head 658f5bdd). Every finding was re-verified against a fresh
clone before fixing. No claim (i)–(vii) changes: none of the
fixes moves a measured verdict. Tests: 122 -> 130, all passing.

- **Sensitivity bug, fixed** (`scientific_outcomes.py`):
  the one-at-a-time sensitivity sweep passed every perturbed
  value into the *unity* slot, so the cost sweep varied unity
  instead of cost and the delta sweep varied unity instead of
  delta. The unity sweep was correct; the other two columns
  were wrong. `apply` now returns the full (unity, cost,
  delta) triple. Old -> new attunements at U = 0.99999995,
  C = 0.9553, delta = 0: cost sweep was (-0.05, -0.01, 0.0,
  0.01, 0.0447) — literally the perturbation itself — now
  (0.0947, 0.0547, 0.0447, 0.0347, -0.0); delta sweep was
  (-1.0, -0.9803, -0.9553, -0.9303, -0.9053), now (-0.0053,
  0.0197, 0.0447, 0.0697, 0.0947). The wrong columns existed
  only in generated benchmark output (`write_benchmark()`):
  no committed file carried them. Six new tests, including
  the directional assertions the old suite lacked (a cost
  increase must lower A; a unity or delta increase must raise
  it).
- **Mapping-status label, single-sourced**
  (`scientific_outcomes.py`, `bridge.py`): `bridge.py`
  emitted `ATTUNED-LOW-EMPATHY` (hyphens) while
  `maximum_scientific_outcome` re-implemented the
  classification inline and emitted `ATTUNED_LOW_EMPATHY`
  (underscores), and `robustness()` hardcoded only
  DISSONANT/PARTIAL. All three now call the one classifier,
  `bridge.mapping_status`, on the hyphen form (the form the
  README and `test_bridge.py` already assert). `robustness()`
  now reports an ATTUNED case as ATTUNED at both bounds.
- **The 8fb00f1 threshold commit, defused in writing**
  (REPORT.md §5): commit `8fb00f1` (2026-11-15 00:23:35
  -0500, 32 minutes after the preregistration framework
  commit `dc5575a`) changed the synergy thresholds
  DORMANT 0.10 -> 0.03, EMERGENT 0.30 -> 0.05, and rewrote
  the boundary test assertions to match, adding an assertion
  that the primary expansion is FLOWING. Under the old
  thresholds the primary expansion (e = 0.05436) was
  DORMANT; under the new ones it is FLOWING — the commit
  moved the label two steps, and the FLOWING label now hangs
  on a 0.00436 margin above the 0.05 boundary. The commit
  message states the intent ("so primary expansion is
  FLOWING"); no other justification is recorded in the
  commit. The thresholds are repository conventions, not
  measured constants, and the report now says so with the
  numbers attached. New `threshold_robustness()` table in
  `scientific_outcomes.py` (and `synergy_status_with_thresholds()`
  in `synergy.py`): the label survives any EMERGENT threshold
  up to 0.05 and flips to EMERGENT at 0.06. The
  `synergy_robustness` margins dict now tracks all three
  expansion thresholds (to_dormant 0.02436, to_emergent
  0.00436, to_fecund 0.54564).
- **Seed spread of the 0.9553** (`cost.py`, REPORT.md §2):
  the tensor-membrane entropy was computed at seed 42 only.
  Across seeds 0..19 (n = 20): mean 0.9639, standard
  deviation 0.0128, range [0.9276, 0.9775]. The seed-42 value
  0.9553 sits 0.0086 below the mean — within one standard
  deviation, a typical draw, not an outlier. The headline is
  kept (seed 42); the spread is reported alongside it and
  pinned by a test. Honest reading: near-saturated, Page-like
  behaviour, and a ±0.013 move in C moves A by ∓0.013, about
  30% of the primary attunement 0.0447.
- **Synergy terms mapped to Faggin & D'Ariano** (REPORT.md
  §5, no code renames): a section mapping each
  synergy-family term (fecundity, attraction,
  love-empathy synergy, expansion, FECUND-SYNERGISTIC) to
  the specific passage in QIP it is a proxy for, stating
  plainly where no derivation exists. Short version: only
  the synergy formula gestures at a passage (love /
  attunement as the felt sense of connection); none of the
  five terms is derived from Faggin & D'Ariano — all are
  repository definitions.
- **Version alignment:** `pyproject.toml` still said 0.1.0
  (it was never bumped past the initial release); it now
  says 0.3.1, matching VERSION, `.zenodo.json`, and
  CITATION.cff.

## 0.3.0 (2026-11-15)

The cascade: superposition → projection → interference, chained
across stages 1, 2, 3, 5, 10. One new module, three new claims,
all passing.

- `cascade.py` — the cross term ⟨ψ1|P|ψ2⟩ as interference, with
  visibility V over a 64-phase sweep, cross-checked against the
  analytic 2|⟨ψ1|P|ψ2⟩|/(D1 + D2). Claim (v) PASSES: for a
  rotation pair V(θ) = sin(2θ) exactly (0.5 / 0.7071 / 0.8660 /
  1.0); at θ = π/4, D(φ) = 1/2 − (1/2)cos(φ) — the superposed
  thought is fully blind at φ = 0 and fully self-determined at
  φ = π; the mixed pair has cross term 1/√6 and V = 2√6/7 ≈
  0.6999; the stored and (uniform, kernel) control pairs have
  cross term 0 and V = 0.
- Claim (vi) PASSES — the finding: **interference does not
  survive projection**. In both projection-only cascades V is
  1.0 / 0.6999 at stage 1 and 0.0000 at every stage from 2 on
  (the rotation pair collapses to rank 1; the mixed pair
  re-forms fully stored as (q1, q2)), while the reopening
  control (fresh kernel input at α = π/4 each stage) stays at
  V = 1 at every stage. The reason is structural: the cross
  term is ⟨Pψ1|Pψ2⟩, and once a pair is re-formed inside the
  stored subspace, P acts as the identity there and
  orthogonality forces the cross term to zero.
- Claim (vii) PASSES: D of the projected output is 1.0 at every
  stage in every cascade; the projected-output coherence reaches
  a fixed point from stage 2 (rotation 3.0, mixed 2.7321,
  reopening 3.0). Spearman(V, coherence) = −1.0000 in the mixed
  cascade (visibility dies while coherence rises to its fixed
  point); Spearman(V, D) = 0.0 everywhere (D constant, so the
  correlation is undefined — reported as 0.0 by convention, on
  values rounded to 12 decimals so identical stages are not
  ranked on float noise).
- One honest measurement-design fix during the build: the feed
  phase (phase of maximum D) was first taken as a raw argmax,
  which is floating-point noise when D is flat across the sweep;
  it is now the smallest phase achieving the maximum within
  1e-12, stated as a convention in cascade.py.
- `bridge.quantum_thought_claims()` now unifies seven claims;
  `scientific_outcomes` carries them under "quantum_thoughts".
  The preregistration non-claims keep their original wording
  and gain an interference/cascade scoping entry.
- Tests: 108 -> 122, all passing.

## 0.2.0 (2026-11-15)

Quantum thoughts: three new modules, four new claims, all passing.

- `thought_entanglement.py` — concurrence (Wootters, exact) and
  reduced-state entropy for a two-thought Bell state. Claim (i)
  PASSES: concurrence 0.9998 at noise sigma = 0.01 (spooky 0.9998
  on the same copies); depolarizing concurrence reproduces
  max(0, 1 - 3p/2) exactly and dies at p = 2/3; reduced entropy
  stays 1 bit throughout (it cannot see the death). Spooky first
  falls below 0.9 at sigma = 0.25 while mean concurrence never
  falls below 0.6520 under vector noise: spooky and concurrence
  part ways, which is why spooky was never entanglement.
- `thought.py` — a thought as a superposition over four basis
  concepts. Claim (ii) PASSES: coherence half-life measured
  14 / 7 / 3 / 1 steps at p = 0.05 / 0.1 / 0.25 / 0.5 against
  analytic 13.51 / 6.58 / 2.41 / 1.00. Claim (iii) PASSES:
  fully dephased uniform thought has entropy 2 bits, a collapsed
  thought 0; decision entropy 2 bits before collapse, 0 after;
  attention bias +0.018739 at delta = +0.05, -0.018738 at -0.05.
- `self_knowing.py` — D = <psi|P|psi>, the self-determinism
  factor vendored from the symmetry-entropy package (own
  implementation, provenance cited). Claim (iv) PASSES: exact
  values D = 1 (stored), 1/3 (non-stored basis), 0 (kernel),
  1/2 (maximally mixed); Spearman(sigma, D) = -1.0;
  Spearman(D, coherence) = 0.9643. Surprise, measured: D
  ANTI-tracks concurrence (Pearson -0.9570), because the noise
  that destroys self-knowing creates entanglement in a product
  thought.
- `bridge.quantum_thought_claims()` unifies the four claims;
  `scientific_outcomes` carries them under "quantum_thoughts".
  The claims registry now distinguishes entanglement measured
  in the model (True) from physical entanglement in hardware
  (still False). The preregistration non-claims keep their
  original wording and gain a scoping entry.
- Copyright line added to `bridge.py`, `scientific_outcomes.py`,
  `synergy.py` (they were missing it).
- Tests: 80 -> 108, all passing.

## 0.1.0 (2026-11-14)

Initial release: attunement A(delta) = U * (1 + delta) - C with
spooky unity, entropy cost, observer/calibrator, mapping status,
maximum-scientific-outcomes framework, and the synergy expansion
(added by Jean in 7 commits on 2026-11-15, with the synergy
robustness analysis). 80 tests.
