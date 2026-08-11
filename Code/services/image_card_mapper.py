# ABS IMAGE CARD MAPPER v1.0
# Converts image filename to TCGdex card id


class ImageCardMapper:

    def normalize(self, filename):

        if not filename:
            return None

        name = filename

        if "." in name:
            name = name.rsplit(".", 1)[0]

        return name


    def map_result(self, matcher_result):

        if not matcher_result:
            return None

        card_file = matcher_result.get("card")

        return {
            "card_id": self.normalize(card_file),
            "image": card_file,
            "score": matcher_result.get("score", 0)
        }
