import sys
import os
import threading
from PyQt5.QtCore import Qt, QSize  
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy

from braw_stars import start_game


# --- ПРЕИЗПОЛЗВАЕМ КЛАС ЗА БУТОН ---
class MenuButton(QPushButton):
    def __init__(self, text, base_color, hover_color, pressed_color=None):
        super().__init__(text)
        if not pressed_color:
            pressed_color = hover_color

        


# --- МЕНЮ ЗА ИГРАТА ---
class GameMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Braw Battle – Menu')
        self.setGeometry(400, 400, 800, 800)

        central = QWidget(self)
        central.setObjectName('Widget')
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

        # Бутоните ще ползват тези цветове (същите като в Settings)
        mode_images = {
            #"training": "training_btn.png",
            "solo": "solo.png",
            #"duo": "duo_btn.png",
        }

        layout = QVBoxLayout(central)
        layout.setContentsMargins(100, 300, 40, 40)
        # Динамично създаване на бутоните за различните режими
        for mode, img_name in mode_images.items():
        # Правим точен път до картинката
            img_path = os.path.join(base_dir, img_name).replace("\\", "/")

            btn = QPushButton()  # Създаваме празен бутон
            btn.setIcon(QIcon(img_path))  # Слагаме картинката вътре
            btn.setIconSize(QSize(200, 200))  # Задаваме големина (ширина, височина)

            # Махаме рамките и сивия фон на бутона, за да се вижда само картинката
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent
                }
                QPushButton:hover {
                    opacity: 0.85;
                }
            """)

            btn.clicked.connect(lambda _, m=mode: self.start_mode(m))
            layout.addWidget(btn, alignment=Qt.AlignCenter)

            row_layout = QHBoxLayout()
            row_layout.addWidget(btn)
            # Добавяме пружина (Spacer) отдясно, която избутва бутона наляво
            row_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            
            layout.addLayout(row_layout)

        layout.addStretch(1)

        # Бутон за връщане назад
        back_btn = MenuButton('← НАЗАД', '#757575', '#616161', '#424242')
        back_btn.setFixedSize(140, 70) 
        back_btn.clicked.connect(self.go_back)
        
        # Центрираме го долу в ниското
        layout.addWidget(back_btn, alignment=Qt.AlignRight) 


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