
from PyQt5.QtWidgets import QPushButton, QLabel, QSlider

# This file is for custom widget definitions.
# For now, we'll just define some simple widgets that we can use in the main window.

class MyButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)

class MyLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)

class MySlider(QSlider):
    def __init__(self):
        super().__init__()
