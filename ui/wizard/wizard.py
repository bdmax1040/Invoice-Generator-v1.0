from PyQt6.QtWidgets import QWidget, QStackedLayout, QApplication, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
import os
import json
import darkdetect

from ui.wizard.welcome import WelcomePage
from ui.wizard.user_info import UserInfoPage


def darken_color(hex_color, factor=0.8):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = max(0, int(r * factor))
    g = max(0, int(g * factor))
    b = max(0, int(b * factor))
    return f"#{r:02X}{g:02X}{b:02X}"


class WizardWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setFixedSize(600, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.current_theme_mode = "dark" if darkdetect.isDark() else "light"
        self.setup_styles()

        # Central content container
        self.content = QWidget(self)
        self.content.setObjectName("content")
        self.content.setGeometry(0, 0, 600, 500)

        # Stacked layout for wizard pages
        self.stack = QStackedLayout(self.content)
        self.stack.setContentsMargins(0, 0, 0, 0)

        # Load pages
        self.welcome_page = WelcomePage(self.config, self.go_to_next_page)
        self.stack.addWidget(self.welcome_page)
        self.user_info_page = UserInfoPage(self.config, self.go_to_next_page)
        self.stack.addWidget(self.user_info_page)
        self.stack.setCurrentWidget(self.welcome_page)

        # Timer to monitor system theme changes
        self.theme_check_timer = QTimer()
        self.theme_check_timer.timeout.connect(self.check_system_theme_change)
        self.theme_check_timer.start(1000)

        # Set main layout to host content widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.content)
        self.setLayout(main_layout)

        # Center the window on screen
        self.center_on_screen()

    def setup_styles(self):
        # Load colours from config
        theme = self.config.get("theme", {})
        accent = theme.get("accent_colour", "#FF3E3E")
        background = theme.get("background", "#ffffff")
        border = theme.get("border", "#cccccc")
        accent_hover = darken_color(accent)

        # Load appropriate QSS
        style_file = f"{self.current_theme_mode}_wizard.qss"
        style_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "styles", style_file)
        with open(style_path, "r") as f:
            raw_style = f.read()
            style_sheet = (
                raw_style
                .replace("{{accent}}", accent)
                .replace("{{accent_hover}}", accent_hover)
                .replace("{{background}}", background)
                .replace("{{border}}", border)
            )
            QApplication.instance().setStyleSheet(style_sheet)

    def check_system_theme_change(self):
        new_theme = "dark" if darkdetect.isDark() else "light"
        if new_theme != self.current_theme_mode:
            self.current_theme_mode = new_theme
            self.setup_styles()

    def go_to_next_page(self):
        self.stack.setCurrentWidget(self.user_info_page)

    def center_on_screen(self):
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
