# ============================================================
# ABS TCGdex ZH-TW IMAGE BUILDER v1.0
#
# Buduje bazę obrazów chińskich kart:
# - czyta database/master_cards_zh.json
# - pobiera dane z TCGdex zh-tw
# - zapisuje obrazy:
#   D:\ABS_DATA\POKEMON\TCG\ZH-TW
#
# Tworzy:
# - database/image_index_zh.json
# - database/missing_images_zh.json
# - database/image_builder_zh_log.json
#
# Nie dotyka EN
# ============================================================


import argparse
import json
import os
import time
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

MASTER = Path("database/master_cards_zh.json")

INDEX = Path("database/image_index_zh.json")

MISSING = Path("database/missing_images_zh.json")

LOG = Path("database/image_builder_zh_log.json")


IMAGE_ROOT = Path("D:/ABS_DATA/POKEMON/TCG/ZH-TW")


LANGUAGE = "zh-tw"


class TCGdexZHImageBuilder:

    def __init__(self, start=0, limit=500, workers=16):

        self.start = start
        self.limit = limit
        self.workers = workers

        self.index = {}
        self.missing = []
        self.stats = {"downloaded": 0, "skipped": 0, "missing": 0}

    def load_json(self, path):

        if not path.exists():

            return {}

        with open(path, "r", encoding="utf-8") as f:

            return json.load(f)

    def save_json(self, path, data):

        temp = path.with_suffix(path.suffix + ".tmp")

        with open(temp, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=4, ensure_ascii=False)

        temp.replace(path)

    def safe_name(self, value):

        if not value:

            return "unknown"

        value = str(value)

        for c in '<>:"/\\|?*':

            value = value.replace(c, "_")

        return value.strip()

    def get_card_data(self, card_id):

        try:

            url = f"https://api.tcgdex.net/v2/" f"{LANGUAGE}/cards/{card_id}"

            r = requests.get(url, timeout=30)

            if r.status_code != 200:

                return None

            return r.json()

        except Exception:

            return None

    def download_image(
        self,
        card,
    ):

        card_id = card.get("id")

        data = self.get_card_data(card_id)

        if not data:

            return (card_id, None)

        image = data.get("image")

        if not image:

            return (card_id, None)

        if not image.endswith(".png"):

            image += "/high.png"

        set_id = card.get("set", {}).get("id", "unknown")

        folder = IMAGE_ROOT / self.safe_name(set_id)

        folder.mkdir(parents=True, exist_ok=True)

        filename = folder / f"{card_id}.png"

        if filename.exists():

            return (card_id, filename)

        try:

            r = requests.get(image, timeout=60)

            if r.status_code != 200:

                return (card_id, None)

            with open(filename, "wb") as f:

                f.write(r.content)

            return (card_id, filename)

        except Exception:

            return (card_id, None)

    def build(self):

        print("=" * 60)
        print("ABS TCGdex ZH-TW IMAGE BUILDER v1.0")
        print("=" * 60)

        cards = self.load_json(MASTER)

        total_cards = len(cards)

        selected = cards[self.start : self.start + self.limit]

        print(
            f"start={self.start} "
            f"limit={self.limit} "
            f"cards={len(selected)} "
            f"workers={self.workers}"
        )

        print("database=", IMAGE_ROOT)

        with ThreadPoolExecutor(max_workers=self.workers) as executor:

            futures = {
                executor.submit(self.download_image, card): card for card in selected
            }

            for i, future in enumerate(as_completed(futures), start=1):

                card = futures[future]

                card_id, path = future.result()

                if path:

                    self.stats["downloaded"] += 1

                    relative = str(path.relative_to(IMAGE_ROOT)).replace("\\", "/")

                    self.index[card_id] = {
                        "id": card_id,
                        "set": card.get("set"),
                        "name": card.get("name"),
                        "language": "ZH-TW",
                        "image": relative,
                    }

                    print(f"[{i}/{len(selected)}] " f"{card_id} DOWNLOADED")

                else:

                    self.stats["missing"] += 1

                    self.missing.append(card_id)

                    print(f"[{i}/{len(selected)}] " f"{card_id} MISSING")

        old_index = self.load_json(INDEX)

        old_index.update(self.index)

        self.save_json(INDEX, old_index)

        old_missing = self.load_json(MISSING)

        missing = list(set(old_missing + self.missing))

        self.save_json(MISSING, missing)

        self.save_json(LOG, self.stats)

        print()
        print("=" * 60)
        print("BUILD COMPLETE")
        print("=" * 60)

        print(self.stats)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--start", type=int, default=0)

    parser.add_argument("--limit", type=int, default=500)

    parser.add_argument("--workers", type=int, default=16)

    args = parser.parse_args()

    builder = TCGdexZHImageBuilder(args.start, args.limit, args.workers)

    builder.build()
