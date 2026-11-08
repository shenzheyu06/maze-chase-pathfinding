from dataclasses import dataclass
from time import perf_counter_ns

from pathfinding.astar import astar_search
from pathfinding.bfs import bfs_search
from pathfinding.result import SearchResult


BENCHMARK_RUNS = 20


@dataclass
class SearchComparison:
    result: SearchResult
    average_ms: float


def compare_searches(
    maze: list[list[str]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> dict[str, SearchComparison]:
    comparisons = {}

    for name, search in (("BFS", bfs_search), ("A*", astar_search)):
        started = perf_counter_ns()
        for _ in range(BENCHMARK_RUNS):
            result = search(maze, start, goal)
        elapsed_ns = perf_counter_ns() - started

        comparisons[name] = SearchComparison(
            result=result,
            average_ms=elapsed_ns / BENCHMARK_RUNS / 1_000_000,
        )

    return comparisons
