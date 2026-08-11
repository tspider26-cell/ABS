import json
from pathlib import Path
from collections import defaultdict

MASTER = Path("database/master_cards.json")


STORAGE = Path(r"D:\ABS_TEST_STORAGE\Pokemon\TCG\EN")


def load_master():

    with open(MASTER, "r", encoding="utf-8") as f:

        return json.load(f)


def clean_name(name):

    chars = '<>:"/\\|?*'

    for c in chars:
        name = name.replace(c, "_")

    return name.replace(" ", "_")


def analyze_expected(cards):

    sets = defaultdict(int)

    for card in cards:

        set_data = card.get("set", {})

        set_id = set_data.get("id")

        set_name = set_data.get("name")

        if set_id:

            folder = f"{set_id}_{clean_name(set_name)}"

            sets[folder] += 1

    return sets


def analyze_storage():

    result = {}

    if not STORAGE.exists():

        return result

    for folder in STORAGE.iterdir():

        if folder.is_dir():

            images = list(folder.rglob("*.png"))

            result[folder.name] = len(images)

    return result


cards = load_master()

expected = analyze_expected(cards)

found = analyze_storage()


print("=" * 60)
print("ABS SET CARD COUNT CHECK")
print("=" * 60)


for folder in sorted(found.keys()):

    exp = expected.get(folder, 0)

    real = found[folder]

    status = "OK" if exp == real else "CHECK"

    print(f"{folder:45} EXPECTED: {exp:4} FOUND: {real:4} {status}")


print()
print("TOTAL SETS FOUND:", len(found))
print("=" * 60)
