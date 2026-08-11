# ABS SMART CARD RESOLVER v1.0
# Local database first, TCGdex fallback

from services.card_database_service_v2 import CardDatabaseService
from services.card_online_resolver import CardOnlineResolver


class SmartCardResolver:

    def __init__(self):

        self.database = CardDatabaseService()
        self.online = CardOnlineResolver()


    def resolve(self, metadata):

        # 1. Try local database using TCGdex id
        tcgdex_id = metadata.get("tcgdex_id")

        if tcgdex_id:

            card = self.database.find_by_id(
                tcgdex_id
            )

            if card:
                return {
                    "found": True,
                    "source": "local_database",
                    "card": card
                }


        # 2. Try local database using set + number
        set_id = metadata.get("set_id")
        number = metadata.get("number")

        if set_id and number:

            card = self.database.find_by_set_number(
                set_id,
                number
            )

            if card:
                return {
                    "found": True,
                    "source": "local_database",
                    "card": card
                }


        # 3. Fallback to TCGdex
        online_result = self.online.resolve(
            metadata
        )

        return online_result
