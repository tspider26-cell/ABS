import cv2
import os
import hashlib
import numpy as np


class HybridMatcher:

    def __init__(self):

        self.orb = cv2.ORB_create(nfeatures=2000)

        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING)

    # ===============================
    # HASH OBRAZU
    # ===============================

    def image_hash(self, path):

        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        if image is None:

            return None

        image = cv2.resize(image, (64, 64))

        return hashlib.md5(image.tobytes()).hexdigest()

    # ===============================
    # KOLOR
    # ===============================

    def color_score(self, img1, img2):

        a = cv2.imread(img1)

        b = cv2.imread(img2)

        if a is None or b is None:

            return 0

        a = cv2.resize(a, (100, 100))

        b = cv2.resize(b, (100, 100))

        diff = np.mean(cv2.absdiff(a, b))

        score = max(0, 100 - diff)

        return int(score)

    # ===============================
    # ORB
    # ===============================

    def orb_score(self, img1, img2):

        a = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)

        b = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)

        if a is None or b is None:

            return 0

        kp1, des1 = self.orb.detectAndCompute(a, None)

        kp2, des2 = self.orb.detectAndCompute(b, None)

        if des1 is None or des2 is None:

            return 0

        matches = self.bf.knnMatch(des1, des2, k=2)

        good = []

        for pair in matches:

            if len(pair) != 2:

                continue

            m, n = pair

            if m.distance < 0.78 * n.distance:

                good.append(m)

        return len(good)

    # ===============================
    # FINAL SCORE
    # ===============================

    def compare(self, source, target):

        orb = self.orb_score(source, target)

        color = self.color_score(source, target)

        hash_bonus = 0

        if self.image_hash(source) == self.image_hash(target):

            hash_bonus = 50

        final = orb * 3 + color * 0.4 + hash_bonus

        return int(final)

    # ===============================
    # SEARCH DATABASE
    # ===============================

    def find_best(self, image_path, database_folder):

        results = []

        for file in os.listdir(database_folder):

            if not file.lower().endswith((".png", ".jpg", ".jpeg")):

                continue

            path = os.path.join(database_folder, file)

            score = self.compare(image_path, path)

            results.append({"card": file, "score": score})

        results.sort(key=lambda x: x["score"], reverse=True)

        return results
