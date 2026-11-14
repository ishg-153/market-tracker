---
name: market-profile
description: Country-specific settings for the Market Tracker - indices, trading hours, currency and number format, news and filing sources, red flags and valuation defaults for each stock market (India and US so far). Load this before any market-tracker analysis so the work follows the right market's conventions.
---

# Market profiles

Every Market Tracker skill is market-neutral. What changes by country lives here, one file per market in `markets/`:

| Code | Market | File |
|---|---|---|
| `IN` | India (NSE, BSE) | `markets/india.md` |
| `US` | United States (NYSE, Nasdaq) | `markets/us.md` |

## How to use

1. Read the dashboard's `config/main` (see `dashboard-writer`). `homeMarket` is the person's main market. `markets` lists every market they track.
2. Read the profile file for `homeMarket`. If any holding, watchlist item or request has a different `market`, read that profile too, and apply each profile only to its own companies.
3. Follow the profile for: which indices and flows go in the snapshot, which sources to search first, how to write numbers, which red flags to check, and which valuation defaults to start from.
4. Anything a profile marks "look up" (interest rates, risk premiums, holiday calendars) changes over time. Look it up each time with a web search and cite it. Don't reuse a number from memory.

## Mixed portfolios

- Each holding is valued and flagged under its own market's profile.
- Never add amounts in different currencies together. Show a subtotal per currency. If the person asks for one total, convert at a rate you looked up that day, name the rate and its source, and keep the per-currency subtotals beside it.
- Briefs cover each market in its own section, home market first. Index snapshots list each market's indices with that market's name.
- A market that is closed (holiday, weekend, or outside hours at run time) gets one line saying so, not a full section.

## Adding a new market

Copy `markets/us.md` to `markets/<country>.md`, fill in every section, add a row to the table above, and add the market to `config.marketMeta` on the dashboard with `{label, currency, locale, tz}` (for example `{label: "UK", currency: "GBP", locale: "en-GB", tz: "Europe/London"}`) so the page can format it. Nothing else needs to change.
