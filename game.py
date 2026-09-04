import pygame

from maze import (
    COLUMNS,
    HUD_HEIGHT,
    PATH_COLOR,
    ROWS,
    TILE_SIZE,
    create_maze,
    draw_maze,
    find_start,
    is_walkable,
    validate_maze,
)
from pathfinding.bfs import bfs


FPS = 60
GHOST_MOVE_DELAY = 300

PLAYER_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 50, 50)
BFS_PATH_COLOR = (50, 200, 100)
TEXT_COLOR = (255, 255, 255)
GAME_OVER_COLOR = (255, 255, 255)

WINDOW_WIDTH = COLUMNS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE + HUD_HEIGHT


def move_player(
    maze: list[list[str]],
    player_row: int,
    player_column: int,
    row_change: int,
    column_change: int,
) -> tuple[int, int]:
    """Move the player if the destination tile is walkable."""
    new_row = player_row + row_change
    new_column = player_column + column_change

    if is_walkable(
        maze,
        new_row,
        new_column,
    ):
        return new_row, new_column

    return player_row, player_column


def collect_pellet(
    maze: list[list[str]],
    row: int,
    column: int,
) -> bool:
    """Remove a pellet if one exists on the tile."""
    if maze[row][column] == ".":
        maze[row][column] = " "
        return True

    return False


def positions_collide(
    player_row: int,
    player_column: int,
    ghost_row: int,
    ghost_column: int,
) -> bool:
    """Return whether the player and ghost occupy the same tile."""
    return (
        player_row == ghost_row
        and player_column == ghost_column
    )


def reset_game() -> tuple[
    list[list[str]],
    int,
    int,
    int,
    int,
    int,
]:
    """Reset the maze, positions, and score."""
    maze = create_maze()

    player_row, player_column = find_start(
        maze,
        "P",
    )

    ghost_row, ghost_column = find_start(
        maze,
        "G",
    )

    score = 0

    return (
        maze,
        player_row,
        player_column,
        ghost_row,
        ghost_column,
        score,
    )


def grid_center(
    row: int,
    column: int,
) -> tuple[int, int]:
    """Convert a grid position to pixel coordinates."""
    x = (
        column * TILE_SIZE
        + TILE_SIZE // 2
    )

    y = (
        row * TILE_SIZE
        + TILE_SIZE // 2
        + HUD_HEIGHT
    )

    return x, y


def draw_bfs_path(
    screen: pygame.Surface,
    path: list[tuple[int, int]],
) -> None:
    """Draw the current BFS path."""
    for row, column in path[1:-1]:
        pygame.draw.circle(
            screen,
            BFS_PATH_COLOR,
            grid_center(row, column),
            5,
        )


def draw_player(
    screen: pygame.Surface,
    row: int,
    column: int,
) -> None:
    """Draw the player."""
    pygame.draw.circle(
        screen,
        PLAYER_COLOR,
        grid_center(row, column),
        TILE_SIZE // 3,
    )


def draw_ghost(
    screen: pygame.Surface,
    row: int,
    column: int,
) -> None:
    """Draw the ghost."""
    pygame.draw.circle(
        screen,
        GHOST_COLOR,
        grid_center(row, column),
        TILE_SIZE // 3,
    )


def draw_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    score: int,
    path_length: int,
) -> None:
    """Draw score and pathfinding information."""
    text = font.render(
        (
            f"Score: {score}    "
            f"BFS path length: {path_length}"
        ),
        True,
        TEXT_COLOR,
    )

    screen.blit(
        text,
        (10, 8),
    )


def draw_game_over(
    screen: pygame.Surface,
    font: pygame.font.Font,
) -> None:
    """Draw the game-over screen."""
    game_over_text = font.render(
        "GAME OVER",
        True,
        GAME_OVER_COLOR,
    )

    restart_text = font.render(
        "Press R to restart",
        True,
        GAME_OVER_COLOR,
    )

    game_over_rect = game_over_text.get_rect(
        center=(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 - 20,
        )
    )

    restart_rect = restart_text.get_rect(
        center=(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 + 20,
        )
    )

    screen.blit(
        game_over_text,
        game_over_rect,
    )

    screen.blit(
        restart_text,
        restart_rect,
    )


def run_game() -> None:
    """Initialize and run the game."""
    validate_maze()

    pygame.init()

    screen = pygame.display.set_mode(
        (
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
        )
    )

    pygame.display.set_caption(
        "Maze Chase Pathfinding"
    )

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    (
        maze,
        player_row,
        player_column,
        ghost_row,
        ghost_column,
        score,
    ) = reset_game()

    running = True
    game_over = False

    last_ghost_move = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if game_over:
                    if event.key == pygame.K_r:
                        (
                            maze,
                            player_row,
                            player_column,
                            ghost_row,
                            ghost_column,
                            score,
                        ) = reset_game()

                        game_over = False

                        last_ghost_move = (
                            pygame.time.get_ticks()
                        )

                    elif event.key == pygame.K_ESCAPE:
                        running = False

                    continue

                old_row = player_row
                old_column = player_column

                if event.key in (
                    pygame.K_UP,
                    pygame.K_w,
                ):
                    player_row, player_column = move_player(
                        maze,
                        player_row,
                        player_column,
                        -1,
                        0,
                    )

                elif event.key in (
                    pygame.K_DOWN,
                    pygame.K_s,
                ):
                    player_row, player_column = move_player(
                        maze,
                        player_row,
                        player_column,
                        1,
                        0,
                    )

                elif event.key in (
                    pygame.K_LEFT,
                    pygame.K_a,
                ):
                    player_row, player_column = move_player(
                        maze,
                        player_row,
                        player_column,
                        0,
                        -1,
                    )

                elif event.key in (
                    pygame.K_RIGHT,
                    pygame.K_d,
                ):
                    player_row, player_column = move_player(
                        maze,
                        player_row,
                        player_column,
                        0,
                        1,
                    )

                elif event.key == pygame.K_ESCAPE:
                    running = False

                player_moved = (
                    player_row != old_row
                    or player_column != old_column
                )

                if player_moved:
                    if collect_pellet(
                        maze,
                        player_row,
                        player_column,
                    ):
                        score += 10

                if positions_collide(
                    player_row,
                    player_column,
                    ghost_row,
                    ghost_column,
                ):
                    game_over = True

        player_position = (
            player_row,
            player_column,
        )

        ghost_position = (
            ghost_row,
            ghost_column,
        )

        bfs_path = bfs(
            maze,
            ghost_position,
            player_position,
        )

        if not game_over:
            current_time = pygame.time.get_ticks()

            if (
                current_time - last_ghost_move
                >= GHOST_MOVE_DELAY
            ):
                if len(bfs_path) > 1:
                    ghost_row, ghost_column = (
                        bfs_path[1]
                    )

                last_ghost_move = current_time

                if positions_collide(
                    player_row,
                    player_column,
                    ghost_row,
                    ghost_column,
                ):
                    game_over = True

        screen.fill(PATH_COLOR)

        draw_maze(
            screen,
            maze,
        )

        draw_bfs_path(
            screen,
            bfs_path,
        )

        draw_player(
            screen,
            player_row,
            player_column,
        )

        draw_ghost(
            screen,
            ghost_row,
            ghost_column,
        )

        draw_hud(
            screen,
            font,
            score,
            max(0, len(bfs_path) - 1),
        )

        if game_over:
            draw_game_over(
                screen,
                font,
            )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()