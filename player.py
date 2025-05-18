"""Player module for Pac-Man One Piece edition."""

import pygame
import os
import sys
from settings import CELL_SIZE

PLAYER_SPEED = CELL_SIZE // 8  # Movement speed scales with screen size

def get_resource_path(relative_path):
    """ PyInstaller futtatási környezethez igazítja az elérési utakat. """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)

class Player:
    """Represents the player character in the game."""

    def __init__(self, x: int, y: int, level) -> None:
        """Initializes player with scalable attributes."""
        self.x = x
        self.y = y
        self.level = level

        # Load dynamically scaled sprites with adjusted paths
        self.sprites = {
            "idle": pygame.transform.scale(pygame.image.load(get_resource_path("sprites/idle.png")),
                                           (CELL_SIZE, CELL_SIZE)),
            "walk_right": [pygame.transform.scale(pygame.image.load(get_resource_path(f"sprites/walk_right_{i}.png")),
                                                  (CELL_SIZE, CELL_SIZE))
                           for i in range(1, 4)],
            "walk_left": [pygame.transform.scale(pygame.image.load(get_resource_path(f"sprites/walk_left_{i}.png")),
                                                 (CELL_SIZE, CELL_SIZE))
                          for i in range(1, 4)]
        }

        self.current_animation = "idle"
        self.frame_index = 0

    def get_grid_position(self) -> tuple[int, int]:
        """Returns the player's position on the grid."""
        return round(self.x / CELL_SIZE), round(self.y / CELL_SIZE)

    def can_move(self, new_x: int, new_y: int) -> bool:
        """Ensures smooth movement by checking multiple edge positions, not just corners."""
        buffer = CELL_SIZE // 4  # Allow small margin for smoother movement

        # Check multiple points along the edges, instead of just corners
        edge_x1 = (new_x + buffer) // CELL_SIZE
        edge_x2 = (new_x + CELL_SIZE - buffer) // CELL_SIZE
        edge_y1 = (new_y + buffer) // CELL_SIZE
        edge_y2 = (new_y + CELL_SIZE - buffer) // CELL_SIZE

        return (
                0 <= edge_x1 < self.level.width and 0 <= edge_y1 < self.level.height and
                0 <= edge_x2 < self.level.width and 0 <= edge_y2 < self.level.height and
                self.level.grid[edge_y1][edge_x1] == "." and
                self.level.grid[edge_y1][edge_x2] == "." and
                self.level.grid[edge_y2][edge_x1] == "." and
                self.level.grid[edge_y2][edge_x2] == "."
        )

    def move(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Handles player movement dynamically."""
        if keys[pygame.K_LEFT] and self.can_move(self.x - PLAYER_SPEED, self.y):
            self.x -= PLAYER_SPEED
            self.current_animation = "walk_left"
        if keys[pygame.K_RIGHT] and self.can_move(self.x + PLAYER_SPEED, self.y):
            self.x += PLAYER_SPEED
            self.current_animation = "walk_right"
        if keys[pygame.K_UP] and self.can_move(self.x, self.y - PLAYER_SPEED):
            self.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.can_move(self.x, self.y + PLAYER_SPEED):
            self.y += PLAYER_SPEED

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the player at the correct scale."""
        frame = self.sprites[self.current_animation][self.frame_index] if isinstance(
            self.sprites[self.current_animation], list) else self.sprites[self.current_animation]
        screen.blit(frame, (self.x, self.y))

    def update_animation(self) -> None:
        """Updates the player's animation frame."""
        if isinstance(self.sprites[self.current_animation], list):
            self.frame_index = (self.frame_index + 1) % len(self.sprites[self.current_animation])
