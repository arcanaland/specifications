# Arcana Land Tarot Spread Specification

**Author**
- Adam Fidel <adam@arcana.land>

**Version**: 1.0 (draft)

## Table of Contents

- [1. Introduction](#1-introduction)
  - [1.1 Scope and Design Goals](#11-scope-and-design-goals)
  - [1.2 Document Conventions](#12-document-conventions)
  - [1.3 Terminology](#13-terminology)
  - [1.4 Versioning and Compatibility](#14-versioning-and-compatibility)
  - [1.5 References](#15-references)
  - [1.6 Licensing of This Specification (Informative)](#16-licensing-of-this-specification-informative)
- [2. Spreads](#2-spreads)
  - [2.1 One Spread, One File](#21-one-spread-one-file)
  - [2.2 The Spread Library](#22-the-spread-library)
    - [2.2.1 Scanning](#221-scanning)
    - [2.2.2 Shadowing](#222-shadowing)
  - [2.3 File Format and Encoding](#23-file-format-and-encoding)
- [3. Identity and Identifiers](#3-identity-and-identifiers)
  - [3.1 Spread Identity](#31-spread-identity)
  - [3.2 Position Identifiers](#32-position-identifiers)
  - [3.3 Grammar](#33-grammar)
- [4. Document Reference](#4-document-reference)
  - [4.1 `[meta]`](#41-meta)
    - [4.1.1 Description](#411-description)
    - [4.1.2 Sources](#412-sources)
  - [4.2 `[[positions]]`](#42-positions)
  - [4.3 `[[groups]]`](#43-groups)
- [5. Layout](#5-layout)
  - [5.1 The Card Unit](#51-the-card-unit)
  - [5.2 The Card Box](#52-the-card-box)
  - [5.3 Rotation](#53-rotation)
  - [5.4 Stacking](#54-stacking)
  - [5.5 A Spread Without a Layout](#55-a-spread-without-a-layout)
- [6. Number and Count](#6-number-and-count)
  - [6.1 Position Numbers](#61-position-numbers)
  - [6.2 Counts](#62-counts)
  - [6.3 Repeating Groups](#63-repeating-groups)
  - [6.4 What a Spread Does Not State](#64-what-a-spread-does-not-state)
- [7. Localization](#7-localization)
- [8. Licensing and Credit](#8-licensing-and-credit)
  - [8.1 What `license` Covers](#81-what-license-covers)
  - [8.2 License Expressions](#82-license-expressions)
  - [8.3 Redistribution and Derivation](#83-redistribution-and-derivation)
  - [8.4 Credit](#84-credit)
- [9. Presenting a Spread](#9-presenting-a-spread)
- [10. Extensibility](#10-extensibility)
- [11. Conformance and Validation](#11-conformance-and-validation)
  - [11.1 Conforming Spread](#111-conforming-spread)
  - [11.2 Errors and Warnings](#112-errors-and-warnings)
  - [11.3 Conforming Applications and Validators](#113-conforming-applications-and-validators)
  - [11.4 Validation Rules](#114-validation-rules)
- [12. Security Considerations](#12-security-considerations)
- [Appendix A. Examples (Informative)](#appendix-a-examples-informative)
  - [A.1 A minimal spread](#a1-a-minimal-spread)
  - [A.2 A spread with a layout](#a2-a-spread-with-a-layout)
  - [A.3 A crossing card](#a3-a-crossing-card)
  - [A.4 A method restated in new words](#a4-a-method-restated-in-new-words)
  - [A.5 A repeating row and a pile](#a5-a-repeating-row-and-a-pile)
- [Appendix B. Reserved Names](#appendix-b-reserved-names)
- [Appendix C. Platform Conventions (Informative)](#appendix-c-platform-conventions-informative)
- [Appendix D. Changelog](#appendix-d-changelog)

## 1. Introduction

### 1.1 Scope and Design Goals

This specification defines a standard format for tarot spreads. A spread is what is on the table and what each place on it is for: a numbered list of positions, each with a label and optionally a meaning, and optionally a layout giving where each position lies and how it is turned.

> **A spread states the rule. It never performs the choice.**

The format is designed to:

- Give every position a permanent identifier, so that an esoterica source can attach a passage to it ([Esoterica Specification](#15-references) §3.3) and a reading can point at it.
- Carry a spread's layout as coordinates, so that it can be drawn with any deck and printed for a reader at a table, and never as a picture.
- Keep credit for a method apart from the licence over the words describing it, since the two routinely belong to different people.
- Provide a portable interchange format between tarot applications that implement this specification.

**Non-goals.** This specification does not define:

- **Readings.** A reading binds cards to positions. A spread holds no cards and names no card.
- **The draw.** Shuffling, randomness, reversal probability, significator selection and the choice of a card are outside this specification, as they are outside the [Esoterica Specification](#15-references)'s §1.1. A spread may state bounds a reader chooses within ([§6](#6-number-and-count)), and nothing in it chooses.
- **Drawings.** A spread file never holds a diagram or an image. Its coordinates are the whole of its layout ([§5](#5-layout)).
- **Decks.** A spread names no deck and is never invalid against one. Whether a spread can be dealt from a given deck is a question about a reading.
- **What a position means beyond its own words.** An esoterica source attaches passages to a position by its identifier. This specification defines the position and the [Esoterica Specification](#15-references) defines the attachment.
- **Discovery and installation.** How a spread arrives on a system is outside this specification, which describes only where an application looks for one ([§2.2](#22-the-spread-library)).

### 1.2 Document Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY" and "OPTIONAL" in this document are to be interpreted as described in BCP 14 ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) when, and only when, they appear in all capitals. Where this document writes "should", "must" or "may" in lower case, the word carries its ordinary English sense and imposes no requirement.

A section whose title carries the suffix (Informative) contains no requirements, and everything else in this document is normative. Whatever section they appear in, all **Notes** and all **Examples** are informative. Where an example appears to conflict with a normative rule, the rule governs and the example is in error.

This specification addresses three kinds of actors: authors who write a spread file, applications that read one in order to present it to a user or lay a reading out on it, and validation tools that check a spread file against this specification.

An author is whoever wrote the file. They may have devised the spread, or they may be restating someone else's method in their own words or transcribing someone else's. Where this document says a spread "declares" or "says" something, the author is who said it.

### 1.3 Terminology

| Term | Meaning |
| --- | --- |
| **author** | Whoever wrote a spread file ([§1.2](#12-document-conventions)). Named in `[meta].author` as who wrote its words ([§8.4](#84-credit)). |
| **card box** | The rectangle, one card unit wide and 1.76 card units tall, that a position's card is fitted inside ([§5.2](#52-the-card-box)). |
| **card unit** | The one unit of length in a spread file, on both axes: the width of the card box ([§5.1](#51-the-card-unit)). |
| **count** | How many cards a position takes, stated as bounds ([§6.2](#62-counts)). |
| **creator** | Who devised the spread's method, named in `[meta].creator` ([§8.4](#84-credit)). Not necessarily the author. |
| **layout** | The positions' centres, rotations and stacking: what any two faithful drawings of a spread agree on, up to translation and scale ([§5](#5-layout)). |
| **method** | How many positions a spread has, in what order, what each is for, and how they are laid out. Distinct from the **words** that describe it ([§8.1](#81-what-license-covers)). |
| **pile** | The cards laid on one place when a position's count allows more than one ([§6.2](#62-counts)). |
| **place** | Where one position is laid in one repetition. A spread with no repeating group has one place per position ([§6.3](#63-repeating-groups)). |
| **position** | One entry of the `[[positions]]` array: something a card is laid for, with an identifier, a label and optionally a meaning and a centre ([§4.2](#42-positions)). |
| **position identifier** | A position's permanent `id`, the fragment by which another document addresses it ([§3.2](#32-position-identifiers)). |
| **position number** | The number a reader sees beside a position: its ordinal in reading order, counting from 1 ([§6.1](#61-position-numbers)). |
| **qualified identifier** | An identifier naming an Arcana Land entity unambiguously across authors, defined by the [deck specification](#15-references) §3.3. |
| **reading** | Cards laid on a spread's places. Not described by this specification. |
| **repeating group** | A run of positions laid more than once, as a block ([§6.3](#63-repeating-groups)). |
| **spread** | A method for laying cards out, written as one file ([§2.1](#21-one-spread-one-file)). |
| **spread library** | An ordered list of **library roots**, each a directory searched for spread files ([§2.2](#22-the-spread-library)). |
| **words** | The strings a spread file carries: its name, description, labels and meanings ([§8.1](#81-what-license-covers)). |

### 1.4 Versioning and Compatibility

Every spread declares the version of this specification it is written against in `[meta].schema_version`. Its value MUST be `"<major>.<minor>"`: two decimal integers separated by a dot. The compatibility contract binds this specification, not any spread or application:

- A minor version update MUST be backward and forward compatible. It MAY add new tables, keys and values, and it MAY deprecate existing ones, but it MUST NOT change or remove the behavior of anything an earlier version of the same major version defined.
- A major version update MAY be incompatible in any respect.

Adding a value to one of this specification's registries, such as the [`took` values](#412-sources), is a minor version change, because an unregistered value is already legal and already ignored.

`[meta].version` is the spread file's own version and is unrelated to `schema_version`. It is a free-form string. This specification defines no syntax for it and no ordering over it, so applications MAY compare two values for equality to detect that a spread has changed, but MUST NOT infer from two values which is the later.

This specification's `schema_version` is independent of the deck specification's and the esoterica specification's.

### 1.5 References

The documents below are referenced normatively unless marked informative. A dated reference applies only to the edition cited, and an undated reference applies to the latest edition.

| Reference | Title | Where used |
| --- | --- | --- |
| **Tarot Deck Specification** | [DECK.md](https://github.com/arcanaland/specifications/blob/main/DECK.md), version 2.0 or later | [§3.1](#31-spread-identity), [§3.2](#32-position-identifiers), [§3.3](#33-grammar), [§4.1.2](#412-sources), [§10](#10-extensibility) |
| **BCP 14** | Key words for use in RFCs ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) | [§1.2](#12-document-conventions) |
| **TOML 1.0.0** | [toml.io/en/v1.0.0](https://toml.io/en/v1.0.0) | [§2.3](#23-file-format-and-encoding) |
| **RFC 5234** | Augmented BNF for Syntax Specifications: ABNF | [§3.3](#33-grammar) |
| **RFC 7405** | Case-Sensitive String Support in ABNF | [§3.3](#33-grammar) |
| **BCP 47** | Tags for Identifying Languages ([RFC 5646](https://www.rfc-editor.org/rfc/rfc5646)) | [§7](#7-localization) |
| **ISO 2108** | International Standard Book Number, with the freely available [ISBN Users' Manual](https://www.isbn-international.org/content/isbn-users-manual/29) | [§4.1.2](#412-sources) |
| **SPDX License List** | [spdx.org/licenses](https://spdx.org/licenses/), with the [license expression syntax](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/) | [§8](#8-licensing-and-credit) |
| **RightsStatements.org** | [Standardized international rights statements](https://rightsstatements.org/) | [§4.1.2](#412-sources) |
| **Esoterica Specification** (informative) | [ESOTERICA.md](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md) | [§1.1](#11-scope-and-design-goals), [§3.2](#32-position-identifiers), [§4.1.2](#412-sources) |
| **XDG Base Directory Specification** (informative) | [specifications.freedesktop.org](https://specifications.freedesktop.org/basedir-spec/latest/) | [Appendix C](#appendix-c-platform-conventions-informative) |

> Note: the esoterica specification is referenced **informatively**. It addresses a spread's positions; this specification needs nothing from it. A later version that lets a position draw from a named group of cards would make that reference normative, and this version reserves the key such a version would use ([Appendix B](#appendix-b-reserved-names)).

### 1.6 Licensing of This Specification (Informative)

This section describes the terms of the specification itself. It is not about the licensing of any spread, which [§8](#8-licensing-and-credit) covers.

The text of this document is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Its machine-facing parts are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) and the author asserts no copyright, database right, patent or trademark over them against anyone:

- the ABNF grammar of [§3.3](#33-grammar);
- the names, types, defaults and enumerated values of every table and key this document defines ([§4](#4-document-reference)), together with every registry of values it publishes, namely the `took` values of [§4.1.2](#412-sources);
- the card unit and card box of [§5](#5-layout);
- the reserved names of [Appendix B](#appendix-b-reserved-names);
- every example in this document.

No permission, notice, registration or fee is required to implement this specification, to publish spreads against it, to cross-reference or map its vocabulary to another scheme, or to build a competing specification on top of it, for any purpose, commercial or otherwise. The author irrevocably undertakes never to assert any such right against anyone who does.

See [LICENSING.md](https://github.com/arcanaland/specifications/blob/main/LICENSING.md) for the operative terms, which govern where this section and they disagree.

## 2. Spreads

### 2.1 One Spread, One File

A **spread** is one file. It has no assets and no directory of its own: a spread carries no image by design ([§1.1](#11-scope-and-design-goals)), and anything an application keeps beside a spread, such as notes or a thumbnail, is the application's own.

A spread is not scoped to a deck. Nothing in a spread file names a card, a suit or a deck, and a spread is read the same way whatever deck it is laid with.

### 2.2 The Spread Library

A **spread library** is an ordered list of **library roots**. Each root is a directory searched for spread files.

How an application determines its library roots is outside the scope of this specification. An application MAY derive them from platform conventions, from its own configuration or from the user. [Appendix C](#appendix-c-platform-conventions-informative) presents conventions in use on common platforms.

#### 2.2.1 Scanning

- Scanning a root is **recursive**. A spread may sit at any depth beneath a root.
- A regular file whose name ends in `.toml` is a candidate spread. An application MUST NOT require any other naming convention of it.
- A candidate that parses as TOML and carries a `[meta]` table with a `schema_version` key is a spread. A candidate that does not is not a spread, and an application MUST NOT report it as a malformed spread.
- A spread whose `schema_version` names a major version the application does not support is skipped. An application SHOULD report it rather than ignoring it silently.
- A spread that carries `[meta].schema_version` and fails any other rule of this specification is a malformed spread. Applications SHOULD report malformed spreads.

**A spread's location on disk is not derived from its identifier, and its identifier is not derived from its location.** An application MUST NOT compute one from the other.

The second rule is what keeps application-private spread formats apart from this one. A file with no top-level `[meta]` is not a spread under this specification, whatever else it carries, and is not reported. A spread root and an esoterica library root SHOULD NOT be the same directory, since a file under either specification is recognized by the same `[meta].schema_version` key.

#### 2.2.2 Shadowing

Roots are searched in order. Where two roots each contain a spread declaring the same `[meta].identifier`, the one in the earlier root wins and the later one is not reported. Where one root contains two files declaring the same identifier, which of them wins is not defined by this specification and a validator MUST report an error.

A spread that declares no identifier ([§3.1](#31-spread-identity)) shadows nothing and is shadowed by nothing.

### 2.3 File Format and Encoding

A spread file MUST be well-formed [TOML 1.0.0](https://toml.io/en/v1.0.0) encoded as UTF-8. Applications MAY skip a leading byte-order mark and a spread SHOULD NOT write one.

This specification defines **no path-valued field**. Nothing in a spread file names a file, so a spread cannot direct an application to read one.

A **number**, wherever this document gives a field that type, is a TOML integer or a TOML float, and MUST be finite. TOML admits `inf` and `nan` as floats, and neither is a number here ([§12](#12-security-considerations)).

## 3. Identity and Identifiers

### 3.1 Spread Identity

A spread MAY declare a **qualified identifier** in `[meta].identifier`, as defined by the deck specification §3.3: a realm and a slash-separated object path, with the first path segment naming an entity kind. A spread's type segment MUST be `spread`.

```
land.arcana/spread/celtic-cross
org.example/spread/the-lantern
id.example.shelf/spread/books/a-book-of-invented-spreads/the-hinge
```

The realm is controlled by whoever mints the identifier, which for a spread file is its author. A realm asserts control of a **name**, not authorship of the **method** it names: an author restating someone else's spread mints the identifier under their own realm and credits the method's creator in [`[meta].creator`](#84-credit).

A spread's `identifier` MUST NOT carry a fragment.

An identifier names the spread across all of its versions. An author who revises a spread MUST NOT change its `identifier` on account of the new `[meta].version`, and MUST mint a new identifier where the file has become a different spread rather than a new version of the same one.

`identifier` is OPTIONAL, because most spreads are written by a person in an application with no realm to write them under. A spread without one is conforming, and its positions cannot be addressed from another document ([§3.2](#32-position-identifiers)). Applications and validators MUST NOT synthesize one for a spread that lacks it.

**A name is not an identity.** Two spreads called *The Horseshoe* by two authors are two spreads, and nothing in this specification says that two spreads are the same one. There is no registry of canonical spreads.

### 3.2 Position Identifiers

Every position carries an `id`. It is REQUIRED, MUST be unique within the file, and MUST match the deck specification's `fragment` production ([§3.3](#33-grammar)): lowercase letters, digits, `.`, `_`, `-` and `:`.

A position identifier is what the fragment of a spread's qualified identifier names. `land.arcana/spread/celtic-cross#challenge` is the position whose `id` is `challenge` in the spread whose `identifier` is `land.arcana/spread/celtic-cross`, and it is how an esoterica source attaches a passage to that position ([Esoterica Specification](#15-references) §3.3).

**A position identifier is permanent.** An author revising a spread:

- MUST NOT change a position's `id` when its number, label, meaning or place changes;
- MUST NOT give an `id` to a position whose purpose is different from that of the position that carried it before; and
- MUST NOT reissue the `id` of a removed position.

A reissued identifier attaches every passage written for the old position to the new one, and nothing can detect it. These rules are what make `id` independent of number: an author who reorders positions after building a spread changes their numbers ([§6.1](#61-position-numbers)) and nothing that points at them.

**A position identifier is not a number and not a label**, and it is not for display. It is not derived from the label, because two positions of one spread can carry the same label; and it is not derived from the number, because numbers change when a spread is reordered.

A position in a [repeating group](#63-repeating-groups) has one identifier, which names it in every repetition.

[Groups](#43-groups) take identifiers from the same namespace: no group's `id` equals any position's `id`. This version defines a fragment as naming a position only.

### 3.3 Grammar

The productions below are [ABNF](https://www.rfc-editor.org/rfc/rfc5234) (RFC 5234), with the case-sensitive string notation of [RFC 7405](https://www.rfc-editor.org/rfc/rfc7405). Every string literal in this grammar is case-sensitive and lowercase.

`realm`, `segment`, `fragment` and `custom-name` are the productions of deck specification §3.5 and are used here unchanged. They are referenced rather than restated so that the two documents cannot drift apart.

```abnf
; ---- Spreads ----------------------------------------------------------

spread-id       = realm "/" %s"spread" 1*( "/" segment )

position-id     = fragment
position-ref    = spread-id "#" position-id

; ---- Credit -----------------------------------------------------------

took-value      = custom-name
```

`spread-id` is a deck specification `qualified-id` whose type segment is `spread` and which carries no fragment. `position-ref` is the same identifier with a position's `id` as its fragment.

Two constraints are not expressible in the grammar and are stated normatively:

- A `position-id` MUST be unique among the position and group identifiers of its file ([§3.2](#32-position-identifiers)).
- A `took-value` outside the registry of [§4.1.2](#412-sources) is legal, but SHOULD be prefixed `x_`.

## 4. Document Reference

Every table this specification defines is listed below with its fields.

A spread file has exactly four top-level names: the `[meta]` table, the `[[positions]]` and `[[groups]]` arrays of tables, and the `[app]` table. A top-level name outside these is not defined by this specification, and [§10](#10-extensibility) reserves such names for future versions of it. [Appendix B](#appendix-b-reserved-names) names one already.

### 4.1 `[meta]`

`[meta]` describes the spread: what it is called, who devised it, who wrote it and under what terms. It says nothing about any position.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `schema_version` | String | **Yes** | n/a | The version of this specification the spread is written against as `"<major>.<minor>"` ([§1.4](#14-versioning-and-compatibility)). |
| `name` | String | **Yes** | n/a | The spread's display name. Non-empty. |
| `identifier` | String | No | none | The spread's qualified identifier ([§3.1](#31-spread-identity)). |
| `description` | String | No | none | What the spread is for and how it is used, in plain text ([§4.1.1](#411-description)). |
| `version` | String | No | none | The spread file's own free-form version ([§1.4](#14-versioning-and-compatibility)). |
| `creator` | String | No | none | Who devised the spread's method ([§8.4](#84-credit)). |
| `author` | String | No | none | Who wrote this file's words ([§8.4](#84-credit)). |
| `sources` | Array of Table | No | `[]` | Where the spread came from, and what was taken from each ([§4.1.2](#412-sources)). |
| `default_language` | String | No | none | BCP 47 tag of the language this file's words are written in ([§7](#7-localization)). |
| `license` | String | No | none | SPDX license expression governing this file's words, and nothing else ([§8.1](#81-what-license-covers)). |
| `copyright` | String | No | none | Copyright notice over this file's words, displayed verbatim as the rights holder wrote it. |
| `attribution` | String | No | none | Credit line to display ([§8.4](#84-credit)). |
| `redistribution` | String | No | `"unstated"` | Whether the author passes on this file's words for republication ([§8.3](#83-redistribution-and-derivation)). |
| `derivation` | String | No | `"unstated"` | Whether the author passes on this file's words for making derived works, including translations ([§8.3](#83-redistribution-and-derivation)). |

**Two keys are required**, `schema_version` and `name`. Everything else describes a spread somebody may not know: a spread learned at a kitchen table has no creator anyone can name, no source and no licence, and is conforming.

#### 4.1.1 Description

`[meta].description` is plain text. Paragraphs are separated by a blank line and an application MUST preserve them. This specification defines no markup in it, and an application MUST NOT interpret any.

**The first paragraph is the spread's purpose**: one or two sentences on what the spread is for. An application with room for one line shows the first paragraph, and there is no separate key for it.

The rest of the description is how the spread is used, in the author's words. A spread whose procedure goes beyond laying one card on each place in order — a count the reader chooses, a group laid more than once, an exercise between two draws — SHOULD state that procedure here ([§6.4](#64-what-a-spread-does-not-state)), because the description is what a reader at a table and an application that implements nothing else will both see.

A position's `meaning` ([§4.2](#42-positions)) follows the same rules.

#### 4.1.2 Sources

`[meta].sources` says where a spread came from. Each entry describes one source, a book, a web page, a video or a teacher, and says what this file took from it.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | No | none | The source's title. |
| `author` | String | No | none | Who wrote or made the source. |
| `publisher` | String | No | none | The source's publisher. |
| `published_date` | String | No | none | When the source was published: the deck specification's `published-date` production, a year, optionally a month, optionally a day. |
| `isbn` | String | No | none | The source's ISBN, as printed, hyphens and all ([ISO 2108](#15-references)). |
| `url` | String (URI) | No | none | Where the source can be found. An absolute URL with a scheme of `http` or `https`. |
| `rights_status` | String (URI) | No | none | The copyright status of the source, as a [RightsStatements.org](https://rightsstatements.org/) or [Creative Commons](https://creativecommons.org/) URI. |
| `note` | String | No | none | Anything else a reader should know about this source, such as *coordinates measured from the diagram on p. 12*. |
| `took` | Array of String | No | `[]` | What this file took from the source, from the registry below. |

`name` through `rights_status` are the esoterica specification's [`[meta.work]`](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md#414-the-work-behind-a-source) keys, under the same names, with the same types and meanings, less its `type`, whose registry belongs to that specification. `published_date` is a TOML string; a bare `2019` is a TOML integer and is not this field.

**`took`** says what was taken. Its values come from the registry below.

| Value | What was taken |
| --- | --- |
| `positions` | How many positions there are, in what order, and what each is for |
| `layout` | Where the positions lie, how each is turned and what lies over what, up to translation and scale ([§5](#5-layout)) |
| `words` | The strings themselves: the name, description, labels or meanings, copied or translated |

The three are independent and a spread can take each from a different source. A spread that takes the positions and layout of a published method and describes them in new words takes `positions` and `layout` and not `words`, however close its new words come to the old ones: writing new text for the same purpose is not taking the words. **The claim is the author's** and nothing checks it.

There is no value for a drawing, because a spread file cannot hold one ([§1.1](#11-scope-and-design-goals)). Where a layout was measured from a diagram, `note` says so.

An entry with no `took`, or an empty one, credits a source and says nothing about what was taken from it. **A spread with no `sources` has made no claim** about where it came from, and a reader MUST NOT infer from the absence that the author devised it.

The `took` registry is open. An application MUST ignore a value it does not recognize and MUST NOT treat one as an error. A later version of this specification MAY add to the registry, so an author naming something no version defines SHOULD prefix the value, as in `x_purposes`. A validator warns about an unprefixed value outside the registry.

This version defines no meaning for the order of entries.

```toml
[[meta.sources]]
name = "A Book of Invented Spreads"
author = "Jane Doe"
publisher = "Example Press"
published_date = "2019"
took = ["positions", "layout"]
note = "Spacing rounded to the nearest quarter card from the diagram on p. 40."
```

### 4.2 `[[positions]]`

`[[positions]]` is the spread's positions, as an array of tables, **in reading order**. The first entry is position 1 ([§6.1](#61-position-numbers)). A spread has at least one position.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `id` | String | **Yes** | n/a | The position's permanent identifier ([§3.2](#32-position-identifiers)). |
| `label` | String | **Yes** | n/a | A short name for the position, such as *The choice* or *Past*. |
| `meaning` | String | No | none | What a card in this position is read as, in plain text ([§4.1.1](#411-description)). |
| `x` | Number | No | none | The horizontal centre of the position's card box, in card units ([§5](#5-layout)). |
| `y` | Number | No | none | The vertical centre of the position's card box, in card units, increasing downwards ([§5](#5-layout)). |
| `rotation` | Number | No | `0` | The position's turn in degrees clockwise, in (−90, 90] ([§5.3](#53-rotation)). |
| `z` | Integer | No | none | The position's place in the stacking order where it overlaps another ([§5.4](#54-stacking)). |
| `count` | Table | No | exactly one | How many cards the position takes ([§6.2](#62-counts)). |

**`label` is required and SHOULD NOT be empty.** It is what a reader sees, beside the position's number, at every place the spread is shown. An empty `label` is conforming and a validator warns about it.

**`label` and `meaning` are apart on purpose.** A label is short and a meaning is a paragraph; many published spreads print both, and an application with room for one shows the label. A spread that has only labels is ordinary.

**Geometry is all or nothing.** Either every position carries both `x` and `y`, or no position carries either ([§5.5](#55-a-spread-without-a-layout)). Absent is not zero.

```toml
[[positions]]
id = "choice"
label = "The choice"
meaning = "The decision as it stands, before anyone has argued with it."
x = 0.0
y = 0.0

[[positions]]
id = "light"
label = "What it lights"
x = 0.0
y = -2.0
```

### 4.3 `[[groups]]`

`[[groups]]` declares [repeating groups](#63-repeating-groups): runs of positions laid more than once, as a block. A spread with no group has no `[[groups]]`.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `id` | String | **Yes** | n/a | The group's identifier, from the same namespace as position identifiers ([§3.2](#32-position-identifiers)). |
| `positions` | Array of String | **Yes** | n/a | The identifiers of the positions the group repeats ([§6.3](#63-repeating-groups)). |
| `repeat` | Table | **Yes** | n/a | How many times the group is laid: `min` and `max`, both integers ([§6.3](#63-repeating-groups)). |
| `step` | Table | Where the spread has a layout | none | The offset of each repetition from the one before: `x` and `y`, both numbers, in card units ([§6.3](#63-repeating-groups)). |
| `label` | String | No | none | A short name for the group, for an application asking a reader how many times to lay it. |

## 5. Layout

A spread's **layout** is where its positions lie, how each is turned, and what lies over what. It is carried as numbers on each position: `x`, `y`, `rotation` and `z`. A spread file never carries a picture of its layout.

The layout is what any two faithful drawings of a spread agree on. **An application MAY translate and uniformly scale the whole layout to fit a surface, and MUST NOT scale one axis without the other, rotate it or mirror it**, since a Celtic Cross with its staff on the left is a different layout and a reader reads it differently.

### 5.1 The Card Unit

There is one unit of length, the **card unit**, on both axes. It is the width of the [card box](#52-the-card-box).

- `x` and `y` are the **centre** of a position's card box, in card units.
- `x` increases to the right and **`y` increases downwards**, as on a page or a screen.
- **The origin carries no meaning.** A spread whose positions are centred on (0, 0) and the same spread moved ten units to the right are the same layout. An author MAY place the origin wherever is convenient, and an application MUST NOT treat any position as special on account of its coordinates.

One unit on both axes is what lets a turned card have a footprint. A card crossing another at 90° has its width along `y`, and a unit that differed by axis would make its size depend on its rotation.

### 5.2 The Card Box

A position's **card box** is a rectangle 1 card unit wide and **1.76** card units tall, centred on the position's `x` and `y` and turned by its `rotation`. It is the card an author designs against.

A deck's cards are rarely exactly that shape. **An application lays a card inside the card box, scaled as large as fits while keeping the card's own aspect ratio, and centred in it.** A card taller in proportion than the box fills the box's height and is narrower than one unit; a card shorter in proportion fills its width and is shorter than 1.76.

This is the fit rule, and it is what makes one layout correct for every deck:

- Cards that do not overlap in the author's layout do not overlap with any deck, since every card fits inside a box that did not.
- The gaps the author saw are kept exactly only for a deck whose cards are the box's shape. A deck of a different shape shows wider gaps along one axis, never narrower ones.

> Note: 1.76 is the proportion of the cards most widely used to design spreads, to within the precision with which any published spread diagram can be measured. A spread measured from a diagram of narrower or wider cards loses nothing a reader at a table would notice.

### 5.3 Rotation

`rotation` is the position's turn, in degrees **clockwise** about its centre, with `y` downwards as in [§5.1](#51-the-card-unit). It is OPTIONAL and defaults to `0`, an upright card.

**Its range is (−90, 90]**: greater than −90 and at most 90. A card crossing another is at `90`.

**Rotation is not reversal.** A card turned 180° looks the same as a reversed card, so a spread that could state 180° would state something about the draw ([§1.1](#11-scope-and-design-goals)). A spread therefore states its positions' turns only up to a half turn. Whether a card laid in a reading is reversed is the reading's business, and an application that lays a reversed card turns it a further 180° on top of the position's `rotation`.

An application reading a `rotation` outside the range MUST normalize it by adding or subtracting a multiple of 180 until it falls in the range, and a validator warns about such a value. `270` is `-90` turned a half further, which is `90`; `350` is `-10`.

### 5.4 Stacking

Where two positions' card boxes overlap, `z` says which lies on top. A position with the greater `z` is laid over a position with the lesser one.

- `z` is OPTIONAL, and is an integer.
- **Only the relative order of `z` values means anything.** `1` and `2` say the same as `44` and `48`. An application MUST NOT give a `z` value any other meaning, and MAY renumber them on rewrite provided their order is kept.
- `z` is a fact about the layout and is not derived from the array's order, so that reordering positions for reading does not silently change which card covers which.

Two positions overlap when their card boxes, at their rotations, intersect in a region of positive area. Boxes that only touch do not overlap. **Two positions that overlap SHOULD both carry a `z`, with different values**, and a validator warns where they do not; an application laying such a pair out decides for itself which is on top. A validator MAY disregard an overlap too small for a reader to see, such as one arising from rounding.

### 5.5 A Spread Without a Layout

A spread MAY carry no layout at all. Then no position carries `x` or `y`. A `rotation` or `z` in such a spread has nothing to turn or stack, so an application ignores it and a validator warns about it.

A spread without a layout is not a defective spread. A reader at a table with a physical deck lays cards however the table allows, and a numbered list with labels and meanings is the whole of what they need.

An application presenting a spread without a layout MAY lay its positions out for display however it chooses, such as in a row or a list. **It MUST NOT write coordinates it chose into the spread** as though the author had stated them, since a spread with an invented layout is indistinguishable from one with a real one.

A spread that carries `x` and `y` on some positions and not others is malformed. A validator reports it as an error, and an application MAY treat such a spread as having no layout.

## 6. Number and Count

### 6.1 Position Numbers

**The array's order is the reading order, and a position's number is its ordinal in that order**, counting from 1. The number is not a key: reordering positions renumbers them, and their [identifiers](#32-position-identifiers) are unchanged.

An application presenting a spread SHOULD show each position's number. The number is also the order in which cards are laid, in this version.

Numbers do not follow geometry. Position 2 need not be beside position 1, and an application MUST NOT derive the order from the coordinates.

In a spread with a [repeating group](#63-repeating-groups), numbers count places rather than positions ([§6.3](#63-repeating-groups)).

### 6.2 Counts

A position takes **exactly one card** unless it declares a `count`.

```toml
count = { min = 1, max = 3 }
```

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `min` | Integer | **Yes** | n/a | The fewest cards the position takes. Zero or more. |
| `max` | Integer | No | no limit | The most cards the position takes. At least `min`, and at least 1. |

The cards a position takes are a **pile** on its place. They share the position's number, label and meaning, and are laid in turn. How a pile is fanned or stacked on its place is the application's to decide; the card box is where it lies.

A `min` of zero is a place that may stay empty, which is a reading the spread allows rather than a gap in one.

**Who picks the number is not stated**, and this is deliberate. The reader picks, within the bounds: a person at a table stopping when the question feels answered, or an application asking its user. A spread MUST NOT be read as asking for a random choice, and an application MUST NOT make one on its behalf unless its user asked it to ([§6.4](#64-what-a-spread-does-not-state)).

### 6.3 Repeating Groups

A **repeating group** is a run of positions laid more than once, as a block, such as a row laid one to four times.

```toml
[[groups]]
id = "row"
label = "A row"
positions = ["step", "cost"]
repeat = { min = 1, max = 4 }
step = { x = 0.0, y = -2.0 }
```

**Every place is in the file.** The positions a group lists are written out once as ordinary `[[positions]]` entries, with their full geometry, and they are the group's first repetition. Each later repetition is the same positions moved by `step` once more. So every place a spread can ever have is known before any card is drawn, from the file alone, and an application can draw all of them.

The rules:

- `positions` is non-empty. Its identifiers name positions in this file, and they are a **contiguous run of `[[positions]]`, listed in array order**.
- A position belongs to at most one group. Groups do not nest.
- `repeat.min` is zero or more. `repeat.max` is REQUIRED, is at least `repeat.min`, and is at least 1. A group with no upper bound would have places no one could draw.
- A group in a spread with a layout carries `step`, both `x` and `y`. Repetition *k*, counting the first as 0, lays each of the group's positions at its own `x` and `y` plus *k* times `step`. Its `rotation` and `count` are unchanged; its `z` is unchanged too, so repetitions that overlap one another are a spread an author SHOULD NOT write.
- A group in a spread without a layout carries no `step`.

**Numbers count places.** In reading order, the group's run of positions is laid once, then again for each further repetition, before the position that follows the run. A row of two positions after one opening position, laid three times, numbers 1; then 2, 3; 4, 5; 6, 7; and whatever follows is 8. A number after a group therefore depends on how many repetitions the reader chose, and an application assigns it when the reading is laid.

A group with `repeat.min` of zero may be laid no times. Its positions are still in the file and still drawn by an application showing the spread's possible places.

**Who picks the number of repetitions is not stated**, on the terms of [§6.2](#62-counts).

### 6.4 What a Spread Does Not State

A spread states bounds and never chooses within them. Nothing in a spread file, and nothing an application does on the file's behalf, shuffles, randomizes or selects a card, or picks a count or a number of repetitions. The party holding the deck does that: a person at a table, or an application acting on its user's instruction.

This version states no procedure beyond laying cards on places in reading order, within the counts and repetitions above. **Everything else a spread asks of a reader is written in its [description](#411-description)**, in words:

- Which cards a position draws from, such as *the Major Arcana only*.
- A step that depends on a card already drawn, such as *keep drawing until an Ace*, or *if the first card is a Major, draw two more*.
- A reading technique that runs over the laid cards, such as counting along them by value.
- An action that draws nothing, such as an exercise between two draws, or setting a card aside by hand before the deal.

A later version of this specification may give some of these a structure, and this version reserves the names it would use ([Appendix B](#appendix-b-reserved-names)). Any structure it adds will keep the rule above.

## 7. Localization

`[meta].default_language` names the language of the file's words, its name, description, labels, meanings and group labels, as a well-formed [BCP 47](https://www.rfc-editor.org/rfc/rfc5646) tag. Tags SHOULD be canonical, using the shortest available ISO 639 subtag (`en`, not `eng`), lowercase language, titlecase script and uppercase region, and applications MUST compare them case-insensitively.

It is OPTIONAL and has **no default**. A spread that declares none has not said what language it is written in, and an application MUST NOT assume one.

This version defines no way for one spread file to translate another. A translated spread is a spread file in its own right, with its own author and its own terms, which credits the spread it translates in [`sources`](#412-sources) with `took` including `words`, since a translation takes the words ([§4.1.2](#412-sources)). It has its own identifier where it has one, and its positions are not the original's: a passage attached to `#challenge` in one is not attached to `#challenge` in the other.

## 8. Licensing and Credit

A spread is two things that are frequently owned by different people: a **method**, which is how many positions there are, in what order, for what, laid out how; and the **words** a particular file uses to describe it. This section keeps them apart.

- `[meta].license` covers the words ([§8.1](#81-what-license-covers)).
- `[meta].creator` credits the method, and `[meta].author` credits the words ([§8.4](#84-credit)).
- `[meta].sources` says where each part came from ([§4.1.2](#412-sources)).

### 8.1 What `license` Covers

**`license` covers the words a spread file carries and nothing else.** It does not cover the number of positions, their order, their coordinates or the purpose of a position, which are not anybody's expression. A file that restates another author's method in its own words owes that author a `creator` credit and needs no licence from them to do so.

A spread file therefore never carries a licence over its layout, and an author MUST NOT write `license` as though it granted or withheld one.

Nothing here is a legal determination and this specification does not make one.

### 8.2 License Expressions

`[meta].license`, where present, SHOULD be a valid [SPDX license expression](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/), and identifiers in it MUST come from the [SPDX License List](https://spdx.org/licenses/) and are case-sensitive. For terms with no SPDX identifier, use a `LicenseRef-` string.

`license` is OPTIONAL. **A spread that declares none grants nothing**: absence is not a dedication to the public domain, and an application MUST NOT read it as one. A validator warns about an absent `license`, because a spread file with no stated terms is one nobody downstream can safely share.

### 8.3 Redistribution and Derivation

| Value | Meaning |
| --- | --- |
| `"full"` | The words may be passed on as they are. |
| `"none"` | The words may not be passed on. |
| `"unstated"` | The default. The author has not said. |

`redistribution` governs republishing this file's words. `derivation` governs making new work from them, **which includes translating them** ([§7](#7-localization)). Neither governs the method, which [§8.1](#81-what-license-covers) puts outside any licence.

The default `"unstated"` does not grant permission. An application MUST NOT read it as `"full"`, and one that redistributes spreads on a user's behalf SHOULD treat `"unstated"` as it treats `"none"`.

These fields describe what the author passes on. They do not enlarge what the author had: a `redistribution = "full"` on words taken from a book in copyright is the author claiming something they cannot give.

### 8.4 Credit

Three fields credit people, and none of them is a licence.

| Field | Who |
| --- | --- |
| `creator` | Who devised the spread's method: its positions, their purposes and its layout |
| `author` | Who wrote this file's words |
| `sources` | Where the method, the layout or the words came from, and which ([§4.1.2](#412-sources)) |

**Credit is not licence.** `creator` survives when the words and the licence are gone: a spread rebuilt in new words under `CC0-1.0` has a new `author` and a new `license`, and the only field left to say whose method it is is `creator`. It asserts no right and nothing checks it.

Where one person devised the spread and wrote the file, the file SHOULD name them once, in `creator`, and MAY omit `author`. Where the two differ, a file SHOULD name both.

**Presentation.** An application presenting a spread SHOULD show its `creator` and `sources` where they are present, and SHOULD show `attribution` where it is present, preferring it to anything composed from the other fields. Two rules are stated because an application could otherwise say something false:

- An application MUST NOT present a spread's words as written by a source's `author` unless that source's `took` includes `words`. A method restated in new words is *based on* that source and not *by* its author.
- An application MUST NOT present a spread's words as written by its `creator` where the spread names a different `author`.

A credit written only in `description` is not a credit an application can show as one. An author SHOULD move it into these fields, and MAY leave the prose as well.

## 9. Presenting a Spread

An application presenting a spread:

- SHOULD show each position's number and label ([§6.1](#61-position-numbers)), and SHOULD make its meaning available where present.
- SHOULD show the first paragraph of `description` as the spread's purpose where it shows the spread in a list ([§4.1.1](#411-description)).
- MUST NOT show a position's `id` as though it were a label or a number. An identifier is for other documents to point at ([§3.2](#32-position-identifiers)).
- MUST NOT require a deck to present a spread, and MUST NOT refuse a spread because a deck has fewer cards than the spread has places. Whether to deal a reading short is a question about the reading.
- Where the spread has a layout, lays positions out by [§5](#5-layout), and where it has none, by [§5.5](#55-a-spread-without-a-layout).
- Where it lays a reading, places cards in reading order ([§6.1](#61-position-numbers)) and asks its user for any count or number of repetitions the spread leaves open ([§6.4](#64-what-a-spread-does-not-state)).

## 10. Extensibility

The `[app]` table is reserved for applications to record data about a spread that this specification does not model. Each application takes a subtable keyed by a [realm](https://github.com/arcanaland/specifications/blob/main/DECK.md#33-qualified-identifiers):

```toml
[app."land.arcana.tarotcanvas"]
version = 1
```

The subtable key MUST be written as a quoted TOML key because a realm always contains a `.` character.

Applications MUST ignore any `[app]` subtable they do not own, and validators MUST NOT report unknown keys within `[app]`.

An application that rewrites a spread file SHOULD preserve every table, key and value it does not understand, including keys inside `[meta]`, `[[positions]]` and `[[groups]]`. A key a later version defines, or a key an author added by hand, then survives an older application's save.

Top-level names outside those of [§4](#4-document-reference) are reserved for future versions of this specification.

## 11. Conformance and Validation

### 11.1 Conforming Spread

A conforming spread:

- MUST be a readable file well-formed under [§2.3](#23-file-format-and-encoding).
- MUST contain a `[meta]` table carrying the two required fields of [§4.1](#41-meta).
- MUST contain at least one position.
- MUST produce no errors under [§11.4](#114-validation-rules).

### 11.2 Errors and Warnings

A validator reports two kinds of violations. An error makes a spread non-conforming and an application MAY refuse it. A warning marks something an author probably did not intend, or a condition this specification allows but has an opinion about. An application MUST load a spread that produces only warnings.

### 11.3 Conforming Applications and Validators

A conforming application:

- MUST implement scanning ([§2.2.1](#221-scanning)) and shadowing ([§2.2.2](#222-shadowing)) over whatever roots it uses.
- MUST read positions in array order and number them by [§6.1](#61-position-numbers).
- MUST apply the card box and fit rule ([§5.2](#52-the-card-box)) wherever it lays a card on a spread with a layout, and MUST normalize `rotation` ([§5.3](#53-rotation)).
- MUST NOT write coordinates it chose into a spread without a layout ([§5.5](#55-a-spread-without-a-layout)).
- MUST NOT make a choice a spread leaves to its reader on the spread's behalf ([§6.4](#64-what-a-spread-does-not-state)).
- MUST ignore `[app]` subtables it does not own ([§10](#10-extensibility)), and every table, key and value this specification does not define.
- MUST NOT reject a spread for warnings ([§11.2](#112-errors-and-warnings)).

An application need not implement counts or repeating groups. Where it does not, it lays one card on each position, lays each group once, and shows the spread's description, which states the rest ([§6.4](#64-what-a-spread-does-not-state)).

An application MAY decline to open a spread larger than it can afford to lay out, such as one with more places than it can draw. Declining is not a finding that the spread is non-conforming, and a validator does not report size ([§12](#12-security-considerations)).

A conforming validator implements the rules in [§11.4](#114-validation-rules).

### 11.4 Validation Rules

Each rule is labeled **E** for error or **W** for warning.

| | Rule |
| --- | --- |
| **E** | The file is valid TOML 1.0.0 encoded as UTF-8 and carries a `[meta]` table ([§2.3](#23-file-format-and-encoding)). |
| **E** | `[meta]` carries `schema_version` and `name`, and `name` is non-empty ([§4.1](#41-meta)). |
| **E** | `[meta].schema_version` has the form [§1.4](#14-versioning-and-compatibility) requires. |
| **E** | Every key [§4](#4-document-reference) defines carries a value of the type its field table gives. A key this specification does not define is [ignored](#10-extensibility) rather than typed. |
| **E** | Every top-level name is `meta`, `positions`, `groups` or `app`, or the reserved `deal` ([§4](#4-document-reference), [Appendix B](#appendix-b-reserved-names)). |
| **E** | Every number is finite ([§2.3](#23-file-format-and-encoding)). |
| **E** | `[meta].identifier`, where present, is a well-formed `spread-id`: a qualified identifier whose type segment is `spread`, carrying no fragment ([§3.1](#31-spread-identity)). |
| **E** | Where a validator can see a whole library, no two spreads within one root declare the same `[meta].identifier` ([§2.2.2](#222-shadowing)). |
| **W** | Where a validator can see a whole library, no two visible spreads declare the same `[meta].identifier`. The earlier root wins ([§2.2.2](#222-shadowing)). |
| **E** | `[[positions]]` has at least one entry ([§4.2](#42-positions)). |
| **E** | Every position carries `id` and `label`, both strings ([§4.2](#42-positions)). |
| **E** | Every position `id` and every group `id` is a well-formed `position-id`, and no two of them, across positions and groups, are equal ([§3.2](#32-position-identifiers)). |
| **W** | A position whose `label` is empty ([§4.2](#42-positions)). |
| **E** | Either every position carries both `x` and `y`, or no position carries either ([§4.2](#42-positions), [§5.5](#55-a-spread-without-a-layout)). |
| **W** | A `rotation` or `z` on a position of a spread without a layout. Neither has anything to apply to ([§5.5](#55-a-spread-without-a-layout)). |
| **W** | A `rotation` outside (−90, 90]. An application normalizes it ([§5.3](#53-rotation)). |
| **W** | Two places whose card boxes overlap, at their rotations and including every repetition of a repeating group up to its `repeat.max`, where the two positions do not both carry a `z` with different values ([§5.4](#54-stacking)). |
| **E** | A position's `count`, where present, carries an integer `min` of zero or more, and its `max`, where present, is an integer of at least `min` and at least 1 ([§6.2](#62-counts)). |
| **E** | Every group carries `id`, `positions` and `repeat`. `positions` is a non-empty array naming positions of this file, which form a contiguous run of `[[positions]]` listed in array order ([§6.3](#63-repeating-groups)). |
| **E** | No position is named by more than one group ([§6.3](#63-repeating-groups)). |
| **E** | A group's `repeat` carries an integer `min` of zero or more and an integer `max` of at least `min` and at least 1 ([§6.3](#63-repeating-groups)). |
| **E** | A group in a spread with a layout carries `step`, with numbers `x` and `y` ([§6.3](#63-repeating-groups)). |
| **W** | A group in a spread without a layout that carries `step`, which has nothing to apply to ([§6.3](#63-repeating-groups)). |
| **W** | A spread using `count` or `[[groups]]` with no `description`. The procedure is written nowhere a reader at a table can see it ([§4.1.1](#411-description)). |
| **E** | Every `[meta].sources` entry is a table. Its `published_date`, where present, is a `published-date` string denoting a real calendar date, and its `url`, where present, is absolute with an `http` or `https` scheme ([§4.1.2](#412-sources)). |
| **W** | A `took` value outside the registry of [§4.1.2](#412-sources) that is not prefixed `x_`. Applications ignore it, and a later version of this specification may claim the name. |
| **W** | A `[meta].sources` entry whose `rights_status` is not a RightsStatements.org or Creative Commons URI ([§4.1.2](#412-sources)). |
| **W** | A `[meta].sources` entry whose `isbn` is not ten or thirteen characters once hyphens and spaces are removed, or whose check digit does not verify ([§4.1.2](#412-sources)). |
| **E** | `[meta].default_language`, where present, is a well-formed BCP 47 language tag ([§7](#7-localization)). |
| **W** | No `[meta].license`. The spread grants nothing ([§8.2](#82-license-expressions)). |
| **W** | A `license` that is not a well-formed SPDX license expression. A spread that fails this check MUST NOT be rejected ([§8.2](#82-license-expressions)). |
| **E** | `redistribution` and `derivation`, where present, are one of `full`, `none` or `unstated` ([§8.3](#83-redistribution-and-derivation)). |
| **E** | Every `[app]` subtable key is a well-formed realm, in particular one with two labels or more ([§10](#10-extensibility)). The contents of such a subtable are the owning application's to define and are not validated. |
| **W** | A `from` key on a position, or a top-level `deal`. Both are reserved for a later version, and an application ignores them ([Appendix B](#appendix-b-reserved-names)). |

## 12. Security Considerations

A spread arrives from outside the system and carries text and numbers an author can abuse.

**Untrusted text.** Every string in a spread is attacker-controlled and is destined for a display surface. An application that renders a spread's words into a terminal MUST restrict the escape sequences it passes through, since a hostile spread can carry OSC 52 sequences that clobber the user's clipboard, or sequences that induce the terminal to write attacker-chosen bytes to the application's standard input. An application that renders them into HTML or any other markup MUST escape them; a spread's words are plain text and this specification defines no markup in them.

**Untrusted numbers.** TOML admits `inf` and `nan` as floats, and some TOML readers accept integers wider than 64 bits. None is a conforming value ([§2.3](#23-file-format-and-encoding)), and an application MUST check every number before using it as a coordinate, an angle or a count. An application SHOULD bound the magnitude of a coordinate it will lay out, since a finite but enormous one can exhaust a renderer as surely as an infinite one.

**Unbounded counts.** A `count` with no `max` takes any number of cards, and a group's `repeat.max` may be large. Nothing in a spread lays a card by itself ([§6.4](#64-what-a-spread-does-not-state)), so neither can run away on its own, but an application drawing every possible place, or asking its user for a count, SHOULD bound what it will draw or accept.

**No file references.** This specification defines no path-valued field ([§2.3](#23-file-format-and-encoding)), so a spread cannot direct an application at a file. An application MUST NOT interpret any value in a spread as a path.

**No fetching.** Qualified identifiers are names and not locations. An application MUST NOT dereference one over the network. A source's `url` is for a user to follow deliberately, never automatically.

**Resource bounds.** Recursive scanning ([§2.2.1](#221-scanning)) walks a user-controlled directory tree. An application SHOULD bound the depth it descends, the number of files it opens and the size of a file it will parse, and SHOULD NOT follow symbolic links out of a library root.

## Appendix A. Examples (Informative)

Every spread, name and string below is invented for this document.

### A.1 A minimal spread

Everything required and nothing else. No layout, no credit and no terms, and conforming, though a validator warns that it states no licence.

```toml
[meta]
schema_version = "1.0"
name = "Three Questions"

[[positions]]
id = "where"
label = "Where am I standing?"

[[positions]]
id = "what"
label = "What am I carrying?"

[[positions]]
id = "next"
label = "Where does this road go?"
```

### A.2 A spread with a layout

A spread its author devised and wrote, with a layout. Two positions are turned. Nothing overlaps, so there is no `z`.

```toml
[meta]
schema_version = "1.0"
identifier = "org.example/spread/the-lantern"
name = "The Lantern"
description = """
For a decision that is already made and needs checking.

Lay the first card for the choice. The other three ring it, the light above and
the two shadows below."""
creator = "Jane Doe"
license = "CC0-1.0"
default_language = "en"

[[positions]]
id = "choice"
label = "The choice"
x = 0.0
y = 0.0

[[positions]]
id = "light"
label = "What it lights"
meaning = "What becomes easier because of the choice."
x = 0.0
y = -2.0

[[positions]]
id = "shadow"
label = "What it hides"
x = -1.3
y = 1.0
rotation = -30.0

[[positions]]
id = "fuel"
label = "What keeps it burning"
x = 1.3
y = 1.0
rotation = 30.0
```

An esoterica source can attach a passage to the third position as `group."org.example/spread/the-lantern#shadow"`.

### A.3 A crossing card

The second card lies across the first, so the two overlap and both carry a `z`. Their numbers come from the array, and the covering card is numbered second.

```toml
[meta]
schema_version = "1.0"
name = "The Knot"
description = "Two forces at work in one situation, and what loosens them."
creator = "A. Writer"
license = "CC-BY-4.0"

[[positions]]
id = "heart"
label = "The heart of it"
x = 0.0
y = 0.0
z = 1

[[positions]]
id = "across"
label = "What crosses it"
x = 0.0
y = 0.0
rotation = 90.0
z = 2

[[positions]]
id = "loosens"
label = "What loosens the knot"
x = 2.2
y = 0.0
```

### A.4 A method restated in new words

The positions and layout are an invented book's, and every word in the file is new. `creator` names who devised the method; `author` names who wrote this file; the source says what was taken and what was not. The licence covers this file's words only.

```toml
[meta]
schema_version = "1.0"
identifier = "id.example/spread/the-bridge"
name = "The Bridge"
description = """
For moving from one situation to another.

Three cards on each bank and one for the crossing. Read the near bank left to
right, then the crossing, then the far bank."""
creator = "A. Writer"
author = "Jane Doe"
license = "CC-BY-SA-4.0"
attribution = "The Bridge, after A. Writer; words by Jane Doe, CC BY-SA 4.0."

[[meta.sources]]
name = "A Book of Invented Spreads"
author = "A. Writer"
publisher = "Example Press"
published_date = "2019"
isbn = "978-0-00-000000-0"
took = ["positions", "layout"]
note = "Spacing measured from the book's diagram and rounded to a quarter card."

[[positions]]
id = "near.ground"
label = "Where I stand"
x = -3.0
y = -2.0

[[positions]]
id = "near.weight"
label = "What I bring"
x = -3.0
y = 0.0

[[positions]]
id = "near.leave"
label = "What I leave"
x = -3.0
y = 2.0

[[positions]]
id = "crossing"
label = "The crossing"
x = 0.0
y = 0.0
rotation = 90.0

[[positions]]
id = "far.ground"
label = "Where I land"
x = 3.0
y = -2.0

[[positions]]
id = "far.find"
label = "What I find"
x = 3.0
y = 0.0

[[positions]]
id = "far.become"
label = "Who I become"
x = 3.0
y = 2.0
```

An application presenting this spread may say it is *based on* A. Writer's method and *by* Jane Doe. It may not say the words are A. Writer's, since the source's `took` does not include `words`.

### A.5 A repeating row and a pile

A question card, then a row of two laid one to four times upward, then a pile of one to three cards for what remains. The description says how the reader decides, because the file does not.

```toml
[meta]
schema_version = "1.0"
name = "The Ladder"
description = """
For a long goal taken one step at a time.

Lay the question. Then lay a rung: a step and what it costs. Lay another rung
above it, and another, until the question feels answered or you have four.
Finish with one to three cards for what is still out of reach, as many as feel
needed."""
creator = "Jane Doe"
license = "CC0-1.0"

[[positions]]
id = "question"
label = "The question"
x = 0.0
y = 0.0

[[positions]]
id = "step"
label = "A step"
x = -0.7
y = -2.0

[[positions]]
id = "cost"
label = "What it costs"
x = 0.7
y = -2.0

[[positions]]
id = "beyond"
label = "Still out of reach"
x = 2.5
y = 0.0
count = { min = 1, max = 3 }

[[groups]]
id = "rung"
label = "A rung"
positions = ["step", "cost"]
repeat = { min = 1, max = 4 }
step = { x = 0.0, y = -2.0 }
```

Laid with three rungs, the question is 1; the rungs are 2 and 3, 4 and 5, 6 and 7; and the pile is 8, whether it holds one card or three. An application that implements neither counts nor groups lays one rung and one card for the pile, and shows the description.

## Appendix B. Reserved Names

The names below are reserved for a later version of this specification. A 1.0 spread SHOULD NOT carry them, an application MUST ignore them in a 1.0 spread, and an application that rewrites a spread SHOULD preserve them ([§10](#10-extensibility)).

| Name | Reserved for |
| --- | --- |
| `from`, on a position | The set of cards a position draws from, such as the Major Arcana only. It would name one of the esoterica specification's builtin groups, which would make that specification a normative reference ([§1.5](#15-references)) |
| `[[deal]]` at the top level | An order of laying cards other than reading order, including steps that depend on a card already drawn ([§6.4](#64-what-a-spread-does-not-state)) |

The names below are spellings an application-private spread format wrote before this specification existed. A 1.0 spread does not carry them, and a 1.0 reader that finds one reports the file's top-level names as [§11.4](#114-validation-rules) requires rather than reading them.

| Name | Was | In this specification |
| --- | --- | --- |
| `name`, `description` at the top level | The spread's name and description | [`[meta].name`](#41-meta) and [`[meta].description`](#411-description) |
| `[[sources]]` at the top level | Where the spread came from | [`[[meta.sources]]`](#412-sources) |
| `year` in a source | An integer year of publication | [`published_date`](#412-sources), a string admitting a year, a month or a day |
| `rotation` in [0, 360) | A turn of up to a full circle | (−90, 90], with normalization ([§5.3](#53-rotation)) |
| `z` on every position | Stacking, written whether or not anything overlapped | `z` only where positions overlap ([§5.4](#54-stacking)) |

## Appendix C. Platform Conventions (Informative)

This appendix records where applications conventionally look for spreads on common platforms. [§2.2](#22-the-spread-library) leaves the choice of library roots to the application and this section provides recommendations. It mirrors the deck specification's Appendix D, with `spreads` in place of `decks`.

**Linux.** Follow the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/) and search `$XDG_DATA_HOME/tarot/spreads` first, then `<dir>/tarot/spreads` for each `<dir>` in `$XDG_DATA_DIRS`. Where `$XDG_DATA_HOME` is unset or empty it defaults to `$HOME/.local/share`, and where `$XDG_DATA_DIRS` is unset or empty it defaults to `/usr/local/share:/usr/share`.

**macOS.** `~/Library/Application Support/tarot/spreads`, then `/Library/Application Support/tarot/spreads`.

**Windows.** `%LOCALAPPDATA%\tarot\spreads`, then `%PROGRAMDATA%\tarot\spreads`.

Because scanning is recursive ([§2.2.1](#221-scanning)), a user may arrange spreads beneath these roots however they like.

## Appendix D. Changelog

### Version 1.0

The first version of this specification. It is derived from the spreads people have actually written: about eighty-four, holding about 670 positions, from at least sixteen hands, including a published compendium, a second application's library converted, and the files written by the first application to store spreads.

**Newly specified.**

- [Spread files](#21-one-spread-one-file), one spread to a file, with no assets, discovered by [recursive scan](#22-the-spread-library) and told apart from application-private formats by `[meta].schema_version`.
- [Spread identity](#31-spread-identity) under the `spread` type segment the deck specification reserved, and [permanent position identifiers](#32-position-identifiers) that are the fragment an esoterica source addresses.
- [Positions](#42-positions) in reading order, each with a required label and an optional meaning.
- A [layout](#5-layout) in one card unit on both axes, with a [card box](#52-the-card-box) and a fit rule that makes one layout correct for every deck, a [rotation](#53-rotation) that cannot express reversal, and [stacking](#54-stacking) only where cards overlap. A spread may have [no layout](#55-a-spread-without-a-layout) at all.
- [Counts](#62-counts) and [repeating groups](#63-repeating-groups), stated as bounds, with every place written in the file.
- [Credit apart from licence](#8-licensing-and-credit): `creator` for the method, `author` for the words, `sources` with what was taken from each, and a `license` that covers the words only.
- [Conformance and validation](#11-conformance-and-validation), with an enumerated rule set, and [security considerations](#12-security-considerations).
