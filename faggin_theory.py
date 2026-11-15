# faggin_theory.py
#
# Federico Faggin's theory of consciousness, recorded as data.
#
# This module makes NO physics claims. It records what Faggin
# claims, where he published it, and how each claim maps (or does
# not map) onto a measurable quantity in this bridge. Faggin's
# metaphysical claims -- that quantum fields ARE conscious -- are
# an interpretation. They are NOT tested here. What this package
# tests is the mapping: the bridge's measurable quantities
# (unity, entropy cost, attunement, calibration) are defined in
# attunement.py, unity.py and cost.py, and they are classical
# computations on synthetic states.
#
# Theory author: Federico Faggin (with Giacomo Mauro D'Ariano).
# Bridge / test author: Jean-Francois Brisson (Spark AI NLP).
# Faggin has not reviewed or endorsed this software.
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

"""Federico Faggin's theory of consciousness, as data.

Faggin -- co-inventor of the MOS silicon-gate technology (1968)
and designer of the Intel 4004, the first commercial
microprocessor (1971) -- argues that consciousness is not an
emergent product of brains or computation but a fundamental
property of quantum fields. The theory is Quantum Information
Panpsychism (QIP), developed with the physicist Giacomo Mauro
D'Ariano (University of Pavia).

Every claim below carries a status. "interpretive" means the
claim is a philosophical interpretation of quantum physics, not
a measured result, and this package does not test it. "mapped"
means the claim has a bridge quantity defined elsewhere in this
package -- and the mapping is explicitly a code quantity, not a
proof of the claim.
"""

# ---------------------------------------------------------------------------
# The theory, as data
# ---------------------------------------------------------------------------

THEORY = {
    "name": "Quantum Information Panpsychism (QIP)",
    "theory_author": "Federico Faggin",
    "collaborator": "Giacomo Mauro D'Ariano (University of Pavia)",
    "works": [
        {
            "title": "Silicon: From the Invention of the "
                     "Microprocessor to the New Science of "
                     "Consciousness",
            "kind": "memoir",
            "year": 2021,
            "note": "Faggin's memoir; the consciousness argument "
                    "is developed in its later chapters.",
        },
        {
            "title": "Irreducible: Consciousness, Life, Computers, "
                     "and Human Nature",
            "kind": "book",
            "publisher": "Essentia Books",
            "year": 2024,
            "note": "The book-length statement of the theory, for "
                    "a general audience.",
        },
        {
            "title": "Quantum Information Panpsychism",
            "kind": "paper",
            "authors": "Federico Faggin and Giacomo Mauro D'Ariano",
            "identifier": "arXiv:2012.06580",
            "year": 2020,
            "note": "The formal statement; quantum theory derived "
                    "from informational axioms, with an interior "
                    "attached to the quantum information.",
        },
        {
            "title": "Hard Problem and Free Will: an "
                     "information-theoretical approach",
            "kind": "paper",
            "authors": "Federico Faggin and Giacomo Mauro D'Ariano",
            "note": "The earlier paper: information is felt from "
                    "the inside by the system that holds it.",
        },
    ],
    "claims": [
        {
            "id": "conscious-fields",
            "claim": "Consciousness is a fundamental property of "
                     "quantum fields, present from the beginning "
                     "of the universe; it does not emerge from "
                     "brains or computation.",
            "status": "interpretive",
            "bridge": None,
            "note": "Not tested here. No experiment has "
                    "demonstrated a conscious quantum field.",
        },
        {
            "id": "entanglement-unity",
            "claim": "Entanglement is the basis of the unity of "
                     "experience: a composite quantum system cannot "
                     "be factored into its parts, so the whole is "
                     "one unified state. This resolves the "
                     "combination problem of panpsychism.",
            "status": "interpretive",
            "bridge": "unity",
            "note": "Mapped, not proved. The bridge's unity metric "
                    "is spooky correlation -- self-similarity under "
                    "noise -- which is NOT entanglement. The mapping "
                    "borrows Faggin's word 'unity' for a classical "
                    "code quantity; it does not measure entanglement.",
        },
        {
            "id": "free-will",
            "claim": "Free will is real: the unpredictable outcomes "
                     "of quantum events are genuine free choices, "
                     "not just randomness. A deterministic quantum "
                     "computer cannot support free-will decisions.",
            "status": "interpretive",
            "bridge": "calibrator",
            "note": "Mapped as an analogy only. The bridge's "
                    "calibrator freely chooses one scalar delta "
                    "inside a bounded range; that choice is not "
                    "determined by the measurement. This is an "
                    "operational analogue, not a measurement of "
                    "free will.",
        },
        {
            "id": "love-attunement",
            "claim": "Love / attunement is a fundamental feature "
                     "of the conscious field: the felt sense of "
                     "connection between conscious entities, the "
                     "deepest expression of their oneness.",
            "status": "interpretive",
            "bridge": "attunement",
            "note": "Mapped as a code quantity. The bridge defines "
                    "attunement A = unity minus a normalized "
                    "entropy cost. A is a number computed from a "
                    "synthetic state, not a human feeling, and the "
                    "empathy value is a supplied proxy, not a "
                    "measured human property.",
        },
        {
            "id": "no-conscious-computers",
            "claim": "A machine can process symbols brilliantly, "
                     "but there is nobody inside to feel them: "
                     "symbols and qualia belong to different kinds "
                     "of reality, so a (classical or quantum) "
                     "computer cannot be conscious.",
            "status": "interpretive",
            "bridge": "scope",
            "note": "Accepted as a scope limit. This bridge is "
                    "classical code running on a classical machine, "
                    "so on Faggin's own account it has no interior. "
                    "It computes quantities; it does not feel them.",
        },
        {
            "id": "gravity-orch-or",
            "claim": "Gravity and consciousness: in Orch OR "
                     "(Penrose-Hameroff), consciousness sits in "
                     "gravitationally induced collapse inside "
                     "microtubules. Faggin's QIP does not invoke "
                     "gravity; consciousness is a property of the "
                     "fields themselves.",
            "status": "unmeasured",
            "bridge": None,
            "note": "No gravity model exists in this package. "
                    "Gravity enters only as this discussion note. "
                    "The notebook config's MICROTUBULE_RATIO "
                    "(0.70) is a parameter of the Omega-Genesis "
                    "simulation, not a measurement of microtubules.",
        },
    ],
    "reception": (
        "QIP is a theoretical proposal, not an experimental result. "
        "It is far from mainstream; critics note there is no "
        "evidence the universe itself is conscious, and that "
        "ordinary science explains more with fewer assumptions. "
        "Faggin himself presents the ideas as speculative in his "
        "own appendix. This package takes no side: it records the "
        "theory, builds the measurable mapping, and reports what "
        "the numbers do."
    ),
}

# The bridge's mapping table: Faggin concept -> bridge quantity ->
# the sparkainlp-x repo the quantity is taken from -> the number.
MAPPING = [
    {
        "faggin_concept": "Unity of experience (entanglement)",
        "bridge_quantity": "Spooky correlation U (mean pairwise "
                           "|dot| over 5 noisy copies)",
        "source_repo": "digital-to-wave-2-debroglie",
        "number": "0.99999995 at sigma = 0.01 (reproduced exactly)",
    },
    {
        "faggin_concept": "Unity of experience (entanglement)",
        "bridge_quantity": "Spooky correlation U, Omega-Genesis "
                           "notebook run",
        "source_repo": "sparkainlp-x-notebook-research",
        "number": "0.9005 (notebook's reported value; synthetic "
                  "reproduction 0.837, same regime, not exact)",
    },
    {
        "faggin_concept": "Entropy / disorder cost of holding a "
                          "state together",
        "bridge_quantity": "Mean single-qubit von Neumann entropy, "
                           "normalized by 1 bit",
        "source_repo": "tensor-membrane",
        "number": "0.955 bits (reproduced: 0.9553)",
    },
    {
        "faggin_concept": "Free will (choice inside a bound)",
        "bridge_quantity": "Calibrator delta in [-0.05, 0.05], "
                           "best improvement log10(1/0.95)",
        "source_repo": "digital-to-wave-2-debroglie",
        "number": "0.022276 orders (reproduced exactly)",
    },
    {
        "faggin_concept": "Love / attunement (felt connection)",
        "bridge_quantity": "Attunement A = U - C, adjusted by "
                           "delta; empathy proxy E",
        "source_repo": "this bridge (new definition)",
        "number": "A in [-1, 1]; empathy proxy default 0.5503 "
                  "(notebook's reported value, supplied, not "
                  "recomputed)",
    },
    {
        "faggin_concept": "Gravity (Orch OR microtubules)",
        "bridge_quantity": "None -- no gravity model",
        "source_repo": "none",
        "number": "UNMEASURED",
    },
]


def theory_summary():
    """The theory, as a data dict (see THEORY)."""
    return THEORY


def mapping_table():
    """The bridge's mapping table (see MAPPING)."""
    return MAPPING


def citation():
    """One-line citation for the theory's formal statement."""
    return (
        "Federico Faggin and Giacomo Mauro D'Ariano, "
        "\"Quantum Information Panpsychism\", arXiv:2012.06580. "
        "Book-length statement: Faggin, \"Irreducible: "
        "Consciousness, Life, Computers, and Human Nature\", "
        "Essentia Books, 2024. Theory author: Faggin. "
        "Bridge / test author: Jean-Francois Brisson (Spark AI NLP). "
        "Faggin has not reviewed or endorsed this software."
    )


def main():
    """Print the theory summary and the mapping table."""
    print("Faggin field bridge -- theory summary")
    print()
    print(f"Theory: {THEORY['name']}")
    print(f"Theory author: {THEORY['theory_author']}")
    print(f"Collaborator: {THEORY['collaborator']}")
    print()
    for work in THEORY["works"]:
        year = work.get("year", "n.d.")
        print(f"  - {work['title']} ({work['kind']}, {year})")
    print()
    for claim in THEORY["claims"]:
        print(f"[{claim['status']}] {claim['claim']}")
        print(f"    bridge: {claim['bridge']}; {claim['note']}")
        print()
    print("Mapping (Faggin concept -> bridge quantity -> source -> number):")
    for row in MAPPING:
        print(f"  {row['faggin_concept']}")
        print(f"    -> {row['bridge_quantity']}")
        print(f"    -> {row['source_repo']}: {row['number']}")
    print()
    print(citation())


if __name__ == "__main__":
    main()
