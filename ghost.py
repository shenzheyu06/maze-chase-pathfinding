from random import choice

import pygame

from maze import HUD_HEIGHT, TILE_SIZE
from pathfinding.flee import distances_from


GHOST_COLOR = (255, 50, 50)
VULNERABLE_COLOR = (60, 100, 255)
SELECTION_COLOR = (255, 255, 255)
MIN_PATROL_DISTANCE = 6
MIN_TARGET_SPACING = 4


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
        self.chasing = False
        self.patrol_target: tuple[int, int] | None = None
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
        self.chasing = False
        self.patrol_target = None
        self.reset_move_timer()

    def ensure_patrol_target(
        self,
        maze: list[list[str]],
        unavailable: set[tuple[int, int]],
        other_targets: list[tuple[int, int]],
    ) -> None:
        """Keep a reachable, distinct destination for this patrol."""
        if self.patrol_target not in (None, self.position) and self.patrol_target not in unavailable:
            return

        distances = distances_from(maze, self.position)
        candidates = [
            tile for tile in distances
            if tile != self.position
            and tile not in unavailable
            and tile not in other_targets
        ]
        if not candidates:
            self.patrol_target = None
            return

        distant = [tile for tile in candidates if distances[tile] >= MIN_PATROL_DISTANCE]
        candidates = distant or candidates
        target_distances = [distances_from(maze, target) for target in other_targets]
        spaced = [
            tile for tile in candidates
            if all(
                target_map.get(tile, float("inf")) >= MIN_TARGET_SPACING
                for target_map in target_distances
            )
        ]
        self.patrol_target = choice(spaced or candidates)

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
