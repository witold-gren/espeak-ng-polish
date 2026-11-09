import subprocess

from espeak_pl.patches import PatchResult, apply_patch, render, touches_phonemes, upstream_tests

TEST_SCRIPT = '''#!/bin/sh
. "`dirname $0`/common"
test_phon pa "x" "y" "Guru"
test_phon pl "m'E~Zny
z'aZuwdz;" "Mężny. Zażółć." "Latn"
test_phon pl "dzvˈɔn" "dzwon" "Polish IPA" "--ipa"
test_phon pt "a" "b" "Latn"
'''


def test_upstream_tests_reads_multiline_calls_and_options(tmp_path):
    path = tmp_path / "language-pronunciation.test"
    path.write_text(TEST_SCRIPT, encoding="utf-8")
    assert upstream_tests(path) == [
        ("m'E~Zny\nz'aZuwdz;", "Mężny. Zażółć.", ""),
        ("dzvˈɔn", "dzwon", "--ipa"),
    ]
    assert upstream_tests(path, "pt") == [("a", "b", "")]


def test_touches_phonemes(tmp_path):
    rules = tmp_path / "a.patch"
    rules.write_text("--- a/dictsource/pl_rules\n+++ b/dictsource/pl_rules\n", encoding="utf-8")
    phonemes = tmp_path / "b.patch"
    phonemes.write_text("--- a/phsource/ph_polish\n+++ b/phsource/ph_polish\n", encoding="utf-8")
    assert not touches_phonemes(rules)
    assert touches_phonemes(phonemes)


def test_apply_patch_outside_a_repository(tmp_path):
    tree = tmp_path / "tree"
    (tree / "dictsource").mkdir(parents=True)
    (tree / "dictsource" / "pl_rules").write_text("a\nb\n", encoding="utf-8")
    original = tmp_path / "orig"
    (original / "dictsource").mkdir(parents=True)
    (original / "dictsource" / "pl_rules").write_text("a\nb\n", encoding="utf-8")
    changed = tmp_path / "new"
    (changed / "dictsource").mkdir(parents=True)
    (changed / "dictsource" / "pl_rules").write_text("a\nc\n", encoding="utf-8")
    diff = subprocess.run(
        ["git", "diff", "--no-index", "--src-prefix=a/", "--dst-prefix=b/", "orig/dictsource/pl_rules", "new/dictsource/pl_rules"],
        cwd=tmp_path, capture_output=True, text=True,
    ).stdout.replace("a/orig/", "a/").replace("b/new/", "b/")
    patch = tmp_path / "0001.patch"
    patch.write_text(diff, encoding="utf-8")
    apply_patch(tree, patch)
    assert (tree / "dictsource" / "pl_rules").read_text(encoding="utf-8") == "a\nc\n"


def test_render_table():
    text = render([PatchResult("0001-x.patch", {
        "wikipron": {"fixed": 3, "broken": 0, "fixed_examples": ["grozić"], "broken_examples": []},
        "hard": {"fixed": 1, "broken": 0, "fixed_examples": ["guzik"], "broken_examples": []},
    })])
    assert "| 0001-x.patch | 3 | 0 | 1 | 0 | guzik, grozić |" in text
