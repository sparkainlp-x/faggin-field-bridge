# bridge.py
#
# The bridge: observer -> calibrator -> attunement -> mapping status.
#
# Wiring:
#   1. The Yang Observer measures unity U and entropy cost C.
#   2. The Yin Calibrator sweeps its bounded delta and finds the
#      best attunement.
#   3. Attunement A is computed at delta = 0 and at the best delta.
#   4. The mapping status labels the result and reports the empathy gate.
#
# Mapping status labels:
#   - DISSONANT: A < 0 (the entropy cost exceeds unity).
#   - PARTIAL: 0 <= A < 0.5 (unity exceeds cost, weakly).
#   - ATTUNED: A >= 0.5 and empathy E >= 0.5 (unity clearly
#     exceeds cost, and the empathy proxy meets its gate).
#   - ATTUNED-LOW-EMPATHY: A >= 0.5 but E < 0.5.
#
# The thresholds 0.5 are chosen cut points of this bridge, not
# measured constants. They are stated here so they can be argued
# with, not hidden.
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""The Faggin field bridge: observer -> calibrator -> attunement.

Theory author: Federico Faggin. Bridge / test author:
Jean-Francois Brisson (Spark AI NLP). The bridge is a classical
computation on synthetic states; on Faggin's own account it has
no interior. It computes quantities; it does not feel them.
"""

import attunement as at
import cost
import unity


# ---------------------------------------------------------------------------
# Mapping status thresholds (chosen cut points of this bridge, not measured)
# ---------------------------------------------------------------------------

ATTUNEMENT_THRESHOLD = 0.5
EMPATHY_GATE = at.EMPATHY_GATE


def mapping_status(attunement_value, empathy):
    """Label an (attunement, empathy) pair.

    Returns a dict with the label, the values, and whether the
    empathy gate is met. Labels: DISSONANT (A < 0), PARTIAL
    (0 <= A < 0.5), ATTUNED (A >= 0.5 and E >= 0.5),
    ATTUNED-LOW-EMPATHY (A >= 0.5 and E < 0.5).
    """
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
    """Run the full bridge on one (unity, cost) pair.

    1. The observer measures (U, C) and A at delta = 0.
    2. The calibrator sweeps its bounded delta for the best A.
    3. The mapping status labels the best-calibrated attunement.
    Returns a dict with every step's result. Nothing here is
    stored between calls.
    """
    observer = at.AttunementObserver()
    calibrator = at.AttunementCalibrator()
    obs = observer.observe(unity_value, cost_value)
    best_delta, best_a = calibrator.best_delta(
        obs.unity, obs.cost
    )
    cal = calibrator
    cal.set_delta(best_delta)
    return {
        "observation": obs,
        "uncalibrated_attunement": obs.attunement,
        "best_delta": best_delta,
        "best_attunement": best_a,
        "calibrated_attunement": cal.calibrated_attunement(
            obs.unity, obs.cost
        ),
        "empathy": at.empathy_proxy(empathy),
        "mapping_status": mapping_status(best_a, empathy),
    }


def bridge_from_entropy(unity_value, entropy_bits, max_entropy_bits,
                        empathy=None):
    """Run the bridge from a measured entropy instead of a cost.

    The observer normalizes the entropy into the cost itself.
    """
    observer = at.AttunementObserver()
    obs = observer.observe_from_entropy(
        unity_value, entropy_bits, max_entropy_bits
    )
    return bridge(obs.unity, obs.cost, empathy=empathy)


def worked_example():
    """The bridge's worked examples, with the reproduced numbers.

    Primary: unity = de Broglie spooky (0.99999995, reproduced
    exactly), cost = tensor-membrane entropy (0.9553, reproduced).
    Secondary: the Omega-Genesis numbers (spooky 0.9005 reported,
    synthetic reproduction 0.837) with the same cost, to show how
    the mapping status moves when the unity is the notebook's instead of
    the de Broglie repo's.
    """
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
    """Print the bridge's worked examples."""
    print("Faggin field bridge -- observer -> calibrator -> attunement")
    print()
    ex = worked_example()
    for name, result in ex.items():
        obs = result["observation"]
        print(f"{name}:")
        print(f"  unity U = {obs.unity:.8f}, cost C = {obs.cost:.4f}")
        print(f"  A(delta = 0) = {result['uncalibrated_attunement']:.4f}")
        print(f"  best delta = {result['best_delta']:.2f}, "
              f"A(best) = {result['best_attunement']:.4f}")
        print(f"  empathy E = {result['empathy']:.4f} "
              f"(gate {EMPATHY_GATE}: "
              f"{'met' if result['mapping_status']['empathy_gate_met'] else 'not met'})")
        print(f"  MAPPING STATUS: {result['mapping_status']['label']}")
        print()
    print("Reading: the de Broglie unity (0.99999995) is the only "
          "one high enough to cover the 0.955 entropy cost, and "
          "only barely -- PARTIAL, weak-positive. The notebook's "
          "unity (0.9005 reported, 0.837 synthetic) does not cover "
          "it even at the best delta: DISSONANT. The bounded "
          "calibrator can move A by at most 0.05 * U (~0.05); it "
          "cannot make a high-entropy state attuned. That is the "
          "bridge's honest result.")


if __name__ == "__main__":
    main()
