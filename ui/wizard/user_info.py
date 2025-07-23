from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QLineEdit, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QGuiApplication, QPen
from PyQt6.QtCore import Qt, QRect
import os
import shutil


class UserInfoPage(QWidget):
    def __init__(self, config, next_callback):
        super().__init__()
        self.config = config
        self.next_callback = next_callback
        self.setObjectName("content")

        self.logo_path = None
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "config.json")
        self.assets_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "assets", "user-logo.png")
        self.setup_ui()
        self.load_user_data()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

        # Logo Preview Section
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(100, 100)
        self.logo_label.setObjectName("logoPreview")
        self.logo_label.setStyleSheet("border-radius: 50px; background-color: #ccc;")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.select_logo_btn = QPushButton("Select Logo")
        self.select_logo_btn.setObjectName("selectLogoButton")
        self.select_logo_btn.clicked.connect(self.select_logo)

        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        logo_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        logo_layout.addWidget(self.select_logo_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Input Fields Section
        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText("Full Name")
        self.full_name_input.setObjectName("inputField")

        self.company_name_input = QLineEdit()
        self.company_name_input.setPlaceholderText("Company Name (Optional)")
        self.company_name_input.setObjectName("inputField")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.email_input.setObjectName("inputField")

        inputs_layout = QVBoxLayout()
        inputs_layout.addWidget(self.full_name_input)
        inputs_layout.addWidget(self.company_name_input)
        inputs_layout.addWidget(self.email_input)

        # Button Footer Section
        self.next_button = QPushButton("Next")
        self.next_button.setObjectName("wizardNextButton")
        self.next_button.clicked.connect(self.handle_next)

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(self.next_button)

        # Combine all sections
        self.layout.addLayout(logo_layout)
        self.layout.addSpacing(20)
        self.layout.addLayout(inputs_layout)
        self.layout.addStretch()
        self.layout.addLayout(button_row)

    def select_logo(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select Logo", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.logo_path = file_path
            self.update_logo_preview(file_path)

            # Copy to internal assets
            dest_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "assets", "user-logo.png")
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copyfile(file_path, dest_path)

    def update_logo_preview(self, image_path):
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        masked_pixmap = QPixmap(100, 100)
        masked_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(masked_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Prepare circular mask
        path = QPainterPath()
        path.addEllipse(0, 0, 100, 100)
        painter.setClipPath(path)

        # Draw image clipped to circle
        painter.drawPixmap(0, 0, pixmap)

        # Draw white border inside the circle
        pen = QPen(Qt.GlobalColor.white, 2)  # 2px white border
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(1, 1, 98, 98)  # offset inward by 1px
        painter.end()

        self.logo_label.setPixmap(masked_pixmap)
    def load_user_data(self):
        import json
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                data = json.load(f)
                user_info = data.get("user_info", {})
                self.full_name_input.setText(user_info.get("full_name", ""))
                self.company_name_input.setText(user_info.get("company_name", ""))
                self.email_input.setText(user_info.get("email", ""))

        if os.path.exists(self.assets_path):
            self.update_logo_preview(self.assets_path)

    def save_user_data(self):
        import json
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                data = json.load(f)
        else:
            data = {}

        data["user_info"] = {
            "full_name": self.full_name_input.text(),
            "company_name": self.company_name_input.text(),
            "email": self.email_input.text()
        }

        with open(self.data_path, "w") as f:
            json.dump(data, f, indent=4)

    def handle_next(self):
        self.save_user_data()
        self.next_callback()

    def mousePressEvent(self, event):
        QWidget.clearFocus(self)
        for child in self.findChildren(QWidget):
            child.clearFocus()
        super().mousePressEvent(event)