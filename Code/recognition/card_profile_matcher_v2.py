import os
import json

from recognition.feature_matcher_v21 import FeatureMatcherV21


class CardProfileMatcherV2:

    def __init__(self, database="database/cards"):

        self.database = database
        self.matcher = FeatureMatcherV21()

    def load_profiles(self):

        profiles = []

        if not os.path.exists(self.database):

            return profiles

        for card_id in os.listdir(self.database):

            profile_path = os.path.join(self.database, card_id, "profile.json")

            if not os.path.isfile(profile_path):

                continue

            with open(profile_path, "r", encoding="utf-8") as file:

                profiles.append(json.load(file))

        return profiles

    def normalize_score(self, score):

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

            reference_results = []

            for reference in profile["references"]:

                score = self.matcher.compare(image_path, reference["image"])

                reference_results.append(
                    {"reference": reference["image"], "score": int(score)}
                )

                if score > best_score:

                    best_score = score
                    best_reference = reference["image"]

            results.append(
                {
                    "card": profile["id"],
                    "score": self.normalize_score(best_score),
                    "best_reference": best_reference,
                    "reference_count": len(profile["references"]),
                    "references": reference_results,
                }
            )

        results.sort(key=lambda item: item["score"], reverse=True)

        return results
