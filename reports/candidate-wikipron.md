# Candidate: WikiPron

- source: `wikipron`
- espeak-ng data: `build/candidate/espeak-ng-data`
- piper-tts: `1.8.0`

| metric | value |
|---|---|
| entries | 148896 |
| wrong entries | 2192 |
| word error rate | 1.47% |
| phoneme error rate | 0.30% |
| stress checked / wrong | 0 / 0 |

## Error groups (orthographic pattern)

| group | words | wrong | error rate |
|---|---:|---:|---:|
| foreign_letters | 1057 | 277 | 26.21% |
| ch_h | 13845 | 322 | 2.33% |
| dz_dż_dź | 6183 | 136 | 2.20% |
| zi_si_ci_dzi_ni | 36527 | 775 | 2.12% |
| proper_noun | 19074 | 362 | 1.90% |
| final_voiced | 9191 | 167 | 1.82% |
| i_before_vowel | 43945 | 740 | 1.68% |
| w_after_voiceless | 3429 | 48 | 1.40% |
| nasal_ą_ę | 23633 | 229 | 0.97% |
| prefix_before_vowel | 18323 | 172 | 0.94% |
| rz | 10991 | 79 | 0.72% |
| prefix_before_z | 186 | 1 | 0.54% |

## Most common confusions (expected → espeak)

| expected | espeak | words | examples |
|---|---|---:|---|
| `j` | `∅` | 267 | Abisynia, Akwitania, Albania, Alwernia, Amazonia, Antonia, Apolonia, Aragonia |
| `n` | `ɲ` | 161 | Andzia, Andzią, Bondzio, Bondziul, Cienciała, Franciszce, Franciszczak, Franciszek |
| `∅` | `u` | 158 | Kentucky, Nuuk, bluff, bluffiarz, bluffować, business, businessman, businesswoman |
| `a` | `b` | 136 | clubbing, dubbing, dubbingach, dubbingami, dubbingi, dubbingiem, dubbingom, dubbingowa |
| `r` | `∅` | 118 | Awerroes, Basseterre, Nawarra, Weltschmerz, Zmarzlak, Zmarzlik, aberracja, aberracjach |
| `ɔ` | `a` | 116 | Aalborg, Aarhus, Abrahamów, Swansea, aalborski, abbacyja, abdach, abdykacz |
| `k` | `ts` | 99 | Balzac, Basilicata, Cagliari, Cambridge, Canberra, Caracas, Castries, Chaco |
| `∅` | `ɛ` | 90 | Beatlesi, Bordeaux, Delaware, Freetown, Maine, McDonald's, Melbourne, Newcastle |
| `l` | `w` | 79 | abiecadło, admirałka, adracjonał, adzamogłan, adzamogłanin, adziamugłan, adziamugłanin, amirał |
| `∅` | `a` | 75 | Aalborg, Aarhus, Bordeaux, Eichstaedt, Graal, Hainaut, Naypyidaw, Polandball |
| `i` | `ɛ` | 75 | Barbie, Castries, Dietrich, Erie, Freetown, Liechtenstein, Lier, Lietz |
| `j` | `i` | 62 | Bloemfontein, Deimos, Hanoi, Heidelberg, Idaho, Maine, Reich, Schneider |
| `ɛ` | `a` | 59 | Cambridge, Delaware, Faraday, Idaho, Maine, Maryland, Michigan, Naypyidaw |
| `∅` | `ɔ` | 53 | Bloemfontein, Espoo, Goetel, Liverpool, MacBook, Melbourne, Sanssouci, audiobook |
| `∅` | `l` | 52 | Ellert, Illinois, Kallisto, Miller, Müller, Thomalla, Valletta, Wellington |
| `k` | `g` | 51 | Göteborg, Heidelberg, Quaoar, Quito, Vorarlberg, aquapark, kdy, prequel |
| `w` | `v` | 50 | Delaware, Iowa, Wagadugu, Wellington, Wimbledon, Wisconsin, abandonware, bowling |
| `f` | `v` | 50 | Gietrzwałd, Gietrzwałdzianin, Gietrzwałdzianka, Gietrzwałdzianką, Quaoar, Quito, Schwarz, Vogel |
| `∅` | `s` | 47 | Anschluss, Auschwitz, Düsseldorf, Grossmann, Missouri, Nossol, Overijssel, Roseau |
| `∅` | `g` | 40 | Aalborg, Cagliari, Liège, Nagy, Quebec, Quicherat, Quicherata, Quicheratowi |
| `∅` | `x` | 40 | Brahma, Bundeswehra, Drenthe, Ehlert, Hainaut, Lesotho, Lhasa, Lilith |
| `tʂ` | `x` | 39 | Chaco, Chile, Chilijczyk, Chilijka, Chubut, Manchester, Nietzsche, Weltschmerz |
| `dʑ` | `∅` | 37 | dziewięćdziesiąta, dziewięćdziesiąte, dziewięćdziesiątego, dziewięćdziesiątej, dziewięćdziesiątemu, dziewięćdziesiątym, dziewięćdziesiątymi, dziewięćdziesiątą |
| `s` | `ɕ` | 36 | Dżesika, Helsinki, Missisipi, Tbilisi, Wisconsin, dewadasi, epsilon, helsinka |
| `∅` | `n` | 32 | Bonn, Connecticut, Grossmann, Hoffmann, Johannesburg, Minnesota, Newcastle, Sanssouci |
| `a` | `u` | 32 | Connecticut, blockbuster, blunt, brunch, bug, bungee, countrowy, crush |
| `w` | `u` | 32 | Gouda, Mateusiak, Mateuszowy, Oulu, Pireus, chillout, foyer, gouda |
| `u` | `w` | 30 | Aleuty, Jaunde, Kafarnaum, Reunion, Scheuring, Seul, aleuccy, aleucka |
| `∅` | `j` | 30 | Barbie, Castries, Dietrich, Erie, GDDKiA, Iolą, Liechtenstein, Lier |
| `∅` | `t` | 30 | Dhaka, Eichstaedt, Littwin, Massachusetts, Newcastle, Schmidt, Szmidt, Tottenham |
| `z` | `s` | 29 | Arkansas, Bundeswehra, Kansas, Molise, Salzburg, accusativus, bezrtęciowy, bonsai |
| `∅` | `k` | 27 | Bordeaux, bordeaux, miękka, miękkawy, miękki, miękkich, miękkie, miękkiego |
| `e` | `ɛ` | 27 | abalienowanie, abaliowanie, abrenuncjowanie, achcież, ałkierz, barwierz, bluźnierz, czel |
| `i` | `ɨ` | 26 | Coventry, Derby, Halloween, Kentucky, Windows, copypasta, copywriter, creepypasta |
| `∅` | `f` | 26 | Hoffmann, Krefft, Tetzlaff, alkotweecie, alkotweet, alkotweetach, alkotweetami, alkotweetem |
| `∅` | `p` | 24 | Bhutan, Bhutanka, Bhutańczyk, Kruppa, Uppsala, appellativum, appendix, bhutańscy |
| `a` | `ɛ` | 23 | Derby, Heidelberg, Reich, Schneider, Schreiber, Weimar, Zeitgeist, alzheimer |
| `∅` | `ts` | 23 | Dickens, Limerick, Nietzsche, Plocke, RiGCz, Weltschmerz, accusativus, blackjack |
| `∅` | `i` | 23 | Illinois, chateaubriand, grapefruit, grapefruitowy, grapefruity, kitesurfing, podrywaliśmy, poliamid |
| `f` | `∅` | 23 | atm, najpierwszy, pierwsza, pierwszak, pierwsze, pierwszego, pierwszej, pierwszemu |

## Wrong entries (first 40 of 2192)

| text | category | espeak | expected |
|---|---|---|---|
| Aalborg |  | `ˈaalbɔrɡ` | `ɔlbɔr / ɔlbɔrk` |
| Aarhus |  | `aˈarxus` | `ɔrxus` |
| Abisynia |  | `ˌabʲisˈɨɲʲa` | `abisɘɲja` |
| Abrahamów |  | `ˌabraxˈamuf` | `abrɒxɒmof` |
| Aecjusz |  | `ˈɛtsjuʃ` | `aɛt͡sjuʂ` |
| Akwitania |  | `ˌakfitˈaɲʲa` | `akfitaɲja` |
| Albania |  | `albˈaɲʲa` | `albaɲja` |
| Aleuty |  | `alˈɛwtɨ` | `alɛutɘ` |
| Alwernia |  | `alvˈɛrɲʲa` | `alvɛrɲja` |
| Amazonia |  | `ˌamazˈɔɲʲa` | `amazɔɲja` |
| Andzia |  | `ˈaɲdʑa` | `and͡ʑa` |
| Andzią |  | `ˈaɲdʑɔ̃` | `and͡ʑɔw̃` |
| Anschluss |  | `ˈansxluss` | `anʂlus` |
| Antonia |  | `antˈɔɲʲa` | `antɔɲja` |
| Apolonia |  | `ˌapɔlˈɔɲʲa` | `apɔlɔɲja` |
| Aragonia |  | `ˌaraɡˈɔɲʲa` | `araɡɔɲja` |
| Arkansas |  | `arkˈansas` | `arkanzas` |
| Armenia |  | `armˈɛɲʲa` | `armɛɲja` |
| Auschwitz |  | `ˈawsxfits` | `awʂfit͡s` |
| Awerroes |  | `ˌavɛrˈɔɛs` | `avɛrrɔɛs` |
| Babilonia |  | `bˌabʲilˈɔɲʲa` | `babilɔɲja` |
| Bacciarelli |  | `bˌatstɕarˈɛlli` | `batt͡ɕarɛlli` |
| Balzac |  | `bˈalzats` | `balzak` |
| Barbie |  | `bˈarbjɛ` | `barbi` |
| Basilicata |  | `bˌaɕilitsˈata` | `bazilikata` |
| Baskonia |  | `baskˈɔɲʲa` | `baskɔɲja` |
| Basseterre |  | `bˌassɛtˈɛrɛ` | `bassɛtɛrrɛ` |
| Beatlesi |  | `bˌɛatlˈɛɕi` | `bitlɛɕi` |
| Beyer |  | `bˈɛjɛr` | `bɛɘɛr` |
| Bhutan |  | `pxˈutan` | `butan` |
| Bhutanka |  | `pxutˈaŋka` | `butanka` |
| Bhutańczyk |  | `pxutˈaɲtʃɨk` | `butaɲt͡ʂɘk` |
| Bitynia |  | `bʲitˈɨɲʲa` | `bitɘɲja` |
| Bloemfontein |  | `blˌɔɛmfɔntˈɛin` | `blumfɔntɛjn` |
| Bolonia |  | `bɔlˈɔɲʲa` | `bɔlɔɲja` |
| Bondzio |  | `bˈɔɲdʑɔ` | `bɔnd͡ʑɔ` |
| Bondziul |  | `bˈɔɲdʑul` | `bɔnd͡ʑul` |
| Bonn |  | `bˈɔnn` | `bɔn` |
| Bordeaux |  | `bɔrdˈɛawks` | `bɔrdɔ` |
| Brahma |  | `brˈaxma` | `brama` |
