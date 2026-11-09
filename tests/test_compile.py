import os
import stat

import pytest

from espeak_pl.compile import _has_errors, compile_data


def test_has_errors():
    assert not _has_errors("Compiled phonemes: 0 errors.")
    assert _has_errors("Compiled phonemes: 3 errors.")
    assert _has_errors("1 error in pl_rules")
    assert _has_errors("Error: can't read file")
    assert not _has_errors("869 rules, 46 groups (0)")


def _fake_espeak(tmp_path, exit_code=0, message="0 errors"):
    """Records its arguments and working directory instead of compiling."""
    log = tmp_path / "calls.log"
    script = tmp_path / "fake-espeak"
    script.write_text(
        f'#!/bin/sh\necho "$(pwd) $*" >> "{log}"\necho "{message}"\nexit {exit_code}\n',
        encoding="utf-8",
    )
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return str(script), log


def _source(tmp_path):
    source = tmp_path / "espeak-ng"
    (source / "dictsource").mkdir(parents=True)
    (source / "dictsource" / "pl_rules").write_text(".group a\n", encoding="utf-8")
    (source / "phsource").mkdir()
    base = tmp_path / "base"
    base.mkdir()
    (base / "phontab").write_bytes(b"x")
    return source, base


def test_compile_copies_base_and_compiles_dictionary(tmp_path):
    source, base = _source(tmp_path)
    espeak, log = _fake_espeak(tmp_path)
    data_dir = compile_data(source, tmp_path / "out", espeak, base=base)
    assert data_dir == (tmp_path / "out" / "espeak-ng-data").resolve()
    assert (data_dir / "phontab").read_bytes() == b"x"
    (call,) = log.read_text(encoding="utf-8").splitlines()
    assert call.startswith(os.path.realpath(source / "dictsource"))
    assert "--compile=pl" in call


def test_compile_phonemes_first(tmp_path):
    source, base = _source(tmp_path)
    espeak, log = _fake_espeak(tmp_path)
    compile_data(source, tmp_path / "out", espeak, phonemes=True, base=base)
    calls = log.read_text(encoding="utf-8").splitlines()
    assert "--compile-phonemes=" in calls[0] and "--compile=pl" in calls[1]


def test_compile_reports_compiler_errors(tmp_path):
    source, base = _source(tmp_path)
    espeak, _log = _fake_espeak(tmp_path, message="2 errors")
    with pytest.raises(RuntimeError, match="2 errors"):
        compile_data(source, tmp_path / "out", espeak, base=base)


def test_compile_needs_rules_and_compiler(tmp_path):
    with pytest.raises(FileNotFoundError, match="pl_rules"):
        compile_data(tmp_path, tmp_path / "out")
    source, base = _source(tmp_path)
    with pytest.raises(FileNotFoundError, match="brew install espeak-ng"):
        compile_data(source, tmp_path / "out", "no-such-espeak-binary", base=base)
