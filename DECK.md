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
  - [1.6 Licensing of This Specification (Informative)](#16-licensing-of-this-specification-informative)
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
    - [4.1.1 Links](#411-links)
    - [4.1.2 `signifies`](#412-signifies)
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
  - [5.8 Surrogate Assets](#58-surrogate-assets)
    - [5.8.1 The Surrogate File](#581-the-surrogate-file)
  - [5.9 Surrogate Decks](#59-surrogate-decks)
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
  - [7.4 Rights Status](#74-rights-status)
  - [7.5 Redistribution and Derivation](#75-redistribution-and-derivation)
  - [7.6 Naming the Packager](#76-naming-the-packager)
  - [7.7 Deck Names and Trademarks](#77-deck-names-and-trademarks)
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
  - [A.6 A Surrogate Deck](#a6-a-surrogate-deck)
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

This specification addresses three kinds of actors: **packagers** who craft a `deck.toml` and arrange files around it, applications that read a deck in order to present it to a user, and validation tools that check a deck against this specification.

A packager is whoever assembles the package. They may be the artist who made the artwork, the publisher who holds the rights to it, or a third party with neither, such as a collector or a distribution maintainer. This specification requires no particular relationship between them and the artwork, and several fields exist precisely because the packager is often not the rights holder ([§7](#7-licensing-and-attribution)). Where this document says a deck "declares" or "says" something, the packager is who said it.

### 1.3 Terminology

| Term | Meaning |
| --- | --- |
| **deck** | A directory containing a `deck.toml`, together with the card assets and name files arranged around it. |
| **deck root** | The directory that directly contains a deck's `deck.toml`. Every path in `deck.toml` is relative to it. |
| **directory name** | The name of the deck root's own directory: the deck's handle within a library ([§3.4](#34-deck-identity)). |
| **deck library** | An ordered list of **library roots**, each a directory whose immediate children are candidate deck roots ([§2.2](#22-the-deck-library)). |
| **reference deck** | A deck a library designates as the source of last resort for a display string or an asset another deck does not supply. A library MAY designate one. It is not a property of any deck. Where none is configured, [Appendix C](#appendix-c-canonical-card-names-informative) supplies the canonical major arcana names. |
| **card** | One addressable image in a deck, named by a canonical ID. |
| **packager** | Whoever assembled a deck package. Not necessarily the artist and not necessarily the rights holder ([§1.2](#12-document-conventions)). |
| **surrogate** | A derived, deliberately lossy stand-in for a card's artwork, such as a color palette or a [thumbhash](https://evanw.github.io/thumbhash/). A surrogate is a card asset of its own kind, carried in the `surrogate/` [image root](#571-image-roots) ([§5.8](#58-surrogate-assets)). |
| **surrogate deck** | A deck that carries surrogates and no other card assets, so that it can describe artwork it does not redistribute. It [signifies](#41-deck) the deck whose artwork that is ([§5.9](#59-surrogate-decks)). |
| **major arcana** | The cards keyed under `major_arcana`. The twenty-two keyed `00`–`21` are the canonical major arcana. |
| **extended major arcanum** | A major arcanum keyed beyond the canonical numbers into `22`–`99` |
| **minor arcana** | The suited cards, canonically fifty-six, keyed by **suit** and **rank** under `minor_arcana`. The canonical suits are `wands`, `cups`, `swords` and `pentacles`. The canonical ranks are `ace` through `ten`, then `page`, `knight`, `queen` and `king`. A deck MAY define others. |
| **card type** | Which of the two arcana a card belongs to: `major_arcana` or `minor_arcana`. Distinct from **kind** ([§5.7.1](#571-image-roots)), which distinguishes scalable, raster, ANSI and surrogate assets. |
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
| **RightsStatements.org** | [Standardized international rights statements](https://rightsstatements.org/) | [§7.4](#74-rights-status) |
| **CSS Color 4** | [Named colors](https://www.w3.org/TR/css-color-4/#named-colors) | [§5.8.1](#581-the-surrogate-file) |
| **ThumbHash** (informative) | [evanw.github.io/thumbhash](https://evanw.github.io/thumbhash/) | [§5.8.1](#581-the-surrogate-file) |
| **XDG Base Directory Specification** | [specifications.freedesktop.org](https://specifications.freedesktop.org/basedir-spec/latest/) | [§2.2](#22-the-deck-library) |
| **SAUCE** (informative) | [Standard Architecture for Universal Comment Extensions](https://www.acid.org/info/sauce/sauce.htm) | [§5.4](#54-ansi-art) |
| **Esoterica Specification** (informative) | [ESOTERICA.md](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md) | [§1.1](#11-scope-and-design-goals), [§4.7](#47-card_variants) |
| **Spread Specification** (informative, proposed) | [SPREAD.md](https://github.com/arcanaland/specifications/blob/main/SPREAD.md) | [§1.1](#11-scope-and-design-goals) |

### 1.6 Licensing of This Specification (Informative)

This section describes the terms of the specification itself. It is not about the licensing of any deck, which [§7](#7-licensing-and-attribution) covers.

The text of this document is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Its machine-facing parts are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) and the author asserts no copyright, database right, patent or trademark over them against anyone:

- the canonical identifiers and the system that mints them ([§3](#3-identity-and-identifiers));
- the ABNF grammar ([§3.5](#35-grammar));
- the names, types, defaults and enumerated values of every file, directory, table and key this document defines ([§4](#4-decktoml-reference)), together with every registry of values it publishes, such as the link relations of [§4.1.1](#411-links) and the `redistribution` and `derivation` vocabularies of [§7.5](#75-redistribution-and-derivation);
- the canonical card names of [Appendix C](#appendix-c-canonical-card-names-informative) and the reserved names of [Appendix B](#appendix-b-reserved-and-deprecated-names);
- every example in this document.

No permission, notice, registration or fee is required to implement this specification, to catalog decks against its identifiers, to cross-reference or map them to another scheme, or to build a competing specification on top of them, for any purpose, commercial or otherwise. The author irrevocably undertakes never to assert any such right against anyone who does.

Appendix C is called out above because it is the one table an implementation is most likely to embed verbatim: it is the last fallback of display name resolution ([§6.3](#63-display-name-resolution)), so an application that resolves a name at all carries a copy of it. Its contents are conventional names of long standing that this specification does not claim to have authored, and nothing about reproducing them is conditioned on anything.

See [LICENSING.md](https://github.com/arcanaland/specifications/blob/main/LICENSING.md) for the operative terms, which govern where this section and they disagree.

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
  surrogate/               # Surrogates: lossy stand-ins for the artwork (optional)
    major_arcana/
      00.toml
    minor_arcana/
      cups/
        ace.toml
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

`deck.toml`, every `names/<tag>.toml` file and every [surrogate file](#581-the-surrogate-file) MUST be well-formed [TOML 1.0.0](https://toml.io/en/v1.0.0) encoded as UTF-8. Applications MAY skip a leading byte-order mark and a deck SHOULD NOT write one.

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
| `signifies` | String | No | none | The [qualified identifier](#33-qualified-identifiers) of another deck, whose artwork this package describes but does not carry ([§4.1.2](#412-signifies)). |
| `default_language` | String | No | `"en"` | BCP 47 tag of the deck's default name file ([§6.2](#62-language-resolution)). |
| `icon` | String (path) | No | none | A preview image for the deck, assumed to share the cards' aspect ratio. |
| `aspect_ratio` | Float | No | `0.5789` | Width ÷ height of the deck's cards. |
| `author` | String | No | none | The artwork's author. |
| `packager` | String | No | none | Whoever assembled this package, where that is not the author ([§7.6](#76-naming-the-packager)). |
| `description` | String | No | none | A prose description of the deck written once in `default_language` ([§6.4](#64-alt-text-guidelines)). |
| `license` | String | No | none | SPDX license expression governing the card assets this package carries ([§7.1](#71-license-expressions)). |
| `license_files` | Array of String (path) | No | `[]` | Full license texts and notices carried in the deck ([§7.2](#72-attribution-and-notices)). |
| `copyright` | String | No | none | Copyright notice, displayed verbatim. |
| `attribution` | String | No | none | Credit line to display ([§7.2](#72-attribution-and-notices)). |
| `rights_status` | String (URI) | No | none | The artwork's copyright *status*, as distinct from any license granted over it ([§7.4](#74-rights-status)). |
| `redistribution` | String | No | `"unstated"` | Whether the packager passes on the artwork for republication ([§7.5](#75-redistribution-and-derivation)). |
| `derivation` | String | No | `"unstated"` | Whether the packager passes on the artwork for making derived works ([§7.5](#75-redistribution-and-derivation)). |
| `created_date` | String | No | none | RFC 3339 `full-date` (`YYYY-MM-DD`), as described below. |
| `updated_date` | String | No | none | RFC 3339 `full-date` (`YYYY-MM-DD`), as described below. |
| `publisher` | String | No | none | The deck's publisher. |
| `links` | Array of Table | No | `[]` | The deck's web addresses, each saying what it points at ([§4.1.1](#411-links)). |
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

#### 4.1.1 Links

`[deck].links` holds the deck's web addresses. A deck MAY declare any number, including several sharing a `rel`. Each entry is a table:

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `rel` | String | **Yes** | n/a | What the target is, from the registry below. MUST be a [custom name](#32-custom-names). |
| `url` | String (URI) | **Yes** | n/a | An absolute URL with a scheme of `http` or `https`. |
| `title` | String | No | none | A label for the link, in the deck's `default_language`. |

The registry:

| `rel` | The target is |
| --- | --- |
| `homepage` | The deck's own page, wherever its author considers it to live |
| `buy` | Somewhere a reader can obtain the physical or digital deck |
| `artist` | The artist, illustrator or creator of the artwork |
| `publisher` | The publisher named in `[deck].publisher` |
| `source` | Where the deck's assets were obtained, such as an archive or a scan repository |
| `documentation` | A companion booklet, guidebook or other explanatory material |
| `support` | Where to report a problem with the deck package |

```toml
[deck]
name = "The Example Tarot"
links = [
  { rel = "buy", url = "https://example.com/shop/the-deck", title = "Buy from the artist" },
  { rel = "artist", url = "https://example.com/about" },
]
publisher = "Example Press"
```

`links` is written as an array of inline tables, which makes it an ordinary key of `[deck]` that MAY appear anywhere among its other keys. Writing it instead as `[[deck.links]]`, a TOML array-of-tables header, would silently capture every `[deck]` key that followed it: the `publisher` line above would become a key of the last link rather than of the deck, TOML would report no error, and `[deck]` could not be reopened to recover. An author who keeps `links` last avoids this, but nothing makes them, so this specification does not offer the shape.

The registry is open. An application MUST ignore a link whose `rel` it does not recognize, and MUST NOT treat an unrecognized `rel` as an error. A future version of this specification MAY add to the registry, so a deck author who needs a relation it does not define SHOULD prefix it, as in `mydeck_kickstarter`, to avoid colliding with a later addition.

A `buy` link is the packager's own; it is not a statement by anyone else that the deck may be sold. Where a deck is packaged from artwork the packager does not own, a `buy` link pointing at the rights holder is the most useful thing the package can carry, and applications SHOULD surface it.

#### 4.1.2 `signifies`

`[deck].signifies` holds the [qualified identifier](#33-qualified-identifiers) of another deck, and says: *the artwork my cards describe is the artwork of that deck, which this package does not carry.*

```toml
[deck]
name = "The Example Tarot"
identifier = "my.personal.domain/deck/example-tarot-surrogate"
signifies = "com.example/deck/example-tarot"
```

The word is borrowed from the tarot **significator**, the card chosen to stand for a querent who is not themselves present at the table.

Two kinds of packager declare it, and the field says the same thing for both. A third party who holds a published deck and wants to describe it points at the deck the rights holder published. A rights holder who ships a free listing of their own paid deck points at their own full package. The field is a statement about the relation between two *packages*, so it carries no claim about who wrote it and confers no rights in either direction.

Rules:

- The value MUST be the `[deck].identifier` of the package it signifies, so that it can serve as a merge key ([§5.9](#59-surrogate-decks)).
- It MUST NOT equal this deck's own `identifier`. A package does not signify itself.
- Nothing resolves a qualified identifier ([§3.3](#33-qualified-identifiers)), so a validator can check that the value is well formed and no more. A `signifies` naming a deck that does not exist, or one that never declared an `identifier`, is permitted and unverifiable.

The last rule has a consequence worth stating plainly for packagers. A realm is a domain its owner controls, so a third party cannot mint an identifier on a rights holder's behalf; they can only point at one the rights holder already published. Where none exists, the packager has two honest options: point at an identifier minted by whoever *does* catalog the work, or omit `signifies` and let the package stand alone. Neither this specification nor any application operates a registry, and no version of this specification will require one.

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

Cards are [discovered from the directory structure](#51-asset-discovery) so the `[cards]` table supplies what is not available from the filename alone, such as the card's printed number, its place in the deck's sequence and fallback display strings. It is OPTIONAL in its entirety.


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
| `surrogate/` | surrogate | none |

`<height>` and `<lines>` are decimal integers greater than zero, written without a sign, leading zeroes or separators. A deck MAY contain any number of raster and ANSI roots, and at most one `scalable/` and one `surrogate/`.

Within an image root, assets are arranged by card type and suit as shown in [§2.1](#21-directory-skeleton): `major_arcana/` and `minor_arcana/<suit>`. An image root MAY also hold a `card_backs/` directory, which supplies card back designs at that root's kind and size ([§5.5](#55-card-back-images)). Any other subdirectory is ignored, and so is any file lying loose in the root itself rather than in one of those subdirectories.

Every other top-level directory is ignored by discovery.

A surrogate is not an image, but it is discovered, keyed, sized against and resolved exactly as one, so this specification treats it as a fourth kind rather than as a mechanism of its own. Everything in [§5.7](#57-card-image-resolution) that speaks of a kind therefore includes it, with the two differences [§5.8](#58-surrogate-assets) gives.

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

`scalable/` and `surrogate/` hold at most one file per card and variant, so selection there is trivial: the file is the file.

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

In `scalable/`, the chain is `svg` alone. In `surrogate/`, it is `toml` alone.

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

An application MUST NOT present a borrowed image as though it were the deck's own, and SHOULD make the substitution visible to the user, on the same terms as a [surrogate](#58-surrogate-assets) ([§5.8](#58-surrogate-assets)). This one needs saying more than the surrogate case does, not less: a surrogate is visibly a placeholder and announces itself, whereas a card resolved from the reference deck is a finished image sitting in the grid beside the deck's own, and nothing in it tells the user that another artist drew it.

Where an application displays attribution, licensing or rights metadata for a borrowed card, it MUST take that metadata from the reference deck rather than from the deck under display. A borrowed image carries the reference deck's terms, which may be narrower than those of the deck it is standing in for, and an application that exports, prints or shares a spread containing one is passing on that deck's artwork under that deck's license.

#### 5.7.7 Resolving a Card Back

An application resolves a back the same way, with three differences:

1. The subpath is `card_backs/` rather than `major_arcana/` or `minor_arcana/<suit>/` and the stem is the design key.
2. Where no image root of the requested kind supplies the design, the top-level `card_backs/` directory is consulted last as a root of no size. Because it declares no kind either, an application that finds nothing there under the chain for the kind it asked for MAY take any file in it whose stem is the design key and whose format it can decode.
3. There is no reference-deck and applications supply their own back.

#### 5.7.8 Resolution Summary

Given a card, a variant key, a kind and a target size, an application:

1. Forms the stem from the card's base, plus `.<variant-key>` where one is requested, and the subpath `major_arcana/` or `minor_arcana/<suit>/`.
2. Ranks the image roots of the requested kind by [§5.7.3](#573-size-selection-within-a-kind) and, best first, looks in `<root>/<subpath>` for that stem under the [extension chain](#574-the-extension-chain), taking the first file it can decode. Walking past a root it cannot decode costs it a fallback rather than the card.
3. Failing that, and where a variant was requested, repeats step 2 for the card's default variant ([§5.7.5](#575-variants)).
4. Failing that, resolves the card against the [reference deck](#13-terminology) where the library has one, the card is not excluded, and the card has a canonical counterpart ([§5.7.6](#576-when-no-asset-is-found)). This step sits outside the per-deck lookup, so a reference deck is consulted once the deck itself is exhausted and never in the middle of size selection.

Card backs follow the same shape with the differences [§5.7.7](#577-resolving-a-card-back) gives. An explicit `image` path wins outright, the subpath is `card_backs/` and the stem is the design key, the top-level `card_backs/` is consulted last, and there is no reference-deck step.

ANSI files are exempt from the extension chain: [§5.4](#54-ansi-art) allows them any extension, so in an ANSI root a lookup matches on stem alone and determines the file's kind from its content. An application MUST apply [§10.2](#102-terminal-escape-injection) to any ANSI file it writes to a terminal.

### 5.8 Surrogate Assets

A surrogate is a derived, deliberately lossy stand-in for a card's artwork that lives in the `surrogate/` [image root](#571-image-roots) and are discovered like other card assets ([§5.1](#51-asset-discovery)):

```
surrogate/
  major_arcana/
    00.toml               # major_arcana.00
    06.two_women.toml     # major_arcana.06:two_women
  minor_arcana/
    wands/
      ace.toml            # minor_arcana.wands.ace
  card_backs/
    classic.toml          # the "classic" design
```


A deck MAY carry them instead of artwork, which makes it a [surrogate deck](#59-surrogate-decks). An application MUST NOT present a surrogate as though it were the artwork, and SHOULD make the distinction visible to the user.

A deck MAY carry surrogates alongside its artwork, where an application could render them as progressive-loading placeholders. 

In contrast to other assets, surrogates are not associated with a reference deck.

#### 5.8.1 The Surrogate File

A surrogate file is a TOML document ([§2.3](#23-file-format-and-encoding)) whose keys are:

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `palette` | Array of String | No | `[]` | Dominant colors, most prominent first, each an sRGB hex triplet written `#rrggbb` in lower case. |
| `palette_snapped` | Array of String | No | `[]` | `palette`, each entry replaced by the nearest [CSS Color 4 named color](https://www.w3.org/TR/css-color-4/#named-colors),|
| `thumbhash` | String | No | none | A [ThumbHash](https://evanw.github.io/thumbhash/) of the artwork, Base64-encoded. |

```toml
# surrogate/major_arcana/00.toml
# generated by libarcana 0.4.2
palette = ["#e8d5a3", "#2b4a6f", "#8c3b2e", "#d9d2c4"]
palette_snapped = ["wheat", "darkslateblue", "sienna", "lightgray"]
thumbhash = "1QcSHQRnh493V4dIh4eXh1h4kJUI"
```


Every key is optional and independent. A deck MAY carry any combination and MAY carry different combinations for different cards. A file carrying none of them is a well-formed surrogate.

### 5.9 Surrogate Decks

A surrogate deck is a deck whose only card assets are surrogates. Because the artwork of most tarot decks is neither the packager's to give away nor, in many cases, licensed for redistribution at all, surrogates allow a deck to be packaged without shipping anyone else's art.

A surrogate deck SHOULD declare [`[deck].signifies`](#412-signifies) naming the deck whose artwork it describes. This field is used as a merge key and allows applications to recognize them as the same underlying deck and prefer the artwork.

A surrogate deck SHOULD also declare [`[deck].rights_status`](#74-rights-status), and it SHOULD contain a `buy` [link](#411-links).

**Licensing the surrogates.** [`[deck].license`](#41-deck) covers the card assets the package carries ([§7](#7-licensing-and-attribution)), so in a surrogate deck it covers the surrogates rather than the artwork. This is the one case where the two come apart, and it is the case the split exists for: the packager generated the surrogates and can license them, while `rights_status` says accurately that the artwork behind them belongs to someone else. A surrogate deck SHOULD declare `license`, since [`derivation`](#75-redistribution-and-derivation) of `"surrogate"` invites a downstream user to pass the surrogates on and `license` is what tells them on what terms.

> **Note (informative).** A deck carrying artwork *and* surrogates has one `license` field for both, which is imprecise where the two are under different terms, as when a packager generates surrogates from artwork they did not license. In practice the packager generating surrogates for a deck they already ship is licensing both under the same terms, so a single field describes the package correctly. Splitting them would need a new field and is left to a later minor version should the case arise.

**The icon.** [`[deck].icon`](#41-deck) is not a card asset, so the rule above does not reach it and a package could otherwise satisfy every requirement of this section while shipping the artwork as its preview image. A surrogate deck's `icon`, where it has one, MUST NOT be the signified deck's artwork or a crop, scaling or recompression of it. It SHOULD be the packager's own work or a rendering of the surrogates the deck carries. A deck that has no icon it is entitled to ship declares none, and an application supplies its own presentation.

No validator can check this, since whether one image derives from another is not decidable from the package. It is stated as a requirement rather than a recommendation because a surrogate deck exists precisely to not redistribute the artwork, and an icon that does defeats the whole package rather than blemishing it.

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

- The license specified by `[deck].license` covers the card assets the package carries. For most decks those assets are the artwork and the field says what may be done with it. For a [surrogate deck](#59-surrogate-decks) they are the surrogates, which the packager generated and is therefore in a position to license, and the artwork they describe is covered by [`rights_status`](#74-rights-status) instead.
- The license in the `[metadata].license` field of a name file covers the strings in that file and `[metadata.alt_text]` narrows that to the alt text alone.

Each of these names its own license texts through its own `license_files`, and no filename is special. In particular a file named `LICENSE` at the deck root carries no meaning this specification assigns: it is the artwork's license only where `[deck].license_files` says so, and a deck whose packaging is licensed separately from its artwork names that file too. Nothing is picked up by convention, because a deck assembled from someone else's artwork usually has two sets of terms in one directory and guessing between them is how the wrong one gets displayed.

Not every deck has a license to name. Where the artwork is published commercially and the packager holds nothing but a copy of it, [`[deck].rights_status`](#74-rights-status) states the artwork's copyright status instead, and [`[deck].redistribution` and `[deck].derivation`](#75-redistribution-and-derivation) state what the packager passes on.

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
| `license` | SPDX license expression governing the card assets the package carries |
| `license_files` | Paths, relative to the deck root, to the full license text and any notices. Empty by default; no filename is picked up by convention ([§7](#7-licensing-and-attribution)) |
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

**Modified artwork.** Several public licenses, Creative Commons Attribution among them, require a downstream user who alters the work to say that they altered it. A packaged deck is very often altered: scans get deskewed, borders cropped, colors corrected, images upscaled. This specification defines no separate field for it, so a deck whose artwork is a modified version of someone else's SHOULD say so in `attribution`, which is the string an application displays and therefore the only place the statement reaches a reader. Where the artwork was obtained from a particular scan or archive rather than from the rights holder, a [`source` link](#411-links) SHOULD name it.

```toml
[deck]
license = "CC-BY-4.0"
copyright = "© 2018 Some Artist"
attribution = "\"The Example Tarot\" by Some Artist, licensed under CC BY 4.0. Cropped and color-corrected for this package."
links = [{ rel = "source", url = "https://example.org/archive/example-tarot" }]
```

### 7.3 Name File Licensing

The strings in a name file are not necessarily the packager's own work, since alt text might be written by a contributor or adapted from a published source. Each name file states its own terms in its [`[metadata]`](#621-name-file-metadata) table, using the same fields as `[deck]` and with the same meanings.

```toml
# names/en.toml
[metadata.alt_text]
source = "Descriptions contributed by Jane Doe."
license = "CC0-1.0"
```

Most decks need only to license their alt text, which `[metadata.alt_text]` does on its own as shown above. Where the whole file is a single person's work, as with a translation, `[metadata]` covers the entire file including its alt text. Where the two differ, `[metadata]` gives the file's terms and `[metadata.alt_text]` overrides them for alt text alone.

```toml
# names/pt-BR.toml
[metadata]
source = "Translated by Paulo Freire."
license = "CC-BY-4.0"
license_files = ["names/LICENSE.pt-BR"]
attribution = "Portuguese translation by Paulo Freire."
```

A name file that transcribes another deck's own names for its cards, as a package describing a deck it does not carry usually does, is reproducing that deck author's choices and not only the packager's: an individual card name is a short phrase, but a full set of one author's renamings is a compilation, and the packager did not write it. Such a file SHOULD say where the names came from in `[metadata].source` and SHOULD carry a [`rights_status`](#74-rights-status) for them rather than a `license` the packager is in no position to grant.

### 7.4 Rights Status

A license is a *grant*. Every SPDX identifier names terms under which someone gave permission, so `[deck].license` can only speak for assets that somebody licensed. Most tarot decks are not licensed to anyone. A deck packaged from a commercially published deck the packager owns a copy of has no grant to record, and leaving `license` empty says only that the field was not filled in.

`[deck].rights_status` records the *artwork's* copyright status instead, which is a statement about the world rather than a permission. The two fields therefore need not be about the same thing: `license` is about the files in this directory and `rights_status` is about the work they depict. For an ordinary deck these coincide and both describe the artwork. For a [surrogate deck](#59-surrogate-decks) they come apart, and that is the point of having both, since the packager can license the surrogates they generated while saying accurately that the artwork behind them is in copyright to someone else.

`rights_status` SHOULD be one of:

- a [RightsStatements.org](https://rightsstatements.org/) URI, which covers the cases SPDX structurally cannot: in copyright with no license granted, in copyright with the holder unknown or unlocatable, and status undetermined or not evaluated;
- a [Creative Commons](https://creativecommons.org/) URI, including the public domain marks `publicdomain/mark/1.0/` and `publicdomain/zero/1.0/`.

```toml
# A deck packaged from a copy the packager owns. No license exists to name.
[deck]
rights_status = "https://rightsstatements.org/vocab/InC/1.0/"
copyright = "© 2012 Some Artist"
attribution = "The Example Tarot by Some Artist."
```

```toml
# A deck whose artwork is old enough that its copyright has expired. Note that a
# faithful reproduction of a public-domain work generally creates no new copyright.
[deck]
license = "CC0-1.0"
rights_status = "https://creativecommons.org/publicdomain/mark/1.0/"
```

`license` and `rights_status` answer different questions about, in general, different objects, and a deck MAY carry both, one, or neither. Where both are present and both are about the artwork, which is the case for any deck that carries its artwork, they MUST NOT contradict each other; a validator cannot check this in general and does not try, beyond the coarse cases [§9.4](#94-validation-rules) lists.

The same field is available in a name file's `[metadata]` and `[metadata.alt_text]` tables, with the same meaning ([§7.3](#73-name-file-licensing)). Freely licensed alt text describing artwork that is not freely licensed is the ordinary case for a deck packaged from a published one, and the two tables are how a deck says so.

### 7.5 Redistribution and Derivation

`license` covers the assets carried and `rights_status` describes the artwork behind them. Neither answers the question an application actually has to act on, which is what it may do with *this package*. `[deck].redistribution` and `[deck].derivation` answer it. Each takes one of:

| Value | Meaning |
| --- | --- |
| `"full"` | The artwork may be passed on as it is. |
| `"surrogate"` | The artwork may not be passed on, but a [surrogate](#58-surrogate-assets) derived from it may. |
| `"none"` | Neither may be passed on. |
| `"unstated"` | The packager has not said. The default. |

`redistribution` governs republishing the artwork; `derivation` governs making new work from it. They vary independently, and the combination that motivates having both is `redistribution = "none"` with `derivation = "surrogate"`: keep the images to yourself, but generate and share a [surrogate deck](#59-surrogate-decks) from them.

```toml
[deck]
name = "The Example Tarot"
rights_status = "https://rightsstatements.org/vocab/InC/1.0/"
redistribution = "none"
derivation = "surrogate"
```

Three rules bound what these fields mean.

- **They are declarations, not grants.** The [packager](#12-document-conventions) says here what they believe they are passing on. Nobody can grant permission they do not hold, and a `redistribution` of `"full"` over artwork the packager had no right to redistribute conveys nothing.
- **Absence is not permission.** `"unstated"` means the question was not answered. An application MUST NOT read it as `"full"`, and one that redistributes decks on a user's behalf SHOULD treat `"unstated"` as it treats `"none"`.
- **They do not narrow a license.** Where `license` grants more than these fields state, the license governs; a deck cannot use these fields to take back permissions it has already given under CC BY or any other public license. They are for artwork no public license covers, which is the case they exist for.

### 7.6 Naming the Packager

Nearly every field in this section is a statement by the [packager](#12-document-conventions): `rights_status` is their reading of the artwork's status, `redistribution` and `derivation` are what they believe they are passing on, and `attribution` is the credit line they judged the license to require. `[deck].packager` names who that was.

```toml
[deck]
name = "The Example Tarot"
author = "Some Artist"          # who drew it
publisher = "Example Press"     # who published it
packager = "Jane Doe <jane@example.org>"   # who built this directory
```

The field is a free-form display string and this specification defines no syntax for it. A name, a handle, an email address or a project is each a reasonable value.

A deck SHOULD declare `packager` where the packager is not the artwork's `author`, and a package describing artwork it does not own SHOULD always declare it. Two things follow from the packager being identifiable. A reader can weigh a rights assertion by who made it, which matters because nothing in this specification verifies one. And a rights holder who disagrees with the assertion has someone to raise it with, which is the difference between a package that can be corrected and one that can only be removed. A [`support` link](#411-links) serves the same end and a deck SHOULD carry one.

`packager` is metadata about the package rather than about the artwork, so it is not localized and an application MUST NOT display it as the deck's author.

### 7.7 Deck Names and Trademarks

The name of a published tarot deck is frequently a trademark of its publisher, and `[deck].name` is displayed verbatim to the user. This raises no issue for the ordinary use of the field. A package that names the deck it contains or describes is referring to that deck, which is what a trademark is for and what its owner wants; using a mark to identify the thing it marks is not an infringement of it.

What a package MUST NOT do is imply an endorsement, affiliation or origin it does not have. Concretely:

- A deck's `name`, `description` and `attribution` MUST NOT state or imply that the rights holder produced, approved or endorsed the package, unless they did.
- A package assembled by a third party SHOULD declare [`packager`](#76-naming-the-packager), which distinguishes it from an official one more plainly than any wording could.
- A [`buy`](#411-links) or `publisher` link SHOULD point at the rights holder rather than at a reseller ([§4.1.1](#411-links)).
- A packager SHOULD NOT reproduce the publisher's logo or wordmark as the deck's `icon`. An icon is the packager's own presentational choice and a mark is not needed to identify a deck already named.

Nothing here is a legal determination and this specification does not make one. Trademark turns on likelihood of confusion, which is a question about a particular package in a particular market, and no field can settle it. These are the practices that keep the question from arising.

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
- MUST have at least one card asset discoverable under [§5.1](#51-asset-discovery). A [surrogate](#58-surrogate-assets) is a card asset, so a [surrogate deck](#59-surrogate-decks) satisfies this rule without an exception being made for it. A deck with no assets of any kind has nothing to show and is not a deck.
- MUST produce no errors under [§9.4](#94-validation-rules).

### 9.2 Errors and Warnings

A validator reports two kinds of violations. An **error** makes a deck non-conforming and an application MAY refuse it. A **warning** marks something an author probably did not intend, or a condition this specification allows but has an opinion about. An application MUST load a deck that produces only warnings.

### 9.3 Conforming Applications and Validators

A conforming application:

- MUST implement deck discovery ([§2.2](#22-the-deck-library), [§5.1](#51-asset-discovery)), display name resolution ([§6.3](#63-display-name-resolution)) and card image resolution ([§5.7](#57-card-image-resolution)).
- MUST support decoding PNG and JPEG ([§5.7.4](#574-the-extension-chain)).
- MUST ignore `[app]` subtables it does not own ([§8](#8-extensibility)), and every table, key and value this specification does not define.
- MUST NOT reject a deck for warnings ([§9.2](#92-errors-and-warnings)).

An application need not implement editions, card variants, ANSI art, SVG, surrogates or localization beyond the deck's default language. Where it does not, it uses the defaults those sections define. An application that does not implement surrogates ignores the `surrogate/` root as it ignores any kind it cannot render, and so treats a [surrogate deck](#59-surrogate-decks) as a deck whose cards have no assets, which [§5.7.6](#576-when-no-asset-is-found) already defines. A conforming validator implements the rules in [§9.4](#94-validation-rules).

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
| **W** | A `rights_status` that is not a RightsStatements.org or Creative Commons URI, in `[deck]` and in every name file's `[metadata]` alike. As with `license`, a deck that fails this check MUST NOT be rejected ([§7.4](#74-rights-status)). |
| **E** | `redistribution` and `derivation`, where present, are one of `full`, `surrogate`, `none` or `unstated` ([§7.5](#75-redistribution-and-derivation)). |
| **W** | A deck that declares neither `license` nor `rights_status`. One of the two is how a deck says what may be done with its artwork, and a deck that says neither leaves every downstream user guessing ([§7](#7-licensing-and-attribution)). |
| **W** | A `redistribution` or `derivation` of `full` alongside a `rights_status` asserting the artwork is in copyright with no license granted, meaning a RightsStatements.org `InC` URI or one of its refinements. The deck says both that nobody granted permission and that the packager passes it on ([§7.5](#75-redistribution-and-derivation)). One of the two fields is wrong, and a validator cannot tell which. |
| **W** | A `redistribution` or `derivation` narrower than `full` on a deck whose `license` is a public license granting redistribution or derivation outright. The license governs and the field does not take it back ([§7.5](#75-redistribution-and-derivation)), so the field misleads a reader without binding anyone. A validator checks this only for licenses it recognizes, and reporting nothing is a conforming outcome. |
| **W** | A [surrogate deck](#59-surrogate-decks) declaring `redistribution = "full"`. The field governs passing on the artwork and the package carries none ([§5.9](#59-surrogate-decks)). A `license` on such a deck is not reported, since it covers the surrogates and a surrogate deck SHOULD carry one. |
| **W** | A [surrogate deck](#59-surrogate-decks) with no `license`. Its surrogates are the packager's own work and `derivation = "surrogate"` invites them to be passed on, so a reader who takes them up has no terms to go by ([§5.9](#59-surrogate-decks)). |
| **W** | A deck that names artwork it did not produce and does not declare `packager`, meaning one carrying `signifies`, or one whose `rights_status` asserts the artwork is in copyright to someone else ([§7.6](#76-naming-the-packager)). Every rights assertion in the package is then unattributable. |
| **W** | A `packager` equal to `author`. Where the two are the same person the field says nothing, and where they are not one of them is wrong ([§7.6](#76-naming-the-packager)). |
| **E** | Every `[deck].links` entry carries a `rel` that is a well-formed [custom name](#32-custom-names) and a `url` that is absolute with an `http` or `https` scheme ([§4.1.1](#411-links)). |
| **W** | A `links` `rel` outside the registry of [§4.1.1](#411-links) that is not prefixed. Applications ignore it, and a later version of this specification may claim the name. |
| **E** | `[deck].signifies`, where present, is a well-formed qualified identifier and is not equal to this deck's own `identifier` ([§4.1.2](#412-signifies)). Whether it names a deck that exists is not checkable and is not checked. |
| **E** | Every file in the `surrogate/` root is well-formed TOML 1.0.0 and carries no key this specification does not define for a [surrogate file](#581-the-surrogate-file). |
| **E** | Every entry of a `palette` is an sRGB hex triplet matching `#` followed by six lower-case hexadecimal digits, every entry of `palette_snapped` is a CSS Color 4 named color. |
| **W** | A `palette_snapped` whose length differs from that of the `palette` beside it. The two are meant to be the same colors in the same order ([§5.8.1](#581-the-surrogate-file)). |
| **W** | A surrogate deck without `[deck].signifies`. Nothing can then connect it to the deck it describes, and an application holding both cannot merge them ([§5.9](#59-surrogate-decks)). |
| **W** | A surrogate deck with no `buy` link and no `[deck].rights_status`. It describes artwork the reader cannot see, without saying why or where to get it ([§5.9](#59-surrogate-decks)). |

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
rights_status = "https://creativecommons.org/publicdomain/mark/1.0/"
redistribution = "full"
derivation = "full"

default_language = "en"
created_date = "1909-12-01"
updated_date = "2025-04-28"
tags = ["traditional", "classic", "beginner-friendly"]
links = [
  { rel = "homepage", url = "https://en.wikipedia.org/wiki/Rider%E2%80%93Waite_Tarot" },
]

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

### A.6 A Surrogate Deck

A collector holds a commercially published deck and wants to list it in a public catalog. The artwork is not theirs to redistribute, but the description of the deck is ordinary fact and the surrogates are derived data. The package carries a `surrogate/` root and no other.

```
example-tarot/
  deck.toml
  names/en.toml
  surrogate/
    major_arcana/
      00.toml
      01.toml
      …
    minor_arcana/
      wands/
        ace.toml
        …
```

```toml
# deck.toml
[deck]
schema_version = "2.0"
name = "The Example Tarot"
identifier = "my.personal.domain/deck/example-tarot-surrogate"
signifies = "com.example/deck/example-tarot"
version = "1.0"
author = "Some Artist"
publisher = "Example Press"
packager = "Jane Doe <jane@example.org>"
aspect_ratio = 0.5789

license = "CC0-1.0"                 # covers the surrogates, which are Jane's work
rights_status = "https://rightsstatements.org/vocab/InC/1.0/"   # covers the artwork
copyright = "© 2012 Some Artist"
attribution = "The Example Tarot by Some Artist, published by Example Press."
redistribution = "none"
derivation = "surrogate"

tags = ["indie", "modern"]
links = [
  { rel = "buy", url = "https://example.com/shop/the-example-tarot", title = "Buy from Example Press" },
  { rel = "artist", url = "https://example.com/artist" },
]
```

```toml
# surrogate/major_arcana/00.toml
# generated by libarcana 0.4.2
palette = ["#e8d5a3", "#2b4a6f", "#8c3b2e"]
palette_snapped = ["wheat", "darkslateblue", "sienna"]
thumbhash = "LEHV6nWB2yk8pyo0adR*.7kCMdnj"
```

```toml
# surrogate/minor_arcana/wands/ace.toml
palette = ["#c2452d", "#f0e4c8", "#3f6b3a"]
palette_snapped = ["firebrick", "cornsilk", "darkolivegreen"]
thumbhash = "L6PZfSjE.AyE_3t7t7R**0o#DgR4"
```

Note what the package does and does not claim. `redistribution = "none"` says the collector passes on no artwork, which is consistent with there being none here. `derivation = "surrogate"` says they consider the surrogates themselves shareable, and `license` says on what terms: the surrogates are Jane's own work and she puts them in the public domain. `rights_status` is about a different object, the artwork the surrogates describe, and says it is in copyright with no license granted, which `license` could not have expressed ([§7.4](#74-rights-status)). `packager` names who made all of these assertions, none of which the artist or the publisher has agreed to. The `buy` link points at the people who can sell the reader the real thing.

`signifies` points at `com.example/deck/example-tarot`, in the publisher's realm rather than the collector's. The collector did not mint that identifier and could not have; they are pointing at one Example Press published. Their own package has its own `identifier` in their own realm, and the two are different packages describing one deck. A user whose library holds both this package and the publisher's full one has a single deck with artwork, and this package's alt text and links besides.

The deck names its cards, orders them, and carries alt text in `names/en.toml`. Card resolution finds nothing for any kind but `surrogate`. An application shows the surrogates, the metadata and the links.

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

This table is dedicated to the public domain under CC0 1.0, along with its selection and arrangement, and is not subject to the attribution term the rest of this document carries ([§1.6](#16-licensing-of-this-specification-informative)). Copy it into an implementation freely.

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
- [Rights status](#74-rights-status), [redistribution and derivation](#75-redistribution-and-derivation), for artwork that no license covers. `[deck].license` now covers the card assets a package carries rather than the artwork specifically, so that a package can license what it ships while `rights_status` describes the work behind it.
- [Surrogates](#58-surrogate-assets) and [surrogate decks](#59-surrogate-decks), so that a deck can be described without its artwork being redistributed. A surrogate is a card asset of its own kind in the `surrogate/` image root, discovered and resolved like any other.
- [`[deck].signifies`](#412-signifies), by which one package names the deck whose artwork it describes but does not carry.
- [`[deck].links`](#411-links), replacing `[deck].website` with typed links that say what they point at.
- [`[deck].packager`](#76-naming-the-packager), naming who assembled a package and therefore who made the rights assertions in it, together with [§7.7](#77-deck-names-and-trademarks) on deck names that are trademarks.

**Other changes.** Restructured the document as a specification, adopting BCP 14 keywords explicitly, replacing the regex identifier forms with one consolidated [ABNF grammar](#35-grammar) and lifting fields out of TOML comments into [normative field tables](#4-decktoml-reference). Added [qualified identifiers](#33-qualified-identifiers) and formalized custom names and display name resolution. Made every card discoverable from the directory structure, added [card variants](#47-card_variants), allowed custom `ranks` for canonical suits and added `name_template` composition. Specified name file language tags as BCP 47, added `default_language`. Specified `license` as SPDX, added `license_files` and `copyright`, and added the `[metadata]` table to name files. Added `rights_status`, `redistribution` and `derivation` for artwork SPDX cannot describe. Named the [packager](#12-document-conventions) as an actor in [§1.2](#12-document-conventions), since the licensing fields exist largely for the case where the packager is not the rights holder. Required an ANSI file's kind to be detected from its content and recommended honoring a SAUCE record. Defined what `[app]` is for and reserved top-level table names outside it.
