# ============================================================
# ABS TCGdex ZH-TW FULL IMPORTER v1.0
#
# Import chińskich kart z TCGdex
#
# Output:
# database/master_cards_zh.json
#
# Nie modyfikuje EN
# ============================================================

import json
import os
import requests


class TCGdexZHImporter:

    def __init__(self):

        self.base_url = "https://api.tcgdex.net/v2/zh-tw"

        self.output = "database/master_cards_zh.json"

    def get_sets(self):

        url = f"{self.base_url}/sets"

        response = requests.get(url, timeout=60)

        if response.status_code != 200:

            print("SETS ERROR:", response.status_code)

            return []

        return response.json()

    def get_set(self, set_id):

        url = f"{self.base_url}/sets/{set_id}"

        response = requests.get(url, timeout=60)

        if response.status_code != 200:

            return None

        return response.json()

    def convert_card(self, card, set_data):

        return {
            "id": card.get("id"),
            "family": "Pokemon",
            "name": card.get("name"),
            "set": {"id": set_data.get("id"), "name": set_data.get("name")},
            "number": card.get("localId"),
            "rarity": card.get("rarity"),
            "images": [],
            "languages": ["ZH-TW"],
            "sources": ["tcgdex"],
        }

    def import_database(self):

        database = []

        sets = self.get_sets()

        print("SETS FOUND:", len(sets))

        for index, item in enumerate(sets, start=1):

            set_id = item.get("id")

            print(f"[{index}/{len(sets)}] IMPORT:", set_id)

            set_data = self.get_set(set_id)

            if not set_data:

                continue

            for card in set_data.get("cards", []):

                database.append(self.convert_card(card, set_data))

        os.makedirs("database", exist_ok=True)

        with open(self.output, "w", encoding="utf-8") as file:

            json.dump(database, file, indent=4, ensure_ascii=False)

        return {"imported": len(database), "database": self.output}


if __name__ == "__main__":

    importer = TCGdexZHImporter()

    print(importer.import_database())
