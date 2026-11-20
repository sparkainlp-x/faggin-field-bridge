# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# symmetry_sweep.py
#
# The symmetry sweep: orbit-averaging the noisy
# direction sweep under sign flips of the noise
# coordinates, to fix the two v0.25.0 FAILs from
# outside the calibrator.
#
# Jean's directive, 2026-11-19: "Symmetry? Explore
# outside the big to fix" — explore outside the
# calibrator (the "big" fix of v0.26.0). The
# exploration (pilots in /tmp, 2026-11-19 ~20:00 EST)
# found the fix for (xci) and proved (xcii)
# unfixable by symmetrization. This module is the
# production re-implementation of the pilot logic;
# the evaluation re-measures the pilot tables
# through this code.
#
# The structural fact, verified in the pilot harness
# (noise-draw reconstruction worst difference 0.0):
# unity.gaussian_copies re-seeds the RNG per sigma,
# so the same 5 noise vectors z1..z5 are reused at
# every sigma, scaled — the sweep traces 5 fixed
# noise directions. Orbit-averaging replaces each
# of the 5 draws by its whole orbit under a group
# acting on the noise coordinates in the
# slide-adapted orthonormal basis:
#   u : stored direction (uniform thought), in P
#   w : the "attention" direction inside P
#   k : kernel direction, orthogonal to P
#   m : the remaining direction, orthogonal to u, w, k
# V4-full is the group of sign flips of (z_u, z_w)
# only — orbit size 4, i.e. 20 copies per sigma from
# the same 5 draws. z_k is NEVER flipped: flipping
# it flattens the opposite D rise — measured, the
# five other groups (Z2-antipodal, V4-plane,
# D4-plane, swap-only, B4) all break the opposite
# D range to 0.2042-0.2317, below the rescuable
# bound 0.2381. Only V4-full preserves the opposite
# D range (0.2490, unchanged from the plain sweep)
# while rescuing the stored Pearson.
#
# The n-copies control is disclosed in full (see
# docs/preregistration-v0.27.0.md): plain copies
# rescue the Pearson too (n=10: -0.9323, n=20:
# -0.9289 on (2026, stored)) — the rescue is
# variance reduction. Symmetry's edge is
# DETERMINISM (the same 5 draws, no new randomness
# — the orbit is a fixed function of the draws
# already used) plus opposite-D-range preservation
# (V4-full holds 0.2490, needing only delta
# +0.0040; n=10 breaks it to 0.2387, needing delta
# +0.0475 at the edge of the bound). n=20 passes
# (xci) 8/8 outright with no calibrator; the claim
# here is that V4-full fixes (xci) from the same 5
# draws, not that no other variance reduction could.
#
# Five claims, (xcviii)-(cii), pre-registered in
# docs/preregistration-v0.27.0.md BEFORE the
# evaluation run. Thresholds are the (xxxii) bars,
# frozen since v0.12.0 and reused unchanged; the
# evaluation seeds are 1234 and 2026 (see the
# blinding note in the preregistration: the group
# selection used the full 4-seed table, so the
# evaluation is a confirmatory re-measurement, not
# a blind held-out test; no bar was fitted to any
# seed).
#
# (xcviii) Orbit estimator exactness: at sigma = 0
#     the V4-full orbit-averaged D and C equal the
#     exact values (cos^2(theta), sin^2(theta))
#     within 1e-12; the orbit average is invariant
#     under relabelling the orbit within 1e-12; the
#     Z2 orbit average equals the theta/theta+pi pair
#     average within 1e-12.
# (xcix) Stored Pearson rescue: V4-full sweep,
#     (2026, stored) Pearson <= -0.90 — the (xxxii)
#     miss removed by orbit-averaging alone.
# (c) (xci) under symmetry + calibration: all 8
#     combos in {42, 7, 1234, 2026} x {stored,
#     opposite} pass all four (xxxii) bars with the
#     V4-full sweep + the frozen v0.26.0 calibrator
#     rule (pilot: 8/8, only delta nonzero is (2026,
#     opposite) +0.0040).
# (ci) Perpendicular stands: the V4-full
#     perpendicular sweep still FAILS the bars on
#     every seed — D range < 0.25 on every seed
#     (pilot: Pearson -0.7256/+0.6364/+0.3704/
#     +0.7481; D range 0.2365/0.0514/0.1141/0.0561).
#     The frozen calibrator rule is applied per seed
#     and reported alongside, not gated.
# (cii) Two failure kinds (diagnostic): Pearson
#     without sigma = 1.0 passes (2026, stored)
#     (pilot -0.9433) and fails every perpendicular
#     (pilot -0.8091/-0.4620/+0.8013/+0.8348) — the
#     stored failure is a saturation-point failure,
#     the perpendicular failure is whole-curve.
#     Dropping sigma = 1.0 is a diagnostic only,
#     never a fix; the bars stay on the full grid.
#
# Honesty, stated up front:
#   - (xcviii) is an exact-identity claim, like
#     (xxxiv) and (lxxxviii)-(xc): the measured
#     content is that the code realizes the orbit
#     estimator exactly. A failure would be a defect
#     in the code, not a result about a theorem.
#   - (xcix)-(cii) are statistical claims on
#     orbit-averaged 5-copy means, like (xxxii)/
#     (xci)/(xcii): the same saturation and
#     finite-sample fragility applies, and a FAIL is
#     a finding about the symmetry sweep, not a
#     defect.
#   - The (xci), (xcii) and (xxxii) verdicts stay
#     FAIL on the record as originally stated. The
#     symmetry sweep tests what orbit-averaging can
#     and cannot do about those failures; it does
#     not rewrite them.
#   - The symmetry-entropy verdict — orbit entropy
#     CANNOT prove reality is a quantum projection —
#     is untouched: only the orbit-averaging
#     mechanism is borrowed, no projection claim is
#     made.
#   - None of this measures consciousness, love, or
#     knowing in a human or physical sense. Classical
#     emulation throughout. Faggin's metaphysics stays
#     interpretive. No scalar Phi is computed anywhere.
#
# Pre-registered verdict rules, written before the
# evaluation run (see docs/preregistration-v0.27.0.md
# and the claim_*_verdict functions):
#   (xcviii) (a) At sigma = 0, |mean D -
#       cos^2(theta)| <= 1e-12 and |mean C -
#       sin^2(theta)| <= 1e-12 on every (seed,
#       direction). (b) Permuting the 4 orbit
#       transforms changes mean D and mean C per
#       sigma by at most 1e-12 on every (seed,
#       direction). (c) |Z2 orbit-averaged mean D/C
#       - theta/theta+pi pair-averaged mean D/C| <=
#       1e-12 per sigma on every (seed, direction).
#   (xcix) V4-full (2026, stored) Pearson <= -0.90.
#   (c) With the V4-full sweep + the frozen
#       calibrator rule, all four bars hold on EVERY
#       (seed, direction) in {42, 7, 1234, 2026} x
#       {0, pi/2}.
#   (ci) On EVERY seed in {42, 7, 1234, 2026} from
#       theta = pi/4, the V4-full sweep has D range
#       < 0.25 AND at least one failing bar.
#   (cii) Pearson without the sigma = 1.0 point:
#       (2026, stored) <= -0.90 AND every
#       perpendicular > -0.90.
#

"""The symmetry sweep: orbit-averaged noisy direction sweeps."""

import itertools
import math

import numpy as np

import bridge
import observer_agents as oa
import observer_cycle as oc
import self_knowing as sk
import thought_entanglement as te
import unity
import wave_direction as wd

# ---------------------------------------------------------------------------
# Seeds
# ---------------------------------------------------------------------------

# Calibration seeds: the frozen expectations come from
# these only (see the blinding note in
# docs/preregistration-v0.27.0.md).
CALIBRATION_SEEDS = (42, 7)
# Evaluation seeds: held out until the evaluation run
# (confirmatory re-measurement — see the blinding note).
EVALUATION_SEEDS = (1234, 2026)
ALL_SEEDS = CALIBRATION_SEEDS + EVALUATION_SEEDS

# ---------------------------------------------------------------------------
# Thresholds (frozen; never moved after the run)
# ---------------------------------------------------------------------------

# Exact-identity tolerance, as in (xxxiv)/(lxxxviii).
EXACT_TOL = 1e-9
# Orbit-estimator tolerance: relabelling / pair-average
# agreement, as in (xcviii).
ORBIT_TOL = 1e-12

# The (xxxii) bars, reused unchanged since v0.12.0.
PEARSON_D_C_MAX = -0.90
SPEARMAN_D_C_MAX = -0.90
D_RANGE_MIN = 0.25
C_RANGE_MIN = 0.25

# The (xci) directions (stored, opposite) and the (xcii)
# direction (perpendicular), from wave_direction.py.
XC_DIRECTIONS = wd.XCI_DIRECTIONS
XCI_DIRECTIONS = wd.XCII_DIRECTIONS
ALL_NOISY_DIRECTIONS = (0.0, math.pi / 4, math.pi / 2)

# The calibrator rule is the frozen v0.26.0 rule, reused
# unchanged (observer_agents.SweepCalibrator).
DELTA_MIN = oa.DELTA_MIN
DELTA_MAX = oa.DELTA_MAX

# The V4-full group: sign flips of (z_u, z_w) only.
GROUP_V4_FULL = "V4-full"
ALL_GROUPS = ("Z2-antipodal", "V4-plane", "D4-plane",
              "swap-only", "B4", "V4-full")


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("EXACT_TOL", EXACT_TOL),
        ("ORBIT_TOL", ORBIT_TOL),
        ("PEARSON_D_C_MAX", PEARSON_D_C_MAX),
        ("SPEARMAN_D_C_MAX", SPEARMAN_D_C_MAX),
        ("D_RANGE_MIN", D_RANGE_MIN),
        ("C_RANGE_MIN", C_RANGE_MIN),
    ) if value is None]
    if missing:
        raise ValueError(
            "symmetry-sweep thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.27.0.md)")
    return {
        "exact_tol": float(EXACT_TOL),
        "orbit_tol": float(ORBIT_TOL),
        "pearson_d_c_max": float(PEARSON_D_C_MAX),
        "spearman_d_c_max": float(SPEARMAN_D_C_MAX),
        "d_range_min": float(D_RANGE_MIN),
        "c_range_min": float(C_RANGE_MIN),
    }


# ---------------------------------------------------------------------------
# Slide-adapted orthonormal basis (u, w, k, m)
# ---------------------------------------------------------------------------

# u : stored direction (uniform thought), in the projector P
# w : the "attention" direction inside P (e0 orthogonalized vs u)
# k : kernel direction, orthogonal to P
# m : the remaining direction, orthogonal to u, w, k
_BASIS_U = np.array([0.5, 0.5, 0.5, 0.5])
_BASIS_W = np.array([0.75, -0.25, -0.25, -0.25]) / math.sqrt(0.75)
_BASIS_K = np.array([0.0, 1.0, -1.0, 0.0]) / math.sqrt(2.0)
_BASIS_M = np.array([0.0, 1.0, 1.0, -2.0]) / math.sqrt(6.0)
# Rows are the basis vectors.
SLIDE_BASIS = np.stack([_BASIS_U, _BASIS_W, _BASIS_K, _BASIS_M])


def basis_orthonormality_error():
    """Worst |G - I| for the slide-adapted basis (0.0 to float noise)."""
    gram = SLIDE_BASIS @ SLIDE_BASIS.T
    return float(np.max(np.abs(gram - np.eye(4))))


def to_coords(z):
    """Noise vector -> (z_u, z_w, z_k, z_m)."""
    return SLIDE_BASIS @ np.asarray(z, dtype=float)


def from_coords(c):
    """(z_u, z_w, z_k, z_m) -> noise vector."""
    return np.asarray(c, dtype=float) @ SLIDE_BASIS


def draw_noise(seed, n_copies=sk.DEFAULT_N_COPIES):
    """The exact standard-normal draws gaussian_copies uses.

    gaussian_copies(state, sigma, n, seed) makes one
    default_rng(seed) and draws standard_normal(4) once
    per copy, in order. This reconstruction is bit-for-bit
    (verified by the pilot harness: worst difference 0.0).
    """
    rng = np.random.default_rng(seed)
    return [rng.standard_normal(4) for _ in range(n_copies)]


# ---------------------------------------------------------------------------
# Groups acting on the noise coordinates
# ---------------------------------------------------------------------------

def _flip(c, idxs):
    c = list(c)
    for i in idxs:
        c[i] = -c[i]
    return tuple(c)


def _swap_uk(c):
    c = list(c)
    c[0], c[2] = c[2], c[0]
    return tuple(c)


def group_transforms(name):
    """The coordinate transforms of a candidate group.

    Z2-antipodal : {I, -I} on all four coords (== the
        opposite-pair average, theta vs theta+pi: D, C
        are invariant under a global sign flip of the
        state, so averaging the theta+pi sweep over the
        same noise IS averaging z vs -z).
    V4-plane     : sign flips of (z_u, z_k) only (4).
    D4-plane     : V4-plane + swap z_u <-> z_k (8).
    swap-only    : {I, swap z_u <-> z_k} (2).
    B4           : all 16 sign flips in (u, w, k, m).
    V4-full      : sign flips of (z_u, z_w) only (4) —
        the group of this build: it touches the
        projector directions but never the kernel.
    """
    if name == "Z2-antipodal":
        return [lambda c: c, lambda c: _flip(c, (0, 1, 2, 3))]
    if name == "V4-plane":
        return [lambda c: c,
                lambda c: _flip(c, (0,)),
                lambda c: _flip(c, (2,)),
                lambda c: _flip(c, (0, 2))]
    if name == "D4-plane":
        base = group_transforms("V4-plane")
        return base + [lambda c, f=f: _swap_uk(f(c)) for f in base]
    if name == "swap-only":
        return [lambda c: c, _swap_uk]
    if name == "B4":
        out = []
        for mask in range(16):
            idxs = tuple(i for i in range(4) if mask >> i & 1)
            out.append(lambda c, idxs=idxs: _flip(c, idxs))
        return out
    if name == "V4-full":
        return [lambda c: c,
                lambda c: _flip(c, (0,)),
                lambda c: _flip(c, (1,)),
                lambda c: _flip(c, (0, 1))]
    raise ValueError("unknown symmetry group %r" % (name,))


# ---------------------------------------------------------------------------
# Orbit-averaged noisy sweeps
# ---------------------------------------------------------------------------

def symmetrized_sweep(seed, theta, group_name,
                      n_copies=sk.DEFAULT_N_COPIES,
                      transforms=None):
    """Mean D / mean C per sigma, noise orbit-averaged.

    For each sigma, each of the n_copies base noise
    vectors is replaced by its whole orbit under the
    group; D and C are averaged over all
    n_copies * |G| copies. The base draws are the exact
    draws gaussian_copies uses for this seed, so the
    orbit is a fixed function of the draws already used
    — no new randomness.
    """
    if transforms is None:
        transforms = group_transforms(group_name)
    start = np.real(oc.slide_state(float(theta)))
    base_noise = draw_noise(seed, n_copies)
    rows = []
    for sigma in sk.SIGMA_GRID:
        ds, cs = [], []
        for z in base_noise:
            c0 = to_coords(z)
            for f in transforms:
                v = start + sigma * from_coords(f(c0))
                v = v / np.linalg.norm(v)
                ds.append(sk.self_knowing_factor(v))
                cs.append(te.concurrence(te.density_matrix(v)))
        rows.append({"sigma": float(sigma),
                     "mean_D": float(np.mean(ds)),
                     "mean_concurrence": float(np.mean(cs))})
    ds = [r["mean_D"] for r in rows]
    cs = [r["mean_concurrence"] for r in rows]
    return {
        "seed": int(seed),
        "theta": float(theta),
        "direction": wd.NOISY_DIRECTIONS.get(float(theta),
                                              "other"),
        "group": group_name,
        "orbit": len(transforms),
        "n_copies": int(n_copies),
        "pearson_d_c": sk.pearson(ds, cs),
        "spearman_d_c": sk.spearman(ds, cs),
        "d_range": float(max(ds) - min(ds)),
        "c_range": float(max(cs) - min(cs)),
        "rows": rows,
    }


def v4_full_sweep(seed, theta, n_copies=sk.DEFAULT_N_COPIES):
    """The V4-full orbit-averaged noisy sweep (this build's estimator)."""
    return symmetrized_sweep(seed, theta, GROUP_V4_FULL,
                             n_copies=n_copies)


def sweep_bars_from_rows(rows):
    """The four (xxxii) bars for a sweep's rows.

    Returns Pearson, Spearman, D range, C range, and
    whether each bar holds. Shared with the calibrator
    path: the same bars the frozen rule minimizes over.
    """
    bars = oa.sweep_bars(rows)
    return {
        "pearson_d_c": bars["pearson_d_c"],
        "spearman_d_c": bars["spearman_d_c"],
        "d_range": bars["d_range"],
        "c_range": bars["c_range"],
        "checks": bars["checks"],
        "n_failing": bars["n_failing"],
    }


def pearson_without_sigma_1(rows):
    """Pearson(D, C) with the sigma = 1.0 point dropped.

    Diagnostic only (claim (cii)): dropping sigma = 1.0
    is never a fix; the bars stay on the full grid.
    The sigma grid's last point is sigma = 1.0.
    """
    ds = [r["mean_D"] for r in rows[:-1]]
    cs = [r["mean_concurrence"] for r in rows[:-1]]
    return float(sk.pearson(ds, cs))


def plain_n_copies_sweep(seed, theta, n_copies):
    """The plain (unsymmetrized) sweep with n copies.

    The n-copies control: fresh draws extend the same
    RNG stream, so the first 5 draws are the baseline's.
    """
    return wd.noisy_direction_sweep(seed, theta,
                                    n_copies=n_copies)


# ---------------------------------------------------------------------------
# Mirror-averaged perpendicular sweeps (candidate 3, rejected)
# ---------------------------------------------------------------------------

def mirror_average(seed, thetas, n_copies=sk.DEFAULT_N_COPIES):
    """Mean D/C per sigma averaged over the listed thetas.

    Candidate 3a: symmetrizing the START by averaging
    the perpendicular sweep over theta = pi/4 and a
    mirror direction (same seed/noise). Measured by
    the exploration pilots; it FAILS on every seed
    (see docs/preregistration-v0.27.0.md) and is not
    carried into the production claims — kept here so
    the pilot table is reproducible in production code.
    """
    sweeps = [wd.noisy_direction_sweep(seed, t,
                                       n_copies=n_copies)
              for t in thetas]
    sigmas = sk.SIGMA_GRID
    ds = [float(np.mean([s["rows"][i]["mean_D"] for s in sweeps]))
          for i in range(len(sigmas))]
    cs = [float(np.mean([s["rows"][i]["mean_concurrence"]
                         for s in sweeps]))
          for i in range(len(sigmas))]
    return {
        "seed": int(seed),
        "thetas": [float(t) for t in thetas],
        "pearson_d_c": sk.pearson(ds, cs),
        "spearman_d_c": sk.spearman(ds, cs),
        "d_range": float(max(ds) - min(ds)),
        "c_range": float(max(cs) - min(cs)),
        "d_at_sigma_0": float(ds[0]),
        "c_at_sigma_0": float(cs[0]),
    }


def symmetrized_state_sweep(seed, thetas,
                            n_copies=sk.DEFAULT_N_COPIES):
    """Per sigma: average the copies' density matrices over
    the mirror pair, then D = Tr(P rho-bar), C =
    Wootters(rho-bar).

    Candidate 3b: the start rho-bar(0) = (rho(pi/4) +
    rho(-pi/4)) / 2 has its u-k coherence cancelled.
    Measured by the exploration pilots; it FAILS on
    every seed (see docs/preregistration-v0.27.0.md)
    and is not carried into the production claims —
    kept here so the pilot table is reproducible.
    """
    ds, cs = [], []
    for sigma in sk.SIGMA_GRID:
        rhos = []
        for theta in thetas:
            start = np.real(oc.slide_state(float(theta)))
            for v in unity.gaussian_copies(start, sigma,
                                           n_copies, seed):
                rhos.append(te.density_matrix(v))
        rho_bar = np.mean(rhos, axis=0)
        ds.append(sk.self_knowing_of_state(rho_bar))
        cs.append(te.concurrence(rho_bar))
    return {
        "seed": int(seed),
        "thetas": [float(t) for t in thetas],
        "pearson_d_c": sk.pearson(ds, cs),
        "spearman_d_c": sk.spearman(ds, cs),
        "d_range": float(max(ds) - min(ds)),
        "c_range": float(max(cs) - min(cs)),
        "d_at_sigma_0": float(ds[0]),
        "c_at_sigma_0": float(cs[0]),
    }


# ---------------------------------------------------------------------------
# Orbit-occupation diagnostic (candidate 4, anti-predictive)
# ---------------------------------------------------------------------------

def _shannon_entropy(counts):
    n = float(sum(counts))
    return -sum((c / n) * math.log2(c / n)
                for c in counts if c > 0)


def orbit_diagnostics(seed, theta, n_copies=sk.DEFAULT_N_COPIES):
    """Diagnostics from the same 5 fixed noise draws.

    m       : mean coupling mean_i <psi(theta)|z_i>
    m_P     : mean_i <psi(theta)|P|z_i> = cos(theta) *
              mean_i z_u,i
    H_sign  : Shannon entropy (bits) of the sign
              distribution of the 5 couplings
    H_quad  : Shannon entropy (bits) of the empirical
              distribution of the 5 copies over the 4
              quadrants of the (z_u, z_k) plane
              (orbit-occupation entropy; max 2 bits).
              Seed-only: the quadrant pattern does not
              depend on theta.
    align   : mean pairwise |cos| between the 5 noise
              vectors (seed-only).
    r_no1.0 : baseline Pearson recomputed without the
              sigma = 1.0 point.

    H_quad is ANTI-predictive (seed 2026 has the
    highest H_quad, 1.92/2.0, yet holds the stored
    failure; seed 7 has the lowest, 0.97, yet stored
    passes) — recorded and abandoned, not tuned.
    """
    psi = np.real(oc.slide_state(float(theta)))
    zs = draw_noise(seed, n_copies)
    couplings = [float(np.dot(psi, z)) for z in zs]
    m = float(np.mean(couplings))
    m_p = float(math.cos(theta)
                * np.mean([to_coords(z)[0] for z in zs]))
    n_pos = sum(1 for c in couplings if c > 0)
    h_sign = _shannon_entropy([n_pos, n_copies - n_pos])
    quads = {}
    for z in zs:
        zu, _, zk, _ = to_coords(z)
        q = (1 if zu > 0 else 0, 1 if zk > 0 else 0)
        quads[q] = quads.get(q, 0) + 1
    h_quad = _shannon_entropy(list(quads.values()))
    dots = []
    for i in range(n_copies):
        for j in range(i + 1, n_copies):
            dots.append(abs(float(np.dot(zs[i], zs[j])
                                / (np.linalg.norm(zs[i])
                                   * np.linalg.norm(zs[j])))))
    align = float(np.mean(dots))
    r = wd.noisy_direction_sweep(seed, theta)
    return {
        "seed": int(seed),
        "theta": float(theta),
        "m": m,
        "m_P": m_p,
        "H_sign": float(h_sign),
        "H_quad": float(h_quad),
        "align": align,
        "pearson": float(r["pearson_d_c"]),
        "pearson_no_sigma1": pearson_without_sigma_1(r["rows"]),
        "n_pos": int(n_pos),
        "d_range": float(r["d_range"]),
        "c_range": float(r["c_range"]),
    }


# ---------------------------------------------------------------------------
# V4-full + frozen calibrator (the (xci) fix)
# ---------------------------------------------------------------------------

def calibrated_symmetry_sweep(seed, theta,
                              n_copies=sk.DEFAULT_N_COPIES):
    """V4-full sweep + the frozen v0.26.0 calibrator rule.

    The observer reads the orbit-averaged sweep, the
    calibrator picks delta by the frozen rule (the
    same function on every seed, unchanged from
    observer_agents.SweepCalibrator), and the
    calibrated sweep is reported with its bars. The
    uncalibrated bars are reported alongside so the
    agent's effect is visible and nothing is hidden.
    """
    calibrator = oa.SweepCalibrator()
    sym = v4_full_sweep(seed, theta, n_copies=n_copies)
    uncalibrated = sweep_bars_from_rows(sym["rows"])
    choice = calibrator.choose_delta(sym["rows"])
    calibrated = sweep_bars_from_rows(
        oa.calibrated_rows(sym["rows"], choice["delta"]))
    return {
        "seed": int(seed),
        "theta": float(theta),
        "direction": sym["direction"],
        "group": GROUP_V4_FULL,
        "delta": float(choice["delta"]),
        "clip_affected": bool(oa.clip_affected(
            sym["rows"], choice["delta"])),
        "n_failing_at_zero": choice["n_failing_at_zero"],
        "n_failing_calibrated": choice["n_failing"],
        "uncalibrated": {
            "pearson_d_c": uncalibrated["pearson_d_c"],
            "spearman_d_c": uncalibrated["spearman_d_c"],
            "d_range": uncalibrated["d_range"],
            "c_range": uncalibrated["c_range"],
            "bars": uncalibrated["checks"],
        },
        "calibrated": {
            "pearson_d_c": calibrated["pearson_d_c"],
            "spearman_d_c": calibrated["spearman_d_c"],
            "d_range": calibrated["d_range"],
            "c_range": calibrated["c_range"],
            "bars": calibrated["checks"],
        },
    }


# ---------------------------------------------------------------------------
# Claims (xcviii)-(cii): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_orbit_estimator_exactness_verdict(
        seeds=None, thetas=None):
    """(xcviii) Orbit estimator exactness.

    PASS iff (a) at sigma = 0 the V4-full
    orbit-averaged D and C equal the exact values
    (cos^2(theta), sin^2(theta)) within 1e-12 on
    every (seed, direction); (b) permuting the 4
    orbit transforms changes mean D and mean C per
    sigma by at most 1e-12 on every (seed,
    direction); (c) the Z2 orbit average equals the
    theta/theta+pi pair average within 1e-12 per
    sigma on every (seed, direction).
    """
    t = _thresholds()
    tol = t["orbit_tol"]
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(ALL_NOISY_DIRECTIONS
                  if thetas is None else thetas)
    v4 = group_transforms(GROUP_V4_FULL)
    worst_sigma0 = 0.0
    worst_relabel = 0.0
    worst_pair = 0.0
    for seed in seeds:
        for theta in thetas:
            sym = v4_full_sweep(seed, theta)
            row0 = sym["rows"][0]
            worst_sigma0 = max(
                worst_sigma0,
                abs(row0["mean_D"] - math.cos(theta) ** 2),
                abs(row0["mean_concurrence"]
                    - math.sin(theta) ** 2))
            # (b) relabelling: reverse the transform order.
            relabelled = symmetrized_sweep(
                seed, theta, GROUP_V4_FULL,
                transforms=list(reversed(v4)))
            for r0, r1 in zip(sym["rows"],
                              relabelled["rows"]):
                worst_relabel = max(
                    worst_relabel,
                    abs(r0["mean_D"] - r1["mean_D"]),
                    abs(r0["mean_concurrence"]
                        - r1["mean_concurrence"]))
            # (c) Z2 orbit average vs theta/theta+pi pair average.
            z2 = symmetrized_sweep(seed, theta, "Z2-antipodal")
            plus = wd.noisy_direction_sweep(seed, theta)
            minus = wd.noisy_direction_sweep(
                seed, (theta + math.pi) % (2.0 * math.pi))
            for rz, rp, rm in zip(z2["rows"], plus["rows"],
                                  minus["rows"]):
                pair_d = 0.5 * (rp["mean_D"] + rm["mean_D"])
                pair_c = 0.5 * (rp["mean_concurrence"]
                                + rm["mean_concurrence"])
                worst_pair = max(
                    worst_pair,
                    abs(rz["mean_D"] - pair_d),
                    abs(rz["mean_concurrence"] - pair_c))
    checks = {
        "sigma0_exact": bool(worst_sigma0 <= tol),
        "relabel_invariant": bool(worst_relabel <= tol),
        "z2_equals_pair_average": bool(worst_pair <= tol),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xcviii) orbit estimator exactness: "
                 "sigma = 0 exact, relabelling invariant, "
                 "Z2 equals the theta/theta+pi pair average",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "worst_sigma0_error": float(worst_sigma0),
        "worst_relabel_change": float(worst_relabel),
        "worst_pair_difference": float(worst_pair),
        "basis_orthonormality_error":
            float(basis_orthonormality_error()),
    }


def claim_stored_pearson_rescue_verdict(seeds=None):
    """(xcix) Stored Pearson rescue: V4-full (2026,
    stored) Pearson <= -0.90, by orbit-averaging
    alone, no calibrator.

    PASS iff the Pearson bar holds on that combo.
    The other three stored Pearsons are reported
    alongside, not gated.
    """
    t = _thresholds()
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    per_seed = [v4_full_sweep(s, 0.0) for s in seeds]
    target = [r for r in per_seed if r["seed"] == 2026][0]
    checks = {
        "pearson_2026_stored_at_most_max": bool(
            target["pearson_d_c"] <= t["pearson_d_c_max"]),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(xcix) stored Pearson rescue: V4-full "
                 "(2026, stored) Pearson <= -0.90",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_symmetry_calibrated_xci_verdict(seeds=None,
                                          thetas=None):
    """(c) (xci) under symmetry + calibration: all 8
    combos pass all four bars with the V4-full sweep
    + the frozen calibrator rule.

    PASS iff all four (xxxii) bars hold on EVERY
    (seed, direction) in {42, 7, 1234, 2026} x
    {stored, opposite}. The delta per combo is
    recorded.
    """
    t = _thresholds()
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(XC_DIRECTIONS if thetas is None else thetas)
    per_combo = [calibrated_symmetry_sweep(s, th)
                 for s in seeds for th in thetas]
    checks = {
        "pearson_at_most_max": all(
            r["calibrated"]["pearson_d_c"]
            <= t["pearson_d_c_max"] for r in per_combo),
        "spearman_at_most_max": all(
            r["calibrated"]["spearman_d_c"]
            <= t["spearman_d_c_max"] for r in per_combo),
        "d_range_at_least_min": all(
            r["calibrated"]["d_range"] >= t["d_range_min"]
            for r in per_combo),
        "c_range_at_least_min": all(
            r["calibrated"]["c_range"] >= t["c_range_min"]
            for r in per_combo),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(c) (xci) under symmetry + calibration: "
                 "all 8 combos pass all four bars",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_combo": per_combo,
    }


def claim_perpendicular_stands_verdict(seeds=None,
                                       thetas=None):
    """(ci) Perpendicular stands: the V4-full
    perpendicular sweep still FAILS the bars on
    every seed.

    PASS iff, on EVERY seed in {42, 7, 1234, 2026}
    from theta = pi/4, the V4-full sweep has D range
    < 0.25 AND at least one failing bar. The frozen
    calibrator rule is applied per seed and reported
    alongside, not gated.
    """
    t = _thresholds()
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(XCI_DIRECTIONS if thetas is None else thetas)
    per_seed = []
    for s in seeds:
        for th in thetas:
            sym = v4_full_sweep(s, th)
            bars = sweep_bars_from_rows(sym["rows"])
            cal = calibrated_symmetry_sweep(s, th)
            per_seed.append({
                "seed": int(s),
                "theta": float(th),
                "direction": sym["direction"],
                "pearson_d_c": bars["pearson_d_c"],
                "spearman_d_c": bars["spearman_d_c"],
                "d_range": bars["d_range"],
                "c_range": bars["c_range"],
                "n_failing": bars["n_failing"],
                "calibrated_delta": float(cal["delta"]),
                "calibrated_d_range":
                    cal["calibrated"]["d_range"],
                "calibrated_n_failing":
                    cal["n_failing_calibrated"],
            })
    checks = {
        "d_range_below_min_on_every_seed": all(
            r["d_range"] < t["d_range_min"] for r in per_seed),
        "at_least_one_failing_bar_on_every_seed": all(
            r["n_failing"] >= 1 for r in per_seed),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(ci) perpendicular stands: the V4-full "
                 "perpendicular sweep still fails the bars "
                 "on every seed",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_seed": per_seed,
    }


def claim_two_failure_kinds_verdict(seeds=None, thetas=None):
    """(cii) Two failure kinds (diagnostic): Pearson
    without sigma = 1.0 passes (2026, stored) and
    fails every perpendicular.

    PASS iff r_no1.0(2026, stored) <= -0.90 AND
    r_no1.0(perp) > -0.90 on every seed. Dropping
    sigma = 1.0 is a diagnostic only, never a fix;
    the bars stay on the full grid.
    """
    t = _thresholds()
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(ALL_NOISY_DIRECTIONS
                  if thetas is None else thetas)
    per_combo = []
    for s in seeds:
        for th in thetas:
            r = wd.noisy_direction_sweep(s, th)
            per_combo.append({
                "seed": int(s),
                "theta": float(th),
                "direction": r["direction"],
                "pearson_d_c": float(r["pearson_d_c"]),
                "pearson_no_sigma1":
                    pearson_without_sigma_1(r["rows"]),
            })
    stored_2026 = [r for r in per_combo
                   if r["seed"] == 2026
                   and r["theta"] == 0.0][0]
    perps = [r for r in per_combo if r["theta"] == math.pi / 4]
    checks = {
        "stored_2026_passes_without_sigma1": bool(
            stored_2026["pearson_no_sigma1"]
            <= t["pearson_d_c_max"]),
        "perpendicular_fails_without_sigma1_on_every_seed":
            bool(all(r["pearson_no_sigma1"]
                     > t["pearson_d_c_max"] for r in perps)),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(cii) two failure kinds: stored is a "
                 "saturation-point failure, perpendicular "
                 "is whole-curve",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "per_combo": per_combo,
    }


def symmetry_sweep_claims():
    """The symmetry-sweep claims (xcviii)-(cii), measured fresh."""
    claim_xcviii = claim_orbit_estimator_exactness_verdict()
    claim_xcix = claim_stored_pearson_rescue_verdict()
    claim_c = claim_symmetry_calibrated_xci_verdict()
    claim_ci = claim_perpendicular_stands_verdict()
    claim_cii = claim_two_failure_kinds_verdict()
    verdicts = [claim_xcviii, claim_xcix, claim_c, claim_ci,
                claim_cii]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_xcviii_orbit_estimator_exactness": claim_xcviii,
        "claim_xcix_stored_pearson_rescue": claim_xcix,
        "claim_c_symmetry_calibrated_xci": claim_c,
        "claim_ci_perpendicular_stands": claim_ci,
        "claim_cii_two_failure_kinds": claim_cii,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the orbit estimator checks, the V4-full
    sweeps, the calibrated (xci) table, the
    perpendicular table, the diagnostic, and the
    claims (xcviii)-(cii) verdicts."""
    print("Symmetry sweep -- claims (xcviii)-(cii)")
    print()
    verdicts = symmetry_sweep_claims()
    xcviii = verdicts["claim_xcviii_orbit_estimator_exactness"]
    print("Orbit estimator exactness:")
    print(f"  basis orthonormality worst |G - I| = "
          f"{xcviii['basis_orthonormality_error']:.2e}")
    print(f"  worst sigma = 0 error = "
          f"{xcviii['worst_sigma0_error']:.2e}, worst "
          f"relabel change = "
          f"{xcviii['worst_relabel_change']:.2e}, worst "
          f"Z2-vs-pair difference = "
          f"{xcviii['worst_pair_difference']:.2e}")
    print(f"claim (xcviii) verdict: "
          f"{'PASS' if xcviii['passed'] else 'FAIL'}")
    print()
    xcix = verdicts["claim_xcix_stored_pearson_rescue"]
    print("Stored Pearson, V4-full, per seed:")
    for r in xcix["per_seed"]:
        print(f"  seed {r['seed']}: Pearson "
              f"{r['pearson_d_c']:.4f}, Spearman "
              f"{r['spearman_d_c']:.4f}, D range "
              f"{r['d_range']:.4f}, C range {r['c_range']:.4f}")
    print(f"claim (xcix) verdict: "
          f"{'PASS' if xcix['passed'] else 'FAIL'}")
    print()
    xc = verdicts["claim_c_symmetry_calibrated_xci"]
    print("V4-full + calibrator on (xci), per (seed, "
          "direction) [uncalibrated -> calibrated]:")
    for r in xc["per_combo"]:
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
    print(f"claim (c) verdict: "
          f"{'PASS' if xc['passed'] else 'FAIL'}")
    print()
    ci = verdicts["claim_ci_perpendicular_stands"]
    print("V4-full perpendicular, per seed [calibrator "
          "alongside]:")
    for r in ci["per_seed"]:
        print(f"  seed {r['seed']}: Pearson "
              f"{r['pearson_d_c']:.4f}, Spearman "
              f"{r['spearman_d_c']:.4f}, D range "
              f"{r['d_range']:.4f}, C range {r['c_range']:.4f}, "
              f"failing {r['n_failing']}, calibrator delta "
              f"{r['calibrated_delta']:+.4f} (D range "
              f"{r['calibrated_d_range']:.4f}, failing "
              f"{r['calibrated_n_failing']})")
    print(f"claim (ci) verdict: "
          f"{'PASS' if ci['passed'] else 'FAIL'}")
    print()
    cii = verdicts["claim_cii_two_failure_kinds"]
    print("Pearson without sigma = 1.0 (diagnostic only), "
          "per (seed, direction):")
    for r in cii["per_combo"]:
        print(f"  seed {r['seed']}, {r['direction']}: "
              f"Pearson {r['pearson_d_c']:.4f} -> "
              f"r_no1.0 {r['pearson_no_sigma1']:.4f}")
    print(f"claim (cii) verdict: "
          f"{'PASS' if cii['passed'] else 'FAIL'}")
    print()
    print(f"claims (xcviii)-(cii): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
