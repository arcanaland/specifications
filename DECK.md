# Tarot Deck Specification

> Maintained By: [Arcana Land](https://github.com/arcanaland)
>
> Version: 2.0

## 1. Introduction

### 1.1 Scope and Design Goals

This specification defines a standard format for tarot decks used by tarot applications. The format is designed to:

- Separate presentation (e.g., images and names) from interpretation (e.g., meanings, divination, etc).
- Establish a canonical identifier system for tarot objects that can be shared across various Arcana Land specifications.
- Support internationalization (i18n) and localization (l10n).
- Support decks with extra or missing cards.
- Allow flexibility for suit and court card renaming.
- Ensure compatibility with other Arcana Land specifications, including the [Esoterica Specification](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md) for interpretive meanings and the proposed [Spread Specification](https://github.com/arcanaland/specifications/blob/main/SPREAD.md) for geometric arrangements.

Decks are directories with a mandatory `deck.toml` file at the root.

### 1.2 Document Conventions

#### 1.2.1 Normative Terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY" and "OPTIONAL" in this document are to be interpreted as described in BCP 14 ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) when, and only when, they appear in all capitals.

These words carry their normative meaning **only** in capitals. Where this document writes "should", "must" or "may" in lower case, the word carries its ordinary English sense and imposes no requirement.

#### 1.2.2 Informative Language

A section whose title carries the suffix (Informative) contains no requirements. Everything else in this document is normative.

Regardless of the section they appear in, all **Notes** and all **Examples** are informative. Where an example appears to conflict with a normative rule, the rule governs and the example is in error.

#### 1.2.3 Audience

This specification addresses three types of actors:

1. Deck authors who craft a `deck.toml` and arrange files around it.
2. Applications that read a deck in order to present it to a user.
3. Validation tools that check a deck against this specification.

### 1.3 Terminology

#### 1.3.1 Decks and Libraries

**deck** — A directory containing a `deck.toml` file, together with the card assets and name files arranged around it.

**deck root** — The directory that directly contains a deck's `deck.toml`. Every path in `deck.toml` is relative to this directory.

**directory name** — The name of a deck root's own directory and the deck's handle within a deck library. It is the deck's library-scoped identity. See [§3.4 Deck Identity](#34-deck-identity).

**deck library** — An ordered list of library roots, searched in order for decks. See [§2.2 The Deck Library](#22-the-deck-library).

**library root** — A single directory whose immediate children are candidate deck roots.

**reference deck** — A deck a library designates as the source of last resort for a display string or an asset another deck does not supply. A library MAY designate one; it is not a property of any deck. Where this specification says a value falls back to the reference deck and no reference deck is configured, [Appendix C](#appendix-c-canonical-card-names-informative) supplies the canonical major arcana names.

#### 1.3.2 Cards

**card** — One addressable image in a deck, named by a canonical ID.

**major arcana** — The trump cards, canonically twenty-two, keyed `00` through `21` under `major_arcana`.

**minor arcana** — The suited cards, canonically fifty-six, keyed by suit and rank under `minor_arcana`.

**suit** — A grouping of minor arcana cards. The four canonical suits are `wands`, `cups`, `swords` and `pentacles`; a deck MAY define others.

**rank** — A card's place within its suit. The fourteen canonical ranks are `ace` through `ten`, then `page`, `knight`, `queen` and `king`; a deck MAY define others.

**court card** — Conventionally the `page`, `knight`, `queen` and `king` of a suit. The term is descriptive; this specification attaches no rule to it.

**canonical ID** — The identifier by which this specification names a card: `major_arcana.<key>` or `minor_arcana.<suit>.<rank>`. A canonical ID is a **slot**, not an assertion about a card's meaning; see [§3.1 Canonical IDs](#31-canonical-ids).

**extended canonical ID** — A canonical ID with `:` and a variant key appended, naming one card variant: `major_arcana.06:two_women`.

#### 1.3.3 Variants, Designs and Editions

**In this specification "variant" means one thing: an alternative artwork for a card.** Nothing else varies by that name. The two other constructs a reader might expect it to cover have nouns of their own, given here so the distinction is fixed once.

**card variant** — An alternative artwork for a card the deck already contains, named by a variant key and addressed by an extended canonical ID. Variants of a card are interchangeable and carry the same meaning. Declared under `[card_variants]`; see [§4.6](#46-card_variants).

**card back design** — One of the card back designs a deck ships, named by a design key. Discovered from `card_backs/` and OPTIONALLY annotated under `[card_backs.designs]`; see [§4.2](#42-card_backs). A card back is not a card: it has no canonical ID, and a back design has no variants of its own, since a back that looks different simply is a different design.

**edition** — A printing or release of a deck that shares the deck's card fronts but selects a different card back and carries its own metadata. Declared under `[editions]`; see [§4.5](#45-editions). An edition does not change which cards the deck has.

Note: version 1.0 of this specification used "variant" for both of the latter — a top-level `[variants]` table for what [§4.5](#45-editions) now calls editions, and `[card_backs.variants]` for what [§4.2](#42-card_backs) now calls designs. A reader of a 1.0 deck therefore meets the word in two senses this document does not use. See [Appendix B](#appendix-b-reserved-and-deprecated-names).

#### 1.3.4 Identifiers

**custom name** — An identifier a deck author coins: a custom card key, suit key, rank key, card back design key, edition key or card variant key. Grammar in [§3.5](#35-grammar).

**qualified identifier** — An identifier naming an Arcana Land entity unambiguously across authors, composed of a realm and a path: `land.arcana/deck/rider-waite-smith`. See [§3.3](#33-qualified-identifiers).

**realm** — The first component of a qualified identifier: a domain name the author controls, written in reverse order. A realm is a namespace, never a network location.

#### 1.3.5 Names and Files

**name file** — A `names/<tag>.toml` file, supplying display strings and alt text for one language tag.

**display string** — A string an application shows to a user: a card name, suit name, rank name or alt text. A resolved display string is used verbatim; see [§6.3](#63-display-name-resolution).

**title-cased key** — The display string derived from a key when no name file and no `deck.toml` fallback supplies one. It is formed by replacing each `_` with a space and uppercasing the first character of each resulting word, leaving every other character as it stands. So `happy_squirrel` yields `Happy Squirrel`, `ace` yields `Ace`, and `mcdonald_wand` yields `Mcdonald Wand`.

**discovery** — Reading a deck's asset directories to determine which cards it has and which files supply them. See [§5.1](#51-asset-discovery).

**base** — The part of a card asset's file stem before the first `.`. In `06.two_women.png` the stem is `06.two_women` and the base is `06`. See [§5.1](#51-asset-discovery) and [§5.7.3](#573-extensions-stems-and-bases).

#### 1.3.6 Actors and Findings

**application** and **validator** are defined in [§1.2.3](#123-audience); **error** and **warning** in [§9.2](#92-errors-and-warnings).

### 1.4 Versioning and Compatibility

#### 1.4.1 `schema_version`

Every deck declares the version of this specification it is written against, in `[deck].schema_version`. The value is `"<major>.<minor>"`: two decimal integers separated by a dot. A deck written against this document declares `schema_version = "2.0"`.

#### 1.4.2 The Compatibility Contract

- A **minor** version update MUST be backward and forward compatible. It MAY add new tables, keys and values, and it MAY deprecate existing ones, but it MUST NOT change or remove the behavior of anything an earlier version of the same major version defined.
- A **major** version update MAY be incompatible in any respect.

The contract binds this specification, not any deck or application. Its consequence for an application is the rule below.

#### 1.4.3 Reading a Deck Whose Version an Application Does Not Know

An application meeting a `schema_version` it does not recognise:

- Where the **major** version matches one the application implements, it SHOULD load the deck and ignore every table, key and value it does not understand. A deck declaring `2.1` is readable by a 2.0 application on exactly this basis: forward compatibility within a major version is what §1.4.2 guarantees.
- Where the **major** version does not match any the application implements, it SHOULD refuse the deck and report why. A 2.0 application meeting `3.0` has no basis for guessing which of its rules still hold.
- Where `schema_version` is absent or is not of the form given in §1.4.1, an application SHOULD treat the deck as malformed rather than assume a version.

#### 1.4.4 Version 2.0 and Version 1.0 Decks

Version 2.0 is a major version and is not compatible with 1.0. An application MAY support 1.0 decks in addition to 2.0 decks. Where it does, it reads a deck declaring `schema_version = "1.0"` **under 1.0's rules**, and the requirements of this document do not apply to it. In particular, a 1.0 deck's `[deck].id`, `[aliases]`, `[variants]` and `[remap_major_arcana]` mean what 1.0 said they meant; see [Appendix B](#appendix-b-reserved-and-deprecated-names) for what became of each.

An application that does not support 1.0 decks refuses them under §1.4.3.

This section is the only place in this document that states a rule about reading an older version. Nothing elsewhere relaxes a 2.0 requirement on the grounds that a deck is old.

Note: version 1.1 was drafted but never published. No deck declares it. A `schema_version` of `"1.1"` is not defined by any released version of this specification.

#### 1.4.5 `[deck].version`

`[deck].version` is the **deck's own** version, and is unrelated to `schema_version`. It is a free-form string. This specification defines no syntax for it and no ordering over it: applications MAY compare two values for equality, to detect that a deck has changed, but MUST NOT infer from two values which is the later. A deck author who wants ordered versions is expected to adopt an ordered scheme, such as [semantic versioning](https://semver.org/), and to state so outside this field.

### 1.5 Normative References

The following documents are referenced normatively. A dated reference applies only to the edition cited; an undated reference applies to the latest edition.

| Reference | Where used |
| --- | --- |
| **BCP 14** — [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) — Key words for use in RFCs | [§1.2.1](#121-normative-terminology) |
| **RFC 5234** — Augmented BNF for Syntax Specifications: ABNF | [§3.5](#35-grammar) |
| **RFC 1035 §2.3.1** — Domain Names: preferred name syntax | [§3.3](#33-qualified-identifiers) |
| **BCP 47** — [RFC 5646](https://www.rfc-editor.org/rfc/rfc5646) — Tags for Identifying Languages | [§6.1](#61-language-tags) |
| **RFC 4647** — Matching of Language Tags | [§6.2](#62-language-resolution) |
| **RFC 3339 §5.6** — Date and Time on the Internet, `full-date` | [§4.1](#41-deck) |
| **TOML 1.0.0** — [toml.io/en/v1.0.0](https://toml.io/en/v1.0.0) | [§2.3](#23-file-format-and-encoding) |
| **SPDX License List** — [spdx.org/licenses](https://spdx.org/licenses/) and the [license expression syntax](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/) | [§7](#7-licensing-and-attribution) |
| **XDG Base Directory Specification** — [specifications.freedesktop.org](https://specifications.freedesktop.org/basedir-spec/latest/) | [§2.2](#22-the-deck-library) |

#### 1.5.1 Informative References

| Reference | Where used |
| --- | --- |
| **SAUCE** — [Standard Architecture for Universal Comment Extensions](https://www.acid.org/info/sauce/sauce.htm) | [§5.4](#54-ansi-art) |
| **Esoterica Specification** — [ESOTERICA.md](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md) | [§1.1](#11-scope-and-design-goals), [§4.6](#46-card_variants) |
| **Spread Specification** — [SPREAD.md](https://github.com/arcanaland/specifications/blob/main/SPREAD.md), proposed | [§1.1](#11-scope-and-design-goals) |

## 2. Deck Structure

### 2.1 Directory Skeleton

```
<deck-directory>/
  deck.toml
  card_backs/              # Card back designs, discovered by filename
    classic.png            # Design key `classic`
    alternative.png        # Design key `alternative`
  scalable/                # Vector images (SVG only)
    card_backs/            # Card backs at this kind and size (optional)
      classic.svg
    major_arcana/
      00.svg               # The Fool
      01.svg               # The Magician
      06.svg               # The Lovers (default variant)
      ...
    minor_arcana/
      wands/
        ace.svg
        two.svg
        ...
  ansi32/                  # ANSI art representations (32 lines recommended)
    major_arcana/
      00.ansi              # The Fool
      01.ansi              # The Magician
    minor_arcana/
      swords/
        three.ansi         # Three of Swords
  h750/                    # Low resolution raster images (optional)
  h1200/                   # Medium resolution raster images (optional)
  h2400/                   # High resolution raster images (optional)
  names/en.toml            # Localized names and alt text (optional)
  names/pt-BR.toml         # (etc)
```

### 2.2 The Deck Library

A **deck library** is an ordered list of **library roots**. Each root is a directory whose immediate children are candidate deck roots.

#### 2.2.1 Locating Library Roots

Applications SHOULD form the default library from the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/), in this order:

1. `$XDG_DATA_HOME/tarot/decks`
2. `<dir>/tarot/decks` for each `<dir>` in `$XDG_DATA_DIRS`, in the order `$XDG_DATA_DIRS` gives them

Where `$XDG_DATA_HOME` is unset or empty, it defaults to `$HOME/.local/share`, per that specification. Where `$XDG_DATA_DIRS` is unset or empty, it defaults to `/usr/local/share:/usr/share`.

An application MAY offer the user additional roots, and MAY let the user reorder them. Nothing requires an application to use the XDG defaults at all — an application given an explicit list of roots uses that list. What this section fixes is the *default*, so that a deck installed to the conventional location is found by every application that has not been told otherwise.

#### 2.2.2 Scanning

- Scanning a root is **non-recursive**: only its immediate children are candidates. A deck nested two levels below a root is not found.
- A directory is a deck **if and only if** it contains a regular file named `deck.toml`. A directory without one is not a deck and MUST NOT be reported as a malformed deck.
- A directory containing a `deck.toml` that cannot be read or parsed **is** a deck, and a malformed one. Applications SHOULD report it as malformed rather than omit it silently, so that an author who has broken their deck can tell.

#### 2.2.3 Shadowing

Roots are searched in order and a deck is identified within the library by its **directory name**. Where two roots each contain a directory of the same name, the one in the earlier root wins and the later one is not reported at all — the same rule `PATH` uses for executables.

Shadowing keys on directory name **only**. Two decks under different directory names are two decks, whatever their `[deck].identifier` fields say. Where two visible decks declare the same `identifier`, a validator reports a warning; see [§9.4](#94-validation-rules). This is a legitimate arrangement — two versions of a deck installed side by side, or a fork — and is not an error.

#### 2.2.4 Non-Goals

This specification does not define:

- an **archive or packaging format** for a deck. Decks are directories. How a deck is compressed for transport is a matter for whoever transports it.
- an **installation mechanism**. Placing a directory in a library root is installation.
- a **network protocol** for discovering, fetching or updating decks.
- a **media type** or **filename extension** registration. There is no archive form to register one for.

These omissions are deliberate. An application that grows any of these features does so outside this specification, and a deck that arrives by such a mechanism is a conforming deck or not on exactly the terms in [§9](#9-conformance-and-validation).

### 2.3 File Format and Encoding

#### 2.3.1 TOML Files

`deck.toml` and every `names/<tag>.toml` file:

- MUST be well-formed [TOML 1.0.0](https://toml.io/en/v1.0.0).
- MUST be encoded as **UTF-8**. A byte order mark is not part of TOML 1.0.0; applications MAY skip a leading `U+FEFF`, and a deck SHOULD NOT write one.

#### 2.3.2 Paths in `deck.toml`

Every path-valued field in `deck.toml` — `icon`, `image`, each entry of `license_files`, and any path field a future version adds:

- is interpreted **relative to the deck root**;
- MUST use `/` as its separator, on every platform, whatever separator the host filesystem uses;
- MUST NOT begin with `/` and MUST NOT contain a `..` segment.

Applications MUST reject a path that breaks these rules rather than resolve it; see [§10.1](#101-path-traversal).

#### 2.3.3 Filename Case

Some filesystems preserve case without distinguishing it, and a deck that relies on the distinction is unportable. Mirroring the language-tag rule in [§6.1](#61-language-tags):

- Applications MUST compare card asset stems case-insensitively.
- A deck MUST NOT ship two files in one directory whose stems differ only in case. A validator reports this as an error.

Note: this rule governs stem comparison. It says nothing about the case of a *display string*, which is always used verbatim; see [§6.3](#63-display-name-resolution).

## 3. Identity and Identifiers

This specification names three different kinds of thing, and keeps them apart. **Cards** are named by canonical IDs. **Keys a deck author coins** — custom cards, suits, ranks, card back designs, editions, card variants — are custom names. **Whole entities across authors** — a deck, a spread — are named by qualified identifiers. [§3.5](#35-grammar) gives the grammar of all three in one place.

### 3.1 Canonical IDs

Cards are referenced internally using canonical IDs, which are the only way this specification identifies a card:

- Major Arcana: `major_arcana.00` to `major_arcana.21`
- Minor Arcana: `minor_arcana.<suit>.<rank>` where:
  - `<suit>`: `wands`, `cups`, `swords`, `pentacles`
  - `<rank>`: `ace`, `two`, ..., `ten`, `page`, `knight`, `queen`, `king`

All references to cards in this specification, including configuration files, custom cards and name files, MUST use these canonical IDs.

Custom cards extend this scheme using the author's own keys: `major_arcana.happy_squirrel`, `minor_arcana.stars.ace`. Because custom names cannot begin with a digit, such an ID is never ambiguous with a canonical one.

#### 3.1.1 A Canonical ID Is a Slot

A canonical ID denotes **the card a deck files at that position**. It is not an assertion about what the card means, and this specification attaches no interpretation to any of them.

`major_arcana.08` is "the card this deck files at 8". It does **not** mean Strength. A deck in the Rider-Waite-Smith tradition files Strength there; a deck following the Marseille or Thoth numbering files Justice there. Both decks are equally conforming, and neither needs to declare anything: each simply puts its own artwork in `08` and, if it wants a name of its own, writes one under `[major_arcana].08` in its name files.

This is why this specification has no remapping mechanism. A deck expresses its numbering tradition by *where it files its cards*, which is the only thing a presentation format can observe. Whether a deck adheres to one tradition or another is an interpretive claim, and belongs in the [Esoterica Specification](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md) rather than here.

[Appendix C](#appendix-c-canonical-card-names-informative) publishes conventional English names for the twenty-two major arcana as a display fallback of last resort. It carries the same caveat, and for the same reason: it is a fallback for decks that supply no name, not a claim about what a slot means.

#### 3.1.2 Extended Canonical IDs

An **extended canonical ID** names a specific [card variant](#46-card_variants) by appending `:` and a variant key to a canonical ID:

```
major_arcana.06:two_women
```

Wherever this specification accepts a canonical ID, an extended canonical ID is also accepted unless stated otherwise. A canonical ID with no suffix denotes the card's default variant.

### 3.2 Custom Names

Custom names are the keys a deck author coins: custom major arcana keys, custom suit keys, custom rank keys, card back design keys, edition keys and card variant keys. Every one of them MUST match the `custom-name` production in [§3.5](#35-grammar) — lowercase letters, digits and underscores, not starting with a digit.

Two further rules apply, and both exist to keep a custom ID from ever colliding with a canonical one:

- A custom name MUST NOT be one of the reserved canonical keys: `major_arcana`, `minor_arcana`, the suits `wands`, `cups`, `swords` and `pentacles`, or the ranks `ace`, `two`, `three`, `four`, `five`, `six`, `seven`, `eight`, `nine`, `ten`, `page`, `knight`, `queen` and `king`.
- A custom **major arcana** key additionally MUST NOT be a two-digit string. Two-digit major arcana keys are reserved: `00` through `21` are the canonical cards, and `22` through `99` are reserved for future versions of this specification.

One position accepts a reserved key: a canonical suit as the table key of `[custom_cards.minor_arcana.<suit>]`, which [extends that suit's rank sequence](#432-custom-suits-and-ranks) rather than naming a new suit.

### 3.3 Qualified Identifiers

Qualified identifiers name Arcana Land entities such as tarot decks or spreads unambiguously across authors.

- `land.arcana/deck/rider-waite-smith`
- `land.arcana/spread/celtic-cross`
- `my.personal.domain/deck/modern-witch-tarot`

A qualified identifier is composed of a **realm** and an object **path**, separated by a slash, with an OPTIONAL **fragment** after a `#`. See [§3.5](#35-grammar) for the grammar.

- The realm is a domain name the author controls, written in reverse order according to [RFC 1035 §2.3.1](https://www.rfc-editor.org/rfc/rfc1035#section-2.3.1). It ends at the first slash.
- The path is one or more slash-separated segments naming an entity within that realm. A deck's path SHOULD be `deck/<name>`.
- The fragment names a target within that entity, and its meaning is the business of whichever specification owns the entity. In *this* specification, the fragment of a deck's qualified identifier is a canonical ID or an extended canonical ID: `land.arcana/deck/rider-waite-smith#major_arcana.00` refers to the card that deck files at `major_arcana.00`.

Note: qualified identifiers are not locations. Nothing in this specification implies that one can be fetched, and applications MUST NOT treat a realm as a network host to contact. See [§10.1](#101-path-traversal).

### 3.4 Deck Identity

A deck has three distinct things that are easy to confuse, and this specification keeps them separate:

| Thing | What it is | Where it lives | Unique? |
|---|---|---|---|
| **Directory name** | The deck's library-scoped handle: how a user or an application addresses it locally | The filesystem — the name of the deck root's own directory | Within a root, by the filesystem. Across roots, the first occurrence wins ([§2.2.3](#223-shadowing)) |
| **`identifier`** | The deck's global identity: what another Arcana Land document points at | `[deck].identifier`, RECOMMENDED | Globally, by construction of the realm |
| **`name`** | The display string shown to a user | `[deck].name`, REQUIRED | No. Two unrelated decks can share a name |

#### 3.4.1 The Directory Name Is the Handle

A deck's handle within a library is its directory name, and nothing inside `deck.toml` overrides it. A deck author who wants their deck addressed as `rider-waite-smith` names the directory `rider-waite-smith`.

A directory name is not required to match `[deck].name`, nor the last segment of `[deck].identifier`. An application MUST NOT require them to agree, and a validator MUST NOT report a disagreement.

#### 3.4.2 `identifier`

`[deck].identifier` is the deck's qualified identifier, and is **RECOMMENDED**. A deck SHOULD carry one:

```toml
[deck]
name = "Rider-Waite-Smith Tarot"
identifier = "land.arcana/deck/rider-waite-smith"
```

The consequence of omitting it is concrete and MUST be understood: **a deck with no `identifier` cannot be referenced from another Arcana Land document.** Nothing in the Esoterica or Spread specifications can name it, because there is no globally unique string to name it by. A directory name is a handle within one library and is not an identity; two people can each have a `rider-waite-smith` and mean different decks.

This is an acceptable trade. A deck a person made for themselves has a perfectly good identity in its directory name, and requiring every author to own a domain would tax the hobbyist for a benefit only the publisher needs.

Applications and validators MUST NOT synthesise an `identifier` for a deck that lacks one — not from the directory name, not from `[deck].name`, not from anything. A deck either has a global identity or it does not, and inventing one would produce an identifier that collides exactly where a real one would not.

Two decks visible in one library MAY declare the same `identifier`, under different directory names. Two versions of a deck installed side by side, or a deck and a fork of it, are the ordinary cases. This is a validator **warning**, never an error, and it does not affect shadowing, which keys on directory name alone.

#### 3.4.3 Edition Identity

An `[editions].<key>` entry follows the same model one level down. Its **table key** is the edition's handle within the deck, and it MAY carry an `identifier` giving the edition a global identity on the terms above.

### 3.5 Grammar

The productions below are [ABNF](https://www.rfc-editor.org/rfc/rfc5234) (RFC 5234). Every string literal in this grammar is **case-sensitive**, with the semantics RFC 7405 gives `%s`; all of them are lowercase.

```abnf
; ---- Card identifiers -------------------------------------------------

canonical-id    = major-id / minor-id

major-id        = "major_arcana" "." major-key
major-key       = canonical-major / custom-name
canonical-major = 2DIGIT

minor-id        = "minor_arcana" "." suit-key "." rank-key
suit-key        = canonical-suit / custom-name
rank-key        = canonical-rank / custom-name

canonical-suit  = "wands" / "cups" / "swords" / "pentacles"
canonical-rank  = "ace" / "two" / "three" / "four" / "five" / "six" /
                  "seven" / "eight" / "nine" / "ten" /
                  "page" / "knight" / "queen" / "king"

extended-id     = canonical-id ":" variant-key
variant-key     = custom-name

card-ref        = canonical-id / extended-id

; ---- Custom names -----------------------------------------------------

custom-name     = name-start *name-char
name-start      = lcalpha / "_"
name-char       = lcalpha / DIGIT / "_"

; ---- Qualified identifiers --------------------------------------------

qualified-id    = realm "/" path [ "#" fragment ]

realm           = 1*realm-char
realm-char      = lcalpha / DIGIT / "." / "-"

path            = segment *( "/" segment )
segment         = 1*segment-char
segment-char    = lcalpha / DIGIT / "-"

fragment        = 1*fragment-char
fragment-char   = lcalpha / DIGIT / "." / "_" / "-" / ":"

; ---- Terminals --------------------------------------------------------

lcalpha         = %x61-7A               ; a-z
DIGIT           = %x30-39               ; 0-9, from RFC 5234 Appendix B.1
```

Three constraints are not expressible in the grammar and are stated normatively where they belong:

- `canonical-major` admits any two digits, but only `00` through `21` are defined. `22` through `99` are reserved; see [§3.2](#32-custom-names).
- A `custom-name` MUST NOT be a reserved canonical key, with the one exception in [§3.2](#32-custom-names).
- A `fragment` on a *deck's* qualified identifier is a `card-ref`; see [§3.3](#33-qualified-identifiers).

## 4. deck.toml Reference

Every table this specification defines is listed below with its fields. In each section the **field table is normative**: it fixes each key's type, whether it is required, and its default. The TOML block beside it illustrates the table in use and is informative.

A key not listed here and not under `[app]` ([§8](#8-extensibility)) is not defined by this specification; [§8](#8-extensibility) reserves such names for future versions of it.

Types name TOML 1.0.0 types. *Path* means a deck-root-relative path as [§2.3.2](#232-paths-in-decktoml) defines it.

### 4.1 `[deck]`

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `schema_version` | String | **Yes** | — | The version of this specification the deck is written against, `"<major>.<minor>"`; see [§1.4.1](#141-schema_version). A deck written against this document declares `"2.0"`. |
| `name` | String | **Yes** | — | The deck's display name. Not required to be unique, and not required to match the directory name ([§3.4](#34-deck-identity)). |
| `version` | String | **Yes** | — | The deck's own version. Free-form; comparable for equality only, with no ordering implied ([§1.4.5](#145-deckversion)). |
| `identifier` | String | RECOMMENDED | none | The deck's qualified identifier ([§3.3](#33-qualified-identifiers)). A deck without one cannot be referenced from another Arcana Land document ([§3.4.2](#342-identifier)). |
| `default_language` | String | No | `"en"` | BCP 47 tag of the deck's default name file ([§6.2](#62-language-resolution)). |
| `icon` | String (path) | No | none | A preview image for the deck, assumed to share the cards' aspect ratio. |
| `aspect_ratio` | Float | No | `0.5789` | Width ÷ height of the deck's cards; see below. |
| `author` | String | No | none | The artwork's author, as displayed. |
| `description` | String | No | none | A prose description of the deck. Not localized: written once, in `default_language` ([§6.4](#64-alt-text-guidelines)). |
| `license` | String | No | none | SPDX license expression governing the artwork ([§7.1](#71-license-expressions)). |
| `license_files` | Array of String (path) | No | `[]` | Full license texts and notices carried in the deck ([§7.2](#72-attribution-and-notices)). |
| `copyright` | String | No | none | Copyright notice, displayed verbatim. |
| `attribution` | String | No | none | Credit line to display ([§7.2](#72-attribution-and-notices)). |
| `created_date` | String | No | none | RFC 3339 `full-date` (`YYYY-MM-DD`); see below. |
| `updated_date` | String | No | none | RFC 3339 `full-date` (`YYYY-MM-DD`); see below. |
| `publisher` | String | No | none | The deck's publisher. |
| `website` | String | No | none | An absolute URL for the deck. |
| `tags` | Array of String | No | `[]` | Free-vocabulary categorization tags. This specification defines no registry of tag values and attaches no behavior to any of them. |

**Dates.** `created_date` and `updated_date` are RFC 3339 `full-date` values written as TOML **strings**, not TOML native dates. A quoted `"1909-12-01"` is correct; a bare `1909-12-01`, which TOML would read as a local date, is an error. The string form is required because a date is metadata to display and compare textually, and because TOML's date types would tempt applications to parse a precision the field does not carry.

**Aspect ratio.** `aspect_ratio` is the width of a card divided by its height, so the traditional 11:19 card is `0.5789`. It governs **layout**: an application reserves space for a card by this ratio. Where an asset's own pixel ratio disagrees with it, the application MUST still preserve the asset's own ratio when scaling it — an image is never stretched to fit the declared value — and SHOULD report the mismatch to the author.

```toml
[deck]
schema_version = "2.0"           # Required: Schema version (this document)
identifier = "land.arcana/deck/rider-waite-smith" # Recommended: qualified identifier (see §3.4)
name = "Rider-Waite-Smith Tarot" # Required: Human readable name
version = "1.0"                  # Required: Deck version
default_language = "en"          # Optional: BCP 47 tag of the deck's default names file (default "en")
icon = "deck-icon.png"           # Optional: deck preview image
author = "Pamela Colman Smith"   # Optional
aspect_ratio = 0.5789            # Optional (default 11:19)
description = "The classic Rider-Waite-Smith tarot deck, first published in 1909." # Optional

# Licensing and attribution (all optional)
license = "CC0-1.0"              # SPDX license expression governing the artwork
license_files = ["LICENSE"]      # Full license text and notices, relative to the deck root
copyright = "© 1909 Pamela Colman Smith" # Copyright notice, verbatim
attribution = "Artwork by Pamela Colman Smith." # Credit line to display

# Additional optional metadata
created_date = "1909-12-01"      # Original creation date
updated_date = "2025-01-15"      # Last update date
publisher = "US Games Systems"   # Publisher information
website = "https://example.com/rws-deck" # Website for the deck
tags = ["traditional", "classic", "beginner-friendly"] # Categorization tags
```

`[deck]` holds the deck's identity and the human-facing metadata about it. Everything that is *content* — card backs, custom cards, card variants, editions, exclusions — is a top-level table of its own, and no table nests under `[deck]`.

Icons are assumed to be the same aspect ratio as the cards.

### 4.2 `[card_backs]`

A **card back design** is one of the back images a deck ships, named by a **design key**. Designs are [discovered from the directory structure](#55-card-back-images) exactly as cards are: a deck that drops `card_backs/classic.png` into place has a design keyed `classic`, and need declare nothing at all. The whole of `[card_backs]` is OPTIONAL.

```toml
[card_backs]
default = "classic"              # Optional; see the default rules below

# Annotate a design. Optional — the files above already define them.
[card_backs.designs.classic]
name = "Classic RWS Back"        # Human-readable name
# Prose about the design: where it comes from, not what it looks like
description = "The 1909 Rider back, reproduced from the Pamela Colman Smith printing."
# What it looks like, for a reader who cannot see it. Prefer names/<tag>.toml
alt_text = "A lattice of blue and white roses and lilies, edge to edge, with no border."
```

**`[card_backs]`**

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `default` | String | No | see below | The design key an application uses where the user or an [edition](#45-editions) has not chosen another. Where present it MUST name a design the deck has ([§9.4](#94-validation-rules)). |

Where a deck has no card back at all, an application supplies its own. Otherwise the default design is the first of these that applies:

1. the design named by `[card_backs].default`;
2. the design keyed `default`, where the deck has one;
3. the lexicographically first design key.

Rule 3 makes the default well defined for a deck with no `deck.toml` declaration at all, and an application MUST NOT substitute filesystem order for it — the same requirement [§5.7.5](#575-the-extension-chain) makes of the extension chain, and for the same reason. A deck shipping more than one design SHOULD nonetheless declare `default` or key a design `default`, rather than rely on collation; a validator says so ([§9.4](#94-validation-rules)).

**`[card_backs.designs.<key>]`** — `<key>` is a [custom name](#32-custom-names) and is the design key. The table is OPTIONAL for every design, and supplies only what a filename cannot.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | resolved per [§6.3](#63-display-name-resolution) | Fallback display name for this design, used where no name file supplies one. |
| `description` | String | No | none | Prose *about* the design — its provenance, its history, what it depicts — for display alongside the back in a picker or an info panel. Not localized: it is written once, in the deck's `default_language`. See [§6.4](#64-alt-text-guidelines). |
| `alt_text` | String | No | none | Fallback alt text: what the back looks like, for a reader who cannot see it. A name file's `[alt_text.card_backs]` takes precedence and is where a deck SHOULD put it ([§6.3](#63-display-name-resolution)). |
| `image` | String (path) | No | found by discovery | An explicit path to this design's image, for a file that does not follow the naming convention or uses a format outside the extension chain ([§5.7.5](#575-the-extension-chain)). |

Declaring a design under `[card_backs.designs]` does not create it. A design the deck has no file for and no `image` path to is a [resolution failure](#577-when-no-asset-is-found), not a validation error, exactly as for a card.

Card backs MAY have different dimensions and formats from the card fronts, and a deck MAY provide several without duplicating the entire deck.

### 4.3 `[custom_cards]`

A deck can hold cards the traditional 78 do not: additional major arcana, entirely new suits, or additional ranks within a suit. Custom card keys, custom suit keys and custom rank keys are custom names and MUST follow the [identifier rules](#3-identity-and-identifiers).

Custom cards are [discovered from the directory structure](#51-asset-discovery) exactly as canonical cards are. A deck that drops `h1200/major_arcana/happy_squirrel.png` into place has added a card, and need declare nothing at all. The `[custom_cards]` table supplies only what a filename cannot: a card's place in the deck's sequence, and fallback display strings. It is OPTIONAL in its entirety.

#### 4.3.1 Custom Major Arcana

```toml
[custom_cards.major_arcana.happy_squirrel]
name = "The Happy Squirrel"  # Optional fallback; prefer names/<tag>.toml
alt_text = "A cheerful squirrel standing on a branch proudly holding an acorn." # Optional fallback
position = 22                # Optional; see Ordering
```

**`[custom_cards.major_arcana.<key>]`** — `<key>` is a [custom name](#32-custom-names) and MUST NOT be two digits ([§3.5](#35-grammar)).

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | resolved per [§6.3](#63-display-name-resolution) | Fallback display name, used where no name file supplies one. |
| `alt_text` | String | No | none | Fallback alt text, used where no name file supplies one. |
| `position` | Integer | No | none | Where the card sits in the deck's sequence; see [§4.3.3](#433-ordering). A card with no `position` follows those that have one. |

The `name` and `alt_text` fields are fallbacks. A deck SHOULD carry both in `names/<tag>.toml`, where they can be localized; see [Display Name Resolution](#63-display-name-resolution).

There is no `image` field. A custom card's images are found by the same convention as every other card's, which is what lets one card exist in several resolutions and formats at once.

#### 4.3.2 Custom Suits and Ranks

A suit's rank sequence is declared by `ranks`, a list of rank keys in the order the deck reads them:

```toml
# A new suit
[custom_cards.minor_arcana.stars]
name = "Stars"  # Optional fallback; prefer names/<tag>.toml
ranks = ["ace", "two", "three", "four", "five", "six", "seven", "eight",
         "nine", "ten", "page", "knight", "queen", "king"]
```

`ranks` MAY also be given for one of the four canonical suits, where it replaces that suit's canonical sequence. This is how a deck adds a rank to a suit it already has:

```toml
# A fifteenth cups card, seated among the court
[custom_cards.minor_arcana.cups]
ranks = ["ace", "two", "three", "four", "five", "six", "seven", "eight",
         "nine", "ten", "princess", "page", "knight", "queen", "king"]
```

The table key here is the canonical suit `cups`. This is the one place in this specification where a reserved key is accepted as a `[custom_cards]` table key, because the intent is to modify that suit rather than to name a new one. The rank keys themselves are custom names and remain subject to the reserved-key rule: a deck MUST NOT introduce a new rank called `page`.

**`[custom_cards.minor_arcana.<key>]`** — `<key>` is a [custom name](#32-custom-names), or one of the four canonical suits where the intent is to modify that suit.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | resolved per [§6.3](#63-display-name-resolution) | Fallback display name for the suit, used where no name file supplies one. |
| `ranks` | Array of String | No | the canonical rank sequence, for a canonical suit; otherwise none | The suit's rank keys, in the order the deck reads them. |

`ranks` is a matter of ordering only, and is OPTIONAL in both forms. A rank whose files are present but which no `ranks` list mentions is still a card of that suit; see below.

Rank and suit keys resolve their display names through `names/<tag>.toml`; see [Display Name Resolution](#63-display-name-resolution).

#### 4.3.3 Ordering

Applications that present a deck in order resolve it as follows. Cards with a declared place come first, in that order: major arcana by `position`, minor arcana by their suit's `ranks`. Everything else follows, sorted by key. Suits with no canonical order follow the four canonical suits, likewise sorted by key.

`position` is an integer and MAY fall anywhere in the sequence, including between two canonical cards; a deck that seats an extra card between `08` and `09` gives it `position = 9` and pushes the rest along. Where two cards claim one position, the order between them is by key.

A deck that simply does not care — one extra major arcanum, no opinion about where it sits — declares nothing and gets it last.

### 4.4 `[excluded_cards]`

```toml
[excluded_cards]
# List cards that are intentionally excluded from this deck
cards = [
  "minor_arcana.pentacles.page",
  "minor_arcana.pentacles.knight"
]
reason = "This deck excludes these specific court cards."
```

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `cards` | Array of String | No | `[]` | Canonical IDs of cards this deck deliberately does not contain. |
| `reason` | String | No | none | Why they are excluded, for display to a user. |

An exclusion is a statement of intent, not a mechanism: a card is absent because the deck ships no asset for it ([§5.1](#51-asset-discovery)). `[excluded_cards]` records that the absence is deliberate, so that an application can tell a user "this deck has no court cards" rather than report a gap, and so that resolution does not go looking for the card in a [reference deck](#131-decks-and-libraries) ([§5.7.7](#577-when-no-asset-is-found)).

### 4.5 `[editions]`

For decks that have multiple editions or printings sharing the same card fronts:

```toml
[editions]
default = "standard"   # Required if multiple editions are defined

# Define deck editions that share the same card fronts
[editions.standard]
name = "Rider-Waite-Smith (Standard)"
card_back = "classic"  # The design key: card_backs/classic.png
publisher = "US Games Systems"

[editions.rider_edition]
name = "Rider-Waite-Smith (Rider Edition)"
card_back = "rider"    # The design key: card_backs/rider.png
publisher = "Rider & Company"
created_date = "1912-01-01"
```

**`[editions]`**

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `default` | String | Required where more than one edition is defined | see below | The edition key an application selects where the user has not chosen another. |

Where exactly one edition is defined and `default` is omitted, that edition is the default. Where more than one is defined, `default` is REQUIRED and MUST name a defined edition ([§9.4](#94-validation-rules)). Editions differ from [card back designs](#42-card_backs) here: an edition exists only because `deck.toml` declares it, so requiring the declaration to be complete costs an author nothing, whereas a design can arrive with no declaration at all and still needs a well-defined default.

**`[editions.<key>]`** — `<key>` is a [custom name](#32-custom-names) and is the edition's handle within the deck ([§3.4.3](#343-edition-identity)).

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | **Yes** | — | The edition's display name. |
| `card_back` | String | No | `[card_backs].default` | The [design key](#42-card_backs) this edition uses. MUST name a card back design the deck has ([§9.4](#94-validation-rules)). |
| `identifier` | String | No | none | A qualified identifier for the edition ([§3.4.3](#343-edition-identity)). |
| `publisher` | String | No | `[deck].publisher` | The edition's publisher, where it differs from the deck's. |
| `created_date` | String | No | `[deck].created_date` | RFC 3339 `full-date`, on the terms in [§4.1](#41-deck). |

An edition MAY also carry any of the optional metadata keys [§4.1](#41-deck) defines for `[deck]` — `description`, `version`, `updated_date`, `author`, `website` and the rest — with the same type and meaning. It MUST NOT carry `schema_version`, which is a property of the deck.

**What an edition is.** An edition selects a card back and supplies metadata that differs from the deck's. It does **not** change which cards the deck has: every edition of a deck shares one set of card fronts, one set of custom cards and one set of exclusions. A printing whose artwork differs is a different deck, not an edition — or, where only some cards differ, a set of [card variants](#46-card_variants).

Where an application has selected an edition, that edition's fields take precedence over `[deck]`'s for display, and a field the edition does not give falls back to `[deck]`'s value. An application that does not model editions at all reads `[deck]` and the default card back, and is conforming.

### 4.6 `[card_variants]`

A card variant is an alternative artwork for a card that a deck already contains.

Variants are addressed by an [extended canonical ID](#31-canonical-ids) of the card's canonical ID, a colon, and the variant key (e.g., `major_arcana.06:two_women`).

File assets are named with the variant key infixed between the card's file stem and its extension:

```
h1200/major_arcana/06.two_women.png
```

Declaring variants in `deck.toml` is OPTIONAL, and is necessary only to choose a non-default default, to supply fallback strings, or to point at a file that does not follow the naming convention.

```toml
[card_variants."major_arcana.06"]
default = "two_women"   # Optional: which variant is used for a bare canonical ID

[card_variants."major_arcana.06".variants.two_women]
name = "The Lovers"     # Optional fallback; prefer names/<tag>.toml
alt_text = "Two women stand hand in hand beneath a winged figure." # Optional fallback
image = "scalable/major_arcana/06.two_women.svg" # Optional: explicit path
```

**`[card_variants."<canonical-id>"]`** — the table key is the card's canonical ID, quoted because it contains dots.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `default` | String | Required where the card has no unsuffixed file | the unsuffixed file | Which variant a bare canonical ID resolves to ([§5.7.6](#576-variants)). MUST name a variant of this card ([§9.4](#94-validation-rules)). |

**`[card_variants."<canonical-id>".variants.<key>]`** — `<key>` is a [custom name](#32-custom-names) and is the variant key.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | resolved per [§6.3](#63-display-name-resolution) | Fallback display name for this variant, used where no name file supplies one. |
| `alt_text` | String | No | none | Fallback alt text for this variant. Variants SHOULD carry their own; see [§6.4](#64-alt-text-guidelines). |
| `image` | String (path) | No | found by discovery | An explicit path to this variant's image, for a file that does not follow the naming convention or uses a format outside the extension chain ([§5.7.5](#575-the-extension-chain)). |

Variant keys are custom names and MUST follow the [identifier rules](#3-identity-and-identifiers).

If `default` is omitted, the unsuffixed file (`06.svg`) is the default variant. If a deck provides only variant files for a card and no unsuffixed file, it MUST declare `default`.

Note that `names/<tag>.toml` also has a `[card_variants]` table, but a flat one keyed by extended canonical ID; see [Internationalization](#6-internationalization).

Variants of a card are interchangeable and carry the same meaning; consumers of interpretive data, including the [Esoterica Specification](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md), discard the variant suffix. Variant keys are deck-wide, so an application MAY prefer a key across the whole deck; where a card has no variant under that key, it MUST use that card's default rather than treat it as an error.

## 5. Card Assets

### 5.1 Asset Discovery

Applications detect files placed in the expected directory structure and map them to cards without further configuration. For example, placing
in image in `h1200/minor_arcana/wands/ace.png` will automatically map it to the card with the canonical ID `minor_arcana.wands.ace`.

This ensures that creating a deck can be as simple as placing files into the correct directory structure.

A file's stem is parsed read by splitting on the first `.` and designating the first portion the base. If the base defines a card that the deck already contains, the remainder is a [variant key](#46-card_variants) and the file is considered a variant of that card. Otherwise, the base designated as a custom name, and the file defines a custom card.

For example,

- `major_arcana/06.two_women.png` is a variant of The Lovers,
- `major_arcana/the_morning.png` is a custom card
- `major_arcana/the_morning.dark.png` is a variant of a custom card

### 5.2 Vector Graphics

Support for SVG is OPTIONAL for an application and MUST be placed in the `scalable/` directory. SVG is the only vector format this specification defines.

### 5.3 Raster Graphics

Raster images MUST be placed in an `h<height>/` directory, where `<height>` is the height of the image in pixels
- Which file formats discovery considers, and in what order, is fixed by the extension chain in [§5.7.5](#575-the-extension-chain)
- PNG with an alpha channel is RECOMMENDED for images requiring transparency

#### 5.3.1 Resolution Usage Guidelines

- h750: Use for mobile applications and thumbnails
- h1200: Use for standard web viewing and most desktop applications
- h2400: Use for high-resolution displays and when fine details need to be preserved

### 5.4 ANSI Art

- Files MUST be stored in an `ansi<lines>/` directory, organized by card type and suit (e.g., `ansi32/major_arcana/00.ansi`). `<lines>` is the number of terminal rows the art occupies.
- ANSI files MAY use any extension. `.ans` is conventional for art carrying escape sequences and `.txt` for plain text.
- Applications MUST determine a file's kind from its content rather than its extension. Art using ANSI escape sequences necessarily contains ESC (`0x1B`) and a file with no ESC byte is plain text and MAY be written to a terminal as-is.
- Plain text files are UTF-8.
- Where a file carries a [SAUCE](https://www.acid.org/info/sauce/sauce.htm) record, applications SHOULD honor it.

Support for ANSI art is OPTIONAL for an application.

### 5.5 Card Back Images

Card backs are discovered, like cards. A `card_backs/` directory is a **card back directory**, and each file in one defines a [design](#42-card_backs) whose key is the file's stem:

```
card_backs/classic.png          → design `classic`, no declared size
h1200/card_backs/classic.png    → design `classic` at 1200px
h2400/card_backs/classic.png    → design `classic` at 2400px
ansi32/card_backs/classic.ans   → design `classic` at 32 rows
scalable/card_backs/classic.svg → design `classic`, scalable
```

A card back directory appears in two places, and both are OPTIONAL:

- **At the top level of the deck root.** `card_backs/` alongside `deck.toml` holds backs of no declared kind or size. This is the simple form, and for most decks it is the only one needed.
- **Inside an [image root](#571-image-roots).** `card_backs/` is a third sibling of `major_arcana/` and `minor_arcana/` within any image root, and its files carry that root's kind and size.

The designs a deck has are the union of the stems found across every card back directory, together with every key declared under `[card_backs.designs]` that carries an `image` path.

Further rules:

- The **whole stem** is the design key; there is no base-and-variant split ([§5.7.3](#573-extensions-stems-and-bases)). A back that looks different is a different design, not a variant of one, so `card_backs/classic.dark.png` defines no design and is ignored — as is any file whose stem is not a well-formed [custom name](#32-custom-names).
- The [extension chain](#575-the-extension-chain) applies, as it does to cards. A deck SHOULD supply its card backs in a format [§5.7.5](#575-the-extension-chain) requires every application to decode, since an application that cannot decode a card back has no fallback for it.
- An explicit `image` path on `[card_backs.designs.<key>]` overrides discovery for that design in every kind and size, and escapes the extension chain. Discovery is a convention; an explicit path is an instruction.
- Card backs MAY have different dimensions and aspect ratios from the card fronts. `[deck].aspect_ratio` describes the fronts and a back is not held to it; an application still preserves a back's *own* aspect ratio when scaling it ([§5.6](#56-aspect-ratio)).

#### 5.5.1 Resolving a Card Back

Given a design key, a kind and a target size, an application resolves a back by [§5.7](#57-card-image-resolution), with three differences:

1. The subpath is `card_backs/` rather than `major_arcana/` or `minor_arcana/<suit>/`, and the stem is the design key.
2. Where no image root of the requested kind supplies the design, the top-level `card_backs/` directory is consulted last, as a root of no size. Because it declares no kind either, an application that finds nothing there under the chain for the kind it asked for MAY take any file in it whose stem is the design key and whose format it can decode — the cross-kind fallback [§5.7.2](#572-choosing-a-rendering-kind) already leaves to its discretion. A deck that ships only `card_backs/classic.png` therefore answers a request for `classic` at any target size, and answers a scalable request too for any application willing to render a raster back.
3. There is no reference-deck step ([§5.7.7](#577-when-no-asset-is-found)). A card back is a property of the deck's own presentation, and borrowing another deck's back misrepresents it. Where resolution finds nothing, the application supplies its own back.

[§5.7.8](#578-resolution-algorithm) states this as pseudocode.

### 5.6 Aspect Ratio

- Standard assumed aspect ratio is **11:19** (~0.5789), declared by [`[deck].aspect_ratio`](#41-deck).
- Applications MUST preserve the aspect ratio when scaling images.

### 5.7 Card Image Resolution

Given a card, a rendering kind and a target size, an application resolves a file to display. This section defines that resolution. It is the algorithm every application implements, and a deck author reads it to know which of several files an application will choose.

#### 5.7.1 Image Roots

An **image root** is a top-level directory of a deck root that discovery searches for card assets. There are three forms:

| Form | Kind | Size |
| --- | --- | --- |
| `scalable/` | scalable | none; a vector image has no intrinsic size |
| `h<height>/` | raster | `<height>`, in pixels |
| `ansi<lines>/` | ANSI | `<lines>`, in terminal rows |

`<height>` and `<lines>` are decimal integers greater than zero, written without a sign, leading zeroes or separators: `h750`, `h1200`, `h2400`, `ansi20`, `ansi32`. Any such integer is legal. `h750`, `h1200` and `h2400` are conventions this specification recommends and no more; `h900` and `ansi48` are equally well-formed, and an application MUST NOT restrict itself to the conventional set.

A deck MAY carry any number of image roots of each form, and MUST NOT carry two roots naming the same kind and size.

Every other top-level directory is **ignored by discovery**. `card_backs/` and `names/` are directories this specification gives other meanings to; a directory named anything else — `src/`, `.git/`, `previews/` — is not an image root and its contents are not cards. The top-level `card_backs/` is not an image root, but it is not inert either: it holds card back designs of no declared size, and [§5.5](#55-card-back-images) defines how they are found.

Within an image root, assets are arranged by card type and suit, as [§2.1](#21-directory-skeleton) shows: `major_arcana/<base>.<ext>` and `minor_arcana/<suit>/<base>.<ext>`. An image root MAY also hold a `card_backs/` directory, which supplies card back designs at that root's kind and size rather than cards ([§5.5](#55-card-back-images)). Any other subdirectory of an image root is ignored.

#### 5.7.2 Choosing a Rendering Kind

Which kind an application renders is **the application's choice**, made from its own capabilities and context: a terminal client renders ANSI, a compositing GUI prefers scalable where it has it, a thumbnailer takes the raster size nearest what it needs. This specification defines resolution *within* a kind and deliberately defines no preference *between* kinds. A deck that ships all three kinds is not asserting an order over them.

An application that finds no asset of its preferred kind MAY fall back to another kind. Where it does, the choice of which is again its own.

#### 5.7.3 Extensions, Stems and Bases

A card asset filename is read as three parts. Given `06.two_women.png`:

| Part | Value | Rule |
| --- | --- | --- |
| extension | `png` | The part after the **last** `.` |
| stem | `06.two_women` | Everything before the last `.` |
| base | `06` | The part of the stem before the **first** `.` |
| variant key | `two_women` | The remainder of the stem after the first `.`, where there is one |

Note that the stem is split on the first `.` and the extension on the last. The two rules differ because a variant key cannot contain a `.` — [§3.5](#35-grammar) forbids it — so at most one dot in a stem is ever a separator, while the extension is always the final component. A file named `06.png` has base `06`, no variant key, and extension `png`.

A file whose name contains no `.` at all has no extension. Discovery ignores it in `scalable/` and in raster roots. In an ANSI root it is a candidate: [§5.4](#54-ansi-art) allows ANSI files any extension or none, and determines their kind from content.

**In a card back directory this parse does not apply.** The extension is read the same way — the part after the last `.` — but everything before it is the [design key](#42-card_backs), undivided. Card backs have no variants ([§5.5](#55-card-back-images)), so a stem containing a `.` is not a design with a variant key; it is not a design at all, and discovery ignores it.

#### 5.7.4 Size Selection Within a Kind

`scalable/` holds at most one image per card and variant, so selection there is trivial: the file is the file.

For raster and ANSI, an application selects among the roots of that kind that supply a file for the card. The rules differ, because the two media degrade in opposite directions:

- **Raster**: prefer the **smallest image at or above** the target height. Downscaling a raster image is well-behaved; upscaling is not.
- **ANSI**: prefer the **largest art at or below** the target number of lines. Art taller than the space available is truncated, which is worse than art that leaves a gap.

Where no candidate lies on the preferred side of the target, an application MUST fall back to the nearest candidate on the other side rather than fail.

Stated exactly, an application ranks each candidate root by the tuple

```
(wrong_side, |size - target|, tiebreak)
```

where, writing `size` for the root's height or line count:

- `wrong_side` is `size < target` for raster and `size > target` for ANSI, with `false` ordering before `true`;
- `tiebreak` is `size` for raster and `-size` for ANSI, so that a tie between two equidistant candidates breaks toward the preferred side.

The candidate with the smallest tuple wins. An exact match always wins, since it alone scores `(false, 0, …)` at the minimum distance.

*Example.* A deck ships `h750/`, `h1200/` and `h2400/`. A raster request for target 1000 resolves to `h1200` — the smallest at or above. A request for target 3000 resolves to `h2400`, the nearest below, no candidate being at or above. A request for target 975, equidistant from 750 and 1200, resolves to `h1200`, the tie breaking toward the preferred side.

#### 5.7.5 The Extension Chain

Within one directory, an application considers extensions in this fixed order:

1. `png`
2. `webp`
3. `avif`
4. `jpeg` and `jpg` — one entry, not two; where a directory holds both, the choice between them is unspecified

In `scalable/`, the chain is `svg` alone.

- Applications MUST support decoding **PNG** and **JPEG**. Support for WebP, AVIF and SVG is OPTIONAL.
- This is a **fallback chain, not a negotiation**. An application MUST skip a file whose format it does not support, or whose bytes it fails to decode, and continue to the next entry in the chain.
- Extensions outside the chain are **ignored by discovery entirely**. A `.tiff` or a `.gif` in `h1200/major_arcana/` does not define a card and is never chosen.
- A deck SHOULD NOT ship two files with the same stem and different chain extensions in one directory. Where it does, applications MUST resolve by this order and MUST NOT resolve by filesystem order; a validator reports the duplication as a warning ([§9.4](#94-validation-rules)).
- Where a directory supplies no file the application can decode — every candidate is either outside the chain or in a format it lacks — that directory does not supply the card, and the application MUST continue with the remaining candidates under [§5.7.4](#574-size-selection-within-a-kind).

A deck that wants a format outside the chain declares an explicit `image` path on the card variant ([§4.6](#46-card_variants)) or card back design ([§4.2](#42-card_backs)). Discovery is a convention; an explicit path is an instruction.

> **Note (informative).** The order looks arbitrary against the usual web ordering, which puts the newest and most compact format first. It is not the same problem. A deck is already on disk and already downloaded, so a second encoding of the same card buys no bandwidth; where a deck does ship two, it is usually an authoring accident — a conversion tool left its output behind — rather than progressive enhancement. The chain therefore favours fidelity and universal decodability over recency: PNG is lossless, alpha-capable and decodable everywhere. The honest consequence is that where a PNG is present, an application that can decode every format will always choose it, and the optional formats matter only where they stand alone. An author who ships `06.avif` and nothing else is served exactly as intended.

#### 5.7.6 Variants

A request MAY name a [variant key](#46-card_variants). Resolution then looks for files whose stem is `<base>.<key>`, and is otherwise unchanged: the same size selection, the same extension chain.

Where the requested card has no variant under that key, the application MUST resolve that card's **default** variant instead, and MUST NOT treat the absence as an error. Variant keys are deck-wide and a card need not carry every key the deck uses; this is the asset-resolution statement of the rule in [§4.6](#46-card_variants).

A request naming no variant key resolves the card's default variant: the unsuffixed file, or the variant named by `[card_variants."<id>"].default` where one is declared.

#### 5.7.7 When No Asset Is Found

Where resolution yields no file for a card in any image root of any kind:

- Where the library designates a [reference deck](#131-decks-and-libraries) and the card is not deliberately absent under [`[excluded_cards]`](#44-excluded_cards), the application SHOULD resolve the same card against that deck.
- Otherwise, this is a **resolution failure**, not a validation error. The application decides what to show — a placeholder, a card back, nothing. A deck is not non-conforming for lacking an asset for some card, and [§9](#9-conformance-and-validation) does not make it so.

#### 5.7.8 Resolution Algorithm

The following expresses [§5.7.1](#571-image-roots)–[§5.7.7](#577-when-no-asset-is-found), and the card back resolution of [§5.5.1](#551-resolving-a-card-back), as pseudocode. Where it and the prose disagree, the prose governs.

```
ResolveCardImage(deck, card_id, variant_key, kind, target):
  file = LookupCardImage(deck, card_id, variant_key, kind, target)
  if file != none:
    return file

  if variant_key != none:
    # §5.7.6: an absent variant falls back to the card's default
    file = LookupCardImage(deck, card_id, none, kind, target)
    if file != none:
      return file

  # §5.7.7
  if deck.library has a reference deck R and deck != R
       and card_id not in deck.excluded_cards:
    return ResolveCardImage(R, card_id, variant_key, kind, target)

  return none


LookupCardImage(deck, card_id, variant_key, kind, target):
  stem = card_id.base
  if variant_key != none:
    stem = stem + "." + variant_key
  subpath = CardSubpath(card_id)          # major_arcana/ or minor_arcana/<suit>/

  if kind == scalable:
    return LookupInDirectory(deck/scalable/subpath, stem, [svg])

  # §5.7.1: the image roots of this kind, with their sizes
  candidates = [ root for root in TopLevelDirectories(deck)
                      if RootKind(root) == kind ]

  # §5.7.4: best first, then the next best, and so on
  for root in SortByRank(candidates, kind, target):
    file = LookupInDirectory(root/subpath, stem, ChainFor(kind))
    if file != none:
      return file

  return none


ResolveCardBack(deck, design_key, kind, target):
  # §4.2: an explicit path is an instruction, in every kind and size
  if deck.card_backs.designs[design_key].image != none:
    return that path

  candidates = [ root for root in TopLevelDirectories(deck)
                      if RootKind(root) == kind
                      and Exists(root/card_backs/) ]

  for root in SortByRank(candidates, kind, target):
    file = LookupInDirectory(root/card_backs, design_key, ChainFor(kind))
    if file != none:
      return file

  # §5.5.1: the unsized top-level directory, consulted last
  file = LookupInDirectory(deck/card_backs, design_key, ChainFor(kind))
  if file != none:
    return file

  # §5.5.1: it declares no kind, so an application MAY take what is there
  file = LookupInDirectory(deck/card_backs, design_key, [png, webp, avif, jpeg|jpg, svg])
  if file != none:
    return file

  # §5.5.1: no reference-deck step — the application supplies its own
  return none


LookupInDirectory(dir, stem, chain):
  # §5.7.5: fixed order, skipping what this application cannot decode
  for ext in chain:                       # [png, webp, avif, jpeg|jpg]; [svg] in scalable/
    for name in FileNamesFor(stem, ext):  # jpeg and jpg are one entry;
                                          # in an ANSI root, any extension matches
      if Exists(dir/name) and CanDecode(dir/name):
        return dir/name
  return none


SortByRank(roots, kind, target):
  # §5.7.4
  prefer_at_least = (kind != ansi)
  rank(root):
    size = SizeOf(root)
    wrong_side = (size < target) if prefer_at_least else (size > target)
    tiebreak   = size if prefer_at_least else -size
    return (wrong_side, abs(size - target), tiebreak)
  return roots sorted ascending by rank
```

Two properties of this shape are deliberate. `LookupCardImage` walks the ranked candidates rather than stopping at the best one, so that a root the application cannot decode ([§5.7.5](#575-the-extension-chain)) costs it a fallback rather than the card. And the reference-deck step sits in `ResolveCardImage`, outside the per-deck lookup, so a reference deck is consulted once the deck itself is exhausted in every kind and size — never in the middle of size selection.

`ResolveCardBack` reuses `SortByRank` and `LookupInDirectory` unchanged, which is the point of giving card backs a directory of their own inside each image root: a back gets the same size selection a card gets, and an implementation gets it for free.

ANSI files are exempt from the extension chain: [§5.4](#54-ansi-art) allows them any extension, so in an ANSI root `LookupInDirectory` matches on stem alone and determines the file's kind from its content. An application MUST apply [§10.2](#102-terminal-escape-injection) to any ANSI file it writes to a terminal.

## 6. Internationalization

Per-card display string (e.g., card names, suit names, alt text) are declared in `names/<tag>.toml`, e.g., `names/en.toml`.

### 6.1 Language Tags

`<tag>` MUST be a well-formed IETF BCP 47 language tag:

```
names/en.toml
names/pt-BR.toml
names/zh-Hans.toml
```

- Tags SHOULD be canonical: the shortest available ISO 639 subtag (`en`, not `eng`), lowercase language, titlecase script, uppercase region.
- Applications MUST compare tags case-insensitively, since some filesystems are. A deck MUST NOT ship two name files whose tags differ only in case.
- `[deck].default_language` declares the tag of the deck's default names file. If absent, applications assume `en`.

### 6.2 Language Resolution

Given a requested tag, applications resolve it using the *Lookup* scheme of RFC 4647: try the requested tag, then progressively remove trailing subtags, then the deck's `default_language`. A key that no name file supplies falls through to the further fallbacks given in [§6.3](#63-display-name-resolution).

For a request of `pt-BR`, that is `names/pt-BR.toml`, then `names/pt.toml`, then the default language file.

Resolution happens per key, not per file: a `pt-BR` file that overrides only a handful of names inherits the rest from `pt`, and anything neither supplies comes from the default language file.

```toml
# Metadata about this name file (optional); see Name File Licensing
[metadata]
source = "Names and alt text written by Jane Doe."
license = "CC-BY-4.0"

# Card name localization
[major_arcana]
00 = "The Fool"
01 = "The Magician"
# ...

[minor_arcana]
name_template = "{rank} of {suit}"  # Optional: how minor arcana names are composed

[minor_arcana.wands]
ace = "Ace of Wands"  # Optional: overrides the template for this card
two = "Two of Wands"
# ...

[suits]
wands = "Wands"
stars = "Stars"      # Custom suit
# ...

[ranks]
page = "Page"
knight = "Warrior"   # Custom rank
# ...

# Alt text localization
[alt_text.major_arcana]
00 = "A young person in colorful clothes steps off a cliff, carrying a white rose. A small dog jumps at their heels."
01 = "A figure standing at a table with the four suit symbols, one hand raised toward the sky, the other pointing to the ground."
# ...

[alt_text.minor_arcana.wands]
ace = "A hand emerging from a cloud holds a flowering wooden staff."
two = "A figure in a flowing robe stands on a cliff holding two staves, looking out over the sea."
# ...

# Card back design names (optional)
[card_backs]
classic = "Classic Back"
alternative = "Starry Night"

# Card back alt text (optional)
[alt_text.card_backs]
classic = "A blue and white geometric pattern featuring roses and lilies"
alternative = "A starry night sky pattern with gold accents"

# Card variants, keyed by extended canonical ID (optional)
[card_variants]
"major_arcana.06:two_women" = "The Lovers"

[alt_text.card_variants]
"major_arcana.06:two_women" = "Two women stand hand in hand beneath a winged figure."
```

Name files are sparse: a name file MAY contain only the keys it wishes to supply. Applications MUST merge name files key by key rather than requiring a complete set and MUST NOT treat a missing key as an error.

#### 6.2.1 Name File Metadata

The `[metadata]` table is OPTIONAL. It describes the name file itself rather than any card in it.

| Key | Purpose |
| --- | --- |
| `source` | Who or what produced the strings in this file |
| `license` | SPDX license expression governing the strings in this file |
| `license_files` | Paths, relative to the deck root, to the full license text and any notices |
| `copyright` | The copyright notice, verbatim as the rights holder wrote it |
| `attribution` | The credit line the license requires downstream users to display |

The OPTIONAL `[metadata.alt_text]` subtable takes the same keys and overrides them for alt text alone. See [Name File Licensing](#73-name-file-licensing).

### 6.3 Display Name Resolution

Each rule below is applied to name files in the order given by [Language Resolution](#62-language-resolution) — the requested tag, its progressively shortened forms, then the deck's `default_language` — before moving on to the next fallback.

A resolved display string is used **verbatim**. Applications MUST NOT apply case conversion, or any other transformation, to a string a deck supplies; a deck that writes `"ace of torches"` means those exact characters. Case transformation appears in this specification only as a fallback for keys the deck never gave a string for.

Suit names are resolved first by searching for `[suits].<key>` in the name files, then (for custom suits only) `[custom_cards.minor_arcana.<key>].name`, then the title-cased key.

Rank names are resolved via `[ranks].<key>` in the name files, then the title-cased key.

Major arcana names are resolved via `[major_arcana].<key>` in the name files, then (for custom cards only) `[custom_cards.major_arcana.<key>].name`, then the [reference deck](#131-decks-and-libraries)'s name for that ID, then — for a canonical key, and where no reference deck is configured — the name given in [Appendix C](#appendix-c-canonical-card-names-informative). A custom major arcana key that reaches the end of this chain falls back to the title-cased key.

Minor arcana names are resolved via `[minor_arcana.<suit>].<rank>` in the name files, then by [composition](#631-minor-arcana-name-composition) from the card's suit and rank names.

Alt text is resolved via `[alt_text.*]` in the name files, then (for custom cards only) the entry's `alt_text` field.

Card back design names are resolved via `[card_backs].<key>` in the name files, then `[card_backs.designs.<key>].name`, then the [title-cased key](#135-names-and-files). Design alt text is resolved via `[alt_text.card_backs].<key>`, then the design's `alt_text` field. A back discovered with no declaration anywhere is therefore still displayable: `card_backs/classic.png` shows as "Classic".

Card variant names are resolved via `[card_variants]."<extended-id>"` in the name files, then `[card_variants."<canonical-id>".variants.<key>].name`, then the name of the card itself. Variant alt text is resolved via `[alt_text.card_variants]."<extended-id>"`, then the variant's `alt_text` field, then the alt text of the card itself — which will describe a variant only approximately, so variants SHOULD carry their own.

#### 6.3.1 Minor Arcana Name Composition

Because a deck MAY rename its suits and ranks, most decks need not write out all 56 minor arcana names. Where a name file gives no explicit name for a minor arcana card, its name is composed from a template:

```toml
[minor_arcana]
name_template = "{rank} of {suit}"
```

`{rank}` and `{suit}` are replaced by the rank and suit names resolved above; no other placeholders are defined, and an application MUST leave any other braced text in the template alone. The template is resolved by the same [Language Resolution](#62-language-resolution) rules as any other key, so a translation supplies its own. If no name file supplies one, the template is `"{rank} of {suit}"`.

Composition applies to custom suits and custom ranks exactly as it does to canonical ones. Since a suit or rank name always resolves — falling back to the title-cased key — composition always yields a name.

Because the template interpolates already-resolved strings and is itself never case-converted, a deck expresses its typographic convention simply by writing its suit and rank names in the case it wants. A deck whose cards read "ace of torches" writes `wands = "torches"` and `ace = "ace"`; one that reads "Ace of Torches" writes `"Torches"` and `"Ace"`. Cards that do not follow the deck's own pattern keep an explicit entry under `[minor_arcana.<suit>]`, which always wins over the template.

Where a deck supplies no value at any level, applications MAY fall back to the corresponding string from the [reference deck](#131-decks-and-libraries).

### 6.4 Alt Text Guidelines

- Alt text SHOULD describe the visual elements of the card without interpretation.
- A deck SHOULD include at least one language file carrying alt text, so that the deck is usable with a screen reader.
- Every card variant SHOULD carry its own alt text, since what distinguishes variants is exactly what alt text describes.
- Alt text for custom cards follows the same pattern in the name files, using the custom card's canonical ID.
- Alt text given in `[custom_cards]`, `[card_variants]` or `[card_backs.designs]` is a fallback only; a name file always wins.

**Alt text and `description` are not the same field twice.** Several tables carry both — `[deck]`, `[editions]`, `[card_backs.designs]` — and they differ in three ways:

| | alt text | `description` |
| --- | --- | --- |
| Stands in for the image, for a reader who cannot see it | Yes | No; it is shown *beside* the image |
| Localized | Yes — every name file MAY carry it | No; written once, in `default_language` |
| MAY interpret, credit or give provenance | No | Yes |

The practical consequence is the first rule above read backwards: anything a screen-reader user needs belongs in alt text, because alt text is the copy that gets translated. A `description` that paraphrases the alt text is redundant in one language and absent in every other.

Note: a deck reproducing well-known artwork, such as the Rider-Waite-Smith, is a good candidate for comprehensive alt text in its default language file, because the same descriptions serve every deck that reproduces it.

## 7. Licensing and Attribution

A deck is comprised of several components that can have separate licensing terms.

- The license specified by `[deck].license` describes the artwork.
- The license in the `[metadata].license` field of a names file covers the strings in that file, and `[metadata.alt_text]` narrows that to the alt text alone.
- A `LICENSE` file at the root of the deck, where one is present, conveys terms for whoever assembled the deck.

### 7.1 License Expressions

The `[deck].license` field SHOULD be a valid [SPDX license expression](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/) and compose:

```toml
[deck]
license = "CC0-1.0 AND LicenseRef-PublicDomain"
```

Identifiers MUST come from the [SPDX License List](https://spdx.org/licenses/) and are case-sensitive.

For terms with no SPDX identifier, use a custom `LicenseRef-` license and record the actual terms in the license file:

```toml
license = "LicenseRef-MyCustomLicense"
license_files = ["LICENSE"]
```

### 7.2 Attribution and Notices

| Field | Purpose |
| --- | --- |
| `license` | SPDX license expression governing the artwork |
| `license_files` | Paths, relative to the deck root, to the full license text and any notices. Defaults to `["LICENSE"]` when that file exists |
| `copyright` | The copyright notice, verbatim as the rights holder wrote it |
| `attribution` | The credit line the license requires downstream users to display |

```toml
[deck]
license = "CC-BY-NC-SA-3.0"
license_files = ["LICENSE"]
copyright = "© 1995-2010 Andreas Schröter"
attribution = "\"Aquatic Tarot\" by Andreas Schröter (http://www.aquatictarot.net/), licensed under CC BY-NC-SA 3.0."
```

Decks SHOULD ship the full license text in the deck directory rather than relying on `license` alone.

### 7.3 Name File Licensing

The strings in a name file are usually not the deck assembler's own work. Alt text might be written by a contributor or adapted from a published source. Each name file therefore states its own terms in its [`[metadata]`](#621-name-file-metadata) table, using the same fields as `[deck]` and with the same meanings.

Most decks need only to license their alt text:

```toml
# names/en.toml
[metadata.alt_text]
source = "Written by Jane Doe."
license = "CC-BY-4.0"
attribution = "Card descriptions by Jane Doe."
```

If instead the whole file is a single person's work, such as with translations, `[metadata]` refers to the entire file, alt text included:

```toml
# names/pt-BR.toml
[metadata]
source = "Translated by Paulo Freire."
license = "CC-BY-4.0"
license_files = ["names/LICENSE.pt-BR"]
attribution = "Portuguese translation by Paulo Freire."
```

When the two differ, `[metadata]` specifies the file's license, and `[metadata.alt_text]` is an override:

```toml
[metadata]
source = "Card names by the deck author."
license = "CC-BY-4.0"

[metadata.alt_text]
source = "Descriptions contributed by Jane Doe."
license = "CC0-1.0"
```

Key meanings:
- `source`:  who or what produced the strings.
- `attribution`: the credit line a license obliges downstream users to display.
- `license_files`: path relative to the deck root.

## 8. Extensibility

The `[app]` table is reserved for applications to record things about a deck that this specification does not model — a rendering hint, a format-specific parameter. Each application takes a subtable keyed by a [realm](#33-qualified-identifiers) it controls:

```toml
[app."land.arcana.cartomancer"]
bleed = true                    # artwork runs to the edge; draw no border
ansi_color_depth = "truecolor"  # ANSI art uses 24-bit SGR; downsample below that
ansi_glyphs = "sextants"        # needs a font covering U+1FB00–U+1FBFF
```

`[app]` is written by the deck's author, and holds properties of the deck. An application's own settings and a user's preferences are not deck data and do not belong here, however convenient it is to put them in reach.

Applications MUST ignore any `[app]` subtable they do not own, and validators MUST NOT report unknown keys within `[app]`. Top-level table names outside `[app]` are reserved for future versions of this specification.

## 9. Conformance and Validation

### 9.1 Conforming Deck

A conforming deck:

- MUST contains a readable `deck.toml` well-formed under [§2.3.1](#231-toml-files).
- MUST contain a `[deck]` table that has the required fields from [§4.1](#41-deck).
- MUST have at least one card asset, discoverable under [§5.1](#51-asset-discovery)
- MUST produces no errors under [§9.4](#94-validation-rules).

### 9.2 Errors and Warnings

A validator's reports two kinds of violations:

- An error makes a deck non-conforming. The deck is broken in a way this specification defines an outcome for and an application MAY refuse it.
- A warning marks something an author probably did not intend, or a condition this specification allows but has an opinion about. An application MUST load a deck that produces only warnings.

### 9.3 Conforming Applications and Validators

A conforming application:

- MUST implement deck discovery ([§2.2](#22-the-deck-library), [§5.1](#51-asset-discovery)), display name resolution ([§6.3](#63-display-name-resolution)) and card image resolution ([§5.7](#57-card-image-resolution)).
- MUST support decoding PNG and JPEG ([§5.7.5](#575-the-extension-chain));
- MUST ignore `[app]` subtables it does not own ([§8](#8-extensibility)), and every table, key and value this specification does not define;
- MUST NOT reject a deck for warnings ([§9.2](#92-errors-and-warnings));

An application need not implement editions, card variants, ANSI art, SVG or localization beyond the deck's default language. Where it does not, it uses the defaults those sections define.

A conforming validator:

- MUST implement the rules in [§9.4](#94-validation-rules);

### 9.4 Validation Rules

Each rule is labelled **[E]** for error or **[W]** for warning.

1. **Required Files**:
   - **[E]** `deck.toml` MUST exist and adhere to the schema.
   - **[E]** All referenced images, licenses and name files MUST exist.

2. **Canonical ID Mapping**:
   - **[E]** Ensure all canonical IDs referenced in `deck.toml` have corresponding images in the defined directories.

3. **Localization Validation**:
   - **[E]** Verify that every key present in a localization file corresponds to a card, suit, rank, card variant, card back design or reserved key (`[minor_arcana].name_template`) the deck defines, or appears in the reserved `[metadata]` table or its `alt_text` subtable.
   - **[E]** Verify that `[minor_arcana].name_template`, where present, contains no placeholder other than `{rank}` and `{suit}`.
   - **[W]** Verify that alt text is provided for all cards in at least one language file.
   - **[E]** Verify that every name file's stem is a well-formed BCP 47 language tag, that no two differ only in case, and that `[deck].default_language` has a corresponding file.

4. **Card Back Validation**:
   - **[E]** Verify that `[card_backs].default`, where present, names a card back design the deck has — discovered from a [card back directory](#55-card-back-images) or declared with an `image` path.
   - **[W]** Where the deck has more than one card back design and neither `[card_backs].default` nor a design keyed `default` is present, report that the default rests on collation order ([§4.2](#42-card_backs)). Resolution is well defined, but the author probably did not choose it.
   - **[E]** Verify that every design key — a discovered stem or a `[card_backs.designs]` table key — is a well-formed [custom name](#32-custom-names).
   - **[W]** Report a file in a card back directory that discovery ignores: a stem containing a `.`, a stem that is not a custom name, or an extension outside the chain with no `image` path pointing at it. Such a file is usually an intended back that will never be shown.
   - **[E]** Verify that every `image` path declared under `[card_backs.designs]` exists.

5. **Identifier Validation**:
   - **[E]** Verify that every custom name matches the `custom-name` grammar of [§3.5](#35-grammar) and is not a reserved canonical key, excepting a canonical suit used as a `[custom_cards.minor_arcana]` table key.
   - **[E]** Verify that every `identifier` field, in `[deck]` and in `[editions].<key>` alike, is a well-formed qualified identifier.
   - **[E]** Verify that every `[app]` subtable key is a well-formed realm. Do not validate the contents of such a subtable, whose keys are the owning application's to define.
   - **[W]** Where a validator can see a whole library, verify that no two visible decks declare the same `[deck].identifier`. Two decks that do are a legitimate arrangement — two versions installed side by side, or a fork — so this is a warning; see [§3.4.2](#342-identifier).
   - **[W]** Verify that `[deck].identifier` is present. It is RECOMMENDED, and a deck without one cannot be referenced from another Arcana Land document ([§3.4.2](#342-identifier)).

6. **Card Variant Validation**:
   - **[E]** Verify that every card referenced in `[card_variants]` is a card the deck defines.
   - **[E]** If a variant table declares `default`, verify that the named variant exists; if it does not declare one, verify that the card has an unsuffixed image file.
   - **[E]** Verify that all referenced variant image files exist.

7. **Custom Card Validation**:
   - **[E]** Verify that every card declared in `[custom_cards]` is a card the deck has files for. A declaration for a card with no images is an error, since `[custom_cards]` no longer defines cards on its own.
   - **[E]** Verify that no custom major arcana key is a two-digit string, and that no custom rank or suit key shadows a canonical one, so that a custom ID can never collide with a canonical one.
   - **[E]** Verify that every rank named in a `ranks` list has files in that suit, and that a suit's `ranks` list contains no duplicates.
   - **[W]** Report a `position` claimed by two cards as a warning, not an error; ordering remains well defined.
   - **[E]** Verify that no card is both excluded by `[excluded_cards]` and declared in `[custom_cards]`.

8. **Edition Validation**:
   - **[E]** If more than one edition is defined, verify that `[editions].default` is present and names a defined edition ([§4.5](#45-editions)).
   - **[E]** Verify that every `[editions].<key>.card_back` names a card back design the deck has ([§4.2](#42-card_backs)).

9. **Asset Validation**:
   - **[E]** Verify that no path field — `icon`, `image`, any `license_files` entry — begins with `/`, contains a `..` segment, or resolves outside the deck root ([§2.3.2](#232-paths-in-decktoml), [§10.1](#101-path-traversal)).
   - **[E]** Verify that no directory holds two files whose stems differ only in case ([§2.3.3](#233-filename-case)).
   - **[W]** Report two files in one directory sharing a stem and differing only in a chain extension — `06.png` beside `06.webp`. Resolution is well defined ([§5.7.5](#575-the-extension-chain)), but one of the two is usually a conversion left behind.
   - **[W]** Report a card asset whose own aspect ratio differs materially from `[deck].aspect_ratio` ([§4.1](#41-deck)). Card backs are exempt: `[deck].aspect_ratio` describes the fronts ([§5.5](#55-card-back-images)).

10. **License Validation**:
   - **[E]** Verify that every file listed in a `license_files` list exists, in `[deck]` and in every name file's `[metadata]` alike.
   - **[W]** Verify that every `license` field is a well-formed SPDX license expression. A deck that fails this check MUST NOT be rejected; see [Licensing and Attribution](#7-licensing-and-attribution) for how to treat free-text values.
   - **[E]** Verify that `[metadata.alt_text]` contains no key that is not defined for `[metadata]`.

## 10. Security Considerations

A deck arrives external to the system and contains data that can be read by an application in a way an author can abuse. This section attempts to describe some of the security concerns that may arise.

### 10.1 Path Traversal

Author-supplied paths such as `icon`, `image` `license_files` could be vectors of abuse.

An application MUST reject:

- a path beginning with `/`, or otherwise absolute on the host platform
- a path containing a `..` segment
- a path that resolves a location outside the deck root.

An application MUST NOT follow a symbolic link that leads outside the deck root.

### 10.2 Terminal Escape Injection

ANSI art is a sequence of bytes an application writes to a terminal. A hostile deck can carry, among others:

- OSC 52 which write to the user's clipboard, clobbering it.
- **DA**, **DSR**, **DECRQSS** and other sequences, which can induce the terminal to write attacker-chosen bytes to the application's standard input

An application that renders ANSI art MUST therefore restrict what it passes through. It is the application's responsibility to safely display ANSI.

## Appendix A. Examples (Informative)

### A.1 Rider Waite Smith

```toml
# deck.toml
[deck]
schema_version = "2.0"
name = "Rider-Waite-Smith"
identifier = "land.arcana/deck/rider-waite-smith"
version = "1.0"
author = "Pamela Colman Smith"

license = "LicenseRef-PublicDomain AND CC0-1.0"
license_files = ["LICENSE"]
copyright = "Artwork © 1909 Pamela Colman Smith (copyright expired)"
attribution = "Original artwork by Pamela Colman Smith (1909). Digital restoration by Luciella Elisabeth Scarlett."
default_language = "en"
created_date = "1909-12-01"
updated_date = "2025-04-28"
publisher = "Original: US Games Systems, Digital: Luciella Elisabeth Scarlett"
website = "https://luciellaes.itch.io/rider-waite-smith-tarot-cards-cc0"
tags = ["traditional", "classic", "beginner-friendly"]

[card_backs]
default = "classic"

[card_backs.designs.classic]
name = "Classic RWS Back"
description = "The 1909 Rider back, digitally restored from the original printing."
```

With names and alt text in `names/en.toml`.

```toml
[metadata.alt_text]
source = "Written by Jane Doe."
license = "CC-BY-4.0"
attribution = "Card descriptions by Jane Done, licensed under CC BY 4.0."

[alt_text.major_arcana]
00 = "A young person in colorful clothes steps off a cliff."
# ...

# Card back alt text
[alt_text.card_backs]
classic = "A lattice of blue and white roses and lilies."
```

### A.2 Simple Custom Deck 

This specification is designed so that creating a custom deck needs only a minimal `deck.toml` file, with the card images placed in a reasonable directory structure.

```
my-custom-deck/
  deck.toml
  card_backs/
    main.png
  h1200/
    major_arcana/
      00.png          # The Fool
      01.png          # The Magician
      ...
      21.png          # The World
    minor_arcana/
      wands/
        ace.png
        two.png
        ...
        king.png
      cups/
        ace.png
        ...
  names/
    en.toml           # Contains both card names and alt text
```

The whole of `deck.toml` is then:

```toml
[deck]
name = "My Custom Deck"
version = "1.0"
schema_version = "2.0"
```

By following this structure and file-naming convention, applications can automatically detect the images and map them to the correct cards based on their canonical IDs.

### A.3 Custom Deck with Non-Standard Names and Multiple Card Backs

This example shows a complex custom deck with custom suits, a new custom major arcana card and multiple card backs.

```toml
# deck.toml
[deck]
name = "Elemental Torches Tarot"
author = "Fire Sage"
version = "1.0"
schema_version = "2.0"
description = "A fire-themed tarot deck with renamed suits and an additional elemental card."
created_date = "2026-01-01"
website = "https://example.com/elemental-torches"
tags = ["elemental", "fire-themed"]


[custom_cards.major_arcana.elemental_force]
name = "The Elemental Force"
alt_text = "A vortex of the four elements swirling together in perfect harmony."
position = 22

[card_backs]
default = "flames"

[card_backs.designs.flames]
name = "Flame Pattern"
description = "The standard back, drawn to match the wands suit."

[card_backs.designs.embers]
name = "Glowing Embers"
description = "Drawn for the deluxe printing, on darker stock."

# Define deck editions with different card backs
[editions]
[editions.standard]
name = "Elemental Torches (Standard Edition)"
card_back = "flames"

[editions.deluxe]
name = "Elemental Torches (Deluxe Edition)"
card_back = "embers"
```

And the names and alt-text in `names/en.toml`:
```toml
[major_arcana]
00 = "The Wanderer" # Custom name for The Fool
01 = "The Alchemist" # Custom name for The Magician
# ... and so on

# This deck's renamed suits and ranks.
[suits]
wands = "Torches"
cups = "Waters"
swords = "Winds"
pentacles = "Stones"

[ranks]
page = "Student"
knight = "Warrior"
queen = "Priestess"
king = "Master"

# Alt text for standard and custom cards
[alt_text.major_arcana]
00 = "A traveler with a backpack walks toward a fiery mountain, unaware of the cliff edge ahead."
# ... and so on
elemental_force = "A vortex of the elements swirling together in harmony."

# Card back alt text
[alt_text.card_backs]
flames = "A dynamic pattern of red and orange flames swirling around a central spark"
embers = "A dark background with scattered glowing embers and occasional small flames"
```

### A.4 Deck with Renamed Suits and a Lowercase Convention

A deck that prints every minor arcana in lower case.

```toml
# names/en.toml
[minor_arcana]
name_template = "{rank} of {suit}"

[suits]
wands = "torches"
cups = "cups"
swords = "swords"
pentacles = "pentacles"

[ranks]
ace = "ace"
two = "two"
# ... through ten
page = "princess"
knight = "prince"
queen = "queen"
king = "king"
```

Cards that break the deck's own pattern are written out individually and take precedence over the template:

```toml
[minor_arcana.pentacles]
ace = "one of pentacles"

[major_arcana]
00 = "the Fool"
21 = "The world"
```

### A.5 Deck with Card Variants

Somes deck provide multiple cards with different artwork for the same canonical ID.

```
inclusive-tarot/
  deck.toml
  h1200/
    major_arcana/
      06.png                  # The Lovers, default artwork
      06.two_women.png        # The Lovers, with two women
      06.two_men.png          # The Lovers, with two men
      ...
    minor_arcana/
      cups/
        two.png
        two.two_women.png     # Two of Cups, with two women
        ...
  names/
    en.toml
```

The variants above are discovered through the directory structure and only the alt text has to be written:

```toml
# names/en.toml
[alt_text.major_arcana]
06 = "A man and a woman stand hand and hand beneath a winged figure, a tree behind each of them."

[alt_text.card_variants]
"major_arcana.06:two_women" = "Two women stand hand in hand beneath a winged figure, a tree behind each of them."
"major_arcana.06:two_men" = "Two men stand hand in hand beneath a winged figure, a tree behind each of them."
```

## Appendix B. Reserved and Deprecated Names

The names below were defined by an earlier version of this specification and are no longer defined by this one. A future version of this specification MUST NOT reuse any of them with a new meaning.

Applications MUST ignore these names in a 2.0 deck.

| Name | Was | Status |
| --- | --- | --- |
| `[deck].id` | The deck's identifier in 1.0. It was both the library handle and the global identity and was inadequate as either | Removed in 2.0. The handle is the [directory name](#341-the-directory-name-is-the-handle) and the global identity is [`[deck].identifier`](#342-identifier).|
| `[aliases]` | Suit and court display names in 1.0 | Removed in 2.0. Superseded by [name files](#6-internationalization) |
| `[variants]` | Deck editions in 1.0 | Renamed to [`[editions]`](#45-editions) in 2.0. The word "variant" now means a [card variant](#46-card_variants)|
| `[card_backs.variants]` | Card back designs in 1.0 | Renamed to [`[card_backs.designs]`](#42-card_backs) in 2.0, so that "variant" has one meaning.|
| `[deck.excluded_cards]` | Excluded cards, nested under `[deck]` in 1.0 | Moved to top-level [`[excluded_cards]`](#44-excluded_cards) in 2.0 |
| `[deck.companions]` | Never specified. Present in early implementations as a list of related documents, each with `id`, `name` and `uri` | Not defined by any version. Superseded by [qualified identifiers](#33-qualified-identifiers), by which another Arcana Land document names a deck rather than the deck naming it |
| `image` on `[custom_cards.major_arcana.<key>]` | An explicit path to a custom card's image in 1.0 | Removed in 2.0. A custom card's images come from [discovery](#51-asset-discovery), like every other card's, which is what lets one card exist in several sizes and formats |
| `id` on `[custom_cards.major_arcana.<key>]` | A custom card's identifier in 1.0 | Removed in 2.0. The table key is the card's key |
| `[remap_major_arcana]` | A table remapping major arcana display positions in 1.0 | Removed in 2.0. No published deck used it and it was unnecessary |

## Appendix C. Canonical Card Names (Informative)

This appendix publishes conventional English names for the twenty-two major arcana to facilitate display name resolution from [§6.3](#63-display-name-resolution).

Nothing in this specification treats a deck as wrong for disagreeing with this table and no conforming application does either.

| Key | Name |
| --- | --- |
| `00` | The Fool |
| `01` | The Magician |
| `02` | The High Priestess |
| `03` | The Empress |
| `04` | The Emperor |
| `05` | The Hierophant |
| `06` | The Lovers |
| `07` | The Chariot |
| `08` | Strength |
| `09` | The Hermit |
| `10` | Wheel of Fortune |
| `11` | Justice |
| `12` | The Hanged Man |
| `13` | Death |
| `14` | Temperance |
| `15` | The Devil |
| `16` | The Tower |
| `17` | The Star |
| `18` | The Moon |
| `19` | The Sun |
| `20` | Judgement |
| `21` | The World |

Suit and rank names can be derived from their keys by the [title-cased key](#135-names-and-files) rule.

> Note: A [canonical ID is a slot](#311-a-canonical-id-is-a-slot). A. E. Waite infamously diverged from the Marseilles tradition by swapping the positions of Justice and Strength. Because `major_arcana.08` represents "the card the deck assigned to position 8" and not specifically Strength, a deck following the Marseille tradition can be represented by providing the appropriate strings in its name file.

## Appendix D. Changelog

### Version 2.0

An application MAY support 1.0 decks alongside 2.0 ones. Where it does, it reads them under 1.0's rules.

Breaking changes:
- **Breaking**: Removed the `[aliases]` section in favor of using names files.
- **Breaking:** Renamed the `[variants]` section to `[editions]`
- **Breaking**: Renamed `[card_backs.variants]` to `[card_backs.designs]`.
- **Breaking:** Moved `[deck.excluded_cards]` to a top-level `[excluded_cards]`.
- **Breaking:** Removed the `image` and `id` fields from `[custom_cards.major_arcana.<key>]`.
- **Breaking:** Keyed `[app]` subtables by a realm the application controls, rather than by a bare custom name.
- **Breaking:** Removed `[deck].id` and `[editions].<key>.id`, and reworked deck identity.
- **Breaking:** Removed `[remap_major_arcana]`.

Document structure:
- Restructured the document as a specification
- Adopted BCP 14 keywords explicitly, and rewrote every lowercase `should`/`must` as either a keyword or a plainly non-normative verb.
- Replaced the regex identifier forms with one consolidated [ABNF grammar](#35-grammar).
- Lifted fields out of TOML comments into [normative field tables](#4-decktoml-reference).

Newly specified:
- [The deck library](#22-the-deck-library): the XDG search path, non-recursive scanning, `deck.toml` as the marker, and first-root-wins shadowing by directory name.
- [Card image resolution](#57-card-image-resolution): image roots, size selection within a kind, the `png`/`webp`/`avif`/`jpeg` extension chain with PNG and JPEG as the mandatory decode baseline, and the algorithm as pseudocode. Previously every consumer had to invent this.
- [Card back discovery](#55-card-back-images): a `card_backs/` directory at the top level or inside any image root, design keys taken from filenames, and card backs resolved by the same size selection cards get — so a back can exist at several resolutions, and in ANSI, which 1.0 gave no way to express.
- [File format and encoding](#23-file-format-and-encoding): TOML 1.0.0, UTF-8, path base and separator, and the filename case rule.
- [Security considerations](#10-security-considerations): path traversal through author-supplied path fields, and terminal escape injection through ANSI assets.
- [Appendix C](#appendix-c-canonical-card-names-informative) publishes the canonical major arcana names, so that the fallback the name-resolution chain ends in is resolvable without a reference deck installed.
- Added `[editions].default`, and stated what an edition actually does.

Naming and Identity:
- Formalized display name resolution rules.
- Added qualified identifiers (`<realm>/<path>`) for decks.
- Added section formalizing custom names and fields.

Custom Cards:
- Made custom cards discoverable from the directory structure.
- Added card variants and extended canonical IDs.
- Allowed custom `ranks` for canonical suits
- Allowed custom minor arcana name composition with `name_template`

Internationalization:
- Specified name file language tags as BCP 47 (RFC 5646) and added `default_language`.
- Drew the boundary between alt text and `description` ([§6.4](#64-alt-text-guidelines)): alt text stands in for the image and is localized, `description` sits beside it and is not. Version 1.0 defined both on a card back and distinguished neither, and its own examples used `description` for a paraphrase of the alt text in one place and for a credit line in another.

Licensing:
- Specified deck's `license` field to use SPDX. Also added `license_files` and `copyright`.
- Added a `[metadata]` table for licensing fields

ANSI Art:
- Required that a file's kind be detected from its content rather than its extension, and clarified that plain text art is UTF-8 and needs no escape sequences to be valid.
- Recommended that applications honor a SAUCE record where a file carries one.

Extensibility:
- Defined what `[app]` is for, and required applications to ignore subtables they do not own.
- Reserved top-level table names outside `[app]` for future versions of this specification.
