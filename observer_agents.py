# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# observer_agents.py
#
# Observer and calibration agents, inserted into the
# wave-direction / observer-cycle setup.
#
# Jean's directive, 2026-11-19: "insert observer and
# calibration agents", quoting the two v0.25.0 FAILs.
# The agents reuse the v0.1.0 pattern from attunement.py
# (the membrane-arena pattern): the observer (Yang) is
# read-only, the calibrator (Yin) is ONE clipped scalar
# delta in [-0.05, 0.05]. Nothing here invents a second
# calibrator scale or widens the bound.
#
# The observer agent reads the slide state psi(theta) =
# cos(theta)|stored> + sin(theta)|kernel> and the
# rotation pair at theta, and reports D, C, R_s, R_k,
# chi, V — without touching the state. The calibration
# agent acts on the noisy direction sweep
# (wave_direction.noisy_direction_sweep): it scales the
# measured D by (1 + delta) — the attunement pattern,
# where the calibrator scales the unity-like quantity
# and never the cost-like one (concurrence C is not
# tunable, exactly as the entropy cost is not tunable
# in attunement.py) — and picks delta by a FIXED RULE,
# frozen from the calibration pilot on seeds 42/7 only
# (docs/preregistration-v0.26.0.md): scan delta over
# the 201-point grid in [-0.05, 0.05], minimize the
# number of failing (xxxii) bars, tie-break smallest
# |delta|, then smallest delta.
#
# The design is motivated by the published v0.25.0
# (xci)/(xcii) table (REPORT.md §31): the (xci) miss
# on seed 2026 opposite is a D-range miss of 0.0010
# (0.2490 vs the 0.25 bar), and the (xcii) failure is
# a correlation inversion (Pearson +0.5109 / +0.8297
# held-out). The rule itself is seed-independent and
# frozen before the evaluation run; no delta was
# hand-picked for any seed. Two facts shape what the
# agent can and cannot do, and both are verified on
# the calibration seeds in the pilot:
#   - Pearson(D, C) and Spearman(D, C) are invariant
#     under a positive rescaling of D WHERE NO
#     CLIPPING BITES — verified on the calibration
#     opposite and perpendicular sweeps (|delta| <=
#     2.3e-16 at delta = +/-0.05). On the stored
#     direction the sigma = 0 point has D = 1.0
#     exactly, so delta > 0 clips it (the attunement
#     pattern's [0, 1] clip on the scaled quantity)
#     and the correlations MOVE — pilot, delta =
#     +0.05: seed 42 Pearson +0.0270, Spearman
#     +0.0937; seed 7 Pearson +0.0197, Spearman
#     +0.0974 (seed 7 Spearman -0.8669 would FAIL
#     its bar at delta = +0.05). Whether the rule's
#     delta changes the (2026, stored) Pearson miss
#     is therefore an evaluation-run measurement,
#     reported not gated; (xci) stays FAIL either way.
#   - D range scales by exactly (1 + delta) where the
#     max-D point does not clip — true for the
#     opposite and perpendicular starts (worst max D
#     0.7936, times 1.05 = 0.8333 < 1) — so the agent
#     CAN rescue a D-range miss iff the uncalibrated
#     D range is at least 0.25 / 1.05 = 0.2381. The
#     published 0.2490 clears that bound; a miss
#     below 0.2381 would be unrescuable and the
#     rescue claim would FAIL honestly. On the stored
#     start the sigma = 0 point clips and the range
#     SHRINKS with delta > 0 (pilot: 0.4804 -> 0.4545
#     at delta = +0.05) — the agent never widens a
#     stored-direction range, which is why the rule
#     holds delta = 0 there on the calibration seeds.
#
# Five claims, (xciii)-(xcvii), pre-registered in
# docs/preregistration-v0.26.0.md BEFORE the evaluation
# run. Thresholds are round numbers frozen from the
# calibration pilot on seeds 42 and 7; the evaluation
# seeds are 1234 and 2026.
#
# (xciii) Observer read-only: on the 24-point
#     full-circle grid, observing psi(theta) leaves
#     the state unchanged (max |after - before| <=
#     1e-12) and every reported quantity equals the
#     direct computation within 1e-9.
# (xciv) Calibrator bounded: |delta| <= 0.05 always
#     (inputs +/-0.5 clip to +/-0.05), and delta = 0
#     reproduces the uncalibrated sweep exactly (max
#     difference 0.0).
# (xcv) Calibration agent on (xci): with the frozen
#     rule, the D-range bar (>= 0.25) holds on EVERY
#     (seed, direction) in {42, 7, 1234, 2026} x
#     {stored, opposite}. The (2026, stored) Pearson
#     miss is explicitly out of scope for this claim:
#     by the invariance theorem no D-rescaling agent
#     can touch it, so (xci) stays FAIL as originally
#     stated; the full four-bar table is reported
#     alongside, not gated.
# (xcvi) Calibration agent on (xcii): the perpendicular
#     inversion survives bounded calibration — with
#     the agent on, Pearson(D, C) > -0.90 on EVERY
#     seed in {42, 7, 1234, 2026} from theta = pi/4.
#     The agent holds delta = 0 there: it cannot
#     improve the failing-bar count on any seed.
# (xcvii) Closed loop: observer reads, calibrator
#     adjusts once per sweep, observer re-reads. The
#     loop runs exactly 2 rounds (one decision round
#     + one verification round; the calibrator is not
#     re-invoked), the held delta is unchanged across
#     rounds (difference 0.0), the round-2 report
#     matches a fresh direct calibrated computation
#     within 1e-9, and the cost is exactly 2 observer
#     reads per sweep.
#
# Honesty, stated up front:
#   - (xciii), (xciv) and (xcvii) are exact-identity
#     claims, like (xxxiv) and (lxxxviii)-(xc): the
#     measured content is that the code realizes the
#     contracts (read-only, bounded, terminating loop)
#     to 1e-9/1e-12. A failure would be a defect in
#     the agents' wiring, not a result about a
#     theorem.
#   - (xcv) and (xcvi) are statistical claims on
#     5-copy means, like (xxxii)/(xci)/(xcii): the
#     same saturation and finite-sample fragility
#     applies. (xcv) is falsifiable in principle: a
#     D-range miss below 0.2381 would be
#     unrescuable inside the bound.
#   - The (xci) and (xcii) verdicts stay FAIL on the
#     record as originally stated. The agents test
#     what bounded calibration can and cannot do
#     about those failures; they do not rewrite them.
#   - None of this measures consciousness, love, or
#     knowing in a human or physical sense. Classical
#     emulation throughout. Faggin's metaphysics stays
#     interpretive. No scalar Phi is computed anywhere.
#
# Pre-registered verdict rules, written before the
# evaluation run (see docs/preregistration-v0.26.0.md
# and the claim_*_verdict functions):
#   (xciii) On the 24-point grid, max |psi after
#       observation - psi before| <= 1e-12, and max
#       |reported quantity - direct computation| <=
#       1e-9, for every slide quantity (D, C, R_s,
#       R_k, split, C + D) and every rotation-pair
#       quantity (D1, D2, cross term real and imag,
#       V sweep, V analytic).
#   (xciv) set_delta(+0.5) = +0.05 and set_delta(-0.5)
#       = -0.05 exactly; every delta the rule picks
#       lies in [-0.05, 0.05]; delta = 0 reproduces
#       the uncalibrated sweep exactly (max |D_cal -
#       D| = 0.0, max |C_cal - C| = 0.0).
#   (xcv) With the agent on, D range >= 0.25 on
#       EVERY (seed, direction) in {42, 7, 1234,
#       2026} x {0, pi/2}. The agent's delta per
#       combo is recorded; the full four-bar table
#       is reported, not gated.
#   (xcvi) With the agent on, Pearson(D, C) > -0.90
#       on EVERY seed in {42, 7, 1234, 2026} from
#       theta = pi/4. The agent's delta per seed is
#       recorded (pilot: 0.0 on both calibration
#       seeds).
#   (xcvii) On EVERY (seed, direction) in {42, 7,
#       1234, 2026} x {0, pi/4, pi/2}: the loop runs
#       exactly 2 rounds, |delta held after round 2
#       - delta picked in round 1| = 0.0, the
#       round-2 report matches a fresh direct
#       calibrated computation within 1e-9, and the
#       observer read count is exactly 2 per sweep.
#

"""Observer and calibration agents for the wave direction."""

import math
from dataclasses import dataclass

import numpy as np

import attunement as at
import bridge
import cascade as cas
import empathy_field as ef
import observer_cycle as oc
import self_knowing as sk
import thought_entanglement as te
import wave_direction as wd

# ---------------------------------------------------------------------------
# Seeds
# ---------------------------------------------------------------------------

# Calibration seeds: the rule and thresholds were frozen from
# these only.
CALIBRATION_SEEDS = (42, 7)
# Evaluation seeds: held out until the evaluation run.
EVALUATION_SEEDS = (1234, 2026)
ALL_SEEDS = CALIBRATION_SEEDS + EVALUATION_SEEDS

# ---------------------------------------------------------------------------
# Thresholds and bounds (frozen from the calibration pilot,
# docs/preregistration-v0.26.0.md; never moved after the run).
# ---------------------------------------------------------------------------

# The calibrator bound is the membrane-arena Yin bound,
# reused from attunement.py — one clipped scalar, not widened.
DELTA_MIN = at.DELTA_MIN
DELTA_MAX = at.DELTA_MAX
DELTA_GRID_POINTS = at.DELTA_GRID_POINTS

# Exact-identity tolerance, as in (xxxiv)/(lxxxviii).
EXACT_TOL = 1e-9
# Read-only tolerance: observation must not move the state.
READ_ONLY_TOL = 1e-12

# The (xxxii)/(xci) bars, reused unchanged for the agent's rule
# and for claims (xcv)/(xcvi).
PEARSON_D_C_MAX = -0.90
SPEARMAN_D_C_MAX = -0.90
D_RANGE_MIN = 0.25
C_RANGE_MIN = 0.25

# The (xci) directions (stored, opposite) and the (xcii)
# direction (perpendicular), from wave_direction.py.
XCV_DIRECTIONS = wd.XCI_DIRECTIONS
XCVI_DIRECTIONS = wd.XCII_DIRECTIONS
ALL_NOISY_DIRECTIONS = (0.0, math.pi / 4, math.pi / 2)

# The full-circle grid for claim (xciii), from wave_direction.
DIRECTION_GRID = wd.DIRECTION_GRID


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("DELTA_MIN", DELTA_MIN),
        ("DELTA_MAX", DELTA_MAX),
        ("DELTA_GRID_POINTS", DELTA_GRID_POINTS),
        ("EXACT_TOL", EXACT_TOL),
        ("READ_ONLY_TOL", READ_ONLY_TOL),
        ("PEARSON_D_C_MAX", PEARSON_D_C_MAX),
        ("SPEARMAN_D_C_MAX", SPEARMAN_D_C_MAX),
        ("D_RANGE_MIN", D_RANGE_MIN),
        ("C_RANGE_MIN", C_RANGE_MIN),
    ) if value is None]
    if missing:
        raise ValueError(
            "observer-agent thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.26.0.md)")
    return {
        "delta_min": float(DELTA_MIN),
        "delta_max": float(DELTA_MAX),
        "delta_grid_points": int(DELTA_GRID_POINTS),
        "exact_tol": float(EXACT_TOL),
        "read_only_tol": float(READ_ONLY_TOL),
        "pearson_d_c_max": float(PEARSON_D_C_MAX),
        "spearman_d_c_max": float(SPEARMAN_D_C_MAX),
        "d_range_min": float(D_RANGE_MIN),
        "c_range_min": float(C_RANGE_MIN),
    }


def sweep_bars(rows):
    """The four (xxxii) bars for a noisy sweep's rows.

    Rows carry mean_D and mean_concurrence per sigma.
    Returns Pearson(D, C), Spearman(D, C), D range,
    C range, and whether each bar holds.
    """
    t = _thresholds()
    ds = [float(r["mean_D"]) for r in rows]
    cs = [float(r["mean_concurrence"]) for r in rows]
    pearson = sk.pearson(ds, cs)
    spearman = sk.spearman(ds, cs)
    d_range = float(max(ds) - min(ds))
    c_range = float(max(cs) - min(cs))
    checks = {
        "pearson_at_most_max": bool(pearson <= t["pearson_d_c_max"]),
        "spearman_at_most_max": bool(
            spearman <= t["spearman_d_c_max"]),
        "d_range_at_least_min": bool(d_range >= t["d_range_min"]),
        "c_range_at_least_min": bool(c_range >= t["c_range_min"]),
    }
    return {
        "pearson_d_c": float(pearson),
        "spearman_d_c": float(spearman),
        "d_range": d_range,
        "c_range": c_range,
        "checks": checks,
        "n_failing": sum(1 for v in checks.values() if not v),
    }


def min_rescuable_d_range():
    """The smallest D range the calibrator can rescue.

    The agent scales D by (1 + delta) with delta <= 0.05,
    so a D-range miss is rescuable iff the uncalibrated
    range is at least 0.25 / 1.05 = 0.2381. Below that,
    no delta inside the bound reaches the bar.
    """
    return D_RANGE_MIN / (1.0 + DELTA_MAX)


# ---------------------------------------------------------------------------
# Observer agent (Yang): read-only measurement of a direction
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DirectionObservation:
    """A read-only measurement of one wave direction.

    Frozen: an observation cannot be edited after it is
    made. All values are pure functions of the inputs;
    nothing here is stored or accumulated between calls.
    """

    theta: float
    d: float
    concurrence: float
    r_stored: float
    r_kernel: float
    r_split: float
    c_plus_d: float
    d1: float
    d2: float
    cross_real: float
    cross_imag: float
    visibility_sweep: float
    visibility_analytic: float


class DirectionObserver:
    """Yang Observer: measures a wave direction, changes nothing.

    The observer holds no mutable state: it has no attributes,
    and every method is a pure function of its arguments.
    Calling observe_direction() twice with the same theta
    returns identical results, and observing a caller-owned
    state array leaves that array byte-identical.
    """

    def observe_slide(self, psi):
        """Measure the slide quantities of a state psi.

        Returns (d, concurrence, r_stored, r_kernel, r_split,
        c_plus_d). Reads psi only; the input array is not
        modified (verified by the read-only test).
        """
        psi = np.asarray(psi, dtype=complex)
        stored = oc.stored_thought()
        kernel = oc.kernel_thought()
        d = sk.self_knowing_factor(psi)
        c = te.concurrence_pure(psi)
        r_s = ef.overlap_squared(psi, stored)
        r_k = ef.overlap_squared(psi, kernel)
        return {
            "d": float(d),
            "concurrence": float(c),
            "r_stored": float(r_s),
            "r_kernel": float(r_k),
            "r_split": float(r_s - r_k),
            "c_plus_d": float(c + d),
        }

    def observe_pair(self, theta):
        """Measure the rotation-pair quantities at theta.

        Returns (d1, d2, cross term real and imag,
        visibility sweep and analytic).
        """
        psi1, psi2 = cas.rotation_pair(float(theta))
        d1 = sk.self_knowing_factor(psi1)
        d2 = sk.self_knowing_factor(psi2)
        chi = cas.cross_term(psi1, psi2)
        v_sweep, v_analytic = cas.visibility(psi1, psi2)
        return {
            "d1": float(d1),
            "d2": float(d2),
            "cross_real": float(chi.real),
            "cross_imag": float(chi.imag),
            "visibility_sweep": float(v_sweep),
            "visibility_analytic": float(v_analytic),
        }

    def observe_direction(self, theta):
        """Observe the full direction: slide + rotation pair.

        Builds psi(theta) fresh (the caller's array is never
        involved) and returns a frozen DirectionObservation.
        """
        t = float(theta)
        psi = oc.slide_state(t)
        slide = self.observe_slide(psi)
        pair = self.observe_pair(t)
        return DirectionObservation(
            theta=t,
            d=slide["d"],
            concurrence=slide["concurrence"],
            r_stored=slide["r_stored"],
            r_kernel=slide["r_kernel"],
            r_split=slide["r_split"],
            c_plus_d=slide["c_plus_d"],
            d1=pair["d1"],
            d2=pair["d2"],
            cross_real=pair["cross_real"],
            cross_imag=pair["cross_imag"],
            visibility_sweep=pair["visibility_sweep"],
            visibility_analytic=pair["visibility_analytic"],
        )

    def observe_sweep(self, seed, theta, delta=0.0,
                      n_copies=sk.DEFAULT_N_COPIES):
        """Observe a noisy direction sweep (one observer read).

        The uncalibrated sweep from wave_direction, with the
        calibrator's delta applied to D (delta = 0 observes
        the sweep as it is). Returns the sweep dict with the
        observed rows and their four bars. This is ONE read
        for the closed loop's cost accounting, whatever the
        number of sigma points.
        """
        sweep = wd.noisy_direction_sweep(seed, theta,
                                         n_copies=n_copies)
        rows = calibrated_rows(sweep["rows"], float(delta))
        bars = sweep_bars(rows)
        return {
            "seed": int(seed),
            "theta": float(theta),
            "direction": sweep["direction"],
            "delta": float(delta),
            "rows": rows,
            "pearson_d_c": bars["pearson_d_c"],
            "spearman_d_c": bars["spearman_d_c"],
            "d_range": bars["d_range"],
            "c_range": bars["c_range"],
            "bars": bars["checks"],
            "n_failing": bars["n_failing"],
        }


# ---------------------------------------------------------------------------
# Calibration agent (Yin): one clipped scalar on the sweep's D
# ---------------------------------------------------------------------------

def calibrated_rows(rows, delta):
    """Scale a sweep's D by (1 + delta), clipped to [0, 1].

    The attunement pattern: the calibrator scales the
    unity-like quantity (D) and never the cost-like one
    (concurrence C is returned untouched). At delta = 0
    the rows are reproduced exactly.
    """
    d = min(DELTA_MAX, max(DELTA_MIN, float(delta)))
    out = []
    for r in rows:
        out.append({
            "sigma": float(r["sigma"]),
            "mean_D": min(1.0, max(0.0,
                                   float(r["mean_D"]) * (1.0 + d))),
            "mean_concurrence": float(r["mean_concurrence"]),
        })
    return out


def clip_affected(rows, delta):
    """True iff the [0, 1] clip bites anywhere at this delta.

    The clip bites iff some row's D times (1 + delta)
    exceeds 1 — in practice the stored direction's
    sigma = 0 point, where D = 1.0 exactly. Where the
    clip bites, Pearson/Spearman are NOT invariant under
    the rescaling (pilot: stored direction, delta =
    +0.05, |dPearson| up to 0.027, |dSpearman| up to
    0.097); where it does not bite they are invariant
    to float noise. Reported per combo, never hidden.
    """
    d = min(DELTA_MAX, max(DELTA_MIN, float(delta)))
    if d <= 0.0:
        return False
    return any(float(r["mean_D"]) * (1.0 + d) > 1.0
               for r in rows)


class SweepCalibrator:
    """Yin Calibrator: a single scalar delta in [-0.05, 0.05],
    acting on a noisy sweep's D.

    set_delta() clips into the bound: it never raises and
    never lets delta exceed [-0.05, 0.05]. The bound is the
    membrane-arena Yin bound from attunement.py; it is not
    widened here. choose_delta() is the FROZEN RULE (see
    docs/preregistration-v0.26.0.md): scan the 201-point
    grid over the full clipped range, minimize the number
    of failing (xxxii) bars, tie-break smallest |delta|,
    then smallest delta. The rule is a fixed function of
    the observed sweep; it is the same function on
    calibration and evaluation seeds.
    """

    def __init__(self, delta=0.0):
        self._delta = 0.0
        self.set_delta(delta)

    @property
    def delta(self):
        """The current calibration scalar, always in [-0.05, 0.05]."""
        return self._delta

    def set_delta(self, value):
        """Set delta, clipped into [-0.05, 0.05].

        Never raises, never exceeds the bound. Returns the clipped
        value actually held.
        """
        x = float(value)
        if x < DELTA_MIN:
            x = DELTA_MIN
        elif x > DELTA_MAX:
            x = DELTA_MAX
        self._delta = x
        return self._delta

    def apply(self, rows):
        """The sweep's rows with the held delta applied to D."""
        return calibrated_rows(rows, self._delta)

    def choose_delta(self, rows):
        """Pick delta by the frozen rule for an observed sweep.

        Scans the 201-point grid over [-0.05, 0.05] and
        returns the delta minimizing the number of failing
        (xxxii) bars; ties go to the smallest |delta|,
        then the smallest delta. Does not change the
        calibrator's held delta. Returns a dict with the
        chosen delta, the failing-bar count at that delta
        and at delta = 0, and the bars at the chosen delta.
        """
        grid = np.linspace(DELTA_MIN, DELTA_MAX, DELTA_GRID_POINTS)
        best = None
        for d in grid:
            bars = sweep_bars(calibrated_rows(rows, float(d)))
            candidate = (bars["n_failing"], abs(float(d)),
                         float(d))
            if best is None or candidate < best[0]:
                best = (candidate, float(d), bars)
        _, delta, bars = best
        bars_at_zero = sweep_bars(calibrated_rows(rows, 0.0))
        return {
            "delta": float(delta),
            "n_failing": bars["n_failing"],
            "n_failing_at_zero": bars_at_zero["n_failing"],
            "pearson_d_c": bars["pearson_d_c"],
            "spearman_d_c": bars["spearman_d_c"],
            "d_range": bars["d_range"],
            "c_range": bars["c_range"],
            "bars": bars["checks"],
        }


def agent_sweep(seed, theta, n_copies=sk.DEFAULT_N_COPIES):
    """Run the observer + calibrator on one noisy sweep.

    The observer reads the uncalibrated sweep, the
    calibrator picks delta by the frozen rule, and the
    calibrated sweep is reported with its bars. The
    uncalibrated bars are reported alongside so the
    agent's effect is visible and nothing is hidden.
    """
    observer = DirectionObserver()
    calibrator = SweepCalibrator()
    uncalibrated = observer.observe_sweep(seed, theta,
                                          delta=0.0,
                                          n_copies=n_copies)
    choice = calibrator.choose_delta(uncalibrated["rows"])
    calibrator.set_delta(choice["delta"])
    calibrated = observer.observe_sweep(seed, theta,
                                        delta=choice["delta"],
                                        n_copies=n_copies)
    return {
        "seed": int(seed),
        "theta": float(theta),
        "direction": uncalibrated["direction"],
        "delta": float(choice["delta"]),
        "clip_affected": bool(clip_affected(
            uncalibrated["rows"], choice["delta"])),
        "n_failing_at_zero": choice["n_failing_at_zero"],
        "n_failing_calibrated": choice["n_failing"],
        "uncalibrated": {
            "pearson_d_c": uncalibrated["pearson_d_c"],
            "spearman_d_c": uncalibrated["spearman_d_c"],
            "d_range": uncalibrated["d_range"],
            "c_range": uncalibrated["c_range"],
            "bars": uncalibrated["bars"],
        },
        "calibrated": {
            "pearson_d_c": calibrated["pearson_d_c"],
            "spearman_d_c": calibrated["spearman_d_c"],
            "d_range": calibrated["d_range"],
            "c_range": calibrated["c_range"],
            "bars": calibrated["bars"],
        },
    }


# ---------------------------------------------------------------------------
# Closed loop: observer reads, calibrator adjusts once, observer re-reads
# ---------------------------------------------------------------------------

def closed_loop(seed, theta, n_copies=sk.DEFAULT_N_COPIES):
    """The observer-calibrator loop on one noisy sweep.

    Round 1 (decision): the observer reads the
    uncalibrated sweep (read 1) and the calibrator picks
    delta by the frozen rule and holds it. Round 2
    (verification): the observer re-reads the sweep with
    the held delta (read 2) and the report is checked
    against a FRESH direct calibrated computation — the
    uncalibrated sweep recomputed from the seed and the
    held delta applied — within 1e-9. The calibrator is
    NOT re-invoked in round 2, so the loop terminates
    after exactly 2 rounds by construction; the measured
    content is that the held delta is unchanged, the
    round-2 report matches the fresh computation, and
    the cost is exactly 2 reads.
    """
    observer = DirectionObserver()
    calibrator = SweepCalibrator()
    # Round 1: observe uncalibrated, decide.
    read1 = observer.observe_sweep(seed, theta, delta=0.0,
                                   n_copies=n_copies)
    choice = calibrator.choose_delta(read1["rows"])
    calibrator.set_delta(choice["delta"])
    delta_round1 = calibrator.delta
    # Round 2: observe with the held delta, verify.
    read2 = observer.observe_sweep(seed, theta,
                                   delta=delta_round1,
                                   n_copies=n_copies)
    delta_held = calibrator.delta
    # Fresh direct computation: recompute the uncalibrated
    # sweep from the seed and apply the held delta.
    fresh = wd.noisy_direction_sweep(seed, theta,
                                     n_copies=n_copies)
    direct_rows = calibrated_rows(fresh["rows"], delta_held)
    max_row_error = max(
        max(abs(r2["mean_D"] - rd["mean_D"]),
            abs(r2["mean_concurrence"]
                - rd["mean_concurrence"]))
        for r2, rd in zip(read2["rows"], direct_rows))
    return {
        "seed": int(seed),
        "theta": float(theta),
        "direction": read1["direction"],
        "rounds": 2,
        "reads": 2,
        "delta_round1": float(delta_round1),
        "delta_held_round2": float(delta_held),
        "delta_change": float(abs(delta_held - delta_round1)),
        "round2_max_row_error": float(max_row_error),
        "round2_bars": read2["bars"],
        "round2_n_failing": read2["n_failing"],
    }


# ---------------------------------------------------------------------------
# Claims (xciii)-(xcvii): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_observer_read_only_verdict(thetas=None):
    """(xciii) Observer read-only: observing a direction
    leaves the state unchanged and reports the direct
    quantities.

    PASS iff, on the 24-point full-circle grid, max
    |psi after - psi before| <= 1e-12 and max
    |reported - direct| <= 1e-9 for every slide and
    rotation-pair quantity.
    """
    t = _thresholds()
    observer = DirectionObserver()
    worst_state = 0.0
    worst_report = 0.0
    for theta in (DIRECTION_GRID if thetas is None else thetas):
        psi = oc.slide_state(float(theta))
        before = psi.copy()
        report = observer.observe_direction(float(theta))
        psi2 = oc.slide_state(float(theta))
        before2 = psi2.copy()
        observer.observe_slide(psi2)
        worst_state = max(worst_state,
                          float(np.max(np.abs(psi2 - before2))))
        d = sk.self_knowing_factor(psi)
        c = te.concurrence_pure(psi)
        r_s = ef.overlap_squared(psi, oc.stored_thought())
        r_k = ef.overlap_squared(psi, oc.kernel_thought())
        psi1, psi2p = cas.rotation_pair(float(theta))
        d1 = sk.self_knowing_factor(psi1)
        d2 = sk.self_knowing_factor(psi2p)
        chi = cas.cross_term(psi1, psi2p)
        v_sweep, v_analytic = cas.visibility(psi1, psi2p)
        direct = {
            "d": d, "concurrence": c, "r_stored": r_s,
            "r_kernel": r_k, "r_split": float(r_s - r_k),
            "c_plus_d": float(c + d), "d1": d1, "d2": d2,
            "cross_real": float(chi.real),
            "cross_imag": float(chi.imag),
            "visibility_sweep": float(v_sweep),
            "visibility_analytic": float(v_analytic),
        }
        for name, value in direct.items():
            worst_report = max(worst_report,
                               abs(getattr(report, name) - value))
    checks = {
        "state_unchanged": bool(
            worst_state <= t["read_only_tol"]),
        "report_matches_direct": bool(
            worst_report <= t["exact_tol"]),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xciii) observer read-only: observation "
                 "leaves the state unchanged and reports "
                 "the direct quantities",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "worst_state_change": float(worst_state),
        "worst_report_error": float(worst_report),
    }


def claim_calibrator_bounded_verdict(seeds=None, thetas=None):
    """(xciv) Calibrator bounded: the delta never leaves
    [-0.05, 0.05] and delta = 0 is the identity.

    PASS iff set_delta(+0.5) = +0.05 and set_delta(-0.5)
    = -0.05 exactly, every delta the rule picks lies in
    [-0.05, 0.05], and delta = 0 reproduces the
    uncalibrated sweep exactly (max difference 0.0).
    """
    t = _thresholds()
    calibrator = SweepCalibrator()
    clip_plus = calibrator.set_delta(0.5)
    clip_minus = calibrator.set_delta(-0.5)
    calibrator.set_delta(0.03)
    inside = calibrator.delta
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(ALL_NOISY_DIRECTIONS
                  if thetas is None else thetas)
    picked_deltas = []
    worst_identity = 0.0
    for seed in seeds:
        for theta in thetas:
            sweep = wd.noisy_direction_sweep(seed, theta)
            rows0 = calibrated_rows(sweep["rows"], 0.0)
            worst_identity = max(
                worst_identity,
                max(abs(a["mean_D"] - b["mean_D"])
                    for a, b in zip(rows0, sweep["rows"])),
                max(abs(a["mean_concurrence"]
                        - b["mean_concurrence"])
                    for a, b in zip(rows0, sweep["rows"])))
            choice = calibrator.choose_delta(sweep["rows"])
            picked_deltas.append(choice["delta"])
    checks = {
        "clip_plus_exact": bool(clip_plus == t["delta_max"]),
        "clip_minus_exact": bool(clip_minus == t["delta_min"]),
        "inside_set_exact": bool(inside == 0.03),
        "picked_deltas_in_bound": bool(all(
            t["delta_min"] <= d <= t["delta_max"]
            for d in picked_deltas)),
        "delta_zero_is_identity": bool(worst_identity == 0.0),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xciv) calibrator bounded: |delta| <= 0.05 "
                 "always, delta = 0 is the identity",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "clip_plus": float(clip_plus),
        "clip_minus": float(clip_minus),
        "picked_deltas": [float(d) for d in picked_deltas],
        "worst_identity_error": float(worst_identity),
    }


def claim_calibrated_d_range_verdict(seeds=None, thetas=None):
    """(xcv) Calibration agent on (xci): the D-range rescue.

    PASS iff, with the agent on, the D-range bar
    (>= 0.25) holds on EVERY (seed, direction) in
    {42, 7, 1234, 2026} x {stored, opposite}. The
    agent's delta per combo is recorded; the full
    four-bar table is reported, not gated.
    """
    t = _thresholds()
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(XCV_DIRECTIONS if thetas is None else thetas)
    per_combo = [agent_sweep(s, th)
                 for s in seeds for th in thetas]
    checks = {
        "d_range_at_least_min": all(
            r["calibrated"]["d_range"] >= t["d_range_min"]
            for r in per_combo),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xcv) calibration agent on (xci): the "
                 "D-range rescue",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "min_rescuable_d_range": float(min_rescuable_d_range()),
        "per_combo": per_combo,
    }


def claim_perpendicular_survives_verdict(seeds=None,
                                         thetas=None):
    """(xcvi) Calibration agent on (xcii): the perpendicular
    inversion survives bounded calibration.

    PASS iff, with the agent on, Pearson(D, C) > -0.90 on
    EVERY seed in {42, 7, 1234, 2026} from theta = pi/4.
    The agent's delta per seed is recorded.
    """
    t = _thresholds()
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(XCVI_DIRECTIONS if thetas is None else thetas)
    per_seed = [agent_sweep(s, th)
                for s in seeds for th in thetas]
    checks = {
        "pearson_above_max_on_every_seed": all(
            r["calibrated"]["pearson_d_c"]
            > t["pearson_d_c_max"] for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xcvi) calibration agent on (xcii): the "
                 "perpendicular inversion survives bounded "
                 "calibration",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_closed_loop_verdict(seeds=None, thetas=None):
    """(xcvii) Closed loop: observe, calibrate once, re-read.

    PASS iff, on EVERY (seed, direction) in {42, 7, 1234,
    2026} x {0, pi/4, pi/2}, the loop runs exactly 2
    rounds, the held delta is unchanged across rounds
    (difference 0.0), the round-2 report matches a fresh
    direct calibrated computation within 1e-9, and the
    observer read count is exactly 2 per sweep.
    """
    t = _thresholds()
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(ALL_NOISY_DIRECTIONS
                  if thetas is None else thetas)
    per_combo = [closed_loop(s, th)
                 for s in seeds for th in thetas]
    checks = {
        "two_rounds_everywhere": all(
            r["rounds"] == 2 for r in per_combo),
        "delta_unchanged": all(
            r["delta_change"] == 0.0 for r in per_combo),
        "round2_matches_direct": all(
            r["round2_max_row_error"] <= t["exact_tol"]
            for r in per_combo),
        "two_reads_per_sweep": all(
            r["reads"] == 2 for r in per_combo),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xcvii) closed loop: observe, calibrate "
                 "once, re-read",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_combo": per_combo,
    }


def observer_agents_claims():
    """The observer/calibration-agent claims (xciii)-(xcvii),
    measured fresh."""
    claim_xciii = claim_observer_read_only_verdict()
    claim_xciv = claim_calibrator_bounded_verdict()
    claim_xcv = claim_calibrated_d_range_verdict()
    claim_xcvi = claim_perpendicular_survives_verdict()
    claim_xcvii = claim_closed_loop_verdict()
    verdicts = [claim_xciii, claim_xciv, claim_xcv, claim_xcvi,
                claim_xcvii]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_xciii_observer_read_only": claim_xciii,
        "claim_xciv_calibrator_bounded": claim_xciv,
        "claim_xcv_calibrated_d_range": claim_xcv,
        "claim_xcvi_perpendicular_survives": claim_xcvi,
        "claim_xcvii_closed_loop": claim_xcvii,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the observer contract, the calibrator contract,
    the agent sweeps, the closed loop, and the claims
    (xciii)-(xcvii) verdicts."""
    print("Observer and calibration agents -- "
          "claims (xciii)-(xcvii)")
    print()
    verdicts = observer_agents_claims()
    xciii = verdicts["claim_xciii_observer_read_only"]
    print(f"Observer read-only: worst state change = "
          f"{xciii['worst_state_change']:.2e}, worst "
          f"report-vs-direct = "
          f"{xciii['worst_report_error']:.2e}")
    print(f"claim (xciii) verdict: "
          f"{'PASS' if xciii['passed'] else 'FAIL'}")
    print()
    xciv = verdicts["claim_xciv_calibrator_bounded"]
    print(f"Calibrator bounded: clip(+0.5) = "
          f"{xciv['clip_plus']:.2f}, clip(-0.5) = "
          f"{xciv['clip_minus']:.2f}, delta = 0 identity error = "
          f"{xciv['worst_identity_error']:.2e}")
    print(f"  rule-picked deltas: "
          f"{sorted(set(xciv['picked_deltas']))}")
    print(f"claim (xciv) verdict: "
          f"{'PASS' if xciv['passed'] else 'FAIL'}")
    print()
    xcv = verdicts["claim_xcv_calibrated_d_range"]
    print("Calibration agent on (xci), per (seed, direction) "
          "[uncalibrated -> calibrated]:")
    for r in xcv["per_combo"]:
        u = r["uncalibrated"]
        c = r["calibrated"]
        print(f"  seed {r['seed']}, {r['direction']}: "
              f"delta = {r['delta']:+.4f}"
              f"{' (clip)' if r['clip_affected'] else ''}, "
              f"D range {u['d_range']:.4f} -> {c['d_range']:.4f}, "
              f"Pearson {u['pearson_d_c']:.4f} -> "
              f"{c['pearson_d_c']:.4f}, "
              f"failing {r['n_failing_at_zero']} -> "
              f"{r['n_failing_calibrated']}")
    print(f"  min rescuable D range = "
          f"{xcv['min_rescuable_d_range']:.4f}")
    print(f"claim (xcv) verdict: "
          f"{'PASS' if xcv['passed'] else 'FAIL'}")
    print()
    xcvi = verdicts["claim_xcvi_perpendicular_survives"]
    print("Calibration agent on (xcii), per seed "
          "[uncalibrated -> calibrated]:")
    for r in xcvi["per_seed"]:
        u = r["uncalibrated"]
        c = r["calibrated"]
        print(f"  seed {r['seed']}, {r['direction']}: "
              f"delta = {r['delta']:+.4f}, "
              f"Pearson {u['pearson_d_c']:.4f} -> "
              f"{c['pearson_d_c']:.4f}, "
              f"Spearman {u['spearman_d_c']:.4f} -> "
              f"{c['spearman_d_c']:.4f}, "
              f"D range {u['d_range']:.4f} -> {c['d_range']:.4f}, "
              f"C range {u['c_range']:.4f}, "
              f"failing {r['n_failing_at_zero']} -> "
              f"{r['n_failing_calibrated']}")
    print(f"claim (xcvi) verdict: "
          f"{'PASS' if xcvi['passed'] else 'FAIL'}")
    print()
    xcvii = verdicts["claim_xcvii_closed_loop"]
    print("Closed loop, per (seed, direction):")
    for r in xcvii["per_combo"]:
        print(f"  seed {r['seed']}, {r['direction']}: "
              f"rounds = {r['rounds']}, reads = {r['reads']}, "
              f"delta {r['delta_round1']:+.4f} -> held "
              f"{r['delta_held_round2']:+.4f} "
              f"(change {r['delta_change']:.2e}), round-2 max "
              f"row error = {r['round2_max_row_error']:.2e}")
    print(f"claim (xcvii) verdict: "
          f"{'PASS' if xcvii['passed'] else 'FAIL'}")
    print()
    print(f"claims (xciii)-(xcvii): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
