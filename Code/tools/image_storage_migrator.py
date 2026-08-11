import json
import shutil
from pathlib import Path

MASTER = Path("database/master_cards.json")

SOURCE = Path(r"D:\ABS_DATA\pokemon_images\tcgdex")

TARGET = Path(r"D:\ABS_DATA\Pokemon\TCG\EN")


LIMIT = None  # None = wszystko


def load_master():

    with open(MASTER, "r", encoding="utf-8") as f:

        cards = json.load(f)

    return {card["id"]: card for card in cards}


def clean_name(name):

    chars = '<>:"/\\|?*'

    for c in chars:
        name = name.replace(c, "_")

    return name.replace(" ", "_")


def migrate():

    database = load_master()

    images = sorted(SOURCE.glob("*.png"))

    if LIMIT:
        images = images[:LIMIT]

    TARGET.mkdir(parents=True, exist_ok=True)

    stats = {"total": len(images), "copied": 0, "missing_metadata": 0}

    print("=" * 50)
    print("ABS IMAGE STORAGE MIGRATOR v1.0")
    print("=" * 50)

    print("FILES:", len(images))

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

        folder = f"{set_id}_{set_name}"

        destination = TARGET / folder

        destination.mkdir(parents=True, exist_ok=True)

        target_file = destination / image.name

        shutil.copy2(image, target_file)

        stats["copied"] += 1

        print(image.name, "->", folder)

    print()
    print(stats)


if __name__ == "__main__":

    migrate()
