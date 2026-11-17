# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only

"""Tests for malus.py: Malus three-polarizer paradox (v0.9.0)."""

import math

import numpy as np
import pytest

import malus as ml


def test_polarizer_is_rank_one_projector():
    for theta in (0.0, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2):
        p = ml.polarizer(theta)
        assert p.shape == (2, 2)
        assert np.allclose(p, p.T, atol=1e-12)
        assert np.allclose(p @ p, p, atol=1e-12)
        assert float(np.trace(p)) == pytest.approx(1.0, abs=1e-12)
        eig = np.linalg.eigvalsh(p)
        assert eig[0] == pytest.approx(0.0, abs=1e-12)
        assert eig[1] == pytest.approx(1.0, abs=1e-12)


def test_polarizer_state_unit_and_angles():
    for theta, expected in ((0.0, (1.0, 0.0)),
                            (math.pi / 4, (math.sqrt(0.5), math.sqrt(0.5))),
                            (math.pi / 2, (0.0, 1.0))):
        v = ml.polarizer_state(theta)
        assert float(np.linalg.norm(v)) == pytest.approx(1.0, abs=1e-12)
        assert v[0] == pytest.approx(expected[0], abs=1e-12)
        assert v[1] == pytest.approx(expected[1], abs=1e-12)


def test_transmission_pure_is_malus_cos_squared():
    # Transmission of |0> through theta is cos^2(theta), and of
    # a general pure state it is |<theta|psi>|^2.
    for theta_deg in (0, 15, 30, 45, 60, 90, 135):
        theta = math.radians(theta_deg)
        psi = ml.polarizer_state(0.0)
        assert ml.transmission_pure(psi, theta) == pytest.approx(
            math.cos(theta) ** 2, abs=1e-12)
    psi = ml.polarizer_state(math.pi / 6)
    for theta_deg in (0, 30, 60, 90):
        theta = math.radians(theta_deg)
        overlap = float(np.vdot(ml.polarizer_state(theta), psi))
        assert ml.transmission_pure(psi, theta) == pytest.approx(
            overlap ** 2, abs=1e-12)


def test_transmission_pure_equals_psi_dagger_p_psi():
    # The bridge mapping: transmission is <psi|P(theta)|psi>,
    # the same functional form as the bridge's D = <psi|P|psi>.
    rng = np.random.default_rng(7)
    for _ in range(5):
        psi = rng.normal(size=2)
        psi = psi / np.linalg.norm(psi)
        theta = float(rng.uniform(0.0, math.pi))
        p = ml.polarizer(theta)
        assert ml.transmission_pure(psi, theta) == pytest.approx(
            float(psi @ p @ psi), abs=1e-12)


def test_project_state_returns_axis_or_none():
    psi = ml.polarizer_state(0.0)
    out = ml.project_state(psi, math.pi / 4)
    assert out is not None
    assert np.allclose(out, ml.polarizer_state(math.pi / 4), atol=1e-12)
    assert ml.project_state(psi, math.pi / 2) is None
    assert ml.project_state(ml.polarizer_state(math.pi / 3),
                            math.pi / 3) is not None


def test_chain_unpolarized_crossed_zero_and_triple_eighth():
    deg = math.radians
    assert ml.chain_unpolarized([deg(0), deg(90)])["total"] == pytest.approx(
        0.0, abs=1e-12)
    assert ml.chain_unpolarized(
        [deg(0), deg(45), deg(90)])["total"] == pytest.approx(
        0.125, abs=1e-12)
    assert ml.chain_unpolarized([deg(0), deg(45)])["total"] == pytest.approx(
        0.25, abs=1e-12)


def test_chain_unpolarized_records_states():
    deg = math.radians
    chain = ml.chain_unpolarized([deg(0), deg(45), deg(90)])
    assert len(chain["steps"]) == 3
    assert chain["steps"][0]["transmission"] == pytest.approx(0.5, abs=1e-12)
    assert chain["steps"][1]["transmission"] == pytest.approx(0.5, abs=1e-12)
    assert chain["steps"][2]["transmission"] == pytest.approx(0.5, abs=1e-12)
    for step, theta_deg in zip(chain["steps"], (0, 45, 90)):
        assert np.allclose(step["state_out"],
                           ml.polarizer_state(deg(theta_deg)), atol=1e-12)


def test_chain_polarized_aligned_input():
    deg = math.radians
    psi0 = ml.polarizer_state(deg(0))
    assert ml.chain_polarized(psi0, [deg(0), deg(90)])["total"] == (
        pytest.approx(0.0, abs=1e-12))
    assert ml.chain_polarized(
        psi0, [deg(0), deg(45), deg(90)])["total"] == pytest.approx(
        0.25, abs=1e-12)
    # A 45-degree input through the 90-degree polarizer: 1/2.
    assert ml.chain_polarized(
        ml.polarizer_state(deg(45)), [deg(90)])["total"] == pytest.approx(
        0.5, abs=1e-12)


def test_angle_curve_formula_on_grid():
    # Hand recomputation of one swept row: T(30 deg) =
    # (1/2) cos^2(30) sin^2(30) = (1/2)(3/4)(1/4) = 3/32.
    assert ml.angle_curve(math.radians(30)) == pytest.approx(
        3.0 / 32.0, abs=1e-12)
    for phi_deg in ml.ANGLE_GRID_DEG:
        phi = math.radians(phi_deg)
        expected = 0.125 * math.sin(2.0 * phi) ** 2
        assert ml.angle_curve(phi) == pytest.approx(expected, abs=1e-12)
        assert ml.chain_unpolarized(
            [0.0, phi, math.pi / 2])["total"] == pytest.approx(
            expected, abs=1e-12)


def test_angle_curve_peak_and_zeros():
    assert ml.angle_curve(0.0) == pytest.approx(0.0, abs=1e-12)
    assert ml.angle_curve(math.pi / 2) == pytest.approx(0.0, abs=1e-12)
    assert ml.angle_curve(math.pi / 4) == pytest.approx(0.125, abs=1e-12)
    fine = [ml.angle_curve(math.radians(d))
            for d in np.arange(0.0, 90.01, 0.5)]
    assert max(fine) == pytest.approx(0.125, abs=1e-12)
    assert int(np.argmax(fine)) == 90  # 45.0 deg at 0.5-deg steps


def test_angle_curve_directional_rise_then_fall():
    # The pre-registered direction: a rise in the middle angle
    # from 0 to 45 deg raises transmission; a fall from 45 to
    # 90 deg lowers it. A sweep with no written direction is
    # untested even when every test passes.
    grid = [ml.angle_curve(math.radians(d))
            for d in ml.ANGLE_GRID_DEG]
    assert all(b >= a for a, b in zip(grid[:4], grid[1:4]))
    assert all(b <= a for a, b in zip(grid[3:], grid[4:]))
    assert grid[3] > grid[0] and grid[3] > grid[-1]


def test_no_bypass_mid_state_and_product():
    deg = math.radians
    triple = ml.chain_unpolarized([deg(0), deg(45), deg(90)])
    mid = triple["steps"][1]["state_out"]
    assert abs(float(np.vdot(ml.polarizer_state(deg(45)), mid))) == (
        pytest.approx(1.0, abs=1e-12))
    t1 = triple["steps"][0]["transmission"]
    t2 = ml.transmission_pure(triple["steps"][0]["state_out"], deg(45))
    t3 = ml.transmission_pure(triple["steps"][1]["state_out"], deg(90))
    assert t1 * t2 * t3 == pytest.approx(0.125, abs=1e-12)
    # Bypass control: the state after the first polarizer
    # straight through 90 deg transmits nothing.
    assert ml.transmission_pure(
        triple["steps"][0]["state_out"], deg(90)) == pytest.approx(
        0.0, abs=1e-12)


def test_stepped_chain_values_and_limit():
    assert ml.stepped_chain(2)["total"] == pytest.approx(0.0, abs=1e-9)
    assert ml.stepped_chain(3)["total"] == pytest.approx(0.125, abs=1e-12)
    # N = 4: (1/2) cos^6(30 deg) = (1/2)(3/4)^3 = 27/128.
    assert ml.stepped_chain(4)["total"] == pytest.approx(
        27.0 / 128.0, abs=1e-12)
    for n in ml.STEPPED_N_GRID:
        step = math.pi / (2.0 * (n - 1))
        assert ml.stepped_chain(n)["total"] == pytest.approx(
            0.5 * math.cos(step) ** (2 * (n - 1)), abs=1e-12)
    totals = [ml.stepped_chain(n)["total"]
              for n in (2, 3, 4, 5, 10, 50, 200)]
    assert all(b > a for a, b in zip(totals, totals[1:]))
    assert abs(ml.stepped_chain(200)["total"] - 0.5) <= 0.01


def test_stepped_chain_rejects_n_below_2():
    with pytest.raises(ValueError):
        ml.stepped_chain(1)
    with pytest.raises(ValueError):
        ml.chain_unpolarized([])
    with pytest.raises(ValueError):
        ml.chain_polarized(ml.polarizer_state(0.0), [])


def test_claim_malus_verdict_passes():
    v = ml.claim_malus_verdict()
    assert v["passed"] is True
    assert all(v["checks"].values())
    assert v["unpolarized_crossed"] == pytest.approx(0.0, abs=1e-12)
    assert v["unpolarized_triple"] == pytest.approx(0.125, abs=1e-12)
    assert v["unpolarized_pair_0_45"] == pytest.approx(0.25, abs=1e-12)
    assert v["polarized_45_to_90"] == pytest.approx(0.5, abs=1e-12)
    assert v["polarized_triple"] == pytest.approx(0.25, abs=1e-12)


def test_claim_angle_selectivity_verdict_passes():
    v = ml.claim_angle_selectivity_verdict()
    assert v["passed"] is True
    assert all(v["checks"].values())
    assert v["fine_peak_deg"] == pytest.approx(45.0, abs=1.0)
    assert v["fine_peak_transmission"] == pytest.approx(0.125, abs=1e-12)
    assert len(v["grid_rows"]) == len(ml.ANGLE_GRID_DEG)


def test_claim_no_bypass_verdict_passes():
    v = ml.claim_no_bypass_verdict()
    assert v["passed"] is True
    assert all(v["checks"].values())
    assert v["mid_state_overlap_45_deg"] == pytest.approx(1.0, abs=1e-9)
    assert v["product_from_states"] == pytest.approx(0.125, abs=1e-12)
    assert v["bypass_transmission"] == pytest.approx(0.0, abs=1e-12)
    assert v["cascade_stage2_visibility"] == pytest.approx(0.0, abs=1e-12)
    assert v["malus_reopened_transmission"] == pytest.approx(
        0.125, abs=1e-12)


def test_stepped_chain_table_descriptive():
    table = ml.stepped_chain_table()
    assert len(table["rows"]) == len(ml.STEPPED_N_GRID)
    assert table["large_n"]["n"] == ml.STEPPED_N_LARGE
    assert table["large_n_within_limit_tol"] is True
    assert table["limit"] == 0.5
