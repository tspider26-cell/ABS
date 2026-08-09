import cv2
import json
import os
import numpy as np


class FeatureMatcher:

    def __init__(self):

        self.orb = cv2.ORB_create(nfeatures=1000)

        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def load_features(self, path):

        with open(path, "r", encoding="utf-8") as file:

            return json.load(file)

    def extract_descriptors(self, image_path):

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:

            return None

        keypoints, descriptors = self.orb.detectAndCompute(image, None)

        return descriptors

    def compare(self, image_a, image_b):

        desc_a = self.extract_descriptors(image_a)

        desc_b = self.extract_descriptors(image_b)

        if desc_a is None or desc_b is None:

            return 0

        matches = self.matcher.match(desc_a, desc_b)

        if len(matches) == 0:

            return 0

        matches = sorted(matches, key=lambda x: x.distance)

        good = [m for m in matches if m.distance < 60]

        score = int(len(good) / len(matches) * 100)

        return score

    def find_best(self, query_image, database_folder):

        results = []

        for file in os.listdir(database_folder):

            if not file.endswith((".png", ".jpg", ".jpeg")):

                continue

            path = os.path.join(database_folder, file)

            score = self.compare(query_image, path)

            results.append({"card": file, "score": score})

        results.sort(key=lambda x: x["score"], reverse=True)

        return results
