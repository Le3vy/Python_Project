import pygame
import os
import sys

# Initialize pygame
pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH: int = info.current_w
SCREEN_HEIGHT: int = info.current_h

# Dynamic Cell Sizing
MAZE_WIDTH = 21
MAZE_HEIGHT = 11
CELL_SIZE = min(SCREEN_WIDTH // MAZE_WIDTH, SCREEN_HEIGHT // MAZE_HEIGHT)

# Display settings
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Pac-Man x One Piece")
clock: pygame.time.Clock = pygame.time.Clock()

# Function to get correct path for bundled files
def get_resource_path(relative_path):
    """ PyInstaller futtatási környezethez igazítja az elérési utakat. """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)

# Sound settings
pygame.mixer.init()
try:
    music_path = get_resource_path("mp3/music.mp3")  # Új elérési út
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
except pygame.error as err:
    print(f"Error loading music: {err}")