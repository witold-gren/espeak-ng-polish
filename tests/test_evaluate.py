import json

from espeak_pl.evaluate import check, compare, evaluate, in_category, load, save, summarize
from espeak_pl.lexicon import Entry


def test_check_accepts_notation_differences():
    result = check(Entry("szczęście", ["ʂt͡ʂɛɲɕt͡ɕɛ"]), "ʃtʃˈɛɲɕtɕɛ")
    assert result.ok and result.distance == 0


def test_check_reports_phoneme_edits():
    result = check(Entry("grozić", ["ɡrɔʑit͡ɕ"]), "ɡrˈɔzitɕ")
    assert not result.ok
    assert result.edits == [("ʑ", "z")]
    assert result.length == 6


def test_check_uses_the_closest_alternative():
    result = check(Entry("od razu", ["ɔtrazu", "ɔdrazu"]), "ɔd rˈazu")
    assert result.ok


def test_check_stress_only_when_reference_has_it():
    assert check(Entry("okej", ["ɔˈkɛj"]), "ˈɔkɛj").stress_ok is False
    assert check(Entry("okej", ["ɔˈkɛj"]), "ɔkˈɛj").stress_ok is True
    assert check(Entry("okej", ["ɔkɛj"]), "ˈɔkɛj").stress_ok is None


def test_in_category_case_rules():
    assert in_category("proper_noun", "Bydgoszcz")
    assert not in_category("proper_noun", "bydgoski")
    assert in_category("prefix_before_vowel", "Bezimienny")


def test_summarize_rates_groups_and_confusions():
    results = evaluate(
        [Entry("grozić", ["grɔʑitɕ"]), Entry("dom", ["dɔm"])],
        {"grozić": "ɡrˈɔzitɕ", "dom": "dˈɔm"}.get,
    )
    summary = summarize(results)
    assert summary["entries"] == 2 and summary["errors"] == 1
    assert summary["word_error_rate"] == 0.5
    assert summary["confusions"][0]["expected"] == "ʑ"
    assert summary["confusions"][0]["examples"] == ["grozić"]
    assert summary["categories"]["zi_si_ci_dzi_ni"]["errors"] == 1


def test_save_load_and_compare(tmp_path):
    entries = [Entry("grozić", ["grɔʑitɕ"]), Entry("dom", ["dɔm"])]
    before = evaluate(entries, {"grozić": "grɔzitɕ", "dom": "dɔm"}.get)
    after = evaluate(entries, {"grozić": "grɔʑitɕ", "dom": "dɔn"}.get)
    save(tmp_path / "before.json", before, {"source": "test"})
    save(tmp_path / "after.json", after, {"source": "test"})
    assert json.loads((tmp_path / "before.json").read_text(encoding="utf-8"))["meta"]["source"] == "test"
    diff = compare(load(tmp_path / "before.json"), load(tmp_path / "after.json"))
    assert [text for text, *_ in diff["fixed"]] == ["grozić"]
    assert [text for text, *_ in diff["broken"]] == ["dom"]
