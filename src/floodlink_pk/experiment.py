"""End-to-end reproducible synthetic experiment."""

import csv
import json
from pathlib import Path
from typing import Dict, List

from .data import FEATURE_COLUMNS, generate_synthetic_rows, grouped_split
from .graph import accessibility_record, build_grid_scenario
from .metrics import classification_metrics
from .model import TinyMLP


def run_experiment(output_dir: Path, seed: int = 17, scenarios: int = 80,
                   segments_per_scenario: int = 50, epochs: int = 55) -> Dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = generate_synthetic_rows(scenarios, segments_per_scenario, seed)
    train_rows, test_rows = grouped_split(rows, test_fraction=0.25, seed=seed + 1)
    model = TinyMLP(seed=seed + 2).fit(train_rows, epochs=epochs)
    probabilities = model.predict_proba(test_rows)
    labels = [int(row["flood_exposed"]) for row in test_rows]
    metrics = classification_metrics(labels, probabilities, threshold=0.5)
    thresholds = (0.25, 0.35, 0.50, 0.65)
    threshold_rows = [classification_metrics(labels, probabilities, threshold=value) for value in thresholds]
    with (output_dir / "threshold_sensitivity.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = list(threshold_rows[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(threshold_rows)
    metrics.update({
        "seed": seed,
        "train_rows": len(train_rows),
        "test_rows": len(test_rows),
        "train_scenarios": len({row["scenario_id"] for row in train_rows}),
        "test_scenarios": len({row["scenario_id"] for row in test_rows}),
        "epochs": epochs,
        "model": "standardized one-hidden-layer MLP (10 tanh units; stdlib only)",
        "synthetic_only": True,
    })

    predictions_path = output_dir / "segment_predictions.csv"
    with predictions_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["scenario_id", "segment_id", "flood_exposed_true", "predicted_probability", "predicted_label"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row, probability in zip(test_rows, probabilities):
            writer.writerow({
                "scenario_id": row["scenario_id"],
                "segment_id": row["segment_id"],
                "flood_exposed_true": int(row["flood_exposed"]),
                "predicted_probability": "{:.8f}".format(probability),
                "predicted_label": int(probability >= 0.5),
            })

    accessibility_rows: List[Dict[str, float]] = []
    for graph_index in range(12):
        edges, node_count, hospitals, demand_nodes = build_grid_scenario(seed + 1000 + graph_index)
        edge_rows = [edge[3] for edge in edges]
        edge_probabilities = model.predict_proba(edge_rows)
        for threshold in thresholds:
            record = accessibility_record(
                edges, node_count, hospitals, demand_nodes, edge_probabilities, threshold=threshold
            )
            record["graph_scenario"] = graph_index
            record["threshold"] = threshold
            accessibility_rows.append(record)

    accessibility_path = output_dir / "accessibility_scenarios.csv"
    with accessibility_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = list(accessibility_rows[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(accessibility_rows)

    accessibility_summary = {}
    for threshold in thresholds:
        matching = [row for row in accessibility_rows if row["threshold"] == threshold]
        accessibility_summary["{:.2f}".format(threshold)] = {
            key: sum(row[key] for row in matching) / len(matching)
            for key in (
                "baseline_access_fraction",
                "oracle_access_fraction",
                "predicted_access_fraction",
                "exposure_precision",
                "exposure_recall",
            )
        }
    metrics["synthetic_graph_accessibility_mean_by_threshold"] = accessibility_summary
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    summary = [
        "# FloodLink-PK experiment summary",
        "",
        "This run uses generated synthetic road-link scenarios only. It is a software and protocol smoke-test, not empirical evidence about Pakistan roads.",
        "",
        "## Grouped hold-out classification metrics",
        "",
    ]
    for key in ("n", "positive_rate", "accuracy", "precision", "recall", "f1", "roc_auc", "brier_score", "expected_calibration_error_10_bins"):
        summary.append("- **{}:** {:.4f}".format(key, metrics[key]))
    summary.extend(["", "## Threshold sensitivity", "", "See `threshold_sensitivity.csv` for classification metrics at thresholds 0.25, 0.35, 0.50 and 0.65.", "", "## Synthetic graph accessibility means", ""])
    for threshold, values in accessibility_summary.items():
        summary.append("- **Threshold {}:** predicted access {:.4f}; oracle access {:.4f}; exposure recall {:.4f}".format(
            threshold, values["predicted_access_fraction"], values["oracle_access_fraction"], values["exposure_recall"]
        ))
    summary.extend([
        "",
        "## Interpretation boundary",
        "",
        "Graph edges marked exposed are treated as unavailable in this simulation. Satellite flood exposure is not equivalent to a verified road closure; real-world accessibility claims require dated closure, passability, or travel-time observations.",
        "",
    ])
    (output_dir / "summary.md").write_text("\n".join(summary), encoding="utf-8")
    return metrics
