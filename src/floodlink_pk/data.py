"""Synthetic scenario generation and CSV utilities.

Synthetic labels are generated from a transparent hazard function. They are
useful for testing the pipeline, not a substitute for observed Pakistan data.
"""

import csv
import math
import random
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

FEATURE_COLUMNS = (
    "elevation_m",
    "slope_pct",
    "distance_to_river_km",
    "rainfall_24h_mm",
    "rainfall_72h_mm",
    "soil_moisture_fraction",
    "road_class_code",
    "bridge_flag",
)

REQUIRED_COLUMNS = ("segment_id", "scenario_id") + FEATURE_COLUMNS + ("flood_exposed",)

ROAD_CLASSES = {
    0: "motorway",
    1: "trunk",
    2: "primary",
    3: "secondary",
    4: "local_or_unclassified",
}


def sigmoid(value: float) -> float:
    if value >= 0.0:
        inverse = math.exp(-value)
        return 1.0 / (1.0 + inverse)
    exponential = math.exp(value)
    return exponential / (1.0 + exponential)


def hazard_probability(features: Dict[str, float]) -> float:
    """Return a transparent synthetic probability of satellite flood exposure."""
    score = (
        -3.55
        + 0.018 * features["rainfall_24h_mm"]
        + 0.007 * features["rainfall_72h_mm"]
        + 1.35 * features["soil_moisture_fraction"]
        - 0.075 * features["elevation_m"]
        - 0.19 * features["distance_to_river_km"]
        + 0.42 * features["bridge_flag"]
        + 0.11 * features["road_class_code"]
        + 0.055 * features["slope_pct"]
    )
    return sigmoid(score)


def sample_segment_features(
    rng: random.Random,
    rainfall_24h_mm: float,
    rainfall_72h_mm: float,
    soil_moisture_fraction: float,
) -> Dict[str, float]:
    """Sample one synthetic road-link feature vector."""
    return {
        "elevation_m": round(rng.uniform(0.5, 38.0), 3),
        "slope_pct": round(rng.uniform(0.0, 8.0), 3),
        "distance_to_river_km": round(rng.uniform(0.05, 12.0), 3),
        "rainfall_24h_mm": round(rainfall_24h_mm, 3),
        "rainfall_72h_mm": round(rainfall_72h_mm, 3),
        "soil_moisture_fraction": round(soil_moisture_fraction, 4),
        "road_class_code": float(rng.randrange(5)),
        "bridge_flag": float(rng.random() < 0.16),
    }


def generate_synthetic_rows(
    scenarios: int = 80,
    segments_per_scenario: int = 50,
    seed: int = 17,
) -> List[Dict[str, float]]:
    """Generate grouped scenarios with shared weather and local road features."""
    if scenarios < 4:
        raise ValueError("scenarios must be at least 4 for a grouped train/test split")
    if segments_per_scenario < 5:
        raise ValueError("segments_per_scenario must be at least 5")

    rng = random.Random(seed)
    rows: List[Dict[str, float]] = []
    for scenario_index in range(scenarios):
        rainfall_24h = rng.uniform(5.0, 170.0)
        rainfall_72h = rainfall_24h + rng.uniform(10.0, 260.0)
        soil_moisture = rng.uniform(0.08, 0.72)
        for segment_index in range(segments_per_scenario):
            features = sample_segment_features(rng, rainfall_24h, rainfall_72h, soil_moisture)
            probability = hazard_probability(features)
            # Bernoulli sampling makes the task probabilistic rather than a
            # deterministic threshold-recovery exercise.
            label = int(rng.random() < probability)
            row: Dict[str, float] = {
                "segment_id": "S{:03d}-R{:04d}".format(scenario_index, segment_index),
                "scenario_id": "SCN-{:03d}".format(scenario_index),
            }
            row.update(features)
            row["flood_exposed"] = label
            rows.append(row)
    return rows


def write_rows(path: Path, rows: Sequence[Dict[str, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(REQUIRED_COLUMNS))
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> List[Dict[str, float]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError("Missing required columns: {}".format(", ".join(missing)))
        rows: List[Dict[str, float]] = []
        for line_number, raw in enumerate(reader, start=2):
            row: Dict[str, float] = {
                "segment_id": raw["segment_id"],
                "scenario_id": raw["scenario_id"],
            }
            for column in FEATURE_COLUMNS + ("flood_exposed",):
                try:
                    row[column] = float(raw[column])
                except (TypeError, ValueError):
                    raise ValueError(
                        "Invalid numeric value for '{}' on line {}".format(column, line_number)
                    )
            if row["flood_exposed"] not in (0.0, 1.0):
                raise ValueError("flood_exposed must be 0 or 1 on line {}".format(line_number))
            rows.append(row)
    if not rows:
        raise ValueError("CSV contains a header but no data rows")
    return rows


def grouped_split(
    rows: Sequence[Dict[str, float]],
    test_fraction: float = 0.25,
    seed: int = 17,
) -> Tuple[List[Dict[str, float]], List[Dict[str, float]]]:
    """Split by scenario, preventing links from one scenario leaking across sets."""
    if not 0.1 <= test_fraction <= 0.5:
        raise ValueError("test_fraction must be between 0.1 and 0.5")
    scenario_ids = sorted({str(row["scenario_id"]) for row in rows})
    if len(scenario_ids) < 4:
        raise ValueError("At least four unique scenarios are required")
    rng = random.Random(seed)
    rng.shuffle(scenario_ids)
    test_count = max(1, int(round(len(scenario_ids) * test_fraction)))
    test_ids = set(scenario_ids[:test_count])
    train_rows = [row for row in rows if str(row["scenario_id"]) not in test_ids]
    test_rows = [row for row in rows if str(row["scenario_id"]) in test_ids]
    return train_rows, test_rows


def feature_vector(row: Dict[str, float]) -> List[float]:
    return [float(row[column]) for column in FEATURE_COLUMNS]
