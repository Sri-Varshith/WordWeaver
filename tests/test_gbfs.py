
import unittest

from core.dictionary import load_dictionary
from core.neighbors import get_neighbors
from core.heuristics import hamming_distance
from algorithms.gbfs import gbfs


class TestGBFS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dictionary = load_dictionary()

    def test_gbfs_finds_valid_path(self):
        result = gbfs("cold", "warm", self.dictionary)

        self.assertTrue(result["found"])
        self.assertEqual(result["path"][0], "cold")
        self.assertEqual(result["path"][-1], "warm")
        self.assertEqual(result["path_length"], len(result["path"]) - 1)

        for i in range(len(result["path"]) - 1):
            self.assertIn(
                result["path"][i + 1],
                get_neighbors(result["path"][i], self.dictionary),
            )
            self.assertEqual(
                hamming_distance(
                    result["path"][i], result["path"][i + 1]
                ),
                1,
            )

    def test_gbfs_same_word(self):
        result = gbfs("cold", "cold", self.dictionary)

        self.assertTrue(result["found"])
        self.assertEqual(result["path"], ["cold"])
        self.assertEqual(result["path_length"], 0)

    def test_gbfs_unreachable_target(self):
        dictionary = {"cold", "cord", "warm"}
        result = gbfs("cold", "warm", dictionary)

        self.assertFalse(result["found"])
        self.assertEqual(result["path"], [])
        self.assertEqual(result["path_length"], 0)

    def test_gbfs_result_format(self):
        result = gbfs("cold", "warm", self.dictionary)

        self.assertEqual(
            set(result),
            {
                "algorithm", "found", "path", "path_length",
                "nodes_expanded", "execution_time",
            },
        )
        self.assertGreaterEqual(result["nodes_expanded"], 0)
        self.assertGreaterEqual(result["execution_time"], 0)


if __name__ == "__main__":
    unittest.main()
