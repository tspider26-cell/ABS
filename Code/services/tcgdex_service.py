import os
import requests


class TCGdexService:

    def __init__(self):

        self.base_url = "https://api.tcgdex.net/v2"

    def get_card(self, card_id, language="en"):

        try:

            url = f"{self.base_url}/" f"{language}/cards/{card_id}"

            response = requests.get(url, timeout=30)

            print("TCGDEX:", response.status_code)

            if response.status_code != 200:

                print(response.text)

                return None

            return response.json()

        except Exception as e:

            print("BŁĄD TCGDEX:", e)

            return None

    def get_card_info(self, card):

        if card is None:

            return None

        return {
            "id": card.get("id"),
            "name": card.get("name"),
            "number": card.get("localId"),
            "rarity": card.get("rarity"),
            "set": card.get("set", {}).get("name"),
            "image": card.get("image"),
        }

    def download_image(self, image_url, filename):

        try:

            if not image_url:

                print("BRAK OBRAZU")

                return None

            if not image_url.endswith(".png"):

                image_url += "/high.png"

            folder = "database/images"

            os.makedirs(folder, exist_ok=True)

            path = os.path.join(folder, filename)

            response = requests.get(image_url, timeout=30)

            print("IMAGE STATUS:", response.status_code)

            if response.status_code != 200:

                print("BŁĄD OBRAZU:", response.text[:200])

                return None

            with open(path, "wb") as file:

                file.write(response.content)

            print("ZAPISANO:", path)

            return path

        except Exception as e:

            print("BŁĄD OBRAZU:", e)

            return None
