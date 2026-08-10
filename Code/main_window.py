# ============================================================
# Artysta Break Studio
# Main Window v3.2
# ROI Card Scanner + Live Recognition
# ============================================================

import sys
import time
import cv2


from PySide6.QtCore import Qt, QTimer

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)


from theme import DARK_THEME

from camera_manager import CameraManager

from widgets.recognition_panel import RecognitionPanel
from widgets.camera_widget import CameraWidget

from vision.card_detector_roi import ROICardDetector

from services.recognition_service import RecognitionService

from utils.sound_player import SoundPlayer



AUTO_CAPTURE_ENABLED = True

CAPTURE_DELAY = 3.0

SCAN_WIDTH = 650
SCAN_HEIGHT = 850



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


        self.camera_manager = CameraManager()

        self.roi_detector = ROICardDetector()

        self.recognition_service = RecognitionService()


        self.roi_ready = False

        self.capture_done = False

        self.card_detected_time = None


        self.camera_timer = QTimer()

        self.camera_timer.timeout.connect(
            self.update_camera
        )


        self.last_time = time.time()

        self.frame_count = 0


        self.create_menu()

        self.create_ui()

        self.load_cameras()



    def create_menu(self):

        self.menuBar().addMenu(
            "Plik"
        )

        self.menuBar().addMenu(
            "Kamera"
        )

        self.menuBar().addMenu(
            "Narzędzia"
        )

        self.menuBar().addMenu(
            "Widok"
        )

        self.menuBar().addMenu(
            "Pomoc"
        )
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


        self.recognition_panel = RecognitionPanel()


        splitter.addWidget(
            self.recognition_panel
        )


        splitter.setSizes(
            [
                350,
                900
            ]
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



    def update_camera(self):

        frame = self.camera_manager.read()


        if frame is None:

            return


        display_frame = frame.copy()


        frame_height, frame_width = frame.shape[:2]


        w = SCAN_WIDTH

        h = SCAN_HEIGHT


        x = (frame_width - w) // 2

        y = (frame_height - h) // 2


        cv2.rectangle(
            display_frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )


        try:

            roi = frame[
                y:y + h,
                x:x + w
            ]


            if not self.roi_ready:

                self.roi_detector.set_reference(
                    roi
                )

                self.roi_ready = True

                print(
                    "ROI PUSTE ZAPISANE"
                )


            card_present = self.roi_detector.check_card(
                roi
            )


            print(
                "ROI KARTA:",
                card_present
            )


            if card_present:

                if AUTO_CAPTURE_ENABLED:

                    if self.card_detected_time is None:

                        self.card_detected_time = time.time()


                    elapsed = time.time() - self.card_detected_time


                    print(
                        "STABILIZACJA:",
                        round(elapsed, 2)
                    )


                    if elapsed >= CAPTURE_DELAY:

                        if not self.capture_done:

                            self.capture_done = True

                            self.save_card_image(
                                roi
                            )

                            print(
                                "KARTA ZAPISANA"
                            )

                            self.reset_scanner()


            else:

                self.card_detected_time = None


        except Exception as e:

            print(
                "BŁĄD SKANERA:",
                e
            )


        self.camera_widget.set_frame(
            display_frame
        )


        self.frame_count += 1


        now = time.time()


        if now - self.last_time >= 1:

            fps = self.frame_count

            self.frame_count = 0

            self.last_time = now

            self.fps_label.setText(
                f"FPS: {fps}"
            )
    def stop_camera(self):

        self.camera_timer.stop()

        self.camera_manager.close()

        self.status.showMessage(
            "🔴 Kamera zatrzymana"
        )



    def save_card_image(self, roi):

        if roi is None:

            return False


        image = self.roi_detector.get_card_image(
            roi
        )


        if image is None:

            return False


        filename = r"C:\ABS\Code\scans\last_card.jpg"


        result = cv2.imwrite(
            filename,
            image
        )


        print(
            "ZAPIS KARTY:",
            filename,
            result
        )


        if result:

            SoundPlayer.play_camera_click()


            self.status.showMessage(
                "📸 Zdjęcie zapisane"
            )


            recognition = self.recognition_service.recognize_card(
                filename
            )


            print(
                "\n======================"
            )

            print(
                "ROZPOZNANIE KARTY:"
            )

            print(
                recognition
            )

            print(
                "======================\n"
            )


            self.recognition_panel.show_result(
                recognition
            )


        return result



    def reset_scanner(self):

        self.card_detected_time = None

        self.capture_done = False

        self.roi_detector.reset()


        print(
            "SKANER ZRESETOWANY"
        )



    def closeEvent(self, event):

        try:

            self.camera_timer.stop()

            self.camera_manager.close()


        except Exception as e:

            print(
                "BŁĄD ZAMYKANIA:",
                e
            )


        event.accept()



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