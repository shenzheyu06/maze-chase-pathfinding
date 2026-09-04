import pygame

from maze import HUD_HEIGHT, TILE_SIZE, is_walkable


PLAYER_COLOR = (255, 255, 0)


class Player:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.score = 0

    @property
    def position(self) -> tuple[int, int]:
        return self.row, self.column

    def move(
        self,
        maze: list[list[str]],
        row_change: int,
        column_change: int,
    ) -> None:
        new_row = self.row + row_change
        new_column = self.column + column_change

        if is_walkable(
            maze,
            new_row,
            new_column,
        ):
            self.row = new_row
            self.column = new_column

            self.collect_pellet(maze)

    def collect_pellet(
        self,
        maze: list[list[str]],
    ) -> None:
        if maze[self.row][self.column] == ".":
            maze[self.row][self.column] = " "
            self.score += 10

    def draw(
        self,
        screen: pygame.Surface,
    ) -> None:
        center_x = (
            self.column * TILE_SIZE
            + TILE_SIZE // 2
        )

        center_y = (
            self.row * TILE_SIZE
            + TILE_SIZE // 2
            + HUD_HEIGHT
        )

        pygame.draw.circle(
            screen,
            PLAYER_COLOR,
            (center_x, center_y),
            TILE_SIZE // 3,
        )