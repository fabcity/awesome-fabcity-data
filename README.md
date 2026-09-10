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

### Region

- **[Occitanie — Panorama des énergies renouvelables](https://www.data.gouv.fr/datasets/panorama-des-energies-renouvelables)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Time series of renewable energy production in Occitanie, 2008-2024, compiled by the region from RTE, SDeS and ENEDIS sources. Fills the regional energy-mix cell of the FCI environmental pillar.

### City

- **[Boston - Greenhouse Gas Emissions inventory](https://data.boston.gov/dataset/greenhouse-gas-emissions)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  Annual citywide greenhouse gas inventory for Boston covering 2005 to 2021, published as three CSVs: community-wide emissions, local government operations emissions, and local government fuels.
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
- **[Occitanie — lycées et offre de formation](https://www.data.gouv.fr/organizations/region-occitanie)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Occitanie's open datasets on its upper-secondary schools and their training offer, including the mapped school register, the 2025-26 school-year list and the evolution of vocational course provision.
- **[WHO Open Data Repository](https://data.who.int/)** — ✅ `live` · `CC-BY-NC-SA-3.0-IGO` · _★_
  World Health Organization global health observatory + indicator repository. ~2,000 indicators across countries, themes, time.

### City

- **[Barcelona - Resultats electorals per seccio censal](https://opendata-ajuntament.barcelona.cat/data/api/action/package_show?id=est-eleccions-locals-seccio-censal)** — ✅ `live` · `CC-BY-4.0` · _BCN_
  Historical results for municipal, autonomic and general elections in Barcelona, published at census-section granularity - the finest official spatial unit below the district.


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
- **[DGFiP — Balances comptables des régions depuis 2010](https://www.data.gouv.fr/datasets/balances-comptables-des-regions-depuis-2010)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Accounting balances of every French region's principal and annexe budgets, 2010 onward, published by DGFiP. Fills the region rung of the public-budget ladder for all French Fab City members from one national file.
- **[Fabriqué en Occitanie — artisans et entreprises affiliés](https://www.data.gouv.fr/datasets/artisans-et-entreprises-affilies-a-la-marque-fabrique-en-occitanie)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Register of artisans and firms certified under Occitanie's regional made-here mark, with an accompanying product list. A rare open, named registry of locally manufacturing producers at regional scale.
- **[LAKLEMS — Latin America KLEMS](http://www.iadb.org/research/latin-american-klems-database)** — ✅ `live` · `custom open (IDB terms)` · _SCL_
  Sectoral productivity database for 18 Latin American economies. Capital, Labour, Energy, Materials, Services inputs at industry level. Maintained by IDB and partner institutions.
- **[Metroverse (Harvard Growth Lab)](https://metroverse.hks.harvard.edu/)** — ✅ `live` · `CC-BY-4.0` · _BCN · BOS · SCL_ · 🔌 wired in PLANETAI
  City-level economic-complexity dashboard covering ~1,200 metro areas. Industry employment, knowledge clusters, peer-city benchmarks, growth predictions.
- **[Région Occitanie — budgets primitifs, supplémentaires et comptes administratifs](https://www.data.gouv.fr/organizations/region-occitanie)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Occitanie's own voted budgets (primitif and supplémentaire) and executed comptes administratifs, published as M57 line-item files split between payment credits and multi-year programme authorisations.
- **[SICONFI DCA - Declaracao de Contas Anuais (estados e municipios)](https://www.tesourotransparente.gov.br/ckan/dataset/api-extrato-entes)** — ✅ `live` · `Open Data Commons Open Database License (ODbL)`
  Brazil's National Treasury annual accounts declaration for states and municipalities as a JSON API, keyed on the IBGE code. Gives the state-tier budget rung - gross realised revenue, deductions and transfers down.

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
- **[DGFiP Balances comptables des communes](https://www.data.gouv.fr/datasets/balances-comptables-des-communes-en-2024/)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Full DGFiP accounting balances for every French commune, covering principal and ancillary budgets (budgets principaux et budgets annexes), published yearly by the French finance ministry as CSV, JSON and ZIP.
- **[DGFiP Comptes individuels des communes (fichier global)](https://data.economie.gouv.fr/explore/dataset/comptes-individuels-des-communes-fichier-global-2023-2024/)** — ✅ `live` · `Licence Ouverte 2.0`
  DGFiP annual individual accounts for every French commune, published as one global file per year cohort on the Ministry of Finance open-data portal. Carries revenue, expenditure, debt and balance-sheet aggregates per commune.
- **[DGFiP — Balances comptables des groupements à fiscalité propre depuis 2010](https://www.data.gouv.fr/datasets/balances-comptables-des-groupements-a-fiscalite-propre-depuis-2010)** — ✅ `live` · `Licence Ouverte / Open Licence version 2.0`
  Accounting balances of French intercommunal groupings (EPCI — métropoles, communautés d'agglomération, communautés de communes), 2010 onward, from DGFiP. The only open source covering the EPCI fiscal tier nationally.
- **[Kota Denpasar - APBD (Ringkasan dan konsistensi RKPD-APBD)](https://satudata.denpasarkota.go.id/dataset?q=APBD)** — ✅ `live` · `Lainnya (Domain Publik)` · _BLI_
  Kota Denpasar publishes its annual budget summaries and RKPD-to-APBD consistency documents as CKAN datasets, mostly from BPKAD, in CSV with a public-domain licence.
- **[Paris - Budgets votes et comptes administratifs](https://opendata.paris.fr/api/explore/v2.1/catalog/datasets?where=theme%3D%22Administration%20et%20Finances%20Publiques%22)** — ✅ `live` · `Open Database License (ODbL)`
  The City of Paris finance corpus on its own open-data portal - voted budgets (planned) and comptes administratifs (executed) for principal and ancillary budgets, plus debt, fixed assets, grants paid and the balance sheet.
- **[Paris - Etats speciaux d'arrondissement (sub-municipal budgets)](https://opendata.paris.fr/api/explore/v2.1/catalog/datasets?where=search%28%22etats%20speciaux%22%29)** — ✅ `live` · `Open Database License (ODbL)`
  Paris publishes the etats speciaux d'arrondissement - the budget delegated to each of its arrondissements - as open data, both voted and executed. A rare case of public finance published BELOW the municipal tier.
- **[Rennes - Budgets primitifs et comptes administratifs](https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets?where=search%28%22budget%22%29)** — ✅ `live` · `Open Database License (ODbL)`
  Ville de Rennes publishes its budget primitif (planned) and compte administratif (executed) as separate yearly datasets from 2008 onward, split into principal budget, annexes and grants to associations.
- **[SICONFI RREO - Relatorio Resumido da Execucao Orcamentaria (municipios)](https://www.tesourotransparente.gov.br/ckan/dataset/api-rreo-entes)** — ✅ `live` · `Open Data Commons Open Database License (ODbL)`
  Brazil's National Treasury bimonthly budget-execution report for every one of the 5,570 municipalities, as a JSON API keyed on the IBGE municipality code. Carries planned and executed revenue and expenditure-by-function in one schema.
- **[Toulouse Metropole - Budgets primitifs et comptes administratifs](https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets?where=theme%3D%22Finance%22)** — ✅ `live` · `Licence Ouverte v2.0 (Etalab)`
  218 finance datasets on Toulouse Metropole's portal: budgets primitifs (planned) and comptes administratifs both alloue and realise (executed), for the city, the metropole and several member communes and their satellite budgets.

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
- **[Région Auvergne-Rhône-Alpes — données essentielles de la commande publique](https://www.data.gouv.fr/organizations/region-auvergne-rhone-alpes)** — ✅ `live` · `Licence Ouverte`
  Auvergne-Rhône-Alpes' statutory public-procurement award register, published continuously as one small JSON record per notified contract following the Etalab commande-publique schema.

### City

- **[Analyze Boston](https://data.boston.gov/dataset)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  City of Boston open data portal, CKAN-based. 235 datasets covering 311 service requests, budget and spending, building permits, employee earnings, food inspections, traffic and public safety.
- **[Bali Satu Data (provincial)](https://balisatudata.baliprov.go.id/search-data)** — ✅ `live` · `not stated` · _BLI_ · 🔌 wired in PLANETAI
  Provinsi Bali's Satu Data portal. Reachable and responding, but its search returns an empty state with no datasets listed by default, so its actual holdings could not be established.
- **[Barcelona - Perfil del contractant i relacio de contractistes](https://opendata-ajuntament.barcelona.cat/data/api/action/package_show?id=perfil-contractant)** — ✅ `live` · `CC-BY-4.0` · _BCN_
  Barcelona's public procurement register: tenders, bids, awards and contract formalisations from the last five years, updated daily, plus a contractors list with tax identifiers and amounts running back to 2012.
- **[Boston - Procurement and discretionary spending](https://data.boston.gov/dataset/city-of-boston-contract-award)** — ✅ `live` · `Open Data Commons Public Domain Dedication and License (PDDL)` · _BOS_
  City of Boston procurement transparency set: awarded contracts with equitable procurement reporting, a forward-looking buying plan, and departmental discretionary spending.
- **[Dados Abertos Belo Horizonte](https://dados.pbh.gov.br/dataset)** — ✅ `live` · `Creative Commons Attribution (564 of 606); Open Data Commons ODbL (23 of 606)`
  Belo Horizonte's municipal open data portal, CKAN 2.10.5. 606 datasets across planning, finance, mobility, health, education and environment, with a working CKAN action API and real-time consolidated revenue and expenditure feeds.
- **[Dados Abertos Recife](http://dados.recife.pe.gov.br/dataset)** — ✅ `live` · `Open Data Commons Open Database License (ODbL)`
  Recife's municipal open data portal, CKAN 2.11.5. 222 datasets, every one of them under ODbL, weighted towards health, mobility and education, published by named municipal secretariats.
- **[datos.gob.cl](https://datos.gob.cl/)** — ✅ `live` · `not stated` · _SCL_
  Chile's national open data portal, CKAN 2.10.4, publishing 3,211 datasets from 272 institutions including central government and many municipalities. Used as the Santiago pilot's open-data substrate.
- **[Open Data BCN](https://opendata-ajuntament.barcelona.cat/data/api/action/package_search)** — ✅ `live` · `CC-BY-4.0` · _BCN_ · 🔌 wired in PLANETAI
  Barcelona municipal open data portal, CKAN-based. 555 datasets covering mobility, environment, demographics, economy, governance and urban fabric, entirely under CC-BY-4.0.
- **[Open Data Paris](https://opendata.paris.fr/api/explore/v2.1/catalog/datasets)** — ✅ `live` · `Open Database License (ODbL)`
  The City of Paris open-data portal (OpenDataSoft), 476 datasets across eight themes, every one of them under an open licence. Carries the city's budgets, procurement, workforce, environment and mobility data.
- **[Open Data Rennes Metropole](https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets)** — ✅ `live` · `Open Database License (ODbL)`
  Rennes and Rennes Metropole's open-data portal (OpenDataSoft), roughly 600 datasets, ODbL-dominant. One of the oldest French municipal open-data programmes and the source of the city's 2008-onward open budget series.
- **[Open Data Toulouse Metropole](https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets)** — ✅ `live` · `Licence Ouverte v2.0 (Etalab)`
  Toulouse Metropole's open-data portal (OpenDataSoft), 835 datasets and entirely openly licensed. The largest municipal catalogue found in the French wave, with a 218-dataset finance theme and a dedicated circular-economy theme.
- **[Paris - Marches publics (procurement register)](https://opendata.paris.fr/api/explore/v2.1/catalog/datasets?where=search%28%22marches%22%29)** — ✅ `live` · `Open Database License (ODbL)`
  Register of public contracts awarded by the Paris collectivite, plus the separate register for CASVP, the city's social-action agency. Published as open data on the city's own portal.
- **[Portal Satu Data Denpasar](https://satudata.denpasarkota.go.id/dataset)** — ✅ `live` · `Lainnya (Domain Publik)` · _BLI_
  Kota Denpasar's municipal open data portal, CKAN 2.8.3, roughly 1,028 datasets across departmental organisations, published almost entirely under a public-domain licence.

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
