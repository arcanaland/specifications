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
    # Fallback titles, for a document whose header has no H1.
    "DECK.md": "Tarot Deck Specification",
    "ESOTERICA.md": "Tarot Esoterica Specification",
    "SPREAD.md": "Tarot Spread Specification",
}

READER = "gfm"

# Everything before the first `## ` heading is the document's header: its
# title, authors, publication date and version. The header is written for a
# reader on GitHub; the build reads those facts out of it, hands them to the
# template, and drops the header from the body so the PDF states them once.
FIRST_SECTION = re.compile(r"^## ", re.MULTILINE)
TITLE = re.compile(r"^#\s+(\S[^\n]*?)\s*$", re.MULTILINE)
AUTHORS = re.compile(r"^\*\*Authors?\*\*\s*\n((?:[-*]\s+[^\n]+\n?)+)", re.MULTILINE)
PUBDATE = re.compile(r"\*\*Publication Date\*\*:\s*([^,\n]+?)\s*(?:,|$)", re.MULTILINE)
VERSION = re.compile(r"\*\*Version\*\*:\s*(\S[^\n]*?)\s*$", re.MULTILINE)
ISO_DATE = re.compile(r"\A\d{4}-\d{2}-\d{2}\Z")

# The header as it was written before 2026-11-13, still used by ESOTERICA.md.
LEGACY_VERSION = re.compile(r"^>\s*Version:\s*(\S[^\n]*?)\s*$", re.MULTILINE)


def provenance() -> str:
    """A short 'tag-or-branch @ commit' string, marked when the tree is dirty."""

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

    branch = (git("describe", "--tags", "--exact-match", "HEAD")
              or git("symbolic-ref", "--short", "-q", "HEAD"))
    commit = git("rev-parse", "--short", "HEAD")
    if not commit:
        return "no git metadata"

    dirty = "-dirty" if git("status", "--porcelain") else ""
    return f"{branch} @ {commit}{dirty}" if branch else f"{commit}{dirty}"


def read_header(doc: Path, text: str) -> tuple[dict[str, object], str] | None:
    """Split a document into its header fields and its body."""
    split = FIRST_SECTION.search(text)
    head, body = (text[:split.start()], text[split.start():]) if split else ("", text)

    title = TITLE.search(head)
    authors = AUTHORS.search(head)
    pubdate = PUBDATE.search(head)
    version = VERSION.search(head) or LEGACY_VERSION.search(head)
    if not version:
        sys.stderr.write(f"FAIL {doc.name}: no '**Version**:' in the header\n")
        return None

    fields: dict[str, object] = {
        "title": title.group(1) if title else DOCS[doc.name],
        "subtitle": f"Version {version.group(1)}",
        "authors": [
            re.sub(r"^[-*]\s+", "", line).strip()
            for line in authors.group(1).splitlines() if line.strip()
        ] if authors else [],
        "pubdate": pubdate.group(1) if pubdate else None,
    }
    return fields, body


def valid_date(value: str | None) -> bool:
    if not value or not ISO_DATE.match(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def build(doc: Path, out_dir: Path, *, final: bool, prov: str) -> bool:
    out = out_dir / f"{doc.stem.lower()}.pdf"

    parsed = read_header(doc, doc.read_text(encoding="utf-8"))
    if parsed is None:
        return False
    fields, source = parsed

    if final and not valid_date(fields["pubdate"]):
        sys.stderr.write(
            f"FAIL {doc.name}: a final build needs a '**Publication Date**:' in "
            f"YYYY-MM-DD form, found {fields['pubdate']!r}\n"
        )
        return False

    cmd = [
        "pandoc",
        "-f", READER,
        "-t", "pdf",
        "--pdf-engine=typst",
        "--pdf-engine-opt=--input",
        f"--pdf-engine-opt=draft={'false' if final else 'true'}",
        "--template", str(TEMPLATE),
        "--metadata", f"title={fields['title']}",
        "--metadata", f"subtitle={fields['subtitle']}",
    ]
    authors = fields["authors"]
    for author in authors:
        cmd += ["--metadata", f"author={author}"]
    if authors:
        # The PDF's own Author property is a plain string, so it gets names
        # without their addresses, which Typst markup would otherwise escape.
        names = ", ".join(re.sub(r"\s*<[^>]*>", "", a) for a in authors)
        cmd += [
            "--metadata", f"author-label={'Authors' if len(authors) > 1 else 'Author'}",
            "--metadata", f"author-names={names}",
        ]
    if fields["pubdate"]:
        cmd += ["--metadata", f"pubdate={fields['pubdate']}"]
    if not final:
        # Which commit a draft came from is the only thing telling two drafts
        # apart. A release is identified by its version and date instead.
        cmd += [
            "--metadata", f"built={date.today().isoformat()}",
            "--metadata", f"provenance={prov}",
        ]
    cmd += ["-o", str(out)]

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
        help="build a release: no DRAFT watermark, no commit, and a publication date required",
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
        ok = all([build(d, out_dir, final=args.final, prov=prov) for d in docs])

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
