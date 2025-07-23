from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

class PreferencesPage(QWidget):
    def __init__(self, config, next_callback, back_callback):
        super().__init__()
        self.config = config
        self.next_callback = next_callback
        self.back_callback = back_callback

        self.setObjectName("content")

        self.setup_layout()

    def setup_layout(self):
        layout = QVBoxLayout()
        row1 = QHBoxLayout()  # Reserved for future content
        row2 = QHBoxLayout()  # Reserved for future content
        row3 = QHBoxLayout()  # Reserved for navigation buttons

        layout.addSpacing(100)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addSpacing(100)

        self.setLayout(layout)