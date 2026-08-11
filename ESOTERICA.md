# Tarot Esoterica Specification

> Maintained By: [Arcana Land](https://github.com/arcanaland)
>
> Version: 1.0 (draft)

## Table of Contents

- [1. Introduction](#1-introduction)
  - [1.1 Scope and Design Goals](#11-scope-and-design-goals)
  - [1.2 Document Conventions](#12-document-conventions)
  - [1.3 Terminology](#13-terminology)
  - [1.4 Versioning and Compatibility](#14-versioning-and-compatibility)
  - [1.5 References](#15-references)
  - [1.6 Licensing of This Specification (Informative)](#16-licensing-of-this-specification-informative)
- [2. Sources](#2-sources)
  - [2.1 One Source, One File](#21-one-source-one-file)
  - [2.2 The Esoterica Library](#22-the-esoterica-library)
    - [2.2.1 Scanning](#221-scanning)
    - [2.2.2 Shadowing](#222-shadowing)
  - [2.3 File Format and Encoding](#23-file-format-and-encoding)
- [3. Identity and Identifiers](#3-identity-and-identifiers)
  - [3.1 Source Identity](#31-source-identity)
  - [3.2 Card References](#32-card-references)
  - [3.3 Group Identifiers](#33-group-identifiers)
  - [3.4 Grammar](#34-grammar)
  - [3.5 Identifiers in TOML](#35-identifiers-in-toml)
- [4. Document Reference](#4-document-reference)
  - [4.1 `[meta]`](#41-meta)
    - [4.1.1 Source Type](#411-source-type)
    - [4.1.2 Citation](#412-citation)
    - [4.1.3 Published Date](#413-published-date)
  - [4.2 Targets](#42-targets)
  - [4.3 Slots](#43-slots)
  - [4.4 Builtin Groups](#44-builtin-groups)
    - [4.4.1 Group Membership](#441-group-membership)
  - [4.5 Author-Defined Groups](#45-author-defined-groups)
- [5. Passages](#5-passages)
  - [5.1 Passage Keys and Values](#51-passage-keys-and-values)
  - [5.2 The Passage Registry](#52-the-passage-registry)
  - [5.3 Divinatory Passages](#53-divinatory-passages)
- [6. Correspondences](#6-correspondences)
  - [6.1 Correspondence Values](#61-correspondence-values)
  - [6.2 The Correspondence Registry](#62-the-correspondence-registry)
- [7. Localization](#7-localization)
  - [7.1 Overlay Files](#71-overlay-files)
  - [7.2 Language Resolution](#72-language-resolution)
- [8. Licensing and Attribution](#8-licensing-and-attribution)
  - [8.1 License Expressions](#81-license-expressions)
  - [8.2 Rights Status](#82-rights-status)
  - [8.3 Redistribution and Derivation](#83-redistribution-and-derivation)
  - [8.4 Attribution in Presentation](#84-attribution-in-presentation)
- [9. Presenting a Source](#9-presenting-a-source)
  - [9.1 Sources Do Not Merge](#91-sources-do-not-merge)
  - [9.2 Group Content](#92-group-content)
- [10. Extensibility](#10-extensibility)
- [11. Conformance and Validation](#11-conformance-and-validation)
  - [11.1 Conforming Source](#111-conforming-source)
  - [11.2 Errors and Warnings](#112-errors-and-warnings)
  - [11.3 Conforming Applications and Validators](#113-conforming-applications-and-validators)
  - [11.4 Validation Rules](#114-validation-rules)
- [12. Security Considerations](#12-security-considerations)
- [Appendix A. Examples (Informative)](#appendix-a-examples-informative)
  - [A.1 A minimal source](#a1-a-minimal-source)
  - [A.2 A book, with the shape a book tends to have](#a2-a-book-with-the-shape-a-book-tends-to-have)
  - [A.3 A tradition](#a3-a-tradition)
  - [A.4 A transcription of a work in copyright](#a4-a-transcription-of-a-work-in-copyright)
  - [A.5 A custom group and a spread position](#a5-a-custom-group-and-a-spread-position)
  - [A.6 A French overlay of A.2](#a6-a-french-overlay-of-a2)
- [Appendix B. Reserved and Deprecated Names](#appendix-b-reserved-and-deprecated-names)
- [Appendix C. Platform Conventions (Informative)](#appendix-c-platform-conventions-informative)
- [Appendix D. Changelog](#appendix-d-changelog)

## 1. Introduction

### 1.1 Scope and Design Goals

This specification defines a standard format for **tarot esoterica**: what a book, an article, a web page or a body of practice says about the cards. Where the [Tarot Deck Specification](#15-references) covers a deck's presentation — its images and the names printed on them — this one covers meaning and correspondence.

The format is designed to:

- Make **the source** the unit of the file, so that one work is one document carrying one attribution and one license.
- Address cards and groups of cards through the canonical identifiers of the deck specification, so that esoterica and decks describe the same objects.
- Keep everything a source says about one card contiguous, because these documents are written by hand.
- Distinguish text written to be read from values drawn from a system outside this specification.
- Stay finishable, by fixing a small registry of keys with a stated process for adding to it rather than admitting anything.

A document under this specification is a static file. It transports what a source says and computes nothing from it.

**Non-goals.** This specification does not define:

- **The draw.** Shuffling, randomness, seeds, reversal probability and significator selection are outside this specification and every Arcana Land specification. An application may do these things; nothing here describes them, and no field in a document under this specification is an input to them.
- **Merging.** Two sources that disagree about a card are two sources that disagree ([§9.1](#91-sources-do-not-merge)). This specification defines no precedence between them and no rule for combining them into one answer.
- **Reversals.** No key of this version distinguishes an upright meaning from a reversed one. A source that draws the distinction states it in its own keys ([§5.1](#51-passage-keys-and-values)).
- **Spread geometry.** A spread's positions and layout belong to the Spread Specification. This specification attaches meaning to a position that specification defines ([§3.3](#33-group-identifiers)).
- **Discovery and installation.** How a source arrives on a system is outside this specification, which describes only where an application looks for one ([§2.2](#22-the-esoterica-library)).

### 1.2 Document Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY" and "OPTIONAL" in this document are to be interpreted as described in BCP 14 ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) when, and only when, they appear in all capitals. Where this document writes "should", "must" or "may" in lower case, the word carries its ordinary English sense and imposes no requirement.

A section whose title carries the suffix (Informative) contains no requirements, and everything else in this document is normative. Whatever section they appear in, all **Notes** and all **Examples** are informative. Where an example appears to conflict with a normative rule, the rule governs and the example is in error.

This specification addresses three kinds of actors: **authors** who write a document and arrange its content, **applications** that read a document in order to present it to a user, and **validation tools** that check a document against this specification.

An author is whoever assembled the document. They may be the writer of the text it carries, a translator, or a third party transcribing a published work they did not write. Where this document says a source "declares" or "says" something, the author is who said it.

### 1.3 Terminology

| Term | Meaning |
| --- | --- |
| **author** | Whoever assembled a source document. Not necessarily the writer of the text in it ([§1.2](#12-document-conventions)). |
| **builtin family** | One of the six reserved names under `group` that names a family of card groups: `all`, `arcana`, `classes`, `suits`, `ranks` and `custom` ([§4.4](#44-builtin-groups)). |
| **canonical ID** | The identifier by which a card is uniquely addressed, defined by the [deck specification](#15-references) §3.1: `major_arcana.<key>` or `minor_arcana.<suit>.<rank>`. |
| **correspondence** | A value a source attaches to a target that is drawn from a system outside this specification, such as an element, a planet or a Hebrew letter ([§6](#6-correspondences)). |
| **court** | A card whose rank is `page`, `knight`, `queen` or `king`. |
| **entry key** | The dotted key path beneath a slot naming one passage or one correspondence, such as `advice.work` ([§4.3](#43-slots)). |
| **group** | Any named set of cards a source can address: a builtin family member, an author-defined group, or an entity named by a qualified identifier ([§3.3](#33-group-identifiers)). |
| **overlay** | A source that translates another source, declaring `translates` and carrying passages in one language ([§7.1](#71-overlay-files)). |
| **passage** | Text a source attaches to a target for a reader to read ([§5](#5-passages)). |
| **pip** | A minor arcanum whose rank is `ace` through `ten`. |
| **qualified identifier** | An identifier naming an Arcana Land entity unambiguously across authors, defined by the [deck specification](#15-references) §3.3. |
| **slot** | One of `passages`, `correspondences` and `cards`: the segment directly beneath a target that says which kind of content follows ([§4.3](#43-slots)). |
| **source** | A work, a body of practice, or any other single origin of esoteric content carrying one attribution and one license. One source is one file ([§2.1](#21-one-source-one-file)). |
| **source library** | An ordered list of **library roots**, each a directory searched for source documents ([§2.2](#22-the-esoterica-library)). |
| **target** | The thing a source is talking about: a card or a group. Targets are the first-class noun of this specification ([§4.2](#42-targets)). |

Note that "target" is not a key. It is the concept `card` and `group` are the two kinds of, and the word this document uses when it does not care which.

### 1.4 Versioning and Compatibility

Every source declares the version of this specification it is written against in `[meta].schema_version`. Its value MUST be `"<major>.<minor>"`: two decimal integers separated by a dot. The compatibility contract binds this specification, not any source or application:

- A minor version update MUST be backward and forward compatible. It MAY add new tables, keys and values, and it MAY deprecate existing ones, but it MUST NOT change or remove the behavior of anything an earlier version of the same major version defined.
- A major version update MAY be incompatible in any respect.

Adding a value to one of this specification's registries — a [source type](#411-source-type), a [passage key](#52-the-passage-registry), a [correspondence key](#62-the-correspondence-registry) — is a minor version change, because an unregistered value is already legal and already preserved ([§5.1](#51-passage-keys-and-values)).

`[meta].version` is the source's own version and is unrelated to `schema_version`. It is a free-form string. This specification defines no syntax for it and no ordering over it, so applications MAY compare two values for equality to detect that a source has changed, but MUST NOT infer from two values which is the later.

This specification's `schema_version` is independent of the deck specification's. A document written against esoterica 1.0 makes no claim about which deck schema version an application supports.

### 1.5 References

The documents below are referenced normatively unless marked informative. A dated reference applies only to the edition cited, and an undated reference applies to the latest edition.

| Reference | Title | Where used |
| --- | --- | --- |
| **Tarot Deck Specification** | [DECK.md](https://github.com/arcanaland/specifications/blob/main/DECK.md), version 2.0 or later | [§3.1](#31-source-identity), [§3.2](#32-card-references), [§3.3](#33-group-identifiers), [§3.4](#34-grammar), [§3.5](#35-identifiers-in-toml), [§4.1.3](#413-published-date), [§10](#10-extensibility) |
| **BCP 14** | Key words for use in RFCs ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) | [§1.2](#12-document-conventions) |
| **TOML 1.0.0** | [toml.io/en/v1.0.0](https://toml.io/en/v1.0.0) | [§2.3](#23-file-format-and-encoding) |
| **RFC 5234** | Augmented BNF for Syntax Specifications: ABNF | [§3.4](#34-grammar) |
| **RFC 7405** | Case-Sensitive String Support in ABNF | [§3.4](#34-grammar) |
| **BCP 47** | Tags for Identifying Languages ([RFC 5646](https://www.rfc-editor.org/rfc/rfc5646)) | [§7.2](#72-language-resolution) |
| **RFC 4647** | Matching of Language Tags | [§7.2](#72-language-resolution) |
| **ISO 2108** | International Standard Book Number, with the freely available [ISBN Users' Manual](https://www.isbn-international.org/content/isbn-users-manual/29) | [§4.1](#41-meta) |
| **SPDX License List** | [spdx.org/licenses](https://spdx.org/licenses/), with the [license expression syntax](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/) | [§8](#8-licensing-and-attribution) |
| **RightsStatements.org** | [Standardized international rights statements](https://rightsstatements.org/) | [§8.2](#82-rights-status) |
| **CSL** (informative) | [Citation Style Language](https://citationstyles.org/) item types | [§4.1.1](#411-source-type) |
| **Dublin Core** (informative) | [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/), `bibliographicCitation` | [§4.1.2](#412-citation) |
| **Spread Specification** (informative, proposed) | [SPREAD.md](https://github.com/arcanaland/specifications/blob/main/SPREAD.md) | [§3.3](#33-group-identifiers) |
| **XDG Base Directory Specification** (informative) | [specifications.freedesktop.org](https://specifications.freedesktop.org/basedir-spec/latest/) | [Appendix C](#appendix-c-platform-conventions-informative) |

> Note: the deck specification is referenced here **normatively**, while it references this one informatively. The dependency runs one way on purpose. This specification borrows the deck specification's identifier system rather than restating it, so that a card means the same thing in both; the deck specification needs nothing from this one.

### 1.6 Licensing of This Specification (Informative)

This section describes the terms of the specification itself. It is not about the licensing of any source, which [§8](#8-licensing-and-attribution) covers.

The text of this document is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Its machine-facing parts are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) and the author asserts no copyright, database right, patent or trademark over them against anyone:

- the ABNF grammar of [§3.4](#34-grammar);
- the names, types, defaults and enumerated values of every table and key this document defines ([§4](#4-document-reference)), together with every registry of values it publishes, namely the source types of [§4.1.1](#411-source-type), the passage keys of [§5.2](#52-the-passage-registry) and the correspondence keys of [§6.2](#62-the-correspondence-registry);
- the builtin group names and their membership ([§4.4](#44-builtin-groups));
- the reserved names of [Appendix B](#appendix-b-reserved-and-deprecated-names);
- every example in this document.

No permission, notice, registration or fee is required to implement this specification, to publish sources against it, to cross-reference or map its registries to another scheme, or to build a competing specification on top of them, for any purpose, commercial or otherwise. The author irrevocably undertakes never to assert any such right against anyone who does.

See [LICENSING.md](https://github.com/arcanaland/specifications/blob/main/LICENSING.md) for the operative terms, which govern where this section and they disagree.

## 2. Sources

### 2.1 One Source, One File

A **source** is a work, a body of practice, or any other single origin of esoteric content carrying one attribution and one license. One source is one file.

A book is one kind of source and is not the privileged one. A chapter, an article, a web page, an unpublished manuscript and a tradition with no single work behind it are all sources, and [§4.1.1](#411-source-type) names them. What makes something a source is that one `[meta]` table can describe it: this text, under these terms, credited this way.

A source is **not** a facet. "Astrology" is not a source, it is a [correspondence key](#62-the-correspondence-registry); "relationships" is not a source, it is a [passage key](#52-the-passage-registry). A document that split one book across eight files by subject would repeat its attribution eight times and force a consumer to rejoin them to render one card.

A source is **not** scoped to a deck. Both bodies of published material this specification was derived from describe the cards rather than any particular deck's artwork, and this version provides no way for a source to say it applies to one deck alone.

### 2.2 The Esoterica Library

A **source library** is an ordered list of **library roots**. Each root is a directory searched for source documents.

How an application determines its library roots is outside the scope of this specification. An application MAY derive them from platform conventions, from its own configuration or from the user. [Appendix C](#appendix-c-platform-conventions-informative) presents conventions in use on common platforms.

#### 2.2.1 Scanning

- Scanning a root is **recursive**. A source may sit at any depth beneath a root.
- A regular file whose name ends in `.toml` is a candidate source. An application MUST NOT require any other naming convention of it.
- A candidate that parses as TOML and carries a `[meta]` table with a `schema_version` key is a source. A candidate that does not is not a source, and an application MUST NOT report it as a malformed source.
- A source whose `schema_version` names a major version the application does not support is skipped. An application SHOULD report it rather than ignoring it silently, because a supported-looking file that yields nothing is the hardest failure to diagnose ([Appendix B](#appendix-b-reserved-and-deprecated-names)).
- A source that carries `[meta].schema_version` and fails any other rule of this specification is a malformed source. Applications SHOULD report malformed sources.

**A source's location on disk is not derived from its identifier, and its identifier is not derived from its location.** An application MUST NOT compute one from the other. A source may sit at any path beneath a root, and two sources whose identifiers share a realm need not sit near each other.

#### 2.2.2 Shadowing

Roots are searched in order and a source is identified within the library by its `[meta].identifier`. Where two roots each contain a source declaring the same identifier, the one in the earlier root wins and the later one is not reported. Where one root contains two files declaring the same identifier, which of them wins is not defined by this specification and a validator MUST report an error.

### 2.3 File Format and Encoding

A source document MUST be well-formed [TOML 1.0.0](https://toml.io/en/v1.0.0) encoded as UTF-8. Applications MAY skip a leading byte-order mark and a source SHOULD NOT write one.

This specification defines **no path-valued field**. Nothing in a source document names a file, so a source cannot direct an application to read one.

Passage text is arbitrary Unicode and is frequently long. Authors SHOULD use TOML multi-line basic strings for anything longer than a line, and SHOULD NOT rely on any escape sequence beyond those TOML defines.

## 3. Identity and Identifiers

Cards are named by the canonical IDs of the deck specification. Sources, and the entities a source points at, are named by qualified identifiers.

### 3.1 Source Identity

Every source declares a **qualified identifier** in `[meta].identifier`, as defined by the deck specification §3.3: a realm and a slash-separated object path, with the first path segment naming an entity kind.

An esoterica document's type segment MUST be `esoterica`.

```
land.arcana/esoterica/mcelroy-tarot-card-meanings
id.example.shelf/esoterica/references/books/tarot-for-change
org.example/esoterica/golden-dawn-correspondences
```

The realm is controlled by whoever mints the identifier, which for a source document is its author. A realm asserts control of a **name**, not authorship of the **work** it names: an author transcribing someone else's book mints the identifier under their own realm and says who wrote the book in [`author`](#41-meta) and what the terms are in [`license`](#81-license-expressions) and [`rights_status`](#82-rights-status). An author MAY delegate a subdomain to separate what they wrote from what they transcribed, as in `id.example.shelf/esoterica/some-published-book`.

A source's `identifier` MUST NOT carry a fragment.

An identifier names the source across all of its versions. An author who revises a source MUST NOT change its `identifier` on account of the new `[meta].version`, and MUST mint a new identifier where the document has become a different source rather than a new version of the same one.

`identifier` is REQUIRED. Unlike a deck, a source has no directory name to fall back on: its identifier is the only handle by which an [overlay](#71-overlay-files) can name it, by which an application can remember that a user disabled it, and by which one installed copy shadows another ([§2.2.2](#222-shadowing)). Applications and validators MUST NOT synthesize one for a source that lacks it.

### 3.2 Card References

A card is addressed by its canonical ID, exactly as the deck specification §3.1 defines it, including custom cards and [extended major arcana](https://github.com/arcanaland/specifications/blob/main/DECK.md#13-terminology):

```
major_arcana.00
major_arcana.happy_squirrel
minor_arcana.wands.ace
minor_arcana.stars.ace
```

A canonical ID denotes a **slot** rather than a particular card of tradition. `major_arcana.08` is the major arcanum numbered eight, which is Strength in a Waite-Smith-descended deck and Justice in a Marseille-descended one. A source that means the card rather than the slot says so in its text; this specification provides no way to say it structurally, and an author writing for one tradition SHOULD say which in `[meta].description`.

**A card reference in a source document MUST NOT carry a variant suffix.** Card variants are alternative artwork for the same card and denote the same meaning, so deck specification §3.1.2 requires consumers of interpretive data to discard the suffix. There is nothing for a source to attach to a variant that it would not attach to the card.

### 3.3 Group Identifiers

A **group** is any named set of cards. A source addresses one of three kinds:

- A **builtin family member**, written as bare segments: `group.suits.wands`, `group.classes.court`, `group.all` ([§4.4](#44-builtin-groups)).
- An **author-defined group**, under the `custom` family: `group.custom.thirteen_lunar` ([§4.5](#45-author-defined-groups)).
- An entity named by a **qualified identifier**, written as a single key: `group."land.arcana/spread/celtic-cross#challenge"`.

The third kind is how a source attaches meaning to something no card grouping names — above all a **position in a published spread**, addressed by the fragment of that spread's qualified identifier. The Spread Specification owns what a spread document contains; this specification owns only the attachment.

**A key directly under `group` that contains a `/` is a qualified identifier and is atomic. Any other key is a builtin family name.** The discriminator is the slash rather than TOML quoting, because quoting does not survive parsing: a TOML reader yields the plain string `land.arcana/spread/celtic-cross#challenge` as one key whether or not the author wrote quotation marks, so a rule stated in terms of quotation marks could not be checked against a parsed document. A qualified identifier always contains at least one `/` and a builtin family name never does, so the two sets are disjoint by construction.

Nothing in this specification resolves a qualified identifier. There is no registry, no index and no fetch. A source that names a spread position an application has never heard of is conforming, and the application ignores that target.

One imprecision is accepted rather than hidden: a spread position is a slot cards are laid into rather than a set of cards, so `group` is not literally accurate for it. No single word covers a builtin family, an author-defined group and a spread position, and this specification prefers one keyword with a stated edge over three keywords.

### 3.4 Grammar

The productions below are [ABNF](https://www.rfc-editor.org/rfc/rfc5234) (RFC 5234), with the case-sensitive string notation of [RFC 7405](https://www.rfc-editor.org/rfc/rfc7405). Every string literal in this grammar is case-sensitive and lowercase.

`canonical-id`, `custom-name`, `suit-key`, `rank-key`, `qualified-id` and `published-date` are the productions of deck specification §3.5 and are used here unchanged. They are referenced rather than restated so that the two documents cannot drift apart.

```abnf
; ---- Targets ----------------------------------------------------------

target          = card-target / group-target

card-target     = %s"card" "." canonical-id
group-target    = %s"group" "." group-key

group-key       = %s"all" / family-member / qualified-id

family-member   = ( %s"arcana"  "." arcana-key ) /
                  ( %s"classes" "." class-key  ) /
                  ( %s"suits"   "." suit-key   ) /
                  ( %s"ranks"   "." rank-key   ) /
                  ( %s"custom"  "." group-name )

arcana-key      = %s"major" / %s"minor"
class-key       = %s"pip" / %s"court"
group-name      = custom-name

; ---- Slots and entry keys ---------------------------------------------

slot            = %s"passages" / %s"correspondences" / %s"cards"

entry-key       = key-part *( "." key-part )
key-part        = custom-name
```

A fully written passage or correspondence is a `target`, then a `.`, then a `slot`, then a `.`, then an `entry-key`. The `cards` slot takes no `entry-key` ([§4.3](#43-slots)).

Four constraints are not expressible in the grammar and are stated normatively:

- A `card-target`'s `canonical-id` and a `group-key`'s `qualified-id` are each written as a **single TOML key**, not as a key path ([§3.5](#35-identifiers-in-toml)). The dots inside them are part of the key's text.
- A `card-target` MUST NOT carry a variant suffix ([§3.2](#32-card-references)), which is why it is `canonical-id` and not the deck specification's `card-ref`.
- `family-member` admits any `suit-key` and any `rank-key`, including custom ones, but a group naming a suit or rank no deck defines names no cards ([§4.4.1](#441-group-membership)).
- An `entry-key` outside this specification's registries is legal and MUST be preserved ([§5.1](#51-passage-keys-and-values)), but SHOULD be prefixed `x_`.

### 3.5 Identifiers in TOML

This specification follows the rule of deck specification §3.6: where a document attaches a record to a single card, the identifier is one TOML key; where it generalizes over cards so that a prefix names a group, the identifier is a key path.

| Site | Form |
| --- | --- |
| `[card."<canonical-id>"]` | Single key |
| `[group."<qualified-id>"]` | Single key |
| `[group.<family>.<member>]` | Key path |
| `[group.all]` | Key path of one segment |
| `[app."<realm>"]` | Single key |
| A `cards` slot's entries | Single strings, one canonical ID each |

Writing a card target as one key is what fixes the slot's position structurally. Because the target occupies exactly one segment under `card`, the segment after it is the slot, whatever the card is called:

```text
[card."major_arcana.passages".passages]
  -> {"card": {"major_arcana.passages": {"passages": { … }}}}
```

A deck that mints a custom card named `passages` therefore reads correctly, and `passages`, `correspondences` and `cards` carry no privilege outside their fixed position. They are ordinary key names everywhere else, including as [entry keys](#43-slots).

The same discipline governs everywhere: **a rule may depend on the key structure that survives parsing, and never on the quotation marks that produced it.**

## 4. Document Reference

Every table this specification defines is listed below with its fields.

A source document has exactly four top-level tables: `[meta]`, `[card]`, `[group]` and `[app]`. A top-level name outside these is not defined by this specification, and [§10](#10-extensibility) reserves such names for future versions of it.

### 4.1 `[meta]`

`[meta]` describes the source: what it is, under what terms, and by what name. It says nothing about any card.

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `schema_version` | String | **Yes** | n/a | The version of this specification the source is written against as `"<major>.<minor>"` ([§1.4](#14-versioning-and-compatibility)). |
| `identifier` | String | **Yes** | n/a | The source's qualified identifier ([§3.1](#31-source-identity)). |
| `name` | String | **Yes** | n/a | The source's display name. |
| `license` | String | **Yes** | n/a | SPDX license expression governing the text this document carries ([§8.1](#81-license-expressions)). |
| `type` | String | No | none | What kind of source this is, from the registry in [§4.1.1](#411-source-type). |
| `version` | String | No | none | The source document's own free-form version ([§1.4](#14-versioning-and-compatibility)). |
| `author` | String | No | none | Who wrote the text. Absent where no one person did ([§4.1.1](#411-source-type)). |
| `publisher` | String | No | none | The work's publisher. |
| `published_date` | String | No | none | When the work this document draws on was published, at the precision the author has ([§4.1.3](#413-published-date)). |
| `isbn` | String | No | none | The work's ISBN, as printed, hyphens and all ([ISO 2108](#15-references)). |
| `url` | String (URI) | No | none | Where the work can be found. An absolute URL with a scheme of `http` or `https`. |
| `citation` | String | No | none | A display citation for provenance no other field captures ([§4.1.2](#412-citation)). |
| `description` | String | No | none | A prose description of the source, written once in `default_language`. |
| `default_language` | String | No | `"en"` | BCP 47 tag of the language this document's passages are written in ([§7.2](#72-language-resolution)). |
| `translates` | String | No | none | The qualified identifier of the source this document is a translation of ([§7.1](#71-overlay-files)). |
| `copyright` | String | No | none | Copyright notice, displayed verbatim. |
| `attribution` | String | No | none | Credit line to display ([§8.4](#84-attribution-in-presentation)). |
| `rights_status` | String (URI) | No | none | The copyright *status* of the work this document draws on, as distinct from any license granted over this document ([§8.2](#82-rights-status)). |
| `redistribution` | String | No | `"unstated"` | Whether the author passes on this document's text for republication ([§8.3](#83-redistribution-and-derivation)). |
| `derivation` | String | No | `"unstated"` | Whether the author passes on this document's text for making derived works, including translations ([§8.3](#83-redistribution-and-derivation)). |
| `tags` | Array of String | No | `[]` | Free-vocabulary categorization tags. This specification defines no registry of tag values and attaches no behavior to any of them. |

**Required means required, and exactly four keys are.** `schema_version`, `identifier`, `name` and `license` are the whole of it. This is what makes a tradition a first-class source rather than a book with holes in it: a document with no author, no date and no ISBN is not merely tolerated, it is conforming, and a validator has nothing to say about it.

`name` is required rather than `title` deliberately. A tradition has a name and does not have a title.

```toml
[meta]
schema_version = "1.0"
identifier = "org.example/esoterica/golden-dawn-correspondences"
name = "Golden Dawn correspondences"
type = "tradition"
license = "CC0-1.0"
# no author, no published_date, no isbn — conforming
```

#### 4.1.1 Source Type

`[meta].type` says what kind of source this is. Its value comes from the registry below.

| Value | The source is |
| --- | --- |
| `book` | A published book |
| `chapter` | One chapter, where the chapter is the licensed unit |
| `article` | An article in a periodical or journal |
| `webpage` | A page or post on the web |
| `manuscript` | An unpublished or self-circulated work |
| `document` | A work that is none of the above |
| `tradition` | A body of practice with no single work behind it, such as Golden Dawn correspondences, elemental dignities, or the pip meanings a modern deck assumes |

The registry is open. An application MUST ignore a `type` it does not recognize and MUST NOT treat one as an error. A later version of this specification MAY add to the registry, so an author naming a kind of source no version defines SHOULD prefix the value, as in `x_lecture`. A validator warns about an unprefixed value outside the registry.

The first six values are [CSL](#15-references) item-type spellings, taken so that this specification invents no bibliographic vocabulary of its own and a future exporter has a mechanical mapping. `tradition` is the one addition, because CSL describes things that were *cited* and a tradition is not. No mapping to CSL is normative and this specification defines no required-field matrix per type: a reader who assumes CSL compatibility will find the vocabulary familiar and the guarantees absent.

`type` is optional because the value adds nothing a consumer must have. A source without one is a source.

#### 4.1.2 Citation

Some provenance no structured field captures — *"as taught in the workshops of X"*, *"from a lecture series recorded in 1974"*. `[meta].citation` is a free-form display string carrying it.

An application that renders an attribution line SHOULD prefer `citation` where present, falling back to whatever it can compose from `author`, `name`, `publisher` and `published_date`.

This is [Dublin Core](#15-references)'s `bibliographicCitation` under a shorter name, and it is what keeps the registry of [§4.1.1](#411-source-type) from having to grow to cover every provenance shape.

#### 4.1.3 Published Date

`[meta].published_date` states when the **work** this document draws on was published. It does not describe the document: when this file was assembled and last revised is `[meta].version`'s business.

Its syntax is the `published-date` production of deck specification §3.5, which is a year, optionally a month, optionally a day:

`"2014"` is a year. `"2014-09"` is a month. `"2014-09-30"` is a day.

A source MUST NOT assert a precision its author does not have. A book whose copyright page gives only a year is `"2014"`, not `"2014-01-01"`.

The value is a TOML **string**. A bare `2014-09-30` is a TOML local date and a bare `2014` is a TOML integer; neither is this field, and [§11.4](#114-validation-rules) reports both.

A tradition usually has no publication date, and omitting the field is the right answer rather than a gap to be filled.

### 4.2 Targets

Every statement a source makes is attached to a **target**, and a target is one of exactly two kinds.

| Kind | Keyword | Addresses |
| --- | --- | --- |
| Card | `card` | One card, by canonical ID ([§3.2](#32-card-references)) |
| Group | `group` | A named set of cards ([§3.3](#33-group-identifiers)) |

```toml
[card."major_arcana.00".passages]
text = "The Fool steps off the cliff because the cliff is not the point."

[card."major_arcana.00".correspondences]
element = "air"
number = 0

[group.suits.wands.passages]
theme = "Intention, action and the direction a thing is pointed in."

[group.suits.wands.correspondences]
element = "fire"
season = "spring"
```

Everything a source says about one card is contiguous, which is the property the layout was chosen for: these documents are written and revised a card at a time, by hand.

A source MAY declare a target it says nothing about, and such a target carries no content and is not an error. A source that declares no target at all is a document with nothing in it, and a validator says so.

### 4.3 Slots

The segment directly beneath a target is a **slot**, and there are three.

| Slot | Holds | Beneath it |
| --- | --- | --- |
| `passages` | Text for a reader to read ([§5](#5-passages)) | An [entry key](#13-terminology), which MAY be dotted |
| `correspondences` | Values drawn from a system outside this specification ([§6](#6-correspondences)) | An entry key, which MAY be dotted |
| `cards` | The members of an author-defined group ([§4.5](#45-author-defined-groups)) | Nothing. Its value is an array |

**A target occupies a fixed number of segments and the segment after it is the slot.** Under `card` the target is one segment. Under `group` it is one segment for `all` and for a qualified identifier, and two for a builtin family member. There is no lookahead, no greedy matching and no reserved vocabulary: the boundary is positional.

A slot key appearing anywhere other than that fixed position is an ordinary key. `advice.text` is a passage named `advice.text`, and `[card."major_arcana.00".passages.cards]` is a passage named `cards`.

### 4.4 Builtin Groups

Six names are reserved under `group`, permanently. They are not deprecated aliases for anything and no future version of this specification will remove them.

| Family | Written | Names |
| --- | --- | --- |
| `all` | `group.all` | Every card |
| `arcana` | `group.arcana.major`, `group.arcana.minor` | One of the two arcana |
| `classes` | `group.classes.pip`, `group.classes.court` | The numbered minor arcana, or the courts |
| `suits` | `group.suits.<suit-key>` | Every card of one suit |
| `ranks` | `group.ranks.<rank-key>` | One rank across every suit |
| `custom` | `group.custom.<name>` | Whatever the source's `cards` slot lists ([§4.5](#45-author-defined-groups)) |

`group.all` replaces the global level that earlier drafts of this specification made a mechanism of its own. "Applies to every card" is a group like any other.

No author may use a bare name under `group` for a group of their own: the six family names are reserved and everything else bare is invalid. This is a closed set at the centre of an otherwise open system, and it is accepted because the escape hatches are real — `custom` takes any name, and a qualified identifier takes any entity.

`group.all` is a target on its own and takes a slot directly. The other five families take exactly one member segment.

```toml
[group.all.passages]
text = "Every card in this deck is a question rather than an answer."

[group.arcana.major.passages]
theme = "The long arc: what happens to a person rather than what a person does."

[group.classes.court.passages]
theme = "People, or the parts of a person that behave like people."

[group.ranks.page.passages]
approach = "Learning. Enthusiastic, and not yet any good at it."
```

#### 4.4.1 Group Membership

This specification defines which cards each builtin family member names, so that an application can decide whether a group's content is relevant to a card it is showing.

| Group | Members |
| --- | --- |
| `group.all` | Every card the deck in hand defines |
| `group.arcana.major` | Every card whose canonical ID begins `major_arcana` |
| `group.arcana.minor` | Every card whose canonical ID begins `minor_arcana` |
| `group.classes.pip` | Every minor arcanum whose rank is one of `ace` through `ten` |
| `group.classes.court` | Every minor arcanum whose rank is `page`, `knight`, `queen` or `king` |
| `group.suits.<suit-key>` | Every minor arcanum whose suit is `<suit-key>` |
| `group.ranks.<rank-key>` | Every minor arcanum whose rank is `<rank-key>` |
| `group.custom.<name>` | Exactly the cards the source's `cards` slot lists ([§4.5](#45-author-defined-groups)) |

Three consequences are stated because an implementer would otherwise have to guess:

- **Membership is evaluated against the deck in hand**, not against a fixed list of seventy-eight. A source is deck-independent, so `group.suits.wands` names whatever a given deck files under `wands`, and names nothing in a deck that renamed the suit.
- **A card whose rank is a custom name is a member of neither class.** `pip` and `court` are defined by the canonical rank keys and this specification does not guess where a deck's invented rank belongs.
- **A group naming a suit or rank no deck defines names no cards.** It is conforming and inert. An author writing for a deck with a fifth suit is doing the right thing, and an application holding a four-suit deck simply finds nothing.

Membership defines relevance and nothing else. It is **not** an inheritance rule: a group's content does not become a card's content, does not override anything, and does not accumulate. [§9.2](#92-group-content) governs how a group's content is presented.

### 4.5 Author-Defined Groups

A source MAY name a group the builtin families do not, under `custom`, and declare its membership with the `cards` slot.

```toml
[group.custom.thirteen_lunar]
cards = [
  "major_arcana.13",
  "major_arcana.18",
  "minor_arcana.cups.queen",
]

[group.custom.thirteen_lunar.passages]
text = "Three cards this book reads as one lunar sequence, taken together."
```

- The `cards` slot's value is an array of canonical IDs, each written as a single string, with no variant suffix and no duplicates.
- The `cards` slot appears only on a `group.custom.<name>` target. Builtin membership is [§4.4.1](#441-group-membership)'s and is not the source's to restate; a qualified identifier's membership is the owning specification's.
- `<name>` is a [custom name](https://github.com/arcanaland/specifications/blob/main/DECK.md#32-custom-names): lowercase letters, digits and underscores, no leading digit.
- A `custom` group SHOULD declare `cards`. One that does not names no cards and is inert.

**An author-defined group is source-local.** It is visible only inside the document that declares it and is not externally addressable. Two sources that both declare `group.custom.lunar` have declared two unrelated groups, and this specification provides no way to say they are the same one. That containment is deliberate: a globally addressable group would be an entity published under an identifier, which is a document type this specification set does not define.

> Note: this is the one construct in this version with no support in the material the specification was derived from. It exists because a card grouping outside the builtin families has nowhere else to live, not because a real source needed it. An author who finds it awkward can always enumerate the cards at the point of use instead.

## 5. Passages

A **passage** is text a source attaches to a target for a reader to read.

### 5.1 Passage Keys and Values

A passage's name is the full [entry key](#13-terminology) beneath the `passages` slot. Entry keys MAY nest, and the dotted path is the name: `advice.work` and `symbols.jester` are single passages whose names contain a dot.

**A passage's value is a non-empty string, or a non-empty array of non-empty strings.** Nothing else. A key beneath `passages` whose value is a table is a nesting step and not a passage.

```toml
[card."major_arcana.00".passages]
text = """
A long passage. Blank-line-separated paragraphs are the author's, and an
application MUST preserve them.
"""
keywords = ["freedom", "faith", "inexperience"]

[card."major_arcana.00".passages.advice]
work = "Leap over the limit rather than round it."
relationships = "Say the thing before you have worked out how to say it."

[card."major_arcana.00".passages.symbols]
jester = "In the royal court the jester's wit bought an indulgence nobody else had."
```

**`text` is the default passage.** An application that can show only one passage for a target shows `text`. A source whose content is one essay per card writes it there and needs no other key.

**Registered and unregistered keys.** [§5.2](#52-the-passage-registry) publishes a core registry. An unregistered key is legal, and an application MUST preserve it and MAY render it; it is simply not portable, because no other implementation knows what it means. An author using a key this specification does not define SHOULD prefix it `x_`, and a validator warns about an unprefixed one, because a later version of this specification may claim the bare name.

This is the middle path between admitting anything, which produces a specification that cannot describe its own documents, and closing the set, which cannot accept the second book.

**Reversals.** No key of this version distinguishes upright from reversed. A source that draws the distinction uses its own prefixed keys — `x_upright`, `x_reversed` — and this specification will register a pair when material that needs them is in hand.

### 5.2 The Passage Registry

| Key | Value | Meaning |
| --- | --- | --- |
| `text` | String | The source's principal treatment of the target. The default passage |
| `keywords` | Array of String | Short words or phrases the source associates with the target |
| `theme` | String | What the target is about, at a level above any one reading |
| `light` | String | The target's constructive range |
| `shadow` | String | The target's destructive range. Not the reverse of `light` and not a reversed meaning |
| `questions` | Array of String | Questions the source puts to a reader who draws the target |
| `affirmation` | String | A first-person statement the source offers with the target |
| `story` | String | A narrative, myth or anecdote the source tells about the target |
| `personality` | String | The character a court card or a rank is read as having |
| `approach` | String | How a rank or class goes about things |
| `symbols.<name>` | String | What one pictured element means. `<name>` is the author's, and is the one open subkey in this registry |
| `advice.relationships` | String | What the source advises in a reading about relationships |
| `advice.work` | String | What the source advises in a reading about work |
| `advice.spirituality` | String | What the source advises in a reading about spiritual life |
| `advice.personal_growth` | String | What the source advises in a reading about personal growth |
| `advice.fortune_telling` † | String | What the source says the target foretells |
| `advice.timing` † | String | When the source says the thing happens |

† Divinatory; see [§5.3](#53-divinatory-passages).

The registry is small on purpose. It is exactly what the published material this specification was derived from uses, and it grows by minor version when a source needs a key it does not have.

### 5.3 Divinatory Passages

Two registered keys are marked **divinatory**: `advice.fortune_telling` and `advice.timing`. The mark is a property of the *registry entry*, not of any passage, so a passage's value stays a plain string and an application can filter by category without inspecting text.

An application MAY offer to hide divinatory passages, and one that does SHOULD hide them by category rather than by guessing from the text.

The keys are registered because a source that carries them cannot otherwise be represented, and this specification's job is to transport what a source says. Transporting a sentence about timing is not performing a divination. **The draw remains excluded** ([§1.1](#11-scope-and-design-goals)): nothing here shuffles, randomizes, or selects a card, and no value in a document under this specification is an input to anything that does.

## 6. Correspondences

A **correspondence** is a value a source attaches to a target that is drawn from a system outside this specification: an element, a planet, a letter, a colour, a number.

The line between a correspondence and a passage is what the value *is*, not where a source printed it. A correspondence is a term in a bounded vocabulary that a consumer can index, filter and cross-reference. A passage is written to be read. A book that prints "Element: Air" and "Affirmation: I go where I have not been" under one heading has one of each, and this specification files them apart.

### 6.1 Correspondence Values

**A correspondence's value is a string, an integer, a float or a boolean, or a non-empty array of those.** A key beneath `correspondences` whose value is a table is a nesting step and not a correspondence.

```toml
[card."major_arcana.00".correspondences]
archetype = "the divine madman"
hebrew_letter = "aleph"
hebrew_letter_meaning = "ox"
hebrew_letter_value = 1
number = 0
element = "air"

[card."minor_arcana.wands.four".correspondences]
astrology = "venus in aries"
decan = "3"
number = 4
```

Correspondence values SHOULD be written lowercase, in the source's own vocabulary, with an application presenting them however it presents such terms. This specification publishes no vocabulary for any correspondence key: what counts as an element is the source's business, and a source using a system with five elements is conforming.

Correspondence values are **not display strings** and are not localized ([§7.1](#71-overlay-files)). Where an application shows a correspondence to a reader in their language, it is rendering a vocabulary term, not quoting the source.

Normalizing a source's compound notation into several registered keys is encouraged and loses nothing this specification cares about. A book printing `Aleph / Ox / 1` becomes the three `hebrew_letter*` keys above.

### 6.2 The Correspondence Registry

| Key | Value | Meaning |
| --- | --- | --- |
| `element` | String or Array of String | The classical element or elements |
| `number` | Integer | The number the source reads the target as carrying |
| `astrology` | String | An astrological attribution, such as a planet in a sign |
| `planet` | String | A planetary ruler |
| `zodiac` | String | A zodiacal sign |
| `decan` | String | A decan of a sign |
| `season` | String | A season |
| `direction` | String | A cardinal direction |
| `color` | String or Array of String | A colour attribution |
| `archetype` | String | The archetype the source names |
| `hebrew_letter` | String | The Hebrew letter attributed to the target |
| `hebrew_letter_meaning` | String | The letter's traditional gloss |
| `hebrew_letter_value` | Integer | The letter's numerical value |

The registry is open on the same terms as [§5.2](#52-the-passage-registry)'s: an unregistered key is legal and MUST be preserved, SHOULD be prefixed `x_`, and is warned about when it is not.

> Note: `hebrew_letter_meaning` is a gloss rather than a vocabulary term, and it is the one entry in this registry that sits awkwardly on the correspondence side of [§6](#6-correspondences)'s line. It is filed here because it is inseparable from the letter it glosses, and separating it would put half of one attribution in each slot.

## 7. Localization

### 7.1 Overlay Files

A translation is a **separate source** declaring what it translates.

```toml
[meta]
schema_version = "1.0"
identifier = "id.example/esoterica/mcelroy-tarot-card-meanings-fr"
name = "Un guide des significations des cartes du tarot"
license = "CC-BY-4.0"
translates = "land.arcana/esoterica/mcelroy-tarot-card-meanings"
default_language = "fr"

[card."major_arcana.00".passages]
text = "Le Fou marche vers la falaise parce que la falaise n'est pas le sujet."
```

An overlay mirrors whatever subset of the base source's targets and entry keys it covers. Partial translations are ordinary: a key the overlay does not carry falls back to the base source ([§7.2](#72-language-resolution)).

- `translates` MUST be a well-formed qualified identifier with no fragment, and MUST NOT equal the overlay's own `identifier`.
- An overlay is a source in every other respect: it declares its own `identifier`, `name` and `license`, because a translation is a work with its own author and its own terms.
- **An overlay carries `passages` only.** A `correspondences` or `cards` slot in an overlay is ignored, and a validator warns about it. Correspondence values are vocabulary terms rather than display strings ([§6.1](#61-correspondence-values)), and membership is not a property of a language.
- Chains are not defined. An overlay whose `translates` names another overlay is conforming and an application MAY follow the chain, but this specification requires nothing of it.
- An overlay of a source the application does not have carries nothing to attach to, and the application ignores it.

Translating a source is making a derived work of it. An author who publishes an overlay of a source whose [`derivation`](#83-redistribution-and-derivation) is `none` is doing something this specification cannot stop and does not endorse.

### 7.2 Language Resolution

A source's passages are written in `[meta].default_language`, which is a well-formed BCP 47 tag and defaults to `en`.

Given a requested tag, an application resolves a passage using the Lookup scheme of RFC 4647:

1. Among the overlays of the source, prefer the one whose `default_language` matches the requested tag, then progressively shorter forms of it. A request for `pt-BR` therefore prefers a `pt-BR` overlay, then a `pt` overlay.
2. Where the chosen overlay carries the passage, use it.
3. Otherwise fall back to the base source's own text.

Applications MUST compare language tags case-insensitively. Tags SHOULD be canonical, using the shortest available ISO 639 subtag (`en`, not `eng`), lowercase language, titlecase script and uppercase region.

Where two overlays of one source declare the same `default_language`, which one wins is decided by [shadowing](#222-shadowing) if they are in different roots, and is otherwise undefined; a validator reports it.

An application that presents a passage from an overlay MUST attribute it to the overlay as well as to the base source, because the two have different authors and may have different terms ([§8.4](#84-attribution-in-presentation)).

## 8. Licensing and Attribution

A source document and the work it draws on are two different things with, frequently, two different sets of terms.

- `[meta].license` covers **the text in this document**. For a source whose author wrote the text, it says what may be done with their writing. For a source transcribing a published book, it says what may be done with this transcription, which is usually nothing.
- `[meta].rights_status` covers **the work behind it** ([§8.2](#82-rights-status)).
- `[meta].redistribution` and `[meta].derivation` say what the author passes on ([§8.3](#83-redistribution-and-derivation)).

### 8.1 License Expressions

`[meta].license` is REQUIRED. It SHOULD be a valid [SPDX license expression](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/), and identifiers in it MUST come from the [SPDX License List](https://spdx.org/licenses/) and are case-sensitive.

For terms with no SPDX identifier, use a `LicenseRef-` string:

```toml
[meta]
schema_version = "1.0"
identifier = "id.example.shelf/esoterica/references/books/some-book"
name = "Some Book"
type = "book"
author = "A. Writer"
license = "LicenseRef-AllRightsReserved"
rights_status = "https://rightsstatements.org/vocab/InC/1.0/"
redistribution = "none"
derivation = "none"
```

`license` is required rather than optional because a source is text, and text with no stated terms is text nobody downstream can use. Where no license is granted at all, saying so with a `LicenseRef-` value and a `rights_status` is the answer; leaving the field out is not.

**A tradition has a license too.** The facts of a correspondence system are not anyone's property, but the expression of them in a particular file is its author's work, and `license` is about the file. An author documenting a tradition chooses terms for their own writing in the ordinary way, and `CC0-1.0` is a common and reasonable choice.

### 8.2 Rights Status

`[meta].rights_status` records the copyright status of the **work** the document draws on, as distinct from any license granted over the document.

For a source whose author wrote the text, the two coincide. For a transcription, an abridgement or a set of notes on someone else's book they do not, and `rights_status` is how the document says the underlying work is in copyright to somebody.

`rights_status` SHOULD be one of:

- a [RightsStatements.org](https://rightsstatements.org/) URI; or
- a [Creative Commons](https://creativecommons.org/) URI.

`license` and `rights_status` answer different questions about, in general, different objects, and a source MAY carry both or only `license`. Where both are present and both describe the same text, they MUST NOT contradict each other; a validator cannot check this in general and does not try, beyond the coarse cases [§11.4](#114-validation-rules) lists.

### 8.3 Redistribution and Derivation

| Value | Meaning |
| --- | --- |
| `"full"` | The text may be passed on as it is. |
| `"none"` | The text may not be passed on. |
| `"unstated"` | The default. The author has not said. |

`redistribution` governs republishing this document's text. `derivation` governs making new work from it, **which includes translating it** ([§7.1](#71-overlay-files)).

The default `"unstated"` does not grant permission. An application MUST NOT read it as `"full"`, and one that redistributes sources on a user's behalf SHOULD treat `"unstated"` as it treats `"none"`.

These fields describe what the author passes on. They do not enlarge what the author had: a `redistribution = "full"` on a transcription of a copyrighted book is the author claiming something they cannot give, and a validator reports the combination it can detect.

### 8.4 Attribution in Presentation

An application that shows a passage or a correspondence to a user MUST make its source identifiable — by name at minimum, and by `attribution` where the source declares one.

This is not politeness. Two sources routinely say incompatible things about one card, this specification deliberately provides no way to reconcile them ([§9.1](#91-sources-do-not-merge)), and an unattributed sentence is therefore a sentence a reader cannot evaluate. It is also the condition most licenses attach to reuse.

Where a passage came from an [overlay](#71-overlay-files), both the overlay and the base source are identified.

## 9. Presenting a Source

### 9.1 Sources Do Not Merge

An application holding two sources that both say something about `major_arcana.00` presents both, attributed. It MUST NOT combine their text for one entry key into one value, and this specification defines no precedence between sources, no override rule and no accumulation.

An application MAY let a user order or disable sources, and MAY present one first. That is a preference the user expressed, not a resolution this specification performed.

This is a capability earlier drafts of this specification claimed and did not have. Conflict-resolution rules for merging overlapping properties across layers were specified, implemented by nothing, and would have produced a composite paragraph attributable to no one. A reader who wants *the* meaning of the Fool is, by design, not served here; a reader who wants to know what two writers said is.

### 9.2 Group Content

A group's content is about the group. An application MAY present it alongside a card that is a member ([§4.4.1](#441-group-membership)), and where it does it MUST present it as the group's rather than the card's.

Group content does not inherit, override or accumulate. A source that says wands are fire and that the Four of Wands is celebration has said two things, not one thing refined by another, and an application showing both shows two labelled statements.

Where a card is a member of several groups a source has content for — its suit, its rank, its class, `all` — the application decides which to show and in what order. This specification imposes no order and no limit.

## 10. Extensibility

The `[app]` table is reserved for applications to record data about a source that this specification does not model. Each application takes a subtable keyed by a [realm](https://github.com/arcanaland/specifications/blob/main/DECK.md#33-qualified-identifiers):

```toml
[app."land.arcana.tarotcanvas"]
collapsed_by_default = true
```

The subtable key MUST be written as a quoted TOML key because a realm always contains a `.` character.

Applications MUST ignore any `[app]` subtable they do not own, and validators MUST NOT report unknown keys within `[app]`.

Top-level table names outside `[app]` are reserved for future versions of this specification.

## 11. Conformance and Validation

### 11.1 Conforming Source

A conforming source:

- MUST be a readable file well-formed under [§2.3](#23-file-format-and-encoding).
- MUST contain a `[meta]` table carrying the four required fields of [§4.1](#41-meta).
- MUST produce no errors under [§11.4](#114-validation-rules).

A conforming source is not required to carry any content. A document with a `[meta]` table and nothing else is conforming and useless, and [§11.4](#114-validation-rules) warns about it.

### 11.2 Errors and Warnings

A validator reports two kinds of violations. An error makes a source non-conforming and an application MAY refuse it. A warning marks something an author probably did not intend, or a condition this specification allows but has an opinion about. An application MUST load a source that produces only warnings.

### 11.3 Conforming Applications and Validators

A conforming application:

- MUST implement scanning ([§2.2.1](#221-scanning)) and shadowing ([§2.2.2](#222-shadowing)) over whatever roots it uses.
- MUST resolve targets and slots by the positional rule of [§4.3](#43-slots).
- MUST preserve every passage and correspondence it reads, including keys this specification does not define ([§5.1](#51-passage-keys-and-values)).
- MUST attribute what it presents ([§8.4](#84-attribution-in-presentation)) and MUST NOT merge sources ([§9.1](#91-sources-do-not-merge)).
- MUST ignore `[app]` subtables it does not own ([§10](#10-extensibility)), and every table, key and value this specification does not define.
- MUST NOT reject a source for warnings ([§11.2](#112-errors-and-warnings)).

An application need not implement overlays, group content or divinatory filtering. Where it does not, it presents the base source's passages in their own language, presents no group content, and hides nothing.

A conforming validator implements the rules in [§11.4](#114-validation-rules).

### 11.4 Validation Rules

Each rule is labeled **E** for error or **W** for warning.

| | Rule |
| --- | --- |
| **E** | The file is valid TOML 1.0.0 encoded as UTF-8 and carries a `[meta]` table ([§2.3](#23-file-format-and-encoding)). |
| **E** | `[meta]` carries `schema_version`, `identifier`, `name` and `license` ([§4.1](#41-meta)). |
| **E** | Every key [§4.1](#41-meta) defines carries a value of the type its field table gives. A key this specification does not define is [ignored](#10-extensibility) rather than typed. |
| **E** | `[meta].schema_version` has the form [§1.4](#14-versioning-and-compatibility) requires. |
| **E** | `[meta].identifier` is a well-formed qualified identifier carrying no fragment ([§3.1](#31-source-identity)). |
| **W** | `[meta].identifier`'s first path segment is `esoterica` ([§3.1](#31-source-identity)). |
| **E** | Where a validator can see a whole library, no two sources within one root declare the same `[meta].identifier` ([§2.2.2](#222-shadowing)). |
| **W** | Where a validator can see a whole library, no two visible sources declare the same `[meta].identifier`. Two sources that do may be a legitimate arrangement, such as two versions installed side by side, and the earlier root wins ([§2.2.2](#222-shadowing)). |
| **E** | `[meta].published_date`, where present, is a `published-date` denoting a real calendar date in the proleptic Gregorian calendar ([§4.1.3](#413-published-date)). It is a string, so a bare `2014-09-30`, which TOML reads as a local date, violates the type rule above, and so does a bare `2014`, which TOML reads as an integer. |
| **W** | An `isbn` that is not ten or thirteen characters once hyphens and spaces are removed, or whose check digit does not verify. Box and copyright-page text is transcribed by hand and this catches the transcription error ([§4.1](#41-meta)). |
| **E** | `[meta].url`, where present, is absolute with an `http` or `https` scheme ([§4.1](#41-meta)). |
| **E** | `[meta].default_language`, where present, is a well-formed BCP 47 language tag ([§7.2](#72-language-resolution)). |
| **W** | A `[meta].type` outside the registry of [§4.1.1](#411-source-type) that is not prefixed `x_`. Applications ignore it, and a later version of this specification may claim the name. |
| **E** | Every top-level table is `meta`, `card`, `group` or `app` ([§4](#4-document-reference)). |
| **E** | Every key under `card` is a well-formed canonical ID written as a single TOML key, carrying no variant suffix ([§3.2](#32-card-references), [§3.5](#35-identifiers-in-toml)). A document writing `[card.major_arcana.00]` has declared a table named `major_arcana` rather than the card `major_arcana.00`. |
| **E** | Every key directly under `group` either contains a `/` and is a well-formed qualified identifier, or contains no `/` and is one of the six builtin family names ([§3.3](#33-group-identifiers), [§4.4](#44-builtin-groups)). |
| **E** | Under a builtin family other than `all`, exactly one member segment follows, and it is a value that family admits: `major` or `minor` under `arcana`, `pip` or `court` under `classes`, a well-formed suit key under `suits`, a well-formed rank key under `ranks`, a well-formed [custom name](https://github.com/arcanaland/specifications/blob/main/DECK.md#32-custom-names) under `custom` ([§4.4](#44-builtin-groups)). |
| **E** | The segment in a target's slot position is `passages`, `correspondences` or `cards` ([§4.3](#43-slots)). |
| **E** | A `cards` slot appears only on a `group.custom.<name>` target, and its value is a non-empty array of strings, each a well-formed canonical ID with no variant suffix, with no duplicates ([§4.5](#45-author-defined-groups)). |
| **W** | A `group.custom.<name>` target with no `cards` slot. It names no cards and nothing it carries can be attached to anything ([§4.5](#45-author-defined-groups)). |
| **E** | Every entry key part beneath `passages` or `correspondences` is a well-formed [custom name](https://github.com/arcanaland/specifications/blob/main/DECK.md#32-custom-names) ([§3.4](#34-grammar)). |
| **E** | Every leaf beneath `passages` is a non-empty string or a non-empty array of non-empty strings ([§5.1](#51-passage-keys-and-values)). |
| **E** | Every leaf beneath `correspondences` is a string, integer, float or boolean, or a non-empty array of those ([§6.1](#61-correspondence-values)). |
| **W** | A passage or correspondence key outside the registries of [§5.2](#52-the-passage-registry) and [§6.2](#62-the-correspondence-registry) that is not prefixed `x_`. It is preserved either way, and a later version of this specification may claim the name. |
| **W** | A source declaring no `card` and no `group` target. The document says nothing ([§11.1](#111-conforming-source)). |
| **E** | `[meta].translates`, where present, is a well-formed qualified identifier carrying no fragment and is not equal to this source's own `identifier` ([§7.1](#71-overlay-files)). |
| **W** | An [overlay](#71-overlay-files) carrying a `correspondences` or `cards` slot, both of which an application ignores ([§7.1](#71-overlay-files)). |
| **W** | Two overlays of one source declaring the same `default_language`, where a validator can see both ([§7.2](#72-language-resolution)). |
| **E** | `redistribution` and `derivation`, where present, are one of `full`, `none` or `unstated` ([§8.3](#83-redistribution-and-derivation)). |
| **W** | A `license` that is not a well-formed SPDX license expression. A source that fails this check MUST NOT be rejected ([§8.1](#81-license-expressions)). |
| **W** | A `rights_status` that is not a RightsStatements.org or Creative Commons URI. As with `license`, a source that fails this check MUST NOT be rejected ([§8.2](#82-rights-status)). |
| **W** | A `redistribution` or `derivation` of `full` alongside a `rights_status` asserting the underlying work is in copyright with no license granted, meaning a RightsStatements.org `InC` URI or one of its refinements. The source says both that nobody granted permission and that the author passes it on ([§8.3](#83-redistribution-and-derivation)). One of the two fields is wrong, and a validator cannot tell which. |
| **W** | A source whose `rights_status` asserts the underlying work is in copyright to someone else and that declares no `author`. Every rights assertion in the document is then unattributable ([§8.2](#82-rights-status)). |
| **E** | Every `[app]` subtable key is a well-formed realm, in particular one with two labels or more, which is what distinguishes `[app."land.arcana"]` from an unquoted `[app.land.arcana]` ([§10](#10-extensibility)). The contents of such a subtable are the owning application's to define and are not validated. |
| **W** | A top-level `passages` table, or a `[meta].id` key. Both are version 0.1 spellings that a 1.0 reader would otherwise pass over in silence ([Appendix B](#appendix-b-reserved-and-deprecated-names)). |

## 12. Security Considerations

A source arrives from outside the system and carries text an author can abuse.

**Untrusted text.** Every passage value is attacker-controlled and is destined for a display surface. An application that renders passages into a terminal MUST restrict the escape sequences it passes through, since a hostile source can carry OSC 52 sequences that clobber the user's clipboard, or sequences that induce the terminal to write attacker-chosen bytes to the application's standard input. An application that renders passages into HTML or any other markup MUST escape them; passage values are plain text and this specification defines no markup in them.

**No file references.** This specification defines no path-valued field ([§2.3](#23-file-format-and-encoding)), so a source cannot direct an application at a file. An application MUST NOT interpret any value in a source document as a path.

**No fetching.** Qualified identifiers are names and not locations ([§3.3](#33-group-identifiers)). An application MUST NOT dereference one over the network. `[meta].url` is the one field naming a network location and it is for a user to follow deliberately, never automatically.

**Resource bounds.** A source is a single file with no size limit and these documents are legitimately large — a complete book of card meanings runs to hundreds of kilobytes. Recursive scanning ([§2.2.1](#221-scanning)) walks a user-controlled directory tree. An application SHOULD bound the depth it descends, the number of files it opens and the size of a file it will parse, and SHOULD NOT follow symbolic links out of a library root.

## Appendix A. Examples (Informative)

### A.1 A minimal source

Everything required and nothing else.

```toml
[meta]
schema_version = "1.0"
identifier = "id.example/esoterica/my-notes"
name = "My notes on the majors"
license = "CC0-1.0"

[card."major_arcana.00".passages]
text = "The first card, and the one I keep changing my mind about."
```

### A.2 A book, with the shape a book tends to have

```toml
[meta]
schema_version = "1.0"
identifier = "id.example.shelf/esoterica/references/books/a-guide-to-card-meanings"
name = "A Guide to Tarot Card Meanings"
type = "book"
author = "A. Writer"
publisher = "Example Press"
published_date = "2014"
isbn = "978-0-00-000000-0"
license = "LicenseRef-ExampleUncopyright"
default_language = "en"
description = "A complete treatment of all seventy-eight cards, uniform in structure."
tags = ["reference", "beginner"]

[card."major_arcana.00".passages]
text = """
The Fool is the card of the leap taken before the ground has been surveyed.

Every other card in the deck knows something. This one is willing not to.
"""
keywords = ["freedom", "faith", "inexperience", "innocence"]
light = "Freeing yourself from a limit that was never real. Beginning gladly."
shadow = "Taking a risk you have not counted, and calling the not-counting courage."
questions = [
  "What would I do if I felt free to take a leap?",
  "How willing am I to be seen not knowing?",
]

[card."major_arcana.00".passages.advice]
relationships = "Say the thing before you have worked out how to say it."
work = "Leap over the limit rather than round it."
spirituality = "You are old and young at once, and both are useful."
personal_growth = "Begin badly. Begin anyway."
fortune_telling = "Watch for a new undertaking arriving from outside the plan."
timing = "Unexpectedly, if at all."

[card."major_arcana.00".passages.symbols]
jester = "In the royal court the jester's wit bought an indulgence nobody else had."
cliff = "The edge is where the picture ends, not where the world does."

[card."major_arcana.00".correspondences]
archetype = "the divine madman"
hebrew_letter = "aleph"
hebrew_letter_meaning = "ox"
hebrew_letter_value = 1
number = 0
element = "air"

[card."minor_arcana.wands.four".passages]
text = "A celebration that is also a structure: the thing built well enough to stand on."
keywords = ["celebration", "harmony", "homecoming"]
affirmation = "I let the work be finished."

[card."minor_arcana.wands.four".correspondences]
number = 4
astrology = "venus in aries"
decan = "3"

[group.suits.wands.passages]
theme = "Intention, action, and the direction a thing is pointed in."

[group.suits.wands.correspondences]
element = "fire"
season = "spring"
direction = "south"
color = "red"

[group.ranks.page.passages]
approach = "Learning. Enthusiastic, and not yet any good at it."

[group.classes.court.passages]
theme = "People, or the parts of a person that behave like people."
```

### A.3 A tradition

No author, no date, no ISBN, and conforming.

```toml
[meta]
schema_version = "1.0"
identifier = "org.example/esoterica/golden-dawn-correspondences"
name = "Golden Dawn correspondences"
type = "tradition"
license = "CC0-1.0"
citation = "As set out in the order's published papers and as taught since."
description = "Decan, planetary and elemental attributions in the form most modern decks assume."

[group.suits.swords.correspondences]
element = "air"

[card."minor_arcana.swords.two".correspondences]
astrology = "moon in libra"
decan = "1"
```

### A.4 A transcription of a work in copyright

The case the licensing fields exist for: the document is the author's, the work is not.

```toml
[meta]
schema_version = "1.0"
identifier = "id.example.shelf/esoterica/references/books/tarot-for-change"
name = "Tarot for Change"
type = "book"
author = "J. Dore"
published_date = "2021"
isbn = "978-0-593-29593-9"
license = "LicenseRef-AllRightsReserved"
rights_status = "https://rightsstatements.org/vocab/InC/1.0/"
redistribution = "none"
derivation = "none"
copyright = "© 2021 J. Dore"

[card."major_arcana.00".passages]
text = "One long essay per card, and no correspondences at all."
```

### A.5 A custom group and a spread position

```toml
[meta]
schema_version = "1.0"
identifier = "id.example/esoterica/reading-notes"
name = "Reading notes"
license = "CC-BY-4.0"
attribution = "Reading notes by Example Author, CC BY 4.0."

[group.custom.thirteen_lunar]
cards = ["major_arcana.13", "major_arcana.18", "minor_arcana.cups.queen"]

[group.custom.thirteen_lunar.passages]
text = "Three cards I read as one lunar sequence when they turn up together."

[group."land.arcana/spread/celtic-cross#challenge".passages]
text = """
The crossing card is not an obstacle. It is the second thing that is true,
laid at right angles to the first so that neither can be read alone.
"""

[group.all.passages]
text = "Nothing in this file is a prediction. It is a set of things to think with."
```

### A.6 A French overlay of A.2

```toml
[meta]
schema_version = "1.0"
identifier = "id.example/esoterica/a-guide-to-card-meanings-fr"
name = "Un guide des significations des cartes"
license = "CC-BY-4.0"
translates = "id.example.shelf/esoterica/references/books/a-guide-to-card-meanings"
default_language = "fr"
attribution = "Traduction française par Example Translator."

[card."major_arcana.00".passages]
text = "Le Fou est la carte du saut fait avant d'avoir mesuré le terrain."
keywords = ["liberté", "foi", "inexpérience", "innocence"]

[card."major_arcana.00".passages.advice]
work = "Franchis la limite au lieu d'en faire le tour."

[group.suits.wands.passages]
theme = "L'intention, l'action, et la direction que prend une chose."
```

## Appendix B. Reserved and Deprecated Names

The names below were defined by version 0.1 of this specification and are no longer defined by this one. A future version MUST NOT reuse any of them with a new meaning.

Applications MUST ignore these names in a 1.0 source.

| Name | Was | Status |
| --- | --- | --- |
| `[meta].id` | The source's identifier in 0.1, a bare handle such as `tarot-for-change-book` | Removed in 1.0. Identity is [`[meta].identifier`](#31-source-identity), a qualified identifier. A 0.1 `id` is not one, so it is not accepted as a fallback |
| `[meta].type` values of the form `facet.*` | The layer's facet namespace in 0.1, such as `facet.context.love`, which also derived the file's path on disk | Redefined in 1.0. [`type`](#411-source-type) says what kind of source this is, and nothing derives a path from it ([§2.2.1](#221-scanning)) |
| `[meta].isbn13` | A thirteen-digit ISBN | Renamed to [`isbn`](#41-meta) in 1.0, which is the ISBN as written without a length claim in the key name |
| `[meta].publication_year` | An integer year | Replaced in 1.0 by [`published_date`](#413-published-date), a string admitting a year, a month or a day |
| `[passages.*]` at the top level | Where the only 0.1-era source in existence stored its content, though no version of this specification ever defined it | Not defined by any version. Content is attached to a [target](#42-targets) under `[card]` or `[group]`. A validator reports a top-level `passages` table ([§11.4](#114-validation-rules)) |
| `[global]` | Properties applying to all cards | Replaced in 1.0 by [`group.all`](#44-builtin-groups), so that "applies to everything" is a group rather than a mechanism |
| `[major_arcana]`, `[minor_arcana]`, `[minor_arcana.<suit>]` | Arcana- and suit-level properties | Replaced in 1.0 by [`group.arcana.<major\|minor>`](#44-builtin-groups) and `group.suits.<suit>` |
| `[court_cards]`, `[non_court_cards]` | Court and non-court properties | Replaced in 1.0 by [`group.classes.court`](#44-builtin-groups) and `group.classes.pip` |
| `[numbers.<number>]` | Properties of all cards carrying a number | Removed in 1.0 with no direct replacement. For the minor arcana it named the same cards as [`group.ranks.<rank>`](#44-builtin-groups); a source meaning a number across both arcana declares a [`custom` group](#45-author-defined-groups), which makes the numerological claim the source's rather than this specification's |
| `[cards.<card-type>.<key>]` | Per-card properties, written as a key path | Replaced in 1.0 by [`[card."<canonical-id>"]`](#35-identifiers-in-toml), written as a single key |
| `[contexts.<name>.*]`, `[traditions.<name>.*]` | Interpretive frameworks nested inside a layer file | Removed in 1.0. A context or a tradition is a [source](#21-one-source-one-file) of its own, or a [passage key](#52-the-passage-registry) such as `advice.relationships` |
| `[layers].namespaces`, and the collection file that carried it | A file listing other layers by namespace | Removed in 1.0. Sources are discovered by [scanning](#221-scanning), not enumerated |
| `upright`, `reversed` | Per-card upright and reversed meanings | Not defined in 1.0 ([§5.1](#51-passage-keys-and-values)) |
| `<key>.<lang>` dotted suffixes | Localization, as in `name.fr` beside `name` | Removed in 1.0. The construct is not valid TOML — a key cannot be a string and a table in one document. Localization is by [overlay file](#71-overlay-files) |

## Appendix C. Platform Conventions (Informative)

This appendix records where applications conventionally look for esoterica sources on common platforms. [§2.2](#22-the-esoterica-library) leaves the choice of library roots to the application and this section provides recommendations. It mirrors the deck specification's Appendix D, with `esoterica` in place of `decks`.

**Linux.** Follow the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/) and search `$XDG_DATA_HOME/tarot/esoterica` first, then `<dir>/tarot/esoterica` for each `<dir>` in `$XDG_DATA_DIRS`. Where `$XDG_DATA_HOME` is unset or empty it defaults to `$HOME/.local/share`, and where `$XDG_DATA_DIRS` is unset or empty it defaults to `/usr/local/share:/usr/share`.

**macOS.** `~/Library/Application Support/tarot/esoterica`, then `/Library/Application Support/tarot/esoterica`.

**Windows.** `%LOCALAPPDATA%\tarot\esoterica`, then `%PROGRAMDATA%\tarot\esoterica`.

Because scanning is recursive ([§2.2.1](#221-scanning)), a user may arrange sources beneath these roots however they like.

## Appendix D. Changelog

### Version 1.0

Version 1.0 is a rewrite. Version 0.1 was a draft that no file in the world ever conformed to, and this version is derived from the material people actually write rather than from a proposed ontology. An application MUST NOT read a 0.1 document under these rules; nothing structural survives.

**Breaking changes.** Every name removed or redefined is listed in [Appendix B](#appendix-b-reserved-and-deprecated-names). The faceted-layer model is gone, and with it the rule that one file holds one facet; the seven-level property cascade and the accumulation and conflict-resolution rules that went with it; collection files; the derivation of a file's path from its `type`; and dotted-suffix localization, which was not valid TOML.

**Newly specified.**

- [Sources](#21-one-source-one-file), the unit of the file: one work, one attribution, one license, whether it is a book or a body of practice with no author at all.
- [Targets and slots](#42-targets), one shape used everywhere: a target, then `passages`, `correspondences` or `cards`, then a key. Everything a source says about one card is contiguous.
- The [positional slot rule](#43-slots), which makes the target/key boundary structural rather than a matter of reserved vocabulary, so that a deck may mint a custom card named `passages`.
- [Builtin groups](#44-builtin-groups) with [defined membership](#441-group-membership), replacing the hardcoded cascade with six reserved names inside an open group namespace.
- [Author-defined groups](#45-author-defined-groups) and the `cards` slot, for a grouping the builtin families do not name.
- [Qualified identifiers under `group`](#33-group-identifiers), by which a source attaches meaning to a position in a published spread.
- The [passage](#52-the-passage-registry) and [correspondence](#62-the-correspondence-registry) registries, open with an `x_` prefix escape, replacing "any category, dynamically."
- The [divinatory mark](#53-divinatory-passages) in the passage registry, so that an application can filter by category, together with the [draw exclusion](#11-scope-and-design-goals) that bounds what this specification will ever describe.
- [Localization by overlay file](#71-overlay-files), replacing a scheme that did not parse.
- [Discovery](#22-the-esoterica-library) by recursive scan, with a source's identifier and its location on disk deliberately independent of each other.
- [Licensing and attribution](#8-licensing-and-attribution), including the split between the terms of this document and the [rights status](#82-rights-status) of the work it draws on, which is the ordinary case for a transcription.
- [Presentation rules](#9-presenting-a-source): sources do not merge, group content does not inherit, and what is shown is attributed.
- [Conformance and validation](#11-conformance-and-validation), with an enumerated rule set, and [security considerations](#12-security-considerations).
