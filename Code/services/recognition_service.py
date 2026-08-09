from recognition.auto_recognizer import AutoRecognizer


class RecognitionService:

    def __init__(self):

        self.recognizer = AutoRecognizer()

    def recognize_card(self, image_path):

        result = self.recognizer.recognize(image_path)

        return result
