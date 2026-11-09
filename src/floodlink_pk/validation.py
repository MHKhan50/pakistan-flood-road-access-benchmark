"""Schema validation for a future Pakistan road-link exposure table."""

from pathlib import Path
from typing import Dict, List

from .data import read_rows


def validate_real_data(path: Path) -> Dict[str, object]:
    rows = read_rows(path)
    scenario_ids = {str(row["scenario_id"]) for row in rows}
    labels = [int(row["flood_exposed"]) for row in rows]
    return {
        "path": str(path),
        "rows": len(rows),
        "unique_scenarios": len(scenario_ids),
        "positive_labels": sum(labels),
        "positive_rate": sum(labels) / len(labels),
        "status": "schema_validated_only",
        "warning": "Schema validation does not establish geospatial correctness, label validity, or road passability.",
    }
