import io

import pygame
from pygame import mixer

# Initialize Pygame mixer
mixer.init()


def start_loop(file_path: str) -> None:
    # Load and play the looping audio file
    mixer.music.load(file_path)
    mixer.music.play(-1)  # -1 makes the audio loop indefinitely


def stop_loop() -> None:
    mixer.quit()


def play_sound(sound: io.BytesIO) -> None:
    sound_obj = pygame.mixer.Sound(sound)
    sound_obj.play()
