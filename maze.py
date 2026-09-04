import pygame


TILE_SIZE = 32
HUD_HEIGHT = 40

WALL_COLOR = (20, 40, 180)
WALL_OUTLINE_COLOR = (70, 110, 255)
PATH_COLOR = (0, 0, 0)
PELLET_COLOR = (240, 240, 240)


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


def create_maze() -> list[list[str]]:
    """Create a mutable copy of the maze layout."""
    return [list(row) for row in MAZE_LAYOUT]


def validate_maze() -> None:
    """Make sure every maze row has the same length."""
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
    """Find a starting symbol and replace it with an empty tile."""
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
    """Return whether a tile can be entered."""
    if row < 0 or row >= ROWS:
        return False

    if column < 0 or column >= COLUMNS:
        return False

    return maze[row][column] != "#"


def draw_maze(
    screen: pygame.Surface,
    maze: list[list[str]],
) -> None:
    """Draw the maze walls, paths, and pellets."""
    for row_index, row in enumerate(maze):
        for column_index, tile in enumerate(row):
            x = column_index * TILE_SIZE
            y = row_index * TILE_SIZE + HUD_HEIGHT

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