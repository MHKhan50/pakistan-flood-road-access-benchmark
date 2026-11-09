import tempfile
import unittest
from pathlib import Path

from floodlink_pk.data import generate_synthetic_rows, write_rows
from floodlink_pk.validation import validate_real_data


class ValidationTests(unittest.TestCase):
    def test_schema_validation_reports_only_schema_status(self):
        rows = generate_synthetic_rows(scenarios=4, segments_per_scenario=5, seed=71)
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "candidate.csv"
            write_rows(path, rows)
            result = validate_real_data(path)
        self.assertEqual(result["status"], "schema_validated_only")
        self.assertIn("does not establish", result["warning"])
        self.assertEqual(result["rows"], 20)


if __name__ == "__main__":
    unittest.main()
