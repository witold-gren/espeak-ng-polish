"""Build a candidate espeak-ng-data folder from an espeak-ng source tree.

Only the data changes: the folder starts as a copy of the one bundled in
piper-tts and gets a new `pl_dict` compiled from `dictsource/pl_rules`,
`pl_list` (and `pl_extra` when present). With `phonemes=True` the phoneme
tables are rebuilt from `phsource` too (needed after editing `ph_polish`).
The compiler is any `espeak-ng` binary (Homebrew 1.52 gives identical output
to the library pinned by Piper for `pl_dict`).
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from .phonemizer import bundled_data_dir


def compile_data(
    source: Path,
    output: Path,
    espeak: str = "espeak-ng",
    phonemes: bool = False,
    base: Path | None = None,
) -> Path:
    """Return the path of the new espeak-ng-data folder (output/espeak-ng-data)."""
    source, output = source.resolve(), output.resolve()
    dictsource = source / "dictsource"
    if not (dictsource / "pl_rules").is_file():
        raise FileNotFoundError(f"{dictsource / 'pl_rules'} not found")
    if shutil.which(espeak) is None:
        raise FileNotFoundError(f"{espeak} not found (macOS: brew install espeak-ng)")

    data_dir = output / "espeak-ng-data"
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copytree(base or bundled_data_dir(), data_dir)

    if phonemes:
        _run([espeak, f"--path={output}", f"--compile-phonemes={source / 'phsource'}"], source)
    _run([espeak, f"--path={output}", "--compile=pl"], dictsource)
    return data_dir


def _run(command: list[str], cwd: Path) -> None:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    output = (completed.stdout + completed.stderr).strip()
    if completed.returncode != 0 or _has_errors(output):
        raise RuntimeError(f"{' '.join(command)} failed:\n{output}")


def _has_errors(output: str) -> bool:
    """espeak-ng reports "N errors" and exits 0; any non-zero count is a failure."""
    counts = re.findall(r"(\d+) errors?", output)
    return any(int(count) for count in counts) or "error:" in output.lower()
