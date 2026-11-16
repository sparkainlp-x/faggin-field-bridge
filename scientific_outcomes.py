# scientific_outcomes.py
#
# Maximum-scientific-outcomes logic for the Faggin Field Bridge.
#
# This module adds reproducibility, uncertainty, sensitivity,
# preregistration, provenance, and benchmark reporting. It does NOT
# test consciousness, validate Quantum Information Panpsychism, or
# measure physical quantum entanglement. (Entanglement as a quantity
# of the model is measured in thought_entanglement.py; see the
# quantum-thought claims below.)
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

import numpy as np

from attunement import DELTA_MAX, DELTA_MIN, attunement
from bridge import bridge, mapping_status, quantum_thought_claims
from synergy import (
    DORMANT_EXPANSION_THRESHOLD,
    EMERGENT_EXPANSION_THRESHOLD,
    FECUND_EXPANSION_THRESHOLD,
    attraction,
    expansion,
    fecundity,
    love_empathy_synergy,
    maximum_synergy_outcome,
    synergy_status,
    synergy_status_with_thresholds,
)


def _clip(value: float, lower: float, upper: float) -> float:
    return min(upper, max(lower, float(value)))


def validate_inputs(unity: float, cost: float, delta: float = 0.0) -> dict[str, float]:
    """Validate and normalize bridge inputs.

    Unity and cost must lie in [0, 1]. Delta is clipped to the
    bridge's declared calibration interval.
    """
    u = float(unity)
    c = float(cost)
    d = float(delta)

    if not np.isfinite(u) or not np.isfinite(c) or not np.isfinite(d):
        raise ValueError("unity, cost, and delta must be finite")
    if not 0.0 <= u <= 1.0:
        raise ValueError("unity must be in [0, 1]")
    if not 0.0 <= c <= 1.0:
        raise ValueError("cost must be in [0, 1]")

    return {
        "unity": u,
        "cost": c,
        "delta": _clip(d, DELTA_MIN, DELTA_MAX),
    }


def bootstrap_attunement(
    unity: float,
    cost: float,
    n_boot: int = 2000,
    unity_sd: float = 0.001,
    cost_sd: float = 0.001,
    seed: int = 42,
    confidence: float = 0.95,
) -> dict[str, float | list[float]]:
    """Bootstrap uncertainty for attunement at delta = 0.

    The input perturbations are explicit measurement-noise models,
    not claims about physical quantum uncertainty.
    """
    if n_boot < 100:
        raise ValueError("n_boot must be at least 100")
    if unity_sd < 0 or cost_sd < 0:
        raise ValueError("standard deviations must be non-negative")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be in (0, 1)")

    rng = np.random.default_rng(seed)
    values = np.empty(n_boot, dtype=float)

    for i in range(n_boot):
        u = _clip(rng.normal(unity, unity_sd), 0.0, 1.0)
        c = _clip(rng.normal(cost, cost_sd), 0.0, 1.0)
        values[i] = attunement(u, c, 0.0)

    alpha = (1.0 - confidence) / 2.0
    return {
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "standard_deviation": float(np.std(values, ddof=1)),
        "lower": float(np.quantile(values, alpha)),
        "upper": float(np.quantile(values, 1.0 - alpha)),
        "confidence": float(confidence),
        "n_boot": int(n_boot),
        "seed": int(seed),
    }


def sensitivity_analysis(
    unity: float,
    cost: float,
    unity_range: Iterable[float] = (-0.05, -0.01, 0.0, 0.01, 0.05),
    cost_range: Iterable[float] = (-0.05, -0.01, 0.0, 0.01, 0.05),
    delta_range: Iterable[float] = (-0.05, -0.025, 0.0, 0.025, 0.05),
) -> dict[str, list[dict[str, float]]]:
    """One-at-a-time sensitivity of attunement to its inputs.

    Each sweep perturbs one parameter and holds the other two at
    their base values. The ``apply`` callable returns the full
    (unity, cost, delta) triple after the perturbation, so a
    perturbation can never leak into the wrong slot.

    NOTE (v0.3.1 fix): through v0.3.0 the sweep helper passed the
    perturbed value into the unity slot for every parameter, so
    the cost sweep varied unity instead of cost and the delta
    sweep varied unity instead of delta. The unity sweep was
    correct; the cost and delta columns were wrong (the cost
    column was literally the perturbation itself). The fix makes
    ``apply`` return the triple and passes all three values to
    ``attunement``. See CHANGELOG 0.3.1 for the old -> new
    numbers.
    """
    base = validate_inputs(unity, cost)

    def sweep(
        name: str,
        values: Iterable[float],
        apply: Callable[[float], tuple[float, float, float]],
    ) -> list[dict[str, float]]:
        rows = []
        for change in values:
            u, c, d = apply(change)
            a = attunement(u, c, d)
            rows.append({
                "parameter": name,
                "change": float(change),
                "value": float({"unity": u, "cost": c, "delta": d}[name]),
                "attunement": float(a),
            })
        return rows

    return {
        "unity": sweep(
            "unity",
            unity_range,
            lambda x: (_clip(base["unity"] + x, 0.0, 1.0), base["cost"], base["delta"]),
        ),
        "cost": sweep(
            "cost",
            cost_range,
            lambda x: (base["unity"], _clip(base["cost"] + x, 0.0, 1.0), base["delta"]),
        ),
        "delta": sweep(
            "delta",
            delta_range,
            lambda x: (base["unity"], base["cost"], _clip(x, DELTA_MIN, DELTA_MAX)),
        ),
    }


def robustness(
    unity: float,
    cost: float,
    empathy: float = 0.5503,
    n_boot: int = 2000,
    seed: int = 42,
) -> dict[str, Any]:
    """Assess whether the mapping status is stable under measurement noise.

    The bound statuses come from the single classifier
    (bridge.mapping_status), so an ATTUNED case is reported as
    ATTUNED rather than forced into DISSONANT/PARTIAL.
    """
    result = bridge(unity, cost, empathy=empathy)
    before = result["mapping_status"]["label"]
    uncertainty = bootstrap_attunement(unity, cost, n_boot=n_boot, seed=seed)

    lower_status = mapping_status(uncertainty["lower"], empathy)["label"]
    upper_status = mapping_status(uncertainty["upper"], empathy)["label"]

    return {
        "reported_status": before,
        "attunement_uncertainty": uncertainty,
        "status_at_lower_bound": lower_status,
        "status_at_upper_bound": upper_status,
        "status_stable_under_uncertainty": lower_status == upper_status,
        "sign_flip_possible": uncertainty["lower"] < 0 <= uncertainty["upper"],
        "calibration_can_rescue": result["best_attunement"] >= 0.5,
    }


def bootstrap_expansion(
    unity: float,
    cost: float,
    love: float = 0.5503,
    empathy: float = 0.5503,
    delta: float = 0.05,
    n_boot: int = 2000,
    unity_sd: float = 0.001,
    cost_sd: float = 0.001,
    seed: int = 42,
    confidence: float = 0.95,
) -> dict[str, float | list[float]]:
    """Bootstrap uncertainty for the synergy expansion at fixed delta.

    Unity and cost are perturbed with the same explicit measurement-noise
    model used for attunement. Love and empathy are supplied proxies, so
    they are held fixed: this interval measures the stability of the
    expansion given the measured inputs, not the uncertainty of the
    proxies themselves.
    """
    if n_boot < 100:
        raise ValueError("n_boot must be at least 100")
    if unity_sd < 0 or cost_sd < 0:
        raise ValueError("standard deviations must be non-negative")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be in (0, 1)")

    rng = np.random.default_rng(seed)
    values = np.empty(n_boot, dtype=float)

    for i in range(n_boot):
        u = _clip(rng.normal(unity, unity_sd), 0.0, 1.0)
        c = _clip(rng.normal(cost, cost_sd), 0.0, 1.0)
        f = fecundity(u, c)
        x = attraction(f, _clip(delta, DELTA_MIN, DELTA_MAX))
        s = love_empathy_synergy(love, empathy, f)
        values[i] = expansion(x, s)

    alpha = (1.0 - confidence) / 2.0
    return {
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "standard_deviation": float(np.std(values, ddof=1)),
        "lower": float(np.quantile(values, alpha)),
        "upper": float(np.quantile(values, 1.0 - alpha)),
        "confidence": float(confidence),
        "n_boot": int(n_boot),
        "seed": int(seed),
    }


def threshold_robustness(
    unity: float,
    cost: float,
    love: float = 0.5503,
    empathy: float = 0.5503,
    delta: float = 0.05,
    dormant_grid: Iterable[float] = (0.01, 0.03, 0.05, 0.10),
    emergent_grid: Iterable[float] = (0.03, 0.05, 0.06, 0.10, 0.30),
) -> dict[str, Any]:
    """What label would this expansion carry under other thresholds?

    The synergy thresholds are repository conventions, not measured
    constants, so the reported status is only as robust as its
    distance to the nearest threshold. This table classifies the
    same point expansion under a grid of (DORMANT, EMERGENT)
    threshold choices, holding the FECUND thresholds at their
    shipped values. The shipped thresholds (0.03, 0.05) are one
    cell of the grid; the pre-8fb00f1 thresholds (0.10, 0.30) are
    another — under them the primary expansion was DORMANT, not
    FLOWING (see REPORT.md §5, "The 8fb00f1 threshold commit").
    """
    outcome = maximum_synergy_outcome(unity, cost, love, empathy, delta)
    point_e = outcome["expansion"]
    point_s = outcome["love_empathy_synergy"]

    dormant_list = list(dormant_grid)
    emergent_list = list(emergent_grid)
    statuses = [
        [
            synergy_status_with_thresholds(point_e, point_s, d, e)
            for e in emergent_list
        ]
        for d in dormant_list
    ]

    return {
        "expansion": float(point_e),
        "love_empathy_synergy": float(point_s),
        "shipped_thresholds": {
            "dormant": DORMANT_EXPANSION_THRESHOLD,
            "emergent": EMERGENT_EXPANSION_THRESHOLD,
            "fecund_expansion": FECUND_EXPANSION_THRESHOLD,
        },
        "shipped_status": outcome["synergy_status"],
        "dormant_grid": [float(d) for d in dormant_list],
        "emergent_grid": [float(e) for e in emergent_list],
        "statuses": statuses,
    }


def synergy_robustness(
    unity: float,
    cost: float,
    love: float = 0.5503,
    empathy: float = 0.5503,
    delta: float = 0.05,
    n_boot: int = 2000,
    seed: int = 42,
) -> dict[str, Any]:
    """Assess whether the synergy status is stable under measurement noise.

    Returns the status at the bootstrap interval bounds, whether the
    status is stable, and the margin from the point estimate to the
    nearest classification threshold. A margin smaller than the
    bootstrap standard deviation means the status is a boundary
    artifact, not a robust classification.
    """
    outcome = maximum_synergy_outcome(unity, cost, love, empathy, delta)
    point_e = outcome["expansion"]
    point_s = outcome["love_empathy_synergy"]
    point_status = outcome["synergy_status"]

    uncertainty = bootstrap_expansion(
        unity, cost, love, empathy, delta, n_boot=n_boot, seed=seed
    )

    lower_status = synergy_status(uncertainty["lower"], point_s)
    upper_status = synergy_status(uncertainty["upper"], point_s)

    # Margin to every expansion threshold that could change the
    # status. The nearest one decides stability; the full dict
    # shows how far each boundary sits. (The FECUND-synergy
    # threshold is not listed: it can only change the status once
    # the expansion is already past the FECUND expansion
    # threshold, which it is not here.)
    margins = {
        "to_dormant": abs(point_e - DORMANT_EXPANSION_THRESHOLD),
        "to_emergent": abs(point_e - EMERGENT_EXPANSION_THRESHOLD),
        "to_fecund": abs(point_e - FECUND_EXPANSION_THRESHOLD),
    }
    nearest_margin = min(margins.values())

    # Fecundity minus attunement at delta = 0. Algebraically
    # F - A = C * (1 - U), so the two coincide exactly when U = 1
    # and differ by C * (1 - U) otherwise. This is an identity of
    # the definitions, not a measured discovery.
    f_point = fecundity(unity, cost)
    a_point = attunement(unity, cost, 0.0)

    return {
        "reported_status": point_status,
        "expansion_uncertainty": uncertainty,
        "status_at_lower_bound": lower_status,
        "status_at_upper_bound": upper_status,
        "status_stable_under_uncertainty": lower_status == upper_status == point_status,
        "margins": {key: float(value) for key, value in margins.items()},
        "margin_to_nearest_threshold": float(nearest_margin),
        "margin_in_standard_deviations": float(
            nearest_margin / uncertainty["standard_deviation"]
        )
        if uncertainty["standard_deviation"] > 0
        else float("inf"),
        "threshold_robustness": threshold_robustness(
            unity, cost, love, empathy, delta
        ),
        "fecundity_minus_attunement": float(f_point - a_point),
        "fecundity_minus_attunement_identity": "C * (1 - U)",
    }


def preregistration() -> dict[str, Any]:
    """Frozen analysis plan for the current mapping.

    These are repository-defined analysis rules, not physical laws
    or independently validated psychological thresholds.
    """
    return {
        "primary_endpoint": "attunement at delta = 0",
        "secondary_endpoint": "best bounded attunement",
        "primary_hypothesis": "Unity proxy exceeds normalized entropy cost",
        "decision_rule": {
            "DISSONANT": "A < 0",
            "PARTIAL": "0 <= A < 0.5",
            "ATTUNED": "A >= 0.5 and empathy >= 0.5",
            "ATTUNED-LOW-EMPATHY": "A >= 0.5 and empathy < 0.5",
        },
        "calibration_bound": [DELTA_MIN, DELTA_MAX],
        "success_criterion": "Reproduce the declared input values and report uncertainty and sensitivity.",
        "non_claims": [
            "This does not test consciousness.",
            "This does not measure quantum entanglement.",
            "This does not validate Faggin's Quantum Information Panpsychism.",
            "Thresholds are repository conventions, not measured constants.",
            "Entanglement is measured only as a quantity of the model "
            "(concurrence of a two-thought Bell state, computed exactly "
            "on classical hardware); it is not a measurement of physical "
            "entanglement in hardware.",
            "Interference and cascade visibility are measured only as "
            "quantities of the model (exact geometry of state vectors "
            "on classical hardware); they are not measurements of "
            "physical interference in hardware.",
        ],
    }


def provenance(inputs: dict[str, Any], seed: int = 42) -> dict[str, Any]:
    """Create a reproducibility manifest for a benchmark run."""
    payload = json.dumps(
        {"inputs": inputs, "seed": seed},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return {
        "input_hash_sha256": hashlib.sha256(payload).hexdigest(),
        "random_seed": int(seed),
        "python_version": sys.version.split()[0],
        "numpy_version": np.__version__,
        "platform": platform.platform(),
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }


def maximum_scientific_outcome(
    unity: float,
    cost: float,
    empathy: float = 0.5503,
    n_boot: int = 2000,
    seed: int = 42,
) -> dict[str, Any]:
    """Produce the complete, bounded scientific outcome report."""
    validated = validate_inputs(unity, cost)
    bridge_result = bridge(
        validated["unity"],
        validated["cost"],
        empathy=empathy,
    )

    before_status = bridge_result["mapping_status"]["label"]

    # Recompute the uncalibrated status with the single classifier
    # (bridge.mapping_status) — the same function bridge() uses, so
    # the label can never drift between the two call sites.
    uncalibrated_a = attunement(validated["unity"], validated["cost"], 0.0)
    uncalibrated_status = mapping_status(uncalibrated_a, empathy)["label"]

    return {
        "point_estimate": {
            "unity": validated["unity"],
            "entropy_cost": validated["cost"],
            "attunement_delta_zero": uncalibrated_a,
            "best_delta": bridge_result["best_delta"],
            "best_attunement": bridge_result["best_attunement"],
        },
        "mapping_status": {
            "before_calibration": uncalibrated_status,
            "after_best_calibration": before_status,
            "calibration_changes_status": uncalibrated_status != before_status,
        },
        "uncertainty": bootstrap_attunement(
            validated["unity"],
            validated["cost"],
            n_boot=n_boot,
            seed=seed,
        ),
        "sensitivity": sensitivity_analysis(validated["unity"], validated["cost"]),
        "robustness": robustness(
            validated["unity"],
            validated["cost"],
            empathy=empathy,
            n_boot=n_boot,
            seed=seed,
        ),
        "synergy_robustness": synergy_robustness(
            validated["unity"],
            validated["cost"],
            # Love and empathy both default to the same supplied
            # Omega value (0.5503). This follows the synergy
            # module's own convention; it is not a measurement
            # that love equals empathy.
            love=empathy,
            empathy=empathy,
            delta=0.05,
            n_boot=n_boot,
            seed=seed,
        ),
        "preregistration": preregistration(),
        "provenance": provenance(
            {
                "unity": validated["unity"],
                "cost": validated["cost"],
                "empathy": empathy,
            },
            seed=seed,
        ),
        "claims": {
            "consciousness_tested": False,
            # Physical entanglement in hardware is not measured.
            # Entanglement as a quantity of the model IS measured
            # (concurrence, thought_entanglement.py) and reported
            # under "quantum_thoughts" below.
            "entanglement_measured": False,
            "entanglement_measured_in_model": True,
            "faggin_endorsed": False,
            "mapping_reproduced": True,
        },
        "quantum_thoughts": quantum_thought_claims(),
    }


def write_benchmark(
    result: dict[str, Any],
    json_path: str | Path = "results/benchmark.json",
    markdown_path: str | Path = "results/BENCHMARK.md",
) -> dict[str, str]:
    """Write deterministic machine- and human-readable benchmark reports."""
    json_path = Path(json_path)
    markdown_path = Path(markdown_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)

    json_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    point = result["point_estimate"]
    status = result["mapping_status"]
    uncertainty = result["uncertainty"]
    synergy = result.get("synergy_robustness")

    markdown = [
        "# Maximum Scientific Outcome Benchmark",
        "",
        "## Point estimate",
        "",
        f"- Unity proxy: `{point['unity']:.8f}`",
        f"- Entropy cost: `{point['entropy_cost']:.4f}`",
        f"- Attunement at delta = 0: `{point['attunement_delta_zero']:.6f}`",
        f"- Best bounded attunement: `{point['best_attunement']:.6f}`",
        "",
        "## Mapping status",
        "",
        f"- Before calibration: `{status['before_calibration']}`",
        f"- After best calibration: `{status['after_best_calibration']}`",
        f"- Calibration changes status: `{status['calibration_changes_status']}`",
        "",
        "## Uncertainty",
        "",
        f"- Bootstrap 95% interval: `[{uncertainty['lower']:.6f}, {uncertainty['upper']:.6f}]`",
        f"- Bootstrap mean: `{uncertainty['mean']:.6f}`",
        "",
    ]

    if synergy is not None:
        exp_u = synergy["expansion_uncertainty"]
        markdown.extend([
            "## Synergy expansion robustness",
            "",
            f"- Reported status: `{synergy['reported_status']}`",
            f"- Expansion 95% interval: `[{exp_u['lower']:.6f}, {exp_u['upper']:.6f}]`",
            f"- Status stable under uncertainty: `{synergy['status_stable_under_uncertainty']}`",
            f"- Margin to nearest threshold: `{synergy['margin_to_nearest_threshold']:.6f}` "
            f"(`{synergy['margin_in_standard_deviations']:.2f}` standard deviations)",
            f"- Fecundity minus attunement: `{synergy['fecundity_minus_attunement']:.2e}` "
            f"(identity: `{synergy['fecundity_minus_attunement_identity']}`)",
            "",
        ])

    markdown.extend([
        "## Non-claims",
        "",
    ])
    markdown.extend(f"- {claim}" for claim in result["preregistration"]["non_claims"])
    markdown.append("")

    markdown_path.write_text("\n".join(markdown), encoding="utf-8")

    return {
        "json": str(json_path),
        "markdown": str(markdown_path),
    }


def main() -> None:
    result = maximum_scientific_outcome(
        unity=0.99999995,
        cost=0.9553,
        empathy=0.5503,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
