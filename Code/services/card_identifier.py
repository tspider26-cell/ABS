# ABS Card Identifier v1.0
# Converts OCR clues into a card identity

class CardIdentifier:

    def __init__(self):

        self.known_cards = [

            {
                "family": "Pokemon",
                "number": "035/088",
                "name": "Spritzee",
                "set": "Perfect Order",
                "code": "POR",
                "language": "EN",
                "rarity": "Common"
            }

        ]


    def identify(self, metadata):

        result = {

            "found": False,
            "name": None,
            "set": None,
            "code": None,
            "number": metadata.get("number"),
            "rarity": None,
            "language": None
        }


        for card in self.known_cards:

            if (
                card["family"] == metadata.get("family")
                and card["number"] == metadata.get("number")
            ):

                result["found"] = True
                result["name"] = card["name"]
                result["set"] = card["set"]
                result["code"] = card["code"]
                result["rarity"] = card["rarity"]
                result["language"] = card["language"]

                return result


        return result
