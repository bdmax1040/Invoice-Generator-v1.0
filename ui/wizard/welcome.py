from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
import os
import json

class WelcomePage(QWidget):
    def __init__(self, config, next_callback):
        super().__init__()
        self.next_callback = next_callback
        self.setObjectName("content")

        self.config = config
        self.accent_colour = self.config.get("theme", {}).get("accent_colour", "#FF3E3E")

        # UI Elements
        self.title = QLabel("Welcome to Invoice Generator")
        self.title.setObjectName("title")

        self.text1 = QLabel("Let's get you set up!")
        self.text1.setObjectName("text1")

        self.button1 = QPushButton("Get Started")
        self.button1.setObjectName("button1")
        self.button1.clicked.connect(self.next_callback)

        # Layout setup
        self.setup_layout()

        # Animations
        self.apply_animations()

    def setup_layout(self):
        layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        row1.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        row2.addWidget(self.text1, alignment=Qt.AlignmentFlag.AlignCenter)
        row3.addWidget(self.button1, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(150)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addSpacing(100)

        self.setLayout(layout)

    def apply_animations(self):
        pass  # Animations temporarily removed
