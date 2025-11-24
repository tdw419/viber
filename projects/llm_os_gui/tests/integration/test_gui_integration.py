
import unittest
import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

app = QApplication(sys.argv)

class TestGUIIntegration(unittest.TestCase):

    def test_app_startup(self):
        """Test that the application starts up without errors."""
        try:
            window = MainWindow()
            window.close()
        except Exception as e:
            self.fail(f"Application startup failed with an exception: {e}")

if __name__ == '__main__':
    unittest.main()
