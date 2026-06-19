import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from shop import Shop


# --- ПРЕИЗПОЛЗВАЕМ КЛАС ЗА БУТОН ---
class MenuButton(QPushButton):
    def __init__(self, text, base_color, hover_color, pressed_color):
        super().__init__(text)
        
        # Задаваме стила динамично чрез подадените цветове
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


# --- ГЛАВЕН ЕКРАН ---
class StartScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Braw Starts")
        self.setGeometry(400, 400, 800, 800)

        # Централен контейнер
        central = QWidget(self)
        central.setObjectName("Widget")
        self.setCentralWidget(central)

        # Фоново изображение
        self.setStyleSheet("""
            QWidget#Widget {
                background-image: url(/home/ana/Downloads/braw_stars/game/start_screen.png);
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            } 
        """)

        # --- СЪЗДАВАНЕ НА БУТОНИТЕ С НОВИЯ КЛАС ---
        # Подаваме: Текст, Основен цвят, Ховър цвят, Натиснат цвят
        play_button = MenuButton("PLAY", "#2da8ff", "#1b8fe6", "#136fb3")
        braw_button = MenuButton("BRAW", "#e53935", "#d32f2f", "#b71c1c")
        shop_button = MenuButton("SHOP", "#9c27b0", "#8e24aa", "#6a1b9a")
        settings_button = MenuButton("SETTINGS", "#43a047", "#388e3c", "#1b5e20")
        
        # --- СВЪРЗВАНЕ НА ФУНКЦИИ ---
        play_button.clicked.connect(self.open_menu)
        braw_button.clicked.connect(lambda: print('BRAW – скоро!'))
        shop_button.clicked.connect(self.open_shop)       
        settings_button.clicked.connect(self.open_settings)
    
        # --- LAYOUT ---
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 185, 0, 20)
        
        layout.addWidget(play_button, alignment=Qt.AlignCenter)
        layout.addWidget(braw_button, alignment=Qt.AlignCenter)
        layout.addWidget(shop_button, alignment=Qt.AlignCenter)
        layout.addWidget(settings_button, alignment=Qt.AlignCenter)

    # --- НАВИГАЦИЯ ---
    def open_shop(self):
        self.shop_win = Shop(self)
        self.shop_win.show()
        self.hide()

    def open_settings(self):
        from settings import Settings
        self.settings_win = Settings()
        self.settings_win.show()
        self.close()

    def open_menu(self):
        from game_menu import GameMenu
        self.menu = GameMenu()
        self.menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartScreen()
    window.show()
    sys.exit(app.exec_())