
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,
    QLabel,QComboBox,QPushButton,QFrame,QSplitter,QGroupBox,QStatusBar
)
from theme import DARK_THEME
from camera_manager import CameraManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Artysta Break Studio")
        self.resize(1400,900)
        self.setStyleSheet(DARK_THEME)

        self.menuBar().addMenu("Plik")
        self.menuBar().addMenu("Kamera")
        self.menuBar().addMenu("Narzędzia")
        self.menuBar().addMenu("Widok")
        self.menuBar().addMenu("Pomoc")

        cm=CameraManager()

        central=QWidget()
        self.setCentralWidget(central)
        layout=QVBoxLayout(central)

        top=QHBoxLayout()
        top.addWidget(QLabel("Kamera:"))
        combo=QComboBox()
        cams=cm.available_cameras()
        if cams:
            for c in cams:
                combo.addItem(f"Kamera {c}", c)
        else:
            combo.addItem("Brak wykrytej kamery")
        top.addWidget(combo)
        top.addWidget(QPushButton("Start"))
        top.addWidget(QPushButton("Stop"))
        top.addStretch()
        top.addWidget(QLabel("FPS: 0"))
        layout.addLayout(top)

        frame=QFrame()
        pv=QVBoxLayout(frame)
        lbl=QLabel("PODGLĄD KAMERY")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setMinimumHeight(500)
        pv.addWidget(lbl)
        layout.addWidget(frame)

        split=QSplitter()
        split.addWidget(QGroupBox("Historia sesji"))
        split.addWidget(QGroupBox("Rozpoznana karta"))
        layout.addWidget(split)

        sb=QStatusBar()
        sb.showMessage("🟢 GOTOWY | ABS v0.2")
        self.setStatusBar(sb)

def main():
    app=QApplication(sys.argv)
    w=MainWindow()
    w.show()
    sys.exit(app.exec())
