import os
import sys
import pygame

from bullet import Bullet
from enemy import Enemy
from player import Player

# --- ГЛОБАЛНИ НАСТРОЙКИ И КОНСТАНТИ ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# Настройки за различните режими на игра
MODE_SETTINGS = {
    "training": {"round_time": 60, "speed": 2, "spawn_ms": 2000},
    "normal": {"round_time": 90, "speed": 4, "spawn_ms": 1500},
}

SPAWN_EVENT = pygame.USEREVENT + 1
SHOOT_COOLDOWN = 300  # ms между изстрелите
DAMAGE_CD = 1000  # ms кооडाउन за демидж върху играча


# --- ПОМОЩНИ КЛАСОВЕ ---
class Button:

    def __init__(self, x, y, w, h, text, color, hover_color, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        current_color = (
            self.hover_color if self.rect.collidepoint(mouse) else self.color
        )

        pygame.draw.rect(screen, current_color, self.rect, border_radius=25)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


# --- ЕКРАН ЗА КРАЙ НА ИГРАТА ---
def show_game_over(window, font, score):
    big_font = pygame.font.Font(None, 80)
    window.fill((20, 0, 0))

    go_text = big_font.render("GAME OVER", True, (255, 50, 50))
    sc_text = font.render(f"Финален резултат: {score}", True, (255, 255, 255))
    hint = font.render("Затваряне след 3 секунди...", True, (180, 180, 180))

    window.blit(go_text, go_text.get_rect(center=(WIDTH // 2, 220)))
    window.blit(sc_text, sc_text.get_rect(center=(WIDTH // 2, 320)))
    window.blit(hint, hint.get_rect(center=(WIDTH // 2, 400)))

    pygame.display.update()
    pygame.time.wait(3000)


# --- ОСНОВНА ФУНКЦИЯ ЗА ИГРАТА ---
def start_game(mode="training"):
    pygame.init()
    pygame.mixer.init()

    # Прозорец и заглавие
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Braw Battle – {mode.upper()}")
    clock = pygame.time.Clock()

    # Шрифтове
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)

    # Звуци
    sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
    shoot_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "shoot.wav"))
    hit_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "hit.wav"))
    shoot_sound.set_volume(0.4)
    hit_sound.set_volume(0.6)

    # Зареждане на конфигурация за режима
    cfg = MODE_SETTINGS.get(mode, MODE_SETTINGS["training"])
    ROUND_TIME = cfg["round_time"]
    ENEMY_SPEED = cfg["speed"]
    spawn_ms = cfg["spawn_ms"]

    pygame.time.set_timer(SPAWN_EVENT, spawn_ms)

    # Спрайт групи и обекти
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player(WIDTH // 2, HEIGHT // 2)
    all_sprites.add(player)

    # Игрови променливи
    score = 0
    start_time = pygame.time.get_ticks()
    last_shot = 0
    damage_cooldown = 0

    running = True
    paused = False

    # --- ИГРОВ ЦИКЪЛ (GAME LOOP) ---
    while running:
        now = pygame.time.get_ticks()

        # 1. СЪБИТИЯ (EVENTS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    paused = not paused  # Пауза/Спиране на пауза с ESC

            if not paused:
                # Спаун на врагове
                if e.type == SPAWN_EVENT:
                    enemy = Enemy(player.rect.centerx, player.rect.centery)
                    enemies.add(enemy)
                    all_sprites.add(enemy)

                # Стрелба с мишката (с cooldown)
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if now - last_shot >= SHOOT_COOLDOWN:
                        mx, my = pygame.mouse.get_pos()
                        b = Bullet(
                            player.rect.centerx, player.rect.centery, mx, my
                        )
                        bullets.add(b)
                        all_sprites.add(b)
                        shoot_sound.play()
                        last_shot = now

        # 2. ОБНОВЯВАНЕ НА ЛОГИКАТА (UPDATE) - Изпълнява се само ако не е на пауза
        if not paused:
            all_sprites.update()

            # Обновяване движението на враговете спрямо играча
            for enemy in enemies:
                enemy.update(player.rect.centerx, player.rect.centery)

            # Проверка за времето
            elapsed = (pygame.time.get_ticks() - start_time) // 1000
            time_left = max(0, ROUND_TIME - elapsed)
            if time_left == 0:
                running = False

            # Сблъсъци: Куршуми удрят Врагове
            hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
            for bullet, hit_enemies in hits.items():
                for enemy in hit_enemies:
                    enemy.take_damage(20)
                    hit_sound.play()
                    if not enemy.is_alive():
                        score += 10

            # Сблъсъци: Врагове удрят Играча (с cooldown за damage)
            player_hits = pygame.sprite.spritecollide(player, enemies, False)
            if player_hits and now - damage_cooldown > DAMAGE_CD:
                player.take_damage(10)
                damage_cooldown = now
                if not player.is_alive():
                    running = False  # Играта свършва, ако играчът умре

        # 3. РИСУВАНЕ НА ЕКРАНА (DRAW)
        window.fill((15, 25, 50))  # Тъмносин фон
        all_sprites.draw(window)

        # Рисуване на UI за HP лента
        MAX_BAR_W = 200
        BAR_H = 22
        hp_ratio = player.hp / player.max_hp
        pygame.draw.rect(
            window, (80, 80, 80), (10, 45, MAX_BAR_W, BAR_H)
        )  # Сива основа
        pygame.draw.rect(
            window,
            (0, 200, 80),
            (10, 45, int(hp_ratio * MAX_BAR_W), BAR_H),
        )  # Зелено HP

        hp_text = font.render(
            f"HP: {player.hp}/{player.max_hp}", True, (255, 255, 255)
        )
        window.blit(hp_text, (220, 45))

        # Рисуване на UI за Резултат и Време
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_text, (10, 10))

        time_text = font.render(f"Time: {time_left}s", True, (255, 255, 255))
        window.blit(time_text, (WIDTH - 150, 10))

        # Ако играта е на пауза, изрисувай надпис
        if paused:
            pause_text = big_font.render("ПАУЗА", True, (255, 220, 0))
            window.blit(
                pause_text, pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            )

        pygame.display.update()
        clock.tick(FPS)

    # Извън уайла: покажи Game Over екран, ако цикълът е приключил
    show_game_over(window, font, score)
    pygame.quit()


# --- СТАРТИРАНЕ ---
if __name__ == "__main__":
    start_game("training")
    sys.exit()
