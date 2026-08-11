# ABS Card Search Service v1.3 DEBUG
# HTTP diagnostics version

import requests


class CardSearchService:

    def __init__(self):

        self.api_url = (
            "https://api.pokemontcg.io/v2/cards"
        )


    def search(self, metadata):

        result = {

            "found": False,
            "family": metadata.get("family"),
            "name": None,
            "set": metadata.get("set"),
            "number": metadata.get("number"),
            "rarity": None,
            "image": None,
            "price": None

        }


        if metadata.get("family") != "Pokemon":
            return result


        number = metadata.get("number")

        if not number:
            return result


        clean_number = number.split("/")[0]


        query = f"number:{clean_number}"


        try:

            response = requests.get(
                self.api_url,
                params={
                    "q": query,
                    "pageSize": 5
                },
                timeout=10
            )


            result["http_status"] = response.status_code

            result["content_type"] = (
                response.headers.get(
                    "content-type"
                )
            )


            result["raw_response"] = (
                response.text[:500]
            )


            if response.status_code != 200:

                return result


            data = response.json()


            cards = data.get(
                "data",
                []
            )


            if cards:

                card = cards[0]

                result["found"] = True
                result["name"] = card.get(
                    "name"
                )
                result["rarity"] = card.get(
                    "rarity"
                )


                result["image"] = (
                    card.get(
                        "images",
                        {}
                    )
                    .get("large")
                )


            return result


        except Exception as e:

            result["exception"] = str(e)

            return result
