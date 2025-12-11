import random
import maze as mz
from typing import List, Tuple, Set


def _fill_walls(maze: mz.Maze):
    # Add all internal horizontal walls
    # h_walls are stored as (x_coordinate, y_line_index)
    # y_line indices 0 and height are boundaries (already set in __init__)
    for y in range(1, maze.height):
        for x in range(maze.width):
            mz.add_horizontal_wall(maze, x, y)
    for x in range(1, maze.width):
        for y in range(maze.height):
            mz.add_vertical_wall(maze, y, x)


def _remove_wall(maze: mz.Maze, curr: Tuple[int, int], next_cell: Tuple[int, int]):
    cx, cy = curr
    nx, ny = next_cell

    # Determine direction
    dx = nx - cx
    dy = ny - cy

    if dy == 1:  # Moving North
        # Wall is at (cx, cy + 1) in h_walls
        if (cx, cy + 1) in maze.h_walls:
            maze.h_walls.remove((cx, cy + 1))
    elif dy == -1:  # Moving South
        # Wall is at (cx, cy) in h_walls (the bottom of current cell)
        if (cx, cy) in maze.h_walls:
            maze.h_walls.remove((cx, cy))
    elif dx == 1:  # Moving East
        # Wall is at (cy, cx + 1) in v_walls
        if (cy, cx + 1) in maze.v_walls:
            maze.v_walls.remove((cy, cx + 1))
    elif dx == -1:  # Moving West
        # Wall is at (cy, cx) in v_walls
        if (cy, cx) in maze.v_walls:
            maze.v_walls.remove((cy, cx))


def generate_maze(width: int, height: int) -> mz.Maze:
    # 1. Initialize empty maze
    maze = mz.create_maze(width, height)

    # 2. Fill it with walls (make it a jail)
    _fill_walls(maze)

    # 3. Setup for Recursive Backtracking
    start_pos = (0, 0)
    visited: Set[Tuple[int, int]] = {start_pos}
    stack: List[Tuple[int, int]] = [start_pos]

    # 4. The "Digger" Loop
    while stack:
        current = stack[-1]
        cx, cy = current

        # Find unvisited neighbors
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        unvisited_neighbors = []

        for dx, dy in deltas:
            nx, ny = cx + dx, cy + dy
            # Check bounds
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    unvisited_neighbors.append((nx, ny))

        if unvisited_neighbors:
            # Choose one random neighbor
            chosen = random.choice(unvisited_neighbors)

            # Knock down the wall between current and chosen
            _remove_wall(maze, current, chosen)

            # Mark visited and push to stack
            visited.add(chosen)
            stack.append(chosen)
        else:
            # Backtrack
            stack.pop()

    return maze