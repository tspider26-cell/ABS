# ============================================================
# CARD DETECTOR v1.7.1 HYBRID
# Full Card Boundary + Fallback Detection
#
# Pokemon / Magic / Lorcana / Marvel / TCG
# ============================================================


import cv2
import numpy as np



class CardDetector:


    def __init__(self):

        self.last_card = None
        self.last_score = 0


        # zakres proporcji różnych kart

        self.min_ratio = 1.15
        self.max_ratio = 1.70



    # --------------------------------------------------------
    # GŁÓWNA FUNKCJA DETEKCJI
    # --------------------------------------------------------

    def detect(self, frame):


        if frame is None:

            return frame, None, 0



        original = frame.copy()



        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )



        # poprawa kontrastu

        gray = cv2.equalizeHist(
            gray
        )



        blur = cv2.GaussianBlur(
            gray,
            (5,5),
            0
        )



        # pierwsza metoda

        edges = cv2.Canny(
            blur,
            40,
            120
        )



        kernel = np.ones(
            (7,7),
            np.uint8
        )


        edges = cv2.morphologyEx(
            edges,
            cv2.MORPH_CLOSE,
            kernel
        )



        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )


        card = self.find_best_contour(
         contours,
          frame.shape
)

        print("KONTURY:", len(contours), "WYNIK:", card is not None)




        if card is None:

         print("BRAK KARTY - kontury:", len(contours))

         return original, None, 0



        score = self.calculate_score(
            cv2.contourArea(card),
            frame.shape[1],
            frame.shape[0]
        )



        self.last_card = card
        self.last_score = score



        return original, card, score

        # --------------------------------------------------------
    # SZUKANIE NAJLEPSZEGO KONTURU
    # --------------------------------------------------------

        # --------------------------------------------------------
    # SZUKANIE NAJLEPSZEGO KONTURU KARTY v1.7.2
    # --------------------------------------------------------

    
    
        # --------------------------------------------------------
    # FIND BEST CARD CONTOUR v1.7.3
    # PRIORYTET: PRAWDZIWA KARTA
    # --------------------------------------------------------

    def find_best_contour(
            self,
            contours,
            shape
    ):


        height, width = shape[:2]

        frame_area = width * height


        best = None
        best_score = 0



        for contour in contours:
            print(
          "AREA:",
            int(cv2.contourArea(contour))
        )


            area = cv2.contourArea(
                contour
            )


            # odrzucamy śmieci

            if area < frame_area * 0.02:

                continue



            if area > frame_area * 0.80:

                continue



            perimeter = cv2.arcLength(
                contour,
                True
            )


            approx = cv2.approxPolyDP(
                contour,
                0.015 * perimeter,
                True
            )



            if len(approx) != 4:
                  continue



            x,y,w,h = cv2.boundingRect(
                approx
            )



            ratio = h / w if w else 0



            # proporcja karty Pokemon

            if ratio < 1.05 or ratio > 1.90:

                continue



            # karta nie może być za mała

            if h < height * 0.12:

                continue



            # środek karty

            cx = x + w/2
            cy = y + h/2



            distance = (
                abs(cx-width/2)
                +
                abs(cy-height/2)
            )



            center_score = max(
                0,
                100 - distance/8
            )



            # preferujemy większą kartę,
            # ale nie ogromny obiekt

            size_score = (
                area / frame_area
            ) * 200



            score = (
                center_score
                +
                size_score
            )



            if score > best_score:

                best_score = score

                best = approx



        return best
    
    def draw_result(
            self,
            frame,
            corners,
            score
    ):


        if corners is None:

            return frame



        points = corners.reshape(
            (-1,2)
        )



        cv2.polylines(
            frame,
            [points],
            True,
            (0,255,0),
            4
        )



        cv2.putText(
            frame,
            f"CARD FOUND {score}%",
            (30,60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0,255,0),
            3
        )



        return frame



    # --------------------------------------------------------
    # KOREKCJA PERSPEKTYWY
    # --------------------------------------------------------

    def correct_perspective(
            self,
            image,
            corners
    ):


        pts = corners.reshape(
            4,2
        ).astype(
            "float32"
        )



        rect = np.zeros(
            (4,2),
            dtype="float32"
        )



        s = pts.sum(
            axis=1
        )


        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]



        diff = np.diff(
            pts,
            axis=1
        )


        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]



        width = 630

        height = 880



        dst = np.array(
            [
                [0,0],
                [width-1,0],
                [width-1,height-1],
                [0,height-1]
            ],
            dtype="float32"
        )



        matrix = cv2.getPerspectiveTransform(
            rect,
            dst
        )



        warped = cv2.warpPerspective(
            image,
            matrix,
            (width,height)
        )



        return warped



    # --------------------------------------------------------
    # POBIERANIE SAMEJ KARTY
    # --------------------------------------------------------

    def get_card_image(
            self,
            frame,
            corners
    ):


        if corners is None:

            return None



        return self.correct_perspective(
            frame,
            corners
        )



    # --------------------------------------------------------
    # ZAPIS
    # --------------------------------------------------------

    def save_card(
            self,
            image,
            filename
    ):


        if image is None:

            return False



        return cv2.imwrite(
            filename,
            image
        )



    # --------------------------------------------------------
    # OCENA
    # --------------------------------------------------------

    def calculate_score(
            self,
            area,
            width,
            height
    ):


        frame_area = width * height


        ratio = area / frame_area



        score = int(
            min(
                ratio * 350,
                99
            )
        )


        if score < 50:

            score = 50



        return score