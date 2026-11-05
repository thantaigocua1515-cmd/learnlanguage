"""
Sentence Matching & Scoring Module for German Examples.
"""
import re
from typing import Set, Dict, List, Optional

CEFR_RANKS = {
    "A1": 1,
    "A2": 2,
    "B1": 3,
    "B2": 4,
    "C1": 5,
    "C2": 6,
}

PUNCTUATION_STRIP_REGEX = re.compile(r"^[^\wÄÖÜäöüß]+|[^\wÄÖÜäöüß]+$")


def tokenize_sentence(sentence: str) -> List[str]:
    """
    Tách từ trong câu:
    - Bỏ dấu câu ở đầu và cuối token
    - Giữ nguyên các ký tự tiếng Đức đặc trưng ä, ö, ü, ß
    """
    if not sentence:
        return []

    raw_tokens = sentence.strip().split()
    tokens = []
    for raw in raw_tokens:
        clean = PUNCTUATION_STRIP_REGEX.sub("", raw)
        if clean:
            tokens.append(clean)
    return tokens


def sentence_contains_target(sentence: str, target_forms: Set[str]) -> bool:
    """
    Kiểm tra xem câu có chứa từ cần tra hay không:
    - So khớp token với toàn bộ tập forms (dạng chia + lemma gốc)
    - So khớp không phân biệt hoa / thường
    - Hỗ trợ động từ tách (separable verbs): dạng 'fährt ab' -> câu phải chứa cả 'fährt' và 'ab'.
    """
    if not sentence or not target_forms:
        return False

    tokens = tokenize_sentence(sentence)
    tokens_lower = {t.lower() for t in tokens}

    for form in target_forms:
        if not form:
            continue
        form_clean = form.strip().lower()
        parts = form_clean.split()
        if len(parts) == 1:
            if parts[0] in tokens_lower:
                return True
        elif len(parts) > 1:
            # Separable verb or multi-word phrase: all parts must be present in sentence
            if all(part in tokens_lower for part in parts):
                return True

    return False


def score_example_sentence(
    sentence_de: str,
    translation_vi: Optional[str] = None,
    target_forms: Optional[Set[str]] = None,
    target_level: str = "A1",
    vocab_level_dict: Optional[Dict[str, str]] = None,
    used_sentence_ids: Optional[Set[int]] = None,
    sentence_id: Optional[int] = None,
) -> float:
    """
    Chấm điểm câu ví dụ theo đúng 4 tiêu chí:
    (a) Có bản dịch tiếng Việt trực tiếp (+50 điểm)
    (b) Độ dài lý tưởng 4–12 từ (+20 điểm). Quá ngắn (<4) hoặc quá dài (>12) bị trừ điểm.
    (c) Câu chỉ dùng từ vựng thuộc level của từ đó trở xuống (+15 điểm).
    (d) Tránh trùng lặp câu giữa các từ (-30 điểm nếu câu đã được sử dụng).
    """
    score = 0.0

    # (a) Có bản dịch tiếng Việt trực tiếp
    has_vi = bool(translation_vi and str(translation_vi).strip())
    if has_vi:
        score += 50.0

    # Tokenize câu
    tokens = tokenize_sentence(sentence_de)
    word_count = len(tokens)

    # (b) Độ dài câu 4–12 từ
    if 4 <= word_count <= 12:
        score += 20.0
    elif word_count < 4:
        score -= (4 - word_count) * 6.0
    else:  # word_count > 12
        score -= min(30.0, (word_count - 12) * 2.5)

    # (c) Đánh giá từ vựng theo level
    target_rank = CEFR_RANKS.get(target_level, 1)
    if vocab_level_dict and word_count > 0:
        in_level_count = 0
        higher_level_count = 0

        for tok in tokens:
            tok_low = tok.lower()
            lvl = vocab_level_dict.get(tok_low)
            if lvl:
                lvl_rank = CEFR_RANKS.get(lvl, 99)
                if lvl_rank <= target_rank:
                    in_level_count += 1
                else:
                    higher_level_count += 1

        if higher_level_count == 0 and in_level_count > 0:
            score += 15.0
        else:
            score -= higher_level_count * 3.0

    # (d) Tránh trùng lặp câu giữa các từ
    if sentence_id is not None and used_sentence_ids is not None:
        if sentence_id in used_sentence_ids:
            score -= 30.0

    return score
