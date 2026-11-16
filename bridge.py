# bridge.py
#
# The bridge: observer -> calibrator -> attunement -> mapping status.
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import attunement as at
import cost
import unity

# No headline claim is emitted by this package. The claims below
# are measured statements with pre-registered rules, not headlines.
HEADLINE_ALLOWED = False


ATTUNEMENT_THRESHOLD = 0.5
EMPATHY_GATE = at.EMPATHY_GATE


def mapping_status(attunement_value, empathy):
    """Classify an attunement and empathy-proxy pair."""
    a = float(attunement_value)
    e = at.empathy_proxy(empathy)

    if a < 0.0:
        label = "DISSONANT"
    elif a < ATTUNEMENT_THRESHOLD:
        label = "PARTIAL"
    elif e >= EMPATHY_GATE:
        label = "ATTUNED"
    else:
        label = "ATTUNED-LOW-EMPATHY"

    return {
        "label": label,
        "attunement": a,
        "empathy": e,
        "empathy_gate": EMPATHY_GATE,
        "empathy_gate_met": e >= EMPATHY_GATE,
        "attunement_threshold": ATTUNEMENT_THRESHOLD,
    }


def bridge(unity_value, cost_value, empathy=None):
    """Run observer, calibrator, attunement, and mapping status."""
    observer = at.AttunementObserver()
    calibrator = at.AttunementCalibrator()

    observation = observer.observe(unity_value, cost_value)
    best_delta, best_attunement = calibrator.best_delta(
        observation.unity,
        observation.cost,
    )
    calibrator.set_delta(best_delta)

    before = mapping_status(observation.attunement, empathy)
    after = mapping_status(best_attunement, empathy)

    return {
        "observation": observation,
        "uncalibrated_attunement": observation.attunement,
        "best_delta": best_delta,
        "best_attunement": best_attunement,
        "calibrated_attunement": calibrator.calibrated_attunement(
            observation.unity,
            observation.cost,
        ),
        "empathy": at.empathy_proxy(empathy),
        "status_before_calibration": before["label"],
        "status_after_calibration": after["label"],
        "calibration_changes_status": before["label"] != after["label"],
        "mapping_status": after,
    }


def bridge_from_entropy(
    unity_value,
    entropy_bits,
    max_entropy_bits,
    empathy=None,
):
    """Run the bridge from an entropy measurement."""
    observer = at.AttunementObserver()
    observation = observer.observe_from_entropy(
        unity_value,
        entropy_bits,
        max_entropy_bits,
    )
    return bridge(observation.unity, observation.cost, empathy=empathy)


def quantum_thought_claims():
    """The four quantum-thought claims (i)-(iv), measured fresh.

    (i)   entanglement measured as a real quantum quantity
          (thought_entanglement.py): concurrence of a two-thought
          Bell state, computed exactly.
    (ii)  coherence half-life measured (thought.py).
    (iii) collapse cost measured (thought.py).
    (iv)  self-knowing measured via D (self_knowing.py).

    Each claim carries its pre-registered rule and verdict. No
    headline claim is emitted: HEADLINE_ALLOWED is False.
    """
    import self_knowing
    import thought
    import thought_entanglement as te

    claim_i = te.claim_entanglement_verdict()
    claim_ii = thought.claim_coherence_verdict()
    claim_iii = thought.claim_collapse_verdict()
    claim_iv = self_knowing.claim_self_knowing_verdict()
    verdicts = [claim_i, claim_ii, claim_iii, claim_iv]
    return {
        "headline_allowed": HEADLINE_ALLOWED,
        "claim_i_entanglement": claim_i,
        "claim_ii_coherence": claim_ii,
        "claim_iii_collapse": claim_iii,
        "claim_iv_self_knowing": claim_iv,
        "n_claims": len(verdicts),
        "n_passed": sum(1 for v in verdicts if v["passed"]),
        "all_pass": all(v["passed"] for v in verdicts),
    }


def worked_example():
    """Return the primary and Omega-Genesis worked examples."""
    primary = bridge_from_entropy(
        unity.debroglie_spooky(),
        cost.tensor_membrane_mean_entropy(),
        1.0,
        empathy=unity.OMEGA_GENESIS_EMPATHY_REPORTED,
    )

    omega_reported = bridge(
        unity.OMEGA_GENESIS_SPOOKY_REPORTED,
        cost.tensor_membrane_cost(),
        empathy=unity.OMEGA_GENESIS_EMPATHY_REPORTED,
    )

    omega_synthetic = bridge(
        unity.omega_genesis_spooky(),
        cost.tensor_membrane_cost(),
        empathy=unity.OMEGA_GENESIS_EMPATHY_REPORTED,
    )

    return {
        "primary_debroglie_tensor": primary,
        "omega_reported": omega_reported,
        "omega_synthetic": omega_synthetic,
    }


def main():
    """Print the worked examples and mapping statuses."""
    print("Faggin field bridge -- observer -> calibrator -> attunement")
    print()

    for name, result in worked_example().items():
        observation = result["observation"]
        print(f"{name}:")
        print(f"  unity U = {observation.unity:.8f}")
        print(f"  entropy cost C = {observation.cost:.4f}")
        print(f"  A(delta = 0) = {result['uncalibrated_attunement']:.4f}")
        print(f"  best delta = {result['best_delta']:.2f}")
        print(f"  best A = {result['best_attunement']:.4f}")
        print(f"  status before calibration = {result['status_before_calibration']}")
        print(f"  status after calibration = {result['status_after_calibration']}")
        print(f"  calibration changes status = {result['calibration_changes_status']}")
        print()


if __name__ == "__main__":
    main()
