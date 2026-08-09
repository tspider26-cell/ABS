import json
import os
import requests


class PokemonDataDownloader:

    def __init__(self):

        self.folder = "database"

        self.sources = {"en": "", "ja": "", "zh": ""}

    def download_language(self, language):

        try:

            url = self.sources.get(language)

            if not url:

                print("BRAK ŹRÓDŁA DLA:", language)

                return False

            os.makedirs(self.folder, exist_ok=True)

            response = requests.get(url, timeout=120)

            if response.status_code != 200:

                print("BŁĄD:", language, response.status_code)

                return False

            cards = response.json()

            file = f"{self.folder}/" f"pokemon_cards_{language}.json"

            with open(file, "w", encoding="utf-8") as f:

                json.dump(cards, f, ensure_ascii=False)

            print("POBRANO:", language, len(cards))

            print("ZAPISANO:", file)

            return True

        except Exception as e:

            print("BŁĄD:", e)

            return False
