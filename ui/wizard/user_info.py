from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

class UserInfoPage(QWidget):
    def __init__(self, config, next_callback):
        super().__init__()
        self.config = config
        self.next_callback = next_callback
        self.setObjectName("content")
        self.setup_layout()

    def setup_layout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)