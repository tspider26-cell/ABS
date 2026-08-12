# ABS Traditional Chinese Image Builder v1.0
# Source: type-null/PTCG-database
# Images: pokemon-card.com Taiwan

import os
import json
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCE = r"C:\ABS\ptcg_database\data_tc"

OUTPUT = r"D:\ABS_DATA\POKEMON\TCG\ZH-TW"

INDEX_FILE = "database/image_index_zh.json"
MISSING_FILE = "database/missing_images_zh.json"


class TCImageBuilder:

    def __init__(self, start=0, limit=None, workers=8):

        self.start = start
        self.limit = limit
        self.workers = workers

        self.cards = []
        self.index = {}
        self.missing = []

        os.makedirs(OUTPUT, exist_ok=True)

    def load_cards(self):

        cards = []

        for root, dirs, files in os.walk(SOURCE):

            for file in files:

                if not file.endswith(".json"):
                    continue

                path = os.path.join(root, file)

                try:

                    with open(path, encoding="utf-8") as f:

                        data = json.load(f)

                    if data.get("img"):

                        set_id = os.path.basename(root).replace(".png", "").strip()

                        number = os.path.splitext(file)[0]

                        cards.append(
                            {
                                "id": f"{set_id}-{number}",
                                "set": set_id,
                                "number": number,
                                "image": data["img"],
                            }
                        )

                except Exception:

                    pass

        self.cards = cards

        print("CARDS FOUND:", len(cards))

    def safe_name(self, value):

        return value.replace("/", "_").replace("\\", "_")

    def download_card(self, card):

        card_id = card["id"]

        set_id = card["set"]

        number = card["number"]

        url = card["image"]

        folder = os.path.join(OUTPUT, set_id)

        os.makedirs(folder, exist_ok=True)

        filename = set_id + "-" + number + ".png"

        path = os.path.join(folder, filename)

        if os.path.exists(path):

            return (card_id, "SKIP", os.path.relpath(path, OUTPUT))

        try:

            r = requests.get(url, timeout=30)

            if r.status_code != 200:

                return (card_id, "MISSING", None)

            with open(path, "wb") as f:

                f.write(r.content)

            return (card_id, "DOWNLOADED", os.path.relpath(path, OUTPUT))

        except Exception:

            return (card_id, "ERROR", None)

    def build(self):

        self.load_cards()

        cards = self.cards[self.start :]

        if self.limit:

            cards = cards[: self.limit]

        print("=" * 60)

        print("START:", self.start, "LIMIT:", len(cards), "WORKERS:", self.workers)

        with ThreadPoolExecutor(max_workers=self.workers) as executor:

            futures = [executor.submit(self.download_card, c) for c in cards]

            for i, future in enumerate(as_completed(futures), start=1):

                card_id, status, path = future.result()

                print(f"[{i}/{len(cards)}]", card_id, status)

                if status in ("DOWNLOADED", "SKIP"):

                    self.index[card_id] = {
                        "image": path,
                        "language": "ZH-TW",
                        "source": "pokemon_asia",
                    }

                else:

                    self.missing.append(card_id)

        with open(INDEX_FILE, "w", encoding="utf-8") as f:

            json.dump(self.index, f, indent=4, ensure_ascii=False)

        with open(MISSING_FILE, "w", encoding="utf-8") as f:

            json.dump(self.missing, f, indent=4, ensure_ascii=False)

        print("=" * 60)

        print("BUILD COMPLETE")

        print({"downloaded": len(self.index), "missing": len(self.missing)})


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--start", type=int, default=0)

    parser.add_argument("--limit", type=int, default=None)

    parser.add_argument("--workers", type=int, default=8)

    args = parser.parse_args()

    builder = TCImageBuilder(start=args.start, limit=args.limit, workers=args.workers)

    builder.build()
