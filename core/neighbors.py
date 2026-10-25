def get_neighbors(word, dictionary):
    """Generates all valid dictionary words that differ from word by exactly one letter."""
    neighbors = []
    for i in range(len(word)):
        for char in "abcdefghijklmnopqrstuvwxyz":
            if char != word[i]:
                candidate = word[:i] + char + word[i + 1:]
                if candidate in dictionary:
                    neighbors.append(candidate)
    return neighbors
