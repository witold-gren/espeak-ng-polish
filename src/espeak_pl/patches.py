"""Measure every patch alone and run the Polish espeak-ng regression tests.

Each patch in patches/ is applied on its own to a clean export of the pinned
espeak-ng commit, compiled and evaluated in a separate process (espeak-ng keeps
one data folder per process), then compared with the unpatched baseline. The
numbers go straight into the pull request description.
"""

from __future__ import annotations

import io
import json
import re
import shlex
import subprocess
import sys
import tarfile
from dataclasses import dataclass
from pathlib import Path

from .compile import compile_data

PINNED_COMMIT = "724808c"  # piper1-gpl CMakeLists.txt, 2026-04-06
EXPORTED_PATHS = ("dictsource", "phsource", "tests")


@dataclass
class PatchResult:
    name: str
    sources: dict[str, dict]


def export_tree(source: Path, commit: str, target: Path) -> Path:
    """Copy the files Polish depends on at `commit` into `target`."""
    archive = subprocess.run(
        ["git", "-C", str(source), "archive", "--format=tar", commit, *EXPORTED_PATHS],
        check=True,
        capture_output=True,
    ).stdout
    target.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(target, filter="data")
    return target


def apply_patch(tree: Path, patch: Path) -> None:
    # plain patch(1): git apply would resolve paths against an enclosing repository
    subprocess.run(
        ["patch", "-p1", "--forward", "--batch", "-i", str(patch.resolve())],
        cwd=tree,
        check=True,
        capture_output=True,
    )


def touches_phonemes(patch: Path) -> bool:
    return "phsource/" in patch.read_text(encoding="utf-8")


def evaluate_in_subprocess(data_dir: Path, source: str, output: Path) -> None:
    subprocess.run(
        [sys.executable, "-m", "espeak_pl.cli", "evaluate", source,
         "--data-dir", str(data_dir), "--output", str(output)],
        check=True,
        capture_output=True,
    )


def measure(
    source: Path,
    patches: list[Path],
    work: Path,
    baselines: dict[str, Path],
    commit: str = PINNED_COMMIT,
) -> list[PatchResult]:
    """Fixed/broken counts per patch and per reference source."""
    from .evaluate import compare, load

    results = []
    for patch in patches:
        tree = export_tree(source, commit, work / patch.stem / "src")
        apply_patch(tree, patch)
        data_dir = compile_data(tree, work / patch.stem / "data", phonemes=touches_phonemes(patch))
        per_source = {}
        for name, baseline in baselines.items():
            run_path = work / patch.stem / f"{name}.json"
            evaluate_in_subprocess(data_dir, name, run_path)
            diff = compare(load(baseline), load(run_path))
            per_source[name] = {
                "fixed": len(diff["fixed"]),
                "broken": len(diff["broken"]),
                "fixed_examples": [text for text, _before, _after in diff["fixed"][:8]],
                "broken_examples": [text for text, _before, _after in diff["broken"][:8]],
            }
        results.append(PatchResult(patch.name, per_source))
    return results


def render(results: list[PatchResult]) -> str:
    lines = [
        "# Patches measured one by one / Łatki mierzone osobno",
        "",
        f"Each patch applied alone on espeak-ng `{PINNED_COMMIT}` (the commit pinned by piper1-gpl).",
        "",
        "| patch | WikiPron fixed | WikiPron broken | hard cases fixed | hard cases broken | examples |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for result in results:
        wiki = result.sources.get("wikipron", {})
        hard = result.sources.get("hard", {})
        examples = ", ".join((hard.get("fixed_examples") or []) + (wiki.get("fixed_examples") or [])[:4])
        lines.append(
            f"| {result.name} | {wiki.get('fixed', '-')} | {wiki.get('broken', '-')} "
            f"| {hard.get('fixed', '-')} | {hard.get('broken', '-')} | {examples} |"
        )
    return "\n".join(lines) + "\n"


def save(results: list[PatchResult], path: Path) -> None:
    path.write_text(
        json.dumps([result.__dict__ for result in results], ensure_ascii=False, indent=1),
        encoding="utf-8",
    )


# --- espeak-ng tests/language-pronunciation.test --------------------------------------

_TEST_START = re.compile(r"^test_phon\s+(\S+)\s", re.MULTILINE)


def upstream_tests(test_file: Path, language: str = "pl") -> list[tuple[str, str, str]]:
    """(expected, text, options) of every `test_phon <language>` call in an espeak-ng test script."""
    content = test_file.read_text(encoding="utf-8")
    starts = [match for match in _TEST_START.finditer(content)]
    calls = []
    for index, match in enumerate(starts):
        if match.group(1) != language:
            continue
        end = starts[index + 1].start() if index + 1 < len(starts) else len(content)
        args = shlex.split(content[match.start() : end], comments=True)
        expected, text = args[2], args[3]
        options = args[5] if len(args) > 5 else ""
        calls.append((expected, text, options))
    return calls


def run_upstream_tests(
    test_file: Path, data_root: Path, espeak: str = "espeak-ng", language: str = "pl"
) -> list[tuple[str, str, str]]:
    """Failures as (text, expected, got); runs like tests/common test_phon (-xq -v pl)."""
    failures = []
    for expected, text, options in upstream_tests(test_file, language):
        command = [espeak, f"--path={data_root}", "-xq", *shlex.split(options), "-v", language, text]
        got = subprocess.run(command, check=True, capture_output=True, text=True).stdout.rstrip("\n")
        if got != expected:
            failures.append((text, expected, got))
    return failures
