import cv2
import os
import json
import hashlib


class FeatureExtractor:

    def __init__(self):

        self.orb = cv2.ORB_create(nfeatures=1000)

    def image_hash(self, path):

        with open(path, "rb") as file:

            data = file.read()

        return hashlib.md5(data).hexdigest()

    def extract(self, image_path):

        if not os.path.exists(image_path):

            return None

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:

            return None

        keypoints, descriptors = self.orb.detectAndCompute(image, None)

        card_id = os.path.splitext(os.path.basename(image_path))[0]

        return {
            "id": card_id,
            "image": image_path,
            "features": {
                "width": image.shape[1],
                "height": image.shape[0],
                "hash": self.image_hash(image_path),
                "orb_points": len(keypoints),
            },
        }

    def save_features(self, card_id, features):

        folder = "database/features"

        os.makedirs(folder, exist_ok=True)

        path = os.path.join(folder, card_id + ".json")

        with open(path, "w", encoding="utf-8") as file:

            json.dump(features, file, indent=4)

        print("ZAPISANO:", path)

        return path
