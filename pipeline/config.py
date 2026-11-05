"""
Configuration module for the German Vocabulary Pipeline.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
OUTPUT_DIR = DATA_DIR / "output"

# Ensure directories exist
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Data Source URLs
DWDS_URLS = {
    "A1": "https://www.dwds.de/api/lemma/goethe/A1.csv",
    "A2": "https://www.dwds.de/api/lemma/goethe/A2.csv",
    "B1": "https://www.dwds.de/api/lemma/goethe/B1.csv",
}

KAIKKI_URL = "https://kaikki.org/dictionary/German/kaikki.org-dictionary-German.jsonl"

TATOEBA_BULK_URLS = {
    "deu_sentences": "https://downloads.tatoeba.org/exports/per_language/deu/deu_sentences.tsv.bz2",
    "vie_sentences": "https://downloads.tatoeba.org/exports/per_language/vie/vie_sentences.tsv.bz2",
    "deu_vie_links": "https://downloads.tatoeba.org/exports/per_language/deu/deu-vie_links.tsv.bz2",
    "deu_eng_links": "https://downloads.tatoeba.org/exports/per_language/deu/deu-eng_links.tsv.bz2",
    "eng_vie_links": "https://downloads.tatoeba.org/exports/per_language/eng/eng-vie_links.tsv.bz2",
}

TATOEBA_API_URL = "https://api.tatoeba.org/v1/sentences"

# Local Cache File Paths
CACHE_FILES = {
    "dwds_A1": CACHE_DIR / "dwds_A1.csv",
    "dwds_A2": CACHE_DIR / "dwds_A2.csv",
    "dwds_B1": CACHE_DIR / "dwds_B1.csv",
    "kaikki_jsonl": CACHE_DIR / "kaikki.org-dictionary-German.jsonl",
    "deu_sentences": CACHE_DIR / "deu_sentences.tsv.bz2",
    "vie_sentences": CACHE_DIR / "vie_sentences.tsv.bz2",
    "deu_vie_links": CACHE_DIR / "deu-vie_links.tsv.bz2",
    "deu_eng_links": CACHE_DIR / "deu-eng_links.tsv.bz2",
    "eng_vie_links": CACHE_DIR / "eng-vie_links.tsv.bz2",
    "tatoeba_sqlite": CACHE_DIR / "tatoeba_cache.sqlite3",
}

# CEFR Level Ordering: lowest level wins (A1 > A2 > B1)
CEFR_PRIORITY = {
    "A1": 1,
    "A2": 2,
    "B1": 3,
    "B2": 4,
    "C1": 5,
    "C2": 6,
}

