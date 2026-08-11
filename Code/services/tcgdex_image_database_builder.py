# ABS TCGDEX IMAGE DATABASE BUILDER v1.0
# Builds local reference image database from TCGdex

import os
import requests


class TCGdexImageDatabaseBuilder:

    def __init__(self):

        self.base_url = "https://api.tcgdex.net/v2"
        self.output = "database/images/tcgdex"

        os.makedirs(
            self.output,
            exist_ok=True
        )


    def download_card_image(self, tcgdex_id):

        try:

            parts = tcgdex_id.split("-")

            if len(parts) != 2:
                return {
                    "success": False,
                    "id": tcgdex_id,
                    "message": "Invalid TCGdex id"
                }


            set_id = parts[0]
            number = parts[1]


            url = (
                f"{self.base_url}/en/cards/{tcgdex_id}"
            )

            response = requests.get(
                url,
                timeout=30
            )


            if response.status_code != 200:

                return {
                    "success": False,
                    "id": tcgdex_id,
                    "message": "Card not found"
                }


            card = response.json()

            image = card.get("image")


            if not image:

                return {
                    "success": False,
                    "id": tcgdex_id,
                    "message": "No image"
                }


            image_url = image + "/high.png"


            img = requests.get(
                image_url,
                timeout=30
            )


            if img.status_code != 200:

                return {
                    "success": False,
                    "id": tcgdex_id,
                    "message": "Image download failed"
                }


            path = os.path.join(
                self.output,
                f"{tcgdex_id}.png"
            )


            with open(path, "wb") as file:

                file.write(
                    img.content
                )


            return {
                "success": True,
                "id": tcgdex_id,
                "file": path
            }


        except Exception as e:

            return {
                "success": False,
                "id": tcgdex_id,
                "message": str(e)
            }


    def build_test_database(self):

        cards = [
            "base1-1",
            "base1-2",
            "base1-3",
            "base1-4",
            "me03-035"
        ]


        results = []


        for card in cards:

            print(
                "DOWNLOAD:",
                card
            )

            result = self.download_card_image(
                card
            )

            print(result)

            results.append(result)


        return results
