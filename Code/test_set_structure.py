import json
from collections import defaultdict

MASTER = "database/master_cards.json"


with open(MASTER, "r", encoding="utf-8") as f:
    cards = json.load(f)


sets = defaultdict(list)


for card in cards:

    set_data = card.get("set", {})

    set_id = set_data.get("id")
    set_name = set_data.get("name")

    if set_id:

        sets[set_id].append({"name": set_name, "id": card["id"]})


print("=" * 60)
print("ABS SET STRUCTURE ANALYZER")
print("=" * 60)


print("TOTAL SETS:", len(sets))
print()


for set_id in list(sets.keys())[:30]:

    cards_count = len(sets[set_id])

    name = sets[set_id][0]["name"]

    print(f"{set_id:10} | {name:35} | {cards_count} cards")
