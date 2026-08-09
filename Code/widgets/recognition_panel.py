from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from PySide6.QtCore import Qt


class RecognitionPanel(QWidget):

    def __init__(self):

        super().__init__()

        self.layout = QVBoxLayout(self)

        self.title = QLabel("Rozpoznana karta")

        self.title.setAlignment(Qt.AlignCenter)

        self.card_label = QLabel("Brak karty")

        self.card_label.setAlignment(Qt.AlignCenter)

        self.score_label = QLabel("Score: -")

        self.score_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.title)

        self.layout.addWidget(self.card_label)

        self.layout.addWidget(self.score_label)

    def show_result(self, result):

        if not result:

            self.card_label.setText("Brak wyniku")

            self.score_label.setText("Score: -")

            return

        card = result.get("card", "Nieznana")

        score = result.get("score", 0)

        self.card_label.setText(f"Karta:\n{card}")

        self.score_label.setText(f"Score: {score}%")
