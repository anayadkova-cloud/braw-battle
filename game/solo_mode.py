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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, px, py, speed=2):
        super().__init__()
        self.speed = speed
        self.hp = 50
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        enemy_img = os.path.join(base_dir, 'enemy.png')
        
        if os.path.exists(enemy_img):
            try:
                self.image = pygame.image.load(enemy_img)
                self.image = pygame.transform.scale(self.image, (45, 45))
            except:
                self.image = pygame.Surface((45, 45))
                self.image.fill((229, 57, 53))
        else:
            self.image = pygame.Surface((45, 45))
            self.image.fill((229, 57, 53))
        
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)))
    
    def update(self, px, py):
        dx = px - self.rect.centerx
        dy = py - self.rect.centery
        dist = math.hypot(dx, dy) or 1
        self.rect.x += dx / dist * self.speed
        self.rect.y += dy / dist * self.speed

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = 5
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        player_img = os.path.join(base_dir, 'player1.png')
        
        if os.path.exists(player_img):
            try:
                self.image = pygame.image.load(player_img)
                self.image = pygame.transform.scale(self.image, (50, 50))
            except:
                self.image = pygame.Surface((50, 50))
                self.image.fill((42, 168, 255))
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill((42, 168, 255))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.hp = 100
        self.max_hp = 100
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y = max(0, self.rect.y - self.speed)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y = min(HEIGHT - 50, self.rect.y + self.speed)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x = max(0, self.rect.x - self.speed)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x = min(WIDTH - 50, self.rect.x + self.speed)

def start_solo():
    pygame.init()
    pygame.display.init()
    
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Braw Battle - SOLO")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)

    pygame.time.set_timer(SPAWN_EVENT, 2000)

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player(WIDTH // 2, HEIGHT // 2)
    all_sprites.add(player)

    score = 0
    start_time = pygame.time.get_ticks()
    last_shot = 0
    dmg_cd = 0
    running = True
    paused = False
    round_time = 90

    while running:
        now = pygame.time.get_ticks()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    paused = not paused
            
            if e.type == SPAWN_EVENT and not paused:
                enemy = Enemy(player.rect.centerx, player.rect.centery, 2)
                enemies.add(enemy)
                all_sprites.add(enemy)
            
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not paused:
                if now - last_shot >= SHOOT_COOLDOWN:
                    mx, my = pygame.mouse.get_pos()
                    bullet = Bullet(player.rect.centerx, player.rect.centery, mx, my)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                    last_shot = now

        if not paused:
            all_sprites.update()
            
            for enemy in enemies:
                enemy.update(player.rect.centerx, player.rect.centery)
            
            hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
            for bullet, hit_list in hits.items():
                for enemy in hit_list:
                    enemy.hp -= 20
                    if enemy.hp <= 0:
                        enemy.kill()
                        score += 10
            
            collisions = pygame.sprite.spritecollide(player, enemies, False)
            if collisions and now - dmg_cd > DAMAGE_CD:
                player.hp -= 10
                dmg_cd = now
                if player.hp <= 0:
                    running = False

            elapsed = (pygame.time.get_ticks() - start_time) // 1000
            if elapsed >= round_time:
                running = False

        window.fill((15, 25, 50))
        all_sprites.draw(window)

        hp = max(0, int(player.hp / player.max_hp * 180))
        pygame.draw.rect(window, (100, 100, 100), (10, 10, 180, 20))
        pygame.draw.rect(window, (0, 255, 0), (10, 10, hp, 20))

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
    start_solo()