from collections import deque

from pathfinding.grid import get_neighbors


def distances_from(
    maze: list[list[str]],
    start: tuple[int, int],
) -> dict[tuple[int, int], int]:
    """Measure shortest maze distance from the player to each reachable tile."""
    distances = {start: 0}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        for neighbor in get_neighbors(maze, current):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    return distances


def flee_path(
    maze: list[list[str]],
    position: tuple[int, int],
    previous_position: tuple[int, int] | None,
    distances: dict[tuple[int, int], int],
) -> list[tuple[int, int]]:
    """Choose the next tile farthest from the player without bouncing back."""
    neighbors = get_neighbors(maze, position)
    if not neighbors:
        return [position]

    if previous_position in neighbors and len(neighbors) > 1:
        neighbors.remove(previous_position)

    heading = None
    if previous_position is not None:
        heading = (
            position[0] - previous_position[0],
            position[1] - previous_position[1],
        )

    def priority(tile: tuple[int, int]) -> tuple[float, bool]:
        direction = (tile[0] - position[0], tile[1] - position[1])
        return distances.get(tile, float("inf")), direction == heading

    return [position, max(neighbors, key=priority)]
