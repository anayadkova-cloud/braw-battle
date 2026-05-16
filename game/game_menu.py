from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
    from PyQt5.QtCore import Qt
    import os
    
    class GameMenu(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Braw Battle – Menu')
            self.setGeometry(400, 400, 800, 800)
    
            central = QWidget(self)
            central.setObjectName('Widget')
            self.setCentralWidget(central)
    
            layout = QVBoxLayout(central)
            layout.setAlignment(Qt.AlignCenter)
            layout.setSpacing(15)
    
            for label, mode in [('TRAINING', 'training'), ('BRAWL', 'brawl'),
                                 ('SOLO', 'solo'), ('DUO', 'duo')]:
                btn = QPushButton(label)
                btn.setMinimumSize(320, 70)
                btn.clicked.connect(lambda _, m=mode: self.start_mode(m))
                layout.addWidget(btn, alignment=Qt.AlignCenter)
    
            back_btn = QPushButton('НАЗАД')
            back_btn.clicked.connect(self.go_back)
            layout.addWidget(back_btn, alignment=Qt.AlignCenter)
    
        def start_mode(self, mode):
            from braw_stars import start_game
            start_game(mode=mode)
    
        def go_back(self):
            from start_screen import StartScreen
            self.start = StartScreen()
            self.start.show()
            self.close()