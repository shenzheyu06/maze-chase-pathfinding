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
from pathfinding.comparison import SearchComparison, compare_searches
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
    comparisons: dict[str, SearchComparison],
    algorithm_name: str,
    debug_mode: bool,
) -> None:
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 4 if debug_mode else 19))

    if not debug_mode:
        return

    debug_text = font.render("DEBUG MODE", True, TEXT_COLOR)
    screen.blit(debug_text, (10, 31))

    for row, name in enumerate(("BFS", "A*")):
        comparison = comparisons[name]
        path_length = max(0, len(comparison.result.path) - 1)
        marker = ">" if name == algorithm_name else " "
        y = 4 + row * 27
        columns = (
            (160, f"{marker} {name}"),
            (250, f"{path_length} steps"),
            (370, f"{len(comparison.result.explored)} visited"),
            (490, f"{comparison.average_ms:.3f} ms avg"),
        )
        for x, label in columns:
            text = font.render(label, True, TEXT_COLOR)
            screen.blit(text, (x, y))


def draw_status_screen(
    screen: pygame.Surface,
    font: pygame.font.Font,
    message: str,
    prompt: str,
) -> None:
    end_text = font.render(
        message,
        True,
        GAME_OVER_COLOR,
    )

    prompt_text = font.render(
        prompt,
        True,
        GAME_OVER_COLOR,
    )

    end_rect = end_text.get_rect(
        center=(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 - 20,
        )
    )

    prompt_rect = prompt_text.get_rect(
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
        prompt_text,
        prompt_rect,
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
    font = pygame.font.Font(None, 24)
    end_font = pygame.font.Font(None, 28)

    maze, player, ghost = reset_game()

    running = True
    game_over = False
    won = False
    paused = False
    pause_started_at = 0
    algorithm_name = "BFS"
    debug_mode = False
    show_exploration = True
    show_path = True
    comparison_positions = None
    comparisons = None

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
                        comparison_positions = None

                    elif event.key == pygame.K_ESCAPE:
                        running = False

                    continue

                if event.key == pygame.K_SPACE:
                    if paused:
                        ghost.last_move_time += (
                            pygame.time.get_ticks() - pause_started_at
                        )
                        paused = False
                    else:
                        pause_started_at = pygame.time.get_ticks()
                        paused = True
                    continue

                if paused:
                    if event.key == pygame.K_ESCAPE:
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

        positions = (ghost.position, player.position)
        if positions != comparison_positions:
            comparisons = compare_searches(maze, *positions)
            comparison_positions = positions
        result = comparisons[algorithm_name].result

        if not game_over and not won and not paused:
            current_time = pygame.time.get_ticks()
            previous_ghost_position = ghost.position

            ghost.move_along_path(
                result.path,
                current_time,
            )

            if ghost.position != previous_ghost_position:
                comparison_positions = (ghost.position, player.position)
                comparisons = compare_searches(maze, *comparison_positions)
                result = comparisons[algorithm_name].result

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
            comparisons,
            algorithm_name,
            debug_mode,
        )

        if game_over or won:
            draw_status_screen(
                screen,
                end_font,
                "GAME OVER" if game_over else "YOU WIN!",
                "Press R to restart",
            )
        elif paused:
            draw_status_screen(
                screen,
                end_font,
                "PAUSED",
                "Press Space to resume",
            )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
