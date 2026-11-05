"""
Tatoeba Sentence Integration & Matching Module.
Supports bulk TSV.BZ2 exports with transitive DE-EN-VI matching
and Tatoeba REST API v1 with SQLite caching and rate-limiting.
"""
import bz2
import json
import os
import re
import sqlite3
import time
import urllib.parse
import urllib.request
from typing import Dict, List, Optional, Set, Tuple
from pipeline.config import CACHE_FILES, TATOEBA_API_URL
from pipeline.scorer import score_example_sentence, sentence_contains_target, tokenize_sentence


class TatoebaService:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = str(CACHE_FILES["tatoeba_sqlite"])
        self.db_path = db_path
        self.sqlite_cache: Dict[str, List[Dict]] = {}
        self._init_sqlite()
        self.bulk_loaded = False
        self.bulk_deu_vie: Dict[int, Dict] = {}  # deu_id -> {id, de, vi, owner}
        self.token_to_sentence_ids: Dict[str, List[int]] = {}  # token_lower -> [deu_id, ...]
        self.used_sentence_ids: Set[int] = set()

    def _init_sqlite(self) -> None:
        """Initialize SQLite cache database for Tatoeba API calls and preload memory cache."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tatoeba_api_cache (
                    query_term TEXT PRIMARY KEY,
                    response_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
            cursor = conn.cursor()
            cursor.execute("SELECT query_term, response_json FROM tatoeba_api_cache")
            for q, r in cursor.fetchall():
                try:
                    self.sqlite_cache[q.lower()] = json.loads(r)
                except Exception:
                    pass

    def load_bulk_data(self) -> None:
        """
        Load bulk German-Vietnamese pairs from cache files:
        1. deu-vie_links.tsv.bz2 (direct links)
        2. deu-eng_links.tsv.bz2 + eng-vie_links.tsv.bz2 (transitive pivot links)
        3. vie_sentences.tsv.bz2
        4. deu_sentences.tsv.bz2
        """
        if self.bulk_loaded:
            return

        vie_path = CACHE_FILES["vie_sentences"]
        deu_path = CACHE_FILES["deu_sentences"]
        deu_vie_path = CACHE_FILES["deu_vie_links"]
        deu_eng_path = CACHE_FILES["deu_eng_links"]
        eng_vie_path = CACHE_FILES["eng_vie_links"]

        if not (vie_path.exists() and deu_path.exists()):
            print("Bulk Tatoeba files not all available in cache; will use API fallback when needed.")
            return

        print("Loading Tatoeba bulk datasets into memory...")

        # 1. Map English -> Vietnamese if eng_vie_links exists
        eng_to_vie_ids: Dict[int, List[int]] = {}
        if eng_vie_path.exists():
            with bz2.open(eng_vie_path, "rt", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("\t")
                    if len(parts) >= 2:
                        try:
                            eng_to_vie_ids.setdefault(int(parts[0]), []).append(int(parts[1]))
                        except ValueError:
                            continue

        # 2. Map German -> Vietnamese (direct + transitive pivot)
        deu_to_vie_ids: Dict[int, int] = {}
        # (a) Direct German -> Vietnamese
        if deu_vie_path.exists():
            with bz2.open(deu_vie_path, "rt", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("\t")
                    if len(parts) >= 2:
                        try:
                            deu_to_vie_ids[int(parts[0])] = int(parts[1])
                        except ValueError:
                            continue

        # (b) Transitive German -> English -> Vietnamese
        if deu_eng_path.exists() and eng_to_vie_ids:
            with bz2.open(deu_eng_path, "rt", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("\t")
                    if len(parts) >= 2:
                        try:
                            d_id = int(parts[0])
                            if d_id not in deu_to_vie_ids:
                                e_id = int(parts[1])
                                if e_id in eng_to_vie_ids:
                                    deu_to_vie_ids[d_id] = eng_to_vie_ids[e_id][0]
                        except ValueError:
                            continue

        # 3. Load Vietnamese sentences
        target_vie_ids = set(deu_to_vie_ids.values())
        vie_texts: Dict[int, str] = {}
        with bz2.open(vie_path, "rt", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 3:
                    try:
                        v_id = int(parts[0])
                        if v_id in target_vie_ids:
                            vie_texts[v_id] = parts[2].strip()
                    except ValueError:
                        continue

        # 4. Load German sentences & build inverted token index
        target_deu_ids = set(deu_to_vie_ids.keys())
        with bz2.open(deu_path, "rt", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 3:
                    try:
                        d_id = int(parts[0])
                        if d_id in target_deu_ids:
                            v_id = deu_to_vie_ids[d_id]
                            v_text = vie_texts.get(v_id)
                            if v_text:
                                de_text = parts[2].strip()
                                self.bulk_deu_vie[d_id] = {
                                    "id": d_id,
                                    "de": de_text,
                                    "vi": v_text,
                                    "source": "tatoeba",
                                    "owner": "Tatoeba Community",
                                    "license": "CC BY 2.0 FR",
                                }
                                # Index tokens for fast O(1) lookup
                                for tok in tokenize_sentence(de_text):
                                    tok_low = tok.lower()
                                    self.token_to_sentence_ids.setdefault(tok_low, []).append(d_id)
                    except ValueError:
                        continue

        self.bulk_loaded = True
        print(f"Loaded {len(self.bulk_deu_vie):,} German-Vietnamese bulk sentences (inverted index built).")

    def query_api_cached(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Query Tatoeba REST API v1 with SQLite cache and rate limiting.
        Endpoint: GET https://api.tatoeba.org/v1/sentences?lang=deu&sort=created&q={query}&trans:lang=vie&limit={limit}
        """
        clean_q = query.strip()
        if not clean_q:
            return []

        # 1. Check SQLite cache
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT response_json FROM tatoeba_api_cache WHERE query_term = ?",
                (clean_q.lower(),),
            )
            row = cursor.fetchone()
            if row:
                try:
                    return json.loads(row[0])
                except Exception:
                    pass

        # 2. Call Tatoeba API
        params = {
            "lang": "deu",
            "sort": "created",
            "q": clean_q,
            "trans:lang": "vie",
            "limit": str(limit),
        }
        url = f"{TATOEBA_API_URL}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "LingoLearning-GermanPipeline/1.0 (Education Project)",
                "Accept": "application/json",
            },
        )

        results = []
        try:
            time.sleep(0.12)
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for item in data.get("data", []):
                    de_text = item.get("text", "").strip()
                    de_id = item.get("id")
                    owner = item.get("owner", "Tatoeba")
                    license_str = item.get("license", "CC BY 2.0 FR")

                    vi_text = None
                    for t in item.get("translations", []):
                        if t.get("lang") == "vie":
                            v = t.get("text", "").strip()
                            if v:
                                vi_text = v
                                break

                    if de_text and vi_text:
                        results.append({
                            "id": de_id,
                            "de": de_text,
                            "vi": vi_text,
                            "source": "tatoeba",
                            "owner": owner,
                            "license": license_str,
                        })

            # Save to SQLite cache and in-memory cache
            self.sqlite_cache[clean_q.lower()] = results
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO tatoeba_api_cache (query_term, response_json) VALUES (?, ?)",
                    (clean_q.lower(), json.dumps(results, ensure_ascii=False)),
                )
                conn.commit()
        except Exception:
            pass

        return results

    def find_examples_for_word(
        self,
        lemma: str,
        forms: List[str],
        level: str = "A1",
        vocab_levels_dict: Optional[Dict[str, str]] = None,
        max_examples: int = 5,
        use_api: bool = True,
    ) -> List[Dict]:
        """
        Find and score candidate examples for a word and its forms.
        Uses fast inverted token index first, then API fallback.
        """
        all_forms = set(forms) | {lemma}
        candidates = []
        candidate_ids = set()

        if not self.bulk_loaded:
            self.load_bulk_data()

        # 1. Fast candidate discovery via inverted index
        for f in all_forms:
            for part in f.lower().split():
                if len(part) >= 2:
                    matched_sids = self.token_to_sentence_ids.get(part, [])
                    for s_id in matched_sids:
                        if s_id not in candidate_ids:
                            s_data = self.bulk_deu_vie.get(s_id)
                            if s_data and sentence_contains_target(s_data["de"], all_forms):
                                candidates.append(s_data)
                                candidate_ids.add(s_id)

        # 2. Check in-memory preloaded SQLite cache for previously queried sentences
        cached_items = self.sqlite_cache.get(lemma.lower(), [])
        for item in cached_items:
            if item.get("id") not in candidate_ids and sentence_contains_target(item.get("de", ""), all_forms):
                candidates.append(item)
                candidate_ids.add(item.get("id"))

        # 3. If fewer than 2 examples found and online API is explicitly enabled
        if use_api and len(candidates) < 2:
            api_results = self.query_api_cached(lemma, limit=5)
            for item in api_results:
                if item["id"] not in candidate_ids:
                    if sentence_contains_target(item["de"], all_forms):
                        candidates.append(item)
                        candidate_ids.add(item["id"])

        if not candidates:
            return []

        # 4. Score and rank candidates
        scored_candidates = []
        for cand in candidates:
            s_score = score_example_sentence(
                sentence_de=cand["de"],
                translation_vi=cand.get("vi"),
                target_forms=all_forms,
                target_level=level,
                vocab_level_dict=vocab_levels_dict,
                used_sentence_ids=self.used_sentence_ids,
                sentence_id=cand.get("id"),
            )
            scored_candidates.append((s_score, cand))

        # Sort descending by score
        scored_candidates.sort(key=lambda x: x[0], reverse=True)

        selected = []
        for _, cand in scored_candidates[:max_examples]:
            self.used_sentence_ids.add(cand["id"])
            selected.append({
                "de": cand["de"],
                "vi": cand.get("vi"),
                "source": "tatoeba",
                "tatoeba_id": cand.get("id"),
            })

        return selected
