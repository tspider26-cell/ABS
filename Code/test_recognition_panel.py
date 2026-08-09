from PySide6.QtWidgets import QApplication

from widgets.recognition_panel import RecognitionPanel


import sys

app = QApplication(sys.argv)


panel = RecognitionPanel()


panel.show_result({"card": "my_first_card.jpg", "score": 100})


panel.resize(400, 300)


panel.show()


sys.exit(app.exec())
