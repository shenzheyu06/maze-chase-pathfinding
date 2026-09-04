import pygame

from maze import HUD_HEIGHT, TILE_SIZE


GHOST_COLOR = (255, 50, 50)


class Ghost:
    def __init__(
        self,
        row: int,
        column: int,
        move_delay: int = 300,
    ) -> None:
        self.row = row
        self.column = column
        self.move_delay = move_delay
        self.last_move_time = pygame.time.get_ticks()

    @property
    def position(self) -> tuple[int, int]:
        return self.row, self.column

    def move_along_path(
        self,
        path: list[tuple[int, int]],
        current_time: int,
    ) -> None:
        if (
            current_time - self.last_move_time
            < self.move_delay
        ):
            return

        if len(path) > 1:
            self.row, self.column = path[1]

        self.last_move_time = current_time

    def reset_move_timer(self) -> None:
        self.last_move_time = pygame.time.get_ticks()

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
            GHOST_COLOR,
            (center_x, center_y),
            TILE_SIZE // 3,
        )