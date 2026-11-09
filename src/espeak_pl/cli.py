"""Command line: espeak-pl fetch | compile | say | evaluate | report | compare | patch-report | upstream-test."""

from __future__ import annotations

import argparse
import sys
from importlib.metadata import version
from pathlib import Path

from . import evaluate as evaluation
from . import lexicon, report


def _phonemizer(data_dir: str | None):
    from .phonemizer import Phonemizer

    return Phonemizer(data_dir)


def cmd_fetch(args: argparse.Namespace) -> int:
    path = lexicon.fetch_wikipron(Path(args.output))
    print(f"saved {path} ({sum(1 for _ in path.open(encoding='utf-8'))} lines)")
    return 0


def cmd_compile(args: argparse.Namespace) -> int:
    from .compile import compile_data

    data_dir = compile_data(Path(args.source), Path(args.output), args.espeak, args.phonemes)
    print(f"compiled {data_dir}")
    return 0


def cmd_say(args: argparse.Namespace) -> int:
    phonemizer = _phonemizer(args.data_dir)
    for text in args.text:
        print(f"{text}\t{phonemizer.phonemize(text)}")
    return 0


def cmd_evaluate(args: argparse.Namespace) -> int:
    if args.source == "wikipron":
        entries = lexicon.load_wikipron(Path(args.input or lexicon.WIKIPRON_FILE))
    else:
        entries = lexicon.load_hard_cases(Path(args.input or lexicon.HARD_CASES_FILE))
    if args.limit:
        entries = entries[: args.limit]
    phonemizer = _phonemizer(args.data_dir)
    results = evaluation.evaluate(entries, phonemizer.phonemize)
    meta = {
        "source": args.input or args.source,
        "data_dir": str(phonemizer.data_dir),
        "piper_tts": version("piper-tts"),
    }
    evaluation.save(Path(args.output), results, meta)
    summary = evaluation.summarize(results)
    print(
        f"{summary['entries']} entries, {summary['errors']} wrong, "
        f"WER {summary['word_error_rate']:.2%}, PER {summary['phoneme_error_rate']:.2%}"
        f", stress wrong {summary['stress_errors']}/{summary['stress_checked']}"
    )
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    run = evaluation.load(Path(args.run))
    text = report.render(run, args.title or Path(args.run).stem, args.failures)
    _write(args.output, text)
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    diff = evaluation.compare(evaluation.load(Path(args.before)), evaluation.load(Path(args.after)))
    _write(args.output, report.render_comparison(diff))
    print(f"fixed {len(diff['fixed'])}, broken {len(diff['broken'])}", file=sys.stderr)
    return 1 if diff["broken"] and args.strict else 0


def cmd_patch_report(args: argparse.Namespace) -> int:
    from . import patches

    files = sorted(Path(args.patches).glob("*.patch"))
    baselines = {"wikipron": Path(args.wikipron_baseline), "hard": Path(args.hard_baseline)}
    missing = [str(path) for path in baselines.values() if not path.is_file()]
    if missing:
        print(f"missing baseline runs: {', '.join(missing)} (make baseline)", file=sys.stderr)
        return 1
    results = patches.measure(Path(args.source), files, Path(args.work), baselines, args.commit)
    patches.save(results, Path(args.work) / "patch-report.json")
    _write(args.output, patches.render(results))
    return 1 if any(source["broken"] for result in results for source in result.sources.values()) else 0


def cmd_upstream_test(args: argparse.Namespace) -> int:
    from . import patches

    test_file = Path(args.source) / "tests" / "language-pronunciation.test"
    calls = patches.upstream_tests(test_file)
    failures = patches.run_upstream_tests(test_file, Path(args.data_root), args.espeak)
    for text, expected, got in failures:
        print(f"FAIL {text}\n  expected: {expected!r}\n  got:      {got!r}")
    print(f"{len(calls) - len(failures)}/{len(calls)} Polish tests passed")
    return 1 if failures else 0


def _write(output: str | None, text: str) -> None:
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="espeak-pl", description=__doc__)
    parser.add_argument("--version", action="version", version=version("espeak-ng-polish"))
    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="download the WikiPron Polish lexicon")
    fetch.add_argument("--output", default=str(lexicon.WIKIPRON_FILE))
    fetch.set_defaults(func=cmd_fetch)

    comp = sub.add_parser("compile", help="build espeak-ng-data with pl_dict from a source tree")
    comp.add_argument("--source", default="../espeak-ng", help="espeak-ng source tree (fork)")
    comp.add_argument("--output", default="build/candidate")
    comp.add_argument("--espeak", default="espeak-ng", help="espeak-ng binary used as the compiler")
    comp.add_argument("--phonemes", action="store_true", help="also rebuild phoneme tables")
    comp.set_defaults(func=cmd_compile)

    say = sub.add_parser("say", help="print espeak-ng IPA for words or phrases")
    say.add_argument("text", nargs="+")
    say.add_argument("--data-dir", help="espeak-ng-data folder (default: the one in piper-tts)")
    say.set_defaults(func=cmd_say)

    run = sub.add_parser("evaluate", help="check espeak-ng against a reference list")
    run.add_argument("source", choices=["wikipron", "hard"])
    run.add_argument("--input", help="reference file (default depends on source)")
    run.add_argument("--data-dir", help="espeak-ng-data folder (default: the one in piper-tts)")
    run.add_argument("--limit", type=int, default=0)
    run.add_argument("--output", required=True, help="JSON file with every result")
    run.set_defaults(func=cmd_evaluate)

    rep = sub.add_parser("report", help="markdown report from a saved run")
    rep.add_argument("run")
    rep.add_argument("--title")
    rep.add_argument("--failures", type=int, default=40, help="how many wrong entries to list")
    rep.add_argument("--output")
    rep.set_defaults(func=cmd_report)

    cmp = sub.add_parser("compare", help="entries fixed and broken between two runs")
    cmp.add_argument("before")
    cmp.add_argument("after")
    cmp.add_argument("--output")
    cmp.add_argument("--strict", action="store_true", help="exit 1 when anything broke")
    cmp.set_defaults(func=cmd_compare)
    rep_patches = sub.add_parser("patch-report", help="measure every patch alone against the pinned commit")
    rep_patches.add_argument("--source", default="../espeak-ng")
    rep_patches.add_argument("--patches", default="patches")
    rep_patches.add_argument("--work", default="build/patches")
    rep_patches.add_argument("--commit", default="724808c")
    rep_patches.add_argument("--wikipron-baseline", default="reports/baseline-wikipron.json")
    rep_patches.add_argument("--hard-baseline", default="reports/baseline-hard.json")
    rep_patches.add_argument("--output")
    rep_patches.set_defaults(func=cmd_patch_report)

    upstream = sub.add_parser("upstream-test", help="run Polish lines of espeak-ng language-pronunciation.test")
    upstream.add_argument("--source", default="../espeak-ng")
    upstream.add_argument("--data-root", default="build/candidate", help="folder that holds espeak-ng-data")
    upstream.add_argument("--espeak", default="espeak-ng")
    upstream.set_defaults(func=cmd_upstream_test)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
