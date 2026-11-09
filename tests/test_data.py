import tempfile
import unittest
from pathlib import Path

from floodlink_pk.data import FEATURE_COLUMNS, generate_synthetic_rows, grouped_split, read_rows, write_rows


class SyntheticDataTests(unittest.TestCase):
    def test_generation_is_deterministic(self):
        first = generate_synthetic_rows(scenarios=8, segments_per_scenario=10, seed=41)
        second = generate_synthetic_rows(scenarios=8, segments_per_scenario=10, seed=41)
        self.assertEqual(first, second)

    def test_grouped_split_has_no_scenario_leakage(self):
        rows = generate_synthetic_rows(scenarios=12, segments_per_scenario=8, seed=7)
        train, test = grouped_split(rows, test_fraction=0.25, seed=19)
        train_ids = {row["scenario_id"] for row in train}
        test_ids = {row["scenario_id"] for row in test}
        self.assertTrue(train_ids)
        self.assertTrue(test_ids)
        self.assertTrue(train_ids.isdisjoint(test_ids))

    def test_features_are_present_and_in_expected_ranges(self):
        rows = generate_synthetic_rows(scenarios=4, segments_per_scenario=5, seed=5)
        for row in rows:
            self.assertTrue(all(column in row for column in FEATURE_COLUMNS))
            self.assertIn(row["flood_exposed"], (0, 1))
            self.assertGreaterEqual(row["soil_moisture_fraction"], 0.0)
            self.assertLessEqual(row["soil_moisture_fraction"], 1.0)

    def test_csv_round_trip(self):
        rows = generate_synthetic_rows(scenarios=4, segments_per_scenario=5, seed=3)
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "segments.csv"
            write_rows(path, rows)
            loaded = read_rows(path)
        self.assertEqual(len(rows), len(loaded))
        self.assertEqual(rows[0]["segment_id"], loaded[0]["segment_id"])
        self.assertEqual(float(rows[0]["flood_exposed"]), loaded[0]["flood_exposed"])


if __name__ == "__main__":
    unittest.main()
