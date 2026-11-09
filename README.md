# espeak-ng-polish

Measure the Polish text-to-phoneme rules of [espeak-ng](https://github.com/espeak-ng/espeak-ng): compare any espeak-ng branch with its base on 148,896 words from Polish Wiktionary and on a hand-checked list of hard cases, and see exactly which words got better or worse.

Polski opis jest niżej: [Po polsku](#po-polsku).

## Results so far

The patches in [patches/](patches/), measured against espeak-ng `724808c` (the version used by [Piper](https://github.com/OHF-Voice/piper1-gpl)):

| | `724808c` | with all patches |
|---|---:|---:|
| Wiktionary words wrong | 3.03% | 1.47% |
| hard cases wrong | 46.1% | 1.7% |
| words made worse | - | 0 |

Upstream status:
- merged: [#2644](https://github.com/espeak-ng/espeak-ng/pull/2644) (preposition *w*), [#2645](https://github.com/espeak-ng/espeak-ng/pull/2645) (IPA label of *dz*), [#2646](https://github.com/espeak-ng/espeak-ng/pull/2646) (minus before a number);
- open: [#2679](https://github.com/espeak-ng/espeak-ng/pull/2679) (*okej*, *Tarzan*), [#2680](https://github.com/espeak-ng/espeak-ng/pull/2680) (acronyms), [#2681](https://github.com/espeak-ng/espeak-ng/pull/2681) (abbreviations);
- overview and discussion: issue [#2643](https://github.com/espeak-ng/espeak-ng/issues/2643).

## Requirements

- Linux or macOS. On Windows use WSL (Ubuntu).
- Python 3.10, 3.11 or 3.12, plus `git` and `make`.
- An `espeak-ng` program. It is only used to compile the Polish data (`pl_dict` and the phoneme tables); the words are then read by the espeak-ng library bundled in the `piper-tts` Python package.
  - macOS: `brew install espeak-ng`
  - Ubuntu or WSL: `sudo apt install espeak-ng python3-venv make git`

Tested with espeak-ng 1.52. With another version, see the FAQ below.

## Install

```sh
git clone https://github.com/witold-gren/espeak-ng-polish.git
cd espeak-ng-polish
make setup              # Python environment in .venv with piper-tts
make fetch              # downloads the WikiPron word list (about 5 MB)
make doctor             # checks that everything is in place
```

If your Python is not called `python3.12`, add it to every command once, for example `make setup PYTHON=python3`.

## Measure your espeak-ng branch

This is the main use: what does my change fix, and what does it break?

1. Have an espeak-ng clone with your branch checked out, next to this folder, with the official repository as a remote:

   ```sh
   cd ..
   git clone https://github.com/<you>/espeak-ng.git
   cd espeak-ng
   git remote add upstream https://github.com/espeak-ng/espeak-ng.git
   git fetch upstream
   git switch <your-branch>
   cd ../espeak-ng-polish
   ```

2. Run the comparison:

   ```sh
   make branch ESPEAK_SRC=../espeak-ng
   ```

   It finds the commit where your branch left `upstream/master` (the merge base), compiles the Polish data of that commit and of your branch, reads all words with both, and compares. Uncommitted changes in your clone are included. It takes a few minutes. To compare with another base, add `BASE_REF=origin/master` or any other git ref.

3. Read the result. The last lines print the totals, for example:

   ```
   148896 entries, 2695 wrong, WER 1.81%   (base)
   148896 entries, 2300 wrong, WER 1.54%   (your branch)
   fixed 395, broken 0
   ```

   The words themselves are in two files, each with a "broken" and a "fixed" section and the IPA before and after:
   - `reports/branch-compare-wikipron.md`: Wiktionary words;
   - `reports/branch-compare-hard.md`: hard cases.

To check single words or phrases with your branch after `make branch`:

```sh
.venv/bin/espeak-pl say --data-dir build/branch/espeak-ng-data "grozić" "w domu" "Bydgoszcz"
```

Each command reads one data folder; to see the base, run it again with `build/base/espeak-ng-data`.

## What the numbers mean

- **WikiPron** is a list of 148,896 single Polish words with IPA from Wiktionary, collected by the [WikiPron](https://github.com/CUNY-CL/wikipron) project (CC BY-SA). It is used only for measuring, never copied into espeak-ng. A word counts as wrong when espeak-ng's IPA differs from every Wiktionary variant after both are written in one notation (for example `ʂ` and `ʃ` count as the same).
- **Hard cases** are in [data/hard_cases.tsv](data/hard_cases.tsv): phrases and words that Wiktionary does not cover, such as prepositions, cross-word voicing, abbreviations, numbers and stress. Columns are separated by tabs: text, accepted IPA (variants split by ` | `), category, note. Add your own lines; the next run uses them.
- Wiktionary is a good reference, but not always right. Always look at the lists of words, not only at the totals.
- Only the data is measured: `dictsource/pl_rules`, `pl_list` and `phsource/ph_polish` of the tree. The C code is the one in `piper-tts` (espeak-ng `724808c`), so changes to `src/libespeak-ng` are not measured.

## Other commands

`make help` lists everything. The most useful:

| command | what it does |
|---|---|
| `make test` | tests of this tool |
| `make upstream-test ESPEAK_SRC=../espeak-ng` | the Polish lines of espeak-ng's `tests/language-pronunciation.test`, on the compiled data |
| `make baseline` then `make candidate compare` | measure Piper's espeak-ng, then the tree in `ESPEAK_SRC`, and fail on any word made worse |
| `make patch-report` | measure every patch in `patches/` alone |

More detail: [docs/en.md](docs/en.md) (how espeak-ng handles Polish, the patches, contributing). The patches with their numbers and test lines: [patches/README.md](patches/README.md).

## FAQ

- **`no merge base with upstream/master`**: the clone has no `upstream` remote. Run the two `git remote add` and `git fetch` commands from step 1, or use `BASE_REF=origin/master`.
- **`espeak-ng not found`**: install it (see Requirements), or give its path: `make branch ESPEAK=/path/to/espeak-ng ...`.
- **`--compile=pl failed: ... N errors`**: a syntax error in `pl_rules` or `pl_list` of the branch; the message has the line. In `pl_list` the word and its phonemes must be separated by a tab.
- **The base already has thousands of wrong words or the numbers look odd**: your `espeak-ng` program may write data in a format the library in `piper-tts` reads differently. Use espeak-ng 1.52.
- **`espeak-ng already uses ...; compare another data folder in a separate process`**: one command can read only one data folder; run `espeak-pl say` again with the other folder.
- More questions: [docs/en.md, section FAQ](docs/en.md#11-faq).

## License

GPL-3.0-or-later, the same as espeak-ng (the patches are changes to espeak-ng). The WikiPron word list is downloaded by `make fetch` and is not part of this repository.

---

## Po polsku

Narzędzie mierzy polskie reguły zamiany tekstu na fonemy w [espeak-ng](https://github.com/espeak-ng/espeak-ng). Porównuje dowolną gałąź espeak-ng z jej bazą na 148 896 słowach z polskiego Wikisłownika i na ręcznie sprawdzonej liście trudnych przypadków, a potem pokazuje, które słowa się poprawiły, a które pogorszyły.

Wyniki i stan PR-ów w espeak-ng są w tabeli na górze strony.

### Wymagania

- Linux lub macOS, na Windows WSL (Ubuntu).
- Python 3.10, 3.11 lub 3.12 oraz `git` i `make`.
- Program `espeak-ng`, używany wyłącznie do kompilacji polskich danych. Słowa czyta biblioteka espeak-ng z pakietu `piper-tts`.
  - macOS: `brew install espeak-ng`
  - Ubuntu lub WSL: `sudo apt install espeak-ng python3-venv make git`

Sprawdzone z espeak-ng 1.52.

### Instalacja

```sh
git clone https://github.com/witold-gren/espeak-ng-polish.git
cd espeak-ng-polish
make setup              # środowisko Pythona w .venv z piper-tts
make fetch              # pobiera słownik WikiPron (około 5 MB)
make doctor             # sprawdza, czy wszystko jest na miejscu
```

Jeśli Python nie nazywa się `python3.12`, dopisz go do poleceń, np. `make setup PYTHON=python3`.

### Pomiar własnej gałęzi espeak-ng

1. Obok tego katalogu potrzebny jest klon espeak-ng z Twoją gałęzią i zdalnym repozytorium `upstream`. Polecenia są takie same jak w kroku 1 wersji angielskiej.
2. Uruchom porównanie:

   ```sh
   make branch ESPEAK_SRC=../espeak-ng
   ```

   Narzędzie znajduje commit, od którego gałąź odeszła od `upstream/master`, kompiluje polskie dane tego commitu i Twojej gałęzi, czyta nimi wszystkie słowa i porównuje wyniki. Niezatwierdzone zmiany w klonie też są brane pod uwagę. Trwa to kilka minut. Inną bazę ustawisz przez `BASE_REF=origin/master`.
3. Na końcu pojawią się liczby: błędne słowa w bazie i w gałęzi oraz „fixed N, broken M”. Same słowa, z IPA przed i po, są w `reports/branch-compare-wikipron.md` i `reports/branch-compare-hard.md`.

Pojedyncze słowa sprawdzisz poleceniem:

```sh
.venv/bin/espeak-pl say --data-dir build/branch/espeak-ng-data "grozić" "w domu"
```

### Co znaczą liczby

- **WikiPron** to 148 896 polskich słów z wymową IPA z Wikisłownika (licencja CC BY-SA). Służy tylko do pomiaru i nie trafia do espeak-ng.
- **Trudne przypadki** są w [data/hard_cases.tsv](data/hard_cases.tsv): frazy, przyimki, upodobnienia między wyrazami, skróty i akcent. Kolumny oddziela tabulator: tekst, IPA (warianty rozdzielone ` | `), kategoria, notatka. Możesz dopisywać własne.
- Wikisłownik to dobry wzorzec, ale nie wyrocznia. Zawsze przejrzyj listy słów, nie tylko sumy.
- Mierzone są tylko dane (`pl_rules`, `pl_list`, `ph_polish`). Kod C pochodzi z `piper-tts`, więc zmian w `src/libespeak-ng` to narzędzie nie zmierzy.

### Pozostałe polecenia i FAQ

`make help` wyświetla listę poleceń po polsku, jeśli system używa polskiego języka, albo z `HELP_LANG=pl`. Szczegóły: [docs/pl.md](docs/pl.md). Najczęstsze błędy:

- **`no merge base with upstream/master`**: w klonie brakuje zdalnego `upstream`. Dodaj go (krok 1) albo użyj `BASE_REF=origin/master`.
- **`espeak-ng not found`**: zainstaluj go albo podaj ścieżkę: `make branch ESPEAK=/ścieżka/espeak-ng ...`.
- **`--compile=pl failed: ... N errors`**: błąd składni w `pl_rules` lub `pl_list`; komunikat podaje linię. W `pl_list` słowo i fonemy oddziela tabulator.
- **Baza ma tysiące błędów albo liczby są dziwne**: program `espeak-ng` może zapisywać dane w innym formacie, niż czyta biblioteka z `piper-tts`. Użyj wersji 1.52.

### Licencja

GPL-3.0-or-later, tak jak espeak-ng. Słownik WikiPron pobiera `make fetch` i nie jest częścią repozytorium.
