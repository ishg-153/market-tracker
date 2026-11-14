# Market Tracker

A Claude plugin that keeps an eye on the stock market for you. Twice every weekday, a scheduled Claude run reads the market, checks every stock you own and every company you're watching, and writes a short brief to your own live dashboard. You add holdings, watch new companies, and ask for deep dives straight from that dashboard or in chat.

Built for the Indian market first (NSE, BSE, ₹ crore, FII/DII flows, concalls, promoter pledges), with the US included. Other countries can be added as market profiles.

> **Not investment advice.** Everything this plugin writes is research notes to help you make your own decisions. It never tells you to buy or sell.

## What you get

- **Morning brief** before the market opens and **evening wrap** after it closes: index levels, institutional flows, what matters today, and news on your holdings and watchlist.
- **Portfolio checks** against a red-flag list for each market (for India: pledges, auditor exits, SEBI action, rating downgrades, surveillance lists, dilution and more), measured against why you own each stock.
- **Watchlist** of companies and sectors. Add something at any time of day and the next run covers it.
- **Deep dives** on any company or sector: industry, business, management, the last 4–5 concalls, growth triggers, moat, competition, risks, a scorecard, and a bull/base/bear valuation.
- **One dashboard** that keeps every brief and deep dive, so past analysis stays in one place.

## Setting it up (one time)

You need a paid Claude plan (Pro, Max or Team) with scheduled tasks.

1. **Add the plugin.** In claude.ai or the Claude desktop app, go to **Customize → Plugins → Add → Add marketplace** and enter:
   ```
   ishg-153/market-tracker
   ```
   Turn on **Sync automatically** so you get improvements without doing anything. Then add **market-tracker** from the list.
2. **Run setup.** Start a new chat and say:
   > Set up my market tracker

   Claude asks which market you're in, what you hold (paste a list or attach your broker's holdings export), and what to watch. It then creates your dashboard.
3. **Schedule the briefs.** Setup gives you two short instructions, one for the morning brief and one for the evening wrap. Paste each into a new chat and click **Schedule** when Claude offers it (or use **Scheduled → New task**). They run in the cloud, so your computer can be off.

That's it. The first brief arrives at the next scheduled time, or ask for one right away.

## Using it

**On the dashboard**

- **Today**: the latest brief, with flags on anything that needs attention.
- **Portfolio**: your holdings with price, gain or loss, and open flags. Add, edit or mark a stock sold.
- **Watchlist**: add a company or sector, remove it with ✕, or ask for a deep dive.
- **History**: every brief and deep dive, searchable.
- **Requests**: deep dives, valuations and questions waiting for the next run.

Every company a brief mentions has **Watch** and **Deep dive** buttons next to it.

**In chat**, any time:

- "Start watching Tata Power" / "Keep an eye on the defence sector" / "Stop watching Zomato"
- "Deep dive on HAL" / "Value Infosys" / "Is Dixon expensive?"
- "Review my portfolio" / "Any red flags in my stocks?"
- "I bought 50 shares of ITC at 410"

## How it works

```
plugins/market-tracker/skills/
├── setup/              publishes the dashboard, records holdings, schedules the briefs
│   └── dashboard/      the dashboard page (HTML)
├── morning-brief/      the scheduled run: market, holdings, watchlist, requests
├── portfolio-watch/    news and red-flag checks per holding; full portfolio review
├── watch/              add or remove watchlist items from chat, with a first look
├── company-deep-dive/  full research on a company or sector
├── valuation-model/    bull/base/bear DCF, multiples, reverse DCF (scripts/dcf.py)
├── market-profile/     everything country-specific: india.md, us.md
└── dashboard-writer/   where data lives on the dashboard and how to write it
```

The dashboard is a Claude artifact with its own small database. The page and the scheduled runs read and write the same data, so a change on the page shows up in the next brief, and a new brief shows up on the page without reloading.

## For the maintainer

**Test locally** with Claude Code from the repo root:

```
claude plugin validate .
claude --plugin-dir plugins/market-tracker
```

**Ship a change**: edit the skills, bump `version` in `plugins/market-tracker/.claude-plugin/plugin.json`, commit and push. Installs with Sync automatically pick it up.

**Change the dashboard page**: edit `skills/setup/dashboard/index.html`, bump the `market-tracker-page` meta tag at the top, push, and have each user say "update my market tracker dashboard". Their data is kept; only the page changes. If you add or rename a field, update `dashboard-writer/data-model.md` in the same commit.

**Add a market**: copy `market-profile/markets/us.md`, fill it in, and add it to the table in `market-profile/SKILL.md`.

**Check before relying on it** (the parts that depend on what a scheduled run is allowed to do):

1. A scheduled run loads this plugin's skills.
2. A scheduled run can write to the dashboard's database (the `ArtifactData` tool).
3. Setup can publish the page from the plugin's folder (it falls back to copying the file first).
4. Prices and index levels from web search match the exchange closely enough for a brief.

## Credits

Some skills are adapted from Anthropic's [financial-services-plugins](https://github.com/anthropics/financial-services-plugins) (Apache 2.0). See NOTICE.
