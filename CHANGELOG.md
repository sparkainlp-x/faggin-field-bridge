# Changelog — Faggin Field Bridge

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
