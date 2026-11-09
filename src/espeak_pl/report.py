"""Markdown reports from saved evaluation runs."""

from __future__ import annotations

from pathlib import Path


def _percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def display_path(path: str) -> str:
    """Path for a shared report: the home folder becomes ~, so no user name leaks."""
    home = str(Path.home())
    return "~" + path[len(home):] if path == home or path.startswith(home + "/") else path


def render(run: dict, title: str, failures: int = 40) -> str:
    """Summary, error groups, top confusions and (for hard cases) every failure."""
    meta, summary = run["meta"], run["summary"]
    lines = [
        f"# {title}",
        "",
        f"- source: `{meta.get('source', '')}`",
        f"- espeak-ng data: `{display_path(meta.get('data_dir', ''))}`",
        f"- piper-tts: `{meta.get('piper_tts', '')}`",
        "",
        "| metric | value |",
        "|---|---|",
        f"| entries | {summary['entries']} |",
        f"| wrong entries | {summary['errors']} |",
        f"| word error rate | {_percent(summary['word_error_rate'])} |",
        f"| phoneme error rate | {_percent(summary['phoneme_error_rate'])} |",
        f"| stress checked / wrong | {summary['stress_checked']} / {summary['stress_errors']} |",
        "",
        "## Error groups (orthographic pattern)",
        "",
        "| group | words | wrong | error rate |",
        "|---|---:|---:|---:|",
    ]
    for name, group in sorted(
        summary["categories"].items(), key=lambda item: -item[1]["error_rate"]
    ):
        lines.append(
            f"| {name} | {group['words']} | {group['errors']} | {_percent(group['error_rate'])} |"
        )

    lines += [
        "",
        "## Most common confusions (expected → espeak)",
        "",
        "| expected | espeak | words | examples |",
        "|---|---|---:|---|",
    ]
    for confusion in summary["confusions"][:40]:
        lines.append(
            f"| `{confusion['expected']}` | `{confusion['got']}` | {confusion['words']} "
            f"| {', '.join(confusion['examples'])} |"
        )

    wrong = [result for result in run["results"] if not (result["phonemes_ok"] and result["stress_ok"] is not False)]
    if wrong:
        lines += [
            "",
            f"## Wrong entries (first {min(failures, len(wrong))} of {len(wrong)})",
            "",
            "| text | category | espeak | expected |",
            "|---|---|---|---|",
        ]
        for result in wrong[:failures]:
            reason = " (stress)" if result["phonemes_ok"] else ""
            lines.append(
                f"| {result['text']} | {result['category']}{reason} | `{result['output']}` "
                f"| `{' / '.join(result['references'])}` |"
            )
    return "\n".join(lines) + "\n"


def render_comparison(diff: dict, limit: int = 200) -> str:
    lines = [f"# Fixed: {len(diff['fixed'])}, broken: {len(diff['broken'])}", ""]
    for name in ("broken", "fixed"):
        if not diff[name]:
            continue
        lines += [f"## {name}", "", "| text | before | after |", "|---|---|---|"]
        lines += [f"| {text} | `{before}` | `{after}` |" for text, before, after in diff[name][:limit]]
        lines.append("")
    return "\n".join(lines)
