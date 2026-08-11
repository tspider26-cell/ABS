# ============================================================
# CARD DETECTOR v1.8
# Stable Card Scanner
# Pokemon / Magic / Lorcana / Marvel / TCG
# ============================================================


import cv2
import numpy as np
import os


class CardDetector:
    print("CARD DETECTOR v1.8 START")

    def __init__(self):

        self.last_card = None
        self.last_score = 0

        # proporcje kart
        self.min_ratio = 1.15
        self.max_ratio = 1.70

    # ========================================================
    # GŁÓWNA DETEKCJA
    # ========================================================

    def detect(self, frame):

        if frame is None:

            return frame, None, 0

        original = frame.copy()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gray = cv2.equalizeHist(gray)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(blur, 60, 150)

        kernel = np.ones((3, 3), np.uint8)

        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        corners = self.find_best_contour(contours, frame.shape)

        print("KONTURY:", len(contours), "WYNIK:", corners is not None)

        if corners is None:

            return original, None, 0

        area = cv2.contourArea(corners.astype("float32"))

        score = self.calculate_score(area, frame.shape[1], frame.shape[0])

        self.last_card = corners
        self.last_score = score

        return original, corners, score
        # ========================================================

    # SZUKANIE NAJLEPSZEGO KONTURU KARTY
    # ========================================================

    def find_best_contour(self, contours, shape):

        height, width = shape[:2]

        frame_area = width * height

        best = None
        best_score = 0

        for contour in contours:

            area = cv2.contourArea(contour)

            print("AREA:", int(area))

            if area < frame_area * 0.02:

                continue

            if area > frame_area * 0.80:

                continue

            perimeter = cv2.arcLength(contour, True)

            approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)

            if len(approx) != 4:

                continue

            x, y, w, h = cv2.boundingRect(approx)
            print("RECT:", x, y, w, h, "RATIO:", round(h / w, 2))

            # ODRZUCAMY CAŁĄ RAMKĘ SKANERA

            if w > width * 0.90 and h > height * 0.90:

                print("ODRZUCONO - CAŁA RAMKA")

                continue

            if w == 0:

                continue

            ratio = h / w

            if ratio < 1.10 or ratio > 2.00:

                continue

            if h < height * 0.12:

                continue

            cx = x + w / 2
            cy = y + h / 2

            distance = abs(cx - width / 2) + abs(cy - height / 2)

            center_score = max(0, 100 - distance / 8)

            size_score = (area / frame_area) * 200

            score = center_score + size_score

            if score > best_score:

                best_score = score

                rect = cv2.minAreaRect(contour)

                box = cv2.boxPoints(rect)

                best = box.astype("float32")

        return best
        # ========================================================

    # RYSOWANIE WYNIKU
    # ========================================================

    def draw_result(self, frame, corners, score):

        if corners is None:

            return frame

        points = corners.reshape((-1, 2)).astype("int32")

        cv2.polylines(frame, [points], True, (0, 255, 0), 4)

        cv2.putText(
            frame,
            f"CARD FOUND {int(score)}%",
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            3,
        )

        return frame

    # ========================================================
    # POBIERANIE OBRAZU KARTY
    # ========================================================

    def get_card_image(self, frame, corners):

        if corners is None:

            return None

        pts = corners.reshape(4, 2).astype("float32")

        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)

        # poprawna kolejność narożników
        # sortowanie niezależne od obrotu karty

        s = pts.sum(axis=1)
        diff = np.diff(pts, axis=1)

        rect[0] = pts[np.argmin(s)]      # lewy góra
        rect[2] = pts[np.argmax(s)]      # prawy dół
        rect[1] = pts[np.argmin(diff)]   # prawy góra
        rect[3] = pts[np.argmax(diff)]   # lewy dół

        width = 630
        height = 880

        dst = np.array(
            [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
            dtype="float32",
        )

        matrix = cv2.getPerspectiveTransform(rect, dst)

        warped = cv2.warpPerspective(frame, matrix, (width, height))

        return warped
        # ========================================================

    # ZAPIS KARTY
    # ========================================================

    def save_card(self, image, filename):

        if image is None:

            return False

        save_folder = r"C:\ABS\Code\scans"

        os.makedirs(save_folder, exist_ok=True)

        save_path = os.path.join(save_folder, filename)
        result = cv2.imwrite(save_path, image)

        print("ZAPIS PLIK:", save_path)
        print("ISTNIEJE:", os.path.exists(save_path))

        return result

    # ========================================================
    # OCENA WYKRYCIA
    # ========================================================

    def calculate_score(self, area, width, height):

        frame_area = width * height

        ratio = area / frame_area

        score = int(min(ratio * 350, 99))

        if score < 50:

            score = 50

        return score
