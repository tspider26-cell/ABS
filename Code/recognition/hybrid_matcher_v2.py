import cv2
import os
import numpy as np


class HybridMatcherV2:

    def __init__(self):

        self.orb = cv2.ORB_create(nfeatures=2500)

        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

    def load_gray(self, path):

        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        return img

    def extract(self, path):

        img = self.load_gray(path)

        if img is None:
            return None, None

        kp, des = self.orb.detectAndCompute(img, None)

        return kp, des

    def compare(self, source, target):

        kp1, des1 = self.extract(source)

        kp2, des2 = self.extract(target)

        if des1 is None or des2 is None:

            return 0

        matches = self.matcher.knnMatch(des1, des2, k=2)

        good = []

        for pair in matches:

            if len(pair) != 2:
                continue

            m, n = pair

            if m.distance < 0.75 * n.distance:

                good.append(m)

        if len(good) < 5:

            return 0

        score = len(good)

        # ======================
        # GEOMETRIA KARTY
        # ======================

        if len(good) >= 8:

            pts1 = np.float32([kp1[m.queryIdx].pt for m in good])

            pts2 = np.float32([kp2[m.trainIdx].pt for m in good])

            H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5)

            if mask is not None:

                inliers = int(mask.sum())

                score += inliers * 5

            else:

                score -= 10

        else:

            score -= 5

        return max(0, int(score))

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
