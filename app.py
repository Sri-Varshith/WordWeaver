import os
import random
import time
from flask import Flask, jsonify, render_template, request

from algorithms.astar import astar
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.gbfs import gbfs
from algorithms.hill_climbing import hill_climbing
from core.dictionary import load_dictionary
from core.heuristics import hamming_distance
from core.validation import validate_words

app = Flask(__name__)

DICTIONARY = load_dictionary()

ALGORITHMS = {
    "astar": {"name": "A* Search", "func": astar, "optimal": True, "description": "Guarantees shortest path using f(n) = g(n) + h(n)."},
    "bfs": {"name": "Breadth-First Search (BFS)", "func": bfs, "optimal": True, "description": "Explores level-by-level; always finds the shortest path."},
    "gbfs": {"name": "Greedy Best-First Search", "func": gbfs, "optimal": False, "description": "Prioritizes lowest heuristic cost h(n) towards target."},
    "hill_climbing": {"name": "Hill Climbing", "func": hill_climbing, "optimal": False, "description": "Greedy local search; fast but can get stuck in local minima."},
    "dfs": {"name": "Depth-First Search (DFS)", "func": dfs, "optimal": False, "description": "Dives deep along branches; path found is rarely shortest."},
}

PRESETS = [
    {"start": "cold", "target": "warm", "description": "Classic 4-step temperature shift"},
    {"start": "lead", "target": "gold", "description": "Alchemy transformation"},
    {"start": "head", "target": "tail", "description": "Coin toss ladder"},
    {"start": "best", "target": "good", "description": "Superlative to baseline"},
    {"start": "fire", "target": "cold", "description": "Elemental transition"},
    {"start": "ruby", "target": "code", "description": "Gets stuck in local minimum for Hill Climbing"},
    {"start": "slow", "target": "fast", "description": "Opposites ladder"},
    {"start": "dark", "target": "moon", "description": "Night sky transition"},
    {"start": "love", "target": "hate", "description": "Emotion journey"},
]


def compute_diffs(path):
    """Computes letter-by-letter mutations between consecutive words in a path."""
    if not path:
        return []
    result = []
    for i, word in enumerate(path):
        changed_idx = None
        if i > 0:
            prev = path[i - 1]
            for char_idx in range(min(len(prev), len(word))):
                if prev[char_idx] != word[char_idx]:
                    changed_idx = char_idx
                    break
        result.append({
            "step": i,
            "word": word.upper(),
            "letters": list(word.upper()),
            "changed_index": changed_idx,
        })
    return result


@app.route("/")
def index():
    return render_template("index.html", presets=PRESETS)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "dictionary_size": len(DICTIONARY)})


@app.route("/api/presets")
def get_presets():
    return jsonify(PRESETS)


@app.route("/api/random")
def get_random_pair():
    preset = random.choice(PRESETS)
    return jsonify(preset)


@app.route("/api/validate", methods=["POST"])
def validate():
    data = request.get_json(silent=True) or {}
    start = (data.get("start") or "").strip().lower()
    target = (data.get("target") or "").strip().lower()

    is_valid, msg = validate_words(start, target, DICTIONARY)
    return jsonify({
        "valid": is_valid,
        "message": msg,
        "start_in_dict": start in DICTIONARY,
        "target_in_dict": target in DICTIONARY,
        "distance": hamming_distance(start, target) if len(start) == 4 and len(target) == 4 else None,
    })


@app.route("/api/solve", methods=["POST"])
def solve():
    data = request.get_json(silent=True) or {}
    start = (data.get("start") or "").strip().lower()
    target = (data.get("target") or "").strip().lower()
    algo_key = (data.get("algorithm") or "all").strip().lower()

    is_valid, msg = validate_words(start, target, DICTIONARY)
    if not is_valid:
        return jsonify({"success": False, "error": msg}), 400

    hamming_dist = hamming_distance(start, target)

    if algo_key != "all" and algo_key in ALGORITHMS:
        info = ALGORITHMS[algo_key]
        raw_res = info["func"](start, target, DICTIONARY)
        result = {
            "key": algo_key,
            "name": info["name"],
            "description": info["description"],
            "optimal": info["optimal"],
            "found": raw_res["found"],
            "path": raw_res["path"],
            "path_length": raw_res["path_length"],
            "nodes_expanded": raw_res["nodes_expanded"],
            "execution_time_ms": round(raw_res["execution_time"] * 1000, 3),
            "steps": compute_diffs(raw_res["path"]),
        }
        return jsonify({
            "success": True,
            "mode": "single",
            "start": start.upper(),
            "target": target.upper(),
            "hamming_distance": hamming_dist,
            "result": result,
        })

    results = {}
    found_algos = []
    fastest_key = None
    shortest_key = None
    most_efficient_key = None

    min_time = float("inf")
    min_length = float("inf")
    min_expanded = float("inf")

    order = ["astar", "bfs", "gbfs", "hill_climbing", "dfs"]
    for key in order:
        info = ALGORITHMS[key]
        raw_res = info["func"](start, target, DICTIONARY)
        time_ms = round(raw_res["execution_time"] * 1000, 3)

        res_item = {
            "key": key,
            "name": info["name"],
            "description": info["description"],
            "optimal": info["optimal"],
            "found": raw_res["found"],
            "path": raw_res["path"],
            "path_length": raw_res["path_length"],
            "nodes_expanded": raw_res["nodes_expanded"],
            "execution_time_ms": time_ms,
            "steps": compute_diffs(raw_res["path"]),
        }
        results[key] = res_item

        if raw_res["found"]:
            found_algos.append(key)
            if time_ms < min_time:
                min_time = time_ms
                fastest_key = key
            if raw_res["path_length"] < min_length:
                min_length = raw_res["path_length"]
                shortest_key = key
            if raw_res["nodes_expanded"] < min_expanded:
                min_expanded = raw_res["nodes_expanded"]
                most_efficient_key = key

    summary = {
        "fastest": fastest_key,
        "shortest": shortest_key,
        "most_efficient": most_efficient_key,
        "found_count": len(found_algos),
        "total_count": len(order),
    }

    return jsonify({
        "success": True,
        "mode": "all",
        "start": start.upper(),
        "target": target.upper(),
        "hamming_distance": hamming_dist,
        "results": results,
        "summary": summary,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
