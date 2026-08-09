# ============================================================
# Artysta Break Studio
# Main Window v2.2
# Camera + Detector + Stable Auto Capture
# ============================================================


import time
import sys
import cv2


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



# ============================================================
# USTAWIENIA SKANERA
# ============================================================


AUTO_CAPTURE_ENABLED = True


# czas stabilizacji karty przed zapisem

CAPTURE_DELAY = 2.0



# Rozmiar ramki skanowania karty

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



        # Kamera

        self.camera_manager = CameraManager()



        # Detector

        self.card_detector = CardDetector()



        # Auto Capture state

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
            # --------------------------------------------------
    # MENU
    # --------------------------------------------------


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



    # --------------------------------------------------
    # UI
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
    # KAMERY
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
    # START KAMERY
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
    # GŁÓWNY SKANER
    # --------------------------------------------------


    def update_camera(self):

        frame = self.camera_manager.read()



        if frame is None:

            return



        display_frame = frame.copy()



        # automatyczne wyśrodkowanie ramki


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
                y:y+h,
                x:x+w
            ]



            result = self.card_detector.detect(
                roi
            )



            if result is not None:


                warped, corners, score = result



                if corners is not None:


                    cv2.putText(
                        display_frame,
                        f"CARD FOUND {int(score)}%",
                        (30,60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0,255,0),
                        3
                    )
                                        

                    # stabilizacja przed zapisem

                    if AUTO_CAPTURE_ENABLED:
                        print("AUTO CAPTURE WESZLO")
                        print("AUTO CAPTURE AKTYWNE")


                        if self.card_detected_time is None:

                            self.card_detected_time = time.time()



                        elapsed = time.time() - self.card_detected_time
                        print("CZEKAM:", elapsed)
                        

                        if elapsed >= CAPTURE_DELAY:
                            


                            # przesunięcie ROI -> pełny obraz

                            print("CORNERS ROI:", corners)

                            x2, y2, w2, h2 = cv2.boundingRect(
                            corners.astype("int32")
                            )

                            card_image = roi[
                            y2:y2+h2,
                            x2:x2+w2
                            ]

                            print("POBRANO OBRAZ KARTY:", card_image is not None)



                            if card_image is not None:


                                saved = self.card_detector.save_card(
                                    card_image,
                                    "last_card.jpg"
                                )
                                print("ZAPIS WYNIK:", saved)



                                if saved:


                                    self.capture_done = True



                                    self.status.showMessage(
                                        "🟢 Karta zapisana: last_card.jpg"
                                    )



            else:

                # karta zniknęła - reset licznika

                self.card_detected_time = None



        except Exception as e:

            print(
                "BŁĄD SKANERA:",
                e
            )



        # pokazujemy obraz kamery


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
    # STOP KAMERY
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



