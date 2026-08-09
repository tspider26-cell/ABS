from recognition.profile_recognizer import ProfileRecognizer


class ProfileRecognitionService:

    def __init__(self):

        self.recognizer = ProfileRecognizer()

    def recognize_card(self, image_path):

        result = self.recognizer.recognize(image_path)

        if result["card"] is None:

            return {"status": "not_found", "card": None, "score": 0}

        return {
            "status": "recognized",
            "card": result["card"],
            "score": result["score"],
            "reference": result["reference"],
            "details": result["details"],
        }
