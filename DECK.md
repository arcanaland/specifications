# Tarot Deck Specification

> Maintained By: [Arcana Land](https://github.com/arcanaland)
>
> Version: 2.0

## Table of Contents

- [1. Introduction](#1-introduction)
  - [1.1 Scope and Design Goals](#11-scope-and-design-goals)
  - [1.2 Document Conventions](#12-document-conventions)
  - [1.3 Terminology](#13-terminology)
  - [1.4 Versioning and Compatibility](#14-versioning-and-compatibility)
  - [1.5 References](#15-references)
- [2. Deck Structure](#2-deck-structure)
  - [2.1 Directory Skeleton](#21-directory-skeleton)
  - [2.2 The Deck Library](#22-the-deck-library)
    - [2.2.1 Locating Library Roots](#221-locating-library-roots)
    - [2.2.2 Scanning](#222-scanning)
    - [2.2.3 Shadowing](#223-shadowing)
  - [2.3 File Format and Encoding](#23-file-format-and-encoding)
- [3. Identity and Identifiers](#3-identity-and-identifiers)
  - [3.1 Canonical IDs](#31-canonical-ids)
    - [3.1.1 A Canonical ID Is a Slot](#311-a-canonical-id-is-a-slot)
    - [3.1.2 Card References and the Variant Suffix](#312-card-references-and-the-variant-suffix)
  - [3.2 Custom Names](#32-custom-names)
  - [3.3 Qualified Identifiers](#33-qualified-identifiers)
  - [3.4 Deck Identity](#34-deck-identity)
  - [3.5 Grammar](#35-grammar)
- [4. deck.toml Reference](#4-decktoml-reference)
  - [4.1 `[deck]`](#41-deck)
  - [4.2 `[card_backs]`](#42-card_backs)
  - [4.3 `[cards]`](#43-cards)
    - [4.3.1 Card Numbers](#431-card-numbers)
    - [4.3.2 Ordering](#432-ordering)
  - [4.4 `[suits]`](#44-suits)
  - [4.5 `[excluded_cards]`](#45-excluded_cards)
  - [4.6 `[editions]`](#46-editions)
  - [4.7 `[card_variants]`](#47-card_variants)
- [5. Card Assets](#5-card-assets)
  - [5.1 Asset Discovery](#51-asset-discovery)
  - [5.2 Vector Graphics](#52-vector-graphics)
  - [5.3 Raster Graphics](#53-raster-graphics)
  - [5.4 ANSI Art](#54-ansi-art)
  - [5.5 Card Back Images](#55-card-back-images)
  - [5.6 Aspect Ratio](#56-aspect-ratio)
  - [5.7 Card Image Resolution](#57-card-image-resolution)
    - [5.7.1 Image Roots](#571-image-roots)
    - [5.7.2 Extensions, Stems and Bases](#572-extensions-stems-and-bases)
    - [5.7.3 Size Selection Within a Kind](#573-size-selection-within-a-kind)
    - [5.7.4 The Extension Chain](#574-the-extension-chain)
    - [5.7.5 Variants](#575-variants)
    - [5.7.6 When No Asset Is Found](#576-when-no-asset-is-found)
    - [5.7.7 Resolving a Card Back](#577-resolving-a-card-back)
    - [5.7.8 Resolution Summary](#578-resolution-summary)
- [6. Internationalization](#6-internationalization)
  - [6.1 Language Tags](#61-language-tags)
  - [6.2 Language Resolution](#62-language-resolution)
    - [6.2.1 Name File Metadata](#621-name-file-metadata)
  - [6.3 Display Name Resolution](#63-display-name-resolution)
    - [6.3.1 Minor Arcana Name Composition](#631-minor-arcana-name-composition)
  - [6.4 Alt Text Guidelines](#64-alt-text-guidelines)
- [7. Licensing and Attribution](#7-licensing-and-attribution)
  - [7.1 License Expressions](#71-license-expressions)
  - [7.2 Attribution and Notices](#72-attribution-and-notices)
  - [7.3 Name File Licensing](#73-name-file-licensing)
- [8. Extensibility](#8-extensibility)
- [9. Conformance and Validation](#9-conformance-and-validation)
  - [9.1 Conforming Deck](#91-conforming-deck)
  - [9.2 Errors and Warnings](#92-errors-and-warnings)
  - [9.3 Conforming Applications and Validators](#93-conforming-applications-and-validators)
  - [9.4 Validation Rules](#94-validation-rules)
- [10. Security Considerations](#10-security-considerations)
  - [10.1 Path Traversal](#101-path-traversal)
  - [10.2 Terminal Escape Injection](#102-terminal-escape-injection)
- [Appendix A. Examples (Informative)](#appendix-a-examples-informative)
  - [A.1 Simple Custom Deck](#a1-simple-custom-deck)
  - [A.2 Rider-Waite-Smith](#a2-rider-waite-smith)
  - [A.3 Renamed Suits, a Custom Card and Multiple Editions](#a3-renamed-suits-a-custom-card-and-multiple-editions)
  - [A.4 A Lowercase Typographic Convention](#a4-a-lowercase-typographic-convention)
  - [A.5 Deck with Card Variants](#a5-deck-with-card-variants)
  - [A.6 A Deck with Extra Major Arcana](#a6-a-deck-with-extra-major-arcana)
  - [A.7 A Second Card at a Number Already Taken](#a7-a-second-card-at-a-number-already-taken)
- [Appendix B. Reserved and Deprecated Names](#appendix-b-reserved-and-deprecated-names)
- [Appendix C. Canonical Card Names (Informative)](#appendix-c-canonical-card-names-informative)
- [Appendix D. Changelog](#appendix-d-changelog)

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

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY" and "OPTIONAL" in this document are to be interpreted as described in BCP 14 ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) when, and only when, they appear in all capitals. Where this document writes "should", "must" or "may" in lower case, the word carries its ordinary English sense and imposes no requirement.

A section whose title carries the suffix (Informative) contains no requirements, and everything else in this document is normative. Whatever section they appear in, all **Notes** and all **Examples** are informative. Where an example appears to conflict with a normative rule, the rule governs and the example is in error.

This specification addresses three kinds of actors: deck authors who craft a `deck.toml` and arrange files around it, applications that read a deck in order to present it to a user, and validation tools that check a deck against this specification.

### 1.3 Terminology

| Term | Meaning |
| --- | --- |
| **deck** | A directory containing a `deck.toml`, together with the card assets and name files arranged around it. |
| **deck root** | The directory that directly contains a deck's `deck.toml`. Every path in `deck.toml` is relative to it. |
| **directory name** | The name of the deck root's own directory: the deck's handle within a library ([§3.4](#34-deck-identity)). |
| **deck library** | An ordered list of **library roots**, each a directory whose immediate children are candidate deck roots ([§2.2](#22-the-deck-library)). |
| **reference deck** | A deck a library designates as the source of last resort for a display string or an asset another deck does not supply. A library MAY designate one. It is not a property of any deck. Where none is configured, [Appendix C](#appendix-c-canonical-card-names-informative) supplies the canonical major arcana names. |
| **card** | One addressable image in a deck, named by a canonical ID. |
| **major arcana** | The cards keyed under `major_arcana`. The twenty-two keyed `00`–`21` are the canonical major arcana. |
| **extended major arcanum** | A major arcanum keyed beyond the canonical numbers into `22`–`99` |
| **minor arcana** | The suited cards, canonically fifty-six, keyed by **suit** and **rank** under `minor_arcana`. The canonical suits are `wands`, `cups`, `swords` and `pentacles`. The canonical ranks are `ace` through `ten`, then `page`, `knight`, `queen` and `king`. A deck MAY define others. |
| **card type** | Which of the two arcana a card belongs to: `major_arcana` or `minor_arcana`. Distinct from **kind** ([§5.7.1](#571-image-roots)), which distinguishes scalable, raster and ANSI assets. |
| **canonical ID** | The identifier by which this specification names a card: `major_arcana.<key>` or `minor_arcana.<suit>.<rank>` ([§3.1](#31-canonical-ids)). It attaches no meaning. |
| **card reference** | A canonical ID, optionally followed by a **variant suffix** (`:` and a variant key). `major_arcana.06` and `major_arcana.06:two_women` are both card references. The suffixed form is also called a **variant reference**. |
| **card variant** | An alternative artwork for a card the deck already contains, named by a variant key. Variants of a card are interchangeable and denote the same meaning. |
| **card back design** | One of the card back images a deck ships, named by a design key ([§4.2](#42-card_backs)). |
| **edition** | A printing of a deck that shares the deck's card fronts but selects a different card back and has its own metadata ([§4.6](#46-editions)). |
| **custom name** | An identifier the deck author coins: custom card, suit, rank, card back design, edition and card variant keys ([§3.2](#32-custom-names)). |
| **card number** | The number printed on a card's face, held as a display string ([§4.3.1](#431-card-numbers)). Distinct from **position**, which orders cards and is never displayed. |
| **position** | An integer sort key placing a major arcanum in the deck's sequence ([§4.3.2](#432-ordering)). |
| **qualified identifier** | An identifier naming an Arcana Land entity unambiguously across authors, composed of a **realm** (a domain name the author controls, written in reverse) and a path ([§3.3](#33-qualified-identifiers)). |
| **name file** | A `names/<tag>.toml` file holding **display strings** for one language tag, such as card, suit and rank names and alt text. |
| **title-cased key** | The display string derived from a key where nothing else supplies one: each `_` becomes a space and the first character of each word is uppercased. |
| **base** | The part of a card asset's file stem before the first dot. In `06.two_women.png` the stem is `06.two_women` and the base is `06` ([§5.7.2](#572-extensions-stems-and-bases)). |

### 1.4 Versioning and Compatibility

Every deck declares the version of this specification it is written against in `[deck].schema_version`, as `"<major>.<minor>"`: two decimal integers separated by a dot. The compatibility contract binds this specification, not any deck or application:

- A minor version update MUST be backward and forward compatible. It MAY add new tables, keys and values, and it MAY deprecate existing ones, but it MUST NOT change or remove the behavior of anything an earlier version of the same major version defined.
- A major version update MAY be incompatible in any respect.

`[deck].version` is the deck's own version and is unrelated to `schema_version`. It is a free-form string. This specification defines no syntax for it and no ordering over it, so applications MAY compare two values for equality to detect that a deck has changed, but MUST NOT infer from two values which is the later. A deck author who wants ordered versions is expected to adopt an ordered scheme such as [semantic versioning](https://semver.org/) and to state so outside this field.

### 1.5 References

The documents below are referenced normatively unless marked informative. A dated reference applies only to the edition cited, and an undated reference applies to the latest edition.

| Reference | Title | Where used |
| --- | --- | --- |
| **BCP 14** | Key words for use in RFCs ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) | [§1.2](#12-document-conventions) |
| **RFC 5234** | Augmented BNF for Syntax Specifications: ABNF | [§3.5](#35-grammar) |
| **RFC 7405** | Case-Sensitive String Support in ABNF | [§3.5](#35-grammar) |
| **RFC 1035 §2.3.1** | Domain Names: preferred name syntax | [§3.3](#33-qualified-identifiers) |
| **BCP 47** | Tags for Identifying Languages ([RFC 5646](https://www.rfc-editor.org/rfc/rfc5646)) | [§6.1](#61-language-tags) |
| **RFC 4647** | Matching of Language Tags | [§6.2](#62-language-resolution) |
| **RFC 3339 §5.6** | Date and Time on the Internet, `full-date` | [§4.1](#41-deck) |
| **TOML 1.0.0** | [toml.io/en/v1.0.0](https://toml.io/en/v1.0.0) | [§2.3](#23-file-format-and-encoding) |
| **SPDX License List** | [spdx.org/licenses](https://spdx.org/licenses/), with the [license expression syntax](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/) | [§7](#7-licensing-and-attribution) |
| **XDG Base Directory Specification** | [specifications.freedesktop.org](https://specifications.freedesktop.org/basedir-spec/latest/) | [§2.2](#22-the-deck-library) |
| **SAUCE** (informative) | [Standard Architecture for Universal Comment Extensions](https://www.acid.org/info/sauce/sauce.htm) | [§5.4](#54-ansi-art) |
| **Esoterica Specification** (informative) | [ESOTERICA.md](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md) | [§1.1](#11-scope-and-design-goals), [§4.7](#47-card_variants) |
| **Spread Specification** (informative, proposed) | [SPREAD.md](https://github.com/arcanaland/specifications/blob/main/SPREAD.md) | [§1.1](#11-scope-and-design-goals) |

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
      22.svg               # An optional twenty-third major arcanum
    minor_arcana/
      wands/
        ace.svg
  ansi32/                  # ANSI art, 32 terminal rows
    major_arcana/
      00.ansi
    minor_arcana/
      swords/
        three.ansi
  h750/                    # Raster images, 750px tall (optional)
  h1200/                   # (etc)
  h2400/
  names/en.toml            # Localized names and alt text (optional)
  names/pt-BR.toml
```

### 2.2 The Deck Library

A **deck library** is an ordered list of **library roots**. Each root is a directory whose immediate children are candidate deck roots.

#### 2.2.1 Locating Library Roots

Applications SHOULD form the default library from the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/), taking `$XDG_DATA_HOME/tarot/decks` first and then `<dir>/tarot/decks` for each `<dir>` in `$XDG_DATA_DIRS`, in the order that variable gives them. Where `$XDG_DATA_HOME` is unset or empty it defaults to `$HOME/.local/share`, and where `$XDG_DATA_DIRS` is unset or empty it defaults to `/usr/local/share:/usr/share`.

An application MAY offer the user additional roots and MAY let the user reorder them. Nothing requires an application to use the XDG defaults at all.

#### 2.2.2 Scanning

- Scanning a root is non-recursive, so decks nested two levels or more below a root are not discovered.
- A directory is a deck if and only if it contains a regular file named `deck.toml`. A directory without one is not a deck and MUST NOT be reported as a malformed deck.
- A directory containing a `deck.toml` that cannot be read or parsed is a malformed deck. Applications SHOULD report malformed decks.

#### 2.2.3 Shadowing

Roots are searched in order and a deck is identified within the library by its directory name. Where two roots each contain a directory of the same name, the one in the earlier root wins and the later one is not reported. Shadowing occurs on directory name only. Where two visible decks declare the same `identifier`, a validator MUST report a warning.

### 2.3 File Format and Encoding

`deck.toml` and every `names/<tag>.toml` file MUST be well-formed [TOML 1.0.0](https://toml.io/en/v1.0.0) encoded as UTF-8. Applications MAY skip a leading byte-order mark and a deck SHOULD NOT write one.

Every path-valued field in `deck.toml` is interpreted relative to the deck root, MUST use `/` as its separator whatever the host filesystem uses, and MUST NOT begin with `/` or contain a `..` segment. Applications MUST reject a path that breaks these rules.

To support case-insensitive filesystems, applications MUST compare card asset stems case-insensitively. A deck MUST NOT ship two files in one directory whose stems differ only in case, and a validator reports this as an error.

## 3. Identity and Identifiers

Cards are named by canonical IDs. Keys that a deck author creates that differ from canonical names are called custom names. Arcana Land entities, such as decks, esoterica and spreads are named by qualified identifiers.

### 3.1 Canonical IDs

Cards are referenced internally using canonical IDs, which are the only way this specification identifies a card:

- Major Arcana: `major_arcana.00` to `major_arcana.99`, of which `00` to `21` are the canonical twenty-two
- Minor Arcana: `minor_arcana.<suit>.<rank>` where:
  - `<suit>`: `wands`, `cups`, `swords`, `pentacles`
  - `<rank>`: `ace`, `two`, ..., `ten`, `page`, `knight`, `queen`, `king`

All references to cards in this specification, including configuration files, custom cards and name files, MUST use these canonical IDs.

Custom cards extend this scheme using the author's own keys. For example: `major_arcana.happy_squirrel`, `minor_arcana.stars.ace`.

#### 3.1.1 A Canonical ID Is a Slot

A canonical ID denotes the card a deck defines at a given position, not a particular card of tradition. A. E. Waite infamously swapped the positions of Strength and Justice from the Marseille ordering. In this specification `major_arcana.08` means the eighth major arcana card, so a deck following the Marseille ordering simply writes Justice under `[major_arcana].08` in its name file. [Appendix C](#appendix-c-canonical-card-names-informative) publishes conventional English names for the twenty-two major arcana as a display fallback of last resort.

A deck whose extra card is not a numbered member of its sequence gives it a [custom name](#32-custom-names) instead, which denotes membership without asserting a number ([§4.3.1](#431-card-numbers)).

#### 3.1.2 Card References and the Variant Suffix

A card reference is how this specification writes a card wherever one is expected. It is a canonical ID, optionally followed by a variant suffix, which is a `:` and a variant key:

```
major_arcana.06             # a card reference
major_arcana.06:two_women   # a card reference with a variant suffix
```

A card reference with no variant suffix denotes the card's default variant. The suffix selects between different artwork of the card and does not change which card is named. `major_arcana.06:two_women` and `major_arcana.06:two_men` are the same card in the same slot with different artwork.

The suffixed form on its own is a **variant reference**, and a name file's `[card_variants]` table is keyed by it.

### 3.2 Custom Names

Custom names are the keys a deck author creates such as custom major arcana keys, custom suit keys, custom rank keys, card back design keys, edition keys and card variant keys. Every custom name MUST match the `custom-name` production in [§3.5](#35-grammar), which allows lowercase letters, digits and underscores, but does not allow a leading digit.

Further:

- A custom name MUST NOT be one of the reserved canonical keys: `major_arcana`, `minor_arcana`, the suits `wands`, `cups`, `swords` and `pentacles`, or the ranks `ace`, `two`, `three`, `four`, `five`, `six`, `seven`, `eight`, `nine`, `ten`, `page`, `knight`, `queen` and `king`.
- A custom major arcana key additionally MUST NOT be a two-digit string.

### 3.3 Qualified Identifiers

Qualified identifiers name Arcana Land entities such as tarot decks or spreads unambiguously across authors.

- `land.arcana/deck/rider-waite-smith`
- `land.arcana/spread/celtic-cross`
- `org.example.my.domain/deck/modern-witch-tarot`

A qualified identifier is composed of a **realm** and an object **path**, separated by a slash, with an OPTIONAL **fragment** after a `#`. See [§3.5](#35-grammar) for the grammar.

- The realm is a domain name the author controls, written in reverse order according to [RFC 1035 §2.3.1](https://www.rfc-editor.org/rfc/rfc1035#section-2.3.1). It ends at the first slash. A realm therefore has two labels or more, each beginning with a letter and neither beginning nor ending with a hyphen. A single bare label is not a realm. A realm is lowercase ASCII, so an internationalized domain is written in its A-label form, and `xn--bcher-kva.example` reversed is `example.xn--bcher-kva`.
- The path is one or more slash-separated segments naming an entity within that realm. A deck's path SHOULD be `deck/<name>`.
- The fragment names a target within that entity, and its meaning is the business of whichever specification owns the entity. In *this* specification, the fragment of a deck's qualified identifier is a [card reference](#312-card-references-and-the-variant-suffix): `land.arcana/deck/rider-waite-smith#major_arcana.00` refers to the card that deck files at `major_arcana.00`.

Realms are compared bytewise. Qualified identifiers are not locations and nothing in this specification implies that one can be fetched.

A qualified identifier is essentially a URI without the scheme, and Arcana Land reserves the scheme `tarot:` for the form `tarot:land.arcana/deck/inclusive-tarot#major_arcana.06:two_women`. No version of this specification defines that scheme and nothing in this document depends on it. It is recorded here for downstream implementation awareness.

### 3.4 Deck Identity

A deck has three distinct properties related to identity:

| Property | Location | Description | Uniqueness |
|---|---|---|---|
| Directory name | The filesystem | Library-scoped handle | Unique within a library root |
| `identifier` | `[deck].identifier`, RECOMMENDED | The deck's [qualified identifier](#33-qualified-identifiers) | Globally |
| `name` | `[deck].name`, REQUIRED | Display string shown to the user | Two unrelated decks can share a name |

The three are independent. A directory name is not required to match `[deck].name` nor the last segment of `[deck].identifier`. An application MUST NOT require them to agree and a validator MUST NOT report a disagreement.

A deck SHOULD provide an `identifier`, since a deck without one cannot be referenced from another Arcana Land document. Applications and validators MUST NOT synthesise one for a deck that lacks it. Two decks in one library MAY declare the same `identifier` under different directory names, although a validator warns about it.

### 3.5 Grammar

The productions below are [ABNF](https://www.rfc-editor.org/rfc/rfc5234) (RFC 5234), with the case-sensitive string notation of [RFC 7405](https://www.rfc-editor.org/rfc/rfc7405). Every string literal in this grammar is case-sensitive and lowercase.

```abnf
; ---- Card identifiers -------------------------------------------------

canonical-id    = major-id / minor-id

major-id        = %s"major_arcana" "." major-key
major-key       = canonical-major / custom-name
canonical-major = 2DIGIT

minor-id        = %s"minor_arcana" "." suit-key "." rank-key
suit-key        = canonical-suit / custom-name
rank-key        = canonical-rank / custom-name

canonical-suit  = %s"wands" / %s"cups" / %s"swords" / %s"pentacles"
canonical-rank  = %s"ace" / %s"two" / %s"three" / %s"four" / %s"five" /
                  %s"six" / %s"seven" / %s"eight" / %s"nine" / %s"ten" /
                  %s"page" / %s"knight" / %s"queen" / %s"king"

card-ref        = canonical-id [ variant-suffix ]
variant-ref     = canonical-id variant-suffix
variant-suffix  = ":" variant-key
variant-key     = custom-name

; ---- Custom names -----------------------------------------------------

custom-name     = name-start *name-char
name-start      = lcalpha / "_"
name-char       = lcalpha / DIGIT / "_"

; ---- Qualified identifiers --------------------------------------------

qualified-id    = realm "/" path [ "#" fragment ]

realm           = label 1*( "." label )
label           = lcalpha [ *61( lcalpha / DIGIT / "-" ) ( lcalpha / DIGIT ) ]

path            = segment *( "/" segment )
segment         = 1*segment-char
segment-char    = lcalpha / DIGIT / "-"

fragment        = 1*fragment-char
fragment-char   = lcalpha / DIGIT / "." / "_" / "-" / ":"

; ---- Terminals --------------------------------------------------------

lcalpha         = %x61-7A               ; a-z
DIGIT           = %x30-39               ; 0-9, from RFC 5234 Appendix B.1
```

Two constraints are not expressible in the grammar and are stated normatively:

- `canonical-major` admits any two digits, but only `00` through `21` have a name in [Appendix C](#appendix-c-canonical-card-names-informative) or any meaning shared between decks ([§3.1.1](#311-a-canonical-id-is-a-slot)). A key MUST be written with both digits.
- A `custom-name` MUST NOT be a reserved canonical key, with the one exception in [§4.4](#44-suits).

## 4. deck.toml Reference

Every table this specification defines is listed below with its fields.

A key not listed here and not under `[app]` is not defined by this specification, and [§8](#8-extensibility) reserves such names for future versions of it.

### 4.1 `[deck]`

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `schema_version` | String | Yes | n/a | The version of this specification the deck is written against as `"<major>.<minor>"` |
| `name` | String | **Yes** | n/a | The deck's display name. Not required to be unique, and not required to match the directory name ([§3.4](#34-deck-identity)). |
| `version` | String | Yes | n/a | The deck's own free-form version. |
| `identifier` | String | RECOMMENDED | none | The deck's qualified identifier ([§3.3](#33-qualified-identifiers)). A deck without one cannot be referenced from another Arcana Land document ([§3.4](#34-deck-identity)). |
| `default_language` | String | No | `"en"` | BCP 47 tag of the deck's default name file ([§6.2](#62-language-resolution)). |
| `icon` | String (path) | No | none | A preview image for the deck, assumed to share the cards' aspect ratio. |
| `aspect_ratio` | Float | No | `0.5789` | Width ÷ height of the deck's cards. |
| `author` | String | No | none | The artwork's author. |
| `description` | String | No | none | A prose description of the deck written once in `default_language` ([§6.4](#64-alt-text-guidelines)). |
| `license` | String | No | none | SPDX license expression governing the artwork ([§7.1](#71-license-expressions)). |
| `license_files` | Array of String (path) | No | `[]` | Full license texts and notices carried in the deck ([§7.2](#72-attribution-and-notices)). |
| `copyright` | String | No | none | Copyright notice, displayed verbatim. |
| `attribution` | String | No | none | Credit line to display ([§7.2](#72-attribution-and-notices)). |
| `created_date` | String | No | none | RFC 3339 `full-date` (`YYYY-MM-DD`), as described below. |
| `updated_date` | String | No | none | RFC 3339 `full-date` (`YYYY-MM-DD`), as described below. |
| `publisher` | String | No | none | The deck's publisher. |
| `website` | String | No | none | An absolute URL for the deck. |
| `tags` | Array of String | No | `[]` | Free-vocabulary categorization tags. This specification defines no registry of tag values and attaches no behavior to any of them. |

```toml
[deck]
schema_version = "2.0"
name = "Rider-Waite-Smith Tarot"
version = "1.0"
identifier = "land.arcana/deck/rider-waite-smith"
author = "Pamela Colman Smith"
icon = "deck-icon.png"
license = "CC0-1.0"
license_files = ["LICENSE"]
created_date = "1909-12-01"
tags = ["traditional", "classic"]
```

**Dates.** `created_date` and `updated_date` are RFC 3339 `full-date` values written as TOML **strings**, not TOML native dates. A quoted `"1909-12-01"` is correct, and a bare `1909-12-01`, which TOML would read as a local date, is an error. The string form is required because a date here is metadata to display and compare textually, and because TOML's date types would tempt applications to parse a precision the field does not carry.

**Aspect ratio.** `aspect_ratio` is the width of a card divided by its height, so the traditional 11:19 card is `0.5789`. It governs **layout**, meaning an application reserves space for a card by this ratio. Where an asset's own pixel ratio disagrees with it, the application MUST still preserve the asset's own ratio when scaling it, never stretching an image to fit the declared value, and SHOULD report the mismatch to the author. An `icon` is assumed to share the cards' aspect ratio.

`[deck]` holds the deck's identity and the human-facing metadata about it. Everything that is *content*, such as card backs, cards, suits, card variants, editions and exclusions, is a top-level table of its own. No table nests under `[deck]`.

### 4.2 `[card_backs]`

A **card back design** is one of the back images a deck ships, named by a **design key**. Designs are [discovered from the directory structure](#55-card-back-images) exactly as cards are, so a deck that drops `card_backs/classic.png` into place has a design keyed `classic` and need declare nothing at all. The whole of `[card_backs]` is OPTIONAL.

```toml
[card_backs]
default = "classic"

[card_backs.designs.classic]
name = "Classic RWS Back"
description = "The 1909 Rider back, reproduced from the Pamela Colman Smith printing."
alt_text = "A lattice of blue and white roses and lilies, edge to edge, with no border."
```

**`[card_backs]`**

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `default` | String | No | see below | The design key an application uses where the user or an [edition](#46-editions) has not chosen another. Where present it MUST name a design the deck has ([§9.4](#94-validation-rules)). |

Where a deck has no card back at all, an application supplies its own. Otherwise the default design is the first of these that applies: the design named by `[card_backs].default`, then the design keyed `default` where the deck has one, then the lexicographically first design key. The last rule makes the default well defined for a deck that declares nothing, and an application MUST NOT substitute filesystem order for it. A deck shipping more than one design SHOULD nonetheless declare `default` or key a design `default` rather than rely on collation, and a validator says so ([§9.4](#94-validation-rules)).

**`[card_backs.designs.<key>]`** takes a [custom name](#32-custom-names) as the design key. The table is OPTIONAL for every design and supplies only what a filename cannot.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | resolved per [§6.3](#63-display-name-resolution) | Fallback display name for this design, used where no name file supplies one. |
| `description` | String | No | none | Prose *about* the design, such as its provenance or history, for display alongside the back in a picker or an info panel. Not localized, so it is written once in the deck's `default_language`. See [§6.4](#64-alt-text-guidelines). |
| `alt_text` | String | No | none | Fallback alt text describing what the back looks like. A name file's `[alt_text.card_backs]` takes precedence and is where a deck SHOULD put it ([§6.3](#63-display-name-resolution)). |
| `image` | String (path) | No | found by discovery | An explicit path to this design's image, for a file that does not follow the naming convention or uses a format outside the extension chain ([§5.7.4](#574-the-extension-chain)). |

Declaring a design under `[card_backs.designs]` does not create it. A design the deck has no file for and no `image` path to is a [resolution failure](#576-when-no-asset-is-found) rather than a validation error, exactly as for a card.

### 4.3 `[cards]`

Cards are [discovered from the directory structure](#51-asset-discovery) so the `[cards]` table supplies what is not availble from the filename alone, such as the card's printed number, its place in the deck's sequence and fallback display strings. It is OPTIONAL in its entirety.


```toml
[cards."major_arcana.23"]
number = "XXIII"

[cards."major_arcana.happy_squirrel"]
name = "The Happy Squirrel"
alt_text = "A cheerful squirrel standing on a branch proudly holding an acorn."
position = 22
```

**`[cards."<canonical-id>"]`** takes a card's [canonical ID](#31-canonical-ids) as the table key, quoted because it contains dots. A [variant reference](#312-card-references-and-the-variant-suffix) is not accepted here and variants provide their own strings under [`[card_variants]`](#47-card_variants).

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | resolved per [§6.3](#63-display-name-resolution) | Fallback display name, used where no name file supplies one. |
| `alt_text` | String | No | none | Fallback alt text, used where no name file supplies one. |
| `number` | String | No | see [§4.3.1](#431-card-numbers) | The number printed on the card's face. |
| `position` | Integer | No | see [§4.3.2](#432-ordering) | Where the card sits in the deck's sequence. Major arcana only. |

`name` and `alt_text` are fallbacks. A deck SHOULD carry both in `names/<tag>.toml`, where they can be localized ([§6.3](#63-display-name-resolution)). There is no `image` field, because a card's images are found by the same convention as every other card's, which is what lets one card exist in several resolutions and formats at once.

An entry for a canonical minor arcanum or for `major_arcana.00` through `major_arcana.21` is always accepted, since those slots exist for every deck. An entry for any other card is an error unless the deck has files for it ([§9.4](#94-validation-rules)).

`position` is meaningful only for a major arcanum. A minor arcanum takes its place from its suit's [`ranks`](#44-suits) sequence and an application MUST ignore a `position` declared on one.

#### 4.3.1 Card Numbers

Many decks print a number on the card face and the `number` field holds that number as an opaque display string (e.g., "XXIII", "23" or "VIII½").

Where `number` is absent, a card's number follows from the shape of its key:

- A major arcanum with a two-digit key is numbered, and its number is that key's value. An application renders it by its own convention, which for a tarot deck is conventionally an upper-case Roman numeral.
- A major arcanum with a custom key is considered unnumbered.
- A minor arcanum is unnumbered.

`number` is not localized.

#### 4.3.2 Ordering

Applications that present a deck in order resolve it as follows. The major arcana come first, then the minor arcana.

Within the major arcana, cards are ordered by `position`. Every major arcanum with a two-digit key has an implicit `position` equal to that key's value. A card with a custom key and no declared `position` follows every card that has one.

Within the minor arcana, cards are ordered by their suit's [`ranks`](#44-suits) sequence. Suits with no declared order follow the four canonical suits, sorted by key, and a rank not named in any `ranks` list follows those that are, likewise sorted by key.

A declared `position` MAY fall anywhere in the sequence and MAY be negative. Where two cards claim the same position, a declared `position` precedes an implicit one, and a tie between two of the same sort breaks by key.

### 4.4 `[suits]`

A deck can hold suits and ranks beyond the canonical ones:

```toml
[suits.stars]
name = "Stars"
ranks = ["ace", "two", "three", "four", "five", "six", "seven", "eight",
         "nine", "ten", "page", "knight", "queen", "king"]

[suits.cups]
ranks = ["ace", "two", "three", "four", "five", "six", "seven", "eight",
         "nine", "ten", "princess", "page", "knight", "queen", "king"]
```

Providing  `ranks` for a canonical suit, such as in the above example, replaces that suit's canonical sequence. 

**`[suits.<key>]`** takes a [custom name](#32-custom-names) as the key, or one of the four canonical suits where the intent is to modify that suit.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | resolved per [§6.3](#63-display-name-resolution) | Fallback display name for the suit |
| `ranks` | Array of String | No | the canonical rank sequence for a canonical suit, otherwise none | The suit's rank keys in the order the deck reads them. |

Like [`[cards]`](#43-cards), `[suits]` describes rather than creates and a suit is created by placing files under `minor_arcana/<suit>/`. The whole table is OPTIONAL. Suit and rank display names resolve through `names/<tag>.toml` ([§6.3](#63-display-name-resolution)).

### 4.5 `[excluded_cards]`

```toml
[excluded_cards]
cards = ["minor_arcana.pentacles.page", "minor_arcana.pentacles.knight"]
reason = "This deck excludes these specific court cards."
```

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `cards` | Array of String | No | `[]` | Canonical IDs of cards this deck deliberately does not contain. |
| `reason` | String | No | none | Why they are excluded, for display to a user. |

An exclusion records that an absence of an expected card is deliberate, so that an application can tell a user "this deck has no court cards" rather than report missing assets.

### 4.6 `[editions]`

For decks that have multiple editions or printings sharing the same card fronts:

```toml
[editions]
default = "standard"

[editions.standard]
name = "Rider-Waite-Smith (Standard)"
card_back = "classic"
publisher = "US Games Systems"

[editions.rider_edition]
name = "Rider-Waite-Smith (Rider Edition)"
card_back = "rider"
publisher = "Rider & Company"
created_date = "1912-01-01"
```

**`[editions]`**

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `default` | String | Required where more than one edition is defined | see below | The edition key an application selects where the user has not chosen another. |

Where exactly one edition is defined and `default` is omitted, that edition is the default. Where more than one is defined, `default` is REQUIRED and MUST name a defined edition ([§9.4](#94-validation-rules)).

**`[editions.<key>]`** takes a [custom name](#32-custom-names) as the edition's handle within the deck.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | **Yes** | n/a | The edition's display name. |
| `card_back` | String | No | `[card_backs].default` | The [design key](#42-card_backs) this edition uses. MUST name a card back design the deck has ([§9.4](#94-validation-rules)). |
| `publisher` | String | No | `[deck].publisher` | The edition's publisher, where it differs from the deck's. |
| `created_date` | String | No | `[deck].created_date` | RFC 3339 `full-date`, on the terms in [§4.1](#41-deck). |

An edition MAY also carry any of the optional metadata keys [§4.1](#41-deck) defines for `[deck]`.

An edition exists to name a specific card back design and to carry metadata that differs from the main printing. A printing with a different number of cards or different front artwork is a separate deck and SHOULD NOT be represented as an edition. By design, an edition has no qualified identifier.

### 4.7 `[card_variants]`

A card variant is an alternative artwork for a card that a deck already contains. Variants are addressed by a [variant reference](#312-card-references-and-the-variant-suffix), which is the card's canonical ID followed by a colon and a variant key, such as `major_arcana.06:two_women`. File assets are named with the variant key infixed between the card's base and its extension, as in `h1200/major_arcana/06.two_women.png`.

Declaring variants in `deck.toml` is OPTIONAL and is necessary only to choose a non-default default, to supply fallback strings or to point at a file that does not follow the naming convention.

```toml
[card_variants."major_arcana.06"]
default = "two_women"

[card_variants."major_arcana.06".variants.two_women]
name = "The Lovers"
alt_text = "Two women stand hand in hand beneath a winged figure."
image = "scalable/major_arcana/06.two_women.svg"
```

**`[card_variants."<canonical-id>"]`** takes the card's canonical ID as the table key, quoted because it contains dots.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `default` | String | Required where the card has no unsuffixed file | the unsuffixed file | Which variant a bare canonical ID resolves to ([§5.7.5](#575-variants)). MUST name a variant of this card ([§9.4](#94-validation-rules)). |

**`[card_variants."<canonical-id>".variants.<key>]`** takes a [custom name](#32-custom-names) as the variant key.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | resolved per [§6.3](#63-display-name-resolution) | Fallback display name for this variant, used where no name file supplies one. |
| `alt_text` | String | No | none | Fallback alt text for this variant. Variants SHOULD carry their own ([§6.4](#64-alt-text-guidelines)). |
| `image` | String (path) | No | found by discovery | An explicit path to this variant's image, for a file that does not follow the naming convention or uses a format outside the extension chain ([§5.7.4](#574-the-extension-chain)). |

Where `default` is omitted, the unsuffixed file such as `06.svg` is the default variant. A deck that provides only variant files for a card and no unsuffixed file MUST declare `default`.

Variants of a card are interchangeable and carry the same meaning, so consumers of interpretive data, including the [Esoterica Specification](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md), discard the variant suffix. Variant keys are deck-wide, so an application MAY prefer a key across the whole deck.

## 5. Card Assets

### 5.1 Asset Discovery

Applications detect files placed in the expected directory structure and map them to cards without further configuration. An image at `h1200/minor_arcana/wands/ace.png` maps to the card with the canonical ID `minor_arcana.wands.ace`, so creating a deck can be as simple as placing files into the right directories.

A file's stem is split on the first `.`, and the first portion is called the base. Where the base names a card the deck already contains, the remainder is a [variant key](#47-card_variants) and the file is a variant of that card. Otherwise the base names a card the file defines: in `major_arcana/` a two-digit base is that [major arcanum](#31-canonical-ids) and any other base is a custom name, and in `minor_arcana/<suit>/` the base is a rank key. For example:

- `major_arcana/06.two_women.png` is a variant of The Lovers
- `major_arcana/23.png` is the deck's twenty-fourth major arcanum
- `major_arcana/the_morning.png` is a major arcanum with a custom key
- `major_arcana/the_morning.dark.png` is a variant of that card

A deck therefore adds a card by adding a file, whether the card is canonical, numbered beyond `21`, or custom-keyed. Nothing in `deck.toml` is required for any of them.

### 5.2 Vector Graphics

SVG card assets MUST be placed in the `scalable/` directory. SVG is the only vector format this specification defines and support for rendering it is OPTIONAL for an application.

### 5.3 Raster Graphics

Raster card assets are discovered only under an `h<height>/` root, where `<height>` is the height of the image in pixels; a raster image anywhere else is not a card asset and is ignored ([§5.7.1](#571-image-roots)). Which file formats discovery considers, and in what order, is fixed by the extension chain in [§5.7.4](#574-the-extension-chain). PNG with an alpha channel is RECOMMENDED for images requiring transparency.

Conventionally, `h750` serves mobile applications and thumbnails, `h1200` standard desktop and web viewing, and `h2400` high-resolution displays.

### 5.4 ANSI Art

- Files MUST be stored in an `ansi<lines>/` directory, organized by card type and suit (e.g., `ansi32/major_arcana/00.ansi`). `<lines>` is the number of terminal rows the art occupies.
- ANSI files MAY use any extension. `.ans` is conventional for art carrying escape sequences and `.txt` for plain text.
- Applications MUST determine a file's kind from its content rather than its extension. Art using ANSI escape sequences necessarily contains ESC (`0x1B`) and a file with no ESC byte is plain text and MAY be written to a terminal as-is.
- Plain text files are UTF-8.
- Where a file carries a [SAUCE](https://www.acid.org/info/sauce/sauce.htm) record, applications SHOULD honor it.

Support for ANSI art is OPTIONAL for an application.

### 5.5 Card Back Images

A `card_backs/` directory is a **card back directory** and each file in one defines a [design](#42-card_backs) whose key is the file's stem:

```
card_backs/classic.png          # "classic" with no declared size
h1200/card_backs/classic.png    # "classic" at 1200px
ansi32/card_backs/classic.ans   # "classic" at 32 rows
scalable/card_backs/classic.svg # scalable "classic"
```

A card back directory appears in two OPTIONAL locations. At the top level of the deck root, `card_backs/` holds backs of no declared kind or size. This is the simple form and for most decks the only one needed. Inside an [image root](#571-image-roots), `card_backs/` sits beside `major_arcana/` and `minor_arcana/` and its files carry that root's kind and size.

The designs a deck has are the union of the stems found across every card back directory, together with every key declared under `[card_backs.designs]` that carries an `image` path. Further rules:

- The whole stem is the design key and card backs have no notion of variants.
- The [extension chain](#574-the-extension-chain) applies.
- An explicit `image` path on `[card_backs.designs.<key>]` overrides discovery for that design in every kind and size.
- Card backs MAY have different dimensions and aspect ratios from the card fronts.

### 5.6 Aspect Ratio

- Standard assumed aspect ratio is 11:19 (~0.5789) declared by [`[deck].aspect_ratio`](#41-deck).
- Applications MUST preserve the aspect ratio when scaling images.

### 5.7 Card Image Resolution

Given a card, a rendering kind and a target size, an application resolves a file to display. This section defines that resolution.

#### 5.7.1 Image Roots

An **image root** is a top-level directory of a deck root that discovery searches for card assets. There are three forms:

| Form | Kind | Size |
| --- | --- | --- |
| `scalable/` | scalable | none |
| `h<height>/` | raster | Height in pixels |
| `ansi<lines>/` | ANSI | Lines in terminal rows |

`<height>` and `<lines>` are decimal integers greater than zero, written without a sign, leading zeroes or separators. A deck MAY contain any number of image roots of each form.

Within an image root, assets are arranged by card type and suit as shown in [§2.1](#21-directory-skeleton): `major_arcana/` and `minor_arcana/<suit>`. An image root MAY also hold a `card_backs/` directory, which supplies card back designs at that root's kind and size ([§5.5](#55-card-back-images)). Any other subdirectory is ignored.

Every other top-level directory is ignored by discovery.

#### 5.7.2 Extensions, Stems and Bases

A card asset filename is read as three parts. Given `06.two_women.png`:

| Part | Value | Rule |
| --- | --- | --- |
| extension | `png` | The part after the **last** `.` |
| stem | `06.two_women` | Everything before the last `.` |
| base | `06` | The part of the stem before the **first** `.` |
| variant key | `two_women` | The remainder of the stem after the first `.`, where there is one |

The stem is split on the first `.` and the extension taken from the last, because a variant key cannot itself contain a `.` ([§3.5](#35-grammar)). A file named `06.png` has base `06`, no variant key and extension `png`.

A file whose name contains no `.` at all has no extension. Discovery ignores it in `scalable/` and in raster roots. In an ANSI root it is a candidate: [§5.4](#54-ansi-art) allows ANSI files any extension or none.

**In a card back directory this parse does not apply.** The extension is read the same way, but everything before it is the [design key](#42-card_backs), undivided. Card backs have no variants ([§5.5](#55-card-back-images)), so a stem containing a `.` is not a design at all, and discovery ignores it.

#### 5.7.3 Size Selection Within a Kind

`scalable/` holds at most one image per card and variant, so selection there is trivial: the file is the file.

For raster and ANSI, an application selects among the roots of that kind that supply a file for the card. The rules differ, because the two media degrade in opposite directions:

- **Raster**: prefer the smallest image at or above the target height. Downscaling a raster image is well-behaved and upscaling is not.
- **ANSI**: prefer the largest art at or below the target number of lines. Art taller than the space available is truncated, which is worse than art that leaves a gap.

Candidates on the preferred side of the target therefore rank ahead of those on the other side. Within a side the nearest to the target wins, and a tie between two equidistant candidates breaks toward the preferred side. An exact match always wins. Where no candidate lies on the preferred side, an application MUST take the nearest on the other side rather than fail.

*Example.* A deck ships `h750/`, `h1200/` and `h2400/`. A raster request for target 1000 resolves to `h1200`, the smallest at or above. A request for 3000 resolves to `h2400`, the nearest below, since no candidate is at or above. A request for 975 is equidistant from 750 and 1200 and resolves to `h1200`.

#### 5.7.4 The Extension Chain

Within one directory, an application considers extensions in this fixed order:

1. `png`
2. `webp`
3. `avif`
4. `jpeg` and `jpg`, which are one entry rather than two. Where a directory holds both, the choice between them is unspecified.

In `scalable/`, the chain is `svg` alone.

- Applications MUST support decoding **PNG** and **JPEG**. Support for WebP, AVIF and SVG is OPTIONAL.
- This is a fallback chain, not a negotiation. An application MUST skip a file whose format it does not support, or whose bytes it fails to decode, and continue to the next entry in the chain.
- Extensions outside the chain are ignored by discovery entirely. A `.tiff` or a `.gif` in `h1200/major_arcana/` does not define a card and is never chosen.
- A deck SHOULD NOT ship two files with the same stem and different chain extensions in one directory. Where it does, applications MUST resolve by this order and MUST NOT resolve by filesystem order. A validator reports the duplication as a warning ([§9.4](#94-validation-rules)).
- Where every candidate in a directory is either outside the chain or in a format the application lacks, that directory does not supply the card, and the application MUST continue with the remaining candidates under [§5.7.3](#573-size-selection-within-a-kind).

A deck that wants a format outside the chain declares an explicit `image` path on the card variant ([§4.7](#47-card_variants)) or card back design ([§4.2](#42-card_backs)). Discovery is a convention and an explicit path is an instruction.

> **Note (informative).** Unlike the usual web ordering, this order favours fidelity and universal decodability over recency. A deck is already on disk, so a second encoding of the same card buys no bandwidth and is usually an authoring accident rather than progressive enhancement. The consequence is that where a PNG is present it always wins, and the optional formats matter only where they stand alone.

#### 5.7.5 Variants

A request MAY name a [variant key](#47-card_variants). Resolution then looks for files whose stem is `<base>.<key>`, and is otherwise unchanged: the same size selection, the same extension chain.

Where the requested card has no variant under that key, the application MUST resolve that card's **default** variant instead, and MUST NOT treat the absence as an error. Variant keys are deck-wide and a card need not carry every key the deck uses. This is the asset-resolution statement of the rule in [§4.7](#47-card_variants).

A request naming no variant key resolves the card's default variant: the unsuffixed file, or the variant named by `[card_variants."<id>"].default` where one is declared.

#### 5.7.6 When No Asset Is Found

Where resolution yields no file for a card in any image root of any kind:

- Where the library designates a [reference deck](#13-terminology) and the card is not deliberately absent under [`[excluded_cards]`](#45-excluded_cards), the application SHOULD resolve the same card against that deck. This step applies only to a card with a **canonical counterpart**, meaning a canonical minor arcanum or a major arcanum keyed `00` through `21`. A card the reference deck could only coincidentally share, meaning an [extended major arcanum](#13-terminology) or any custom-keyed card, MUST NOT be resolved against it: two decks that each define `major_arcana.23` have not agreed on a card ([§3.1.1](#311-a-canonical-id-is-a-slot)), and borrowing the image would show the user a card the deck does not contain.
- Otherwise, this is a **resolution failure**, not a validation error. The application decides what to show, whether a placeholder, a card back or nothing. A deck is not non-conforming for lacking an asset for some card, and [§9](#9-conformance-and-validation) does not make it so.

#### 5.7.7 Resolving a Card Back

An application resolves a back the same way, with three differences:

1. The subpath is `card_backs/` rather than `major_arcana/` or `minor_arcana/<suit>/` and the stem is the design key.
2. Where no image root of the requested kind supplies the design, the top-level `card_backs/` directory is consulted last as a root of no size. Because it declares no kind either, an application that finds nothing there under the chain for the kind it asked for MAY take any file in it whose stem is the design key and whose format it can decode.
3. There is no reference-deck and applications supply their own back.

#### 5.7.8 Resolution Summary

Given a card, a variant key a kind and a target size, an application:

1. Forms the stem from the card's base, plus `.<variant-key>` where one is requested, and the subpath `major_arcana/` or `minor_arcana/<suit>/`.
2. Ranks the image roots of the requested kind by [§5.7.3](#573-size-selection-within-a-kind) and, best first, looks in `<root>/<subpath>` for that stem under the [extension chain](#574-the-extension-chain), taking the first file it can decode. Walking past a root it cannot decode costs it a fallback rather than the card.
3. Failing that, and where a variant was requested, repeats step 2 for the card's default variant ([§5.7.5](#575-variants)).
4. Failing that, resolves the card against the [reference deck](#13-terminology) where the library has one, the card is not excluded, and the card has a canonical counterpart ([§5.7.6](#576-when-no-asset-is-found)). This step sits outside the per-deck lookup, so a reference deck is consulted once the deck itself is exhausted and never in the middle of size selection.

Card backs follow the same shape with the differences [§5.7.7](#577-resolving-a-card-back) gives. An explicit `image` path wins outright, the subpath is `card_backs/` and the stem is the design key, the top-level `card_backs/` is consulted last, and there is no reference-deck step.

ANSI files are exempt from the extension chain: [§5.4](#54-ansi-art) allows them any extension, so in an ANSI root a lookup matches on stem alone and determines the file's kind from its content. An application MUST apply [§10.2](#102-terminal-escape-injection) to any ANSI file it writes to a terminal.

## 6. Internationalization

Display strings such as card, suit and rank names and alt text are declared in `names/<tag>.toml`.

### 6.1 Language Tags

`<tag>` MUST be a well-formed IETF BCP 47 language tag.

- Tags SHOULD be canonical, using the shortest available ISO 639 subtag (`en`, not `eng`), lowercase language, titlecase script and uppercase region.
- Applications MUST compare tags case-insensitively. A deck MUST NOT ship two name files whose tags differ only in case.
- `[deck].default_language` declares the tag of the deck's default name file. Where absent, applications assume `en`.

### 6.2 Language Resolution

Given a requested tag, applications resolve it using the Lookup scheme of RFC 4647, trying the requested tag, then progressively shorter forms of it, then the deck's `default_language`. A request for `pt-BR` therefore reads `names/pt-BR.toml`, then `names/pt.toml`, then the default language file. A key that no name file supplies falls through to the further fallbacks in [§6.3](#63-display-name-resolution).

```toml
[metadata]                          # Optional, see §7.3
source = "Names and alt text written by Jane Doe."
license = "CC-BY-4.0"

[major_arcana]
00 = "The Fool"
01 = "The Magician"

[minor_arcana]
name_template = "{rank} of {suit}"  # Optional, see §6.3.1

[minor_arcana.wands]
ace = "Ace of Wands"                # Optional, overrides the template

[suits]
wands = "Wands"
stars = "Stars"                     # Custom suit

[ranks]
page = "Page"
knight = "Warrior"                  # Renamed rank

[alt_text.major_arcana]
00 = "A young person in colorful clothes steps off a cliff, carrying a white rose. A small dog jumps at their heels."

[alt_text.minor_arcana.wands]
ace = "A hand emerging from a cloud holds a flowering wooden staff."

[card_backs]                        # Card back design names
classic = "Classic Back"

[alt_text.card_backs]
classic = "A blue and white geometric pattern featuring roses and lilies."

[card_variants]                     # Keyed by variant reference
"major_arcana.06:two_women" = "The Lovers"

[alt_text.card_variants]
"major_arcana.06:two_women" = "Two women stand hand in hand beneath a winged figure."
```

Name files are sparse and MAY contain a subset of keys. Applications MUST merge name files key by key rather than requiring a complete set, and MUST NOT treat a missing key as an error.

#### 6.2.1 Name File Metadata

The `[metadata]` table is OPTIONAL and describes the name file itself rather than any card in it.

| Key | Purpose |
| --- | --- |
| `source` | Who or what produced the strings in this file |
| `license` | SPDX license expression governing the strings in this file |
| `license_files` | Paths, relative to the deck root, to the full license text and any notices |
| `copyright` | The copyright notice, verbatim as the rights holder wrote it |
| `attribution` | The credit line the license requires downstream users to display |

The OPTIONAL `[metadata.alt_text]` subtable takes the same keys and overrides them for alt text alone. See [Name File Licensing](#73-name-file-licensing).

### 6.3 Display Name Resolution

Each chain below is applied to name files in the order given by [Language Resolution](#62-language-resolution).

A resolved display string is used verbatim. Applications MUST NOT apply case conversion or any other transformation to a string a deck supplies. Case transformation appears in this specification only as a fallback for keys the deck does not define a string for.

| Value | Resolution chain |
| --- | --- |
| Suit name | `[suits].<key>` in the name file, then `[suits.<key>].name` in `deck.toml`, then the title-cased key |
| Rank name | `[ranks].<key>`, then the title-cased key |
| Major arcana name | `[major_arcana].<key>`, then `[cards."major_arcana.<key>"].name`, then, **for a key `00` through `21` only**, the [reference deck](#13-terminology)'s name for that ID and then [Appendix C](#appendix-c-canonical-card-names-informative) where no reference deck is configured. See below for a key that reaches the end. |
| Minor arcana name | `[minor_arcana.<suit>].<rank>`, then `[cards."minor_arcana.<suit>.<rank>"].name`, then [composition](#631-minor-arcana-name-composition) from the card's suit and rank names |
| Card back design name | `[card_backs].<key>`, then `[card_backs.designs.<key>].name`, then the [title-cased key](#13-terminology) |
| Card variant name | `[card_variants]."<variant-ref>"`, then `[card_variants."<canonical-id>".variants.<key>].name`, then the name of the card itself |
| Alt text | `[alt_text.*]`, then the `alt_text` field of the corresponding `[cards]`, `[card_backs.designs]` or variant entry |
| Card variant alt text | `[alt_text.card_variants]."<variant-ref>"`, then the variant's `alt_text` field, then the card's own alt text |

A major arcana key that reaches the end of its chain has **no name**. Where that key is custom, an application uses the title-cased key, which for a key an author chose is usually a serviceable name. Where it is an [extended major arcanum](#13-terminology) the title-cased key is the bare digits, which names nothing, so an application SHOULD instead present the card by its [number](#431-card-numbers). The reference deck and [Appendix C](#appendix-c-canonical-card-names-informative) are both absent from this chain above `21` for the reason [§3.1.1](#311-a-canonical-id-is-a-slot) gives: no deck's twenty-third major arcanum names another's. A deck that has extended major arcana SHOULD name them in a name file, and a validator says so ([§9.4](#94-validation-rules)).

#### 6.3.1 Minor Arcana Name Composition

Because a deck MAY rename its suits and ranks, most decks need not write out all 56 minor arcana names. Where a name file gives no explicit name for a minor arcana card, its name is composed from a template:

```toml
[minor_arcana]
name_template = "{rank} of {suit}"
```

`{rank}` and `{suit}` are replaced by the rank and suit names resolved above. No other placeholders are defined, and an application MUST leave any other braced text in the template alone. The template is resolved by the same [Language Resolution](#62-language-resolution) rules as any other key, so a translation supplies its own. Where no name file supplies one, the template is `"{rank} of {suit}"`.

Where a deck supplies no value of the minor arcana at any level, applications MAY fall back to the corresponding string from the [reference deck](#13-terminology).

### 6.4 Alt Text Guidelines

- Alt text SHOULD describe the visual elements of the card without interpretation.
- A deck SHOULD include at least one language file carrying alt text.
- Every card variant SHOULD carry its own alt text.
- Alt text given in `[cards]`, `[card_variants]` or `[card_backs.designs]` is a fallback only, and a name file always prevails.

## 7. Licensing and Attribution

A deck is comprised of several components that can have separate licensing terms.

- The license specified by `[deck].license` describes the artwork.
- The license in the `[metadata].license` field of a name file covers the strings in that file and `[metadata.alt_text]` narrows that to the alt text alone.
- A `LICENSE` file at the root of the deck conveys terms for whoever assembled the deck.

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

Decks SHOULD ship the full license text in the deck directory.

### 7.3 Name File Licensing

The strings in a name file are not necessarily the deck assembler's own work, since alt text might be written by a contributor or adapted from a published source. Each name file therefore states its own terms in its [`[metadata]`](#621-name-file-metadata) table, using the same fields as `[deck]` and with the same meanings.

Most decks need only to license their alt text, which `[metadata.alt_text]` does on its own. Where the whole file is a single person's work, as with a translation, `[metadata]` covers the entire file including its alt text. Where the two differ, `[metadata]` gives the file's terms and `[metadata.alt_text]` overrides them for alt text alone.

```toml
# names/pt-BR.toml
[metadata]
source = "Translated by Paulo Freire."
license = "CC-BY-4.0"
license_files = ["names/LICENSE.pt-BR"]
attribution = "Portuguese translation by Paulo Freire."

[metadata.alt_text]
source = "Descriptions contributed by Jane Doe."
license = "CC0-1.0"
```

## 8. Extensibility

The `[app]` table is reserved for applications to record data about a deck that this specification does not model. Each application takes a subtable keyed by a [realm](#33-qualified-identifiers):

```toml
[app."land.arcana.tarotcanvas"]
bleed = true # artwork runs to the edge

[app."land.arcana.cartomancer"]
ansi_color_depth = "truecolor"  # ANSI art uses 24-bit SGR
ansi_glyphs = "sextants"        # needs a font covering U+1FB00–U+1FBFF
```

The subtable key MUST be written as a quoted TOML key because a realm always contains a '.' character.

Applications MUST ignore any `[app]` subtable they do not own, and validators MUST NOT report unknown keys within `[app]`.

Top-level table names outside `[app]` are reserved for future versions of this specification.

## 9. Conformance and Validation

### 9.1 Conforming Deck

A conforming deck:

- MUST contain a readable `deck.toml` well-formed under [§2.3](#23-file-format-and-encoding).
- MUST contain a `[deck]` table carrying the required fields from [§4.1](#41-deck).
- MUST have at least one card asset, discoverable under [§5.1](#51-asset-discovery).
- MUST produce no errors under [§9.4](#94-validation-rules).

### 9.2 Errors and Warnings

A validator reports two kinds of violations. An **error** makes a deck non-conforming and an application MAY refuse it. A **warning** marks something an author probably did not intend, or a condition this specification allows but has an opinion about. An application MUST load a deck that produces only warnings.

### 9.3 Conforming Applications and Validators

A conforming application:

- MUST implement deck discovery ([§2.2](#22-the-deck-library), [§5.1](#51-asset-discovery)), display name resolution ([§6.3](#63-display-name-resolution)) and card image resolution ([§5.7](#57-card-image-resolution)).
- MUST support decoding PNG and JPEG ([§5.7.4](#574-the-extension-chain)).
- MUST ignore `[app]` subtables it does not own ([§8](#8-extensibility)), and every table, key and value this specification does not define.
- MUST NOT reject a deck for warnings ([§9.2](#92-errors-and-warnings)).

An application need not implement editions, card variants, ANSI art, SVG or localization beyond the deck's default language. Where it does not, it uses the defaults those sections define. A conforming validator implements the rules in [§9.4](#94-validation-rules).

### 9.4 Validation Rules

Each rule is labelled **E** for error or **W** for warning.

| | Rule |
| --- | --- |
| **E** | `deck.toml` exists and is valid TOML 1.0.0, and every image, license file and name file it references exists. |
| **E** | `[deck]` carries `schema_version`, `name` and `version` ([§4.1](#41-deck)). |
| **E** | Every key in a name file corresponds to a card, suit, rank, card variant or card back design the deck defines, or is `[minor_arcana].name_template`, or appears in the reserved `[metadata]` table or its `alt_text` subtable. |
| **E** | `[minor_arcana].name_template`, where present, contains no placeholder other than `{rank}` and `{suit}`. |
| **E** | Every name file's stem is a well-formed BCP 47 language tag, no two differ only in case, and `[deck].default_language` has a corresponding file. |
| **W** | Alt text is provided for all cards in at least one name file. |
| **E** | `[card_backs].default`, where present, names a card back design the deck has, whether discovered from a [card back directory](#55-card-back-images) or declared with an `image` path. |
| **E** | Every design key, whether a discovered stem or a `[card_backs.designs]` table key, is a well-formed [custom name](#32-custom-names), and every `image` path declared under `[card_backs.designs]` exists. |
| **W** | Where the deck has more than one card back design and neither `[card_backs].default` nor a design keyed `default` is present, the default rests on collation order ([§4.2](#42-card_backs)). Resolution is well defined, but the author probably did not choose it. |
| **W** | A file in a card back directory that discovery ignores, meaning a stem containing a `.`, a stem that is not a custom name, or an extension outside the chain with no `image` path pointing at it. Such a file is usually an intended back that will never be shown. |
| **E** | Every custom name matches the `custom-name` grammar of [§3.5](#35-grammar) and is not a reserved canonical key, excepting a canonical suit used as a `[suits]` table key. |
| **E** | `[deck].identifier`, where present, is a well-formed qualified identifier. |
| **E** | Every `[app]` subtable key is a well-formed realm, in particular one with two labels or more, which is what distinguishes `[app."land.arcana"]` from an unquoted `[app.land.arcana]` ([§8](#8-extensibility)). The contents of such a subtable are the owning application's to define and are not validated. |
| **W** | `[deck].identifier` is present. It is RECOMMENDED, and a deck without one cannot be referenced from another Arcana Land document ([§3.4](#34-deck-identity)). |
| **W** | Where a validator can see a whole library, no two visible decks declare the same `[deck].identifier`. Two decks that do are a legitimate arrangement, such as a fork or two versions installed side by side, so this is only a warning. |
| **E** | Every card referenced in `[card_variants]` is a card the deck defines, and every referenced variant image file exists. |
| **E** | Where a variant table declares `default`, the named variant exists. |
| **E** | Where a card has variant files but no unsuffixed file, `[card_variants]."<canonical-id>".default` is declared ([§4.7](#47-card_variants)). A card with no files at all is a [resolution failure](#576-when-no-asset-is-found), not a violation of this rule. |
| **E** | Every `[cards]` table key is a well-formed [canonical ID](#31-canonical-ids), in particular a two-digit major arcana key written with both digits. A [variant reference](#312-card-references-and-the-variant-suffix) is not a valid key here. |
| **E** | Every card declared in `[cards]` is a card the deck has files for, since `[cards]` does not define cards on its own. A canonical minor arcanum and a major arcanum keyed `00` through `21` are exempt, because those slots exist for every deck whether or not it ships the asset ([§4.3](#43-cards)). |
| **E** | `number`, where present, is a non-empty string. A card is made unnumbered by the shape of its key, not by an empty `number` ([§4.3.1](#431-card-numbers)). |
| **W** | A `position` declared on a minor arcanum, which an application ignores ([§4.3](#43-cards)). |
| **W** | Every [extended major arcanum](#13-terminology) the deck has is named in at least one name file. Nothing else can name it ([§6.3](#63-display-name-resolution)), so one that is not will be shown to the user as a bare number. |
| **E** | No custom major arcana key is a two-digit string and no custom rank or suit key shadows a canonical one, so that a custom ID can never collide with a canonical one. |
| **E** | Every rank named in a `ranks` list has files in that suit, and no `ranks` list contains duplicates. |
| **E** | No card is both excluded by `[excluded_cards]` and declared in `[cards]`. |
| **W** | No card listed in `[excluded_cards]` has an image file. An exclusion is a statement of intent ([§4.5](#45-excluded_cards)); a deck that ships the asset anyway has probably changed its mind and not updated the list. |
| **W** | A `position` **declared** by two cards. Ordering remains well defined ([§4.3.2](#432-ordering)). A declared `position` that coincides with an implicit one is not reported, since seating a card against a numbered neighbour is the field's purpose. |
| **E** | Where more than one edition is defined, `[editions].default` is present and names a defined edition, and every `[editions].<key>.card_back` names a card back design the deck has. |
| **E** | No path field, meaning `icon`, `image` or any `license_files` entry, begins with `/`, contains a `..` segment or resolves outside the deck root ([§2.3](#23-file-format-and-encoding), [§10.1](#101-path-traversal)). |
| **E** | No directory holds two files whose stems differ only in case ([§2.3](#23-file-format-and-encoding)). |
| **E** | Every file listed in a `license_files` list exists, in `[deck]` and in every name file's `[metadata]` alike, and `[metadata.alt_text]` contains no key that is not defined for `[metadata]`. |
| **W** | Two files in one directory sharing a stem and differing only in a chain extension, such as `06.png` beside `06.webp`. Resolution is well defined ([§5.7.4](#574-the-extension-chain)), but one of the two is usually a conversion left behind. |
| **W** | A card asset whose own aspect ratio differs from `[deck].aspect_ratio` by more than 10%, measured as `\|actual - declared\| / declared` ([§4.1](#41-deck)). Card backs are exempt, since `[deck].aspect_ratio` describes the fronts, and so is ANSI art, whose extent is counted in character cells rather than pixels and is not comparable to a ratio of lengths. |
| **W** | A `license` field that is not a well-formed SPDX license expression. A deck that fails this check MUST NOT be rejected ([§7](#7-licensing-and-attribution)). |

## 10. Security Considerations

A deck arrives from outside the system and carries data an author can abuse. This section describes the security concerns that can arise.

### 10.1 Path Traversal

Author-supplied paths such as `icon`, `image` and `license_files` can be vectors of abuse. An application MUST reject a path beginning with `/` or otherwise absolute on the host platform, a path containing a `..` segment, and a path that resolves to a location outside the deck root. An application MUST NOT follow a symbolic link that leads outside the deck root.

### 10.2 Terminal Escape Injection

ANSI art is a sequence of bytes an application writes to a terminal, and a hostile deck can carry OSC 52 sequences that clobber the user's clipboard, or sequences that induce the terminal to write attacker-chosen bytes to the application's standard input. An application that renders ANSI art MUST therefore restrict what it passes through. Displaying ANSI safely is the application's responsibility.


## Appendix A. Examples (Informative)

### A.1 Simple Custom Deck

Creating a deck needs only a minimal `deck.toml` with the card images placed in the expected directories. Applications detect the images and map them to canonical IDs without further configuration.

```
my-custom-deck/
  deck.toml
  card_backs/
    main.png
  h1200/
    major_arcana/
      00.png          # The Fool, through 21.png, The World
    minor_arcana/
      cups/
        ace.png       # through king.png
      wands/
        ace.png
  names/
    en.toml           # Card names and alt text
```

And a small `deck.toml`:

```toml
[deck]
name = "My Custom Deck"
version = "1.0"
schema_version = "2.0"
```

### A.2 Rider-Waite-Smith

A published deck, with full metadata, licensing and a declared card back.

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
attribution = "Original artwork by Pamela Colman Smith (1909)."

default_language = "en"
created_date = "1909-12-01"
updated_date = "2025-04-28"
website = "https://en.wikipedia.org/wiki/Rider%E2%80%93Waite_Tarot"
tags = ["traditional", "classic", "beginner-friendly"]

[card_backs]
default = "classic"

[card_backs.designs.classic]
name = "Classic RWS Back"
description = "The 1909 Rider back, digitally restored from the original printing."
```

And `names/en.toml`:

```toml
[metadata.alt_text]
source = "Written by Jane Doe."
license = "CC-BY-4.0"
attribution = "Card descriptions by Jane Doe, licensed under CC BY 4.0."

[alt_text.major_arcana]
00 = "A young person in colorful clothes steps off a cliff."

[alt_text.card_backs]
classic = "A lattice of blue and white roses and lilies."
```

### A.3 Renamed Suits, a Custom Card and Multiple Editions

```toml
# deck.toml
[deck]
name = "Elemental Torches Tarot"
version = "1.0"
schema_version = "2.0"
description = "A fire-themed tarot deck with renamed suits and an additional elemental card."

[cards."major_arcana.elemental_force"]
name = "The Elemental Force"
position = 22

[card_backs]
default = "flames"

[card_backs.designs.embers]
name = "Glowing Embers"
description = "Drawn for the deluxe printing, on darker stock."

[editions]
default = "standard"

[editions.standard]
name = "Elemental Torches (Standard Edition)"
card_back = "flames"

[editions.deluxe]
name = "Elemental Torches (Deluxe Edition)"
card_back = "embers"
```

And `names/en.toml`:

```toml
[major_arcana]
00 = "The Wanderer"   # This deck's name for The Fool

[suits]
wands = "Torches"
cups = "Waters"
swords = "Winds"
pentacles = "Stones"

[ranks]
page = "Student"
knight = "Warrior"

[alt_text.major_arcana]
00 = "A traveler with a backpack walks toward a fiery mountain."
elemental_force = "A vortex of the elements swirling together in harmony."

[alt_text.card_backs]
flames = "A dynamic pattern of red and orange flames swirling around a central spark."
```

### A.4 A Lowercase Typographic Convention

A deck that prints every minor arcana in lower case writes its suit and rank names that way and lets composition do the rest. Cards that break the deck's own pattern are written out individually and take precedence over the template.

```toml
# names/en.toml
[minor_arcana]
name_template = "{rank} of {suit}"

[suits]
wands = "torches"
cups = "cups"

[ranks]
ace = "ace"
page = "princess"
knight = "prince"

[minor_arcana.pentacles]
ace = "one of pentacles"
# other suits are still "ace"

[major_arcana]
00 = "the Fool"
21 = "The world"
```

### A.5 Deck with Card Variants

Some decks provide several artworks for the same canonical ID. The variants are discovered through the directory structure, so only the alt text has to be written.

```
inclusive-tarot/
  deck.toml
  h1200/
    major_arcana/
      06.png                  # The Lovers, default artwork
      06.two_women.png
      06.two_men.png
    minor_arcana/
      cups/
        two.png
  names/
    en.toml
```

And `names/en.toml`:

```toml
[alt_text.major_arcana]
06 = "A man and a woman stand hand in hand beneath a winged figure."

[alt_text.card_variants]
"major_arcana.06:two_women" = "Two women stand hand in hand beneath a winged figure."
"major_arcana.06:two_men" = "Two men stand hand in hand beneath a winged figure."
```

## Appendix B. Reserved and Deprecated Names

The names below were defined by an earlier version of this specification and are no longer defined by this one. A future version of this specification MUST NOT reuse any of them with a new meaning.

Applications MUST ignore these names in a 2.0 deck.

| Name | Was | Status |
| --- | --- | --- |
| `[deck].id` | The deck's identifier in 1.0. It was both the library handle and the global identity and was inadequate as either | Removed in 2.0. The handle is the directory name and the global identity is [`[deck].identifier`](#34-deck-identity).|
| `[aliases]` | Suit and court display names in 1.0 | Removed in 2.0. Superseded by [name files](#6-internationalization) |
| `[variants]` | Deck editions in 1.0 | Renamed to [`[editions]`](#46-editions) in 2.0. The word "variant" now means a [card variant](#47-card_variants)|
| `[card_backs.variants]` | Card back designs in 1.0 | Renamed to [`[card_backs.designs]`](#42-card_backs) in 2.0, so that "variant" has one meaning.|
| `[deck.excluded_cards]` | Excluded cards, nested under `[deck]` in 1.0 | Moved to top-level [`[excluded_cards]`](#45-excluded_cards) in 2.0 |
| `[deck.companions]` | Never specified. Present in early implementations as a list of related documents, each with `id`, `name` and `uri` | Not defined by any version. Superseded by [qualified identifiers](#33-qualified-identifiers), by which another Arcana Land document names a deck rather than the deck naming it |
| `[custom_cards]` | Custom major arcana, suits and ranks in 1.0 | Split in 2.0. Per-card metadata for every card, canonical or custom, moved to [`[cards]`](#43-cards), keyed by canonical ID; suit structure moved to [`[suits]`](#44-suits). A card is no longer "custom" for the purpose of describing it |
| `image` on `[custom_cards.major_arcana.<key>]` | An explicit path to a custom card's image in 1.0 | Removed in 2.0. A card's images come from [discovery](#51-asset-discovery), like every other card's, which is what lets one card exist in several sizes and formats |
| `id` on `[custom_cards.major_arcana.<key>]` | A custom card's identifier in 1.0 | Removed in 2.0. The table key is the card's canonical ID |
| `[remap_major_arcana]` | A table remapping major arcana display positions in 1.0 | Removed in 2.0. No published deck used it and it was unnecessary |

## Appendix C. Canonical Card Names (Informative)

This appendix publishes conventional English names for the twenty-two canonical major arcana as the last fallback of display name resolution ([§6.3](#63-display-name-resolution)). Nothing in this specification treats a deck as wrong for disagreeing with this table.

The table stops at `21` and no future version of this specification will extend it. A major arcanum keyed `22` or above belongs to the deck that defines it and no convention names it ([§3.1.1](#311-a-canonical-id-is-a-slot)).

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

Suit and rank names can be derived from their keys by the [title-cased key](#13-terminology) rule.

Recall that a [canonical ID is a slot](#311-a-canonical-id-is-a-slot), so a deck following the Marseille ordering of Justice and Strength can denote this by swapping the appropriate strings in its name file.

## Appendix D. Changelog

### Version 2.0

An application MAY support 1.0 decks alongside 2.0 ones. Where it does, it reads them under 1.0's rules.

**Breaking changes.** Every name removed or renamed is listed in [Appendix B](#appendix-b-reserved-and-deprecated-names). Version 2.0 removes `[aliases]`, `[remap_major_arcana]`, `[deck].id`, `[editions].<key>.id` and the `image` and `id` fields of a custom major arcanum, renames `[variants]` to `[editions]` and `[card_backs.variants]` to `[card_backs.designs]`, splits `[custom_cards]` into [`[cards]`](#43-cards) and [`[suits]`](#44-suits), moves `[deck.excluded_cards]` to a top-level `[excluded_cards]`, and keys `[app]` subtables by a realm rather than a bare custom name.

**Newly specified.**

- [The deck library](#22-the-deck-library), covering XDG discovery.
- [Card image resolution](#57-card-image-resolution), covering image roots and size selection.
- [Card back discovery](#55-card-back-images), so that a back can exist at several resolutions or as ANSI.
- [File format and encoding](#23-file-format-and-encoding).
- [Security considerations](#10-security-considerations), covering path traversal and ANSI escape codes.
- [Appendix C](#appendix-c-canonical-card-names-informative) for fallback name-resolution chains.

**Other changes.** Restructured the document as a specification, adopting BCP 14 keywords explicitly, replacing the regex identifier forms with one consolidated [ABNF grammar](#35-grammar) and lifting fields out of TOML comments into [normative field tables](#4-decktoml-reference). Added [qualified identifiers](#33-qualified-identifiers) and formalized custom names and display name resolution. Made every card discoverable from the directory structure, added [card variants](#47-card_variants), allowed custom `ranks` for canonical suits and added `name_template` composition. Specified name file language tags as BCP 47, added `default_language`. Specified `license` as SPDX, added `license_files` and `copyright`, and added the `[metadata]` table to name files. Required an ANSI file's kind to be detected from its content and recommended honoring a SAUCE record. Defined what `[app]` is for and reserved top-level table names outside it.
