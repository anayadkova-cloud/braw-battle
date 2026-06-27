import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QLabel, QComboBox, QSlider, QHBoxLayout)
from PyQt5.QtGui import QFont

from config import Config
from sound_manager import SoundManager


# --- ПРЕИЗПОЛЗВАЕМ КЛАС ЗА БУТОН ---
class MenuButton(QPushButton):
    def __init__(self, text, base_color, hover_color, pressed_color=None):
        super().__init__(text)
        
        if not pressed_color:
            pressed_color = hover_color

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {base_color};
                color: white;
                border: none;
                border-radius: 18px;
                font-size: 26px;
                font-weight: bold;
                min-width: 320px;
                min-height: 75px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
        """)


# --- ЕКРАН НАСТРОЙКИ ---
class Settings(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(400, 400, 800, 800)

        # Получаваме глобалните настройки
        self.config = Config()
        self.sound_manager = SoundManager()

        # Централен контейнер
        central = QWidget(self)
        central.setObjectName("Widget")
        self.setCentralWidget(central)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path  = os.path.join(base_dir, 'players.png').replace('\\', '/')

        # Фоново изображение
        self.setStyleSheet(f"""
            QWidget#Widget {{
                background-image: url('{bg_path}');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }}
        """)

        # --- СЪЗДАВАНЕ НА ЛЕЙАУТА ПЪРВО ---
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 80, 50, 50)

        # --- ЗВУК НАСТРОЙКА ---
        sound_layout = QHBoxLayout()
        sound_label = QLabel("SOUND:")
        sound_label.setFont(QFont("Arial", 18, QFont.Bold))
        sound_label.setStyleSheet("color: white; background-color: rgba(0,0,0,100); padding: 10px; border-radius: 5px;")
        sound_label.setFixedWidth(150)
        
        self.sound_button = MenuButton(
            "ON" if self.config.get('sound_enabled') else "OFF",
            "#43a047" if self.config.get('sound_enabled') else "#d32f2f",
            "#388e3c" if self.config.get('sound_enabled') else "#c62828",
            "#1b5e20" if self.config.get('sound_enabled') else "#b71c1c"
        )
        self.sound_button.setFixedSize(200, 70)
        self.sound_button.clicked.connect(self.toggle_sound)
        
        sound_layout.addWidget(sound_label)
        sound_layout.addWidget(self.sound_button)
        sound_layout.addStretch()
        layout.addLayout(sound_layout)

        # --- BRIGHTNESS НАСТРОЙКА ---
        brightness_layout = QHBoxLayout()
        brightness_label = QLabel("BRIGHTNESS:")
        brightness_label.setFont(QFont("Arial", 18, QFont.Bold))
        brightness_label.setStyleSheet("color: white; background-color: rgba(0,0,0,100); padding: 10px; border-radius: 5px;")
        brightness_label.setFixedWidth(200)
        
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(50)
        self.brightness_slider.setMaximum(150)
        self.brightness_slider.setValue(self.config.get('brightness', 100))
        self.brightness_slider.setFixedWidth(250)
        self.brightness_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: rgba(200, 200, 200, 150);
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)
        
        self.brightness_value_label = QLabel(f"{self.config.get('brightness', 100)}%")
        self.brightness_value_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.brightness_value_label.setStyleSheet("color: white; background-color: rgba(0,0,0,100); padding: 5px; border-radius: 5px; min-width: 50px;")
        
        self.brightness_slider.valueChanged.connect(self.on_brightness_changed)
        
        brightness_layout.addWidget(brightness_label)
        brightness_layout.addWidget(self.brightness_slider)
        brightness_layout.addWidget(self.brightness_value_label)
        brightness_layout.addStretch()
        layout.addLayout(brightness_layout)

        # --- RESOLUTION НАСТРОЙКА ---
        resolution_layout = QHBoxLayout()
        resolution_label = QLabel("RESOLUTION:")
        resolution_label.setFont(QFont("Arial", 18, QFont.Bold))
        resolution_label.setStyleSheet("color: white; background-color: rgba(0,0,0,100); padding: 10px; border-radius: 5px;")
        resolution_label.setFixedWidth(200)
        
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(self.config.available_resolutions)
        self.resolution_combo.setCurrentText(self.config.get('resolution', '800x600'))
        self.resolution_combo.setFixedWidth(150)
        self.resolution_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border: 2px solid #2196F3;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QComboBox:hover {
                background-color: #f0f0f0;
            }
        """)
        self.resolution_combo.currentTextChanged.connect(self.on_resolution_changed)
        
        resolution_layout.addWidget(resolution_label)
        resolution_layout.addWidget(self.resolution_combo)
        resolution_layout.addStretch()
        layout.addLayout(resolution_layout)

        layout.addSpacing(20)

        # Бутон за връщане назад
        back_button = MenuButton('← НАЗАД', '#757575', '#616161', '#424242')
        back_button.setFixedSize(200, 70)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

    # --- ЛОГИКА ---
    def toggle_sound(self):
        current_enabled = self.config.get('sound_enabled', False)
        new_enabled = not current_enabled

        self.config.set('sound_enabled', new_enabled)
        self.sound_manager.toggle_sound(new_enabled)

        # Пускаме звук при натискане
        self.sound_manager.play_sound("click")

        # Обновяване на бутона
        button_text = "ON" if new_enabled else "OFF"
        button_color = "#43a047" if new_enabled else "#d32f2f"
        button_hover = "#388e3c" if new_enabled else "#c62828"
        button_pressed = "#1b5e20" if new_enabled else "#b71c1c"

        self.sound_button.setText(button_text)
        self.sound_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_color};
                color: white;
                border: none;
                border-radius: 18px;
                font-size: 26px;
                font-weight: bold;
                min-width: 200px;
                min-height: 70px;
            }}
            QPushButton:hover {{
                background-color: {button_hover};
            }}
            QPushButton:pressed {{
                background-color: {button_pressed};
            }}
        """)


    def on_brightness_changed(self, value):
        """Обновя яркостта"""
        self.config.set_brightness(value)
        self.brightness_value_label.setText(f"{value}%")

    def on_resolution_changed(self, text):
        """Обновя разделителната способност"""
        self.config.set_resolution(text)

    def go_back(self):
        from start_screen import StartScreen
        self.start = StartScreen()
        self.start.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Settings()
    window.show()
    sys.exit(app.exec_())