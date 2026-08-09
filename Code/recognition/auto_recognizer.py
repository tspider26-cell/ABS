from recognition.feature_matcher import FeatureMatcher


class AutoRecognizer:

    def __init__(self):

        self.matcher = FeatureMatcher()

        self.database = "database/images"

    def recognize(self, image_path):

        results = self.matcher.find_best(image_path, self.database)

        if not results:

            return {"card": None, "score": 0}

        best = results[0]

        return {"card": best["card"], "score": best["score"], "all_results": results}
