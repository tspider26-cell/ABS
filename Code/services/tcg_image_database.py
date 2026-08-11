import os
import requests
from config.settings import IMAGE_DATABASE


class TCGImageDatabase:

    def __init__(self):

        self.folder = IMAGE_DATABASE

    def download_card_image(self, card_id, image_url):

        try:

            if not image_url:

                print("BRAK URL OBRAZU")

                return None

            os.makedirs(self.folder, exist_ok=True)

            url = image_url

            if not url.endswith(".png"):

                url += "/high.png"

            response = requests.get(url, timeout=30)

            if response.status_code != 200:

                print("BŁĄD OBRAZU:", response.status_code)

                return None

            filename = f"{card_id}.png"

            path = os.path.join(self.folder, filename)

            with open(path, "wb") as file:

                file.write(response.content)

            print("ZAPISANO OBRAZ:", path)

            return path

        except Exception as e:

            print("BŁĄD:", e)

            return None
