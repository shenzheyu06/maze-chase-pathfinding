from pathfinding.flee import distances_from, flee_path


def test_distances_follow_maze_corridors():
    maze = [list("..."), 
            list("##."), 
            list("...")]

    distances = distances_from(maze, (0, 0))

    assert distances[(2, 0)] == 6
    assert (1, 0) not in distances


def test_flee_chooses_farthest_neighbor_and_avoids_bouncing():
    maze = [list(".....")]
    distances = distances_from(maze, (0, 0))

    assert flee_path(maze, (0, 2), None, distances) == [(0, 2), (0, 3)]
    assert flee_path(maze, (0, 3), (0, 4), distances) == [(0, 3), (0, 2)]
    assert flee_path(maze, (0, 4), (0, 3), distances) == [(0, 4), (0, 3)]


def test_flee_prefers_continuing_straight_when_distances_tie():
    maze = [list("..."), 
            list("..."), 
            list("...")]
    distances = distances_from(maze, (0, 0))

    assert flee_path(maze, (1, 1), (1, 0), distances) == [(1, 1), (1, 2)]
