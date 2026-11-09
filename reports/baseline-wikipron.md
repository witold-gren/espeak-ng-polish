# Baseline: WikiPron

- source: `wikipron`
- espeak-ng data: `~/Home Assistant/espeak-ng-polish/.venv/lib/python3.12/site-packages/piper/espeak-ng-data`
- piper-tts: `1.8.0`

| metric | value |
|---|---|
| entries | 148896 |
| wrong entries | 4506 |
| word error rate | 3.03% |
| phoneme error rate | 0.50% |
| stress checked / wrong | 0 / 0 |

## Error groups (orthographic pattern)

| group | words | wrong | error rate |
|---|---:|---:|---:|
| dz_dż_dź | 6183 | 1948 | 31.51% |
| foreign_letters | 1057 | 281 | 26.58% |
| prefix_before_z | 186 | 39 | 20.97% |
| zi_si_ci_dzi_ni | 36527 | 1580 | 4.33% |
| ch_h | 13845 | 531 | 3.84% |
| i_before_vowel | 43945 | 1483 | 3.37% |
| rz | 10991 | 361 | 3.28% |
| nasal_ą_ę | 23633 | 742 | 3.14% |
| w_after_voiceless | 3429 | 107 | 3.12% |
| proper_noun | 19074 | 541 | 2.84% |
| prefix_before_vowel | 18323 | 510 | 2.78% |
| final_voiced | 9191 | 236 | 2.57% |

## Most common confusions (expected → espeak)

| expected | espeak | words | examples |
|---|---|---:|---|
| `dz` | `dʑ` | 1815 | Adze, Bodzan, Bodzanów, Bodzechowie, Bodzechów, Bodzenta, Bodzentyn, Bodzoń |
| `j` | `∅` | 267 | Abisynia, Akwitania, Albania, Alwernia, Amazonia, Antonia, Apolonia, Aragonia |
| `ʑ` | `z` | 248 | Ambrozik, Brzezicki, Brzeziny, Brzeziński, Bzik, Duzinkiewicz, Gruzin, Gruzince |
| `n` | `ɲ` | 161 | Andzia, Andzią, Bondzio, Bondziul, Cienciała, Franciszce, Franciszczak, Franciszek |
| `∅` | `u` | 158 | Kentucky, Nuuk, bluff, bluffiarz, bluffować, business, businessman, businesswoman |
| `a` | `b` | 136 | clubbing, dubbing, dubbingach, dubbingami, dubbingi, dubbingiem, dubbingom, dubbingowa |
| `r` | `∅` | 119 | Awerroes, Basseterre, Nawarra, Tarzan, Weltschmerz, Zmarzlak, Zmarzlik, aberracja |
| `ɔ` | `a` | 116 | Aalborg, Aarhus, Abrahamów, Swansea, aalborski, abbacyja, abdach, abdykacz |
| `∅` | `ɛ` | 100 | Beatlesi, Bordeaux, Delaware, Freetown, Google, Maine, McDonald's, Melbourne |
| `k` | `ts` | 99 | Balzac, Basilicata, Cagliari, Cambridge, Canberra, Caracas, Castries, Chaco |
| `l` | `w` | 79 | abiecadło, admirałka, adracjonał, adzamogłan, adzamogłanin, adziamugłan, adziamugłanin, amirał |
| `∅` | `a` | 75 | Aalborg, Aarhus, Bordeaux, Eichstaedt, Graal, Hainaut, Naypyidaw, Polandball |
| `i` | `ɛ` | 75 | Barbie, Castries, Dietrich, Erie, Freetown, Liechtenstein, Lier, Lietz |
| `w` | `∅` | 75 | Idaho, Jundziłł, Radziwiłł, Wyoming, bódł, darł, doszedł, dotarł |
| `ɕ` | `s` | 72 | Grosicki, Gęsicka, Gęsicki, Harasimowicz, Hirosima, Kosiba, Kosibor, Ksit |
| `j` | `i` | 63 | Bloemfontein, Deimos, Hanoi, Heidelberg, Idaho, Maine, Reich, Schneider |
| `ɛ` | `a` | 60 | Cambridge, Delaware, Facebook, Faraday, Idaho, Maine, Maryland, Michigan |
| `∅` | `ɔ` | 57 | Bloemfontein, Espoo, Facebook, Goetel, Google, Liverpool, MacBook, Melbourne |
| `∅` | `s` | 56 | Anschluss, Auschwitz, Düsseldorf, Grossmann, Missouri, Nossol, Overijssel, Roseau |
| `∅` | `l` | 52 | Ellert, Illinois, Kallisto, Miller, Müller, Thomalla, Valletta, Wellington |
| `k` | `g` | 51 | Göteborg, Heidelberg, Quaoar, Quito, Vorarlberg, aquapark, kdy, prequel |
| `w` | `v` | 50 | Delaware, Iowa, Wagadugu, Wellington, Wimbledon, Wisconsin, abandonware, bowling |
| `f` | `v` | 50 | Gietrzwałd, Gietrzwałdzianin, Gietrzwałdzianka, Gietrzwałdzianką, Quaoar, Quito, Schwarz, Vogel |
| `x` | `h` | 47 | Andrychiewicz, Banachiewicz, Eustachia, Eustachiusz, Lachiewicz, Melchior, Monachium, Paluchiewicz |
| `g` | `dʐ` | 46 | Angelą, Bydgoszcz, Bydgoszczy, Bydgoszczą, Ewangelia, Ewangelią, Ludgarda, angeliczny |
| `∅` | `g` | 40 | Aalborg, Cagliari, Liège, Nagy, Quebec, Quicherat, Quicherata, Quicheratowi |
| `∅` | `x` | 40 | Brahma, Bundeswehra, Drenthe, Ehlert, Hainaut, Lesotho, Lhasa, Lilith |
| `tʂ` | `x` | 39 | Chaco, Chile, Chilijczyk, Chilijka, Chubut, Manchester, Nietzsche, Weltschmerz |
| `dʑ` | `∅` | 37 | dziewięćdziesiąta, dziewięćdziesiąte, dziewięćdziesiątego, dziewięćdziesiątej, dziewięćdziesiątemu, dziewięćdziesiątym, dziewięćdziesiątymi, dziewięćdziesiątą |
| `∅` | `k` | 36 | Bordeaux, bordeaux, mchach, mchami, mchem, mchom, mchoszczur, mchowi |
| `s` | `ɕ` | 36 | Dżesika, Helsinki, Missisipi, Tbilisi, Wisconsin, dewadasi, epsilon, helsinka |
| `∅` | `n` | 32 | Bonn, Connecticut, Grossmann, Hoffmann, Johannesburg, Minnesota, Newcastle, Sanssouci |
| `a` | `u` | 32 | Connecticut, blockbuster, blunt, brunch, bug, bungee, countrowy, crush |
| `w` | `u` | 32 | Gouda, Mateusiak, Mateuszowy, Oulu, Pireus, chillout, foyer, gouda |
| `∅` | `i` | 32 | Illinois, barcią, charcia, charcią, charcię, chateaubriand, czarcia, czarcią |
| `u` | `w` | 30 | Aleuty, Jaunde, Kafarnaum, Reunion, Scheuring, Seul, aleuccy, aleucka |
| `∅` | `t` | 30 | Dhaka, Eichstaedt, Littwin, Massachusetts, Newcastle, Schmidt, Szmidt, Tottenham |
| `z` | `s` | 29 | Arkansas, Bundeswehra, Kansas, Molise, Salzburg, accusativus, bezrtęciowy, bonsai |
| `∅` | `j` | 29 | Barbie, Castries, Dietrich, Erie, GDDKiA, Iolą, Liechtenstein, Lier |
| `e` | `ɛ` | 27 | abalienowanie, abaliowanie, abrenuncjowanie, achcież, ałkierz, barwierz, bluźnierz, czel |

## Wrong entries (first 40 of 4506)

| text | category | espeak | expected |
|---|---|---|---|
| Aalborg |  | `ˈaalbɔrɡ` | `ɔlbɔr / ɔlbɔrk` |
| Aarhus |  | `aˈarxus` | `ɔrxus` |
| Abisynia |  | `ˌabʲisˈɨɲʲa` | `abisɘɲja` |
| Abrahamów |  | `ˌabraxˈamuf` | `abrɒxɒmof` |
| Adze |  | `ˈadʑɛ` | `ad͡zɛ` |
| Aecjusz |  | `ˈɛtsjuʃ` | `aɛt͡sjuʂ` |
| Akwitania |  | `ˌakfitˈaɲʲa` | `akfitaɲja` |
| Albania |  | `albˈaɲʲa` | `albaɲja` |
| Aleuty |  | `alˈɛwtɨ` | `alɛutɘ` |
| Alwernia |  | `alvˈɛrɲʲa` | `alvɛrɲja` |
| Amazonia |  | `ˌamazˈɔɲʲa` | `amazɔɲja` |
| Ambrozik |  | `ambrˈɔzik` | `ambrɔʑik` |
| Andrychiewicz |  | `ˌandrɨhjˈɛvitʃ` | `andrɘxjɛvit͡ʂ` |
| Andzia |  | `ˈaɲdʑa` | `and͡ʑa` |
| Andzią |  | `ˈaɲdʑɔ̃` | `and͡ʑɔw̃` |
| Angelą |  | `andʒˈɛlɔ̃` | `aŋɡɛlɔw̃` |
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
| Banachiewicz |  | `bˌanahjˈɛvitʃ` | `banaxjɛvit͡ʂ` |
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
| Bodzan |  | `bˈɔdʑan` | `bɔd͡zan` |
