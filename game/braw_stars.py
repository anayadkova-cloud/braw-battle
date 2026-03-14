import pygame
import sys


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


def start_game(mode="training"):
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(f"Shooter – {mode}")

    clock = pygame.time.Clock()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        window.fill((20, 20, 20))

        # Тук по-късно ще добавим:
        # - мишени
        # - точки
        # - таймер
        # - трудност според mode

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

import pygame
