import unittest
from core.dictionary import load_dictionary
from core.neighbors import get_neighbors
from core.heuristics import hamming_distance
from core.validation import validate_words
from algorithms.bfs import bfs
from algorithms.hill_climbing import hill_climbing

class TestMember1Components(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dict = load_dictionary()

    def test_dictionary_loaded(self):
        self.assertGreater(len(self.dict), 0)
        self.assertIn("cold", self.dict)
        self.assertIn("warm", self.dict)

    def test_neighbors(self):
        neighbors = get_neighbors("cold", self.dict)
        self.assertIn("cord", neighbors)
        self.assertIn("gold", neighbors)
        for n in neighbors:
            self.assertEqual(len(n), 4)
            self.assertEqual(hamming_distance("cold", n), 1)

    def test_heuristics(self):
        self.assertEqual(hamming_distance("cold", "warm"), 4)
        self.assertEqual(hamming_distance("cold", "cord"), 1)
        self.assertEqual(hamming_distance("cold", "cold"), 0)

    def test_validation(self):
        valid, _ = validate_words("cold", "warm", self.dict)
        self.assertTrue(valid)

        invalid_len, msg1 = validate_words("col", "warm", self.dict)
        self.assertFalse(invalid_len)

        invalid_dict, msg2 = validate_words("zzzz", "warm", self.dict)
        self.assertFalse(invalid_dict)

    def test_bfs_shortest_path(self):
        result = bfs("cold", "warm", self.dict)
        self.assertTrue(result["found"])
        self.assertEqual(result["path_length"], 4)
        self.assertEqual(result["path"][0], "cold")
        self.assertEqual(result["path"][-1], "warm")

    def test_bfs_same_word(self):
        result = bfs("cold", "cold", self.dict)
        self.assertTrue(result["found"])
        self.assertEqual(result["path"], ["cold"])
        self.assertEqual(result["path_length"], 0)
        self.assertEqual(result["nodes_expanded"], 0)

    def test_hill_climbing(self):
        result = hill_climbing("cold", "warm", self.dict)
        self.assertTrue(result["found"])
        self.assertEqual(result["path"], ["cold", "cord", "card", "ward", "warm"])
        self.assertEqual(result["path_length"], 4)

        # Test local minimum where it gets stuck
        stuck_result = hill_climbing("ruby", "code", self.dict)
        self.assertFalse(stuck_result["found"])
        self.assertEqual(stuck_result["path_length"], 0)

if __name__ == "__main__":
    unittest.main()
