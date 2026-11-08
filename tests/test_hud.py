from unittest.mock import Mock

from game import draw_hud
from pathfinding.comparison import SearchComparison
from pathfinding.result import SearchResult


def test_comparison_columns_only_appear_in_debug_mode():
    comparisons = {
        "BFS": SearchComparison(SearchResult([(0, 0), (0, 1)], [(0, 0)]), 0.09),
        "A*": SearchComparison(SearchResult([(0, 0)], [(0, 0)]), 0.04),
    }
    screen = Mock()
    font = Mock()
    font.render.side_effect = lambda label, *_: label

    draw_hud(screen, font, 10, comparisons, "BFS", False)
    assert [call.args[0] for call in screen.blit.call_args_list] == ["Score: 10"]

    screen.blit.reset_mock()
    draw_hud(screen, font, 10, comparisons, "BFS", True)
    drawn = [call.args for call in screen.blit.call_args_list]

    bfs_row = drawn[2:6]
    astar_row = drawn[6:10]
    assert drawn[0][0] == "Score: 10"
    assert drawn[1] == ("DEBUG MODE", (10, 31))
    assert bfs_row[0][0].strip() == "> BFS"
    assert astar_row[0][0].strip() == "A*"
    assert [position[0] for _, position in bfs_row] == [
        position[0] for _, position in astar_row
    ]
    assert bfs_row[0][1][0] > drawn[0][1][0]
    assert len({position[1] for _, position in bfs_row}) == 1
    assert len({position[1] for _, position in astar_row}) == 1
