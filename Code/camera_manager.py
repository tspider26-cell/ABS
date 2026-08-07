"""
Artysta Break Studio
Camera Manager

Odpowiada za:
- wykrywanie kamer,
- otwieranie kamery,
- pobieranie klatek,
- zamykanie kamery.
"""

import cv2


class CameraManager:

    def __init__(self):

        self.cap = None
        self.camera_index = None

    # --------------------------------------------------

    def available_cameras(self, max_index=5):

        cameras = []

        for index in range(max_index):

            cap = cv2.VideoCapture(index)

            if cap.isOpened():
                cameras.append(index)
                cap.release()

        return cameras

    # --------------------------------------------------

    def open(self, camera_index):

        self.close()

        self.cap = cv2.VideoCapture(
            camera_index,
            cv2.CAP_DSHOW
        )

        if not self.cap.isOpened():

            self.cap = None
            return False

        self.camera_index = camera_index

        return True

    # --------------------------------------------------

    def read(self):

        if self.cap is None:
            return None

        ok, frame = self.cap.read()

        if not ok:
            return None

        return frame

    # --------------------------------------------------

    def close(self):

        if self.cap is not None:
            self.cap.release()
            self.cap = None

    # --------------------------------------------------

    def is_open(self):

        return self.cap is not None