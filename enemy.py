"""Enemy module for Pac-Man One Piece edition."""

import random
import pygame
import os
import sys
from settings import CELL_SIZE

# Constants
ENEMY_SIZE = CELL_SIZE
MOVE_STEP = CELL_SIZE // 10  # Adjusted for dynamic grid size
CHASE_RANGE = 160

def get_resource_path(relative_path):
    """ PyInstaller futtatási környezethez igazítja az elérési utakat. """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)

class Enemy:
    """Represents an enemy character in the game."""

    def __init__(self, x: int, y: int, speed: int, level) -> None:
        """Initializes the enemy."""
        self.x = x
        self.y = y
        self.speed = speed
        self.level = level
        self.direction = random.SystemRandom().choice(
            [(0, -1), (0, 1), (-1, 0), (1, 0)])  # Random initial direction

        # Load enemy sprite with PyInstaller compatibility
        enemy_sprite_path = get_resource_path("sprites/enemy.png")
        self.image = pygame.transform.scale(
            pygame.image.load(enemy_sprite_path), (ENEMY_SIZE, ENEMY_SIZE)
        )

    def correct_position(self) -> None:
        """Moves the enemy to the nearest valid tile if it spawns inside a wall."""
        for dx in [-CELL_SIZE, 0, CELL_SIZE]:
            for dy in [-CELL_SIZE, 0, CELL_SIZE]:
                if self.is_valid_move(self.x + dx, self.y + dy):
                    self.x += dx
                    self.y += dy
                    return  # Stop once a valid position is found

    def move(self, player_x: int, player_y: int) -> None:
        """Moves the enemy towards the player while avoiding walls."""
        if not self.is_valid_move(self.x, self.y):  # If inside a wall, reposition
            self.correct_position()

        next_x = self.x + self.direction[0] * MOVE_STEP
        next_y = self.y + self.direction[1] * MOVE_STEP

        if self.is_valid_move(next_x, next_y):
            self.x, self.y = next_x, next_y
        else:
            self.direction = random.SystemRandom().choice(
                [(0, -1), (0, 1), (-1, 0), (1, 0)])  # Change direction if stuck

        if abs(self.x - player_x) + abs(self.y - player_y) < CHASE_RANGE:
            self.chase_player(player_x, player_y)

    def chase_player(self, player_x: int, player_y: int) -> None:
        """Moves enemy towards the player using basic pathfinding."""
        possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        best_move = None
        min_distance = float("inf")

        for dx, dy in possible_moves:
            next_x, next_y = self.x + dx * MOVE_STEP, self.y + dy * MOVE_STEP
            if self.is_valid_move(next_x, next_y):
                distance_to_player = abs(next_x - player_x) + abs(next_y - player_y)
                if distance_to_player < min_distance:
                    min_distance = distance_to_player
                    best_move = (dx, dy)

        if best_move:
            self.direction = best_move

    def is_valid_move(self, x: int, y: int) -> bool:
        """Checks if the enemy remains within walkable tiles."""
        grid_x1, grid_y1 = x // ENEMY_SIZE, y // ENEMY_SIZE
        grid_x2, grid_y2 = ((x + ENEMY_SIZE - 1) // ENEMY_SIZE,
                            (y + ENEMY_SIZE - 1) // ENEMY_SIZE)

        return (
            0 <= grid_x1 < self.level.width
            and 0 <= grid_y1 < self.level.height
            and 0 <= grid_x2 < self.level.width
            and 0 <= grid_y2 < self.level.height
            and self.level.grid[grid_y1][grid_x1] == "."
            and self.level.grid[grid_y2][grid_x2] == "."
        )

    def check_collision(self, player_x: int, player_y: int) -> bool:
        """Checks if the enemy touches the player."""
        return abs(self.x - player_x) < ENEMY_SIZE and abs(self.y - player_y) < ENEMY_SIZE

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the enemy on the screen."""
        screen.blit(self.image, (self.x, self.y))
