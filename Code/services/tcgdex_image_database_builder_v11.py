# ABS TCGDEX IMAGE DATABASE BUILDER v1.1

import json
import os
import time
from pathlib import Path
from config.settings import IMAGE_DATABASE

import requests


class TCGdexImageDatabaseBuilderV11:
    API_BASE = "https://api.tcgdex.net/v2"
    MASTER_DATABASE = Path("database/master_cards.json")
    IMAGE_DIR = IMAGE_DATABASE
    INDEX_FILE = Path("database/image_index.json")
    LOG_FILE = Path("database/image_builder_log.json")

    def __init__(self, batch_size=100, timeout=30, delay=0.0):
        self.batch_size = batch_size
        self.timeout = timeout
        self.delay = delay
        self.IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    def load_cards(self):
        with self.MASTER_DATABASE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("master_cards.json must contain a list")

        return data

    def load_index(self):
        if not self.INDEX_FILE.exists():
            return {}

        try:
            with self.INDEX_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError):
            return {}

    def save_json(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix(path.suffix + ".tmp")

        with temp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        temp.replace(path)

    def get_card_image_url(self, tcgdex_id):
        url = f"{self.API_BASE}/en/cards/{tcgdex_id}"
        response = requests.get(url, timeout=self.timeout)

        if response.status_code != 200:
            return None, f"card_http_{response.status_code}"

        card = response.json()
        image = card.get("image")

        if not image:
            return None, "no_image"

        return image.rstrip("/") + "/high.png", None

    def download_image(self, tcgdex_id):
        image_path = self.IMAGE_DIR / f"{tcgdex_id}.png"

        if image_path.exists() and image_path.stat().st_size > 0:
            return {"status": "skipped", "id": tcgdex_id, "file": str(image_path)}

        image_url, error = self.get_card_image_url(tcgdex_id)

        if error:
            return {"status": "failed", "id": tcgdex_id, "error": error}

        try:
            response = requests.get(image_url, timeout=self.timeout)

            if response.status_code != 200:
                return {
                    "status": "failed",
                    "id": tcgdex_id,
                    "error": f"image_http_{response.status_code}",
                }

            content_type = response.headers.get("Content-Type", "")
            if not response.content or (
                "image" not in content_type.lower()
                and not image_url.lower().endswith(".png")
            ):
                return {
                    "status": "failed",
                    "id": tcgdex_id,
                    "error": "invalid_image_response",
                }

            with image_path.open("wb") as f:
                f.write(response.content)

            return {
                "status": "downloaded",
                "id": tcgdex_id,
                "file": str(image_path),
                "bytes": len(response.content),
            }

        except requests.RequestException as exc:
            return {"status": "failed", "id": tcgdex_id, "error": str(exc)}

    def build(self):
        cards = self.load_cards()
        index = self.load_index()

        batch = cards[: self.batch_size]

        stats = {
            "total_requested": len(batch),
            "downloaded": 0,
            "skipped": 0,
            "failed": 0,
        }

        failures = []
        processed = []

        print("=" * 40)
        print("ABS TCGDEX IMAGE DATABASE BUILDER v1.1")
        print("=" * 40)
        print(f"TOTAL MASTER CARDS: {len(cards)}")
        print(f"TEST BATCH: {len(batch)}")
        print()

        for position, card in enumerate(batch, 1):
            tcgdex_id = card.get("id")

            if not tcgdex_id:
                stats["failed"] += 1
                failures.append({"position": position, "error": "missing_card_id"})
                print(f"[{position}/{len(batch)}] FAILED: missing id")
                continue

            result = self.download_image(tcgdex_id)
            status = result["status"]

            if status == "downloaded":
                stats["downloaded"] += 1
            elif status == "skipped":
                stats["skipped"] += 1
            else:
                stats["failed"] += 1
                failures.append(result)

            index[tcgdex_id] = {
                "image": f"{tcgdex_id}.png",
                "name": card.get("name"),
                "set": card.get("set", {}),
                "number": card.get("number"),
                "source": "tcgdex",
            }

            processed.append(tcgdex_id)

            print(f"[{position}/{len(batch)}] " f"{tcgdex_id}: {status.upper()}")

            if self.delay:
                time.sleep(self.delay)

        log = {
            "builder": "ABS TCGDEX IMAGE DATABASE BUILDER v1.1",
            "batch_size": self.batch_size,
            "master_total": len(cards),
            "processed_ids": processed,
            "stats": stats,
            "failures": failures,
        }

        self.save_json(self.INDEX_FILE, index)
        self.save_json(self.LOG_FILE, log)

        print()
        print("DOWNLOADED:", stats["downloaded"])
        print("SKIPPED:", stats["skipped"])
        print("FAILED:", stats["failed"])
        print("INDEX:", self.INDEX_FILE)
        print("LOG:", self.LOG_FILE)
        print("=" * 40)

        return log


if __name__ == "__main__":
    TCGdexImageDatabaseBuilderV11(batch_size=100).build()
