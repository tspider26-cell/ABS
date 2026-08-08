# ============================================================
# Artysta Break Studio
# Main Window v2.1
# Camera + Detector Test Mode
# ============================================================

import time
import sys

from PySide6.QtCore import Qt, QTimer

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
    QLabel,
)

from theme import DARK_THEME

from camera_manager import CameraManager
from widgets.camera_widget import CameraWidget

from vision.card_detector import CardDetector


# AutoCapture wyłączony na czas testów
AUTO_CAPTURE_ENABLED = False



class MainWindow(QMainWindow):


    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "Artysta Break Studio"
        )


        self.resize(
            1400,
            900
        )


        self.setStyleSheet(
            DARK_THEME
        )


        # Kamera

        self.camera_manager = CameraManager()


        # Detector

        self.card_detector = CardDetector()



        self.camera_timer = QTimer()

        self.camera_timer.timeout.connect(
            self.update_camera
        )



        self.last_time = time.time()

        self.frame_count = 0



        self.create_menu()

        self.create_ui()

        self.load_cameras()



    # --------------------------------------------------

    def create_menu(self):

        self.menuBar().addMenu("Plik")
        self.menuBar().addMenu("Kamera")
        self.menuBar().addMenu("Narzędzia")
        self.menuBar().addMenu("Widok")
        self.menuBar().addMenu("Pomoc")



    # --------------------------------------------------

    def create_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )


        layout = QVBoxLayout(
            central
        )


        toolbar = QHBoxLayout()


        toolbar.addWidget(
            QLabel("Kamera:")
        )


        self.camera_combo = QComboBox()


        toolbar.addWidget(
            self.camera_combo
        )


        self.start_button = QPushButton(
            "▶ Start"
        )


        self.stop_button = QPushButton(
            "■ Stop"
        )


        toolbar.addWidget(
            self.start_button
        )


        toolbar.addWidget(
            self.stop_button
        )


        toolbar.addStretch()


        self.fps_label = QLabel(
            "FPS: 0"
        )


        toolbar.addWidget(
            self.fps_label
        )


        layout.addLayout(
            toolbar
        )


        self.camera_widget = CameraWidget()


        layout.addWidget(
            self.camera_widget
        )

        splitter = QSplitter(
            Qt.Horizontal
        )


        splitter.addWidget(
            QGroupBox(
                "Historia sesji"
            )
        )


        splitter.addWidget(
            QGroupBox(
                "Rozpoznana karta"
            )
        )


        splitter.setSizes(
            [350,900]
        )


        layout.addWidget(
            splitter
        )



        self.status = QStatusBar()


        self.status.showMessage(
            "🟢 GOTOWY"
        )


        self.setStatusBar(
            self.status
        )



        self.start_button.clicked.connect(
            self.start_camera
        )


        self.stop_button.clicked.connect(
            self.stop_camera
        )



    # --------------------------------------------------

    def load_cameras(self):

        self.camera_combo.clear()


        cameras = self.camera_manager.available_cameras()


        if not cameras:

            self.camera_combo.addItem(
                "Brak wykrytej kamery"
            )

            self.start_button.setEnabled(
                False
            )

            return



        for camera in cameras:

            self.camera_combo.addItem(
                f"Kamera {camera}",
                camera
            )



    # --------------------------------------------------

    def start_camera(self):

        index = self.camera_combo.currentData()


        if index is None:

            return



        success = self.camera_manager.open(
            index
        )


        if not success:

            self.status.showMessage(
                f"🔴 Nie udało się uruchomić kamery {index}"
            )

            return



        self.camera_timer.start(
            30
        )


        self.status.showMessage(
            "🟢 Kamera uruchomiona"
        )



    # --------------------------------------------------

    def update_camera(self):

        frame = self.camera_manager.read()


        if frame is None:

            return



        # zachowujemy oryginalny obraz kamery

        display_frame = frame.copy()



        # DETECTOR TEST

        try:

            result = self.card_detector.detect(
                frame
            )


            if result is not None:

                warped, corners, score = result


                if corners is not None:

                    display_frame = self.card_detector.draw_result(
                        display_frame,
                        corners,
                        score
                    )


        except Exception:

            # detector nie może zatrzymać kamery

            pass



        # pokazujemy zawsze obraz z kamery

        self.camera_widget.set_frame(
            display_frame
        )
                # FPS

        self.frame_count += 1

        now = time.time()


        if now - self.last_time >= 1:


            fps = self.frame_count


            self.frame_count = 0


            self.last_time = now


            self.fps_label.setText(
                f"FPS: {fps}"
            )



    # --------------------------------------------------

    def stop_camera(self):

        self.camera_timer.stop()


        self.camera_manager.close()


        self.camera_widget.clear_preview()


        self.fps_label.setText(
            "FPS: 0"
        )


        self.status.showMessage(
            "🔴 Kamera zatrzymana"
        )



# =====================================================
# START PROGRAMU
# =====================================================


def main():

    app = QApplication(
        sys.argv
    )


    window = MainWindow()


    window.show()


    sys.exit(
        app.exec()
    )



if __name__ == "__main__":

    main()