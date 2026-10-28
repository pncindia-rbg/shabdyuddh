"""Word rules for Shabd Yuddh: loading, round letter picking, validation, scoring.

Hindi words are split into graphemes (a consonant plus its matra/virama stays one
tile), so "पानी" is two tiles: "पा" and "नी". English is split into single letters.
"""
import random
import re
import unicodedata
from collections import Counter

ROUND_TILES = 7      # letters shown per round
MIN_LEN = 3          # minimum tiles in a valid word
RARE_BONUS = 2       # extra points per rare tile
RARE = {
    "en": set("qxzjkvwy"),
    "hi": {"ञ", "ठ", "ढ", "ण", "ळ", "ङ", "ऐ", "औ", "ॠ", "ऊ", "ॐ"},
    "vi": set(),   # no rare-letter bonus yet
    "id": set(),
    "ar": set(),
}


def canon(word, lang):
    """Per-language cleanup before tiling: Arabic drops tatweel and harakat and unifies alef forms."""
    if lang != "ar":
        return word
    word = word.replace("\u0640", "")                       # tatweel
    word = re.sub(r"[\u0622\u0623\u0625\u0671]", "\u0627", word)  # آ أ إ ٱ -> ا
    return "".join(ch for ch in unicodedata.normalize("NFC", word) if unicodedata.category(ch) != "Mn")


def graphemes(word):
    """Split a word into tiles. Combining marks (matras, nukta, virama) attach to the previous tile."""
    out = []
    for ch in unicodedata.normalize("NFC", word.strip().lower()):
        if ch.isspace():
            continue
        if out and unicodedata.category(ch) in ("Mn", "Mc", "Me"):
            out[-1] += ch
        else:
            out.append(ch)
    return out


def normalize(word):
    return "".join(graphemes(word))


def load_words(path, lang):
    """Read a word list (one word per line, '#' comments allowed). Returns unique normalized words."""
    seen, out = set(), []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            tiles = graphemes(canon(line, lang))
            if len(tiles) < MIN_LEN:
                continue
            if lang == "en" and not all(t.isalpha() for t in tiles):
                continue
            w = "".join(tiles)
            if w not in seen:
                seen.add(w)
                out.append(w)
    return out


def pick_round(words, rng=random):
    """Build a 7-tile round from a random seed word, padded with filler tiles if the seed is shorter.

    Returns (seed_word, shuffled_tiles, round_counter) or None if the list is empty.
    round_counter is the multiset of tiles players can use this round.
    """
    if not words:
        return None
    grams = {w: graphemes(w) for w in words}
    pool = Counter(t for g in grams.values() for t in g)
    tiles_pool = list(pool.elements())
    seed = rng.choice(words)
    tiles = grams[seed][:]
    # pad with filler tiles drawn by frequency so every round has ROUND_TILES letters
    while len(tiles) < ROUND_TILES:
        tiles.append(rng.choice(tiles_pool))
    tiles = tiles[:ROUND_TILES]
    rng.shuffle(tiles)
    return seed, tiles, Counter(tiles)


def score_word(raw, lang, seed_counter, valid_set):
    """Returns (ok, normalized_word_or_reason_code, points). Reason codes: short, not_in_list, letters."""
    tiles = graphemes(canon(raw, lang))
    if len(tiles) < MIN_LEN:
        return False, "short", 0
    w = "".join(tiles)
    if w not in valid_set:
        return False, "not_in_list", 0
    if Counter(tiles) - seed_counter:
        return False, "letters", 0
    rare = sum(1 for t in tiles if t in RARE.get(lang, set()))
    return True, w, len(tiles) + RARE_BONUS * rare
