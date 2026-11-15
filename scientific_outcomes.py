# scientific_outcomes.py
#
# Maximum-scientific-outcomes logic for the Faggin Field Bridge.
#
# This module adds reproducibility, uncertainty, sensitivity,
# preregistration, provenance, and benchmark reporting. It does NOT
# test consciousness, validate Quantum Information Panpsychism, or
# measure quantum entanglement.
#
# SPDX-License-Identifier: AGPL-3.0-only

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
from bridge import bridge


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
    """One-at-a-time sensitivity of attunement to its inputs."""
    base = validate_inputs(unity, cost)

    def sweep(name: str, values: Iterable[float], apply: Callable[[float], float]) -> list[dict[str, float]]:
        rows = []
        for change in values:
            u = apply(change)
            a = attunement(u, base["cost"], base["delta"])
            rows.append({
                "parameter": name,
                "change": float(change),
                "value": float(u),
                "attunement": float(a),
            })
        return rows

    return {
        "unity": sweep(
            "unity",
            unity_range,
            lambda x: _clip(base["unity"] + x, 0.0, 1.0),
        ),
        "cost": sweep(
            "cost",
            cost_range,
            lambda x: _clip(base["cost"] + x, 0.0, 1.0),
        ),
        "delta": sweep(
            "delta",
            delta_range,
            lambda x: _clip(x, DELTA_MIN, DELTA_MAX),
        ),
    }


def robustness(
    unity: float,
    cost: float,
    empathy: float = 0.5503,
    n_boot: int = 2000,
    seed: int = 42,
) -> dict[str, Any]:
    """Assess whether the mapping status is stable under measurement noise."""
    result = bridge(unity, cost, empathy=empathy)
    before = result["mapping_status"]["label"]
    uncertainty = bootstrap_attunement(unity, cost, n_boot=n_boot, seed=seed)

    lower_status = "DISSONANT" if uncertainty["lower"] < 0 else "PARTIAL"
    upper_status = "DISSONANT" if uncertainty["upper"] < 0 else "PARTIAL"

    return {
        "reported_status": before,
        "attunement_uncertainty": uncertainty,
        "status_at_lower_bound": lower_status,
        "status_at_upper_bound": upper_status,
        "status_stable_under_uncertainty": lower_status == upper_status,
        "sign_flip_possible": uncertainty["lower"] < 0 <= uncertainty["upper"],
        "calibration_can_rescue": result["best_attunement"] >= 0.5,
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
            "ATTUNED_LOW_EMPATHY": "A >= 0.5 and empathy < 0.5",
        },
        "calibration_bound": [DELTA_MIN, DELTA_MAX],
        "success_criterion": "Reproduce the declared input values and report uncertainty and sensitivity.",
        "non_claims": [
            "This does not test consciousness.",
            "This does not measure quantum entanglement.",
            "This does not validate Faggin's Quantum Information Panpsychism.",
            "Thresholds are repository conventions, not measured constants.",
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

    # Recompute the uncalibrated status directly.
    uncalibrated_a = attunement(validated["unity"], validated["cost"], 0.0)
    if uncalibrated_a < 0:
        uncalibrated_status = "DISSONANT"
    elif uncalibrated_a < 0.5:
        uncalibrated_status = "PARTIAL"
    else:
        uncalibrated_status = "ATTUNED" if empathy >= 0.5 else "ATTUNED_LOW_EMPATHY"

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
            "entanglement_measured": False,
            "faggin_endorsed": False,
            "mapping_reproduced": True,
        },
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
        "## Non-claims",
        "",
    ]
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
