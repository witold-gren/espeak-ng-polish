"""Compare espeak-ng output with reference pronunciations."""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Iterable

from .ipa import edits, normalize, stress_positions, tokenize
from .lexicon import Entry

# orthographic patterns used to group errors; one word can be in many groups
CATEGORIES: dict[str, re.Pattern[str]] = {
    "i_before_vowel": re.compile(r"[^aeiouyąęó]i[aeouąęó]"),
    "zi_si_ci_dzi_ni": re.compile(r"(dz|[zscn])i"),
    "rz": re.compile(r"rz"),
    "dz_dż_dź": re.compile(r"d[zżź]"),
    "prefix_before_vowel": re.compile(r"^(bez|roz|przez|od|nad|pod|przed|ob|wz|z|s|w)[aeiouy]"),
    "prefix_before_z": re.compile(r"^(od|nad|pod|przed)[zżź]"),
    "nasal_ą_ę": re.compile(r"[ąę]"),
    "final_voiced": re.compile(r"([bdgwzżź]|dz|rz)$"),
    "w_after_voiceless": re.compile(r"[ptkfsśhc]w|[sc]zw|chw"),
    "ch_h": re.compile(r"ch|h"),
    "foreign_letters": re.compile(r"[qvx]|th|sh|ee|oo|ea|ou|^ph|y[aeiou]$"),
    "proper_noun": re.compile(r"^[A-ZĄĆĘŁŃÓŚŹŻ]"),
}


def in_category(name: str, text: str) -> bool:
    """Proper nouns are matched on the original case, other groups on lower case."""
    return bool(CATEGORIES[name].search(text if name == "proper_noun" else text.lower()))


@dataclass
class Result:
    """One checked entry."""

    text: str
    output: str
    references: list[str]
    phonemes_ok: bool
    stress_ok: bool | None
    distance: int
    length: int
    edits: list[tuple[str, str]] = field(default_factory=list)
    category: str = ""
    note: str = ""

    @property
    def ok(self) -> bool:
        return self.phonemes_ok and self.stress_ok is not False


def check(entry: Entry, output: str) -> Result:
    """Compare one output with the closest reference."""
    hypothesis = tokenize(normalize(output))
    best: tuple[int, list[tuple[str, str]], str, list[str]] | None = None
    for reference in entry.references:
        expected = tokenize(normalize(reference))
        differences = edits(expected, hypothesis)
        distance = len(differences)
        if best is None or distance < best[0]:
            best = (distance, differences, reference, expected)
    assert best is not None, f"no reference for {entry.text}"
    distance, differences, reference, expected = best

    stress_ok: bool | None = None
    with_stress = [ref for ref in entry.references if "ˈ" in ref]
    if with_stress and distance == 0:
        stress_ok = stress_positions(output) in {stress_positions(ref) for ref in with_stress}

    return Result(
        text=entry.text,
        output=output,
        references=entry.references,
        phonemes_ok=distance == 0,
        stress_ok=stress_ok,
        distance=distance,
        length=len(expected),
        edits=differences,
        category=entry.category,
        note=entry.note,
    )


def evaluate(entries: Iterable[Entry], phonemize: Callable[[str], str]) -> list[Result]:
    return [check(entry, phonemize(entry.text)) for entry in entries]


def summarize(results: list[Result]) -> dict:
    """Word and phoneme error rates, error groups and the most common confusions."""
    total = len(results)
    wrong = [result for result in results if not result.ok]
    phonemes = sum(result.length for result in results)
    distance = sum(result.distance for result in results)

    confusions: Counter[tuple[str, str]] = Counter()
    examples: dict[tuple[str, str], list[str]] = {}
    for result in wrong:
        for pair in set(map(tuple, result.edits)):
            confusions[pair] += 1
            examples.setdefault(pair, [])
            if len(examples[pair]) < 8:
                examples[pair].append(result.text)

    categories = {}
    for name, pattern in CATEGORIES.items():
        members = [result for result in results if in_category(name, result.text)]
        errors = [result for result in members if not result.ok]
        categories[name] = {
            "words": len(members),
            "errors": len(errors),
            "error_rate": round(len(errors) / len(members), 4) if members else 0.0,
        }

    stress_checked = [result for result in results if result.stress_ok is not None]
    return {
        "entries": total,
        "errors": len(wrong),
        "word_error_rate": round(len(wrong) / total, 4) if total else 0.0,
        "phoneme_error_rate": round(distance / phonemes, 4) if phonemes else 0.0,
        "stress_checked": len(stress_checked),
        "stress_errors": sum(1 for result in stress_checked if not result.stress_ok),
        "categories": categories,
        "confusions": [
            {
                "expected": expected or "∅",
                "got": got or "∅",
                "words": count,
                "examples": examples[(expected, got)],
            }
            for (expected, got), count in confusions.most_common(60)
        ],
    }


def save(path: Path, results: list[Result], meta: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "meta": meta,
        "summary": summarize(results),
        "results": [asdict(result) for result in results],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compare(before: dict, after: dict) -> dict:
    """Entries fixed and broken between two saved runs over the same input."""

    def ok(result: dict) -> bool:
        return result["phonemes_ok"] and result["stress_ok"] is not False

    old = {result["text"]: result for result in before["results"]}
    fixed, broken = [], []
    for result in after["results"]:
        previous = old.get(result["text"])
        if previous is None:
            continue
        if ok(result) and not ok(previous):
            fixed.append((result["text"], previous["output"], result["output"]))
        elif ok(previous) and not ok(result):
            broken.append((result["text"], previous["output"], result["output"]))
    return {"fixed": fixed, "broken": broken}
