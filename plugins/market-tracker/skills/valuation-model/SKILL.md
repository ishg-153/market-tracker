---
name: valuation-model
description: Value a listed company for the Market Tracker with stated assumptions, segment-level growth, bull, base and bear scenarios over 3-5 years, a discounted cash flow, peer and historical multiples, and a reverse DCF showing what the current price assumes. Use for "value X", "what is X worth", "is X expensive", a valuation request from the dashboard, or step 9 of a deep dive.
---

# Valuation model

Adapted from the dcf-model and comps-analysis skills in Anthropic's financial-services-plugins (Apache 2.0); see NOTICE. The three-scenario structure follows common practice in community stock-analysis skills.

Load `market-profile` for the company's market: it sets the risk-free rate source, equity risk premium, terminal growth range, tax rate and units.

The output is a range with its assumptions in plain view, so the person can disagree with a specific number. It is not a price target.

## Steps

### 1. Gather (cite every figure)

- 5 years of history: revenue by segment, operating profit (EBIT), depreciation, capex, change in working capital, tax rate, net debt, share count (diluted).
- Current price (with time), market cap.
- Guidance from the last 2 earnings calls.
- Peer multiples (P/E, EV/EBITDA, EV/Sales, P/B for financials) and the company's own 5- and 10-year multiple range.
- Rates from the profile: risk-free rate and equity risk premium, looked up today. Beta from a public source, or a peer average.

### 2. Assumptions table

For each scenario (bear, base, bull), by segment where segments differ:

| Assumption | Bear | Base | Bull | Why |
|---|---|---|---|---|

Cover: revenue growth per segment for each forecast year (3 or 5 years), operating margin path, capex as % of revenue, working capital as % of revenue, tax rate, discount rate, terminal growth. The "Why" column cites history, guidance or industry data. The base case should follow guidance only where management has a record of delivering it (see the deep dive's say-vs-do).

### 3. Run the numbers

Use `scripts/dcf.py` in this skill's folder where you can run code (Python 3, standard library only):

```
python3 scripts/dcf.py inputs.json
```

`inputs.json` holds the base-year figures and one block per scenario; see the docstring at the top of the script for the exact fields. It returns, per scenario: projected free cash flow, enterprise value, equity value, value per share, upside or downside vs the current price, the share of value from the terminal year, and a sensitivity grid (discount rate ±1% by terminal growth ±1%). It also solves the reverse DCF: the revenue growth the current price implies under base-case margins.

If you can't run code, do the same steps carefully in a table and say that the arithmetic was done by hand.

Banks, insurers and NBFCs: don't use free cash flow. Use a P/B vs ROE framework or a dividend discount model instead and say so.

### 4. Cross-check with multiples

Apply peer and historical multiples to next year's base-case earnings or EBITDA. If the DCF and the multiples disagree by more than 30%, explain why in one or two lines.

### 5. Write it up

Sections for the entry (or for the deep dive's valuation section):

1. **Summary**: base-case value per share, the bear–bull range, the current price, and the reverse-DCF answer ("the current price assumes about X% revenue growth a year for 5 years, against Y% over the last 5"). This last line is often the most useful.
2. **Assumptions** table (above).
3. **Scenario results** table: value per share, upside or downside, terminal value share, for each scenario.
4. **Sensitivity** table for the base case.
5. **Multiples cross-check** table.
6. **What would change the answer**: the two or three assumptions the value is most sensitive to, and what to watch for each.

Save the structured numbers in the entry's extra `valuation` field (`{currentPrice, currency, scenarios: [{name, valuePerShare, upsidePct}], impliedGrowth, asOf}`) so later runs can compare. Write `kind: "valuation"` when it's its own entry.

## Rules

- Terminal growth never above the risk-free rate.
- If terminal value is more than 75% of enterprise value, say so: the answer depends mostly on the far future.
- Use diluted shares. Subtract minority interests; add cash and investments not used in operations.
- Units from the profile (₹ crore and ₹ per share for India; $M and $ per share for the US).
- No buy or sell calls. "Below the bear case" or "above the bull case" are facts the person can act on themselves.
