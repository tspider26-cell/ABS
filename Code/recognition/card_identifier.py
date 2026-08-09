import os
import json


class CardIdentifier:

    def __init__(self):

        self.features_path = "database/features"

    def load_database(self):

        cards = []

        if not os.path.exists(self.features_path):

            return cards

        for file in os.listdir(self.features_path):

            if file.endswith(".json"):

                path = os.path.join(self.features_path, file)

                with open(path, "r", encoding="utf-8") as data:

                    cards.append(json.load(data))

        return cards

    def compare_hash(self, query_hash, card_hash):

        if query_hash == card_hash:

            return 100

        return 0

    def identify(self, features):

        database = self.load_database()

        best = None

        score = 0

        query_hash = features["features"]["hash"]

        for card in database:

            card_hash = card["features"]["hash"]

            result = self.compare_hash(query_hash, card_hash)

            if result > score:

                score = result

                best = card

        return {"card": best, "score": score}
