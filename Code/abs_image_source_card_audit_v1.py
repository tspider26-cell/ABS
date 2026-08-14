from pathlib import Path
import json
from collections import Counter

BASE = Path(r"D:\PTCG_FULL_DATABASE")

INDEX = BASE / "database" / "image_master_index.json"

OUTPUT = BASE / "logs" / "image_source_card_audit_v1.json"


def main():

    print("=" * 70)
    print("ABS DATABASE v2")
    print("IMAGE SOURCE CARD AUDIT v1")
    print("=" * 70)

    with open(INDEX, "r", encoding="utf-8") as f:
        data = json.load(f)

    cards = data["cards"]

    stats = {
        "total_cards": len(cards),
        "cards_with_serebii": 0,
        "cards_with_abs_data": 0,
        "cards_with_tcgdex": 0,
        "cards_with_multiple_sources": 0,
        "cards_without_source": 0,
    }

    source_card_count = Counter()

    examples = {
        "only_serebii": [],
        "only_abs_data": [],
        "only_tcgdex": [],
        "multiple_sources": [],
        "no_source": [],
    }

    for key, images in cards.items():

        sources = set(img.get("source") for img in images)

        if not sources:
            stats["cards_without_source"] += 1
            examples["no_source"].append(key)

        if any(s.startswith("SEREBII") for s in sources):

            stats["cards_with_serebii"] += 1

        if any(s.startswith("ABS_DATA") for s in sources):

            stats["cards_with_abs_data"] += 1

        if "TCGDEX" in sources:

            stats["cards_with_tcgdex"] += 1

        if len(sources) > 1:

            stats["cards_with_multiple_sources"] += 1
            examples["multiple_sources"].append(key)

        for s in sources:
            source_card_count[s] += 1

    report = {
        "statistics": stats,
        "source_card_count": dict(source_card_count),
        "examples": {k: v[:100] for k, v in examples.items()},
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:

        json.dump(report, f, indent=2, ensure_ascii=False)

    print()

    for k, v in stats.items():
        print(k, ":", v)

    print()
    print("SOURCES:")

    for k, v in source_card_count.items():
        print(k, v)

    print()
    print("OUTPUT:")
    print(OUTPUT)

    print("=" * 70)


if __name__ == "__main__":
    main()
