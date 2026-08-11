# ABS Card Database Service v1.0

import json
from pathlib import Path


class CardDatabaseService:

    def __init__(self, database_path="database/cards.json"):

        self.database_path = Path(database_path)

        self.cards = self.load()


    def load(self):

        if not self.database_path.exists():

            return []

        with open(
            self.database_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    def find(self, metadata):

        for card in self.cards:

            if (
                card.get("family") == metadata.get("family")
                and card.get("number") == metadata.get("number")
            ):

                return card


        return None
