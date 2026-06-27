import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel)
from PyQt5.QtGui import QFont
 
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
        central.setObjectName('ShopWidget')
        self.setCentralWidget(central)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(base_dir, 'players.png').replace('\\', '/')
        
        self.setStyleSheet(f"""
            QWidget#ShopWidget {{
                background-image: url('{bg_path}');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }}
        """)
        
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        layout.setContentsMargins(50, 100, 50, 50)
 
        title = QLabel('SHOP')
        title.setFont(QFont('Arial', 32, QFont.Bold))
        title.setStyleSheet('color: white; background-color: rgba(0,0,0,150); padding: 10px; border-radius: 5px;')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.coins_label = QLabel(f'Монети: {self.coins}')
        self.coins_label.setStyleSheet('font-size: 24px; font-weight: bold; color: gold; background-color: rgba(0,0,0,150); padding: 10px; border-radius: 5px;')
        self.coins_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.coins_label, alignment=Qt.AlignCenter)
        
        layout.addSpacing(20)
 
        for item in self.ITEMS:
            row = QHBoxLayout()
            
            btn = QPushButton(f"{item['name']} ({item['desc']}) — {item['price']}")
            btn.setFont(QFont('Arial', 14, QFont.Bold))
            btn.setFixedHeight(60)
            btn.setEnabled(not self.upgrades.get(item['key'], False))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                }
                QPushButton:hover:enabled {
                    background-color: #1976D2;
                }
                QPushButton:disabled {
                    background-color: #90CAF9;
                    color: #E0E0E0;
                }
            """)
            btn.clicked.connect(lambda _, k=item['key'], p=item['price']: self.buy_item(k, p))
            row.addWidget(btn)
            layout.addLayout(row)
 
        layout.addSpacing(20)
        
        back_button = QPushButton('← НАЗАД')
        back_button.setFont(QFont('Arial', 14, QFont.Bold))
        back_button.setFixedHeight(60)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
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