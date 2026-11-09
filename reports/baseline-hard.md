# Baseline: hard cases

- source: `hard`
- espeak-ng data: `~/Home Assistant/espeak-ng-polish/.venv/lib/python3.12/site-packages/piper/espeak-ng-data`
- piper-tts: `1.8.0`

| metric | value |
|---|---|
| entries | 115 |
| wrong entries | 53 |
| word error rate | 46.09% |
| phoneme error rate | 13.33% |
| stress checked / wrong | 36 / 1 |

## Error groups (orthographic pattern)

| group | words | wrong | error rate |
|---|---:|---:|---:|
| w_after_voiceless | 4 | 3 | 75.00% |
| foreign_letters | 7 | 5 | 71.43% |
| proper_noun | 29 | 18 | 62.07% |
| ch_h | 10 | 6 | 60.00% |
| final_voiced | 7 | 4 | 57.14% |
| dz_dż_dź | 13 | 7 | 53.85% |
| zi_si_ci_dzi_ni | 35 | 18 | 51.43% |
| prefix_before_vowel | 8 | 4 | 50.00% |
| i_before_vowel | 32 | 15 | 46.88% |
| prefix_before_z | 3 | 1 | 33.33% |
| rz | 8 | 2 | 25.00% |
| nasal_ą_ę | 15 | 2 | 13.33% |

## Most common confusions (expected → espeak)

| expected | espeak | words | examples |
|---|---|---:|---|
| `v` | `w` | 6 | w domu, w ogóle, w Warszawie, w lesie, w niedzielę, w godz. pracy |
| `ʑ` | `z` | 6 | grozić, wozili, guzik, Gruzin, Brzeziny, kazirodztwo |
| `n` | `∅` | 6 | tel. domowy, w godz. pracy, nr 5, -3, temperatura -5, od -5 do 5 |
| `∅` | `ɔ` | 6 | ok jutro, YouTube, na YouTubie, Google, Google'a, Facebook |
| `∅` | `ɛ` | 5 | mchem, mchu, iPhone, Google, Google'a |
| `a` | `∅` | 5 | ul. Kwiatowa, al. Róż, iPhone, na iPhonie, iPad |
| `i` | `∅` | 5 | ul. Kwiatowa, w godz. pracy, -3, temperatura -5, od -5 do 5 |
| `dz` | `dʑ` | 4 | dzwon, rodzaj, Sieradzan, odzyskać |
| `j` | `∅` | 4 | Albania, Dania, al. Róż, AGD |
| `ɛ` | `∅` | 4 | al. Róż, tel. domowy, AGD, SMS |
| `ɕ` | `s` | 3 | dusimy, Kosiba, sitwa |
| `g` | `dʐ` | 3 | Bydgoszcz, Ludgarda, Ewangelia |
| `s` | `∅` | 3 | -3, temperatura -5, od -5 do 5 |
| `u` | `∅` | 3 | -3, temperatura -5, od -5 do 5 |
| `m` | `∅` | 3 | -3, temperatura -5, od -5 do 5 |
| `j` | `i` | 3 | iPhone, na iPhonie, iPad |
| `u` | `ɔ` | 3 | Google, Google'a, Facebook |
| `d` | `∅` | 2 | Bydgoszcz, Ludgarda |
| `x` | `h` | 2 | Melchior, Monachium |
| `∅` | `k` | 2 | mchem, mchu |
| `w` | `∅` | 2 | doszedł, jadł |
| `∅` | `i` | 2 | barcią, czarcia |
| `tɕ` | `j` | 2 | barcią, czarcia |
| `∅` | `s` | 2 | barcią, czarcia |
| `z` | `ʑ` | 1 | bezimienny |
| `z` | `ʐ` | 1 | Tarzan |
| `r` | `∅` | 1 | Tarzan |
| `ts` | `∅` | 1 | ul. Kwiatowa |
| `ɔ` | `∅` | 1 | tel. domowy |
| `f` | `∅` | 1 | tel. domowy |
| `dʑ` | `∅` | 1 | w godz. pracy |
| `a` | `ts` | 1 | w godz. pracy |
| `m` | `n` | 1 | nr 5 |
| `u` | `ɛ` | 1 | nr 5 |
| `j` | `ɔ` | 1 | ok jutro |
| `ɛ` | `w` | 1 | ok jutro |
| `d` | `k` | 1 | AGD |
| `ɛ` | `t` | 1 | AGD |
| `g` | `∅` | 1 | AGD |
| `p` | `ɛ` | 1 | YouTube |

## Wrong entries (first 53 of 53)

| text | category | espeak | expected |
|---|---|---|---|
| w domu | preposition_w | `w dˈɔmu` | `vdɔmu` |
| w ogóle | preposition_w | `w ɔɡˈulɛ` | `vɔgulɛ` |
| w Warszawie | preposition_w | `w varʃˈavʲɛ` | `vvarʂavjɛ` |
| w lesie | preposition_w | `w lˈɛɕɛ` | `vlɛɕɛ` |
| w niedzielę | preposition_w | `w ɲʲɛdʑˈɛlɛ` | `vɲɛdʑɛlɛ` |
| grozić | zi_si | `ɡrˈɔzitɕ` | `ˈgrɔʑitɕ` |
| wozili | zi_si | `vɔzˈili` | `vɔˈʑili` |
| guzik | zi_si | `ɡˈuzik` | `ˈguʑik` |
| Gruzin | zi_si | `ɡrˈuzin` | `ˈgruʑin` |
| Brzeziny | zi_si | `bʒɛzˈinɨ` | `bʐɛˈʑinɨ` |
| kazirodztwo | zi_si | `kˌazirˈɔtstfɔ` | `kaʑiˈrɔtstfɔ` |
| dusimy | zi_si | `dusˈimɨ` | `duˈɕimɨ` |
| Kosiba | zi_si | `kɔsˈiba` | `kɔˈɕiba` |
| sitwa | zi_si | `sˈitfa` | `ˈɕitfa` |
| bezimienny | zi_si | `bˌɛʑimjˈɛnnɨ` | `bɛziˈmjɛnnɨ` |
| dzwon | dz_dź | `dʑvˈɔn` | `dzvɔn` |
| rodzaj | dz_dź | `rˈɔdʑaj` | `ˈrɔdzaj` |
| Sieradzan | dz_dź | `ɕɛrˈadʑan` | `ɕɛˈradzan` |
| odzyskać | dz_dź | `ɔdʑˈɨskatɕ` | `ɔdˈzɨskatɕ / ɔˈdzɨskatɕ` |
| Bydgoszcz | dg | `bˈɨdʒɔʃtʃ` | `ˈbɨdgɔʂtʂ` |
| Ludgarda | dg | `ludʒˈarda` | `ludˈgarda` |
| Melchior | chi | `mˈɛlhjɔr` | `ˈmɛlxjɔr` |
| Monachium | chi | `mɔnˈahjum` | `mɔˈnaxjum` |
| mchem | mch | `mɛkxˈɛm` | `mxɛm` |
| mchu | mch | `mɛkxˈu` | `mxu` |
| doszedł | final_consonant_ł | `dˈɔʃɛd` | `ˈdɔʂɛdw / ˈdɔʂɛt` |
| jadł | final_consonant_ł | `jˈad` | `jadw / jat` |
| barcią | rci | `barsˈijɔ̃` | `ˈbartɕɔ̃` |
| czarcia | rci | `tʃarsˈija` | `ˈtʂartɕa` |
| Ewangelia | ng_el | `ˌɛvandʒˈɛlja` | `ɛvanˈgɛlja` |
| Tarzan | rz_boundary | `tˈaʒan` | `ˈtarzan` |
| okej | stress (stress) | `ˈɔkɛj` | `ɔˈkɛj` |
| Albania | i_before_vowel | `albˈaɲʲa` | `alˈbaɲja` |
| Dania | i_before_vowel | `dˈaɲʲa` | `ˈdaɲja` |
| ul. Kwiatowa | abbreviations | `ˈul kfʲatˈɔva` | `ulˈitsa kfjatˈɔva` |
| al. Róż | abbreviations | `ˈal rˈuʃ` | `alˈɛja ˈruʂ` |
| tel. domowy | abbreviations | `tˈɛl dɔmˈɔvɨ` | `tɛlɛfɔn dɔmɔvɨ` |
| w godz. pracy | abbreviations | `w ɡˈɔts prˈatsɨ` | `v gɔdʑina pratsɨ` |
| nr 5 | abbreviations | `ˌɛnˈɛr pʲˈɛɲtɕ` | `numɛr pjɛɲtɕ` |
| ok jutro | abbreviations | `ɔkˈɔwɔ jˈutrɔ` | `ɔkɛj jutrɔ` |
| AGD | acronyms | `ˈakt` | `agjɛdɛ` |
| SMS | acronyms | `sms` | `ɛsɛmɛs` |
| -3 | minus | `tʃˈɨ` | `minus tʂɨ` |
| temperatura -5 | minus | `tˌɛmpɛratˈura pʲˈɛɲtɕ` | `tɛmpɛratura minus pjɛɲtɕ` |
| od -5 do 5 | minus | `ɔt pʲˈɛɲdʑ dɔ pʲˈɛɲtɕ` | `ɔt minus pjɛɲdʑ dɔ pjɛɲtɕ / ɔt minus pjɛɲtɕ dɔ pjɛɲtɕ` |
| iPhone | loanwords | `i fˈɔnɛ` | `ajfɔn` |
| na iPhonie | loanwords | `na i fˈɔɲʲɛ` | `na ajfɔɲɛ` |
| iPad | loanwords | `i pˈat` | `ajpat` |
| YouTube | loanwords | `jˈɔu tˈubɛ` | `jutup` |
| na YouTubie | loanwords | `na jˈɔu tˈubjɛ` | `na jutubjɛ` |
| Google | loanwords | `ɡɔˈɔɡlɛ` | `gugl / gukl` |
| Google'a | loanwords | `ɡˌɔɔɡlˈɛa` | `gugla` |
| Facebook | loanwords | `fˌatsɛbˈɔɔk` | `fɛjzbuk / fɛjsbuk` |
