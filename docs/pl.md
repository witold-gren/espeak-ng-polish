# espeak-ng i język polski: jak działa, co poprawiamy i jak to wysłać do projektu

## 1. Po co ten projekt

Piper (piper1-gpl) nie czyta tekstu bezpośrednio. Najpierw espeak-ng zamienia tekst na fonemy IPA, dopiero te fonemy trafiają do sieci neuronowej (VITS), która generuje dźwięk. Jeśli espeak-ng poda złe fonemy, nawet najlepiej wytrenowany głos powie słowo źle. To repozytorium:

- mierzy, jak dobrze espeak-ng zamienia polski tekst na fonemy (ten sam espeak-ng, którego używa Piper),
- pozwala poprawiać reguły i od razu sprawdzać, co się naprawiło i czy coś się nie zepsuło,
- przygotowuje łatki (`patches/`) z opisami, liczbami i testami do wysłania do projektu espeak-ng.

## 2. Jak Piper używa espeak-ng

- piper1-gpl buduje espeak-ng statycznie z przypiętego commita (`CMakeLists.txt`: `GIT_TAG 724808c`, 2026-04-06). Pakiet `piper-tts==1.8.0` zawiera dokładnie tę wersję wraz z katalogiem `espeak-ng-data`.
- Używany jest **tylko fonemizator** (`src/piper/phonemize_espeak.py` → `espeakbridge.get_phonemes()`), wynik to IPA, np. `ɡrˈɔʑitɕ`. Syntezator formantowy espeak-ng (to, co słychać w `espeak-ng -v pl "tekst"`) nie ma znaczenia.
- Polskie reguły to wyłącznie **dane**: `espeak-ng-data/pl_dict` (reguły i wyjątki) oraz `phontab`/`phonindex`/`phondata` (tabele fonemów, z nich bierze się symbol IPA). Poprawka nie wymaga przebudowy kodu C ani Pipera, wystarczy podmienić te pliki.
- **Ważne:** modele Piper uczą się na fonemach z konkretnej wersji espeak-ng. Po zmianie reguł istniejący głos dostaje trochę inne wejście. Pełny efekt daje dopiero dotrenowanie głosu (fine-tune) na nowych fonemach. Większość naszych poprawek zamienia jeden znany modelowi symbol na inny, też znany (`z`→`ʑ`, `w`→`v`), więc powinny pomóc także bez dotrenowania, ale trzeba to sprawdzić na słuch.

## 3. Jak espeak-ng obsługuje polski

| Plik | Co zawiera |
|---|---|
| `espeak-ng-data/lang/zlw/pl` | definicja głosu: `name Polish`, `language pl`, `intonation 2`; brak opiekuna (`maintainer`) |
| `dictsource/pl_rules` | ok. 870 reguł litera → fonem w 46 grupach |
| `dictsource/pl_list` | słownik wyjątków: całe słowa z gotową wymową, skróty, liczebniki, słowa bez akcentu |
| `dictsource/pl_extra` | (opcjonalny, nie istnieje) lokalne dopiski do słownika, doklejane przy kompilacji |
| `phsource/ph_polish` | tabela polskich fonemów: dźwięk i symbol IPA (`ipa ...`) |
| `src/libespeak-ng/tr_languages.c` | ustawienia języka w C: akcent na przedostatniej sylabie, upodobnienia |

### Składnia reguł (`pl_rules`)

```
.group z                      ← grupa dla wyrazów zaczynających dopasowanie od litery z
        z          z          ← domyślnie: litera z → fonem z
        z (_       s          ← z na końcu słowa (_ = granica słowa) → s (ubezdźwięcznienie)
        z (i       Z;         ← z przed i → ʑ
     _) zi (C      z_i        ← początek słowa + zi + spółgłoska (C)
    _be) zi (C     zi         ← po "be" na początku słowa (bez-imienny) → twarde zi
```

- Lewa część `kontekst)` to litery **przed** dopasowaniem, prawa `(kontekst` to litery **po**; `_` to granica słowa, `C` spółgłoska, `A` samogłoska, `L01`…`L04` to zdefiniowane na początku pliku listy liter.
- Wygrywa reguła, która dopasowuje najwięcej liter (punkty widać w trybie śledzenia).
- Fonemy zapisane są **mnemonikami** espeak-ng, nie IPA: `Z;`=ʑ, `S`=ʂ, `Z`=ʐ, `tS`=tʂ, `dz;`=dʑ, `n^`=ɲ, `E~`=ę, `O~`=ą, `R`=r, `w`=**ł** (!), `v`=w, `x`=ch, `'` = akcent.
- Śledzenie, która reguła zadziałała: `espeak-ng -v pl -X "słowo"`. To podstawowe narzędzie przy poprawkach.

### Akcent i upodobnienia

- Akcent domyślnie pada na przedostatnią sylabę. Wyjątki obsługują znaczniki w regułach (np. `=a` w `-łbyśmy`) i wpisy w `pl_list`. Pomiar pokazał, że działa to bardzo dobrze: *matematyka, polityka, zrobilibyśmy, czterysta*, a nawet *NIE wiem* (przy jednosylabowym czasowniku akcent pada na „nie”).
- Ubezdźwięcznienie na końcu słowa i upodobnienia wewnątrz słowa zapewnia `voicingswitch` w `ph_polish`.
- Upodobnienia **między wyrazami** też działają (*jak było* → `jag bɨwɔ`, *w Polsce* → `f pɔlstsɛ`, *Zażółć gęślą* → `…uwdʑ gɛ…`).

## 4. Jak mierzymy

1. **WikiPron** (`make fetch`): 157 tys. polskich haseł z Wikisłownika z wymową IPA. Po odrzuceniu skrótowców i fraz zostaje 148 896 słów. Licencja CC BY-SA, więc dane służą **tylko do pomiaru** i nie wolno ich kopiować do espeak-ng (GPL).
2. **Normalizacja** (`src/espeak_pl/ipa.py`): espeak-ng i Wikisłownik zapisują te same dźwięki innymi symbolami (`ʃ`/`ʂ`, `ʲ`/`j`, `ɔ̃`/`ɔw̃`, `ŋk`/`nk`, `ç`/`x`, akcenty, łuki `͡`). Obie strony sprowadzamy do jednego zapisu, żeby liczyły się tylko prawdziwe różnice w wymowie.
3. **Trudne przypadki** (`data/hard_cases.tsv`): ręcznie sprawdzone słowa i frazy (przyimki, akcent, upodobnienia między wyrazami), których WikiPron nie obejmuje. Kolumna `ipa` może mieć kilka dopuszczalnych wariantów rozdzielonych `|`. Jeśli wariant ma `ˈ`, sprawdzany jest też akcent.
4. **Metryki**: WER (odsetek słów z jakimkolwiek błędem), PER (odsetek błędnych fonemów), grupy błędów według pisowni i najczęstsze zamiany fonemów z przykładami.

## 5. Wyniki

| | Piper (espeak-ng 724808c) | z łatkami 0001–0014 |
|---|---:|---:|
| WikiPron, błędne słowa | 4506 / 148 896 (3,03%) | 2192 (1,47%) |
| WikiPron, błędne fonemy | 0,50% | 0,30% |
| trudne przypadki, błędne | 53 / 115 (46,1%) | 2 (1,7%) |
| zepsute przez łatki | - | 0 |

Najważniejsze znalezione błędy (szczegóły i liczby: [patches/README.md](../patches/README.md)):

- przyimek **w** czytany jak **ł** (*w domu* → „ł domu”),
- **zi/si** przed spółgłoską czytane twardo: *grozić, wozić, razić, guzik, Gruzin, dusimy*,
- **dz** i **dź** z tym samym symbolem IPA `dʑ`, więc Piper ich nie odróżnia (*dzwon* = *dźwięk*, 1811 słów),
- *ch* → `h` (*Melchior*), *dg* → `dʒ` (*Bydgoszcz*), *mchu* → „mekchu”, *doszedł* → `dɔʂɛd`, *barcią* → „barsiją”, *Ewangelia* → „ewandżelia”,
- skróty i zapisy, które obchodzi `pl_tts` w polish-piper: *ul., al., tel., godz., nr* czytane jak słowa, *ok* bez kropki jako „około”, *AGD* jak „akt”, **minus przed liczbą pomijany** (*-3* → „trzy”), *iPhone* → „i fone”, *Google* → „go-ogle” (łatki 0011–0014, rozdział 9).

Pozostałe różnice z Wikisłownikiem to głównie zapożyczenia (*Albania, agonia*: `ɲja` zamiast `ɲa`), obce nazwy własne oraz warianty, które Wikisłownik zapisuje staranniej niż mowa potoczna (*pierwszy* z `f`, *miękki* bez podwojenia, archaiczne `ɔ` za „á”).

## 6. Praca krok po kroku

```sh
make doctor              # czy jest espeak-ng (brew install espeak-ng), klon ../espeak-ng i słownik
make baseline            # pomiar espeak-ng z Pipera → reports/baseline-*.md
# edytuj ../espeak-ng/dictsource/pl_rules, pl_list albo phsource/ph_polish
make say TEXT="grozić w domu"   # IPA przed i po
make candidate           # kompilacja i pomiar → reports/candidate-*.md
make compare             # lista naprawionych i zepsutych słów; kończy się błędem przy regresji
make test-all            # testy narzędzia + polskie testy espeak-ng na kandydacie
make branch ESPEAK_SRC=../espeak-ng   # dowolna gałąź względem bazy z upstream/master (BASE_REF)
```

Do kompilacji danych używamy `espeak-ng` z Homebrew (1.52). Sprawdziliśmy, że kompilacja niezmienionych reguł z commita 724808c daje identyczną fonemizację wszystkich 148 896 słów co espeak-ng w Piperze, więc nie trzeba budować espeak-ng ze źródeł.

Nowa łatka tematyczna (bez commitów, względem czystego drzewa):

```sh
.venv/bin/python tools/make_topic_patch.py ../espeak-ng patches/0011-polish-cos.patch edits.json
# dopisz opis do patches/topics.json
make patch-report        # każda łatka osobno + odświeżenie patches/README.md
```

## 7. Wkład do espeak-ng

Zasady projektu (`docs/contributing.md`, `AGENTS.md`):

- **jeden problem na pull request**, z opisem i **testem** (`tests/language-pronunciation.test`),
- testy muszą przechodzić (`ctest`), bez konfliktów, bez zmian czysto kosmetycznych,
- poprawki języka recenzuje jego opiekun. **Polski nie ma opiekuna**, a zgłosić się można, dopisując `maintainer Imię Nazwisko <e-mail>` w `espeak-ng-data/lang/zlw/pl` w osobnym PR,
- odpowiedź zajmuje zwykle 1–2 tygodnie (wolontariusze).

Kolejne kroki:

1. Zgłoszenie „Polish: pronunciation fixes measured on Wiktionary” z tabelą z punktu 5, linkiem do #2295 i listą planowanych PR-ów.
2. Fork `espeak-ng/espeak-ng` na GitHubie, potem `git remote add fork …` w `~/Home Assistant/espeak-ng`.
3. Dla każdej łatki: `git switch -c polish-soft-zi master && git apply …/patches/0001-….patch`, dopisanie linii `test_phon` z `patches/README.md`, commit i PR. Najpierw zalecam **0008 (w)** i **0002 (dz)**: są małe, a błąd oczywisty.
4. Do recenzji warto zaprosić Łukasza Golonkę (ostatnie polskie zmiany, społeczność NVDA), bo użytkownicy czytników ekranu słuchają espeak-ng po polsku na co dzień.
5. Przed każdym PR: `git fetch origin && git rebase origin/master`, potem znowu `make candidate compare` (upstream mógł się zmienić).

Szablon opisu PR (po angielsku):

```
Polish: <what>

<one paragraph: wrong rule, examples, correct pronunciation>

Measured on 148,896 Polish words from Wiktionary (WikiPron) with the Polish
espeak-ng data compiled before/after this change: N words fixed, 0 changed for
the worse. Test added to tests/language-pronunciation.test.
```

## 8. Użycie w naszym Piperze przed przyjęciem zmian

Najprościej skopiować do obrazu `polish-piper` pliki z `build/candidate/espeak-ng-data`: `pl_dict`, `phontab`, `phonindex`, `phondata`, nadpisując te w `site-packages/piper/espeak-ng-data`. Alternatywą jest zmiana `GIT_TAG` w piper1-gpl na commit z forka, ale to wymaga przebudowy Pipera. Przed wdrożeniem: odsłuch tych samych zdań na starym i nowym słowniku. Po wdrożeniu: dotrenowanie głosów (piper-voice-cloner) na nowej fonemizacji.

## 9. espeak-ng a pl_tts i Morfeusz (polish-piper)

[home-assistant-polish-piper](https://github.com/witold-gren/home-assistant-polish-piper) poprawia tekst przed espeak-ng (`pl_tts`) i używa Morfeusza 2. Sprawdziliśmy, co z tego może robić sam espeak-ng.

| Problem | espeak-ng dziś | Gdzie naprawiać |
|---|---|---|
| zgodność liczebnika z rzeczownikiem („z dwiema osobami”, „brakuje dwóch osób”) | „z dwa osobami” | `pl_tts` + Morfeusz: wymaga rodzaju i przypadku rzeczownika oraz kontekstu zdania |
| godziny i daty („o 9:05”, „20.10.2026”) | „dziewięć zero pięć” | `pl_tts`: odmiana zależy od przyimku |
| jednostki („6°C”, „50 km/h”) | „stopień ce”, „ka em slesz ha” | `pl_tts`: liczba i przypadek jednostki zależą od liczby |
| liczebniki porządkowe i rzymskie („2. piętro”, „XXI wieku”) | „dwa piętro”, „iks iks i” | `pl_tts`: forma zależy od rzeczownika |
| telefony („+48 600 100 200”) | „sześćset miliardów…” | `pl_tts`: spacja w liczbie to dla espeak separator tysięcy |
| *np., itd., itp., prof., św., ok., dr, mgr*, adresy e-mail | czyta dobrze | już w espeak-ng |
| *ul., al., tel., godz., nr*, *ok* bez kropki | jak słowa, „en er”, „około” | **espeak-ng, łatka 0011** |
| *AGD, SMS* | „akt”, „sms” | **espeak-ng, łatka 0012** |
| minus przed liczbą (*-3*) | pomijany | **espeak-ng, łatka 0013**; znak `−` (U+2212) poprawiony już w master (#2451) |
| *iPhone, iPad, YouTube, Google, Facebook* | „i fone”, „go-ogle” | **espeak-ng, łatka 0014**; nazwy niszowe i prywatne zostają w słowniku `pl_tts` |
| *m.in.* | „em kropka in” | `pl_tts`: wpis wielowyrazowy z kropkami nie działa w `pl_list` |

Wniosek: espeak-ng widzi litery jednego słowa i stałe wpisy słownika, bez morfologii i kontekstu zdania. Wszystko, co zależy od odmiany, zostaje w `pl_tts` z Morfeuszem; Morfeusz nie pomoże za to w wymowie (nie dzieli słów na przedrostki). Do espeak-ng należą stałe zapisy: skróty, skrótowce, znaki, popularne zapożyczenia. Gdy łatki trafią do Pipera (albo dane zostaną podmienione w obrazie, rozdział 8), odpowiedniki w `pl_tts` można usunąć.

## 10. Co dalej

- zapożyczenia na `-nia/-nii/-nię` (*Albania, agonia, Kalifornia*): rozwiązanie słownikowe, do ustalenia z opiekunami (forma odmiany),
- obce słowa i nazwy (angielskie *-ing, -ee, c*): częściowo zadanie dla normalizacji tekstu w `pl_tts`,
- `n` przed `ć/dź` (*Franciszek*, *abonamencie*): espeak daje `ɲ`, Wikisłownik `n`; to wariant wymowy, nie błąd,
- rozszerzanie `data/hard_cases.tsv` o każdy błąd usłyszany w Piperze (zdania z Home Assistanta).

## 11. FAQ: błędy i rozwiązania

**`espeak-ng already uses …; compare another data folder in a separate process`**
espeak-ng ładuje jeden katalog danych na proces. Każdy pomiar uruchamiaj osobnym poleceniem (`make candidate` i `espeak-pl patch-report` już to robią).

**`espeak-ng not found (macOS: brew install espeak-ng)`**
Do kompilacji `pl_dict` potrzebny jest program `espeak-ng`: `brew install espeak-ng`. Inną ścieżkę podasz przez `make compile ESPEAK=/ścieżka/espeak-ng`.

**`espeak-ng --path=… --compile=pl failed: … N errors`**
Błąd składni w `pl_rules` albo `pl_list`. Komunikat podaje numer linii. Najczęstsze przyczyny to nieznany mnemonik fonemu albo spacja zamiast tabulatora w `pl_list`.

**`… pl_rules not found`**
`ESPEAK_SRC` nie wskazuje klonu espeak-ng: `git clone https://github.com/espeak-ng/espeak-ng.git ../espeak-ng` albo `make … ESPEAK_SRC=/ścieżka`.

**`missing baseline runs: … (make baseline)`**
`patch-report` porównuje z pomiarem bazowym. Najpierw uruchom `make baseline`.

**`make compare` kończy się błędem, `fixed N, broken M`**
Zmiana zepsuła M słów. Ich listę z wymową przed i po znajdziesz w `reports/compare-wikipron.md` i `reports/compare-hard.md` (sekcja `broken`). Dodaj wąski wyjątek w regule albo w `pl_list`.

**`Reversed (or previously applied) patch detected` przy `git apply`/`patch`**
Łatka jest już nałożona na to drzewo. Sprawdź `git -C ../espeak-ng diff`.

**`error: patch failed: dictsource/pl_list:545` / `patch does not apply` przy nakładaniu łatki na klon z innymi łatkami**
Każda łatka powstaje na czystym `master`, więc sąsiednie łatki (np. 0009 i 0011 w tym samym miejscu `pl_list`) nie nakładają się jedna na drugą. Upstream to nie przeszkadza: PR-y wysyła się po kolei, z rebase po każdym scaleniu. Lokalnie nałóż zmianę ręcznie albo wygeneruj łatkę na nowo (`tools/make_topic_patch.py`).

**`git apply` nie znajduje łatki podanej względną ścieżką**
`git -C ../espeak-ng apply patches/…` szuka pliku względem klonu. Podaj ścieżkę bezwzględną (`"$PWD/patches/…"`); `tools/make_topic_patch.py` robi to sam.

**Czy espeak-ng z Homebrew (1.52) daje to samo co Piper (724808c)?**
Tak: sprawdzone na 148 896 słowach, identyczna fonemizacja przy kompilacji reguł i fonemów. Gdy Piper zmieni przypięty commit, powtórz test: pomiar na danych Pipera vs. kompilacja czystego drzewa z tego commita.

**`workflow ci.yml not found on the default branch` na forku**
GitHub nie rejestruje workflowów w nowym forku, dopóki nie potwierdzisz ich w zakładce Actions, a `ci.yml` działa tylko dla `master`, PR-ów i uruchomienia ręcznego. Push do gałęzi forka niczego nie startuje; pierwszy pełny przebieg jest w PR-ze.

**`The configuration 'macos-14-arm64-us-default' is not supported` (zadania macOS anulowane w PR-ze)**
GitHub odrzuca ten runner, zadanie w ogóle nie startuje i żaden test się nie wykonuje. Nie powoduje tego łatka: od 2026-11-06 tak samo kończą się niezwiązane PR-y. Poprawka należy do `.github/workflows/ci.yml` w upstreamie.

**`no merge base with upstream/master` przy `make branch`**
Klon espeak-ng nie ma zdalnego `upstream`: `git -C ../espeak-ng remote add upstream https://github.com/espeak-ng/espeak-ng.git && git -C ../espeak-ng fetch upstream` albo podaj `BASE_REF=origin/master`.
