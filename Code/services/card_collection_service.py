import json
from pathlib import Path

from services.card_family_service import CardFamilyService


class CardCollectionService:

    def __init__(self):

        self.index_file = Path("scans/archive/index.json")

        self.family_service = CardFamilyService()

    def load_index(self):

        if not self.index_file.exists():

            return []

        with open(self.index_file, "r", encoding="utf-8") as file:

            return json.load(file)

    def save_index(self, data):

        with open(self.index_file, "w", encoding="utf-8") as file:

            json.dump(data, file, indent=4, ensure_ascii=False)

    def update_family(self, card_file):

        index = self.load_index()

        filename = Path(card_file).name

        result = self.family_service.analyze_card(card_file)

        updated = False

        for card in index:

            if card["file"] == filename:

                card["family"] = result["family"]

                card["family_confidence"] = result["family_confidence"]

                card["family_signals"] = result["family_signals"]

                updated = True

        if updated:

            self.save_index(index)

        return {
            "updated": updated,
            "file": filename,
            "family": result["family"],
            "confidence": result["family_confidence"],
        }
