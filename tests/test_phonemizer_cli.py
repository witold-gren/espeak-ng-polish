"""Integration with the espeak-ng bundled in piper-tts (one data folder per process)."""

import json

import pytest

from espeak_pl.cli import build_parser, main
from espeak_pl.phonemizer import Phonemizer, bundled_data_dir


def test_bundled_phonemizer_reads_polish():
    phonemizer = Phonemizer()
    assert phonemizer.data_dir == bundled_data_dir()
    assert "ʑ" in phonemizer.phonemize("zimny")
    assert phonemizer.phonemize("dom") == "dˈɔm"


def test_second_data_folder_in_the_same_process_is_refused(tmp_path):
    Phonemizer()
    with pytest.raises(RuntimeError, match="separate process"):
        Phonemizer(tmp_path)


def test_cli_say(capsys):
    assert main(["say", "dom"]) == 0
    assert capsys.readouterr().out == "dom\tdˈɔm\n"


def test_cli_evaluate_and_report(tmp_path, capsys):
    cases = tmp_path / "hard.tsv"
    cases.write_text("text\tipa\tcategory\tnote\ndom\tdɔm\tbasic\t\nzimny\tʑimnɨ\tzi_si\t\n", encoding="utf-8")
    output = tmp_path / "run.json"
    assert main(["evaluate", "hard", "--input", str(cases), "--output", str(output)]) == 0
    assert "2 entries, 0 wrong" in capsys.readouterr().out
    assert json.loads(output.read_text(encoding="utf-8"))["summary"]["errors"] == 0
    report = tmp_path / "run.md"
    assert main(["report", str(output), "--output", str(report)]) == 0
    assert "| entries | 2 |" in report.read_text(encoding="utf-8")


def test_cli_compare_strict(tmp_path):
    run = {"meta": {}, "summary": {}, "results": [
        {"text": "dom", "output": "dɔm", "phonemes_ok": True, "stress_ok": None}]}
    worse = {"meta": {}, "summary": {}, "results": [
        {"text": "dom", "output": "dɔn", "phonemes_ok": False, "stress_ok": None}]}
    (tmp_path / "a.json").write_text(json.dumps(run), encoding="utf-8")
    (tmp_path / "b.json").write_text(json.dumps(worse), encoding="utf-8")
    out = str(tmp_path / "c.md")
    assert main(["compare", str(tmp_path / "a.json"), str(tmp_path / "b.json"), "--output", out]) == 0
    assert main(["compare", str(tmp_path / "a.json"), str(tmp_path / "b.json"), "--output", out, "--strict"]) == 1


def test_parser_has_every_command():
    commands = build_parser()._subparsers._group_actions[0].choices
    assert set(commands) == {"fetch", "compile", "say", "evaluate", "report", "compare", "patch-report", "upstream-test"}
