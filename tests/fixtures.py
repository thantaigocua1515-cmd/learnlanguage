"""
Test fixtures for unit testing the German vocabulary pipeline.
These lightweight fixtures run offline with zero dependency on external 1GB datasets.
"""

SAMPLE_DWDS_LEMMAS = [
    # raw_lemma, wortart, expected_normalized
    ("ab|fahren", "Verb", "abfahren"),
    ("an·kommen", "Verb", "ankommen"),
    ("Haus", "Substantiv", "Haus"),
    ("haus", "Substantiv", "Haus"),
    ("Apfel", "Substantiv", "Apfel"),
    ("groß", "Adjektiv", "groß"),
    ("Groß", "Adjektiv", "groß"),
    ("über|raschen", "Verb", "überraschen"),
    (" schön ", "Adjektiv", "schön"),
    ("auf", "Präposition", "auf"),
    ("Auf", "Präposition", "auf"),
    ("CD-ROM", "Substantiv", "CD-ROM"),
]

SAMPLE_WORTART_MAPPINGS = [
    ("Substantiv", "noun"),
    ("Verb", "verb"),
    ("Adjektiv", "adj"),
    ("Komparativ", "adj"),
    ("Superlativ", "adj"),
    ("Adverb", "adv"),
    ("Präposition", "prep"),
    ("Pronomen", "pron"),
    ("Konjunktion", "conj"),
    ("Artikel", "det"),
    ("bestimmter Artikel", "det"),
    ("unbestimmter Artikel", "det"),
    ("Kardinalzahlwort", "num"),
    ("Interjektion", "intj"),
]

SAMPLE_SENTENCES_SCORING = [
    {
        "sentence_de": "Mein Haus ist schmutzig.",
        "translation_vi": "Nhà tôi bẩn lắm.",
        "target_level": "A1",
        "sentence_id": 14067743,
        "expect_high_score": True,
    },
    {
        "sentence_de": "Haus.",
        "translation_vi": None,
        "target_level": "A1",
        "sentence_id": 9999,
        "expect_high_score": False,  # Quá ngắn (<4 từ), không có bản dịch tiếng Việt
    },
    {
        "sentence_de": "In diesem außergewöhnlich komplizierten und philosophisch hochstehenden Gebäude ereignete sich eine unvorhersehbare Katastrophe.",
        "translation_vi": None,
        "target_level": "A1",
        "sentence_id": 8888,
        "expect_high_score": False,  # Quá dài (>12 từ), không có bản dịch tiếng Việt, từ vựng C1/C2
    },
]

SAMPLE_KAIKKI_FIXTURE_ENTRIES = [
    {
        "word": "Haus",
        "pos": "noun",
        "sounds": [{"ipa": "/haʊ̯s/"}],
        "forms": [
            {"form": "Hauses", "tags": ["genitive", "singular"]},
            {"form": "Häuser", "tags": ["nominative", "plural"]},
            {"form": "Häusern", "tags": ["dative", "plural"]},
        ],
        "senses": [
            {
                "glosses": ["house; home; building"],
                "examples": [
                    {"text": "Wir bauen ein neues Haus.", "english": "We are building a new house."}
                ],
            }
        ],
        "translations": [
            {"code": "vi", "lang": "Vietnamese", "word": "ngôi nhà"}
        ],
    },
    {
        "word": "abfahren",
        "pos": "verb",
        "sounds": [{"ipa": "/ˈapˌfaːʁən/"}],
        "forms": [
            {"form": "fährt ab", "tags": ["present", "singular", "third-person"]},
            {"form": "fuhr ab", "tags": ["preterite", "singular", "third-person"]},
            {"form": "abgefahren", "tags": ["participle", "past"]},
        ],
        "senses": [
            {
                "glosses": ["to depart; to leave (by vehicle)"],
            }
        ],
        "translations": [],
    },
]

