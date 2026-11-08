# Maze Chase Pathfinding

A tile-based maze chase game built with Python and Pygame Community Edition to practise and compare pathfinding algorithms against a moving player.

## Current Features

- Grid-based maze rendering, player movement, and wall collision
- Smooth visual movement between grid cells for the player and ghosts
- Pellet collection and scoring
- Power pellets make ghosts vulnerable for six seconds; eaten ghosts stay gone until a new game
- Three lives; losing a life resets positions while keeping score and collected pellets
- Six ghosts that follow patrol destinations until the player is nearby, then chase using BFS or A*, switchable during play
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
- [ and ]: select the previous or next ghost while debug mode is on
- Space: pause or resume the game
- R: restart after winning or game over
- Esc: quit

The explored-tile and path settings are restored when debug mode is turned back on.
Ghosts keep a space between each other when there is an open tile to move into. A ghost may briefly step away from its route to avoid crowding another ghost, then continue chasing or patrolling toward the same goal.
In debug mode, the first ghost is selected when debug mode opens. The selected ghost has a white outline and its number appears in the HUD. Ghosts choose reachable patrol destinations at least six maze steps away when possible, while spreading their destinations apart. They start chasing within seven maze steps of the player and return to patrol at ten steps. The debug HUD shows the selected ghost's current behavior. The route, explored tiles, and aligned BFS/A* comparisons refer to its current patrol destination or the player when chasing. Search times average 20 runs and update when the selected ghost, player, or patrol destination changes. The `>` marker shows the selected pathfinding algorithm. The score remains visible when debug mode is off.
Large pellets activate the power effect. The HUD shows its remaining time, and vulnerable ghosts turn blue and flee toward neighboring tiles farther from the player by maze distance. They avoid immediately retracing their last step when another route is available. The effect ends if the player loses a life. While fleeing, the debug overlay shows the selected ghost's next escape step and the BFS distance search; the comparison numbers remain labeled as chase stats.

## Project Structure

| File | Purpose |
|---|---|
| `main.py` | Application entry point |
| `animation.py` | Visual interpolation between grid cells |
| `game.py` | Game loop, input handling, HUD, and game states |
| `maze.py` | Maze layout, validation, collision checks, and rendering |
| `player.py` | Player movement, pellet collection, and score |
| `ghost.py` | Enemy movement and rendering |
| `pathfinding/` | BFS, A*, and shared maze-neighbor rules |
| `requirements.txt` | Python dependencies |
| `requirements-dev.txt` | Test dependencies |
| `tests/` | Game logic tests |
