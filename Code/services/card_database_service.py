# ============================================================
# Pokémon TCG Database Service
# Pobieranie informacji i obrazów kart
# ============================================================

import os
import requests


class CardDatabaseService:

    def __init__(self):

        self.base_url = "https://api.pokemontcg.io/v2/cards"

    # ========================================================
    # WYSZUKIWANIE KARTY
    # ========================================================

    def search_card(self, name):

        try:

            params = {"q": f"name {name}"}

            response = requests.get(self.base_url, params=params, timeout=30)

            print("API URL:", response.url)
            print("API STATUS:", response.status_code)

            if response.status_code != 200:

                print("BŁĄD API:", response.text)

                return None

            data = response.json()

            cards = data.get("data", [])

            if not cards:

                print("NIE ZNALEZIONO:", name)

                return None

            return cards[0]

        except requests.exceptions.Timeout:

            print("API TIMEOUT - brak odpowiedzi serwera")

            return None

        except Exception as e:

            print("BŁĄD POŁĄCZENIA:", e)

            return None

    # ========================================================
    # DANE KARTY
    # ========================================================

    def get_card_info(self, card):

        if card is None:

            return None

        return {
            "id": card.get("id", ""),
            "name": card.get("name", ""),
            "set": card.get("set", {}).get("name", ""),
            "number": card.get("number", ""),
            "rarity": card.get("rarity", ""),
            "image": card.get("images", {}).get("large", ""),
        }

    # ========================================================
    # POBIERANIE OBRAZU
    # ========================================================

    def download_card_image(self, image_url, filename):

        try:

            if not image_url:

                print("BRAK OBRAZU")

                return None

            folder = "cards/images"

            os.makedirs(folder, exist_ok=True)

            path = os.path.join(folder, filename)

            response = requests.get(image_url, timeout=30)

            if response.status_code != 200:

                print("BŁĄD OBRAZU:", response.status_code)

                return None

            with open(path, "wb") as file:

                file.write(response.content)

            print("ZAPISANO:", path)

            return path

        except Exception as e:

            print("BŁĄD POBIERANIA:", e)

            return None
