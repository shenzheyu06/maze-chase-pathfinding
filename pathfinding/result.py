from dataclasses import dataclass


@dataclass
class SearchResult:
    path: list[tuple[int, int]]
    explored: list[tuple[int, int]]
