# ABS JP IMAGE BUILDER v2.1
# Japanese Pokemon Card Image Downloader
# Resume + Cache + Safe filenames


import os
import json
import argparse
import requests
import re

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

        os.makedirs("database", exist_ok=True)

        os.makedirs(OUTPUT, exist_ok=True)

    def safe_name(self, name):

        name = str(name)

        name = name.replace("/", "-")

        name = name.replace("\\", "-")

        name = re.sub(r'[<>:"|?*]', "-", name)

        name = name.replace("\xa0", "")

        return name.strip()

    def load_cache(self):

        if os.path.exists(CACHE_FILE):

            print("LOADING JP CACHE...")

            with open(CACHE_FILE, encoding="utf-8") as f:

                self.cards = json.load(f)

            print("CACHE CARDS:", len(self.cards))

            return True

        return False

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

                    url = data.get("img")

                    if not url:
                        continue

                    set_name = os.path.basename(root)

                    number = str(data.get("number", ""))

                    cards.append(
                        {
                            "id": f"JP-{data.get('jp_id')}",
                            "set": set_name,
                            "number": number,
                            "url": url,
                        }
                    )

                except Exception as e:

                    print("JSON ERROR:", path, e)

        self.cards = cards

        with open(CACHE_FILE, "w", encoding="utf-8") as f:

            json.dump(cards, f, indent=4, ensure_ascii=False)

        print("CACHE CREATED:", len(cards))

    def load_cards(self):

        if not self.load_cache():

            self.build_cache()

    def load_existing_database(self):

        if os.path.exists(INDEX_FILE):

            with open(INDEX_FILE, encoding="utf-8") as f:

                self.index = json.load(f)

            print("EXISTING INDEX:", len(self.index))

        if os.path.exists(MISSING_FILE):

            with open(MISSING_FILE, encoding="utf-8") as f:

                self.missing = json.load(f)

    def download(self, card):

        folder = os.path.join(OUTPUT, self.safe_name(card["set"]))

        os.makedirs(folder, exist_ok=True)

        filename = self.safe_name(card["id"]) + ".jpg"

        path = os.path.join(folder, filename)

        if os.path.isfile(path):

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

    def save(self):

        with open(INDEX_FILE, "w", encoding="utf-8") as f:

            json.dump(self.index, f, indent=4, ensure_ascii=False)

        with open(MISSING_FILE, "w", encoding="utf-8") as f:

            json.dump(list(set(self.missing)), f, indent=4, ensure_ascii=False)

    def build(self):

        self.load_cards()

        self.load_existing_database()

        cards = self.cards[self.start :]

        if self.limit:

            cards = cards[: self.limit]

        print("=" * 60)

        print("START:", self.start, "LIMIT:", len(cards), "WORKERS:", self.workers)

        with ThreadPoolExecutor(max_workers=self.workers) as executor:

            futures = [executor.submit(self.download, card) for card in cards]

            for i, f in enumerate(as_completed(futures), start=1):

                cid, status, path = f.result()

                print(f"[{i}/{len(cards)}]", cid, status)

                if path:

                    self.index[cid] = {
                        "image": path,
                        "language": "JP",
                        "source": "pokemon-card.com",
                    }

                else:

                    self.missing.append(cid)

        self.save()

        print("=" * 60)

        print("BUILD COMPLETE")

        print({"index": len(self.index), "missing": len(set(self.missing))})


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--start", type=int, default=0)

    parser.add_argument("--limit", type=int, default=None)

    parser.add_argument("--workers", type=int, default=8)

    args = parser.parse_args()

    JPImageBuilder(args.start, args.limit, args.workers).build()
