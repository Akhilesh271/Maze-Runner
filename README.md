# Algorithmic Maze Generator & Solver

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/akhilesh271/maze-runner/graphs/commit-activity)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A high-performance, algorithmic framework built in Python for procedurally generating complex maze environments and computing optimal navigation routes [cite: 2]. This project serves as a robust testbed for analyzing search algorithm efficiency, heuristic performance, and memory management in pathfinding problems [cite: 2].

---

## Key Features

* **Procedural Maze Generation:** Utilizes an optimized, randomized Depth-First Search (DFS) architecture to reliably generate perfect, solvable mazes of arbitrary dimensions [cite: 2].
* **Optimal Pathfinding:** Implements a highly efficient A* (A-Star) search algorithm equipped with optimized heuristics to precisely calculate the shortest path from start to finish [cite: 2].
* **Performance Analytics Pipeline:** Features a programmatic data logging system that automatically tracks and exports algorithmic complexity metrics (time, nodes expanded, memory state) to `exploration.csv` and `statistics.txt` for in-depth analysis [cite: 2].
* **Modular Architecture:** Game logic, maze state, and solving algorithms are strictly decoupled, allowing for rapid swapping of generation algorithms or heuristic functions without refactoring core engine components [cite: 2].

---

## Repository Structure

```text
maze-runner/
│
├── maze.py               # Core data structures for the maze grid and node states
├── maze_generator.py     # Randomized DFS implementation for procedural generation
├── astar_solver.py       # A* algorithm implementation with custom heuristic functions
├── runner.py / runner2.py# Execution entry points and CLI handling
├── maze_runner.py        # Orchestrator integrating generation, solving, and logging
├── exploration.csv       # Exported runtime metrics and node exploration data
└── statistics.txt        # Aggregated performance summaries for completed runs
```

---

## Installation & Setup

### Prerequisites
This project requires **Python 3.12** or higher [cite: 2].

1. **Clone the repository:**
   ```bash
   git clone https://github.com/akhilesh271/maze-runner.git
   cd maze-runner
   ```

2. **(Optional) Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   *(Note: This project relies primarily on Python standard libraries to minimize overhead, but any required analysis packages like `pandas` for reading CSVs can be installed via a requirements file if present)* [cite: 2].
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the main solver from the command line [cite: 2]. You can configure the dimensions of the generated maze directly within the execution script or via command-line arguments (if enabled) [cite: 2].

```bash
python runner.py
```

### Example Output
When executed, the program will generate the maze, compute the optimal path, and output a summary similar to the following to the console, while simultaneously updating the logging files [cite: 2]:

```text
[+] Initializing 1000x1000 Grid...
[+] Generating Maze (Randomized DFS)... Done (142ms)
[+] Running A* Pathfinding...
[+] Target Reached!
    - Path Length: 4,231 steps
    - Nodes Explored: 450,122
    - Search Time: 310ms
[+] Metrics exported to exploration.csv and statistics.txt
```

---

## Analytics & Logging

The framework automatically intercepts core pathfinding metrics to facilitate algorithmic complexity analysis [cite: 2]:

* **`exploration.csv`**: Contains granular, step-by-step data of the A* search tree, including `node_id`, `g_cost`, `h_cost`, `f_cost`, and `exploration_timestamp` [cite: 2]. 
* **`statistics.txt`**: Logs macro-level execution data per run, ideal for benchmarking different heuristic functions against mazes of scaling dimensions [cite: 2].

---

## Future Enhancements
* **Algorithm Expansion:** Integration of Dijkstra's Algorithm and Breadth-First Search (BFS) for comparative baseline testing against A* [cite: 2].
* **Visualizer UI:** Implementation of a lightweight `pygame` or `tkinter` frontend for real-time visualization of the pathfinding frontier [cite: 2].
* **Heuristic Weighting:** Dynamic weighting parameter for A* to allow testing of greedy best-first search behaviors [cite: 2].

---

## License
This project is open-source and available under the [MIT License](LICENSE) [cite: 2].
