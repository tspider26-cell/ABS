# ABS Pokemon API Provider v1.0

import requests


class PokemonAPIProvider:

    def __init__(self):
        self.url = "https://api.pokemontcg.io/v2/cards"


    def search(self, card):

        result = {
            "found": False,
            "provider": "pokemon_api",
            "name": None,
            "image_url": None,
            "set": None,
            "number": None,
            "rarity": None,
            "error": None
        }


        if card.get("family") != "Pokemon":
            return result


        number = card.get("number")

        if not number:
            return result


        try:

            response = requests.get(
                self.url,
                params={
                    "q": f'number:{number.split("/")[0]}',
                    "pageSize": 5
                },
                timeout=10
            )

            result["http_status"] = response.status_code

            if response.status_code != 200:
                return result


            data = response.json()

            cards = data.get("data", [])

            if not cards:
                return result


            item = cards[0]

            result["found"] = True
            result["name"] = item.get("name")
            result["number"] = item.get("number")
            result["rarity"] = item.get("rarity")
            result["set"] = item.get("set", {}).get("name")
            result["image_url"] = item.get("images", {}).get("large")

            return result


        except Exception as e:

            result["error"] = str(e)

            return result
