# maze.py
from typing import Tuple, Set


class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.h_walls: Set[Tuple[int, int]] = set()
        self.v_walls: Set[Tuple[int, int]] = set()

        for x in range(width):
            self.h_walls.add((x, 0))
            self.h_walls.add((x, height))

        # Left and Right boundaries
        for y in range(height):
            self.v_walls.add((y, 0))
            self.v_walls.add((y, width))


def create_maze(width: int = 5, height: int = 5) -> Maze:
    return Maze(width, height)


def add_horizontal_wall(maze: Maze, x_coordinate: int, horizontal_line: int) -> Maze:
    maze.h_walls.add((x_coordinate, horizontal_line))
    return maze


def add_vertical_wall(maze: Maze, y_coordinate: int, vertical_line: int) -> Maze:
    maze.v_walls.add((y_coordinate, vertical_line))
    return maze


def get_dimensions(maze: Maze) -> Tuple[int, int]:
    return (maze.width, maze.height)


def get_walls(maze: Maze, x: int, y: int) -> Tuple[bool, bool, bool, bool]:
    north = (x, y + 1) in maze.h_walls
    south = (x, y) in maze.h_walls
    east = (y, x + 1) in maze.v_walls
    west = (y, x) in maze.v_walls

    return north, east, south, west