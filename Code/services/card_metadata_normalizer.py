# ABS CARD METADATA NORMALIZER v1.0
# Fixes common OCR errors before online search


class CardMetadataNormalizer:


    def __init__(self):

        self.set_corrections = {
            "3508S": "POR",
            "3508s": "POR",
            "350BS": "POR",
            "P0R": "POR",
            "por": "POR"
        }


    def normalize_set(self, value):

        if not value:
            return value

        clean = str(value).strip()

        if clean in self.set_corrections:
            return self.set_corrections[clean]

        return clean


    def normalize_number(self, value):

        if not value:
            return value

        value = str(value).strip()

        if "/" in value:

            left, right = value.split("/", 1)

            left = left.zfill(3)
            right = right.zfill(3)

            return f"{left}/{right}"

        return value


    def normalize(self, metadata):

        result = dict(metadata)

        result["set_raw"] = self.normalize_set(
            metadata.get("set_raw")
        )

        result["number_raw"] = self.normalize_number(
            metadata.get("number_raw")
        )

        return result
