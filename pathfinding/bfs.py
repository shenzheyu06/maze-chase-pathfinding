from collections import deque

from pathfinding.grid import get_neighbors
from pathfinding.result import SearchResult


def bfs_search(
    maze: list[list[str]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> SearchResult:
    queue = deque([start])
    visited = {start}
    explored = []

    came_from = {
        start: None
    }

    while queue:
        current = queue.popleft()
        explored.append(current)

        if current == goal:
            break

        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                came_from[neighbor] = current

    if goal not in came_from:
        return SearchResult([], explored)

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()

    return SearchResult(path, explored)


def bfs(
    maze: list[list[str]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    return bfs_search(maze, start, goal).path
