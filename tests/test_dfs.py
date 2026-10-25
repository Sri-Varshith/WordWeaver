
import unittest

from core.dictionary import load_dictionary
from core.neighbors import get_neighbors
from core.heuristics import hamming_distance
from algorithms.dfs import dfs


class TestDFS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dictionary = load_dictionary()

    def assert_valid_path(self, result):
        path = result["path"]

        self.assertTrue(result["found"])
        self.assertGreaterEqual(len(path), 1)
        self.assertEqual(result["path_length"], len(path) - 1)

        for i in range(len(path) - 1):
            self.assertIn(path[i], self.dictionary)
            self.assertIn(
                path[i + 1],
                get_neighbors(path[i], self.dictionary),
            )
            self.assertEqual(
                hamming_distance(path[i], path[i + 1]), 1
            )

    def test_dfs_finds_valid_path(self):
        result = dfs("cold", "warm", self.dictionary)

        self.assertEqual(result["algorithm"], "DFS")
        self.assert_valid_path(result)
        self.assertEqual(result["path"][0], "cold")
        self.assertEqual(result["path"][-1], "warm")

    def test_dfs_same_word(self):
        result = dfs("cold", "cold", self.dictionary)

        self.assertTrue(result["found"])
        self.assertEqual(result["path"], ["cold"])
        self.assertEqual(result["path_length"], 0)
        self.assertEqual(result["nodes_expanded"], 0)

    def test_dfs_unreachable_target(self):

        dictionary = {"cold", "cord", "warm"}

        result = dfs("cold", "warm", dictionary)

        self.assertFalse(result["found"])
        self.assertEqual(result["path"], [])
        self.assertEqual(result["path_length"], 0)

    def test_dfs_result_format(self):
        result = dfs("cold", "warm", self.dictionary)

        expected_keys = {
            "algorithm",
            "found",
            "path",
            "path_length",
            "nodes_expanded",
            "execution_time",
        }

        self.assertEqual(set(result.keys()), expected_keys)
        self.assertGreaterEqual(result["nodes_expanded"], 0)
        self.assertGreaterEqual(result["execution_time"], 0)


if __name__ == "__main__":
    unittest.main()
