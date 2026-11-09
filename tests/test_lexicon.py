from pathlib import Path

from espeak_pl.lexicon import HARD_CASES_FILE, is_usable_word, load_hard_cases, load_wikipron

ROOT = Path(__file__).resolve().parents[1]


def test_is_usable_word():
    assert is_usable_word("grozić")
    assert is_usable_word("Bydgoszcz")
    assert not is_usable_word("TV")
    assert not is_usable_word("PKP")
    assert not is_usable_word("w domu")
    assert not is_usable_word("3D")
    assert not is_usable_word("")


def test_load_wikipron_groups_pronunciations(tmp_path):
    path = tmp_path / "pol.tsv"
    path.write_text("dom\td ɔ m\nTV\tt i v i\nopera\tɔ p ɛ r a\nopera\tɔ p ɛ r a2\n", encoding="utf-8")
    entries = {entry.text: entry for entry in load_wikipron(path)}
    assert set(entries) == {"dom", "opera"}
    assert entries["dom"].references == ["dɔm"]
    assert len(entries["opera"].references) == 2


def test_load_hard_cases_reads_alternatives_and_skips_comments(tmp_path):
    path = tmp_path / "hard.tsv"
    path.write_text(
        "# comment\ntext\tipa\tcategory\tnote\nod razu\tɔtrazu | ɔdrazu\tvoicing\t\n",
        encoding="utf-8",
    )
    (entry,) = load_hard_cases(path)
    assert entry.text == "od razu"
    assert entry.references == ["ɔtrazu", "ɔdrazu"]
    assert entry.category == "voicing"


def test_shipped_hard_cases_are_complete():
    entries = load_hard_cases(ROOT / HARD_CASES_FILE)
    assert len(entries) >= 80
    for entry in entries:
        assert entry.references, entry.text
        assert entry.category, entry.text


def test_shipped_hard_cases_cover_pl_tts_topics():
    # problems that home-assistant-polish-piper (pl_tts) works around before espeak-ng
    categories = {entry.category for entry in load_hard_cases(ROOT / HARD_CASES_FILE)}
    assert {"abbreviations", "acronyms", "minus", "loanwords"} <= categories
