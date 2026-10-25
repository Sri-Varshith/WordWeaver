
import time
import heapq
from itertools import count

from core.neighbors import get_neighbors
from core.heuristics import hamming_distance


def astar(start_word, target_word, dictionary):
    start_time = time.perf_counter()
    start_word = start_word.lower()
    target_word = target_word.lower()

    if start_word == target_word:
        return {
            "algorithm": "A*",
            "found": True,
            "path": [start_word],
            "path_length": 0,
            "nodes_expanded": 0,
            "execution_time": round(time.perf_counter() - start_time, 6),
        }

    tie_breaker = count()
    frontier = [
        (hamming_distance(start_word, target_word), next(tie_breaker),
         start_word)
    ]
    g_score = {start_word: 0}
    parent = {start_word: None}
    nodes_expanded = 0

    while frontier:
        _, _, current = heapq.heappop(frontier)

        current_g = g_score[current]
        nodes_expanded += 1

        if current == target_word:
            path = []
            word = current

            while word is not None:
                path.append(word)
                word = parent[word]

            path.reverse()

            return {
                "algorithm": "A*",
                "found": True,
                "path": path,
                "path_length": len(path) - 1,
                "nodes_expanded": nodes_expanded,
                "execution_time": round(
                    time.perf_counter() - start_time, 6
                ),
            }

        for neighbor in get_neighbors(current, dictionary):
            tentative_g = current_g + 1

            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                parent[neighbor] = current

                f_score = tentative_g + hamming_distance(
                    neighbor, target_word
                )

                heapq.heappush(
                    frontier,
                    (f_score, next(tie_breaker), neighbor),
                )

    return {
        "algorithm": "A*",
        "found": False,
        "path": [],
        "path_length": 0,
        "nodes_expanded": nodes_expanded,
        "execution_time": round(time.perf_counter() - start_time, 6),
    }
