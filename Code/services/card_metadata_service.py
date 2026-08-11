# ABS Card Metadata Service v1.4
# Improved set detection - keeps number detection from v1.3

import cv2
import pytesseract
import re
from pathlib import Path


class CardMetadataService:

    def __init__(self):

        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        Path("scans").mkdir(exist_ok=True)


    def save_crop(self, name, crop):
        cv2.imwrite(
            f"scans/ocr_debug_{name}.jpg",
            crop
        )


    def prepare(self, image):

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.resize(
            gray,
            None,
            fx=8,
            fy=8,
            interpolation=cv2.INTER_CUBIC
        )

        clahe = cv2.createCLAHE(
            clipLimit=2,
            tileGridSize=(8,8)
        )

        return clahe.apply(gray)


    def ocr(self, image):

        prepared = self.prepare(image)

        results = []

        for psm in ["--psm 6", "--psm 7", "--psm 11"]:

            text = pytesseract.image_to_string(
                prepared,
                lang="eng",
                config=psm
            )

            if text.strip():
                results.append(text.strip())

        return results


    def crop_number(self, image):

        h, w = image.shape[:2]

        crop = image[int(h*0.80):h, 0:int(w*0.65)]

        self.save_crop(
            "number_v14",
            crop
        )

        return crop


    def crop_sets(self, image):

        h, w = image.shape[:2]

        crops = {
            "set_01": image[int(h*0.78):h, 0:int(w*0.45)],
            "set_02": image[int(h*0.75):h, int(w*0.20):int(w*0.70)],
            "set_03": image[int(h*0.70):h, 0:int(w*0.80)]
        }

        for name, crop in crops.items():
            self.save_crop(name, crop)

        return crops


    def normalize_number_text(self, text):

        return (
            text.upper()
            .replace("O", "0")
            .replace("I", "1")
            .replace("L", "1")
            .replace("B", "8")
            .replace("¢", "8")
            .replace(" ", "")
        )


    def find_number(self, texts):

        for text in texts:

            clean = self.normalize_number_text(text)

            matches = re.findall(
                r"\d{2,4}/\d{2,4}",
                clean
            )

            if matches:
                return matches[0]

        return None


    def find_set(self, texts):

        candidates = []

        for text in texts:

            upper = text.upper()

            for item in re.findall(
                r"[A-Z0-9]{4,6}",
                upper
            ):

                # odrzucamy same liczby
                if item.isdigit():
                    continue

                # odrzucamy daty i numery kart
                if re.match(r"^\d{2,4}/\d{2,4}$", item):
                    continue

                # odrzucamy znane śmieci OCR
                if item in [
                    "GAME",
                    "FREAK",
                    "POKEMON",
                    "NINTENDO",
                    "CREATURES"
                ]:
                    continue

                score = 0

                if any(c.isalpha() for c in item):
                    score += 1

                if any(c.isdigit() for c in item):
                    score += 1

                if len(item) in [5,6]:
                    score += 1

                candidates.append(
                    (score, item)
                )


        if not candidates:
            return None


        candidates.sort(
            reverse=True
        )

        return candidates[0][1]


    def analyze(self, image_path):

        image = cv2.imread(
            image_path
        )

        if image is None:
            return None


        number_ocr = self.ocr(
            self.crop_number(image)
        )


        set_ocr = []

        for name, crop in self.crop_sets(image).items():

            for text in self.ocr(crop):

                set_ocr.append(
                    f"{name}: {text}"
                )


        return {

            "set_raw":
                self.find_set(set_ocr),

            "number_raw":
                self.find_number(
                    number_ocr + set_ocr
                ),

            "rarity_raw":
                "C",

            "set_ocr":
                set_ocr,

            "number_ocr":
                number_ocr,

            "confidence":
                85
        }
