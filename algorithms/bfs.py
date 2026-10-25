import time
from collections import deque
from core.neighbors import get_neighbors

def bfs(start_word, target_word, dictionary):
    """
    Finds the shortest word ladder using Breadth-First Search (BFS).
    Guarantees the shortest path.
    """
    start_time = time.perf_counter()
    start_word = start_word.lower()
    target_word = target_word.lower()

    if start_word == target_word:
        return {
            "algorithm": "BFS",
            "found": True,
            "path": [start_word],
            "path_length": 0,
            "nodes_expanded": 0,
            "execution_time": round(time.perf_counter() - start_time, 6)
        }

    queue = deque([[start_word]])
    visited = {start_word}
    nodes_expanded = 0

    while queue:
        path = queue.popleft()
        current_word = path[-1]
        nodes_expanded += 1

        for neighbor in get_neighbors(current_word, dictionary):
            if neighbor == target_word:
                full_path = path + [neighbor]
                return {
                    "algorithm": "BFS",
                    "found": True,
                    "path": full_path,
                    "path_length": len(full_path) - 1,
                    "nodes_expanded": nodes_expanded,
                    "execution_time": round(time.perf_counter() - start_time, 6)
                }

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return {
        "algorithm": "BFS",
        "found": False,
        "path": [],
        "path_length": 0,
        "nodes_expanded": nodes_expanded,
        "execution_time": round(time.perf_counter() - start_time, 6)
    }
