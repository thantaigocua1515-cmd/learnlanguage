#!/usr/bin/env python3
"""
CLI Runner for the German Vocabulary Pipeline.
Merges DWDS (Goethe), Kaikki (Wiktionary), and Tatoeba datasets.
"""
import argparse
import json
import sys
from pathlib import Path

from pipeline.builder import build_vocabulary_entry
from pipeline.config import CACHE_FILES, OUTPUT_DIR
from pipeline.dwds import load_dwds_vocab
from pipeline.kaikki import stream_kaikki_for_lemmas
from pipeline.reporter import generate_pipeline_report, print_report_summary
from pipeline.tatoeba import TatoebaService


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge DWDS + Kaikki + Tatoeba into a clean German A1-B1 vocabulary dataset."
    )
    parser.add_argument(
        "--level",
        type=str,
        default="A1",
        choices=["A1", "A2", "B1", "all"],
        help="CEFR level to extract (default: A1)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of vocabulary words to process (e.g. 100 for sample testing)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run full extraction across A1, A2, and B1 levels (overrides --level)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSON file path (default: data/output/vocab_<level>_<limit>.json)",
    )
    parser.add_argument(
        "--report",
        type=str,
        default=None,
        help="Report JSON file path (default: data/output/report_<level>_<limit>.json)",
    )
    parser.add_argument(
        "--no-api",
        action="store_true",
        help="Disable Tatoeba online API queries (use only local bulk datasets)",
    )
    parser.add_argument(
        "--enable-api",
        action="store_true",
        help="Force enable online Tatoeba API calls even during full dataset build",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    levels = ["A1", "A2", "B1"] if (args.full or args.level == "all") else [args.level]
    print(f"🚀 Starting German Vocabulary Pipeline for levels: {', '.join(levels)}")
    if args.limit:
        print(f"⚙️ Execution Mode: Limited sample to {args.limit} words")
    else:
        print("⚙️ Execution Mode: Full dataset extraction")

    # Step 1: Load and resolve DWDS Goethe Wordlist
    print("\n[Step 1/4] Loading & deduplicating DWDS / Goethe wordlist...")
    dwds_entries = load_dwds_vocab(levels=levels)
    print(f"Found {len(dwds_entries)} unique (lemma, pos) entries in DWDS.")

    # Apply limit if specified
    if args.limit and args.limit > 0:
        dwds_entries = dwds_entries[: args.limit]
        print(f"Applied limit: processing {len(dwds_entries)} entries.")

    # Target map: (lemma, pos) -> item
    target_lemmas_map = {(item["lemma"], item["pos"]): item for item in dwds_entries}
    vocab_levels_dict = {item["lemma"].lower(): item["level"] for item in dwds_entries}

    # Step 2: Stream Kaikki JSONL for target lemmas
    print("\n[Step 2/4] Streaming Kaikki JSONL to match target vocabulary...")
    kaikki_matches = stream_kaikki_for_lemmas(target_lemmas_map)
    print(f"Matched {len(kaikki_matches)} / {len(dwds_entries)} entries in Kaikki dictionary.")

    # Step 3: Match & Score Tatoeba Sentences
    print("\n[Step 3/4] Finding & scoring Tatoeba example sentences...")
    tatoeba_service = TatoebaService()
    tatoeba_service.load_bulk_data()

    results = []
    total = len(dwds_entries)
    # In full mode, default to high-performance local bulk + SQLite cache; enable online API only if requested or in sample mode
    if args.full:
        use_api = args.enable_api and not args.no_api
    else:
        use_api = not args.no_api

    for idx, dwds_item in enumerate(dwds_entries, 1):
        key = (dwds_item["lemma"], dwds_item["pos"])
        kaikki_item = kaikki_matches.get(key)
        if not kaikki_item:
            # Case-insensitive fallback
            for (w, p), k_val in kaikki_matches.items():
                if w.lower() == dwds_item["lemma"].lower() and p == dwds_item["pos"]:
                    kaikki_item = k_val
                    break

        forms = kaikki_item.get("forms", []) if kaikki_item else [dwds_item["lemma"]]
        examples = tatoeba_service.find_examples_for_word(
            lemma=dwds_item["lemma"],
            forms=forms,
            level=dwds_item["level"],
            vocab_levels_dict=vocab_levels_dict,
            max_examples=5,
            use_api=use_api,
        )

        entry = build_vocabulary_entry(
            dwds_item=dwds_item,
            kaikki_item=kaikki_item,
            examples=examples,
        )
        results.append(entry)

        if idx % 20 == 0 or idx == total:
            pct = (idx / total) * 100.0
            print(f"Building entries: {pct:.1f}% ({idx}/{total})...")

    # Step 4: Output Files & Report Generation
    print("\n[Step 4/4] Generating JSON output and verification report...")
    suffix = f"{levels[0]}_{args.limit}" if args.limit else f"{'_'.join(levels)}_full"
    output_path = Path(args.output) if args.output else (OUTPUT_DIR / f"vocab_{suffix}.json")
    report_path = Path(args.report) if args.report else (OUTPUT_DIR / f"report_{suffix}.json")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    report = generate_pipeline_report(results, output_file=report_path)
    print_report_summary(report)

    print(f"\n✅ Output JSON saved to: {output_path}")
    print(f"✅ Report JSON saved to: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

