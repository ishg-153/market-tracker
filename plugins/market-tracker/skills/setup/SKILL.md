---
name: setup
description: Set up the Market Tracker for someone - publish their interactive dashboard, record their market, holdings and watchlist, and schedule the morning and evening briefs. Also republishes the dashboard page when the plugin ships a new version. Use when someone says "set up my market tracker", "set up the stock tracker", "update my market tracker dashboard", or installs this plugin for the first time.
---

# Set up the Market Tracker

Load `dashboard-writer` and `market-profile` first. This skill has two modes:

- **First-time setup**: no Market Tracker dashboard exists for this person yet.
- **Update the page**: one exists, and the plugin's `dashboard/index.html` is newer than the one published (compare the `market-tracker-page` meta tag in the file with `config.pageVersion`).

Check which applies with `Artifact` `action: "list"` (look for a title starting "Market Tracker"). If one exists and the person didn't ask for a second dashboard, use update mode.

## First-time setup

Keep the conversation short. Ask everything in one message, with defaults filled in, so the person can answer in one reply:

1. **Home market**: India or US (others can be added later; see `market-profile`). Default India.
2. **Other markets** they hold or follow, if any.
3. **Holdings**: ask them to paste a list or attach their broker's holdings export (CSV or Excel). For each holding you need symbol, quantity and average buy price. Company name, buy date and "why I own it" are optional but make the daily checks better.
4. **Watchlist**: any companies or sectors to follow from day one.
5. **Brief times**: the profile's defaults (India 08:00 and 18:00 IST; US 08:00 and 17:00 ET), weekdays only. Ask only whether those work.
6. **Name** for the dashboard, default "Market Tracker".

### Reading a broker export

Columns differ by broker. Map them by meaning, then show the person a short table of what you read (symbol, name, qty, avg price) and ask them to confirm before writing anything.

- **ICICIdirect** uses its own stock codes, which often differ from NSE symbols (Reliance Industries is `RELIND` there, `RELIANCE` on NSE). Convert every code to the NSE symbol by looking up the company name, and list any you couldn't match.
- **Zerodha, Groww, Upstox and others** usually export NSE symbols already. Check a few.
- Drop rows with zero quantity. Combine duplicate rows for the same stock (sum quantity, weight the average price).
- Mutual funds, bonds and ETFs: ask whether to include them. The daily checks are built for listed company shares.

### Publish the dashboard

1. Publish this skill's `dashboard/index.html` with the `Artifact` tool:
   - `file_path`: the path to `dashboard/index.html` inside this skill's folder. If publishing from the plugin folder isn't allowed, copy the file unchanged into your working folder and publish the copy.
   - `capabilities`: `{"db": {}, "user": {}}`
   - `icon`: `"chart"`
   - `description`: "Daily market briefs, portfolio and watchlist, updated by scheduled Claude runs."
   Do not edit the file. The page's `<title>` stays "Market Tracker" so later runs can find it; the person's chosen name goes in `config.name` and shows on the page.
2. Note the URL the publish returns.

### Write the starting data

One `ArtifactData` `batch` (split into several if over 50 writes), following `dashboard-writer/data-model.md`:

- `config/main`: `name`, `homeMarket`, `markets`, `timezone` (the home profile's), `runs`, `dashboardUrl` (the URL above), `pageVersion` (from the file's `market-tracker-page` meta tag), `createdAt`.
- One `holdings/<MARKET>-<SYMBOL>` per confirmed holding, `status: "open"`, `updatedBy: "chat"`.
- One `watchlist/...` per watchlist item, `status: "active"`, `source: "chat"`.

Then read `config/main` back once to confirm the write landed.

### Schedule the briefs

The person needs two scheduled tasks, each running weekdays at their brief time in their time zone. Scheduled tasks run in the cloud, so their computer can be off.

If this session has a tool for creating scheduled tasks, create both. Otherwise, give the person these two instructions to paste, one at a time, into a new chat (Claude then offers to schedule it and they click **Schedule**), or into **Scheduled → New task** in the Claude app:

> **Market Tracker morning brief**, every weekday at <morning time> <time zone>:
> Use the market-tracker plugin. Run the morning-brief skill with run = morning for the dashboard at <dashboard URL>.

> **Market Tracker evening wrap**, every weekday at <evening time> <time zone>:
> Use the market-tracker plugin. Run the morning-brief skill with run = evening for the dashboard at <dashboard URL>.

Fill in the real URL and times. The URL in the task is how each run finds the dashboard.

### Finish

- Offer to run the first brief now so the dashboard isn't empty. If they agree, run `morning-brief` (choose `morning` or `evening` by the time of day in their market).
- Tell them, in a few lines: the dashboard link is in the card above; they can add and remove holdings and watchlist items on the page, tap **Watch** or **Deep dive** next to any company a brief mentions, and ask for things in chat ("start watching Tata Power", "deep dive on the defence sector").
- Remind them once that the briefs are research notes to inform their own decisions, not buy or sell advice.

## Update the page

When the plugin ships a newer `dashboard/index.html`:

1. Read the existing dashboard with `Artifact` `action: "read"` and its `url` (required before a publish to it).
2. Publish this skill's `dashboard/index.html` to that same `url`. Omit `capabilities` and `icon` so the artifact keeps what it has.
3. `update` `config/main` with the new `pageVersion` (pass its `version` as `if_version`).

All data (holdings, watchlist, history) stays: it lives in the dashboard's database, not in the page. Tell the person in one line what changed.
