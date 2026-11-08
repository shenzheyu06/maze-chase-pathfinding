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
        "draw_status_screen",
        lambda screen, font, message, prompt: messages.append(message),
    )

    game.run_game()

    assert players[0].position == (0, 1)
    assert players[0].score == 10
    assert players[1].position == (0, 0)
    assert players[1].score == 0
    assert messages == ["YOU WIN!", "YOU WIN!"]
    assert comparisons == [((0, 3), (0, 1)), ((0, 3), (0, 0))]


def test_pause_freezes_movement_and_preserves_ghost_delay(monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")

    player = Player(0, 0)
    ghost = Ghost(0, 3)
    ghost.last_move_time = 0
    monkeypatch.setattr(game, "reset_game", lambda: ([list(" ...")], player, ghost))

    frames = iter(
        [
            (0, []),
            (100, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]),
            (1100, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)]),
            (1200, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_o)]),
            (2100, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]),
            (2250, []),
            (2300, []),
            (2350, [pygame.event.Event(pygame.QUIT)]),
        ]
    )
    now = [0]
    positions = []
    messages = []
    debug_flags = []
    real_draw_hud = game.draw_hud

    def get_events():
        now[0], events = next(frames)
        return events

    def draw_hud(screen, font, score, comparisons, algorithm_name, debug_mode):
        debug_flags.append(debug_mode)
        real_draw_hud(screen, font, score, comparisons, algorithm_name, debug_mode)

    monkeypatch.setattr(pygame.time, "get_ticks", lambda: now[0])
    monkeypatch.setattr(pygame.event, "get", get_events)
    monkeypatch.setattr(game, "draw_hud", draw_hud)
    monkeypatch.setattr(
        pygame.display,
        "flip",
        lambda: positions.append((player.position, ghost.position)),
    )
    monkeypatch.setattr(
        game,
        "draw_status_screen",
        lambda screen, font, message, prompt: messages.append((message, prompt)),
    )

    game.run_game()

    assert all(player_position == (0, 0) for player_position, _ in positions)
    assert [ghost_position for _, ghost_position in positions[:6]] == [(0, 3)] * 6
    assert [ghost_position for _, ghost_position in positions[6:]] == [(0, 2)] * 2
    assert messages == [("PAUSED", "Press Space to resume")] * 3
    assert debug_flags == [False, False, False, True, True, True, True, True]
