import os
import json
import shutil


class CardProfileService:

    def __init__(self, database="database/cards"):

        self.database = database

        os.makedirs(self.database, exist_ok=True)

    def create_profile(self, card_id, image_path):

        folder = os.path.join(self.database, card_id)

        images = os.path.join(folder, "images")

        os.makedirs(images, exist_ok=True)

        target = os.path.join(images, "ref_01.jpg")

        shutil.copy(image_path, target)

        profile = {"id": card_id, "references": [{"image": target}]}

        with open(os.path.join(folder, "profile.json"), "w", encoding="utf-8") as f:

            json.dump(profile, f, indent=4)

        return profile
