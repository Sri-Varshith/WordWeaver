def hamming_distance(word1, word2):
    """Calculates the number of differing characters between two words."""
    return sum(c1 != c2 for c1, c2 in zip(word1, word2))
