"""
Reporting & Verification Module.
Generates statistical reports on matching rates, coverage, and missing entries.
"""
from typing import Dict, List
import json
from pathlib import Path


def generate_pipeline_report(entries: List[Dict], output_file: Path = None) -> Dict:
    """
    Generate statistics:
    - Total words by CEFR level
    - % matched with Kaikki
    - % with example sentences
    - % with Vietnamese translation
    - First 50 words with missing data
    """
    total = len(entries)
    if total == 0:
        return {"total": 0}

    by_level = {}
    kaikki_matched = 0
    with_examples = 0
    with_meaning_vi = 0
    missing_words = []

    for item in entries:
        lvl = item.get("level", "Unknown")
        by_level[lvl] = by_level.get(lvl, 0) + 1

        missing = item.get("missing", [])
        if "kaikki" not in missing:
            kaikki_matched += 1

        if "examples" not in missing and len(item.get("examples", [])) > 0:
            with_examples += 1

        if item.get("meaning_vi") is not None and str(item.get("meaning_vi")).strip():
            with_meaning_vi += 1

        if len(missing) > 0:
            if len(missing_words) < 50:
                missing_words.append({
                    "lemma": item.get("lemma"),
                    "level": item.get("level"),
                    "pos": item.get("pos"),
                    "missing": missing,
                })

    report = {
        "total_words": total,
        "by_level": by_level,
        "kaikki_match_count": kaikki_matched,
        "kaikki_match_percent": round((kaikki_matched / total) * 100.0, 2),
        "with_examples_count": with_examples,
        "with_examples_percent": round((with_examples / total) * 100.0, 2),
        "with_meaning_vi_count": with_meaning_vi,
        "with_meaning_vi_percent": round((with_meaning_vi / total) * 100.0, 2),
        "without_meaning_vi_percent": round((1.0 - (with_meaning_vi / total)) * 100.0, 2),
        "missing_data_count": len(missing_words),
        "first_50_missing_words": missing_words,
    }

    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    return report


def print_report_summary(report: Dict) -> None:
    """Print a clean formatted terminal summary."""
    print("=" * 65)
    print(" 🇩🇪 PIPELINE VERIFICATION & INTEGRATION REPORT")
    print("=" * 65)
    print(f"Total Words Processed: {report['total_words']}")
    print("Breakdown by Level:")
    for lvl, count in sorted(report["by_level"].items()):
        print(f"  • Level {lvl}: {count} words")
    print("-" * 65)
    print(f"Kaikki (Wiktionary) Match Rate : {report['kaikki_match_percent']}% ({report['kaikki_match_count']}/{report['total_words']})")
    print(f"Tatoeba Examples Coverage      : {report['with_examples_percent']}% ({report['with_examples_count']}/{report['total_words']})")
    print(f"Direct Vietnamese Meanings     : {report['with_meaning_vi_percent']}% ({report['with_meaning_vi_count']}/{report['total_words']})")
    print(f"Meaning VI Pending (meaning_en): {report['without_meaning_vi_percent']}%")
    print("-" * 65)
    missing_count = len(report.get("first_50_missing_words", []))
    print(f"Words with missing flags (sample up to 50): {missing_count} words")
    if missing_count > 0:
        for i, m in enumerate(report["first_50_missing_words"][:10], 1):
            print(f"  {i}. {m['lemma']} ({m['level']}, {m['pos']}) -> missing: {m['missing']}")
        if missing_count > 10:
            print(f"  ... and {missing_count - 10} more in report JSON.")
    print("=" * 65)

