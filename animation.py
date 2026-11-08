class GridMotion:
    """Interpolate a sprite between logical grid positions."""

    def __init__(self, position: tuple[int, int]) -> None:
        self.start = tuple(map(float, position))
        self.target = position
        self.waypoints: list[tuple[int, int]] = []
        self.started_at = 0
        self.duration_ms = 0

    def _position_and_remaining(
        self, current_time: int
    ) -> tuple[tuple[float, float], list[tuple[int, int]]]:
        if self.duration_ms == 0:
            return self.target, []

        progress = max(
            0.0,
            min(1.0, (current_time - self.started_at) / self.duration_ms),
        )
        points = [self.start, *self.waypoints]
        lengths = [
            abs(end[0] - start[0]) + abs(end[1] - start[1])
            for start, end in zip(points, points[1:])
        ]
        distance_left = sum(lengths) * progress
        for index, length in enumerate(lengths):
            if distance_left < length:
                start, end = points[index], points[index + 1]
                segment_progress = distance_left / length
                position = (
                    start[0] + (end[0] - start[0]) * segment_progress,
                    start[1] + (end[1] - start[1]) * segment_progress,
                )
                return position, self.waypoints[index:]
            distance_left -= length

        return self.target, []

    def position_at(self, current_time: int) -> tuple[float, float]:
        return self._position_and_remaining(current_time)[0]

    def move_to(
        self,
        position: tuple[int, int],
        current_time: int,
        duration_ms: int,
    ) -> None:
        self.start, remaining = self._position_and_remaining(current_time)
        self.waypoints = [*remaining, position]
        self.target = position
        self.started_at = current_time
        self.duration_ms = max(1, duration_ms)

    def shift_time(self, duration_ms: int) -> None:
        self.started_at += duration_ms

    def snap_to(self, position: tuple[int, int]) -> None:
        self.start = tuple(map(float, position))
        self.target = position
        self.waypoints = []
        self.duration_ms = 0
