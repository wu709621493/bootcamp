# In-City Metrics Estimation Framework for Chinese Cities

A concise set of measurable indicators to benchmark livability, inclusiveness, and sustainability within Chinese cities. Metrics emphasize locally available data (e.g., Gaode/AMap transit GTFS, MEE air-quality feeds, National Bureau of Statistics releases, city open-data portals) and can be updated quarterly or monthly depending on data cadence.

## 1. Mobility & Access
- **15-Minute Basic Services Coverage**: share of residents within 15 minutes' walk of a community clinic, wet market, primary school, and park; compute via population-weighted isochrones on 250–500 m grids.
- **Transit Speed Reliability**: median vs. 90th percentile bus travel time ratio on top 20 routes during peak hours using GPS pings; values closer to 1 indicate reliability.
- **Universal Access Score**: percentage of metro/bus stops with step-free access, tactile paving continuity, and audible/visual announcements; weight metro/bus 40/60 based on passenger volumes.
- **Shared-Mobility Saturation**: bikes/scooters per 1,000 residents within built-up area, adjusted by parking compliance rate (dock/geo-fence adherence).

## 2. Environment & Public Health
- **PM2.5 Exposure Hours**: annual hours when PM2.5 exceeds 35 µg/m³ averaged over stations; combine with population distribution to report person-hours of exposure.
- **Urban Heat Risk Index**: composite of land surface temperature percentile, tree canopy coverage, and vulnerable population density (65+, outdoor workers); report by subdistrict to target cooling measures.
- **Per-Capita Green Space**: public green area (parks, greenways, riverfronts) divided by resident population; include pocket parks (>400 m²) to reflect fine-grain livability.
- **Blue-Green Connectivity**: share of continuous shaded pedestrian/bicycle corridors (>1 km) that link parks/waterfronts to transit hubs, measured as % of corridor length meeting 40% canopy coverage.

## 3. Housing & Affordability
- **Rent-to-Income Ratio**: median monthly rent of 60–90 m² units divided by median disposable income of renters; track by district to detect displacement pressure.
- **Public Housing Access**: eligible households vs. actual allocations and occupancy rates of保障性租赁住房/公租房; include average wait time to highlight backlog.
- **Eviction/Relocation Stability**: annual evictions or redevelopment relocations per 1,000 households, with compensation adherence rate (actual/contracted payouts).

## 4. Equity & Well-Being
- **Health Services Reach**: average travel time (public transit + walk) to tiered hospitals and community health centers for the lowest-income quintile vs. citywide median.
- **Education Opportunity Gap**: variance in compulsory education quality proxies (teacher-student ratio, school facility scores) across districts; lower variance reflects equity.
- **Care Infrastructure Density**: eldercare and childcare slots per 1,000 residents, disaggregated by affordability tiers; track utilization to avoid idle capacity.

## 5. Safety & Resilience
- **Vision Zero Progress**: traffic fatalities per 100,000 people and per 100 million vehicle-km; map high-injury corridors to prioritize calming interventions.
- **Flood Resilience Score**: percentage of roads/intersections with effective drainage and sponge-city features (permeable pavement, bioswales); pair with modeled ponding depth for 50- and 100-year storms.
- **Emergency Response Time**: median dispatch-to-arrival times for EMS and fire services by district during peak and off-peak periods; include 90th percentile to capture tails.

## 6. Governance & Participation
- **Open Data Freshness**: share of key datasets (transit GTFS, air quality, land use, permits) updated within mandated cadence (e.g., weekly/monthly); counts as on-time vs. stale.
- **Community Feedback Closure**: percentage of citizen-reported issues (road defects, noise, accessibility gaps) resolved within SLA; include median closure days and re-open rate.
- **Budget Transparency**: publication rate of project-level urban investment (PPP, metro expansions, park upgrades) with spend vs. plan variance.

## 7. Implementation Notes
- Use **1 km² tiles** or **subdistricts** (街道/乡镇) as default spatial units to allow comparison while respecting privacy.
- Provide **confidence bands** for survey- or model-based metrics (e.g., ±5% for rent estimates) and annotate data gaps explicitly.
- Publish a **public dashboard** with drill-downs for vulnerable groups (older adults, low-income, persons with disabilities) to ensure metrics drive inclusive policy decisions.
