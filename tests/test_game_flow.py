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

    def draw_hud(screen, font, score, lives, power_remaining_ms,
                 comparisons, algorithm_name, debug_mode, fleeing):
        debug_flags.append(debug_mode)
        real_draw_hud(screen, font, score, lives, power_remaining_ms,
                      comparisons, algorithm_name, debug_mode, fleeing)

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


def test_power_pellet_removes_eaten_ghost(monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")

    maze = [list(" o..")]
    player = Player(0, 0)
    ghost = Ghost(0, 2)
    ghost.last_move_time = 0
    monkeypatch.setattr(game, "reset_game", lambda: (maze, player, ghost))

    frames = iter(
        [
            (0, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)]),
            (100, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]),
            (7000, []),
            (7100, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]),
            (7200, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)]),
            (7300, [pygame.event.Event(pygame.QUIT)]),
        ]
    )
    now = [0]
    hud = []

    def get_events():
        now[0], events = next(frames)
        return events

    monkeypatch.setattr(pygame.time, "get_ticks", lambda: now[0])
    monkeypatch.setattr(pygame.event, "get", get_events)
    monkeypatch.setattr(
        game,
        "draw_hud",
        lambda screen, font, score, lives, power_remaining_ms,
               comparisons, algorithm_name, debug_mode, fleeing: hud.append(
                   (score, lives, power_remaining_ms, comparisons)
               ),
    )

    game.run_game()

    assert player.position == (0, 2)
    assert maze[0][1] == " "
    assert [score for score, *_ in hud] == [50, 50, 50, 50, 260, 260]
    assert all(lives == 3 and power > 0 for _, lives, power, _ in hud)
    assert [power for _, _, power, _ in hud[:4]] == [6000, 5900, 5900, 5900]
    assert hud[0][3] is not None
    assert all(comparison is None for *_, comparison in hud[4:])


def test_lost_lives_keep_pellets_and_score_until_game_over(monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")

    maze = [list(" ..   .")]
    player = Player(0, 0)
    ghost = Ghost(0, 3)
    ghost.last_move_time = 0
    monkeypatch.setattr(game, "reset_game", lambda: (maze, player, ghost))

    frames = iter(
        [
            (time, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)])
            for time in range(0, 450, 50)
        ]
        + [(450, [pygame.event.Event(pygame.QUIT)])]
    )
    now = [0]
    hud = []
    messages = []

    def get_events():
        now[0], events = next(frames)
        return events

    monkeypatch.setattr(pygame.time, "get_ticks", lambda: now[0])
    monkeypatch.setattr(pygame.event, "get", get_events)
    monkeypatch.setattr(
        game,
        "draw_hud",
        lambda screen, font, score, lives, power_remaining_ms,
               comparisons, algorithm_name, debug_mode, fleeing: hud.append(
                   (score, lives, player.position)
               ),
    )
    monkeypatch.setattr(
        game,
        "draw_status_screen",
        lambda screen, font, message, prompt: messages.append(message),
    )

    game.run_game()

    assert [lives for _, lives, _ in hud] == [3, 3, 2, 2, 2, 1, 1, 1, 0, 0]
    assert hud[2] == (20, 2, (0, 0))
    assert hud[5] == (20, 1, (0, 0))
    assert hud[8] == (20, 0, (0, 3))
    assert maze[0][1:3] == [" ", " "]
    assert maze[0][6] == "."
    assert messages == ["GAME OVER", "GAME OVER"]


def test_powered_ghost_moves_away_from_player(monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")

    player = Player(0, 0)
    ghost = Ghost(0, 3)
    ghost.last_move_time = 0
    monkeypatch.setattr(
        game, "reset_game", lambda: ([list(" o...")], player, ghost)
    )

    frames = iter(
        [
            (0, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)]),
            (300, []),
            (350, [pygame.event.Event(pygame.QUIT)]),
        ]
    )
    now = [0]
    positions = []

    def get_events():
        now[0], events = next(frames)
        return events

    monkeypatch.setattr(pygame.time, "get_ticks", lambda: now[0])
    monkeypatch.setattr(pygame.event, "get", get_events)
    monkeypatch.setattr(
        pygame.display, "flip", lambda: positions.append(ghost.position)
    )

    game.run_game()

    assert player.position == (0, 1)
    assert positions == [(0, 3), (0, 4), (0, 4)]
