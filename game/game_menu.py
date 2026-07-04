import sys
import os
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel

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

class GameMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Braw Battle – Menu')
        self.setGeometry(400, 400, 800, 800)

        central = QWidget(self)
        central.setObjectName('Widget')
        self.setCentralWidget(central)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(base_dir, 'players.png').replace('\\', '/')

        self.setStyleSheet(f"""
            QWidget#Widget {{
                background-image: url('{bg_path}');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }}
        """)

        mode_images = {
            "training": "training.png",
            "solo": "solo.png",
            "duo": "duo.png",
        }

        mode_descriptions = {
            "training": "TRAINING\nВремето: ∞\nСложност: Лека",
            "solo": "SOLO\nВремето: 90s\nСложност: Средна",
            "duo": "DUO\nВремето: 120s\nСложност: Висока",
        }

        layout = QVBoxLayout(central)
        layout.setContentsMargins(50, 250, 50, 50)
        layout.setSpacing(20)
        
        modes_layout = QHBoxLayout()
        modes_layout.setSpacing(20)
        modes_layout.setAlignment(Qt.AlignCenter)
        
        for mode, img_name in mode_images.items():
            mode_vbox = QVBoxLayout()
            mode_vbox.setSpacing(5)
            
            img_path = os.path.join(base_dir, img_name).replace("\\", "/")

            btn = QPushButton()
            if os.path.exists(img_path):
                btn.setIcon(QIcon(img_path))
            btn.setIconSize(QSize(150, 150))
            btn.setFixedSize(180, 200)

            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    padding: 5px;
                }
                QPushButton:hover {
                    opacity: 0.85;
                }
                QPushButton:pressed {
                    opacity: 0.7;
                }
            """)

            btn.clicked.connect(lambda _, m=mode: self.start_mode(m))
            mode_vbox.addWidget(btn, alignment=Qt.AlignCenter)
            
            desc_label = QLabel(mode_descriptions[mode])
            desc_label.setFont(QFont("Arial", 11, QFont.Bold))
            desc_label.setStyleSheet("""
                color: white;
                background-color: rgba(0, 0, 0, 150);
                padding: 8px;
                border-radius: 5px;
                text-align: center;
            """)
            desc_label.setAlignment(Qt.AlignCenter)
            mode_vbox.addWidget(desc_label)
            
            modes_layout.addLayout(mode_vbox)
        
        layout.addLayout(modes_layout)
        layout.addStretch(1)

        back_btn = MenuButton('← НАЗАД', '#757575', '#616161', '#424242')
        back_btn.setFixedSize(140, 70)
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

    def start_mode(self, mode):
        # ВАЖНО: pygame се стартира СИНХРОННО на главната нишка (не в threading.Thread),
        # за да получи истински OS фокус върху клавиатурата/мишката.
        self.hide()
        QApplication.processEvents()

        try:
            if mode == "training":
                from training_mode import start_training
                start_training()
            elif mode == "solo":
                from solo_mode import start_solo
                start_solo()
            elif mode == "duo":
                from duo_mode import start_duo
                start_duo()
        finally:
            self.show()

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