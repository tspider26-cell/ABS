import json
import time
from pathlib import Path
from config.settings import IMAGE_DATABASE

import requests


class TCGdexFullImageBuilder:

    API = "https://api.tcgdex.net/v2"

    MASTER = Path("database/master_cards.json")
    ("database/images/tcgdex")
    IMAGE_DIR = IMAGE_DATABASE
    LOG = Path("database/full_image_builder_log.json")
    MISSING = Path("database/missing_images.json")
    INDEX = Path("database/image_index.json")

    def __init__(self, limit=500, delay=0.15):

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

    def get_image(self, card_id):

        url = f"{self.API}/en/cards/{card_id}"

        r = requests.get(url, timeout=30)

        if r.status_code != 200:
            return None

        data = r.json()

        image = data.get("image")

        if not image:
            return None

        return image + "/high.png"

    def download(self, card):

        card_id = card["id"]

        target = self.IMAGE_DIR / (card_id + ".png")

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

        if self.limit:

            cards = cards[: self.limit]

        index = self.load_json(self.INDEX)

        missing = []

        stats = {"total": len(cards), "downloaded": 0, "skipped": 0, "missing": 0}

        print("=" * 40)
        print("ABS TCGDEX FULL IMAGE BUILDER v1.0")
        print("=" * 40)

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

            index[card["id"]] = {
                "name": card.get("name"),
                "set": card.get("set"),
                "number": card.get("number"),
                "image": card["id"] + ".png",
            }

            time.sleep(self.delay)

        self.save_json(self.INDEX, index)

        self.save_json(self.MISSING, missing)

        self.save_json(self.LOG, stats)

        print()
        print(stats)

        return stats
