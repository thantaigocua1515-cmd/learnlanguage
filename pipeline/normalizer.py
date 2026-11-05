"""
Normalization and Part-of-Speech Mapping Module.
"""
import unicodedata
import re

# DWDS Wortart to Kaikki POS mapping table
DWDS_TO_KAIKKI_POS = {
    "Substantiv": "noun",
    "Verb": "verb",
    "Adjektiv": "adj",
    "Komparativ": "adj",
    "Superlativ": "adj",
    "partizipiales Adjektiv": "adj",
    "Adverb": "adv",
    "Pronominaladverb": "adv",
    "Präposition": "prep",
    "Präposition + Artikel": "prep",
    "Pronomen": "pron",
    "Demonstrativpronomen": "pron",
    "Indefinitpronomen": "pron",
    "Interrogativpronomen": "pron",
    "Personalpronomen": "pron",
    "Possessivpronomen": "pron",
    "Reflexivpronomen": "pron",
    "Konjunktion": "conj",
    "Artikel": "det",
    "bestimmter Artikel": "det",
    "unbestimmter Artikel": "det",
    "Kardinalzahlwort": "num",
    "Ordinalzahlwort": "num",
    "Interjektion": "intj",
    "Partikel": "particle",
    "Eigenname": "name",
    "Affix": "affix",
    "Mehrwortausdruck": "phrase",
    "Symbol": "symbol",
}


def normalize_lemma(lemma: str, wortart: str = "") -> str:
    """
    Chuẩn hoá lemma:
    1. Unicode NFC
    2. Giữ nguyên ký tự ä/ö/ü/ß (không thay thế thành ae, oe, ue, ss)
    3. Bỏ ký tự đánh dấu tách động từ: '|' (ví dụ: 'ab|fahren' -> 'abfahren', 'an·kommen' -> 'ankommen')
    4. Bỏ khoảng trắng thừa ở đầu, cuối và giữa các từ
    5. Danh từ: viết hoa chữ đầu (Capitalized / Title-like for first char, keep rest)
       Động từ / tính từ / từ loại khác: chuyển chữ thường chữ đầu (hoặc toàn bộ nếu không phải viết tắt)
    """
    if not lemma:
        return ""

    # 1. Unicode NFC normalization
    s = unicodedata.normalize("NFC", str(lemma).strip())

    # 2. Loại bỏ dấu phân tách phân từ / tiếp đầu ngữ / ký tự đánh dấu
    s = s.replace("|", "").replace("·", "")

    # Chuẩn hoá khoảng trắng
    s = re.sub(r"\s+", " ", s).strip()

    if not s:
        return ""

    # 3. Quy tắc viết hoa / viết thường theo từ loại
    w_clean = (wortart or "").strip()
    pos = map_dwds_to_kaikki_pos(w_clean) if w_clean else ""

    if pos == "noun" or w_clean == "Substantiv":
        # Danh từ: viết hoa ký tự đầu
        s = s[0].upper() + s[1:]
    elif pos in ("verb", "adj", "adv", "prep", "conj", "det", "particle", "intj"):
        # Động từ / tính từ / từ khác: ký tự đầu viết thường nếu không phải viết tắt toàn bộ
        if not s.isupper():
            s = s[0].lower() + s[1:]

    return s


def map_dwds_to_kaikki_pos(dwds_wortart: str) -> str:
    """
    Ánh xạ từ loại DWDS sang chuẩn Kaikki / Wiktionary POS tag:
    - Substantiv -> noun
    - Verb -> verb
    - Adjektiv -> adj
    - Adverb -> adv
    - Präposition -> prep
    - Pronomen -> pron
    - Konjunktion -> conj
    - Artikel -> det
    - v.v...
    """
    cleaned = (dwds_wortart or "").strip()
    if cleaned in DWDS_TO_KAIKKI_POS:
        return DWDS_TO_KAIKKI_POS[cleaned]

    # Heuristic fallback
    low = cleaned.lower()
    if "substantiv" in low or "nomen" in low:
        return "noun"
    if "verb" in low:
        return "verb"
    if "adjektiv" in low:
        return "adj"
    if "adverb" in low:
        return "adv"
    if "präposition" in low:
        return "prep"
    if "pronomen" in low:
        return "pron"
    if "konjunktion" in low:
        return "conj"
    if "artikel" in low:
        return "det"
    if "zahl" in low or "numerale" in low:
        return "num"
    if "interjektion" in low:
        return "intj"
    if "partikel" in low:
        return "particle"

    return "other"

