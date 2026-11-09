from espeak_pl.ipa import align, edits, normalize, stress_positions, tokenize


def test_normalize_maps_espeak_and_wiktionary_notation():
    assert normalize("ʃˈɛʃtʃ") == normalize("ʂ ɛ ʂ t͡ʂ") == "ʂɛʂtʂ"
    assert normalize("bʒˈɛɡ") == "bʐɛg"
    assert normalize("kadɘks") == "kadɨks"


def test_normalize_softening_and_palatal_nasal():
    assert normalize("kʲˈɛvitʃ") == "kjɛvitʂ"
    assert normalize("ɲʲˈɛ") == "ɲɛ"
    assert normalize("bʲˈilɛt") == "bilɛt"


def test_normalize_allophones():
    assert normalize("çˈinɨ") == "xinɨ"
    assert normalize("afɡˈaŋka") == "afganka"
    assert normalize("bɔw̃k") == normalize("bɔ̃k") == "bɔ̃k"


def test_normalize_keeps_stress_on_request():
    assert normalize("matˈɛ", keep_stress=True) == "matˈɛ"
    assert normalize("matˈɛ") == "matɛ"


def test_tokenize_affricates_and_combining_marks():
    assert tokenize("tʂɔ̃dʑ") == ["tʂ", "ɔ̃", "dʑ"]
    assert tokenize("dzvɔn") == ["dz", "v", "ɔ", "n"]


def test_align_and_edits():
    pairs = align(["a", "b", "c"], ["a", "x", "c", "d"])
    assert pairs == [("a", "a"), ("b", "x"), ("c", "c"), ("", "d")]
    assert edits(["a", "b"], ["a", "b"]) == []
    assert edits(["a", "b"], ["b"]) == [("a", "")]


def test_stress_positions_ignore_onset_placement_and_secondary_stress():
    assert stress_positions("maˈtɛ") == stress_positions("matˈɛ") == (1,)
    assert stress_positions("mˌatɛmˈatɨka") == (2,)
    assert stress_positions("ɲˈɛ vjɛm") == (0,)
    assert stress_positions("dom") == ()
