import pygame
import os


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, player_id=1):
        super().__init__()
        self.speed = 5
        self.width = 50
        self.height = 50
        self.player_id = player_id

        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, 'player1.png')
        
        if os.path.exists(img_path):
            try:
                self.image = pygame.image.load(img_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
                
                if player_id == 2:
                    self.image = pygame.transform.flip(self.image, True, False)
            except:
                self.image = pygame.Surface((self.width, self.height))
                color = (42, 168, 255) if player_id == 1 else (255, 168, 42)  # Син или оранжев
                self.image.fill(color)
        else:
            self.image = pygame.Surface((self.width, self.height))
            color = (42, 168, 255) if player_id == 1 else (255, 168, 42)  # Син или оранжев
            self.image.fill(color)
        
        self.rect = self.image.get_rect(center=(x, y))

        # Характеристики
        self.hp = 100
        self.max_hp = 100

    def update(self):
        keys = pygame.key.get_pressed()

        if self.player_id == 1:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.rect.y += self.speed
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
        else:  # Player 2
            if keys[pygame.K_i]:
                self.rect.y -= self.speed
            if keys[pygame.K_k]:
                self.rect.y += self.speed
            if keys[pygame.K_j]:
                self.rect.x -= self.speed
            if keys[pygame.K_l]:
                self.rect.x += self.speed

        self.rect.clamp_ip(pygame.Rect(0, 0, 800, 600))

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def is_alive(self):
        return self.hp > 0