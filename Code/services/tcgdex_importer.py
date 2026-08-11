# ABS TCGdex Importer v1.0
# Imports cards from TCGdex compatible JSON data

import json
from pathlib import Path


class TCGdexImporter:

    def __init__(
        self,
        source_path="database/sources/tcgdex/cards.json"
    ):

        self.source_path = Path(source_path)


    def load_source(self):

        if not self.source_path.exists():

            return []

        with open(
            self.source_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    def normalize_card(self, card):

        return {

            "id": card.get("id"),

            "name": card.get(
                "name"
            ),

            "set": {

                "name": card.get(
                    "set"
                ),

                "code": card.get(
                    "set_code"
                )

            },

            "number": card.get(
                "number"
            ),

            "languages": card.get(
                "languages",
                []
            ),

            "rarity": card.get(
                "rarity"
            ),

            "images": card.get(
                "images",
                []
            ),

            "sources": [
                "tcgdex"
            ]
        }


    def import_cards(self):

        source = self.load_source()

        result = []

        for card in source:

            result.append(
                self.normalize_card(card)
            )

        return result
