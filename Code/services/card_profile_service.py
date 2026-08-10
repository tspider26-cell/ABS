import os
import json
import hashlib
import cv2


class CardProfileService:

    MAX_REFERENCES = 10

    def __init__(self, database="database/cards"):

        self.database = database

    def get_card_path(self, card_id):

        return os.path.join(self.database, card_id)

    def get_profile_path(self, card_id):

        return os.path.join(self.get_card_path(card_id), "profile.json")

    def load_profile(self, card_id):

        path = self.get_profile_path(card_id)

        if not os.path.exists(path):

            return {"id": card_id, "references": []}

        with open(path, "r", encoding="utf-8") as file:

            return json.load(file)

    def save_profile(self, profile):

        path = self.get_profile_path(profile["id"])

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as file:

            json.dump(profile, file, indent=4, ensure_ascii=False)

    def image_hash(self, image_path):

        with open(image_path, "rb") as file:

            return hashlib.md5(file.read()).hexdigest()

    def capture_reference(self, card_id, image_path):

        return self.add_reference(card_id, image_path)

    def add_reference(self, card_id, image_path):

        profile = self.load_profile(card_id)

        references = profile["references"]

        if len(references) >= self.MAX_REFERENCES:

            return {
                "status": "limit_reached",
                "message": "Osiągnięto maksymalną liczbę referencji",
                "total": len(references),
            }

        new_hash = self.image_hash(image_path)

        for ref in references:

            if self.image_hash(ref["image"]) == new_hash:

                return {
                    "status": "duplicate",
                    "message": "Ta referencja już istnieje",
                    "image": ref["image"],
                }

        images_dir = os.path.join(self.get_card_path(card_id), "images")

        os.makedirs(images_dir, exist_ok=True)

        number = len(references) + 1

        filename = f"ref_{number:02d}.jpg"

        destination = os.path.join(images_dir, filename)

        image = cv2.imread(image_path)

        if image is None:

            return {"status": "error", "message": "Nie można odczytać obrazu"}

        cv2.imwrite(destination, image)

        references.append({"image": destination})

        profile["references"] = references

        self.save_profile(profile)

        return {"status": "added", "reference": destination, "total": len(references)}
