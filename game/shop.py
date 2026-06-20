import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel)
 
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shop_data.json')
 
 
class Shop(QMainWindow):
    ITEMS = [
        {'name': 'Extra HP',    'desc': '+50 HP',       'price': 50,  'key': 'hp'},
        {'name': 'Speed Boost', 'desc': '+2 скорост',   'price': 75,  'key': 'speed'},
        {'name': 'Rapid Fire',  'desc': 'Cooldown / 2', 'price': 100, 'key': 'rapid'},
    ]
 
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self.setWindowTitle('Braw Battle – Shop')
        self.setGeometry(400, 400, 800, 800)
 
        self.coins = 0
        self.upgrades = {}
        self.load_data()
 
        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
 
        self.coins_label = QLabel(f'Монети: {self.coins}')
        self.coins_label.setStyleSheet('font-size: 24px; font-weight: bold;')
        layout.addWidget(self.coins_label, alignment=Qt.AlignCenter)
 
        for item in self.ITEMS:
            row = QHBoxLayout()
            btn = QPushButton(f"{item['name']} ({item['desc']}) — {item['price']}")
            btn.setEnabled(not self.upgrades.get(item['key'], False))
            btn.clicked.connect(lambda _, k=item['key'], p=item['price']: self.buy_item(k, p))
            row.addWidget(btn)
            layout.addLayout(row)
 
        back_button = QPushButton('\u2190 НАЗАД')
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)
 
    def buy_item(self, key, price):
        if self.coins >= price:
            self.coins -= price
            self.upgrades[key] = True
            self.save_data()
            self.coins_label.setText(f'Монети: {self.coins}')
 
    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.coins = data.get('coins', 0)
                self.upgrades = data.get('upgrades', {})
 
    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({'coins': self.coins, 'upgrades': self.upgrades}, f)
 
    def go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

