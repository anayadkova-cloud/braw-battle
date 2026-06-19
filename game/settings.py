import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget


# --- ПРЕИЗПОЛЗВАЕМ КЛАС ЗА БУТОН ---
class MenuButton(QPushButton):
    def __init__(self, text, base_color, hover_color, pressed_color=None):
        super().__init__(text)
        
        # Ако не е подаден цвят при натискане, генерираме го автоматично (малко по-тъмен)
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

        # Централен контейнер
        central = QWidget(self)
        central.setObjectName("Widget")
        self.setCentralWidget(central)

        # Фоново изображение
        self.setStyleSheet("""
            QWidget#Widget {
                background-image: url(/home/Downloads/braw_stars/game/settings.png);
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            } 
        """)

        # --- СЪЗДАВАНЕ НА ЛЕЙАУТА ПЪРВО ---
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 185, 0, 20)

        # --- СЪЗДАВАНЕ НА БУТОНИТЕ ---
        sound_button = MenuButton("SOUND: ON/OFF", "#43a047", "#388e3c", "#1b5e20")
        layout.addWidget(sound_button, alignment=Qt.AlignCenter)

        # Цветове за различните режими (ако са необходими тук)
        colors = {
            'training': ('#2da8ff', '#1b8fe6'),
            'brawl':    ('#e53935', '#d32f2f'),
            'solo':     ('#9c27b0', '#8e24aa'),
            'duo':      ('#43a047', '#388e3c'),
        }
    
        # Генериране на бутоните за режими
        for label, mode in [('TRAINING', 'training'), ('BRAWL', 'brawl'),
                            ('SOLO', 'solo'), ('DUO', 'duo')]:
            bg, hover = colors[mode]
            btn = MenuButton(label, bg, hover)
            btn.clicked.connect(lambda _, m=mode: self.start_mode(m))
            layout.addWidget(btn, alignment=Qt.AlignCenter)

        # Бутон за връщане назад
        back_button = MenuButton('← НАЗАД', '#757575', '#616161', '#424242')
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

    # --- НАВИГАЦИЯ И ЛОГИКА ---
    def go_back(self):
        from start_screen import StartScreen
        self.start = StartScreen()
        self.start.show()
        self.close()

    def start_mode(self, mode):
        print(f"Стартиране на режим: {mode}")
        # Тук добави логиката за стартиране на конкретния режим

    def open_menu(self):
        from game_menu import GameMenu
        self.menu = GameMenu()
        self.menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Settings()
    window.show()
    sys.exit(app.exec_())