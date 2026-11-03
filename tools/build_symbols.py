#!/usr/bin/env python3
"""Generates ../symbols.json from curated.py plus the accented Latin letters."""

import json
import unicodedata
from pathlib import Path

from curated import CATEGORIES, FAVORITES

MARK_KEYWORDS = {
    "ACUTE": "acute aigu",
    "GRAVE": "grave",
    "CIRCUMFLEX": "circumflex hat",
    "DIAERESIS": "diaeresis dieresis umlaut trema",
    "TILDE": "tilde",
    "RING ABOVE": "ring",
    "CEDILLA": "cedilla cedille",
    "CARON": "caron hacek",
    "OGONEK": "ogonek",
    "MACRON": "macron",
    "BREVE": "breve",
    "DOT ABOVE": "dot",
    "DOUBLE ACUTE": "double acute",
}

# No canonical decomposition, so the unicode name alone can't give the base letter.
STANDALONE = {
    "ß": ("ss", "Sharp s", "eszett german"),
    "ẞ": ("ss", "Capital sharp s", "eszett german"),
    "æ": ("ae", "Ae ligature", "ash"),
    "Æ": ("ae", "Capital Ae ligature", "ash"),
    "œ": ("oe", "Oe ligature", "french"),
    "Œ": ("oe", "Capital Oe ligature", "french"),
    "ĳ": ("ij", "Ij ligature", "dutch"),
    "Ĳ": ("ij", "Capital Ij ligature", "dutch"),
    "ø": ("o", "O with stroke", "slash danish norwegian"),
    "Ø": ("o", "Capital O with stroke", "slash danish norwegian"),
    "đ": ("d", "D with stroke", "croatian vietnamese"),
    "Đ": ("d", "Capital D with stroke", "croatian vietnamese"),
    "ł": ("l", "L with stroke", "polish"),
    "Ł": ("l", "Capital L with stroke", "polish"),
    "ð": ("d", "Eth", "icelandic"),
    "Ð": ("d", "Capital Eth", "icelandic"),
    "þ": ("th", "Thorn", "icelandic"),
    "Þ": ("th", "Capital Thorn", "icelandic"),
    "ħ": ("h", "H with stroke", "maltese"),
    "ı": ("i", "Dotless i", "turkish"),
    "ŋ": ("ng", "Eng", ""),
}

# Languages Jeffrey writes first, then the rest of Latin-1 and Latin Extended-A.
PRIORITY_BASES = "eaoiuycn"


def mark_keywords(mark):
    name = unicodedata.name(mark).replace("COMBINING ", "")
    for key, keywords in MARK_KEYWORDS.items():
        if name.startswith(key):
            return keywords
    return None


def accented_letters():
    seen = set()
    for code in list(range(0xC0, 0x100)) + list(range(0x100, 0x180)):
        glyph = chr(code)
        if glyph in ("×", "÷") or not glyph.isalpha():
            continue
        if glyph in STANDALONE:
            base, name, extra = STANDALONE[glyph]
            yield glyph, name, f"{base} {extra}"
            continue
        decomposed = unicodedata.normalize("NFD", glyph)
        if len(decomposed) < 2:
            continue
        marks = [mark_keywords(m) for m in decomposed[1:]]
        marks = [m for m in marks if m]
        if not marks or glyph in seen:
            continue
        seen.add(glyph)
        base = decomposed[0]
        label = f"{base} {' '.join(marks[0].split()[:1])}"
        prefix = "Capital " if base.isupper() else ""
        yield glyph, f"{prefix}{label}", f"{base.lower()} {' '.join(marks)} accent"


def letter_order(entry):
    glyph, name, keywords = entry
    base = keywords.split()[0]
    rank = PRIORITY_BASES.find(base)
    return (glyph.isupper(), 0 if rank >= 0 else 1, rank if rank >= 0 else ord(base[0]), ord(glyph))


def tokens(*parts):
    seen, out = set(), []
    for word in " ".join(parts).lower().split():
        if word not in seen and word not in ("with", "sign", "of"):
            seen.add(word)
            out.append(word)
    return " ".join(out)


def build():
    entries = []
    letters = sorted(accented_letters(), key=letter_order)
    entries += [
        {"e": g, "n": n, "c": "letters", "k": tokens(n, k, "letter accented diacritic latin")}
        for g, n, k in letters
    ]
    for category, category_keywords, rows in CATEGORIES:
        entries += [
            {"e": g, "n": n, "c": category, "k": tokens(n, k, category, category_keywords)}
            for g, n, k in rows
        ]

    by_glyph = {}
    for entry in reversed(entries):
        by_glyph[entry["e"]] = entry
    entries = [e for e in entries if by_glyph[e["e"]] is e]
    favorites = [by_glyph[g] for g in FAVORITES]
    rest = [e for e in entries if e["e"] not in FAVORITES]
    return favorites + rest


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "symbols.json"
    symbols = build()
    out.write_text(json.dumps(symbols, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"{len(symbols)} symbols -> {out}")
