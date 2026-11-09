"""Text to IPA with the same espeak-ng library that Piper uses.

piper-tts bundles espeak-ng (piper1-gpl pins the commit in CMakeLists.txt) as
the `espeakbridge` extension. Pointing it at another `espeak-ng-data` folder,
for example one compiled from a fork with changed `pl_rules`, tests new rules
without rebuilding Piper: the Polish rules live only in the data file `pl_dict`.
"""

from __future__ import annotations

from pathlib import Path

from piper import espeakbridge
from piper.phonemize_espeak import ESPEAK_DATA_DIR

VOICE = "pl"

_initialized_with: str | None = None


def bundled_data_dir() -> Path:
    """espeak-ng-data shipped inside the installed piper-tts."""
    return Path(ESPEAK_DATA_DIR)


class Phonemizer:
    """Polish phonemizer; one data folder per process (espeak-ng is global)."""

    def __init__(self, data_dir: Path | str | None = None) -> None:
        global _initialized_with
        path = str(Path(data_dir) if data_dir else bundled_data_dir())
        if _initialized_with is None:
            espeakbridge.initialize(path)
            _initialized_with = path
        elif _initialized_with != path:
            raise RuntimeError(
                f"espeak-ng already uses {_initialized_with}; "
                "compare another data folder in a separate process"
            )
        espeakbridge.set_voice(VOICE)
        self.data_dir = Path(path)

    def phonemize(self, text: str) -> str:
        """IPA with stress marks; clauses joined with a space."""
        clauses = espeakbridge.get_phonemes(text)
        return " ".join(phonemes for phonemes, _terminator, _end in clauses).strip()
