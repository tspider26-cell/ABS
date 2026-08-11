# ABS Card Online Enrichment Service v1.0
# Adds online data layer after card identification

import requests


class CardOnlineEnrichmentService:

    def __init__(self):
        self.sources = [
            "pokemon_tcg_api"
        ]


    def enrich(self, card):

        result = dict(card)

        result.update({
            "image_url": None,
            "market_price": None,
            "source": None
        })


        if card.get("family") != "Pokemon":
            return result


        # Future online connector point
        # Uses identified card data:
        # name + set + number

        try:

            query = (
                f'name:"{card.get("name")}" '
                f'number:{card.get("number").split("/")[0]}'
            )


            # Placeholder:
            # real provider connection will be added here

            result["source"] = "pending_connector"


        except Exception as e:

            result["error"] = str(e)


        return result
