# ABS TCGdex Sync v1.1
# Prepares TCGdex source structure for ABS

from pathlib import Path
import json


class TCGdexSync:

    def __init__(
        self,
        source_folder="database/sources/tcgdex",
        output="database/sources/tcgdex/cards.json"
    ):

        self.source_folder = Path(source_folder)
        self.output = Path(output)


    def scan_source(self):

        cards = []

        if not self.source_folder.exists():
            return {
                "found": 0,
                "cards": []
            }


        for file in self.source_folder.rglob("*.json"):

            try:

                with open(
                    file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    data = json.load(f)


                if isinstance(data, dict) and "name" in data:

                    cards.append(data)

            except Exception:
                pass


        return {
            "found": len(cards),
            "cards": cards
        }


    def build_cards_file(self):

        result = self.scan_source()

        self.output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.output,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                result["cards"],
                f,
                indent=4,
                ensure_ascii=False
            )


        return {
            "synced": True,
            "cards_found": result["found"],
            "file": str(self.output)
        }
