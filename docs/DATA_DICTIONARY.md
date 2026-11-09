# Data dictionary

The generated CSV contains one synthetic road-link observation per row. The schema is also the required input format for `validate-real-data`, although the latter checks only syntax and value types.

| Column | Type | Unit / allowed values | Definition |
|---|---|---|---|
| `segment_id` | string | Unique within a scenario | Stable synthetic road-link identifier. For real data, retain OSM way/segment identifiers and a deterministic segment key. |
| `scenario_id` | string | Event/date or synthetic scenario key | Identifies the shared event/time context. Must be used for grouped splitting. |
| `elevation_m` | float | metres | Elevation sampled along the segment. Synthetic values are sampled from 0.5–38 m; real values should come from a documented DEM. |
| `slope_pct` | float | percent | Local slope summary along the segment. Synthetic values are sampled from 0–8%. |
| `distance_to_river_km` | float | kilometres | Minimum distance to a mapped river/waterway. Synthetic values are sampled from 0.05–12 km. |
| `rainfall_24h_mm` | float | millimetres | Precipitation accumulated over the 24 hours preceding the observation time. |
| `rainfall_72h_mm` | float | millimetres | Precipitation accumulated over the 72 hours preceding the observation time. |
| `soil_moisture_fraction` | float | fraction, nominally 0–1 | Pre-event surface soil-moisture estimate. Preserve source quality flags in a real feature table. |
| `road_class_code` | integer-like float | 0–4 | Synthetic mapping: 0 motorway, 1 trunk, 2 primary, 3 secondary, 4 local/unclassified. Real OSM mapping must be documented and versioned. |
| `bridge_flag` | integer-like float | 0 or 1 | Indicates a bridge tag in the synthetic data. In real data, unknown/missing tags must not automatically be interpreted as 0. |
| `flood_exposed` | integer | 0 or 1 | Synthetic Bernoulli label generated from the documented hazard function. In real data, this should mean satellite-observed flood exposure only—not confirmed closure. |

## Generated experiment outputs

| File | Columns / contents | Meaning |
|---|---|---|
| `segment_predictions.csv` | `scenario_id`, `segment_id`, `flood_exposed_true`, `predicted_probability`, `predicted_label` | MLP predictions for held-out synthetic scenarios. |
| `accessibility_scenarios.csv` | Graph scenario, road-link counts, baseline/oracle/predicted access fractions, exposure precision/recall | Simulated grid-network results. Not observed Pakistan road accessibility. |
| `metrics.json` | Classification metrics, split counts, seed, model description, synthetic graph summary | Machine-readable experiment record. |
| `summary.md` | Human-readable metrics and interpretation boundary | Compact run summary. |
