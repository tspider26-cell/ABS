from pathlib import Path
import json
from collections import Counter

BASE = Path(r"D:\PTCG_FULL_DATABASE")

INDEX = BASE / "database" / "image_master_index.json"

OUTPUT = BASE / "logs" / "image_master_index_audit_v1.json"


def main():

    print("=" * 70)
    print("ABS DATABASE v2")
    print("IMAGE MASTER INDEX AUDIT v1")
    print("=" * 70)

    with open(INDEX, "r", encoding="utf-8") as f:
        data = json.load(f)

    cards = data.get("cards", {})

    stats = {
        "total_card_keys": len(cards),
        "single_image_cards": 0,
        "multi_image_cards": 0,
        "missing_source": 0,
        "possible_bad_keys": 0,
    }

    image_counts = Counter()
    source_counts = Counter()

    bad_keys = []
    single_cards = []
    multi_cards = []

    for key, images in cards.items():

        count = len(images)

        image_counts[count] += 1

        if count == 1:
            stats["single_image_cards"] += 1
            single_cards.append(key)

        else:
            stats["multi_image_cards"] += 1
            multi_cards.append(key)

        for img in images:

            source = img.get("source")

            if not source:
                stats["missing_source"] += 1

            else:
                source_counts[source] += 1

        # kontrola podejrzanych nazw

        if "-" not in key:
            stats["possible_bad_keys"] += 1
            bad_keys.append(key)

    report = {
        "project": "ABS DATABASE v2",
        "index": str(INDEX),
        "statistics": stats,
        "image_count_distribution": dict(image_counts),
        "sources": dict(source_counts),
        "examples": {
            "single_image_cards": single_cards[:100],
            "multi_image_cards": multi_cards[:100],
            "bad_keys": bad_keys[:100],
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w", encoding="utf-8") as f:

        json.dump(report, f, indent=2, ensure_ascii=False)

    print()
    print("CARD KEYS:", stats["total_card_keys"])
    print("SINGLE IMAGE:", stats["single_image_cards"])
    print("MULTI IMAGE:", stats["multi_image_cards"])
    print("MISSING SOURCE:", stats["missing_source"])
    print("BAD KEYS:", stats["possible_bad_keys"])

    print()
    print("SOURCES:")

    for k, v in source_counts.items():
        print(k, v)

    print()
    print("OUTPUT:")
    print(OUTPUT)

    print("=" * 70)


if __name__ == "__main__":
    main()
