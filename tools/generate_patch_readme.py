"""Write patches/README.md: description, numbers and the upstream test line of every patch.

Needs `make patch-report` first (per-patch builds in build/patches/); "before" is the
espeak-ng-data bundled in piper-tts. Run with the project environment (.venv/bin/python).
Usage: python tools/generate_patch_readme.py [patches/topics.json]
"""

import json, subprocess, sys
from pathlib import Path

from piper.phonemize_espeak import ESPEAK_DATA_DIR

BASELINE_ROOT = str(Path(ESPEAK_DATA_DIR).parent)
report = {r["name"].removesuffix(".patch"): r["sources"] for r in json.load(open("build/patches/patch-report.json", encoding="utf-8"))}
topics = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "patches/topics.json", encoding="utf-8"))
def run(path, text, opt):
    cmd = ["espeak-ng", f"--path={path}", "-xq", *([opt] if opt else []), "-v", "pl", text]
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout.rstrip("\n")
out = ["# Patches for espeak-ng Polish / Łatki dla polskiego w espeak-ng", "",
 "Each patch is independent and made against espeak-ng `724808c` (pinned by piper1-gpl); apply with `git apply` in an espeak-ng clone. "
 "Upstream asks for one problem per pull request, with a test: use one patch + its `test_phon` line per PR. "
 "`0010` holds all test lines together for local use (test lines of separate PRs touch the same spot of the file, rebase after each merge). "
 "Numbers: `make patch-report` (each patch alone, compared with Piper's espeak-ng).", "",
 "Każda łatka jest niezależna i zrobiona względem espeak-ng `724808c` (wersja przypięta w piper1-gpl); nakłada się `git apply` w klonie espeak-ng. "
 "espeak-ng wymaga jednego problemu na PR i testu: jedna łatka + jej linia `test_phon` = jeden PR. "
 "`0010` zawiera wszystkie linie testów razem, do użytku lokalnego (testy osobnych PR-ów zmieniają to samo miejsce pliku, po każdym scaleniu trzeba zrobić rebase). "
 "Liczby: `make patch-report` (każda łatka osobno, w porównaniu z espeak-ng z Pipera).", "",
 "| patch | WikiPron fixed / broken | hard cases fixed / broken |", "|---|---:|---:|"]
for t in topics:
    r = report[t["name"]]
    out.append(f"| [{t['name']}](#{t['name']}) | {r['wikipron']['fixed']} / {r['wikipron']['broken']} | {r['hard']['fixed']} / {r['hard']['broken']} |")
out.append("")
for t in topics:
    name, text, opt = t["name"], t["text"], t["opt"]
    before = run(BASELINE_ROOT, text, opt); after = run(f"build/patches/{name}/data", text, opt)
    r = report[name]["wikipron"]
    test = f'test_phon pl "{after}" "{text}"' + (f' "" "{opt}"' if opt else "")
    out += [f"## {name}", "", f"**{t['title_en']}**: {t['en']}", "", f"**{t['title_pl']}**: {t['pl']}", "",
            f"Examples fixed / przykłady: {', '.join(r['fixed_examples'][:8]) or '-'}", "",
            "```", f"before: {before}", f"after:  {after}", "```", "",
            "Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:", "",
            "```sh", test, "```", ""]
out += ["## 0010-polish-regression-tests", "",
        "All test lines above in one patch, for the local tree with every patch applied (`make upstream-test`). / "
        "Wszystkie linie testów w jednej łatce, do lokalnego drzewa ze wszystkimi łatkami (`make upstream-test`).", ""]
open("patches/README.md", "w", encoding="utf-8").write("\n".join(out))
print("ok")
