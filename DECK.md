# Tarot Deck Specification

> Maintained By: [Arcana Land](https://github.com/arcanaland)
> Version: 1.1

## Overview

This specification defines a standard format for tarot decks used by tarot applications. The format is designed to:

- Separate presentation (e.g., images and names) from interpretation (e.g., meanings, divination, etc).
- Establish a canonical identifier system for tarot objects that can be shared across various Arcana Land specifications.
- Support internationalization (i18n) and localization (l10n).
- Support decks with extra or missing cards.
- Allow flexibility for suit and court card renaming and remapping.
- Ensure compatibility with other Arcana Land specifications, including the [Esoterica Specification](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md) for interpretive meanings and the proposed [Spread Specification](https://github.com/arcanaland/specifications/blob/main/SPREAD.md) for geometric arrangements.

Decks are directories with a mandatory `deck.toml` file at the root.

## Directory Skeleton

```
<deck-directory>/
  deck.toml
  card_backs/              # Card back images in various formats
    classic.png            # Default card back
    alternative.png        # Optional variant backs
  scalable/                # Vector images (SVG only)
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

## deck.toml Schema

### Common Fields

```toml
[deck]
schema_version = "1.1"           # Required: Schema version (this document)
id = "rider-waite-smith"         # Required: Unique identifier (see Identifiers)
identifier = "land.arcana/deck/rider-waite-smith" # Optional: qualified identifier
name = "Rider-Waite-Smith Tarot" # Required: Human readable name
version = "1.0"                  # Required: Deck version
default_language = "en"          # Optional: BCP 47 tag of the deck's default names file (default "en")
icon = "deck-icon.png"           # Optional: deck preview image
author = "Pamela Colman Smith"   # Optional
license = "Public Domain"        # Optional
aspect_ratio = 0.5789            # Optional (default 11:19)
description = "The classic Rider-Waite-Smith tarot deck, first published in 1909." # Optional

# Additional optional metadata
created_date = "1909-12-01"      # Original creation date
updated_date = "2025-01-15"      # Last update date
publisher = "US Games Systems"   # Publisher information
website = "https://example.com/rws-deck" # Website for the deck
tags = ["traditional", "classic", "beginner-friendly"] # Categorization tags
```

`[deck]` holds the deck's identity and the human-facing metadata about it. Everything that is *content* — card backs, custom cards, variants, editions, exclusions — is a top-level table of its own, and no table nests under `[deck]`.

Icons are assumed to be the same aspect ratio as the cards.

### Card Back Configuration

```toml
[card_backs]
default = "classic"              # Required if multiple variants are defined

# Define each card back variant
[card_backs.variants.classic]
name = "Classic RWS Back"        # Human-readable name
image = "card_backs/classic.png" # Path to the card back image
description = "The original blue and white rose pattern back" # Optional description
alt_text = "A blue and white geometric pattern featuring roses and lilies" # Optional alt text
```

Card backs can have different dimensions and formats from the card fronts, and may be provided in multiple variants without duplicating the entire deck.

### Optional Custom Major and Minor Arcana

A deck may hold cards the traditional 78 do not: additional major arcana, entirely new suits, or additional ranks within a suit. Custom card keys, custom suit keys and custom rank keys are custom names and MUST follow the [identifier rules](#identifiers).

Custom cards are [discovered from the directory structure](#file-location-based-defaults) exactly as canonical cards are. A deck that drops `h1200/major_arcana/happy_squirrel.png` into place has added a card, and need declare nothing at all. The `[custom_cards]` table supplies only what a filename cannot: a card's place in the deck's sequence, and fallback display strings. It is optional in its entirety.

#### Custom Major Arcana

```toml
[custom_cards.major_arcana.happy_squirrel]
name = "The Happy Squirrel"  # Optional fallback; prefer names/<tag>.toml
alt_text = "A cheerful squirrel standing on a branch proudly holding an acorn." # Optional fallback
position = 22                # Optional; see Ordering
```

The `name` and `alt_text` fields are fallbacks. A deck should carry both in `names/<tag>.toml`, where they can be localized; see [Display Name Resolution](#display-name-resolution).

There is no `image` field. A custom card's images are found by the same convention as every other card's, which is what lets one card exist in several resolutions and formats at once.

#### Custom Suits and Ranks

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

The table key here is the canonical suit `cups`. This is the one place in this specification where a reserved key is accepted as a `[custom_cards]` table key, because the intent is to modify that suit rather than to name a new one. The rank keys themselves are custom names and remain subject to the reserved-key rule: a deck may not introduce a new rank called `page`.

`ranks` is a matter of ordering only, and is optional in both forms. A rank whose files are present but which no `ranks` list mentions is still a card of that suit; see below.

Rank and suit keys resolve their display names through `names/<tag>.toml`; see [Display Name Resolution](#display-name-resolution).

#### Ordering

Applications that present a deck in order resolve it as follows. Cards with a declared place come first, in that order: major arcana by `position`, minor arcana by their suit's `ranks`. Everything else follows, sorted by key. Suits with no canonical order follow the four canonical suits, likewise sorted by key.

`position` is an integer and MAY fall anywhere in the sequence, including between two canonical cards; a deck that seats an extra card between `08` and `09` gives it `position = 9` and pushes the rest along. Where two cards claim one position, the order between them is by key.

A deck that simply does not care — one extra major arcanum, no opinion about where it sits — declares nothing and gets it last.

### Optional Major Arcana Remapping

```toml
[remap_major_arcana]
08 = "justice"  # Swap Justice to 8
11 = "strength" # Swap Strength to 11
```

### Optional Excluded Cards

```toml
[excluded_cards]
# List cards that are intentionally excluded from this deck
cards = [
  "minor_arcana.pentacles.page",
  "minor_arcana.pentacles.knight"
]
reason = "This deck excludes these specific court cards."
```

### Optional Deck Editions

For decks that have multiple editions or printings sharing the same card fronts:

```toml
[editions]
# Define deck editions that share the same card fronts
[editions.standard]
id = "rider-waite-smith-standard"
name = "Rider-Waite-Smith (Standard)"
card_back = "classic"  # References card_backs.variants.classic
publisher = "US Games Systems"

[editions.rider_edition]
id = "rider-waite-smith-rider"
name = "Rider-Waite-Smith (Rider Edition)"
card_back = "rider"    # References card_backs.variants.rider
publisher = "Rider & Company"
created_date = "1912-01-01"
```

### Card Variants

A card variant is an alternative artwork for a card that a deck already contains.

Variants are addressed by an [extended canonical ID](#extended-canonical-ids) of the card's canonical ID, a colon, and the variant key (e.g., `major_arcana.06:two_women`).

File assets are named with the variant key infixed between the card's file stem and its extension:

```
h1200/major_arcana/06.two_women.png
```

Declaring variants in `deck.toml` is optional, and is only necessary to choose a non-default default, to supply fallback strings, or to point at a file that does not follow the naming convention.

```toml
[card_variants."major_arcana.06"]
default = "two_women"   # Optional: which variant is used for a bare canonical ID

[card_variants."major_arcana.06".variants.two_women]
name = "The Lovers"     # Optional fallback; prefer names/<tag>.toml
alt_text = "Two women stand hand in hand beneath a winged figure." # Optional fallback
image = "scalable/major_arcana/06.two_women.svg" # Optional: explicit path
```

The table key is the card's canonical ID, quoted because it contains dots. Variant keys are custom names and MUST follow the [identifier rules](#identifiers).

If `default` is omitted, the unsuffixed file (`06.svg`) is the default variant. If a deck provides only variant files for a card and no unsuffixed file, it MUST declare `default`.

Note that `names/<tag>.toml` also has a `[card_variants]` table, but a flat one keyed by extended canonical ID; see [Internationalization](#internationalization).

Variants of a card are interchangeable and carry the same meaning; consumers of interpretive data, including the [Esoterica Specification](https://github.com/arcanaland/specifications/blob/main/ESOTERICA.md), discard the variant suffix. Variant keys are deck-wide, so an application may prefer a key across the whole deck; where a card has no variant under that key, it MUST use that card's default rather than treat it as an error.

## Canonical ID and File Behavior

Cards are referenced internally using canonical IDs, which are the only official way to identify cards in this specification:

- Major Arcana: `major_arcana.00` to `major_arcana.21`
- Minor Arcana: `minor_arcana.<suit>.<rank>` where:
  - `<suit>`: `wands`, `cups`, `swords`, `pentacles`
  - `<rank>`: `ace`, `two`, ..., `ten`, `page`, `knight`, `queen`, `king`

All references to cards in the specification, including configuration files, custom cards and i18n files must use these canonical IDs.

Custom cards extend this scheme using the author's own keys: `major_arcana.happy_squirrel`, `minor_arcana.stars.ace`. Because custom names cannot begin with a digit, such an ID is never ambiguous with a canonical one.

An **extended canonical ID** names a specific [card variant](#card-variants) by appending `:` and a variant key to a canonical ID:

```
extended-id = canonical-id ":" custom-name
```

Wherever this specification accepts a canonical ID, an extended canonical ID is also accepted unless stated otherwise. A canonical ID with no suffix denotes the card's default variant.

### File-Location-Based Defaults

Applications should be designed to automatically detect and use files placed in the expected directory structure without requiring additional configuration. For example:
- Dropping an image into `h1200/minor_arcana/wands/ace.png` will automatically map it to the card with the canonical ID `minor_arcana.wands.ace`.

This ensures that creating a deck can be as simple as placing files into the correct directory structure.

Discovery defines which cards a deck has. This holds for [custom cards](#optional-custom-major-and-minor-arcana) as much as for canonical ones: dropping `h1200/major_arcana/happy_squirrel.png` into place defines `major_arcana.happy_squirrel`, and `h1200/minor_arcana/stars/ace.png` defines `minor_arcana.stars.ace` along with the suit `stars` that contains it. Declaring such a card in `deck.toml` is never required in order for it to exist; `[custom_cards]` governs only its ordering and its fallback strings.

A file's stem is read as follows. Split it on the first `.`; call the part before it the *base*.

- If the base names a card the deck already has — a canonical ID component, or a custom card defined elsewhere in the same directory — the remainder is a [variant key](#card-variants) and the file is a variant of that card.
- Otherwise the base is itself a custom name, and the file defines a custom card. Any remainder is a variant key of that new card.

So in `major_arcana/`, `06.two_women.png` is a variant of The Lovers, `the_morning.png` is a custom card, and `the_morning.night.png` is a variant of that custom card. A base that is neither a canonical key nor a well-formed [custom name](#custom-names) is an error.

## Identifiers

This specification uses two identifier grammars: custom names, which appear as keys and as path components inside a deck, and qualified identifiers, which name a whole deck across authors.

### Custom Names

Custom names, such as custom major arcana keys, custom suit keys, custom rank keys, card back variant keys, deck edition keys, card variant keys and the application key in `[app.<key>]` MUST match:

```
custom-name = ^[a-z_][a-z0-9_]*$
```

That is, lowercase letters, numbers and underscores, not starting with a number. A custom name MUST NOT be one of the reserved canonical keys: `major_arcana`, `minor_arcana`, the suits `wands`, `cups`, `swords`, `pentacles` or the ranks `ace`, `two`, ..., `ten`, `page`, `knight`, `queen`, `king`. A custom major arcana key additionally MUST NOT be a two-digit string, so that it can never collide with a canonical one.

One position accepts a reserved key: a canonical suit as the table key of `[custom_cards.minor_arcana.<suit>]`, which [extends that suit's rank sequence](#custom-suits-and-ranks) rather than naming a new suit.

### Qualified Identifiers

Qualified identifiers name Arcana Land entities such as tarot decks or spreads unambiguously across authors. 
- `land.arcana/deck/rider-waite-smith`
- `land.arcana/spread/celtic-cross`
- `my.personal.domain/deck/modern-witch-tarot`


It is composed of two components: a realm and an object path separated by a slash.

```
qualified-id = realm "/" path
realm        = ^[a-z0-9.-]+$
path         = segment ("/" segment)*
segment      = ^[a-z0-9-]+$
```

- The realm is a domain name the author controls, written in reverse order according to [RFC 1035 §2.3.1](https://www.rfc-editor.org/rfc/rfc1035#section-2.3.1). It ends at the first slash.
- The path is one or more slash-separated segments naming an entity within that realm. A deck's path SHOULD be `deck/<name>`.

Further, qualified identifiers MAY contain a final segment after a single `#` which represents a spec-specifc target. For example, `land.arcana/deck/rider-waite-smith#major_arcana.00` refers to the canonical "The Fool" card distributed by Arcana Land.

Note: qualified identifiers are not locations. Nothing in this specification implies that one can be fetched and applications MUST NOT treat a realm as a network host to contact.

### Deck Identifiers

The `id` fields of `[deck]` and of `[editions]` are deck identifiers: a lowercase label with dashes (`rider-waite-smith`) matching the `segment` grammar above. Version 1.0 had no other form of deck identity, so a bare `id` remains required and keeps its exact meaning of naming a deck within an implicit unqualified namespace, where two authors may collide.

A deck SHOULD also carry an `identifier` field in `[deck]`, giving its qualified identifier:

```toml
[deck]
id = "rider-waite-smith"                          # Required, unchanged from 1.0
identifier = "land.arcana/deck/rider-waite-smith" # Optional, qualified
```

An `[editions]` entry MAY carry an `identifier` on the same terms. Where both fields are present, `id` MUST equal the last path segment of `identifier`, so that the two never drift into different names for one deck.


## Image Formats

### Vector Graphics
- Vector graphics should be placed in the `scalable/` directory
- SVG is the only supported vector format

### Raster Graphics
- Recommended formats: PNG (preferred), JPEG, WebP
- Recommended resolutions: h750, h1200, h2400 (height in pixels)
- Each resolution should have its own directory (e.g., `h750/`, `h1200/`, `h2400/`)
- PNG with alpha channel recommended for images requiring transparency

#### Resolution Usage Guidelines
- **h750**: Use for mobile applications, thumbnails, and low-bandwidth environments
- **h1200**: Use for standard web viewing, most desktop applications, and tablets
- **h2400**: Use for high-resolution displays, printing, and when fine details need to be preserved

### ANSI Art
- Files should be stored in the `ansi<lines>/` directory, organized by card type and suit (e.g., `ansi32/major_arcana/00.ansi`).
- ANSI files can use any extension.
- Applications can assume that files with a `.txt` extension contain just ASCII text while files with an `.ansi` extension contain ANSI escape codes.

Applications should treat ANSI art as an optional format, falling back to other image formats if ANSI files are not provided.

### Card Back Images
- Placed in the `card_backs/` directory
- Can use any supported image format
- May have different dimensions and aspect ratios from the card fronts


## Aspect Ratio

- Standard assumed aspect ratio is **11:19** (~0.5789).
- Raster folders are named `h<height>/`, e.g., `h750/`, `h1200/`.
- Applications must preserve the aspect ratio when scaling images.


## Internationalization

Per-card display string (e.g., card names, suit names, alt text) are declared in `names/<tag>.toml`, e.g., `names/en.toml`.

### Language Tags

`<tag>` MUST be a well-formed language tag as defined by BCP 47 (RFC 5646). BCP 47 composes the relevant ISO standards — ISO 639 for the language, ISO 15924 for the script, ISO 3166-1 for the region — so a deck can express distinctions a bare two-letter code cannot:

```
names/en.toml        # English
names/pt-BR.toml     # Portuguese as written in Brazil
names/zh-Hans.toml   # Chinese in Simplified script
```

- Tags SHOULD be canonical: the shortest available ISO 639 subtag (`en`, not `eng`), lowercase language, titlecase script, uppercase region.
- Applications MUST compare tags case-insensitively, since some filesystems are. A deck MUST NOT ship two name files whose tags differ only in case.
- `[deck].default_language` declares the tag of the deck's default names file. If absent, applications assume `en`.

### Language Resolution

Given a requested tag, applications resolve it using the *Lookup* scheme of RFC 4647: try the requested tag, then progressively remove trailing subtags, then the deck's `default_language`, then the canonical value for that ID.

For a request of `pt-BR`, that is `names/pt-BR.toml`, then `names/pt.toml`, then the default language file.

Resolution happens per key, not per file: a `pt-BR` file that overrides only a handful of names inherits the rest from `pt`, and anything neither supplies comes from the default language file.

```toml
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

Name files are sparse and may contain only keys it wishes to. Applications MUST merge name files key by key rather than requiring a complete set and MUST NOT treat a missing key as an error.

### Display Name Resolution

Each rule below is applied to name files in the order given by [Language Resolution](#language-resolution) — the requested tag, its progressively shortened forms, then the deck's `default_language` — before moving on to the next fallback.

A resolved display string is used **verbatim**. Applications MUST NOT apply case conversion, or any other transformation, to a string a deck supplies; a deck that writes `"ace of torches"` means those exact characters. Case transformation appears in this specification only as a fallback for keys the deck never gave a string for.

Suit names are resolved first by searching for `[suits].<key>` in the name files, then (for custom suits only) `[custom_cards.minor_arcana.<key>].name`, then the title-cased key.

Rank names are resolved via `[ranks].<key>` in the name files, then the title-cased key.

Major arcana names are resolved via `[major_arcana].<key>` in the name files, then (for custom cards only) `[custom_cards.major_arcana.<key>].name`, then the canonical name for that ID.

Minor arcana names are resolved via `[minor_arcana.<suit>].<rank>` in the name files, then by [composition](#minor-arcana-name-composition) from the card's suit and rank names.

Alt text is resolved via `[alt_text.*]` in the name files, then (for custom cards only) the entry's `alt_text` field.

Card variant names are resolved via `[card_variants]."<extended-id>"` in the name files, then `[card_variants."<canonical-id>".variants.<key>].name`, then the name of the card itself. Variant alt text is resolved via `[alt_text.card_variants]."<extended-id>"`, then the variant's `alt_text` field, then the alt text of the card itself — which will describe a variant only approximately, so variants SHOULD carry their own.

#### Minor Arcana Name Composition

Because a deck may rename its suits and ranks, most decks need not write out all 56 minor arcana names. Where a name file gives no explicit name for a minor arcana card, its name is composed from a template:

```toml
[minor_arcana]
name_template = "{rank} of {suit}"
```

`{rank}` and `{suit}` are replaced by the rank and suit names resolved above; no other placeholders are defined, and an application MUST leave any other braced text in the template alone. The template is resolved by the same [Language Resolution](#language-resolution) rules as any other key, so a translation supplies its own. If no name file supplies one, the template is `"{rank} of {suit}"`.

Composition applies to custom suits and custom ranks exactly as it does to canonical ones. Since a suit or rank name always resolves — falling back to the title-cased key — composition always yields a name.

Because the template interpolates already-resolved strings and is itself never case-converted, a deck expresses its typographic convention simply by writing its suit and rank names in the case it wants. A deck whose cards read "ace of torches" writes `wands = "torches"` and `ace = "ace"`; one that reads "Ace of Torches" writes `"Torches"` and `"Ace"`. Cards that do not follow the deck's own pattern keep an explicit entry under `[minor_arcana.<suit>]`, which always wins over the template.

Where a deck supplies no value at any level, applications may fall back to the corresponding string from the default deck.

### Alt Text Guidelines

- Alt text should describe the visual elements of the card without interpretation
- For the standard Rider Waite Smith deck, comprehensive alt text should be included in the default language file
- Every deck should include at least one language file with alt text for accessibility
- Alt text for custom cards follows the same pattern in the localization files, using the custom card's canonical ID
- Every card variant should carry its own alt text, since what distinguishes variants is exactly what alt text describes
- If alt text is provided in the `custom_cards` or `card_variants` sections, it should be considered a fallback only

## Validation Rules

Applications should validate the following:

1. **Required Files**:
   - `deck.toml` must exist and adhere to the schema.
   - All referenced images and name files must exist.

2. **Canonical ID Mapping**:
   - Ensure all canonical IDs referenced in `deck.toml` have corresponding images in the defined directories.

3. **Localization Validation**:
   - Verify that every key present in a localization file corresponds to a card, suit, rank, card variant or reserved key (`[minor_arcana].name_template`) the deck defines. Name files are sparse, so a *missing* key is not an error; an *unrecognized* key is.
   - Verify that `[minor_arcana].name_template`, where present, contains no placeholder other than `{rank}` and `{suit}`.
   - Verify that alt text is provided for all cards in at least one language file.
   - Verify that every name file's stem is a well-formed BCP 47 language tag, that no two differ only in case, and that `[deck].default_language` has a corresponding file.

4. **Card Back Validation**:
   - If card back variants are defined, verify that the default card back exists.
   - Verify that all referenced card back image files exist.

5. **Identifier Validation**:
   - Verify that every custom name matches the custom name grammar and is not a reserved canonical key, excepting a canonical suit used as a `[custom_cards.minor_arcana]` table key.
   - Verify that every `id` field is a valid deck identifier.
   - Verify that every `identifier` field is a well-formed qualified identifier, and that where an `id` accompanies it, the `id` equals the last path segment of the `identifier`.
   - Version 1.0 did not constrain these, so applications SHOULD report violations in a deck declaring `schema_version = "1.0"` as warnings rather than rejecting the deck.

6. **Card Variant Validation**:
   - Verify that every card referenced in `[card_variants]` is a card the deck defines.
   - If a variant table declares `default`, verify that the named variant exists; if it does not declare one, verify that the card has an unsuffixed image file.
   - Verify that all referenced variant image files exist.

7. **Custom Card Validation**:
   - Verify that every card declared in `[custom_cards]` is a card the deck has files for. A declaration for a card with no images is an error, since `[custom_cards]` no longer defines cards on its own.
   - Verify that no custom major arcana key is a two-digit string, and that no custom rank or suit key shadows a canonical one, so that a custom ID can never collide with a canonical one.
   - Verify that every rank named in a `ranks` list has files in that suit, and that a suit's `ranks` list contains no duplicates.
   - Report a `position` claimed by two cards as a warning, not an error; ordering remains well defined.
   - Verify that no card is both excluded by `[excluded_cards]` and declared in `[custom_cards]`.


## Licensing and Attribution

- A `license` field should be included in `deck.toml` to indicate the deck's licensing terms.
- Attribution requirements must be specified (if any):

```toml
[deck]
license = "CC-BY-SA-4.0"
attribution = "Artwork by Pamela Colman Smith (Public Domain)."
```

## Extensibility for Applications

- A reserved namespace `[app]` allows applications to include custom configurations without conflicts:

```toml
[app.my_tarot_app]
default_layout = "grid"
favorite_cards = ["major_arcana.00", "minor_arcana.wands.ace"]
```

## Examples

### Rider Waite Smith

```toml
# deck.toml
[deck]
id = "rider-waite-smith"
name = "Rider-Waite-Smith"
version = "1.0"
author = "Pamela Colman Smith"
license = "Public Domain (original artwork), CC0 (digital restoration)"
attribution = "Original artwork by Pamela Colman Smith (1909). Digital restoration by Luciella Elisabeth Scarlett."
description = "The classic Rider-Waite-Smith tarot deck, first published in 1909."
schema_version = "1.1"
default_language = "en"
created_date = "1909-12-01"
updated_date = "2025-04-28"
publisher = "Original: US Games Systems, Digital: Luciella Elisabeth Scarlett"
website = "https://luciellaes.itch.io/rider-waite-smith-tarot-cards-cc0"
tags = ["traditional", "classic", "beginner-friendly"]

# Card back configuration
[card_backs]
default = "classic"

[card_backs.variants.classic]
name = "Classic RWS Back"
image = "card_backs/classic.png"
description = "Card back design provided by Luciella Elisabeth Scarlett"
```

With names and alt text in `names/en.toml`:
```toml
[major_arcana]
# You usually only need to give major arcana names that are different
00 = "The Fool"
01 = "The Magician"
02 = "The High Priestess"

[alt_text.major_arcana]
00 = "A young person in colorful clothes steps off a cliff, carrying a white rose. A small dog jumps at their heels."
01 = "A figure standing at a table with the four suit symbols, one hand raised toward the sky, the other pointing to the ground."
02 = "A robed female figure sits between two pillars, one black and one white, with a crescent moon at her feet."
# ...

[alt_text.minor_arcana.wands]
ace = "A hand emerging from a cloud holds a flowering wooden staff."
two = "A figure in a flowing robe stands on a cliff holding two staves, looking out over the sea."
# ...

# Card back alt text
[alt_text.card_backs]
classic = "A blue and white geometric pattern"
```

### Simple Custom Deck 

This spec is designed so that creating a custom deck should only require creating a minimal `deck.toml` file with your card images placed in a reasonable directory structure.

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

By following this structure and file-naming convention, applications can **automatically detect the images** and map them to the correct cards based on their canonical IDs.


### Custom Deck with Non-Standard Names and Multiple Card Backs

This example shows a complex custom deck with custom suits, a new custom major arcana card and multiple card backs.

```toml
# deck.toml
[deck]
id = "elemental-torches"
name = "Elemental Torches Tarot"
author = "Fire Sage"
version = "1.0"
schema_version = "1.1"
description = "A fire-themed tarot deck with renamed suits and additional elemental cards."
created_date = "2025-01-01"
website = "https://example.com/elemental-torches"
tags = ["elemental", "fire-themed"]

# Card back configuration with multiple variants
[card_backs]
default = "flames"

[card_backs.variants.flames]
name = "Flame Pattern"
image = "card_backs/flames.png"
description = "A dynamic pattern of red and orange flames"

[card_backs.variants.embers]
name = "Glowing Embers"
image = "card_backs/embers.png"
description = "A dark background with smoldering red embers"

# Add a custom elemental card
# The card itself comes from scalable/major_arcana/elemental_force.svg;
# this block exists only to seat it at 22 and supply fallback strings.
[custom_cards.major_arcana.elemental_force]
name = "The Elemental Force"
alt_text = "A vortex of the four elements swirling together in perfect harmony."
position = 22

# Define deck editions with different card backs
[editions]
[editions.standard]
id = "elemental-torches-standard"
name = "Elemental Torches (Standard Edition)"
card_back = "flames"

[editions.deluxe]
id = "elemental-torches-deluxe"
name = "Elemental Torches (Deluxe Edition)"
card_back = "embers"
```

And the names and alt-text in `names/en.toml`:
```toml
# Standard card names follow canonical IDs
[major_arcana]
00 = "The Wanderer" # Custom name for The Fool
01 = "The Alchemist" # Custom name for The Magician
# ... and so on

# This deck's renamed suits and ranks. A translation of this deck
# supplies its own names/<tag>.toml with these tables translated.
# All 56 minor arcana names compose from these two tables, so none of
# them are written out: "Ace of Torches", "Student of Waters", and so on.
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

# Alt text for standard cards
[alt_text.major_arcana]
00 = "A traveler with a backpack walks toward a fiery mountain, unaware of the cliff edge ahead."
01 = "A figure in red robes manipulates the four elemental symbols above a workbench filled with alchemical tools."
# ... and so on

# Alt text for custom cards
[alt_text.major_arcana]
elemental_force = "A vortex of the elements swirling together in harmony."

# Card back alt text
[alt_text.card_backs]
flames = "A dynamic pattern of red and orange flames swirling around a central spark"
embers = "A dark background with scattered glowing embers and occasional small flames"
```

### Deck with Renamed Suits and a Lowercase Convention

A deck that calls its wands "torches", its pages and knights "princesses" and "princes", and prints every card name in lower case except where a card's own title is capitalized.

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

That is the whole minor arcana: `minor_arcana.wands.ace` resolves to "ace of torches" and `minor_arcana.cups.knight` to "prince of cups", with no `[minor_arcana.<suit>]` tables at all. The lower case is not a setting — the deck simply wrote its suit and rank names that way, and applications reproduce them as given.

Cards that break the deck's own pattern are written out individually, and take precedence over the template:

```toml
[minor_arcana.pentacles]
ten = "ten of pentacles, reversed fortune"

[major_arcana]
00 = "the fool"
01 = "the Magus"
20 = "Judgement"
21 = "the universe"
# ...
```

Major arcana names have no template — a deck that renames them lists them.

### Deck with Card Variants

A deck that draws its figures more than one way. Only the cards that depict people are varied; everything else is a single artwork and needs no configuration at all.

```
inclusive-tarot/
  deck.toml
  h1200/
    major_arcana/
      06.png                  # The Lovers, default artwork
      06.two_women.png
      06.two_men.png
      06.dark_skin.png
      ...
    minor_arcana/
      cups/
        two.png
        two.two_women.png
        ...
  names/
    en.toml
```

The variants above are discovered from the directory, so `deck.toml` declares nothing about them:

```toml
# deck.toml
[deck]
schema_version = "1.1"
id = "inclusive-tarot"
name = "Inclusive Tarot"
version = "1.0"
default_language = "en"
```

Only the alt text has to be written, since that is what differs between variants:

```toml
# names/en.toml
[alt_text.major_arcana]
06 = "A man and a woman stand beneath a winged figure, a tree behind each of them."

[alt_text.card_variants]
"major_arcana.06:two_women" = "Two women stand hand in hand beneath a winged figure, a tree behind each of them."
"major_arcana.06:two_men" = "Two men stand hand in hand beneath a winged figure, a tree behind each of them."
"minor_arcana.cups.two:two_women" = "Two women raise their cups to one another in a toast."
```

Variant keys are deck-wide, so an application can prefer `two_women` everywhere: it renders `major_arcana.06:two_women` and `minor_arcana.cups.two:two_women`, and the default artwork for every other card.

## Changelog

### Version 1.1

- **Breaking**: Removed the `[aliases]` section from the manifest in favor of using a names file.
- **Breaking:** Renamed the `[variants]` section to `[editions]`.
- **Breaking:** Moved `[deck.excluded_cards]` to a top-level `[excluded_cards]`. `[deck]` now holds only the deck's identity and metadata, and no table nests under it.
- **Breaking:** Removed the `image` and `id` fields from `[custom_cards.major_arcana.<key>]`. A custom card's images are now found by the same directory convention as every other card's, so one custom card can exist in several resolutions and formats.
- Formalized display name resolution rules.
- Added card variants and extended canonical IDs.
- Made custom cards discoverable from the directory structure, so that adding a card requires no manifest edit at all. `[custom_cards]` is now optional in its entirety and governs only ordering and fallback strings.
- Defined how a file stem is read as either a card or a variant of one, so that custom cards and variants are unambiguous.
- Allowed `ranks` on a canonical suit, so that a deck can add a rank to a suit it already has rather than only defining whole new suits.
- Defined deck ordering, and specified `position` as an optional integer that may fall anywhere in the sequence.
- Added an Identifiers section formalizing custom names and fields.
- Added qualified identifiers (`<realm>/<path>`) and the optional `[deck].identifier` field.
- Defined minor arcana name composition and the `name_template` key, so that a deck that renames its suits need not write out all 56 names.
- Required that display strings supplied by a deck be used verbatim, so a deck controls its own capitalization.
- Specified name file language tags as BCP 47 (RFC 5646) and added `default_language`.

