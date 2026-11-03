# Symbols

An [Omarchy](https://omarchy.org) overlay for typing the symbols that aren't on
your keyboard: the euro sign, accented letters, math, arrows, quotes and more.

Type a few keywords, arrow to the symbol you want, press Enter, and it's
inserted into whatever was focused.

## Install

```bash
omarchy plugin add https://github.com/CornillieJ/omarchy-symbol-picker.git --enable
```

## Remove

```bash
omarchy plugin remove jeffrey.symbols
```

## Use

Enabling the plugin adds a "Symbols" entry to the Omarchy menu automatically,
by adding a `trigger.symbols` row to
`~/.config/omarchy/extensions/omarchy-menu.jsonc` the first time it loads. It
only does this if that key isn't already there, so hand edits stick.

Prefer a keybinding (`~/.config/hypr/bindings.lua`)?

```lua
o.bind(hyper .. "S", "Symbols", "omarchy-shell shell toggle jeffrey.symbols")
```

## Search

The list opens on the symbols a Dutch/English-speaking European types most
(`€ £ é è ë ï ç ° © — …`), then everything else. Every word you type must match
a keyword, and exact words rank above prefixes.

| Type | You get |
|---|---|
| `euro` | € |
| `money` | every currency sign |
| `e` | every e with an accent (lowercase first) |
| `E` | capital E variants only |
| `acute`, `trema`, `umlaut`, `cedille` | letters carrying that accent |
| `dutch`, `ij` | ĳ and Dutch quote marks |
| `arrow`, `greek`, `math`, `keys`, `box` | the whole category |
| `shrug` | ¯\\_(ツ)_/¯ and other text combos |

The selected symbol's name and category show below the grid. Escape clears the
filter first, then closes the overlay.

## Extending

`symbols.json` is generated. Add entries to `tools/curated.py` and run:

```bash
python3 tools/build_symbols.py
```

Accented Latin letters come from Python's `unicodedata`, so they need no
manual entries.

## License

MIT
