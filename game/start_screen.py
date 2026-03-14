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

        play_button = QPushButton("PLAY")
        play_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: #2da8ff;
                                        color: white;
                                        border: none;
                                        border-radius: 18px;
                                        font-size: 26px;
                                        font-weight: bold;
                                        min-width: 320px;
                                        min-height: 75px;
                                    }
                                    QPushButton:hover {
                                        background-color: #1b8fe6;
                                    }
                                    QPushButton:pressed {
                                        background-color: #136fb3;
                                    }
                                    """)
        

        braw_button = QPushButton("BRAW")
        braw_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: #e53935;
                                        color: white;
                                        border: none;
                                        border-radius: 18px;
                                        font-size: 26px;
                                        font-weight: bold;
                                        min-width: 320px;
                                        min-height: 75px;
                                    }
                                    QPushButton:hover {
                                        background-color: #d32f2f;
                                    }
                                    QPushButton:pressed {
                                        background-color: #b71c1c;
                                    }
                                    """)
        
        shop_button = QPushButton("SHOP")
        shop_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: #9c27b0;
                                        color: white;
                                        border: none;
                                        border-radius: 18px;
                                        font-size: 26px;
                                        font-weight: bold;
                                        min-width: 320px;
                                        min-height: 75px;
                                    }
                                    QPushButton:hover {
                                        background-color: #8e24aa;
                                    }
                                    QPushButton:pressed {
                                        background-color: #6a1b9a;
                                    }
                                    """)
        
        settings_button = QPushButton("SETTINGS")
        settings_button.setStyleSheet("""
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
        layout.addWidget(play_button, alignment=Qt.AlignCenter)
        layout.addWidget(braw_button, alignment=Qt.AlignCenter)
        layout.addWidget(shop_button, alignment=Qt.AlignCenter)
        layout.addWidget(settings_button, alignment=Qt.AlignCenter)
        


    def open_menu(self):
        from game_menu import GameMenu
        self.menu = GameMenu()
        self.menu.show()
        self.close()
