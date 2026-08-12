# ABS TCGdex Full Image Builder v5.0
#
# Pobieranie kart TCGdex z równoległymi workerami.
# Zachowuje strukturę:
# D:/ABS_DATA/POKEMON/TCG/EN/<set_id>_<set_name>/<card_id>.png
#
# Uruchomienie:
# python -m services.tcgdex_full_image_builder --start 0 --limit 100 --workers 16

import argparse
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
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

    def __init__(self, start=0, limit=500, workers=16):

        self.start = start
        self.limit = limit
        self.workers = max(1, workers)

        self.IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # JSON
    # ---------------------------------------------------------

    def load_json(self, path):

        if not path.exists():
            return {}

        try:

            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception:

            return {}

        def save_json(self, path, data):

            path.parent.mkdir(parents=True, exist_ok=True)

        try:

            with open(path, "w", encoding="utf-8") as f:

                json.dump(data, f, indent=4, ensure_ascii=False)

        except PermissionError:

            print(f"[WARN] Cannot save {path}")

    # ---------------------------------------------------------
    # SAFE FOLDER NAME
    # ---------------------------------------------------------

    def safe_name(self, value):

        if value is None:
            return "Unknown"

        value = str(value).strip()

        value = re.sub(r'[<>:"/\\|?*]', "_", value)

        value = value.rstrip(". ")

        if not value:
            return "Unknown"

        return value

    # ---------------------------------------------------------
    # SET FOLDER
    # ---------------------------------------------------------

    def get_set_folder(self, card):

        card_set = card.get("set") or {}

        set_id = card_set.get("id") or "unknown"

        set_name = card_set.get("name") or "Unknown"

        set_id = self.safe_name(set_id)

        set_name = self.safe_name(set_name)

        folder_name = f"{set_id}_{set_name}"

        folder = self.IMAGE_DIR / folder_name

        folder.mkdir(parents=True, exist_ok=True)

        return folder, folder_name

    # ---------------------------------------------------------
    # GET IMAGE URL
    # ---------------------------------------------------------

    def get_image(self, card_id):

        url = f"{self.API}/en/cards/{card_id}"

        try:

            response = requests.get(url, timeout=30)

            if response.status_code != 200:
                return None

            data = response.json()

            image = data.get("image")

            if not image:
                return None

            return image.rstrip("/") + "/high.png"

        except Exception:

            return None

    # ---------------------------------------------------------
    # DOWNLOAD ONE CARD
    # ---------------------------------------------------------

    def download(self, card):

        card_id = card["id"]

        folder, relative_folder = self.get_set_folder(card)

        target = folder / f"{card_id}.png"

        relative_image = f"{relative_folder}/{card_id}.png"

        # Existing image
        if target.exists():

            return {
                "status": "SKIP",
                "card": card,
                "image": relative_image,
            }

        image_url = self.get_image(card_id)

        if not image_url:

            return {
                "status": "MISSING",
                "card": card,
                "image": relative_image,
            }

        try:

            response = requests.get(image_url, timeout=30)

            if response.status_code != 200:

                return {
                    "status": "MISSING",
                    "card": card,
                    "image": relative_image,
                }

            if not response.content:

                return {
                    "status": "MISSING",
                    "card": card,
                    "image": relative_image,
                }

            # Temporary file prevents partially written PNGs
            temp_target = target.with_suffix(".tmp")

            with open(temp_target, "wb") as f:

                f.write(response.content)

            temp_target.replace(target)

            return {
                "status": "DOWNLOADED",
                "card": card,
                "image": relative_image,
            }

        except Exception:

            return {
                "status": "MISSING",
                "card": card,
                "image": relative_image,
            }

    # ---------------------------------------------------------
    # BUILD
    # ---------------------------------------------------------

    def build(self):

        cards = self.load_json(self.MASTER)

        if not isinstance(cards, list):

            raise RuntimeError(
                "database/master_cards.json does not contain a card list."
            )

        selected_cards = cards[self.start : self.start + self.limit]

        index = self.load_json(self.INDEX)

        if not isinstance(index, dict):

            index = {}

        missing = []

        stats = {
            "start": self.start,
            "total": len(selected_cards),
            "downloaded": 0,
            "skipped": 0,
            "missing": 0,
        }

        print("=" * 60)
        print("ABS TCGdex Full Image Builder v5.0")
        print("=" * 60)

        print(
            f"start={self.start} "
            f"limit={self.limit} "
            f"cards={len(selected_cards)} "
            f"workers={self.workers}"
        )

        print(f"image_database={self.IMAGE_DIR}")

        print()

        completed = 0

        # -----------------------------------------------------
        # PARALLEL DOWNLOAD
        # -----------------------------------------------------

        with ThreadPoolExecutor(max_workers=self.workers) as executor:

            futures = {
                executor.submit(self.download, card): card for card in selected_cards
            }

            for future in as_completed(futures):

                card = futures[future]

                try:

                    result = future.result()

                except Exception as exc:

                    result = {
                        "status": "MISSING",
                        "card": card,
                        "image": None,
                    }

                    print(f"[ERROR] {card['id']} {exc}")

                status = result["status"]

                if status == "DOWNLOADED":

                    stats["downloaded"] += 1

                elif status == "SKIP":

                    stats["skipped"] += 1

                else:

                    stats["missing"] += 1

                    missing.append(card["id"])

                # -------------------------------------------------
                # INDEX
                # -------------------------------------------------

                index[card["id"]] = {
                    "name": card.get("name"),
                    "set": card.get("set"),
                    "number": card.get("number"),
                    "image": result["image"],
                }

                completed += 1

                print(
                    f"[{completed}/{len(selected_cards)}] " f"{card['id']} " f"{status}"
                )

                # -------------------------------------------------
                # PROGRESS
                # -------------------------------------------------

                progress = {
                    "start": self.start,
                    "limit": self.limit,
                    "processed": completed,
                    "workers": self.workers,
                }

                if completed % 10 == 0 or completed == len(selected_cards):

                    self.save_json(self.PROGRESS, progress)

        # ---------------------------------------------------------
        # FINAL SAVE
        # ---------------------------------------------------------

        self.save_json(self.INDEX, index)

        self.save_json(self.MISSING, missing)

        self.save_json(self.LOG, stats)

        print()
        print("=" * 60)
        print("BUILD COMPLETE")
        print("=" * 60)

        print(stats)

        return stats


# -------------------------------------------------------------
# COMMAND LINE
# -------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="ABS TCGdex Full Image Builder v5.0")

    parser.add_argument("--start", type=int, default=0)

    parser.add_argument("--limit", type=int, default=500)

    parser.add_argument("--workers", type=int, default=16)

    args = parser.parse_args()

    builder = TCGdexFullImageBuilder(
        start=args.start, limit=args.limit, workers=args.workers
    )

    builder.build()
