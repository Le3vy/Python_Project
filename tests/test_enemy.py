import pytest
import random
from enemy import Enemy
from settings import CELL_SIZE

@pytest.fixture
def mock_level():
    """Creates a mock level with an open grid for testing."""
    class MockLevel:
        width = 21
        height = 11
        grid = [["."] * 21 for _ in range(11)]  # Open grid (walkable)
    return MockLevel()

@pytest.fixture
def enemy(mock_level):
    """Creates an enemy instance for testing."""
    return Enemy(100, 100, speed=5, level=mock_level)

def test_enemy_initialization(enemy):
    """Tests if the enemy initializes correctly."""
    assert enemy.x == 100
    assert enemy.y == 100
    assert enemy.speed == 5
    assert isinstance(enemy.direction, tuple)

def test_enemy_movement(enemy):
    """Tests if the enemy moves within valid positions."""
    prev_x, prev_y = enemy.x, enemy.y
    enemy.move(player_x=200, player_y=200)  # Simulate movement
    assert (enemy.x, enemy.y) != (prev_x, prev_y)  # Enemy should move

def test_enemy_stuck_change_direction(enemy):
    """Checks if the enemy changes direction when stuck."""
    enemy.direction = (0, 1)  # Force enemy to move downward
    enemy.level.grid[enemy.y // CELL_SIZE][enemy.x // CELL_SIZE] = "#"  # Simulate wall
    enemy.move(player_x=200, player_y=200)
    assert enemy.direction != (0, 1)  # Direction should change

def test_enemy_chase_player(enemy):
    """Ensures enemy moves toward the player when within range."""
    player_x, player_y = 120, 120
    prev_x, prev_y = enemy.x, enemy.y
    enemy.chase_player(player_x, player_y)
    assert abs(enemy.x - player_x) + abs(enemy.y - player_y) < abs(prev_x - player_x) + abs(prev_y - player_y)

def test_enemy_collision(enemy):
    """Checks if collision detection works correctly."""
    player_x, player_y = enemy.x, enemy.y  # Player and enemy in the same spot
    assert enemy.check_collision(player_x, player_y) == True

    player_x, player_y = enemy.x + CELL_SIZE * 2, enemy.y + CELL_SIZE * 2  # Player far away
    assert enemy.check_collision(player_x, player_y) == False
