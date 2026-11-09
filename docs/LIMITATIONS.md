# Limitations and threats to validity

1. **Synthetic-only results in v0.1.0.** The generated rows and grid networks are artificial. Any metric produced by the included experiment is a code/protocol check, not a Pakistan empirical result.
2. **Exposure is not closure.** Satellite-detected water intersecting a road does not establish that the road was closed, impassable or unusable by emergency vehicles.
3. **Missing operational labels.** No national, time-stamped, independently verified road-closure or ambulance travel-time dataset was identified for this release. Without one, operational accessibility claims cannot be validated.
4. **OSM coverage bias.** Rural roads, bridges, clinics and hospitals may be missing or outdated. Missing OSM features are not evidence that infrastructure does not exist.
5. **Scale mismatch.** A 20 m flood mask, 30 m DEM, 0.1° rainfall estimate and approximately 9 km soil-moisture grid represent different spatial supports. Resampling them to road links does not make them equally precise.
6. **Satellite observation limits.** Flood mapping may miss water under vegetation, in built-up areas or in masked/no-data zones. Product-specific quality flags and validation notes must be retained.
7. **Population uncertainty.** Gridded population is modelled, not a household register. Results should be sensitivity-tested across years and population products.
8. **Facility completeness.** Open healthcare points are not a verified national hospital registry. Facility service capacity, operating status and emergency capability are not encoded in this release.
9. **Model scope.** The MLP is a small standard-library baseline. It does not exploit raster texture, temporal sequences, graph message passing or physical hydrodynamic constraints.
10. **Synthetic label mechanism.** The generator uses a known probabilistic formula. Learning it does not establish that the same relationships hold in Sindh or elsewhere in Pakistan.
11. **Network simplification.** The graph experiment uses a small regular grid, two synthetic hospitals and equal-status demand nodes. It does not represent real road hierarchy, traffic, bridges, ferries, congestion, ambulance routing or facility capacity.
12. **Threshold dependence.** Turning predicted exposure probabilities into closed edges requires a decision threshold. Accessibility can change substantially with that threshold; the real study should report a sensitivity curve.

## Claims not supported by this release

Do not claim that FloodLink-PK has measured actual road closures, predicted real emergency travel times, identified the most vulnerable Pakistani districts, improved emergency response, or achieved a validated field performance score. Those claims require real geospatial inputs and independent ground truth.
