from pathfinding.flee import distances_from
from pathfinding.grid import get_neighbors


def grid_distance(first: tuple[int, int], second: tuple[int, int]) -> int:
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def separate_path(
    maze: list[list[str]],
    position: tuple[int, int],
    planned_path: list[tuple[int, int]],
    other_positions: set[tuple[int, int]],
    goal: tuple[int, int],
    fleeing: bool = False,
) -> list[tuple[int, int]]:
    """Keep a ghost from moving beside another when a free step exists."""
    if not other_positions:
        return planned_path

    next_tile = planned_path[1] if len(planned_path) > 1 else None
    if next_tile is not None and all(
        grid_distance(next_tile, other) > 1 for other in other_positions
    ):
        return planned_path

    adjacent = any(
        grid_distance(position, other) == 1 for other in other_positions
    )
    if not adjacent and next_tile is None:
        return planned_path

    open_tiles = [
        tile for tile in get_neighbors(maze, position)
        if all(grid_distance(tile, other) > 1 for other in other_positions)
    ]
    if not open_tiles:
        return [position]

    distances = distances_from(maze, goal)

    def priority(tile: tuple[int, int]) -> tuple[float, float]:
        separation = min(grid_distance(tile, other) for other in other_positions)
        goal_distance = distances.get(tile, float("inf"))
        return separation, goal_distance if fleeing else -goal_distance

    return [position, max(open_tiles, key=priority)]
