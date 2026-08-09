from recognition.card_profile_matcher_v2 import CardProfileMatcherV2


class ProfileRecognizer:

    def __init__(self, database="database/cards"):

        self.matcher = CardProfileMatcherV2(database)

    def recognize(self, image_path):

        results = self.matcher.recognize(image_path)

        if not results:

            return {"card": None, "score": 0}

        best = results[0]

        return {
            "card": best["card"],
            "score": best["score"],
            "reference": best["best_reference"],
            "details": best["references"],
        }
