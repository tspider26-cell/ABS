# ABS Image Index Rebuilder v1.0
#
# Odbudowa image_index.json z istniejących obrazów
#
# Źródło:
# D:/ABS_DATA/POKEMON/TCG/EN
#
# Wynik:
# database/image_index.json


import json
from pathlib import Path

MASTER = Path("database/master_cards.json")

INDEX = Path("database/image_index.json")

IMAGE_ROOT = Path("D:/ABS_DATA/POKEMON/TCG/EN")


def load_json(path):

    with open(path, "r", encoding="utf-8") as f:

        return json.load(f)


def save_json(path, data):

    with open(path, "w", encoding="utf-8") as f:

        json.dump(data, f, indent=4, ensure_ascii=False)


def build():

    print("=" * 60)
    print("ABS Image Index Rebuilder v1.0")
    print("=" * 60)

    cards = load_json(MASTER)

    metadata = {}

    for card in cards:

        metadata[card["id"]] = card

    index = {}

    count = 0
    missing_meta = 0

    for image in IMAGE_ROOT.rglob("*.png"):

        card_id = image.stem

        relative = image.relative_to(IMAGE_ROOT)

        card = metadata.get(card_id)

        if card:

            index[card_id] = {
                "name": card.get("name"),
                "set": card.get("set"),
                "number": card.get("number"),
                "image": str(relative).replace("\\", "/"),
            }

        else:

            missing_meta += 1

            index[card_id] = {
                "name": None,
                "set": None,
                "number": None,
                "image": str(relative).replace("\\", "/"),
            }

        count += 1

        print(f"[{count}] {card_id}")

    save_json(INDEX, index)

    print()
    print("=" * 60)
    print("DONE")
    print("=" * 60)

    print("Images:", count)

    print("Index:", len(index))

    print("Missing metadata:", missing_meta)


if __name__ == "__main__":

    build()
