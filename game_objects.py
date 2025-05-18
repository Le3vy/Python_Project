"""Game objects module for Pac-Man One Piece edition."""

from player import Player
from level import Level
from settings import MAZE_WIDTH, MAZE_HEIGHT, CELL_SIZE  # Corrected import
from enemy import Enemy

# Initialize game objects
level = Level(MAZE_WIDTH, MAZE_HEIGHT, CELL_SIZE)

# Player setup
PLAYER_START_X = 1 * CELL_SIZE
PLAYER_START_Y = 1 * CELL_SIZE
player = Player(PLAYER_START_X, PLAYER_START_Y, level)

# Enemy setup
ENEMY_START_X = 5 * CELL_SIZE
ENEMY_START_Y = 5 * CELL_SIZE
enemy = Enemy(ENEMY_START_X, ENEMY_START_Y,1, level)

# Tracking visited cells
visited_cells: set[tuple[int, int]] = set()

# Player score initialization
player_score: int = 0  # Start at 0 points
