import sys
import argparse
import time
from typing import List, Optional, Tuple
import maze as mz
import runner as rn
import astar_solver
import maze_generator as mg


def shortest_path(maze_obj, starting: Optional[Tuple[int, int]] = None,
                  goal: Optional[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
    if starting is None:
        starting = (0, 0)
    if goal is None:
        dims = mz.get_dimensions(maze_obj)
        goal = (dims[0] - 1, dims[1] - 1)

    sim_runner = rn.create_runner(starting[0], starting[1], "N")
    path_stack = [starting]

    return path_stack


def trace_path_from_actions(start: Tuple[int, int], actions: str) -> List[Tuple[int, int]]:
    r = rn.create_runner(start[0], start[1], "N")
    path_stack = [start]

    for char in actions:
        if char == 'L':
            rn.turn(r, "Left")
        elif char == 'R':
            rn.turn(r, "Right")
        elif char == 'F':
            rn.forward(r)
            new_pos = (rn.get_x(r), rn.get_y(r))

            # Loop Erasure Logic
            if new_pos in path_stack:
                # If we are here, we looped. Pop until we are back at this valid node.
                while path_stack[-1] != new_pos:
                    path_stack.pop()
            else:
                path_stack.append(new_pos)

    return path_stack


def maze_reader(maze_file: str):
    try:
        with open(maze_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise IOError(f"Could not read file: {maze_file}")

    lines = [line.strip() for line in lines if line.strip()]
    grid_height = len(lines)
    if grid_height < 3:
        raise ValueError("Maze file too small")

    grid_width = len(lines[0])
    mz_height = (grid_height - 1) // 2
    mz_width = (grid_width - 1) // 2

    new_maze = mz.create_maze(mz_width, mz_height)

    for row_idx, line in enumerate(lines):
        is_horizontal_line = (row_idx % 2 == 0)

        if is_horizontal_line:
            y_line = mz_height - (row_idx // 2)
            for x in range(mz_width):
                char_idx = 1 + (x * 2)
                if char_idx < len(line) and line[char_idx] == '#':
                    mz.add_horizontal_wall(new_maze, x, y_line)
        else:
            y_cell = mz_height - 1 - (row_idx // 2)
            for v_line in range(mz_width + 1):
                char_idx = v_line * 2
                if char_idx < len(line) and line[char_idx] == '#':
                    mz.add_vertical_wall(new_maze, y_cell, v_line)

    return new_maze


def write_logs(filename, runner_start, maze, actions, path):
    r = rn.create_runner(runner_start[0], runner_start[1], "N")

    with open("exploration.csv", "w") as f:
        f.write("Step,x-coordinate,y-coordinate,Actions\n")
        step_count = 1
        buffer = ""

        for char in actions:
            buffer += char
            if char == 'F':
                f.write(f"{step_count},{rn.get_x(r)},{rn.get_y(r)},{buffer}\n")
                for c in buffer:
                    if c == 'L':
                        rn.turn(r, "Left")
                    elif c == 'R':
                        rn.turn(r, "Right")
                    elif c == 'F':
                        rn.forward(r)
                step_count += 1
                buffer = ""

    expl_steps = step_count - 1
    path_len = len(path)
    score = (expl_steps / 4) + path_len

    with open("statistics.txt", "w") as f:
        f.write(f"{filename}\n")
        f.write(f"{score}\n")
        f.write(f"{expl_steps}\n")
        f.write(f"{path}\n")
        f.write(f"{path_len}\n")


def print_maze_console(maze_obj, path: List[Tuple[int, int]] = []):
    dims = mz.get_dimensions(maze_obj)
    w, h = dims

    # Create a grid of characters
    # Size: (h * 2 + 1) rows, (w * 2 + 1) cols
    grid_h = h * 2 + 1
    grid_w = w * 2 + 1
    grid = [[' ' for _ in range(grid_w)] for _ in range(grid_h)]

    # Fill corners
    for r in range(0, grid_h, 2):
        for c in range(0, grid_w, 2):
            grid[r][c] = '+'

    # Fill Walls
    for x in range(w):
        for y in range(h):
            # Map (x,y) to grid coordinates
            cy = (h - 1 - y) * 2 + 1
            cx = x * 2 + 1

            walls = mz.get_walls(maze_obj, x, y)  # N, E, S, W

            # North Wall (y+1) -> Grid row cy-1
            if walls[0]: grid[cy - 1][cx] = '-'
            # South Wall (y)   -> Grid row cy+1
            if walls[2]: grid[cy + 1][cx] = '-'
            # East Wall (x+1)  -> Grid col cx+1
            if walls[1]: grid[cy][cx + 1] = '|'
            # West Wall (x)    -> Grid col cx-1
            if walls[3]: grid[cy][cx - 1] = '|'

            # Mark Path
            if (x, y) in path:
                grid[cy][cx] = '.'

    print("\nMaze Visual:")
    for row in grid:
        print("".join(row))
    print()


def run_benchmark(maze_obj, start, goal):
    print(f"\n{'-' * 15} BENCHMARKING {'-' * 15}")

    # 1. DFS
    print(f"Running DFS...", end=" ", flush=True)
    r_dfs = rn.create_runner(start[0], start[1], "N")
    t0 = time.perf_counter()
    dfs_act = rn.explore(r_dfs, maze_obj, goal)
    t1 = time.perf_counter()
    dfs_ms = (t1 - t0) * 1000
    print(f"Done! ({dfs_ms:.2f} ms, {len(dfs_act)} steps)")

    # 2. A*
    print(f"Running A* ...", end=" ", flush=True)
    t0 = time.perf_counter()
    astar_act = astar_solver.solve(maze_obj, start, goal, "N")
    t1 = time.perf_counter()
    astar_ms = (t1 - t0) * 1000
    print(f"Done! ({astar_ms:.2f} ms, {len(astar_act)} steps)")

    # Stats
    print(f"{'-' * 45}")
    speedup = dfs_ms / astar_ms if astar_ms > 0 else 0
    print(f"Speedup: {speedup:.1f}x faster")
    print(f"Path Efficiency: A* used {len(dfs_act) - len(astar_act)} fewer steps")
    print(f"{'-' * 45}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ECS Maze Runner Pro")
    parser.add_argument("maze", nargs="?", help="The maze file (optional if generating)")
    parser.add_argument("--generate", help="Generate random maze 'W,H' e.g. '20,20'")
    parser.add_argument("--starting", help="Start pos 'x,y'")
    parser.add_argument("--goal", help="Goal pos 'x,y'")
    parser.add_argument("--astar", action="store_true", help="Use A* Solver")
    parser.add_argument("--benchmark", action="store_true", help="Compare DFS vs A*")
    parser.add_argument("--visualize", action="store_true", help="Print maze to console")

    args = parser.parse_args()

    try:
        # --- 1. ACQUIRE MAZE ---
        if args.generate:
            try:
                dims = args.generate.split(',')
                w, h = int(dims[0]), int(dims[1])
                print(f"Generating {w}x{h} maze...")
                maze = mg.generate_maze(w, h)
                filename = "generated_maze"

                # Default start/goal for generated
                start_pos = (0, 0)
                goal_pos = (w - 1, h - 1)
            except Exception:
                print("Error: Gen format is '20,20'")
                sys.exit(1)
        elif args.maze:
            print(f"Loading {args.maze}...")
            maze = maze_reader(args.maze)
            filename = args.maze

            # Default start/goal for file
            start_pos = (0, 0)
            dims = mz.get_dimensions(maze)
            goal_pos = (dims[0] - 1, dims[1] - 1)
        else:
            print("Error: Provide a file or use --generate")
            sys.exit(1)

        # Overwrite start/goal if specified manually
        if args.starting:
            p = args.starting.split(',')
            start_pos = (int(p[0]), int(p[1]))
        if args.goal:
            p = args.goal.split(',')
            goal_pos = (int(p[0]), int(p[1]))

        # --- 2. EXECUTE ---
        actions = ""

        if args.benchmark:
            run_benchmark(maze, start_pos, goal_pos)
            # Default to A* for the final output
            actions = astar_solver.solve(maze, start_pos, goal_pos, "N")

        elif args.astar:
            print("Solving with A*...")
            actions = astar_solver.solve(maze, start_pos, goal_pos, "N")

        else:
            print("Exploring with DFS...")
            runner_inst = rn.create_runner(start_pos[0], start_pos[1], "N")
            actions = rn.explore(runner_inst, maze, goal_pos)

        # Convert actions string to a  Path (Loop Erasure)
        path = trace_path_from_actions(start_pos, actions)

        if args.visualize:
            print_maze_console(maze, path)

        # Write Files
        write_logs(filename, start_pos, maze, actions, path)
        print(f"Solved! Steps: {len(actions)}. Path len: {len(path)}.")
        print(f"Logs written to 'statistics.txt' and 'exploration.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback

        traceback.print_exc()