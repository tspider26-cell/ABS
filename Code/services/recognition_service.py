from recognition.auto_recognizer import AutoRecognizer
from services.profile_recognition_service import ProfileRecognitionService

PROFILE_MODE = True


class RecognitionService:

    def __init__(self):

        self.profile_mode = PROFILE_MODE

        if self.profile_mode:

            self.recognizer = ProfileRecognitionService()

        else:

            self.recognizer = AutoRecognizer()

    def recognize_card(self, image_path):

        if self.profile_mode:

            return self.recognizer.recognize_card(image_path)

        else:

            return self.recognizer.recognize(image_path)
