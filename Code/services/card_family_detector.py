import cv2
import pytesseract
from pathlib import Path
from difflib import SequenceMatcher


class CardFamilyDetector:

    def __init__(self):

        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        Path("scans").mkdir(exist_ok=True)

        self.rules = {
            "Pokemon": {
                "keywords": {
                    "POKEMON": 40,
                    "NINTENDO": 35,
                    "CREATURES": 35,
                    "GAMEFREAK": 45,
                    "GAME FREAK": 45,
                }
            },
            "Disney Lorcana": {
                "keywords": {"DISNEY": 40, "LORCANA": 50, "RAVENSBURGER": 35}
            },
            "Topps": {"keywords": {"TOPPS": 80}},
            "One Piece": {"keywords": {"BANDAI": 40, "ONE PIECE": 50}},
        }

    def similarity(self, a, b):

        return SequenceMatcher(None, a, b).ratio()

    def prepare(self, crop):

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        gray = cv2.resize(gray, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)

        clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))

        return clahe.apply(gray)

    def create_areas(self, image):

        h, w = image.shape[:2]

        return {
            "bottom": image[int(h * 0.75) : h, 0:w],
            "bottom_left": image[int(h * 0.70) : h, 0 : int(w * 0.55)],
            "bottom_right": image[int(h * 0.70) : h, int(w * 0.45) : w],
        }

    def read_area(self, crop):

        prepared = self.prepare(crop)

        return pytesseract.image_to_string(
            prepared, lang="eng", config="--psm 6"
        ).upper()

    def split_words(self, text):

        text = text.replace("/", " ").replace("-", " ").replace("\n", " ")

        return [x.strip() for x in text.split() if len(x.strip()) > 1]

    def find_keyword(self, words, keyword):

        keyword = keyword.replace(" ", "")

        best = 0

        for word in words:

            clean = word.replace(" ", "")

            score = self.similarity(clean, keyword)

            # dodatkowy bonus za podobny początek
            if clean[:3] == keyword[:3]:

                score += 0.10

            if score > best:

                best = score

        return min(best, 1)

    def detect(self, image_path):

        image = cv2.imread(image_path)

        if image is None:

            return {"family": "Unknown", "confidence": 0, "signals": []}

        full_text = ""

        for name, crop in self.create_areas(image).items():

            cv2.imwrite(f"scans/family_{name}.jpg", crop)

            full_text += " "

            full_text += self.read_area(crop)

        words = self.split_words(full_text)

        results = []

        for family, data in self.rules.items():

            points = 0
            signals = []

            for keyword, weight in data["keywords"].items():

                match = self.find_keyword(words, keyword)

                if match >= 0.55:

                    points += int(weight * match)

                    signals.append({"keyword": keyword, "match": round(match, 2)})

            if points:

                results.append(
                    {
                        "family": family,
                        "confidence": min(points, 100),
                        "signals": signals,
                        "ocr_text": full_text,
                    }
                )

        if not results:

            return {
                "family": "Unknown",
                "confidence": 0,
                "signals": [],
                "ocr_text": full_text,
            }

        results.sort(key=lambda x: x["confidence"], reverse=True)

        return results[0]
