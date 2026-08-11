# ABS CARD RECOGNITION PIPELINE v3.1

from recognition.feature_matcher import FeatureMatcher
from services.smart_card_resolver import SmartCardResolver
from services.image_card_mapper import ImageCardMapper


class CardRecognitionPipeline:

    def __init__(self):

        self.matcher = FeatureMatcher()
        self.resolver = SmartCardResolver()
        self.mapper = ImageCardMapper()

        self.database = "database/images/tcgdex"


    def recognize(self, image_path):

        results = self.matcher.find_best(
            image_path,
            self.database
        )


        if not results:

            return {
                "found": False,
                "source": None,
                "card": None,
                "score": 0
            }


        best = results[0]


        mapped = self.mapper.map_result(
            best
        )


        metadata = {
            "tcgdex_id": mapped.get("card_id")
        }


        resolved = self.resolver.resolve(
            metadata
        )


        return {
            "found": resolved.get("found", False),
            "source": resolved.get("source"),
            "card": resolved.get("card"),
            "score": mapped.get("score"),
            "matcher": mapped,
            "all_results": results
        }
