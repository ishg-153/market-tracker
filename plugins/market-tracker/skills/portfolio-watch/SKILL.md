---
name: portfolio-watch
description: Check the Market Tracker's holdings for news, results, red flags and opportunities, measured against why the person owns each stock. Runs inside every scheduled brief, and on its own for "review my portfolio", "any red flags in my stocks", "is my thesis on X still intact", or "how is my portfolio doing".
---

# Portfolio watch

Adapted from the thesis-tracker skill in Anthropic's financial-services-plugins (Apache 2.0); see NOTICE.

Load `dashboard-writer` and `market-profile` first. Each holding is checked under its own market's profile.

## Quick check (inside every brief)

For each open holding:

1. **Price**: latest price with time and source. Day's move in %.
2. **What's new since `lastCheckedAt`**: exchange or SEC filings, results, concall or earnings call, management commentary, rating actions, news that names the company. Ignore rehashed news and generic market commentary.
3. **Red flags**: go through the profile's red-flag list. Only flag what you found evidence for this run, with the source. Carry over earlier `openFlags` that still apply (keep their `since` date); drop ones that are resolved and say so once.
4. **Against the thesis**: if the holding has a `thesis`, say in one line whether today's news supports it, weakens it, or doesn't touch it. If there's no thesis, skip this; don't invent one.
5. **Opportunity**: a large fall with no bad news, results ahead of expectations, a new order or approval. Mark these `info`, not as a reason to buy.

Return for each holding: `lastPrice`, `lastPriceAt`, `openFlags` (`[{severity, text, since}]`), and one status line for the brief. Holdings with nothing new get no line in the brief text.

### Severity

- `high`: could change whether the person should keep holding it (governance, fraud allegations, auditor exit, pledge invoked, regulatory action, guidance withdrawn). Always also add it to the entry's `flags`.
- `medium`: worth reviewing this week (guidance cut, promoter or insider selling, key person exit, results miss, rating watch).
- `info`: useful context or an opportunity.

## Full review (on request)

When asked to review the portfolio, write a `portfolio-review` entry:

1. **Snapshot table**: each holding's invested amount, current value, gain or loss in % and amount, weight in the portfolio, and open flags. Separate tables per currency.
2. **Concentration**: any single stock above 15–20% of its currency's total, any sector above 30–35%, and how much sits in small caps. State the numbers; let the person judge.
3. **Thesis scorecard**: for each holding with a thesis, a row: thesis in short, what has happened since purchase, status (on track / behind / broken), trend.
4. **Catalyst calendar**: next results date, AGM, dividend record date, lock-in expiry, regulatory decision, for each holding in the next 90 days.
5. **Red flags**: everything open, worst first.
6. **What to look at**: up to three holdings that most deserve the person's attention this month, with the reason. No buy or sell instructions.

If the person asks about tax (India's capital gains, US short vs long term), give the rule with its source and the holding period from `buyDate`, and suggest they confirm with their tax adviser.

Do the arithmetic in code where you can run code. Never do sums in your head for money.

## Rules

- Evidence first: every flag cites a source from this run or an earlier entry.
- A holding without a symbol you can trade data on: flag it `info` "couldn't find market data for this symbol" and ask the person (in chat) or leave it flagged (scheduled run).
- Don't edit `qty`, `avgPrice`, `buyDate` or `thesis`. Those belong to the person.
