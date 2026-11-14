---
name: company-deep-dive
description: Full research on one company or sector for the Market Tracker - industry structure, business, management, the last 4-5 earnings calls, growth triggers, moat, competition (listed and unlisted), risks, a scorecard and a 3-5 year valuation - written to the dashboard. Use for "deep dive on X", "research X for me", "should I look at X", a deep-dive request from the dashboard, or a sector study.
---

# Company deep dive

Builds on the sector-overview, competitive-analysis, catalyst-calendar and earnings-analysis skills in Anthropic's financial-services-plugins (Apache 2.0); see NOTICE.

Load `dashboard-writer` and `market-profile` first and use the company's market profile for sources, units, terms and red flags.

The goal is a decision aid the person can read in 10–15 minutes, not an analyst report. Each section answers its question directly, then gives the evidence.

## Before starting

- Confirm the exact company and symbol (or the sector's boundary and constituents).
- Read the person's `note` on the request, if any, and give that topic extra depth.
- Check `entries` for an earlier deep dive or first look on the same company. If there is one under 90 days old, build on it and say what changed rather than starting over.

## Sections

Write each as an entry section. Use tables where the content is a comparison.

1. **Industry**: size (with year and source), growth rate, how it's structured (fragmented or consolidated), sub-segments, where profit pools sit, and the main listed and unlisted players with approximate shares. What's changing (regulation, technology, demand) in the next 3–5 years.
2. **The business**: what it sells, to whom, segment mix of revenue and profit (table), unit economics, customer concentration, capacity and utilisation where relevant, 5-year revenue, operating margin, profit, ROCE and debt trend (table).
3. **Management**: who runs it and their record; promoter or founder holding and its trend; pledges; capital allocation (acquisitions, dividends, buybacks, capex outcomes); related-party dealings; remuneration vs profit; **say vs do**: what they guided over the last 2–3 years and what was delivered (table).
4. **Last 4–5 earnings calls**: a table with one row per quarter: guidance given, key numbers, main topics, tone, and what was later delivered. Then 3–5 bullets on how the story has shifted across the calls. Use the transcripts (exchange filings or investor relations pages). Paraphrase; quote at most a short phrase.
5. **Growth triggers**: specific, dated where possible (capacity coming online, new products, approvals, policy tailwinds, market share gains). For each, rough size of impact and how likely.
6. **Moat**: what kind, if any (brand, cost, network, switching costs, licences, distribution, scale). Show the evidence: ROCE above cost of capital for years, margins vs peers, share gains. Say plainly if there's no moat.
7. **Competition**: listed peers (table: revenue, growth, margin, ROCE, P/E, EV/EBITDA) and unlisted or foreign competitors from news, funding announcements and industry reports. Who is gaining and why.
8. **Risks**: industry risks and company risks separately, each with what would show it's happening. Run the profile's red-flag list and report every hit.
9. **Valuation**: run `valuation-model` and include its summary section and scenario table. Put its full output in a separate `valuation` entry if it's long.

## Scorecard

End with a table scoring 1–5, each with a one-line reason:

| Dimension | What it measures |
|---|---|
| Business quality and moat | Durability of returns |
| Cash flow quality | Operating cash flow vs profit, free cash flow conversion, working capital trend |
| Management and governance | Say vs do, capital allocation, treatment of minority shareholders |
| Growth | Visibility and size of growth over 3–5 years |
| Valuation | Price vs the base-case value from `valuation-model` |

Then 3 lines: the case for, the case against, and what to watch to tell which is playing out. No buy or sell call.

## Sector deep dive

Same structure, at sector level: industry (1), then a peer table across the constituents in place of sections 2–3, triggers, moats compared, risks, and a short valuation comparison by multiples. End with which 2–3 companies deserve a company deep dive and why.

## Writing it

- One `deep-dive` entry: `title` "Deep dive: <Company>", `headline` the one-sentence conclusion, `sections` as above, `mentions` with the company and every peer named, `sources` for every figure.
- Store the scorecard numbers in an extra `scores` field so later runs can track changes.
- If this came from a request, mark it done with `entryId`.
- Use real figures from filings and data pages, each with its period ("FY26", "Q2 FY27", "TTM"). If a number isn't available, say so; never estimate a historical figure.
- Do arithmetic (growth rates, margins, averages) in code where you can run code.
