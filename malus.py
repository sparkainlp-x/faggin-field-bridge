# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only

"""Malus three-polarizer paradox (v0.9.0).

Classical optics, Malus's law: a polarizer at angle theta
transmits the component of the light along its axis, so a
polarized beam of intensity I through a polarizer at relative
angle theta emerges with I cos^2(theta). Two crossed
polarizers (0 deg and 90 deg) transmit 0. Insert a third
polarizer at 45 deg between them and light gets through:

  unpolarized input I0:  (1/2) x cos^2(45) x cos^2(45) = I0/8
  polarized input I0 at 0 deg: cos^2(45) x cos^2(45) = I0/4

The middle projection CREATES transmission out of a closed
channel. This is the counter-case to the v0.3.0 cascade
finding (interference does NOT survive projection: V = 1.0
at stage 1, 0.0000 from stage 2 on): the same operation --
project and renormalize -- here reopens a channel instead
of closing one. The difference is structural, not a matter
of noise: in the cascade the projected PAIR collapses onto
one stored direction (rank 1), so the cross term dies; here
a SINGLE state is rotated by the projection into a direction
with nonzero overlap with the final axis. A projection does
not create energy: it discards the orthogonal component,
and the surviving component happens to overlap the next
axis. More filtering, more light -- because each filter
re-aims what survives it.

Mapping onto the bridge: a polarizer IS a projector.
P(theta) = |theta><theta| is the 2D analogue of the bridge's
stored-subspace projector P, and the transmission of a pure
state through a polarizer is <psi|P(theta)|psi> -- the same
functional form as the bridge's self-knowing factor
D = <psi|P|psi>. Malus's law is D measured along a rotated
axis. The state after each polarizer is the projected and
renormalized state, exactly the cascade's project_state
semantics, in polarization space instead of thought space.

Honesty: this is classical optics computed exactly with
NumPy (the same honesty as the rest of the quantum-thought
modules). The polarizers are ideal (no absorption beyond
the projection, no depolarization); the input is either
unpolarized (maximally mixed, the textbook I0/8 case) or
a pure Jones vector. Nothing here is a measurement of a
mind. Faggin's metaphysics stays interpretive.

Pre-registered verdict rules, written before any measurement
(see claim_malus_verdict, claim_angle_selectivity_verdict,
claim_no_bypass_verdict). Thresholds are the exact
tolerances EXACT_TOL = 1e-9: every gated number is an exact
analytic prediction (I0/8, 1/4, 1/2, cos^2), so the freeze
is the analytic value itself, never moved.
  (xxiii) crossed polarizers transmit 0; inserting the
      45-degree middle projection yields I0/8. Direction:
      adding the middle polarizer RAISES transmission from
      0 to 1/8 -- more filtering, more light. Claim (xxiii)
      PASSES iff, for unpolarized input, |T(0, 90) - 0| <=
      1e-9 and |T(0, 45, 90) - 1/8| <= 1e-9, with the
      decomposition |T(0, 45) - 1/4| <= 1e-9 and
      |T(45 -> 90 | |45>) - 1/2| <= 1e-9; and for polarized
      input aligned at 0 deg, T(0, 90) = 0 and
      T(0, 45, 90) = 1/4 within 1e-9.
  (xxiv) the reopening is angle-selective: transmission
      through (0, phi, 90) with unpolarized input is
      T(phi) = (1/2) cos^2(phi) sin^2(phi)
             = (1/8) sin^2(2 phi). Direction: T rises from
      0 deg to 45 deg and falls from 45 deg to 90 deg.
      Claim (xxiv) PASSES iff |T(phi) - (1/8) sin^2(2 phi)|
      <= 1e-9 on the grid phi in {0, 15, 30, 45, 60, 75,
      90} deg, the fine-grid argmax is within 1 deg of 45
      deg with value 1/8 within 1e-9, T(0) = T(90) = 0
      within 1e-9, and T is monotone non-decreasing on
      [0, 45] and non-increasing on [45, 90] on the grid.
  (xxv) the projection story is consistent with the v0.3.0
      cascade: the middle step's output state is what the
      second projection acts on (no hidden bypass). Claim
      (xxv) PASSES iff (a) the recorded state after the
      middle polarizer is exactly |45 deg> (overlap >=
      1 - 1e-9); (b) the total transmission recomputed from
      the recorded intermediate states alone -- step
      transmissions T1, T2, T3, each evaluated on the
      recorded state entering that step, never on the angle
      list -- multiplies to 1/8 within 1e-9; (c) the
      bypass control is zero: the state after the first
      polarizer sent directly through 90 deg transmits 0
      within 1e-9, so the middle step is necessary; (d)
      the cascade contrast, recomputed live: the rotation
      cascade's visibility at stage 2 is 0 within 1e-9
      while the Malus reopened transmission is 1/8 > 0.1
      -- the same project-and-renormalize operation, the
      opposite outcome, because a pair collapses and a
      single state rotates.
Descriptive, not gated: the evenly stepped N-polarizer
chain from 0 deg to 90 deg, T(N) = (1/2) cos^(2(N-1)) of
the step angle, rising with N toward 1/2 -- projection
applied repeatedly keeps reopening the channel.
"""

import math

import numpy as np

import cascade as cs

# ---------------------------------------------------------------------------
# Pre-registered thresholds (frozen before the final run)
# ---------------------------------------------------------------------------

EXACT_TOL = 1e-9
PROJECT_ZERO_TOL = 1e-12
ANGLE_GRID_DEG = (0, 15, 30, 45, 60, 75, 90)
FINE_GRID_STEP_DEG = 0.5
PEAK_ANGLE_TOL_DEG = 1.0
REOPENED_MIN = 0.1
STEPPED_N_GRID = (2, 3, 4, 5, 10)
STEPPED_N_LARGE = 200
STEPPED_LIMIT_TOL = 0.01


# ---------------------------------------------------------------------------
# Polarizers: projectors onto a polarization direction
# ---------------------------------------------------------------------------

def polarizer_state(theta):
    """|theta>: the unit Jones vector at angle theta (radians)."""
    return np.array([math.cos(float(theta)), math.sin(float(theta))],
                    dtype=float)


def polarizer(theta):
    """P(theta) = |theta><theta|: the rank-1 polarizer projector."""
    v = polarizer_state(theta)
    return np.outer(v, v)


def transmission_pure(psi, theta):
    """<psi|P(theta)|psi>: transmission of a pure state.

    Equal to |<theta|psi>|^2 by construction; this is the
    bridge's D = <psi|P|psi> with the projector rotated to
    the polarizer axis.
    """
    psi = np.asarray(psi, dtype=float)
    p = polarizer(theta)
    return float(psi @ p @ psi)


def project_state(psi, theta):
    """The normalized projected state P(theta) psi / ||...||, or None.

    None means the state projects to (numerically) zero: it is
    orthogonal to the polarizer axis, so no transmitted state
    exists. Same semantics as cascade.project_state.
    """
    psi = np.asarray(psi, dtype=float)
    out = polarizer(theta) @ psi
    n = float(np.linalg.norm(out))
    if n <= PROJECT_ZERO_TOL:
        return None
    return out / n


# ---------------------------------------------------------------------------
# Chains: sequences of polarizers
# ---------------------------------------------------------------------------

def chain_unpolarized(thetas):
    """Unpolarized input (intensity I0 = 1) through polarizers.

    The first polarizer transmits 1/2 and outputs its own
    axis state; each later polarizer transmits cos^2 of the
    relative angle and outputs its axis state. Returns the
    total transmission, the per-step transmissions, and the
    recorded state after each polarizer.
    """
    thetas = [float(t) for t in thetas]
    if not thetas:
        raise ValueError("the chain needs at least one polarizer")
    steps = []
    total = 0.5
    state = polarizer_state(thetas[0])
    steps.append({"theta": thetas[0], "transmission": 0.5,
                  "state_in": None, "state_out": state.copy()})
    for theta in thetas[1:]:
        t = float(math.cos(theta - thetas[len(steps) - 1]) ** 2)
        total *= t
        state = polarizer_state(theta)
        steps.append({"theta": theta, "transmission": t,
                      "state_in": steps[-1]["state_out"].copy(),
                      "state_out": state.copy()})
    return {"total": float(total), "steps": steps}


def chain_polarized(psi, thetas):
    """Pure input state psi (unit) through polarizers.

    Each step transmits |<theta|psi_in>|^2 and outputs the
    projected state. Returns the total transmission, the
    per-step transmissions, and the recorded state after
    each polarizer (None where the step transmits zero).
    """
    thetas = [float(t) for t in thetas]
    if not thetas:
        raise ValueError("the chain needs at least one polarizer")
    psi = np.asarray(psi, dtype=float)
    steps = []
    total = 1.0
    state = psi / float(np.linalg.norm(psi))
    for theta in thetas:
        t = transmission_pure(state, theta)
        total *= t
        out = project_state(state, theta)
        steps.append({"theta": theta, "transmission": float(t),
                      "state_in": state.copy(),
                      "state_out": None if out is None else out.copy()})
        if out is None:
            break
        state = out
    return {"total": float(total), "steps": steps}


def angle_curve(phi):
    """T(phi) for the chain (0, phi, 90 deg), unpolarized input.

    T = (1/2) cos^2(phi) sin^2(phi) = (1/8) sin^2(2 phi).
    """
    return float(0.5 * math.cos(float(phi)) ** 2
                 * math.sin(float(phi)) ** 2)


def stepped_chain(n):
    """N polarizers evenly stepped from 0 deg to 90 deg, unpolarized.

    Step angle pi / (2 (N - 1)); total transmission
    (1/2) cos^(2 (N - 1))(step). N = 2 is the crossed pair
    (0); N = 3 is the Malus triple (1/8); N -> infinity
    tends to 1/2.
    """
    n = int(n)
    if n < 2:
        raise ValueError("the stepped chain needs at least 2 polarizers")
    step = math.pi / (2.0 * (n - 1))
    total = 0.5 * math.cos(step) ** (2 * (n - 1))
    angles = [k * step for k in range(n)]
    return {"n": n, "step_deg": math.degrees(step),
            "angles": angles, "total": float(total)}


# ---------------------------------------------------------------------------
# Claims (xxiii), (xxiv), (xxv): pre-registered verdicts
# ---------------------------------------------------------------------------

def claim_malus_verdict():
    """Pre-registered verdict for claim (xxiii): crossed 0, middle 45 -> I0/8.

    PASS iff, for unpolarized input, |T(0, 90) - 0| <= 1e-9
    and |T(0, 45, 90) - 1/8| <= 1e-9, with the decomposition
    |T(0, 45) - 1/4| <= 1e-9 and |T(45 -> 90 | |45>) - 1/2|
    <= 1e-9; and for polarized input aligned at 0 deg,
    T(0, 90) = 0 and T(0, 45, 90) = 1/4 within 1e-9.
    """
    deg = math.radians
    crossed = chain_unpolarized([deg(0), deg(90)])
    triple = chain_unpolarized([deg(0), deg(45), deg(90)])
    pair = chain_unpolarized([deg(0), deg(45)])
    middle_to_last = chain_polarized(polarizer_state(deg(45)),
                                     [deg(90)])
    pol_crossed = chain_polarized(polarizer_state(deg(0)),
                                  [deg(0), deg(90)])
    pol_triple = chain_polarized(polarizer_state(deg(0)),
                                 [deg(0), deg(45), deg(90)])

    ok_a = abs(crossed["total"]) <= EXACT_TOL
    ok_b = abs(triple["total"] - 0.125) <= EXACT_TOL
    ok_c = (abs(pair["total"] - 0.25) <= EXACT_TOL
            and abs(middle_to_last["total"] - 0.5) <= EXACT_TOL)
    ok_d = (abs(pol_crossed["total"]) <= EXACT_TOL
            and abs(pol_triple["total"] - 0.25) <= EXACT_TOL)
    passed = bool(ok_a and ok_b and ok_c and ok_d)
    return {
        "claim": "(xxiii) crossed polarizers transmit 0; "
                 "45-degree middle yields I0/8",
        "passed": passed,
        "checks": {
            "a_crossed_zero_unpolarized": bool(ok_a),
            "b_triple_one_eighth": bool(ok_b),
            "c_decomposition_quarter_then_half": bool(ok_c),
            "d_polarized_input_quarter": bool(ok_d),
        },
        "unpolarized_crossed": crossed["total"],
        "unpolarized_triple": triple["total"],
        "unpolarized_pair_0_45": pair["total"],
        "polarized_45_to_90": middle_to_last["total"],
        "polarized_crossed": pol_crossed["total"],
        "polarized_triple": pol_triple["total"],
    }


def claim_angle_selectivity_verdict():
    """Pre-registered verdict for claim (xxiv): reopening peaks at 45 deg.

    PASS iff |T(phi) - (1/8) sin^2(2 phi)| <= 1e-9 on the
    grid phi in {0, 15, 30, 45, 60, 75, 90} deg, the
    fine-grid argmax is within 1 deg of 45 deg with value
    1/8 within 1e-9, T(0) = T(90) = 0 within 1e-9, and T
    is monotone non-decreasing on [0, 45] and
    non-increasing on [45, 90] on the grid.
    """
    deg = math.radians
    rows = []
    ok_formula = True
    for phi_deg in ANGLE_GRID_DEG:
        phi = deg(phi_deg)
        measured = chain_unpolarized(
            [deg(0), phi, deg(90)])["total"]
        expected = 0.125 * math.sin(2.0 * phi) ** 2
        ok = abs(measured - expected) <= EXACT_TOL
        ok_formula = ok_formula and ok
        rows.append({"phi_deg": float(phi_deg),
                     "transmission": measured,
                     "expected": expected})

    fine = [(phi_deg,
             angle_curve(deg(phi_deg)))
            for phi_deg in np.arange(0.0, 90.0 + FINE_GRID_STEP_DEG,
                                     FINE_GRID_STEP_DEG)]
    peak_phi, peak_t = max(fine, key=lambda row: row[1])
    ok_peak = (abs(peak_phi - 45.0) <= PEAK_ANGLE_TOL_DEG
               and abs(peak_t - 0.125) <= EXACT_TOL)
    ok_ends = (abs(rows[0]["transmission"]) <= EXACT_TOL
               and abs(rows[-1]["transmission"]) <= EXACT_TOL)
    grid_t = [r["transmission"] for r in rows]
    ok_rise = all(b >= a for a, b in zip(grid_t[:4], grid_t[1:4]))
    ok_fall = all(b <= a for a, b in zip(grid_t[3:], grid_t[4:]))
    passed = bool(ok_formula and ok_peak and ok_ends
                  and ok_rise and ok_fall)
    return {
        "claim": "(xxiv) reopening is angle-selective: "
                 "peaks at 45 deg, vanishes at 0/90 deg",
        "passed": passed,
        "checks": {
            "a_formula_one_eighth_sin2_2phi": bool(ok_formula),
            "b_peak_at_45_deg": bool(ok_peak),
            "c_ends_zero": bool(ok_ends),
            "d_rises_to_45_falls_after": bool(ok_rise and ok_fall),
        },
        "grid_rows": rows,
        "fine_peak_deg": float(peak_phi),
        "fine_peak_transmission": float(peak_t),
    }


def claim_no_bypass_verdict():
    """Pre-registered verdict for claim (xxv): no hidden bypass.

    PASS iff (a) the recorded state after the middle
    polarizer is exactly |45 deg> (overlap >= 1 - 1e-9);
    (b) the total transmission recomputed from the recorded
    intermediate states alone multiplies to 1/8 within
    1e-9; (c) the bypass control is zero: the state after
    the first polarizer sent directly through 90 deg
    transmits 0 within 1e-9; (d) the cascade contrast,
    recomputed live: the rotation cascade's visibility at
    stage 2 is 0 within 1e-9 while the Malus reopened
    transmission is 1/8 > 0.1.
    """
    deg = math.radians
    triple = chain_unpolarized([deg(0), deg(45), deg(90)])
    mid_state = triple["steps"][1]["state_out"]
    overlap = float(abs(np.vdot(polarizer_state(deg(45)), mid_state)))
    ok_a = overlap >= 1.0 - EXACT_TOL

    # Recompute from the recorded states alone: each step's
    # transmission is evaluated on the recorded state that
    # enters it, never on the angle list.
    t1 = triple["steps"][0]["transmission"]
    state_after_first = triple["steps"][0]["state_out"]
    t2 = transmission_pure(state_after_first, deg(45))
    state_after_mid = triple["steps"][1]["state_out"]
    t3 = transmission_pure(state_after_mid, deg(90))
    product = t1 * t2 * t3
    ok_b = abs(product - 0.125) <= EXACT_TOL

    bypass = transmission_pure(state_after_first, deg(90))
    ok_c = abs(bypass) <= EXACT_TOL

    rot = cs.cascade_projection_only(
        stages=[1, 2], pair_fn=lambda: cs.rotation_pair(math.pi / 4))
    v_stage2 = rot[1]["visibility"]
    ok_d = (abs(v_stage2) <= EXACT_TOL
            and triple["total"] > REOPENED_MIN)
    passed = bool(ok_a and ok_b and ok_c and ok_d)
    return {
        "claim": "(xxv) the middle step's output state is "
                 "what the second projection acts on",
        "passed": passed,
        "checks": {
            "a_mid_state_is_45_deg": bool(ok_a),
            "b_product_from_recorded_states": bool(ok_b),
            "c_bypass_control_zero": bool(ok_c),
            "d_cascade_contrast_stage2_zero_vs_reopened": bool(ok_d),
        },
        "mid_state_overlap_45_deg": overlap,
        "step_transmissions_from_states": [t1, t2, t3],
        "product_from_states": float(product),
        "bypass_transmission": float(bypass),
        "cascade_stage2_visibility": float(v_stage2),
        "malus_reopened_transmission": triple["total"],
    }


def stepped_chain_table(ns=None):
    """Descriptive (not gated): the evenly stepped N-polarizer chain.

    T(N) = (1/2) cos^(2(N-1))(step), step = 90 deg / (N - 1).
    Rises with N toward 1/2: projection applied repeatedly
    keeps reopening the channel.
    """
    ns = list(STEPPED_N_GRID if ns is None else ns)
    rows = [stepped_chain(n) for n in ns]
    large = stepped_chain(STEPPED_N_LARGE)
    return {"rows": rows, "large_n": large,
            "limit": 0.5,
            "large_n_within_limit_tol": bool(
                abs(large["total"] - 0.5) <= STEPPED_LIMIT_TOL)}


def main():
    """Print the Malus measurements and the three verdicts."""
    v = claim_malus_verdict()
    print("Malus -- claim (xxiii)")
    print(f"  crossed (0, 90), unpolarized: {v['unpolarized_crossed']:.6f}")
    print(f"  triple (0, 45, 90), unpolarized: "
          f"{v['unpolarized_triple']:.6f} (I0/8 = 0.125)")
    print(f"  pair (0, 45): {v['unpolarized_pair_0_45']:.6f} "
          f"(1/4 = 0.25)")
    print(f"  polarized (0, 45, 90): {v['polarized_triple']:.6f} "
          f"(1/4 = 0.25)")
    print(f"  claim (xxiii) verdict: {'PASS' if v['passed'] else 'FAIL'}")
    print()

    s = claim_angle_selectivity_verdict()
    print("Angle selectivity -- claim (xxiv)")
    print("  phi | T(phi) | (1/8) sin^2(2 phi)")
    for r in s["grid_rows"]:
        print(f"  {r['phi_deg']:>4.0f} | {r['transmission']:.6f} | "
              f"{r['expected']:.6f}")
    print(f"  fine peak: {s['fine_peak_deg']:.1f} deg, "
          f"T = {s['fine_peak_transmission']:.6f}")
    print(f"  claim (xxiv) verdict: {'PASS' if s['passed'] else 'FAIL'}")
    print()

    b = claim_no_bypass_verdict()
    print("No bypass -- claim (xxv)")
    print(f"  mid-state overlap with |45 deg>: "
          f"{b['mid_state_overlap_45_deg']:.12f}")
    print(f"  step transmissions from recorded states: "
          f"{[f'{t:.6f}' for t in b['step_transmissions_from_states']]}")
    print(f"  product: {b['product_from_states']:.6f}, "
          f"bypass: {b['bypass_transmission']:.6f}")
    print(f"  cascade stage-2 V: {b['cascade_stage2_visibility']:.6f} "
          f"vs Malus reopened: {b['malus_reopened_transmission']:.6f}")
    print(f"  claim (xxv) verdict: {'PASS' if b['passed'] else 'FAIL'}")
    print()

    t = stepped_chain_table()
    print("Stepped chain (descriptive): N polarizers, 0 -> 90 deg")
    for r in t["rows"]:
        print(f"  N = {r['n']:>2}: T = {r['total']:.6f}")
    print(f"  N = {t['large_n']['n']}: T = "
          f"{t['large_n']['total']:.6f} (limit 1/2)")


if __name__ == "__main__":
    main()
