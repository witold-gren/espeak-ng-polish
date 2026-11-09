# espeak-ng and Polish: how it works, what we fix and how to send it upstream

## 1. Why

Piper (piper1-gpl) does not read text directly: espeak-ng turns text into IPA phonemes and only those reach the neural network (VITS) that makes the sound. Wrong phonemes from espeak-ng mean a wrong word, however good the voice. This repository:

- measures Polish text-to-phoneme quality of the same espeak-ng Piper uses,
- lets you edit the rules and see at once what got fixed and whether anything broke,
- prepares patches (`patches/`) with descriptions, numbers and tests for the espeak-ng project.

## 2. How Piper uses espeak-ng

- piper1-gpl builds espeak-ng statically from a pinned commit (`CMakeLists.txt`: `GIT_TAG 724808c`, 2026-04-06); `piper-tts==1.8.0` ships exactly that version with its `espeak-ng-data`.
- Only the **phonemizer** is used (`src/piper/phonemize_espeak.py` → `espeakbridge.get_phonemes()`), output is IPA such as `ɡrˈɔʑitɕ`. The espeak-ng formant synthesizer plays no part.
- The Polish rules are **data only**: `espeak-ng-data/pl_dict` (rules and exceptions) and `phontab`/`phonindex`/`phondata` (phoneme tables, where IPA symbols come from). No C or Piper rebuild is needed, only these files.
- **Important:** Piper voices learn from phonemes of one espeak-ng version. Changed rules give an existing voice slightly different input; the full benefit needs a fine-tune on the new phonemes. Most of our fixes swap one known symbol for another known one (`z`→`ʑ`, `w`→`v`), so they should help without retraining too, but listen before deploying.

## 3. How espeak-ng handles Polish

| File | Contents |
|---|---|
| `espeak-ng-data/lang/zlw/pl` | voice definition: `name Polish`, `language pl`, `intonation 2`; no `maintainer` |
| `dictsource/pl_rules` | ~870 letter-to-phoneme rules in 46 groups |
| `dictsource/pl_list` | exceptions: whole words, abbreviations, numbers, unstressed words |
| `dictsource/pl_extra` | (optional, absent) local additions, appended when compiling |
| `phsource/ph_polish` | Polish phonemes: sound and IPA label (`ipa ...`) |
| `src/libespeak-ng/tr_languages.c` | language options in C: penultimate stress, assimilation |

Rule syntax: `pre) letters (post  phonemes`, `_` word boundary, `C` consonant, `A` vowel, `L01`… letter lists; the rule matching most letters wins. Phonemes are espeak mnemonics, not IPA: `Z;`=ʑ, `S`=ʂ, `Z`=ʐ, `tS`=tʂ, `dz;`=dʑ, `n^`=ɲ, `E~`=ę, `O~`=ą, `R`=r, `w`=**ł**, `v`=w, `x`=ch, `'` stress. Trace which rule fired: `espeak-ng -v pl -X "word"`.

Stress (penultimate, exceptions via rule markers and `pl_list`) works very well: *matematyka, polityka, zrobilibyśmy, czterysta*, even *NIE wiem*. Final devoicing, word-internal and **cross-word** voicing assimilation work too (*jak było* → `jag bɨwɔ`, *w Polsce* → `f pɔlstsɛ`).

## 4. Measurement

1. **WikiPron** (`make fetch`): 157k Polish Wiktionary entries with IPA, 148,896 single words after filtering. CC BY-SA: used **for measurement only**, never copied into espeak-ng (GPL).
2. **Normalisation** (`src/espeak_pl/ipa.py`): both sides mapped to one notation (`ʃ`/`ʂ`, `ʲ`/`j`, `ɔ̃`/`ɔw̃`, `ŋk`/`nk`, `ç`/`x`, stress marks, ties) so only real pronunciation differences count.
3. **Hard cases** (`data/hard_cases.tsv`): hand-checked words and phrases (prepositions, stress, cross-word voicing) that WikiPron lacks; alternatives split by `|`, stress checked when the reference has `ˈ`.
4. **Metrics**: word error rate, phoneme error rate, error groups by spelling, top phoneme confusions with examples.

## 5. Results

| | Piper (espeak-ng 724808c) | with patches 0001–0014 |
|---|---:|---:|
| WikiPron wrong words | 4506 / 148,896 (3.03%) | 2192 (1.47%) |
| WikiPron phoneme error rate | 0.50% | 0.30% |
| hard cases wrong | 53 / 115 (46.1%) | 2 (1.7%) |
| broken by the patches | - | 0 |

Main bugs found (details: [patches/README.md](../patches/README.md)): the preposition **w** read as **ł**; **zi/si** before a consonant read hard (*grozić, guzik, dusimy*); **dz** and **dź** with the same IPA `dʑ` (1811 words); *ch* → `h`, *dg* → `dʒ` (*Bydgoszcz*), *mchu* → "mekchu", *doszedł* → `dɔʂɛd`, *barcią*, *Ewangelia*; and the things `pl_tts` in polish-piper works around: *ul., al., tel., godz., nr* read as words, *ok* without a dot as *około*, *AGD* as *akt*, **a minus before a number dropped** (*-3* → *trzy*), *iPhone* → *i fone* (patches 0011–0014, section 9).

## 6. Workflow

```sh
make doctor              # espeak-ng compiler (brew install espeak-ng), ../espeak-ng clone, word list
make baseline            # measure Piper's espeak-ng → reports/baseline-*.md
# edit ../espeak-ng/dictsource/pl_rules, pl_list or phsource/ph_polish
make say TEXT="grozić w domu"
make candidate           # compile + measure → reports/candidate-*.md
make compare             # fixed/broken lists, fails on any regression
make test-all            # tool tests + Polish espeak-ng tests on the candidate
make branch ESPEAK_SRC=../espeak-ng   # any branch vs its merge base with upstream/master (BASE_REF)
```

Homebrew `espeak-ng` 1.52 compiles the data; compiling the untouched 724808c rules and phonemes gives phonemes identical to Piper's for all 148,896 words, so no espeak-ng build from source is needed. New patch: `tools/make_topic_patch.py`, describe it in `patches/topics.json`, then `make patch-report`.

## 7. Contributing upstream

espeak-ng asks for **one problem per pull request** with a description and a **test**, passing `ctest`, no conflicts. Language changes are reviewed by the language maintainer: **Polish has none**; volunteer by adding `maintainer Name <e-mail>` to `espeak-ng-data/lang/zlw/pl`. Replies take 1–2 weeks. Steps: an issue with the results table (link #2295), a fork, then per patch a branch from `master` + `git apply` + its `test_phon` line from `patches/README.md` + commit + PR; start with 0008 (w) and 0002 (dz). Rebase and re-run `make candidate compare` before each PR.

## 8. Using it in our Piper before upstream merges

Copy `pl_dict`, `phontab`, `phonindex`, `phondata` from `build/candidate/espeak-ng-data` over `site-packages/piper/espeak-ng-data` in the `polish-piper` image (or point piper1-gpl `GIT_TAG` at the fork and rebuild). Listen to the same sentences before/after; fine-tune voices (piper-voice-cloner) on the new phonemes.

## 9. espeak-ng vs pl_tts and Morfeusz (polish-piper)

[home-assistant-polish-piper](https://github.com/witold-gren/home-assistant-polish-piper) rewrites text before espeak-ng (`pl_tts`) and uses Morfeusz 2. What could espeak-ng do itself?

| Problem | espeak-ng today | Where to fix |
|---|---|---|
| numeral–noun agreement (*z dwiema osobami*) | *z dwa osobami* | `pl_tts` + Morfeusz: needs the noun's gender, case and the sentence context |
| times and dates (*o 9:05*, *20.10.2026*) | digits | `pl_tts`: the form depends on the preposition |
| units (*6°C*, *50 km/h*) | symbols spelled | `pl_tts`: number and case depend on the number |
| ordinals, Roman numerals (*2. piętro*, *XXI wieku*) | cardinals, letters | `pl_tts`: the form depends on the noun |
| phone numbers (*+48 600 100 200*) | *six hundred billion…* | `pl_tts`: a space inside a number is a thousands separator for espeak |
| *np., itd., itp., prof., św., ok., dr, mgr*, e-mail addresses | right | already in espeak-ng |
| *ul., al., tel., godz., nr*, *ok* without a dot | read as words / spelled / *około* | **espeak-ng, patch 0011** |
| *AGD, SMS* | read as words | **espeak-ng, patch 0012** |
| minus before a number (*-3*) | dropped | **espeak-ng, patch 0013**; `−` (U+2212) already fixed on master (#2451) |
| *iPhone, iPad, YouTube, Google, Facebook* | *i fone*, *go-ogle* | **espeak-ng, patch 0014**; niche and private names stay in `pl_tts` |
| *m.in.* | *em kropka in* | `pl_tts`: dotted multi-word entries do not work in `pl_list` |

espeak-ng sees the letters of one word and fixed dictionary entries, with no morphology and no sentence context. Everything that depends on inflection stays in `pl_tts` with Morfeusz (which does not help pronunciation either: it does not split prefixes). Fixed spellings belong to espeak-ng: abbreviations, acronyms, symbols, common loanwords. Once the patches reach Piper (or the data is overlaid in the image, section 8), their counterparts in `pl_tts` can go.

## 10. Next

Loanwords in `-nia` (*Albania, agonia*), foreign words and names (partly a job for `pl_tts` text normalisation), and every mispronunciation heard in Piper as a new line in `data/hard_cases.tsv`.

## 11. FAQ

- **`espeak-ng already uses …; compare another data folder in a separate process`**: espeak-ng loads one data folder per process; run each measurement as its own command.
- **`espeak-ng not found (macOS: brew install espeak-ng)`**: install it, or `make compile ESPEAK=/path/espeak-ng`.
- **`… --compile=pl failed: … N errors`**: syntax error in `pl_rules`/`pl_list`; the message has the line number (unknown phoneme mnemonic, spaces instead of a tab in `pl_list`).
- **`… pl_rules not found`**: `ESPEAK_SRC` is not an espeak-ng clone.
- **`missing baseline runs: … (make baseline)`**: run `make baseline` first.
- **`make compare` fails with `fixed N, broken M`**: see the `broken` section of `reports/compare-*.md`; add a narrow exception.
- **`Reversed (or previously applied) patch detected`**: the patch is already in that tree.
- **`error: patch failed: dictsource/pl_list:545` / `patch does not apply` on a clone with other patches**: each patch is made on clean `master`, so neighbouring patches (0009 and 0011 touch the same spot of `pl_list`) do not stack. Upstream PRs go one by one with a rebase; locally apply the change by hand or regenerate it with `tools/make_topic_patch.py`.
- **`git apply` cannot find a patch given by a relative path**: `git -C ../espeak-ng apply patches/…` resolves it against the clone; use an absolute path (`tools/make_topic_patch.py` does).
- **Is Homebrew espeak-ng 1.52 equal to Piper's 724808c?** Yes for compiled Polish data (verified on 148,896 words); re-check when Piper moves its pin.
- **`workflow ci.yml not found on the default branch` on a fork**: GitHub registers no workflows in a new fork until you confirm them in its Actions tab, and `ci.yml` runs only on `master`, pull requests and manual dispatch. A push to a branch of the fork starts nothing; the first full run is on the pull request.
- **`The configuration 'macos-14-arm64-us-default' is not supported` (macOS jobs cancelled on a pull request)**: GitHub refuses that runner, the job never starts and no test runs. It is not caused by the patch: since 2026-11-06 unrelated pull requests fail the same way. The fix belongs in `.github/workflows/ci.yml` upstream.
- **`no merge base with upstream/master` from `make branch`**: the espeak-ng clone has no `upstream` remote: `git -C ../espeak-ng remote add upstream https://github.com/espeak-ng/espeak-ng.git && git -C ../espeak-ng fetch upstream`, or pass `BASE_REF=origin/master`.
