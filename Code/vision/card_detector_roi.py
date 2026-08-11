# ============================================================
# CARD DETECTOR ROI v1.0
# Stable Scanner - Fixed Area Detection
# ============================================================


import cv2
import numpy as np
import time


class ROICardDetector:

    def __init__(self):

        # stan pustej ramki
        self.reference = None

        # wykrycie karty
        self.card_present = False

        # czas stabilizacji
        self.detect_start = None

        # opóźnienie przed capture
        self.capture_delay = 3.0

    # ========================================================
    # USTAWIENIE PUSTEGO OBSZARU
    # ========================================================

    def set_reference(self, roi):

        if roi is None:
            return False

        self.reference = roi.copy()

        print("ROI REFERENCJA USTAWIONA")

        return True

    # ========================================================
    # WYKRYWANIE KARTY
    # ========================================================

    def detect(self, roi):

        if self.reference is None:

            return False

        if roi is None:

            return False
            # ========================================================

    # ANALIZA ZMIANY W OBSZARZE
    # ========================================================

    def analyze_difference(self, roi):

        if self.reference is None:

            return 0

        # różnica między pustą ramką a aktualnym obrazem

        diff = cv2.absdiff(roi, self.reference)

        # zamiana na szarość

        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # średnia zmiana pikseli

        value = np.mean(gray)

        return value

    # ========================================================
    # GŁÓWNA FUNKCJA DETEKCJI
    # ========================================================

    def check_card(self, roi):

        difference = self.analyze_difference(roi)

        print("ROI DIFFERENCE:", round(difference, 2))

        # próg wykrycia karty

        threshold = 15

        if difference > threshold:

            if not self.card_present:

                self.card_present = True

                self.detect_start = time.time()

                print("KARTA WYKRYTA - START TIMERA")

            elapsed = time.time() - self.detect_start

            print("KARTA CZAS:", round(elapsed, 2))

            if elapsed >= self.capture_delay:

                print("KARTA STABILNA - GOTOWA DO ZAPISU")

                return True

        else:

            self.card_present = False

            self.detect_start = None

        return False
        # ========================================================

    # POBRANIE OBRAZU KARTY
    # ========================================================

    def get_card_image(self, roi):

        if roi is None:

            return None

        # Szukamy właściwej krawędzi karty wewnątrz ROI
        # i wycinamy tylko kartę zamiast całego pola skanera.

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(
            gray,
            (5, 5),
            0
        )

        edges = cv2.Canny(
            blur,
            50,
            150
        )

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        best = None
        best_area = 0

        for contour in contours:

            area = cv2.contourArea(contour)

            if area < 5000:
                continue

            perimeter = cv2.arcLength(
                contour,
                True
            )

            approx = cv2.approxPolyDP(
                contour,
                0.03 * perimeter,
                True
            )

            if len(approx) != 4:
                continue

            if area > best_area:

                best_area = area
                best = approx

        if best is None:
            return roi.copy()


        pts = best.reshape(4, 2).astype("float32")

        # kolejność narożników
        s = pts.sum(axis=1)
        diff = np.diff(pts, axis=1)

        rect = np.zeros(
            (4, 2),
            dtype="float32"
        )

        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        width = 630
        height = 880

        dst = np.array(
            [
                [0, 0],
                [width - 1, 0],
                [width - 1, height - 1],
                [0, height - 1]
            ],
            dtype="float32"
        )

        matrix = cv2.getPerspectiveTransform(
            rect,
            dst
        )

        card = cv2.warpPerspective(
            roi,
            matrix,
            (width, height)
        )

        # delikatne czarne obramowanie
        result = np.zeros(
            (height + 80, width + 80, 3),
            dtype=np.uint8
        )

        result[40:40 + height, 40:40 + width] = card

        return result

    # ========================================================
    # RESET PO ZAPISIE
    # ========================================================

    def reset(self):

        self.card_present = False

        self.detect_start = None
        # ========================================================

    # INFORMACJE DEBUG
    # ========================================================

    def get_status(self):

        return {
            "reference": self.reference is not None,
            "card_present": self.card_present,
            "timer_active": self.detect_start is not None,
        }
