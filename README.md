# Finplanr

A free, browser-based savings-plan calculator: split one monthly budget across ETFs, stocks, commodities (ETCs), crypto and savings accounts, lock positions, and see the result as euro amounts and percentages. English at `/`, German at `/de/`.

Live site: https://finplanr.net

**Not investment advice.** Finplanr is a planning tool with target amounts. It has no price feeds and no bank connection.

## Features
- Monthly budget with category and holding weights (whole euros or cents)
- Locks and "balance only with" partners, automatic sorting by size
- Interactive allocation donut (hover to enlarge, click to jump to the category)
- JSON backup/import, CSV export, personal reset point
- Optional online search for stocks, ETFs and crypto, an optional logo search (Wikimedia Commons) offered after adding a holding, and an optional TradingView chart (only after consent); holdings without a logo get a locally drawn letter badge
- Your data stays in your browser (localStorage); Finplanr itself sets no cookies of its own (technical cookies of the hosting provider's security features may exist, see the privacy policy)

## Build
The app itself is plain HTML, CSS and JavaScript without dependencies. A small Python 3 script (standard library only) assembles the deployable site in `dist/`: it generates the German page and the privacy-policy pages and injects the operator details (name, address, e-mail, Impressum link) from a local configuration file that is **not** part of this repository.

```bash
cp config/operator.example.json config/operator.json    # then edit config/operator.json (git-ignored)
python3 -I tools/build.py                                # creates dist/ (rebuilt from scratch on every run)
python3 -m http.server 8000 --directory dist             # preview at http://localhost:8000
```

Sources contain `{{PLACEHOLDERS}}` instead of personal data; `tools/build.py` replaces them and verifies the result. Run `python3 -I tools/check-repo.py` before every commit: it fails if any operator value, infrastructure detail or token-like string is about to be committed (`git config core.hooksPath .githooks` runs it automatically).

## Deployment
`dist/` is a static site: serve it with any web server. `docker-compose.example.yaml` shows a generic nginx setup (optionally behind a Cloudflare Tunnel, see `tunnel.env.example`); copy it to `docker-compose.yaml`, which is git-ignored together with `tunnel.env`. `config/default.conf` is the nginx configuration (security headers, caching, compression).

## Layout
| Path | Content |
|---|---|
| `site/` | Source of the static site (app, user guides, styles, images); contains placeholders |
| `parked-for-later/datenschutz-text.*.md` | Privacy-policy source texts (placeholders), rendered to HTML by the build |
| `config/operator.example.json` | Template for the local operator configuration |
| `config/default.conf` | nginx configuration |
| `tools/build.py` | Build: `site/` + configuration to `dist/` |
| `tools/check-repo.py`, `.githooks/` | Pre-commit safety check |
| `tools/og-image.html` | Source of the social preview image |
| `docker-compose.example.yaml`, `tunnel.env.example` | Generic deployment examples |

## Copyright
© 2026 Kerim Turacan. All rights reserved. This repository is published for viewing only: no copying, hosting or redistribution without permission. Contact via the Impressum on https://finplanr.net. See [LICENSE](LICENSE). Third-party names and logos belong to their respective owners.
