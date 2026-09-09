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
| **Status** | `live` · `stale` · `paywalled` · `deprecated` · `planned` |
| **Pillar** | environmental · social · economic · governance |
| **Scale** | planet · bioregion · region · city · community |
| **License** | SPDX where possible (CC-BY-4.0, ODbL-1.0, CC0, MIT) |
| **Pilots** | which PLANETAI pilots have non-trivial coverage |
| **Wired** | whether a connector is currently live in the [PLANETAI observatory](https://planetai.fab.city/observatory/) |

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
- **[Google Flood Hub](https://sites.research.google/floods/)** — ✅ `live` · `Google Maps Platform terms (free tier)` · _BLI · BCN · SCL · ★_ · 🔌 wired in PLANETAI
  Riverine flood forecasts up to 7 days ahead for ~80 countries including Indonesia, Spain, Chile. Inundation maps + alerts via free public API (rate-limited).
- **[Microsoft Aurora](https://microsoft.github.io/aurora/)** — ✅ `live` · `MIT (model weights); CDS license for ERA5 training inputs` · _★_ · 🔌 wired in PLANETAI
  Earth-system foundation model from Microsoft Research. Hourly forecasts to 14 days for atmosphere, ocean wave, and air quality state. Model weights released under MIT.
- **[NASA GISTEMP v4 — surface temperature analysis](https://data.giss.nasa.gov/gistemp/)** — ✅ `live` · `No formal license — acknowledgement expected; credit NASA GISS/GISTEMP` · _★_
  NASA GISS land-ocean surface temperature anomaly analysis. Global, hemispheric and zonal CSV tables plus 2x2 degree gridded NetCDF and Zarr anomaly fields relative to a 1951-1980 baseline.
- **[NOAA Global Monitoring Laboratory — CO2 trends](https://gml.noaa.gov/ccgg/trends/data.html)** — ✅ `live` · `No formal license — freely available to the public and the scientific community; citation requested` · _★_
  NOAA GML's canonical atmospheric CO2 record: Mauna Loa daily, weekly and monthly means plus the globally averaged marine surface annual mean, from the NOAA cooperative air sampling network.
- **[Open-Meteo](https://open-meteo.com/)** — ✅ `live` · `CC-BY-4.0` · _★_ · 🔌 wired in PLANETAI
  Free weather + climate API with no auth required. Backed by ECMWF + GFS + DWD + KNMI. Hourly forecasts to 14 days, historical reanalysis, climate projections, marine forecasts.
- **[UNEP IRP Global Material Flows Database](https://energydata.info/en/dataset/world-unep-irp-global-material-flows-database)** — ✅ `live` · `CC-BY-4.0` · _★_
  UNEP International Resource Panel material flow accounts: domestic extraction, direct trade and material footprint in raw-material equivalents by material category for 200+ countries. Compiled with CSIRO and WU Vienna.

### Bioregion

- **[Caravan — large-sample hydrology](https://github.com/kratzert/Caravan)** — ✅ `live` · `CC-BY-4.0` · _BLI · BCN · BOS · SCL_
  Community-curated large-sample hydrology benchmark dataset. Daily streamflow + meteorological forcing for ~7,000 catchments globally. Underlies most modern deep-learning hydrology research.
- **[ESA WorldCover](https://esa-worldcover.org/en/data-access)** — ✅ `live` · `CC-BY-4.0` · _★_
  ESA's 10 m global land cover map from Sentinel-1/2 with 11 classes including tree cover, shrubland, grassland, cropland and wetland. Delivered as Cloud-Optimized GeoTIFFs on a 1-degree grid.
- **[GBIF — Global Biodiversity Information Facility](https://www.gbif.org/)** — ✅ `live` · `CC-BY-4.0 (most records); some CC0; some CC-BY-NC` · _★_ · 🔌 wired in PLANETAI
  Aggregated species occurrence records from 2,000+ data publishers. ~3 billion records globally with a public REST API and bulk download via DOI. The de facto biodiversity backbone.
- **[Global Footprint Network — National Footprint & Biocapacity Accounts](https://www.footprintnetwork.org/licenses/public-data-package-free/)** — ✅ `live` · `CC-BY-SA-4.0 (registration and source acknowledgement required)` · _★_
  Free public data package of Ecological Footprint and biocapacity accounts for 195+ countries, run by Global Footprint Network. Carries per-capita gha footprint and biocapacity, land-type breakdown and data- quality scores.
- **[Global Forest Watch Data API — Hansen/UMD tree cover](https://data-api.globalforestwatch.org/datasets)** — ✅ `live` · `CC-BY-4.0 (per-dataset; other catalogue layers vary, several are non-commercial)` · _★_
  WRI's Global Forest Watch data API serving the Hansen/UMD 30 m global forest change products - annual tree cover loss and 2000/2010 tree cover density - plus a large catalogue of third-party layers.
- **[HydroSHEDS — HydroBASINS](https://www.hydrosheds.org/products/hydrobasins)** — ✅ `live` · `HydroSHEDS license — free for scientific, educational and commercial use with attribution` · _★_
  Global vector polygons of sub-basin boundaries, hierarchically nested across 12 levels with Pfafstetter coding and upstream/downstream topology. About 1.0 million sub-basin polygons covering 135 million square kilometres.
- **[ISRIC SoilGrids 2.0](https://www.isric.org/explore/soilgrids)** — ✅ `live` · `CC-BY-4.0` · _★_
  ISRIC World Soil Information's global digital soil mapping system. Machine-learned predictions of pH, organic carbon, bulk density, nitrogen, CEC and texture at 250 m across six standard depths.
- **[UNEP GEMS/Water Global Freshwater Quality Archive](https://zenodo.org/records/14230628)** — ✅ `live` · `CC-BY-4.0 (open archive; additional data available under CC-BY-NC-4.0)` · _★_
  UNEP GEMS/Water's global freshwater quality archive: over 20 million measurements across 608 parameters from 13,660 monitoring stations. Hosted by the International Centre for Water Resources and Global Change at the German Federal Institute of Hydrology.
- **[WRI Aqueduct 4.0 — Global Water Risk Atlas](https://www.wri.org/data/aqueduct-global-maps-40-data)** — ✅ `live` · `Creative Commons (variant not specified on the source page - verify before publishing derived values)` · _★_
  WRI's global water risk framework: 13 baseline annual and 3 baseline monthly indicators covering water stress, depletion, variability and quality, plus CMIP6-driven projections for 2030, 2050 and 2080.

### City

- **[Google Air Quality API](https://developers.google.com/maps/documentation/air-quality)** — 💲 `paywalled` · `Google Maps Platform terms (free quota tier available)` · _★_ · 🔌 wired in PLANETAI
  500m-resolution PM2.5 + AQI grid derived from regulatory stations, satellite, and modelling. Global coverage with hourly updates.
- **[OpenAQ](https://openaq.org/)** — ✅ `live` · `CC-BY-4.0` · _BCN · BOS · SCL · BLI · ★_ · 🔌 wired in PLANETAI
  Reference-grade air quality aggregator. Pulls from ~10k+ regulatory monitoring stations globally and harmonises to a common schema. Free public API with optional auth for higher rate limits.
- **[Sensor.Community](https://sensor.community/)** — ✅ `live` · `DbCL-1.0` · _BCN · ★_
  Citizen-science air quality sensor network rooted in Germany, active across the EU. ~30k SDS011-based PM sensors with public API and bulk archive download.

### Community

- **[AirGradient](https://www.airgradient.com/)** — ✅ `live` · `CC-BY-4.0 (data) + custom open (hardware)` · _★_
  Open-hardware indoor + outdoor air quality monitoring network with public REST API. PM2.5, PM10, CO2, TVOC, NOx, temperature, humidity. ~10k+ devices deployed globally; transparent pricing for the open variant.
- **[iNaturalist](https://www.inaturalist.org/)** — ✅ `live` · `CC-BY-NC (default per-observation; varies by uploader)` · _★_ · 🔌 wired in PLANETAI
  Community species observation platform. ~200M+ research-grade observations globally with photo verification by community identifiers. Used as the de facto biodiversity citizen-science layer.
- **[Smart Citizen](https://smartcitizen.me/)** — ✅ `live` · `CC-BY-SA-4.0 (data) + GPL-3.0 (firmware/hardware)` · _BCN · ★_ · 🔌 wired in PLANETAI
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

- **[GDELT — Global Database of Events, Language & Tone](https://www.gdeltproject.org/)** — ✅ `live` · `CC-BY-4.0` · _★_
  Real-time news event + tone time series in 100+ languages. Parses global news media to extract entities, themes, sentiment. ~150M events per year. Bulk download + BigQuery integration.
- **[IHME Global Burden of Disease](https://ghdx.healthdata.org/gbd-2021)** — ✅ `live` · `custom open (registration required)` · _★_
  Mortality + morbidity by cause × geography × age × year for ~370 diseases and injuries across ~200 countries. The de facto global health-burden time series.
- **[WHO Open Data Repository](https://data.who.int/)** — ✅ `live` · `CC-BY-NC-SA-3.0-IGO` · _★_
  World Health Organization global health observatory + indicator repository. ~2,000 indicators across countries, themes, time.


## Economic

### Planet

- **[Atlas of Economic Complexity (Harvard Growth Lab)](https://atlas.cid.harvard.edu/)** — ✅ `live` · `CC-BY-4.0` · _★_ · 🔌 wired in PLANETAI
  Global trade + economic-complexity indicators (ECI, product-space, diversification metrics) for ~250 countries × ~6,000 products. Bulk download via Dataverse; interactive web tool for exploration.
- **[Climate Funds Update](https://climatefundsupdate.org/data-dashboard/)** — ✅ `live` · `Not stated on the source page — freely downloadable, licence UNDECLARED` · _★_
  Independent monitor of multilateral climate finance run by ODI and Heinrich Boell Stiftung. Tracks money pledged, deposited and approved by fund, contributor country and recipient country, downloadable as Excel.
- **[Our World in Data — grapher CSV endpoints](https://ourworldindata.org/grapher/food-supply-kcal.csv)** — ✅ `live` · `CC-BY-4.0 for OWID's processing; upstream licences still apply to underlying values` · _★_
  OWID republishes FAOSTAT, World Bank and other series as clean, tidy, versioned CSVs at a stable URL pattern. Useful as the machine-readable escape hatch when an upstream agency's own API is unreachable.
- **[World Bank What a Waste 2.0](https://datacatalog.worldbank.org/search/dataset/0039597)** — ✅ `live` · `CC-BY-4.0` · _★_ · 🔌 wired in PLANETAI
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
- **[materialflows.net (UN International Resource Panel)](https://www.materialflows.net/)** — ✅ `live` · `custom open (UN IRP terms)` · _★_ · 🔌 wired in PLANETAI
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
- **[LAKLEMS — Latin America KLEMS](http://www.iadb.org/research/latin-american-klems-database)** — ✅ `live` · `custom open (IDB terms)` · _SCL_
  Sectoral productivity database for 18 Latin American economies. Capital, Labour, Energy, Materials, Services inputs at industry level. Maintained by IDB and partner institutions.
- **[Metroverse (Harvard Growth Lab)](https://metroverse.hks.harvard.edu/)** — ✅ `live` · `CC-BY-4.0` · _BCN · BOS · SCL_ · 🔌 wired in PLANETAI
  City-level economic-complexity dashboard covering ~1,200 metro areas. Industry employment, knowledge clusters, peer-city benchmarks, growth predictions.

### Community

- **[Fab Lab Activity Index (Boeing 2024)](https://link.springer.com/chapter/10.1007/978-3-658-44114-2_9)** — ✅ `live` · `CC-BY-4.0 (chapter, Open Access)` · _★_ · 🔌 wired in PLANETAI
  Per-lab activity baseline derived from the Fab Lab Census and fablabs.io registry. The first peer-reviewed quantitative index of distributed-production capacity at the community tier.


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

- **[ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)** — ✅ `live` · `custom open (ENTSO-E terms; free for non-commercial)` · _BCN_
  European electricity grid data: generation by source, consumption, cross-border flows, balancing, day-ahead prices. Hourly resolution for all EU + UK + Norway + Switzerland.
- **[Generalitat de Catalunya — Dades Obertes](https://analisi.transparenciacatalunya.cat/)** — ✅ `live` · `CC-BY-4.0` · _BCN_ · 🔌 wired in PLANETAI
  Catalan regional open data portal. Includes Estadistiques de residus municipals (per-capita waste, all 947 Catalan municipalities), Idescat IPC (consumer prices), Mercabarna figures, energy mix.
- **[MassGIS](https://www.mass.gov/orgs/massgis-bureau-of-geographic-information)** — ✅ `live` · `public` · _BOS_
  Massachusetts state geospatial data: parcels, buildings, transit network, hydrography, environmental constraints, election districts. Bulk download via state portal + ArcGIS REST services.

### City

- **[Analyze Boston](https://data.boston.gov/)** — ✅ `live` · `public` · _BOS_
  City of Boston open data portal. ~200 datasets covering 311 service requests, building permits, employee earnings, food inspections, traffic, public safety. CKAN-based.
- **[Bali Satu Data](https://balisatudata.baliprov.go.id/)** — ✅ `live` · `public (Indonesian government)` · _BLI_ · 🔌 wired in PLANETAI
  Bali provincial open data hub. Cross-domain datasets for the Bali pilot: demography, environment, economy, public services, customary-village indicators.
- **[datos.gob.cl](https://datos.gob.cl/)** — ✅ `live` · `public domain (Chilean government)` · _SCL_
  Chilean national open data portal. Datasets from across central government and many municipalities including Santiago. CKAN-based.
- **[Open Data BCN](https://opendata-ajuntament.barcelona.cat/)** — ✅ `live` · `CC-BY-4.0` · _BCN_ · 🔌 wired in PLANETAI
  Barcelona municipal open data portal. ~600 datasets covering mobility, environment, demographics, economy, governance, urban fabric. CKAN-based; full bulk + REST API.

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
