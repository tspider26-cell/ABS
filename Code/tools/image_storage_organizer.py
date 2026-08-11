import json
import shutil
from pathlib import Path

MASTER = Path("database/master_cards.json")

SOURCE = Path(r"D:\ABS_DATA\pokemon_images\tcgdex")

TARGET = Path(r"D:\ABS_TEST_STORAGE")


LIMIT = 816


def load_master():

    with open(MASTER, "r", encoding="utf-8") as f:

        cards = json.load(f)

    return {card["id"]: card for card in cards}


def clean_name(name):

    chars = '<>:"/\\|?*'

    for c in chars:
        name = name.replace(c, "_")

    return name.replace(" ", "_")


def organize():

    database = load_master()

    TARGET.mkdir(parents=True, exist_ok=True)

    images = sorted(SOURCE.glob("*.png"))

    images = images[:LIMIT]

    stats = {"total": len(images), "copied": 0, "missing_metadata": 0}

    print("=" * 50)
    print("ABS IMAGE STORAGE ORGANIZER v1.0")
    print("=" * 50)

    print("TEST IMAGES:", len(images))

    for image in images:

        card_id = image.stem

        card = database.get(card_id)

        if not card:

            print(card_id, "NO MASTER DATA")

            stats["missing_metadata"] += 1
            continue

        set_data = card.get("set", {})

        set_id = set_data.get("id")

        set_name = clean_name(set_data.get("name", "Unknown"))

        folder_name = f"{set_id}_{set_name}"

        destination = TARGET / "Pokemon" / "TCG" / "EN" / folder_name

        destination.mkdir(parents=True, exist_ok=True)

        target_file = destination / image.name

        shutil.copy2(image, target_file)

        stats["copied"] += 1

        print(image.name, "->", folder_name)

    print()
    print(stats)


if __name__ == "__main__":

    organize()
