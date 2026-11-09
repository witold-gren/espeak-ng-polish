"""Make one independent patch from exact text edits.

The edits ([file, old, new] triples in a JSON file) are applied to a clean espeak-ng tree
(local changes are stashed), the diff is saved, then the patch is applied on top of the
local changes again. Nothing is committed.
Usage: python tools/make_topic_patch.py ../espeak-ng patches/0011-name.patch edits.json
"""
import json, os, subprocess, sys
repo, edits_json = sys.argv[1], sys.argv[3]
patch_path = os.path.abspath(sys.argv[2])  # git -C would resolve it against the repo
edits = json.load(open(edits_json, encoding="utf-8"))
def git(*a, **k): return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=True, **k)
def apply():
    for path, old, new in edits:
        full = f"{repo}/{path}"; s = open(full, encoding="utf-8").read()
        assert s.count(old) == 1, (path, old)
        open(full, "w", encoding="utf-8").write(s.replace(old, new))
git("stash", "push", "-q")
try:
    apply()
    diff = git("diff").stdout
    open(patch_path, "w", encoding="utf-8").write(diff)
    git("checkout", "-q", ".")
finally:
    git("stash", "pop", "-q")
git("apply", patch_path)
print("saved", patch_path, len(diff.splitlines()), "lines")
