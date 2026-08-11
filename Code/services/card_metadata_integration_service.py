# ABS CARD METADATA INTEGRATION SERVICE v1.3
# OCR -> Normalizer -> Online Resolver -> index update

import json
from pathlib import Path

from services.card_metadata_service import CardMetadataService
from services.card_online_resolver import CardOnlineResolver
from services.card_metadata_normalizer import CardMetadataNormalizer


class CardMetadataIntegrationService:

    def __init__(self):

        self.index_file = Path(
            "scans/archive/index.json"
        )

        self.metadata_service = CardMetadataService()
        self.normalizer = CardMetadataNormalizer()
        self.online_resolver = CardOnlineResolver()


    def load_index(self):

        if not self.index_file.exists():
            return []

        with open(
            self.index_file,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)


    def save_index(self, data):

        with open(
            self.index_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )


    def build_online_metadata(self, metadata):

        set_code = metadata.get("set_raw")

        return {
            "family": "Pokemon",
            "name": metadata.get("name"),
            "set": set_code,
            "code": set_code,
            "number": metadata.get("number_raw"),
            "language": metadata.get("language", "EN")
        }


    def update_metadata(self, image_path):

        index = self.load_index()

        filename = Path(image_path).name

        metadata = self.metadata_service.analyze(
            image_path
        )

        metadata = self.normalizer.normalize(
            metadata
        )

        online_metadata = self.build_online_metadata(
            metadata
        )

        online_result = self.online_resolver.resolve(
            online_metadata
        )

        updated = False

        for card in index:

            if card["file"] == filename:

                card["set"] = online_result.get(
                    "set",
                    metadata.get("set_raw")
                )

                card["number"] = online_result.get(
                    "number",
                    metadata.get("number_raw")
                )

                card["name"] = online_result.get(
                    "name"
                )

                card["rarity"] = online_result.get(
                    "rarity",
                    metadata.get("rarity_raw")
                )

                card["image"] = online_result.get(
                    "image"
                )

                card["source"] = online_result.get(
                    "source"
                )

                updated = True


        if updated:
            self.save_index(index)


        return {
            "updated": updated,
            "file": filename,
            "metadata": metadata,
            "online": online_result
        }
