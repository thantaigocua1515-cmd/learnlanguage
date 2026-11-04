#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys

sys.path.append('/home/jikay/Desktop/LingoLearning/scripts')
from data_a1 import A1_WORDS
from data_a2 import A2_WORDS
from data_b1 import B1_WORDS
from data_b2_c1_c2 import B2_C1_C2_WORDS
from merge_and_pad_1000_extra import EXTRA_POOL

all_words = []
seen = set()

def normalize_and_register(item, default_lvl='A1'):
    w = str(item[0]).strip()
    if w in seen:
        return False

    g = None
    pl = None
    ipa = None
    pos = "Noun"
    lvl = default_lvl
    vi = ""
    en = ""
    ex_de = ""
    ex_vi = ""

    for elem in item[1:]:
        if not isinstance(elem, str):
            continue
        elem_s = elem.strip()
        if elem_s in {'der', 'die', 'das'}:
            g = elem_s
        elif elem_s in {'A1', 'A2', 'B1', 'B2', 'C1', 'C2'}:
            lvl = elem_s
        elif elem_s in {'Noun', 'Verb', 'Adjective', 'Adverb', 'Numeral'}:
            pos = elem_s
        elif elem_s.startswith('/') and elem_s.endswith('/'):
            ipa = elem_s
        elif elem_s.startswith('die ') and len(elem_s.split()) <= 3 and not vi:
            pl = elem_s
        elif not vi:
            vi = elem_s
        elif not en:
            en = elem_s
        elif not ex_de:
            ex_de = elem_s
        elif not ex_vi:
            ex_vi = elem_s

    if not ex_de:
        ex_de = f"Das Wort '{w}' ist im Deutschen sehr wichtig."
    if not ex_vi:
        ex_vi = f"Từ vựng '{w}' rất quan trọng trong tiếng Đức."
    if not en:
        en = w
    if not vi:
        vi = w

    seen.add(w)
    all_words.append({
        "word": w,
        "gender": g,
        "plural_form": pl,
        "ipa": ipa,
        "pos": pos,
        "cefr_level": lvl,
        "meaning_vi": vi,
        "meaning_en": en,
        "example_de": ex_de,
        "example_vi": ex_vi
    })
    return True

for it in A1_WORDS:
    normalize_and_register(it, 'A1')

for it in A2_WORDS:
    normalize_and_register(it, 'A2')

for it in B1_WORDS:
    normalize_and_register(it, 'B1')

for it in B2_C1_C2_WORDS:
    normalize_and_register(it, 'B2')

for ext in EXTRA_POOL:
    normalize_and_register(ext)
    if len(all_words) >= 1000:
        break

all_words = all_words[:1000]
print(f"Final distinct words in dataset: {len(all_words)}")

with open("/home/jikay/Desktop/LingoLearning/scripts/vocab_1000_final.json", "w", encoding="utf-8") as f:
    json.dump(all_words, f, ensure_ascii=False, indent=2)

print("Saved scripts/vocab_1000_final.json successfully!")
