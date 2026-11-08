import pygame

import game
from animation import GridMotion
from ghost import Ghost
from maze import HUD_HEIGHT
from player import Player


def test_grid_motion_interpolates_and_continues_from_current_visual_position():
    motion = GridMotion((0, 0))
    motion.move_to((0, 1), 100, 200)

    assert motion.position_at(100) == (0, 0)
    assert motion.position_at(200) == (0, 0.5)

    motion.move_to((1, 1), 200, 200)
    assert motion.position_at(200) == (0, 0.5)
    assert motion.position_at(300) == (0.25, 1)
    assert motion.position_at(400) == (1, 1)

    motion.snap_to((2, 2))
    assert motion.position_at(400) == (2, 2)


def test_player_and_ghost_keep_logical_grid_positions_during_animation(monkeypatch):
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 100)
    player = Player(0, 0)
    ghost = Ghost(0, 2, move_delay=300)

    player.move([list(" ..")], 0, 1)
    ghost.last_move_time = 0
    ghost.move_along_path([(0, 2), (0, 1)], 300)

    assert player.position == (0, 1)
    assert player.motion.position_at(160) == (0, 0.5)
    assert ghost.position == (0, 1)
    assert ghost.motion.position_at(450) == (0, 1.5)

    surface = pygame.Surface((96, HUD_HEIGHT + 32))
    player.draw(surface, 160)
    assert surface.get_at((32, HUD_HEIGHT + 16))[:3] == (255, 255, 0)
    surface.fill((0, 0, 0))
    ghost.draw(surface, current_time=450)
    assert surface.get_at((64, HUD_HEIGHT + 16))[:3] == (255, 50, 50)

    player.reset_position()
    ghost.reset_position()
    assert player.motion.position_at(450) == (0, 0)
    assert ghost.motion.position_at(450) == (0, 2)


def test_pause_freezes_visual_movement_until_resumed(monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")

    player = Player(0, 0)
    ghost = Ghost(0, 3, move_delay=99999)
    monkeypatch.setattr(
        game, "reset_game", lambda: ([list(" ...")], player, [ghost])
    )
    frames = iter([
        (0, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)]),
        (60, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]),
        (1060, []),
        (1160, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]),
        (1220, []),
        (1240, [pygame.event.Event(pygame.QUIT)]),
    ])
    now = [0]
    drawn_positions = []
    real_draw = player.draw

    def get_events():
        now[0], events = next(frames)
        return events

    def draw_player(screen, current_time):
        drawn_positions.append(player.motion.position_at(current_time))
        real_draw(screen, current_time)

    monkeypatch.setattr(pygame.time, "get_ticks", lambda: now[0])
    monkeypatch.setattr(pygame.event, "get", get_events)
    monkeypatch.setattr(player, "draw", draw_player)

    game.run_game()

    assert drawn_positions == [
        (0, 0),
        (0, 0.5),
        (0, 0.5),
        (0, 0.5),
        (0, 1),
        (0, 1),
    ]
