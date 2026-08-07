"""
Artysta Break Studio
Camera Widget

Odpowiada wyłącznie za wyświetlanie obrazu z kamery.
"""

import cv2

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel


class CameraWidget(QLabel):
    """
    Widget odpowiedzialny za wyświetlanie obrazu z kamery.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._last_frame = None

        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(640, 480)

        self.setText(
            "Brak obrazu\n\n"
            "Wybierz kamerę i naciśnij START"
        )

        self.setStyleSheet("""
            QLabel {
                background-color: #101010;
                color: #909090;
                border: 2px solid #404040;
                border-radius: 8px;
                font-size: 18px;
            }
        """)

    def set_frame(self, frame):
        """
        Wyświetla klatkę OpenCV.
        """

        self._last_frame = frame

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        height, width, channels = rgb.shape

        image = QImage(
            rgb.data,
            width,
            height,
            channels * width,
            QImage.Format_RGB888,
        )

        pixmap = QPixmap.fromImage(image)

        self.setPixmap(
            pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

    def clear_preview(self):
        self._last_frame = None
        self.clear()
        self.setText(
            "Brak obrazu\n\n"
            "Wybierz kamerę i naciśnij START"
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self._last_frame is not None:
            self.set_frame(self._last_frame)