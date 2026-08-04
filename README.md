# Arcana Land Specifications

Open standards for digital tarot decks and esoterica.

## Tarot Decks

The [Tarot Deck Specification](./DECK.md) describes how a deck is laid out on disk, its the directory structure, its `deck.toml` manifest, canonical card identifiers, image formats and internationalization.

Implemented by [libarcana](https://github.com/arcanaland/libarcana) (full v1.0) and [Tarot Canvas](https://github.com/arcanaland/tarot-canvas) (partial v1.0).

## Esoterica

The [Esoterica Specification](./ESOTERICA.md) provides meanings for the cards.

*Draft, in progress.*

## Canonical Identifiers

Both specifications address tarot objects by the same identifiers, which any project is free to adopt:

```toml
major_arcana.00                 # The Fool
major_arcana.21                 # The World
minor_arcana.wands.ace          # Ace of Wands
minor_arcana.pentacles.king     # King of Pentacles
minor_arcana.stars.prince       # Prince of Stars (example custom card)
```


