# Maze Chase Pathfinding

A tile-based maze chase game built with Python and Pygame Community Edition to practise and compare pathfinding algorithms against a moving player.

## Current Features

- Grid-based maze rendering, player movement, and wall collision
- Pellet collection and scoring
- A ghost that follows a shortest route using BFS or A*, switchable during play
- Live route and explored-tile visualization
- Debug-mode BFS and A* comparison of path length, visited tiles, and average search time
- Pause and inspect the game without losing the current debug view
- Win and game-over detection, with restart

## Controls

- Arrow keys or WASD: move the player
- Tab: switch between BFS and A*
- O: toggle debug mode and its visual overlays
- V: toggle explored tiles while debug mode is on
- P: toggle the projected ghost path while debug mode is on
- Space: pause or resume the game
- R: restart after winning or game over
- Esc: quit

The explored-tile and path settings are restored when debug mode is turned back on.
In debug mode, a "DEBUG MODE" label appears beside aligned HUD columns comparing BFS and A* for the current ghost and player tiles. Search times average 20 runs and update when either moves. The `>` marker shows which algorithm controls the ghost. The score remains visible when debug mode is off.

## Planned Features

- Multiple enemy targeting behaviours

## Project Structure

| File | Purpose |
|---|---|
| `main.py` | Application entry point |
| `game.py` | Game loop, input handling, HUD, and game states |
| `maze.py` | Maze layout, validation, collision checks, and rendering |
| `player.py` | Player movement, pellet collection, and score |
| `ghost.py` | Enemy movement and rendering |
| `pathfinding/` | BFS, A*, and shared maze-neighbor rules |
| `requirements.txt` | Python dependencies |
| `requirements-dev.txt` | Test dependencies |
| `tests/` | Game logic tests |
