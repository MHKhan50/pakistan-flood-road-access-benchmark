import unittest

from floodlink_pk.graph import accessibility_record, build_grid_scenario


class GraphTests(unittest.TestCase):
    def test_accessibility_record_is_bounded(self):
        edges, node_count, hospitals, demand_nodes = build_grid_scenario(seed=91, side=5)
        probabilities = [0.9 if edge[4] else 0.1 for edge in edges]
        result = accessibility_record(edges, node_count, hospitals, demand_nodes, probabilities)
        for key in ("baseline_access_fraction", "oracle_access_fraction", "predicted_access_fraction"):
            self.assertGreaterEqual(result[key], 0.0)
            self.assertLessEqual(result[key], 1.0)
        self.assertAlmostEqual(result["baseline_access_fraction"], 1.0)


if __name__ == "__main__":
    unittest.main()
