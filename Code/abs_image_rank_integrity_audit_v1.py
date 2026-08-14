from pathlib import Path
import json

INDEX = Path(r"D:\PTCG_FULL_DATABASE\database\image_master_index_ranked_v2.json")

OUTPUT = Path(r"D:\PTCG_FULL_DATABASE\logs\abs_image_rank_integrity_audit_v1.json")


def main():

    print("=" * 70)
    print("ABS DATABASE v2")
    print("IMAGE RANK INTEGRITY AUDIT v1")
    print("=" * 70)

    with open(INDEX, "r", encoding="utf-8") as f:
        data = json.load(f)

    cards = data["cards"]

    total = len(cards)

    no_preferred = []
    multiple_preferred = []
    bad_rank = []
    missing_path = []

    for card_id, images in cards.items():

        preferred = []

        for img in images:

            if img.get("preferred"):

                preferred.append(img)

        if len(preferred) == 0:

            no_preferred.append(card_id)

        elif len(preferred) > 1:

            multiple_preferred.append(card_id)

        else:

            item = preferred[0]

            if item.get("rank") != 1:
                bad_rank.append({"card": card_id, "rank": item.get("rank")})

            path = item.get("file") or item.get("path")

            if not path:
                missing_path.append(card_id)

    report = {
        "cards": total,
        "no_preferred": len(no_preferred),
        "multiple_preferred": len(multiple_preferred),
        "bad_rank": len(bad_rank),
        "missing_path": len(missing_path),
        "details": {
            "no_preferred": no_preferred[:100],
            "multiple_preferred": multiple_preferred[:100],
            "bad_rank": bad_rank[:100],
            "missing_path": missing_path[:100],
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w", encoding="utf-8") as f:

        json.dump(report, f, indent=2, ensure_ascii=False)

    print()
    print("CARDS:", total)
    print("NO PREFERRED:", len(no_preferred))
    print("MULTIPLE PREFERRED:", len(multiple_preferred))
    print("BAD RANK:", len(bad_rank))
    print("MISSING PATH:", len(missing_path))

    print()
    print("OUTPUT:")
    print(OUTPUT)

    print("=" * 70)


if __name__ == "__main__":
    main()
