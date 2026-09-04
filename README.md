# Maze Chase Pathfinding

A tile-based maze chase game built with Python and Pygame. The project is designed to practise pathfinding algorithms by having enemies navigate through a maze toward a moving player.

## Current Features

- Two-dimensional tile-based maze
- Maze rendering with Pygame
- Keyboard-controlled player movement
- Wall collision detection
- Arrow-key and WASD controls
- Pellet rendering
- Configurable tile and window sizes

## Planned Features

- Pellet collection and scoring
- Breadth-First Search pathfinding
- A* pathfinding
- Enemy movement
- Dynamic path recalculation
- Multiple enemy targeting behaviours
- Pathfinding visualization
- Game-over and restart states
- Pathfinding performance comparisons

## Technologies

- Python
- Pygame
- Git
- GitHub

## Project Structure

```text
maze-chase-pathfinding/
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

The project will be divided into additional modules as more game systems are added.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/maze-chase-pathfinding.git
cd maze-chase-pathfinding
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the game

```powershell
python main.py
```

## Controls

| Action | Controls |
|---|---|
| Move up | `W` or Up Arrow |
| Move down | `S` or Down Arrow |
| Move left | `A` or Left Arrow |
| Move right | `D` or Right Arrow |
| Exit | `Esc` |

Movement currently occurs one grid tile at a time.

## Maze Representation

The maze is represented as a two-dimensional list of strings.

```python
MAZE = [
    "#########",
    "#...P...#",
    "#########",
]
```

Each character represents one tile:

| Character | Meaning |
|---|---|
| `#` | Wall |
| `.` | Open path containing a pellet |
| `P` | Player starting position |

Tiles are accessed using:

```python
MAZE[row][column]
```

Rows determine vertical position, while columns determine horizontal position.

## Movement and Collision

When the player attempts to move, the game calculates the destination tile.

The move is accepted only when:

- The destination is inside the maze
- The destination is not a wall

Otherwise, the player remains in the current position.

## Pathfinding Plan

The first enemy will use Breadth-First Search to find the shortest unweighted path between its position and the player.

A later implementation will add A* pathfinding. The algorithms may be compared using:

- Number of visited tiles
- Path length
- Search time
- Behaviour when the player changes position

A debug mode will eventually display explored tiles and the final calculated path.

## Development Progress

- [x] Set up Python and Pygame
- [x] Create the game window and game loop
- [x] Represent the maze as a two-dimensional grid
- [x] Render walls, paths, and pellets
- [x] Add player movement
- [x] Add wall collision
- [x] Add pellet collection
- [x] Implement Breadth-First Search
- [x] Add a pathfinding enemy
- [ ] Implement A*
- [ ] Add path visualization
- [ ] Add scoring and game states