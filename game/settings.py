from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import QWindow
from PyQt5.QtCore import Qt
import sys

class StartScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Braw Starts")
        self.setGeometry(400, 400, 800, 800)

        central = QWidget(self)
        central.setObjectName("Widget")
        self.setCentralWidget(central)

        # Фон
        self.setObjectName("Widget")
        self.setStyleSheet("""
            QWidget#Widget {
                background-image: url(/home/ana/Downloads/braw_stars/game/start_screen.png);
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            } 
        """)

        sound_button = QPushButton("SETTINGS")
        sound_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: #43a047;
                                        color: white;
                                        border: none;
                                        border-radius: 18px;
                                        font-size: 26px;
                                        font-weight: bold;
                                        min-width: 320px;
                                        min-height: 75px;
                                    }
                                    QPushButton:hover {
                                        background-color: #388e3c;
                                    }
                                    QPushButton:pressed {
                                        background-color: #1b5e20;
                                    }
                                    """)
        # Layout
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 185, 0, 0)
        layout.addWidget(sound_button, alignment=Qt.AlignCenter)

        
    def open_menu(self):
        from game_menu import GameMenu
        self.menu = GameMenu()
        self.menu.show()
        self.close()
