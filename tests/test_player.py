import pytest
from settings import CELL_SIZE
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings import CELL_SIZE
from player import Player



@pytest.fixture
def mock_level():
    """Creates a mock level with a simple grid for testing."""

    class MockLevel:
        width = 21
        height = 11
        grid = [["."] * 21 for _ in range(11)]  # Empty grid for testing

    return MockLevel()


@pytest.fixture
def player(mock_level):
    """Creates a player instance for testing."""
    return Player(100, 100, mock_level)


def test_player_initialization(player):
    """Tests if the player initializes correctly."""
    assert player.x == 100
    assert player.y == 100
    assert player.current_animation == "idle"


def test_get_grid_position(player):
    """Checks if the grid position function works correctly."""
    assert player.get_grid_position() == (100 // CELL_SIZE, 100 // CELL_SIZE)


def test_can_move(player):
    """Ensures the player can move within valid positions."""
    assert player.can_move(150, 150) == True  # Inside the grid
    assert player.can_move(-50, -50) == False  # Out of bounds


def test_animation_update(player):
    """Tests animation frame updates with a multi-frame animation."""
    player.current_animation = "walk_right"  # Ensure a multi-frame animation is used
    player.update_animation()
    assert player.frame_index == 1

