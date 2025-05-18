"""Level module for Pac-Man One Piece edition."""

import random

class Level:
    """Represents the game level, including maze generation."""

    def __init__(self, width: int, height: int, cell_size: int) -> None:
        """Initializes the level with a dynamic grid."""
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [['#' for _ in range(self.width)] for _ in range(self.height)]
        self.tile_count = 0  # Counter for open tiles
        self.generate_maze(1, 1)

    def generate_maze(self, x: int, y: int) -> None:
        """DFS-based maze generation ensuring correct tile count."""
        self.tile_count = 0
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.SystemRandom().shuffle(directions)

        if self.grid[y][x] != '.':
            self.grid[y][x] = '.'
            self.tile_count += 1

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1 and self.grid[ny][nx] == '#':
                self.grid[ny][nx] = '.'
                self.grid[y + dy // 2][x + dx // 2] = '.'
                self.tile_count += 2
                self.generate_maze(nx, ny)

        # Randomly create additional intersections
        if random.SystemRandom().random() < 0.2:
            self.create_crossroad(x, y)

    def create_crossroad(self, x: int, y: int) -> None:
        """Forces the creation of crossroads within limits."""
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.SystemRandom().shuffle(directions)

        for dx, dy in directions[:random.SystemRandom().randint(2, 3)]:
            nx, ny = x + dx, y + dy
            if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1 and self.grid[ny][nx] == '#':
                self.grid[ny][nx] = '.'
                self.tile_count += 1

    def display(self) -> None:
        """Prints the maze grid for debugging."""
        for row in self.grid:
            print("".join(row))

    def get_tile_count(self) -> int:
        """Recounts open tiles dynamically."""
        return sum(row.count(".") for row in self.grid)
