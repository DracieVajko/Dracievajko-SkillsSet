---
name: yfinance-ai
description: "World-class AI-powered Yahoo Finance integration: 56+ tools for stocks, crypto, forex, commodities and ETFs."
version: 3.0.4
author: DracieVajko
tags: [finance, yahoo-finance, stocks, crypto, forex, commodities, etf, python]
category: investing
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/yfinance-ai/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# yfinance-ai

World-class AI-powered Yahoo Finance integration: 56+ tools for stocks, crypto, forex, commodities and ETFs.

## When to Use

- The user needs financial market data: quotes, prices, historical data, financial statements, ratios, dividends/splits, analyst data, earnings calendars, holdings, options, news, market indices, ETF/fund data, bulk operations or peer comparisons.
- Use the `yfinance_ai` Python package rather than copying code.

## Procedure

1. **Install** the package: `pip install "yfinance-ai>=3.0.4"` (or `uv add yfinance-ai`).
2. **Use the `Tools` class** from `yfinance_ai` — do not copy the upstream source code.
3. **Cover the needed data domain** using the appropriate tool: quote/price, historical data, financial statements, ratios, dividends/splits, analyst data, earnings calendar, holdings, options, news, market indices, ETF/fund data, bulk operations, peer comparison.
4. **Return concise, clearly labeled results** with units and timestamps.
5. **Add a disclaimer** — financial data is informational only, not investment advice.

Upstream reference: https://github.com/lucas0/yfinance-ai

## Pitfalls

- Copying thousands of lines of upstream source instead of using the package.
- Presenting financial data as investment advice.
- Missing units or timestamps in results.
- Exceeding API rate limits with bulk operations.

## Verification

- The `Tools` class is imported from `yfinance_ai`, not reimplemented.
- Results include units and timestamps.
- A disclaimer is included with financial data.
- Upstream reference is cited.
