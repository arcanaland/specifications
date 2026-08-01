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
  names/en.toml            # Optional localized names and alt text
  names/es.toml            # (etc)
```

## deck.toml Schema

### Common Fields

```toml
[deck]
[meta]
schema_version = "1.1"           # Required: Schema version (this document)
id = "rider-waite-smith"         # Required: Unique identifier
name = "Rider-Waite-Smith Tarot" # Required: Human readable name
version = "1.0"                  # Required: Deck version
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

> Note that version 1.0 of the spec did not have a [meta] section. For backwards compatibility, assume any bare property on the deck table is also a member of the [meta] section

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


### Optional Major Arcana Remapping

```toml
[remap_major_arcana]
08 = "justice"  # Swap Justice to 8
11 = "strength" # Swap Strength to 11
```

### Optional Excluded Cards

```toml
[deck.excluded_cards]
# List cards that are intentionally excluded from this deck
cards = [
  "minor_arcana.pentacles.page",
  "minor_arcana.pentacles.knight"
]
reason = "This historical Tarocchi deck excludes these court cards."
```

### Optional Custom Major and Minor Arcana

Custom major or minor arcana cards can be defined under `[custom_cards]`. This allows for decks with entirely new suits or additional major arcana.

```toml
[custom_cards]

# Add a new suit
[custom_cards.minor_arcana.stars]
name = "Stars"
ranks = ["ace", "two", ..., "page", "knight", "queen", "king"]  # or a custom sequence
```

A custom suit's ranks are keys, not display strings. Both the suit key and every rank key resolve their display name through `[suits]` and `[ranks]` in `names/<lang>.toml`, exactly as canonical suits and ranks do. A custom suit that reuses canonical rank keys therefore inherits whatever those ranks are called in the selected language: if a deck's name file sets `page = "Princess"`, then `minor_arcana.stars.page` renders as "Princess of Stars."

Where no name file supplies a string, the resolution order given under [Display Name Resolution](#display-name-resolution) applies: for a suit, `[custom_cards.minor_arcana.<key>].name`, then the title-cased key; for a rank, the title-cased key.

```toml
[custom_cards.major_arcana.happy_squirrel]
id = "happy_squirrel"
name = "The Happy Squirrel"
image = "scalable/major_arcana/happy_squirrel.svg"
alt_text = "A cheerful squirrel standing on a branch proudly holding an acorn."
position = 22  # Optional, indicates position in sequence after traditional cards
```

The `name` and `alt_text` fields here are fallbacks. A deck should carry both in `names/<lang>.toml`, where they can be localized; see [Display Name Resolution](#display-name-resolution).

### Optional Deck Variants

For decks that have multiple editions or variants sharing the same card fronts:

```toml
[variants]
# Define deck variants that share the same card fronts
[variants.standard]
id = "rider-waite-smith-standard"
name = "Rider-Waite-Smith (Standard)"
card_back = "classic"  # References card_backs.variants.classic
publisher = "US Games Systems"

[variants.rider_edition]
id = "rider-waite-smith-rider"
name = "Rider-Waite-Smith (Rider Edition)"
card_back = "rider"    # References card_backs.variants.rider
publisher = "Rider & Company"
created_date = "1912-01-01"
```

## Canonical ID and File Behavior

Cards are referenced internally using canonical IDs, which are the only official way to identify cards in this specification:

- Major Arcana: `major_arcana.00` to `major_arcana.21`
- Minor Arcana: `minor_arcana.<suit>.<rank>` where:
  - `<suit>`: `wands`, `cups`, `swords`, `pentacles`
  - `<rank>`: `ace`, `two`, ..., `ten`, `page`, `knight`, `queen`, `king`

All references to cards in the specification, including configuration files, custom cards and i18n files must use these canonical IDs.

### File-Location-Based Defaults

Applications should be designed to automatically detect and use files placed in the expected directory structure without requiring additional configuration. For example:
- Dropping an image into `h1200/minor_arcana/wands/ace.png` will automatically map it to the card with the canonical ID `minor_arcana.wands.ace`.

This ensures that creating a deck can be as simple as placing files into the correct directory structure.

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

---

## Internationalization

Per-card display string (e.g., card names, suit names, alt text) are declared in `names/<lang>.toml`, e.g., `names/en.toml`.

```toml
# Card name localization
[major_arcana]
00 = "The Fool"
01 = "The Magician"
# ...

[minor_arcana.wands]
ace = "Ace of Wands"
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
```

Name files are sparse and may contain only keys it wishes to. Applications MUST merge name files key by key rather than requiring a complete set and MUST NOT treat a missing key as an error.

### Display Name Resolution

Card names are resolved first by inspecting `names/<lang>.toml`, then the deck's default language file, then the canonical name for that ID.

Suit names are resolved first by searching for `[suits].<key>` in `names/<lang>.toml`, then the deck's default language file, then (for custom suits only) `[custom_cards.minor_arcana.<key>].name`, then the title-cased key.

Rank names are resolved via `[ranks].<key>` in `names/<lang>.toml`, then the deck's default language file, then the title-cased key.

Alt text is resolved via `[alt_text.*]` in `names/<lang>.toml`, then the deck's default language file, then (for custom cards only) the entry's `alt_text` field.

Where a deck supplies no value at any level, applications may fall back to the corresponding string from the default deck.

### Alt Text Guidelines

- Alt text should describe the visual elements of the card without interpretation
- For the standard Rider Waite Smith deck, comprehensive alt text should be included in the default language file
- Every deck should include at least one language file with alt text for accessibility
- Alt text for custom cards follows the same pattern in the localization files, using the custom card's canonical ID
- If alt text is provided in the `custom_cards` section, it should be considered a fallback only

## Validation Rules

Applications should validate the following:

1. **Required Files**:
   - `deck.toml` must exist and adhere to the schema.
   - All referenced images and name files must exist.

2. **Canonical ID Mapping**:
   - Ensure all canonical IDs referenced in `deck.toml` have corresponding images in the defined directories.

3. **Localization Validation**:
   - Verify that every key present in a localization file corresponds to a card, suit, or rank the deck defines. Name files are sparse, so a *missing* key is not an error; an *unrecognized* key is.
   - Verify that alt text is provided for all cards in at least one language file.

4. **Card Back Validation**:
   - If card back variants are defined, verify that the default card back exists.
   - Verify that all referenced card back image files exist.


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
[custom_cards.major_arcana.elemental_force]
id = "elemental_force"
name = "The Elemental Force"
image = "scalable/major_arcana/elemental_force.svg"
alt_text = "A vortex of the four elements swirling together in perfect harmony."
position = 22

# Define deck variants with different card backs
[variants]
[variants.standard]
id = "elemental-torches-standard"
name = "Elemental Torches (Standard Edition)"
card_back = "flames"

[variants.deluxe]
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
# supplies its own names/<lang>.toml with these tables translated.
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
[alt_text.major_arcana.elemental_force]
elemental_force = "A vortex of the four elements (fire, water, air, earth) swirling together in perfect harmony."

# Card back alt text
[alt_text.card_backs]
flames = "A dynamic pattern of red and orange flames swirling around a central spark"
embers = "A dark background with scattered glowing embers and occasional small flames"
```

## Changelog

### Version 1.1

- Removed the `[aliases]` section from the manifest in favor of using a names file.
- Formalized display name resolution rules.

