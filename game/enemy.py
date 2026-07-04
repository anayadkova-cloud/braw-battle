import pygame, math, random, os
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, speed=2):
        super().__init__()
        self.speed = speed
        self.hp    = 50
        self.width = 45
        self.height = 45
    
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, 'enemy1.png')
        
        if os.path.exists(img_path):
            try:
                self.image = pygame.image.load(img_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            except:
                self.image = pygame.Surface((self.width, self.height))
                self.image.fill((229, 57, 53))  # ЧЕРВЕН
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((229, 57, 53))  # ЧЕРВЕН
    
        side = random.choice(['top','bottom','left','right'])
        if side == 'top':    x, y = random.randint(0,800),  0
        elif side == 'bottom': x, y = random.randint(0,800), 600
        elif side == 'left': x, y = 0,   random.randint(0,600)
        else:                x, y = 800, random.randint(0,600)
    
        self.rect = self.image.get_rect(center=(x, y))
    
        dx = player_x - x
        dy = player_y - y
        dist = math.hypot(dx, dy) or 1
        self.vx = dx / dist * self.speed
        self.vy = dy / dist * self.speed
    
    def update(self, player_x=0, player_y=0):
        dx = player_x - self.rect.centerx
        dy = player_y - self.rect.centery
        dist = math.hypot(dx, dy) or 1
        self.vx = dx / dist * self.speed
        self.vy = dy / dist * self.speed
        self.rect.x += self.vx
        self.rect.y += self.vy

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()

    def is_alive(self):
        return self.hp > 0