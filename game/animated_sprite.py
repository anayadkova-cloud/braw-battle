import pygame
import os
from PIL import Image

class AnimatedSprite(pygame.sprite.Sprite):
    
    def __init__(self, x, y, sprite_type="player"):
        super().__init__()
        self.sprite_type = sprite_type
        self.x = x
        self.y = y
        self.state = "idle"  
        self.direction = 1  
        
        self.animations = {}
        self.current_frame = 0
        self.frame_counter = 0
        self.animation_speed = 5  
        
        self.load_sprites()
        
        self.image = pygame.Surface((50, 50))
        self.image.fill((42, 168, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.hp = 100
        self.max_hp = 100
    
    def load_sprites(self):
        base_dir = os.path.join(os.path.dirname(__file__),"hero")
        
        sprite_config = {
            "idle": ("idle.png", 9, 5),
            "walk": ("Walk.png", 7, 5),
            "run": ("Run.png", 8, 4),
            "attack": ("Attack.png", 3, 6),
            "shoot1": ("shot_1.png", 4, 6),
            "shoot2": ("Shot_2.png", 4, 6),
            "hurt": ("Hurt.png", 3, 5),
            "dead": ("Dead.png", 4, 8),
        }
        
        for state, (filename, frames, speed) in sprite_config.items():
            path = os.path.join(base_dir, filename)
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    frame_width = img.width // frames
                    frame_height = img.height
                    
                    frames_list = []
                    for i in range(frames):
                        frame = img.crop((
                            i * frame_width, 0,
                            (i + 1) * frame_width, frame_height
                        ))
                        frame_data = pygame.image.fromstring(
                            frame.tobytes(),
                            frame.size,
                            frame.mode
                        )
                        frame_data = pygame.transform.scale(frame_data, (70, 70))
                        frames_list.append(frame_data)
                    
                    self.animations[state] = {
                        "frames": frames_list,
                        "speed": speed,
                        "frame_count": frames
                    }
                except Exception as e:
                    print(f"⚠️ Грешка при зареждане на {filename}: {e}")
    
    def update(self, keys=None):
        if self.state in self.animations:
            anim = self.animations[self.state]
            self.frame_counter += 1
            
            if self.frame_counter >= anim["speed"]:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % anim["frame_count"]
            
            frame = anim["frames"][self.current_frame]
            
            if self.direction == -1:
                frame = pygame.transform.flip(frame, True, False)
            
            self.image = frame
            self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def set_state(self, new_state):
        if new_state != self.state and new_state in self.animations:
            self.state = new_state
            self.current_frame = 0
            self.frame_counter = 0
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)
        
        if dx > 0:
            self.direction = 1
        elif dx < 0:
            self.direction = -1
    
    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self.hp > 0:
            self.set_state("hurt")
        else:
            self.set_state("dead")
    
    def is_alive(self):
        return self.hp > 0

