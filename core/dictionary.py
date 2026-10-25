import os

def load_dictionary(filepath="data/words.txt"):
    """Loads and returns words from the dictionary file as a set of lowercase strings."""
    if not os.path.exists(filepath):
        filepath = os.path.join(os.path.dirname(__file__), "..", filepath)
    
    with open(filepath, "r", encoding="utf-8") as f:
        return set(line.strip().lower() for line in f if line.strip())
