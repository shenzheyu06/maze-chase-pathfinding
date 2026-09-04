from collections import deque


def get_neighbors(
    maze: list[list[str]],
    position: tuple[int, int],
) -> list[tuple[int, int]]:
    row, column = position

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    rows = len(maze)
    columns = len(maze[0])

    neighbors = []

    for row_change, column_change in directions:
        new_row = row + row_change
        new_column = column + column_change

        if (
            0 <= new_row < rows
            and 0 <= new_column < columns
            and maze[new_row][new_column] != "#"
        ):
            neighbors.append((new_row, new_column))

    return neighbors


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