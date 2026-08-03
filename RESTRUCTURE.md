# RESTRUCTURE: Deck Spec v2.0 structural rewrite

> **For the implementing agent.** This is a self-contained work brief for restructuring
> `DECK.md` from its current shape into a conventional specification document, and for
> renumbering the in-progress version from 1.1 to **2.0**. The *what* and *in what order*
> are here; the "Decisions already made" table is **binding** — if you think a row is
> wrong, say so before writing prose rather than quietly deviating.
>
> Read `DECK.md` in full before starting. Read `agents/NOTES.md` for the v-next gap list
> that motivated several v2.0 features; do not re-open items it already settled.
>
> Line references below are to `DECK.md` **as it stands at the time of writing** (the
> version declaring `schema_version = "1.1"`). Verify before relying on any of them.

## The problem in one paragraph

`DECK.md`'s in-progress next version is substantively good — the Display Name Resolution,
name-composition and identifier sections are carefully specified — but it is structured as
a feature tour rather than as a specification. It never invokes RFC 2119 despite using
`MUST`/`SHOULD` throughout (and mixes them with lowercase "should" that reads as normative
but is not); it has no terminology section, no conformance classes, no versioning
contract, and no field reference tables, so field types, required-ness and defaults exist
only inside TOML comments. Two normative dangling references have no referent anywhere in
the document ("the canonical name for that ID", "the default deck"), and image resolution
— the algorithm every consumer must implement — is never specified at all. Separately, the
draft is numbered 1.1 while making five changes its own changelog calls **breaking**, and
it preserves `[deck].id` in a form that guarantees identifier collisions forever. This
task reorganizes the document into the target outline below, writes the missing sections,
lifts field documentation out of comments into tables, renumbers to 2.0, and reworks deck
identity. **No existing rule changes except where this brief explicitly authorizes it.**

## Decisions already made (binding)

| Question | Decision |
|---|---|
| Version number | **2.0**, not 1.1. The draft's own changelog lists five breaking changes, which the versioning rule in step 4 forbids a minor version from making. Renumbering is near-free: `libarcana` has no releases and no downstream packagers, and the two other implementations are slated to be retired. |
| Do we change semantics? | **Only where this brief authorizes it** — namely the deck-identity rework (step 8), the extension preference order (step 9), and the four small closures named in step 7. Everywhere else this is a restructure: rules move verbatim or near-verbatim. If you find an existing rule that is self-contradictory, record it in `agents/NOTES.md` and leave the text alone. |
| Normative keyword source | BCP 14 (RFC 2119 + RFC 8174). Uppercase only. |
| Lowercase "should"/"must" | Rewrite every lowercase instance as either an uppercase keyword (if normative) or a non-keyword verb like "is expected to" / "typically" (if not). Do not leave ambiguous lowercase keywords anywhere. |
| Informative marking | Adopt glTF's convention verbatim in spirit: sections containing only informative language get `(Informative)` suffixed to the title; everything else is normative; all Notes and Examples are informative. |
| Conformance actors | Three, named explicitly: **deck author**, **application** (reads decks), **validator** (checks decks). Every normative sentence must bind exactly one of them. |
| Grammar notation | ABNF (RFC 5234) throughout, in one consolidated section. Delete the regex forms. `^[a-z_][a-z0-9_]*$` becomes an ABNF production. |
| Deck identity: the model | Three distinct things, never again conflated. **Directory name** = library-scoped handle. **`identifier`** = optional global identity (qualified). **`name`** = display string. See step 8. |
| `[deck].id` | **Removed in 2.0.** It conflated handle and identity and was good at neither. Reading a 1.0 deck, an application maps its `id` to nothing — the directory name is the handle. Goes in Appendix B as reserved-never-reuse. |
| `[editions].id` | Removed on the same terms. Editions are keyed by their table key and MAY carry an `identifier`. |
| Is `identifier` required? | **No — SHOULD, not MUST.** A purely local deck has a perfectly good identity in its directory name, and requiring a domain would tax hobbyist authors for no benefit. The honest consequence, which the spec MUST state: a deck without an `identifier` cannot be referenced from another Arcana Land document. |
| Shadowing key | **Directory name**, matching `libarcana` today. Two decks in one library declaring the same `identifier` under different directory names is legal; a validator reports it as a **warning**. |
| Do we spec an archive/packaging form? | **No.** Decks are directories. Out of scope; note it as a non-goal in §2.2 so the omission reads as deliberate. |
| Do we spec Flatpak/sandbox root overrides? | **No.** That is `libarcana` implementation detail. The spec says XDG; how an implementation relocates `$XDG_DATA_HOME` under a sandbox is its business. |
| Media type / file extension registration | **Not now.** There is no archive form to register a type for. Omit the section rather than write a placeholder. |
| `[deck.companions]` | Exists in `libarcana` (`esoterica_companion`: id/name/uri) and in the stale `README.md` examples, but **not** in `DECK.md`. Do **not** add it. `RFC-002-cross-spec-identifiers` supersedes it. Appendix B, reserved-never-reuse. |
| `[aliases]`, `[variants]` | Removed/renamed in this version. Both go in Appendix B. A future version MUST NOT reuse either name with new meaning. |
| `[remap_major_arcana]` | **Removed in 2.0.** See step 8b for the reasoning. Appendix B, reserved-never-reuse. |
| Are canonical IDs semantic? | **No — a canonical ID is a slot, not a claim about meaning.** `major_arcana.08` is "the card this deck files at 8", not "Strength". State this explicitly in §3; it is what makes remapping unnecessary and a reader will ask. |
| Asset extension handling | **Fixed fallback chain, not a priority negotiation.** Order: `png`, `webp`, `avif`, `jpeg`/`jpg`; in `scalable/`, `svg` only. See step 9 for the full rule and its rationale. |
| Mandatory decode baseline | Applications MUST support **PNG and JPEG**. WebP, AVIF and SVG are OPTIONAL; an application MUST skip a file it cannot decode and continue down the chain. |
| Unlisted extensions | Ignored by discovery entirely. To use a format not in the chain, a deck declares an explicit `image` path (the escape hatch already at L210/L219). |
| Raster/ANSI size selection | Ratify `libarcana`'s behavior: raster picks the **smallest at or above** the target height, falling back to the closest below; ANSI picks the **largest at or below** the target lines, falling back to the closest above. |
| Cross-kind preference (`scalable` vs raster vs ANSI) | The **application** chooses the rendering kind from its own capabilities; the spec defines resolution *within* a kind only. State this explicitly so it reads as deliberate. |
| "Title-cased key" | Currently undefined but used as a terminal fallback three times. Define it once in Terminology, matching `libarcana`'s `titlecase_key`: replace `_` with a space, uppercase the first character of each resulting word, leave other characters as-is. |
| "The canonical name for that ID" / "the default deck" | Both are the same thing, and it is the **reference deck** (`libarcana`'s `library_options::reference_deck`). Define the term, and publish the canonical major arcana names as Appendix C so the reference is resolvable without a reference deck installed. |
| Should Appendix C be normative? | **Informative.** It is a fallback of last resort; pinning it normatively would freeze naming choices the spec has no business freezing. |
| Where does the library search path live? | New §2.2 "The Deck Library". Grounded in `libarcana` — see the facts table below. |
| Do we add `$XDG_DATA_DIRS`? | **Yes, in the spec.** `libarcana` implements only `$XDG_DATA_HOME` today; that is an implementation gap, not a spec constraint. Record the divergence in `agents/NOTES.md`; do not weaken the spec to match. |
| Security section scope | Two concrete threats only: author-supplied path traversal, and terminal escape injection via ANSI assets. No hand-waving about untrusted content generally. |
| Section numbering | Number all sections and subsections (`3.2`, `5.7`). The document is now cross-referential enough that anchor-only links are insufficient for review. |
| Preserve anchors? | Best-effort. Existing `#display-name-resolution`-style anchors SHOULD survive; where a heading must change, that is acceptable. Nothing external pins them. |

## Grounding facts: the deck library (from `libarcana`)

Observed behaviors of the reference implementation at `~/Projects/arcanaland/libarcana`,
to be written up as §2.2. Cited so you do not have to re-derive them.

| Fact | Source |
|---|---|
| Default library root is `$XDG_DATA_HOME/tarot/decks`, falling back to `$HOME/.local/share/tarot/decks` when the variable is unset or empty | `src/paths.cpp:32-57` |
| A library is an **ordered list of roots**, searched like `PATH` | `include/arcana/library.hpp:57-61` |
| Earlier roots **shadow** later ones by directory name; the shadowed deck is not reported at all | `src/library.cpp:36-67` |
| A directory is a deck iff it contains a regular file named `deck.toml` | `src/library.cpp:55` |
| Scanning is **non-recursive** — only immediate children of a root are candidates | `src/library.cpp:49-53` |
| A deck's identity *within a library* is its **directory name** | `deck_library::find(directory_name)`, `include/arcana/library.hpp:103` |
| `[deck].id` may collide across decks; `find_all_by_id` returns a vector | `src/library.cpp:122-128` |
| Directories whose `deck.toml` cannot be read are **reported as malformed**, not silently skipped | `malformed_deck`, `src/library.cpp:96-102` |
| A library may name a **reference deck** — the deck to fall back to when another lacks a card | `include/arcana/library.hpp:63-64` |

Write §2.2 to say: applications SHOULD locate decks in `$XDG_DATA_HOME/tarot/decks`
followed by `<dir>/tarot/decks` for each entry of `$XDG_DATA_DIRS`; roots are searched in
order and the first occurrence of a given directory name wins; scanning is non-recursive;
`deck.toml` is the marker; a directory name is the deck's library-scoped handle. State the
non-goal: this specification does not define an archive format, an installation mechanism,
or a network protocol for obtaining decks.

## Grounding facts: image resolution (from `libarcana`)

| Fact | Source |
|---|---|
| Image roots are `scalable/` plus any top-level directory matching `h<digits>` or `ansi<digits>` | `src/loader/loader.cpp:400-416, 75-90` |
| Therefore `h900/` and `ansi20/` are already legal; `h750`/`h1200`/`h2400` are conventions, not a closed set | same |
| Raster: smallest at or above target height; ties and misses fall back to nearest, breaking toward the preferred side | `src/card.cpp:219-247` (`best_of_kind`, `prefer_at_least = true`) |
| ANSI: largest at or below target lines, same fallback shape | same, `prefer_at_least = false` |
| Scalable: first match wins; there is only ever one | `src/card.cpp:258-266` |
| Extension preference within a directory is **undefined** — first directory entry with a matching stem, then `break` | `src/loader/loader.cpp:445-473` |

## Target outline

```
1. Introduction
  1.1 Scope and Design Goals                    ← current Overview (L6–17)
  1.2 Document Conventions                      ← NEW
  1.3 Terminology                               ← NEW
  1.4 Versioning and Compatibility              ← NEW; absorbs the 1.0-leniency rule at L527
  1.5 Normative References                      ← NEW
2. Deck Structure
  2.1 Directory Skeleton                        ← L19–50
  2.2 The Deck Library                          ← NEW
  2.3 File Format and Encoding                  ← NEW
3. Identity and Identifiers                     ← L267–319, moved earlier, reworked, ABNF unified
4. deck.toml Reference                          ← L52–228, restructured into field tables
5. Card Assets
  5.1 Asset Discovery                           ← L251–265
  5.2 Vector Graphics                           ← L324–326
  5.3 Raster Graphics                           ← L328–337
  5.4 ANSI Art                                  ← L339–346
  5.5 Card Back Images                          ← L348–351
  5.6 Aspect Ratio                              ← L354–358
  5.7 Card Image Resolution                     ← NEW: the algorithm
6. Internationalization                         ← L361–499, largely intact
7. Licensing and Attribution                    ← L547–632, moved ahead of validation
8. Extensibility                                ← L634–647
9. Conformance and Validation                   ← L501–545 + NEW conformance definitions
10. Security Considerations                     ← NEW
11. Implementation Notes (Informative)          ← NEW
Appendix A. Examples (Informative)              ← L649–924
Appendix B. Reserved and Deprecated Names       ← NEW
Appendix C. Canonical Card Names (Informative)  ← NEW
Appendix D. Changelog                           ← L926–962, rewritten as 2.0
```

## Work plan

Each step is independently verifiable. Do them in order; later steps assume earlier
sections exist to cross-reference. Commit per step.

### Step 1 — Skeleton and relocation, no new prose

Reorder the existing document into the target outline. Move text verbatim. Add section
numbers. Fix every cross-reference broken by the move.

**Acceptance:** `git diff --stat` shows a large reordering; a word-level diff of the moved
blocks shows no substantive edits. Every intra-document link resolves.

### Step 2 — Renumber to 2.0

Mechanical but do it early, so later steps write `2.0` naturally.

- Header `> Version: 2.0`.
- Every `schema_version = "1.1"` in every example becomes `"2.0"`.
- The changelog heading `### Version 1.1` becomes `### Version 2.0` (rewritten in step 12).
- Prose referring to "this document" as 1.1 updated.

Leave references to *reading* 1.0 decks alone; those are about the old version and are
still correct.

**Acceptance:** `grep -n '1\.1' DECK.md` returns nothing except deliberate historical
references, if any survive.

### Step 3 — §1.2 Document Conventions

Write three subsections: normative terminology (BCP 14), informative language (the
`(Informative)` suffix rule, plus "all Notes and Examples are informative"), and audience
(deck author / application / validator; requirements bind only the audience of the text
they appear in).

Then sweep the whole document for lowercase `should`/`must`/`may` and resolve each per the
binding decision. Known instances to start from: L253, L325, L346, L503, L494–499, and the
Alt Text Guidelines bullets.

**Acceptance:** `grep -nE '\b(should|must|may|shall|required|optional|recommended)\b' DECK.md`
returns only prose uses that are demonstrably non-normative.

### Step 4 — §1.3 Terminology

Definition list. Minimum set, each one sentence:

`deck`, `deck root`, `deck library`, `library root`, `reference deck`, `directory name`,
`card`, `major arcana`, `minor arcana`, `suit`, `rank`, `court card`, `canonical ID`,
`extended canonical ID`, `custom name`, `qualified identifier`, `realm`, `card variant`,
`edition`, `card back variant`, `name file`, `display string`, `title-cased key`,
`discovery`, `base` (of a file stem), `application`, `validator`, `error`, `warning`.

Three need care:

- **`card variant` vs `edition` vs `card back variant`.** "Variant" carries three meanings,
  and 2.0 renames `[variants]` → `[editions]`, so a reader of a 1.0 deck meets a fourth.
  Define all three adjacently and cross-reference them.
- **`reference deck`.** Define it here, then use the term at what are currently L467 and
  L490, replacing "the canonical name for that ID" and "the default deck".
- **`directory name`.** Now load-bearing (step 8). Define it as the deck's library-scoped
  handle and say plainly that it is *not* required to match anything inside `deck.toml`.

**Acceptance:** every term defined once; the two dangling references now resolve to a
defined term and to Appendix C.

### Step 5 — §1.4 Versioning and Compatibility

State the `schema_version` contract, adapting glTF §2.5's shape:

- Minor-version updates MUST be backward and forward compatible.
- A minor update MAY add features and MAY deprecate, but MUST NOT change or remove
  existing behavior.
- Major updates MAY be incompatible.
- An application meeting a *minor* version it does not know SHOULD load the deck and ignore
  what it does not understand; a *major* version it does not know SHOULD be refused.

Then state 2.0's relationship to 1.0 in one place: a 2.0 application MAY support 1.0 decks,
and if it does it reads them under 1.0 rules. This **replaces** the scattered leniency
rules — in particular the "report violations in a 1.0 deck as warnings" clause at L527,
which was a compatibility shim that a major version bump makes unnecessary. Delete it there.

Separately, specify the format of `[deck].version` (the deck's own version), currently a
bare required string with no stated syntax: free-form, compared only for equality, no
ordering implied.

**Acceptance:** §1.4 answers "what happens when I read a deck declaring 1.0", "…2.1", and
"…3.0" without the reader consulting any other section. No leniency rule survives outside
§1.4.

### Step 6 — §1.5 Normative References

Split normative from informative. Normative: BCP 14, RFC 5234 (ABNF), RFC 1035 §2.3.1,
BCP 47 / RFC 5646, RFC 4647, RFC 3339, TOML 1.0.0, SPDX License List and expression syntax,
XDG Base Directory Specification. Informative: SAUCE, the sibling Esoterica and Spread
specifications.

### Step 7 — §2.2 The Deck Library and §2.3 File Format and Encoding

§2.2 per the grounding-facts table above.

§2.3 pins what is currently unstated: `deck.toml` and every `names/<tag>.toml` are
**TOML 1.0.0** encoded as **UTF-8**. Card asset filenames: state the case-sensitivity rule,
mirroring the language-tag rule already at L376 — applications MUST compare stems
case-insensitively, and a deck MUST NOT ship two files in one directory whose stems differ
only in case. State that all paths in `deck.toml` are relative to the deck root and use
`/` as separator.

**Acceptance:** the TOML version, the encoding, the path base, the path separator, and the
filename case rule are each stated exactly once, normatively.

### Step 8 — §3 Identity and Identifiers

Two jobs: the grammar consolidation, and the identity rework. Do the rework first, since
it changes what the grammar has to describe.

#### 8a. The identity rework

The defect: `[deck].id` is simultaneously the library handle and the global identity, and
is inadequate as both. As a handle it duplicates the directory name, which `libarcana`
already treats as authoritative. As an identity it is unqualified, so collisions are
*expected* — which is why `find_all_by_id` returns a vector. The current draft locks this
in permanently at L309 ("a bare `id` remains required and keeps its exact meaning… where
two authors may collide"). A major version can simply fix it.

Write the three-way model:

| Thing | What it is | Where it lives | Unique? |
|---|---|---|---|
| Directory name | The deck's library-scoped handle; how a user or application addresses it locally | The filesystem | Per root, by the filesystem. Across roots, first wins (§2.2) |
| `identifier` | The deck's global identity; what another Arcana Land document points at | `[deck].identifier`, optional (SHOULD) | Globally, by construction of the realm |
| `name` | Display string | `[deck].name`, required | No |

Concretely:

- **Delete `[deck].id`** and `[editions].<key>.id`. Delete the L309 paragraph and the
  L319 "where both fields are present, `id` MUST equal the last path segment" rule, which
  exists only to reconcile the two fields.
- `[deck].identifier` is **RECOMMENDED**, not required. State the consequence plainly: a
  deck with no `identifier` cannot be referenced from another Arcana Land document. Do not
  invent a synthetic or defaulted identifier for such a deck.
- `[editions].<key>` MAY carry an `identifier` on the same terms; the table key is the
  edition's handle.
- Two decks in one library declaring the same `identifier` under different directory names
  is legal (two versions installed, a fork) and is a **validator warning**, not an error.
  Shadowing keys on directory name only.
- Keep the "qualified identifiers are not locations" note (L305) intact.

Record in `agents/NOTES.md`: `libarcana`'s `deck_summary::id`, `find_all_by_id` and the
`[deck].id` parse path all become 1.0-compat concerns; `find_all_by_id` becomes a
diagnostic rather than a lookup path. Do not touch the code.

#### 8b. Remove `[remap_major_arcana]`

Delete the section at L157–163, the design-goal clause at L14 that advertises "renaming and
remapping", and every other reference.

The reasoning, which belongs in the changelog rather than lost here:

- **It is authored by nobody.** The only file in the `arcanaland` tree that sets it is
  `libarcana/tests/fixtures/aliased-deck/deck.toml`, a synthetic fixture that also carries
  `[aliases]` and `[variants]` — both already removed by this version. It is implemented
  three times (`cartomancer/internal/deck/deck.go:327`,
  `libarcana/src/loader/loader.hpp:45`, documented in `reference-esoterica/README.md:112`)
  and used by zero real decks.
- **What is implemented is not remapping.** `libarcana`'s own test is named
  `[remap_major_arcana] moves display positions, not canonical ids`
  (`tests/deck_test.cpp:218`) and asserts that `major_arcana.08` keeps
  `display_name == "Strength"` while gaining `number == 11`. It changes the printed
  numeral and nothing else.
- **Its values name a namespace the specification does not define.** `08 = "justice"` —
  `"justice"` is not a key anywhere in `DECK.md`, where canonical major arcana keys are
  two-digit strings. This is why `agents/NOTES.md` could not pin the map's direction: one
  side of it is not in the spec's vocabulary.
- **It is not needed for the case it is named after.** The Justice/Strength split between
  the Marseille/Thoth and Rider-Waite-Smith families is real and covers a large share of
  decks in existence, but a Marseille deck expresses it by putting Justice art in `08.svg`
  and writing `08 = "Justice"` in its name file. No mechanism required.
- **It leaks interpretation into a presentation format**, against the design goal at L10.
  A deck's adherence to a numbering tradition is an interpretive claim and belongs in the
  Esoterica successor, where it wants to be a single convention field rather than a
  22-entry permutation table.

While here, add the positive statement to §3 that makes this coherent: **a canonical ID is
a slot, not an assertion about meaning.** `major_arcana.08` denotes the card a deck files
at position 8; it does not mean Strength. Cross-reference Appendix C's caveat (step 13).

#### 8c. Grammar consolidation

One ABNF block. Productions required: `canonical-id` (currently has **no** grammar despite
being the central concept), `extended-id`, `custom-name`, `qualified-id`, `realm`, `path`,
`segment`, and the `#`-fragment form used at L303 which the current grammar omits entirely.
Delete the regex forms and the ABNF/regex hybrid at L296. The `deck-id` production goes
away with `[deck].id`.

Keep every existing prose rule: the reserved-key list, the two-digit prohibition on custom
major keys, the single exception for a canonical suit as a `[custom_cards.minor_arcana]`
table key.

**Acceptance:** the block parses as valid ABNF. Every identifier form used anywhere in the
document has a production. No regex remains. `grep -n '^id\|\bid\b *=' DECK.md` finds no
surviving `[deck].id` or `[editions].*.id`.

### Step 9 — §5 Card Assets, including §5.7 Card Image Resolution

The centerpiece, and the section a consumer most needs. Model it on the Icon Theme spec's
`FindIcon`/`LookupIcon` treatment: prose rules **plus** pseudocode.

Specify:

1. **Image roots.** `scalable/`, `h<height>/` where `<height>` is a positive integer, and
   `ansi<lines>/` likewise. State explicitly that `h750`/`h1200`/`h2400` are conventions
   and any positive integer is legal — already true of the implementation but only implied
   by the current text. Unknown top-level directories are ignored.
2. **Kind selection is the application's.** Given a card and a rendering kind, resolution
   proceeds within that kind. Do not invent a cross-kind preference order.
3. **Within-kind size selection**, per the grounding-facts table: raster
   smallest-at-or-above, ANSI largest-at-or-below, both falling back to nearest on the
   wrong side; scalable is singular.
4. **Extension chain.** The full rule:
   - Order is `png`, `webp`, `avif`, `jpeg`/`jpg`. In `scalable/`, `svg` only.
     `jpg` and `jpeg` are one entry, not two.
   - Applications MUST support **PNG and JPEG**. WebP, AVIF and SVG support is OPTIONAL.
   - It is a **fallback chain, not a negotiation**: an application MUST skip a file whose
     format it cannot decode and continue down the chain.
   - Extensions not in the chain are ignored by discovery entirely. A deck wanting a format
     outside it declares an explicit `image` path (the escape hatch at L210/L219).
   - A deck SHOULD NOT ship two files with the same stem in one directory. Where it does,
     applications MUST resolve by this order rather than filesystem order.
   - **Write the rationale as a Note**, because the ordering looks arbitrary otherwise:
     unlike a web format, a deck is already on disk, so multi-encoding buys no bandwidth
     and is usually an authoring accident rather than progressive enhancement. The chain
     therefore favours fidelity and compatibility over recency. State the honest
     consequence: where a PNG is present, an application that can decode everything will
     always choose it, and the optional formats matter only when they stand alone.
   - Define "extension" as the final `.`-separated component of the filename, distinctly
     from the stem-splitting rule at L260 which splits on the *first* dot.
     `06.two_women.png` → extension `png`, stem `06.two_women`, base `06`, variant
     `two_women`.
5. **Variant interaction.** A requested variant key that a card does not have falls back to
   that card's default — this rule exists at L228 but lives in the wrong section and is
   stated only for the interpretive case. Restate it here for asset resolution.
6. **Missing card.** When a card has no asset in any root: fall back to the reference deck
   if one is configured; otherwise it is a resolution failure, not a validation error.
7. **Pseudocode** covering the above, in the Icon Theme spec's style.

Also update §5.3 Raster Graphics, whose current "Recommended formats: PNG (preferred),
JPEG, WebP" (L329) is now a normative chain defined in §5.7 — cross-reference rather than
restate, and delete the informal list.

**Acceptance:** an implementer can write `best_image_for(card, kind, target)` from §5.7
alone, and the result agrees with `libarcana`'s `best_raster_for_height` /
`best_ansi_for_lines` on every case those functions define. The word "preferred" no longer
appears in §5.3.

### Step 10 — §4 deck.toml Reference: field tables

The largest step; deliberately after step 8 so the identity fields are already settled.

Every table currently documented only through TOML comments gets a field table. Columns:
**Key | Type | Required | Default | Description**. Keep the example TOML blocks — they are
good — but demote them to illustration; the table is normative.

Tables to write: `[deck]`, `[card_backs]`, `[card_backs.variants.<key>]`, `[editions]`,
`[editions.<key>]`, `[custom_cards.major_arcana.<key>]`,
`[custom_cards.minor_arcana.<key>]`, `[card_variants."<id>"]`,
`[card_variants."<id>".variants.<key>]`, `[excluded_cards]`. (Not
`[remap_major_arcana]` — removed by step 8b.)

Fields whose type/format is currently unstated and MUST be pinned:

| Field | Pin it to |
|---|---|
| `aspect_ratio` | TOML float, width ÷ height, default `0.5789` (11:19). State what an application does when an asset's real ratio disagrees: the declared value governs layout; applications MUST preserve the asset's own ratio when scaling and SHOULD report the mismatch. |
| `created_date`, `updated_date` | RFC 3339 `full-date` (`YYYY-MM-DD`), as a TOML **string**, not a TOML native date |
| `icon`, `image`, `license_files[]` | deck-root-relative path, `/`-separated, no `..` segment, no leading `/` (cross-ref §10) |
| `tags` | array of strings, free vocabulary, no registry |
| `website` | absolute URL |
| `version` | free-form string, equality-comparable only (per step 5) |
| `identifier` | qualified identifier per §3; RECOMMENDED |

Four gaps to close while you are in here:

1. **`[editions]` has no `default` key** while `[card_backs]` does, and the spec never says
   what an application *does* with an edition. Add a `default` key to `[editions]` on the
   same terms as `[card_backs].default`, and one paragraph on edition semantics: an edition
   selects a card back and supplies alternate metadata; it does not change which cards the
   deck has.
2. **Card back default when undeclared.** `libarcana` treats a lone card back as the
   default even with no `default` key (`src/deck.cpp:178-191`). The spec says `default` is
   "Required if multiple variants are defined", which implies this but does not state it.
   State it.
3. **`[deck].name` required-ness.** Currently marked Required in a comment only; confirm in
   the table and confirm nothing else in the document treats it as optional.
4. **Removed fields.** `[deck].id` and `[editions].<key>.id` must appear in **no** table.
   Verify the examples in Appendix A were updated by step 8.

**Acceptance:** every key appearing in any TOML example in the document appears in exactly
one field table. No key's type, required-ness or default is discoverable only from a
comment.

### Step 11 — §9 Conformance and Validation

Prefix the existing validation rules with conformance definitions:

- **Conforming deck**: a directory containing a readable `deck.toml` with the required
  `[deck]` fields, plus at least one card asset.
- **Conforming application**: MUST implement discovery, name resolution and image
  resolution; MUST support PNG and JPEG; MUST ignore unknown `[app]` subtables; MUST NOT
  reject a deck for warnings.
- **Conforming validator**: MUST implement the rules in §9; MUST distinguish error from
  warning.
- Define **error** and **warning**: an error makes a deck non-conforming; a warning does
  not, and an application MUST load a deck that produces only warnings.

Keep the eight existing rule groups, with these changes:

- **Rewrite Rule 5 (Identifier Validation)** for the new identity model: no `id` to
  validate; `identifier` well-formedness where present; realm well-formedness for `[app]`
  subtables (unchanged); delete the 1.0-leniency clause (now in §1.4).
- **Add**: two decks in one library sharing an `identifier` — warning.
- **Add**: `editions.*.card_back` names an existing card back variant (currently unchecked;
  Rule 4 covers only `[card_backs].default`).
- **Add**: `[editions].default` names an existing edition.
- **Add**: no path field escapes the deck root (cross-ref §10).
- **Add**: two files with the same stem and different chain extensions in one directory —
  warning, per step 9.
- Move the license rules so they follow §7 in reading order rather than preceding it.

**Acceptance:** every rule is labelled error or warning. No rule references a section
defined later in the document.

### Step 12 — §10 Security Considerations

Two threats, concretely:

1. **Path traversal.** `image`, `icon`, `license_files` and every other path field are
   author-supplied. Applications MUST reject paths containing `..` segments, absolute
   paths, and paths resolving outside the deck root, and MUST NOT follow symlinks out of
   it. Applications MUST NOT treat a realm as a network host (rule exists at L305 —
   cross-reference rather than restate).
2. **Terminal escape injection.** ANSI assets are, by construction, sequences an
   application writes to a terminal. A hostile deck can carry OSC 52 (clipboard write),
   OSC 0/2 (title manipulation), cursor and scroll-region manipulation, and query sequences
   that induce a terminal to write attacker-chosen bytes to stdin. Specify a permitted
   subset — SGR (`CSI … m`) and the cursor positioning necessary to draw — and require
   applications to strip or reject everything else, OSC sequences in particular. Note that
   the current text at L342–343 tells applications to write plain-text art to a terminal
   "as-is", which is safe only because a plain-text file by definition contains no ESC;
   make that reasoning explicit rather than incidental.

**Acceptance:** both threats name the concrete field or byte sequence at issue. No generic
"validate your inputs" filler.

### Step 13 — §11 Implementation Notes, and the appendices

§11 (Informative), modeled on Icon Theme §8: discovery walks up to five asset trees per
deck, so applications are expected to cache directory listings; suggest invalidating on
directory mtime. Note that `deck_summary`-style cheap metadata loading — reading
`deck.toml` without walking asset trees — is the right shape for a deck picker.

**Appendix B — Reserved and Deprecated Names.** Table of names that MUST NOT be reused with
a new meaning. Columns: Name | Was | Status.

| Name | Was |
|---|---|
| `[deck].id` | The deck's identifier in 1.0/1.1; removed in 2.0 in favour of directory name + `identifier` |
| `[editions].<key>.id` | Same, for editions |
| `[aliases]` | Suit and court display names in 1.0; superseded by name files |
| `[variants]` | Deck editions in 1.0; renamed to `[editions]` |
| `[deck.excluded_cards]` | Moved to top-level `[excluded_cards]` |
| `[deck.companions]` | Never specified; present in early implementations, superseded by qualified identifiers |
| `image`, `id` on `[custom_cards.major_arcana.<key>]` | Removed; assets come from discovery |
| `[remap_major_arcana]` | Major arcana display-position remapping in 1.0/1.1; removed in 2.0, unused by any deck, and unnecessary — a deck files its cards at the positions it uses |

This is the Desktop Entry spec's Appendix B/C pattern and exists so a future version cannot
silently collide with a 1.0-era deck.

**Appendix C — Canonical Card Names (Informative).** The 22 major arcana names, as the
last-resort fallback the spec references but never publishes. (Suits and ranks are omitted
— they are recoverable from the keys via the title-case rule; see the open question below.)

Appendix C MUST carry a caveat, and it is load-bearing after step 8b: this list is an
informative display fallback for decks that supply no name of their own. It is **not** a
claim that slot 8 means Strength. A deck following Marseille or Thoth numbering files
Justice at `08`, names it in its name file, and is entirely conforming. Without this
caveat the appendix would quietly reintroduce the semantics that made `[remap_major_arcana]`
seem necessary.

**Appendix D — Changelog.** Rewrite the current 1.1 entry as **Version 2.0**. The existing
"Breaking changes" list stays and gains two entries: the identity rework (step 8a) and the
removal of `[remap_major_arcana]` (step 8b), the latter with a one-line reason so it does
not read as an oversight. Add:

- A short **"Reading a 1.0 deck"** paragraph — the changelog lists what broke but never says
  what an application should do when it meets a 1.0 deck in the wild. Point at §1.4.
- A note that this version is 2.0 rather than 1.1 *because* of the breaking list, so the
  reasoning is on the record.

**Acceptance:** Appendix C resolves both dangling references identified in step 4.
Appendix B lists every name this version retired, `[deck].id` included.

## Out of scope

- **Any semantic change not authorized above.** If a rule looks wrong, it goes in
  `agents/NOTES.md`, not in the diff.
- **Archive/packaging format, media type registration, installation or fetch protocol.**
  Non-goals; §2.2 says so once.
- **`COLLECTION.md` and the spread/collection split.** Lives in
  `agents/RFC-001-three-spec-trinity`, unaccepted.
- **Qualified-identifier *design*.** Lives in `agents/RFC-002-cross-spec-identifiers`. §3
  documents the grammar this version ships and reworks which field carries identity —
  it does not redesign the identifier scheme itself.
- **Updating `libarcana`.** It is a 1.0-era implementation — it still parses `[aliases]`
  and `[variants]`, its `is_valid_identifier` accepts leading digits and all-digit strings
  (laxer than the `custom-name` grammar), and it does not split variant stems. After step 8
  its `deck_summary::id` / `find_all_by_id` become 1.0-compat concerns, and its
  `major_arcana_remap`, `remapped_positions_` and two remap tests become dead code — note
  that `card::number` itself survives, since custom majors still carry a `position`.
  `cartomancer/internal/deck/deck.go:327` and `internal/validator/validator.go:462` are
  likewise affected. Record all of these as spec-vs-implementation divergences in
  `agents/NOTES.md`; do not bend the spec toward them, and do not touch the code.
- **`README.md`.** Its stale `[deck.companions]` examples are parked by `agents/STATUS.md`;
  its "Status: implemented" line will be wrong after 2.0 lands, which is a follow-up.

## Verification

1. **No unauthorized semantic drift.** Produce a table of every normative statement in the
   current document and its location in the new one. Any statement without a destination,
   or any new statement not authorized by this brief, must be justified in the PR
   description.
2. **Keyword sweep.** No lowercase normative keyword remains (step 3 acceptance).
3. **Version sweep.** No stray `1.1` (step 2 acceptance).
4. **Identity sweep.** No `[deck].id` or `[editions].*.id` survives in prose, tables or
   examples; every example that carried one still parses as valid TOML.
5. **Link integrity.** Every intra-document anchor resolves; every external reference
   appears in §1.5.
6. **Table coverage.** Every key in every TOML example appears in exactly one field table.
7. **Algorithm agreement.** §5.7's pseudocode agrees with `libarcana`'s `best_of_kind`
   (`src/card.cpp:219-247`) wherever that function is defined, and its extension chain is
   a strict refinement of the loader's current undefined behavior — never a contradiction
   of a case the loader defines.
8. **Dangling references.** `grep -n "default deck\|canonical name for that ID" DECK.md`
   returns nothing.
9. **Reading test.** A reader who knows tarot but not this format can, from §1–§5 alone,
   build a conforming minimal deck and write a loader for it without consulting the
   examples.

## Questions for Adam (none are blocking; all steps may proceed)

1. **`[editions].default`.** Step 10 adds it for symmetry with `[card_backs]`. This is the
   only place the restructure adds a field rather than documents or removes one. Confirm,
   or drop it and instead state that no edition is default.
2. **Appendix C scope.** Currently scoped to the 22 major arcana only, on the grounds that
   suit and rank names are recoverable from their keys via the title-case rule. Add them
   anyway for completeness?
3. **`identifier` as SHOULD, not MUST** (step 8a). The reasoning is that a local deck has a
   good handle already and requiring a domain taxes hobbyist authors. The cost is that
   such decks are unaddressable from Esoterica/Spread. Confirm, or make it MUST.

---

## Implementation status

> Appended by the implementing agent, 2026-08-03. Branch `deck-v2`. Steps 1–8 are
> committed; steps 9–13 and the verification pass are outstanding. Every commit below is
> on top of `8454638`, the last commit of the 1.1 draft.

### Answers to the three questions

Adam answered all three on 2026-08-03, and all three confirm the brief as written:

1. **`[editions].default`** — **add it**, on the same terms as `[card_backs].default`.
2. **Appendix C scope** — **majors only**. Suit and rank names stay recoverable from their
   keys via the title-case rule; listing them would create a second source of truth.
3. **`identifier` as SHOULD** — **confirmed**, not MUST.

### Grounding facts: verified

Every fact in both grounding tables was re-checked against `libarcana` before use and all
of them hold. Two worth recording:

- `best_of_kind` (`src/card.cpp:219-247`) ranks candidates by the tuple
  `{wrong_side, |size - target|, prefer_at_least ? size : -size}`. That is exactly
  "smallest at or above, else nearest below" for raster and the mirror for ANSI, with ties
  broken toward the preferred side. §5.7 must reproduce this tuple, not a paraphrase.
- `looks_like_raster_root` accepts `h` followed by *any* run of digits, so `h0` parses
  today. §5.7 says positive integer, which is a strict refinement and therefore allowed.

### Commits so far

| Step | Commit | What landed |
|---|---|---|
| 1 | `b99cbc0` | Reorder into the target outline, numbered. Text verbatim; only intra-document anchors changed. NEW sections present as empty headings. |
| 2 | `f5a1b43` | Renumber to 2.0: header, every `schema_version` example, changelog heading. |
| 3 | `17d50aa` | §1.2 Document Conventions (BCP 14, `(Informative)` rule, three actors) + the lowercase-keyword sweep. |
| 4 | `deefd33` | §1.3 Terminology, ~30 terms. Resolves the dangling references. |
| 5–6 | `010b525` | §1.4 Versioning and Compatibility, §1.5 Normative References. Deletes the Rule 5 leniency shim. |
| 7 | `183d6b5` | §2.2 The Deck Library, §2.3 File Format and Encoding. |
| 8 | `ffd4ef3` | §3 rewritten: identity rework, `[remap_major_arcana]` removed, ABNF consolidated. |

### Decisions taken inside the brief's latitude

These are choices the brief left to judgement. Flag any you disagree with before step 9
builds on them.

- **A third dangling reference.** The brief names two ("the canonical name for that ID",
  "the default deck"). §6.2 Language Resolution had a third with the same defect — "then
  the canonical value for that ID" — which the brief's `grep` in Verification #8 would not
  have caught. Fixed on the same terms.
- **§5.1's "Applications should be designed to automatically detect…"** became a flat
  statement of the mechanism rather than a `SHOULD`. Making it `SHOULD` would have
  contradicted step 11's conforming-application `MUST implement discovery`; making it
  `MUST` here would have been a semantic change this section is not the right home for.
  The normative force now lives in §5.7 and §9.
- **§5.4's ANSI fallback sentence** ("treat ANSI art as an optional format, falling back to
  other image formats") became "support for ANSI art is OPTIONAL", cross-referencing §5.7.
  The original asserted a cross-kind fallback order that the binding decision on kind
  selection forbids.
- **Two-digit major keys `22`–`99`** are stated as reserved for future versions. Previously
  they were unusable by construction (canonical is `00`–`21`; custom names may not be two
  digits) but nothing said so. Clarification, not a new constraint.
- **`schema_version` format** is pinned to `"<major>.<minor>"` in §1.4.1. It was never
  stated; §1.4's rules are unusable without it.
- **§1.4.4 carries a Note that 1.1 was never published**, so a reader meeting a `"1.1"` deck
  in the wild knows it corresponds to no released version.

### Defects found and fixed in passing

- An Appendix A example (`A.3`, the Elemental Torches name file) declared
  `[alt_text.major_arcana]` **twice** and was therefore not valid TOML. Pre-existing, not
  introduced by this work. Merged into one table. All 26 TOML blocks in the document now
  parse under `tomllib`.

### Outstanding

- **Step 9** — §5 Card Assets and §5.7 Card Image Resolution. Not started. This is the
  centerpiece and the largest remaining piece of new prose.
- **Step 10** — §4 field tables. Note that step 8 already removed `[deck].id` and
  `[editions].<key>.id` from every example, so gap 4 of step 10 is satisfied in advance.
  `[editions].default` is confirmed for addition.
- **Step 11** — §9 Conformance and Validation. Rule 5 has already been rewritten for the
  new identity model and the 1.0-leniency clause deleted; the conformance definitions, the
  five added rules and the licensing reorder remain.
- **Step 12** — §10 Security Considerations.
- **Step 13** — §11 Implementation Notes, Appendices B, C, D.
- **Verification** — the nine checks. Four already hold: no stray `1.1`, no surviving
  `[deck].id` or `[editions].*.id`, no dangling references, and every TOML example parses.
- **`agents/NOTES.md` does not exist.** The brief instructs the agent to read it for the
  v-next gap list and to record divergences in it. `agents/CLAUDE.md:96` places Adam's
  working notes at `../NOTES.md`, i.e. `specifications/NOTES.md`, untracked — and no file
  is at either path now. The gap list was therefore **not** available while writing steps
  1–8. Nothing in those steps depended on it, but step 9 (image resolution) and step 10
  (field tables) are the two most likely to have been shaped by it. **Worth confirming the
  file is not simply missing from this checkout before those steps proceed.**

### Divergences to record in `agents/NOTES.md` once it exists

Accumulated while writing steps 1–8. Do not bend the spec toward any of them; do not touch
the code.

| Divergence | Detail |
|---|---|
| `$XDG_DATA_DIRS` | §2.2.1 requires it; `libarcana` implements `$XDG_DATA_HOME` only (`src/paths.cpp:54-57`). Implementation gap. |
| `deck_summary::id`, `find_all_by_id` | Become 1.0-compat concerns after step 8a. `find_all_by_id` becomes a diagnostic — "these decks claim one identifier" — rather than a lookup path. |
| `major_arcana_remap`, `remapped_positions_` | Dead after step 8b, along with the two remap tests (`tests/deck_test.cpp:218`). `card::number` survives: custom majors still carry `position`. |
| `is_valid_identifier` | Accepts leading digits and all-digit strings; laxer than the `custom-name` production in §3.5. |
| `[aliases]`, `[variants]` | Still parsed by `libarcana`; removed from the spec in this version. |
| Variant stems | `libarcana` does not split variant stems, so it does not implement §5.1's base/variant rule at all. |
| Extension preference | `libarcana` takes the first directory entry with a matching stem and breaks (`src/loader/loader.cpp:445-473`). §5.7's chain refines undefined behavior; it contradicts no case the loader defines. |
| `cartomancer` | `internal/deck/deck.go:327` (remap) and `internal/validator/validator.go:462` are affected on the same terms. |
