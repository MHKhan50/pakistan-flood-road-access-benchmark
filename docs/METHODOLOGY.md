# Methodology and experimental protocol

## 1. Research question

Can open satellite flood observations and open geospatial covariates support calibrated road-link flood-exposure estimates, and how does prediction uncertainty propagate into network-level emergency healthcare accessibility estimates in flood-affected Pakistan?

The initial case study is Sindh during the 2022 monsoon floods. The work is intentionally downstream of flood segmentation: it asks what the observed water extent may imply for a road network and access to healthcare, rather than proposing another generic flood-mask model.

## 2. Candidate research contribution

The candidate contribution is a reproducible, uncertainty-aware bridge between (a) satellite-derived flood exposure at road-link scale and (b) population-weighted access to mapped healthcare facilities. The research should test whether calibrated link-level exposure probabilities produce more reliable accessibility estimates than hard-threshold exposure masks.

This is a research hypothesis, not a novelty or performance claim. Pakistan 2022 flood-mapping studies already exist. The contribution must therefore be distinguished from flood delineation by its road-network and service-access analysis, and the literature review must search for comparable flood-aware accessibility studies before making a novelty claim.

## 3. Target definition

Primary target:

- `flood_exposed = 1`: a road segment intersects a dated, quality-screened satellite flood polygon or flood-mask pixel set.
- `flood_exposed = 0`: a road segment does not intersect the observed flood extent for that date and study area.

This is an exposure proxy. It is not a verified closure label. The distinction must be retained in variable names, figures and paper language.

Secondary network outcome:

- Population-weighted share of demand locations that remain connected to at least one mapped hospital/clinic under a stated link-removal scenario.
- Report multiple thresholds and probabilistic edge-removal strategies rather than presenting a single accessibility number as ground truth.

## 4. Candidate input features

| Feature | Proposed construction | Candidate source |
|---|---|---|
| `elevation_m` | Median elevation sampled along the road segment | Copernicus DEM GLO-30 |
| `slope_pct` | Median local slope derived from elevation | Copernicus DEM GLO-30 |
| `distance_to_river_km` | Minimum geodesic distance from segment to mapped river/waterway | OpenStreetMap waterways |
| `rainfall_24h_mm` | Accumulated precipitation for the 24 hours preceding the flood observation | NASA GPM IMERG |
| `rainfall_72h_mm` | Accumulated precipitation for the preceding 72 hours | NASA GPM IMERG |
| `soil_moisture_fraction` | Nearest valid pre-event soil-moisture observation, with quality flags | NASA SMAP L3 |
| `road_class_code` | Explicit mapping from OSM `highway` values to ordinal categories | OpenStreetMap roads |
| `bridge_flag` | OSM `bridge` tag converted to 0/1, with unknown retained separately in a real study | OpenStreetMap roads |

The feature set is deliberately modest. Resolution mismatch is substantial: the flood masks may be around 20 m, while SMAP soil-moisture observations are much coarser (about 9 km for the cited L3 product). Do not interpret coarse environmental pixels as segment-scale measurements.

## 5. Synthetic benchmark protocol in this release

1. Generate shared rainfall and soil-moisture conditions for each synthetic scenario.
2. Sample local road-link features within each scenario.
3. Generate probabilistic exposure labels from the documented hazard function in `src/floodlink_pk/data.py`.
4. Split by complete `scenario_id` groups. Links from one scenario cannot appear in both training and test sets.
5. Fit feature standardisation on training rows only.
6. Train a one-hidden-layer MLP using stochastic gradient descent.
7. Evaluate classification and probability quality on held-out scenarios.
8. Generate independent synthetic grid networks, infer edge exposure probabilities and compare no-closure, oracle-exposure and predicted-exposure accessibility.

The synthetic label generator is intentionally transparent. High performance on these generated rows only demonstrates that the software pipeline can learn patterns from its own simulator. It does not validate the method on Pakistan's flood events.

## 6. Required real-data validation protocol

1. Select a bounded study area (recommended first pass: one or two flood-affected Sindh districts) and exact observation dates.
2. Download the TU Wien Pakistan 2022 Sentinel-1 flood product or the relevant UNOSAT dated flood polygon. Record the product, acquisition time, version, coordinate reference system and quality mask.
3. Download a dated OpenStreetMap road extract. Split long ways into stable analysis segments; preserve OSM IDs and snapshot date.
4. Derive flood-exposure labels by intersecting each road segment with the satellite flood mask after reprojection to a suitable local metric CRS. Record intersection length and fraction, not just a binary label.
5. Sample elevation/slope from Copernicus DEM; derive river distance from mapped waterways; aggregate GPM rainfall and SMAP soil moisture using explicit time windows and quality flags.
6. Create a spatially and temporally grouped hold-out. Do not randomly split neighbouring road segments from the same flood event across train and test.
7. Obtain mapped health facilities and population estimates. Document completeness, source date, licensing and positional uncertainty.
8. Seek independent road closure/passability records, emergency dispatch records, field reports or observed travel times. If none are available, stop short of claiming measured accessibility loss.
9. Compare at least: logistic regression, the MLP in this repository, a tree-based baseline, a spatially naive baseline and a calibrated probability baseline.
10. Report calibration, class imbalance, spatial transfer, temporal transfer, sensitivity to exposure threshold, and uncertainty in facility/population coverage.

## 7. Evaluation metrics

### Link-level classification

- Precision, recall, F1 and ROC-AUC.
- Brier score and expected calibration error (10 equal-width bins).
- Confusion matrix and class prevalence by district, date and road class.

### Network-level accessibility

- Share of population-weighted demand cells connected to at least one mapped healthcare facility.
- Change relative to the no-flood network.
- Difference between predicted-exposure and oracle-exposure scenarios.
- Sensitivity to link-closure threshold, facility completeness and population-grid resolution.

Do not use ROC-AUC alone: the operational decision is affected by calibration and false closure estimates.

## 8. Reproducibility controls

- Use fixed seeds and preserve the exact configuration.
- Keep event dates grouped between train and test for temporal generalisation tests.
- Keep entire districts or spatial blocks out for geographic transfer tests.
- Store raw data checksums and processing scripts.
- Record software versions and the exact OSM snapshot timestamp.
- Publish the data dictionary and source-specific licences with any derived dataset.
