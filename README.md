# PraiaIdeal

Static web app with beach suggestions for Búzios. The site is hosted from the repository root and uses the custom domain declared in `CNAME`.

## Current behavior

- Shows weather and marine forecasts from Open-Meteo for beaches in Búzios.
- Displays `sea_level_height_msl` as a model-estimated anomaly above mean sea level. The high/medium/low label compares the current estimate with the next 24 forecast hours; it is not an official tide table.
- Ranks beaches deterministically using forecast wind direction, hand-entered beach protection ranges (`prot`), and a hand-entered sensitivity flag (`critica`) together with the modeled sea-level range. These beach profiles are owner-curated from local geography and experience (for example, Ferradura is enclosed and more sheltered); the app does not infer them from coordinates. Preserve those values when changing recommendation logic. The result is a suggestion, not a safety assessment.
- Shows an approximate ARS-per-R$1 conversion derived from USD/ARS and USD/BRL references. It does not compare actual wallet offers or guarantee a rate.
- Provides a static offline shell through `sw.js`; forecasts and exchange data still require a network connection.
- Does not load Google Analytics. Third-party services used by the page are listed in `privacidade.html`.

## Data sources and attribution

Open-Meteo provides weather and marine forecasts. Its Marine API documentation says sea-level height includes tidal effects, is referenced to global mean sea level, can be unreliable in coastal areas, and must not be used for coastal navigation. The marine forecast attribution must credit DWD and Open-Meteo. PraiaIdeal shows that attribution in the page footer. The beach protection/sensitivity profiles are manually curated site content, not API output.

Exchange reference providers: DolarApi (USD/ARS crypto reference) and ExchangeRate-API (USD/BRL). Their output is labelled as an approximate conversion, not a live wallet quote.

## Important before monetizing

Open-Meteo's public pricing page says the free endpoint is for non-commercial use and its paid plans provide a commercial-use license. This site contains advertising/contact and PIX-support features, so confirm the intended use with Open-Meteo and obtain the appropriate license before commercial operation. If a paid API key is needed, do not place it in this public static repository; add a server-side proxy or equivalent protected runtime first.

## Deploy and smoke-check

The repository is a static site; no build step is required. GitHub Pages must publish the intended branch and the DNS/TLS for `praiaideal.com` must be active.

Before publishing, check:

1. The page loads at desktop and mobile widths.
2. Spanish, Portuguese, and English labels update without changing the selected beach.
3. The displayed time is Búzios time even when the browser device uses another timezone.
4. When APIs are blocked, the page shows an error and never invents weather or tide values.
5. Repeated loads with the same conditions return the same beach ranking.
6. The tide label is visibly described as an estimate and the DWD/Open-Meteo attribution appears.
7. The installed/offline shell opens; forecast values are not presented as fresh while offline.
8. The PIX section shows only the approximate conversion reference, not wallet-specific “best rates”.
9. The privacy page is reachable, and no analytics request is made.
