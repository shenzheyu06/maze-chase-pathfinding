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
    find_starts,
    validate_maze,
)
from pathfinding.astar import astar_search
from pathfinding.bfs import bfs_search
from pathfinding.comparison import SearchComparison, compare_searches
from pathfinding.flee import distances_from, flee_path
from pathfinding.separation import separate_path
from player import Player


FPS = 60
STARTING_LIVES = 3
POWER_DURATION_MS = 6000
GHOST_BONUS = 200
GHOST_COLORS = (
    (255, 50, 50),
    (255, 130, 190),
    (255, 165, 50),
    (50, 220, 230),
    (80, 220, 90),
    (180, 100, 255),
)
CHASE_ENTER_DISTANCE = 7
CHASE_EXIT_DISTANCE = 10

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
    include_destination: bool = False,
) -> None:
    visible_path = path[1:] if include_destination else path[1:-1]
    for row, column in visible_path:
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
    lives: int,
    power_remaining_ms: int,
    comparisons: dict[str, SearchComparison] | None,
    algorithm_name: str,
    debug_mode: bool,
    fleeing: bool = False,
    ghost_label: str | None = None,
) -> None:
    summary = f"Score: {score}    Lives: {lives}"
    if power_remaining_ms:
        summary += f"    Power: {(power_remaining_ms + 999) // 1000}s"
    summary_text = font.render(summary, True, TEXT_COLOR)
    screen.blit(summary_text, (10, 4 if debug_mode else 31))

    if not debug_mode:
        return

    debug_text = font.render("DEBUG MODE", True, TEXT_COLOR)
    screen.blit(debug_text, (520, 4))
    if fleeing:
        fleeing_text = font.render("FLEEING", True, TEXT_COLOR)
        screen.blit(fleeing_text, (400, 4))

    if comparisons is None:
        no_ghosts = font.render("No ghosts remaining", True, TEXT_COLOR)
        screen.blit(no_ghosts, (160, 31))
        return

    if ghost_label:
        label = font.render(ghost_label, True, TEXT_COLOR)
        screen.blit(label, (10, 31))

    if fleeing:
        chase_text = font.render("Chase stats", True, TEXT_COLOR)
        screen.blit(chase_text, (10, 58 if ghost_label else 31))

    for row, name in enumerate(("BFS", "A*")):
        comparison = comparisons[name]
        path_length = max(0, len(comparison.result.path) - 1)
        marker = ">" if name == algorithm_name else " "
        y = 31 + row * 27
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


def handle_collisions(
    player: Player,
    ghosts: list[Ghost],
    powered: bool,
) -> bool:
    """Return whether the player was caught by a non-vulnerable ghost."""
    for ghost in ghosts[:]:
        if not entities_collide(player, ghost):
            continue
        if powered:
            ghosts.remove(ghost)
            player.score += GHOST_BONUS
        else:
            return True
    return False


def reset_positions(player: Player, ghosts: list[Ghost]) -> None:
    player.reset_position()
    for ghost in ghosts:
        ghost.reset_position()


def reset_game() -> tuple[
    list[list[str]],
    Player,
    list[Ghost],
]:
    maze = create_maze()

    player_row, player_column = find_start(
        maze,
        "P",
    )

    ghost_starts = find_starts(maze, "G")

    player = Player(
        player_row,
        player_column,
    )

    ghosts = [
        Ghost(row, column, color=GHOST_COLORS[index % len(GHOST_COLORS)])
        for index, (row, column) in enumerate(ghost_starts)
    ]

    return maze, player, ghosts


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

    maze, player, ghosts = reset_game()
    selected_ghost = ghosts[0] if ghosts else None

    running = True
    game_over = False
    won = False
    lives = STARTING_LIVES
    powered_until = 0
    paused = False
    pause_started_at = 0
    algorithm_name = "BFS"
    debug_mode = False
    show_exploration = True
    show_path = True
    comparison_positions = None
    comparisons = None
    distance_player_position = None
    player_distances = None

    while running:
        life_lost_this_frame = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    debug_mode = not debug_mode
                    if debug_mode:
                        selected_ghost = ghosts[0] if ghosts else None
                        comparison_positions = None
                elif (
                    debug_mode
                    and event.key in (pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET)
                    and ghosts
                ):
                    direction = -1 if event.key == pygame.K_LEFTBRACKET else 1
                    selected_index = (ghosts.index(selected_ghost) + direction) % len(ghosts)
                    selected_ghost = ghosts[selected_index]
                    comparison_positions = None
                elif debug_mode and event.key == pygame.K_v:
                    show_exploration = not show_exploration
                elif debug_mode and event.key == pygame.K_p:
                    show_path = not show_path

                if game_over or won:
                    if event.key == pygame.K_r:
                        maze, player, ghosts = reset_game()
                        selected_ghost = ghosts[0] if ghosts else None
                        game_over = False
                        won = False
                        lives = STARTING_LIVES
                        powered_until = 0
                        for ghost in ghosts:
                            ghost.reset_move_timer()
                        comparison_positions = None
                        distance_player_position = None

                    elif event.key == pygame.K_ESCAPE:
                        running = False

                    continue

                if event.key == pygame.K_SPACE:
                    if paused:
                        paused_duration = pygame.time.get_ticks() - pause_started_at
                        for ghost in ghosts:
                            ghost.last_move_time += paused_duration
                        if powered_until:
                            powered_until += paused_duration
                        paused = False
                    else:
                        pause_started_at = pygame.time.get_ticks()
                        paused = True
                    continue

                if paused:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    continue

                if life_lost_this_frame:
                    continue

                collected = None
                if event.key in (
                    pygame.K_UP,
                    pygame.K_w,
                ):
                    collected = player.move(
                        maze,
                        -1,
                        0,
                    )

                elif event.key in (
                    pygame.K_DOWN,
                    pygame.K_s,
                ):
                    collected = player.move(
                        maze,
                        1,
                        0,
                    )

                elif event.key in (
                    pygame.K_LEFT,
                    pygame.K_a,
                ):
                    collected = player.move(
                        maze,
                        0,
                        -1,
                    )

                elif event.key in (
                    pygame.K_RIGHT,
                    pygame.K_d,
                ):
                    collected = player.move(
                        maze,
                        0,
                        1,
                    )

                elif event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_TAB:
                    algorithm_name = "A*" if algorithm_name == "BFS" else "BFS"

                if collected == "o":
                    powered_until = pygame.time.get_ticks() + POWER_DURATION_MS
                    distance_player_position = None
                    for ghost in ghosts:
                        ghost.previous_position = None
                        ghost.patrol_target = None

                if handle_collisions(
                    player, ghosts, pygame.time.get_ticks() < powered_until
                ):
                    lives -= 1
                    powered_until = 0
                    life_lost_this_frame = True
                    if lives == 0:
                        game_over = True
                    else:
                        reset_positions(player, ghosts)
                elif not any(tile in (".", "o") for row in maze for tile in row):
                    won = True

                if selected_ghost not in ghosts:
                    selected_ghost = ghosts[0] if ghosts else None

        if ghosts and not game_over and not won and not life_lost_this_frame:
            current_time = pygame.time.get_ticks()
            powered = current_time < powered_until
            if distance_player_position != player.position:
                player_distances = distances_from(maze, player.position)
                distance_player_position = player.position

            if not powered:
                for ghost in ghosts:
                    distance = player_distances.get(ghost.position, float("inf"))
                    was_chasing = ghost.chasing
                    ghost.chasing = (
                        distance < CHASE_EXIT_DISTANCE if was_chasing
                        else distance <= CHASE_ENTER_DISTANCE
                    )
                    if ghost.chasing != was_chasing:
                        ghost.patrol_target = None
                    if not ghost.chasing:
                        unavailable = {player.position} | {
                            other.position for other in ghosts if other is not ghost
                        }
                        other_targets = [
                            other.patrol_target for other in ghosts
                            if other is not ghost and other.patrol_target is not None
                        ]
                        ghost.ensure_patrol_target(
                            maze, unavailable, other_targets
                        )

        if ghosts and not game_over and not won and not paused and not life_lost_this_frame:
            search = bfs_search if algorithm_name == "BFS" else astar_search
            for ghost in ghosts[:]:
                if ghost not in ghosts:
                    continue
                if current_time - ghost.last_move_time < ghost.move_delay:
                    continue
                occupied_positions = {
                    other.position for other in ghosts if other is not ghost
                }
                if powered:
                    movement_path = flee_path(
                        maze, ghost.position, ghost.previous_position, player_distances
                    )
                else:
                    goal = player.position if ghost.chasing else ghost.patrol_target
                    movement_path = (
                        search(maze, ghost.position, goal).path
                        if goal is not None else [ghost.position]
                    )
                movement_path = separate_path(
                    maze,
                    ghost.position,
                    movement_path,
                    occupied_positions,
                    player.position if powered or ghost.chasing else (
                        ghost.patrol_target or ghost.position
                    ),
                    powered,
                )
                ghost.move_along_path(
                    movement_path, current_time, occupied_positions
                )

                if not powered and not ghost.chasing and ghost.position == ghost.patrol_target:
                    ghost.patrol_target = None
                    unavailable = {player.position} | {
                        other.position for other in ghosts if other is not ghost
                    }
                    other_targets = [
                        other.patrol_target for other in ghosts
                        if other is not ghost and other.patrol_target is not None
                    ]
                    ghost.ensure_patrol_target(maze, unavailable, other_targets)

                if handle_collisions(player, ghosts, powered):
                    lives -= 1
                    powered_until = 0
                    if lives == 0:
                        game_over = True
                    else:
                        reset_positions(player, ghosts)
                    break

                if selected_ghost not in ghosts:
                    selected_ghost = ghosts[0] if ghosts else None

        display_time = pause_started_at if paused else pygame.time.get_ticks()
        fleeing = bool(ghosts) and display_time < powered_until
        patrolling = (
            selected_ghost is not None
            and not fleeing
            and not selected_ghost.chasing
        )
        if selected_ghost is not None:
            comparison_goal = (
                selected_ghost.patrol_target if patrolling else player.position
            )
            if comparison_goal is None:
                comparison_goal = player.position
            positions = (selected_ghost, selected_ghost.position, comparison_goal)
            if positions != comparison_positions:
                comparisons = compare_searches(
                    maze, selected_ghost.position, comparison_goal
                )
                comparison_positions = positions
            result = comparisons[algorithm_name].result
        else:
            comparison_positions = None
            comparisons = None
            result = None

        if fleeing:
            if distance_player_position != player.position:
                player_distances = distances_from(maze, player.position)
                distance_player_position = player.position
            display_path = flee_path(
                maze, selected_ghost.position, selected_ghost.previous_position,
                player_distances,
            )
            explored = list(player_distances)
        else:
            display_path = result.path if result is not None else []
            explored = result.explored if result is not None else []

        avoiding = False
        if debug_mode and show_path and selected_ghost is not None:
            other_positions = {
                ghost.position for ghost in ghosts if ghost is not selected_ghost
            }
            separated_path = separate_path(
                maze,
                selected_ghost.position,
                display_path,
                other_positions,
                player.position if fleeing else comparison_goal,
                fleeing,
            )
            avoiding = separated_path != display_path
            display_path = separated_path

        screen.fill(PATH_COLOR)

        draw_maze(
            screen,
            maze,
        )

        if debug_mode and show_exploration and ghosts:
            draw_explored_tiles(
                screen,
                explored,
            )

        if debug_mode and show_path and ghosts:
            draw_path(
                screen,
                display_path,
                fleeing or patrolling or avoiding,
            )

        player.draw(screen)
        for ghost in ghosts:
            ghost.draw(
                screen,
                display_time < powered_until,
                debug_mode and ghost is selected_ghost,
            )

        ghost_label = (
            f"Ghost {ghosts.index(selected_ghost) + 1}/{len(ghosts)}"
            if selected_ghost is not None else None
        )

        draw_hud(
            screen,
            font,
            player.score,
            lives,
            max(0, powered_until - display_time),
            comparisons,
            algorithm_name,
            debug_mode,
            fleeing,
            ghost_label,
        )

        if debug_mode and patrolling:
            screen.blit(font.render("PATROLLING", True, TEXT_COLOR), (400, 4))
            screen.blit(font.render("Patrol stats", True, TEXT_COLOR), (10, 58))
        elif debug_mode and selected_ghost is not None and not fleeing:
            screen.blit(font.render("CHASING", True, TEXT_COLOR), (400, 4))

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
