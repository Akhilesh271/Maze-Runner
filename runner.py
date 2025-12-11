# runner.py
from typing import Tuple, Optional, List, Set
import maze as mz


class Runner:
    def __init__(self, x: int, y: int, orientation: str):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.visited: Set[Tuple[int, int]] = {(x, y)}
        self.stack: List[Tuple[int, int]] = []  # To track path for backtracking


def create_runner(x: int = 0, y: int = 0, orientation: str = "N") -> Runner:
    return Runner(x, y, orientation)


def get_x(runner: Runner) -> int:
    return runner.x


def get_y(runner: Runner) -> int:
    return runner.y


def get_orientation(runner: Runner) -> str:
    return runner.orientation


def turn(runner: Runner, direction: str) -> Runner:
    dirs = ["N", "E", "S", "W"]
    idx = dirs.index(runner.orientation)
    if direction == "Left":
        new_idx = (idx - 1) % 4
    elif direction == "Right":
        new_idx = (idx + 1) % 4
    else:
        new_idx = idx
    runner.orientation = dirs[new_idx]
    return runner


def forward(runner: Runner) -> Runner:
    if runner.orientation == "N":
        runner.y += 1
    elif runner.orientation == "E":
        runner.x += 1
    elif runner.orientation == "S":
        runner.y -= 1
    elif runner.orientation == "W":
        runner.x -= 1
    return runner


def sense_walls(runner: Runner, maze_obj) -> Tuple[bool, bool, bool]:
    walls = mz.get_walls(maze_obj, runner.x, runner.y)
    dirs = ["N", "E", "S", "W"]
    current_idx = dirs.index(runner.orientation)
    left_wall = walls[(current_idx - 1) % 4]
    front_wall = walls[current_idx]
    right_wall = walls[(current_idx + 1) % 4]
    return (left_wall, front_wall, right_wall)


def go_straight(runner: Runner, maze_obj) -> Runner:
    if sense_walls(runner, maze_obj)[1]:
        raise ValueError("Wall in front")
    return forward(runner)


# --- Helper for Smart Movement ---
def _get_neighbor_coords(x, y, orientation) -> Tuple[int, int]:
    # Returns coordinates of the cell in front
    if orientation == "N": return (x, y + 1)
    if orientation == "E": return (x + 1, y)
    if orientation == "S": return (x, y - 1)
    if orientation == "W": return (x - 1, y)
    return (x, y)


def move(runner: Runner, maze_obj) -> Tuple[Runner, str]:
    walls = sense_walls(runner, maze_obj)  # Left, Front, Right
    current_pos = (runner.x, runner.y)

    # Current orientation index: 0:N, 1:E, 2:S, 3:W
    dirs = ["N", "E", "S", "W"]
    curr_idx = dirs.index(runner.orientation)

    # Calculate potential neighbors absolute coordinates
    # Left relative
    left_orient = dirs[(curr_idx - 1) % 4]
    left_pos = _get_neighbor_coords(runner.x, runner.y, left_orient)

    # Front relative
    front_orient = dirs[curr_idx]
    front_pos = _get_neighbor_coords(runner.x, runner.y, front_orient)

    # Right relative
    right_orient = dirs[(curr_idx + 1) % 4]
    right_pos = _get_neighbor_coords(runner.x, runner.y, right_orient)


    # Try Left (if no wall and unvisited)
    if not walls[0] and left_pos not in runner.visited:
        runner.stack.append(current_pos)
        runner.visited.add(left_pos)
        runner = turn(runner, "Left")
        runner = forward(runner)
        return runner, "LF"

    # Try Front (if no wall and unvisited)
    if not walls[1] and front_pos not in runner.visited:
        runner.stack.append(current_pos)
        runner.visited.add(front_pos)
        runner = forward(runner)
        return runner, "F"

    # Try Right (if no wall and unvisited)
    if not walls[2] and right_pos not in runner.visited:
        runner.stack.append(current_pos)
        runner.visited.add(right_pos)
        runner = turn(runner, "Right")
        runner = forward(runner)
        return runner, "RF"

    # --- ALL PATHS BLOCKED OR VISITED: BACKTRACK ---
    if not runner.stack:
        # Nowhere to go, stuck
        return runner, ""

    target_back = runner.stack.pop()


    dx = target_back[0] - runner.x
    dy = target_back[1] - runner.y

    target_orient = ""
    if dy == 1:
        target_orient = "N"
    elif dy == -1:
        target_orient = "S"
    elif dx == 1:
        target_orient = "E"
    elif dx == -1:
        target_orient = "W"

    # Rotate until we face target
    actions = ""
    while runner.orientation != target_orient:
        # Turn right until aligned
        runner = turn(runner, "Right")
        actions += "R"

    runner = forward(runner)
    actions += "F"

    return runner, actions


def explore(runner: Runner, maze_obj, goal: Optional[Tuple[int, int]] = None) -> str:
    if goal is None:
        dims = mz.get_dimensions(maze_obj)
        goal = (dims[0] - 1, dims[1] - 1)

    full_log = ""
    steps = 0
    max_steps = 20000  # Safety limit

    while (runner.x, runner.y) != goal and steps < max_steps:
        runner, act = move(runner, maze_obj)
        full_log += act
        steps += 1

        # If move returns empty string (stack empty, explored everything), stop
        if act == "":
            break

    return full_log