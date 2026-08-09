import os
import json

from recognition.feature_matcher_v21 import FeatureMatcherV21


class CardProfileMatcher:

    def __init__(self, database="database/cards"):

        self.database = database
        self.matcher = FeatureMatcherV21()

    def load_profiles(self):

        profiles = []

        if not os.path.exists(self.database):

            return profiles

        for card_id in os.listdir(self.database):

            folder = os.path.join(self.database, card_id)

            profile_file = os.path.join(folder, "profile.json")

            if not os.path.isfile(profile_file):

                continue

            with open(profile_file, "r", encoding="utf-8") as f:

                profile = json.load(f)

            profiles.append(profile)

        return profiles

    def normalize_score(self, score):

        # ograniczamy wynik do 0-100

        if score <= 0:

            return 0

        if score >= 8000:

            return 100

        return int((score / 8000) * 100)

    def recognize(self, image_path):

        results = []

        profiles = self.load_profiles()

        for profile in profiles:

            best_score = 0

            best_reference = None

            for ref in profile["references"]:

                score = self.matcher.compare(image_path, ref["image"])

                if score > best_score:

                    best_score = score

                    best_reference = ref["image"]

            results.append(
                {
                    "card": profile["id"],
                    "score": self.normalize_score(best_score),
                    "best_reference": best_reference,
                }
            )

        results.sort(key=lambda x: x["score"], reverse=True)

        return results
