from collections import deque

import pygame


TILE_SIZE = 32
HUD_HEIGHT = 40
FPS = 60
GHOST_MOVE_DELAY = 300

WALL_COLOR = (20, 40, 180)
WALL_OUTLINE_COLOR = (70, 110, 255)
PATH_COLOR = (0, 0, 0)
PELLET_COLOR = (240, 240, 240)
PLAYER_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 50, 50)
BFS_PATH_COLOR = (50, 200, 100)
TEXT_COLOR = (255, 255, 255)
GAME_OVER_COLOR = (255, 255, 255)


# # = wall
# . = path with pellet
# P = player starting position
# G = ghost starting position
MAZE_LAYOUT = [
    "#####################",
    "#G........#.........#",
    "#.###.###.#.###.###.#",
    "#.#...............#.#",
    "#.#.###.#####.###.#.#",
    "#.....#...#...#.....#",
    "#####.#.#.#.#.#.#####",
    "#.....#.#...#.#.....#",
    "#.#####.##.##.#####.#",
    "#.........P.........#",
    "#.#####.##.##.#####.#",
    "#.....#.#...#.#.....#",
    "#####.#.#.#.#.#.#####",
    "#.....#...#...#.....#",
    "#.#.###.#####.###.#.#",
    "#.#...............#.#",
    "#.###.###.#.###.###.#",
    "#.........#.........#",
    "#####################",
]

ROWS = len(MAZE_LAYOUT)
COLUMNS = len(MAZE_LAYOUT[0])

WINDOW_WIDTH = COLUMNS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE + HUD_HEIGHT


def create_maze() -> list[list[str]]:
    """Create a mutable copy of the maze."""
    return [list(row) for row in MAZE_LAYOUT]


def validate_maze() -> None:
    """Check that every maze row has the same number of columns."""
    for row_index, row in enumerate(MAZE_LAYOUT):
        if len(row) != COLUMNS:
            raise ValueError(
                f"Row {row_index} has {len(row)} columns; "
                f"expected {COLUMNS}."
            )


def find_start(
    maze: list[list[str]],
    symbol: str,
) -> tuple[int, int]:
    """Find a start symbol and replace it with an empty tile."""
    for row_index, row in enumerate(maze):
        for column_index, tile in enumerate(row):
            if tile == symbol:
                maze[row_index][column_index] = " "
                return row_index, column_index

    raise ValueError(
        f"The maze does not contain '{symbol}'."
    )


def is_walkable(
    maze: list[list[str]],
    row: int,
    column: int,
) -> bool:
    """Return whether the given tile can be entered."""
    if row < 0 or row >= ROWS:
        return False

    if column < 0 or column >= COLUMNS:
        return False

    return maze[row][column] != "#"


def move_player(
    maze: list[list[str]],
    player_row: int,
    player_column: int,
    row_change: int,
    column_change: int,
) -> tuple[int, int]:
    """Move the player if the destination is walkable."""
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
    """Remove a pellet if one exists."""
    if maze[row][column] == ".":
        maze[row][column] = " "
        return True

    return False


def get_neighbors(
    maze: list[list[str]],
    position: tuple[int, int],
) -> list[tuple[int, int]]:
    """Return all walkable neighbors of a tile."""
    row, column = position

    directions = [
        (-1, 0),  # up
        (1, 0),   # down
        (0, -1),  # left
        (0, 1),   # right
    ]

    neighbors = []

    for row_change, column_change in directions:
        new_row = row + row_change
        new_column = column + column_change

        if is_walkable(
            maze,
            new_row,
            new_column,
        ):
            neighbors.append(
                (new_row, new_column)
            )

    return neighbors


def bfs(
    maze: list[list[str]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    """Return the shortest path using BFS."""
    queue = deque([start])
    visited = {start}

    came_from: dict[
        tuple[int, int],
        tuple[int, int] | None,
    ] = {
        start: None
    }

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for neighbor in get_neighbors(
            maze,
            current,
        ):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                came_from[neighbor] = current

    if goal not in came_from:
        return []

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()

    return path


def positions_collide(
    player_row: int,
    player_column: int,
    ghost_row: int,
    ghost_column: int,
) -> bool:
    """Return whether player and ghost occupy the same tile."""
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
    """Reset maze, positions, and score."""
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


def draw_maze(
    screen: pygame.Surface,
    maze: list[list[str]],
) -> None:
    """Draw walls and pellets."""
    for row_index, row in enumerate(maze):
        for column_index, tile in enumerate(row):
            x = column_index * TILE_SIZE
            y = (
                row_index * TILE_SIZE
                + HUD_HEIGHT
            )

            tile_rect = pygame.Rect(
                x,
                y,
                TILE_SIZE,
                TILE_SIZE,
            )

            if tile == "#":
                pygame.draw.rect(
                    screen,
                    WALL_COLOR,
                    tile_rect,
                )

                pygame.draw.rect(
                    screen,
                    WALL_OUTLINE_COLOR,
                    tile_rect,
                    width=2,
                )

            else:
                pygame.draw.rect(
                    screen,
                    PATH_COLOR,
                    tile_rect,
                )

                if tile == ".":
                    pygame.draw.circle(
                        screen,
                        PELLET_COLOR,
                        tile_rect.center,
                        3,
                    )


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
    """Draw score and BFS information."""
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
    """Draw game-over information."""
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
    """Initialize and run the main game loop."""
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
                    player_row, player_column = (
                        move_player(
                            maze,
                            player_row,
                            player_column,
                            -1,
                            0,
                        )
                    )

                elif event.key in (
                    pygame.K_DOWN,
                    pygame.K_s,
                ):
                    player_row, player_column = (
                        move_player(
                            maze,
                            player_row,
                            player_column,
                            1,
                            0,
                        )
                    )

                elif event.key in (
                    pygame.K_LEFT,
                    pygame.K_a,
                ):
                    player_row, player_column = (
                        move_player(
                            maze,
                            player_row,
                            player_column,
                            0,
                            -1,
                        )
                    )

                elif event.key in (
                    pygame.K_RIGHT,
                    pygame.K_d,
                ):
                    player_row, player_column = (
                        move_player(
                            maze,
                            player_row,
                            player_column,
                            0,
                            1,
                        )
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