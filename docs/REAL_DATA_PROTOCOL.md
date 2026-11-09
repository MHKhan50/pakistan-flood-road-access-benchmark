# Real-data preparation protocol (Pakistan 2022 flood case study)

This release does not automatically download or process the external geospatial sources. They are large, versioned and have distinct licences. Prepare the spatial dataset in a GIS workflow, then export one row per road segment and observation scenario using the schema in `data/templates/real_road_segments_template.csv`.

## Suggested bounded pilot

Start with a limited area in Sindh rather than processing all of Pakistan. Choose one or two districts with a clearly dated flood product and sufficient OSM coverage. Freeze the district boundary, road extract timestamp and flood observation date before feature engineering.

## Spatial processing sequence

1. Download the Pakistan OSM `.osm.pbf` or shapefile extract from Geofabrik. Extract road classes, bridge tags, waterways and candidate hospitals/clinics. Preserve the OSM source timestamp and attribution.
2. Download the relevant TU Wien Pakistan 2022 Sentinel-1 flood mask or UNOSAT product. Use its documented coordinate system and mask semantics. Do not assume masked/no-data pixels mean dry land.
3. Download Copernicus DEM GLO-30 and derive slope using a documented algorithm. Record that GLO-30 is a digital surface model.
4. Download NASA GPM IMERG precipitation and aggregate the preceding 24-hour and 72-hour windows relative to each satellite observation time. Record whether Final, Late or Early Run was used.
5. Download NASA SMAP L3 soil moisture. Apply quality flags and define the temporal matching rule. The product's approximately 9 km grid is coarse relative to individual road segments.
6. Optionally add WorldPop population estimates and map candidate health facilities. Match population year to the event and document facility completeness.
7. Reproject vector layers to an appropriate local metric CRS before measuring distance, length or intersection. Keep the original coordinates and transformation metadata.
8. Split long roads into reproducible segments (for example, fixed-length segments) while preserving source way IDs and segment ordering.
9. For each dated scenario, calculate the fraction of each road segment intersecting the flood mask. Keep the continuous intersection fraction in the source table; derive `flood_exposed` only using a pre-registered threshold.
10. Export the required columns in the template. Unknown feature values should be represented and handled explicitly in a future schema revision; do not silently convert unknown to zero.

## Critical label distinction

A road segment that intersects a satellite flood mask is labelled `flood_exposed`, not `closed`. The model can estimate the probability of observed flood exposure. A separate dataset is needed to learn passability or closure. If no independent closure/travel-time observations can be acquired, network edge removal is only a sensitivity scenario.

## Validation and split design

- Hold out entire dates/events for temporal transfer.
- Hold out entire districts or spatial blocks for geographic transfer.
- Avoid placing adjacent segments from the same road corridor in both training and test sets.
- Validate satellite labels against independent imagery, field reports or another flood product where possible.
- Validate OSM hospitals against provincial health department facility lists.
- Validate the population-weighted accessibility result against known service locations, observed travel times or emergency-response logs.
- Report the number and share of unmatched road links, missing features, masked satellite pixels and uncertain facility locations.

## Reuse and attribution

The source dataset licences remain separate from the MIT licence on the project code. OSM-derived databases may trigger ODbL share-alike requirements. TU Wien's Pakistan 2022 dataset is CC BY 4.0. WorldPop, NASA, Copernicus and ESA terms/attribution should be checked for each exact product and version. Do not include external raster/vector source files in a redistributed ZIP without checking redistribution rights and size.
