#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["abnf>=2.2"]
# ///
#
# SPDX-FileCopyrightText: 2026 Adam Fidel
# SPDX-License-Identifier: MIT
"""Check the ABNF grammar embedded in DECK.md against a corpus of cases.
"""

import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")  # DIGIT redefines the core rule
from abnf.parser import Rule  # noqa: E402

DOC = Path(__file__).resolve().parent.parent / "DECK.md"

"""
A case is (rule, string, expected). `expected` is one of:

  ACCEPT  the grammar matches the whole string and the spec agrees
  REJECT  the grammar does not match and the spec agrees
  LOOSE   the grammar matches, but a normative rule outside the grammar
          would reject the string
"""
ACCEPT, REJECT, LOOSE = "ACCEPT", "REJECT", "LOOSE"
CASES = [
    # ---- canonical IDs -------------------------------------------------
    ("canonical-id", "major_arcana.00", ACCEPT),
    ("canonical-id", "major_arcana.21", ACCEPT),
    ("canonical-id", "minor_arcana.wands.ace", ACCEPT),
    ("canonical-id", "minor_arcana.pentacles.king", ACCEPT),
    ("canonical-id", "major_arcana.happy_squirrel", ACCEPT),
    ("canonical-id", "minor_arcana.stars.ace", ACCEPT),
    ("canonical-id", "major_arcana.22", ACCEPT),
    ("canonical-id", "major_arcana.99", ACCEPT),

    # case sensitivity
    ("canonical-id", "MAJOR_ARCANA.00", REJECT),
    ("canonical-id", "minor_arcana.WANDS.ace", REJECT),
    ("canonical-id", "minor_arcana.wands.ACE", REJECT),

    # structure
    ("canonical-id", "major_arcana", REJECT),
    ("canonical-id", "major_arcana.", REJECT),
    ("canonical-id", "minor_arcana.wands", REJECT),
    ("canonical-id", "major_arcana.0", REJECT),
    ("canonical-id", "major_arcana.000", REJECT),
    ("canonical-id", "major_arcana.6", REJECT),

    # a custom name must not be a reserved canonical key
    ("canonical-id", "minor_arcana.stars.page", LOOSE),

    # ---- card references -----------------------------------------------
    # the suffix is optional: a bare canonical ID is a card-ref
    ("card-ref", "major_arcana.06", ACCEPT),
    ("card-ref", "major_arcana.06:two_women", ACCEPT),
    ("card-ref", "minor_arcana.cups.ace:alt", ACCEPT),
    ("card-ref", "major_arcana.happy_squirrel:dark", ACCEPT),
    ("card-ref", "major_arcana.06:", REJECT),
    ("card-ref", "major_arcana.06:two.women", REJECT),
    ("card-ref", "major_arcana.06:Two_Women", REJECT),

    # ---- variant references --------------------------------------------
    # the form name files key [card_variants] by; the suffix is mandatory
    ("variant-ref", "major_arcana.06:two_women", ACCEPT),
    ("variant-ref", "minor_arcana.cups.ace:alt", ACCEPT),
    ("variant-ref", "major_arcana.06", REJECT),
    ("variant-ref", "major_arcana.06:", REJECT),
    ("variant-ref", "major_arcana.06:two.women", REJECT),

    ("variant-suffix", ":two_women", ACCEPT),
    ("variant-suffix", ":alt", ACCEPT),
    ("variant-suffix", ":", REJECT),
    ("variant-suffix", "two_women", REJECT),
    ("variant-suffix", ":two_women:more", REJECT),

    # ---- custom names --------------------------------------------------
    ("custom-name", "happy_squirrel", ACCEPT),
    ("custom-name", "two_women", ACCEPT),
    ("custom-name", "_leading", ACCEPT),
    ("custom-name", "a1", ACCEPT),
    ("custom-name", "1a", REJECT),      # must not start with a digit
    ("custom-name", "22", REJECT),
    ("custom-name", "Happy", REJECT),
    ("custom-name", "has-hyphen", REJECT),
    ("custom-name", "has.dot", REJECT),
    ("custom-name", "", REJECT),
    ("custom-name", "page", LOOSE),     # reserved canonical key
    ("custom-name", "wands", LOOSE),

    # ---- realms --------------------------------------------------------
    ("realm", "land.arcana", ACCEPT),
    ("realm", "my.personal.domain", ACCEPT),
    ("realm", "land.arcana.cartomancer", ACCEPT),
    ("realm", "example.xn--bcher-kva", ACCEPT),
    ("realm", "a.b", ACCEPT),
    ("realm", "x1-2.example", ACCEPT),
    ("realm", "land", REJECT),          # single label: catches [app.land.arcana]
    ("realm", "LAND.ARCANA", REJECT),
    ("realm", "land.arcana.TarotCanvas", REJECT),
    ("realm", "land.arcana.", REJECT),
    ("realm", ".land.arcana", REJECT),
    ("realm", "land..arcana", REJECT),
    ("realm", "-land.arcana", REJECT),
    ("realm", "land-.arcana", REJECT),
    ("realm", "1and.arcana", REJECT),   # RFC 1035: labels start with a letter
    ("realm", "land.arcana/deck/x", REJECT),
    ("realm", "a" * 64 + ".example", REJECT),  # 63-octet label cap
    ("realm", "a" * 63 + ".example", ACCEPT),

    # ---- qualified identifiers -----------------------------------------
    ("qualified-id", "land.arcana/deck/rider-waite-smith", ACCEPT),
    ("qualified-id", "land.arcana/spread/celtic-cross", ACCEPT),
    ("qualified-id", "my.personal.domain/deck/modern-witch-tarot", ACCEPT),
    ("qualified-id", "land.arcana/deck/rws#major_arcana.00", ACCEPT),
    ("qualified-id", "land.arcana/deck/rws#major_arcana.06:two_women", ACCEPT),
    ("qualified-id", "land.arcana/deck", ACCEPT),
    ("qualified-id", "land.arcana/", REJECT),
    ("qualified-id", "land.arcana", REJECT),
    ("qualified-id", "/deck/rws", REJECT),
    ("qualified-id", "land.arcana/deck/rider_waite", REJECT),  # no _ in segments
    ("qualified-id", "land.arcana/deck/RWS", REJECT),
    ("qualified-id", "https://land.arcana/deck/rws", REJECT),
    ("qualified-id", "land.arcana/deck/rws#", REJECT),
    ("qualified-id", "land.arcana/deck/rws#not-a-card", LOOSE),
    ("qualified-id", "id.fidel.shelf/deck/example-tarot", ACCEPT),
    ("qualified-id", "id.example/esoterica/references/books/example-book", ACCEPT),

    # requires a deck's type segment to be `deck`
    ("qualified-id", "land.arcana/deck-archive/foo", LOOSE),

    # ---- path segments -------------------------------------------------
    ("segment", "deck", ACCEPT),
    ("segment", "rider-waite-smith", ACCEPT),
    ("segment", "x-collection-notes", ACCEPT),
    ("segment", "a", ACCEPT),
    ("segment", "2024", ACCEPT),          # unlike a label, a segment may lead with a digit
    ("segment", "-deck", REJECT),
    ("segment", "deck-", REJECT),
    ("segment", "-", REJECT),
    ("segment", "de--ck", ACCEPT),
    ("segment", "deck_two", REJECT),
    ("segment", "Deck", REJECT),
    ("segment", "deck/x", REJECT),
]


def load_grammar():
    text = DOC.read_text(encoding="utf-8")
    fences = re.findall(r"```abnf\n(.*?)```", text, re.S)
    if len(fences) != 1:
        sys.exit(f"expected exactly one ```abnf fence in {DOC.name}, found {len(fences)}")

    class Grammar(Rule):
        pass

    # RFC 5234 rulelists are CRLF-delimited.
    Grammar.load_grammar(fences[0].replace("\n", "\r\n"))
    return Grammar


def matches(grammar, rule, text):
    """True when `rule` matches the whole of `text`."""
    try:
        _, consumed = grammar(rule).parse(text, 0)
    except Exception:
        return False
    return consumed == len(text)


def main():
    grammar = load_grammar()
    defined = {r.name for r in grammar.rules()}

    failures, notes = [], []
    for rule, text, expected in CASES:
        if rule not in defined:
            failures.append(f"  no such rule {rule!r} (grammar defines {sorted(defined)})")
            continue
        got = matches(grammar, rule, text)
        if expected is ACCEPT and not got:
            failures.append(f"  {rule:14} {text!r} should parse, did not")
        elif expected is REJECT and got:
            failures.append(f"  {rule:14} {text!r} parsed, should not have")
        elif expected is LOOSE and not got:
            notes.append(f"  {rule:14} {text!r} parses but has further reqs")

    print(f"{len(CASES)} cases over {len(defined)} rules")
    if notes:
        print("\nnotes:")
        print("\n".join(notes))
    if failures:
        print(f"\n{len(failures)} FAILED:")
        print("\n".join(failures))
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
