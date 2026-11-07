from collections import deque

from pathfinding.grid import get_neighbors


def bfs(
    maze: list[list[str]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    queue = deque([start])
    visited = {start}

    came_from = {
        start: None
    }

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for neighbor in get_neighbors(maze, current):
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
