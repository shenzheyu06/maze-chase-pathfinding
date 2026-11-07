from maze import is_walkable
from pathfinding.bfs import bfs
from player import Player


def test_bfs_finds_shortest_route_around_walls():
    maze = [list("..."), 
            list("##."), 
            list("...")]

    path = bfs(maze, (0, 0), (2, 0))

    assert path == [
        (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0)
    ]


def test_bfs_handles_unreachable_and_same_tile_goals():
    maze = [list(".#.")]

    assert bfs(maze, (0, 0), (0, 2)) == []
    assert bfs(maze, (0, 0), (0, 0)) == [(0, 0)]


def test_player_respects_walls_and_collects_each_pellet_once():
    maze = [list("##"), 
            list(" .")]
    player = Player(1, 0)

    player.move(maze, -1, 0)
    assert player.position == (1, 0)
    assert player.score == 0

    player.move(maze, 0, 1)
    assert player.position == (1, 1)
    assert player.score == 10
    assert maze[1][1] == " "

    player.move(maze, 0, -1)
    player.move(maze, 0, 1)
    assert player.score == 10


def test_walkability_uses_the_supplied_maze_size():
    maze = [list("."), list(".#")]

    assert is_walkable(maze, 1, 0)
    assert not is_walkable(maze, 1, 1)
    assert not is_walkable(maze, 0, 1)
    assert not is_walkable(maze, 2, 0)
    assert not is_walkable([], 0, 0)
