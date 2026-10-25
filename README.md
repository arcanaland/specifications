# Arcana Land Specifications

Open standards for digital tarot decks and esoterica.

## Specifications

| Specification | Version | Status | Implementations |
| --- | --- | --- | --- |
| [Tarot Deck](./DECK.md) | 2.0 | Release Candidate 1 | [Tarot Canvas](https://github.com/arcanaland/tarot-canvas) (reading), [libarcana](https://github.com/arcanaland/libarcana) (in progress) |
| [Tarot Deck](https://github.com/arcanaland/specifications/blob/deck/v1.0/DECK.md) | 1.0 | Stable | [libarcana](https://github.com/arcanaland/libarcana) (full), [Tarot Canvas](https://github.com/arcanaland/tarot-canvas) (partial) |
| [Esoterica](./ESOTERICA.md) | 1.0 | Draft | [Tarot Canvas](https://github.com/arcanaland/tarot-canvas) (reading) |

### Tarot Decks

The [Tarot Deck Specification](./DECK.md) describes canonical card identifiers, how a deck is structured as a directory, its TOML manifest,  image formats and internationalization.

### Esoterica

The [Esoterica Specification](./ESOTERICA.md) describes meanings, correspondences and other interpretive material for the cards. It is an early draft and is not implemented anywhere currently.

Esoterica packs are now being built at [arcanaland/esoterica](https://github.com/arcanaland/esoterica) and can be read in Tarot Canvas.

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

## Releases

Released versions are tagged in this repo.

| Tag | Specification | Released | PDF |
| --- | --- | --- | --- |
| [`deck/v2.0-rc.1`](https://github.com/arcanaland/specifications/releases/tag/deck%2Fv2.0-rc.1) | Tarot Deck 2.0 (Release Candidate 1) | 2026-10-25 | [PDF](https://github.com/arcanaland/specifications/releases/download/deck%2Fv2.0-rc.1/deck-v2.0-rc.1.pdf) |
| [`deck/v1.0`](https://github.com/arcanaland/specifications/releases/tag/deck%2Fv1.0) | Tarot Deck 1.0 | 2025-04-30 | |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Licensing

The specification prose is CC-BY-4.0. The identifier scheme, vocabulary and examples are CC0-1.0. Tooling is MIT. See [LICENSING.md](./LICENSING.md).
