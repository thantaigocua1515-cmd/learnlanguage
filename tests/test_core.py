"""
Unit tests for the 3 core functions of the German Vocabulary Pipeline:
1. normalize_lemma
2. map_dwds_to_kaikki_pos
3. score_example_sentence
"""
import unittest
from pipeline.normalizer import normalize_lemma, map_dwds_to_kaikki_pos
from pipeline.scorer import score_example_sentence, tokenize_sentence, sentence_contains_target
from tests.fixtures import (
    SAMPLE_DWDS_LEMMAS,
    SAMPLE_WORTART_MAPPINGS,
    SAMPLE_SENTENCES_SCORING,
)


class TestGermanVocabularyPipelineCore(unittest.TestCase):

    def test_normalize_lemma_comprehensive(self):
        """Test Unicode normalization, separator removal, and casing rules."""
        for raw, wortart, expected in SAMPLE_DWDS_LEMMAS:
            with self.subTest(raw=raw, wortart=wortart):
                result = normalize_lemma(raw, wortart)
                self.assertEqual(
                    result,
                    expected,
                    f"Failed normalizing '{raw}' ({wortart}): expected '{expected}', got '{result}'",
                )

        # Test preserving special German characters ä/ö/ü/ß
        self.assertEqual(normalize_lemma("Bücher", "Substantiv"), "Bücher")
        self.assertEqual(normalize_lemma("süß", "Adjektiv"), "süß")
        self.assertEqual(normalize_lemma("weiß", "Adjektiv"), "weiß")
        self.assertEqual(normalize_lemma("groß", "Adjektiv"), "groß")

    def test_map_dwds_to_kaikki_pos(self):
        """Test accurate mapping between DWDS Wortart and Kaikki POS tags."""
        for dwds_pos, expected_kaikki_pos in SAMPLE_WORTART_MAPPINGS:
            with self.subTest(dwds_pos=dwds_pos):
                result = map_dwds_to_kaikki_pos(dwds_pos)
                self.assertEqual(
                    result,
                    expected_kaikki_pos,
                    f"Failed mapping '{dwds_pos}': expected '{expected_kaikki_pos}', got '{result}'",
                )

    def test_tokenize_sentence(self):
        """Test German sentence tokenization with umlauts and punctuation stripping."""
        tokens = tokenize_sentence("Mein Haus ist schmutzig!")
        self.assertEqual(tokens, ["Mein", "Haus", "ist", "schmutzig"])

        tokens_umlauts = tokenize_sentence("»Die Äpfel sind süß und schön!«")
        self.assertEqual(tokens_umlauts, ["Die", "Äpfel", "sind", "süß", "und", "schön"])

    def test_sentence_contains_target_inflections(self):
        """Test matching sentence tokens against target lemma and inflected forms."""
        # Inflected verb: 'fährt ab' / 'fuhr ab' for lemma 'abfahren'
        forms = {"abfahren", "fährt ab", "fuhr", "abgefahren"}
        self.assertTrue(sentence_contains_target("Der Zug fuhr pünktlich ab.", forms))
        self.assertTrue(sentence_contains_target("Wir sind gestern abgefahren.", forms))
        self.assertFalse(sentence_contains_target("Wir essen zu Abend.", forms))

        # Inflected noun: 'Häuser' for 'Haus'
        noun_forms = {"Haus", "Hauses", "Häuser", "Häusern"}
        self.assertTrue(sentence_contains_target("In dieser Straße stehen viele schöne Häuser.", noun_forms))

    def test_score_example_sentence(self):
        """Test sentence scoring criteria: Vietnamese translation, ideal word length, level vocabulary, and deduplication."""
        vocab_levels = {
            "mein": "A1",
            "haus": "A1",
            "ist": "A1",
            "schmutzig": "A1",
        }

        # Case 1: Ideal 4-12 words sentence with Vietnamese translation
        score_ideal = score_example_sentence(
            sentence_de="Mein Haus ist schmutzig.",
            translation_vi="Nhà tôi bẩn lắm.",
            target_level="A1",
            vocab_level_dict=vocab_levels,
            sentence_id=14067743,
            used_sentence_ids=set(),
        )

        # Case 2: Too short, no translation
        score_short = score_example_sentence(
            sentence_de="Haus.",
            translation_vi=None,
            target_level="A1",
            sentence_id=9999,
            used_sentence_ids=set(),
        )

        # Case 3: Reused / duplicate sentence (penalized)
        score_reused = score_example_sentence(
            sentence_de="Mein Haus ist schmutzig.",
            translation_vi="Nhà tôi bẩn lắm.",
            target_level="A1",
            vocab_level_dict=vocab_levels,
            sentence_id=14067743,
            used_sentence_ids={14067743},
        )

        self.assertGreater(
            score_ideal,
            score_short,
            "Ideal sentence with translation should score significantly higher than short untranslated word",
        )
        self.assertGreater(
            score_ideal,
            score_reused,
            "Reused sentence should receive penalty compared to unused sentence",
        )
        # Score ideal should have +50 (has VI) + 20 (length 4) + 15 (all in level) = 85.0
        self.assertGreaterEqual(score_ideal, 70.0)


if __name__ == "__main__":
    unittest.main()

