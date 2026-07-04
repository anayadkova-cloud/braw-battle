import os
import pygame
import math

WIDTH, HEIGHT = 800, 600
FPS = 60
SHOOT_COOLDOWN = 300

PLAYER_SIZE = (200, 200)

BG_COLOR = (173, 216, 230)     # бледо синьо
UI_TEXT_COLOR = (20, 30, 40)

EXIT_BTN_RECT = pygame.Rect(WIDTH - 130, 10, 120, 40)

P2_TINT = (255, 120, 120, 90)  # червеникав оттенък за Player 2, за да се различават


def load_animation_frames(base_dir, filename, frames, size=PLAYER_SIZE, tint=None):
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

                if tint:
                    overlay = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
                    overlay.fill(tint)
                    frame.blit(overlay, (0, 0))

                frames_list.append(frame)
        except Exception as e:
            print(f"⚠️ Грешка при зареждане на {filename}: {e}")

    return frames_list


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sx, sy, tx, ty, color=(255, 140, 0)):
        super().__init__()
        self.speed = 12
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (6, 6), 6)
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
        self.direction = 1 if pid == 1 else -1
        self.state = "idle"
        self.current_frame = 0
        self.frame_counter = 0

        base_dir = os.path.dirname(os.path.abspath(__file__))
        hero_dir = os.path.join(base_dir, "hero")
        tint = P2_TINT if pid == 2 else None

        self.animations = {
            "idle": {"frames": load_animation_frames(hero_dir, "idle.png", 9, PLAYER_SIZE, tint), "speed": 6},
            "walk": {"frames": load_animation_frames(hero_dir, "Walk.png", 7, PLAYER_SIZE, tint), "speed": 5},
        }

        if self.animations["idle"]["frames"]:
            self.image = self.animations["idle"]["frames"][0]
        else:
            player_img = os.path.join(base_dir, "player1.png")
            if os.path.exists(player_img):
                try:
                    self.image = pygame.image.load(player_img)
                    self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
                    if pid == 2:
                        self.image = pygame.transform.flip(self.image, True, False)
                except Exception:
                    self.image = pygame.Surface(PLAYER_SIZE)
                    self.image.fill((42, 168, 255) if pid == 1 else (255, 168, 42))
            else:
                self.image = pygame.Surface(PLAYER_SIZE)
                self.image.fill((42, 168, 255) if pid == 1 else (255, 168, 42))

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

        if self.pid == 1:
            up, down, left, right = pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d
        else:
            up, down, left, right = pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l

        if up in held_keys:
            self.rect.y = max(0, self.rect.y - self.speed)
            moving = True
        if down in held_keys:
            self.rect.y = min(HEIGHT - self.rect.height, self.rect.y + self.speed)
            moving = True
        if left in held_keys:
            self.rect.x = max(0, self.rect.x - self.speed)
            self.direction = -1
            moving = True
        if right in held_keys:
            self.rect.x = min(WIDTH - self.rect.width, self.rect.x + self.speed)
            self.direction = 1
            moving = True

        self.set_state("walk" if moving else "idle")
        self.animate()


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


def start_duo():
    try:
        _run_duo()
    except Exception:
        import traceback
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(base_dir, "duo_crash_log.txt")
        with open(log_path, "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        traceback.print_exc()
        try:
            pygame.display.quit()
            pygame.quit()
        except Exception:
            pass


def _run_duo():
    pygame.init()
    pygame.display.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Braw Battle - DUO (Player 1 vs Player 2)")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)
    small_font = pygame.font.Font(None, 22)
    exit_font = pygame.font.Font(None, 20)

    p1 = Player(WIDTH // 4, HEIGHT // 2, pid=1)
    p2 = Player(3 * WIDTH // 4, HEIGHT // 2, pid=2)

    p1_bullets = pygame.sprite.Group()
    p2_bullets = pygame.sprite.Group()

    held_keys = set()

    score1 = 0
    score2 = 0
    start_time = pygame.time.get_ticks()
    last_shot_p1 = 0
    last_shot_p2 = 0
    running = True
    round_time = 120
    winner = None

    while running:
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                held_keys.add(e.key)

                if e.key == pygame.K_ESCAPE:
                    running = False

                # --- P1 стреля със SPACE, цели се с мишката ---
                if e.key == pygame.K_SPACE:
                    if now - last_shot_p1 >= SHOOT_COOLDOWN:
                        mx, my = mouse_pos
                        p1_bullets.add(Bullet(p1.rect.centerx, p1.rect.centery, mx, my, color=(255, 140, 0)))
                        last_shot_p1 = now
                        p1.direction = 1 if mx >= p1.rect.centerx else -1

                # --- P2 стреля с U, автоматично се цели към P1 ---
                if e.key == pygame.K_u:
                    if now - last_shot_p2 >= SHOOT_COOLDOWN:
                        p2_bullets.add(Bullet(p2.rect.centerx, p2.rect.centery,
                                               p1.rect.centerx, p1.rect.centery, color=(80, 160, 255)))
                        last_shot_p2 = now
                        p2.direction = 1 if p1.rect.centerx >= p2.rect.centerx else -1

            if e.type == pygame.KEYUP:
                held_keys.discard(e.key)

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if EXIT_BTN_RECT.collidepoint(mouse_pos):
                    running = False

        p1.update(held_keys)
        p2.update(held_keys)
        p1_bullets.update()
        p2_bullets.update()

        hits_on_p2 = pygame.sprite.spritecollide(p2, p1_bullets, True)
        if hits_on_p2:
            for _ in hits_on_p2:
                p2.hp -= 8
                score1 += 5
            if p2.hp <= 0:
                running = False
                winner = "Player 1"

        hits_on_p1 = pygame.sprite.spritecollide(p1, p2_bullets, True)
        if hits_on_p1:
            for _ in hits_on_p1:
                p1.hp -= 8
                score2 += 5
            if p1.hp <= 0:
                running = False
                winner = "Player 2"

        elapsed = (pygame.time.get_ticks() - start_time) // 1000
        if elapsed >= round_time and running:
            running = False
            if p1.hp > p2.hp:
                winner = "Player 1"
            elif p2.hp > p1.hp:
                winner = "Player 2"
            else:
                winner = "Draw"

        # --- РИСУВАНЕ ---
        window.fill(BG_COLOR)
        window.blit(p1.image, p1.rect)
        window.blit(p2.image, p2.rect)
        p1_bullets.draw(window)
        p2_bullets.draw(window)
        draw_crosshair(window, mouse_pos)

        hp1 = max(0, int(p1.hp / p1.max_hp * 150))
        pygame.draw.rect(window, (60, 60, 60), (10, 10, 150, 15))
        pygame.draw.rect(window, (0, 200, 0), (10, 10, hp1, 15))
        window.blit(small_font.render(f"P1: {int(p1.hp)}", True, UI_TEXT_COLOR), (10, 30))

        hp2 = max(0, int(p2.hp / p2.max_hp * 150))
        pygame.draw.rect(window, (60, 60, 60), (WIDTH - 300, 10, 150, 15))
        pygame.draw.rect(window, (0, 200, 0), (WIDTH - 300, 10, hp2, 15))
        window.blit(small_font.render(f"P2: {int(p2.hp)}", True, UI_TEXT_COLOR), (WIDTH - 300, 30))

        score_text = font.render(f"P1: {score1}   P2: {score2}", True, UI_TEXT_COLOR)
        window.blit(score_text, (WIDTH // 2 - 80, 55))

        time_left = max(0, round_time - elapsed)
        time_text = small_font.render(f"Time: {time_left}s", True, UI_TEXT_COLOR)
        window.blit(time_text, (WIDTH // 2 - 40, 90))

        info_text = small_font.render(
            "P1: WASD move + SPACE shoot (aim mouse) | P2: IJKL move + U shoot (auto-aim)",
            True, (60, 70, 80)
        )
        window.blit(info_text, (10, HEIGHT - 30))

        draw_exit_button(window, exit_font)

        pygame.display.flip()
        clock.tick(FPS)

    window.fill(BG_COLOR)
    go_text = big_font.render("GAME OVER", True, (200, 30, 30))
    window.blit(go_text, go_text.get_rect(center=(WIDTH // 2, 220)))
    if winner:
        winner_text = font.render(f"{winner} Wins!", True, UI_TEXT_COLOR)
        window.blit(winner_text, winner_text.get_rect(center=(WIDTH // 2, 300)))
    sc_text = font.render(f"P1: {score1}   P2: {score2}", True, UI_TEXT_COLOR)
    window.blit(sc_text, sc_text.get_rect(center=(WIDTH // 2, 360)))
    pygame.display.flip()
    pygame.time.wait(2500)

    pygame.display.quit()
    pygame.quit()


if __name__ == "__main__":
    start_duo()