"""
DWDS / Goethe-Institut Wordlist Loader & Level Resolver.
"""
import csv
import urllib.request
from typing import Dict, List, Tuple
from pipeline.config import DWDS_URLS, CACHE_FILES, CEFR_PRIORITY
from pipeline.normalizer import normalize_lemma, map_dwds_to_kaikki_pos

GENDER_MAP = {
    "mask.": "masculine",
    "fem.": "feminine",
    "neutr.": "neuter",
}

ARTICLE_TO_GENDER = {
    "der": "masculine",
    "die": "feminine",
    "das": "neuter",
}


def download_dwds_csvs() -> None:
    """Download DWDS CSV files for A1, A2, B1 if not already cached."""
    for level, url in DWDS_URLS.items():
        cache_path = CACHE_FILES[f"dwds_{level}"]
        if not cache_path.exists() or cache_path.stat().st_size == 0:
            print(f"Downloading DWDS {level} from {url}...")
            req = urllib.request.Request(url, headers={"User-Agent": "LingoLearning-Pipeline/1.0"})
            with urllib.request.urlopen(req) as resp, open(cache_path, "wb") as f:
                f.write(resp.read())


def load_dwds_vocab(levels: List[str] = None) -> List[Dict]:
    """
    Load DWDS vocabulary from CSV files, resolving CEFR levels and deduplicating.
    Quy tắc level:
    - Nếu một từ xuất hiện ở nhiều file thì lấy level thấp nhất (A1 thắng A2 thắng B1).
    - Khử trùng lặp theo (lemma chuẩn hoá, pos).
    """
    download_dwds_csvs()

    if levels is None:
        levels = ["A1", "A2", "B1"]

    # Map (normalized_lemma, pos) -> entry
    vocab_map: Dict[Tuple[str, str], Dict] = {}

    for lvl in levels:
        cache_path = CACHE_FILES[f"dwds_{lvl}"]
        if not cache_path.exists():
            continue

        with open(cache_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_lemma = row.get("Lemma", "").strip()
                if not raw_lemma or raw_lemma in ("%", "&"):
                    continue

                wortart = row.get("Wortart", "").strip()
                pos = map_dwds_to_kaikki_pos(wortart)
                norm_lemma = normalize_lemma(raw_lemma, wortart)
                if not norm_lemma:
                    continue

                genus = row.get("Genus", "").strip()
                article = row.get("Artikel", "").strip().lower()
                if not article and genus in ("mask.", "fem.", "neutr."):
                    if genus == "mask.":
                        article = "der"
                    elif genus == "fem.":
                        article = "die"
                    elif genus == "neutr.":
                        article = "das"

                gender = GENDER_MAP.get(genus) or ARTICLE_TO_GENDER.get(article)
                nur_im_plural = row.get("nur_im_Plural", "0").strip() == "1"

                key = (norm_lemma, pos)
                if key in vocab_map:
                    # Level comparison: lowest level wins (A1 has priority 1 < A2 priority 2 < B1 priority 3)
                    existing = vocab_map[key]
                    existing_priority = CEFR_PRIORITY.get(existing["level"], 99)
                    current_priority = CEFR_PRIORITY.get(lvl, 99)
                    if current_priority < existing_priority:
                        existing["level"] = lvl
                        if article:
                            existing["article"] = article
                        if gender:
                            existing["gender"] = gender
                else:
                    vocab_map[key] = {
                        "lemma": norm_lemma,
                        "raw_lemma": raw_lemma,
                        "level": lvl,
                        "wortart": wortart,
                        "pos": pos,
                        "article": article if article in ("der", "die", "das") else None,
                        "gender": gender,
                        "nur_im_plural": nur_im_plural,
                        "dwds_url": row.get("URL", "").strip(),
                    }

    return list(vocab_map.values())

