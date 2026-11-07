# Maze Chase Pathfinding

A tile-based maze chase game built with Python and Pygame Community Edition to practise and compare pathfinding algorithms against a moving player.

## Current Features

- Grid-based maze rendering, player movement, and wall collision
- Pellet collection and scoring
- A ghost that follows the shortest path using Breadth-First Search (BFS)
- Path recalculation each frame, with the route and path length displayed
- Game-over detection and restart

## Planned Features

- A* pathfinding
- Multiple enemy targeting behaviours
- Debug visualization of explored tiles
- Algorithm comparisons using visited tiles, path length, and search time

## Project Structure

| File | Purpose |
|---|---|
| `main.py` | Application entry point |
| `game.py` | Game loop, input handling, HUD, and game states |
| `maze.py` | Maze layout, validation, collision checks, and rendering |
| `player.py` | Player movement, pellet collection, and score |
| `ghost.py` | Enemy movement and rendering |
| `pathfinding/bfs.py` | BFS shortest-path search |
| `requirements.txt` | Python dependencies |
| `requirements-dev.txt` | Test dependencies |
| `tests/` | Game logic tests |
