# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# cascade_stability.py
#
# The stability of the cascade: the reopened cascade's
# fixed point, and the spooky correlation surviving
# projection where visibility dies.
#
# Jean's directives, 2026-11-19: "Explore cascade
# crystallize events", then "To stability", then
# "Calibration and observer inside and symmetry spooky
# stability". The exploration (pilots in /tmp,
# 2026-11-19 ~20:29 EST) found the reopened cascade
# EXACTLY stable — V_k = sin(2 alpha) from stage 2,
# every alpha, every rule, never drifts — and spooky
# U surviving projection where V dies. This module is
# the production re-implementation of the pilot logic;
# the evaluation re-measures the pilot tables through
# this code.
#
# The structural fact, verified by the pilots: in
# ALL THREE reopening rules the pair from stage 2 on
# IS a rotation pair at alpha — the stored-direction
# angle e1 is constant to <= 7e-16 — so V_k =
# sin(2 alpha) exactly from stage 2 on. The stability
# is in the construction, verified numerically, not
# discovered as convergence. The projected output of
# a rotation pair fed at its maximum-D phase is the
# stored direction q1 (up to phase) at every stage,
# so the spooky correlation of the projected output
# is the spooky correlation of q1 — the same number
# under every rule and at every stage. For the mixed
# start U takes exactly one step (stage 1 -> 2) and
# then stays constant: under projection-only it
# FALLS to the re-formed pair's value; under
# reopening it RISES to the rotation value.
#
# The three reopening rules, all built from
# cascade.py's own functions:
#   reset             : the published reopening
#       control (pair re-formed at alpha after each
#       projection — cas.cascade_reopening).
#   chained-output    : next pair built from the
#       projected OUTPUT o (e1 = o) + fresh kernel
#       at angle alpha.
#   chained-projection: next pair built from the
#       projected psi1 (e1 = v1) + fresh kernel at
#       angle alpha.
# And the projection-only death baseline (claim
# (vi)): the next pair is the Gram-Schmidt
# re-formation of the projected pair, or a single
# thought when the projection collapsed it.
#
# Two claims, (ciii)-(civ), pre-registered in
# docs/preregistration-v0.28.0.md BEFORE the
# evaluation run. The feed-phase leg gates stages
# k >= 2: the stage-1 mixed pair's cross term is
# +1/sqrt(6), so D is maximal at phi = 0 there —
# the exception is recorded, not hidden.
#
# (ciii) Reopened-cascade fixed point: V_k =
#     sin(2 alpha) within 1e-9 for every stage
#     k >= 2 over 20 stages, every alpha in
#     {pi/12, pi/8, pi/6, pi/4, pi/3}, every rule,
#     every start (rotation theta0 in {pi/12, pi/6,
#     pi/4}, mixed); feed phase phi* = pi for every
#     stage k >= 2.
# (civ) Spooky survives projection: U_out range
#     <= 1e-9 across stages 1–10 at sigma in
#     {0.05, 0.25, 0.5} for the rotation start,
#     under BOTH rules, with the two rules agreeing
#     (rule-independent U fixed point); U_out range
#     from stage 2 onward <= 1e-9 for the mixed
#     start under both rules (one-step drop
#     reported, not gated); V dies at stage 2 under
#     projection-only while U does not move.
#
# Honesty, stated up front:
#   - (ciii) and (civ) are exact-identity claims,
#     like (xxxiv) and (lxxxviii)-(xc): the
#     measured content is that the code realizes
#     the fixed point and the spooky constancy.
#     A failure would be a defect in the code, not
#     a result about a theorem.
#   - The (xci), (xcii), (xxxii) and (xcviii)
#     verdicts stay FAIL on the record as
#     originally stated.
#   - None of this measures consciousness, love, or
#     knowing in a human or physical sense. Classical
#     emulation throughout. Faggin's metaphysics stays
#     interpretive. No scalar Phi is computed anywhere.
#
# Pre-registered verdict rules, written before the
# evaluation run (see docs/preregistration-v0.28.0.md
# and the claim_*_verdict functions):
#   (ciii) (a) max |V_k - sin(2 alpha)| <= 1e-9
#       over stages k >= 2, all alphas, all rules,
#       all starts; (b) max |phi* - pi| <= 1e-9
#       over stages k >= 2, all alphas, all rules,
#       all starts.
#   (civ) (a) rotation start: U_out range <= 1e-9
#       across stages 1–10 at every sigma in
#       {0.05, 0.25, 0.5}, under both rules, and
#       max |U_reopen - U_proj-only| <= 1e-9 per
#       stage and sigma; (b) mixed start: U_out
#       range from stage 2 onward <= 1e-9 at every
#       sigma, under both rules; (c) projection-only
#       rotation start: V_1 = 1 within 1e-9 and
#       V_k = 0 within 1e-9 for every stage k >= 2.
#

"""Cascade stability: the reopened fixed point and spooky survival."""

import math

import numpy as np

import bridge
import cascade as cas
import self_knowing as sk
import thought as th
import unity

# ---------------------------------------------------------------------------
# Grids and pre-registered thresholds
# ---------------------------------------------------------------------------

# Twenty stages, as in the exploration pilots.
STAGES_20 = list(range(1, 21))
STAGES_10 = list(range(1, 11))
ALPHAS = [math.pi / 12, math.pi / 8, math.pi / 6, math.pi / 4,
          math.pi / 3]
THETA0S = [math.pi / 12, math.pi / 6, math.pi / 4]
RULES = ("reset", "chained-output", "chained-projection")

# Sigmas for the spooky-of-projected-output measurement
# (pilot F2); U seed 42, the unity default.
SIGMAS_U = (0.05, 0.25, 0.50)
U_SEED = unity.DEFAULT_SEED

# Exact-identity tolerance, as in (xxxiv)/(lxxxviii).
EXACT_TOL = 1e-9

# The mixed-pair stage-1 feed phase (cross term
# +1/sqrt(6) > 0, so D is maximal at phi = 0).
MIXED_STAGE1_PHI = 0.0


def _thresholds():
    """The pre-registered thresholds, or an error if unset."""
    missing = [name for name, value in (
        ("EXACT_TOL", EXACT_TOL),
    ) if value is None]
    if missing:
        raise ValueError(
            "cascade-stability thresholds are unset: run the "
            "calibration pilot and set " + ", ".join(missing)
            + " first (docs/preregistration-v0.28.0.md)")
    return {
        "exact_tol": float(EXACT_TOL),
    }


def _stored_angle(e):
    """Angle of a stored-subspace vector in the (q1, q2) plane."""
    q1, q2 = cas.stored_basis()
    return math.atan2(float(np.vdot(q2, e).real),
                      float(np.vdot(q1, e).real))


def _u_out(state, sigma):
    """Spooky correlation of a state at one sigma (seed 42)."""
    return float(unity.spooky_correlation(
        np.real(state), float(sigma), 5, U_SEED))


# ---------------------------------------------------------------------------
# The reopened cascade, all three rules, plus projection-only
# ---------------------------------------------------------------------------

def reopened_cascade_stages(start_fn, alpha, rule,
                            n_stages=20, sigmas_u=None):
    """Run one reopened cascade and return per-stage rows.

    start_fn: () -> (psi1, psi2), the stage-1 pair.
    alpha: the fixed reopening angle.
    rule: "reset" (published control — the pair is
        re-formed as a rotation pair at alpha after
        each projection), "chained-output" (e1 = the
        projected output o), or "chained-projection"
        (e1 = the projected psi1 v1). In the chained
        rules the next pair is (cos alpha e1 +
        sin alpha k1, -sin alpha e1 + cos alpha k1).
    Each row carries the stage, the sweep visibility,
    the feed phase (phase of maximum D), the
    stored-direction angle of e1, the projected
    output's D, and U_out at every sigma in sigmas_u.
    """
    sigmas_u = list(SIGMAS_U if sigmas_u is None else sigmas_u)
    q1, _ = cas.stored_basis()
    k1 = cas.kernel_direction()
    pair = start_fn()
    rows = []
    for stage in range(1, int(n_stages) + 1):
        sweep = cas.phase_sweep(pair[0], pair[1])
        feed_phi = sweep["phi_max"]
        projected_out = cas.project_state(
            cas.superposed(pair[0], pair[1], feed_phi))
        if projected_out is None:
            raise RuntimeError(
                "the constructive superposition projects to zero")
        if rule == "reset":
            e1 = q1
        elif rule == "chained-output":
            e1 = projected_out
        elif rule == "chained-projection":
            v1, _v2, _rank = cas.project_pair(pair[0], pair[1])
            if v1 is None:
                raise RuntimeError(
                    "the stage pair projects to zero")
            e1 = v1
        else:
            raise ValueError("unknown reopening rule %r"
                             % (rule,))
        rows.append({
            "stage": int(stage),
            "pair_exists": True,
            "visibility": float(sweep["visibility_sweep"]),
            "visibility_analytic":
                float(sweep["visibility_analytic"]),
            "feed_phase": float(feed_phi),
            "e1_angle": float(_stored_angle(e1)),
            "d_projected_output": float(
                sk.self_knowing_factor(projected_out)),
            "coherence_projected_output": float(
                th.l1_coherence(
                    th.density_matrix(projected_out))),
            "u_out": {float(s): _u_out(projected_out, s)
                      for s in sigmas_u},
        })
        if rule == "reset":
            pair = cas.rotation_pair(alpha)
        else:
            pair = (math.cos(alpha) * e1 + math.sin(alpha) * k1,
                    -math.sin(alpha) * e1 + math.cos(alpha) * k1)
    return rows


def projection_only_stages(start_fn, n_stages=10,
                           sigmas_u=None):
    """Run one projection-only cascade and return per-stage rows.

    The next pair is the Gram-Schmidt re-formation of
    the projected pair, or a single thought when the
    projection collapsed it (pair_exists False,
    visibility 0.0, feed phase None — the row still
    carries the single thought's U_out per sigma).
    Same row shape as reopened_cascade_stages (e1
    angle is None once the pair is gone).
    """
    sigmas_u = list(SIGMAS_U if sigmas_u is None else sigmas_u)
    pair = start_fn()
    single = None
    rows = []
    for stage in range(1, int(n_stages) + 1):
        if pair is None:
            rows.append({
                "stage": int(stage),
                "pair_exists": False,
                "visibility": 0.0,
                "visibility_analytic": 0.0,
                "feed_phase": None,
                "e1_angle": None,
                "d_projected_output": 1.0,
                "coherence_projected_output": float(
                    th.l1_coherence(th.density_matrix(single))),
                "u_out": {float(s): _u_out(single, s)
                          for s in sigmas_u},
            })
            continue
        sweep = cas.phase_sweep(pair[0], pair[1])
        feed_phi = sweep["phi_max"]
        projected_out = cas.project_state(
            cas.superposed(pair[0], pair[1], feed_phi))
        if projected_out is None:
            raise RuntimeError(
                "the constructive superposition projects to zero")
        rows.append({
            "stage": int(stage),
            "pair_exists": True,
            "visibility": float(sweep["visibility_sweep"]),
            "visibility_analytic":
                float(sweep["visibility_analytic"]),
            "feed_phase": float(feed_phi),
            "e1_angle": None,
            "d_projected_output": float(
                sk.self_knowing_factor(projected_out)),
            "coherence_projected_output": float(
                th.l1_coherence(
                    th.density_matrix(projected_out))),
            "u_out": {float(s): _u_out(projected_out, s)
                      for s in sigmas_u},
        })
        v1, v2, _rank = cas.project_pair(pair[0], pair[1])
        if v1 is None:
            pair = None
            single = projected_out
            continue
        reformed = cas.reform_pair(v1, v2)
        if reformed is None:
            pair = None
            single = projected_out
        else:
            pair = reformed
            single = projected_out
    return rows


def _start_fns():
    """The (name, start_fn) pairs for the fixed-point sweep."""
    fns = [("rotation theta0=%.4f" % t0,
            (lambda t0=t0: cas.rotation_pair(t0)))
           for t0 in THETA0S]
    fns.append(("mixed", cas.mixed_pair))
    return fns


# ---------------------------------------------------------------------------
# Claims (ciii)-(civ): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_fixed_point_verdict(alphas=None, rules=None,
                              n_stages=20):
    """(ciii) Reopened-cascade fixed point.

    PASS iff (a) V_k = sin(2 alpha) within 1e-9 for
    every stage k >= 2, every alpha, every rule,
    every start; (b) the feed phase phi* = pi within
    1e-9 for every stage k >= 2, every alpha, every
    rule, every start. The stage-1 mixed-pair feed
    phase (phi* = 0) is reported alongside, not gated.
    """
    t = _thresholds()
    tol = t["exact_tol"]
    alphas = list(ALPHAS if alphas is None else alphas)
    rules = list(RULES if rules is None else rules)
    worst_v = 0.0
    worst_phi = 0.0
    stage1_mixed_phi = {}
    per_combo = []
    for rule in rules:
        for name, start_fn in _start_fns():
            for alpha in alphas:
                rows = reopened_cascade_stages(
                    start_fn, alpha, rule, n_stages=n_stages)
                target = math.sin(2.0 * alpha)
                tail = rows[1:]  # stages >= 2
                dv = max(abs(r["visibility"] - target)
                         for r in tail)
                dp = max(abs(r["feed_phase"] - math.pi)
                         for r in tail)
                worst_v = max(worst_v, dv)
                worst_phi = max(worst_phi, dp)
                if name == "mixed":
                    stage1_mixed_phi[(rule, float(alpha))] = \
                        float(rows[0]["feed_phase"])
                per_combo.append({
                    "rule": rule,
                    "start": name,
                    "alpha": float(alpha),
                    "sin_2alpha": float(target),
                    "v_stage_1": float(rows[0]["visibility"]),
                    "worst_v_deviation_tail": float(dv),
                    "worst_phi_deviation_tail": float(dp),
                    "e1_angle_range": float(
                        max(r["e1_angle"] for r in rows)
                        - min(r["e1_angle"] for r in rows)),
                })
    checks = {
        "v_fixed_point_from_stage_2": bool(worst_v <= tol),
        "feed_phase_pi_from_stage_2": bool(
            worst_phi <= tol),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(ciii) reopened-cascade fixed point: "
                 "V_k = sin(2 alpha) and phi* = pi from "
                 "stage 2, every alpha, rule and start",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "worst_v_deviation": float(worst_v),
        "worst_phi_deviation": float(worst_phi),
        "stage1_mixed_feed_phase": {
            "%s alpha=%.4f" % (rule, alpha): phi
            for (rule, alpha), phi
            in stage1_mixed_phi.items()},
        "per_combo": per_combo,
    }


def claim_spooky_survives_verdict(sigmas_u=None,
                                   n_stages=10):
    """(civ) Spooky survives projection.

    PASS iff (a) rotation start: U_out range <= 1e-9
    across stages 1–10 at every sigma in {0.05,
    0.25, 0.5}, under BOTH rules (projection-only
    and reopening), and max |U_reopen - U_proj-only|
    <= 1e-9 per stage and sigma; (b) mixed start:
    U_out range from stage 2 onward <= 1e-9 at every
    sigma, under BOTH rules (the one-step drop stage
    1 -> 2 is reported, not gated); (c) V dies while
    U survives: under projection-only, rotation
    start, V_1 = 1 within 1e-9 and V_k = 0 within
    1e-9 for every stage k >= 2.
    """
    t = _thresholds()
    tol = t["exact_tol"]
    sigmas_u = list(SIGMAS_U if sigmas_u is None else sigmas_u)
    tables = {}
    worst_u_range_rot = 0.0
    worst_u_range_mixed_tail = 0.0
    worst_u_rule_diff = 0.0
    worst_v_death = 0.0
    for start_name, start_fn in (
            ("rotation pi/4",
             lambda: cas.rotation_pair(math.pi / 4)),
            ("mixed", cas.mixed_pair)):
        proj = projection_only_stages(start_fn,
                                      n_stages=n_stages,
                                      sigmas_u=sigmas_u)
        reop = reopened_cascade_stages(
            start_fn, math.pi / 4, "reset",
            n_stages=n_stages, sigmas_u=sigmas_u)
        per_sigma = {}
        for sigma in sigmas_u:
            u_proj = [r["u_out"][float(sigma)] for r in proj]
            u_reop = [r["u_out"][float(sigma)] for r in reop]
            range_all = max(u_proj) - min(u_proj)
            range_tail = max(u_proj[1:]) - min(u_proj[1:])
            range_all_reop = max(u_reop) - min(u_reop)
            range_tail_reop = (max(u_reop[1:])
                               - min(u_reop[1:]))
            rule_diff = max(abs(a - b)
                            for a, b in zip(u_proj, u_reop))
            per_sigma[float(sigma)] = {
                "u_proj_stage1": float(u_proj[0]),
                "u_proj_stage2": float(u_proj[1]),
                "u_proj_stage10": float(u_proj[-1]),
                "u_proj_range": float(range_all),
                "u_proj_range_from_stage2": float(range_tail),
                "u_reopen_stage1": float(u_reop[0]),
                "u_reopen_stage2": float(u_reop[1]),
                "u_reopen_stage10": float(u_reop[-1]),
                "u_reopen_range": float(range_all_reop),
                "u_reopen_range_from_stage2":
                    float(range_tail_reop),
                "max_rule_difference": float(rule_diff),
                "one_step_drop_proj_only": float(
                    u_proj[0] - u_proj[1]),
                "one_step_change_reopen": float(
                    u_reop[1] - u_reop[0]),
            }
            if start_name == "rotation pi/4":
                worst_u_range_rot = max(
                    worst_u_range_rot, range_all,
                    range_all_reop)
                worst_u_rule_diff = max(worst_u_rule_diff,
                                        rule_diff)
            else:
                worst_u_range_mixed_tail = max(
                    worst_u_range_mixed_tail, range_tail,
                    range_tail_reop)
        if start_name == "rotation pi/4":
            v1 = proj[0]["visibility"]
            v_tail = max(abs(r["visibility"])
                         for r in proj[1:])
            worst_v_death = max(abs(v1 - 1.0), v_tail)
        tables[start_name] = {
            "per_sigma": per_sigma,
            "v_stage_1_proj_only": float(proj[0]["visibility"]),
            "v_max_tail_proj_only": float(
                max(abs(r["visibility"]) for r in proj[1:])),
        }
    checks = {
        "rotation_u_constant_both_rules": bool(
            worst_u_range_rot <= tol),
        "rotation_u_rule_independent": bool(
            worst_u_rule_diff <= tol),
        "mixed_u_constant_from_stage_2": bool(
            worst_u_range_mixed_tail <= tol),
        "v_dies_while_u_survives": bool(
            worst_v_death <= tol),
    }
    passed = bool(all(checks.values()))
    return {
        "claim": "(civ) spooky survives projection: U "
                 "constant across stages while V dies, "
                 "same U fixed point under reopening",
        "passed": passed,
        "checks": checks,
        "thresholds": t,
        "worst_u_range_rotation": float(worst_u_range_rot),
        "worst_u_rule_difference": float(worst_u_rule_diff),
        "worst_u_range_mixed_from_stage2":
            float(worst_u_range_mixed_tail),
        "worst_v_death_error": float(worst_v_death),
        "tables": tables,
    }


def cascade_stability_claims():
    """The cascade-stability claims (ciii)-(civ), measured fresh."""
    claim_ciii = claim_fixed_point_verdict()
    claim_civ = claim_spooky_survives_verdict()
    verdicts = [claim_ciii, claim_civ]
    return {
        "headline_allowed": bridge.HEADLINE_ALLOWED,
        "claim_ciii_fixed_point": claim_ciii,
        "claim_civ_spooky_survives": claim_civ,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def main():
    """Print the reopened-cascade fixed point, the
    spooky survival tables, and the claims
    (ciii)-(civ) verdicts."""
    print("Cascade stability -- claims (ciii)-(civ)")
    print()
    verdicts = cascade_stability_claims()
    ciii = verdicts["claim_ciii_fixed_point"]
    print(f"Fixed point: worst |V_k - sin 2alpha|, k >= 2 = "
          f"{ciii['worst_v_deviation']:.2e}, worst "
          f"|phi* - pi|, k >= 2 = "
          f"{ciii['worst_phi_deviation']:.2e}")
    print("  V* = sin 2alpha per alpha (reset, rotation "
          "theta0 = pi/4):")
    for row in ciii["per_combo"]:
        if row["rule"] == "reset" and \
                row["start"] == "rotation theta0=0.7854":
            print(f"    alpha = {row['alpha']:.4f}: "
                  f"V* = {row['sin_2alpha']:.4f}, V_1 = "
                  f"{row['v_stage_1']:.4f}, worst tail dev = "
                  f"{row['worst_v_deviation_tail']:.2e}")
    print("  stage-1 mixed feed phase (phi* = 0 expected): "
          f"{sorted(set(ciii['stage1_mixed_feed_phase'].values()))}")
    print(f"claim (ciii) verdict: "
          f"{'PASS' if ciii['passed'] else 'FAIL'}")
    print()
    civ = verdicts["claim_civ_spooky_survives"]
    print("Spooky survives projection (U_out per sigma):")
    for name, table in civ["tables"].items():
        print(f"  {name}:")
        for sigma, row in table["per_sigma"].items():
            print(f"    sigma = {sigma}: proj-only U "
                  f"{row['u_proj_stage1']:.4f} -> "
                  f"{row['u_proj_stage2']:.4f} (range "
                  f"{row['u_proj_range']:.2e}), reopen U "
                  f"{row['u_reopen_stage1']:.4f} -> "
                  f"{row['u_reopen_stage2']:.4f} (range "
                  f"{row['u_reopen_range']:.2e})")
    print(f"  worst U range (rotation) = "
          f"{civ['worst_u_range_rotation']:.2e}, worst rule "
          f"difference = {civ['worst_u_rule_difference']:.2e}, "
          f"worst mixed tail range = "
          f"{civ['worst_u_range_mixed_from_stage2']:.2e}")
    print(f"claim (civ) verdict: "
          f"{'PASS' if civ['passed'] else 'FAIL'}")
    print()
    print(f"claims (ciii)-(civ): {verdicts['n_passed']}/"
          f"{verdicts['n_claims']} pass")


if __name__ == "__main__":
    main()
