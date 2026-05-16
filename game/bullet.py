import pygame, math
    
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, start_x, start_y, target_x, target_y):
            super().__init__()
            self.speed  = 10
            self.image  = pygame.Surface((10, 10))
            self.image.fill((255, 230, 50))   # ЖЪЛТ куршум
            self.rect   = self.image.get_rect(center=(start_x, start_y))
    
            dx = target_x - start_x
            dy = target_y - start_y
            dist = math.hypot(dx, dy) or 1
            self.vx = dx / dist * self.speed
            self.vy = dy / dist * self.speed
    
        def update(self):
            self.rect.x += self.vx
            self.rect.y += self.vy
            # Унищожи ако излезе от екрана
            if not pygame.Rect(0,0,800,600).colliderect(self.rect):
                self.kill()
