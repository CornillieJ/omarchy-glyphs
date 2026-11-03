# Glyphs

An [Omarchy](https://omarchy.org) overlay for typing the symbols that aren't on
your keyboard: the euro sign, accented letters, math, arrows, quotes and more.

It has three tabs, switched with Tab and Shift+Tab (or a click): Symbols, Nerd
Font icons, and emojis. The search text carries over when you switch tabs. The
icon list is bundled; emojis are read from Omarchy's own emoji plugin.

Type a few keywords, arrow to the symbol you want, press Enter, and it's
inserted into whatever was focused.

## Install

```bash
omarchy plugin add https://github.com/CornillieJ/omarchy-glyphs.git --enable
```

## Remove

```bash
omarchy plugin remove jeffrey.glyphs
```

## Use

Enabling the plugin adds a "Special Characters" entry to the Omarchy menu automatically,
by adding a `trigger.glyphs` row to
`~/.config/omarchy/extensions/omarchy-menu.jsonc` the first time it loads. It
only does this if that key isn't already there, so hand edits stick.

Prefer a keybinding (`~/.config/hypr/bindings.lua`)?

```lua
o.bind("SUPER + COMMA", "Special Characters", "omarchy-shell shell toggle jeffrey.glyphs")
```

## Requirements and behavior

- Omarchy with the Quickshell shell (Quattro), plus `wtype` and `wl-clipboard`
  (both ship with Omarchy).
- The Emojis tab reads `$OMARCHY_PATH/shell/plugins/emojis/emojis.json`, so it
  needs Omarchy's built-in emoji plugin. The other tabs work without it.
- Inserting copies the symbol to the clipboard and sends Shift+Insert to the
  focused window. The clipboard is not restored afterwards, and the copy is
  marked sensitive so clipboard history skips it.
- On first load the plugin edits `~/.config/omarchy/extensions/omarchy-menu.jsonc`
  once, to add its menu row. It parses the file before and after and skips the
  write if either parse fails.
- No network access. `icons.json` is a bundled Nerd Font glyph list.
- Regenerating `symbols.json` needs Python 3 (standard library only).

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
