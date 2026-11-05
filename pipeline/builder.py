"""
Vocabulary Entry Builder & Schema Assembler.
Combines DWDS metadata, Kaikki lexical entry, and Tatoeba examples into the final JSON schema.
"""
from typing import Dict, List, Optional


def build_vocabulary_entry(
    dwds_item: Dict,
    kaikki_item: Optional[Dict],
    examples: List[Dict],
) -> Dict:
    """
    Build a single vocabulary item adhering strictly to the required schema:
    {
      "lemma": "Haus",
      "level": "A1",
      "pos": "noun",
      "article": "das",
      "gender": "neuter",
      "plural": "Häuser",
      "ipa": "haʊ̯s",
      "meaning_en": "house; home",
      "meaning_vi": null,
      "forms": ["Haus", "Hauses", "Häuser", "Häusern"],
      "examples": [ ... ],
      "synonyms": [],
      "missing": [],
      "sources": { "level": "DWDS/Goethe", "dictionary": "Kaikki/Wiktionary", "examples": "Tatoeba" }
    }
    """
    lemma = dwds_item["lemma"]
    level = dwds_item["level"]
    pos = dwds_item["pos"]
    article = dwds_item.get("article")
    gender = dwds_item.get("gender")

    missing = []
    if not kaikki_item:
        missing.append("kaikki")
        plural = None
        ipa = None
        meaning_en = None
        meaning_vi = None
        forms = [lemma]
        synonyms = []
    else:
        # Plural is only valid for nouns
        plural = (kaikki_item.get("plural") if pos == "noun" else None)
        ipa = kaikki_item.get("ipa")
        meaning_en = kaikki_item.get("meaning_en")
        meaning_vi = kaikki_item.get("meaning_vi")
        forms = kaikki_item.get("forms", [lemma])
        if lemma not in forms:
            forms.insert(0, lemma)
        synonyms = kaikki_item.get("synonyms", [])

    if not examples:
        missing.append("examples")

    return {
        "lemma": lemma,
        "level": level,
        "pos": pos,
        "article": article,
        "gender": gender,
        "plural": plural,
        "ipa": ipa,
        "meaning_en": meaning_en,
        "meaning_vi": meaning_vi,
        "forms": forms,
        "examples": examples,
        "synonyms": synonyms,
        "missing": missing,
        "sources": {
            "level": "DWDS/Goethe",
            "dictionary": "Kaikki/Wiktionary",
            "examples": "Tatoeba",
        },
    }
