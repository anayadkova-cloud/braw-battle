import os
import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
FPS = 60
SPAWN_EVENT = pygame.USEREVENT + 1
SHOOT_COOLDOWN = 300
DAMAGE_CD = 1000

class Bullet(pygame.sprite.Sprite):
    def __init__(self, sx, sy, tx, ty):
        super().__init__()
        self.speed = 10
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 230, 50), (6, 6), 6)
        self.rect = self.image.get_rect(center=(sx, sy))
        
        dx = tx - sx
        dy = ty - sy
        dist = math.hypot(dx, dy) or 1
        self.vx = dx / dist * self.speed
        self.vy = dy / dist * self.speed
    
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, pid=1):
        super().__init__()
        self.speed = 5
        self.pid = pid
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        player_img = os.path.join(base_dir, 'player1.png')
        
        if os.path.exists(player_img):
            try:
                self.image = pygame.image.load(player_img)
                self.image = pygame.transform.scale(self.image, (50, 50))
                if pid == 2:
                    self.image = pygame.transform.flip(self.image, True, False)
            except:
                self.image = pygame.Surface((50, 50))
                self.image.fill((42, 168, 255) if pid == 1 else (255, 168, 42))
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill((42, 168, 255) if pid == 1 else (255, 168, 42))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.hp = 100
        self.max_hp = 100
    
    def update(self):
        keys = pygame.key.get_pressed()
        if self.pid == 1:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.rect.y = max(0, self.rect.y - self.speed)
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.rect.y = min(HEIGHT - 50, self.rect.y + self.speed)
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.rect.x = max(0, self.rect.x - self.speed)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.rect.x = min(WIDTH - 50, self.rect.x + self.speed)
        else:
            if keys[pygame.K_i]:
                self.rect.y = max(0, self.rect.y - self.speed)
            if keys[pygame.K_k]:
                self.rect.y = min(HEIGHT - 50, self.rect.y + self.speed)
            if keys[pygame.K_j]:
                self.rect.x = max(0, self.rect.x - self.speed)
            if keys[pygame.K_l]:
                self.rect.x = min(WIDTH - 50, self.rect.x + self.speed)

def start_duo():
    pygame.init()
    pygame.display.init()
    
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Braw Battle - DUO")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    p1 = Player(WIDTH // 3, HEIGHT // 2, 1)
    p2 = Player(2 * WIDTH // 3, HEIGHT // 2, 2)
    all_sprites.add(p1, p2)

    score = 0
    start_time = pygame.time.get_ticks()
    last_shot = 0
    running = True
    paused = False
    round_time = 120

    while running:
        now = pygame.time.get_ticks()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    paused = not paused
            
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not paused:
                if now - last_shot >= SHOOT_COOLDOWN:
                    mx, my = pygame.mouse.get_pos()
                    bullet = Bullet(p1.rect.centerx, p1.rect.centery, mx, my)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                    last_shot = now

        if not paused:
            all_sprites.update()
            
            collisions = pygame.sprite.spritecollide(p2, bullets, True)
            if collisions:
                for _ in collisions:
                    p2.hp -= 5
                    score += 5
                if p2.hp <= 0:
                    running = False

            elapsed = (pygame.time.get_ticks() - start_time) // 1000
            if elapsed >= round_time:
                running = False

        window.fill((15, 25, 50))
        all_sprites.draw(window)

        hp1 = max(0, int(p1.hp / p1.max_hp * 180))
        hp2 = max(0, int(p2.hp / p2.max_hp * 180))
        pygame.draw.rect(window, (100, 100, 100), (10, 10, 180, 20))
        pygame.draw.rect(window, (0, 255, 0), (10, 10, hp1, 20))
        pygame.draw.rect(window, (100, 100, 100), (WIDTH - 190, 10, 180, 20))
        pygame.draw.rect(window, (0, 255, 0), (WIDTH - 190, 10, hp2, 20))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_text, (10, 50))

        elapsed = (pygame.time.get_ticks() - start_time) // 1000
        time_left = max(0, round_time - elapsed)
        time_text = font.render(f"Time: {time_left}s", True, (255, 255, 255))
        window.blit(time_text, (WIDTH - 180, 50))

        if paused:
            pause_text = big_font.render("PAUSED", True, (255, 220, 0))
            window.blit(pause_text, pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        pygame.display.flip()
        clock.tick(FPS)

    window.fill((20, 0, 0))
    go_text = big_font.render("GAME OVER", True, (255, 50, 50))
    sc_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(go_text, go_text.get_rect(center=(WIDTH // 2, 220)))
    window.blit(sc_text, sc_text.get_rect(center=(WIDTH // 2, 320)))
    pygame.display.flip()
    pygame.time.wait(3000)
    
    pygame.display.quit()
    pygame.quit()

if __name__ == "__main__":
    start_duo()