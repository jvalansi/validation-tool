# Opportunity sweep

1 niches, 16 clusters (1 excluded by profile or under 3 items).
Score = 100 × share of the niche's pains × (1 + paying share) × fit (clusters with ≥3 items); fit and clustering are Claude judgements.

## 2 newly validated (top-ranked clusters not validated in earlier sweeps)

### 1. Connect a Google Sheet/Excel file and get an auto-updating hosted web map (or AGOL layer sync) with pop-ups and change history.  (gis-surveying, score 12.7)
- Pain: Teams keep data in Excel/Google Sheets/OneDrive and re-import, re-geocode and re-join it into GIS or AGOL layers by hand; there is no live sync, incremental merge or custom pop-up hosting.
- Items 21 · paying signals 17 · fit 0.85
- Validation: **validate further** · competition contested · capture 0.01 · market ~$10,000,000/yr
  - risk: Esri can close the gap natively (Data Pipelines, scheduled Sheets refresh), and it already owns the search results with 60% vendor share, nearly all esri.com hosts
  - risk: Generic no-code map tools (iipmaps, Shareables, get-instamaps) and FME or Power Automate integrations already cover the non-AGOL and enterprise ends
  - risk: No observed price point, and the buyers include many nonprofits and universities with small budgets
  - https://www.reddit.com/r/gis/comments/js7ipm/what_particular_gis_tasks_are_you_most_proud_of/
  - https://www.reddit.com/r/gis/comments/1i2rpeb/talk_to_me_about_fme_data_integration/
  - https://www.reddit.com/r/gis/comments/p0rrto/how_to_tell_if_a_gps_location_is_on_land_or_water/

### 2. Paid QGIS plugin/web API bundling one-click topology repair, centerlines, oriented grids and balanced territory/district generation.  (gis-surveying, score 10.2)
- Pain: There are no easy batch tools for fixing topology gaps and overlaps, closing line gaps, extracting centerlines, simplifying while keeping shared edges, rotated plot grids, territory balancing, contiguous districting and gap-filling.
- Items 22 · paying signals 18 · fit 0.65
- Validation: **validate further** · competition contested · capture 0.01 · market ~$1,000,000/yr
  - risk: Free substitutes already cover parts of the bundle (QGIS Topology Checker and Geometry Checker, GRASS v.clean, the built-in Create Grid, free centerline plugins), so willingness to pay is weak
  - risk: Search results are dominated by plugins.qgis.org and content sites, and the listed 'incumbents' are free directories, not paid vendors, so there is no proven paid demand and discovery is hard
  - risk: Esri ArcGIS users, who are more willing to pay, already have Esri's Redistricting and territory-design tools
  - https://www.reddit.com/r/gis/comments/1gvoqif/i_have_a_shapefile_with_tens_of_thousands_of/
  - https://www.reddit.com/r/gis/comments/1hhv0l4/does_anyone_know_of_a_way_to_create/
  - https://www.reddit.com/r/gis/comments/1pbg3cv/need_to_digitize_a_group_of_lines_into_one_solid/

## Next 20 not yet validated

- 9.7 · gis-surveying · Template-driven map-book generator that rebuilds styled per-site PDFs/SVGs from data changes with design-grade output.
- 9.3 · gis-surveying · AI GIS copilot that explains geoprocessing errors and repairs broken/portable QGIS-ArcGIS project packages.
- 8.0 · gis-surveying · Upload a scanned map, PDF plan or legal description and get georeferenced, vectorized GeoJSON/DXF with an auto-detected CRS.
- 7.2 · gis-surveying · Hosted no-code pipeline: draw an AOI and date range and get cloud-free, normalized composites, indices or LST as COGs via UI/API.
- 6.6 · gis-surveying · Lightweight survey-firm job board: map-indexed job history, crew/truck/instrument scheduling, and a mobile field book.
- 6.1 · gis-surveying · Searchable archive/mirror of public ArcGIS REST and OGC services with change alerts, field dictionaries and one-click export.
- 5.9 · gis-surveying · Upload a messy spreadsheet; the tool detects coordinate formats and CRS, geocodes addresses and place names globally, and returns clean points with confidence flags.
- 5.1 · gis-surveying · Drag-drop raster/LiDAR upload that auto-optimizes to COG/COPC, checks NoData, and gives a shareable client viewer link.
- 5.0 · gis-surveying · AI-generated FS practice bank with step-by-step solutions, an adaptive tutor and a calculator-workflow trainer.
- 4.8 · gis-surveying · Web converter between survey/CAD/GIS formats (JobXML, FLD, DXF, LandXML) with transparent least-squares traverse adjustment.
- 4.7 · gis-surveying · One-click hosting for qgis2web/GeoJSON exports with custom domain, embed code and data-update endpoint.
- 3.8 · gis-surveying · Upload imagery and get detected objects or land-cover classes as clean vector polygons, with pretrained models and an accuracy report.
- 3.6 · gis-surveying · Web/QGIS-plugin converter that turns ArcGIS .lyrx/.aprx/.mxd projects and symbology into QGIS projects with a fidelity report.
