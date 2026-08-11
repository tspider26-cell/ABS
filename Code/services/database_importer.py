# ABS Database Importer v1.0
# Builds unified ABS master card database

import json
from pathlib import Path


class DatabaseImporter:

    def __init__(self, output_path="database/master_cards.json"):

        self.output_path = Path(output_path)


    def load(self):

        if not self.output_path.exists():
            return []

        with open(
            self.output_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)


    def save(self, cards):

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                cards,
                file,
                indent=4,
                ensure_ascii=False
            )


    def normalize_card(self, card):

        return {
            "id": card.get("id"),
            "name": card.get("name"),
            "set": {
                "name": card.get("set"),
                "code": card.get("code")
            },
            "number": card.get("number"),
            "languages": card.get("languages", []),
            "rarity": card.get("rarity"),
            "images": card.get("images", []),
            "sources": card.get("sources", [])
        }


    def import_cards(self, cards):

        database = self.load()

        for card in cards:
            database.append(
                self.normalize_card(card)
            )

        self.save(database)

        return {
            "imported": len(cards),
            "total": len(database),
            "database": str(self.output_path)
        }
