import unittest

from floodlink_pk.data import generate_synthetic_rows, grouped_split
from floodlink_pk.metrics import classification_metrics
from floodlink_pk.model import TinyMLP


class ModelTests(unittest.TestCase):
    def test_model_returns_probabilities_in_unit_interval(self):
        rows = generate_synthetic_rows(scenarios=12, segments_per_scenario=12, seed=11)
        train, test = grouped_split(rows, test_fraction=0.25, seed=13)
        model = TinyMLP(seed=23).fit(train, epochs=8)
        probabilities = model.predict_proba(test)
        self.assertEqual(len(probabilities), len(test))
        self.assertTrue(all(0.0 <= value <= 1.0 for value in probabilities))

    def test_metrics_are_finite(self):
        result = classification_metrics([0, 1, 0, 1], [0.1, 0.8, 0.4, 0.7])
        self.assertAlmostEqual(result["accuracy"], 1.0)
        self.assertAlmostEqual(result["roc_auc"], 1.0)
        self.assertGreaterEqual(result["brier_score"], 0.0)
        self.assertLessEqual(result["brier_score"], 1.0)

    def test_metrics_reject_empty_input(self):
        with self.assertRaises(ValueError):
            classification_metrics([], [])


if __name__ == "__main__":
    unittest.main()
