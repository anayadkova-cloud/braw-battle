import pygame
import sys

from player import Player
from bullet import Bullet
from enemy import Enemy

def start_game(mode='training'):
        pygame.init()
        window = pygame.display.set_mode((800, 600))
        clock  = pygame.time.Clock()
    
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        player = Player(400, 300)
        all_sprites.add(player)
    
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: running = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE: running = False

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mx, my = pygame.mouse.get_pos()
            b = Bullet(player.rect.centerx, player.rect.centery, mx, my)
            bullets.add(b)
            all_sprites.add(b)
    
            all_sprites.update()
            window.fill((15, 25, 50))
            all_sprites.draw(window)
            pygame.display.update()
            clock.tick(60)

            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)




bullets = pygame.sprite.Group()
    
    # В event loop:



  # spawn на 2 сек
    
enemies = pygame.sprite.Group()
    
# В event loop:
if e.type == SPAWN_EVENT:
    enemy = Enemy(player.rect.centerx, player.rect.centery)
    enemies.add(enemy)
    all_sprites.add(enemy)

for enemy in enemies:
    enemy.update(player.rect.centerx, player.rect.centery)


    
# В game loop:
now = pygame.time.get_ticks()
player_hits = pygame.sprite.spritecollide(player, enemies, False)
if player_hits and now - damage_cooldown > DAMAGE_CD:
    player.take_damage(10)
    damage_cooldown = now
    if not player.is_alive():
        running = False   # game over


class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse) else self.color

        pygame.draw.rect(screen, current_color, self.rect, border_radius=25)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


    def start_game(mode='training'):
            pygame.init()
            window = pygame.display.set_mode((800, 600))
            pygame.display.set_caption(f'Braw Battle – {mode.upper()}')
            clock = pygame.time.Clock()
        
            BG_COLOR = (15, 25, 50)   # тъмносин фон

            SPAWN_EVENT = pygame.USEREVENT + 1
            pygame.time.set_timer(SPAWN_EVENT, 2000) 
        
            running = True
            while running:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        running = False
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            running = False   # ESC затваря
        
                window.fill(BG_COLOR)
                pygame.display.update()
                clock.tick(60)
        
            pygame.quit()

    hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
    for bullet, hit_enemies in hits.items():
        for enemy in hit_enemies:
            enemy.take_damage(20)


        # В event loop:
    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
        now = pygame.time.get_ticks()
        if now - last_shot >= SHOOT_COOLDOWN:
            mx, my = pygame.mouse.get_pos()
            b = Bullet(player.rect.centerx, player.rect.centery, mx, my)
            bullets.add(b)
            all_sprites.add(b)
            last_shot = now

    DAMAGE_CD    = 1000   # ms cooldown за damage
    damage_cooldown = 0 
    now = pygame.time.get_ticks()
    player_hits = pygame.sprite.spritecollide(player, enemies, False)
    if player_hits and now - damage_cooldown > DAMAGE_CD:
        player.take_damage(10)
        damage_cooldown = now
        if not player.is_alive():
            running = False   # game over


sys.exit()
