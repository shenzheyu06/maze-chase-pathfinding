import pygame

from maze import HUD_HEIGHT, TILE_SIZE


GHOST_COLOR = (255, 50, 50)
VULNERABLE_COLOR = (60, 100, 255)
SELECTION_COLOR = (255, 255, 255)


class Ghost:
    def __init__(
        self,
        row: int,
        column: int,
        move_delay: int = 300,
        color: tuple[int, int, int] = GHOST_COLOR,
    ) -> None:
        self.start_position = (row, column)
        self.previous_position: tuple[int, int] | None = None
        self.row = row
        self.column = column
        self.move_delay = move_delay
        self.color = color
        self.last_move_time = pygame.time.get_ticks()

    @property
    def position(self) -> tuple[int, int]:
        return self.row, self.column

    def move_along_path(
        self,
        path: list[tuple[int, int]],
        current_time: int,
        occupied_positions: set[tuple[int, int]] | None = None,
    ) -> None:
        if (
            current_time - self.last_move_time
            < self.move_delay
        ):
            return

        if len(path) > 1 and (
            occupied_positions is None or path[1] not in occupied_positions
        ):
            self.previous_position = self.position
            self.row, self.column = path[1]

        self.last_move_time = current_time

    def reset_move_timer(self) -> None:
        self.last_move_time = pygame.time.get_ticks()

    def reset_position(self) -> None:
        self.row, self.column = self.start_position
        self.previous_position = None
        self.reset_move_timer()

    def draw(
        self,
        screen: pygame.Surface,
        vulnerable: bool = False,
        selected: bool = False,
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
            VULNERABLE_COLOR if vulnerable else self.color,
            (center_x, center_y),
            TILE_SIZE // 3,
        )

        if selected:
            pygame.draw.circle(
                screen,
                SELECTION_COLOR,
                (center_x, center_y),
                TILE_SIZE // 3 + 4,
                width=2,
            )
