"""Main module for the Pac-Man One Piece edition game."""

import pygame
import game_logic
from settings import screen, SCREEN_WIDTH, SCREEN_HEIGHT
from game_objects import player
from game_logic import draw, update

# Font setup for score display
font: pygame.font.Font = pygame.font.Font(None, int(SCREEN_WIDTH // 50))  # Scales dynamically

# Volume Bar Setup (scaled dynamically)
VOLUME_BAR = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT - SCREEN_HEIGHT // 20,
                         SCREEN_WIDTH // 5, SCREEN_HEIGHT // 50)
VOLUME_HANDLE = pygame.Rect(VOLUME_BAR.x + VOLUME_BAR.width // 2, VOLUME_BAR.y - 5,
                            SCREEN_WIDTH // 100, SCREEN_HEIGHT // 25)
CURRENT_VOLUME = 0.5
pygame.mixer.music.set_volume(CURRENT_VOLUME)
DRAGGING = False

# Exit button setup
EXIT_BUTTON = pygame.Rect(SCREEN_WIDTH // 20, SCREEN_HEIGHT - SCREEN_HEIGHT // 20,
                          SCREEN_WIDTH // 10, SCREEN_HEIGHT // 20)
EXIT_TEXT = font.render("Exit", True, (255, 255, 255))


def draw_volume_bar() -> None:
    """Draws the dynamically scaled volume bar and handle."""
    pygame.draw.rect(screen, (200, 200, 200), VOLUME_BAR)
    pygame.draw.rect(screen, (255, 100, 100), VOLUME_HANDLE)


def draw_exit_button() -> None:
    """Draws the dynamically scaled exit button."""
    pygame.draw.rect(screen, (200, 0, 0), EXIT_BUTTON)
    screen.blit(EXIT_TEXT, (EXIT_BUTTON.x + EXIT_BUTTON.width // 4,
                            EXIT_BUTTON.y + EXIT_BUTTON.height // 4))


def handle_events() -> bool:
    """Processes user input events and returns whether the game is still running."""
    global DRAGGING, CURRENT_VOLUME

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.MOUSEBUTTONDOWN and EXIT_BUTTON.collidepoint(event.pos)
        ):
            return False

        if event.type == pygame.KEYDOWN:
            print(f"Key pressed: {event.key}")

        if event.type == pygame.MOUSEBUTTONDOWN and VOLUME_HANDLE.collidepoint(event.pos):
            DRAGGING = True

        if event.type == pygame.MOUSEBUTTONUP:
            DRAGGING = False

        if event.type == pygame.MOUSEMOTION and DRAGGING:
            VOLUME_HANDLE.x = max(VOLUME_BAR.x, min(event.pos[0], VOLUME_BAR.x + VOLUME_BAR.width))
            CURRENT_VOLUME = (VOLUME_HANDLE.x - VOLUME_BAR.x) / VOLUME_BAR.width
            pygame.mixer.music.set_volume(CURRENT_VOLUME)

    return True


def game_loop() -> None:
    """Runs the main game loop."""
    running = True
    while running:
        running = handle_events()

        keys = pygame.key.get_pressed()
        player.move(keys)
        player.update_animation()

        screen.fill((0, 0, 0))
        draw()
        draw_volume_bar()
        draw_exit_button()

        # Display score in top-right corner dynamically
        score_text = font.render(f"Pontok: {game_logic.PLAYER_SCORE}",
                                 True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH - SCREEN_WIDTH // 10,
                                 SCREEN_HEIGHT-SCREEN_HEIGHT // 20))

        update()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    game_loop()