import os
import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
FPS = 60
SHOOT_COOLDOWN = 300

PLAYER_SIZE = (220, 220)   # 2 пъти по-голям от преди (беше 110x110)
ENEMY_SIZE = (90, 90)

BG_COLOR = (173, 216, 230)     # бледо синьо
UI_TEXT_COLOR = (20, 30, 40)   # тъмен текст, за да се чете добре на светъл фон

EXIT_BTN_RECT = pygame.Rect(WIDTH - 130, 10, 120, 40)


def load_animation_frames(base_dir, filename, frames, size=PLAYER_SIZE):
    """Зарежда и нарязва спрайт-лист от папка hero на отделни кадри (само pygame, без PIL)."""
    path = os.path.join(base_dir, filename)
    frames_list = []

    if os.path.exists(path):
        try:
            sheet = pygame.image.load(path)
            try:
                sheet = sheet.convert_alpha()
            except pygame.error:
                pass

            sheet_w = sheet.get_width()
            sheet_h = sheet.get_height()
            frame_width = sheet_w // frames

            for i in range(frames):
                rect = pygame.Rect(i * frame_width, 0, frame_width, sheet_h)
                frame = sheet.subsurface(rect).copy()
                frame = pygame.transform.scale(frame, size)
                frames_list.append(frame)
        except Exception as e:
            print(f"⚠️ Грешка при зареждане на {filename}: {e}")

    return frames_list


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sx, sy, tx, ty):
        super().__init__()
        self.speed = 12
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 140, 0), (6, 6), 6)
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
    def __init__(self, x, y):
        super().__init__()
        self.speed = 5
        self.x = x
        self.y = y
        self.direction = 1  # 1 = дясно, -1 = ляво
        self.state = "idle"
        self.current_frame = 0
        self.frame_counter = 0

        base_dir = os.path.dirname(os.path.abspath(__file__))
        hero_dir = os.path.join(base_dir, "hero")

        self.animations = {
            "idle": {
                "frames": load_animation_frames(hero_dir, "idle.png", 9, PLAYER_SIZE),
                "speed": 6,
            },
            "walk": {
                "frames": load_animation_frames(hero_dir, "Walk.png", 7, PLAYER_SIZE),
                "speed": 5,
            },
        }

        if self.animations["idle"]["frames"]:
            self.image = self.animations["idle"]["frames"][0]
        else:
            player_img = os.path.join(base_dir, "player1.png")
            if os.path.exists(player_img):
                try:
                    self.image = pygame.image.load(player_img)
                    self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
                except Exception:
                    self.image = pygame.Surface(PLAYER_SIZE)
                    self.image.fill((42, 168, 255))
            else:
                self.image = pygame.Surface(PLAYER_SIZE)
                self.image.fill((42, 168, 255))

        self.rect = self.image.get_rect(center=(x, y))
        self.hp = 100
        self.max_hp = 100

    def set_state(self, new_state):
        if new_state != self.state and self.animations.get(new_state, {}).get("frames"):
            self.state = new_state
            self.current_frame = 0
            self.frame_counter = 0

    def animate(self):
        anim = self.animations.get(self.state)
        if not anim or not anim["frames"]:
            return

        self.frame_counter += 1
        if self.frame_counter >= anim["speed"]:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(anim["frames"])

        frame = anim["frames"][self.current_frame]
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)

        center = self.rect.center
        self.image = frame
        self.rect = self.image.get_rect(center=center)

    def update(self, held_keys):
        moving = False

        if pygame.K_w in held_keys or pygame.K_UP in held_keys:
            self.rect.y = max(0, self.rect.y - self.speed)
            moving = True
        if pygame.K_s in held_keys or pygame.K_DOWN in held_keys:
            self.rect.y = min(HEIGHT - self.rect.height, self.rect.y + self.speed)
            moving = True
        if pygame.K_a in held_keys or pygame.K_LEFT in held_keys:
            self.rect.x = max(0, self.rect.x - self.speed)
            self.direction = -1
            moving = True
        if pygame.K_d in held_keys or pygame.K_RIGHT in held_keys:
            self.rect.x = min(WIDTH - self.rect.width, self.rect.x + self.speed)
            self.direction = 1
            moving = True

        self.set_state("walk" if moving else "idle")
        self.animate()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=1):
        super().__init__()
        self.speed = speed
        self.hp = 50
        self.max_hp = 50
        self.y = y
        self.hit_flash = 0  # брояч за визуален "flash" при попадение

        base_dir = os.path.dirname(os.path.abspath(__file__))
        enemy_img = os.path.join(base_dir, "enemy1.png")

        self.base_image = None
        if os.path.exists(enemy_img):
            try:
                self.base_image = pygame.image.load(enemy_img).convert_alpha()
                self.base_image = pygame.transform.scale(self.base_image, ENEMY_SIZE)
            except Exception:
                self.base_image = None

        if self.base_image is None:
            self.base_image = pygame.Surface(ENEMY_SIZE, pygame.SRCALPHA)
            self.base_image.fill((229, 57, 53))

        self.image = self.base_image
        self.rect = self.image.get_rect(center=(x, y))

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        self.hit_flash = 6  # кадри, в които спрайтът мига червено

    def update(self, held_keys):
        if pygame.K_i in held_keys:
            self.rect.y = max(0, self.rect.y - self.speed * 2)
        if pygame.K_k in held_keys:
            self.rect.y = min(HEIGHT - self.rect.height, self.rect.y + self.speed * 2)

        if self.hit_flash > 0:
            self.hit_flash -= 1
            flash_img = self.base_image.copy()
            red_overlay = pygame.Surface(self.base_image.get_size(), pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 90))
            flash_img.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT if False else 0)
            self.image = flash_img
        else:
            self.image = self.base_image


def draw_crosshair(window, pos):
    x, y = pos
    color = (200, 20, 20)
    pygame.draw.circle(window, color, (x, y), 14, 2)
    pygame.draw.line(window, color, (x - 20, y), (x - 6, y), 2)
    pygame.draw.line(window, color, (x + 6, y), (x + 20, y), 2)
    pygame.draw.line(window, color, (x, y - 20), (x, y - 6), 2)
    pygame.draw.line(window, color, (x, y + 6), (x, y + 20), 2)


def draw_exit_button(window, font):
    pygame.draw.rect(window, (200, 40, 40), EXIT_BTN_RECT, border_radius=8)
    pygame.draw.rect(window, (120, 10, 10), EXIT_BTN_RECT, 2, border_radius=8)
    text = font.render("ИЗХОД (ESC)", True, (255, 255, 255))
    text_rect = text.get_rect(center=EXIT_BTN_RECT.center)
    window.blit(text, text_rect)


def start_training():
    try:
        _run_training()
    except Exception:
        import traceback
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(base_dir, "training_crash_log.txt")
        with open(log_path, "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        traceback.print_exc()
        try:
            pygame.display.quit()
            pygame.quit()
        except Exception:
            pass


def _run_training():
    pygame.init()
    pygame.display.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Braw Battle - TRAINING (Player shoots, Enemy I/K)")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    exit_font = pygame.font.Font(None, 20)

    bullets = pygame.sprite.Group()

    player = Player(WIDTH // 4, HEIGHT // 2)
    enemy = Enemy(3 * WIDTH // 4, HEIGHT // 2, speed=2)

    held_keys = set()

    score = 0
    last_shot = 0
    running = True

    while running:
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                held_keys.add(e.key)
                if e.key == pygame.K_ESCAPE:
                    running = False  # ESC = директен изход към менюто

                if e.key == pygame.K_SPACE:
                    if now - last_shot >= SHOOT_COOLDOWN:
                        mx, my = mouse_pos
                        bullet = Bullet(player.rect.centerx, player.rect.centery, mx, my)
                        bullets.add(bullet)
                        last_shot = now
                        # играчът се обръща в посоката, в която стреля (към мишката)
                        player.direction = 1 if mx >= player.rect.centerx else -1

            if e.type == pygame.KEYUP:
                held_keys.discard(e.key)

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if EXIT_BTN_RECT.collidepoint(mouse_pos):
                    running = False

        player.update(held_keys)
        enemy.update(held_keys)
        bullets.update()

        hits = pygame.sprite.spritecollide(enemy, bullets, True)
        if hits:
            for _ in hits:
                enemy.take_damage(20)
                score += 10
                if enemy.hp <= 0:
                    enemy.hp = enemy.max_hp
                    enemy.rect.center = (3 * WIDTH // 4, random.randint(50, HEIGHT - 50))

        # --- РИСУВАНЕ ---
        window.fill(BG_COLOR)
        window.blit(enemy.image, enemy.rect)
        window.blit(player.image, player.rect)
        bullets.draw(window)
        draw_crosshair(window, mouse_pos)

        hp_player = max(0, int(player.hp / player.max_hp * 150))
        hp_enemy = max(0, int(enemy.hp / enemy.max_hp * 150))

        pygame.draw.rect(window, (60, 60, 60), (10, 10, 150, 15))
        pygame.draw.rect(window, (0, 200, 0), (10, 10, hp_player, 15))
        window.blit(small_font.render(f"You: {int(player.hp)}", True, UI_TEXT_COLOR), (10, 30))

        pygame.draw.rect(window, (60, 60, 60), (WIDTH - 300, 10, 150, 15))
        pygame.draw.rect(window, (220, 0, 0), (WIDTH - 300, 10, hp_enemy, 15))
        window.blit(small_font.render(f"Enemy: {int(enemy.hp)}", True, UI_TEXT_COLOR), (WIDTH - 300, 30))

        score_text = font.render(f"Score: {score}", True, UI_TEXT_COLOR)
        window.blit(score_text, (10, 60))

        info_text = small_font.render("Player: WASD move + SPACE shoot (aim with mouse) | Enemy: I (up) / K (down)", True, (60, 70, 80))
        window.blit(info_text, (10, HEIGHT - 30))

        draw_exit_button(window, exit_font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.display.quit()
    pygame.quit()


if __name__ == "__main__":
    start_training()