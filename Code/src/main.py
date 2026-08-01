
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Artysta Break Studio")
        self.resize(1000, 600)

        label = QLabel(
            "Artysta Break Studio\n\n"
            "Build 0.03 - Studio\n\n"
            "Status: READY",
            alignment=Qt.AlignCenter,
        )
        self.setCentralWidget(label)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
