
import time
import heapq
from itertools import count

from core.neighbors import get_neighbors
from core.heuristics import hamming_distance


def gbfs(start_word, target_word, dictionary):
    start_time = time.perf_counter()
    start_word = start_word.lower()
    target_word = target_word.lower()

    if start_word == target_word:
        return {
            "algorithm": "GBFS",
            "found": True,
            "path": [start_word],
            "path_length": 0,
            "nodes_expanded": 0,
            "execution_time": round(time.perf_counter() - start_time, 6),
        }

    tie_breaker = count()
    frontier = [(hamming_distance(start_word, target_word),
                 next(tie_breaker), start_word)]
    visited = {start_word}
    parent = {start_word: None}
    nodes_expanded = 0

    while frontier:
        _, _, current = heapq.heappop(frontier)
        nodes_expanded += 1

        if current == target_word:
            path = []
            word = current

            while word is not None:
                path.append(word)
                word = parent[word]

            path.reverse()

            return {
                "algorithm": "GBFS",
                "found": True,
                "path": path,
                "path_length": len(path) - 1,
                "nodes_expanded": nodes_expanded,
                "execution_time": round(time.perf_counter() - start_time, 6),
            }

        for neighbor in get_neighbors(current, dictionary):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                priority = hamming_distance(neighbor, target_word)
                heapq.heappush(
                    frontier, (priority, next(tie_breaker), neighbor)
                )

    return {
        "algorithm": "GBFS",
        "found": False,
        "path": [],
        "path_length": 0,
        "nodes_expanded": nodes_expanded,
        "execution_time": round(time.perf_counter() - start_time, 6),
    }
