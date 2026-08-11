# ABS Smart Online Resolver v1.0
# Multi source online resolution layer

class SmartOnlineResolver:

    def __init__(self):
        self.providers = [
            "pokemon_api",
            "web_provider",
            "image_provider"
        ]


    def empty_result(self, card):

        return {
            "found": False,
            "provider": None,
            "name": card.get("name"),
            "set": card.get("set"),
            "number": card.get("number"),
            "rarity": card.get("rarity"),
            "image_url": None,
            "market_price": None,
            "source": None
        }


    def resolve(self, card):

        result = self.empty_result(card)

        if card.get("family") != "Pokemon":
            return result


        # Provider placeholders
        # Next step:
        # pokemon_api_provider
        # web_provider
        # image_provider


        result["source"] = "no_provider_result"

        return result
