import sys
import threading
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from braw_stars import start_game


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


# --- МЕНЮ ЗА ИГРАТА ---
class GameMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Braw Battle – Menu')
        self.setGeometry(400, 400, 800, 800)

        central = QWidget(self)
        central.setObjectName('Widget')
        self.setCentralWidget(central)

        # Бутоните ще ползват тези цветове (същите като в Settings)
        colors = {
            'training': ('#2da8ff', '#1b8fe6'),
            'brawl':    ('#e53935', '#d32f2f'),
            'solo':     ('#9c27b0', '#8e24aa'),
            'duo':      ('#43a047', '#388e3c'),
        }

        # Настройка на лейаута
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 20, 0, 20)

        # Динамично създаване на бутоните за различните режими
        for label, mode in [('TRAINING', 'training'), ('BRAWL', 'brawl'),
                            ('SOLO', 'solo'), ('DUO', 'duo')]:
            bg, hover = colors[mode]
            btn = MenuButton(label, bg, hover)
            btn.clicked.connect(lambda _, m=mode: self.start_mode(m))
            layout.addWidget(btn, alignment=Qt.AlignCenter)

        # Бутон за връщане назад
        back_btn = MenuButton('← НАЗАД', '#757575', '#616161', '#424242')
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

    # --- ЛОГИКА ---
    def start_mode(self, mode):
        self.close()
        # Стартиране на Pygame в отделен Thread, за да не замръзва PyQt
        t = threading.Thread(target=start_game, args=(mode,), daemon=True)
        t.start()

    def go_back(self):
        from start_screen import StartScreen
        self.start = StartScreen()
        self.start.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameMenu()
    window.show()
    sys.exit(app.exec_())