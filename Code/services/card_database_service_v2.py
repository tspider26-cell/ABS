# ABS CARD DATABASE SERVICE v2.0
# Local master_cards.json database engine

import json
import os


class CardDatabaseService:

    def __init__(self, database_path="database/master_cards.json"):

        self.database_path = database_path
        self.cards = []
        self.load()


    def load(self):

        if not os.path.exists(self.database_path):
            self.cards = []
            return

        with open(
            self.database_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.cards = json.load(file)


    def normalize_number(self, number):

        if number is None:
            return None

        value = str(number).split("/")[0]

        return value.zfill(3)


    def find_by_id(self, tcgdex_id):

        for card in self.cards:

            if card.get("id") == tcgdex_id:
                return card

        return None


    def find_by_set_number(self, set_id, number):

        number = self.normalize_number(number)

        for card in self.cards:

            card_set = card.get("set", {})

            if (
                card_set.get("id") == set_id
                and self.normalize_number(card.get("number")) == number
            ):
                return card

        return None


    def search_name(self, name):

        if not name:
            return []

        name = name.lower()

        results = []

        for card in self.cards:

            if name in card.get("name", "").lower():
                results.append(card)

        return results


    def resolve_from_tcgdex_id(self, tcgdex_id):

        return self.find_by_id(tcgdex_id)


    def stats(self):

        return {
            "cards": len(self.cards),
            "database": self.database_path
        }
