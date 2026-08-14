from pathlib import Path
import json
from collections import defaultdict

BASE = Path(r"D:\PTCG_FULL_DATABASE")

INVENTORY = BASE / "logs" / "abs_image_inventory_v1.json"
SOURCES = BASE / "logs" / "abs_image_source_report_v2.json"

OUTPUT = BASE / "database" / "image_master_index.json"


def detect_source(path):

    p = path.lower()

    if "\\images\\serebii\\english\\" in p:
        return "SEREBII_EN"

    if "\\images\\serebii\\japanese\\" in p:
        return "SEREBII_JP"

    if "\\images\\serebii\\" in p:
        return "SEREBII_ROOT"

    if "\\abs_data\\pokemon\\tcg\\en\\" in p:
        return "ABS_DATA_EN"

    if "\\abs_data\\pokemon\\tcg\\jp\\" in p:
        return "ABS_DATA_JP"

    if "jp_archive_old" in p:
        return "ABS_DATA_JP_ARCHIVE"

    if "\\zh-tw\\" in p.lower():
        return "ABS_DATA_ZH"

    if "\\tcgdex\\" in p.lower():
        return "TCGDEX"

    return "UNKNOWN"


def parse_card_key(path):

    p = Path(path)

    number = p.stem
    folder = p.parent.name

    return f"{folder}-{number}"


def quality(source):

    if source.startswith("SEREBII"):
        return "original"

    if source.startswith("ABS_DATA"):
        return "backup"

    if source == "TCGDEX":
        return "reference"

    return "unknown"


def main():

    print("=" * 70)
    print("ABS DATABASE v2")
    print("IMAGE MASTER INDEX BUILDER v1")
    print("=" * 70)

    with open(INVENTORY, "r", encoding="utf-8") as f:
        inventory = json.load(f)

    cards = defaultdict(list)

    for img in inventory["images"]:

        path = img["file"]

        key = parse_card_key(path)

        item = {
            "path": path,
            "source": detect_source(path),
            "quality": quality(detect_source(path)),
            "width": img.get("width"),
            "height": img.get("height"),
            "bytes": img.get("bytes"),
            "hash": img.get("hash"),
        }

        cards[key].append(item)

    result = {
        "project": "ABS DATABASE v2",
        "created": inventory["created"],
        "statistics": {"total_images": inventory["total"], "card_keys": len(cards)},
        "cards": cards,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w", encoding="utf-8") as f:

        json.dump(result, f, indent=2, ensure_ascii=False)

    print()
    print("TOTAL IMAGES:", inventory["total"])
    print("CARD KEYS:", len(cards))

    print()
    print("OUTPUT:")
    print(OUTPUT)

    print("=" * 70)


if __name__ == "__main__":
    main()
