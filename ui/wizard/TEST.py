#Imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGraphicsOpacityEffect
import json
import os
import darkdetect


def darken_color(hex_color, factor=0.8):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = max(0, int(r * factor))
    g = max(0, int(g * factor))
    b = max(0, int(b * factor))
    return f"#{r:02X}{g:02X}{b:02X}"


# Main App Objects & Settings
app = QApplication([])
main_window = QWidget()
main_window.setFixedSize(600, 500)
main_window.setWindowFlags(Qt.FramelessWindowHint)  # Removes traffic light bar
main_window.setAttribute(Qt.WA_TranslucentBackground)  # Allows rounded corners

content = QWidget(main_window)
content.setObjectName("content")
content.setGeometry(0, 0, 600, 500)


# Create all App Objects
title = QLabel("Welcome to Invoice Generator")
title.setObjectName("title")

text1 = QLabel("Let's get you set up!")
text1.setObjectName("text1")

with open(os.path.join(os.path.dirname(__file__), "..", "..", "data", "config.json"), "r") as f:
    settings = json.load(f)
accent_colour = settings.get("theme", {}).get("accent_colour", "#FF3E3E")
accent_hover = darken_color(accent_colour)
background_colour = settings.get("theme", {}).get("background", "#ffffff")
border_colour = settings.get("theme", {}).get("border", "#cccccc")

# Detect system theme
theme_mode = "dark" if darkdetect.isDark() else "light"
style_file = f"{theme_mode}_wizard.qss"

style_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "styles", style_file)
with open(style_path, "r") as f:
    raw_style = f.read()
    style_sheet = (
        raw_style
        .replace("{{accent}}", accent_colour)
        .replace("{{accent_hover}}", accent_hover)
        .replace("{{background}}", background_colour)
        .replace("{{border}}", border_colour)
    )
    app.setStyleSheet(style_sheet)
button1 = QPushButton("Get Started")
button1.setObjectName("button1")


#All Design Here
master_layout = QVBoxLayout()

row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()

row1.addWidget(title, alignment=Qt.AlignCenter)
row2.addWidget(text1, alignment=Qt.AlignCenter)
row3.addWidget(button1, alignment=Qt.AlignCenter)

master_layout.addSpacing(150)
master_layout.addLayout(row1)
master_layout.addLayout(row2)
master_layout.addLayout(row3)
master_layout.addSpacing(100)

content.setLayout(master_layout)


#Functions
def button_clicked():
    app.quit()


# Theme change detection
current_theme_mode = "dark" if darkdetect.isDark() else "light"

def check_system_theme_change():
    global current_theme_mode
    new_theme_mode = "dark" if darkdetect.isDark() else "light"
    if new_theme_mode != current_theme_mode:
        current_theme_mode = new_theme_mode
        style_file = f"{new_theme_mode}_wizard.qss"
        style_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "styles", style_file)
        with open(style_path, "r") as f:
            raw_style = f.read()
            style_sheet = (
                raw_style
                .replace("{{accent}}", accent_colour)
                .replace("{{accent_hover}}", accent_hover)
                .replace("{{background}}", background_colour)
                .replace("{{border}}", border_colour)
            )
            app.setStyleSheet(style_sheet)


#Events
button1.clicked.connect(button_clicked)


#Animation
from PyQt5.QtCore import QPauseAnimation

for widget in [title, text1, button1]:
    effect = QGraphicsOpacityEffect()
    widget.setGraphicsEffect(effect)
    effect.setOpacity(0)

title_anim = QPropertyAnimation(title.graphicsEffect(), b"opacity")
title_anim.setDuration(800)
title_anim.setStartValue(0)
title_anim.setEndValue(1)
title_anim.setEasingCurve(QEasingCurve.InOutQuad)

text1_anim = QPropertyAnimation(text1.graphicsEffect(), b"opacity")
text1_anim.setDuration(800)
text1_anim.setStartValue(0)
text1_anim.setEndValue(1)
text1_anim.setEasingCurve(QEasingCurve.InOutQuad)

button_anim = QPropertyAnimation(button1.graphicsEffect(), b"opacity")
button_anim.setDuration(800)
button_anim.setStartValue(0)
button_anim.setEndValue(1)
button_anim.setEasingCurve(QEasingCurve.InOutQuad)

pause = QPauseAnimation(600)  # 300ms delay before the first animation

fade_sequence = QSequentialAnimationGroup()
fade_sequence.addAnimation(pause)
fade_sequence.addAnimation(title_anim)
fade_sequence.addAnimation(text1_anim)
fade_sequence.addAnimation(button_anim)
fade_sequence.start()

# Start timer to check for system theme changes
theme_check_timer = QTimer()
theme_check_timer.timeout.connect(check_system_theme_change)
theme_check_timer.start(1000)  # check every 1 second

#Show/Run App
screen = app.primaryScreen() # Find screen size
screen_geometry = screen.availableGeometry() # Find avalible screen
x = (screen_geometry.width() - main_window.width()) // 2 # Mid point calc
y = (screen_geometry.height() - main_window.height()) // 2 # Mid point calc
main_window.move(x, y) # Move window to mid-point for x & y

main_window.show()
app.exec_()