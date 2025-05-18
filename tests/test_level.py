import pytest
from level import Level

@pytest.fixture
def level():
    """Creates a level instance for testing."""
    return Level(width=21, height=11, cell_size=32)

def test_level_initialization(level):
    """Tests if the level initializes correctly with correct attributes."""
    assert level.width == 21
    assert level.height == 11
    assert isinstance(level.grid, list)
    assert len(level.grid) == level.height  # Correct number of rows
    assert len(level.grid[0]) == level.width  # Correct number of columns

def test_maze_generation(level):
    """Ensures maze generation creates open paths."""
    level.generate_maze(1, 1)
    assert level.grid[1][1] == "."  # The starting position should be open
    assert level.get_tile_count() > 0  # Ensure some tiles are opened

def test_create_crossroad(level):
    """Checks if crossroads are being created."""
    prev_tile_count = level.get_tile_count()
    level.create_crossroad(5, 5)
    assert level.get_tile_count() > prev_tile_count  # More tiles should be open

def test_get_tile_count(level):
    """Ensures tile counting returns the correct number of open spaces."""
    level.generate_maze(1, 1)
    open_tiles = level.get_tile_count()
    assert open_tiles == sum(row.count(".") for row in level.grid)  # Dynamic check

def test_display_output(level, capsys):
    """Verifies that display() prints the correct output."""
    level.display()
    captured = capsys.readouterr()
    assert len(captured.out.strip()) > 0  # Output should not be empty
