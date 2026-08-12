import json
import time
from pathlib import Path

import requests

from config.settings import IMAGE_DATABASE


class TCGdexFullImageBuilder:

    API = "https://api.tcgdex.net/v2"

    MASTER = Path("database/master_cards.json")

    IMAGE_DIR = IMAGE_DATABASE

    LOG = Path("database/full_image_builder_log.json")
    MISSING = Path("database/missing_images.json")
    INDEX = Path("database/image_index.json")
    PROGRESS = Path("database/image_builder_progress.json")

    def __init__(self, start=0, limit=500, delay=0.25):

        self.start = start
        self.limit = limit
        self.delay = delay

        self.IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    def load_json(self, path):

        if not path.exists():
            return {}

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_json(self, path, data):

        with open(path, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=4, ensure_ascii=False)

    def clean_name(self, name):

        chars = '<>:"/\\|?*'

        for c in chars:
            name = name.replace(c, "_")

        return name.replace(" ", "_")

    def get_storage_folder(self, card):

        set_data = card.get("set", {})

        set_id = set_data.get("id", "unknown")

        set_name = self.clean_name(set_data.get("name", "Unknown_Set"))

        folder = self.IMAGE_DIR / (f"{set_id}_{set_name}")

        folder.mkdir(parents=True, exist_ok=True)

        return folder

    def get_image(self, card_id):

        url = f"{self.API}/en/cards/{card_id}"

        try:

            r = requests.get(url, timeout=30)

            if r.status_code != 200:
                return None

            data = r.json()

            image = data.get("image")

            if not image:
                return None

            return image + "/high.png"

        except Exception:

            return None

    def download(self, card):

        card_id = card["id"]

        folder = self.get_storage_folder(card)

        target = folder / (card_id + ".png")

        if target.exists():

            return "SKIP"

        image_url = self.get_image(card_id)

        if not image_url:

            return "MISSING"

        try:

            img = requests.get(image_url, timeout=30)

            if img.status_code != 200:

                return "MISSING"

            with open(target, "wb") as f:

                f.write(img.content)

            return "DOWNLOADED"

        except Exception:

            return "MISSING"

    def build(self):

        cards = self.load_json(self.MASTER)

        cards = cards[self.start : self.start + self.limit]

        index = self.load_json(self.INDEX)

        progress = {"start": self.start, "limit": self.limit, "processed": 0}

        missing = []

        stats = {
            "start": self.start,
            "total": len(cards),
            "downloaded": 0,
            "skipped": 0,
            "missing": 0,
        }

        print("=" * 40)
        print("ABS TCGDEX FULL IMAGE BUILDER v4.1")
        print("=" * 40)

        print("START:", self.start)

        print("CARDS:", len(cards))

        for i, card in enumerate(cards, 1):

            result = self.download(card)

            print(f"[{i}/{len(cards)}]", card["id"], result)

            if result == "DOWNLOADED":

                stats["downloaded"] += 1

            elif result == "SKIP":

                stats["skipped"] += 1

            else:

                stats["missing"] += 1

                missing.append(card["id"])

            folder = self.get_storage_folder(card)

            relative_image = str(folder.name + "/" + card["id"] + ".png")

            index[card["id"]] = {
                "name": card.get("name"),
                "set": card.get("set"),
                "number": card.get("number"),
                "image": relative_image,
            }

            progress["processed"] = i

            self.save_json(self.PROGRESS, progress)

            time.sleep(self.delay)

        self.save_json(self.INDEX, index)

        self.save_json(self.MISSING, missing)

        self.save_json(self.LOG, stats)

        print()
        print(stats)

        return stats


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int, default=500)

    args = parser.parse_args()

    builder = TCGdexFullImageBuilder(start=args.start, limit=args.limit)

    builder.build()
