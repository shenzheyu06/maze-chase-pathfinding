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
    neighbors = []

    for row_change, column_change in directions:
        new_row = row + row_change
        new_column = column + column_change

        if (
            0 <= new_row < len(maze)
            and 0 <= new_column < len(maze[new_row])
            and maze[new_row][new_column] != "#"
        ):
            neighbors.append((new_row, new_column))

    return neighbors
