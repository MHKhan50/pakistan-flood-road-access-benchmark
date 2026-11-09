# Pakistan context and candidate source datasets

All sources below are external to this code package. Check the current product version, geographic coverage, terms and acquisition dates before use.

## Pakistan-specific problem evidence

1. **World Bank / Government-led Pakistan Floods 2022 Post-Disaster Needs Assessment.** The World Bank reports that the 2022 floods affected 33 million people, that Sindh was the worst-affected province with close to 70% of total damages and losses, and that transport and communications suffered an estimated USD 3.3 billion in damage. This establishes the transport-resilience problem; it does not provide road-by-road closure labels.  
   https://www.worldbank.org/en/news/press-release/2022/10/28/pakistan-flood-damages-and-economic-losses-over-usd-30-billion-and-reconstruction-needs-over-usd-16-billion-new-assessme

2. **UNOSAT satellite assessment for Sindh, 31 August 2022.** UNOSAT reported about 11,300 km² of detected surface water within its analysed area of approximately 25,000 km², and around 4.6 million people potentially exposed or living close to flooded areas. UNOSAT marks this as preliminary and not field-validated.  
   https://unosat.org/products/3348

3. **World Bank Sindh Flood Emergency Rehabilitation Project factsheet.** Describes the effect of the 2022 floods on Sindh's transport, agriculture and public infrastructure, and the rehabilitation programme.  
   https://www.worldbank.org/en/news/factsheet/2022/12/19/factsheet-sindh-flood-emergency-rehabilitation-project

## Open geospatial datasets

1. **TU Wien Research Data — Sentinel-1 based analysis of the Pakistan Flood in 2022.** Pakistan-specific flood maps for the southern part of the country, covering 10 August–23 September 2022. The record describes 20 m flood-mask tiles, flood-frequency and first-detection rasters, and CC BY 4.0 reuse. The published archive is approximately 457.6 MiB. This is the strongest directly relevant open event dataset identified for the proposed first case study.  
   Dataset DOI: https://doi.org/10.48436/zvvmh-nan78  
   Landing page: https://researchdata.tuwien.ac.at/records/zvvmh-nan78

2. **UNOSAT Pakistan flood products.** Dated satellite-detected flood extents are available with downloadable GIS formats on individual product pages, including Sindh and national assessments. Read each product's preliminary/validation caveats.  
   Sindh, 31 August 2022: https://unosat.org/products/3348  
   Pakistan, July–August 2022 cumulative extent: https://unosat.org/products/3346

3. **OpenStreetMap / Geofabrik Pakistan extract.** Roads, bridges, waterways and mapped healthcare points can be derived from an OSM snapshot. Geofabrik provides free regional extracts, commonly updated daily. OSM data are licensed under ODbL 1.0; attribution and share-alike obligations can apply to derived databases. OSM completeness is uneven and facilities must be independently checked.  
   Geofabrik downloads: https://download.geofabrik.de/asia/pakistan.html  
   Geofabrik download and licensing notes: https://www.geofabrik.de/data/download.html  
   OSM copyright and licence: https://www.openstreetmap.org/copyright

4. **Copernicus DEM GLO-30.** Global 30 m digital surface model suitable for deriving approximate elevation and slope covariates. It is a DSM, so buildings and vegetation affect surface elevations; it is not a bare-earth terrain model.  
   https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM

5. **NASA GPM IMERG.** Global precipitation estimates at 0.1° spatial resolution, with half-hourly and daily products. The daily Final product is research-oriented and has a latency of roughly 3.5 months. It can support retrospective 2022 rainfall accumulation features; it is not a local rain-gauge replacement.  
   https://gpm.nasa.gov/data/imerg  
   NASA GPM data directory: https://gpm.nasa.gov/data/directory

6. **NASA SMAP L3 soil moisture.** Global daily 9 km soil-moisture product. Its spatial resolution is much coarser than a road segment or 20 m flood mask; use as a contextual covariate, not as segment-scale ground truth.  
   DOI: https://doi.org/10.5067/7KKNQ5UURM2W  
   NASA catalogue: https://catalog.data.gov/dataset/smap-l3-radar-radiometer-global-daily-9-km-ease-grid-soil-moisture-v003

7. **WorldPop population grids.** WorldPop provides gridded population estimates, including global 100 m products for 2000–2020 and country-specific products through WOPR. Match population year to the flood event where possible, and preserve the model/version and uncertainty information.  
   Global 2000–2020 catalogue: https://hub.worldpop.org/Global1_2000-2020  
   WOPR: https://wopr.worldpop.org/

8. **ESA WorldCover.** Global land-cover maps at 10 m for 2020 and 2021, provided under CC BY 4.0. Optional for built-up/land-cover context; not required by the current synthetic baseline.  
   https://esa-worldcover.org/en/data-access

## Data gaps that affect the research claim

- No national, time-stamped, independently verified road-closure/passability dataset or ambulance travel-time dataset was identified for this release.
- OSM road and hospital coverage may be incomplete, particularly in rural and flood-affected locations.
- Satellite flood extent is an observation of surface water, not proof that a road was closed or impassable.
- UNOSAT exposure/population figures are preliminary estimates; do not treat them as exact census counts.
- Population rasters, SMAP, GPM and DEM have different spatial and temporal resolutions. Resampling does not create new information.

The project therefore provides a synthetic benchmark and a real-data protocol. It does not ship a prepared, labelled Pakistan road-access dataset.
