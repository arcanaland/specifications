#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# ///
#
# SPDX-FileCopyrightText: 2026 Adam Fidel
# SPDX-License-Identifier: MIT
"""Build the specification documents as PDFs via pandoc and Typst.
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "tools" / "spec.typ"
BUILD_DIR = ROOT / "build"

DOCS = {
    "DECK.md": ("Tarot Deck Specification", "Version 2.0 (Draft)"),
    "ESOTERICA.md": ("Tarot Esoterica Specification", "Version 1.0 (Draft)"),
}

READER = "gfm"

LEADING_H1 = re.compile(r"\A\s*#\s+\S[^\n]*\n")


def provenance() -> str:
    """A short 'branch @ commit' string, marked when the tree is dirty.
    """

    def git(*args: str) -> str | None:
        try:
            out = subprocess.run(
                ["git", "-C", str(ROOT), *args],
                capture_output=True,
                text=True,
                check=True,
            )
        except (OSError, subprocess.CalledProcessError):
            return None
        return out.stdout.strip()

    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    commit = git("rev-parse", "--short", "HEAD")
    if not branch or not commit:
        return "no git metadata"

    dirty = git("status", "--porcelain")
    suffix = "-dirty" if dirty else ""
    return f"{branch} @ {commit}{suffix}"


def build(doc: Path, out_dir: Path, *, watermark: bool, prov: str) -> bool:
    title, subtitle = DOCS[doc.name]
    out = out_dir / f"{doc.stem.lower()}.pdf"

    source = LEADING_H1.sub("", doc.read_text(encoding="utf-8"), count=1)

    cmd = [
        "pandoc",
        "-f", READER,
        "-t", "pdf",
        "--pdf-engine=typst",
        "--pdf-engine-opt=--input",
        f"--pdf-engine-opt=draft={'true' if watermark else 'false'}",
        "--template", str(TEMPLATE),
        "--metadata", f"title={title}",
        "--metadata", f"subtitle={subtitle}",
        "--metadata", f"date={date.today().isoformat()}",
        "--metadata", f"provenance={prov}",
        "-o", str(out),
    ]

    result = subprocess.run(cmd, input=source, text=True, capture_output=True)
    if result.returncode != 0:
        sys.stderr.write(f"FAIL {doc.name}\n")
        sys.stderr.write(result.stderr)
        # Typst reports against the generated source, which pandoc writes to a
        # temporary file, so its line numbers do not map back to the markdown.
        if "does not exist in the document" in result.stderr:
            sys.stderr.write(
                f"\nhint: a label that does not exist is a cross-reference in {doc.name}\n"
                "      pointing at a heading that is not there. Search the markdown for the\n"
                "      anchor named above; line numbers in the error are the generated Typst.\n"
            )
        return False

    if result.stderr.strip():
        sys.stderr.write(result.stderr)

    size = out.stat().st_size
    print(f"ok   {doc.name} -> {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}"
          f" ({size / 1024:.0f} KB)")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "docs", nargs="*", default=list(DOCS),
        help=f"documents to build (default: {', '.join(DOCS)})",
    )
    parser.add_argument(
        "--final", action="store_true",
        help="build without the DRAFT watermark",
    )
    parser.add_argument(
        "--check", action="store_true",
        help="build to a temporary directory and discard the output",
    )
    args = parser.parse_args()

    missing = [t for t in ("pandoc", "typst") if shutil.which(t) is None]
    if missing:
        sys.stderr.write(
            f"{' '.join(missing)} not found."
        )
        return 2

    docs = []
    for name in args.docs:
        doc = ROOT / Path(name).name
        if doc.name not in DOCS:
            sys.stderr.write(f"{doc.name}: not a specification document ({', '.join(DOCS)})\n")
            return 2
        if not doc.is_file():
            sys.stderr.write(f"{doc}: no such file\n")
            return 2
        docs.append(doc)

    prov = provenance()

    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp) if args.check else BUILD_DIR
        out_dir.mkdir(parents=True, exist_ok=True)
        ok = all([build(d, out_dir, watermark=not args.final, prov=prov) for d in docs])

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
