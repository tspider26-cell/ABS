# ABS Web Card Provider v1.0

class WebCardProvider:

    def search(self, card):

        result = {
            "found": False,
            "provider": "web_provider",
            "query": None,
            "name": None,
            "source": None
        }


        query = (
            f'{card.get("name")} '
            f'{card.get("number")} '
            f'{card.get("set")}'
        )


        result["query"] = query


        # Connector for browser/search engine
        # will be added in next step


        return result
