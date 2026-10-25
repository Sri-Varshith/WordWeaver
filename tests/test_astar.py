
import unittest

from core.dictionary import load_dictionary
from core.neighbors import get_neighbors
from algorithms.bfs import bfs
from algorithms.astar import astar


class TestAStar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dictionary = load_dictionary()

    def test_astar_finds_valid_path(self):
        result = astar("cold", "warm", self.dictionary)

        self.assertTrue(result["found"])
        self.assertEqual(result["path"][0], "cold")
        self.assertEqual(result["path"][-1], "warm")
        self.assertEqual(result["path_length"], len(result["path"]) - 1)

        for i in range(len(result["path"]) - 1):
            self.assertIn(
                result["path"][i + 1],
                get_neighbors(result["path"][i], self.dictionary),
            )

    def test_astar_matches_bfs_shortest_path(self):
        astar_result = astar("cold", "warm", self.dictionary)
        bfs_result = bfs("cold", "warm", self.dictionary)

        self.assertTrue(astar_result["found"])
        self.assertTrue(bfs_result["found"])
        self.assertEqual(
            astar_result["path_length"],
            bfs_result["path_length"],
        )

    def test_astar_same_word(self):
        result = astar("cold", "cold", self.dictionary)

        self.assertTrue(result["found"])
        self.assertEqual(result["path"], ["cold"])
        self.assertEqual(result["path_length"], 0)

    def test_astar_unreachable_target(self):
        dictionary = {"cold", "cord", "warm"}
        result = astar("cold", "warm", dictionary)

        self.assertFalse(result["found"])
        self.assertEqual(result["path"], [])
        self.assertEqual(result["path_length"], 0)

    def test_astar_result_format(self):
        result = astar("cold", "warm", self.dictionary)

        self.assertEqual(
            set(result),
            {
                "algorithm", "found", "path", "path_length",
                "nodes_expanded", "execution_time",
            },
        )


if __name__ == "__main__":
    unittest.main()
