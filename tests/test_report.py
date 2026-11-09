from espeak_pl.evaluate import evaluate, summarize
from espeak_pl.lexicon import Entry
from pathlib import Path

from espeak_pl.report import display_path, render, render_comparison


def _run():
    results = evaluate(
        [Entry("grozić", ["grɔʑitɕ"], "zi_si"), Entry("okej", ["ɔˈkɛj"], "stress")],
        {"grozić": "grɔzitɕ", "okej": "ˈɔkɛj"}.get,
    )
    return {
        "meta": {"source": "hard", "data_dir": "/x", "piper_tts": "1.8.0"},
        "summary": summarize(results),
        "results": [result.__dict__ for result in results],
    }


def test_render_lists_metrics_groups_and_failures():
    text = render(_run(), "Test")
    assert text.startswith("# Test")
    assert "| word error rate | 100.00% |" in text
    assert "| grozić | zi_si |" in text
    assert "| okej | stress (stress) |" in text
    assert "`ʑ` | `z`" in text


def test_render_comparison():
    text = render_comparison({"fixed": [("dom", "a", "b")], "broken": []})
    assert text.startswith("# Fixed: 1, broken: 0")
    assert "| dom | `a` | `b` |" in text
    assert "## broken" not in text


def test_display_path_hides_the_home_folder():
    home = str(Path.home())
    assert display_path(f"{home}/espeak-ng-polish/build") == "~/espeak-ng-polish/build"
    assert display_path(home + "other/x") == home + "other/x"
    assert display_path("/opt/data") == "/opt/data"


def test_render_does_not_show_the_home_folder():
    run = _run()
    run["meta"]["data_dir"] = f"{Path.home()}/x/espeak-ng-data"
    assert "`~/x/espeak-ng-data`" in render(run, "Test")
