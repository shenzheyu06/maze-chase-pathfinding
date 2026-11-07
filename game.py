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
from pathfinding.astar import astar_search
from pathfinding.bfs import bfs_search
from player import Player


FPS = 60

ROUTE_COLOR = (50, 200, 100)
EXPLORED_COLOR = (150, 90, 230, 70)
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


def draw_path(
    screen: pygame.Surface,
    path: list[tuple[int, int]],
) -> None:
    for row, column in path[1:-1]:
        pygame.draw.circle(
            screen,
            ROUTE_COLOR,
            grid_center(row, column),
            5,
        )


def draw_explored_tiles(
    screen: pygame.Surface,
    explored: list[tuple[int, int]],
) -> None:
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    tile.fill(EXPLORED_COLOR)

    for row, column in explored:
        screen.blit(
            tile,
            (column * TILE_SIZE, row * TILE_SIZE + HUD_HEIGHT),
        )


def draw_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    score: int,
    path_length: int,
    visited_count: int,
    algorithm_name: str,
) -> None:
    text = font.render(
        (
            f"Score: {score}    "
            f"{algorithm_name} path: {path_length}    "
            f"Visited: {visited_count}"
        ),
        True,
        TEXT_COLOR,
    )

    screen.blit(
        text,
        (10, 8),
    )


def draw_end_screen(
    screen: pygame.Surface,
    font: pygame.font.Font,
    message: str,
) -> None:
    end_text = font.render(
        message,
        True,
        GAME_OVER_COLOR,
    )

    restart_text = font.render(
        "Press R to restart",
        True,
        GAME_OVER_COLOR,
    )

    end_rect = end_text.get_rect(
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
        end_text,
        end_rect,
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
    won = False
    algorithm_name = "BFS"
    debug_mode = False
    show_exploration = True
    show_path = True
    pathfinders = {"BFS": bfs_search, "A*": astar_search}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    debug_mode = not debug_mode
                elif debug_mode and event.key == pygame.K_v:
                    show_exploration = not show_exploration
                elif debug_mode and event.key == pygame.K_p:
                    show_path = not show_path

                if game_over or won:
                    if event.key == pygame.K_r:
                        maze, player, ghost = reset_game()
                        game_over = False
                        won = False
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

                elif event.key == pygame.K_TAB:
                    algorithm_name = "A*" if algorithm_name == "BFS" else "BFS"

                if entities_collide(
                    player,
                    ghost,
                ):
                    game_over = True
                elif not any("." in row for row in maze):
                    won = True

        pathfinder = pathfinders[algorithm_name]
        result = pathfinder(
            maze,
            ghost.position,
            player.position,
        )

        if not game_over and not won:
            current_time = pygame.time.get_ticks()
            previous_ghost_position = ghost.position

            ghost.move_along_path(
                result.path,
                current_time,
            )

            if ghost.position != previous_ghost_position:
                result = pathfinder(
                    maze,
                    ghost.position,
                    player.position,
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

        if debug_mode and show_exploration:
            draw_explored_tiles(
                screen,
                result.explored,
            )

        if debug_mode and show_path:
            draw_path(
                screen,
                result.path,
            )

        player.draw(screen)
        ghost.draw(screen)

        draw_hud(
            screen,
            font,
            player.score,
            max(0, len(result.path) - 1),
            len(result.explored),
            algorithm_name,
        )

        if game_over or won:
            draw_end_screen(
                screen,
                font,
                "GAME OVER" if game_over else "YOU WIN!",
            )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
