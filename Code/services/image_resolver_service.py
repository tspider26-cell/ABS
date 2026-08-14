from pathlib import Path
import json


class ImageResolverService:

    def __init__(
        self, index_file=r"D:\PTCG_FULL_DATABASE\database\image_master_index.json"
    ):

        self.index_file = Path(index_file)

        with open(self.index_file, "r", encoding="utf-8") as f:

            self.database = json.load(f)

        self.cards = self.database.get("cards", {})

    def find_card(self, card_key):

        return self.cards.get(card_key, [])

    def get_best_images(self, card_key, limit=5):

        images = self.find_card(card_key)

        if not images:
            return []

        # priorytet jakości

        priority = {"original": 0, "reference": 1, "backup": 2, "unknown": 3}

        images = sorted(images, key=lambda x: priority.get(x.get("quality"), 9))

        return images[:limit]

    def statistics(self):

        return {
            "cards": len(self.cards),
            "images": self.database.get("statistics", {}).get("total_images", 0),
        }
