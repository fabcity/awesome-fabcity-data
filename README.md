# awesome-fabcity-data

> A curated, network-maintained inventory of open data sources for measuring distributed production at every scale — from a single fab lab to the planet.

Maintained by the **Fab City** network. Organised by the [**Full Stack Metrics Framework**](#the-taxonomy): four pillars — Environmental, Social, Economic, Governance — across five scales — Planet, Bioregion, Region, City, Community.

This list exists because the gap between Earth-scale instruments (Copernicus, NOAA, Aurora) and community-scale instruments (Smart Citizen, repair cafés, fab-lab logs) is *not* well covered by general-purpose data registries. Awesome lists like [`awesome-public-datasets`](https://github.com/awesomedata/awesome-public-datasets) carry the planet end and the research-archive end; community-tier instruments and material-flow accounting fall through. This list fills that gap, from the perspective of people who actually deploy the instruments.

It is opinionated. Inclusion means a member of the network has either *used* the source in production or *audited* it as fit-for-purpose for a fab-lab or partner-city use case. We are not aiming for completeness — we are aiming for honest, current, navigable.

---

## How to read this list

Every entry carries:

| Field | What it tells you |
| --- | --- |
| **Status** | `candidate` · `live` · `stale` · `paywalled` · `deprecated` · `planned` — `candidate` means verified but not yet read by anyone for a real place; `live` means a review file or an `adapter` exists. See [CONTRIBUTING](CONTRIBUTING.md#criterion-3-is-two-states). |
| **Pillar** | environmental · social · economic · governance |
| **Scale** | planet · bioregion · region · city · community |
| **License** | SPDX where possible (CC-BY-4.0, ODbL-1.0, CC0, MIT) |
| **Pilots** | which PLANETAI pilots have non-trivial coverage |
| **Wired** | whether a connector is currently live in the [PLANETAI observatory](https://planetai.fab.city/observatory/) |
| **Reviewed** | `reviewed AB 2026-09` — initials and month of the newest usable review in [`reviews/`](reviews/) |

Entries live as YAML files under `data/{pillar}/{scale}/{slug}.yaml` — that's the source of truth. This README is generated from them by `scripts/build_readme.py`.

## The taxonomy

The four pillars × five scales come from the **Full Stack Metrics Framework** [Vivanco 2024, 2025], which operationalises *The Fab City Full Stack* [Diez, Niaros, Ferro 2024]. They are not a replacement for ESG, SDG, or doughnut economics — they are a way to organise *where measurement happens* in a distributed-production network.

```
                              ┌──────────────┐
                              │   Planet     │  Earth-system models, planetary boundaries
                              ├──────────────┤
                              │  Bioregion   │  Watersheds, food sheds, multi-city basins
                              ├──────────────┤
                              │   Region     │  Multi-city, state, province, autonomy
                              ├──────────────┤
                              │    City      │  Municipal jurisdiction
                              ├──────────────┤
                              │  Community   │  Neighbourhood, fab-lab shed, household
                              └──────────────┘
            Environmental │ Social │ Economic │ Governance
```

A dataset can be relevant at multiple scales. We classify by where its **strongest signal** lives — the resolution at which it actually reports.

## Pilots

Four bioregional pilots run by the [PLANETAI](https://planetai.fab.city/) program inside Fab City. Pilot tags on entries indicate non-trivial coverage:

- `barcelona` — Spain / Catalonia (Open Data BCN, Generalitat, Mercabarna, IAAC, Fab Lab BCN)
- `boston` — Massachusetts / New England (Analyze Boston, MassGIS, MIT CBA, Fab Foundation)
- `santiago` — Chile (datos.gob.cl, ChileCompra, UC Chile, Núcleo Milenio FAIR, CENIA)
- `bali` — Indonesia (Bali Satu Data, IT Del, CAST Foundation, Fab Lab Bali, MDG)
- `global` — meaningful planetary or cross-pilot coverage

---

<!-- BEGIN GENERATED -->

## Environmental

### Planet

- **[GLODAP v2.2023 — Global Ocean Data Analysis Project](https://glodap.info/index.php/merged-and-adjusted-data-product-v2-2023/)** — ✅ `live` · `Website content CC-BY-4.0; the data product is gated behind a Data Use Statement — data license UNCONFIRMED` · _★_
  Uniformly calibrated global open-ocean data product of inorganic carbon variables including DIC, total alkalinity and pH, merged from research cruises. Maintained by GEOMAR and the ICOS Ocean Thematic Centre, archived at NOAA NCEI.
- **[Google Flood Hub](https://sites.research.google/floods/)** — ✅ `live` · `Google Maps Platform terms (free tier)` · _BLI · BCN · SCL · ★_
  Riverine flood forecasts up to 7 days ahead for ~80 countries including Indonesia, Spain, Chile. Inundation maps + alerts via free public API (rate-limited).
- **[Microsoft Aurora](https://microsoft.github.io/aurora/)** — ✅ `live` · `MIT (model weights); CDS license for ERA5 training inputs` · _★_
  Earth-system foundation model from Microsoft Research. Hourly forecasts to 14 days for atmosphere, ocean wave, and air quality state. Model weights released under MIT.
- **[NASA GISTEMP v4 — surface temperature analysis](https://data.giss.nasa.gov/gistemp/)** — ✅ `live` · `No formal license — acknowledgement expected; credit NASA GISS/GISTEMP` · _★_
  NASA GISS land-ocean surface temperature anomaly analysis. Global, hemispheric and zonal CSV tables plus 2x2 degree gridded NetCDF and Zarr anomaly fields relative to a 1951-1980 baseline.
- **[NASA POWER](https://power.larc.nasa.gov/)** — ✅ `live` · `US Government work (public domain); NASA POWER asks for citation` · _★_ · 🔌 `core:power_climatology`
  NASA Langley's Prediction Of Worldwide Energy Resources: solar and meteorological parameters from MERRA-2 and CERES, hourly to climatology, for any point on Earth since 1981, via a key-free REST API.
- **[NOAA Global Monitoring Laboratory — CO2 trends](https://gml.noaa.gov/ccgg/trends/data.html)** — ✅ `live` · `No formal license — freely available to the public and the scientific community; citation requested` · _★_
  NOAA GML's canonical atmospheric CO2 record: Mauna Loa daily, weekly and monthly means plus the globally averaged marine surface annual mean, from the NOAA cooperative air sampling network.
- **[Open-Meteo](https://open-meteo.com/)** — ✅ `live` · `CC-BY-4.0` · _★_ · 🔌 `core:openmeteo`
  Free weather + climate API with no auth required. Backed by ECMWF + GFS + DWD + KNMI. Hourly forecasts to 14 days, historical reanalysis, climate projections, marine forecasts.
- **[Open-Meteo Air Quality API (Copernicus CAMS)](https://open-meteo.com/en/docs/air-quality-api)** — ✅ `live` · `CC-BY-4.0 (Open-Meteo) with mandatory attribution to CAMS / Copernicus as data provider` · _★_ · 🔌 `core:openmeteo_air`
  Key-free hourly air-quality forecasts and 92 days of history from the Copernicus CAMS global (0.4 deg) and European (0.1 deg) models: PM2.5, PM10, O3, NO2, SO2, CO, dust, aerosol optical depth, UV index, pollen (EU).
- **[UNEP IRP Global Material Flows Database](https://energydata.info/en/dataset/world-unep-irp-global-material-flows-database)** — ✅ `live` · `CC-BY-4.0` · _★_
  UNEP International Resource Panel material flow accounts: domestic extraction, direct trade and material footprint in raw-material equivalents by material category for 200+ countries. Compiled with CSIRO and WU Vienna.

### Bioregion

- **[Caravan — large-sample hydrology](https://github.com/kratzert/Caravan)** — ✅ `live` · `CC-BY-4.0` · _BLI · BCN · BOS · SCL_
  Community-curated large-sample hydrology benchmark dataset. Daily streamflow + meteorological forcing for ~7,000 catchments globally. Underlies most modern deep-learning hydrology research.
- **[ESA WorldCover](https://esa-worldcover.org/en/data-access)** — ✅ `live` · `CC-BY-4.0` · _★_
  ESA's 10 m global land cover map from Sentinel-1/2 with 11 classes including tree cover, shrubland, grassland, cropland and wetland. Delivered as Cloud-Optimized GeoTIFFs on a 1-degree grid.
- **[GBIF — Global Biodiversity Information Facility](https://www.gbif.org/)** — ✅ `live` · `CC-BY-4.0 (most records); some CC0; some CC-BY-NC` · _★_
  Aggregated species occurrence records from 2,000+ data publishers. ~3 billion records globally with a public REST API and bulk download via DOI. The de facto biodiversity backbone.
- **[Global Footprint Network — National Footprint & Biocapacity Accounts](https://www.footprintnetwork.org/licenses/public-data-package-free/)** — ✅ `live` · `CC-BY-SA-4.0 (registration and source acknowledgement required)` · _★_
  Free public data package of Ecological Footprint and biocapacity accounts for 195+ countries, run by Global Footprint Network. Carries per-capita gha footprint and biocapacity, land-type breakdown and data- quality scores.
- **[Global Forest Watch Data API — Hansen/UMD tree cover](https://data-api.globalforestwatch.org/datasets)** — ✅ `live` · `CC-BY-4.0 (per-dataset; other catalogue layers vary, several are non-commercial)` · _★_
  WRI's Global Forest Watch data API serving the Hansen/UMD 30 m global forest change products - annual tree cover loss and 2000/2010 tree cover density - plus a large catalogue of third-party layers.
- **[HydroSHEDS — HydroBASINS](https://www.hydrosheds.org/products/hydrobasins)** — ✅ `live` · `HydroSHEDS license — free for scientific, educational and commercial use with attribution` · _★_
  Global vector polygons of sub-basin boundaries, hierarchically nested across 12 levels with Pfafstetter coding and upstream/downstream topology. About 1.0 million sub-basin polygons covering 135 million square kilometres.
- **[ISRIC SoilGrids 2.0](https://www.isric.org/explore/soilgrids)** — ✅ `live` · `CC-BY-4.0` · _★_
  ISRIC World Soil Information's global digital soil mapping system. Machine-learned predictions of pH, organic carbon, bulk density, nitrogen, CEC and texture at 250 m across six standard depths.
- **[Open-Meteo Marine Weather API](https://open-meteo.com/en/docs/marine-weather-api)** — ✅ `live` · `CC-BY-4.0 (Open-Meteo) with mandatory attribution to the model providers (DWD, ECMWF, Meteo-France, NCEP)` · _BLI · BCN · BOS · SCL · ★_ · 🔌 `pack:coast`
  Key-free hourly marine forecasts to 16 days: wave height, period and direction (wind, swell, secondary swell), sea surface temperature, sea level with tides, ocean current. Backed by MFWAM, ECMWF WAM, GFS Wave, EWAM.
- **[UNEP GEMS/Water Global Freshwater Quality Archive](https://zenodo.org/records/14230628)** — ✅ `live` · `CC-BY-4.0 (open archive; additional data available under CC-BY-NC-4.0)` · _★_
  UNEP GEMS/Water's global freshwater quality archive: over 20 million measurements across 608 parameters from 13,660 monitoring stations. Hosted by the International Centre for Water Resources and Global Change at the German Federal Institute of Hydrology.
- **[WRI Aqueduct 4.0 — Global Water Risk Atlas](https://www.wri.org/data/aqueduct-global-maps-40-data)** — ✅ `live` · `Creative Commons (variant not specified on the source page - verify before publishing derived values)` · _★_
  WRI's global water risk framework: 13 baseline annual and 3 baseline monthly indicators covering water stress, depletion, variability and quality, plus CMIP6-driven projections for 2030, 2050 and 2080.

### Region

- **[Bhutan 186 Watershed Boundaries (NSDI)](https://nsdi.systems.gov.bt/portal/sharing/rest/content/items/565e1b5cac0046e9b2f64b76d8c4bca0?f=json)** — ✅ `live` · `Open (Geo-Information Policy 2018 §6.3.1 open tier: "Open data shall be openly and freely accessible")`
  The 186-unit watershed delineation of Bhutan published by the Department of Water. Finer-grained than basin boundaries and usable as a sub-dzongkhag environmental reporting unit.
- **[Bhutan Land Use Land Cover 2020 (NSDI)](https://nsdi.systems.gov.bt/portal/sharing/rest/content/items/e9db104416b74226839b72b226cb3ae6?f=json)** — ✅ `live` · `Open (Geo-Information Policy 2018 §6.3.1 open tier: "Open data shall be openly and freely accessible")`
  National land use and land cover for Bhutan derived from Sentinel-2 imagery with random-forest classification, 87% overall accuracy, showing 69% forest cover. Published by the National Land Commission Secretariat.
- **[Bhutan National Solar Energy Roadmap Sites (NSDI)](https://nsdi.systems.gov.bt/portal/sharing/rest/content/items/3fdb11bd00d645ea9cd92ffdf708d4ce?f=json)** — ✅ `live` · `Open (Geo-Information Policy 2018 §6.3.1 open tier: "Open data shall be openly and freely accessible")`
  Candidate and planned solar generation sites identified under Bhutan's National Solar Energy Roadmap, published by the Department of Energy. Points, so this is a renewable-capacity siting layer.
- **[Bhutan River Basin Boundaries (NSDI)](https://nsdi.systems.gov.bt/portal/sharing/rest/content/items/547f76f1a5d54c5a9ddd6536baad7dd2?f=json)** — ✅ `live` · `Open (Geo-Information Policy 2018 §6.3.1 open tier: "Open data shall be openly and freely accessible")`
  River basin boundary polygons for Bhutan published by the Department of Water on the national spatial data infrastructure. Provides the hydrological regional frame for water-resource indicators.
- **[BMKG Prakiraan Cuaca (Indonesia public weather forecast API)](https://data.bmkg.go.id/prakiraan-cuaca/)** — ✅ `live` · `BMKG terms of use; attribution "Sumber: BMKG" mandatory; repackaging into third-party applications and commercial use require written permission from BMKG (Ketentuan Penggunaan s.9.3)` · _BLI_ · 🔌 `pack:forecast`
  Indonesia's meteorological agency publishes a three-day, 3-hourly forecast for every kelurahan and desa in the country, keyed by the level-IV administrative code, refreshed twice daily. Key-free JSON, 60 req/min/IP.
- **[GeoStat Environment Statistics (PxWeb) - Georgia](https://pc-axis.geostat.ge/PXWeb/pxweb/en/Database/Environment%20Statistics)** — ✅ `live` · `GeoStat open terms of use - download, use, adapt, modify, create derivative works, disseminate and share for any purpose including commercial, without prior permission; attribution to GEOSTAT required`
  Georgia's national environment statistics - air pollution, waste, water resources, forests, protected areas and environmental-economic accounts - queryable through a live PxWeb REST API run by GeoStat.
- **[Occitanie — Panorama des énergies renouvelables](https://www.data.gouv.fr/datasets/panorama-des-energies-renouvelables)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Time series of renewable energy production in Occitanie, 2008-2024, compiled by the region from RTE, SDeS and ENEDIS sources. Fills the regional energy-mix cell of the FCI environmental pillar.

### City

- **[AlphaEarth Foundations - Satellite Embedding V1 (Google DeepMind)](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL)** — ✅ `live` · `CC-BY-4.0 (attribution required)` · _★_ · 🔌 `pack:earth`
  Annual 10 m global embeddings (64 dimensions per pixel) learned from Sentinel-1/2, Landsat, GEDI, ERA5 and more, 2017-2024. A general-purpose land representation: change, similarity and classification without labels.
- **[ARSO hourly air quality measurements (Slovenia)](http://www.arso.gov.si/xml/zrak/ones_zrak_urni_podatki_zadnji.xml)** — ✅ `live` · `CC-BY-4.0`
  Hourly XML feed from Slovenia's national air quality network - 24 stations, three of them in Ljubljana, reporting PM10, PM2.5, NO2, O3, SO2, benzene, CO and NOx with coordinates and elevation.
- **[Boston - Greenhouse Gas Emissions inventory](https://data.boston.gov/dataset/greenhouse-gas-emissions)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  Annual citywide greenhouse gas inventory for Boston covering 2005 to 2021, published as three CSVs: community-wide emissions, local government operations emissions, and local government fuels.
- **[Emissions de GES de la collectivite montrealaise (GPC)](https://donnees.montreal.ca/dataset/emissions-ges-collectivite-montrealaise)** — ✅ `live` · `CC-BY-4.0`
  Community-scale greenhouse gas inventory for Montreal built on the GPC protocol, carrying GPC reference numbers and Scope 1/2/3 across stationary energy, transport, waste, IPPU and AFOLU.
- **[Geoportal Kvaliteta zraka Grada Zagreba](https://data.gov.hr/ckan/dataset/geoportal-kvaliteta-zraka)** — ✅ `live` · `Otvorena dozvola (OD)`
  Inventory of Zagreb's urban air-quality monitoring stations - location, substances measured, operating institution and competent authority - served as CSV, GeoJSON, KML and SHP from the city's ArcGIS Hub.
- **[Google Air Quality API](https://developers.google.com/maps/documentation/air-quality)** — 💲 `paywalled` · `Google Maps Platform terms (free quota tier available)` · _★_
  500m-resolution PM2.5 + AQI grid derived from regulatory stations, satellite, and modelling. Global coverage with hourly updates.
- **[Kamakura Waste and Recycling Open Data (鎌倉市 ごみ・資源オープンデータ)](https://www.city.kamakura.kanagawa.jp/gomi/shigen.html)** — ✅ `live` · `CC-BY-4.0`
  Four CSV series on Kamakura's municipal waste system: incineration tonnage and waste generation split household/commercial, recycling rate, and resource collection volume. The recycling rate series runs FY2010-FY2024, rising 46.5% to 59.8%.
- **[Local authority collected waste management - annual results (England)](https://www.gov.uk/government/statistics/local-authority-collected-waste-management-annual-results)** — ✅ `live` · `Open Government Licence v3.0`
  Per-authority and regional waste tonnage, recycling rates and household waste per person for England, 2024/25 with a back-series to 2012-13, published as ODS spreadsheets from WasteDataFlow returns.
- **[Luchtmeetnet / Landelijk Meetnet Luchtkwaliteit (RIVM)](https://api-docs.luchtmeetnet.nl/)** — ✅ `live` · `CC-BY-4.0`
  The Dutch national air quality monitoring network, run by RIVM with regional environment agencies. Open JSON API serving station metadata and hourly concentrations for NO2, PM10, PM2.5, O3 and more.
- **[OpenAQ](https://openaq.org/)** — ✅ `live` · `CC-BY-4.0` · _BCN · BOS · SCL · BLI · ★_
  Reference-grade air quality aggregator. Pulls from ~10k+ regulatory monitoring stations globally and harmonises to a common schema. Free public API with optional auth for higher rate limits.
- **[RSQA - Indice de la qualite de l'air, temps reel (Montreal)](https://donnees.montreal.ca/dataset/rsqa-indice-qualite-air)** — ✅ `live` · `CC-BY-4.0`
  Hourly air quality index per monitoring station from Montreal's RSQA network, covering SO2, CO, O3, NO2 and PM2.5. Published as a rolling daily CSV, updated about ten minutes past each hour.
- **[Sensor.Community](https://sensor.community/)** — ✅ `live` · `DbCL-1.0` · _BCN · ★_
  Citizen-science air quality sensor network rooted in Germany, active across the EU. ~30k SDS011-based PM sensors with public API and bulk archive download.
- **[Seoul Daily Average Air Environment Information (서울시 기간별 일평균 대기환경 정보)](https://data.seoul.go.kr/dataList/OA-2220/S/1/datasetView.do)** — ⛔ `deprecated` · `공공누리 1유형 : 출처표시 (상업적 이용 및 변경 가능) - KOGL Type 1`
  Daily-average air quality index, PM10, ozone, NO2, CO and SO2 for Seoul, with a series running from 1987 to 2025. The ~38-year depth is exceptional for an urban air-quality record.
- **[Seoul GHG Inventory by Direct/Indirect (서울시 온실가스 인벤토리 직간접별 현황)](https://data.seoul.go.kr/dataList/OA-21082/S/1/datasetView.do)** — ⛔ `deprecated` · `공공누리 1유형 : 출처표시 (상업적 이용 및 변경 가능) - KOGL Type 1`
  Seoul's annual greenhouse gas inventory split by direct and indirect emissions, published by the city's Climate and Environment Bureau. Companion dataset OA-21081 gives the same inventory broken out by sector.
- **[SYKE municipal and regional greenhouse gas emissions (ALas)](https://paastot.hiilineutraalisuomi.fi/)** — ✅ `live` · `CC-BY-4.0`
  Per-municipality and per-region GHG emissions by sector for Finland under the ALas/Hinku model - electricity, heating, transport, industry, agriculture, waste - downloadable as Excel tables. Run by SYKE.
- **[UK local authority and regional greenhouse gas emissions statistics](https://www.gov.uk/government/statistics/uk-local-authority-and-regional-greenhouse-gas-emissions-statistics-2005-to-2024)** — ✅ `live` · `Open Government Licence v3.0`
  Annual territorial GHG emissions for every UK local authority and region, 2005-2024, as an 82.6 MB CSV plus Excel tables. Excludes aviation, shipping, military transport and fluorinated gases.

### Community

- **[AirGradient](https://www.airgradient.com/)** — ✅ `live` · `CC-BY-4.0 (data) + custom open (hardware)` · _★_ · 🔌 `core:airgradient`
  Open-hardware indoor + outdoor air quality monitoring network with public REST API. PM2.5, PM10, CO2, TVOC, NOx, temperature, humidity. ~10k+ devices deployed globally; transparent pricing for the open variant.
- **[Bali Air Dispatch](https://baliairdispatch.com/)** — ✅ `live` · `Public-interest archive; redistribution encouraged with attribution to Bali Air Dispatch and to the originating network named in each row. Upstream readings remain under their networks' terms.` · _BLI_ · 🔌 `core:baliairdispatch`
  Island-wide PM2.5 archive for Bali aggregating eight sensor networks (Nafas, IQAir, PurpleAir, AQICN, OpenAQ, AirGradient, Smart Citizen, Airly) into one key-free, read-only API with raw and humidity-corrected values.
- **[iNaturalist](https://www.inaturalist.org/)** — ✅ `live` · `CC-BY-NC (default per-observation; varies by uploader)` · _★_
  Community species observation platform. ~200M+ research-grade observations globally with photo verification by community identifiers. Used as the de facto biodiversity citizen-science layer.
- **[Smart Citizen](https://smartcitizen.me/)** — ✅ `live` · `CC-BY-SA-4.0 (data) + GPL-3.0 (firmware/hardware)` · _BCN · ★_ · 🔌 `core:smartcitizen`
  Open-hardware community sensor network from Fab Lab Barcelona / IAAC. ~25k kits deployed globally measuring PM2.5, sound, temperature, humidity, light, CO2. FOSS hardware + firmware, public REST API.


## Social

### Planet

- **[UNDP Human Development Report — composite indices time series](https://hdr.undp.org/data-center/documentation-and-downloads)** — ✅ `live` · `Not formally stated — UNDP commits to free public accessibility of key statistics; licence UNCONFIRMED` · _★_
  UNDP Human Development Report Office composite indices as a single tidy CSV covering 1990-2023: HDI, inequality-adjusted HDI, Gender Development Index and Gender Inequality Index for around 193 countries.
- **[UNESCO Institute for Statistics (UIS) API](https://api.uis.unesco.org/api/public/versions)** — ✅ `live` · `Could not be verified — UNESCO data is commonly CC-BY-SA-3.0-IGO but neither the terms page nor the disclaimer carried licence text` · _★_
  UNESCO's official statistics API for education, science, culture and demographics. Indicator CR.3 gives upper-secondary completion rate and CR.3.GPIA its gender parity index, matching the framework's education- access and gender indicators directly.
- **[WHO Global Health Observatory (GHO) OData API](https://ghoapi.azureedge.net/api/WHOSIS_000001)** — ✅ `live` · `Not retrievable from the API endpoint — WHO GHO is generally CC-BY-NC-SA-3.0-IGO but this is UNVERIFIED` · _★_
  WHO's official global health statistics service exposed as an open OData API. Indicator WHOSIS_000001 carries life expectancy at birth by country, year and sex with confidence intervals; hundreds of other indicators share the interface.
- **[World Bank Poverty and Inequality Platform (PIP)](https://pip.worldbank.org/)** — ✅ `live` · `CC-BY-4.0 (World Bank dataset terms)` · _★_
  The World Bank's authoritative poverty and distributional statistics engine, computed from harmonised household surveys. Serves headcount, poverty gap, Gini, MLD and full income deciles per country-year with survey provenance.

### Bioregion

- **[Glottolog](https://glottolog.org/meta/downloads)** — ✅ `live` · `CC-BY-4.0` · _★_
  The Max Planck Institute for Evolutionary Anthropology's catalogue of the world's languages, dialects and families, with geographic coordinates per languoid and full bibliographic references. Openly licensed and versioned with DOIs.
- **[LandMark — Global Platform of Indigenous and Community Lands](https://www.landmarkmap.org/data-methods/access-data)** — ✅ `live` · `CC-BY-SA-4.0 (plus assent to LandMark Terms of Service)` · _★_
  The only global georeferenced platform mapping Indigenous and community lands, run by a WRI-originated steering group. Carries community-level polygons plus national tenure-security scoring against ten legal indicators.

### Region

- **[Bhutan Education Centers - Schools (NSDI)](https://nsdi.systems.gov.bt/portal/sharing/rest/content/items/4959d9acb1e141e0a363b8dd91ac803b?f=json)** — ✅ `live` · `Open (Geo-Information Policy 2018 §6.3.1 open tier: "Open data shall be openly and freely accessible")`
  Point locations of schools and colleges across Bhutan published by the National Land Commission Secretariat. Supports education-access indicators when joined to gewog and dzongkhag boundaries.
- **[GDELT — Global Database of Events, Language & Tone](https://www.gdeltproject.org/)** — ✅ `live` · `CC-BY-4.0` · _★_
  Real-time news event + tone time series in 100+ languages. Parses global news media to extract entities, themes, sentiment. ~150M events per year. Bulk download + BigQuery integration.
- **[IHME Global Burden of Disease](https://ghdx.healthdata.org/gbd-2021)** — ✅ `live` · `custom open (registration required)` · _★_
  Mortality + morbidity by cause × geography × age × year for ~370 diseases and injuries across ~200 countries. The de facto global health-burden time series.
- **[Japan 2020 Census Workplace/School Location Tabulation (従業地・通学地集計)](https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&lid=000001296018)** — ✅ `live` · `政府標準利用規約（第2.0版）- explicitly CC BY 4.0 compatible`
  The 2020 Census tabulation of population by place of residence cross-tabulated against place of work or school at municipality level - a true municipality-to-municipality origin-destination commuting matrix, plus daytime and night-time population.
- **[Occitanie — lycées et offre de formation](https://www.data.gouv.fr/organizations/region-occitanie)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Occitanie's open datasets on its upper-secondary schools and their training offer, including the mapped school register, the 2025-26 school-year list and the evolution of vocational course provision.
- **[WHO Open Data Repository](https://data.who.int/)** — ✅ `live` · `CC-BY-NC-SA-3.0-IGO` · _★_
  World Health Organization global health observatory + indicator repository. ~2,000 indicators across countries, themes, time.

### City

- **[Barcelona - Resultats electorals per seccio censal](https://opendata-ajuntament.barcelona.cat/data/api/action/package_show?id=est-eleccions-locals-seccio-censal)** — ✅ `live` · `CC-BY-4.0` · _BCN_
  Historical results for municipal, autonomic and general elections in Barcelona, published at census-section granularity - the finest official spatial unit below the district.
- **[Cambridge - Housing stock, permits and code violations](https://data.cambridgema.gov/Housing/Housing-Stock-and-Residential-Properties-by-Neighb/wiba-69ua)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  City of Cambridge housing series: housing stock and residential properties by neighbourhood, residential permits from 1996, housing code violations, and foreclosure filings from 2003.
- **[CBS Kerncijfers wijken en buurten](https://www.cbs.nl/nl-nl/cijfers/detail/85984NED)** — ✅ `live` · `Verveelvoudiging is toegestaan, mits het CBS als bron wordt vermeld (CC-BY-4.0 site-wide)`
  Statistics Netherlands' core indicators for every Dutch municipality, district and neighbourhood - population, household composition, income, housing, cars, energy use, distance to services - via the StatLine OData API.
- **[Seoul Employment Indicators (서울시 고용지표 통계)](https://data.seoul.go.kr/dataList/OA-475/S/1/datasetView.do)** — ⛔ `deprecated` · `공공누리 1유형 : 출처표시 (상업적 이용 및 변경 가능) - KOGL Type 1`
  Monthly unemployment rate, employment rate and labour-force participation rate for Seoul, broken out by sex. Sourced from KOSIS and republished by the city on its open data portal.
- **[Seoul Living Population by Administrative Dong (행정동 단위 서울 생활인구)](https://data.seoul.go.kr/dataList/OA-14991/S/1/datasetView.do)** — ⛔ `deprecated` · `공공누리 1유형 : 출처표시 (상업적 이용 및 변경 가능) - KOGL Type 1`
  Hourly estimates of the population actually present in each Seoul administrative dong, built by fusing city administrative data with telecom data. Daily updates from 2017 to the present.


## Economic

### Planet

- **[Appropedia](https://www.appropedia.org/)** — ✅ `live` · `CC-BY-SA-4.0 (site default; proprietary licences allowed only on approval)` · _★_ · 🛠 design
  The wiki of appropriate technology and sustainable development: build instructions, project pages and research for tools people make and repair locally. The largest openly licensed body of practical how-to on the web.
- **[Atlas of Economic Complexity (Harvard Growth Lab)](https://atlas.hks.harvard.edu/)** — ✅ `live` · `CC-BY-4.0` · _★_
  Global trade + economic-complexity indicators (ECI, product-space, diversification metrics) for ~250 countries × ~6,000 products. Bulk download via Dataverse; interactive web tool for exploration.
- **[Climate Funds Update](https://climatefundsupdate.org/data-dashboard/)** — ✅ `live` · `Not stated on the source page — freely downloadable, licence UNDECLARED` · _★_
  Independent monitor of multilateral climate finance run by ODI and Heinrich Boell Stiftung. Tracks money pledged, deposited and approved by fund, contributor country and recipient country, downloadable as Excel.
- **[Field Ready — humanitarian supply solutions](https://www.fieldready.org/)** — ✅ `live` · `CERN-OHL variant per catalogue metadata on 156 of 193 items — the organisation's own site says All rights reserved. Confirmation pending, see notes.` · _★_ · 🛠 design
  Designs for parts and tools made where they are needed instead of shipped: medical fittings, water and sanitation parts, shelter hardware. Built for aid contexts where the supply chain is the failure.
- **[Open Know-How Search (Internet of Production Alliance)](https://search.openknowhow.org/)** — ✅ `live` · `Creative Commons — version and variant not stated by the publisher (see notes)` · _★_ · 🛠 design
  A federated index of Open Know-How manifests — machine-readable descriptions of hardware designs, each naming its own files, processes and licence. The closest thing open hardware has to a card catalogue.
- **[OSHWA Open Source Hardware Certification](https://certification.oshwa.org/)** — ✅ `live` · `CC-BY-SA-4.0` · _★_ · 🛠 design
  The register of hardware certified as open source by the Open Source Hardware Association — each entry a project that has committed to publishing its design files under an open licence, with a certification UID to cite.
- **[Our World in Data — grapher CSV endpoints](https://ourworldindata.org/grapher/food-supply-kcal.csv)** — ✅ `live` · `CC-BY-4.0 for OWID's processing; upstream licences still apply to underlying values` · _★_
  OWID republishes FAOSTAT, World Bank and other series as clean, tidy, versioned CSVs at a stable URL pattern. Useful as the machine-readable escape hatch when an upstream agency's own API is unreachable.
- **[Things That Work (Fab City Foundation)](https://ttw.fab.city/)** — ✅ `live` · `CC-BY-SA-4.0 (content); MIT (code); third-party assets under their own terms` · _★_ · 🛠 design
  A curated index of solutions for when services fail — drinkable water when the tap is cut, light in a blackout, a part to print when the supply chain is gone. Tagged by what each one does and which scarcity it answers.
- **[World Bank What a Waste 2.0](https://datacatalog.worldbank.org/search/dataset/0039597)** — ✅ `live` · `CC-BY-4.0` · _★_
  National-level municipal solid waste accounts: per-capita generation, composition, collection, treatment. Coverage for ~217 economies.
- **[World Bank World Development Indicators](https://datacatalog.worldbank.org/search/dataset/0037712/World-Development-Indicators)** — ✅ `live` · `CC-BY-4.0` · _★_
  The World Bank's flagship cross-country indicator database served through a free unauthenticated REST API. Carries global and national GDP, value added by sector, adjusted net savings and natural-resource depletion rents.

### Bioregion

- **[Eurostat — Circular Material Use Rate (cei_srm030)](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/cei_srm030)** — ✅ `live` · `Eurostat re-use policy (Commission Decision 2011/833/EU) — free re-use with attribution` · _BCN · ★_
  Eurostat's circularity headline indicator: the share of material recycled and fed back into the economy as a fraction of total material use. The only officially compiled, openly licensed, machine-readable circularity-share series in existence.
- **[Eurostat — Environmental Goods and Services Sector (EGSS)](https://ec.europa.eu/eurostat/databrowser/view/env_ac_egss1/default/table?lang=en)** — ✅ `live` · `Eurostat re-use policy (Commission Decision 2011/833/EU) — free re-use with attribution, equivalent to CC-BY-4.0` · _BCN · ★_
  Eurostat's official green-jobs account: employment in full-time equivalents, value added and output for the environmental goods and services sector, split by NACE industry and CEPA/CReMA environmental purpose, for EU and EFTA countries.
- **[EXIOBASE 3 — multi-regional environmentally extended input-output tables](https://zenodo.org/records/5589597)** — ✅ `live` · `CC-BY-SA-4.0 for v3.8.2 — NOTE v3.9.6 and later are non-commercial only, see notes` · _★_
  Global multi-regional environmentally extended input-output database covering 44 countries plus 5 rest-of-world regions and 163 industries, with employment, material, land and emissions satellite accounts alongside monetary flows.
- **[FAOSTAT Food Balance Sheets](https://www.fao.org/faostat/en/#data/FBS)** — ✅ `live` · `CC-BY-4.0 (FAO standard database licence — not confirmable from the pages fetched; verify at download)` · _★_
  FAO Food Balance Sheets: production, imports, exports, stock change, feed, seed, losses and food supply per commodity per country. The canonical basis for any food self-sufficiency ratio.
- **[materialflows.net (UN International Resource Panel)](https://www.materialflows.net/)** — ✅ `live` · `custom open (UN IRP terms)` · _★_
  Economy-wide material flow accounts published by the UN International Resource Panel. National-level material extraction, imports, exports, consumption by category.
- **[OECD Green Growth Indicators (SDMX)](https://sdmx.oecd.org/public/rest/dataflow/OECD.ENV.EPI/all/latest)** — ✅ `live` · `OECD terms — CC-BY-4.0 for most OECD statistical data, not restated on the SDMX endpoint; verify per dataflow` · _★_
  OECD's green growth indicator set delivered over a public SDMX REST API with no key. Carries green jobs, environmental goods and services trade, environmental taxation, fossil-fuel support and resource productivity for OECD and partner economies.
- **[OECD Material Flow Accounts (SDMX)](https://sdmx.oecd.org/public/rest/dataflow/OECD.ENV.EPI/all/latest)** — ✅ `live` · `OECD terms — CC-BY-4.0 for most OECD statistical data, not restated on the endpoint` · _★_
  OECD economy-wide material flow accounts by material category covering metals, non-metallic minerals, biomass and fossil energy carriers. Includes domestic material consumption and material footprint, the consumption-based measure needed for honest circularity accounting.
- **[UN SEEA Global Data Collection](https://seea.un.org/en/data/global-data-collection)** — 📋 `planned` · `Not stated` · _★_
  UN Statistics Division's environmental-economic accounting programme. Currently a country-implementation tracker plus an Excel questionnaire collection; a compiled global account database is announced but not yet published.
- **[World Bank Carbon Pricing Dashboard](https://datacatalog.worldbank.org/search/dataset/0042051)** — ✅ `live` · `CC-BY-4.0` · _★_
  World Bank register of carbon taxes and emissions trading systems worldwide with prices, coverage and revenues by jurisdiction, at both national and sub-national level. Companion to the annual State and Trends of Carbon Pricing report.
- **[World Bank Changing Wealth of Nations (CWON)](https://datacatalog.worldbank.org/search/dataset/0042066)** — ✅ `live` · `CC-BY-4.0` · _★_
  World Bank wealth accounts measuring produced, human and natural capital as stocks per country. The only globally consistent open natural-capital valuation series, machine-readable through the Data360 API.

### Region

- **[Asian KLEMS](http://www.asiaklems.net/)** — ✅ `live` · `custom open` · _BLI_
  Sectoral productivity database for 12 Asian economies including Indonesia. Capital, Labour, Energy, Materials, Services at the industry level.
- **[BMF Datenportal - Bundeshaushalt Gesamtuebersicht (S05)](https://www.bundesfinanzministerium.de/Datenportal/Daten/offene-daten/haushalt-oeffentliche-finanzen/s05-bundeshaushalt-Gesamtuebersicht/s05-bundeshaushalt-Gesamtuebersicht.html)** — ✅ `live` · `dl-de/by-2-0 (Datenlizenz Deutschland - Namensnennung - Version 2.0)`
  The German federal budget overview as open data from the Federal Ministry of Finance: revenue, expenditure and their development over time, released as CSV and XLSX alongside the ministry's other fiscal series.
- **[Budget de depenses du Quebec - Secretariat du Conseil du tresor](https://www.donneesquebec.ca/recherche/dataset/budget-de-depenses)** — ✅ `live` · `CC-BY-4.0`
  Quebec's annual expenditure budget tabled at the Assemblee nationale, as CSV - ministry credits, transfer credits by project and beneficiary, special funds and non-budgetary bodies. 2021-22 to 2026-27.
- **[CBS Gemeentebegrotingen; baten en lasten naar regio en grootteklasse](https://www.cbs.nl/nl-nl/cijfers/detail/83641NED)** — ✅ `live` · `Verveelvoudiging is toegestaan, mits het CBS als bron wordt vermeld (CC-BY-4.0 site-wide)`
  Budgeted revenue and expenditure of Dutch municipalities per taakveld (policy field), in millions of euro and euro per inhabitant, broken down by province and municipality size class. 2017-2026, annual, via StatLine OData.
- **[Core Responsibilities as per Public Accounts of Canada](https://open.canada.ca/data/en/dataset/c9675417-100a-433a-92d4-79b710408def)** — ✅ `live` · `Open Government Licence - Canada`
  Canadian federal expenditure broken out by departmental core responsibility in CSV and XML - the closest published analogue to a functional or COFOG-style classification of federal spending.
- **[DGFiP — Balances comptables des régions depuis 2010](https://www.data.gouv.fr/datasets/balances-comptables-des-regions-depuis-2010)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Accounting balances of every French region's principal and annexe budgets, 2010 onward, published by DGFiP. Fills the region rung of the public-budget ladder for all French Fab City members from one national file.
- **[Fabriqué en Occitanie — artisans et entreprises affiliés](https://www.data.gouv.fr/datasets/artisans-et-entreprises-affilies-a-la-marque-fabrique-en-occitanie)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Register of artisans and firms certified under Occitanie's regional made-here mark, with an accompanying product list. A rare open, named registry of locally manufacturing producers at regional scale.
- **[GeoStat National Accounts (PxWeb) - Georgia](https://pc-axis.geostat.ge/PXWeb/pxweb/en/Database/National%20Accounts)** — ✅ `live` · `GeoStat open terms of use - download, use, adapt, modify, create derivative works, disseminate and share for any purpose including commercial, without prior permission; attribution to GEOSTAT required`
  Georgia's national accounts database, split by methodology into SNA 1993 and SNA 2008 branches, served through GeoStat's live PxWeb REST API under an open attribution licence.
- **[Kanagawa Prefectural Economic Accounts (神奈川県県民経済計算)](https://catalog.opendata.pref.kanagawa.jp/dataset/e73a198f6ebb90f4ef6c570a995fc8ff)** — ✅ `live` · `CC-BY-4.0`
  Kanagawa's SNA-consistent regional accounts: gross prefectural product by economic activity (nominal and real chain-linked), income distribution, expenditure-side GDP, integrated accounts, and employment by economic activity.
- **[Kanagawa Prefecture Transaction-Level Expenditure (神奈川県 1件ごとの支出情報)](https://catalog.opendata.pref.kanagawa.jp/dataset/92b4932f5f41d4ba0750bde96b6b1bdf)** — ✅ `live` · `CC-BY-4.0`
  Transaction-level expenditure records for Kanagawa Prefecture's general and special accounts, published monthly as XLSX by the prefectural Accounting Bureau under CC BY 4.0. Individual payments, not aggregates.
- **[Korea Local Finance Yearbook - Budget (지방재정365 지방재정연감(예산))](https://www.data.go.kr/data/15138678/fileData.do)** — ✅ `live` · `이용허락범위 제한 없음 (no restriction on scope of use)`
  Annual budget totals and itemised detail for every Korean local government, explicitly including 특별·광역시도, 도, 시, 군 and 자치구, so Seoul and all 25 of its districts are in scope. The bulk route to the gu tier.
- **[Korea Local Fiscal Independence Ratio, Final (지방재정365 재정자립도(최종))](https://www.data.go.kr/data/15058102/openapi.do)** — ✅ `live` · `이용허락범위 제한 없음 (no restriction on scope of use)`
  The share of each Korean local authority's budget it can fund from its own revenue sources, computed on the year-end final budget. A direct fiscal-autonomy indicator comparable across all Korean municipalities from FY2010.
- **[Korea National Revenue/Expenditure Settlement by Account (회계별 세입/세출결산 현황)](https://www.data.go.kr/data/15056702/openapi.do)** — ✅ `live` · `이용허락범위 제한 없음 (no restriction on scope of use)`
  Korean central-government revenue and expenditure settlement by accounting type, alongside national bond status, tax revenue, tax burden ratio and supplementary budget trends. The national rung of the Korean budget ladder.
- **[KOSIS Indicator Information API (국가데이터처 KOSIS 지표정보 조회 서비스)](https://www.data.go.kr/data/15127763/openapi.do)** — ✅ `live` · `공공저작물 : 출처표시 (제 1유형) - KOGL Type 1, attribution only`
  REST access to the KOSIS 100 major national indicators spanning population, employment, economic trends and prices, plus North Korea and G20 series. The general-purpose route into Korea's national statistics database.
- **[LAKLEMS — Latin America KLEMS](http://www.iadb.org/research/latin-american-klems-database)** — ⏳ `stale` · `custom open (IDB terms)` · _SCL_
  Sectoral productivity database for 18 Latin American economies. Capital, Labour, Energy, Materials, Services inputs at industry level. Maintained by IDB and partner institutions.
- **[Main Estimates - Treasury Board of Canada Secretariat](https://search.open.canada.ca/opendata/)** — ✅ `live` · `Open Government Licence - Canada`
  Canada's annual appropriation estimates by department and vote, published as CSV per fiscal year running 1 April to 31 March. Each year is a separate CKAN package, discoverable through the open API.
- **[Metroverse (Harvard Growth Lab)](https://metroverse.hks.harvard.edu/)** — ✅ `live` · `CC-BY-4.0` · _BCN · BOS · SCL_
  City-level economic-complexity dashboard covering ~1,200 metro areas. Industry employment, knowledge clusters, peer-city benchmarks, growth predictions.
- **[Presupuesto Abierto Argentina](https://www.presupuestoabierto.gob.ar/sici/datos-abiertos)** — ✅ `live` · `CC-BY-4.0`
  Argentina's national budget credit, revenue, physical execution and cross-cutting financial analysis, published by the Secretaría de Hacienda. Queryable through a documented v1 REST API and as bulk open data.
- **[Profil financier des municipalites locales - MAMH Quebec](https://www.donneesquebec.ca/recherche/dataset/profil-financier-des-municipalites-locales)** — ✅ `live` · `Creative Commons 4.0 Attribution (CC-BY) licence - Quebec (qc-cc-by)`
  Derived financial and fiscal profiles with computed ratios for Quebec municipalities, pre-aggregated to municipality, MRC, administrative region, population class and province. CSV and XLSX, 2018-2025.
- **[Public Expenditure Statistical Analyses (PESA) - HM Treasury](https://www.gov.uk/government/statistics/public-expenditure-statistical-analyses-2026)** — ✅ `live` · `Open Government Licence v3.0`
  HM Treasury's annual analysis of UK public spending by function, department and economic category, published as chapter and annex Excel tables plus a 246-page report. The UK national budget rung.
- **[Rapport financier des organismes municipaux - MAMH Quebec](https://www.donneesquebec.ca/recherche/dataset/rapport-financier-des-organismes-municipaux-et-autres-documents)** — ✅ `live` · `Creative Commons 4.0 Attribution (CC-BY) licence - Quebec (qc-cc-by)`
  Annual financial returns filed by every Quebec municipality, MRC, metropolitan community, transit body and regie, keyed on COD_GEO. 189 resources in XLSX and CSV covering 2015-2026.
- **[Région Occitanie — budgets primitifs, supplémentaires et comptes administratifs](https://www.data.gouv.fr/organizations/region-occitanie)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Occitanie's own voted budgets (primitif and supplémentaire) and executed comptes administratifs, published as M57 line-item files split between payment credits and multi-year programme authorisations.
- **[SICONFI DCA - Declaracao de Contas Anuais (estados e municipios)](https://www.tesourotransparente.gov.br/ckan/dataset/api-extrato-entes)** — ✅ `live` · `Open Data Commons Open Database License (ODbL)`
  Brazil's National Treasury annual accounts declaration for states and municipalities as a JSON API, keyed on the IBGE code. Gives the state-tier budget rung - gross realised revenue, deductions and transfers down.
- **[StatFin - General government expenditure by function (COFOG)](https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin/jmete)** — ✅ `live` · `CC-BY-4.0`
  Finnish general government expenditure classified by COFOG function, served through Statistics Finland's PxWeb REST API. The only verified COFOG-coded public spending series for Finland.
- **[StatFin - Regional accounts (altp)](https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin/altp)** — ✅ `live` · `CC-BY-4.0`
  Finnish regional accounts - GDP, gross value added and industry composition at maakunta level, including Pohjois-Pohjanmaa (code 17), the region containing Oulu. Served via Statistics Finland's PxWeb API.
- **[STATISTIK AUSTRIA open.data](https://data.statistik.gv.at/web/catalog.jsp)** — ✅ `live` · `CC-BY-4.0`
  Statistics Austria's open data catalogue: national and regional statistics on labour, prices, trade, regional and national accounts, tourism, transport, demography, health and education, in CSV and JSON with some OGC services.
- **[vulekamali - South African Budget Data Portal](https://vulekamali.gov.za/datasets)** — ✅ `live` · `National Treasury Terms and Conditions - use, download, copy, publish, distribute and transmit freely including commercially; attribution to National Treasury plus date of publication and disclosure of modifications required`
  National Treasury and Imali Yethu budget portal carrying national and provincial estimates of revenue and expenditure, budgeted-versus-actual spending, division of revenue and appropriation acts.
- **[Yucatan Datos Abiertos - Egresos y Cuenta Publica del Estado](https://transparencia.yucatan.gob.mx/datos_abiertos.php)** — ✅ `live` · `Datos digitales puestos a disposicion de cualquier persona para ser usados, reutilizados y redistribuidos libremente`
  The State of Yucatan's expenditure data as open CSV: annual Cuenta Publica 2021-2024 and quarterly execution reports 2021-2025, each shipped with a data dictionary. Published by the state transparency office.

### City

- **[Barcelona - Cens d'activitat economica i padro de l'IAE](https://opendata-ajuntament.barcelona.cat/data/api/action/package_show?id=cens-locals-planta-baixa-act-economica)** — ✅ `live` · `CC-BY-4.0` · _BCN_
  Two complementary Barcelona business registers: a census of ground-floor commercial premises by activity, and the padro of the economic activities tax (IAE) by activity type. Together a business-density signal.
- **[Barcelona - Pressupost municipal i execucio](https://opendata-ajuntament.barcelona.cat/data/api/action/package_show?id=evolucio-despeses-per-capitols-i-articles)** — ✅ `live` · `CC-BY-4.0` · _BCN_
  Ajuntament de Barcelona publishes its municipal budget and its settled execution as annual CSV series - revenue and expenditure, planned (inicial) and liquidated, by chapter, article and programme.
- **[Boston - Capital Plan](https://data.boston.gov/dataset/capital-budget)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  City of Boston five-year capital investment plan, FY27-31, roughly 4.4 billion USD, published as bulk CSV with a PDF data dictionary and refreshed annually.
- **[Boston - Checkbook Explorer](https://data.boston.gov/dataset/checkbook-explorer)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  Actual executed City of Boston expenditure by vendor and department, transaction level, published as per-fiscal-year CSVs from FY2012 onward and refreshed monthly.
- **[Boston - Operating and Revenue Budget](https://data.boston.gov/dataset/operating-budget)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  City of Boston adopted operating budget and revenue budget, published as bulk CSV with a PDF data dictionary, by department and programme for the General Fund.
- **[Budget de fonctionnement - Ville de Montreal](https://donnees.montreal.ca/dataset/budget)** — ✅ `live` · `CC-BY-4.0`
  Annual operating budget for the Ville de Montreal and the agglomeration, tabled each autumn for the following calendar year. XLSX series 2013-2026, published by the Service des finances.
- **[Cambridge - Capital budget](https://data.cambridgema.gov/d/9chi-2ed3)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  City of Cambridge capital budget project funding by fiscal year, FY2020 to FY2031, with per-project latitude and longitude for each funded capital project.
- **[Cambridge - Operating budget, revenues and expenditures](https://data.cambridgema.gov/d/ixyv-mje6)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  City of Cambridge annual operating budget as two paired Socrata datasets - budgeted revenues by source and budgeted expenditures by department and division - covering FY2011 to FY2027.
- **[DGFiP Balances comptables des communes](https://www.data.gouv.fr/datasets/balances-comptables-des-communes-en-2024/)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Full DGFiP accounting balances for every French commune, covering principal and ancillary budgets (budgets principaux et budgets annexes), published yearly by the French finance ministry as CSV, JSON and ZIP.
- **[DGFiP Comptes individuels des communes (fichier global)](https://data.economie.gouv.fr/explore/dataset/comptes-individuels-des-communes-fichier-global-2023-2024/)** — ✅ `live` · `Licence Ouverte 2.0`
  DGFiP annual individual accounts for every French commune, published as one global file per year cohort on the Ministry of Finance open-data portal. Carries revenue, expenditure, debt and balance-sheet aggregates per commune.
- **[DGFiP — Balances comptables des groupements à fiscalité propre depuis 2010](https://www.data.gouv.fr/datasets/balances-comptables-des-groupements-a-fiscalite-propre-depuis-2010)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Accounting balances of French intercommunal groupings (EPCI — métropoles, communautés d'agglomération, communautés de communes), 2010 onward, from DGFiP. The only open source covering the EPCI fiscal tier nationally.
- **[INEGI DENUE - Directorio Estadistico Nacional de Unidades Economicas](https://www.inegi.org.mx/servicios/api_denue.html)** — ✅ `live` · `INEGI Terminos de Libre Uso de la Informacion`
  Mexico's national business register as a geocoded REST API: over five million establishments with activity code, employee-size band, address and coordinates. Run by INEGI, free token required.
- **[INEGI EFIPEM - Estadistica de Finanzas Publicas Estatales y Municipales](https://www.inegi.org.mx/programas/finanzas/)** — ✅ `live` · `INEGI Terminos de Libre Uso de la Informacion`
  INEGI's annual revenue-and-expenditure series for every Mexican state government, municipality, Mexico City and its 16 demarcaciones, 1989-2025, keyed on the INEGI state and municipality clave.
- **[Japan 2021 Economic Census for Business Activity (経済センサス-活動調査)](https://www.e-stat.go.jp/stat-search/files?tstat=000001145590)** — ✅ `live` · `政府標準利用規約（第2.0版）- explicitly CC BY 4.0 compatible`
  Japan's full-coverage census of every business establishment and enterprise, giving number of establishments, employees and sales by industry down to municipality level. Survey reference June 2021, published 2023-06-27, updated through December 2025.
- **[Kamakura City Budget and Settlement Open Data (鎌倉市 予算・決算オープンデータ)](https://www.city.kamakura.kanagawa.jp/zaisei/yosan.html)** — ✅ `live` · `CC-BY-4.0`
  Kamakura City publishes initial budget and final settlement, each split into revenue and expenditure, as annual CSV files covering FY2004-FY2024 under CC BY 4.0. Classified by the Japanese statutory 目的別 (purpose) and 性質別 (nature) schemes.
- **[Kota Denpasar - APBD (Ringkasan dan konsistensi RKPD-APBD)](https://satudata.denpasarkota.go.id/dataset?q=APBD)** — ✅ `live` · `Lainnya (Domain Publik)` · _BLI_
  Kota Denpasar publishes its annual budget summaries and RKPD-to-APBD consistency documents as CKAN datasets, mostly from BPKAD, in CSV with a public-domain licence.
- **[Local authority revenue expenditure and financing England - Revenue Outturn multi-year data set](https://www.gov.uk/government/statistics/local-authority-revenue-expenditure-and-financing-england-revenue-outturn-multi-year-data-set)** — ✅ `live` · `Open Government Licence v3.0`
  Per-authority English local government revenue expenditure and financing from statutory RO returns, 2017-18 to 2024-25, as one CSV time series on CIPFA SeRCOP service lines. Covers Plymouth.
- **[Local Government Finance Survey, Japan (地方財政状況調査)](https://www.e-stat.go.jp/stat-search/files?toukei=00200251&tstat=000001077755)** — ✅ `live` · `政府標準利用規約（第2.0版）- explicitly CC BY 4.0 compatible`
  Japan's standardised annual fiscal survey of every local authority, FY1990-FY2025, with 4,973 tables in the municipal section alone, keyed on 団体コード so municipalities are directly comparable. The federatable cross-municipal fiscal series for Japan.
- **[Municipal Money (South Africa National Treasury)](https://municipaldata.treasury.gov.za/)** — ✅ `live` · `National Treasury Terms of Use - free commercial and non-commercial reuse, redistribution permitted, attribution to National Treasury plus date of publication required`
  National Treasury's municipal finance API for all 292 South African municipalities: budgeted and audited income, expenditure, cash flow, capital and grants, 2008-09 to 2025-26. Built with OpenUp.
- **[Municipal Settlement Status Survey, Japan (市町村別決算状況調)](https://www.soumu.go.jp/iken/zaisei/r06_shichouson.html)** — ✅ `live` · `公共データ利用規約（第1.0版）PDL1.0 - explicitly CC BY 4.0 compatible`
  MIC's pre-tabulated annual settlement tables for all Japanese municipalities, FY2002-FY2024, as ten Excel files per year split 市部/町村 covering summary, revenue breakdown, expenditure by purpose and by nature, and outstanding local debt.
- **[ONS Regional gross domestic product - local authorities](https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/regionalgrossdomesticproductlocalauthorities)** — ✅ `live` · `Open Government Licence v3.0`
  Balanced UK regional GDP 1998-2023 in current prices and chained volume measures for local authority districts, unitary authorities, Scottish council areas and ITL regions. Excel.
- **[Paris - Budgets votes et comptes administratifs](https://opendata.paris.fr/api/explore/v2.1/catalog/datasets?where=theme%3D%22Administration%20et%20Finances%20Publiques%22)** — ✅ `live` · `Open Database License (ODbL)`
  The City of Paris finance corpus on its own open-data portal - voted budgets (planned) and comptes administratifs (executed) for principal and ancillary budgets, plus debt, fixed assets, grants paid and the balance sheet.
- **[Paris - Etats speciaux d'arrondissement (sub-municipal budgets)](https://opendata.paris.fr/api/explore/v2.1/catalog/datasets?where=search%28%22etats%20speciaux%22%29)** — ✅ `live` · `Open Database License (ODbL)`
  Paris publishes the etats speciaux d'arrondissement - the budget delegated to each of its arrondissements - as open data, both voted and executed. A rare case of public finance published BELOW the municipal tier.
- **[Poslovni register Slovenije (AJPES business register)](https://podatki.gov.si/publisher/agencija_republike_slovenije_za_javnopravne_evidence_in_storitve)** — ✅ `live` · `CC-BY-4.0`
  Slovenia's national business register from AJPES - every registered entity with its seat municipality, giving business density and sector composition for Ljubljana. CSV, XML and a programmatic interface.
- **[Presupuesto Abierto Chile — Pagos municipales](https://presupuestoabierto.gob.cl/municipalities)** — ✅ `live` · `CC-BY-SA-4.0` · _SCL_
  Transaction-level payments made by every Chilean municipality, keyed on the official comuna code (CUT). Run by DIPRES (Dirección de Presupuestos, Ministerio de Hacienda). Served as filterable CSV over a public REST API.
- **[Proracun Grada Zagreba](https://data.zagreb.hr/dataset/proracun-grada-zagreba-2026)** — ✅ `live` · `Otvorena dozvola (OD)`
  Consolidated City of Zagreb budget - planned revenue and expenditure by year, published as XLSX and CSV on the city open data portal. Two datasets cover 2026 (plus 2027-2028 projections) and 2022-2025.
- **[Reddition de comptes financiere - Ville de Montreal](https://donnees.montreal.ca/dataset/reddition-comptes-financiere)** — ✅ `live` · `CC-BY-4.0`
  Budget-versus-actual financial accountability reporting for Montreal, allowing comparison of fiscal and budgetary data for the same year. Eight annual XLSX files covering 2018-2025.
- **[Regionaldatenbank Deutschland - Kommunale Kassenergebnisse (71517)](https://www.regionalstatistik.de/genesis/online?operation=statistic&code=71517)** — ✅ `live` · `dl-de/by-2-0 (Datenlizenz Deutschland - Namensnennung - Version 2.0)`
  Cash results for German municipal government: gross revenue and gross expenditure of Gemeinden and Kreise, published at individual municipality resolution by the Laender statistical offices via IT.NRW.
- **[Rennes - Budgets primitifs et comptes administratifs](https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets?where=search%28%22budget%22%29)** — ✅ `live` · `Open Database License (ODbL)`
  Ville de Rennes publishes its budget primitif (planned) and compte administratif (executed) as separate yearly datasets from 2008 onward, split into principal budget, annexes and grants to associations.
- **[SCB Rakenskapssammandrag - municipal costs and revenues by function](https://api.scb.se/OV0104/v1/doris/sv/ssd/OE/OE0107/OE0107B/KostnDR)** — ✅ `live` · `CC0-1.0`
  Costs and revenues for all 290 Swedish municipalities across 65 functional areas, 2011-2025, in thousands of SEK at current prices, via Statistics Sweden's PxWeb API. Lund is kommunkod 1281.
- **[Seoul Expenditure Operations - Projects and Budget (서울시 세출운용 사업 및 예산 정보)](https://data.seoul.go.kr/dataList/OA-13269/S/1/datasetView.do)** — ⛔ `deprecated` · `이용허락범위 제한 없음 (no restriction on scope of use)`
  Project-level Seoul metropolitan expenditure showing current available budget, amount spent and unexecuted balance side by side, classified by 분야/부문 (functional field and sector) and by department. Updated daily.
- **[SICONFI RREO - Relatorio Resumido da Execucao Orcamentaria (municipios)](https://www.tesourotransparente.gov.br/ckan/dataset/api-rreo-entes)** — ✅ `live` · `Open Data Commons Open Database License (ODbL)`
  Brazil's National Treasury bimonthly budget-execution report for every one of the 5,570 municipalities, as a JSON API keyed on the IBGE municipality code. Carries planned and executed revenue and expenditure-by-function in one schema.
- **[Somerville - Capital Investment Plan FY16-26](https://data.somervillema.gov/d/wz6k-gm5k)** — ⏳ `stale` · `Open Data Commons Open Database License (ODbL)` · _BOS_
  City of Somerville ten-year capital investment plan - infrastructure, building improvements, park redesigns and equipment - with per-project addresses, coordinates, funding source and year-by-year amounts.
- **[Sredstva mjesne samouprave Grada Zagreba](https://data.zagreb.hr/dataset/sredstva-mjesne-samouprave-2001-2023)** — ✅ `live` · `Otvorena dozvola (OD)`
  Funds allocated to Zagreb's sub-municipal self-government units (gradske cetvrti and mjesni odbori) for small communal works, 2001-2024, roughly EUR 1.094 billion in total. CSV and XLSX.
- **[Toulouse Metropole - Budgets primitifs et comptes administratifs](https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets?where=theme%3D%22Finance%22)** — ✅ `live` · `Licence Ouverte v2.0 (Etalab)`
  218 finance datasets on Toulouse Metropole's portal: budgets primitifs (planned) and comptes administratifs both alloue and realise (executed), for the city, the metropole and several member communes and their satellite budgets.

### Community

- **[Fab Lab Activity Index (Boeing 2024)](https://link.springer.com/chapter/10.1007/978-3-658-44114-2_9)** — ✅ `live` · `CC-BY-4.0 (chapter, Open Access)` · _★_
  Per-lab activity baseline derived from the Fab Lab Census and fablabs.io registry. The first peer-reviewed quantitative index of distributed-production capacity at the community tier.
- **[Fab Lab Network Data — the labs.json archive](https://gitlab.fabcloud.org/fl-management/fablab-network-data)** — ✅ `live` · `No licence published — the repository has none, and the records are fablabs.io's, under its Terms of Use. See economic/community/fablabs-io.` · _★_ · 🔌 `pack:make` · 🛠 facility
  Forty-eight dated freezes of the fablabs.io lab directory, monthly since 2025, kept in a public Fab Foundation repository. The same records as the live endpoint, but pinnable: a dated file instead of a moving target.
- **[fablabs.io — Fab Lab Network directory](https://www.fablabs.io/)** — ✅ `live` · `NOT OPEN — no data licence published. Platform ToS §7.4 restricts mass harvesting, §7.5 restricts commercial use, §8.1 leaves copyright with each lab. See notes.` · _★_ · 🔌 `pack:make` · 🛠 facility
  The Fab Foundation's directory of fab labs: name, coordinates, activity status and a six-token capability vocabulary, self-entered by the labs themselves. The closest thing the network has to a census of where things can be made.
- **[OpenStreetMap (Overpass API)](https://www.openstreetmap.org/)** — ✅ `live` · `ODbL-1.0` · _★_ · 🔌 `pack:place`
  The collaborative world map: buildings, roads, land use, shops, workshops, amenities, with a free query API (Overpass). The densest open record of what a neighbourhood physically contains, edited by the people who live in it.


## Governance

### Planet

- **[Global Data Barometer (2nd edition, 2024)](https://globaldatabarometer.org/open-data/)** — ✅ `live` · `CC-BY-4.0` · _★_
  Country-level assessment of data governance, capability and availability across eight thematic clusters including public procurement, public finance, land management and political integrity. Hosted by D4D.net and ILDA with IDRC funding.
- **[IATI Datastore API](https://docs.datastore.iatistandard.org/en/latest/api/)** — ✅ `live` · `Per-publisher — IATI publisher data is generally released openly but the licence is set by each publisher and was NOT verified here` · _★_
  Solr-backed query layer over all published IATI activity, transaction and budget data - the largest machine-readable register of aid and development finance flows, including climate-tagged spend, published by donors and implementers themselves.
- **[OONI — Open Observatory of Network Interference](https://ooni.org/)** — ✅ `live` · `CC-BY-NC-SA-4.0` · _★_
  Country-level measurement of internet censorship and traffic interference. Open data archive of probes from ~30k volunteers across 200+ countries. The empirical baseline for measuring state-level interference with the data substrate a federation runs on.
- **[Open Government Partnership — Open Data](https://www.opengovpartnership.org/open-data/)** — ✅ `live` · `CC-BY-4.0` · _★_
  OGP's commitment-level databases covering national and local action plans, with Independent Reporting Mechanism assessments of ambition, completion and early results. Run by the OGP Support Unit.
- **[Sustainable Development Report / SDG Index (SDSN)](https://dashboards.sdgindex.org/downloads)** — ✅ `live` · `Not stated on the downloads page — licensing questions directed to info@sdgindex.org; UNCONFIRMED` · _★_
  SDSN and Bertelsmann's annual index scoring 193 UN member states on all 17 SDGs, with per-indicator values, goal scores and trend arrows indicating whether a country is on track to meet each goal by 2030.

### Bioregion

- **[ChileCompra](https://www.chilecompra.cl/)** — ✅ `live` · `public domain` · _SCL_
  Chilean national public-procurement portal. All government procurement lifecycle: bases de licitacion, ofertas, adjudicaciones. Public REST API + bulk download.
- **[LKPP / SPSE — Indonesian National Procurement](https://www.lkpp.go.id/)** — ✅ `live` · `public (Indonesian government)` · _BLI_
  Indonesian Lembaga Kebijakan Pengadaan Barang/Jasa Pemerintah (LKPP) operates SPSE, the national e-procurement system. Public tender data for central government and most regional bodies including Bali province.
- **[Ramsar Sites Information Service (RSIS)](https://rsis.ramsar.org/)** — ✅ `live` · `Open access statement only — the Secretariat provides open access to promote conservation and wise use; no reuse terms, no SPDX identifier` · _★_
  Convention on Wetlands database of 2,000+ internationally important wetland sites across 160+ Contracting Parties, with wetland type, ecology, land use, threats, hydrological values and a Ramsar Information Sheet per site.
- **[TED — Tenders Electronic Daily](https://ted.europa.eu/)** — ✅ `live` · `CC-BY-4.0` · _BCN_
  Every public-tender notice published in the EU. Full procurement lifecycle: notice published, bid deadline, award, completion. Bulk download via Open Data Portal of the EU; daily updates.
- **[TFDD International Freshwater Treaties Database](https://transboundarywaters.ceoas.oregonstate.edu/international-freshwater-treaties-database)** — ⏳ `stale` · `None stated — OSU copyright applies; translations described as unofficial and for informational and academic purposes only` · _★_
  Over 800 international freshwater agreements from 1820 to 2021, coded by basin, signatory countries, date, topic, allocation measures, conflict- resolution mechanisms and non-water linkages. The canonical dataset for water-sharing agreements between jurisdictions.
- **[TFDD International River Basin Organization Database](https://transboundarywaters.ceoas.oregonstate.edu/international-river-basin-organization-database)** — ⏳ `stale` · `None stated — OSU copyright applies` · _★_
  Institutional-design data for more than 120 river basin organisations across more than 110 internationally shared watercourses, coded for membership, functional scope, legal foundation, financing, decision- making, data sharing, monitoring and dispute resolution.
- **[TFDD Transboundary Freshwater Spatial Database — 313 international river basins](https://transboundarywaters.ceoas.oregonstate.edu/spatial-datasets)** — ✅ `live` · `Not copyrighted; wide use encouraged with attribution to the Transboundary Freshwater Diplomacy Database, OSU CEOAS` · _★_
  Shapefiles of the world's 313 international river basins plus basin country units (basin by country intersections) with a codebook of biophysical, social and political attributes. Maintained by Oregon State University's Program in Water Conflict Management and Transformation.

### Region

- **[Bhutan NSDI Geospatial Catalogue (ArcGIS Portal API)](https://nsdi.systems.gov.bt/portal/sharing/rest/search?q=type%3A%22Feature%20Service%22&f=json&num=25)** — ✅ `live` · `Open (Geo-Information Policy 2018 §6.3.1 open tier: "Open data shall be openly and freely accessible")`
  The anonymous ArcGIS Enterprise catalogue API for Bhutan's National Spatial Data Infrastructure, returning 193 feature services with per-item licence category across 22 contributing agencies. The only machine-readable government data catalogue in Bhutan.
- **[Catalogo de Datos Abiertos del Estado de Nuevo Leon](http://catalogodatos.nl.gob.mx/dataset/)** — ✅ `live` · `Open Data Commons Attribution License (105 datasets) / Creative Commons Attribution (19)`
  Nuevo Leon's state open data catalogue, CKAN 2.10, 127 datasets published by named state secretariats and agencies, every one of them under an open licence. The region rung for Monterrey.
- **[Data.overheid.nl](https://data.overheid.nl/)** — ✅ `live` · `CC0-1.0`
  The Netherlands' national open data register, run by KOOP. CKAN-backed DCAT catalogue indexing datasets from ministries, provinces, water boards and municipalities, including ones with no portal of their own.
- **[Datos Argentina (datos.gob.ar)](https://datos.gob.ar/)** — ✅ `live` · `Los datos publicados acá son públicos y se pueden reutilizar libremente citando la fuente.`
  Argentina's national open data portal, running CKAN 2.11.5. Indexes roughly 1,285 datasets from about 45 national organisations, including the budget classifiers and the geographic normalisation service.
- **[Donnees Quebec](https://www.donneesquebec.ca/recherche/dataset)** — ✅ `live` · `CC-BY-4.0`
  Quebec's CKAN 2.11.3 provincial catalogue, federating state and municipal publishers - 1609 datasets with 1549 under CC BY 4.0. Its largest single publisher is a municipality, Ville de Montreal.
- **[e-Gov Data Portal (e-Govデータポータル), Japan national open data catalogue](https://data.e-gov.go.jp/data/api/3/action/package_list)** — ✅ `live` · `公共データ利用規約（第1.0版）PDL1.0 - explicitly CC BY 4.0 compatible`
  Japan's national CKAN open data catalogue, successor to data.go.jp, exposing roughly 2,800 government datasets through a working CKAN Action API under the Public Data License 1.0.
- **[ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)** — ✅ `live` · `custom open (ENTSO-E terms; free for non-commercial)` · _BCN_
  European electricity grid data: generation by source, consumption, cross-border flows, balancing, day-ahead prices. Hourly resolution for all EU + UK + Norway + Switzerland.
- **[Find a Tender Service - OCDS API (UK)](https://www.find-tender.service.gov.uk/Developer/Documentation)** — ✅ `live` · `Open Government Licence v3.0`
  UK national procurement notice register under the Procurement Act 2023, from 24 February 2025, serving OCDS 1.1.5 JSON release and record packages. Also carries a payments transparency register.
- **[Generalitat de Catalunya — Dades Obertes](https://analisi.transparenciacatalunya.cat/)** — ✅ `live` · `CC-BY-4.0` · _BCN_
  Catalan regional open data portal. Includes Estadistiques de residus municipals (per-capita waste, all 947 Catalan municipalities), Idescat IPC (consumer prices), Mercabarna figures, energy mix.
- **[Georef — Servicio de Normalización de Datos Geográficos (Argentina)](https://datosgobar.github.io/georef-ar-api/)** — ✅ `live` · `CC-BY-4.0`
  Argentina's official API for resolving and normalising administrative units — provincias, departamentos, municipios, localidades and addresses — to their national identifier codes. Run by Datos Argentina on IGN base data.
- **[Georgia State Procurement Agency OCDS feed](https://data.open-contracting.org/en/publication/24)** — ⛔ `deprecated` · `CC0-1.0`
  Open Contracting Data Standard release of Georgia's unified e-procurement system - 275,439 tender records across planning, tender, award and contract stages, CC0 licensed, but frozen at June 2019.
- **[Kanagawa Open Data Catalogue (神奈川県オープンデータカタログサイト)](https://catalog.opendata.pref.kanagawa.jp/dataset)** — ✅ `live` · `CC-BY-4.0 (763 datasets); CC-BY-NC (24 datasets)`
  Kanagawa Prefecture's CKAN open data catalogue and the regional data-sharing platform for the Kamakura administrative chain, holding 811 datasets of which 763 are CC-BY and 24 are CC-BY-NC.
- **[KONEPS Open Data Standard Service (나라장터 공공데이터개방표준서비스)](https://www.data.go.kr/data/15058815/openapi.do)** — ✅ `live` · `이용허락범위 제한 없음 (no restriction on scope of use)`
  Bid, award and contract records from KONEPS, Korea's national e-procurement system, structured to the Ministry of the Interior and Safety open-data standard. The spend-side counterpart to the Korean budget ladder.
- **[KONEPS Tender Notice Information Service (나라장터 입찰공고정보서비스)](https://www.data.go.kr/data/15129394/openapi.do)** — ✅ `live` · `이용허락범위 제한 없음 (no restriction on scope of use); 무료`
  Tender announcements across goods, services, construction and foreign procurement in Korea, with base amounts, licence restrictions and eligible-region information. Regional filtering is possible via 참가가능지역정보.
- **[Korea Administrative Standard Code - Legal Dong Code (행정표준코드 법정동코드)](https://www.data.go.kr/data/15077871/openapi.do)** — ✅ `live` · `이용허락범위 제한 없음 (no restriction on scope of use)`
  The authoritative Korean administrative code register, resolving the full chain from 시도 through 시군구 to 읍면동. The canonical join key for every other Korean dataset in the Fab City Index matrix.
- **[Korea Local Government Fiscal Disclosure Index (지방재정365 우리 지자체 재정공시)](https://www.data.go.kr/data/15138709/openapi.do)** — ✅ `live` · `이용허락범위 제한 없음 (no restriction on scope of use)`
  A machine-readable index of every Korean local authority's statutory fiscal disclosure, covering revenue, expenditure, local bonds, funds and investment projects. It harmonises where to look across municipalities rather than publishing the figures.
- **[MassGIS](https://www.mass.gov/orgs/massgis-bureau-of-geographic-information)** — ✅ `live` · `public` · _BOS_
  Massachusetts state geospatial data: parcels, buildings, transit network, hydrography, environmental constraints, election districts. Bulk download via state portal + ArcGIS REST services.
- **[Open Government Portal - Government of Canada](https://search.open.canada.ca/opendata/)** — ✅ `live` · `Open Government Licence - Canada`
  Canada's federal CKAN catalogue, uniformly licensed under the Open Government Licence - Canada, with a fully open API. Over 1200 budget-related datasets and the reference source for federal fiscal data.
- **[Portal otvorenih podataka Republike Hrvatske (data.gov.hr)](https://data.gov.hr/ckan/dataset)** — ✅ `live` · `Otvorena dozvola (OD)`
  Croatia's national open data portal, CKAN-based, run by Sredisnji drzavni ured za razvoj digitalnog drustva. 3,874 datasets from ministries, agencies, counties, towns and municipalities.
- **[Région Auvergne-Rhône-Alpes — données essentielles de la commande publique](https://www.data.gouv.fr/organizations/region-auvergne-rhone-alpes)** — ✅ `live` · `Licence Ouverte`
  Auvergne-Rhône-Alpes' statutory public-procurement award register, published continuously as one small JSON record per notified contract following the Etalab commande-publique schema.
- **[South African eTenders OCDS API](https://ocds-api.etenders.gov.za/)** — ✅ `live` · `CC-BY-4.0`
  National Treasury procurement releases for South African national and provincial government in Open Contracting Data Standard format, drawn from the eTender portal, BAS and the Central Supplier Database.
- **[Systeme electronique d'appel d'offres (SEAO) - Quebec](https://www.donneesquebec.ca/recherche/dataset/systeme-electronique-dappel-doffres-seao)** — ✅ `live` · `CC-BY-4.0`
  Quebec's public tender and awarded-contract register, covering government, health, education and municipal bodies. Weekly and monthly files, XML from 2009 and JSON from March 2021.
- **[TenderNed - Aankondigingen van overheidsopdrachten](https://data.overheid.nl/dataset/aankondigingen-van-overheidsopdrachten---tenderned)** — ✅ `live` · `CC0-1.0`
  Every Dutch public procurement notice - market consultations, contract notices, awards, modifications and early terminations - published by PIANOo via TenderNed, downloadable in bulk and available as feeds and a webservice.

### City

- **[Amsterdam Open Data / DataPunt API](https://data.amsterdam.nl/catalogus/)** — ✅ `live` · `CC0-1.0`
  Gemeente Amsterdam's data catalogue and its DataPunt REST API, which serves roughly 100 versioned dataset collections (BAG, trees, ecology, waste, gas-free zones) as JSON, plus WFS and MVT layers.
- **[Analyze Boston](https://data.boston.gov/dataset)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_ · 🔌 `core:ckan`
  City of Boston open data portal, CKAN-based. 235 datasets covering 311 service requests, budget and spending, building permits, employee earnings, food inspections, traffic and public safety.
- **[Bali Satu Data (provincial)](https://balisatudata.baliprov.go.id/search-data)** — ✅ `live` · `not stated` · _BLI_ · 🔌 `core:ckan`
  Provinsi Bali's Satu Data portal. Reachable and responding, but its search returns an empty state with no datasets listed by default, so its actual holdings could not be established.
- **[Barcelona - Perfil del contractant i relacio de contractistes](https://opendata-ajuntament.barcelona.cat/data/api/action/package_show?id=perfil-contractant)** — ✅ `live` · `CC-BY-4.0` · _BCN_
  Barcelona's public procurement register: tenders, bids, awards and contract formalisations from the last five years, updated daily, plus a contractors list with tax identifiers and amounts running back to 2012.
- **[Boston - Procurement and discretionary spending](https://data.boston.gov/dataset/city-of-boston-contract-award)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  City of Boston procurement transparency set: awarded contracts with equitable procurement reporting, a forward-looking buying plan, and departmental discretionary spending.
- **[Cambridge - Participatory budgeting](https://data.cambridgema.gov/d/54vd-wdqj)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  Resident-submitted ideas and final ballot projects from the City of Cambridge participatory budgeting cycles, published as open datasets on the city Socrata portal.
- **[Cambridge Open Data](https://data.cambridgema.gov/)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  City of Cambridge, Massachusetts open data portal on Socrata, carrying 447 datasets across budget, housing, energy disclosure, inspections and participatory budgeting, with a full SODA API and discovery catalogue.
- **[Dados Abertos Belo Horizonte](https://dados.pbh.gov.br/dataset)** — ✅ `live` · `Creative Commons Attribution (564 of 606); Open Data Commons ODbL (23 of 606)`
  Belo Horizonte's municipal open data portal, CKAN 2.10.5. 606 datasets across planning, finance, mobility, health, education and environment, with a working CKAN action API and real-time consolidated revenue and expenditure feeds.
- **[Dados Abertos Recife](http://dados.recife.pe.gov.br/dataset)** — ✅ `live` · `Open Data Commons Open Database License (ODbL)`
  Recife's municipal open data portal, CKAN 2.11.5. 222 datasets, every one of them under ODbL, weighted towards health, mobility and education, published by named municipal secretariats.
- **[Data Place Plymouth](https://plymouth.thedata.place/dataset)** — ✅ `live` · `Open Government Licence v3.0`
  Plymouth's CKAN open data portal - 174 datasets from 10 publishers including the city council, public health, a CCG, the police and Plymouth Marine Laboratory. 144 under OGL, the rest CC-BY and ODbL.
- **[data.gv.at - Stadt Linz](https://data.linz.gv.at/)** — ✅ `live` · `CC-BY-4.0`
  Linz publishes its open data as a publishing body on data.gv.at, Austria's national open government data portal, rather than on a portal of its own: 823 datasets covering mobility, statistics, planning, tourism and procurement.
- **[datos.gob.cl](https://datos.gob.cl/)** — ✅ `live` · `not stated` · _SCL_ · 🔌 `core:ckan`
  Chile's national open data portal, CKAN 2.10.4, publishing 3,211 datasets from 272 institutions including central government and many municipalities. Used as the Santiago pilot's open-data substrate.
- **[Donnees ouvertes - Ville de Montreal](https://donnees.montreal.ca/dataset)** — ✅ `live` · `CC-BY-4.0`
  Montreal's CKAN 2.11.5 open data catalogue - 404 datasets, 394 under CC BY 4.0 and 284 carrying a CSV. Hosts non-municipal publishers alongside the city. Catalogue breadth and licence openness are themselves governance indicators.
- **[Fab City pledged cities](https://gitlab.fabcloud.org/fl-management/fablab-network-data/-/blob/main/data/fabcity.xlsx)** — ✅ `live` · `No licence published — the repository carries none. The Foundation's own list, and the one source here it could license with a sentence.` · _★_ · 🛠 network
  The cities, regions and countries that have pledged to produce most of what they consume by 2054, with the year each one signed. The Fab City commitment as a list rather than a map on a website.
- **[Kolada v3 - Swedish municipal and regional KPI database](https://www.kolada.se/om-oss/api/)** — ✅ `live` · `Free of charge, no agreement required, commercial use permitted; attribution "Kalla, Kolada" required unless the data has been substantially processed`
  Sweden's municipal KPI database - roughly 6000 indicators across finance, schools, care, environment and governance for every kommun and region, with an open JSON API. Lund is municipality_id 1281.
- **[Odprti podatki Mestne obcine Ljubljana (ArcGIS Hub)](https://mol-ljubljana.hub.arcgis.com/)** — ✅ `live` · `CC-BY-4.0`
  Ljubljana's municipal open data portal on ArcGIS Hub - geospatial layers for roads, cycle paths, parking, sports, schools, health network and heritage, downloadable as CSV, GeoJSON and KML.
- **[Offene Daten Wuppertal](https://offenedaten-wuppertal.de/)** — ✅ `live` · `CC-BY-4.0`
  Wuppertal's municipal open data portal, run on DKAN and hosted for the city by Stadt Koeln. Around 290 datasets across geodata, population, budget, mobility, environment and elections for the largest city of the Bergisches Staedtedreieck.
- **[ONS Open Geography Portal - ArcGIS REST services](https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services)** — ✅ `live` · `Open Government Licence v3.0`
  Queryable ArcGIS FeatureServers for UK statistical geography, serving vintaged GSS codes and boundaries from output area to country. Around 600 vintage-suffixed services, no key, no authentication.
- **[Open Data BCN](https://opendata-ajuntament.barcelona.cat/data/api/action/package_search)** — ✅ `live` · `CC-BY-4.0` · _BCN_ · 🔌 `core:ckan`
  Barcelona municipal open data portal, CKAN-based. 555 datasets covering mobility, environment, demographics, economy, governance and urban fabric, entirely under CC-BY-4.0.
- **[Open Data Paris](https://opendata.paris.fr/api/explore/v2.1/catalog/datasets)** — ✅ `live` · `Open Database License (ODbL)`
  The City of Paris open-data portal (OpenDataSoft), 476 datasets across eight themes, every one of them under an open licence. Carries the city's budgets, procurement, workforce, environment and mobility data.
- **[Open Data Rennes Metropole](https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets)** — ✅ `live` · `Open Database License (ODbL)`
  Rennes and Rennes Metropole's open-data portal (OpenDataSoft), roughly 600 datasets, ODbL-dominant. One of the oldest French municipal open-data programmes and the source of the city's 2008-onward open budget series.
- **[Open Data Toulouse Metropole](https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets)** — ✅ `live` · `Licence Ouverte v2.0 (Etalab)`
  Toulouse Metropole's open-data portal (OpenDataSoft), 835 datasets and entirely openly licensed. The largest municipal catalogue found in the French wave, with a 218-dataset finance theme and a dedicated circular-economy theme.
- **[open.bydata - Stadt Augsburg](https://augsburg.bydata.de/)** — ✅ `live` · `Declared per distribution in DCAT-AP.de; sampled distribution is CC0-1.0`
  Augsburg's open data, published as two sub-catalogues of open.bydata, the Bavarian state open data portal: the city catalogue and the city statistics office catalogue, together the largest municipal holding on that portal.
- **[Paris - Marches publics (procurement register)](https://opendata.paris.fr/api/explore/v2.1/catalog/datasets?where=search%28%22marches%22%29)** — ✅ `live` · `Open Database License (ODbL)`
  Register of public contracts awarded by the Paris collectivite, plus the separate register for CASVP, the city's social-action agency. Published as open data on the city's own portal.
- **[Plymouth City Council spend over 500 pounds (2015 archive)](https://www.data.gov.uk/dataset/9e9b0128-9095-4bde-b24b-d04e60789016/plymouth-spend-over-f500-2015)** — ⛔ `deprecated` · `Open Government Licence v3.0`
  Transaction-level council payments above 500 pounds for four months of 2015, as CSV. Statutory transparency data, but the open-data publication stopped in 2015 while the council kept publishing elsewhere.
- **[Portal otvorenih podataka Grada Zagreba](https://data.zagreb.hr/dataset)** — ✅ `live` · `Otvorena dozvola (OD)`
  City of Zagreb open data portal, CKAN-based. 199 datasets covering city budget, local self-government funding, transport, utilities, kindergartens, air quality geodata and council composition.
- **[Portal Satu Data Denpasar](https://satudata.denpasarkota.go.id/dataset)** — ✅ `live` · `Lainnya (Domain Publik)` · _BLI_
  Kota Denpasar's municipal open data portal, CKAN 2.8.3, roughly 1,028 datasets across departmental organisations, published almost entirely under a public-domain licence.
- **[Seoul Participatory Budget - Project Execution (서울시 시민참여예산사업 예산집행 정보)](https://data.seoul.go.kr/dataList/OA-15413/S/1/datasetView.do)** — ⛔ `deprecated` · `이용허락범위 제한 없음 (no restriction on scope of use)`
  Links each citizen-proposed Seoul project to its allocated amount, its actual expenditure and its execution date, with plan documents and result reports attached. Covers proposal through allocation to spend in one table.
- **[Somerville - Participatory budgeting](https://data.somervillema.gov/d/brrj-v9a4)** — ✅ `live` · `Open Data Commons Open Database License (ODbL)` · _BOS_
  Full record of the City of Somerville participatory budgeting cycle: resident-submitted ideas with coordinates, voting results, and voter and submitter demographics.
- **[Somerville Open Data](https://data.somervillema.gov/)** — ✅ `live` · `Open Data Commons Open Database License (ODbL)` · _BOS_
  City of Somerville, Massachusetts open data portal on Socrata: a small, 52-dataset catalogue licensed ODbL, notable for participatory budgeting and the long-running municipal wellbeing survey.
- **[Statistics Finland Classification API](https://data.stat.fi/api/classifications/v2/)** — ✅ `live` · `CC-BY-4.0`
  Authoritative register of Finnish administrative codes as a REST API, versioned by year - kuntanumero (municipality), maakunta (region) and their correspondence tables. Returns per-code items as JSON.
- **[Transparenzportal Hamburg](https://suche.transparenz.hamburg.de/)** — ✅ `live` · `Datenlizenz Deutschland - Namensnennung - 2.0 (dl-de/by-2-0), declared per record`
  The Free and Hanseatic City of Hamburg's transparency portal: a CKAN catalogue that publishes datasets and, unusually, the administrative documents the Hamburgisches Transparenzgesetz compels the city and its bodies to disclose.

<!-- END GENERATED -->

---

## Distributed-production network

Sources specific to the fab-lab + maker network. Not in the four-pillar taxonomy because they describe the *infrastructure* doing the measuring rather than the phenomena being measured. Listed here for completeness.

- **[fablabs.io](https://www.fablabs.io/)** — registry of ~2,700 Fab Labs globally. Wired in PLANETAI.
- **[Wikifactory](https://wikifactory.com/)** — open hardware project repository.
- **[Precious Plastic Community Map](https://community.preciousplastic.com/map)** — distributed plastic-recycling workshops.
- **[Internet of Production Alliance — OKH/OKW](https://www.internetofproduction.org/)** — Open Know-How + Open Know-Where standards.
- **[OSHWA — Open Source Hardware Association](https://certification.oshwa.org/)** — certified open hardware registry.

---

## Contributing

We welcome contributions from anyone in the Fab City network — fab-lab managers, partner-city open-data leads, researchers, and anyone deploying instruments at any scale.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow. Short version: each entry is a YAML file. Validation runs in CI. The README is regenerated from the YAML by `scripts/build_readme.py`.

If you spot a stale entry, broken link, or licensing change, open an issue. Honest curation matters more than completeness.

## License

The curation work in this repository — entries, taxonomy, README — is licensed under [CC-BY-4.0](LICENSE). The build scripts in `scripts/` are MIT.

The datasets *linked from* this list are governed by their own respective licenses; see each entry's `license` field.

## Acknowledgements

This list is built on the shoulders of [`awesome-public-datasets`](https://github.com/awesomedata/awesome-public-datasets), the Fab City network's ten-plus years of metric-infrastructure work (Fab City Index 2018, 2024; Fab City Full Stack 2024; PLANETAI 2026), and the open-data communities of Barcelona, Boston, Santiago de Chile, and Bali. The Full Stack Metrics Framework [Vivanco 2024] underpins the taxonomy.

Maintained by [Fab City Foundation](https://fab.city/) and program contributors.
