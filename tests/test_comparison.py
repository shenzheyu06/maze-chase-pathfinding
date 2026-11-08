from pathfinding import comparison


def test_comparison_measures_both_searches_for_the_same_positions(monkeypatch):
    times = iter((0, 2_000_000, 2_000_000, 6_000_000))
    monkeypatch.setattr(comparison, "perf_counter_ns", lambda: next(times))
    monkeypatch.setattr(comparison, "BENCHMARK_RUNS", 2)

    results = comparison.compare_searches([list("...")], (0, 0), (0, 2))

    assert results["BFS"].result.path == results["A*"].result.path
    assert results["BFS"].result.path == [(0, 0), (0, 1), (0, 2)]
    assert results["BFS"].average_ms == 1.0
    assert results["A*"].average_ms == 2.0
