# ABS Online Connector Service v1.0
# Real online data connector layer

import requests


class OnlineConnectorService:

    def __init__(self):
        self.api_url = "https://api.pokemontcg.io/v2/cards"


    def search_card(self, card):

        result = dict(card)

        result.update({
            "image_url": None,
            "market_price": None,
            "source": None,
            "online_found": False
        })


        if card.get("family") != "Pokemon":
            return result


        name = card.get("name")
        number = card.get("number")

        if not name or not number:
            return result


        query = (
            f'name:"{name}" '
            f'number:{number.split("/")[0]}'
        )


        try:

            response = requests.get(
                self.api_url,
                params={
                    "q": query,
                    "pageSize": 5
                },
                timeout=10
            )


            if response.status_code != 200:
                result["http_status"] = response.status_code
                return result


            data = response.json()

            cards = data.get(
                "data",
                []
            )


            if not cards:
                return result


            online_card = cards[0]

            result["online_found"] = True
            result["source"] = "PokemonTCG API"

            result["image_url"] = (
                online_card.get(
                    "images",
                    {}
                )
                .get("large")
            )

            result["rarity"] = (
                online_card.get(
                    "rarity"
                )
            )

            result["set_online"] = (
                online_card.get(
                    "set",
                    {}
                )
                .get("name")
            )


            result["market_price"] = (
                online_card.get(
                    "tcgplayer",
                    {}
                )
                .get("prices")
            )


        except Exception as e:

            result["error"] = str(e)


        return result
