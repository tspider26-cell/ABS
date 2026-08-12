# ============================================================
# ABS Card Database Checker v1.0
#
# Sprawdza spójność:
# - database/master_cards.json
# - database/image_index.json
# - database/missing_images.json
# - D:\ABS_DATA\POKEMON\TCG\EN
#
# NIE MODYFIKUJE ŻADNYCH PLIKÓW
# ============================================================

import json
from pathlib import Path

MASTER = Path("database/master_cards.json")
INDEX = Path("database/image_index.json")
MISSING = Path("database/missing_images.json")

IMAGE_ROOT = Path("D:/ABS_DATA/POKEMON/TCG/EN")


def load_json(path):

    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    print("=" * 70)
    print("ABS CARD DATABASE CHECKER v1.0")
    print("=" * 70)

    master = load_json(MASTER)
    index = load_json(INDEX)
    missing = load_json(MISSING)

    master_ids = {c.get("id") for c in master if c.get("id")}

    index_ids = set(index.keys())

    png_files = list(IMAGE_ROOT.rglob("*.png"))

    png_ids = {p.stem for p in png_files}

    # ------------------------------------
    # Missing względem master
    # ------------------------------------

    missing_from_images = master_ids - png_ids

    # ------------------------------------
    # PNG bez indeksu
    # ------------------------------------

    png_without_index = png_ids - index_ids

    # ------------------------------------
    # Indeks wskazuje na brakujący plik
    # ------------------------------------

    broken_paths = []

    for card_id, data in index.items():

        image = data.get("image")

        if image:

            path = IMAGE_ROOT / image

            if not path.exists():

                broken_paths.append((card_id, image))

    # ------------------------------------
    # Katalogi ze spacjami
    # ------------------------------------

    folders_with_spaces = []

    for folder in IMAGE_ROOT.iterdir():

        if folder.is_dir():

            if " " in folder.name:

                folders_with_spaces.append(folder.name)

    print()

    print(f"MASTER CARDS:       {len(master_ids)}")

    print(f"IMAGE INDEX:        {len(index_ids)}")

    print(f"PNG FILES:          {len(png_files)}")

    print(f"MISSING JSON:       {len(missing)}")

    print()
    print("-" * 70)

    print(f"BRAK OBRAZU:        {len(missing_from_images)}")

    print(f"PNG BEZ INDEKSU:    {len(png_without_index)}")

    print(f"ZEPSUTE ŚCIEŻKI:   {len(broken_paths)}")

    print(f"KATALOGI SPACJE:   {len(folders_with_spaces)}")

    print()
    print("=" * 70)

    if broken_paths:

        print("\nPRZYKŁADOWE ZEŚCIEŻKI:")
        for item in broken_paths[:10]:
            print(item[0], "->", item[1])

    if folders_with_spaces:

        print("\nKATALOGI ZE SPACJĄ:")
        for f in folders_with_spaces:
            print(f)

    print()
    print("CHECK COMPLETE")
    print("=" * 70)


if __name__ == "__main__":

    main()
