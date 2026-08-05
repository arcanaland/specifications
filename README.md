# Arcana Land Specifications

Open standards for digital tarot decks and esoterica.

## Specifications

| Specification | Version | Status | Implementations |
| --- | --- | --- | --- |
| [Tarot Deck](./DECK.md) | 1.0 | Stable | [libarcana](https://github.com/arcanaland/libarcana) (full), [Tarot Canvas](https://github.com/arcanaland/tarot-canvas) (partial) |
| [Esoterica](./ESOTERICA.md) | 0.1 | Draft | None |

### Tarot Decks

The [Tarot Deck Specification](./DECK.md) describes how a deck is laid out on disk: its directory structure, its `deck.toml` manifest, canonical card identifiers, image formats and internationalization.

### Esoterica

The [Esoterica Specification](./ESOTERICA.md) describes meanings, correspondences and other interpretive material for the cards. It is an early draft, is not implemented anywhere, and will change.

## Canonical Identifiers

Both specifications address tarot objects by the same identifiers, which any project is free to adopt:

```
major_arcana.00                 # The Fool
major_arcana.21                 # The World
minor_arcana.wands.ace          # Ace of Wands
minor_arcana.pentacles.king     # King of Pentacles
```

The identifier scheme is dedicated to the public domain and carries a non-assertion covenant, so that it can be used as shared vocabulary without anyone needing permission. See [LICENSING.md](./LICENSING.md).

## Versioning and Stability

Each specification carries a version of the form `MAJOR.MINOR`.

- **Major** versions may change or remove existing requirements. A deck or file valid under one major version is not guaranteed to be valid under the next.
- **Minor** versions only add. Anything valid under `X.Y` remains valid under `X.Y+1`.

A deck declares the version it targets in `deck.toml` as `schema_version`.

A specification is **stable** once released. Released versions are tagged in this repository and are not edited in place; corrections are published as a new version. A specification marked **draft** has not been released, may change in any way, and should not be implemented.

## Work in Progress

A substantial revision of the deck specification is in development on the [`deck-v2`](https://github.com/arcanaland/specifications/tree/deck-v2) branch. It is a draft, it is not stable, and it should not be implemented. Version 1.0 remains the current specification until v2 is released.

## Licensing

The specification prose is CC-BY-4.0. The identifier scheme, vocabulary and examples are CC0-1.0. Tooling is MIT. See [LICENSING.md](./LICENSING.md) for the details and for the non-assertion covenant.
