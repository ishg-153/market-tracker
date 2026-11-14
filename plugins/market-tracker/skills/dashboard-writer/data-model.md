# Market Tracker data model

Collections in the dashboard's database. The page (`setup/dashboard/index.html`) reads exactly these fields; keep them in sync if either side changes.

## `config/main`

| Field | Type | Notes |
|---|---|---|
| `name` | string | Shown as the page title, e.g. "Market Tracker" |
| `homeMarket` | string | Profile code, `IN` or `US` |
| `markets` | string[] | Every market the person tracks, home first |
| `timezone` | string | IANA zone for display and run times, e.g. `Asia/Kolkata` |
| `marketMeta` | object | Only for markets beyond IN and US: `{CODE: {label, currency, locale, tz}}` |
| `runs` | object | `{morning: "08:00", evening: "18:00"}` in `timezone` |
| `dashboardUrl` | string | This artifact's URL, so any run can find its way back |
| `pageVersion` | string | Version of the page last published, e.g. `0.1.0` |
| `createdAt` | string | UTC ISO |

## `holdings/<MARKET>-<SYMBOL>`

| Field | Owner | Notes |
|---|---|---|
| `symbol` | person | Exchange symbol as traded (`TATAPOWER`, `AAPL`, `M&M`) |
| `market` | person | Profile code |
| `name` | person | Company name |
| `qty`, `avgPrice` | person | Numbers. `avgPrice` in the market's currency |
| `buyDate` | person | `YYYY-MM-DD` or null |
| `thesis` | person | Why they own it; the daily check measures news against this |
| `status` | person | `open` or `sold`; `soldAt` when sold |
| `lastPrice`, `lastPriceAt` | runs | Latest price you found and when it was quoted (UTC ISO) |
| `openFlags` | runs | `[{severity, text, since}]`: unresolved red flags. Replace the whole array each run; drop flags that are resolved |
| `lastCheckedAt` | runs | When a run last checked this holding |
| `addedAt`, `updatedAt`, `updatedBy` | both | `updatedBy` is `page`, `chat` or `run` |

## `watchlist/<MARKET>-<SYMBOL>` or `watchlist/<MARKET>-sector-<slug>`

| Field | Owner | Notes |
|---|---|---|
| `kind` | person | `company` or `sector` |
| `market`, `name`, `symbol` | person | `symbol` may be null when added from the page |
| `needsResolve` | page | true when the page couldn't confirm the symbol. A run fills `symbol` and sets this false |
| `reason` | person | Why it caught their eye |
| `status` | person | `active` or `removed`; `removedAt` |
| `source` | — | `page`, `chat` or `run` |
| `constituents` | runs | Sectors only: 3–8 listed symbols that define the sector for tracking |
| `lastSummary` | runs | One or two sentences from the latest check |
| `lastCheckedAt` | runs | UTC ISO |
| `addedAt` | — | UTC ISO |

## `requests/<auto id>`

| Field | Notes |
|---|---|
| `kind` | `deep-dive`, `valuation` or `question` |
| `target`, `symbol`, `market` | What it's about |
| `note` | What the person wants covered |
| `status` | `open`, `done` or `cancelled` |
| `createdAt`, `doneAt` | UTC ISO |
| `entryId` | The `entries` id holding the answer; the page links to it |
| `result` | Optional short line, e.g. "Skipped: symbol not found" |

## `entries/<yyyymmdd>T<hhmm>Z-<kind>[-<slug>]`

See section 4 of `SKILL.md`. Optional extra fields the page ignores but later runs can read: `valuation` (the numbers from `valuation-model`), `scores` (the deep-dive scorecard), `followUps` (things the next run should check).

## Limits

- 256 KB per document, 25,000 documents per dashboard. Two briefs a day is about 730 entries a year, so no pruning is needed for years.
- The page loads the latest 200 entries and 100 requests.
