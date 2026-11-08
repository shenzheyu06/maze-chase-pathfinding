import pygame

from animation import GridMotion
from maze import HUD_HEIGHT, TILE_SIZE, is_walkable


PLAYER_COLOR = (255, 255, 0)
MOVE_ANIMATION_MS = 120


class Player:
    def __init__(self, row: int, column: int) -> None:
        self.start_position = (row, column)
        self.row = row
        self.column = column
        self.score = 0
        self.motion = GridMotion(self.position)

    @property
    def position(self) -> tuple[int, int]:
        return self.row, self.column

    def move(
        self,
        maze: list[list[str]],
        row_change: int,
        column_change: int,
    ) -> str | None:
        new_row = self.row + row_change
        new_column = self.column + column_change

        if is_walkable(
            maze,
            new_row,
            new_column,
        ):
            self.motion.move_to(
                (new_row, new_column),
                pygame.time.get_ticks(),
                MOVE_ANIMATION_MS,
            )
            self.row = new_row
            self.column = new_column

            return self.collect_pellet(maze)

        return None

    def reset_position(self) -> None:
        self.row, self.column = self.start_position
        self.motion.snap_to(self.position)

    def collect_pellet(
        self,
        maze: list[list[str]],
    ) -> str | None:
        tile = maze[self.row][self.column]
        if tile in (".", "o"):
            maze[self.row][self.column] = " "
            self.score += 50 if tile == "o" else 10
            return tile

        return None

    def draw(
        self,
        screen: pygame.Surface,
        current_time: int | None = None,
    ) -> None:
        if current_time is None:
            current_time = pygame.time.get_ticks()
        row, column = self.motion.position_at(current_time)
        center_x = (
            column * TILE_SIZE
            + TILE_SIZE // 2
        )

        center_y = (
            row * TILE_SIZE
            + TILE_SIZE // 2
            + HUD_HEIGHT
        )

        pygame.draw.circle(
            screen,
            PLAYER_COLOR,
            (round(center_x), round(center_y)),
            TILE_SIZE // 3,
        )
