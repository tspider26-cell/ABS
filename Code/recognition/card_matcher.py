import cv2
import os


class CardMatcher:

    def __init__(self):

        self.detector = cv2.ORB_create(nfeatures=1500)

    def load_image(self, path):

        if not os.path.exists(path):

            return None

        return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    def compare_images(self, image1, image2):

        key1, des1 = self.detector.detectAndCompute(image1, None)

        key2, des2 = self.detector.detectAndCompute(image2, None)

        if des1 is None or des2 is None:

            return 0

        matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

        matches = matcher.knnMatch(des1, des2, k=2)

        good = []

        for m, n in matches:

            if m.distance < 0.75 * n.distance:

                good.append(m)

        if len(good) == 0:

            return 0

        score = len(good)

        return score

    def find_best_match(self, scanned_path, database_folder):

        scanned = self.load_image(scanned_path)

        if scanned is None:

            return None

        best_card = None
        best_score = 0

        for file in os.listdir(database_folder):

            if not file.endswith(".png"):

                continue

            path = os.path.join(database_folder, file)

            reference = self.load_image(path)

            if reference is None:

                continue

            score = self.compare_images(scanned, reference)

            print(file, "->", score)

            if score > best_score:

                best_score = score

                best_card = file

        return {"card": best_card, "score": best_score}
