"""IPA normalisation and phoneme-level comparison.

espeak-ng and Wiktionary (WikiPron) write the same Polish sounds with different
symbols: espeak uses ʃ/ʒ for sz/ż, ʲ for softening and ɔ̃ for ą, Wiktionary uses
ʂ/ʐ, j and ɔw̃. Both sides are mapped to one notation before comparing, so only
real pronunciation differences count as errors.
"""

from __future__ import annotations

import re
import unicodedata

STRESS_MARKS = "ˈˌ"
TIE = "͡"
NASAL = "̃"
VOWELS = "aɛeiɨɔouɒ"

# (pattern, replacement) applied in order; first symbol conventions, then
# allophones that one side writes and the other does not
_SUBSTITUTIONS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"[ \-.‿]"), ""),
    (re.compile(TIE), ""),
    (re.compile("ʃ"), "ʂ"),
    (re.compile("ʒ"), "ʐ"),
    (re.compile("ɘ"), "ɨ"),
    (re.compile("ɡ"), "g"),
    (re.compile("ɫ"), "l"),
    (re.compile("ɒ"), "ɔ"),
    # nasal vowels: Wiktionary "ɔw̃", "ɛj̃" -> "ɔ̃", "ɛ̃"
    (re.compile(f"([ɔɛ]){NASAL}?[wjɰ]{NASAL}"), rf"\1{NASAL}"),
    # palatal nasal written with an extra softening mark
    (re.compile("ɲʲ"), "ɲ"),
    # softened consonant before a vowel: "kʲɛ" == "kjɛ"; before i the j is implied
    (re.compile(f"ʲ(?=i)"), ""),
    (re.compile("ʲ"), "j"),
    (re.compile(f"j(?=i)"), ""),
    # palatal fricative of "chi" is an allophone of x (text is NFD here: c + cedilla)
    (re.compile("c\u0327"), "x"),
    # n is velar before k/g/x ("bank", "Afganka"); Wiktionary writes it either way
    (re.compile("ŋ(?=[kgx])"), "n"),
]

AFFRICATES = ("ts", "tʂ", "tɕ", "dz", "dʐ", "dʑ")


def normalize(ipa: str, keep_stress: bool = False) -> str:
    """Map an IPA string to the shared notation."""
    text = unicodedata.normalize("NFD", ipa.strip())
    if not keep_stress:
        text = text.translate({ord(mark): None for mark in STRESS_MARKS})
    for pattern, replacement in _SUBSTITUTIONS:
        text = pattern.sub(replacement, text)
    return unicodedata.normalize("NFC", text)


def tokenize(ipa: str) -> list[str]:
    """Split a normalised IPA string into phonemes.

    Combining marks stay with their base letter, affricates are one phoneme and
    stress marks are separate tokens.
    """
    tokens: list[str] = []
    text = unicodedata.normalize("NFD", ipa)
    i = 0
    while i < len(text):
        pair = text[i : i + 2]
        if pair in AFFRICATES:
            token, i = pair, i + 2
        else:
            token, i = text[i], i + 1
        while i < len(text) and unicodedata.combining(text[i]):
            token += text[i]
            i += 1
        tokens.append(unicodedata.normalize("NFC", token))
    return tokens


def align(reference: list[str], hypothesis: list[str]) -> list[tuple[str, str]]:
    """Levenshtein alignment as (reference, hypothesis) pairs; "" marks a gap."""
    rows, cols = len(reference) + 1, len(hypothesis) + 1
    cost = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        cost[r][0] = r
    for c in range(cols):
        cost[0][c] = c
    for r in range(1, rows):
        for c in range(1, cols):
            substitution = cost[r - 1][c - 1] + (reference[r - 1] != hypothesis[c - 1])
            cost[r][c] = min(substitution, cost[r - 1][c] + 1, cost[r][c - 1] + 1)

    pairs: list[tuple[str, str]] = []
    r, c = rows - 1, cols - 1
    while r or c:
        if r and c and cost[r][c] == cost[r - 1][c - 1] + (reference[r - 1] != hypothesis[c - 1]):
            pairs.append((reference[r - 1], hypothesis[c - 1]))
            r, c = r - 1, c - 1
        elif r and cost[r][c] == cost[r - 1][c] + 1:
            pairs.append((reference[r - 1], ""))
            r -= 1
        else:
            pairs.append(("", hypothesis[c - 1]))
            c -= 1
    pairs.reverse()
    return pairs


def edits(reference: list[str], hypothesis: list[str]) -> list[tuple[str, str]]:
    """Only the differing pairs of the alignment."""
    return [pair for pair in align(reference, hypothesis) if pair[0] != pair[1]]


def stress_positions(ipa: str) -> tuple[int, ...]:
    """Indices (0-based, over all vowels) of the vowels that carry primary stress.

    Independent of where the mark sits inside the syllable onset ("maˈtɛ" and
    "matˈɛ" are the same) and ignores secondary stress.
    """
    positions: list[int] = []
    vowel_index = 0
    pending = False
    for char in unicodedata.normalize("NFD", normalize(ipa, keep_stress=True)):
        if char == "ˈ":
            pending = True
        elif char in VOWELS:
            if pending:
                positions.append(vowel_index)
                pending = False
            vowel_index += 1
    return tuple(positions)
