import cv2
import os
import numpy as np


class FeatureMatcherV21:

    def __init__(self):

        self.orb = cv2.ORB_create(nfeatures=2000)

        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING)

    def preprocess(self, image_path):

        image = cv2.imread(image_path)

        if image is None:

            return None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # poprawa światła

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

        enhanced = clahe.apply(gray)

        # lekka redukcja szumu

        enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)

        return enhanced

    def extract(self, image_path):

        image = self.preprocess(image_path)

        if image is None:

            return None, None

        kp, des = self.orb.detectAndCompute(image, None)

        return kp, des

    def compare(self, image1, image2):

        kp1, des1 = self.extract(image1)

        kp2, des2 = self.extract(image2)

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

        score = len(good)

        # geometria

        if len(good) >= 8:

            pts1 = np.float32([kp1[m.queryIdx].pt for m in good])

            pts2 = np.float32([kp2[m.trainIdx].pt for m in good])

            H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5)

            if mask is not None:

                inliers = int(mask.sum())

                score += inliers * 3

        return int(score)

    def find_best(self, image_path, database_folder):

        results = []

        for file in os.listdir(database_folder):

            if not file.lower().endswith((".png", ".jpg", ".jpeg")):

                continue

            full_path = os.path.join(database_folder, file)

            score = self.compare(image_path, full_path)

            results.append({"card": file, "score": int(score)})

        results.sort(key=lambda x: x["score"], reverse=True)

        return results
