#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# ///
#
# SPDX-FileCopyrightText: 2026 Adam Fidel
# SPDX-License-Identifier: MIT
"""Check that every TOML example embedded in a specification document parses.

Each ```toml fence is parsed on its own. A fence preceded by the comment

    <!-- toml-check: invalid -->

is a deliberate counterexample and MUST fail to parse instead.

Untagged fences that look like TOML are reported as notes, since an example
that is not tagged ```toml is not checked by anything.
"""

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DOCS = [ROOT / "DECK.md", ROOT / "ESOTERICA.md"]

FENCE = re.compile(r"^```(\w*)[^\n]*\n(.*?)^```", re.S | re.M)
INVALID_MARKER = re.compile(r"<!--\s*toml-check:\s*invalid\s*-->\s*\Z")

# A first meaningful line of `[table]` or `key = ...`.
LOOKS_LIKE_TOML = re.compile(r"^\s*(?:\[[\w.\"-]+\]|[\w.\"-]+\s*=)", re.M)


def fences(text):
    """Yield (line, language, body, expect_invalid) for every fence."""
    for m in FENCE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        yield line, m.group(1), m.group(2), bool(INVALID_MARKER.search(text[:m.start()]))


def strip_comments(body):
    return "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("#"))


def main():
    checked = 0
    failures, notes = [], []
    for doc in DOCS:
        text = doc.read_text(encoding="utf-8")

        for line, lang, body, expect_invalid in fences(text):
            if lang != "toml":
                if lang == "" and LOOKS_LIKE_TOML.search(strip_comments(body)):
                    notes.append(f"  {doc.name}:{line} untagged fence looks like TOML")
                continue

            checked += 1
            try:
                tomllib.loads(body)
            except tomllib.TOMLDecodeError as e:
                if not expect_invalid:
                    failures.append(f"  {doc.name}:{line} does not parse: {e}")
            else:
                if expect_invalid:
                    failures.append(f"  {doc.name}:{line} marked invalid but parses")

    print(f"{checked} toml fences in {', '.join(d.name for d in DOCS)}")
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
