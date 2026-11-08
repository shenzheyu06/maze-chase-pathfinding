import pygame

import game
from ghost import Ghost
from player import Player


def test_last_pellet_wins_and_restart_resets_game(monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")

    players = []

    def reset_game():
        player = Player(0, 0)
        players.append(player)
        return [list(" .# ")], player, Ghost(0, 3)

    event_batches = iter(
        [
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)],
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)],
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)],
            [pygame.event.Event(pygame.QUIT)],
        ]
    )
    messages = []
    comparisons = []

    real_compare_searches = game.compare_searches

    def compare_searches(maze, start, goal):
        comparisons.append((start, goal))
        return real_compare_searches(maze, start, goal)

    monkeypatch.setattr(game, "reset_game", reset_game)
    monkeypatch.setattr(game, "compare_searches", compare_searches)
    monkeypatch.setattr(pygame.event, "get", lambda: next(event_batches))
    monkeypatch.setattr(
        game,
        "draw_end_screen",
        lambda screen, font, message: messages.append(message),
    )

    game.run_game()

    assert players[0].position == (0, 1)
    assert players[0].score == 10
    assert players[1].position == (0, 0)
    assert players[1].score == 0
    assert messages == ["YOU WIN!", "YOU WIN!"]
    assert comparisons == [((0, 3), (0, 1)), ((0, 3), (0, 0))]
