import heapq
import maze as mz
from typing import List, Tuple, Dict, Optional


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


# --- STEP 2: The Heuristic (Manhattan Distance) ---
def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


# --- STEP 3: The "Eyes" (Get Neighbors using Maze Model) ---
def get_neighbors(maze_obj, current: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = current
    neighbors = []

    # mz.get_walls returns (North, East, South, West) booleans
    walls = mz.get_walls(maze_obj, x, y)

    # Deltas correspond to: North, East, South, West
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for i, (dx, dy) in enumerate(directions):
        if not walls[i]:  # If there is NO wall
            nx, ny = x + dx, y + dy
            # Bounds check
            dims = mz.get_dimensions(maze_obj)
            if 0 <= nx < dims[0] and 0 <= ny < dims[1]:
                neighbors.append((nx, ny))
    return neighbors


# --- CORE A* ALGORITHM ---
def a_star_search(maze_obj, start: Tuple[int, int], goal: Tuple[int, int]):
    frontier = PriorityQueue()
    frontier.put(start, 0)

    came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {}
    cost_so_far: Dict[Tuple[int, int], float] = {}

    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next_node in get_neighbors(maze_obj, current):
            new_cost = cost_so_far[current] + 1
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                frontier.put(next_node, priority)
                came_from[next_node] = current

    return came_from


# --- STEP 4: The Translator (Path -> "L", "R", "F") ---
def path_to_actions(path: List[Tuple[int, int]], start_orient: str) -> str:
    actions = ""
    curr_orient = start_orient
    dirs = ["N", "E", "S", "W"]  # Clockwise order

    for i in range(len(path) - 1):
        curr_pos = path[i]
        next_pos = path[i + 1]

        dx = next_pos[0] - curr_pos[0]
        dy = next_pos[1] - curr_pos[1]

        # Determine target direction
        target_orient = ""
        if dx == 0 and dy == 1:
            target_orient = "N"
        elif dx == 1 and dy == 0:
            target_orient = "E"
        elif dx == 0 and dy == -1:
            target_orient = "S"
        elif dx == -1 and dy == 0:
            target_orient = "W"

        # Calculate Turns
        curr_idx = dirs.index(curr_orient)
        target_idx = dirs.index(target_orient)
        diff = (target_idx - curr_idx) % 4

        if diff == 1:  # Right
            actions += "R"
            curr_orient = dirs[(curr_idx + 1) % 4]
        elif diff == 3:  # Left (equivalent to -1)
            actions += "L"
            curr_orient = dirs[(curr_idx - 1) % 4]
        elif diff == 2:  # U-Turn
            actions += "RR"
            curr_orient = dirs[(curr_idx + 2) % 4]

        actions += "F"

    return actions


# --- MAIN PUBLIC FUNCTION ---
def solve(maze_obj, start_pos, goal_pos, start_orient="N") -> str:
    # 1. Run A* to get the 'came_from' map
    came_from = a_star_search(maze_obj, start_pos, goal_pos)

    # 2. Reconstruct the path list backwards
    if goal_pos not in came_from:
        return ""  # No path found

    current = goal_pos
    path = []
    while current != start_pos:
        path.append(current)
        current = came_from[current]
    path.append(start_pos)
    path.reverse()  # Now it is Start -> Goal

    # 3. Translate to Runner Actions
    return path_to_actions(path, start_orient)