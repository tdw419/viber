
import unittest
import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

app = QApplication(sys.argv)

class TestGUI(unittest.TestCase):

    def test_main_window(self):
        """Test the main window."""
        window = MainWindow()
        self.assertEqual(window.label.text(), 'Hello, LLM OS!')
        window.button.click()
        self.assertEqual(window.label.text(), 'Button Clicked!')

if __name__ == '__main__':
    unittest.main()
