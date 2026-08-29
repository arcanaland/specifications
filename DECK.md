# Tarot Deck Specification

> Maintained By: [Arcana Land](https://github.com/arcanaland)
>
> Version: 2.0 (draft)

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
    - [2.2.1 The Library Model](#221-the-library-model)
    - [2.2.2 Scanning](#222-scanning)
    - [2.2.3 Shadowing](#223-shadowing)
  - [2.3 File Format and Encoding](#23-file-format-and-encoding)
  - [2.4 Deck Containers](#24-deck-containers)
- [3. Identity and Identifiers](#3-identity-and-identifiers)
  - [3.1 Canonical IDs](#31-canonical-ids)
    - [3.1.1 A Canonical ID Is a Slot](#311-a-canonical-id-is-a-slot)
    - [3.1.2 Card References and the Variant Suffix](#312-card-references-and-the-variant-suffix)
  - [3.2 Custom Names](#32-custom-names)
  - [3.3 Qualified Identifiers](#33-qualified-identifiers)
  - [3.4 Deck Identity](#34-deck-identity)
  - [3.5 Grammar](#35-grammar)
  - [3.6 Identifiers in TOML](#36-identifiers-in-toml)
- [4. deck.toml Reference](#4-decktoml-reference)
  - [4.1 `[deck]`](#41-deck)
    - [4.1.1 Links](#411-links)
    - [4.1.2 `surrogate_for`](#412-surrogate_for)
    - [4.1.3 `follows`](#413-follows)
    - [4.1.4 `pips`](#414-pips)
    - [4.1.5 Product Identifiers](#415-product-identifiers)
    - [4.1.6 Content Rating](#416-content-rating)
    - [4.1.7 Published Date](#417-published-date)
    - [4.1.8 Artwork Origin](#418-artwork-origin)
    - [4.1.9 Related Decks](#419-related-decks)
  - [4.2 `[card_backs]`](#42-card_backs)
  - [4.3 `[cards]`](#43-cards)
    - [4.3.1 Card Numbers](#431-card-numbers)
    - [4.3.2 Ordering](#432-ordering)
  - [4.4 `[suits]`](#44-suits)
  - [4.5 `[ranks]`](#45-ranks)
  - [4.6 `[excluded_cards]`](#46-excluded_cards)
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
    - [6.2.2 Group Names](#622-group-names)
  - [6.3 Display Name Resolution](#63-display-name-resolution)
    - [6.3.1 Minor Arcana Name Composition](#631-minor-arcana-name-composition)
  - [6.4 Alt Text Guidelines](#64-alt-text-guidelines)
- [7. Licensing and Attribution](#7-licensing-and-attribution)
  - [7.1 License Expressions](#71-license-expressions)
  - [7.2 Attribution and Notices](#72-attribution-and-notices)
  - [7.3 Name File Licensing](#73-name-file-licensing)
  - [7.4 Rights Status](#74-rights-status)
  - [7.5 Redistribution and Derivation](#75-redistribution-and-derivation)
  - [7.6 Roles and Credits](#76-roles-and-credits)
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
  - [A.3 Renamed Suits, a Custom Card and Two Card Backs](#a3-renamed-suits-a-custom-card-and-two-card-backs)
  - [A.4 A Lowercase Typographic Convention](#a4-a-lowercase-typographic-convention)
  - [A.5 Deck with Card Variants](#a5-deck-with-card-variants)
  - [A.6 A Surrogate Deck](#a6-a-surrogate-deck)
- [Appendix B. Reserved and Deprecated Names](#appendix-b-reserved-and-deprecated-names)
- [Appendix C. Canonical Card Names (Informative)](#appendix-c-canonical-card-names-informative)
- [Appendix D. Platform Conventions (Informative)](#appendix-d-platform-conventions-informative)
- [Appendix E. Changelog](#appendix-e-changelog)

## 1. Introduction

### 1.1 Scope and Design Goals

This specification defines a standard format for tarot decks used by tarot applications. The format is designed to:

- Separate presentation (e.g., images and names) from interpretation (e.g., meanings and divination).
- Establish a canonical identifier system for tarot objects that can be shared across various Arcana Land specifications.
- Support internationalization (i18n) and localization (l10n).
- Support decks with extra or missing cards.
- Allow flexibility for suit and court card renaming.
- Ensure compatibility with other Arcana Land specifications, including the [Esoterica Specification](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md) for interpretive meanings and the proposed [Spread Specification](https://github.com/arcanaland/specifications/blob/main/SPREAD.md) for geometric arrangements.

Decks are directories with a mandatory `deck.toml` file at the root.

### 1.2 Document Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY" and "OPTIONAL" in this document are to be interpreted as described in BCP 14 ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) when, and only when, they appear in all capitals. Where this document writes "should", "must" or "may" in lower case, the word carries its ordinary English sense and imposes no requirement.

A section whose title carries the suffix (Informative) contains no requirements, and everything else in this document is normative. Whatever section they appear in, all **Notes** and all **Examples** are informative. Where an example appears to conflict with a normative rule, the rule governs and the example is in error.

This specification addresses three kinds of actors: packagers who craft a `deck.toml` and arrange files around it, applications that read a deck in order to present it to a user, and validation tools that check a deck against this specification.

A packager is whoever assembles the package. They may be the artist who made the artwork, the publisher who holds the rights to it, or a third party with neither, such as a collector or a distribution maintainer. Where this document says a deck "declares" or "says" something, the packager is who said it.

### 1.3 Terminology

| Term | Meaning |
| --- | --- |
| **artwork** | Any image within a deck such as a card's default artwork, a [card variant](#312-card-references-and-the-variant-suffix), or a [card back design](#42-card_backs). |
| **base** | The part of a card asset's file stem before the first dot. In `06.two_women.png` the stem is `06.two_women` and the base is `06` ([§5.7.2](#572-extensions-stems-and-bases)). |
| **canonical ID** | The identifier by which a card is uniquely addressed: `major_arcana.<key>` or `minor_arcana.<suit>.<rank>` ([§3.1](#31-canonical-ids)). It attaches no meaning. |
| **card back design** | One of the card back images inside a deck, named by a design key ([§4.2](#42-card_backs)). |
| **card number** | The number printed on a card's face as a display string ([§4.3.1](#431-card-numbers)). Distinct from **position**, which orders cards relative to each other. |
| **card reference** | A canonical ID, optionally followed by a **variant suffix** (`:` and a variant key). `major_arcana.06` and `major_arcana.06:two_women` are both card references. The suffixed form is also called a **variant reference**. |
| **card type** | Which of the two arcana a card belongs to: `major_arcana` or `minor_arcana`. |
| **card variant** | An alternative artwork for a card. Variants of a card are interchangeable and denote the same meaning. |
| **container** | A single zip file containing a deck directory ([§2.4](#24-deck-containers)). |
| **custom name** | An identifier created by the packager. For example, custom cards, suits, ranks, card back designs and card variant keys ([§3.2](#32-custom-names)). |
| **deck** | A directory containing a `deck.toml`, together with the card assets and name files arranged around it. |
| **deck library** | An ordered list of **library roots**, each a directory whose immediate children are candidate deck roots ([§2.2](#22-the-deck-library)). |
| **deck root** | The directory that directly contains a deck's `deck.toml`. |
| **extended major arcanum** | A major arcanum keyed beyond the canonical numbers into `22`–`99`. |
| **major arcana** | The cards keyed under `major_arcana`. The twenty-two keyed `00`–`21` are the canonical major arcana. |
| **minor arcana** | The suited cards, canonically fifty-six, keyed by **suit** and **rank** under `minor_arcana`. The canonical suits are `wands`, `cups`, `swords` and `pentacles`. The canonical ranks are `ace` through `ten`, then `page`, `knight`, `queen` and `king`. A deck MAY define others. |
| **name file** | A `names/<tag>.toml` file enumerating display strings for one language tag. |
| **packager** | Whoever assembled a deck package. Not necessarily the artist and not necessarily the rights holder ([§1.2](#12-document-conventions)). |
| **position** | An integer sort key placing a major arcanum in the deck's sequence ([§4.3.2](#432-ordering)). |
| **realm** | A domain name (preferably, one the packager controls) written in reverse ([§3.3](#33-qualified-identifiers)). |
| **qualified identifier** | An identifier naming an Arcana Land entity unambiguously across authors, composed of a **realm** and a path ([§3.3](#33-qualified-identifiers)). |
| **reference deck** | A deck a library designates as the source of last resort for a display string or an asset another deck does not supply. A library MAY designate one. Where none is configured, [Appendix C](#appendix-c-canonical-card-names-informative) supplies the canonical major arcana names. |
| **surrogate** | A derived, deliberately lossy stand-in for a card's artwork, such as a color palette or a [thumbhash](https://evanw.github.io/thumbhash/) ([§5.8](#58-surrogate-assets)). |
| **surrogate deck** | A deck that contains surrogate artwork and no other card assets. It records a correspondence to the artwork it stands in for, by a [`surrogate_for`](#412-surrogate_for) relation or by [`[deck.product_ids]`](#415-product-identifiers) ([§5.9](#59-surrogate-decks)). |
| **title-cased key** | The display string derived from a key where nothing else supplies one: each `_` becomes a space and the first character of each word is uppercased. |

### 1.4 Versioning and Compatibility

Every deck declares the version of this specification it is written against in `[deck].schema_version`. Its value MUST be `"<major>.<minor>"`: two decimal integers separated by a dot. The compatibility contract binds this specification, not any deck or application:

- A minor version update MUST be backward and forward compatible. It MAY add new tables, keys and values, and it MAY deprecate existing ones, but it MUST NOT change or remove the behavior of anything an earlier version of the same major version defined.
- A major version update MAY be incompatible in any respect.

`[deck].version` is the deck's own version and is unrelated to `schema_version`. It is a free-form string. This specification defines no syntax for it and no ordering over it, so applications MAY compare two values for equality to detect that a deck has changed, but MUST NOT infer from two values which is the later. A packager who wants ordered versions is expected to adopt an ordered scheme such as [semantic versioning](https://semver.org/) and to state so outside this field.

### 1.5 References

The documents below are referenced normatively unless marked informative. A dated reference applies only to the edition cited, and an undated reference applies to the latest edition.

| Reference | Title | Where used |
| --- | --- | --- |
| **Esoterica Specification** (informative) | [ESOTERICA.md](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md) | [§1.1](#11-scope-and-design-goals), [§3.1.2](#312-card-references-and-the-variant-suffix) |
| **BCP 14** | Key words for use in RFCs ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) | [§1.2](#12-document-conventions) |
| **TOML 1.0.0** | [toml.io/en/v1.0.0](https://toml.io/en/v1.0.0) | [§2.3](#23-file-format-and-encoding) |
| **.ZIP File Format Specification** | [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT) | [§2.4](#24-deck-containers) |
| **RFC 1035 §2.3.1** | Domain Names: preferred name syntax | [§3.3](#33-qualified-identifiers) |
| **RFC 5234** | Augmented BNF for Syntax Specifications: ABNF | [§3.5](#35-grammar) |
| **RFC 7405** | Case-Sensitive String Support in ABNF | [§3.5](#35-grammar) |
| **ISO 2108** | International Standard Book Number, with the freely available [ISBN Users' Manual](https://www.isbn-international.org/content/isbn-users-manual/29) | [§4.1.5](#415-product-identifiers) |
| **GS1 General Specifications** | [ref.gs1.org/standards/genspecs](https://ref.gs1.org/standards/genspecs/) | [§4.1.5](#415-product-identifiers) |
| **OARS 1.1** | Open Age Ratings Service, [specification](https://github.com/hughsie/oars/blob/master/specification/oars-1.1.md) and [attribute list](https://hughsie.github.io/oars/generate.html) | [§4.1.6](#416-content-rating) |
| **IPTC Digital Source Type** | IPTC NewsCodes [controlled vocabulary](https://cv.iptc.org/newscodes/digitalsourcetype/), also carried by [C2PA](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) | [§4.1.8](#418-artwork-origin) |
| **SAUCE** (informative) | [Standard Architecture for Universal Comment Extensions](https://www.acid.org/info/sauce/sauce.htm) | [§5.4](#54-ansi-art) |
| **CSS Color 4** | [Named colors](https://www.w3.org/TR/css-color-4/#named-colors) | [§5.8.1](#581-the-surrogate-file) |
| **ThumbHash** (informative) | [evanw.github.io/thumbhash](https://evanw.github.io/thumbhash/) | [§5.8.1](#581-the-surrogate-file) |
| **BCP 47** | Tags for Identifying Languages ([RFC 5646](https://www.rfc-editor.org/rfc/rfc5646)) | [§6.1](#61-language-tags) |
| **RFC 4647** | Matching of Language Tags | [§6.2](#62-language-resolution) |
| **SPDX License List** | [spdx.org/licenses](https://spdx.org/licenses/), with the [license expression syntax](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/) | [§7](#7-licensing-and-attribution) |
| **RightsStatements.org** | [Standardized international rights statements](https://rightsstatements.org/) | [§7.4](#74-rights-status) |
| **Spread Specification** (informative, proposed) | [SPREAD.md](https://github.com/arcanaland/specifications/blob/main/SPREAD.md) | [§1.1](#11-scope-and-design-goals) |
| **XDG Base Directory Specification** (informative) | [specifications.freedesktop.org](https://specifications.freedesktop.org/basedir-spec/latest/) | [Appendix D](#appendix-d-platform-conventions-informative) |

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

A **deck library** is an ordered list of **library roots**. Each root is a directory whose immediate children are candidate deck roots. The library is what gives a set of installed decks an order, a namespace of [directory names](#34-deck-identity) and a [reference deck](#13-terminology).

#### 2.2.1 The Library Model

How an application determines its library roots is outside the scope of this specification. An application MAY derive them from platform conventions, from its own configuration or from the user. [Appendix D](#appendix-d-platform-conventions-informative) presents conventions in use on common platforms.

An application MAY offer the user additional roots and MAY let the user reorder them. Where a library has several roots, an application SHOULD present their order to the user as meaningful, since it decides [shadowing](#223-shadowing).

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

### 2.4 Deck Containers

A deck container is a single zip file containing a deck directory. It is not a second kind of deck: an application unpacks one and reads the result under the ordinary rules of this specification.

A container:

- MUST be a ZIP archive.
- MUST carry the contents of exactly one [deck root](#13-terminology) at the root of the archive. A deck sitting inside a wrapping directory is not a container.
- MUST contain every file the deck needs to conform, in particular every file named by [`license_files`](#72-attribution-and-notices) and the [name file](#13-terminology) `default_language` names.
- SHOULD use the file extension `.tarotdeck` and the media type `application/vnd.arcana-land.tarotdeck+zip`.
- MUST use `/` as its entry-name separator, MUST write entry names in UTF-8 and MUST NOT contain an entry whose name is absolute, begins with `/`, names a drive, contains a `..`, `.` or empty segment or repeats the name of another entry.
- MUST NOT contain a symbolic link, a hard link or any entry that is neither a regular file nor a directory and MUST NOT contain an encrypted entry. Compression MUST be stored or deflate.
- SHOULD begin with an entry named `mimetype`, stored uncompressed and carrying no extra field, whose content is the ASCII string `application/vnd.arcana-land.tarotdeck+zip` with no trailing whitespace and no line break. This puts a fixed string at a fixed offset, so a container can be recognized by its content rather than by its name.

An application MUST accept a container that satisfies every rule above except the `mimetype` entry. An application that unpacks a container:

- MUST reject the whole container where any entry breaks an entry rule above and MUST NOT repair an entry name and continue. Some archive libraries repair by default, so it MUST check entry names itself rather than rely on one.
- MUST bound the total uncompressed size, the number of entries, and the ratio of uncompressed to compressed size. A ratio limit of 100:1 is RECOMMENDED: card artwork is already compressed ([§5.7.4](#574-the-extension-chain)) and comes nowhere near it, while a hostile archive exceeds it by orders of magnitude. This specification fixes no absolute limit.
- SHOULD unpack into a location it controls and SHOULD NOT unpack over an installed deck, so that a partly written directory is never [scanned](#222-scanning).
- SHOULD name the unpacked deck root from the last segment of [`[deck].identifier`](#34-deck-identity), or failing that from the container's file name without its extension; MUST make that name a single path segment carrying no separator; and MUST NOT overwrite an unrelated deck that already holds it.

The unpacked `mimetype` file is ignored by discovery ([§5.7.1](#571-image-roots)) as any other non-asset file is, and leaving it in place lets the deck be packed again unchanged.

> Note: example [shared-mime-info](https://specifications.freedesktop.org/shared-mime-info-spec/latest/) rule:
>
> ```xml
> <mime-type type="application/vnd.arcana-land.tarotdeck+zip">
>   <comment>Tarot deck</comment>
>   <glob pattern="*.tarotdeck"/>
>   <magic priority="60">
>     <match type="string" value="PK\003\004" offset="0">
>       <match type="string" value="mimetype" offset="30">
>         <match type="string"
>                value="application/vnd.arcana-land.tarotdeck+zip" offset="38"/>
>       </match>
>     </match>
>   </magic>
> </mime-type>
> ```

## 3. Identity and Identifiers

Cards are named by canonical IDs. Keys that a packager creates that differ from canonical names are called custom names. Arcana Land entities, such as decks, esoterica and spreads, are named by qualified identifiers.

### 3.1 Canonical IDs

Cards are referenced internally using canonical IDs, which are the only way this specification identifies a card:

- Major arcana: `major_arcana.00` to `major_arcana.99`, of which `00` to `21` are the canonical twenty-two
- Minor arcana: `minor_arcana.<suit>.<rank>` where:
  - `<suit>`: `wands`, `cups`, `swords`, `pentacles`
  - `<rank>`: `ace`, `two`, ..., `ten`, `page`, `knight`, `queen`, `king`

All references to cards in this specification, including configuration files, custom cards and name files, MUST use these canonical IDs.

Custom cards extend this scheme using the packager's own keys. For example: `major_arcana.happy_squirrel`, `minor_arcana.stars.ace`.

#### 3.1.1 A Canonical ID Is a Slot

A canonical ID denotes the card a deck defines at a given position, not a particular card of tradition. A. E. Waite infamously swapped the positions of Strength and Justice from the Marseille ordering. In this specification `major_arcana.08` means the major arcanum numbered eight, so a deck following the Marseille ordering simply writes Justice under `[name.card.major_arcana].08` in its name file. [Appendix C](#appendix-c-canonical-card-names-informative) publishes conventional English names for the twenty-two major arcana as a display fallback of last resort.

A deck whose extra card is not a numbered member of its sequence gives it a [custom name](#32-custom-names) instead, which denotes membership without asserting a number ([§4.3.1](#431-card-numbers)).

#### 3.1.2 Card References and the Variant Suffix

A card reference is how this specification writes a card wherever one is expected. It is a canonical ID, optionally followed by a variant suffix, which is a `:` and a variant key:

```
major_arcana.06             # a card reference
major_arcana.06:two_women   # a card reference with a variant suffix
```

A card reference with no variant suffix denotes the card's default variant. The suffix selects between different artwork of the card and does not change which card is named. `major_arcana.06:two_women` and `major_arcana.06:two_men` are the same card in the same slot with different artwork.

The suffixed form on its own is a **variant reference**. A variant is created by a file ([§5.1](#51-asset-discovery)) or by an explicit `image` path, and a variant reference is a valid key wherever a card reference is: an entry in [`[cards]`](#43-cards) supplies a variant's strings, image and content rating, and a name file's `variant` tables are keyed by it ([§6.2](#62-language-resolution)).

Variants of a card are interchangeable and carry the same meaning, so consumers of interpretive data, including the [Esoterica Specification](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md), discard the variant suffix. Variant keys are deck-wide, so an application MAY prefer a key across the whole deck.

### 3.2 Custom Names

Custom names are the keys a packager creates such as custom major arcana keys, custom suit keys, custom rank keys, card back design keys and card variant keys. Every custom name MUST match the `custom-name` production in [§3.5](#35-grammar), which allows lowercase letters, digits and underscores, but does not allow a leading digit.

Further:

- A custom name MUST NOT be one of the reserved canonical keys: `major_arcana`, `minor_arcana`, the suits `wands`, `cups`, `swords` and `pentacles`, or the ranks `ace`, `two`, `three`, `four`, `five`, `six`, `seven`, `eight`, `nine`, `ten`, `page`, `knight`, `queen` and `king`.
- A custom major arcana key additionally MUST NOT be a two-digit string.
- A custom suit key additionally MUST NOT be `name_template`.

### 3.3 Qualified Identifiers

Qualified identifiers name Arcana Land entities such as tarot decks or spreads unambiguously across authors.

- `land.arcana/deck/rider-waite-smith`
- `land.arcana/spread/celtic-cross`
- `org.example.my.domain/deck/modern-witch-tarot`

A qualified identifier is composed of a **realm** and an object **path**, separated by a slash, with an OPTIONAL **fragment** after a `#`. See [§3.5](#35-grammar) for the grammar.

- The realm is a domain name controlled by whoever mints the identifier, written in reverse order according to [RFC 1035 §2.3.1](https://www.rfc-editor.org/rfc/rfc1035#section-2.3.1). It ends at the first slash.
- The path is one or more slash-separated segments naming an entity within that realm. The first segment is the type segment and names an entity kind. The remaining segments name the entity within that kind and their structure is the realm holder's to choose. A deck's type segment MUST be `deck`.
- The fragment names a target within that entity, and its meaning is the prerogative of whichever specification owns the entity. In this specification, the fragment of a deck's qualified identifier is a [card reference](#312-card-references-and-the-variant-suffix). For example, `land.arcana/deck/rider-waite-smith#major_arcana.00` refers to globally unique entity of "The Fool."

Realms are compared bytewise. Qualified identifiers are not locations and nothing in this specification implies that one can be fetched.

A realm asserts control of a name, not authorship of the work it names. A packager MAY delegate a subdomain to separate the entities they originate from the ones they package, so a packager at `example.org` might mint `org.example/deck/their-own-deck` for their own work and `org.example.shelf/deck/some-published-deck` for a deck they package.

The type segments this specification allows:

| Type segment | Names | Owning specification |
| --- | --- | --- |
| `deck` | A tarot deck | This specification |
| `spread` | A spread | Spread specification (not yet published) |
| `esoterica` | An esoterica document | Tarot Esoterica Specification |

The registry is open on the same terms as the [link relations](#411-links) of §4.1.1: an application MUST ignore an identifier whose type segment it does not recognize and MUST NOT treat one as an error. A later version of this or another Arcana Land specification MAY add to the registry, so a realm holder naming a kind of entity no specification defines SHOULD prefix the segment, as in `x-collection-notes`. Note that the prefix is `x-` and not the `x_` used elsewhere: a path segment admits `-` and not `_` ([§3.5](#35-grammar)), while a [custom name](#32-custom-names) admits `_` and not `-`.

A qualified identifier is essentially a URI without the scheme, and Arcana Land reserves the scheme `tarot:` for the form `tarot:land.arcana/deck/inclusive-tarot#major_arcana.06:two_women`. No version of this specification defines that scheme and nothing in this document depends on it. It is recorded here for downstream implementation awareness.

### 3.4 Deck Identity

A deck has three distinct properties related to identity:

| Property | Location | Description | Uniqueness |
| --- | --- | --- | --- |
| `name` | `[deck].name`, REQUIRED | Display string shown to the user | Two unrelated decks can share a name |
| `identifier` | `[deck].identifier`, RECOMMENDED | The deck's [qualified identifier](#33-qualified-identifiers) | Globally |
| Directory name | The filesystem | Library-scoped handle | Unique within a library root |

The three are independent. A directory name is not required to match `[deck].name` nor the last segment of `[deck].identifier`. An application MUST NOT require them to agree and a validator MUST NOT report a disagreement.

An `identifier` names the deck as a whole and MUST NOT carry a fragment.

An identifier names the deck across all of its versions. A packager who reissues a deck MUST NOT change its `identifier` on account of the new `[deck].version`, and MUST mint a new identifier where the package has become a different deck rather than a new version of the same one.

A deck SHOULD provide an `identifier`, since a deck without one cannot be referenced from another Arcana Land document. Applications and validators MUST NOT synthesize one for a deck that lacks it. Two decks in one library MAY declare the same `identifier` under different directory names, although a validator warns about it.

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
segment         = segment-char [ *( segment-char / "-" ) segment-char ]
segment-char    = lcalpha / DIGIT

fragment        = 1*fragment-char
fragment-char   = lcalpha / DIGIT / "." / "_" / "-" / ":"

; ---- Dates ------------------------------------------------------------

published-date  = year [ "-" month [ "-" day ] ]
year            = 4DIGIT
month           = 2DIGIT
day             = 2DIGIT

; ---- Terminals --------------------------------------------------------

lcalpha         = %x61-7A               ; a-z
DIGIT           = %x30-39               ; 0-9, from RFC 5234 Appendix B.1
```

Three constraints are not expressible in the grammar and are stated normatively:

- `canonical-major` admits any two digits, but only `00` through `21` have a name in [Appendix C](#appendix-c-canonical-card-names-informative) or any meaning shared between decks ([§3.1.1](#311-a-canonical-id-is-a-slot)). A key MUST be written with both digits.
- A `custom-name` MUST NOT be a name reserved by [§3.2](#32-custom-names), with the one exception in [§4.4](#44-suits).
- `published-date` admits any `month` and `day` digits, but a value MUST denote a real calendar date in the proleptic Gregorian calendar ([§4.1](#41-deck)).

### 3.6 Identifiers in TOML

A [canonical ID](#31-canonical-ids) is a compound, which, when used in TOML as a key, has a few considerations:

- Where a document attaches a record to a single card, the identifier is written as a single TOML key. For example, in `[cards."minor_arcana.wands.ace"]` the table `cards` has one key whose text is `minor_arcana.wands.ace`.
- Where a document generalizes over cards, so that a prefix names a group, the identifier is written as a key path. A name file's `[minor_arcana.wands]` names every card of that suit and the rank key beneath it completes the identifier.
- A [card reference](#312-card-references-and-the-variant-suffix) with a variant suffix is always a single key.

| Site | Form |
| --- | --- |
| [`[cards."<card-ref>"]`](#43-cards) | Single key |
| [`[app."<realm>"]`](#8-extensibility) | Single key |
| A name file's `[name.variant]` and `[alt_text.variant]` ([§6.2](#62-language-resolution)) | Single key, a variant reference |
| A name file's `[<facet>.card.major_arcana]` and `[<facet>.card.minor_arcana.<suit>]` | Key path |
| [`[suits.<key>]`](#44-suits) | Key path |

## 4. deck.toml Reference

Every table this specification defines is listed below with its fields.

A key not listed here and not under `[app]` is not defined by this specification, and [§8](#8-extensibility) reserves such names for future versions of it.

### 4.1 `[deck]`

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `schema_version` | String | **Yes** | n/a | The version of this specification the deck is written against as `"<major>.<minor>"` |
| `name` | String | **Yes** | n/a | The deck's display name. Not required to be unique, and not required to match the directory name ([§3.4](#34-deck-identity)). |
| `version` | String | **Yes** | n/a | The deck's own free-form version. |
| `identifier` | String | RECOMMENDED | none | The deck's qualified identifier ([§3.3](#33-qualified-identifiers)). A deck without one cannot be referenced from another Arcana Land document ([§3.4](#34-deck-identity)). |
| `related` | Array of Table | No | `[]` | Other decks this deck stands in a stated relation to, each saying what that relation is ([§4.1.9](#419-related-decks)). |
| `pips` | String | No | `"unstated"` | Whether the deck's numbered minor arcana depict scenes ([§4.1.4](#414-pips)). |
| `default_language` | String | No | `"en"` | BCP 47 tag of the deck's default name file ([§6.2](#62-language-resolution)). |
| `metadata_language` | String | No | the value of `default_language` | BCP 47 tag of the language the package is in ([§6.1](#61-language-tags)). |
| `artwork_language` | Array of String | No | none | BCP 47 tags of the languages of text printed on the deck's artwork, in no significant order ([§6.1](#61-language-tags)). Informative only. |
| `icon` | String (path) | No | none | A preview image for the deck, assumed to share the cards' aspect ratio. |
| `aspect_ratio` | Float | No | `0.5789` | Width ÷ height of the deck's cards. |
| `card_size_mm` | Array of two Floats | No | none | The physical card's width and height in millimetres, in that order, where the deck has a physical printing ([§5.6](#56-aspect-ratio)). |
| `creator` | String | No | none | Who devised the deck, where that is not who drew it ([§7.6](#76-roles-and-credits)). |
| `artist` | String | No | none | Who made the deck's artwork ([§7.6](#76-roles-and-credits)). |
| `packager` | String | No | none | Whoever assembled this package, where that is not the artist ([§7.6](#76-roles-and-credits)). |
| `description` | String | No | none | A prose description of the deck written once in `metadata_language` ([§6.4](#64-alt-text-guidelines)). |
| `license` | String | No | none | SPDX license expression governing the card assets this package carries ([§7.1](#71-license-expressions)). |
| `license_files` | Array of String (path) | No | `[]` | Full license texts and notices carried in the deck ([§7.2](#72-attribution-and-notices)). |
| `copyright` | String | No | none | Copyright notice, displayed verbatim. |
| `attribution` | String | No | none | Credit line to display ([§7.2](#72-attribution-and-notices)). |
| `rights_status` | String (URI) | No | none | The artwork's copyright *status*, as distinct from any license granted over it ([§7.4](#74-rights-status)). |
| `redistribution` | String | No | `"unstated"` | Whether the packager passes on the artwork for republication ([§7.5](#75-redistribution-and-derivation)). |
| `derivation` | String | No | `"unstated"` | Whether the packager passes on the artwork for making derived works ([§7.5](#75-redistribution-and-derivation)). |
| `published_date` | String | No | none | When the deck this package reproduces was published, at the precision the packager has ([§4.1.7](#417-published-date)). |
| `publisher` | String | No | none | The deck's publisher. |
| `product_ids` | Table | No | none | External identifiers for the commercial product this deck reproduces such as an ISBN ([§4.1.5](#415-product-identifiers)). |
| `content_rating` | Table | No | none | What the deck's artwork depicts, keyed by rating system ([§4.1.6](#416-content-rating)). |
| `origin` | Table | No | none | How the deck's artwork came to exist (e.g., AI generated), keyed by vocabulary system ([§4.1.8](#418-artwork-origin)). |
| `links` | Array of Table | No | `[]` | The deck's web addresses, each saying what it points at ([§4.1.1](#411-links)). |
| `tags` | Array of String | No | `[]` | Free-vocabulary categorization tags. This specification defines no registry of tag values and attaches no behavior to any of them. |

```toml
[deck]
schema_version = "2.0"
name = "Rider-Waite-Smith Tarot"
version = "1.0"
identifier = "land.arcana/deck/rider-waite-smith"
creator = "A. E. Waite"
artist = "Pamela Colman Smith"
icon = "deck-icon.png"
license = "CC0-1.0"
license_files = ["LICENSE"]
published_date = "1909-12"
tags = ["traditional", "classic"]
```

#### 4.1.1 Links

`[deck].links` holds the deck's web addresses. A deck MAY declare any number, including several sharing a `rel`. Each entry is a table:

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `rel` | String | **Yes** | n/a | What the target is, from the registry below. MUST be a [custom name](#32-custom-names). |
| `url` | String (URI) | **Yes** | n/a | An absolute URL with a scheme of `http` or `https`. |
| `title` | String | No | none | A label for the link, in the deck's [`metadata_language`](#41-deck). |

The registry:

| `rel` | The target is |
| --- | --- |
| `homepage` | The deck's own page |
| `buy` | Somewhere a reader can obtain the physical or digital deck |
| `artist` | The artist, illustrator or creator of the artwork |
| `publisher` | The publisher named in `[deck].publisher` |
| `source` | Where the deck's assets were obtained, such as an archive or a scan repository |

```toml
[deck]
name = "The Example Tarot"
links = [
  { rel = "buy", url = "https://example.com/shop/the-deck", title = "Buy from the artist" },
  { rel = "artist", url = "https://example.com/about" },
]
publisher = "Example Press"
```

The registry is open. An application MUST ignore a link whose `rel` it does not recognize, and MUST NOT treat an unrecognized `rel` as an error. A future version of this specification MAY add to the registry, so a packager who needs a relation it does not define SHOULD prefix it, as in `x_kickstarter`, to avoid colliding with a later addition.

#### 4.1.2 `surrogate_for`

A `surrogate_for` [relation](#419-related-decks) names another deck whose artwork this package describes but does not carry. It is the one relation in the registry that asserts the two packages are the same deck. It functions as a merge key: an application holding both presents them as one deck and prefers the artwork over the surrogate ([§5.9](#59-surrogate-decks)).

```toml
[deck]
name = "The Example Tarot"
identifier = "net.example.jdoe/deck/example-tarot-surrogate"
related = [
  { rel = "surrogate_for", deck = "com.example/deck/example-tarot" },
]
```

Rules, in addition to those every relation carries ([§4.1.9](#419-related-decks)):

- The value MUST be the `[deck].identifier` of the package it stands in for, so that it can serve as a merge key.
- A deck MUST NOT declare more than one `surrogate_for` relation. A package cannot stand in for two different decks.
- The relation names a package. Where the artwork belongs to a commercial product that no one has packaged, there is no value for this relation and [`[deck.product_ids]`](#415-product-identifiers) records the correspondence instead ([§5.9](#59-surrogate-decks)).
- `surrogate_for` is a [recognized relation](#419-related-decks): an application that does not implement it MUST NOT present the package as an ordinary deck.

Until 2.0 this relation was the flat key `[deck].signifies`, named from the tarot significator ([Appendix B](#appendix-b-reserved-and-deprecated-names)). The current name is *surrogate record*, the cataloguing term for a structured description standing in for an item the catalogue does not hold, which is what [§5.8](#58-surrogate-assets) and [§5.9](#59-surrogate-decks) call the thing throughout.

#### 4.1.3 `follows`

A `follows` [relation](#419-related-decks) names the deck whose structure and iconography this deck is patterned on. Most tarot decks published in the last fifty years are patterned on another deck (usually Rider-Waite-Smith). It allows an application to tell whether borrowing from a [reference deck](#13-terminology) is safe ([§5.7.6](#576-when-no-asset-is-found)).

```toml
[deck]
name = "My Example Tarot"
identifier = "com.example/deck/example-tarot"
related = [
  { rel = "follows", deck = "land.arcana/deck/rider-waite-smith" },
]
```

> Note: this example uses `land.arcana/deck/rider-waite-smith` as the globally-unique qualified identifier for the traditional Rider-Waite-Smith. This specification assigns no specific meaning to this string, but you are free to use this identifier to describe "the thing that we all commonly refer to as the normal RWS deck."

Rules, in addition to those every relation carries ([§4.1.9](#419-related-decks)):

- A deck MUST NOT declare more than one `follows` relation. [§5.7.6](#576-when-no-asset-is-found)'s lineage condition compares a deck against one pattern and this specification defines no ordering over several.
- `follows` carries no merge semantics, in contrast to `rel = "surrogate_for"` ([§4.1.2](#412-surrogate_for), [§5.9](#59-surrogate-decks)); an application MUST NOT treat the two decks as one.
- `follows` is not a rights claim. It asserts solely a resemblance in structure and iconography, grants and implies no permission, and does not exempt a deck from [§7.7](#77-deck-names-and-trademarks)'s prohibition on implying endorsement. Rights are stated in [§7](#7-licensing-and-attribution).
- Following is not transitive for any purpose this specification defines.

#### 4.1.4 `pips`

`[deck].pips` states whether the deck's numbered minor arcana depict scenes:

| Value | Meaning |
| --- | --- |
| `"scenic"` | The numbered minors depict scenes. |
| `"emblematic"` | The numbered minors are arrangements of the suit's signs, as in the Marseille pattern. |
| `"unstated"` | The default. The packager has not said. |

Rules:

- The field describes the numbered minors `two` through `ten` in every suit the deck has. Aces are conventionally a single emblem of the suit in every tradition, so they are not described by it, and neither are the courts or the major arcana.
- The default is `"unstated"` and an application MUST NOT read it as either of the other two.
- A deck whose suits differ among themselves SHOULD declare nothing. There is no value meaning "mixed", so such a deck is indistinguishable from one that has not said — which is the intent, since neither can be borrowed against.

#### 4.1.5 Product Identifiers

`[deck.product_ids]` records the product identifiers a published commercial deck carries. It is a table whose keys name identifier schemes and whose values are strings.

```toml
[deck]
name = "The Example Tarot"
publisher = "Example Press"

[deck.product_ids]
isbn = "9789999999991"
gtin = "00201234567899"
publisher_sku = "EXT-078"
```

The registry:

| Scheme | The value is |
| --- | --- |
| `isbn` | An International Standard Book Number |
| `gtin` | A GTIN, the family that subsumes the UPC and the EAN |
| `publisher_sku` | The publisher's own item or catalog number |

A product identifier does not replace the deck's own identity within Arcana Land [`[deck].identifier`](#34-deck-identity).

An application MAY treat two packages that declare an equal value for the same scheme as describing the same product, and where it does, it SHOULD prefer the package carrying the artwork. Two values are equal when they are equal after the normalization their scheme's rule below defines; an application comparing values MUST apply that normalization first, and MUST NOT compare values across schemes.

Inequality is not evidence of difference. A product identifier names a printing rather than a work, so two printings of the same artwork — a publisher's edition for another territory, a reissue, a boxed set — carry different identifiers, and a deck sold without one carries none at all. An application MUST NOT read an absent or differing identifier as a claim that two packages are unrelated.

Rules:

- Every key MUST be a [custom name](#32-custom-names) and every value MUST be a non-empty string.
- An `isbn` value is written as an ISBN-13 or an ISBN-10, in which hyphens and spaces are OPTIONAL. Applications comparing two values MUST first remove hyphens and spaces and uppercase a trailing `x`.
- A `gtin` value is written as digits alone and SHOULD be zero-padded to fourteen digits. Applications comparing two values MUST first zero-pad each to fourteen digits, so that a UPC written as twelve digits matches the same UPC written as fourteen.
- A `publisher_sku` value is opaque and is unique only within one publisher, so two publishers' numbers can collide. An application MUST NOT use it as evidence that two packages describe the same product.

The registry is open on the same terms as the [link relations](#411-links) of §4.1.1: an application MUST ignore a scheme it does not recognize and MUST NOT treat one as an error, and a packager who needs a scheme this specification does not define SHOULD prefix it with `x_`.

#### 4.1.6 Content Rating

`[deck.content_rating]` states what the deck's artwork depicts in a named rating system. It is a table of tables where each subtable key names a rating system. The subtable contains that system's descriptors as key-value pairs.

```toml
[deck.content_rating."oars-1.1"]
sex_nudity = "mild"
violence_fantasy = "mild"
violence_bloodshed = "mild"
```

A deck MAY declare more than one system. Nothing requires the declarations to agree and this specification defines no mapping between systems.

The registry:

| System | Descriptors are |
| --- | --- |
| `oars-1.1` | The attribute ids of OARS 1.1, each `-` written as `_`, valued `none`, `mild`, `moderate` or `intense` |

The registry is open on the same terms as the [link relations](#411-links) of §4.1.1: an application MUST ignore a system it does not recognize and MUST NOT treat one as an error, and a packager who needs a system this specification does not define SHOULD prefix it with `x_`.

`oars-1.1` names version 1.1 of the [Open Age Ratings Service](https://hughsie.github.io/oars/) vocabulary, whose descriptor keys are its twenty-two attribute ids: `sex_nudity`, `sex_themes`, `violence_cartoon`, `violence_fantasy`, `violence_realistic`, `violence_bloodshed`, `violence_desecration`, `violence_slavery`, `violence_sexual`, `drugs_alcohol`, `drugs_narcotics`, `drugs_tobacco`, `language_profanity`, `language_humor`, `language_discrimination`, `money_advertising`, `money_gambling`, `money_purchasing`, `social_chat`, `social_audio`, `social_contacts`, `social_info` and `social_location`. The underscore rewriting keeps every key a [custom name](#32-custom-names) and is reversed mechanically where an application emits OARS.

Most of those attributes are reachable for a deck. Seven are out of scope because they describe application capabilities: `social_chat`, `social_audio`, `social_contacts`, `social_info`, `social_location`, `money_purchasing` and `money_advertising`. They remain legal to maintain compatibility.

An absent `[deck.content_rating]` means the packager has not declared a rating and an application MUST NOT read it as `none`.

Within a declared system subtable, an omitted descriptor is `none` for that system. For example, `[deck.content_rating."oars-1.1"]` with no descriptors communicates that this deck was reviewed and contains nothing the system describes. A deck that annotates its artwork states the same thing a second way, described under per-artwork descriptors below.

**Per-artwork descriptors.** A card carries the same table under its [`[cards]`](#43-cards) entry, a [variant](#312-card-references-and-the-variant-suffix) under its own entry in the same table, and a [card back design](#42-card_backs) under `[card_backs.designs.<key>]`:

```toml
[cards."major_arcana.06"]
content_rating = { "oars-1.1" = { sex_nudity = "mild" } }

[cards."minor_arcana.swords.ten".content_rating."oars-1.1"]
violence_bloodshed = "mild"
```

Rules:

- A descriptor declared on an [artwork](#13-terminology) MUST be written under a system the deck also declares in `[deck.content_rating]`.
- A value declared on an artwork MUST NOT exceed the deck-level value **declared** for the same system and descriptor. For OARS, descriptor values are ordered `none` < `mild` < `moderate` < `intense`. A descriptor the deck-level subtable omits constrains nothing under `artwork_complete = true`, since it is derived from the artwork, and is `none` otherwise. The rule binds only a system whose ordering this specification defines, which is `oars-1.1` alone.
- Where any artwork declares a descriptor for a system, that system's subtable in `[deck.content_rating]` MUST carry the boolean key `artwork_complete`, which says whether the annotation covers the whole deck. It is reserved in every system subtable and is never a descriptor; a descriptor is always a string, so the two never collide.
  - `artwork_complete = true` states that every artwork the deck ships depicting anything the system describes carries an entry, so an artwork with no entry is `none` for that system. The deck-level value of a descriptor the subtable omits is then **the greatest value any artwork declares for it**, and this is the one case in which an omitted deck-level descriptor does not assert `none`.
  - `artwork_complete = false` states that artwork was annotated where the packager saw a reason to. An artwork with no entry is unstated, an application MUST NOT read it as `none`, and where it needs a value it SHOULD use the deck-level one.
- There is no default. A deck that annotates no artwork says nothing about coverage and SHOULD omit the key.
- A card's value describes that card's **default artwork**, which is what a [bare card reference](#312-card-references-and-the-variant-suffix) denotes. It is not a ceiling over the card's other artwork: a card whose default artwork depicts nothing the system describes MAY carry a variant that depicts something, and each states its own value.
- A [variant](#312-card-references-and-the-variant-suffix) is rated under its own [`[cards]`](#43-cards) entry, on the same terms. A variant declaring no subtable for a system takes its card's value for that system, so a card-level descriptor covers every variant the deck does not rate separately. Within a variant's *declared* subtable an omitted descriptor is `none`, as anywhere else, so a variant that depicts nothing the system describes declares that subtable empty rather than inheriting its card's value.
- A [card back design](#42-card_backs) is rated under its own `[card_backs.designs.<key>]` entry, on the same terms. A back belongs to no card and so inherits nothing: one that declares no subtable for a system is `none` under `artwork_complete = true` and unstated otherwise, like any other artwork.
- `artwork_complete` needs no entry for artwork that resolves to another. A variant that declares nothing resolves to its card, which a complete card annotation already accounts for.
- A descriptor covers the deck's own assets. Where an application [borrows a card](#576-when-no-asset-is-found) from a reference deck, it SHOULD take the descriptor of whichever deck supplied the image.

A deck reviewed card by card:

```toml
[deck.content_rating."oars-1.1"]
artwork_complete = true

[cards."major_arcana.06".content_rating."oars-1.1"]
sex_nudity = "mild"

[cards."major_arcana.15".content_rating."oars-1.1"]
sex_nudity = "mild"

[cards."major_arcana.16".content_rating."oars-1.1"]
violence_fantasy = "mild"

[cards."major_arcana.17".content_rating."oars-1.1"]
sex_nudity = "mild"

[cards."major_arcana.20".content_rating."oars-1.1"]
sex_nudity = "mild"

[cards."major_arcana.21".content_rating."oars-1.1"]
sex_nudity = "mild"

[cards."minor_arcana.swords.ten".content_rating."oars-1.1"]
violence_bloodshed = "mild"
```

The seventy-one cards with no entry are `none`, and the deck as a whole is `sex_nudity = "mild"`, `violence_fantasy = "mild"` and `violence_bloodshed = "mild"` without those values appearing anywhere in the file. A deck MAY declare them at deck level as well, and one that does MUST NOT declare a value below what its artwork carries.

In a different deck, one whose default Lovers artwork is clothed and which ships a nude alternate beside it, each artwork states its own value and the card's describes what a bare `major_arcana.06` shows:

```toml
[cards."major_arcana.06".content_rating."oars-1.1"]
# the default artwork, reviewed and depicting nothing this system describes

[cards."major_arcana.06:two_women".content_rating."oars-1.1"]
sex_nudity = "mild"
```

`major_arcana.06:two_men`, declaring nothing, takes `none` from its card. An application filtering at card granularity shows The Lovers, because the artwork it would show depicts nothing the system describes; one that offers the `two_women` variant reads that variant's own value before showing it.

A deck whose only rated artwork is a card back says so where the back is declared, and needs no card entries at all:

```toml
[deck.content_rating."oars-1.1"]
artwork_complete = true

[card_backs.designs.classic.content_rating."oars-1.1"]
sex_nudity = "mild"
```

#### 4.1.7 Published Date

`[deck].published_date` records when the deck was published: the date printed on a physical deck's box or in its accompanying material, or the date a digital deck was first released. It describes the work, not this package. The package's own revisions are what [`[deck].version`](#41-deck) tracks.

The value is a `published-date` ([§3.5](#35-grammar)) — a year, a year and month, or a full date. `"1909"` where the year is all that is known, `"1909-12"` where the month is on record, `"2018-10-16"` where the day is.

A packager MUST NOT state a precision they do not have. Where only the year is known, the year alone is the correct value; padding it to `1909-01-01` asserts a day nobody knows.

`published_date` is a TOML string. TOML's native types MUST NOT be used for it: unquoted, `1909-12-01` reads as a local date and `1909` reads as an integer ([§9.4](#94-validation-rules)).

#### 4.1.8 Artwork Origin

`[deck.origin]` states how the deck's [artwork](#13-terminology) came to exist, in a named vocabulary. It is a table whose keys name vocabulary systems and whose values are terms of that system.

```toml
[deck.origin]
"iptc-dst" = "print"
```

The registry:

| System | Values are |
| --- | --- |
| `iptc-dst` | Term names of the IPTC Digital Source Type NewsCodes vocabulary |

The registry is open on the same terms as the [link relations](#411-links) of §4.1.1: an application MUST ignore a system it does not recognize and MUST NOT treat one as an error, and a packager who needs a system this specification does not define SHOULD prefix it with `x_`.

`iptc-dst` names the [IPTC Digital Source Type](https://cv.iptc.org/newscodes/digitalsourcetype/) vocabulary adopted whole. Terms are written verbatim to maintain interoperability.

The terms a packager may reach for, informatively:

| If the artwork... | Term |
| --- | --- |
| ...was scanned from physical cards | `print` |
| ...was photographed | `digitalCapture` |
| ...was drawn or painted with non-generative tools | `digitalCreation` |
| ...was produced by an algorithm not trained on sampled content | `algorithmicMedia` |
| ...was made one way and then altered by a generative model | `compositeWithTrainedAlgorithmicMedia` |
| ...was generated by a trained model | `trainedAlgorithmicMedia` |

Declare the term describing how the artwork principally came to exist. Where a later operation changed what the image depicts, declare the term for that operation instead. Routine preparation tasks such as deskewing, cropping, dust removal and color correction do not change the term.

An absent `origin` means the packager gave no value and an application MUST NOT read it as an assertion that the artwork is human-made.

**Per-artwork origin.** A card carries the same table under its [`[cards]`](#43-cards) entry, a [variant](#312-card-references-and-the-variant-suffix) under its own entry in the same table, and a [card back design](#42-card_backs) under `[card_backs.designs.<key>]`:

```toml
[deck.origin]
"iptc-dst" = "print"                 # scanned from the physical cards

[cards."major_arcana.13"]
origin = { "iptc-dst" = "compositeWithTrainedAlgorithmicMedia" }   # water damage repaired

[card_backs.designs.classic.origin]
"iptc-dst" = "digitalCreation"
```

Rules:

- Every key MUST be a [custom name](#32-custom-names) and every value MUST be a non-empty string.
- An origin declared on an [artwork](#13-terminology) MUST be written under a system the deck also declares in `[deck.origin]`.
- A card that declares no value takes the deck's value. A [variant](#312-card-references-and-the-variant-suffix) that declares no value for a system takes its card's value. A [card back design](#42-card_backs) that declares no value takes the deck's value.
- The deck-level value is the default for any artwork that does not state its own.
- A deck whose artwork did not all come to exist the same way SHOULD annotate the exceptions.

Unlike a [content rating](#416-content-rating), there is no coverage flag and no ordering.

#### 4.1.9 Related Decks

`[deck].related` contains this deck's outbound references to other decks. A deck MAY declare any number, including several sharing a `rel` and several naming the same deck under different `rel`s, except where a relation's own section bounds it. Each entry is a table:

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `rel` | String | **Yes** | n/a | What the target is, from the registry below. MUST be a [custom name](#32-custom-names). |
| `deck` | String | **Yes** | n/a | The [qualified identifier](#33-qualified-identifiers) of the related deck. |
| `title` | String | No | none | A label, in the deck's [`metadata_language`](#41-deck). |

The registry:

| `rel` | The target is | Recognition |
| --- | --- | --- |
| `follows` | The deck whose structure and iconography this deck is patterned on ([§4.1.3](#413-follows)) | Advisory |
| `surrogate_for` | The deck whose artwork this package describes and does not carry; a merge key ([§4.1.2](#412-surrogate_for)) | **Recognized** |
| `expands` | The deck this package adds cards to. The package is not a standalone deck ([§5.7.6](#576-when-no-asset-is-found)) | **Recognized** |
| `companion` | A deck this one was published to be used alongside. The relation is self-inverse and carries no behavior | Advisory |

```toml
[deck]
schema_version = "2.0"
name = "Prisma Visions Extra Majors"
identifier = "com.example/deck/example-tarot-extra-majors"
version = "0.1"
related = [
  { rel = "expands", deck = "com.example/deck/example-tarot" },
]
```

Rules:

- The value of `deck` MUST be a well-formed qualified identifier naming a deck: it MUST NOT carry a fragment and is neither a [card reference nor a variant reference](#312-card-references-and-the-variant-suffix).
- It MUST NOT equal this deck's own `identifier`. A deck stands in no relation to itself.
- No deck may name the same target under both `follows` and `surrogate_for`. A deck that stands in for another is that deck; it does not also resemble it.
- **Relations are not reciprocated.** The dependent package carries the pointer and the target says nothing back. A deck is never edited because another deck came to name it.
- Nothing resolves a qualified identifier ([§3.3](#33-qualified-identifiers)), so a validator checks that the value is well formed and no more. A relation to a deck nobody has packaged is legal.

**Recognition.** The registry is open for **advisory** relations on [§4.1.1](#411-links)'s terms: an application MUST ignore an advisory `rel` it does not recognize and MUST NOT treat one as an error, and a packager who needs a relation this specification does not define SHOULD prefix it, as in `x_kickstarter`.

A **recognized** relation is different in kind, because it governs what the package *is* rather than what it points at. A package declaring one is not a deck an application may render on its own terms: a surrogate deck holds no artwork ([§5.8](#58-surrogate-assets)) and an expansion holds a handful of cards out of seventy-eight. An application that does not implement a recognized `rel` MUST NOT present the package as though the relation were absent. It SHOULD tell the user it cannot fully render the package, and it MUST NOT complete the package's canonical cards from a [reference deck](#13-terminology) ([§5.7.6](#576-when-no-asset-is-found)).

**The set of recognized relations is closed within a major version.** A minor version MAY add advisory relations and MUST NOT add recognized ones, since an application written against an earlier minor version cannot know to withhold a rendering for a name it has never heard of ([§1.4](#14-versioning-and-compatibility)). An application conforming to this version therefore knows the whole of the recognized set, and any `rel` outside it is advisory.

### 4.2 `[card_backs]`

A card back design is one of the back images a deck ships, named by a design key. Designs are [discovered from the directory structure](#55-card-back-images) exactly as cards are, so a deck that contains an image `card_backs/classic.png` has a design keyed `classic` and need declare nothing at all. The whole of `[card_backs]` is OPTIONAL.

```toml
[card_backs]
default = "classic"

[card_backs.designs.classic]
name = "Classic RWS Back"
description = "The 1909 Rider back, reproduced from the Pamela Colman Smith printing."
alt_text = "A lattice of blue and white roses and lilies, edge to edge, with no border."
reversible = true
```

**`[card_backs]`**

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `default` | String | No | see below | The design key an application uses where the user has not chosen another. Where present it MUST name a design the deck has ([§9.4](#94-validation-rules)). |

Where a deck has no card back at all, an application supplies its own. Otherwise the default design is the first of these that applies: the design named by `[card_backs].default`, then the design keyed `default` where the deck has one, then the lexicographically first design key.

**`[card_backs.designs.<key>]`** takes a [custom name](#32-custom-names) as the design key. The table is OPTIONAL for every design.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | resolved per [§6.3](#63-display-name-resolution) | Fallback display name for this design, used where no name file supplies one. |
| `description` | String | No | none | Prose *about* the design, such as its provenance or history, for display alongside the back in a picker or an info panel. Not localized: it is the packager's own statement about where the design came from rather than a display string belonging to the artwork, and a translation would restate someone's factual claim in words they did not write. It is written once in the deck's [`metadata_language`](#41-deck). See [§6.4](#64-alt-text-guidelines). |
| `alt_text` | String | No | none | Fallback alt text describing what the back looks like. A name file's `[alt_text.card_back]` takes precedence and is where a deck SHOULD put it ([§6.3](#63-display-name-resolution)). |
| `inscription` | String or Array of String | No | none | Text printed on this design other than its name ([§4.3.3](#433-inscriptions)). Not localized. |
| `content_rating` | Table | No | none | What this back design depicts, keyed by rating system, on the terms in [§4.1.6](#416-content-rating). |
| `origin` | Table | No | the deck's | How this back design came to exist, keyed by vocabulary system, on the terms in [§4.1.8](#418-artwork-origin). |
| `reversible` | Boolean | No | unstated | Whether the design looks the same turned 180°, so that a card lying face down does not reveal which way round it is. See below. |
| `image` | String (path) | No | found by discovery | An explicit path to this design's image, for a file that does not follow the naming convention or uses a format outside the extension chain ([§5.7.4](#574-the-extension-chain)). |

**`reversible`** is a statement about the artwork and not about card meanings, which this specification does not model. A back with a border that differs top from bottom, or with an image that stands the right way up, is not reversible, and an application that draws such a back at a card's own orientation makes a face-down card legible as one turned around. Absence is a third state distinct from either value: the packager has not said, and an application MUST NOT assume an answer. No validator can check the claim, because a scan of a reversible design differs from its own rotation by misregistration and press variation alone, by more than a directional design on pale stock differs from its; [§9.4](#94-validation-rules) therefore checks the type and nothing further.

Declaring a design under `[card_backs.designs]` does not create it. A design the deck has no file for and no `image` path to is a [resolution failure](#576-when-no-asset-is-found) rather than a validation error.

### 4.3 `[cards]`

Cards are [discovered from the directory structure](#51-asset-discovery) so the `[cards]` table supplies what is not available from the filename alone, such as the card's printed number, its place in the deck's sequence and fallback display strings. It is OPTIONAL in its entirety. A card's [variants](#312-card-references-and-the-variant-suffix) are entries in the same table, keyed by a variant reference.

```toml
[cards."major_arcana.23"]
number = "XXIII"

[cards."major_arcana.happy_squirrel"]
name = "The Happy Squirrel"
alt_text = "A cheerful squirrel standing on a branch proudly holding an acorn."
position = 22

[cards."major_arcana.06"]
default_variant = "two_women"

[cards."major_arcana.06:two_women"]
name = "The Lovers"
alt_text = "Two women stand hand in hand beneath a winged figure."
image = "scalable/major_arcana/06.two_women.svg"
```

**`[cards."<card-ref>"]`** takes a [card reference](#312-card-references-and-the-variant-suffix) as the table key, quoted because it contains dots. The key is a [canonical ID](#31-canonical-ids) such as `"major_arcana.06"`, naming the card, or a [variant reference](#312-card-references-and-the-variant-suffix) such as `"major_arcana.06:two_women"`, naming one of that card's variants. The two are disjoint: a variant reference contains a colon and a canonical ID cannot.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | resolved per [§6.3](#63-display-name-resolution) | Fallback display name, used where no name file supplies one. |
| `alt_text` | String | No | none | Fallback alt text, used where no name file supplies one. |
| `number` | String | No | see [§4.3.1](#431-card-numbers) | The number printed on the card's face. |
| `unnumbered` | Boolean | No | `false` | The card's face carries no number, whatever its key shape implies ([§4.3.1](#431-card-numbers)). Display only and does not affect ordering ([§4.3.2](#432-ordering)). |
| `unnamed` | Boolean | No | `false` | The card's face carries no name. Truncates display name resolution ([§6.3](#63-display-name-resolution)). |
| `inscription` | String or Array of String | No | none | Text printed on this card's artwork other than its name and its number ([§4.3.3](#433-inscriptions)). Not localized. |
| `position` | Integer | No | see [§4.3.2](#432-ordering) | Where the card sits in the deck's sequence. Major arcana only. |
| `content_rating` | Table | No | none | What this card depicts, keyed by rating system, on the terms in [§4.1.6](#416-content-rating). |
| `origin` | Table | No | the deck's | How this card's artwork came to exist, keyed by vocabulary system, on the terms in [§4.1.8](#418-artwork-origin). |
| `image` | String (path) | No | found by discovery | An explicit path to this card's image, for a file that does not follow the naming convention or uses a format outside the extension chain ([§5.7.4](#574-the-extension-chain)). |
| `default_variant` | String | Required where the card has variant files but no unsuffixed file | the unsuffixed file | Which variant a bare canonical ID resolves to ([§5.7.5](#575-variants)). MUST name a variant of this card ([§9.4](#94-validation-rules)). |

`name` and `alt_text` are the deck's own strings. Where a deck's card names are printed on the artwork a deck SHOULD declare them here, and reserve `names/<tag>.toml` for strings addressed to a reader of a particular language ([§6.2](#62-language-resolution)). Where a deck's names are the packager's own words, a deck SHOULD carry them in a name file, where they can be localized ([§6.3](#63-display-name-resolution)).

An entry for a canonical minor arcanum or for `major_arcana.00` through `major_arcana.21` is always accepted, since those slots exist for every deck. An entry for any other card, and an entry for any variant, is an error unless the deck has files for it ([§9.4](#94-validation-rules)).

`position` is meaningful only for major arcana. A minor arcanum takes its place from its suit's [`ranks`](#44-suits) sequence and an application MUST ignore a `position` declared on one.

**On a variant-reference key** the entry supplies that variant's strings, image and content rating. Declaring one does not create the variant; a variant is created by a file ([§5.1](#51-asset-discovery)) or by an `image` path. `number`, `unnumbered`, `unnamed`, `position` and `default_variant` belong to the card rather than to one of its artworks, and an application MUST ignore any of the five declared on a variant-reference key: a variant does not sit elsewhere in the sequence and does not carry a different printed number, or a different absence of one, because it is the same card.

`inscription` is legal on a variant-reference key. A variant is a different artwork of the same card, so it may carry different ink even though it cannot carry a different number ([§4.3.3](#433-inscriptions)).

Where `default_variant` is omitted, the unsuffixed file such as `06.svg` is the default variant. A deck that provides only variant files for a card and no unsuffixed file MUST declare it. The field describes the card-to-variant relation and sits on the card, which is the party that has one default.

#### 4.3.1 Card Numbers

Many decks print a number on the card face and the `number` field holds that number as an opaque display string (e.g., "XXIII", "23" or "VIII½").

Where `number` is absent, a card's number follows from the shape of its key:

- A major arcanum with a two-digit key is numbered, and its number is that key's value. An application renders it by its own convention, which for a tarot deck is conventionally an upper-case Roman numeral.
- A major arcanum with a custom key is considered unnumbered.
- A minor arcanum is unnumbered.

A card that declares `unnumbered = true` carries no number whatever its key shape implies, and an application MUST NOT present one for it. `number` and `unnumbered` answer the same question and a card MUST NOT declare both. **Ordering is unaffected**: a major arcanum with a two-digit key keeps the implicit `position` of [§4.3.2](#432-ordering), so a card can be seated in the numbered sequence and print nothing, which is the Marseille's The Fool.

`number` and `inscription` ([§4.3.3](#433-inscriptions)) are not localized: each reproduces what is printed on the artwork, which is a property of the artwork rather than of the language an application is showing.

#### 4.3.2 Ordering

Applications that present a deck in order resolve it as follows. The major arcana come first, then the minor arcana.

Within the major arcana, cards are ordered by `position`. Every major arcanum with a two-digit key has an implicit `position` equal to that key's value. A card with a custom key and no declared `position` follows every card that has one.

Within the minor arcana, the suits come in the canonical order `wands`, `cups`, `swords`, `pentacles`, and every other suit the deck has follows those four, sorted by key. Within a suit, cards are ordered by that suit's [`ranks`](#44-suits) sequence, and a rank the sequence does not name follows every rank it does, likewise sorted by key. A suit with no `ranks` sequence therefore orders its cards by key alone.

A declared `position` MAY fall anywhere in the sequence and MAY be negative. Where two cards claim the same position, a declared `position` precedes an implicit one, and a tie between two of the same sort breaks by key.

#### 4.3.3 Inscriptions

An **inscription** is text printed on an [artwork](#13-terminology) other than the card's name and its number.

```toml
[cards."major_arcana.09"]
inscription = "Lux ex tenebris"

[cards."minor_arcana.wands.ace"]
inscription = ["Sacred Fire", "The Awakening"]  # two inscriptions, in reading order

[card_backs.designs.classic]
inscription = "Ex libris"
```

- The value is a non-empty string, or a non-empty array of non-empty strings.
- An array is ordered and applications MUST preserve the order. A packager SHOULD write the strings in the artwork's reading order. Nothing else is asserted about where on the artwork any of them sits.
- **Transcription is verbatim.** An inscription reproduces the ink, including a restatement of the card's name where the ink restates it, and including the packager's line breaks collapsed to spaces. Applications MUST NOT case-convert it, as with every other display string ([§6.3](#63-display-name-resolution)).
- An inscription is not a resolved display string and has no resolution chain. It is a fact about the artwork, like [`number`](#431-card-numbers), and absence means the artwork carries no inscription rather than that one is to be found elsewhere.

An inscription is never translated. Where a deck exists in two printings whose ink differs, those are two artworks and the axis is the [card variant](#312-card-references-and-the-variant-suffix), not the name file ([§6.2](#62-language-resolution)).

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

Providing `ranks` for a canonical suit, such as in the above example, replaces that suit's canonical sequence.

**`[suits.<key>]`** takes a [custom name](#32-custom-names) as the key, or one of the four canonical suits where the intent is to modify that suit.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | resolved per [§6.3](#63-display-name-resolution) | Fallback display name for the suit |
| `ranks` | Array of String | No | the canonical rank sequence for a canonical suit, otherwise none | The suit's rank keys in the order the deck reads them. |

Like [`[cards]`](#43-cards), `[suits]` describes rather than creates and a suit is created by placing files under `minor_arcana/<suit>/`. The whole table is OPTIONAL.

As with a card's `name` ([§4.3](#43-cards)), `[suits].name` is the deck's own string: a deck whose suit names are printed on its cards SHOULD declare them here and a deck whose suit names are the packager's own words SHOULD carry them in a name file, where they can be localized ([§6.2](#62-language-resolution), [§6.3](#63-display-name-resolution)). A deck whose courts print a full title and whose pips print nothing is the ambiguous case, and the printed title governs: the words exist on the artwork, so they are the deck's own.

### 4.5 `[ranks]`

A deck can name its ranks in the manifest, on the same terms as its suits:

```toml
[ranks.two]
name = "Deux"

[ranks.king]
name = "Roy"
```

**`[ranks.<key>]`** takes a [custom name](#32-custom-names) as the key, or one of the canonical ranks where the intent is to name that rank.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | resolved per [§6.3](#63-display-name-resolution) | Fallback display name for the rank. |

Like [`[suits]`](#44-suits), `[ranks]` describes rather than creates: a rank is created by a file, or by a suit's `ranks` sequence. The whole table is OPTIONAL.


### 4.6 `[excluded_cards]`

```toml
[excluded_cards]
cards = ["minor_arcana.pentacles.page", "minor_arcana.pentacles.knight"]
reason = "This deck excludes these specific court cards."
```

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `cards` | Array of String | No | `[]` | Canonical IDs of cards this deck deliberately does not contain. |
| `reason` | String | No | none | Why they are excluded, for display to a user. |

An exclusion records that the absence of an expected card is deliberate.

## 5. Card Assets

### 5.1 Asset Discovery

Applications detect files placed in the expected directory structure and map them to cards without further configuration. An image at `h1200/minor_arcana/wands/ace.png` maps to the card with the canonical ID `minor_arcana.wands.ace`, so creating a deck can be as simple as placing files into the right directories.

A file's stem is split on the first `.`, and the first portion is called the base. Where the base names a card the deck already contains, the remainder is a [variant key](#312-card-references-and-the-variant-suffix) and the file is a variant of that card. Otherwise the base names a card the file defines: in `major_arcana/` a two-digit base is that [major arcanum](#31-canonical-ids) and any other base is a custom name, and in `minor_arcana/<suit>/` the base is a rank key. For example:

- `major_arcana/06.two_women.png` is a variant of The Lovers
- `major_arcana/23.png` is the deck's twenty-fourth major arcanum
- `major_arcana/the_morning.png` is a major arcanum with a custom key
- `major_arcana/the_morning.dark.png` is a variant of that card

A deck therefore adds a card by adding a file, whether the card is canonical, numbered beyond `21`, or custom-keyed. Nothing in `deck.toml` is required for any of them.

### 5.2 Vector Graphics

SVG card assets are discovered only under the `scalable/` root; an SVG anywhere else is not a card asset and is ignored ([§5.7.1](#571-image-roots)). SVG is the only vector format this specification defines and support for rendering it is OPTIONAL for an application.

### 5.3 Raster Graphics

Raster card assets are discovered only under an `h<height>/` root, where `<height>` is the height of the image in pixels. A raster image anywhere else is ignored ([§5.7.1](#571-image-roots)). Which file formats discovery considers, and in what order, is fixed by the extension chain in [§5.7.4](#574-the-extension-chain).

Conventionally, `h750` serves mobile applications and thumbnails, `h1200` standard desktop and web viewing, and `h2400` high-resolution displays.

### 5.4 ANSI Art

- ANSI card assets are discovered only under an `ansi<lines>/` root, organized by card type and suit (e.g., `ansi32/major_arcana/00.ansi`); an ANSI file anywhere else is not a card asset and is ignored ([§5.7.1](#571-image-roots)). `<lines>` is the number of terminal rows the art occupies.
- ANSI files MAY use any extension. `.ans` is conventional for art carrying escape sequences and `.txt` for plain text.
- Applications MUST determine a file's kind from its content rather than its extension. Art using ANSI escape sequences necessarily contains ESC (`0x1B`) and a file with no ESC byte is plain text and MAY be written to a terminal as-is.
- Plain text files are UTF-8.
- Where a file carries a [SAUCE](https://www.acid.org/info/sauce/sauce.htm) record, applications SHOULD honor it.

Support for ANSI art is OPTIONAL for an application.

### 5.5 Card Back Images

Files in the card back directory `card_backs/` define a [design](#42-card_backs) whose key is the file's stem:

```
card_backs/classic.png          # "classic" with no declared size
h1200/card_backs/classic.png    # "classic" at 1200px
ansi32/card_backs/classic.ans   # "classic" at 32 rows
scalable/card_backs/classic.svg # scalable "classic"
```

A card back directory appears in two OPTIONAL locations. At the top level of the deck root, `card_backs/` holds backs of no declared kind or size. This is the simple form and for most decks the only one needed. Inside an [image root](#571-image-roots), `card_backs/` sits beside `major_arcana/` and `minor_arcana/` and its files carry that root's kind and size.

The designs a deck has are the union of the stems found across every card back directory, together with every key declared under `[card_backs.designs]` that carries an `image` path. Further rules:

- The whole stem is the design key and card backs have no notion of variants.
- A stem that is not a well-formed [custom name](#32-custom-names) defines no design. Discovery ignores the file, which is reported as a warning rather than an error ([§9.4](#94-validation-rules)), exactly as a raster image outside an image root is ignored.
- The [extension chain](#574-the-extension-chain) applies. A deck SHOULD supply each design in a [baseline format](#574-the-extension-chain). A card has a reference deck to fall back on and a back does not ([§5.7.7](#577-resolving-a-card-back)), so an application that cannot decode a design substitutes its own generic back and the deck's design is never seen.
- An explicit `image` path on `[card_backs.designs.<key>]` overrides discovery for that design in every kind and size.
- Card backs MAY have different dimensions and aspect ratios from the card fronts.

### 5.6 Aspect Ratio

- Standard assumed aspect ratio is 11:19 (~0.5789) declared by [`[deck].aspect_ratio`](#41-deck).
- Applications MUST preserve the aspect ratio when scaling images.

A deck taken from a physical printing MAY also record that card's width and height in millimetres as [`[deck].card_size_mm`](#41-deck). Where the physical size disagrees with `aspect_ratio`, the ratio governs.

### 5.7 Card Image Resolution

Given a card, a rendering kind and a target size, an application resolves a file to display. This section defines that resolution.

#### 5.7.1 Image Roots

An image root is a top-level directory of a deck root that discovery searches for card assets. There are four forms:

| Form | Kind | Size |
| --- | --- | --- |
| `scalable/` | scalable | none |
| `h<height>/` | raster | Height in pixels |
| `ansi<lines>/` | ANSI | Lines in terminal rows |
| `surrogate/` | surrogate | none |

`<height>` and `<lines>` are decimal integers greater than zero, written without a sign, leading zeroes or separators. A deck MAY contain any number of raster and ANSI roots, and at most one `scalable/` and one `surrogate/`.

Within an image root, assets are arranged by card type and suit as shown in [§2.1](#21-directory-skeleton): `major_arcana/` and `minor_arcana/<suit>`. An image root MAY also hold a `card_backs/` directory, which supplies card back designs at that root's kind and size ([§5.5](#55-card-back-images)). Any other subdirectory is ignored, and so is any file lying loose in the root itself rather than in one of those subdirectories.

Every other top-level directory is ignored by discovery.

The top-level names this specification defines are `deck.toml`, `card_backs/`, `names/` and the image roots above. A deck MAY therefore keep material of its own beside its card assets under any name that is not one of the above.

#### 5.7.2 Extensions, Stems and Bases

A card asset filename is read as four parts. Given `06.two_women.png`:

| Part | Value | Rule |
| --- | --- | --- |
| extension | `png` | The part after the **last** `.` |
| stem | `06.two_women` | Everything before the last `.` |
| base | `06` | The part of the stem before the **first** `.` |
| variant key | `two_women` | The remainder of the stem after the first `.`, where there is one |

The stem is split on the first `.` and the extension taken from the last, because a variant key cannot itself contain a `.` ([§3.5](#35-grammar)). A file named `06.png` has base `06`, no variant key and extension `png`.

A file whose name contains no `.` at all has no extension. Discovery ignores it in `scalable/` and in raster roots. In an ANSI root it is a candidate: [§5.4](#54-ansi-art) allows ANSI files any extension or none.

Card backs have no variants ([§5.5](#55-card-back-images)), so a stem containing a `.` is not a valid design and discovery ignores it.

#### 5.7.3 Size Selection Within a Kind

Selection for `scalable/` and `surrogate/` is trivial due to those directories containing at most one file per card and variant.

For raster and ANSI, an application selects among the roots of that kind that supply a file for the card. The rules differ, because the two media degrade in opposite directions:

- Raster: prefer the smallest image at or above the target height. Downscaling a raster image is well-behaved and upscaling is not.
- ANSI: prefer the largest art at or below the target number of lines. Art taller than the space available is truncated.

Candidates on the preferred side of the target therefore rank ahead of those on the other side. Within a side the nearest to the target wins, and a tie between two equidistant candidates breaks toward the preferred side. An exact match always wins. Where no candidate lies on the preferred side, an application MUST take the nearest on the other side rather than fail.

#### 5.7.4 The Extension Chain

Within a raster directory, an application considers extensions in this fixed order:

1. `png`
2. `webp`
3. `avif`
4. `jpeg` and `jpg`. Where a directory holds both, the choice between them is unspecified.

In `scalable/`, the chain is `svg` alone. In `surrogate/`, it is `toml` alone.

- Applications MUST support decoding PNG, JPEG and WebP. Support for AVIF and SVG is OPTIONAL. These three are the **baseline formats**, and this document uses that term for them wherever the distinction matters.
- Extensions outside the chain are ignored by discovery entirely.
- A deck SHOULD NOT ship two files with the same stem and different chain extensions in one directory. Where it does, applications MUST resolve by this order and MUST NOT resolve by filesystem order. A validator reports the duplication as a warning.
- Where every candidate in a directory is either outside the chain or in a format the application lacks, that directory does not supply the card and the application MUST continue with the remaining candidates under [§5.7.3](#573-size-selection-within-a-kind).

A deck that wants a format outside the chain declares an explicit `image` path on the card or card variant ([§4.3](#43-cards)) or on the card back design ([§4.2](#42-card_backs)).

#### 5.7.5 Variants

A request MAY name a [variant key](#312-card-references-and-the-variant-suffix). Resolution then looks for files whose stem is `<base>.<key>`, and is otherwise unchanged.

Where the requested card has no variant under that key, the application MUST resolve that card's default variant instead, and MUST NOT treat the absence as an error. A card's default variant is the one its [`default_variant`](#43-cards) names, or the unsuffixed file where the card declares none.

#### 5.7.6 When No Asset Is Found

Where resolution yields no file for a card in any image root of any kind and the library designates a [reference deck](#13-terminology) and the card is not deliberately absent under [`[excluded_cards]`](#46-excluded_cards), the application SHOULD resolve the same card against that deck. This step applies only to a canonical minor arcanum or a major arcanum keyed `00` through `21`.

An application MUST NOT present a borrowed image as though it were the deck's own and SHOULD make the substitution visible, on the same terms as a [surrogate](#58-surrogate-assets). Where it displays attribution or rights metadata for a borrowed card, it MUST take that metadata from the reference deck, whose terms may be narrower than those of the deck it stands in for.

An application MUST NOT resolve a card against a reference deck for a package that declares [`rel = "expands"`](#419-related-decks). Such a package is a set of cards added to another deck rather than a deck in its own right, so every canonical slot it does not carry is a slot it was never meant to carry, and filling them from a reference deck presents someone else's complete deck under the expansion's name. The three conditions below are all checked against declarations a whole deck makes, and an expansion passes them by declaring nothing.

The remaining conditions assume the two decks agree about what the card is. Each is checked against the decks' own declarations, so a deck that declares nothing fails none of them:

- **Lineage.** An application SHOULD NOT borrow where the two decks declare incompatible lineage via a [`follows`](#413-follows) relation. Two decks are lineage-compatible where the borrowing deck `follows` the reference deck's `identifier`, or the reference deck `follows` the borrowing deck's `identifier`, or both follow the same deck, or either declares no `follows`. The last clause makes this condition permissive by default, which is deliberate and is easy to misread as an oversight: a [reference deck](#13-terminology) is the deck others are patterned on, so it is normally a pattern root carrying no `follows` of its own, and the condition then holds for every borrowing deck. Lineage blocks a borrow only where both decks name a lineage and the two disagree.
- **Pip style.** An application SHOULD NOT borrow an image for a minor arcanum keyed `two` through `ten` where both decks declare a [`pips`](#414-pips) value and the values differ. Aces, court cards and the major arcana are unaffected ([§4.1.4](#414-pips)).
- **Name coherence.** An application SHOULD NOT borrow an image for a card where the borrowing deck supplies its own name for that card and the reference deck's name for the same [canonical ID](#31-canonical-ids) differs, since a canonical ID is a [slot](#311-a-canonical-id-is-a-slot) and two decks may put different cards in it. Both names are resolved by [§6.3](#63-display-name-resolution) in the language being displayed, rather than compared as declared strings, since a deck may name a card in its manifest instead of a name file ([§6.2](#62-language-resolution)). This is the condition that fires on two decks in different patterns: each is typically a pattern root declaring no `follows`, so the lineage condition above passes and this one is what remains.

These conditions gate the borrow only. Where one blocks it, the outcome is the one below for a card no reference deck supplies.

Otherwise, this is a resolution failure and it is up to the application to decide what to show.

#### 5.7.7 Resolving a Card Back

An application resolves a back similarly to the main algorithm, with three differences:

1. The subpath is `card_backs/` rather than `major_arcana/` or `minor_arcana/<suit>/` and the stem is the design key.
2. Where no image root of the requested kind supplies the design, the top-level `card_backs/` directory is consulted last as a root of no size.
3. There is no reference-deck step and applications supply their own back.

#### 5.7.8 Resolution Summary

Given a card, a variant key, a kind and a target size, an application:

1. Forms the stem from the card's base, plus `.<variant-key>` where one is requested, and the subpath `major_arcana/` or `minor_arcana/<suit>/`.
2. Ranks the image roots of the requested kind by [§5.7.3](#573-size-selection-within-a-kind) and, best first, looks in `<root>/<subpath>` for that stem under the [extension chain](#574-the-extension-chain), taking the first file it can decode. Walking past a root it cannot decode costs it a fallback rather than the card.
3. Failing that, and where a variant was requested, repeats step 2 for the card's default variant ([§5.7.5](#575-variants)).
4. Failing that, resolves the card against the [reference deck](#13-terminology) where the library has one, the card is not excluded, and the card has a canonical counterpart ([§5.7.6](#576-when-no-asset-is-found)). This step sits outside the per-deck lookup, so a reference deck is consulted once the deck itself is exhausted and never in the middle of size selection.

Card backs follow the same shape with the differences [§5.7.7](#577-resolving-a-card-back) gives. An explicit `image` path wins outright, the subpath is `card_backs/` and the stem is the design key, the top-level `card_backs/` is consulted last, and there is no reference-deck step.

ANSI files are exempt from the extension chain: [§5.4](#54-ansi-art) allows them any extension, so in an ANSI root a lookup matches on stem alone and determines the file's kind from its content. An application MUST apply [§10.2](#102-terminal-escape-injection) to any ANSI file it writes to a terminal.

### 5.8 Surrogate Assets

A surrogate is a derived, deliberately lossy stand-in for a card's artwork that lives in the `surrogate/` [image root](#571-image-roots) and is discovered like other card assets ([§5.1](#51-asset-discovery)):

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
| `palette_snapped` | Array of String | No | `[]` | `palette`, each entry replaced by the nearest [CSS Color 4 named color](https://www.w3.org/TR/css-color-4/#named-colors). |
| `thumbhash` | String | No | none | A [ThumbHash](https://evanw.github.io/thumbhash/) of the artwork, Base64-encoded. |

An example `surrogate/major_arcana/00.toml`:

```toml
# generated by libarcana 0.4.2
palette = ["#e8d5a3", "#2b4a6f", "#8c3b2e", "#d9d2c4"]
palette_snapped = ["wheat", "darkslateblue", "sienna", "lightgray"]
thumbhash = "1QcSHQRnh493V4dIh4eXh1h4kJUI"
```

Every key is optional and independent. A deck MAY carry any combination and MAY carry different combinations for different cards. A file carrying none of them is a well-formed surrogate.

### 5.9 Surrogate Decks

A surrogate deck is a deck whose only card assets are surrogates. Because the artwork of most tarot decks is neither the packager's to give away nor, in many cases, licensed for redistribution at all, surrogates allow a deck to be packaged without shipping anyone else's art.

A surrogate deck SHOULD declare a correspondence to the artwork it describes: a [`surrogate_for`](#412-surrogate_for) relation where a package of that artwork exists within Arcana Land, [`[deck.product_ids]`](#415-product-identifiers) where the artwork belongs to a commercial product that carries a published identifier, or both. Either allows applications to recognize a surrogate and a package as the same underlying deck and prefer the artwork over the surrogate.

The two differ in who assigns them. `surrogate_for` names a package and its value is chosen by that package's packager, so it can only be used where such a package exists and is known. A product identifier is assigned by the publisher and printed on the product, so two packagers who have never met will record the same value for the same deck. A surrogate deck for a commercial deck that no one has packaged SHOULD therefore carry `[deck.product_ids]`, and one for a deck already packaged within Arcana Land SHOULD carry a `surrogate_for` relation.

A surrogate deck SHOULD NOT invent an `identifier` for a package that does not exist in order to have something for `surrogate_for` to name.

A surrogate deck SHOULD also declare [`[deck].rights_status`](#74-rights-status), and MAY contain a `buy` [link](#411-links) where available.

Because [`[deck].license`](#41-deck) covers the card assets in the package ([§7](#7-licensing-and-attribution)), a surrogate deck covers the surrogates rather than the artwork. A surrogate deck SHOULD declare `license`.

A surrogate deck's `icon`, where it has one, SHOULD avoid using the signified deck's artwork or a crop, scaling or recompression of it. It SHOULD be the packager's own work or a rendering of the surrogates inside the deck.

## 6. Internationalization

Display strings such as card names, suit names, rank names and alt text are declared in `names/<tag>.toml`.

### 6.1 Language Tags

`<tag>` MUST be a well-formed IETF BCP 47 language tag.

- Tags SHOULD be canonical, using the shortest available ISO 639 subtag (`en`, not `eng`), lowercase language, titlecase script and uppercase region.
- Applications MUST compare tags case-insensitively. A deck MUST NOT ship two name files whose tags differ only in case.
- `[deck].default_language` declares the tag of the deck's default name file, and nothing else. Where absent, applications assume `en`.

A deck has up to three languages and they are not the same question:

| Key | Names the language of |
| --- | --- |
| `default_language` | the name file a lookup falls back to ([§6.2](#62-language-resolution)) |
| `metadata_language` | the packager's own prose |
| `artwork_language` | the text printed on the cards themselves |

`metadata_language` defaults to `default_language`, so a deck that declares neither is unchanged in meaning. It is not itself localizable.

`artwork_language` is an array (multilingual card faces are common). When a card contains no text as expected, this can be expressed with the BCP 47 tag `zxx` (no linguistic content.

```toml
default_language  = "fr"          # the name file, and the card faces
metadata_language = "en"          # the packager, who is writing in English
artwork_language  = ["fr"]
```

### 6.2 Language Resolution

Display strings live in two layers. A **name file** is a translation catalogue: every string in it is addressed to a reader of that file's language tag, and a packager writes one by asking what a reader of that language should be shown. The manifest is the source layer where every string in it reproduces or describes the deck itself, in whatever language the deck is in.

A string that reproduces text printed on an artwork belongs in the manifest, whatever language that text is in.

Given a requested tag, applications resolve it using the Lookup scheme of RFC 4647, trying the requested tag, then progressively shorter forms of it, then the deck's `default_language`. A request for `pt-BR` therefore reads `names/pt-BR.toml`, then `names/pt.toml`, then the default language file. A key that no name file supplies falls through to the further fallbacks in [§6.3](#63-display-name-resolution).

A name file is organized by **facet**: the outermost table names the kind of string, the tables below it name the kind of entity, and the keys name entities.

```
[<facet>.<entity-kind>]
<entity-key> = "<string>"
```

```toml
[metadata]                            # Optional
source = "Names and alt text written by Jane Doe."
license = "CC-BY-4.0"

[name.card.major_arcana]
00 = "The Fool"
01 = "The Magician"

[name.card.minor_arcana]
name_template = "{rank} of {suit}"    # Optional

[name.card.minor_arcana.wands]
ace = "Ace of Wands"                  # Optional, overrides the template

[name.suit]
wands = "Wands"
stars = "Stars"                       # Custom suit

[name.rank]
page = "Page"
knight = "Warrior"                    # Renamed rank

[name.card_back]
classic = "Classic Back"

[name.variant]                        # Keyed by variant reference
"major_arcana.06:two_women" = "The Lovers"

[name.group.arcana]                   # Optional, see §6.2.2
major = "Major Arcana"

[alt_text.card.major_arcana]
00 = "A young person in colorful clothes steps off a cliff, carrying a white rose. A small dog jumps at their heels."

[alt_text.card.minor_arcana.wands]
ace = "A hand emerging from a cloud holds a flowering wooden staff."

[alt_text.card_back]
classic = "A blue and white geometric pattern featuring roses and lilies."

[alt_text.variant]
"major_arcana.06:two_women" = "Two women stand hand in hand beneath a winged figure."
```

This is deliberately the transpose of `deck.toml` due to the nature of the intended authors.

Two facets are defined, `name` and `alt_text`. Together with the reserved [`[metadata]`](#621-name-file-metadata) they are the only top-level tables a name file carries and a validator SHOULD report any other ([§9.4](#94-validation-rules)) rather than ignore it.

Below the facet, the entity kinds are closed:

| Kind | Names | Its keys are |
| --- | --- | --- |
| `card` | a card | written as a key path below the kind: `[<facet>.card.major_arcana]` keyed by a major arcana key, and `[<facet>.card.minor_arcana.<suit>]` keyed by a rank key |
| `suit` | a suit | a suit key |
| `rank` | a rank | a rank key |
| `card_back` | a [card back design](#42-card_backs) | a design key |
| `variant` | one [artwork](#13-terminology) of a card | a whole [variant reference](#312-card-references-and-the-variant-suffix), quoted, since [§3.6](#36-identifiers-in-toml) makes it a single key rather than a key path |
| `group` | a set of cards ([§6.2.2](#622-group-names)) | a family member key |

Each kind is written in the singular, which distinguishes it from the identically spelled plural card-set families of the [Esoterica Specification](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md): `[name.suit]` names a suit and that specification's `group.suits.wands` names every card of one.

A localizable facet this specification adds later takes a top-level table of its own, mirroring the kinds above, and a field of the same name on the corresponding `deck.toml` entity table as the unlocalized fallback. Where a field an entity carries is deliberately not localizable, its field table in [§4](#4-decktoml-reference) says so and says why: [`description`](#42-card_backs), [`number`](#431-card-numbers) and [`inscription`](#433-inscriptions) are the three. The last two are not localizable for the same reason, which is the source-layer rule above rather than three separate exceptions.

**Name files changed shape in 2.0.** A 1.0 name file is facet-outer in the same sense but writes the `name` facet without naming it, so that `[major_arcana]`, `[minor_arcana.<suit>]`, `[suits]`, `[ranks]`, `[card_backs]` and `[card_variants]` are its name tables while `[alt_text.*]` are its alt-text tables ([Appendix B](#appendix-b-reserved-and-deprecated-names)). An application reads `[deck].schema_version` from the manifest before it reads any name file, so which shape a file is written in is known before it is parsed. The two never mix: a deck declares one version and all of its name files are of that version's shape.

Name files are sparse and MAY contain a subset of keys. Applications MUST merge name files key by key rather than requiring a complete set, and MUST NOT treat a missing key as an error.

#### 6.2.1 Name File Metadata

The `[metadata]` table is OPTIONAL and describes the name file itself rather than any card in it.

| Key | Purpose |
| --- | --- |
| `source` | Who or what produced the strings in this file |
| `origin` | How the strings in this file came to exist, keyed by vocabulary system, on the terms of [§4.1.8](#418-artwork-origin) |
| `license` | SPDX license expression governing the strings in this file |
| `license_files` | Paths, relative to the deck root, to the full license text and any notices |
| `copyright` | The copyright notice, verbatim as the rights holder wrote it |
| `rights_status` | URI for the artwork's copyright status |
| `attribution` | The credit line the license requires downstream users to display |

The OPTIONAL `[metadata.alt_text]` subtable takes the same keys and overrides them for alt text alone. See [Name File Licensing](#73-name-file-licensing).

`source` and `attribution` are the packager's own prose about the file rather than strings addressed to its reader, so they are written in the deck's [`metadata_language`](#41-deck) like the manifest's prose fields, and not in the language the file's tag names.

The `origin` field uses the same systems (IPTC) and terms as [§4.1.8](#418-artwork-origin). When chosing a term, consider `digitalCreation` for strings a human wrote, `trainedAlgorithmicMedia` for strings a model produced, and `compositeWithTrainedAlgorithmicMedia` for strings a human drafted and a model expanded. The `source` field is intended to provide the prose account beside the origin term.

```toml
[metadata]
origin = { "iptc-dst" = "digitalCreation" }

[metadata.alt_text]
origin = { "iptc-dst" = "trainedAlgorithmicMedia" }
source = "Alt text created by ACME's ExampleLLM 2.0."
```

A name file whose strings a human wrote need not declare an origin at all and omission is the common case. Declare it where something in the file was machine-produced, or where the packager wants the human authorship of the rest on the record.

#### 6.2.2 Group Names

The `group` kind names sets of cards rather than cards. The [Esoterica Specification](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md) attaches interpretive content to such sets and defines the families; this specification supplies their display strings, because what a deck calls its two arcana is the deck's own business and is localizable like every other string in this file.

| Table | Keys | Names |
| --- | --- | --- |
| `[name.group.arcana]` | `major`, `minor` | One of the two arcana |
| `[name.group.classes]` | `pip`, `court` | The numbered minor arcana, or the courts |

```toml
[name.group.arcana]
major = "Major Arcana"
minor = "Minor Arcana"

[name.group.classes]
pip = "Pips"
court = "Court Cards"
```

Two further families are named elsewhere in the same file and take no table of their own: a group of one suit is named by `[name.suit]` and a group of one rank by `[name.rank]`. The remaining families are not a deck's to name — a source's author-defined group is local to that source, and no group naming every card is defined here.

Where no name file supplies a group name, an application supplies its own localized string. There is no title-cased fallback, because a key such as `major` does not title-case into a name anyone would print.

### 6.3 Display Name Resolution

Each chain below is applied to name files in the order given by [Language Resolution](#62-language-resolution).

A resolved display string is used verbatim. Applications MUST NOT apply case conversion or any other transformation to a string a deck supplies. Case transformation appears in this specification only as a fallback for keys the deck does not define a string for.

Every chain has the same three steps: **the name file, then the corresponding field in the manifest, then a fallback that depends on what is being named.** Two rows depart from that pattern and are the only two that do: a minor arcanum's name is composed rather than fetched, and the major arcana chain carries two further steps that apply to the canonical keys `00` through `21` alone.

| Value | In the name file | In the manifest | Then |
| --- | --- | --- | --- |
| Suit name | `[name.suit].<key>` | `[suits.<key>].name` | for a canonical key, a string the application supplies; for a custom key, the [title-cased key](#13-terminology) |
| Rank name | `[name.rank].<key>` | `[ranks.<key>].name` | as above |
| Major arcana name | `[name.card.major_arcana].<key>` | `[cards."major_arcana.<key>"].name` | for a key `00` through `21` only, the [reference deck](#13-terminology)'s name for that ID and then [Appendix C](#appendix-c-canonical-card-names-informative) where no reference deck is configured. See below for a key that reaches the end. |
| Minor arcana name | `[name.card.minor_arcana.<suit>].<rank>` | `[cards."minor_arcana.<suit>.<rank>"].name` | [composition](#631-minor-arcana-name-composition) from the card's suit and rank names |
| Card back design name | `[name.card_back].<key>` | `[card_backs.designs.<key>].name` | the title-cased key |
| Card variant name | `[name.variant]."<variant-ref>"` | `[cards."<variant-ref>"].name` | the name of the card itself |
| Group name | `[name.group.<family>].<member>` | — | a string the application supplies ([§6.2.2](#622-group-names)) |
| Alt text | `[alt_text.<kind>…].<key>` | the `alt_text` field of the corresponding `[cards]` or `[card_backs.designs]` entry | none |
| Card variant alt text | `[alt_text.variant]."<variant-ref>"` | `[cards."<variant-ref>"].alt_text` | the card's own alt text |

A dash means the manifest has no field for that value, a group being the one thing `deck.toml` does not describe as an entity of its own.

Canonical suit and rank keys are a closed set this specification defines, so where no name file and no manifest field supplies a string an application supplies its own, localized to the language it is displaying, exactly as it does for a group name ([§6.2.2](#622-group-names)). A **custom** key is a word the packager chose, so its title-cased form is a string in the deck's [`metadata_language`](#41-deck); an application presents it as given and MUST NOT translate it. The same rule governs the two other places a title-cased key survives — a card back design key, and a custom major arcana key — both of which are always custom.

A card that declares `unnamed = true` resolves its name through the name file and the manifest as usual and the chain then stops: the reference-deck step and [Appendix C](#appendix-c-canonical-card-names-informative) do not apply, and where neither supplies a string the card has no name. A name file may still give one and it still wins, so a packager who wants a conventional label for a picker can supply it; what the flag forbids is a name being invented for a face that carries none. A card MUST NOT declare both `unnamed = true` and a `name`.

A major arcana key that reaches the end of its chain has no name. Where that key is custom, an application uses the title-cased key, which for a key the packager chose is usually a serviceable name. Where it is an [extended major arcanum](#13-terminology) the title-cased key is the bare digits so an application SHOULD instead present the card by its [number](#431-card-numbers).

The reference deck steps of these chains are subject to the lineage condition of [§5.7.6](#576-when-no-asset-is-found): an application SHOULD NOT borrow a name where the two decks declare incompatible lineage, and resolution continues to the next step of the chain instead. The pip-style and name-coherence conditions govern images alone and do not apply here.

The reference-deck and [Appendix C](#appendix-c-canonical-card-names-informative) steps of the major arcana chain assume the deck seats the canonical cards where those names expect them. A deck that departs from that seating — most commonly by exchanging `08` and `11`, as the Marseille pattern does — SHOULD supply its own names for at least the departing keys, and a validator says so ([§9.4](#94-validation-rules)). This is a SHOULD on the deck rather than a MUST on the application because an application cannot detect the departure: a [canonical ID is a slot](#311-a-canonical-id-is-a-slot), and nothing in the file says which card the packager put in it.

The reference deck and [Appendix C](#appendix-c-canonical-card-names-informative) are both absent from this chain above `21`. A deck that has extended major arcana SHOULD name them in a name file, and a validator says so ([§9.4](#94-validation-rules)).

#### 6.3.1 Minor Arcana Name Composition

Because a deck MAY rename its suits and ranks, most decks need not write out all 56 minor arcana names. Where a name file gives no explicit name for a minor arcana card, its name is composed from a template:

```toml
[name.card.minor_arcana]
name_template = "{rank} of {suit}"
```

`{rank}` and `{suit}` are replaced by the rank and suit names resolved above. No other placeholders are defined, and an application MUST leave any other braced text in the template alone. The template is resolved by the same [Language Resolution](#62-language-resolution) rules as any other key, so a translation supplies its own. Where no name file supplies one, the template is `"{rank} of {suit}"`.

A template and the names it composes MUST come from one language. Where a name file in the resolution order supplies `name_template`, `{rank}` and `{suit}` are resolved from that same file, and a file that supplies none of the three is skipped for all three together.

The manifest holds the deck's own words, in the artwork's language rather than a reader's ([§6.2](#62-language-resolution)), so it is consulted for `{rank}` and `{suit}` only where the template came from the deck's [`default_language`](#41-deck) name file, or where no name file supplies a template and the deck takes the default above. A template drawn from any other name file MUST NOT compose with a manifest string: where that file names no suit or rank, resolution continues to the terminal step of [§6.3](#63-display-name-resolution)'s Suit name and Rank name rows instead. A deck whose `default_language` is not `en` SHOULD supply its own template, since the default above is English and would otherwise set English grammar over the deck's own words.

Without these rules a partially translated deck composes a name out of two languages at once — an English template over French suit names — and every such string is well defined and wrong.

The template performs substitution only. Where a language requires elision, inflection or agreement between the rank and suit names, a deck SHOULD write the affected names out explicitly rather than expect the template to produce them: French elides before a vowel, so a template cannot turn `de` and `Epee` into `d'Epee`.

Where a deck supplies no name for a minor arcanum at any level, applications MAY fall back to the corresponding string from the [reference deck](#13-terminology), subject to the same lineage condition.

### 6.4 Alt Text Guidelines

- Alt text SHOULD describe the visual elements of the card without interpretation.
- A deck SHOULD include at least one language file carrying alt text.
- Every card variant SHOULD carry its own alt text.
- Alt text given in `[cards]` or `[card_backs.designs]` is a fallback only, and a name file always prevails.
- Where a card carries text on its face, put the transcription in [`inscription`](#433-inscriptions) and let the alt text describe the artwork. Alt text need not repeat the ink, and a deck that has been carrying printed epithets inside its alt text SHOULD move them: the ink is part of the artwork and is covered by the artwork's licence, while alt text is the packager's own writing and is often licensed separately ([§7.3](#73-name-file-licensing)).

## 7. Licensing and Attribution

A deck comprises several components that can have separate licensing terms.

- The license specified by `[deck].license` covers the card assets the package contains. For most decks those assets are the artwork and the field says what may be done with it. For a [surrogate deck](#59-surrogate-decks) they are the surrogates and the artwork they describe is covered by [`rights_status`](#74-rights-status) instead.
- The license in the `[metadata].license` field of a name file covers the strings in that file and `[metadata.alt_text]` narrows that to the alt text alone.

Each of these names its own license texts through its own `license_files`.

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

For public licenses that require a downstream user who alters the work to say that they altered it, a deck whose artwork is a modified version of someone else's SHOULD say so in `attribution`. Where the artwork was obtained from a particular scan or archive rather than from the rights holder, a [`source` link](#411-links) SHOULD name it.

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
source = "Translated by Jane Doe."
license = "CC-BY-4.0"
license_files = ["names/LICENSE.pt-BR"]
attribution = "Portuguese translation by Jane Doe."
```

Typically, the strings in a name file are the packager's choice, or a translator's. A full set of one contributor's renamings is a compilation and such a file SHOULD say where the names came from in `[metadata].source` and SHOULD carry a [`rights_status`](#74-rights-status) for them.

### 7.4 Rights Status

Most tarot decks are not licensed to anyone. A deck packaged from a commercially available product the packager purchased has no license to grant.

For this reason, `[deck].rights_status` records the artwork's copyright status instead. The `license` pertains to the files in this directory while `rights_status` is about the work they depict.

For an ordinary deck these coincide and both describe the artwork. For a [surrogate deck](#59-surrogate-decks), a packager is free to license the surrogates they generated (or reused) while accurately recording that the artwork behind them is in copyright to someone else.

`rights_status` SHOULD be one of:

- a [RightsStatements.org](https://rightsstatements.org/) URI; or
- a [Creative Commons](https://creativecommons.org/) URI.

```toml
# A deck whose artwork is old enough that its copyright has expired.
[deck]
license = "CC0-1.0"
rights_status = "https://creativecommons.org/publicdomain/mark/1.0/"
```

For copyrighted decks:

```toml
[deck]
rights_status = "https://rightsstatements.org/vocab/InC/1.0/"
copyright = "© 2012 Some Artist"
attribution = "The Example Tarot by Some Artist."
```

`license` and `rights_status` answer different questions about, in general, different objects, and a deck MAY carry both, one, or neither. Where both are present and both are about the artwork, which is the case for any deck that carries its artwork, they MUST NOT contradict each other; a validator cannot check this in general and does not try, beyond the coarse cases [§9.4](#94-validation-rules) lists.

The same field is available in a name file's `[metadata]` and `[metadata.alt_text]` tables, with the same meaning ([§7.3](#73-name-file-licensing)).

### 7.5 Redistribution and Derivation

The two fields governing how a package can be redistributed or used to create new works are `[deck].redistribution` and `[deck].derivation`:

| Value | Meaning |
| --- | --- |
| `"full"` | The artwork may be passed on as it is. |
| `"surrogate"` | The artwork may not be passed on, but a [surrogate](#58-surrogate-assets) derived from it may. |
| `"none"` | Neither may be passed on. |
| `"unstated"` | The default. The packager has not said. |

```toml
[deck]
name = "The Example Tarot"
rights_status = "https://rightsstatements.org/vocab/InC/1.0/"
redistribution = "none"
derivation = "surrogate"
```

The default value is `"unstated"` which does not grant permission. An application MUST NOT read it as `"full"` and one that redistributes decks on a user's behalf SHOULD treat `"unstated"` as it treats `"none"`.

### 7.6 Roles and Credits

This specification defines four fields that are used to credit people. A name or email address are reasonable values for these fields.

| Field | Who |
| --- | --- |
| `artist` | Who made the artwork |
| `creator` | Who devised the deck (if different from `artist`) |
| `publisher` | Who published the deck |
| `packager` | Who assembled this package ([§1.2](#12-document-conventions)) |

```toml
[deck]
name = "The Example Tarot"
creator = "A. E. Deviser"        # who devised it
artist = "Some Artist"          # who drew it
publisher = "Example Press"     # who published it
packager = "Jane Doe <jane@example.org>"   # who built this directory
```

Most decks need fewer than four. Where one person occupies two roles, the deck SHOULD name them once in the more specific field. For example, a deck drawn by the person who devised it only needs to declare `artist` instead of both `artist` and `creator`.

`creator` exists because the two roles are sometimes separate. For example, A. E. Waite devised the Rider-Waite-Smith deck and Pamela Colman Smith drew all 78 cards.

A deck SHOULD declare `packager` where the packager is not the deck's `artist`, and a package describing artwork it does not own SHOULD always declare it.

### 7.7 Deck Names and Trademarks

The name of a published tarot deck is frequently a trademark of its publisher and using a mark to identify the deck is generally permitted in most jurisdictions.

However, a package MUST NOT imply an endorsement, affiliation or origin it does not have. Concretely:

- A deck's `name`, `description` and `attribution` MUST NOT state or imply that the rights holder produced, approved or endorsed the package, unless they did.
- A package assembled by a third party SHOULD declare [`packager`](#76-roles-and-credits).
- A [`buy`](#411-links) or `publisher` link SHOULD point to the rights holder rather than a reseller ([§4.1.1](#411-links)).
- A packager SHOULD NOT reproduce the publisher's logo or wordmark as the deck's `icon`.

Nothing here is a legal determination and this specification does not make one.

## 8. Extensibility

The `[app]` table is reserved for applications to record data about a deck that this specification does not model. Each application takes a subtable keyed by a [realm](#33-qualified-identifiers):

```toml
[app."land.arcana.tarotcanvas"]
bleed = true # artwork runs to the edge

[app."land.arcana.cartomancer"]
ansi_color_depth = "truecolor"  # ANSI art uses 24-bit SGR
ansi_glyphs = "sextants"        # needs a font covering U+1FB00–U+1FBFF
```

The subtable key MUST be written as a quoted TOML key because a realm always contains a `.` character.

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

A validator reports two kinds of violations. An error makes a deck non-conforming and an application MAY refuse it. A warning marks something the packager probably did not intend, or a condition this specification allows but has an opinion about. An application MUST load a deck that produces only warnings.

### 9.3 Conforming Applications and Validators

A conforming application:

- MUST implement the library model and scanning rules ([§2.2](#22-the-deck-library)) over whatever roots it uses, asset discovery ([§5.1](#51-asset-discovery)), display name resolution ([§6.3](#63-display-name-resolution)) and card image resolution ([§5.7](#57-card-image-resolution)).
- MUST support decoding the baseline formats PNG, JPEG and WebP ([§5.7.4](#574-the-extension-chain)).
- MUST ignore `[app]` subtables it does not own ([§8](#8-extensibility)), and every table, key and value this specification does not define.
- MUST NOT reject a deck for warnings ([§9.2](#92-errors-and-warnings)).

An application need not implement card variants, ANSI art, SVG, surrogates or localization beyond the deck's default language. Where it does not, it uses the defaults those sections define. An application that does not implement surrogates ignores the `surrogate/` root as it ignores any kind it cannot render, and so treats a [surrogate deck](#59-surrogate-decks) as a deck whose cards have no assets, which [§5.7.6](#576-when-no-asset-is-found) already defines. A conforming validator implements the rules in [§9.4](#94-validation-rules).

Neither an application nor a validator need accept a [container](#24-deck-containers). One that does not is unaffected by the container rules of [§9.4](#94-validation-rules) and remains conforming.

### 9.4 Validation Rules

Each rule is labeled **E** for error or **W** for warning.

| | Rule |
| --- | --- |
| **E** | `deck.toml` exists and is valid TOML 1.0.0, and every image, license file and name file it references exist. |
| **E** | Every key whose Required column in [§4](#4-decktoml-reference) reads **Yes** is present: `[deck].schema_version`, `name` and `version` ([§4.1](#41-deck)), `rel` and `url` on each `[deck].links` entry ([§4.1.1](#411-links)), `rel` and `deck` on each `[deck].related` entry ([§4.1.9](#419-related-decks)). A key whose Required column states a condition rather than **Yes** is reported by the rule below that states the same condition, and a key marked RECOMMENDED is not Required and is not reported at all. |
| **E** | Every key [§4](#4-decktoml-reference) defines carries a value of the type its field table gives. A key the deck omits is left to the rule above, and a key this specification does not define is [ignored](#8-extensibility) rather than typed. |
| **E** | `[deck].schema_version` has the form [§1.4](#14-versioning-and-compatibility) requires. |
| **E** | `[deck].published_date` is a `published-date` ([§3.5](#35-grammar)) denoting a real calendar date ([§4.1.7](#417-published-date)). |
| **E** | Every top-level table in a name file is a facet this specification defines, meaning `name` or `alt_text`, or is the reserved `[metadata]` table ([§6.2](#62-language-resolution)). This is an error and not the silent ignoring of [§8](#8-extensibility), because an unrecognized facet supplies no strings at all and a fully translated deck would present as an untranslated one. |
| **E** | Below the facet, every table names an [entity kind](#62-language-resolution) this specification defines, and every key corresponds to a card, suit, rank, card variant or card back design the deck defines or to a [group family member](#622-group-names), or is `name_template` under `[name.card.minor_arcana]`, or appears in the reserved `[metadata]` table or its `alt_text` subtable. |
| **E** | `[name.card.minor_arcana].name_template`, where present, contains no placeholder other than `{rank}` and `{suit}`. |
| **E** | Every name file's stem is a well-formed BCP 47 language tag, no two differ only in case, and `[deck].default_language` has a corresponding file. |
| **E** | A name file carries no top-level `[inscription]` table. An inscription is a manifest fact and not a display string a reader's language selects, so it is declared as [`[cards].inscription`](#433-inscriptions). A validator reporting this SHOULD name that field. |
| **E** | `metadata_language`, where present, is a well-formed BCP 47 language tag, and `artwork_language`, where present, is a non-empty array of well-formed BCP 47 language tags ([§6.1](#61-language-tags)). |
| **W** | An `artwork_language` containing `zxx` alongside any other tag. *No linguistic content* and a named language cannot both describe the same faces ([§6.1](#61-language-tags)). A warning and not an error, because a deck could conceivably carry lettered and unlettered faces. |
| **W** | A deck declaring a `metadata_language` different from its `default_language`. Informational: the row exists so a validator can show the packager that the distinction was read as intended rather than as a typo ([§6.1](#61-language-tags)). |
| **E** | Every `[ranks.<key>]` table key is a well-formed [custom name](#32-custom-names) or a canonical rank ([§4.5](#45-ranks)). |
| **W** | Alt text is provided for all cards in at least one name file. |
| **W** | A name file that names an entity and gives it no alt text, where that file gives alt text to any other entity of the same [kind](#62-language-resolution). The two facets are written as separate blocks ([§6.2](#62-language-resolution)), so an entity missed out of one of them is invisible to a reader checking the other. |
| **E** | `[card_backs].default`, where present, names a card back design the deck has, whether discovered from a [card back directory](#55-card-back-images) or declared with an `image` path. |
| **E** | `reversible`, where present on a `[card_backs.designs]` entry, is a boolean. Its truth is the packager's claim and is not checked ([§4.2](#42-card_backs)). |
| **E** | Every `[card_backs.designs]` table key is a well-formed [custom name](#32-custom-names), and every `image` path declared under it exists. A discovered stem is not covered by this rule: an ill-formed stem defines no design and is a file discovery ignores ([§5.5](#55-card-back-images)), which the warning below reports. |
| **W** | Where the deck has more than one card back design and neither `[card_backs].default` nor a design keyed `default` is present, the default rests on collation order ([§4.2](#42-card_backs)). Resolution is well defined, but the packager probably did not choose it. |
| **W** | A file in a card back directory that discovery ignores, meaning a stem containing a `.`, a stem that is not a custom name, or an extension outside the chain with no `image` path pointing at it. Such a file is usually an intended back that will never be shown. |
| **W** | A card back design supplied in no [baseline format](#574-the-extension-chain). Unlike a card, a back has no reference deck to fall back on ([§5.7.7](#577-resolving-a-card-back)), so an application that cannot decode it substitutes its own and the design is never seen ([§5.5](#55-card-back-images)). |
| **W** | A card whose every raster asset, across all image roots, is in no [baseline format](#574-the-extension-chain). |
| **E** | Every custom name matches the `custom-name` grammar of [§3.5](#35-grammar) and is not a name reserved by [§3.2](#32-custom-names), excepting a canonical suit used as a `[suits]` table key. |
| **E** | `[deck].identifier`, where present, is a well-formed qualified identifier without a fragment. It names the deck as a whole ([§3.4](#34-deck-identity)). |
| **E** | Every `[app]` subtable key is a well-formed realm, in particular one with two labels or more, which is what distinguishes `[app."land.arcana"]` from an unquoted `[app.land.arcana]` ([§8](#8-extensibility)). The contents of such a subtable are the owning application's to define and are not validated. |
| **W** | `[deck].identifier`'s first path segment is `deck` ([§3.3](#33-qualified-identifiers)). |
| **W** | `[deck].identifier` is present. It is RECOMMENDED, and a deck without one cannot be referenced from another Arcana Land document ([§3.4](#34-deck-identity)). |
| **W** | Where a validator can see a whole library, no two visible decks declare the same `[deck].identifier`. Two decks that do are a legitimate arrangement, such as a fork or two versions installed side by side, so this is only a warning. |
| **E** | Every `[cards]` table key is a well-formed [card reference](#312-card-references-and-the-variant-suffix), in particular a two-digit major arcana key written with both digits and a variant key that is a well-formed [custom name](#32-custom-names). |
| **E** | `[cards]` holds single keys and not key paths ([§3.6](#36-identifiers-in-toml)). A document writing `[cards.major_arcana.00]` has declared a table named `major_arcana` rather than the card `major_arcana.00`. The rule governs the card reference itself; a subtable written beneath one, as in `[cards."major_arcana.06".content_rating."oars-1.1"]`, is unaffected. |
| **E** | Every card declared in `[cards]` is a card the deck has files for, since `[cards]` does not define cards on its own. A canonical minor arcanum and a major arcanum keyed `00` through `21` are exempt, because those slots exist for every deck whether or not it ships the asset ([§4.3](#43-cards)). A [variant reference](#312-card-references-and-the-variant-suffix) is never exempt: the card it names is a card the deck defines, and the variant itself is one the deck has a file for or declares an `image` path to. |
| **E** | Every `image` path declared in `[cards]` exists. |
| **E** | Where a card has variant files but no unsuffixed file, `default_variant` is declared on that card, and where it is declared it names a variant that card has ([§4.3](#43-cards)). A card with no files at all is a [resolution failure](#576-when-no-asset-is-found), not a violation of this rule. |
| **E** | `number`, where present, is a non-empty string. A card is made unnumbered by the shape of its key or by `unnumbered`, not by an empty `number` ([§4.3.1](#431-card-numbers)). |
| **E** | `unnumbered` and `unnamed`, where present, are booleans ([§4.3](#43-cards)). |
| **E** | No card declares both `number` and `unnumbered = true`. The two contradict and this specification supplies no precedence ([§4.3.1](#431-card-numbers)). |
| **E** | No card declares both `name` and `unnamed = true`, for the same reason ([§6.3](#63-display-name-resolution)). |
| **W** | `unnumbered = true` on a minor arcanum or on a custom-keyed major arcanum, both of which the key shape already makes unnumbered ([§4.3.1](#431-card-numbers)). The declaration says nothing. |
| **W** | `unnumbered = true` on an [extended major arcanum](#13-terminology) that no name file names. [§6.3](#63-display-name-resolution) presents such a card by its number, so the combination leaves an application with nothing to show. |
| **E** | Every `inscription`, on a card, on a variant and on a card back design alike, is a non-empty string or a non-empty array of non-empty strings ([§4.3.3](#433-inscriptions)). |
| **W** | A card's `inscription` equal to its resolved `number` or to its resolved name. The definition excludes both, so the packager has transcribed something that already has a home and the two will be rendered twice ([§4.3.3](#433-inscriptions)). It is a warning and not an error because a deck whose printed epithet genuinely equals its printed name is possible and is not a validator's business to forbid. |
| **W** | A `position` declared on a minor arcanum, which an application ignores ([§4.3](#43-cards)). |
| **W** | A `number`, `unnumbered`, `unnamed`, `position` or `default_variant` declared on a variant-reference key, all five of which an application ignores ([§4.3](#43-cards)). An `inscription` on such a key is not reported: it belongs to the artwork and is legal there ([§4.3.3](#433-inscriptions)). |
| **W** | A deck whose major arcana seating departs from [Appendix C](#appendix-c-canonical-card-names-informative) and which supplies no name for a departing key, so that an application borrows a name for a card the deck did not put in that slot ([§6.3](#63-display-name-resolution)). |
| **W** | Every [extended major arcanum](#13-terminology) the deck has is named in at least one name file. Nothing else can name it ([§6.3](#63-display-name-resolution)), so one that is not will be shown to the user as a bare number. |
| **E** | No custom major arcana key is a two-digit string and no custom rank or suit key shadows a canonical one, so that a custom ID can never collide with a canonical one. |
| **E** | Every rank named in a `ranks` list has files in that suit, and no `ranks` list contains duplicates. |
| **E** | No card is both excluded by `[excluded_cards]` and declared in `[cards]`. |
| **W** | No card listed in `[excluded_cards]` has an image file. An exclusion is a statement of intent ([§4.6](#46-excluded_cards)); a deck that ships the asset anyway has probably changed its mind and not updated the list. |
| **W** | A `position` **declared** by two cards. Ordering remains well defined ([§4.3.2](#432-ordering)). A declared `position` that coincides with an implicit one is not reported, since seating a card against a numbered neighbor is the field's purpose. |
| **E** | No path field, meaning `icon`, `image` or any `license_files` entry, begins with `/`, contains a `..` segment or resolves outside the deck root ([§2.3](#23-file-format-and-encoding), [§10.1](#101-path-traversal)). |
| **E** | No directory holds two files whose stems differ only in case ([§2.3](#23-file-format-and-encoding)). |
| **E** | Every file listed in a `license_files` list exists, in `[deck]` and in every name file's `[metadata]` alike, and `[metadata.alt_text]` contains no key that is not defined for `[metadata]`. |
| **W** | Two files in one directory sharing a stem and differing only in a chain extension, such as `06.png` beside `06.webp`. Resolution is well defined ([§5.7.4](#574-the-extension-chain)), but one of the two is usually a conversion left behind. |
| **W** | A card asset whose own aspect ratio differs from `[deck].aspect_ratio` by more than 10%, measured as `\|actual - declared\| / declared` ([§4.1](#41-deck)). Card backs are exempt, since `[deck].aspect_ratio` describes the fronts, and so is ANSI art, whose extent is counted in character cells rather than pixels and is not comparable to a ratio of lengths. |
| **E** | `card_size_mm`, where present, holds exactly two numbers and both are greater than zero ([§4.1](#41-deck)). |
| **W** | Where both `card_size_mm` and `aspect_ratio` are present, the ratio `width ÷ height` of `card_size_mm` differs from `aspect_ratio` by more than 10%, measured as above. One of the two is likely a transcription error, though `aspect_ratio` governs either way ([§5.6](#56-aspect-ratio)). |
| **W** | A `license` field that is not a well-formed SPDX license expression. A deck that fails this check MUST NOT be rejected ([§7](#7-licensing-and-attribution)). |
| **W** | A `rights_status` that is not a RightsStatements.org or Creative Commons URI, in `[deck]` and in every name file's `[metadata]` alike. As with `license`, a deck that fails this check MUST NOT be rejected ([§7.4](#74-rights-status)). |
| **E** | `redistribution` and `derivation`, where present, are one of `full`, `surrogate`, `none` or `unstated` ([§7.5](#75-redistribution-and-derivation)). |
| **W** | A deck that declares neither `license` nor `rights_status`. One of the two is how a deck says what may be done with its artwork, and a deck that says neither leaves every downstream user guessing ([§7](#7-licensing-and-attribution)). |
| **W** | A `redistribution` or `derivation` of `full` alongside a `rights_status` asserting the artwork is in copyright with no license granted, meaning a RightsStatements.org `InC` URI or one of its refinements. The deck says both that nobody granted permission and that the packager passes it on ([§7.5](#75-redistribution-and-derivation)). One of the two fields is wrong, and a validator cannot tell which. |
| **W** | A `redistribution` or `derivation` narrower than `full` on a deck whose `license` is a public license granting redistribution or derivation outright. The license governs and the field does not take it back ([§7.5](#75-redistribution-and-derivation)), so the field misleads a reader without binding anyone. A validator checks this only for licenses it recognizes, and reporting nothing is a conforming outcome. |
| **W** | A [surrogate deck](#59-surrogate-decks) declaring `redistribution = "full"`. The field governs passing on the artwork and the package carries none ([§5.9](#59-surrogate-decks)). A `license` on such a deck is not reported, since it covers the surrogates and a surrogate deck SHOULD carry one. |
| **W** | A [surrogate deck](#59-surrogate-decks) with no `license`. Its surrogates are the packager's own work and `derivation = "surrogate"` invites them to be passed on, so a reader who takes them up has no terms to go by ([§5.9](#59-surrogate-decks)). |
| **W** | A deck that names artwork it did not produce and does not declare `packager`, meaning one carrying a `surrogate_for` relation, or one whose `rights_status` asserts the artwork is in copyright to someone else ([§7.6](#76-roles-and-credits)). Every rights assertion in the package is then unattributable. |
| **W** | A `packager` equal to `artist`, or a `creator` equal to `artist`. Where the two are the same person the field says nothing, and where they are not one of them is wrong ([§7.6](#76-roles-and-credits)). |
| **E** | On every `[deck].links` entry, `rel` is a well-formed [custom name](#32-custom-names) and `url` is absolute with an `http` or `https` scheme ([§4.1.1](#411-links)). That both are present is the required-key rule's to report. |
| **W** | A `links` `rel` outside the registry of [§4.1.1](#411-links) that is not prefixed. Applications ignore it, and a later version of this specification may claim the name. |
| **E** | On every `[deck].related` entry, `rel` is a well-formed [custom name](#32-custom-names) and `deck` is a well-formed qualified identifier carrying no fragment and not equal to this deck's own `identifier` ([§4.1.9](#419-related-decks)). Whether it names a deck that exists is not checkable and is not checked. That both keys are present is the required-key rule's to report. |
| **E** | A deck declares at most one `follows` relation and at most one `surrogate_for` relation, and names no deck under both ([§4.1.2](#412-surrogate_for), [§4.1.3](#413-follows)). |
| **W** | A `related` `rel` outside the registry of [§4.1.9](#419-related-decks) that is not prefixed. Applications ignore it, and a later version of this specification may claim the name. |
| **W** | A package declaring `rel = "expands"` that also declares `[excluded_cards]` covering the canonical slots it does not carry. The relation already says the package is not a whole deck, so the exclusions are a second statement of the same thing and neither is read by anything the other is not ([§5.7.6](#576-when-no-asset-is-found)). |
| **E** | `pips`, where present, is one of `scenic`, `emblematic` or `unstated` ([§4.1.4](#414-pips)). |
| **E** | Every `product_ids` key is a well-formed [custom name](#32-custom-names) and every value is a non-empty string ([§4.1.5](#415-product-identifiers)). |
| **W** | An `isbn` that is not ten or thirteen characters once hyphens and spaces are removed, or whose check digit does not verify. Box copy is transcribed by hand and this catches the transcription error, which is the failure this field actually meets ([§4.1.5](#415-product-identifiers)). |
| **W** | A `gtin` that is not eight, twelve, thirteen or fourteen digits, that contains a character other than a digit, or whose check digit does not verify ([§4.1.5](#415-product-identifiers)). |
| **W** | A `product_ids` scheme outside the registry of [§4.1.5](#415-product-identifiers) that is not prefixed. As with a `links` `rel`, applications ignore it and a later version of this specification may claim the name. |
| **E** | Every `content_rating` subtable key is a well-formed [custom name](#32-custom-names), in `[deck]` and on every card and card back design alike, and every descriptor key within a system subtable is a well-formed custom name carrying a non-empty string value. `artwork_complete`, where present, is a boolean and appears only at the deck level ([§4.1.6](#416-content-rating)). |
| **E** | Within an `oars-1.1` subtable, every descriptor key is one of the twenty-two OARS 1.1 attribute ids written with underscores and every value is one of `none`, `mild`, `moderate` or `intense` ([§4.1.6](#416-content-rating)). A validator does not check that a value is one the attribute admits, since OARS restricts some attributes to a subset of the four and this specification does not track those restrictions across OARS revisions. |
| **E** | Every rating system named on an [artwork](#13-terminology) is a system `[deck.content_rating]` also declares, and no descriptor declared on an artwork exceeds the deck-level value declared for the same system and descriptor under the ordering `none` < `mild` < `moderate` < `intense` ([§4.1.6](#416-content-rating)). A descriptor the deck-level subtable omits is `none`, and so admits no value above it on any artwork, except under `artwork_complete = true`, where it is derived from the artwork and constrains nothing. |
| **W** | A `content_rating` system outside the registry of [§4.1.6](#416-content-rating) that is not prefixed. As with a `links` `rel`, applications ignore it and a later version of this specification may claim the name. |
| **E** | Where any [artwork](#13-terminology) declares a descriptor for a system, that system's subtable in `[deck.content_rating]` declares `artwork_complete` ([§4.1.6](#416-content-rating)). Without it an application cannot tell an unannotated artwork from an unrated one, and the specification supplies no default. |
| **W** | Under `artwork_complete = true`, a declared deck-level descriptor whose value exceeds every value the deck's artwork carries for it. The deck says the content is somewhere in it and a complete annotation says it is nowhere, so one of the two is unfinished ([§4.1.6](#416-content-rating)). A deck-level descriptor that merely restates what the artwork already carries is not reported. |
| **W** | An `artwork_complete` on a system no artwork declares a descriptor for. The key describes an annotation that does not exist ([§4.1.6](#416-content-rating)). |
| **E** | Every `origin` system key is a well-formed [custom name](#32-custom-names), in `[deck]`, on every card and card back design, and in every name file's `[metadata]` and `[metadata.alt_text]` alike, and every value is a non-empty string ([§4.1.8](#418-artwork-origin)). |
| **E** | Every origin system named on an [artwork](#13-terminology) is a system `[deck.origin]` also declares ([§4.1.8](#418-artwork-origin)). |
| **W** | A value under an `iptc-dst` key that is not a term name of the IPTC Digital Source Type vocabulary ([§4.1.8](#418-artwork-origin)). The vocabulary is not this specification's to close and IPTC adds terms without renaming existing ones, so an unrecognized term is ignored rather than rejected. The cost is that a misspelled term passes quietly. |
| **W** | An `origin` system outside the registry of [§4.1.8](#418-artwork-origin) that is not prefixed. As with a `links` `rel`, applications ignore it and a later version of this specification may claim the name. |
| **E** | Every file in the `surrogate/` root is well-formed TOML 1.0.0 and carries no key this specification does not define for a [surrogate file](#581-the-surrogate-file). |
| **E** | Every entry of a `palette` is an sRGB hex triplet matching `#` followed by six lower-case hexadecimal digits, every entry of `palette_snapped` is a CSS Color 4 named color. |
| **W** | A `palette_snapped` whose length differs from that of the `palette` beside it. The two are meant to be the same colors in the same order ([§5.8.1](#581-the-surrogate-file)). |
| **W** | A surrogate deck that declares neither a [`surrogate_for`](#412-surrogate_for) relation nor any [`[deck.product_ids]`](#415-product-identifiers) entry. Nothing can then connect it to the deck it describes, and an application holding both cannot merge them ([§5.9](#59-surrogate-decks)). |
| **W** | A surrogate deck with no `buy` link and no `[deck].rights_status`. It describes artwork the reader cannot see, without saying why or where to get it ([§5.9](#59-surrogate-decks)). |
| **E** | Where a validator is given a [container](#24-deck-containers), the archive holds `deck.toml` at its root rather than inside a wrapping directory, and no entry name is absolute, names a drive, or carries a `..`, `.` or empty segment ([§2.4](#24-deck-containers)). |
| **E** | Where a validator is given a container, no entry is a symbolic link, a hard link, an encrypted entry, or anything other than a regular file or a directory, and every entry is stored or deflated ([§2.4](#24-deck-containers)). |
| **W** | A container whose first entry is not an uncompressed `mimetype` carrying the media type of [§2.4](#24-deck-containers). Applications still read it, but it cannot be identified by its content, so a desktop that recognizes files by their leading bytes presents it as a plain archive. |

## 10. Security Considerations

A deck arrives from outside the system and carries data a packager can abuse. This section describes the security concerns that can arise.

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
creator = "A. E. Waite"
artist = "Pamela Colman Smith"

license = "LicenseRef-PublicDomain AND CC0-1.0"
license_files = ["LICENSE"]
copyright = "Artwork © 1909 Pamela Colman Smith (copyright expired)"
attribution = "Original artwork by Pamela Colman Smith (1909)."
rights_status = "https://creativecommons.org/publicdomain/mark/1.0/"
redistribution = "full"
derivation = "full"

default_language = "en"
published_date = "1909-12"
tags = ["traditional", "classic", "beginner-friendly"]
links = [
  { rel = "homepage", url = "https://en.wikipedia.org/wiki/Rider%E2%80%93Waite_Tarot" },
]

[deck.content_rating."oars-1.1"]
sex_nudity = "mild"
violence_fantasy = "mild"
violence_bloodshed = "mild"

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

[alt_text.card.major_arcana]
00 = "A young person in colorful clothes steps off a cliff."

[alt_text.card_back]
classic = "A lattice of blue and white roses and lilies."
```

### A.3 Renamed Suits, a Custom Card and Two Card Backs

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
```

The deluxe printing is a [card back design](#42-card_backs) and the `description` on it is where the printing is stated. Two printings that differ in their cards are two decks, optionally related by a [`follows`](#413-follows) relation.

And `names/en.toml`:

```toml
[name.card.major_arcana]
00 = "The Wanderer"   # This deck's name for The Fool

[name.suit]
wands = "Torches"
cups = "Waters"
swords = "Winds"
pentacles = "Stones"

[name.rank]
page = "Student"
knight = "Warrior"

[alt_text.card.major_arcana]
00 = "A traveler with a backpack walks toward a fiery mountain."
elemental_force = "A vortex of the elements swirling together in harmony."

[alt_text.card_back]
flames = "A dynamic pattern of red and orange flames swirling around a central spark."
```

### A.4 A Lowercase Typographic Convention

A deck that prints every minor arcana in lower case writes its suit and rank names that way and lets composition do the rest. Cards that break the deck's own pattern are written out individually and take precedence over the template.

```toml
# names/en.toml
[name.card.minor_arcana]
name_template = "{rank} of {suit}"

[name.suit]
wands = "torches"
cups = "cups"

[name.rank]
ace = "ace"
page = "princess"
knight = "prince"

[name.card.minor_arcana.pentacles]
ace = "one of pentacles"
# other suits are still "ace"

[name.card.major_arcana]
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

And `names/en.toml`, which both names the variants and describes them. `deck.toml` declares nothing about them at all:

```toml
[name.card.major_arcana]
06 = "The Lovers"

[name.variant]
"major_arcana.06:two_women" = "The Lovers"
"major_arcana.06:two_men" = "The Lovers"

[alt_text.card.major_arcana]
06 = "A man and a woman stand hand in hand beneath a winged figure."

[alt_text.variant]
"major_arcana.06:two_women" = "Two women stand hand in hand beneath a winged figure."
"major_arcana.06:two_men" = "Two men stand hand in hand beneath a winged figure."
```

A deck needs a `[cards]` entry for a variant only to choose a non-default default, to supply fallback strings, to rate the variant separately from its card or to point at a file that does not follow the naming convention. A deck that ships no unsuffixed `06` file is the first of those cases, and names its default in `deck.toml`:

```
    major_arcana/
      06.two_women.png        # no 06.png
      06.two_men.png
```

```toml
[cards."major_arcana.06"]
default_variant = "two_women"
```

### A.6 A Surrogate Deck

A surrogate deck can be created for commercial decks with non-redistributable artwork by providing surrogate assets.

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

In the main `deck.toml`:

```toml
[deck]
schema_version = "2.0"
name = "The Example Tarot"
identifier = "net.example.jdoe/deck/example-tarot-surrogate"
version = "1.0"
artist = "Some Artist"
publisher = "Example Press"
packager = "Jane Doe <jane@example.org>"
aspect_ratio = 0.5833
card_size_mm = [70, 120]

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

# Example Press has not packaged this deck, so there is no identifier for a
# surrogate_for relation to name, and the correspondence is recorded against the
# product itself instead (§5.9).
[deck.product_ids]
isbn = "9789999999991"
```

With a surrogate for The Fool:

```toml
# surrogate/major_arcana/00.toml
# generated by libarcana 0.4.2
palette = ["#e8d5a3", "#2b4a6f", "#8c3b2e"]
palette_snapped = ["wheat", "darkslateblue", "sienna"]
thumbhash = "LEHV6nWB2yk8pyo0adR*.7kCMdnj"
```

## Appendix B. Reserved and Deprecated Names

The names below were defined by an earlier version of this specification, or by an earlier draft of this one, and are not defined by it now. A future version of this specification MUST NOT reuse any of them with a new meaning.

Applications MUST ignore these names in a 2.0 deck.

| Name | Was | Status |
| --- | --- | --- |
| `[deck].author` | The artwork's author in 1.0 | Renamed in 2.0 to [`[deck].artist`](#41-deck) and split the role with [`[deck].creator`](#76-roles-and-credits) |
| `[deck].signifies` | The deck whose artwork a package describes and does not carry, as a flat key in an earlier 2.0 draft | Folded into [`[deck].related`](#419-related-decks) as `rel = "surrogate_for"` ([§4.1.2](#412-surrogate_for)) |
| `[deck].follows` | The deck this deck is patterned on, as a flat key in an earlier 2.0 draft | Folded into [`[deck].related`](#419-related-decks) as `rel = "follows"` ([§4.1.3](#413-follows)) |
| `[deck].id` | The deck's identifier in 1.0. | Removed in 2.0. The handle is the directory name and the global identity is [`[deck].identifier`](#34-deck-identity). |
| `[aliases]` | Suit and court display names in 1.0 | Removed in 2.0. Superseded by [name files](#6-internationalization) |
| `[variants]` | Deck editions in 1.0 | Removed in 2.0. A printing that differs only in its card back is a [card back design](#42-card_backs). The word "variant" now means a [card variant](#312-card-references-and-the-variant-suffix) |
| A name file's `[major_arcana]`, `[minor_arcana]`, `[minor_arcana.<suit>]`, `[suits]`, `[ranks]`, `[card_backs]` and `[card_variants]` | The `name` facet of a 1.0 name file, written without naming the facet | Renamed in 2.0. Every facet is now written out fully. |
| `[card_backs.variants]` | Card back designs in 1.0 | Renamed to [`[card_backs.designs]`](#42-card_backs) in 2.0. |
| `[deck.excluded_cards]` | Excluded cards, nested under `[deck]` in 1.0 | Moved to top-level [`[excluded_cards]`](#46-excluded_cards) in 2.0 |
| `[deck.companions]` | Never specified. | Superseded by [qualified identifiers](#33-qualified-identifiers), by which another Arcana Land document names a deck rather than the deck naming it |
| `[custom_cards]` | Custom major arcana, suits and ranks in 1.0 | Split in 2.0. Per-card metadata for every card, canonical or custom, moved to [`[cards]`](#43-cards) and suit structure moved to [`[suits]`](#44-suits). |
| `image` on `[custom_cards.major_arcana.<key>]` | An explicit path to a custom card's image in 1.0 | Removed in 2.0. A card's images come from [discovery](#51-asset-discovery)|
| `id` on `[custom_cards.major_arcana.<key>]` | A custom card's identifier in 1.0 | Removed in 2.0. The table key is the card's canonical ID |
| `[remap_major_arcana]` | A table remapping major arcana display positions in 1.0 | Removed in 2.0. No published deck used it and it was unnecessary |
| `created_date`, `updated_date` | Two dates on `[deck]` in 1.0 | Replaced in 2.0 by [`published_date`](#417-published-date). |

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

## Appendix D. Platform Conventions (Informative)

This appendix records where applications conventionally look for decks on common platforms. [§2.2.1](#221-the-library-model) leaves the choice of [library roots](#13-terminology) to the application and this section provides recommendations.

**Linux.** Follow the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/) and search `$XDG_DATA_HOME/tarot/decks` first, then `<dir>/tarot/decks` for each `<dir>` in `$XDG_DATA_DIRS`. Where `$XDG_DATA_HOME` is unset or empty it defaults to `$HOME/.local/share`, and where `$XDG_DATA_DIRS` is unset or empty it defaults to `/usr/local/share:/usr/share`.

**macOS.** `~/Library/Application Support/tarot/decks`, then `/Library/Application Support/tarot/decks`.

**Windows.** `%LOCALAPPDATA%\tarot\decks`, then `%PROGRAMDATA%\tarot\decks`.

## Appendix E. Changelog

### Version 2.0

An application MAY support 1.0 decks alongside 2.0 ones. Where it does, it reads them under 1.0's rules.

**Breaking changes.** Every name removed or renamed is listed in [Appendix B](#appendix-b-reserved-and-deprecated-names). Version 2.0 removes `[aliases]`, `[remap_major_arcana]`, `[variants]`, `[deck].id` and the `image` and `id` fields of a custom major arcanum, replaces `created_date` and `updated_date` with [`published_date`](#417-published-date), renames `[deck].author` to [`[deck].artist`](#76-roles-and-credits), renames `[card_backs.variants]` to `[card_backs.designs]`, splits `[custom_cards]` into [`[cards]`](#43-cards) and [`[suits]`](#44-suits), moves `[deck.excluded_cards]` to a top-level `[excluded_cards]`, keys `[app]` subtables by a realm rather than a bare custom name, and renames every table in a [name file](#62-language-resolution) so that the facet is written out.

**Newly specified.**

- [The deck library](#22-the-deck-library), covering scanning and shadowing across an ordered list of roots. Where an application finds those roots is left to the application, with the platform conventions gathered informatively in [Appendix D](#appendix-d-platform-conventions-informative).
- [Card image resolution](#57-card-image-resolution), covering image roots and size selection. Also promoted WebP to first-class format.
- [Card back discovery](#55-card-back-images), so that a back can exist at several resolutions or as ANSI.
- [File format and encoding](#23-file-format-and-encoding).
- [Deck containers](#24-deck-containers), a single-file transfer form carrying one deck directory, so that a deck can be shared as one file without the directory ceasing to be what this specification describes.
- [Security considerations](#10-security-considerations), covering path traversal and ANSI escape codes.
- [Appendix C](#appendix-c-canonical-card-names-informative) for fallback name-resolution chains.
- [Rights status](#74-rights-status), [redistribution and derivation](#75-redistribution-and-derivation), for artwork that no license covers. `[deck].license` now covers the card assets a package carries rather than the artwork specifically, so that a package can license what it ships while `rights_status` describes the work behind it.
- [Surrogates](#58-surrogate-assets) and [surrogate decks](#59-surrogate-decks), so that a deck can be described without its artwork being redistributed. A surrogate is a card asset of its own kind in the `surrogate/` image root, discovered and resolved like any other.
- [Group names](#622-group-names), by which a name file supplies the deck's own localized strings for its arcana and its card classes.
- [`[deck].packager`](#76-roles-and-credits), naming who assembled the package.
- [`[deck].creator`](#76-roles-and-credits), naming who devised a deck they did not draw.
- [`[deck].related`](#419-related-decks), one table of typed outbound references to other decks. It carries [`follows`](#413-follows), by which a deck names the deck or tradition it is patterned on; [`surrogate_for`](#412-surrogate_for), by which a package names the deck whose artwork it describes but does not contain (e.g., due to copyright); `expands`, by which an add-on package names the deck it adds cards to; and `companion`. Recognized relations govern what the package is and are closed within a major version, while advisory ones are an open registry an application may ignore.
- [`[deck].metadata_language`](#61-language-tags) and [`[deck].artwork_language`](#61-language-tags), separating the language the packager writes in and the language printed on the cards from the `default_language` that selects a name file.
- The [two-layer rule](#62-language-resolution) for display strings: a name file is a translation catalogue and the manifest is the source layer. [`[ranks]`](#45-ranks) is new, supplying the source step a rank never had, and a canonical suit or rank the deck does not name now falls to a string the application localizes rather than to a title-cased English key.
- [`inscription`](#433-inscriptions) on a card, a card variant and a card back design, transcribing text printed on the artwork other than its name and its number.
- [`unnumbered`](#431-card-numbers) and [`unnamed`](#63-display-name-resolution) on a card, by which a face that carries no numeral or no title says so without being unseated from the sequence.
- [`[deck].pips`](#414-pips), by which a deck can specify whether its numbered minor cards depict scenes.
- [`[deck].links`](#411-links), replacing `[deck].website` with typed links that say what they point at.
- [`[deck.product_ids]`](#415-product-identifiers), recording the identifiers of a commercial published deck.
- [`[deck].published_date`](#417-published-date), when the deck was published, at whatever precision the packager has.
- [`[deck].content_rating`](#416-content-rating) stating what the artwork depicts in the vocabulary of a named rating system.
- [`origin`](#418-artwork-origin), stating how a deck's artwork came to exist (e.g., AI generated), in the vocabulary of a named system.
- [`reversible`](#42-card_backs) on a card back design, stating whether the back looks the same turned 180°.

**Other changes.** Restructured the document as a specification, adopting BCP 14 keywords explicitly, replacing the regex identifier forms with one consolidated [ABNF grammar](#35-grammar) and lifting fields out of TOML comments into [normative field tables](#4-decktoml-reference). Added [qualified identifiers](#33-qualified-identifiers) and formalized custom names and display name resolution. Made every card discoverable from the directory structure, added [card variants](#312-card-references-and-the-variant-suffix), which are entries in [`[cards]`](#43-cards) keyed by a variant reference rather than a table of their own, allowed custom `ranks` for canonical suits and added `name_template` composition. Specified name file language tags as BCP 47, added `default_language`. Added [`[deck].card_size_mm`](#41-deck) as informative metadata about a physical printing, distinct from the `aspect_ratio` that rendering uses ([§5.6](#56-aspect-ratio)). Specified `license` as SPDX, added `license_files` and `copyright`, and added the `[metadata]` table to name files. Added `rights_status`, `redistribution` and `derivation` for artwork SPDX cannot describe. Defined what `[app]` is for and reserved top-level table names outside it.
