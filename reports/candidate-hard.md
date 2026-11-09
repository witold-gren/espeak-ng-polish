# Candidate: hard cases

- source: `hard`
- espeak-ng data: `build/candidate/espeak-ng-data`
- piper-tts: `1.8.0`

| metric | value |
|---|---|
| entries | 115 |
| wrong entries | 2 |
| word error rate | 1.74% |
| phoneme error rate | 0.25% |
| stress checked / wrong | 60 / 0 |

## Error groups (orthographic pattern)

| group | words | wrong | error rate |
|---|---:|---:|---:|
| proper_noun | 29 | 2 | 6.90% |
| i_before_vowel | 32 | 2 | 6.25% |
| zi_si_ci_dzi_ni | 35 | 2 | 5.71% |
| rz | 8 | 0 | 0.00% |
| dz_dż_dź | 13 | 0 | 0.00% |
| prefix_before_vowel | 8 | 0 | 0.00% |
| prefix_before_z | 3 | 0 | 0.00% |
| nasal_ą_ę | 15 | 0 | 0.00% |
| final_voiced | 7 | 0 | 0.00% |
| w_after_voiceless | 4 | 0 | 0.00% |
| ch_h | 10 | 0 | 0.00% |
| foreign_letters | 7 | 0 | 0.00% |

## Most common confusions (expected → espeak)

| expected | espeak | words | examples |
|---|---|---:|---|
| `j` | `∅` | 2 | Albania, Dania |

## Wrong entries (first 2 of 2)

| text | category | espeak | expected |
|---|---|---|---|
| Albania | i_before_vowel | `albˈaɲʲa` | `alˈbaɲja` |
| Dania | i_before_vowel | `dˈaɲʲa` | `ˈdaɲja` |
