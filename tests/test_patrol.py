from ghost import Ghost


def test_patrol_destination_is_reachable_and_far_enough(monkeypatch):
    ghost = Ghost(0, 7)
    maze = [list("               ")]
    monkeypatch.setattr("ghost.choice", lambda options: options[0])

    ghost.ensure_patrol_target(maze, {(0, 0)}, [])

    assert ghost.patrol_target is not None
    assert abs(ghost.patrol_target[1] - 7) >= 6
    assert ghost.patrol_target != (0, 0)

    arrived_target = ghost.patrol_target
    ghost.row, ghost.column = arrived_target
    ghost.ensure_patrol_target(maze, {(0, 0)}, [])
    assert ghost.patrol_target != arrived_target


def test_patrol_destinations_avoid_other_ghosts_and_their_targets(monkeypatch):
    ghost = Ghost(0, 0)
    maze = [list("             ")]
    monkeypatch.setattr("ghost.choice", lambda options: options[0])

    ghost.ensure_patrol_target(maze, {(0, 6)}, [(0, 7)])

    assert ghost.patrol_target == (0, 11)
    ghost.reset_position()
    assert ghost.patrol_target is None


def test_patrol_target_stays_in_reachable_section_when_maze_is_split():
    ghost = Ghost(0, 0)

    ghost.ensure_patrol_target([list("   #   ")], set(), [])

    assert ghost.patrol_target in {(0, 1), (0, 2)}


def test_patrol_target_does_not_duplicate_another_in_a_small_maze():
    ghost = Ghost(0, 0)

    ghost.ensure_patrol_target([list("   ")], set(), [(0, 1)])

    assert ghost.patrol_target == (0, 2)
