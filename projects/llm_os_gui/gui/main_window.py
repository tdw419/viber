
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from projects.llm_os_gui.gui.table_view import TableView, PandasModel
from projects.llm_os_core import db
import pandas as pd
from projects.llm_os_gui.gui.widgets.connection import ConnectionWidget
from projects.llm_os_gui.gui.widgets.search import SearchWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LLM OS GUI')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.connection_widget = ConnectionWidget(self)
        self.connection_widget.connect_clicked.connect(self.connect_to_db)
        self.connection_widget.table_selected.connect(self.on_table_selected)
        layout.addWidget(self.connection_widget)

        self.search_widget = SearchWidget(self)
        self.search_widget.search_clicked.connect(self.search_table)
        layout.addWidget(self.search_widget)
        
        self.table_view = TableView(pd.DataFrame()) # Start with an empty table
        layout.addWidget(self.table_view)

        self.setLayout(layout)
        self.show()

    def connect_to_db(self):
        """Connects to the LanceDB database and populates the table combo box."""
        try:
            table_names = db.get_tables(db.DB_URI)
            self.connection_widget.add_tables(table_names)
        except Exception as e:
            print(f"Error connecting to DB: {e}")

    def on_table_selected(self, table_name):
        """Called when a table is selected in the combo box."""
        if table_name:
            try:
                df = db.get_table_contents(db.DB_URI, table_name)
                self.table_view.setModel(PandasModel(df))
            except Exception as e:
                print(f"Error getting table contents: {e}")

    def search_table(self, query):
        """Called when the search button is clicked."""
        table_name = self.connection_widget.get_selected_table()
        if table_name and query:
            try:
                df = db.search_table(db.DB_URI, table_name, query)
                self.table_view.setModel(PandasModel(df))
            except Exception as e:
                print(f"Error searching table: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
