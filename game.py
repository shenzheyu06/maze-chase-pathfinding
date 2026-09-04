import pygame

from ghost import Ghost
from maze import (
    COLUMNS,
    HUD_HEIGHT,
    PATH_COLOR,
    ROWS,
    TILE_SIZE,
    create_maze,
    draw_maze,
    find_start,
    validate_maze,
)
from pathfinding.bfs import bfs
from player import Player


FPS = 60

BFS_PATH_COLOR = (50, 200, 100)
TEXT_COLOR = (255, 255, 255)
GAME_OVER_COLOR = (255, 255, 255)

WINDOW_WIDTH = COLUMNS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE + HUD_HEIGHT


def grid_center(
    row: int,
    column: int,
) -> tuple[int, int]:
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
    for row, column in path[1:-1]:
        pygame.draw.circle(
            screen,
            BFS_PATH_COLOR,
            grid_center(row, column),
            5,
        )


def draw_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    score: int,
    path_length: int,
) -> None:
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


def entities_collide(
    player: Player,
    ghost: Ghost,
) -> bool:
    return player.position == ghost.position


def reset_game() -> tuple[
    list[list[str]],
    Player,
    Ghost,
]:
    maze = create_maze()

    player_row, player_column = find_start(
        maze,
        "P",
    )

    ghost_row, ghost_column = find_start(
        maze,
        "G",
    )

    player = Player(
        player_row,
        player_column,
    )

    ghost = Ghost(
        ghost_row,
        ghost_column,
    )

    return maze, player, ghost


def run_game() -> None:
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

    maze, player, ghost = reset_game()

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        maze, player, ghost = reset_game()
                        game_over = False
                        ghost.reset_move_timer()

                    elif event.key == pygame.K_ESCAPE:
                        running = False

                    continue

                if event.key in (
                    pygame.K_UP,
                    pygame.K_w,
                ):
                    player.move(
                        maze,
                        -1,
                        0,
                    )

                elif event.key in (
                    pygame.K_DOWN,
                    pygame.K_s,
                ):
                    player.move(
                        maze,
                        1,
                        0,
                    )

                elif event.key in (
                    pygame.K_LEFT,
                    pygame.K_a,
                ):
                    player.move(
                        maze,
                        0,
                        -1,
                    )

                elif event.key in (
                    pygame.K_RIGHT,
                    pygame.K_d,
                ):
                    player.move(
                        maze,
                        0,
                        1,
                    )

                elif event.key == pygame.K_ESCAPE:
                    running = False

                if entities_collide(
                    player,
                    ghost,
                ):
                    game_over = True

        bfs_path = bfs(
            maze,
            ghost.position,
            player.position,
        )

        if not game_over:
            current_time = pygame.time.get_ticks()

            ghost.move_along_path(
                bfs_path,
                current_time,
            )

            if entities_collide(
                player,
                ghost,
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

        player.draw(screen)
        ghost.draw(screen)

        draw_hud(
            screen,
            font,
            player.score,
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