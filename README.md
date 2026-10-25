# WordWeaver

WordWeaver is a Python-based word ladder solver and search algorithm benchmark. It finds valid transformation paths between two 4-letter words by altering one letter at a time, where every intermediate word must exist in a dictionary.

---

## Features

- **Breadth-First Search (BFS)**: Uninformed search that guarantees finding the optimal (shortest) word ladder path.
- **Greedy Hill Climbing**: Heuristic-guided search utilizing Hamming distance. Prioritizes steepest descent toward the target; can encounter local minima / plateaus.
- **Dictionary & Neighbor Generation**: Fast O(1) set-based dictionary lookups and 1-letter mutation discovery.
- **Input Validation**: Ensures inputs are valid 4-letter alphabetic words present in the dictionary.
- **Automated Unit Tests**: Comprehensive test suite covering core modules and search algorithms.

---

## Project Structure

```text
wordweaver/
├── algorithms/
│   ├── __init__.py
│   ├── bfs.py               # BFS shortest-path solver
│   └── hill_climbing.py     # Greedy hill climbing with Hamming distance
├── core/
│   ├── __init__.py
│   ├── dictionary.py        # Loads word list into a set
│   ├── heuristics.py        # Hamming distance metric
│   ├── neighbors.py         # 1-letter mutation generator
│   └── validation.py        # Validates start/target words
├── data/
│   ├── dictionary.txt -> words.txt
│   └── words.txt            # 4-letter word dataset
├── tests/
│   ├── __init__.py
│   └── test_member1.py      # Unit tests
├── dictionary.txt
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher (no external dependencies required).

### Installation

Clone the repository and enter the directory:

```bash
git clone https://github.com/Sri-Varshith/WordWeaver.git
cd WordWeaver
```

---

## Usage Example

```python
from core.dictionary import load_dictionary
from core.validation import validate_words
from algorithms.bfs import bfs
from algorithms.hill_climbing import hill_climbing

# 1. Load dictionary
dictionary = load_dictionary()

# 2. Validate input words
start, target = "cold", "warm"
is_valid, msg = validate_words(start, target, dictionary)

if not is_valid:
    print(f"Validation error: {msg}")
else:
    # 3. Solve with BFS (Optimal)
    bfs_res = bfs(start, target, dictionary)
    print("BFS Result:")
    print(f"  Path: {' -> '.join(bfs_res['path'])}")
    print(f"  Length: {bfs_res['path_length']}")
    print(f"  Nodes Expanded: {bfs_res['nodes_expanded']}")
    print(f"  Execution Time: {bfs_res['execution_time']}s\n")

    # 4. Solve with Hill Climbing (Heuristic)
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
| **BFS** | Uniform breadth exploration | Yes | Yes (Shortest path) | Yes |
| **Hill Climbing** | Greedy Hamming distance | No | No | No (Can get trapped) |

---

## Running Tests

Execute the unit test suite:

```bash
python3 -m unittest discover tests
```
