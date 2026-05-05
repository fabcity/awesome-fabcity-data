# awesome-fabcity-data

> A curated, network-maintained inventory of open data sources for measuring distributed production at every scale — from a single fab lab to the planet.

Maintained by the **Fab City** network. Organised by the [**Vivanco Full-Stack Metrics framework**](#the-taxonomy): four pillars — Environmental, Social, Economic, Governance — across five scales — Planet, Bioregion, Region, City, Community.

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

The four pillars × five scales come from Laura Vivanco's *Full-Stack Metrics for Fab Cities* (2024–25), which operationalises Tomas Diez's *Fab City Full Stack* (Diez, Niaros, Ferro 2024). They are not a replacement for ESG, SDG, or doughnut economics — they are a way to organise *where measurement happens* in a distributed-production network.

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

- **[Google Flood Hub](https://sites.research.google/floods/)** — ✅ `live` · `Google Maps Platform terms (free tier)` · _BLI · BCN · SCL · ★_ · 🔌 wired in PLANETAI
  Riverine flood forecasts up to 7 days ahead for ~80 countries including Indonesia, Spain, Chile. Inundation maps + alerts via free public API (rate-limited).
- **[Microsoft Aurora](https://microsoft.github.io/aurora/)** — ✅ `live` · `MIT (model weights); CDS license for ERA5 training inputs` · _★_ · 🔌 wired in PLANETAI
  Earth-system foundation model from Microsoft Research. Hourly forecasts to 14 days for atmosphere, ocean wave, and air quality state. Model weights released under MIT.
- **[Open-Meteo](https://open-meteo.com/)** — ✅ `live` · `CC-BY-4.0` · _★_ · 🔌 wired in PLANETAI
  Free weather + climate API with no auth required. Backed by ECMWF + GFS + DWD + KNMI. Hourly forecasts to 14 days, historical reanalysis, climate projections, marine forecasts.

### Bioregion

- **[Caravan — large-sample hydrology](https://github.com/kratzert/Caravan)** — ✅ `live` · `CC-BY-4.0` · _BLI · BCN · BOS · SCL_
  Community-curated large-sample hydrology benchmark dataset. Daily streamflow + meteorological forcing for ~7,000 catchments globally. Underlies most modern deep-learning hydrology research.
- **[GBIF — Global Biodiversity Information Facility](https://www.gbif.org/)** — ✅ `live` · `CC-BY-4.0 (most records); some CC0; some CC-BY-NC` · _★_ · 🔌 wired in PLANETAI
  Aggregated species occurrence records from 2,000+ data publishers. ~3 billion records globally with a public REST API and bulk download via DOI. The de facto biodiversity backbone.

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
- **[World Bank What a Waste 2.0](https://datacatalog.worldbank.org/search/dataset/0039597)** — ✅ `live` · `CC-BY-4.0` · _★_ · 🔌 wired in PLANETAI
  National-level municipal solid waste accounts: per-capita generation, composition, collection, treatment. Coverage for ~217 economies.

### Bioregion

- **[materialflows.net (UN International Resource Panel)](https://www.materialflows.net/)** — ✅ `live` · `custom open (UN IRP terms)` · _★_ · 🔌 wired in PLANETAI
  Economy-wide material flow accounts published by the UN International Resource Panel. National-level material extraction, imports, exports, consumption by category.

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

- **[OONI — Open Observatory of Network Interference](https://ooni.org/)** — ✅ `live` · `CC-BY-NC-SA-4.0` · _★_
  Country-level measurement of internet censorship and traffic interference. Open data archive of probes from ~30k volunteers across 200+ countries. The empirical baseline for measuring state-level interference with the data substrate a federation runs on.

### Bioregion

- **[ChileCompra](https://www.chilecompra.cl/)** — ✅ `live` · `public domain` · _SCL_
  Chilean national public-procurement portal. All government procurement lifecycle: bases de licitacion, ofertas, adjudicaciones. Public REST API + bulk download.
- **[LKPP / SPSE — Indonesian National Procurement](https://www.lkpp.go.id/)** — ✅ `live` · `public (Indonesian government)` · _BLI_
  Indonesian Lembaga Kebijakan Pengadaan Barang/Jasa Pemerintah (LKPP) operates SPSE, the national e-procurement system. Public tender data for central government and most regional bodies including Bali province.
- **[TED — Tenders Electronic Daily](https://ted.europa.eu/)** — ✅ `live` · `CC-BY-4.0` · _BCN_
  Every public-tender notice published in the EU. Full procurement lifecycle: notice published, bid deadline, award, completion. Bulk download via Open Data Portal of the EU; daily updates.

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

This list is built on the shoulders of [`awesome-public-datasets`](https://github.com/awesomedata/awesome-public-datasets), the Fab City network's ten-plus years of metric-infrastructure work (Fab City Index 2018, 2024; Fab City Full Stack 2024; PLANETAI 2026), and the open-data communities of Barcelona, Boston, Santiago de Chile, and Bali. The Vivanco Full-Stack Metrics framework underpins the taxonomy.

Maintained by [Fab City Foundation](https://fab.city/) and program contributors.
