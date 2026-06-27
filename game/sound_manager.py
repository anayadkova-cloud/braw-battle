import os
import pygame
import threading
from config import Config


class SoundManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SoundManager, cls).__new__(cls)
                cls._instance._init()
        return cls._instance

    def _init(self):
        pygame.mixer.init()
        self.config = Config()

        self.sounds = {}
        self.load_sound()
        self.apply_settings()

    def load_sound(self):
        """Зарежда единствения звук sound.wav"""
        base = os.path.join(os.path.dirname(__file__), "audio")
        path = os.path.join(base, "sound.wav")

        if os.path.exists(path):
            try:
                self.sounds["click"] = pygame.mixer.Sound(path)
            except Exception as e:
                print("Грешка при зареждане на sound.wav:", e)

    def apply_settings(self):
        enabled = self.config.get("sound_enabled", True)
        volume = 1.0 if enabled else 0.0

        for snd in self.sounds.values():
            snd.set_volume(volume)

    def play_sound(self, name="click"):
        if not self.config.get("sound_enabled", True):
            return
        if name in self.sounds:
            self.sounds[name].play()

    def toggle_sound(self, enabled):
        self.config.set("sound_enabled", enabled)
        self.apply_settings()
