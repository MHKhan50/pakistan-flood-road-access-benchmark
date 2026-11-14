# FloodLink-PK

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24229218.svg)](https://doi.org/10.5281/zenodo.24229218)

**FloodLink-PK: A Pakistan Flood-Exposure and Emergency Road-Access Research Benchmark**  
Version: `0.1.0` · Release date: `2026-11-09` · Python: `3.9+` · Runtime dependencies: none

## Research problem

Pakistan's 2022 monsoon floods caused major transport and communications damage. The World Bank's Post-Disaster Needs Assessment estimated USD 3.3 billion in damage to transport and communications; Sindh accounted for close to 70% of total national damages and losses. UNOSAT's 31 August 2022 satellite assessment reported approximately 11,300 km² of detected floodwater in its analysed Sindh area and around 4.6 million people potentially exposed or living close to flooded areas. UNOSAT explicitly described that estimate as preliminary and not field-validated.

FloodLink-PK studies a downstream question that is different from flood segmentation itself:

> Can satellite-observed flood exposure and open geospatial covariates support calibrated road-link exposure estimates, and how sensitive are emergency healthcare accessibility estimates to uncertainty in those link predictions?

The proposed real-world study area is flood-affected Sindh, with a later extension to southern Punjab and Balochistan. The initial event window is the 2022 monsoon flood, because an open Pakistan-specific Sentinel-1 flood-map dataset is available from TU Wien for 10 August–23 September 2022.

## What this release contains

This is a reproducible research scaffold, not a completed Pakistan field study.

- A deterministic synthetic road-link scenario generator.
- A dependency-free, one-hidden-layer multilayer perceptron (MLP) for link-level flood-exposure classification.
- Scenario-grouped train/test splitting to reduce spatial/event leakage.
- Classification and probability-quality metrics: precision, recall, F1, ROC-AUC, Brier score and 10-bin expected calibration error.
- A small synthetic road-graph experiment comparing baseline, oracle-exposure and predicted-exposure accessibility.
- CSV schema validation for a future real-data feature table.
- Tests, methodology, data dictionary, real-data protocol, limitations and citation metadata.

No Pakistan road, hospital, population or flood raster is bundled. The synthetic generator is only for checking the code and experimental protocol. Its output must not be described as observed flood data or evidence of model performance in Pakistan.

## Quick start (Mac / Python 3.9+)

```bash
export PYTHONPATH=src
python -m unittest discover -s tests -v
python -m floodlink_pk.cli generate --output data/synthetic_segments.csv --scenarios 80 --segments-per-scenario 50 --seed 17
python -m floodlink_pk.cli experiment --output-dir outputs --seed 17
```

The default generator creates 4,000 synthetic road-link rows across 80 scenarios. The experiment holds out complete scenarios rather than randomly splitting individual links.

## CLI

```bash
# Generate a synthetic link table
PYTHONPATH=src python -m floodlink_pk.cli generate \
  --output data/synthetic_segments.csv \
  --scenarios 80 --segments-per-scenario 50 --seed 17

# Run the grouped MLP and synthetic graph-access experiment
PYTHONPATH=src python -m floodlink_pk.cli experiment \
  --output-dir outputs --seed 17 --epochs 55

# Check the schema of a future real-data CSV
PYTHONPATH=src python -m floodlink_pk.cli validate-real-data \
  --input path/to/real_road_segments.csv
```

## Research boundary and interpretation

The model target in the proposed real-data study is **satellite-observed flood exposure of a road segment**, not verified road closure. A road intersecting a flood polygon is not necessarily impassable. The graph experiment therefore makes an explicit simulation assumption: exposed links are treated as unavailable. This is a stress-test assumption, not a statement about actual road passability.

A defensible Pakistan result requires time-aligned satellite masks, road geometry, elevation, rainfall, soil-moisture covariates, population grids and healthcare-facility locations, plus independent observations of road closure/passability or travel time. The open sources identified in `docs/SOURCES.md` provide much of the geospatial foundation, but no national, time-stamped, independently verified road-closure or ambulance-travel-time dataset was identified for this release. Until such labels are secured, accessibility outputs must be presented as modelled scenarios rather than measured service disruption.

## Repository structure

```text
src/floodlink_pk/       Synthetic data, MLP, metrics, graph and CLI
 tests/                 Standard-library unit tests
 docs/                  Methodology, data dictionary, sources, limitations and real-data protocol
 data/templates/        Empty schema template for future observed road-link data
 outputs/               Created locally by the experiment command
```

## Reproducibility

- All random generators accept explicit seeds.
- Training and test sets are separated by `scenario_id`.
- The MLP is implemented using the Python standard library; no GPU is required.
- The generated data are synthetic and reproducible, but not calibrated to a particular district or flood event.
- Store raw source data outside this repository and record exact product version, acquisition date, CRS, processing steps and checksums before analysis.

## Licensing

The project code is released under the MIT License. External datasets retain their own terms. In particular, OpenStreetMap-derived databases carry ODbL obligations; TU Wien's Pakistan 2022 flood-map dataset is CC BY 4.0; WorldPop and ESA WorldCover products have their own attribution requirements. Do not relicense source data under this repository's MIT license. See `docs/SOURCES.md` and `docs/REAL_DATA_PROTOCOL.md`.

## Citation

Cite this software with the metadata in `CITATION.cff` (DOI: [10.5281/zenodo.24229218](https://doi.org/10.5281/zenodo.24229218)). No peer-reviewed publication is claimed for this version. Cite the source datasets and studies separately as listed in `docs/SOURCES.md`.
