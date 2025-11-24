
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtCore import pyqtSignal

class ConnectionWidget(QWidget):
    """
    A widget for connecting to the database and selecting a table.
    """
    table_selected = pyqtSignal(str)
    connect_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.connect_button = QPushButton("Connect to DB", self)
        self.connect_button.clicked.connect(self.connect_clicked.emit)
        layout.addWidget(self.connect_button)

        self.table_combo = QComboBox(self)
        self.table_combo.currentIndexChanged.connect(self.on_table_selected)
        layout.addWidget(self.table_combo)

        self.setLayout(layout)

    def on_table_selected(self, index):
        table_name = self.table_combo.itemText(index)
        if table_name:
            self.table_selected.emit(table_name)

    def add_tables(self, tables):
        self.table_combo.clear()
        self.table_combo.addItems(tables)

    def get_selected_table(self):
        return self.table_combo.currentText()
