from vision.card_detector import CardDetector
from recognition.feature_matcher import FeatureMatcher

import cv2

IMAGE = "scans/last_card.jpg"


print("WCZYTUJE OBRAZ:")
print(IMAGE)


frame = cv2.imread(IMAGE)


if frame is None:

    print("BŁĄD: nie znaleziono obrazu")

    exit()


# ==========================
# DETEKCJA KARTY
# ==========================

detector = CardDetector()


original, corners, score = detector.detect(frame)


print("\nDETEKCJA:")
print("CORNERS:", corners)
print("SCORE:", score)


if corners is None:

    print("NIE WYKRYTO KARTY")

    exit()


# ==========================
# WYCIĘCIE KARTY
# ==========================

card = detector.get_card_image(frame, corners)


if card is None:

    print("BŁĄD WYCIĘCIA KARTY")

    exit()


save_path = "scans/processed_card.jpg"


cv2.imwrite(save_path, card)


print("\nZAPISANO:")
print(save_path)


# ==========================
# MATCHING
# ==========================

matcher = FeatureMatcher()


results = matcher.find_best(save_path, "database/images")


print("\nWYNIKI ROZPOZNANIA:")


for result in results:

    print(result)
