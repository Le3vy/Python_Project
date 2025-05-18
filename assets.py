import pygame
import os
import sys
from settings import CELL_SIZE

def get_resource_path(relative_path):
    """ PyInstaller futtatási környezethez igazítja az elérési utakat. """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)

def load_texture(file_path: str, size: tuple[int, int]) -> pygame.Surface:
    """Loads and scales a texture, handling PyInstaller paths."""
    full_path = get_resource_path(file_path)  # Módosított elérési út
    try:
        return pygame.transform.scale(pygame.image.load(full_path), size)
    except pygame.error as err:
        print(f"Error loading texture {full_path}: {err}")
        return pygame.Surface(size)  # Return empty surface

# Load textures dynamically based on CELL_SIZE
wall_texture = load_texture("sprites/barrel.png", (CELL_SIZE, CELL_SIZE))
floor_texture = load_texture("sprites/meat.png", (CELL_SIZE - 10, CELL_SIZE - 10))
grass_texture = load_texture("sprites/grass.png", (CELL_SIZE, CELL_SIZE))
tile_texture = load_texture("sprites/tile.png", (CELL_SIZE, CELL_SIZE))
