# Contributing

Issues and pull requests are welcome.

## Where work happens

| Branch | What it is |
| --- | --- |
| `main` | Released specifications. Tarot Deck 1.0, Esoterica 0.1. |
| `deck-v2` | The in-progress rewrite of the deck specification. Draft, unstable. |

Corrections to a released specification go to `main`. Anything that changes or removes an existing requirement belongs on `deck-v2` instead, since released versions are not edited in place.

Open an issue before a substantial change, so the design can be settled before anyone writes prose.

## What makes a good specification change

- Say what an implementation must do, not what it might like to do. Use RFC 2119 keywords deliberately.
- Every normative requirement should be checkable by someone reading a deck directory.
- Add an example for anything non-obvious. Examples are checked by CI, so they have to actually parse.
- Prefer extending the existing vocabulary over inventing a parallel one.

## Checks

CI runs on every pull request:

- `tools/toml_check.py` parses every ` ```toml ` fence in `DECK.md`. A fence preceded by `<!-- toml-check: invalid -->` is a deliberate counterexample and must fail to parse instead.
- `tools/abnf_check.py` (on `deck-v2` only) checks the embedded ABNF grammar against a corpus of cases.

Both are standalone `uv` scripts. Run them directly:

```
./tools/toml_check.py
```

## Licensing of contributions

By contributing you agree that your contribution is licensed under the terms in [LICENSING.md](./LICENSING.md): CC-BY-4.0 for specification prose, CC0-1.0 for the identifier scheme, vocabulary, tabulations and examples, and MIT for anything under `tools/`.

The identifier scheme and vocabulary are public domain on purpose, so that other projects can adopt them without asking. Please keep contributions compatible with that intent.
