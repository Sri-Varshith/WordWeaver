
import time
from core.neighbors import get_neighbors


def dfs(start_word, target_word, dictionary):
    """
    Finds a word ladder using Depth-First Search (DFS).
    It finds a valid path if one exists, but
    does not guarantee the shortest path.
    """
    start_time = time.perf_counter()

    start_word = start_word.lower()
    target_word = target_word.lower()

    if start_word == target_word:
        return {
            "algorithm": "DFS",
            "found": True,
            "path": [start_word],
            "path_length": 0,
            "nodes_expanded": 0,
            "execution_time": round(
                time.perf_counter() - start_time, 6
            ),
        }


    stack = [start_word]

    visited = {start_word}


    parent = {start_word: None}

    nodes_expanded = 0

    while stack:
        current = stack.pop()
        nodes_expanded += 1

        for neighbor in get_neighbors(current, dictionary):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            parent[neighbor] = current


            if neighbor == target_word:
                path = []
                word = target_word

                while word is not None:
                    path.append(word)
                    word = parent[word]

                path.reverse()

                return {
                    "algorithm": "DFS",
                    "found": True,
                    "path": path,
                    "path_length": len(path) - 1,
                    "nodes_expanded": nodes_expanded,
                    "execution_time": round(
                        time.perf_counter() - start_time, 6
                    ),
                }

            stack.append(neighbor)

    # No path exists in the reachable dictionary graph.
    return {
        "algorithm": "DFS",
        "found": False,
        "path": [],
        "path_length": 0,
        "nodes_expanded": nodes_expanded,
        "execution_time": round(
            time.perf_counter() - start_time, 6
        ),
    }
