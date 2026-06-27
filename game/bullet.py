import pygame
import math
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.speed = 10
        
        # Рисуване на кръгче като куршум
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 230, 50), (6, 6), 6)  # Жълто кръгче
        
        self.rect = self.image.get_rect(center=(start_x, start_y))
    
        dx = target_x - start_x
        dy = target_y - start_y
        dist = math.hypot(dx, dy) or 1
        self.vx = dx / dist * self.speed
        self.vy = dy / dist * self.speed
    
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Унищожи ако излезе от екрана
        if not pygame.Rect(0, 0, 800, 600).colliderect(self.rect):
            self.kill()