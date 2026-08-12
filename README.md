# Arcana Land Specifications

Open standards for digital tarot decks and esoterica.

## Specifications

| Specification | Version | Status | Implementations |
| --- | --- | --- | --- |
| [Tarot Deck](./DECK.md) | 1.0 | Stable | [libarcana](https://github.com/arcanaland/libarcana) (full), [Tarot Canvas](https://github.com/arcanaland/tarot-canvas) (partial) |
| [Tarot Deck](https://github.com/arcanaland/specifications/blob/deck-v2/DECK.md) | 2.0 | Draft | [libarcana](https://github.com/arcanaland/libarcana) (in progress) |
| [Esoterica](https://github.com/arcanaland/specifications/blob/deck-v2/ESOTERICA.md) | 1.0 | Draft | None |

### Tarot Decks

The [Tarot Deck Specification](./DECK.md) describes canonical card identifiers, how a deck is structured as a directory, its TOML manifest,  image formats and internationalization.

### Esoterica

The [Esoterica Specification](https://github.com/arcanaland/specifications/blob/deck-v2/ESOTERICA.md) describes meanings, correspondences and other interpretive material for the cards. It is an early draft and is not implemented anywhere currently.

Esoterica packs are now being built at [arcanaland/esoterica](https://github.com/arcanaland/esoterica), but no implementation currently exists to consume them.

## Canonical Identifiers

Both specifications address tarot objects by the same identifiers, which any project is free to adopt:

```
major_arcana.00                 # The Fool
major_arcana.21                 # The World
minor_arcana.wands.ace          # Ace of Wands
minor_arcana.pentacles.king     # King of Pentacles
```

## Versioning and Stability

Each specification carries a version of the form `MAJOR.MINOR`.

Major versions may change or remove existing requirements. A conforming artifact valid under one major version is not guaranteed to be valid under the next.

A substantial revision of the deck specification is in development on the [`deck-v2`](https://github.com/arcanaland/specifications/tree/deck-v2) branch.

## Releases

Released versions are tagged in this repo.

| Tag | Specification | Released |
| --- | --- | --- |
| [`deck/v1.0`](https://github.com/arcanaland/specifications/releases/tag/deck%2Fv1.0) | Tarot Deck 1.0 | 2025-04-30 |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Licensing

The specification prose is CC-BY-4.0. The identifier scheme, vocabulary and examples are CC0-1.0. Tooling is MIT. See [LICENSING.md](./LICENSING.md).
