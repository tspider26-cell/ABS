# ABS CARD ONLINE RESOLVER v1.8
# Correct TCGdex ID format: set_id-localId with zero padding
# Example: me03-035

from services.tcgdex_service import TCGdexService


class CardOnlineResolver:

    def __init__(self):

        self.tcgdex = TCGdexService()

        # Pokemon set codes -> TCGdex set ids
        self.set_mapping = {
            "POR": "me03",
            "por": "me03"
        }


    def empty_result(self, metadata):

        return {
            "found": False,
            "source": None,
            "tcgdex_id": None,
            "name": None,
            "set_name": metadata.get("set"),
            "set_id": None,
            "code": metadata.get("code"),
            "number": metadata.get("number"),
            "rarity": None,
            "image": None,
            "price": None,
        }


    def resolve_set_id(self, code):

        if not code:
            return None

        return self.set_mapping.get(
            str(code).strip()
        )


    def build_tcgdex_id(self, metadata):

        set_id = self.resolve_set_id(
            metadata.get("code")
        )

        number = metadata.get("number")

        if not set_id or not number:
            return None

        # Keep TCGdex three digit localId format
        local_id = str(number).split("/")[0]
        local_id = local_id.zfill(3)

        return f"{set_id}-{local_id}"


    def resolve(self, metadata):

        result = self.empty_result(
            metadata
        )

        if metadata.get("family") != "Pokemon":
            return result


        tcgdex_id = self.build_tcgdex_id(
            metadata
        )

        if not tcgdex_id:
            return result


        card = self.tcgdex.get_card(
            tcgdex_id,
            metadata.get("language", "en").lower()
        )


        if not card:
            return result


        info = self.tcgdex.get_card_info(
            card
        )


        result["found"] = True
        result["source"] = "tcgdex"
        result["tcgdex_id"] = tcgdex_id
        result["name"] = info.get("name")
        result["set_name"] = info.get("set")
        result["set_id"] = tcgdex_id.split("-")[0]
        result["number"] = info.get("number")
        result["rarity"] = info.get("rarity")
        result["image"] = info.get("image")

        return result
