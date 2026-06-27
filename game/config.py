import json
import os
import threading


class Config:
    _instance = None
    _lock = threading.Lock()

    DEFAULTS = {
        "sound_enabled": True,
        "brightness": 100,
        "resolution": "800x600"
    }

    available_resolutions = [
        "800x600",
        "1024x768",
        "1280x720",
        "1366x768",
        "1600x900",
        "1920x1080"
    ]

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Config, cls).__new__(cls)
                cls._instance._init()
        return cls._instance

    def _init(self):
        self.path = os.path.join(os.path.dirname(__file__), "settings.json")
        self.data = {}

        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    self.data = json.load(f)
            except:
                self.data = self.DEFAULTS.copy()
        else:
            self.data = self.DEFAULTS.copy()
            self._save()

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4)

    # --- PUBLIC API ---
    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self._save()

    def set_brightness(self, value):
        self.data["brightness"] = int(value)
        self._save()

    def set_resolution(self, value):
        self.data["resolution"] = value
        self._save()
