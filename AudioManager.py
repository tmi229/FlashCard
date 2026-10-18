
import pygame
from pathlib import Path


class AudioManager:
    def __init__(self):
        self.enabled = False
        self.sounds = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            self.enabled = True

        except pygame.error as e:
            print(f"Không thể khởi tạo âm thanh: {e}")
            return

        self.sound_dir = Path(__file__).resolve().parent / "assets" / "sounds"

        self.load_sound("click", "click.mp3")
        self.load_sound("correct", "correct.mp3")
        self.load_sound("wrong", "wrong.mp3")
        self.load_sound("flip", "flip.mp3")

    def load_sound(self, name, filename):
        if not self.enabled:
            return

        path = self.sound_dir / filename

        try:
            self.sounds[name] = pygame.mixer.Sound(str(path))

        except (pygame.error, OSError) as e:
            print(f"Không thể nạp âm thanh '{filename}': {e}")

    def play(self, name):
        if not self.enabled:
            return

        sound = self.sounds.get(name)

        if sound is None:
            return

        try:
            sound.play()
        except pygame.error as e:
            print(f"Không thể phát âm thanh '{name}': {e}")

    def set_volume(self, volume):
        volume = max(0.0, min(1.0, volume))

        for sound in self.sounds.values():
            sound.set_volume(volume)
