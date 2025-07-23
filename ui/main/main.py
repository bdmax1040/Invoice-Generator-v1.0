from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self, config, env):
        super().__init__()
        self.setWindowTitle("Invoice Generator - Main Window")
        self.setFixedSize(800, 600)

        label = QLabel("Main application window")
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)