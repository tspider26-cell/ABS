"""
Artysta Break Studio

Auto Capture Engine v0.1

Automatyczne wykonywanie zdjęcia
gdy karta jest stabilnie widoczna.
"""

import cv2
import time


class AutoCapture:


    def __init__(self):

        # ile kolejnych klatek karta musi być stabilna

        self.required_frames = 30

        self.stable_frames = 0


        self.last_corners = None


        self.capture_ready = False


        self.cooldown = 3

        self.last_capture_time = 0



    def is_stable(self, corners):

        if corners is None:

            self.stable_frames = 0
            self.last_corners = None

            return False



        if self.last_corners is None:

            self.last_corners = corners

            self.stable_frames = 1

            return False



        # sprawdzamy różnicę narożników

        difference = cv2.norm(
            corners,
            self.last_corners,
            cv2.NORM_L2
        )


        self.last_corners = corners



        if difference < 50:

            self.stable_frames += 1

        else:

            self.stable_frames = 0



        return (
            self.stable_frames
            >=
            self.required_frames
        )



    def should_capture(self, corners):


        if not self.is_stable(corners):

            return False



        now = time.time()


        if now - self.last_capture_time < self.cooldown:

            return False



        self.last_capture_time = now


        return True



    def capture(self, frame):

        filename = (
            "scans/card_"
            +
            str(int(time.time()))
            +
            ".jpg"
        )


        cv2.imwrite(
            filename,
            frame
        )


        return filename