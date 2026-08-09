import cv2
import os


class FeatureMatcherV2:

    def __init__(self):

        self.orb = cv2.ORB_create(nfeatures=1500)

        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

    def extract_features(self, image_path):

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:

            return None, None

        keypoints, descriptors = self.orb.detectAndCompute(image, None)

        return keypoints, descriptors

    def compare(self, image1, image2):

        kp1, des1 = self.extract_features(image1)

        kp2, des2 = self.extract_features(image2)

        if des1 is None or des2 is None:

            return 0

        matches = self.bf.knnMatch(des1, des2, k=2)

        good = []

        for m, n in matches:

            if m.distance < 0.75 * n.distance:

                good.append(m)

        if len(good) < 5:

            return 0

        score = len(good)

        # próba geometrii

        if len(good) >= 8:

            pts1 = []

            pts2 = []

            for match in good:

                pts1.append(kp1[match.queryIdx].pt)

                pts2.append(kp2[match.trainIdx].pt)

            import numpy as np

            pts1 = np.float32(pts1)

            pts2 = np.float32(pts2)

            H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)

            if mask is not None:

                inliers = sum(mask.ravel())

                score = score + (inliers * 2)

        return score

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
