# ABS JP IMAGE BUILDER v2.0
# Japanese Pokemon Card Image Downloader

import os
import json
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCE = r"C:\ABS\ptcg_database\data_jp"

OUTPUT = r"D:\ABS_DATA\POKEMON\TCG\JP"

CACHE_FILE = "database/jp_cards_cache.json"
INDEX_FILE = "database/image_index_jp.json"
MISSING_FILE = "database/missing_images_jp.json"


class JPImageBuilder:

    def __init__(self, start=0, limit=None, workers=8):

        self.start = start
        self.limit = limit
        self.workers = workers

        self.cards = []
        self.index = {}
        self.missing = []

        os.makedirs(OUTPUT, exist_ok=True)

    def load_cache(self):

        if not os.path.exists(CACHE_FILE):
            return False

        print("LOADING JP CACHE...")

        with open(CACHE_FILE, encoding="utf-8") as f:

            self.cards = json.load(f)

        print("CACHE CARDS:", len(self.cards))

        return True

    def build_cache(self):

        print("SCANNING JP DATABASE...")

        cards = []

        for root, dirs, files in os.walk(SOURCE):

            for file in files:

                if not file.endswith(".json"):
                    continue

                path = os.path.join(root, file)

                try:

                    with open(path, encoding="utf-8") as f:

                        data = json.load(f)

                    img = data.get("img")

                    if not img:
                        continue

                    set_name = os.path.basename(root)

                    number = str(data.get("number", ""))

                    card_id = set_name + "-" + number

                    cards.append(
                        {"id": card_id, "set": set_name, "number": number, "url": img}
                    )

                except Exception as e:

                    print("JSON ERROR:", path, e)

        self.cards = cards

        os.makedirs("database", exist_ok=True)

        with open(CACHE_FILE, "w", encoding="utf-8") as f:

            json.dump(cards, f, indent=4, ensure_ascii=False)

        print("CACHE CREATED:", len(cards))

    def load_cards(self):

        if not self.load_cache():

            self.build_cache()

    def download(self, card):

        folder = os.path.join(OUTPUT, card["set"])

        os.makedirs(folder, exist_ok=True)

        filename = card["set"] + "-" + card["number"] + ".jpg"

        path = os.path.join(folder, filename)

        if os.path.exists(path):

            return (card["id"], "SKIP", path)

        try:

            r = requests.get(card["url"], timeout=30)

            if r.status_code != 200:

                return (card["id"], "MISSING", None)

            with open(path, "wb") as f:

                f.write(r.content)

            return (card["id"], "DOWNLOADED", path)

        except Exception:

            return (card["id"], "ERROR", None)

    def save_database(self):

        os.makedirs("database", exist_ok=True)

        with open(INDEX_FILE, "w", encoding="utf-8") as f:

            json.dump(self.index, f, indent=4, ensure_ascii=False)

        with open(MISSING_FILE, "w", encoding="utf-8") as f:

            json.dump(self.missing, f, indent=4, ensure_ascii=False)

    def build(self):

        self.load_cards()

        cards = self.cards[self.start :]

        if self.limit:

            cards = cards[: self.limit]

        print("=" * 60)

        print("START:", self.start, "LIMIT:", len(cards), "WORKERS:", self.workers)

        with ThreadPoolExecutor(max_workers=self.workers) as executor:

            futures = [executor.submit(self.download, card) for card in cards]

            for i, future in enumerate(as_completed(futures), start=1):

                cid, status, path = future.result()

                print(f"[{i}/{len(cards)}]", cid, status)

                if path:

                    self.index[cid] = {
                        "image": path,
                        "language": "JP",
                        "source": "pokemon-card.com",
                    }

                else:

                    self.missing.append(cid)

        self.save_database()

        print("=" * 60)

        print("BUILD COMPLETE")

        print({"downloaded": len(self.index), "missing": len(self.missing)})


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--start", type=int, default=0)

    parser.add_argument("--limit", type=int, default=None)

    parser.add_argument("--workers", type=int, default=8)

    args = parser.parse_args()

    JPImageBuilder(args.start, args.limit, args.workers).build()
