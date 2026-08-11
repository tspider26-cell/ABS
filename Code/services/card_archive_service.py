import json
import shutil
from pathlib import Path
from datetime import datetime


class CardArchiveService:

    def __init__(self):

        self.archive_dir = Path("scans/archive")

        self.index_file = self.archive_dir / "index.json"

        self.archive_dir.mkdir(parents=True, exist_ok=True)

    def load_index(self):

        if not self.index_file.exists():
            return []

        with open(self.index_file, "r", encoding="utf-8") as file:

            return json.load(file)

    def save_index(self, data):

        with open(self.index_file, "w", encoding="utf-8") as file:

            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_next_id(self):

        index = self.load_index()

        if not index:
            return 1

        return max(item["id"] for item in index) + 1

    def create_card_record(self, card_id, filename):

        return {
            "id": card_id,
            "file": filename,
            "family": None,
            "game": None,
            "set": None,
            "number": None,
            "rarity": None,
            "variant": None,
            "quantity": 1,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "camera",
        }

    def archive_card(self, source_file):

        source = Path(source_file)

        if not source.exists():
            return None

        card_id = self.get_next_id()

        filename = f"card_{card_id:04}.jpg"

        destination = self.archive_dir / filename

        shutil.copy2(source, destination)

        index = self.load_index()

        record = self.create_card_record(card_id, filename)

        index.append(record)

        self.save_index(index)

        return destination
