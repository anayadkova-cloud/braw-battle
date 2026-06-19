class Shop(QMainWindow):
        ITEMS = [
            {'name': 'Extra HP',    'desc': '+50 HP',          'price': 50,  'key': 'hp'},
            {'name': 'Speed Boost', 'desc': '+2 скорост',      'price': 75,  'key': 'speed'},
            {'name': 'Rapid Fire',  'desc': 'Cooldown / 2',    'price': 100, 'key': 'rapid'},
        ]
    
        def buy_item(self, key, price):
            if self.coins >= price:
                self.coins -= price
                self.upgrades[key] = True
                self.save_data()

