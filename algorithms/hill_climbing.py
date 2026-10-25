import time
from core.neighbors import get_neighbors
from core.heuristics import hamming_distance

def hill_climbing(start_word, target_word, dictionary):
    """
    Finds a word ladder using Greedy Hill Climbing with the Hamming distance heuristic.
    Selects strictly improving neighbors. Can get stuck in local minima.
    """
    start_time = time.perf_counter()
    start_word = start_word.lower()
    target_word = target_word.lower()

    if start_word == target_word:
        return {
            "algorithm": "Hill Climbing",
            "found": True,
            "path": [start_word],
            "path_length": 0,
            "nodes_expanded": 0,
            "execution_time": round(time.perf_counter() - start_time, 6)
        }

    current = start_word
    path = [current]
    visited = {current}
    nodes_expanded = 0

    while current != target_word:
        nodes_expanded += 1
        current_h = hamming_distance(current, target_word)
        neighbors = get_neighbors(current, dictionary)

        # Find unvisited neighbors that strictly improve heuristic (smaller Hamming distance)
        improving = [
            n for n in neighbors
            if n not in visited and hamming_distance(n, target_word) < current_h
        ]

        if not improving:
            # Stuck in local minimum / plateau
            return {
                "algorithm": "Hill Climbing",
                "found": False,
                "path": [],
                "path_length": 0,
                "nodes_expanded": nodes_expanded,
                "execution_time": round(time.perf_counter() - start_time, 6)
            }

        # Choose the neighbor with smallest Hamming distance (alphabetical tie-breaker)
        improving.sort(key=lambda n: (hamming_distance(n, target_word), n))
        current = improving[0]
        visited.add(current)
        path.append(current)

    return {
        "algorithm": "Hill Climbing",
        "found": True,
        "path": path,
        "path_length": len(path) - 1,
        "nodes_expanded": nodes_expanded,
        "execution_time": round(time.perf_counter() - start_time, 6)
    }
