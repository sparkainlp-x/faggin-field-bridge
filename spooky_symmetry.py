# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# spooky_symmetry.py
#
# Spooky stability under symmetry, and the fresh-seed
# correction to the v0.27.0 rescue story.
#
# Jean's directive, 2026-11-19: "Calibration and
# observer inside and symmetry spooky stability".
# Spooky U is the Omega-Genesis definition
# (unity.spooky_correlation): mean pairwise |dot|
# over 5 noisy copies of the same state — a
# self-similarity under noise, not entanglement.
# Orbit-averaging replaces each of the 5 draws by
# its orbit; the orbit copies are sign-flipped
# partners of the same draws, so they stay close to
# each other and U moves — mostly up. This module
# measures by how much, per sigma, and records the
# fresh-seed correction: the V4-full rescue of
# (xci) that v0.27.0 measured 8/8 on the file
# seeds does NOT generalize blindly. On the fresh
# seeds {5, 99, 2, 777, 2024} V4-full passes 3/5
# and plain n=20 passes 4/5; V4 BREAKS seed 2024
# (plain −0.9527 -> V4-full −0.8830); seed 5 fails
# under every method.
#
# Three claims, (cvii)-(cix), pre-registered in
# docs/preregistration-v0.28.0.md BEFORE the
# evaluation run. The fresh seeds are a second
# evaluation set with the blinding note (this
# exploration's pilots already saw them — exactly
# as v0.27.0 disclosed for the file seeds).
#
# (cvii) Spooky preserved at low sigma, not at
#     high sigma: max |U_orbit - U_plain| <= 0.003
#     at sigma <= 0.05 and <= 0.01 at sigma <= 0.1
#     under V4-full — AND max |dU| > 0.01 at sigma
#     = 0.5 (the break). Both legs are gated.
# (cviii) Rescue seed-fragility (CORRECTION to the
#     v0.27.0 story): V4-full stored Pearson <=
#     −0.90 on exactly 3/5 fresh seeds, plain n=20
#     on exactly 4/5; V4 BREAKS seed 2024; seed 5
#     fails under every method. Claim (c) stands as
#     measured on the file seeds; this claim
#     records that the rescue does not generalize
#     blindly.
# (cix) Perpendicular D-range stands on fresh
#     seeds: V4-full D range < 0.25 on every fresh
#     seed, with the Pearson sign seed-variable
#     exactly as piloted (positive on 6/9 seeds
#     plain, 5/9 under V4-full). Claim (ci) as
#     stated survives fresh seeds; only the
#     "inversion" description carries the seed
#     caveat.
#
# Honesty, stated up front:
#   - (cvii) is a statistical claim on 5-copy (and
#     orbit-averaged) means, like (xxxii)/(xci)/
#     (xcii): the same saturation and finite-sample
#     fragility applies, and a FAIL is a finding
#     about the construction, not a defect. Its
#     sigma = 0.1 leg is thin by construction
#     (pilot maximum 0.009930 against the 0.01
#     bar) and is disclosed as such.
#   - (cviii) and (cix) are statistical claims on
#     the same means. (cviii) CORRECTS the v0.27.0
#     story; it does not retract claim (c), which
#     stands as measured on the file seeds.
#   - The (xci), (xcii), (xxxii) and (xcviii)
#     verdicts stay FAIL on the record as
#     originally stated.
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
# evaluation run (see docs/preregistration-v0.28.0.md
# and the claim_*_verdict functions):
#   (cvii) (a) max |dU| <= 0.003 for sigma in {0,
#       0.01, 0.05}; (b) max |dU| <= 0.01 for sigma
#       in {0, 0.01, 0.05, 0.1}; (c) max |dU| > 0.01
#       at sigma = 0.5.
#   (cviii) (a) V4-full stored Pearson <= -0.90 on
#       exactly 3/5 fresh seeds (99, 2, 777 pass; 5
#       and 2024 fail); (b) plain n=20 stored
#       Pearson <= -0.90 on exactly 4/5 fresh seeds
#       (only 5 fails); (c) V4 breaks 2024 (plain
#       -0.9527 -> V4 -0.8830); (d) seed 5 fails
#       under every method (plain -0.6814, V4
#       -0.8338, n=20 -0.8749).
#   (cix) (a) V4-full perpendicular D range < 0.25
#       on every fresh seed; (b) Pearson positive on
#       exactly 6/9 seeds (file + fresh) plain and
#       exactly 5/9 under V4-full.
#

"""Spooky stability under symmetry + the fresh-seed correction."""

import math

import numpy as np

import bridge
import observer_cycle as oc
import self_knowing as sk
import symmetry_sweep as ss
import unity
import wave_direction as wd

# ---------------------------------------------------------------------------
# Seeds
# ---------------------------------------------------------------------------

# Calibration seeds: the frozen expectations come
# from these only (see the blinding note in
# docs/preregistration-v0.28.0.md).
CALIBRATION_SEEDS = (42, 7)
# Evaluation seeds: held out until the evaluation
# run (confirmatory re-measurement — see the
# blinding note).
EVALUATION_SEEDS = (1234, 2026)
ALL_SEEDS = CALIBRATION_SEEDS + EVALUATION_SEEDS
# Second evaluation set: fresh seeds, already seen
# by the exploration pilots (blinding note).
FRESH_SEEDS = (5, 99, 2, 777, 2024)

# ---------------------------------------------------------------------------
# Thresholds (frozen; never moved after the run)
# ---------------------------------------------------------------------------

# Exact-identity tolerance, as in (xxxiv)/(lxxxviii).
EXACT_TOL = 1e-9

# Spooky-preservation bars, frozen from the
# calibration pilot on seeds 42/7 (round numbers;
# the sigma = 0.1 leg is thin by construction).
DU_MAX_LOW_SIGMA = 0.003
DU_MAX_MID_SIGMA = 0.01
SIGMAS_LOW = (0.0, 0.01, 0.05)
SIGMAS_MID = (0.0, 0.01, 0.05, 0.1)
SIGMA_BREAK = 0.5

# The (xxxii) bars, reused unchanged since v0.12.0.
PEARSON_D_C_MAX = -0.90

# Directions, from wave_direction.py.
ALL_NOISY_DIRECTIONS = (0.0, math.pi / 4, math.pi / 2)
XCII_DIRECTIONS = wd.XCII_DIRECTIONS


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("EXACT_TOL", EXACT_TOL),
        ("DU_MAX_LOW_SIGMA", DU_MAX_LOW_SIGMA),
        ("DU_MAX_MID_SIGMA", DU_MAX_MID_SIGMA),
        ("PEARSON_D_C_MAX", PEARSON_D_C_MAX),
    ) if value is None]
    if missing:
        raise ValueError(
            "spooky-symmetry thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.28.0.md)")
    return {
        "exact_tol": float(EXACT_TOL),
        "du_max_low_sigma": float(DU_MAX_LOW_SIGMA),
        "du_max_mid_sigma": float(DU_MAX_MID_SIGMA),
        "pearson_d_c_max": float(PEARSON_D_C_MAX),
    }


# ---------------------------------------------------------------------------
# Spooky under the V4-full orbit average
# ---------------------------------------------------------------------------

def orbit_copies(seed, theta, sigma,
                 group_name=ss.GROUP_V4_FULL,
                 n_copies=sk.DEFAULT_N_COPIES):
    """The orbit-averaged copies: each base draw replaced
    by its whole orbit under the group.

    The base draws are the exact draws
    gaussian_copies uses for this seed, so the orbit
    is a fixed function of the draws already used —
    no new randomness.
    """
    start = np.real(oc.slide_state(float(theta)))
    base = ss.draw_noise(seed, n_copies)
    out = []
    for f in ss.group_transforms(group_name):
        for z in base:
            v = start + sigma * ss.from_coords(f(ss.to_coords(z)))
            out.append(v / np.linalg.norm(v))
    return out


def spooky_orbit_table(seed, theta,
                       group_name=ss.GROUP_V4_FULL,
                       n_copies=sk.DEFAULT_N_COPIES):
    """U_plain vs U_orbit per sigma, for one (seed, direction).

    Returns per-sigma U_plain (mean pairwise |dot|
    over the 5 plain copies), U_orbit (over the 20
    orbit copies), and dU = U_orbit - U_plain.
    """
    start = np.real(oc.slide_state(float(theta)))
    rows = []
    for sigma in sk.SIGMA_GRID:
        plain = unity.gaussian_copies(start, sigma,
                                      n_copies, seed)
        u_plain = unity.spooky_from_vectors(plain)
        orb = orbit_copies(seed, theta, sigma, group_name,
                           n_copies)
        u_orb = unity.spooky_from_vectors(orb)
        rows.append({
            "sigma": float(sigma),
            "u_plain": float(u_plain),
            "u_orbit": float(u_orb),
            "du": float(u_orb - u_plain),
        })
    return {
        "seed": int(seed),
        "theta": float(theta),
        "direction": wd.NOISY_DIRECTIONS.get(float(theta),
                                              "other"),
        "group": group_name,
        "rows": rows,
    }


def max_du_by_sigma(seeds=None, thetas=None,
                    group_name=ss.GROUP_V4_FULL):
    """Max |dU| per sigma over (seed, direction).

    Returns {sigma: (max |dU|, (seed, theta) where it
    occurs, mean |dU|)}.
    """
    seeds = list(ALL_SEEDS if seeds is None else seeds)
    thetas = list(ALL_NOISY_DIRECTIONS
                  if thetas is None else thetas)
    tables = [spooky_orbit_table(s, th, group_name)
              for s in seeds for th in thetas]
    out = {}
    for sigma in sk.SIGMA_GRID:
        worst = 0.0
        worst_at = None
        tot = 0.0
        cnt = 0
        for table in tables:
            row = [r for r in table["rows"]
                   if r["sigma"] == float(sigma)][0]
            d = abs(row["du"])
            tot += d
            cnt += 1
            if worst_at is None or d > worst:
                worst = d
                worst_at = (table["seed"], table["theta"])
        out[float(sigma)] = {
            "max_abs_du": float(worst),
            "worst_at": worst_at,
            "mean_abs_du": float(tot / cnt),
        }
    return out


# ---------------------------------------------------------------------------
# Fresh-seed rescue tables
# ---------------------------------------------------------------------------

def fresh_rescue_table(seeds=None):
    """Stored Pearson plain / V4-full / n=20 per fresh seed,
    plus the full 8-bar checks.

    The 8-bar check is all four (xxxii) bars on both
    directions (stored, opposite): V4-full + frozen
    calibrator rule, and plain n=20 copies. Reported
    alongside the Pearson counts, not gated by them.
    """
    seeds = list(FRESH_SEEDS if seeds is None else seeds)
    rows = []
    for seed in seeds:
        plain = wd.noisy_direction_sweep(seed, 0.0)
        v4 = ss.v4_full_sweep(seed, 0.0)
        n20 = ss.plain_n_copies_sweep(seed, 0.0, 20)
        cal_s = ss.calibrated_symmetry_sweep(seed, 0.0)
        cal_o = ss.calibrated_symmetry_sweep(seed, math.pi / 2)
        v4_8bar = (cal_s["calibrated"]["pearson_d_c"]
                   <= PEARSON_D_C_MAX
                   and cal_s["calibrated"]["spearman_d_c"]
                   <= -0.90
                   and cal_s["calibrated"]["d_range"] >= 0.25
                   and cal_s["calibrated"]["c_range"] >= 0.25
                   and cal_o["calibrated"]["pearson_d_c"]
                   <= PEARSON_D_C_MAX
                   and cal_o["calibrated"]["spearman_d_c"]
                   <= -0.90
                   and cal_o["calibrated"]["d_range"] >= 0.25
                   and cal_o["calibrated"]["c_range"] >= 0.25)
        n20_8bar = True
        for theta in (0.0, math.pi / 2):
            r = ss.plain_n_copies_sweep(seed, theta, 20)
            n20_8bar = n20_8bar and (
                r["pearson_d_c"] <= PEARSON_D_C_MAX
                and r["spearman_d_c"] <= -0.90
                and r["d_range"] >= 0.25
                and r["c_range"] >= 0.25)
        rows.append({
            "seed": int(seed),
            "plain_pearson": float(plain["pearson_d_c"]),
            "v4_pearson": float(v4["pearson_d_c"]),
            "n20_pearson": float(n20["pearson_d_c"]),
            "v4_passes": bool(
                v4["pearson_d_c"] <= PEARSON_D_C_MAX),
            "n20_passes": bool(
                n20["pearson_d_c"] <= PEARSON_D_C_MAX),
            "v4_8bar_passes": bool(v4_8bar),
            "n20_8bar_passes": bool(n20_8bar),
            "v4_cal_delta_stored": float(cal_s["delta"]),
            "v4_cal_delta_opposite": float(cal_o["delta"]),
        })
    return rows


def perpendicular_fresh_table(seeds=None):
    """Perpendicular Pearson plain / V4-full, and V4-full
    D range, per seed (fresh + file, for the counts)."""
    seeds = list(FRESH_SEEDS + ALL_SEEDS
                 if seeds is None else seeds)
    rows = []
    for seed in seeds:
        plain = wd.noisy_direction_sweep(seed, math.pi / 4)
        v4 = ss.v4_full_sweep(seed, math.pi / 4)
        cal = ss.calibrated_symmetry_sweep(seed, math.pi / 4)
        rows.append({
            "seed": int(seed),
            "plain_pearson": float(plain["pearson_d_c"]),
            "v4_pearson": float(v4["pearson_d_c"]),
            "v4_cal_pearson":
                float(cal["calibrated"]["pearson_d_c"]),
            "v4_cal_delta": float(cal["delta"]),
            "plain_d_range": float(plain["d_range"]),
            "v4_d_range": float(v4["d_range"]),
            "v4_cal_d_range":
                float(cal["calibrated"]["d_range"]),
        })
    return rows


# ---------------------------------------------------------------------------
# Claims (cvii)-(cix): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_spooky_preserved_verdict(seeds=None, thetas=None):
    """(cvii) Spooky preserved at low sigma, not at high sigma.

    PASS iff (a) max |dU| <= 0.003 for sigma in {0,
    0.01, 0.05}; (b) max |dU| <= 0.01 for sigma in
    {0, 0.01, 0.05, 0.1}; (c) max |dU| > 0.01 at
    sigma = 0.5. Both legs are gated: the low-sigma
    preservation AND the high-sigma break.
    """
    t = _thresholds()
    by_sigma = max_du_by_sigma(seeds, thetas)
    worst_low = max(by_sigma[s]["max_abs_du"]
                    for s in SIGMAS_LOW)
    worst_mid = max(by_sigma[s]["max_abs_du"]
                    for s in SIGMAS_MID)
    break_value = by_sigma[float(SIGMA_BREAK)]["max_abs_du"]
    checks = {
        "preserved_at_sigma_le_0.05": bool(
            worst_low <= t["du_max_low_sigma"]),
        "preserved_at_sigma_le_0.1": bool(
            worst_mid <= t["du_max_mid_sigma"]),
        "breaks_at_sigma_0.5": bool(
            break_value > t["du_max_mid_sigma"]),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(cvii) spooky preserved at low sigma, "
                 "not at high sigma, under V4-full",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "worst_low_sigma": float(worst_low),
        "worst_mid_sigma": float(worst_mid),
        "break_at_sigma_0.5": float(break_value),
        "max_du_by_sigma": {
            str(s): {"max_abs_du": v["max_abs_du"],
                     "worst_at_seed": v["worst_at"][0],
                     "worst_at_theta": v["worst_at"][1],
                     "mean_abs_du": v["mean_abs_du"]}
            for s, v in by_sigma.items()},
    }


def claim_rescue_fragility_verdict(seeds=None):
    """(cviii) Rescue seed-fragility (CORRECTION to the
    v0.27.0 story).

    PASS iff (a) V4-full stored Pearson <= -0.90 on
    exactly 3 of the 5 fresh seeds (99, 2, 777 pass;
    5 and 2024 fail); (b) plain n=20 stored Pearson
    <= -0.90 on exactly 4 of the 5 fresh seeds
    (only 5 fails); (c) V4 BREAKS seed 2024: plain
    -0.9527 -> V4-full -0.8830; (d) seed 5 fails
    under every method (plain -0.6814, V4-full
    -0.8338, n=20 -0.8749). The full 8-bar check is
    reported alongside, not gated.
    """
    t = _thresholds()
    rows = fresh_rescue_table(seeds)
    v4_passing = sorted(r["seed"] for r in rows
                        if r["v4_passes"])
    n20_passing = sorted(r["seed"] for r in rows
                         if r["n20_passes"])
    seed_2024 = [r for r in rows if r["seed"] == 2024][0]
    seed_5 = [r for r in rows if r["seed"] == 5][0]
    checks = {
        "v4_passes_3_of_5": bool(
            v4_passing == [2, 99, 777]),
        "n20_passes_4_of_5": bool(
            n20_passing == [2, 99, 777, 2024]),
        "v4_breaks_2024": bool(
            seed_2024["plain_pearson"] <= t["pearson_d_c_max"]
            and seed_2024["v4_pearson"]
            > t["pearson_d_c_max"]),
        "seed_5_fails_every_method": bool(
            seed_5["plain_pearson"] > t["pearson_d_c_max"]
            and seed_5["v4_pearson"] > t["pearson_d_c_max"]
            and seed_5["n20_pearson"] > t["pearson_d_c_max"]),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(cviii) rescue seed-fragility: V4-full "
                 "passes 3/5 fresh seeds, n=20 passes 4/5, "
                 "V4 breaks 2024, seed 5 fails everywhere",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "v4_passing_seeds": v4_passing,
        "n20_passing_seeds": n20_passing,
        "per_seed": rows,
    }


def claim_perpendicular_fresh_verdict(seeds=None):
    """(cix) Perpendicular D-range stands on fresh seeds.

    PASS iff (a) V4-full perpendicular D range <
    0.25 on EVERY fresh seed; (b) the Pearson sign
    is seed-variable exactly as piloted: positive on
    exactly 6 of the 9 seeds (file + fresh) under
    the plain sweep and exactly 5 of 9 under
    V4-full.
    """
    t = _thresholds()
    rows = perpendicular_fresh_table(seeds)
    fresh = [r for r in rows if r["seed"] in FRESH_SEEDS]
    plain_positive = sorted(r["seed"] for r in rows
                            if r["plain_pearson"] > 0.0)
    v4_positive = sorted(r["seed"] for r in rows
                         if r["v4_pearson"] > 0.0)
    checks = {
        "d_range_below_min_on_every_fresh_seed": bool(all(
            r["v4_d_range"] < 0.25 for r in fresh)),
        "plain_positive_on_6_of_9": bool(
            plain_positive == [5, 7, 99, 1234, 2024, 2026]),
        "v4_positive_on_5_of_9": bool(
            v4_positive == [5, 7, 1234, 2024, 2026]),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(cix) perpendicular D-range stands on "
                 "fresh seeds, Pearson sign seed-variable",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "plain_positive_seeds": plain_positive,
        "v4_positive_seeds": v4_positive,
        "max_v4_d_range_fresh": float(max(
            r["v4_d_range"] for r in fresh)),
        "per_seed": rows,
    }


def spooky_symmetry_claims():
    """The spooky-symmetry claims (cvii)-(cix), measured fresh."""
    claim_cvii = claim_spooky_preserved_verdict()
    claim_cviii = claim_rescue_fragility_verdict()
    claim_cix = claim_perpendicular_fresh_verdict()
    verdicts = [claim_cvii, claim_cviii, claim_cix]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_cvii_spooky_preserved": claim_cvii,
        "claim_cviii_rescue_fragility": claim_cviii,
        "claim_cix_perpendicular_fresh": claim_cix,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the spooky-per-sigma table, the fresh-seed
    rescue table, the perpendicular table, and the
    claims (cvii)-(cix) verdicts."""
    print("Spooky symmetry -- claims (cvii)-(cix)")
    print()
    verdicts = spooky_symmetry_claims()
    cvii = verdicts["claim_cvii_spooky_preserved"]
    print("Max |U_orbit - U_plain| per sigma (V4-full):")
    for sigma, row in cvii["max_du_by_sigma"].items():
        print(f"  sigma = {sigma}: max |dU| = "
              f"{row['max_abs_du']:.6f} (seed "
              f"{row['worst_at_seed']}, theta "
              f"{row['worst_at_theta']:.4f}), mean = "
              f"{row['mean_abs_du']:.6f}")
    print(f"claim (cvii) verdict: "
          f"{'PASS' if cvii['passed'] else 'FAIL'}")
    print()
    cviii = verdicts["claim_cviii_rescue_fragility"]
    print("Fresh-seed rescue, stored Pearson "
          "(plain / V4 / n20) [V4+cal 8-bar / n20 8-bar]:")
    for r in cviii["per_seed"]:
        print(f"  seed {r['seed']}: "
              f"{r['plain_pearson']:+.4f} / "
              f"{r['v4_pearson']:+.4f} / "
              f"{r['n20_pearson']:+.4f} "
              f"[{'PASS' if r['v4_8bar_passes'] else 'FAIL'} / "
              f"{'PASS' if r['n20_8bar_passes'] else 'FAIL'}]")
    print(f"  V4 passing seeds: {cviii['v4_passing_seeds']}, "
          f"n20 passing seeds: {cviii['n20_passing_seeds']}")
    print(f"claim (cviii) verdict: "
          f"{'PASS' if cviii['passed'] else 'FAIL'}")
    print()
    cix = verdicts["claim_cix_perpendicular_fresh"]
    print("Perpendicular, all nine seeds (plain / V4 "
          "Pearson, V4 D range):")
    for r in cix["per_seed"]:
        print(f"  seed {r['seed']}: "
              f"{r['plain_pearson']:+.4f} / "
              f"{r['v4_pearson']:+.4f}, D range "
              f"{r['v4_d_range']:.4f}")
    print(f"  plain positive seeds: "
          f"{cix['plain_positive_seeds']}, V4 positive "
          f"seeds: {cix['v4_positive_seeds']}")
    print(f"claim (cix) verdict: "
          f"{'PASS' if cix['passed'] else 'FAIL'}")
    print()
    print(f"claims (cvii)-(cix): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
