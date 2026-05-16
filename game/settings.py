from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import QWindow
from PyQt5.QtCore import Qt
import sys

class Settings(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(400, 400, 800, 800)

        central = QWidget(self)
        central.setObjectName("Widget")
        self.setCentralWidget(central)

        # Фон
        self.setObjectName("Widget")
        self.setStyleSheet("""
            QWidget#Widget {
                background-image: url(/home/Downloads/braw_stars/game/settings.png);
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
        
        back_button = QPushButton('← НАЗАД')
        back_button.setStyleSheet('''
                                    QPushButton {
                                        background-color: #757575; color: white;
                                        border-radius: 18px; font-size: 22px;
                                        font-weight: bold; min-width: 320px; min-height: 65px;
                                    }
                                    QPushButton:hover { background-color: #616161; }
                                ''')
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        colors = {
            'training': ('#2da8ff', '#1b8fe6'),
            'brawl':    ('#e53935', '#d32f2f'),
            'solo':     ('#9c27b0', '#8e24aa'),
            'duo':      ('#43a047', '#388e3c'),
    }
    
        for label, mode in [('TRAINING','training'),('BRAWL','brawl'),
                            ('SOLO','solo'),('DUO','duo')]:
            bg, hover = colors[mode]
            btn = QPushButton(label)
            btn.setMinimumSize(320, 75)
            btn.setStyleSheet(f'''
                QPushButton {{ background-color:{bg}; color:white;
                    border-radius:18px; font-size:26px; font-weight:bold; }}
                QPushButton:hover {{ background-color:{hover}; }}
            ''')
            btn.clicked.connect(lambda _, m=mode: self.start_mode(m))
            layout.addWidget(btn, alignment=Qt.AlignCenter)

        
            def go_back(self):
                from start_screen import StartScreen
                self.start = StartScreen()
                self.start.show()
                self.close()

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
