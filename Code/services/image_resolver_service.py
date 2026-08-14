from pathlib import Path
import json


class ImageResolverService:

    def __init__(
        self,
        index_file=r"D:\PTCG_FULL_DATABASE\database\image_master_index_ranked_v2.json",
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

        images = sorted(images, key=lambda x: x.get("quality_score", 0), reverse=True)

        return images[:limit]

    def get_preferred_image(self, card_key):

        images = self.get_best_images(card_key, limit=1)

        if not images:
            return None

        return images[0]

    def statistics(self):

        total_images = 0

        for images in self.cards.values():
            total_images += len(images)

        return {
            "cards": len(self.cards),
            "images": total_images,
        }
