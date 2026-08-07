"""
Artysta Break Studio
Card Scanner v1.1

Perspective Transform
Wyprostowanie wykrytej karty.
"""

import cv2
import numpy as np


class CardScanner:


    def __init__(self):

        # standardowy format karty Pokemon
        self.card_width = 744
        self.card_height = 1039



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


        return rect



    def scan(self, frame, corners):

        if corners is None:
            return None


        points = self.order_points(
            corners
        )


        destination = np.array(
            [
                [0,0],
                [
                    self.card_width-1,
                    0
                ],
                [
                    self.card_width-1,
                    self.card_height-1
                ],
                [
                    0,
                    self.card_height-1
                ]

            ],
            dtype="float32"
        )


        matrix = cv2.getPerspectiveTransform(
            points,
            destination
        )


        scanned = cv2.warpPerspective(
            frame,
            matrix,
            (
                self.card_width,
                self.card_height
            )
        )


        return scanned