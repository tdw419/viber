
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import pyqtSignal

class SearchWidget(QWidget):
    """
    A widget for entering a search query and initiating a search.
    """
    search_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.query_input = QLineEdit(self)
        layout.addWidget(self.query_input)

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.on_search_clicked)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def on_search_clicked(self):
        query = self.query_input.text()
        self.search_clicked.emit(query)
