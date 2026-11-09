# Patches for espeak-ng Polish / Łatki dla polskiego w espeak-ng

Each patch is independent and made against espeak-ng `724808c` (pinned by piper1-gpl); apply with `git apply` in an espeak-ng clone. Upstream asks for one problem per pull request, with a test: use one patch + its `test_phon` line per PR. `0010` holds all test lines together for local use (test lines of separate PRs touch the same spot of the file, rebase after each merge). Numbers: `make patch-report` (each patch alone, compared with Piper's espeak-ng).

Każda łatka jest niezależna i zrobiona względem espeak-ng `724808c` (wersja przypięta w piper1-gpl); nakłada się `git apply` w klonie espeak-ng. espeak-ng wymaga jednego problemu na PR i testu: jedna łatka + jej linia `test_phon` = jeden PR. `0010` zawiera wszystkie linie testów razem, do użytku lokalnego (testy osobnych PR-ów zmieniają to samo miejsce pliku, po każdym scaleniu trzeba zrobić rebase). Liczby: `make patch-report` (każda łatka osobno, w porównaniu z espeak-ng z Pipera).

| patch | WikiPron fixed / broken | hard cases fixed / broken |
|---|---:|---:|
| [0001-polish-soft-zi-si](#0001-polish-soft-zi-si) | 313 / 0 | 10 / 0 |
| [0002-polish-dz-ipa-label](#0002-polish-dz-ipa-label) | 1811 / 0 | 4 / 0 |
| [0003-polish-chi-velar](#0003-polish-chi-velar) | 47 / 0 | 2 / 0 |
| [0004-polish-initial-mch](#0004-polish-initial-mch) | 9 / 0 | 2 / 0 |
| [0005-polish-dg](#0005-polish-dg) | 17 / 0 | 2 / 0 |
| [0006-polish-final-consonant-l](#0006-polish-final-consonant-l) | 72 / 0 | 2 / 0 |
| [0007-polish-narrow-loan-rules](#0007-polish-narrow-loan-rules) | 38 / 0 | 3 / 0 |
| [0008-polish-preposition-w](#0008-polish-preposition-w) | 0 / 0 | 5 / 0 |
| [0009-polish-list-okej-tarzan](#0009-polish-list-okej-tarzan) | 1 / 0 | 2 / 0 |
| [0011-polish-abbreviations](#0011-polish-abbreviations) | 1 / 0 | 5 / 0 |
| [0012-polish-acronyms](#0012-polish-acronyms) | 1 / 0 | 2 / 0 |
| [0013-polish-minus](#0013-polish-minus) | 0 / 0 | 3 / 0 |
| [0014-polish-loanwords](#0014-polish-loanwords) | 4 / 0 | 8 / 0 |

## 0001-polish-soft-zi-si

**Soft zi/si before a consonant**: `zi (C → zi` made every non-initial *zi* + consonant hard, so whole verb classes were wrong: *grozić, wozić, razić, mrozić* (-zić, -ził, -zili), *guzik, Gruzin, Brzeziny*. Hard `si (b/c/d/m/r/t` did the same for *dusimy, Kosiba, sitwa, Grosicki*. Wiktionary data: soft in ~95% of such words; hard only after the prefixes bez-/roz-/dez- and in a few loanwords, which keep explicit rules. Related: issue #2295.

**Miękkie zi/si przed spółgłoską**: Reguła `zi (C → zi` czytała każde nie-początkowe *zi* + spółgłoska twardo, przez co źle brzmiały całe klasy czasowników: *grozić, wozić, razić, mrozić*, a także *guzik, Gruzin, Brzeziny*. Twarde `si (b/c/d/m/r/t` psuły *dusimy, Kosiba, sitwa, Grosicki*. Wg Wikisłownika ~95% takich słów ma wymowę miękką; twardą tylko po przedrostkach bez-/roz-/dez- i w kilku zapożyczeniach (zostają jako wyjątki). Zgłoszenie #2295.

Examples fixed / przykłady: Ambrozik, Brzezicki, Brzeziny, Brzeziński, Bzik, Duzinkiewicz, Grosicki, Gruzin

```
before: gR'Ozidz; g'uzig gR'uzin_ dus'imy
after:  gR'OZ;idz; g'uZ;ig gR'uZ;in_ duS;'imy
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl "gR'OZ;idz; g'uZ;ig gR'uZ;in_ duS;'imy" "grozić guzik Gruzin dusimy"
```

## 0002-polish-dz-ipa-label

**IPA label of dz**: Phoneme `dz` in `ph_polish` had `ipa dʑ`, the same symbol as `dz;` (dź). The sound was right, but `--ipa` output (the input of Piper and other neural TTS models) could not tell *dzwon* from *dźwięk*.

**Etykieta IPA fonemu dz**: Fonem `dz` w `ph_polish` miał `ipa dʑ`, czyli ten sam symbol co `dz;` (dź). Dźwięk espeak był dobry, ale wyjście `--ipa` (wejście modeli Piper i innych neuronowych TTS) nie odróżniało *dzwon* od *dźwięk*.

Examples fixed / przykłady: Adze, Bodzan, Bodzanów, Bodzechowie, Bodzechów, Bodzenta, Bodzentyn, Bodzoń

```
before: dʑvˈɔn
dʑvʲˈɛŋk
after:  dzvˈɔn
dʑvʲˈɛŋk
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl "dzvˈɔn
dʑvʲˈɛŋk" "dzwon, dźwięk" "" "--ipa"
```

## 0003-polish-chi-velar

**chi + vowel is velar x**: `chi (A → hj` used the glottal `h`; Polish *ch* is always the velar `x` (*Melchior, Monachium, Banachiewicz*).

**chi + samogłoska to x**: `chi (A → hj` dawało krtaniowe `h`; polskie *ch* to zawsze `x` (*Melchior, Monachium, Banachiewicz*).

Examples fixed / przykłady: Andrychiewicz, Banachiewicz, Eustachia, Eustachiusz, Lachiewicz, Melchior, Monachium, Paluchiewicz

```
before: m'ElhjOR mOn'ahjum_
after:  m'ElxjOR mOn'axjum_
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl "m'ElxjOR mOn'axjum_" "Melchior Monachium"
```

## 0004-polish-initial-mch

**Initial mch**: The rule for the Scottish *Mc-* prefix (`_) mc (P2t → mEk`) turned *mchu, mchem* (forms of *mech*) into *mekchu*.

**Początkowe mch**: Reguła dla szkockiego przedrostka *Mc-* zamieniała *mchu, mchem* (od *mech*) w *mekchu*.

Examples fixed / przykłady: mchach, mchami, mchem, mchom, mchoszczur, mchowi, mchu, mchy

```
before: mEkx'u mEkx'Em_
after:  mx'u mx'Em_
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl "mx'u mx'Em_" "mchu mchem"
```

## 0005-polish-dg

**dg is d+g**: Default `dg → dZ` (English *judge*) broke *Bydgoszcz*; Polish words have d+g, English *-dge* keeps its own rule, *pidgin* gets an exception.

**dg to d+g**: Domyślne `dg → dZ` (jak angielskie *judge*) psuło *Bydgoszcz*; polskie słowa mają d+g, angielskie *-dge* ma własną regułę, *pidgin* wyjątek.

Examples fixed / przykłady: Bydgoszcz, Bydgoszczy, Bydgoszczą, Ludgarda, bydgoscy, bydgoska, bydgoski, bydgoskich

```
before: b'ydZOStS ludZ'aRda#_
after:  b'ydgOStS ludg'aRda#_
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl "b'ydgOStS ludg'aRda#_" "Bydgoszcz Ludgarda"
```

## 0006-polish-final-consonant-l

**Final consonant + ł**: An empty rule `ł (_` silenced final ł after a consonant and left the consonant voiced (*doszedł* → [dɔʂɛd]). Now ł is kept as [w] like in *biegł, Przemysł*, matching Wiktionary.

**Końcowe spółgłoska + ł**: Pusta reguła `ł (_` wyciszała końcowe ł po spółgłosce i zostawiała ją dźwięczną (*doszedł* → [dɔʂɛd]). Teraz ł zostaje jako [w], jak już było w *biegł, Przemysł* i jak podaje Wikisłownik.

Examples fixed / przykłady: Radziwiłł, bódł, darł, doszedł, dotarł, gniótł, jadł, kisł

```
before: d'OSEd j'ad
after:  d'OSEdw j'adw
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl "d'OSEdw j'adw" "doszedł jadł"
```

## 0007-polish-narrow-loan-rules

**Narrow two loanword rules**: `ar) ci (L03_ → sij` (for *Garcia*) hit *barcią, czarcia, charcia*; `a) ng (el → ndZ` (for *Angelika*) hit *Ewangelia, angelologia*. Both now require the word start.

**Zawężenie dwóch reguł dla zapożyczeń**: `ar) ci (L03_ → sij` (dla *Garcia*) psuło *barcią, czarcia, charcia*; `a) ng (el → ndZ` (dla *Angelika*) psuło *Ewangelia, angelologia*. Obie wymagają teraz początku słowa.

Examples fixed / przykłady: Angelą, Ewangelia, Ewangelią, angeliczny, angelizm, angelizmem, angelizmie, angelizmowi

```
before: baRs'ijO~_ ,EvandZ'Elja#_
after:  b'aRts;O~_ ,EvaNg'Elja#_
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl "b'aRts;O~_ ,EvaNg'Elja#_" "barcią Ewangelia"
```

## 0008-polish-preposition-w

**The preposition w is [v]**: `_) w (_ → w` and `_) w (_f/_mn → wE` used phoneme `w`, which in the Polish table is the sound of **ł**: *w domu* was read *ł domu*. The parallel rules for *z* use `z`.

**Przyimek w to [v]**: `_) w (_ → w` oraz `_) w (_f/_mn → wE` używały fonemu `w`, który w polskiej tabeli jest dźwiękiem **ł**: *w domu* było czytane *ł domu*. Analogiczne reguły dla *z* używają `z`.

Examples fixed / przykłady: -

```
before: w d'Omu
w Og'ulE
v'Emn^;E
after:  v d'Omu
v Og'ulE
v'Emn^;E
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl "v d'Omu
v Og'ulE
v'Emn^;E" "w domu, w ogóle, we mnie"
```

## 0009-polish-list-okej-tarzan

**pl_list: okej, Tarzan**: Lowercase *okej* got initial stress (only all-caps *OK* had an entry); *Tarzan* is r+z, not ż.

**pl_list: okej, Tarzan**: Pisane małymi literami *okej* miało akcent na pierwszej sylabie (wpis był tylko dla *OK*); *Tarzan* to r+z, nie ż.

Examples fixed / przykłady: Tarzan

```
before: 'OkEj t'aZa#n_
after:  Ok'Ej t'aRzan
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl "Ok'Ej t'aRzan" "okej Tarzan"
```

## 0011-polish-abbreviations

**Common abbreviations**: *ul., al., tel., godz.* were read as words (*ul* is also a word, beehive) and *nr* was spelled *en er*. New entries use `$hasdot` where the bare word exists, so *ul pszczeli* is unchanged. Lowercase *ok* without a dot was read *około*; now `$hasdot` keeps *około* for *ok.* and the bare word is *okej*. *godz.* gets the nominative only; case after prepositions needs context that espeak does not have.

**Popularne skróty**: *ul., al., tel., godz.* czytane jak słowa (*ul* to też zwykłe słowo), *nr* literowane *en er*. Nowe wpisy mają `$hasdot` tam, gdzie istnieje słowo bez kropki, więc *ul pszczeli* się nie zmienia. *ok* bez kropki było czytane *około*; teraz `$hasdot` zostawia *około* dla *ok.*, a samo *ok* to *okej*. *godz.* tylko w mianowniku; przypadek po przyimku wymaga kontekstu, którego espeak nie ma.

Examples fixed / przykłady: nr

```
before: 'ul_
kf;at'Ova#_
t'El_ dOm'Ovy
,En'ER p;'En^ts;
Ok'OwO j'utRO
after:  ul'itsa
kf;at'Ova#_
tEl'EfOn dOm'Ovy
n'umER p;'En^ts;
Ok'Ej j'utRO
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl "ul'itsa
kf;at'Ova#_
tEl'EfOn dOm'Ovy
n'umER p;'En^ts;
Ok'Ej j'utRO" "ul. Kwiatowa, tel. domowy, nr pięć, ok jutro"
```

## 0012-polish-acronyms

**Acronyms spelled out**: Acronyms with a vowel were read as words: *AGD* as *akt*, *SMS* as *sms*. `$abbrev` spells them like the existing *usg, ekg*.

**Skrótowce literowane**: Skrótowce z samogłoską były czytane jak słowa: *AGD* jak *akt*, *SMS* jak *sms*. `$abbrev` literuje je jak istniejące *usg, ekg*.

Examples fixed / przykłady: sms

```
before: 'akt
,ERt,Ef'aw
sms
,Em,Em'Es
p,Ek,ap'E
after:  ,agj,Ed'E
,ERt,Ef'aw
,Es,Em'Es
,Em,Em'Es
p,Ek,ap'E
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl ",agj,Ed'E
,ERt,Ef'aw
,Es,Em'Es
,Em,Em'Es
p,Ek,ap'E" "AGD, RTV, SMS, MMS, PKP"
```

## 0013-polish-minus

**Minus before a number**: A hyphen-minus before a digit was silent: *-3* was read *trzy*. The same rule as in `cs_rules` and `en_rules` (`__) - (_D`) says *minus*; *2-3* and hyphenated words are unchanged.

**Minus przed liczbą**: Minus (łącznik) przed cyfrą był pomijany: *-3* czytane *trzy*. Ta sama reguła co w `cs_rules` i `en_rules` (`__) - (_D`) mówi *minus*; *2-3* i wyrazy z łącznikiem bez zmian.

Examples fixed / przykłady: -

```
before: t,EmpERat'uRa#_ tS'y
after:  t,EmpERat'uRa#_ m'inus tS'y
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl "t,EmpERat'uRa#_ m'inus tS'y" "temperatura -3"
```

## 0014-polish-loanwords

**Common English brand names**: *iPhone* was read *i fone*, *Google* *go-ogle*, *YouTube* *jou tube*, *Facebook* *facebo-ok*. Entries in the Polish way people say them, with the most common case forms, like the existing *(e mail)* forms. *iPhone, iPad, YouTube* are split at the inner capital before the lookup, so they are multi-word entries; side effect: the lowercase phrase *i pad* also becomes *ajpad*. Worth asking the maintainers whether brand names are welcome.

**Popularne angielskie nazwy**: *iPhone* czytane *i fone*, *Google* *go-ogle*, *YouTube* *jou tube*, *Facebook* *facebo-ok*. Wpisy tak, jak mówi się po polsku, z najczęstszymi formami, jak istniejące *(e mail)*. *iPhone, iPad, YouTube* są dzielone na wielkiej literze przed wyszukaniem, więc to wpisy wielowyrazowe; skutek uboczny: fraza *i pad* małymi literami też brzmi *ajpad*. Warto zapytać opiekunów, czy chcą nazw marek.

Examples fixed / przykłady: Facebook, Google, YouTube, iPhone

```
before: na__! i f'On^;E#
j'Ou t'ubE
gO'OglE
f,atsEb'OOk
after:  na_ ajf'On^E
j'utup
g'ugl
f'Ejzbuk
```

Test line for `tests/language-pronunciation.test` (after the existing `test_phon pl` line) / linia testu:

```sh
test_phon pl "na_ ajf'On^E
j'utup
g'ugl
f'Ejzbuk" "na iPhonie, YouTube, Google, Facebook"
```

## 0010-polish-regression-tests

All test lines above in one patch, for the local tree with every patch applied (`make upstream-test`). / Wszystkie linie testów w jednej łatce, do lokalnego drzewa ze wszystkimi łatkami (`make upstream-test`).
