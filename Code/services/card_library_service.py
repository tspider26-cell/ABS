import os
import shutil

from recognition.feature_extractor import FeatureExtractor


class CardLibraryService:

    def __init__(self):

        self.images_folder = "database/images"

        self.extractor = FeatureExtractor()

        os.makedirs(self.images_folder, exist_ok=True)

    def add_card(self, source_image, card_id):

        extension = os.path.splitext(source_image)[1]

        filename = card_id + extension

        destination = os.path.join(self.images_folder, filename)

        shutil.copy2(source_image, destination)

        print("DODANO OBRAZ:", destination)

        features = self.extractor.extract(destination)

        if features is None:

            print("BŁĄD CECH")

            return None

        self.extractor.save_features(card_id, features)

        return features
