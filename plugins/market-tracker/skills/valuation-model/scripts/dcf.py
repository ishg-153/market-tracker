#!/usr/bin/env python3
"""Three-scenario DCF with sensitivity grid and reverse DCF. Standard library only.

Usage:  python3 dcf.py inputs.json            (prints JSON results)

All money amounts and the share count must use the same scale, e.g. Rs crore and
crore shares (India) or $ million and million shares (US). Value per share then
comes out in the currency's units.

inputs.json:
{
  "company": "Example Ltd",
  "currency": "INR",
  "currentPrice": 450.0,            # per share, same currency
  "shares": 320.0,                  # diluted share count (same scale as amounts)
  "netDebt": 1200.0,                # debt minus cash; negative for net cash
  "minorityInterest": 0.0,          # optional
  "nonOperatingAssets": 0.0,        # optional: investments etc. not in the forecast
  "baseRevenue": 10000.0,           # last full year; optional when every scenario uses segments
  "scenarios": {
    "base": {
      "years": 5,                                   # optional; else taken from growth lists
      "revenueGrowth": [0.12, 0.12, 0.11, 0.10, 0.10],   # or one number for every year
      "segments": [                                  # optional, replaces revenueGrowth
        {"name": "Power", "baseRevenue": 6000, "growth": 0.08},
        {"name": "Renewables", "baseRevenue": 4000, "growth": [0.25, 0.22, 0.2, 0.18, 0.15]}
      ],
      "ebitMargin": [0.14, 0.145, 0.15, 0.15, 0.15],  # or one number
      "taxRate": 0.2517,
      "daPctRevenue": 0.04,          # depreciation & amortisation
      "capexPctRevenue": 0.06,
      "nwcPctRevenue": 0.10,         # net working capital as % of revenue
      "discountRate": 0.12,          # WACC (or cost of equity for an unlevered, cash-rich firm)
      "terminalGrowth": 0.05
    },
    "bear": {...}, "bull": {...}
  }
}
"""
import json
import sys


def _series(v, n, name):
    if isinstance(v, (int, float)):
        return [float(v)] * n
    if isinstance(v, list) and len(v) >= n and all(isinstance(x, (int, float)) for x in v[:n]):
        return [float(x) for x in v[:n]]
    raise ValueError(f"{name} must be a number or a list of at least {n} numbers")


def _years(sc):
    if "years" in sc:
        return int(sc["years"])
    if isinstance(sc.get("revenueGrowth"), list):
        return len(sc["revenueGrowth"])
    for seg in sc.get("segments", []):
        if isinstance(seg.get("growth"), list):
            return len(seg["growth"])
    return 5


def revenues(sc, base_revenue, n, growth_override=None):
    """Return (base total revenue, list of projected total revenues, per-segment detail)."""
    if growth_override is not None:
        rev, out = base_revenue, []
        for _ in range(n):
            rev *= 1 + growth_override
            out.append(rev)
        return base_revenue, out, None
    if sc.get("segments"):
        detail, totals = [], [0.0] * n
        base_total = 0.0
        for seg in sc["segments"]:
            g = _series(seg["growth"], n, f"segment {seg.get('name')} growth")
            r = float(seg["baseRevenue"])
            base_total += r
            path = []
            for y in range(n):
                r *= 1 + g[y]
                path.append(r)
                totals[y] += r
            detail.append({"name": seg.get("name"), "revenue": [round(x, 2) for x in path]})
        return base_total, totals, detail
    if base_revenue is None:
        raise ValueError("baseRevenue is required when a scenario has no segments")
    g = _series(sc["revenueGrowth"], n, "revenueGrowth")
    rev, out = base_revenue, []
    for y in range(n):
        rev *= 1 + g[y]
        out.append(rev)
    return base_revenue, out, None


def value(inp, sc, discount=None, terminal=None, growth_override=None):
    n = _years(sc)
    base_rev, revs, segs = revenues(sc, inp.get("baseRevenue"), n, growth_override)
    margin = _series(sc["ebitMargin"], n, "ebitMargin")
    tax = float(sc["taxRate"])
    da = _series(sc.get("daPctRevenue", 0.0), n, "daPctRevenue")
    capex = _series(sc["capexPctRevenue"], n, "capexPctRevenue")
    nwc = _series(sc.get("nwcPctRevenue", 0.0), n, "nwcPctRevenue")
    r = float(sc["discountRate"] if discount is None else discount)
    g = float(sc["terminalGrowth"] if terminal is None else terminal)
    if g >= r:
        raise ValueError(f"terminal growth {g:.3f} must be below the discount rate {r:.3f}")

    rows, pv_sum, prev_rev = [], 0.0, base_rev
    prev_nwc = nwc[0] * base_rev
    for y in range(n):
        ebit = revs[y] * margin[y]
        nwc_level = nwc[y] * revs[y]
        fcf = ebit * (1 - tax) + revs[y] * da[y] - revs[y] * capex[y] - (nwc_level - prev_nwc)
        pv = fcf / (1 + r) ** (y + 1)
        pv_sum += pv
        rows.append({"year": y + 1, "revenue": round(revs[y], 2), "ebit": round(ebit, 2), "fcf": round(fcf, 2), "pv": round(pv, 2)})
        prev_rev, prev_nwc = revs[y], nwc_level
    tv = rows[-1]["fcf"] * (1 + g) / (r - g)
    pv_tv = tv / (1 + r) ** n
    ev = pv_sum + pv_tv
    equity = ev - float(inp.get("netDebt", 0)) - float(inp.get("minorityInterest", 0)) + float(inp.get("nonOperatingAssets", 0))
    per_share = equity / float(inp["shares"])
    return {
        "years": n, "discountRate": r, "terminalGrowth": g,
        "projection": rows, "segments": segs,
        "enterpriseValue": round(ev, 2), "equityValue": round(equity, 2),
        "valuePerShare": round(per_share, 2),
        "terminalShareOfEV": round(pv_tv / ev, 3) if ev else None,
        "_raw": per_share,
    }


def sensitivity(inp, sc):
    r0, g0 = float(sc["discountRate"]), float(sc["terminalGrowth"])
    steps = [-0.01, -0.005, 0.0, 0.005, 0.01]
    rates = [round(r0 + s, 4) for s in steps]
    growths = [round(g0 + s, 4) for s in steps]
    grid = []
    for r in rates:
        row = []
        for g in growths:
            row.append(round(value(inp, sc, r, g)["_raw"], 2) if g < r else None)
        grid.append(row)
    return {"rows_discountRate": rates, "cols_terminalGrowth": growths, "valuePerShare": grid}


def reverse_dcf(inp, sc):
    """Constant annual revenue growth (on total revenue) that makes value per share equal the current price."""
    price = float(inp["currentPrice"])
    base = inp.get("baseRevenue")
    if base is None and sc.get("segments"):
        base = sum(float(s["baseRevenue"]) for s in sc["segments"])
    inp2 = dict(inp, baseRevenue=base)

    def f(gr):
        return value(inp2, sc, growth_override=gr)["_raw"] - price

    lo, hi = -0.5, 1.5
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return None
    for _ in range(100):
        mid = (lo + hi) / 2
        fm = f(mid)
        if abs(fm) < 1e-6:
            break
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return round((lo + hi) / 2, 4)


def main(path):
    with open(path) as fh:
        inp = json.load(fh)
    for key in ("currentPrice", "shares", "scenarios"):
        if key not in inp:
            raise ValueError(f"missing {key}")
    price = float(inp["currentPrice"])
    out = {"company": inp.get("company"), "currency": inp.get("currency"), "currentPrice": price, "scenarios": {}}
    for name, sc in inp["scenarios"].items():
        res = value(inp, sc)
        res["upsidePct"] = round((res["_raw"] / price - 1) * 100, 1)
        res.pop("_raw")
        out["scenarios"][name] = res
    base = inp["scenarios"].get("base") or next(iter(inp["scenarios"].values()))
    out["sensitivityBase"] = sensitivity(inp, base)
    out["impliedRevenueGrowth"] = reverse_dcf(inp, base)
    out["notes"] = []
    for name, res in out["scenarios"].items():
        if res["terminalShareOfEV"] and res["terminalShareOfEV"] > 0.75:
            out["notes"].append(f"{name}: terminal value is {res['terminalShareOfEV']:.0%} of enterprise value")
    if out["impliedRevenueGrowth"] is None:
        out["notes"].append("reverse DCF: no growth rate between -50% and 150% matches the current price")
    json.dump(out, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    try:
        main(sys.argv[1])
    except (ValueError, KeyError, TypeError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
