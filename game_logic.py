"""Game logic module for Pac-Man One Piece edition."""

import pygame
from enemy import Enemy
from settings import screen, CELL_SIZE  # Dynamically use CELL_SIZE
from assets import wall_texture, floor_texture, grass_texture, tile_texture
from game_objects import player, level, visited_cells, enemy

# Constants
DEFAULT_DIFFICULTY = 500

TILE_COUNT = level.get_tile_count()
LAST_ENEMY_MOVE_TIME = 0  # Track last enemy movement
PLAYER_SCORE = 0
DIFFICULTY_LEVEL = DEFAULT_DIFFICULTY


def update() -> None:
    """Updates the game state, including player movement, enemy behavior, and scoring."""
    global LAST_ENEMY_MOVE_TIME, PLAYER_SCORE, TILE_COUNT

    player_x, player_y = map(int, player.get_grid_position())  # Ensure integer indices
    print(f"Player grid position: {player_x}, {player_y}")
    print(f"Enemy grid position: {enemy.x}, {enemy.y}")
    print(f"Speed: {DIFFICULTY_LEVEL}")

    current_time = pygame.time.get_ticks()  # Get current time

    # Enemy movement timing logic
    if current_time - LAST_ENEMY_MOVE_TIME > DIFFICULTY_LEVEL:
        enemy.move(player_x * CELL_SIZE, player_y * CELL_SIZE)
        LAST_ENEMY_MOVE_TIME = current_time

    # Update player scoring logic
    if (player_x, player_y) not in visited_cells and level.grid[player_y][player_x] == ".":
        visited_cells.add((player_x, player_y))
        print(f"Tile removed at: {player_x}, {player_y}")
        TILE_COUNT -= 1
        print(f"Remaining tiles: {TILE_COUNT}")
        PLAYER_SCORE += 100

    print(f"Score: {PLAYER_SCORE}")

    # Handle enemy interactions
    enemy.move(player_x * CELL_SIZE, player_y * CELL_SIZE)  # Update enemy movement
    if enemy.check_collision(player.x, player.y):
        PLAYER_SCORE = 0
        restart_game()

    # Advance to next level if all tiles are cleared
    if TILE_COUNT == 0:
        next_level()


def draw() -> None:
    """Draws the game environment, including the level, player, and enemy."""
    screen.fill((0, 0, 0))  # Clear screen
    updated_rects = []

    for y, row in enumerate(level.grid):
        for x, cell in enumerate(row):
            screen.blit(grass_texture, (x * CELL_SIZE, y * CELL_SIZE))
            updated_rects.append(pygame.Rect(x * CELL_SIZE, y * CELL_SIZE,
                                             CELL_SIZE, CELL_SIZE))

            if cell == ".":
                screen.blit(tile_texture, (x * CELL_SIZE, y * CELL_SIZE))
                updated_rects.append(pygame.Rect(x * CELL_SIZE, y * CELL_SIZE,
                                                 CELL_SIZE, CELL_SIZE))

                if (x, y) not in visited_cells:
                    screen.blit(floor_texture, (x * CELL_SIZE + 12, y * CELL_SIZE + 6))
                    updated_rects.append(pygame.Rect(x * CELL_SIZE, y * CELL_SIZE,
                                                     CELL_SIZE, CELL_SIZE))

            elif cell == "#":
                screen.blit(wall_texture, (x * CELL_SIZE, y * CELL_SIZE - 4))
                updated_rects.append(pygame.Rect(x * CELL_SIZE, y * CELL_SIZE,
                                                 CELL_SIZE, CELL_SIZE))

    enemy.draw(screen)  # Draw the enemy
    player.draw(screen)
    pygame.display.update(updated_rects)


def restart_game() -> None:
    """Resets the game state and generates a new level."""
    global enemy, TILE_COUNT, DIFFICULTY_LEVEL

    print("Game Over! Restarting with a new maze...")
    pygame.time.delay(1000)  # Short delay before restart

    # Regenerate maze properly
    level.grid = [['#' for _ in range(level.width)] for _ in range(level.height)]
    level.generate_maze(1, 1)

    TILE_COUNT = level.get_tile_count()  # Reset tile count
    visited_cells.clear()  # Ensure visited tiles don't interfere

    player.x, player.y = CELL_SIZE, CELL_SIZE  # Corrected placement
    enemy = Enemy(5 * CELL_SIZE, 5 * CELL_SIZE, 1, level)  # Start enemy at position (5,5)
    DIFFICULTY_LEVEL = DEFAULT_DIFFICULTY

    print(f"New TILE_COUNT after reset: {TILE_COUNT}")  # Debugging

def next_level() -> None:
    """Advances the game to the next level."""
    global enemy, TILE_COUNT, DIFFICULTY_LEVEL

    print("Next level! Generating a new maze...")
    level.grid = [['#' for _ in range(level.width)] for _ in range(level.height)]
    level.generate_maze(1, 1)
    player.x, player.y = CELL_SIZE, CELL_SIZE  # Corrected placement
    enemy = Enemy(5 * CELL_SIZE, 5 * CELL_SIZE, 1, level)  # Start enemy at position (5,5)

    DIFFICULTY_LEVEL = max(DIFFICULTY_LEVEL - 60, 5)
    TILE_COUNT = level.get_tile_count()
    visited_cells.clear()  # Reset visited cells and score

    print("New maze generated!")
