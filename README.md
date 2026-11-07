# Maze Chase Pathfinding

A tile-based maze chase game built with Python and Pygame Community Edition to practise and compare pathfinding algorithms against a moving player.

## Current Features

- Grid-based maze rendering, player movement, and wall collision
- Pellet collection and scoring
- A ghost that follows a shortest route using BFS or A*, switchable during play
- Live route and explored-tile visualization, with path length and visited count
- Game-over detection and restart

## Planned Features

- Multiple enemy targeting behaviours
- Algorithm comparisons using search time

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
