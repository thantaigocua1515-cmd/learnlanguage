"""
Kaikki.org / Wiktionary Streaming Parser.
Reads the 1GB JSONL line-by-line (stream mode, low RAM footprint)
and filters only entries present in Source A's target lemma set.
"""
import json
import os
import re
from typing import Dict, Set, Optional, Tuple, List
from pipeline.config import CACHE_FILES
from pipeline.normalizer import normalize_lemma

COMPATIBLE_POS = {
    "prep": {"prep", "contraction", "postp"},
    "det": {"det", "article", "pron"},
    "pron": {"pron", "det", "adj"},
    "conj": {"conj", "adv", "particle"},
    "adv": {"adv", "particle", "conj"},
    "adj": {"adj", "adv", "pron"},
    "num": {"num", "adj", "noun"},
    "name": {"name", "noun"},
    "noun": {"noun", "name"},
    "verb": {"verb"},
    "intj": {"intj", "particle"},
    "particle": {"particle", "adv"},
}

EXCLUDED_FORM_TAGS = {
    "table-tags",
    "inflection-template",
    "class",
    "auxiliary",
    "multiword-construction",
}

EXCLUDED_FORM_WORDS = {
    "strong",
    "weak",
    "mixed",
    "haben",
    "sein",
    "werden",
    "haben or sein",
}


def clean_ipa(raw_ipa: str) -> str:
    """Clean IPA string removing enclosing slashes or brackets."""
    if not raw_ipa:
        return ""
    s = raw_ipa.strip()
    if (s.startswith("/") and s.endswith("/")) or (s.startswith("[") and s.endswith("]")):
        s = s[1:-1]
    return s.strip()


def extract_plural(forms: List[Dict], pos: str = "noun") -> Optional[str]:
    """Find plural form of noun from forms list (nouns only)."""
    if pos != "noun" or not forms:
        return None

    # Prioritize nominative plural
    for f in forms:
        tags = set(f.get("tags", []))
        if tags & EXCLUDED_FORM_TAGS:
            continue
        form_word = f.get("form", "").strip()
        if not form_word or form_word.lower() in EXCLUDED_FORM_WORDS:
            continue
        if "plural" in tags and ("nominative" in tags or len(tags) == 1):
            return form_word

    # Fallback to any plural tag
    for f in forms:
        tags = set(f.get("tags", []))
        if tags & EXCLUDED_FORM_TAGS:
            continue
        form_word = f.get("form", "").strip()
        if not form_word or form_word.lower() in EXCLUDED_FORM_WORDS:
            continue
        if "plural" in tags:
            return form_word
    return None


def extract_word_forms(lemma: str, forms: List[Dict], pos: str = "") -> List[str]:
    """Extract distinct valid surface forms for the word, filtering metadata tags."""
    result = {lemma}
    if not forms:
        return sorted(list(result))

    is_verb = (pos == "verb")

    for f in forms:
        tags = set(f.get("tags", []))
        # Filter out grammatical metadata tags
        if tags & EXCLUDED_FORM_TAGS:
            continue

        form_str = f.get("form", "").strip()
        if not form_str or form_str.startswith("de-") or len(form_str) <= 1:
            continue

        # Filter out metadata terms like "6 strong" or auxiliary verbs
        low_form = form_str.lower()
        if any(w in low_form for w in ("strong", "weak", "mixed", "inflection")):
            continue
        if is_verb and low_form in EXCLUDED_FORM_WORDS:
            continue

        # Filter out compound phrases with auxiliary verbs like "bin abgefahren", "hätte abgefahren"
        # Keep base inflections like "abgefahren", "fuhr ab", "fährt ab"
        tokens = form_str.split()
        if len(tokens) > 1:
            # Check if it contains auxiliary
            if tokens[0].lower() in ("bin", "bist", "ist", "sind", "seid", "war", "warst", "waren", "wart",
                                    "habe", "hast", "hat", "haben", "habt", "hatte", "hattest", "hatten",
                                    "werde", "wirst", "wird", "werden", "werdet", "würde", "hätte", "wäre"):
                # keep only the main participle if relevant
                main_part = tokens[-1]
                if len(main_part) > 2:
                    result.add(main_part)
                continue

        result.add(form_str)

    return sorted(list(result))


def extract_vietnamese_translation(entry: Dict) -> Optional[str]:
    """Extract Vietnamese translation if available in Kaikki/Wiktionary."""
    for t in entry.get("translations", []):
        if t.get("code") in ("vi", "vie") or t.get("lang") == "Vietnamese":
            word = t.get("word", "").strip()
            if word:
                return word

    for s in entry.get("senses", []):
        for t in s.get("translations", []):
            if t.get("code") in ("vi", "vie") or t.get("lang") == "Vietnamese":
                word = t.get("word", "").strip()
                if word:
                    return word
    return None


def extract_english_meaning(senses: List[Dict]) -> Optional[str]:
    """Extract English glosses from senses."""
    if not senses:
        return None

    glosses = []
    for s in senses:
        for g in s.get("glosses", []):
            clean_g = g.strip()
            if clean_g and clean_g not in glosses:
                glosses.append(clean_g)

    if not glosses:
        return None
    return "; ".join(glosses[:3])


def extract_ipa_sound(sounds: List[Dict]) -> Optional[str]:
    """Extract IPA phonetic transcription."""
    if not sounds:
        return None
    for s in sounds:
        ipa = s.get("ipa")
        if ipa:
            tags = set(s.get("tags", []))
            if "standard" in tags or "Germany" in tags:
                return clean_ipa(ipa)

    for s in sounds:
        ipa = s.get("ipa")
        if ipa:
            return clean_ipa(ipa)
    return None


def extract_synonyms(entry: Dict) -> List[str]:
    """Extract synonyms from entry and senses."""
    syns = set()
    for s in entry.get("synonyms", []):
        w = s.get("word", "").strip() if isinstance(s, dict) else str(s).strip()
        if w:
            syns.add(w)

    for sense in entry.get("senses", []):
        for s in sense.get("synonyms", []):
            w = s.get("word", "").strip() if isinstance(s, dict) else str(s).strip()
            if w:
                syns.add(w)
    return sorted(list(syns))


def parse_kaikki_entry(data: Dict) -> Dict:
    """Parse raw Kaikki JSON dict into structured dictionary data."""
    word = data.get("word", "").strip()
    pos = data.get("pos", "").strip()
    senses = data.get("senses", [])
    forms = data.get("forms", [])
    sounds = data.get("sounds", [])

    return {
        "word": word,
        "pos": pos,
        "senses_count": len(senses),
        "ipa": extract_ipa_sound(sounds),
        "plural": extract_plural(forms, pos=pos),
        "forms": extract_word_forms(word, forms, pos=pos),
        "meaning_en": extract_english_meaning(senses),
        "meaning_vi": extract_vietnamese_translation(data),
        "synonyms": extract_synonyms(data),
    }


def stream_kaikki_for_lemmas(
    target_lemmas_map: Dict[Tuple[str, str], Dict],
    jsonl_path: Optional[str] = None,
    max_scan_lines: Optional[int] = None,
    progress_callback=None,
) -> Dict[Tuple[str, str], Dict]:
    """
    Stream Kaikki JSONL line by line.
    - Matches (normalized_word, pos).
    - If multiple entries match (word, pos), selects the one with the most senses.
    """
    if jsonl_path is None:
        jsonl_path = str(CACHE_FILES["kaikki_jsonl"])

    if not os.path.exists(jsonl_path):
        print(f"Warning: Kaikki JSONL file {jsonl_path} does not exist.")
        return {}

    target_words_set = {k[0].lower() for k in target_lemmas_map.keys()}

    best_entries: Dict[Tuple[str, str], Dict] = {}
    file_size = os.path.getsize(jsonl_path)
    bytes_read = 0
    line_count = 0

    with open(jsonl_path, mode="r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line_count += 1
            bytes_read += len(line.encode("utf-8"))

            if line_count % 35000 == 0:
                percent = (bytes_read / file_size) * 100.0 if file_size > 0 else 0.0
                if progress_callback:
                    progress_callback(percent, len(best_entries))
                else:
                    print(f"Kaikki scan: {percent:.1f}% ({line_count:,} lines, {len(best_entries)} matched)...")

            if max_scan_lines and line_count >= max_scan_lines:
                break

            if '"word":' not in line:
                continue

            try:
                data = json.loads(line)
            except Exception:
                continue

            raw_word = data.get("word", "")
            if not raw_word or raw_word.lower() not in target_words_set:
                continue

            pos = data.get("pos", "")
            parsed = parse_kaikki_entry(data)

            # Match against target_lemmas_map
            for (t_lemma, t_pos), t_item in target_lemmas_map.items():
                if t_lemma.lower() != raw_word.lower():
                    continue

                matched = False
                if t_pos == pos:
                    matched = True
                elif t_pos == "other" or not t_pos:
                    matched = True
                elif t_pos in COMPATIBLE_POS and pos in COMPATIBLE_POS[t_pos]:
                    matched = True

                if matched:
                    target_key = (t_lemma, t_pos)
                    if (
                        target_key not in best_entries
                        or parsed["senses_count"] > best_entries[target_key]["senses_count"]
                    ):
                        best_entries[target_key] = parsed

            if len(best_entries) == len(target_lemmas_map):
                print(f"All {len(target_lemmas_map)} target entries found in Kaikki! Early stop at line {line_count:,}.")
                break

    return best_entries
