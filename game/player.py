import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.speed = 5
        self.width = 50
        self.height = 50

        # Визуализация и позиция
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((42, 168, 255))  # СИНЬО
        self.rect = self.image.get_rect(center=(x, y))

        # Характеристики (Правилното място за HP!)
        self.hp = 100
        self.max_hp = 100

    def update(self):
        # Вземане на натиснатите клавиши
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Ограничение да не излиза извън екрана (800x600)
        self.rect.clamp_ip(pygame.Rect(0, 0, 800, 600))

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def is_alive(self):
        return self.hp > 0
