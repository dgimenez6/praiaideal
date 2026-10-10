# PraiaIdeal

Static web app with beach suggestions for Búzios. GitHub Pages publishes the repository root; the custom domain is declared in `CNAME`.

## Recommendation logic

- The app keeps the beach-specific `prot` direction ranges and `critica` flags as manually curated site data. They reflect local beach geography and the owner's experience, including the shelter of Ferradura. Coordinates do not generate or overwrite these profiles.
- It ranks beaches using MET Norway's forecast wind direction and speed, the manual profiles, and a tide level interpolated between high/low points in a nearby port's tide table.
- It shows NOAA WaveWatch III as a broad offshore reference for surf beaches. Its grid is about 50 km, so the reading does not describe the conditions inside each bay or beach.
- Suggestions are approximate. They are not safety, rescue, navigation, or surf reports. Confirm conditions locally.

## Data and attribution

- **Weather and wind:** MET Norway Locationforecast. Its global forecast is based on ECMWF, uses roughly 9 km resolution outside the Nordics, and is updated four times a day. Data are available under CC BY 4.0, including commercial use. The page attributes MET Norway.
- **Tides:** Tábua de Maré API, which documents public no-key use (16 requests/minute, unlimited monthly quota) and a geolocation endpoint that selects a nearby port in Rio de Janeiro. It returns tide-table extrema and reports the source institution associated with the selected port. PraiaIdeal interpolates between those extrema to estimate an in-between level; it does not claim that interpolation is an observed or official hourly value.
- **Waves:** NOAA / PacIOOS WaveWatch III global forecast, approximately 0.5 degrees / 50 km resolution, displayed from an offshore point near Búzios. The dataset permits free use and redistribution but warns against legal or safety reliance; the app labels the limitation.
- **PIX:** Wallet quotes from ComparaPix's documented public, no-auth API, fetched server-side by GitHub Actions every 15 minutes. Data are published as `pix-quotes.json` and read from raw GitHub to avoid waiting for Pages rebuilds after bot commits. Compare `buy` ascending for the selected symbol, filter `isPix`, preserve provider links, disclose additional fees and attribution. The calculator multiplies the chosen BRL amount by each rate, without currency conversion or invented wallet margins.

Sources: [MET Norway](https://api.met.no/), [MET Norway license](https://docs.api.met.no/doc/License.html), [MET Norway terms](https://api.met.no/doc/TermsOfService), [Tábua de Maré docs](https://tabuamare.api.br/docs), [Tábua de Maré terms](https://tabuamare.api.br/termos), [NOAA / PacIOOS dataset and license](https://upwell.pfeg.noaa.gov/erddap/info/ww3_global/index.html).

## PIX freshness and operation

[ComparaPix API documentation](https://comparapix.ar/api.md) explicitly documents public developer access and server-side GET requests. No API key or paid subscription is used. This is not a contractual uptime or commercial license guarantee. The provider links are ComparaPix referral links; PraiaIdeal does not replace their referral parameters.

GitHub Actions schedules can be delayed. The UI displays each source timestamp and excludes provider-stale quotes, missing timestamps and data older than 60 minutes. A failed refresh preserves the previous JSON; expired data cannot become a current ranking. Refreshing the UI retrieves the latest published snapshot; it does not trigger an API fetch. GitHub Actions must be enabled and permitted to write repository contents. See the `Update PIX quotes` workflow for failures or manual refresh. The public API documentation has an inconsistent example saying `Max buy`; its core rule and actual site use **lowest buy**, which is implemented here.

## Privacy and offline behavior

The browser requests weather and wave data from the listed providers and PIX/tide snapshots from public GitHub files. Tide tables are refreshed at most once per day by the scheduled updater; snapshots older than 72 hours are rejected. Weather remains visible if tide data fail. Their servers may receive technical request data such as IP address and browser headers. No Google Analytics is loaded. The service worker caches only the static app shell; live conditions require a network connection.

## Deploy and smoke-check

No build step is required. GitHub Pages must publish the intended branch, with DNS/TLS active for `praiaideal.com`.

Check the Spanish, Portuguese, and English views; the displayed Búzios local time; tide-table and provider outage states; stable recommendations for unchanged inputs; the named reference port; and the offline shell.
## Activity planning and trail guide

`enhancements.js` adds relax/family/swimming/snorkeling/surf preferences without changing manual beach geography. Surf mode considers only owner-marked surf beaches. Other plans penalize exposed surf profiles; family and snorkeling preferences are transparent editorial choices, not safety or visibility measurements. Upcoming 09:00 and 15:00 slots use MET wind/air forecasts and interpolated tide tables, with each slot's date shown. Selecting a suggested beach displays its current conditions, not the future slot's conditions.

Seven trail cards include terrain, source links, preparation, reference map searches and published distance/time ranges where supported. Map searches are not verified trailheads or GPX routes. Current access, facilities and closures remain unconfirmed. Images are inherited site assets. No visitor reports or live parking/service availability are invented. Access notes cite Central Búzios; trail sources include the municipality, Cactus, RL Trips, Visit Búzios and the dated firsthand account linked on the Emerências card. Review date is 2026-10-10.
