from services.card_family_detector import CardFamilyDetector


class CardFamilyService:

    def __init__(self):

        self.detector = CardFamilyDetector()

    def analyze_card(self, image_path):

        result = self.detector.detect(image_path)

        return {
            "family": result.get("family", "Unknown"),
            "family_confidence": result.get("confidence", 0),
            "family_signals": result.get("signals", []),
        }
