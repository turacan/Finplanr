# Finplanr

A free, browser-based savings-plan calculator: split one monthly budget across ETFs, stocks, commodities (ETCs), crypto and savings accounts, lock positions, and see the result as euro amounts and percentages. English at `/`, German at `/de/`.

Live site: https://finplanr.net

**Not investment advice.** Finplanr is a planning tool with target amounts. It has no price feeds and no bank connection.

## Features
- Monthly budget with category and holding weights (whole euros or cents)
- The plan shown at first start is a marked example; "Create my own plan" starts an empty plan (budget and settings kept) with one-tap type buttons for the first category. Categories and holdings can be freely changed, added or removed; "+ Add holding" and "+ Add category" are always visible, Edit mode is for renaming, colours, symbols, ordering and deleting
- Locks and "balance only with" partners, automatic sorting by size
- Interactive allocation donut (hover to enlarge, click to jump to the category)
- "Rebalance" tab (next to the "Plan" tab; clicking the donut jumps back to the plan, `#rebalance` opens it directly): enter the current value of each holding (with a counted/not counted checkbox per holding and category) and see the difference to your plan's target shares, the one-time amount per holding needed to reach the target, and a month-by-month schedule for a chosen horizon with an optional extra one-time amount, each available as a CSV download (a calculation from the values you enter; values stay in your browser and in the JSON backup)
- JSON backup/import, CSV export, personal reset point
- Live search for a holding by name, ISIN, WKN or ticker across an instrument database of (essentially) the whole market: a static file generated at build time from openly reusable reference data (ESMA FIRDS; tickers from OpenFIGI and Wikidata), served from our own server and searched locally in the browser (no third-party request, no consent needed); results show type, currency and trading venues and can be narrowed with type buttons (All, ETF, ETC/ETN, Stocks, Funds; the search tab is called "Securities"), and an ISIN that is not in the database can still be added on its own
- Optional online search (Wikidata for stocks and ETFs, CoinGecko for crypto), an optional logo search (Wikimedia Commons) offered after adding a holding, and an optional TradingView chart (all only after consent); holdings without a logo get a locally drawn letter badge
- Your data stays in your browser (localStorage); Finplanr itself sets no cookies of its own (technical cookies of the hosting provider's security features may exist, see the privacy policy)

## Build
The app itself is plain HTML, CSS and JavaScript without dependencies. A small Python 3 script (standard library only) assembles the deployable site in `dist/`: it generates the German page and the privacy-policy pages and injects the operator details (name, address, e-mail, Impressum link) from a local configuration file that is **not** part of this repository.

```bash
cp config/operator.example.json config/operator.json    # then edit config/operator.json (git-ignored)
python3 -I tools/build.py                                # creates dist/ (rebuilt from scratch on every run)
python3 -m http.server 8000 --directory dist             # preview at http://localhost:8000
```

Sources contain `{{PLACEHOLDERS}}` instead of personal data; `tools/build.py` replaces them and verifies the result. Run `python3 -I tools/check-repo.py` before every commit: it fails if any operator value, infrastructure detail or token-like string is about to be committed (`git config core.hooksPath .githooks` runs it automatically).

Deploy helper (optional, WSL/Linux): `tools/deploy.sh site` builds and mirrors `dist/` into a mounted server folder, deleting stale files; `tools/deploy.sh check` runs a live check of the public site. Set the folder in `config/deploy.env` (copy `config/deploy.env.example`; git-ignored).

Wording guard: `python3 -I tools/check-wording.py` fails the build (and the pre-commit hook) if advice-like words appear in the built pages; `--src` also scans the sources. Finplanr only calculates from the values you enter. The banned words (EN + DE) and the small allowlist of disclaimer phrases are constants at the top of the script.

## Instrument data (search)
The search dialog reads `/data/instruments.v1.json` (first-party, loaded when the search opens, searched in the browser). The file is **generated, not committed**: `tools/fetch-instruments.py` downloads the reference data into `build-cache/` (git-ignored) and builds `build-cache/instruments.v1.json`; `tools/build.py` validates it and copies it unchanged to `dist/data/instruments.v1.json`.

```bash
python3 -I tools/fetch-instruments.py --refresh    # download the sources again and rebuild build-cache/instruments.v1.json
python3 -I tools/build.py                          # validate and copy it into dist/data/ (summary: build date, number of instruments)
```
The first run takes about 25 minutes (the free OpenFIGI API allows 25 requests per minute); its answers are cached for 30 days, so later runs take one to two minutes. Without the file the build still succeeds (with a warning) and the app falls back to a small built-in list plus the optional online search. File format: `{"v":1,"built","sources":[{id,name,date,attr,attr_de}],"venues":{MIC:name},"cols":["isin","name","wkn","ticker","type","ccy","venues"],"rows":[[...]]}` with the type codes `E` (ETF/ETP fund), `C` (ETC/ETN), `S` (stock), `F` (other fund), `O` (other). Refresh it regularly (ESMA publishes the full files weekly); the nginx configuration caches the index for one hour. The attribution shown in the search dialog and the privacy policy comes from the `sources` entries of the file.

**Data sources and licences (by default only sources that may be reused without asking anybody; details and quotes in the private notes):**

| Source | Used for | Licence status |
|---|---|---|
| [ESMA FIRDS](https://registers.esma.europa.eu) | ISIN, names, type, trading venues | Public by law (MiFIR Art. 27); the ESMA legal notice authorises reproduction if the source is acknowledged and changes are stated; listed on the EU Open Data Portal under the Commission reuse notice (Decision 2011/833/EU, commercial use included). Not endorsed by ESMA. |
| [OpenFIGI](https://www.openfigi.com) (Bloomberg) | Xetra ticker (ISIN to ticker) | FIGI identifiers are dedicated to the public domain; free API, no re-use restrictions stated. |
| [Wikidata](https://www.wikidata.org) | Nasdaq / NYSE ticker of US stocks | CC0. |
| WKN | German ISINs only | Calculated: the WKN is part of a `DE000...` ISIN. |

The Deutsche Börse "All tradable instruments" files (WKN and Xetra ticker for foreign ISINs) are **not** used by default: they come with no reuse licence. `python3 -I tools/fetch-instruments.py --with-xetra` adds them for private builds only; do not publish such a build unless Deutsche Börse has granted a licence. Consequence of the default: foreign instruments have no WKN in the search results (name and ISIN always).

## Deployment
`dist/` is a static site: serve it with any web server. `docker-compose.example.yaml` shows a generic nginx setup (optionally behind a Cloudflare Tunnel, see `tunnel.env.example`); copy it to `docker-compose.yaml`, which is git-ignored together with `tunnel.env`. `config/default.conf` is the nginx configuration (security headers, caching, compression, and an allowlist: only the site's own file types, `robots.txt` and the instrument index are served; dotfiles, backups, archives, scripts and other stray files answer 404). Copy only the contents of `dist/` to the served folder.

## Layout
| Path | Content |
|---|---|
| `site/` | Source of the static site (app, user guides, styles, images); contains placeholders |
| `parked-for-later/datenschutz-text.*.md` | Privacy-policy source texts (placeholders), rendered to HTML by the build |
| `config/operator.example.json` | Template for the local operator configuration |
| `config/default.conf` | nginx configuration |
| `tools/build.py` | Build: `site/` + configuration to `dist/` |
| `tools/fetch-instruments.py`, `tools/validate-instruments.py` | Instrument index: download of the official reference data and format check (see Instrument data) |
| `instrument-updater/` | `run.py`: the daily index refresh loop of the optional `instrument-updater` Docker service |
| `build-cache/` | Generated instrument index and raw downloads (git-ignored) |
| `data/` (in `dist/`) | Generated, not committed: `data/instruments.v1.json`, the instrument index served to the search |
| `tools/check-repo.py`, `.githooks/` | Pre-commit safety check |
| `tools/check-wording.py` | Wording guard: banned-word check of the built pages (see Build) |
| `tools/og-image.html` | Source of the social preview image |
| `docker-compose.example.yaml`, `tunnel.env.example` | Generic deployment examples |

## Copyright
© 2026 Kerim Turacan. All rights reserved. This repository is published for viewing only: no copying, hosting or redistribution without permission. Contact via the Impressum on https://finplanr.net. See [LICENSE](LICENSE). Third-party names and logos belong to their respective owners.
