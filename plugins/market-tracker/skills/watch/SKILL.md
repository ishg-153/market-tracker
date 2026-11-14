---
name: watch
description: Add or remove companies and sectors on the Market Tracker watchlist from chat, at any time of day, and give a quick first look at anything newly added. Use when someone says "start watching X", "keep an eye on the X sector", "add X to my watchlist", "stop watching X", "what's on my watchlist", or picks something interesting out of a recent brief.
---

# Watch

Load `dashboard-writer` and `market-profile` first. The watchlist is read by every scheduled brief, so anything added here is covered from the next run. No new schedule is needed.

The person can also do all of this on the dashboard page itself. This skill is for doing it in conversation.

## Add

1. **Work out what they mean.**
   - A company: find its exchange symbol and market. If the name matches several listed companies (e.g. "Tata", "Adani", "Bajaj"), list the likely ones with symbols and ask which. If they named something from a recent brief, take it from that entry's `mentions`.
   - A sector or theme ("defence", "EV batteries", "regional banks"): define it in one line and pick 3–8 listed companies that represent it in that market, as `constituents`. Show them and let the person change the list.
   - Market: the company's listing; for a sector, the person's home market unless they say otherwise.
2. **Ask why**, briefly, only if they haven't said. One line is enough ("reason" on the watchlist). Skip if they seem in a hurry.
3. **Write it** to `watchlist/<MARKET>-<SYMBOL>` (company) or `watchlist/<MARKET>-sector-<slug>` (sector), `status: "active"`, `source: "chat"`, `addedAt`. If a document with that id exists and is `removed`, update it back to `active` instead.
4. **First look.** Unless they say they don't need it, write a `first-look` entry (keep it short):
   - Company: what it does and where the money comes from (segments); last two quarters' revenue and profit growth; margins; debt; valuation vs its own history and peers (P/E, EV/EBITDA); promoter or insider holding trend; the last month's news; and 3 things to watch. 
   - Sector: size and growth, the main listed players with one line each, what drives it now, main risks, what to watch.
   Put the companies named in `mentions`. Fill `lastSummary` on the watchlist item with one line from it.
5. Tell them it's on the watchlist, give the two or three most useful lines of the first look, and say the full first look is on the dashboard.

If they want the full analysis now, run `company-deep-dive` directly in the chat instead of queuing a request.

## Remove

Set `status: "removed"` and `removedAt`. Don't delete: past summaries stay in history, and the page lets them restore it. If the name matches more than one active item, ask which.

## List

Show active items grouped by market: name, symbol, why they added it, and the latest one-line summary.

## Holding vs watching

If they say they bought something on the watchlist, add it to `holdings` (ask for quantity and average price) and set the watchlist item to `removed` with `note: "Moved to holdings"`.
