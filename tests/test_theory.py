# test_theory.py
#
# Tests for faggin_theory.py (the theory as data + the honesty guards).
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)

import pathlib

import faggin_theory as ft


def test_theory_author_is_faggin():
    """The theory is Faggin's; the bridge is Jean's."""
    assert ft.THEORY["theory_author"] == "Federico Faggin"
    assert "D'Ariano" in ft.THEORY["collaborator"]
    assert ft.THEORY["name"] == "Quantum Information Panpsychism (QIP)"


def test_theory_cites_the_paper_and_books():
    """The formal statement (arXiv:2012.06580) and both books are cited."""
    assert "arXiv:2012.06580" in ft.citation()
    assert "Irreducible" in ft.citation()
    titles = [w["title"] for w in ft.THEORY["works"]]
    assert any("Silicon" in t for t in titles)
    assert any("Irreducible" in t for t in titles)
    assert any(w.get("identifier") == "arXiv:2012.06580"
               for w in ft.THEORY["works"])


def test_every_claim_carries_a_status():
    """No claim in the theory data is presented without a status."""
    for claim in ft.THEORY["claims"]:
        assert claim["status"] in ("interpretive", "mapped", "unmeasured")
        assert claim["claim"]
        assert claim["note"]


def test_gravity_is_marked_unmeasured():
    """Gravity has no model here; the claim is marked unmeasured."""
    gravity = [c for c in ft.THEORY["claims"]
               if c["id"] == "gravity-orch-or"]
    assert len(gravity) == 1
    assert gravity[0]["status"] == "unmeasured"
    assert gravity[0]["bridge"] is None


def test_no_conscious_computer_claim():
    """The bridge is classical code: on Faggin's account it has no interior."""
    claim = [c for c in ft.THEORY["claims"]
             if c["id"] == "no-conscious-computers"]
    assert len(claim) == 1
    assert claim[0]["status"] == "interpretive"


def test_mapping_table_covers_every_piece():
    """The mapping table names a source repo (or 'none') for every piece."""
    for row in ft.mapping_table():
        assert row["faggin_concept"]
        assert row["bridge_quantity"]
        assert row["source_repo"]
        assert row["number"]


def test_no_private_theory_in_the_code():
    """Guard: no module in this package uses or cites the private
    theory. The exclusion is stated in the README as a boundary,
    but the code itself must not contain it."""
    root = pathlib.Path(__file__).resolve().parent.parent
    for path in sorted(root.glob("*.py")):
        text = path.read_text(encoding="utf-8").lower()
        assert "tisu" not in text, f"{path.name} mentions the private theory"
        assert "belkadi" not in text, f"{path.name} mentions Belkadi"
        assert "stress-test" not in text, f"{path.name} mentions stress-test"
