from heapq import heappop, heappush
from itertools import count

from pathfinding.grid import get_neighbors


def manhattan_distance(
    position: tuple[int, int],
    goal: tuple[int, int],
) -> int:
    """Estimate remaining steps when movement is limited to four directions."""
    # Walls may lengthen a route, so this estimate never exceeds the real cost.
    # Which makes this heuristic admissible.
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


def astar(
    maze: list[list[str]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    """Find a shortest path through the maze using A*."""
    tie_breaker = count()
    frontier = [(manhattan_distance(start, goal), next(tie_breaker), 0, start)]
    best_cost = {start: 0}
    came_from = {start: None}

    while frontier:
        _, _, cost, current = heappop(frontier)

        # Ignore an old heap entry if a shorter route was found later.
        if cost != best_cost[current]:
            continue

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for neighbor in get_neighbors(maze, current):
            # Every move costs one; keep only a shorter route to each tile.
            next_cost = cost + 1
            if neighbor in best_cost and next_cost >= best_cost[neighbor]:
                continue

            best_cost[neighbor] = next_cost
            came_from[neighbor] = current

            # Rank by steps taken plus estimated steps left; break ties in order. (g + h)
            priority = next_cost + manhattan_distance(neighbor, goal)
            heappush(frontier, (priority, next(tie_breaker), next_cost, neighbor))

    return []
