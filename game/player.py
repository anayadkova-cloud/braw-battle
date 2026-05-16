import pygame
    
    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.speed  = 5
            self.width  = 50
            self.height = 50
    
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((42, 168, 255))   # СИНЬО
            self.rect  = self.image.get_rect(center=(x, y))
    
        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.rect.y += self.speed
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
    
            # Не излиза извън екрана
            self.rect.clamp_ip(pygame.Rect(0, 0, 800, 600))

            self.hp     = 100
            self.max_hp = 100
            
            def take_damage(self, amount):
                self.hp = max(0, self.hp - amount)
            
            def heal(self, amount):
                self.hp = min(self.max_hp, self.hp + amount)
            
            def is_alive(self):
                return self.hp > 0
        

        SHOOT_COOLDOWN = 500   # ms между изстрели
        last_shot = 0
                
            # В event loop:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            now = pygame.time.get_ticks()
            if now - last_shot >= SHOOT_COOLDOWN:
                mx, my = pygame.mouse.get_pos()
                b = Bullet(player.rect.centerx, player.rect.centery, mx, my)
                bullets.add(b)
                all_sprites.add(b)
                last_shot = now
