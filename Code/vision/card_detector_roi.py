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

        # kopiujemy aktualny obszar skanowania

        card = roi.copy()

        return card

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
