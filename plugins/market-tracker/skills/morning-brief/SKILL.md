---
name: morning-brief
description: The Market Tracker's scheduled run - a morning brief before the market opens or an evening wrap after it closes, covering the market, every holding, the watchlist and any open requests, written to the person's dashboard. Use when a scheduled task says "run the morning-brief skill", or when someone asks for today's market brief, a market update, or "what happened in the market today".
---

# Morning brief and evening wrap

Adapted from the morning-note and thesis-tracker skills in Anthropic's financial-services-plugins (Apache 2.0); see NOTICE.

The input names the run: `morning` (before the open) or `evening` (after the close). If not given, pick by the current time in the home market.

A brief is read in two minutes on a phone. Lead with the one thing that matters most. "Nothing material changed" is a valid and useful brief.

## Steps

### 1. Load context

- Load `dashboard-writer` and follow it to find the dashboard and read config, open holdings, active watchlist, open requests and the last few entries.
- Load `market-profile` and read the profile for each market in play.
- Skim the last morning and evening entries so you don't repeat old news as new, and so you can follow up on anything they said to watch.

If a market is closed today (weekend or holiday per its profile), write one line for it and skip its snapshot and price updates.

### 2. Market snapshot

From the profile's snapshot list. Search the web; take every number with its time and source.

- **Morning**: previous close for each index, the pre-market indicator (GIFT Nifty for India, futures for the US), overnight global moves, flows from the previous session, today's calendar.
- **Evening**: today's close and % change for each index, the day's flows, sector moves that stood out, what drove the day in one or two sentences, tomorrow's calendar.

Write indices into `snapshot.indices` as numbers (`value`, `changePct`). If two sources disagree on a level, use the exchange's own figure or say "approx." in `note`.

### 3. Holdings

For each open holding, follow `portfolio-watch` (quick check). It returns: latest price, any news since the last run, any red flags, and a one-line status. Keep it short for holdings with nothing new: they appear only in the table, not in the text.

### 4. Watchlist

For each active item:

- **Company**: news, results or filings since the last check, and price move. One or two sentences into `lastSummary`. If `needsResolve` is true or `symbol` is empty, find the exchange symbol first, set it, and set `needsResolve: false`. If you can't identify the company, say so in `lastSummary` and leave it for the person to fix.
- **Sector**: if it has no `constituents`, pick 3–8 listed companies that best represent it in that market and save them. Then one line on how the sector did and any news that moves it. Once a week (Monday morning run), a short paragraph instead.
- If something on the watchlist looks worth a closer look (results beat, big fall, a new trigger), add a `medium` or `info` flag with the reason. Don't open a deep dive request yourself; the person decides.

### 5. Open requests

Handle at most **one deep dive and one valuation per run**, oldest first, so the run stays manageable. Questions are short: answer all of them.

- `deep-dive`: run `company-deep-dive` and write its entry.
- `valuation`: run `valuation-model` and write its entry.
- `question`: answer in a short `answer` entry with sources.

Mark each handled request `status: "done"`, `doneAt`, `entryId`. Leave the rest open; mention in the brief how many are queued. If a request can't be done (company not found, no data), mark it done with a `result` line saying why.

### 6. Write the entry

One entry, `kind` `morning` or `evening`, title like "Morning brief · Fri 14 Nov" or "Evening wrap · Fri 14 Nov".

**Morning sections**:

1. `What matters today`: 2–4 bullets, most important first. Include why it matters to this person's holdings.
2. `Your holdings`: only holdings with news or flags. One bullet each: what happened, why it matters, what to watch.
3. `Watchlist`: one bullet per item with something new.
4. `Today's calendar`: results, policy decisions, data releases with times in the person's time zone.

**Evening sections**:

1. `What happened`: what moved the market and why, in 2–4 bullets.
2. `Your holdings`: the day's move for each holding that moved more than ±3% or had news; one bullet each.
3. `Flows`: institutional flows and what they suggest, one or two lines.
4. `Watchlist`: anything new.
5. `Tomorrow`: what's scheduled.

Also fill `headline`, `snapshot`, `flags` (from holdings and watchlist checks), `mentions` (every company and sector named, so the person can tap Watch or Deep dive), and `sources`.

### 7. Write everything back

One `ArtifactData` batch with:

- the new entry;
- each holding's `lastPrice`, `lastPriceAt`, `openFlags`, `lastCheckedAt` (`update`, pinned to the version you read);
- each watchlist item's `lastSummary`, `lastCheckedAt`, and any resolved `symbol` or `constituents`;
- requests marked done.

If the batch fails because the person changed something during the run, re-read those documents and retry once with their changes kept.

## Rules

- **Never invent a number.** Every price, index level, flow figure and financial comes from a source you found this run, with its time. If you couldn't find it, write "not found" and move on.
- **Prices are delayed** in web results. Say "as of <time>".
- **Don't give buy or sell calls.** Use "watch", "review", "worth a closer look". Size urgency through flag severity, not through instructions.
- **Follow up on yesterday.** If the last brief said "watch for X", say whether X happened.
- Keep the whole entry under about 40 KB. Long detail belongs in a deep dive, not the brief.
- At the end of a scheduled run, the run's summary is the headline plus any `high` flags, so the person sees them in their notification.
