import cv2
import os


class CardMatcher:

    def __init__(self):

        self.detector = cv2.ORB_create(nfeatures=1000)

    def load_image(self, path):

        if not os.path.exists(path):

            print("BRAK PLIKU:", path)

            return None

        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        return image

    def compare(self, scanned_path, reference_path):

        scanned = self.load_image(scanned_path)

        reference = self.load_image(reference_path)

        if scanned is None or reference is None:

            return 0

        key1, des1 = self.detector.detectAndCompute(scanned, None)

        key2, des2 = self.detector.detectAndCompute(reference, None)

        if des1 is None or des2 is None:

            return 0

        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        matches = matcher.match(des1, des2)

        matches = sorted(matches, key=lambda x: x.distance)

        good = matches[:50]

        score = len(good)

        print("DOPASOWANIA:", score)

        return score
