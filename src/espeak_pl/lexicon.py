"""Reference pronunciations: WikiPron (Wiktionary) and the hand-made hard cases."""

from __future__ import annotations

import csv
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

WIKIPRON_URL = (
    "https://raw.githubusercontent.com/CUNY-CL/wikipron/master/data/scrape/tsv/pol_latn_broad.tsv"
)
WIKIPRON_FILE = Path("data/wikipron/pol_latn_broad.tsv")
HARD_CASES_FILE = Path("data/hard_cases.tsv")


@dataclass
class Entry:
    """Text with one or more accepted pronunciations."""

    text: str
    references: list[str] = field(default_factory=list)
    category: str = ""
    note: str = ""


def fetch_wikipron(target: Path = WIKIPRON_FILE, url: str = WIKIPRON_URL) -> Path:
    """Download the Polish WikiPron list (CC BY-SA, from Wiktionary)."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as response:
        target.write_bytes(response.read())
    return target


def is_usable_word(word: str) -> bool:
    """Single words only; abbreviations (TV, PKP) are read letter by letter."""
    if not word or " " in word or any(char.isdigit() for char in word):
        return False
    letters = [char for char in word if char.isalpha()]
    if not letters:
        return False
    if len(letters) > 1 and all(char.isupper() for char in letters):
        return False
    return True


def load_wikipron(path: Path = WIKIPRON_FILE) -> list[Entry]:
    """Words with every pronunciation Wiktionary lists for them."""
    entries: dict[str, Entry] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 2:
                continue
            word, ipa = parts
            if not is_usable_word(word):
                continue
            entry = entries.setdefault(word, Entry(word))
            entry.references.append(ipa.replace(" ", ""))
    return list(entries.values())


def load_hard_cases(path: Path = HARD_CASES_FILE) -> list[Entry]:
    """Hand-checked words and phrases; alternatives in the ipa column split by " | "."""
    entries: list[Entry] = []
    with path.open(encoding="utf-8", newline="") as handle:
        rows = (row for row in handle if row.strip() and not row.startswith("#"))
        for row in csv.DictReader(rows, delimiter="\t"):
            references = [ipa.strip() for ipa in row["ipa"].split("|") if ipa.strip()]
            entries.append(
                Entry(row["text"], references, row.get("category", ""), row.get("note") or "")
            )
    return entries
