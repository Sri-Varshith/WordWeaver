# AI Group Project - WordWeaver (word ladder)

**Group Name:** Num 3.14

### Team Members
- Umesh Vishwakarma — B24CS507
- Mahesh — B24EC509
- Srivarshith — B24EC510
- Swarit Dixit — B24EC514
- S B Pranay — B24EE045



# WordWeaver

WordWeaver is a Python-based word ladder solver and search algorithm benchmark. It finds valid transformation paths between two 4-letter words by altering one letter at a time, where every intermediate word must exist in a dictionary.

---

## Features

- **Breadth-First Search (BFS)**: Uninformed search exploring level-by-level; guarantees finding the optimal (shortest) word ladder.
- **A\* Search**: Informed heuristic search using $f(n) = g(n) + h(n)$ with admissible Hamming distance; guarantees optimal paths with fewer node expansions.
- **Greedy Best-First Search (GBFS)**: Heuristic-driven search prioritizing nodes with the lowest Hamming distance $h(n)$ to the target.
- **Greedy Hill Climbing**: Local search selecting strictly improving neighbors based on Hamming distance; fast but can get trapped in local minima.
- **Depth-First Search (DFS)**: Uninformed search diving deep into graph branches; finds a valid path if one exists without optimality guarantees.
- **Performance Benchmark**: Script measuring latency, peak memory, nodes expanded, and path length across all algorithms.
- **Minimalist Web Interface**: Interactive single-page application for solving word ladders and comparing algorithms side by side.
- **Dictionary & Neighbor Generation**: $O(1)$ set-based lookups and 1-letter mutation discovery.
- **Input Validation**: Verifies that start and target words are valid 4-letter alphabetic dictionary entries.

---

## Project Structure

```text
wordweaver/
├── algorithms/
│   ├── __init__.py
│   ├── astar.py             # A* Search solver
│   ├── bfs.py               # BFS shortest-path solver
│   ├── dfs.py               # Depth-First Search solver
│   ├── gbfs.py              # Greedy Best-First Search solver
│   └── hill_climbing.py     # Greedy Hill Climbing solver
├── core/
│   ├── __init__.py
│   ├── dictionary.py        # Loads word list into a set
│   ├── heuristics.py        # Hamming distance metric
│   ├── neighbors.py         # 1-letter mutation generator
│   └── validation.py        # Validates start/target words
├── data/
│   ├── dictionary.txt
│   └── words.txt            # 4-letter word dataset
├── templates/
│   └── index.html           # Web interface frontend
├── app.py                   # Flask server and API endpoints
├── benchmark.py             # Multi-algorithm performance benchmark
├── requirements.txt         # Project dependencies
├── dictionary.txt
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher.
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Running the Web Interface

Launch the local web application:

```bash
python3 app.py
```

Then navigate to `http://localhost:5000` in your browser.

### Running the Benchmark

Execute the algorithm performance comparison suite:

```bash
python3 benchmark.py
```

---

## Usage Example

```python
from core.dictionary import load_dictionary
from core.validation import validate_words
from algorithms.bfs import bfs
from algorithms.astar import astar
from algorithms.hill_climbing import hill_climbing

# 1. Load dictionary
dictionary = load_dictionary()

# 2. Validate input words
start, target = "cold", "warm"
is_valid, msg = validate_words(start, target, dictionary)

if not is_valid:
    print(f"Validation error: {msg}")
else:
    # 3. Solve with A* (Optimal, heuristic-guided)
    astar_res = astar(start, target, dictionary)
    print("A* Result:")
    print(f"  Path: {' -> '.join(astar_res['path'])}")
    print(f"  Length: {astar_res['path_length']}")
    print(f"  Nodes Expanded: {astar_res['nodes_expanded']}")
    print(f"  Execution Time: {astar_res['execution_time']}s\n")

    # 4. Solve with BFS (Optimal, uniform breadth)
    bfs_res = bfs(start, target, dictionary)
    print("BFS Result:")
    print(f"  Path: {' -> '.join(bfs_res['path'])}")
    print(f"  Length: {bfs_res['path_length']}")
    print(f"  Nodes Expanded: {bfs_res['nodes_expanded']}")
    print(f"  Execution Time: {bfs_res['execution_time']}s\n")

    # 5. Solve with Hill Climbing (Local search)
    hc_res = hill_climbing(start, target, dictionary)
    print("Hill Climbing Result:")
    print(f"  Found: {hc_res['found']}")
    print(f"  Path: {' -> '.join(hc_res['path'])}")
    print(f"  Nodes Expanded: {hc_res['nodes_expanded']}")
    print(f"  Execution Time: {hc_res['execution_time']}s")
```

---

## Algorithm Comparison

| Algorithm | Strategy | Complete? | Optimal? | Handles Local Minima? |
| :--- | :--- | :--- | :--- | :--- |
| **BFS** | Level-by-level breadth exploration | Yes | Yes (Shortest path) | Yes |
| **A\*** | Path cost + Hamming heuristic ($g + h$) | Yes | Yes (Shortest path) | Yes |
| **GBFS** | Greedy lowest heuristic cost ($h$) | Yes | No | Yes (Backtracks out) |
| **Hill Climbing** | Steepest descent on Hamming distance | No | No | No (Can get trapped) |
| **DFS** | Exhaustive branch-first traversal | Yes | No | Yes |
