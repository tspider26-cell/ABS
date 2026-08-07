"""
Artysta Break Studio
Card Detector v1.3

Stable Hybrid Detection

Wersja bazująca na v1.0:
- jasność
- kontur
- filtr obiektów
- stabilny LOCK
"""

import cv2
import numpy as np


class CardDetector:

    def __init__(self):

        self.min_area = 15000

        self.last_card = None

        self.lock_counter = 0
        self.max_lock = 30



    def order_points(self, pts):

        pts = pts.reshape(4,2)

        rect = np.zeros(
            (4,2),
            dtype="float32"
        )

        s = pts.sum(axis=1)

        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(
            pts,
            axis=1
        )

        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect.astype(np.int32).reshape(4,1,2)



    def detect(self, frame):

        result = frame.copy()


        height, width = frame.shape[:2]


        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )


        blur = cv2.GaussianBlur(
            gray,
            (7,7),
            0
        )


        # stały próg - sprawdzony w v1.0

        _, mask = cv2.threshold(
            blur,
            160,
            255,
            cv2.THRESH_BINARY
        )


        kernel = np.ones(
            (7,7),
            np.uint8
        )


        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel
        )


        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )


        best_card = None
        best_score = 0



        for contour in contours:


            area = cv2.contourArea(
                contour
            )


            if area < self.min_area:
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



            ordered = self.order_points(
                approx
            )



            x,y,w,h = cv2.boundingRect(
                ordered
            )


            if w == 0:
                continue



            ratio = h / float(w)



            # proporcja karty

            if ratio < 1.15 or ratio > 1.85:
                continue



            # obiekt musi być rozsądnie duży

            if w < width * 0.15:
                continue


            if h < height * 0.15:
                continue



            # preferujemy środek kadru

            cx = x + w/2
            cy = y + h/2


            distance = (
                abs(cx-width/2)
                +
                abs(cy-height/2)
            )


            score = area - distance*20



            if score > best_score:

                best_score = score
                best_card = ordered




        # LOCK

        if best_card is not None:

            self.last_card = best_card

            self.lock_counter = self.max_lock



        elif self.last_card is not None and self.lock_counter > 0:

            best_card = self.last_card

            self.lock_counter -= 1


        else:

            self.last_card = None




        if best_card is not None:


            cv2.drawContours(
                result,
                [best_card],
                -1,
                (0,255,0),
                5
            )


            for point in best_card:

                x,y = point[0]

                cv2.circle(
                    result,
                    (x,y),
                    8,
                    (0,0,255),
                    -1
                )


            cv2.putText(
                result,
                "CARD DETECTOR v1.3",
                (40,60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0,255,0),
                3
            )


        else:


            cv2.putText(
                result,
                "SEARCHING CARD",
                (40,60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0,0,255),
                3
            )



        return result, best_card