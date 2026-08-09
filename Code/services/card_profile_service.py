import os
import json
import shutil
import hashlib


class CardProfileService:

    def __init__(self, database="database/cards"):

        self.database = database

        os.makedirs(self.database, exist_ok=True)

    def file_hash(self, path):

        with open(path, "rb") as f:

            return hashlib.md5(f.read()).hexdigest()

    def load_profile(self, card_id):

        profile_file = os.path.join(self.database, card_id, "profile.json")

        if not os.path.isfile(profile_file):

            return None

        with open(profile_file, "r", encoding="utf-8") as f:

            return json.load(f)

    def save_profile(self, card_id, profile):

        folder = os.path.join(self.database, card_id)

        with open(os.path.join(folder, "profile.json"), "w", encoding="utf-8") as f:

            json.dump(profile, f, indent=4)

    def capture_reference(self, card_id, source_image):

        profile = self.load_profile(card_id)

        if profile is None:

            raise Exception("Profil karty nie istnieje")

        new_hash = self.file_hash(source_image)

        for ref in profile["references"]:

            if os.path.exists(ref["image"]):

                if self.file_hash(ref["image"]) == new_hash:

                    return {
                        "status": "duplicate",
                        "message": "Ta referencja już istnieje",
                    }

        folder = os.path.join(self.database, card_id, "images")

        number = len(profile["references"]) + 1

        filename = f"ref_{number:02d}.jpg"

        target = os.path.join(folder, filename)

        shutil.copy(source_image, target)

        profile["references"].append({"image": target})

        self.save_profile(card_id, profile)

        return {
            "status": "added",
            "reference": target,
            "total": len(profile["references"]),
        }
