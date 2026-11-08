from pathfinding.separation import separate_path


def test_adjacent_ghost_steps_away_from_occupied_next_tile():
    maze = [list("      ")]

    path = separate_path(
        maze, (0, 3), [(0, 3), (0, 4)], {(0, 4)}, (0, 0)
    )

    assert path == [(0, 3), (0, 2)]


def test_ghost_does_not_follow_parallel_path_that_keeps_them_adjacent():
    maze = [list("      ")]

    path = separate_path(
        maze, (0, 3), [(0, 3), (0, 2)], {(0, 1)}, (0, 0)
    )

    assert path == [(0, 3), (0, 4)]


def test_ghost_waits_if_no_tile_can_create_space():
    maze = [list("  ")]

    path = separate_path(
        maze, (0, 0), [(0, 0), (0, 1)], {(0, 1)}, (0, 1)
    )

    assert path == [(0, 0)]
