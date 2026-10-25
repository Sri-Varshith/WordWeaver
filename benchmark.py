
import time
import tracemalloc
import statistics

from core.dictionary import load_dictionary
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.gbfs import gbfs
from algorithms.astar import astar
from algorithms.hill_climbing import hill_climbing
from collections import deque
from core.neighbors import get_neighbors


ALGORITHMS = {
    "BFS": bfs,
    "DFS": dfs,
    "GBFS": gbfs,
    "A*": astar,
    "Hill Climbing": hill_climbing,
}


TEST_CASES = [
    ("cold", "warm"),
    ("cold", "cord"),
    ("cold", "cold"),
    ("ruby", "code"),
]


def benchmark_algorithm(algorithm, start, target, dictionary, repeats=5):
    times = []
    result = None

    for _ in range(repeats):
        start_time = time.perf_counter()
        result = algorithm(start, target, dictionary)
        times.append(time.perf_counter() - start_time)

    tracemalloc.start()
    algorithm(start, target, dictionary)
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "found": result["found"],
        "path_length": result["path_length"],
        "nodes_expanded": result["nodes_expanded"],
        "execution_time": statistics.median(times),
        "peak_memory_kb": peak_memory / 1024,
    }


def find_unreachable_pair(dictionary):
    unseen = set(dictionary)
    components = []

    while unseen:
        start = next(iter(unseen))
        unseen.remove(start)
        queue = deque([start])
        component = [start]

        while queue:
            word = queue.popleft()

            for neighbor in get_neighbors(word, dictionary):
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
                    component.append(neighbor)

        components.append(component)

        if len(components) == 2:
            return components[0][0], components[1][0]

    return None


def run_benchmarks():
    dictionary = load_dictionary()

    test_cases = [
    ("cold", "warm"),
    ("cold", "cord"),
    ("cold", "cold"),
    ]

    unreachable = find_unreachable_pair(dictionary)

    if unreachable:
        test_cases.append(unreachable)
        print(f"Unreachable test case: {unreachable[0]} -> {unreachable[1]}")
    else:
        print("No disconnected dictionary components found.")

    print("WordWeaver Algorithm Benchmark")
    print(f"Dictionary size: {len(dictionary)} words")
    print("Runtime: median of 5 runs\n")

    for start, target in test_cases:
        print(f"\nTest case: {start} -> {target}")
        print("-" * 90)
        print(
            f"{'Algorithm':<18} {'Found':<8} {'Length':<8} "
            f"{'Expanded':<12} {'Time (ms)':<12} {'Peak KB':<10}"
        )

        for name, algorithm in ALGORITHMS.items():
            metrics = benchmark_algorithm(
                algorithm, start, target, dictionary
            )

            print(
                f"{name:<18} "
                f"{str(metrics['found']):<8} "
                f"{metrics['path_length']:<8} "
                f"{metrics['nodes_expanded']:<12} "
                f"{metrics['execution_time'] * 1000:<12.3f} "
                f"{metrics['peak_memory_kb']:<10.2f}"
            )


if __name__ == "__main__":
    run_benchmarks()
