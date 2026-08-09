from recognition.feature_extractor import FeatureExtractor
import os

IMAGE_FOLDER = "database/images"


extractor = FeatureExtractor()


def build_features():

    if not os.path.exists(IMAGE_FOLDER):

        print("BRAK FOLDERU:", IMAGE_FOLDER)

        return

    files = os.listdir(IMAGE_FOLDER)

    count = 0

    for file in files:

        if not file.lower().endswith((".png", ".jpg", ".jpeg")):

            continue

        image_path = os.path.join(IMAGE_FOLDER, file)

        print("\nPRZETWARZAM:", image_path)

        features = extractor.extract(image_path)

        if features is None:

            print("BŁĄD:", file)

            continue

        card_id = os.path.splitext(file)[0]

        extractor.save_features(card_id, features)

        count += 1

    print("\nGOTOWE. UTWORZONO CECH:", count)


build_features()
