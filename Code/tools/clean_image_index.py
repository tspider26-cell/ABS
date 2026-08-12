# ============================================================
# ABS Image Index Cleaner v1.0
#
# Usuwa z image_index.json tylko te wpisy,
# dla których obraz PNG faktycznie nie istnieje.
#
# NIE USUWA ŻADNYCH OBRAZÓW.
# NIE MODYFIKUJE master_cards.json.
# NIE POBIERA NIC Z INTERNETU.
#
# Przed zapisem tworzy kopię:
# database/image_index_before_clean.json
# ============================================================

import json
import shutil
from pathlib import Path

INDEX = Path("database/image_index.json")

BACKUP = Path("database/image_index_before_clean.json")

IMAGE_ROOT = Path("D:/ABS_DATA/POKEMON/TCG/EN")


def load_json(path):

    with open(path, "r", encoding="utf-8") as f:

        return json.load(f)


def save_json(path, data):

    temp = path.with_suffix(path.suffix + ".tmp")

    with open(temp, "w", encoding="utf-8") as f:

        json.dump(data, f, indent=4, ensure_ascii=False)

    temp.replace(path)


def main():

    print("=" * 70)
    print("ABS IMAGE INDEX CLEANER v1.0")
    print("=" * 70)

    if not INDEX.exists():

        print()
        print("ERROR:")
        print("Nie znaleziono:")
        print(INDEX)
        return

    # --------------------------------------------------------
    # Backup
    # --------------------------------------------------------

    shutil.copy2(INDEX, BACKUP)

    print()
    print("Backup:", BACKUP)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    index = load_json(INDEX)

    original_count = len(index)

    clean_index = {}

    removed = []

    # --------------------------------------------------------
    # Check paths
    # --------------------------------------------------------

    for card_id, data in index.items():

        image = data.get("image")

        if not image:

            removed.append((card_id, "NO IMAGE PATH"))

            continue

        image_path = IMAGE_ROOT / image

        if image_path.is_file():

            clean_index[card_id] = data

        else:

            removed.append((card_id, image))

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_json(INDEX, clean_index)

    final_count = len(clean_index)

    print()
    print("-" * 70)

    print("INDEX BEFORE:", original_count)

    print("REMOVED:", len(removed))

    print("INDEX AFTER:", final_count)

    # --------------------------------------------------------
    # Removed entries
    # --------------------------------------------------------

    if removed:

        print()
        print("USUNIĘTE WPISY:")

        for card_id, image in removed[:30]:

            print(f"{card_id} -> {image}")

        if len(removed) > 30:

            print(f"... oraz " f"{len(removed) - 30} kolejnych")

    print()
    print("=" * 70)
    print("CLEAN COMPLETE")
    print("=" * 70)


if __name__ == "__main__":

    main()
